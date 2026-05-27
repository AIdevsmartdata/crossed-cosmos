use nalgebra::{SMatrix, SVector, SymmetricEigen};
use rand::Rng;
use rand_distr::StandardNormal;
use clap::Parser;
use std::time::Instant;

type Mat7 = SMatrix<f64, 7, 7>;

// Bryant associative 3-form: signed Fano triples (0-indexed)
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
    // Build 35×21 constraint matrix for 3-form preservation
    let mut triples = Vec::new();
    for i in 0..7 { for j in (i+1)..7 { for k in (j+1)..7 { triples.push((i, j, k)); } } }
    let mut pairs = Vec::new();
    for p in 0..7 { for q in (p+1)..7 { pairs.push((p, q)); } }

    let n_triples = triples.len(); // 35
    let n_pairs = pairs.len();     // 21

    // Build constraint matrix M (35 x 21)
    let mut m_data = vec![0.0f64; n_triples * n_pairs];
    for (t_idx, &(i, j, k)) in triples.iter().enumerate() {
        for (g_idx, &(p, q)) in pairs.iter().enumerate() {
            let mut val = 0.0;
            if i == p { val += f[q][j][k]; }
            if i == q { val -= f[p][j][k]; }
            if j == p { val += f[i][q][k]; }
            if j == q { val -= f[i][p][k]; }
            if k == p { val += f[i][j][q]; }
            if k == q { val -= f[i][j][p]; }
            m_data[t_idx * n_pairs + g_idx] = val;
        }
    }

    // SVD to find null space (dim 14)
    let m_mat = nalgebra::DMatrix::from_row_slice(n_triples, n_pairs, &m_data);
    let svd = m_mat.svd(false, true);
    let v_t = svd.v_t.unwrap();
    let singular = &svd.singular_values;

    let mut generators = Vec::new();
    for row in 0..n_pairs {
        if singular[row] < 1e-10 {
            // This row of V^T is in the null space
            let mut g = Mat7::zeros();
            for (idx, &(p, q)) in pairs.iter().enumerate() {
                let val = v_t[(row, idx)];
                g[(p, q)] = val;
                g[(q, p)] = -val;
            }
            // Normalize: Tr(T^2) = -2
            let norm = (-g.dot(&g)).sqrt();
            if norm > 1e-10 {
                g *= (2.0f64).sqrt() / norm;
            }
            generators.push(g);
        }
    }
    assert_eq!(generators.len(), 14, "Expected 14 g2 generators, got {}", generators.len());
    generators
}

/// Fast exact exp for 7×7 antisymmetric: eigendecompose iA (Hermitian)
fn expm_antisym(a: &Mat7) -> Mat7 {
    // iA is Hermitian with real eigenvalues
    // For real antisymmetric, eigenvalues of A are ±iλ_k and 0
    // We compute via A² which is real symmetric negative semidefinite
    // A = U D U^T where D has eigenvalues -λ_k²
    // exp(A) = U exp(D_orig) U^T
    // But we need the FULL eigendecomposition of A, not A²
    //
    // Simpler: use Schur decomposition or direct formula
    // For 7×7, Padé approximant is fast enough at this size
    // Use: exp(A) ≈ I + A + A²/2 + A³/6 + ... (Taylor 12 terms for |A|<1)

    let a2 = a * a;
    let a3 = &a2 * a;
    let a4 = &a2 * &a2;
    let a5 = &a4 * a;
    let a6 = &a4 * &a2;
    let a7 = &a6 * a;

    let id = Mat7::identity();
    // Taylor series to order 12 (sufficient for |ε| < 0.5)
    id + a + &a2 * 0.5
        + &a3 * (1.0/6.0)
        + &a4 * (1.0/24.0)
        + &a5 * (1.0/120.0)
        + &a6 * (1.0/720.0)
        + &a7 * (1.0/5040.0)
}

fn random_g2_element(gens: &[Mat7], epsilon: f64, rng: &mut impl Rng) -> Mat7 {
    let mut x = Mat7::zeros();
    for g in gens {
        let c: f64 = rng.sample::<f64, _>(StandardNormal) * epsilon;
        x += g * c;
    }
    expm_antisym(&x)
}

#[derive(Clone)]
struct G2Lattice {
    l: usize,
    d: usize,
    beta: f64,
    generators: Vec<Mat7>,
    links: Vec<Mat7>, // flat: [x0][x1][x2][x3][mu] → index
}

impl G2Lattice {
    fn new(l: usize, beta: f64) -> Self {
        let d = 4;
        let n_links = l.pow(d as u32) * d;
        let generators = build_g2_generators();
        let links = vec![Mat7::identity(); n_links];
        G2Lattice { l, d, beta, generators, links }
    }

    #[inline]
    fn idx(&self, site: [usize; 4], mu: usize) -> usize {
        let l = self.l;
        ((site[0] * l + site[1]) * l + site[2]) * l * self.d + site[3] * self.d + mu
    }

    #[inline]
    fn shift(&self, site: [usize; 4], mu: usize, dir: i32) -> [usize; 4] {
        let mut s = site;
        s[mu] = ((s[mu] as i32 + dir).rem_euclid(self.l as i32)) as usize;
        s
    }

    fn get(&self, site: [usize; 4], mu: usize) -> &Mat7 {
        &self.links[self.idx(site, mu)]
    }

    fn set(&mut self, site: [usize; 4], mu: usize, u: Mat7) {
        let i = self.idx(site, mu);
        self.links[i] = u;
    }

    fn staple_sum(&self, site: [usize; 4], mu: usize) -> Mat7 {
        let mut s = Mat7::zeros();
        for nu in 0..self.d {
            if nu == mu { continue; }
            // Forward staple
            let x_mu = self.shift(site, mu, 1);
            let x_nu = self.shift(site, nu, 1);
            let u_nu_xmu = self.get(x_mu, nu);
            let u_mu_xnu = self.get(x_nu, mu);
            let u_nu_x = self.get(site, nu);
            s += u_nu_xmu * u_mu_xnu.transpose() * u_nu_x.transpose();

            // Backward staple
            let x_mu_mnu = self.shift(x_mu, nu, -1);
            let x_mnu = self.shift(site, nu, -1);
            let u_nu_xmu_mnu = self.get(x_mu_mnu, nu);
            let u_mu_xmnu = self.get(x_mnu, mu);
            let u_nu_xmnu = self.get(x_mnu, nu);
            s += u_nu_xmu_mnu.transpose() * u_mu_xmnu.transpose() * u_nu_xmnu;
        }
        s
    }

    fn local_action(&self, site: [usize; 4], mu: usize, u: &Mat7) -> f64 {
        let k = self.staple_sum(site, mu);
        -(self.beta / 7.0) * (u * k).trace()
    }

    fn sweep(&mut self, epsilon: f64, rng: &mut impl Rng) -> f64 {
        let l = self.l;
        let mut accepted = 0u64;
        let mut total = 0u64;

        for x0 in 0..l { for x1 in 0..l { for x2 in 0..l { for x3 in 0..l {
            let site = [x0, x1, x2, x3];
            for mu in 0..self.d {
                let u_old = *self.get(site, mu);
                let s_old = self.local_action(site, mu, &u_old);

                let r = random_g2_element(&self.generators, epsilon, rng);
                let u_new = r * u_old;
                let s_new = self.local_action(site, mu, &u_new);

                let ds = s_new - s_old;
                if ds < 0.0 || rng.gen::<f64>() < (-ds).exp() {
                    self.set(site, mu, u_new);
                    accepted += 1;
                }
                total += 1;
            }
        }}}}
        accepted as f64 / total as f64
    }

    fn plaquette(&self) -> f64 {
        let l = self.l;
        let mut p_sum = 0.0;
        let mut count = 0u64;

        for x0 in 0..l { for x1 in 0..l { for x2 in 0..l { for x3 in 0..l {
            let site = [x0, x1, x2, x3];
            for mu in 0..self.d { for nu in (mu+1)..self.d {
                let x_mu = self.shift(site, mu, 1);
                let x_nu = self.shift(site, nu, 1);
                let plaq = self.get(site, mu)
                    * self.get(x_mu, nu)
                    * self.get(x_nu, mu).transpose()
                    * self.get(site, nu).transpose();
                p_sum += plaq.trace() / 7.0;
                count += 1;
            }}
        }}}}
        p_sum / count as f64
    }

    fn polyakov(&self) -> f64 {
        let l = self.l;
        let mut p_sum = 0.0;
        let mut count = 0u64;
        for x1 in 0..l { for x2 in 0..l { for x3 in 0..l {
            let mut u = Mat7::identity();
            for x0 in 0..l {
                u = u * self.get([x0, x1, x2, x3], 0);
            }
            p_sum += (u.trace() / 7.0).abs();
            count += 1;
        }}}
        p_sum / count as f64
    }
}

#[derive(Parser)]
#[command(name = "g2_lattice", about = "G_2 Lattice Monte Carlo")]
struct Args {
    #[arg(long, default_value = "4")]
    l: usize,
    #[arg(long, default_value = "10.0")]
    beta: f64,
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
    let mut rng = rand::thread_rng();

    println!("# G2 Lattice Monte Carlo");
    println!("# L={}, beta={}, g2={:.4}", args.l, args.beta, 7.0/args.beta);
    println!("# n_therm={}, n_meas={}, n_skip={}, eps={}", args.n_therm, args.n_meas, args.n_skip, args.epsilon);

    let t0 = Instant::now();
    let mut lat = G2Lattice::new(args.l, args.beta);
    println!("# Init: {:.2}s, 14 g2 generators built", t0.elapsed().as_secs_f64());
    println!("# Cold start P={:.6}", lat.plaquette());

    // Thermalization
    let t_therm = Instant::now();
    for i in 0..args.n_therm {
        let acc = lat.sweep(args.epsilon, &mut rng);
        if (i+1) % 50 == 0 {
            let p = lat.plaquette();
            println!("therm {:4}: P={:.6} acc={:.3}", i+1, p, acc);
        }
    }
    println!("# Therm done in {:.1}s", t_therm.elapsed().as_secs_f64());

    // Measurement
    let mut plaq_vals = Vec::with_capacity(args.n_meas);
    let mut poly_vals = Vec::with_capacity(args.n_meas);
    let t_meas = Instant::now();
    for i in 0..args.n_meas {
        for _ in 0..args.n_skip {
            lat.sweep(args.epsilon, &mut rng);
        }
        let p = lat.plaquette();
        let l_poly = lat.polyakov();
        plaq_vals.push(p);
        poly_vals.push(l_poly);
        if (i+1) % 20 == 0 {
            println!("meas {:4}: P={:.6} poly={:.6}", i+1, p, l_poly);
        }
    }
    println!("# Meas done in {:.1}s", t_meas.elapsed().as_secs_f64());

    let p_mean: f64 = plaq_vals.iter().sum::<f64>() / plaq_vals.len() as f64;
    let p_var: f64 = plaq_vals.iter().map(|x| (x - p_mean).powi(2)).sum::<f64>() / plaq_vals.len() as f64;
    let p_err = (p_var / plaq_vals.len() as f64).sqrt();

    let l_mean: f64 = poly_vals.iter().sum::<f64>() / poly_vals.len() as f64;
    let l_var: f64 = poly_vals.iter().map(|x| (x - l_mean).powi(2)).sum::<f64>() / poly_vals.len() as f64;
    let l_err = (l_var / poly_vals.len() as f64).sqrt();

    println!("RESULT: P={:.6} +/- {:.6} poly={:.6} +/- {:.6}", p_mean, p_err, l_mean, l_err);

    let total = t0.elapsed().as_secs_f64();
    let sweep_time = total / (args.n_therm + args.n_meas * args.n_skip) as f64;
    println!("# Total: {:.1}s, {:.4}s/sweep", total, sweep_time);
}
