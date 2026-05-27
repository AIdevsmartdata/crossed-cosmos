use nalgebra::SMatrix;
use rand::Rng;
use rand_distr::StandardNormal;
use clap::Parser;
use std::time::Instant;

type Mat7 = SMatrix<f64, 7, 7>;

const SIGNED_TRIPLES: [(usize, usize, usize, f64); 7] = [
    (0, 1, 2, 1.0), (0, 3, 4, 1.0), (0, 5, 6, 1.0), (1, 3, 5, 1.0),
    (1, 4, 6, -1.0), (2, 3, 6, -1.0), (2, 4, 5, -1.0),
];

fn build_structure_constants() -> [[[f64; 7]; 7]; 7] {
    let mut f = [[[0.0f64; 7]; 7]; 7];
    for &(i, j, k, s) in &SIGNED_TRIPLES {
        f[i][j][k] = s; f[j][k][i] = s; f[k][i][j] = s;
        f[j][i][k] = -s; f[k][j][i] = -s; f[i][k][j] = -s;
    }
    f
}

fn build_g2_generators() -> Vec<Mat7> {
    let f = build_structure_constants();
    let mut triples = Vec::new();
    for i in 0..7 { for j in (i+1)..7 { for k in (j+1)..7 { triples.push((i, j, k)); } } }
    let mut pairs = Vec::new();
    for p in 0..7 { for q in (p+1)..7 { pairs.push((p, q)); } }
    let n_t = triples.len();
    let n_p = pairs.len();
    let mut m_data = vec![0.0f64; n_t * n_p];
    for (t_idx, &(i, j, k)) in triples.iter().enumerate() {
        for (g_idx, &(p, q)) in pairs.iter().enumerate() {
            let mut val = 0.0;
            if i == p { val += f[q][j][k]; } if i == q { val -= f[p][j][k]; }
            if j == p { val += f[i][q][k]; } if j == q { val -= f[i][p][k]; }
            if k == p { val += f[i][j][q]; } if k == q { val -= f[i][j][p]; }
            m_data[t_idx * n_p + g_idx] = val;
        }
    }
    let m_mat = nalgebra::DMatrix::from_row_slice(n_t, n_p, &m_data);
    let svd = m_mat.svd(false, true);
    let v_t = svd.v_t.unwrap();
    let singular = &svd.singular_values;
    let mut generators = Vec::new();
    for row in 0..n_p {
        if singular[row] < 1e-10 {
            let mut g = Mat7::zeros();
            for (idx, &(p, q)) in pairs.iter().enumerate() {
                let val = v_t[(row, idx)];
                g[(p, q)] = val; g[(q, p)] = -val;
            }
            let norm = (-g.dot(&g)).sqrt();
            if norm > 1e-10 { g *= (2.0f64).sqrt() / norm; }
            generators.push(g);
        }
    }
    assert_eq!(generators.len(), 14);
    generators
}

fn expm_antisym(a: &Mat7) -> Mat7 {
    let a2 = a * a;
    let a3 = &a2 * a;
    let a4 = &a2 * &a2;
    let a5 = &a4 * a;
    let a6 = &a4 * &a2;
    let a7 = &a6 * a;
    Mat7::identity() + a + &a2 * 0.5
        + &a3 * (1.0/6.0) + &a4 * (1.0/24.0)
        + &a5 * (1.0/120.0) + &a6 * (1.0/720.0) + &a7 * (1.0/5040.0)
}

fn random_g2_element(gens: &[Mat7], epsilon: f64, rng: &mut impl Rng) -> Mat7 {
    let mut x = Mat7::zeros();
    for g in gens { x += g * (rng.sample::<f64, _>(StandardNormal) * epsilon); }
    expm_antisym(&x)
}

struct G2LatticeEE {
    ls: usize,       // spatial size
    lt: usize,       // temporal size
    beta: f64,
    generators: Vec<Mat7>,
    links: Vec<Mat7>,
}

impl G2LatticeEE {
    fn new(ls: usize, lt: usize, beta: f64) -> Self {
        let generators = build_g2_generators();
        let n_links = ls * ls * ls * lt * 4;
        let links = vec![Mat7::identity(); n_links];
        G2LatticeEE { ls, lt, beta, generators, links }
    }

    #[inline]
    fn size(&self, d: usize) -> usize {
        if d < 3 { self.ls } else { self.lt }
    }

    #[inline]
    fn idx(&self, s: [usize; 4], mu: usize) -> usize {
        ((s[0] * self.ls + s[1]) * self.ls + s[2]) * self.lt * 4 + s[3] * 4 + mu
    }

    #[inline]
    fn shift(&self, s: [usize; 4], mu: usize, dir: i32) -> [usize; 4] {
        let mut r = s;
        let sz = self.size(mu);
        r[mu] = ((r[mu] as i32 + dir).rem_euclid(sz as i32)) as usize;
        r
    }

    fn get(&self, s: [usize; 4], mu: usize) -> &Mat7 { &self.links[self.idx(s, mu)] }

    fn set(&mut self, s: [usize; 4], mu: usize, u: Mat7) {
        let i = self.idx(s, mu); self.links[i] = u;
    }

    fn staple_sum(&self, site: [usize; 4], mu: usize) -> Mat7 {
        let mut s = Mat7::zeros();
        for nu in 0..4 {
            if nu == mu { continue; }
            let x_mu = self.shift(site, mu, 1);
            let x_nu = self.shift(site, nu, 1);
            s += self.get(x_mu, nu) * self.get(x_nu, mu).transpose() * self.get(site, nu).transpose();
            let x_mu_mnu = self.shift(x_mu, nu, -1);
            let x_mnu = self.shift(site, nu, -1);
            s += self.get(x_mu_mnu, nu).transpose() * self.get(x_mnu, mu).transpose() * self.get(x_mnu, nu);
        }
        s
    }

    fn is_boundary(&self, site: [usize; 4], mu: usize) -> bool {
        mu == 0 && site[0] == self.ls / 2 - 1
    }

    fn local_action_alpha(&self, site: [usize; 4], mu: usize, u: &Mat7, alpha: f64) -> f64 {
        let k = self.staple_sum(site, mu);
        let base = -(self.beta / 7.0) * (u * k).trace();
        if self.is_boundary(site, mu) { (1.0 - alpha) * base } else { base }
    }

    fn sweep_alpha(&mut self, alpha: f64, epsilon: f64, rng: &mut impl Rng) -> f64 {
        let ls = self.ls; let lt = self.lt;
        let mut acc = 0u64; let mut tot = 0u64;
        for x0 in 0..ls { for x1 in 0..ls { for x2 in 0..ls { for x3 in 0..lt {
            let site = [x0, x1, x2, x3];
            for mu in 0..4 {
                let u_old = *self.get(site, mu);
                let s_old = self.local_action_alpha(site, mu, &u_old, alpha);
                let r = random_g2_element(&self.generators, epsilon, rng);
                let u_new = r * u_old;
                let s_new = self.local_action_alpha(site, mu, &u_new, alpha);
                let ds = s_new - s_old;
                if ds < 0.0 || rng.gen::<f64>() < (-ds).exp() {
                    self.set(site, mu, u_new); acc += 1;
                }
                tot += 1;
            }
        }}}}
        acc as f64 / tot as f64
    }

    fn measure_dS_dalpha(&self, alpha: f64) -> f64 {
        let ls = self.ls; let lt = self.lt;
        let mut ds = 0.0;
        for x1 in 0..ls { for x2 in 0..ls { for x3 in 0..lt {
            let site = [ls/2 - 1, x1, x2, x3];
            let u = self.get(site, 0);
            let k = self.staple_sum(site, 0);
            let base = -(self.beta / 7.0) * (u * k).trace();
            ds += base;
        }}}
        // d/dalpha [(1-alpha)*base] = -base
        -ds
    }

    fn plaquette(&self) -> f64 {
        let ls = self.ls; let lt = self.lt;
        let mut p = 0.0; let mut c = 0u64;
        for x0 in 0..ls { for x1 in 0..ls { for x2 in 0..ls { for x3 in 0..lt {
            let site = [x0, x1, x2, x3];
            for mu in 0..4 { for nu in (mu+1)..4 {
                let x_mu = self.shift(site, mu, 1);
                let x_nu = self.shift(site, nu, 1);
                let plaq = self.get(site, mu) * self.get(x_mu, nu)
                    * self.get(x_nu, mu).transpose() * self.get(site, nu).transpose();
                p += plaq.trace() / 7.0; c += 1;
            }}
        }}}}
        p / c as f64
    }
}

#[derive(Parser)]
#[command(name = "g2_ee", about = "G_2 Entanglement Entropy — Replica Trick")]
struct Args {
    #[arg(long, default_value = "8")]
    ls: usize,
    #[arg(long, default_value = "0")]
    lt: usize,
    #[arg(long, default_value = "10.0")]
    beta: f64,
    #[arg(long, default_value = "11")]
    n_alpha: usize,
    #[arg(long, default_value = "500")]
    n_therm: usize,
    #[arg(long, default_value = "200")]
    n_meas: usize,
    #[arg(long, default_value = "5")]
    n_skip: usize,
    #[arg(long, default_value = "0.15")]
    epsilon: f64,
}

fn main() {
    let args = Args::parse();
    let lt = if args.lt == 0 { 2 * args.ls } else { args.lt };
    let mut rng = rand::thread_rng();

    println!("# G2 Entanglement Entropy — Replica Trick");
    println!("# Ls={}, Lt={}, beta={}", args.ls, lt, args.beta);
    println!("# n_alpha={}, n_therm={}, n_meas={}, n_skip={}", args.n_alpha, args.n_therm, args.n_meas, args.n_skip);

    let t0 = Instant::now();

    let n_alpha = args.n_alpha;
    let mut alphas = Vec::with_capacity(n_alpha);
    let mut ds_means = Vec::with_capacity(n_alpha);
    let mut ds_errs = Vec::with_capacity(n_alpha);

    for i in 0..n_alpha {
        let alpha = i as f64 / (n_alpha - 1) as f64;
        alphas.push(alpha);

        println!("\n# --- alpha={:.3} ({}/{}) ---", alpha, i+1, n_alpha);
        let mut lat = G2LatticeEE::new(args.ls, lt, args.beta);

        // Thermalization
        for s in 0..args.n_therm {
            lat.sweep_alpha(alpha, args.epsilon, &mut rng);
            if (s+1) % 100 == 0 {
                println!("# therm {}: P={:.6}", s+1, lat.plaquette());
            }
        }

        // Measurement
        let mut measurements = Vec::with_capacity(args.n_meas);
        for m in 0..args.n_meas {
            for _ in 0..args.n_skip {
                lat.sweep_alpha(alpha, args.epsilon, &mut rng);
            }
            let val = lat.measure_dS_dalpha(alpha);
            measurements.push(val);
        }

        let mean: f64 = measurements.iter().sum::<f64>() / measurements.len() as f64;
        let var: f64 = measurements.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / measurements.len() as f64;
        let err = (var / measurements.len() as f64).sqrt();

        ds_means.push(mean);
        ds_errs.push(err);
        println!("ALPHA {:.3}: dS/dalpha = {:.6} +/- {:.6}", alpha, mean, err);
    }

    // Trapezoidal integration
    let mut s2 = 0.0;
    let mut s2_err_sq = 0.0;
    for i in 0..(n_alpha - 1) {
        let da = alphas[i+1] - alphas[i];
        s2 += da * 0.5 * (ds_means[i] + ds_means[i+1]);
        s2_err_sq += (da * 0.5).powi(2) * (ds_errs[i].powi(2) + ds_errs[i+1].powi(2));
    }
    let s2_err = s2_err_sq.sqrt();

    let area = (args.ls as f64).powi(2) * lt as f64;
    let n_bdy = args.ls * args.ls * lt;

    println!("\n# ============================");
    println!("# RESULTS: G2 EE Replica");
    println!("# ============================");
    println!("RESULT: S2={:.6} +/- {:.6}", s2, s2_err);
    println!("RESULT: S2/area={:.6} +/- {:.6}", s2 / area, s2_err / area);
    println!("RESULT: n_boundary_links={}", n_bdy);
    println!("RESULT: area={:.0}", area);

    println!("\n# Predictions:");
    println!("#   (1-1/N^2)*zeta(3)/sqrt(pi), N=3 : kappa = 0.603");
    println!("#   (1-1/dim)*zeta(3)/sqrt(pi), dim=14: kappa = 0.630");
    println!("#   0.518*sqrt(rank)-0.458, rank=2    : kappa = 0.275");
    println!("#   kappa_FP = 1/12                   : kappa = 0.083");

    let total = t0.elapsed().as_secs_f64();
    println!("# Total time: {:.1}s = {:.1}h", total, total / 3600.0);
}
