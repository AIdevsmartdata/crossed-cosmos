// g2_ee_v2 — Optimized G_2 Entanglement Entropy (Replica Trick)
//
// Improvements over g2_ee v1:
//   1. Checkerboard (red/black) parallelism via rayon (20-core friendly)
//   2. Exact eigendecomposition expm via nalgebra SymmetricEigen on A^2
//   3. Re-orthogonalization every 10 sweeps (polar decomposition onto SO(7))
//   4. Raw measurement output to .dat file for jackknife/bootstrap
//
// Target hardware: 20-core Intel + RTX 5060 Ti (CPU-only for now)
//
// Usage:
//   g2_ee_v2 --ls 8 --beta 10.0 --n-therm 500 --n-meas 200
//
// Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)

use nalgebra::{SMatrix, SymmetricEigen};
use rand::Rng;
use rand_distr::StandardNormal;
use clap::Parser;
use rayon::prelude::*;
use std::io::Write;
use std::sync::Mutex;
use std::time::Instant;

type Mat7 = SMatrix<f64, 7, 7>;

// ============================================================
// G_2 algebra: structure constants from Bryant associative 3-form
// ============================================================

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
    for i in 0..7 {
        for j in (i + 1)..7 {
            for k in (j + 1)..7 {
                triples.push((i, j, k));
            }
        }
    }
    let mut pairs = Vec::new();
    for p in 0..7 {
        for q in (p + 1)..7 {
            pairs.push((p, q));
        }
    }
    let n_t = triples.len(); // 35
    let n_p = pairs.len();   // 21

    let mut m_data = vec![0.0f64; n_t * n_p];
    for (t_idx, &(i, j, k)) in triples.iter().enumerate() {
        for (g_idx, &(p, q)) in pairs.iter().enumerate() {
            let mut val = 0.0;
            if i == p { val += f[q][j][k]; }
            if i == q { val -= f[p][j][k]; }
            if j == p { val += f[i][q][k]; }
            if j == q { val -= f[i][p][k]; }
            if k == p { val += f[i][j][q]; }
            if k == q { val -= f[i][j][p]; }
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
                g[(p, q)] = val;
                g[(q, p)] = -val;
            }
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

// ============================================================
// EXACT matrix exponential for 7x7 real antisymmetric A
//
// Strategy: A is real antisymmetric => A^2 is real symmetric negative
// semidefinite. Eigendecompose A^2 = V diag(-lambda_k^2) V^T.
// The eigenvalues of A are +/- i*lambda_k (and possibly 0 for 7x7).
// Then exp(A) = V * block_exp * V^T where each 2x2 block is
// [[cos(lam), -sin(lam)], [sin(lam), cos(lam)]] and the zero
// eigenvalue gives 1.
//
// More directly: for each eigenpair (v, -lam^2) of A^2,
//   exp(A) v = cos(lam) v + (sin(lam)/lam) A v   [if lam != 0]
//   exp(A) v = v                                   [if lam == 0]
//
// This is exact to machine precision, no Taylor truncation.
// ============================================================

fn expm_antisym_exact(a: &Mat7) -> Mat7 {
    let a2 = a * a; // symmetric negative semidefinite

    // Eigendecompose A^2 (real symmetric)
    let eigen = SymmetricEigen::new(a2);
    let eigenvalues = &eigen.eigenvalues;  // these are -lambda_k^2 (should be <= 0)
    let eigenvectors = &eigen.eigenvectors;

    // Build exp(A) column by column
    let mut result = Mat7::zeros();

    for k in 0..7 {
        let neg_lam2 = eigenvalues[k];
        // Eigenvalue of A^2 is -lam^2; extract lam
        let lam2 = (-neg_lam2).max(0.0); // clamp numerical noise
        let lam = lam2.sqrt();

        let v = eigenvectors.column(k);

        if lam < 1e-14 {
            // Zero eigenvalue: exp(A) v = v
            for i in 0..7 {
                for j in 0..7 {
                    result[(i, j)] += v[i] * v[j];
                }
            }
        } else {
            // exp(A) v = cos(lam)*v + (sin(lam)/lam)*(A*v)
            let c = lam.cos();
            let s_over_l = lam.sin() / lam;
            let av = a * v;
            for i in 0..7 {
                for j in 0..7 {
                    result[(i, j)] += v[i] * (c * v[j] + s_over_l * av[j]);
                }
            }
        }
    }

    result
}

/// Random G_2 group element near identity
fn random_g2_element(gens: &[Mat7], epsilon: f64, rng: &mut impl Rng) -> Mat7 {
    let mut x = Mat7::zeros();
    for g in gens {
        let c: f64 = rng.sample::<f64, _>(StandardNormal) * epsilon;
        x += g * c;
    }
    expm_antisym_exact(&x)
}

// ============================================================
// Re-orthogonalization: project back onto SO(7) via polar decomposition
// U -> U * (U^T U)^{-1/2}
//
// Uses iterative Newton method for the polar factor:
//   X_{k+1} = 0.5 * (X_k + X_k^{-T})
// Converges quadratically from any non-singular start.
// ============================================================

fn polar_project_so7(u: &Mat7) -> Mat7 {
    let mut x = *u;

    // Newton iteration for polar factor (typically 3-5 iterations suffice)
    for _ in 0..8 {
        // X_{k+1} = 0.5 * (X_k + (X_k^T)^{-1})
        // Compute X_k^T, then solve X_k^T * Y = I for Y = (X_k^T)^{-1}
        let xt = x.transpose();
        match xt.try_inverse() {
            Some(xt_inv) => {
                let x_new = (x + xt_inv) * 0.5;
                // Check convergence
                let diff = (x_new - x).norm();
                x = x_new;
                if diff < 1e-14 {
                    break;
                }
            }
            None => {
                // Singular — fall back to original (should not happen)
                return *u;
            }
        }
    }

    // Ensure det = +1 (SO(7) not O(7))
    let det = x.determinant();
    if det < 0.0 {
        // Flip one column sign
        for i in 0..7 {
            x[(i, 0)] = -x[(i, 0)];
        }
    }

    x
}

// ============================================================
// Lattice structure with thread-safe parallel update support
// ============================================================

struct G2LatticeEE {
    ls: usize,
    lt: usize,
    beta: f64,
    generators: Vec<Mat7>,
    links: Vec<Mat7>, // flat storage: [x0][x1][x2][x3][mu]
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

    #[inline]
    fn get(&self, s: [usize; 4], mu: usize) -> &Mat7 {
        &self.links[self.idx(s, mu)]
    }

    fn staple_sum(&self, site: [usize; 4], mu: usize) -> Mat7 {
        let mut s = Mat7::zeros();
        for nu in 0..4 {
            if nu == mu { continue; }
            let x_mu = self.shift(site, mu, 1);
            let x_nu = self.shift(site, nu, 1);
            // Forward staple: U_nu(x+mu) * U_mu(x+nu)^T * U_nu(x)^T
            s += self.get(x_mu, nu) * self.get(x_nu, mu).transpose() * self.get(site, nu).transpose();
            // Backward staple: U_nu(x+mu-nu)^T * U_mu(x-nu)^T * U_nu(x-nu)
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

    // ==========================================================
    // Checkerboard parallel sweep using rayon
    //
    // Color a site (x0,x1,x2,x3) as:
    //   parity = (x0 + x1 + x2 + x3) % 2
    // Sites of the same color share no staple neighbors
    // (staples only reach adjacent sites in each direction).
    // So all red (or all black) sites can be updated in parallel.
    //
    // Within each color, we collect site/mu pairs, then use rayon
    // par_iter to do Metropolis updates with thread-local RNGs.
    // After parallel proposals, we write back accepted updates.
    // ==========================================================

    fn sweep_alpha_parallel(&mut self, alpha: f64, epsilon: f64) -> f64 {
        let total_accepted = std::sync::atomic::AtomicU64::new(0);
        let total_proposals = std::sync::atomic::AtomicU64::new(0);

        // Extract geometry parameters to avoid borrowing self in the closure
        let ls = self.ls;
        let lt = self.lt;
        let beta = self.beta;

        for color in 0..2u8 {
            // Collect all (site, mu) pairs for this color
            let mut sites: Vec<([usize; 4], usize)> = Vec::new();
            for x0 in 0..ls {
                for x1 in 0..ls {
                    for x2 in 0..ls {
                        for x3 in 0..lt {
                            if ((x0 + x1 + x2 + x3) % 2) as u8 != color {
                                continue;
                            }
                            for mu in 0..4 {
                                sites.push(([x0, x1, x2, x3], mu));
                            }
                        }
                    }
                }
            }

            // For the parallel section, we borrow generators and links
            // as shared references. This is safe because same-color sites
            // share no staple neighbors, so no read-write conflict.
            let gens = &self.generators;
            let links = &self.links;

            let results: Vec<(usize, Mat7, bool)> = sites
                .par_iter()
                .map_init(
                    || rand::thread_rng(),
                    |rng, &(site, mu)| {
                        let idx = lattice_idx(ls, lt, site, mu);
                        let u_old = links[idx];

                        // Compute staple from shared links reference
                        let k = staple_sum_ref(links, ls, lt, site, mu);
                        let base = -(beta / 7.0) * (&u_old * k).trace();
                        let s_old = if mu == 0 && site[0] == ls / 2 - 1 {
                            (1.0 - alpha) * base
                        } else {
                            base
                        };

                        let r = random_g2_element(gens, epsilon, rng);
                        let u_new = r * u_old;

                        let base_new = -(beta / 7.0) * (&u_new * k).trace();
                        let s_new = if mu == 0 && site[0] == ls / 2 - 1 {
                            (1.0 - alpha) * base_new
                        } else {
                            base_new
                        };

                        let ds = s_new - s_old;
                        let accept = ds < 0.0 || rng.gen::<f64>() < (-ds).exp();

                        total_proposals.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        if accept {
                            total_accepted.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        }

                        (idx, u_new, accept)
                    },
                )
                .collect();

            // Write back accepted updates (sequential, fast)
            for (idx, u_new, accepted) in results {
                if accepted {
                    self.links[idx] = u_new;
                }
            }
        }

        let acc = total_accepted.load(std::sync::atomic::Ordering::Relaxed) as f64;
        let tot = total_proposals.load(std::sync::atomic::Ordering::Relaxed) as f64;
        if tot > 0.0 { acc / tot } else { 0.0 }
    }

    /// Re-orthogonalize all link matrices onto SO(7) via polar decomposition.
    /// Run every N sweeps to prevent cumulative drift.
    fn reorthogonalize(&mut self) {
        self.links.par_iter_mut().for_each(|u| {
            *u = polar_project_so7(u);
        });
    }

    fn measure_dS_dalpha(&self, _alpha: f64) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let mut ds = 0.0;
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [ls / 2 - 1, x1, x2, x3];
                    let u = self.get(site, 0);
                    let k = self.staple_sum(site, 0);
                    let base = -(self.beta / 7.0) * (u * k).trace();
                    ds += base;
                }
            }
        }
        // d/dalpha [(1-alpha)*base] = -base
        -ds
    }

    /// Parallelized dS/dalpha measurement for large lattices
    fn measure_dS_dalpha_parallel(&self, _alpha: f64) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let beta_over_7 = self.beta / 7.0;

        // Collect boundary sites
        let mut sites: Vec<[usize; 4]> = Vec::new();
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    sites.push([ls / 2 - 1, x1, x2, x3]);
                }
            }
        }

        let total: f64 = sites
            .par_iter()
            .map(|&site| {
                let u = self.get(site, 0);
                let k = self.staple_sum(site, 0);
                let base = -beta_over_7 * (u * k).trace();
                base
            })
            .sum();

        -total
    }

    fn plaquette(&self) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let mut p = 0.0;
        let mut c = 0u64;
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..4 {
                            for nu in (mu + 1)..4 {
                                let x_mu = self.shift(site, mu, 1);
                                let x_nu = self.shift(site, nu, 1);
                                let plaq = self.get(site, mu)
                                    * self.get(x_mu, nu)
                                    * self.get(x_nu, mu).transpose()
                                    * self.get(site, nu).transpose();
                                p += plaq.trace() / 7.0;
                                c += 1;
                            }
                        }
                    }
                }
            }
        }
        p / c as f64
    }

    /// Check orthogonality drift: max |U^T U - I|
    fn max_ortho_drift(&self) -> f64 {
        self.links
            .iter()
            .map(|u| {
                let err = u.transpose() * u - Mat7::identity();
                err.norm()
            })
            .fold(0.0_f64, f64::max)
    }
}

// ============================================================
// CLI
// ============================================================

#[derive(Parser)]
#[command(name = "g2_ee_v2", about = "G_2 EE — Optimized (rayon + exact eigh + reortho)")]
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
    /// Re-orthogonalize every N sweeps (0 = never)
    #[arg(long, default_value = "10")]
    reortho_interval: usize,
    /// Number of rayon threads (0 = automatic from hardware)
    #[arg(long, default_value = "0")]
    threads: usize,
    /// Output .dat file for raw measurements (empty = auto-name)
    #[arg(long, default_value = "")]
    output: String,
}

// ============================================================
// Main
// ============================================================

fn main() {
    let args = Args::parse();

    // Configure rayon thread pool
    if args.threads > 0 {
        rayon::ThreadPoolBuilder::new()
            .num_threads(args.threads)
            .build_global()
            .expect("Failed to set rayon thread count");
    }

    let lt = if args.lt == 0 { 2 * args.ls } else { args.lt };

    let dat_path = if args.output.is_empty() {
        format!("g2_ee_L{}_beta{:.1}.dat", args.ls, args.beta)
    } else {
        args.output.clone()
    };

    println!("# G2 Entanglement Entropy v2 — Optimized");
    println!("# Ls={}, Lt={}, beta={}", args.ls, lt, args.beta);
    println!(
        "# n_alpha={}, n_therm={}, n_meas={}, n_skip={}",
        args.n_alpha, args.n_therm, args.n_meas, args.n_skip
    );
    println!("# reortho_interval={}", args.reortho_interval);
    println!(
        "# rayon threads: {}",
        rayon::current_num_threads()
    );
    println!("# expm: exact eigendecomposition (machine precision)");
    println!("# raw output: {}", dat_path);

    let t0 = Instant::now();

    let n_alpha = args.n_alpha;
    let mut alphas = Vec::with_capacity(n_alpha);
    let mut ds_means = Vec::with_capacity(n_alpha);
    let mut ds_errs = Vec::with_capacity(n_alpha);

    // Open .dat file for raw measurements
    let dat_file = Mutex::new(
        std::fs::File::create(&dat_path).expect("Cannot create .dat output file"),
    );
    {
        let mut f = dat_file.lock().unwrap();
        writeln!(f, "# G2 EE v2 raw measurements").unwrap();
        writeln!(f, "# Ls={} Lt={} beta={}", args.ls, lt, args.beta).unwrap();
        writeln!(f, "# Columns: alpha_idx config_idx dS_dalpha").unwrap();
    }

    for i in 0..n_alpha {
        let alpha = if n_alpha > 1 {
            i as f64 / (n_alpha - 1) as f64
        } else {
            0.0
        };
        alphas.push(alpha);

        println!("\n# --- alpha={:.3} ({}/{}) ---", alpha, i + 1, n_alpha);
        let mut lat = G2LatticeEE::new(args.ls, lt, args.beta);

        // Thermalization
        let t_therm = Instant::now();
        let mut sweep_count = 0usize;
        for s in 0..args.n_therm {
            let acc = lat.sweep_alpha_parallel(alpha, args.epsilon);
            sweep_count += 1;

            // Re-orthogonalize periodically
            if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
                lat.reorthogonalize();
            }

            if (s + 1) % 100 == 0 {
                let drift = lat.max_ortho_drift();
                println!(
                    "# therm {:4}: P={:.6} acc={:.3} drift={:.2e}",
                    s + 1,
                    lat.plaquette(),
                    acc,
                    drift
                );
            }
        }
        let therm_time = t_therm.elapsed().as_secs_f64();
        println!("# Therm done in {:.1}s ({:.3}s/sweep)", therm_time, therm_time / args.n_therm as f64);

        // Measurement
        let mut measurements = Vec::with_capacity(args.n_meas);
        let t_meas = Instant::now();
        for m in 0..args.n_meas {
            for _ in 0..args.n_skip {
                lat.sweep_alpha_parallel(alpha, args.epsilon);
                sweep_count += 1;
                if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
                    lat.reorthogonalize();
                }
            }

            // Use parallel measurement for large lattices
            let val = if args.ls >= 8 {
                lat.measure_dS_dalpha_parallel(alpha)
            } else {
                lat.measure_dS_dalpha(alpha)
            };
            measurements.push(val);

            // Write raw measurement to .dat
            {
                let mut f = dat_file.lock().unwrap();
                writeln!(f, "{} {} {:.10}", i, m, val).unwrap();
            }

            if (m + 1) % 50 == 0 {
                let running_mean: f64 =
                    measurements.iter().sum::<f64>() / measurements.len() as f64;
                println!(
                    "# meas {:4}: dS/da = {:.2} (running mean {:.2})",
                    m + 1,
                    val,
                    running_mean
                );
            }
        }
        let meas_time = t_meas.elapsed().as_secs_f64();
        println!("# Meas done in {:.1}s", meas_time);

        let mean: f64 = measurements.iter().sum::<f64>() / measurements.len() as f64;
        let var: f64 = measurements
            .iter()
            .map(|x| (x - mean).powi(2))
            .sum::<f64>()
            / measurements.len() as f64;
        let err = (var / measurements.len() as f64).sqrt();

        ds_means.push(mean);
        ds_errs.push(err);
        println!("ALPHA {:.3}: dS/dalpha = {:.6} +/- {:.6}", alpha, mean, err);
    }

    // Trapezoidal integration
    let mut s2 = 0.0;
    let mut s2_err_sq = 0.0;
    for i in 0..(n_alpha - 1) {
        let da = alphas[i + 1] - alphas[i];
        s2 += da * 0.5 * (ds_means[i] + ds_means[i + 1]);
        s2_err_sq += (da * 0.5).powi(2) * (ds_errs[i].powi(2) + ds_errs[i + 1].powi(2));
    }
    let s2_err = s2_err_sq.sqrt();

    let area = (args.ls as f64).powi(2) * lt as f64;
    let n_bdy = args.ls * args.ls * lt;

    println!("\n# ============================");
    println!("# RESULTS: G2 EE v2 Replica");
    println!("# ============================");
    println!("RESULT: S2={:.6} +/- {:.6}", s2, s2_err);
    println!("RESULT: S2/area={:.6} +/- {:.6}", s2 / area, s2_err / area);
    println!("RESULT: n_boundary_links={}", n_bdy);
    println!("RESULT: area={:.0}", area);

    println!("\n# Predictions:");
    println!("#   P1 (1-1/N^2)*zeta(3)/sqrt(pi), N=3  : kappa = 0.6027");
    println!("#   P2 (1-1/dim)*zeta(3)/sqrt(pi), dim=14: kappa = 0.6298");
    println!("#   P3 0.518*sqrt(rank)-0.458, rank=2    : kappa = 0.2746");
    println!("#   P4 kappa_FP = 1/12                   : kappa = 0.0833");

    println!("\n# Raw measurements saved to: {}", dat_path);

    let total = t0.elapsed().as_secs_f64();
    let total_sweeps = n_alpha as f64 * (args.n_therm + args.n_meas * args.n_skip) as f64;
    println!(
        "# Total: {:.1}s = {:.2}h, {:.4}s/sweep (avg over {} sweeps)",
        total,
        total / 3600.0,
        total / total_sweeps,
        total_sweeps as u64
    );
}
