// G_2 Lattice Gauge Theory -- Metropolis Monte Carlo (Rust)
//
// G_2 = Aut(O) is the 14-dimensional exceptional Lie group, embedded in SO(7).
// Lattice links are 7x7 real orthogonal matrices in the G_2 subgroup.
//
// Implementation follows:
// - Bruno-Caselle-Panero-Pellegrini (arXiv:1409.8305, JHEP 2015)
// - Holland-Pepe-Wiese (hep-lat/0302023)
//
// Port from Python/NumPy version by Kevin Remondiere.

use clap::Parser;
use nalgebra::{DMatrix, DVector, SMatrix, SVector};
use rand::Rng;
use rand_distr::StandardNormal;
use std::time::Instant;

// 7x7 real matrix type
type Mat7 = SMatrix<f64, 7, 7>;
type Vec7 = SVector<f64, 7>;

const DIM: usize = 7;
const NDIM: usize = 4; // spacetime dimensions
const NUM_GENERATORS: usize = 14;

// ============================================================
// G_2 Lie algebra generators in the 7-dim fundamental rep
// ============================================================

/// Build the 14 generators of g_2 in so(7) via SVD null space of the
/// Bryant associative 3-form constraint system.
///
/// phi = e^{123} + e^{145} + e^{167} + e^{246} - e^{257} - e^{347} - e^{356}
fn build_g2_generators() -> [Mat7; NUM_GENERATORS] {
    // Signed Fano triples (1-indexed, with orientation sign)
    let signed_triples: [(usize, usize, usize, f64); 7] = [
        (1, 2, 3, 1.0),
        (1, 4, 5, 1.0),
        (1, 6, 7, 1.0),
        (2, 4, 6, 1.0),
        (2, 5, 7, -1.0),
        (3, 4, 7, -1.0),
        (3, 5, 6, -1.0),
    ];

    // Build structure constants f_{ijk} (0-indexed)
    let mut f = [[[0.0f64; 7]; 7]; 7];
    for &(i, j, k, sign) in &signed_triples {
        let (i0, j0, k0) = (i - 1, j - 1, k - 1);
        f[i0][j0][k0] = sign;
        f[j0][k0][i0] = sign;
        f[k0][i0][j0] = sign;
        f[j0][i0][k0] = -sign;
        f[k0][j0][i0] = -sign;
        f[i0][k0][j0] = -sign;
    }

    // so(7) basis: pairs (p,q) with p < q, 21 total
    let mut so7_pairs: Vec<(usize, usize)> = Vec::with_capacity(21);
    for p in 0..7 {
        for q in (p + 1)..7 {
            so7_pairs.push((p, q));
        }
    }

    // All triples (i,j,k) with i < j < k, 35 total
    let mut triples: Vec<(usize, usize, usize)> = Vec::with_capacity(35);
    for i in 0..7 {
        for j in (i + 1)..7 {
            for k in (j + 1)..7 {
                triples.push((i, j, k));
            }
        }
    }

    // Build the 35x21 constraint matrix M
    // Constraint: (L_D phi)(i,j,k) = 0
    let nrows = triples.len(); // 35
    let ncols = so7_pairs.len(); // 21
    let mut m_data = DMatrix::<f64>::zeros(nrows, ncols);

    for (t_idx, &(i, j, k)) in triples.iter().enumerate() {
        for (g_idx, &(p, q)) in so7_pairs.iter().enumerate() {
            let mut val = 0.0;
            if i == p {
                val += f[q][j][k];
            }
            if i == q {
                val -= f[p][j][k];
            }
            if j == p {
                val += f[i][q][k];
            }
            if j == q {
                val -= f[i][p][k];
            }
            if k == p {
                val += f[i][j][q];
            }
            if k == q {
                val -= f[i][j][p];
            }
            m_data[(t_idx, g_idx)] = val;
        }
    }

    // SVD to find null space
    let svd = m_data.svd(true, true);
    let s_vals = &svd.singular_values;

    // Count null dimensions (singular values < 1e-10)
    let mut null_dim = 0;
    for i in 0..s_vals.len() {
        if s_vals[i] < 1e-10 {
            null_dim += 1;
        }
    }
    assert_eq!(
        null_dim, NUM_GENERATORS,
        "Expected 14 g_2 generators, got {}",
        null_dim
    );

    // Extract null space from V^T (last null_dim rows)
    let vt = svd.v_t.as_ref().unwrap();
    let mut generators = [Mat7::zeros(); NUM_GENERATORS];

    for gen_idx in 0..NUM_GENERATORS {
        let row_idx = ncols - NUM_GENERATORS + gen_idx;
        let mut g = Mat7::zeros();
        for (pair_idx, &(p, q)) in so7_pairs.iter().enumerate() {
            let val = vt[(row_idx, pair_idx)];
            g[(p, q)] = val;
            g[(q, p)] = -val;
        }

        // Normalize: Tr(T_a T_b) = -2 delta_{ab}
        let norm_sq = -(g * g).trace();
        if norm_sq > 1e-20 {
            let scale = (2.0f64).sqrt() / norm_sq.sqrt();
            g *= scale;
        }
        generators[gen_idx] = g;
    }

    generators
}

// ============================================================
// Matrix exponential for antisymmetric 7x7
// ============================================================

/// Exact matrix exponential for a 7x7 antisymmetric matrix.
///
/// Since A is real antisymmetric, iA is Hermitian. We use eigendecomposition
/// of iA (real symmetric after converting) to compute exp(A) exactly.
///
/// For a real antisymmetric A, eigenvalues of A are purely imaginary: +/- i*theta_k and 0.
/// We compute via: form A^2 (symmetric negative semidefinite), eigendecompose,
/// then reconstruct exp(A) = V * diag(cos(theta_k)) * V^T + V * (sin(theta_k)/theta_k * A) terms.
///
/// Alternatively (and more robustly), use the Rodrigues-like approach:
/// exp(A) can be computed from the eigendecomposition of A*A (which is symmetric).
fn expm_antisym7(a: &Mat7) -> Mat7 {
    // A is antisymmetric. A^2 is symmetric negative semidefinite.
    // Eigenvalues of A^2 are -theta_k^2.
    // exp(A) = I + sin(theta)/theta * A + (1-cos(theta))/theta^2 * A^2
    // but this only works for simple cases. For general antisymmetric, we need
    // the full spectral approach.

    // Use nalgebra's eigendecomposition on A*A (symmetric)
    let a_sq = a * a;

    // a_sq is symmetric, eigendecompose it
    let eigen = nalgebra::SymmetricEigen::new(a_sq);
    let eigenvalues = &eigen.eigenvalues;
    let eigenvectors = &eigen.eigenvectors;

    // eigenvalues of A^2 are -theta_k^2 (non-positive)
    // We need to find the rotation angles theta_k
    // For each eigenvalue lambda = -theta^2, theta = sqrt(-lambda)

    // Group eigenvalues into pairs (+/- i*theta) and zeros
    // For 7x7, we have at most 3 pairs + 1 zero

    // Direct approach: use spectral decomposition
    // exp(A) = sum_k exp(i*theta_k) * P_k where P_k are spectral projectors
    // For real antisymmetric: eigenvalues come in conjugate pairs +/- i*theta
    // The result is real.

    // Simpler robust approach: compute the series via Pade or use the eigendecomposition
    // of the complexified matrix.

    // We'll use the approach from the Python code: eigendecompose i*A (Hermitian),
    // get real eigenvalues, then exp(-i * eigenvalues) and reconstruct.

    // i*A is Hermitian (since A is real antisymmetric, (iA)^* = -iA^T = iA)
    // But nalgebra doesn't have complex eigendecomposition built-in for SMatrix.
    // Instead, we use the A^2 approach with careful handling.

    // Build exp(A) via spectral projectors of A^2:
    // A^2 has eigenvalues -theta_k^2 with eigenvectors v_k
    // For each pair (theta, -theta), the 2D eigenspace of A^2 for eigenvalue -theta^2
    // splits into A-eigenspaces for +i*theta and -i*theta.

    // Practical approach: diagonalize A^2, then for each eigenspace compute
    // cos(theta)*P + sin(theta)/theta * A*P where P is the projector.

    // Collect unique |theta| values and their eigenspaces
    let n = 7;
    let mut result = Mat7::zeros();

    // For each eigenvector v_k of A^2 with eigenvalue lambda_k = -theta_k^2:
    // The contribution to exp(A) in direction v_k is:
    //   cos(theta_k) * v_k * v_k^T + sin(theta_k)/theta_k * (A * v_k) * v_k^T
    // (when eigenvalues are simple)

    // But eigenvectors may cluster. Let's handle it properly.
    // For the zero eigenvalue: exp(A) acts as identity on that subspace.
    // For eigenvalue -theta^2: the 2D plane gets rotation by theta.

    // Since A^2 is symmetric with eigenvalues in pairs for the non-zero eigenvalues,
    // we process each eigenvector individually.

    for k in 0..n {
        let lambda_k = eigenvalues[k]; // -theta_k^2
        let v_k: Vec7 = eigenvectors.column(k).into();

        if lambda_k.abs() < 1e-30 {
            // Zero eigenvalue: exp(A) * v = v
            result += v_k * v_k.transpose();
        } else {
            let theta_k = (-lambda_k).sqrt();
            // cos(theta) * |v><v| + sin(theta)/theta * A|v><v|
            let a_v = a * v_k;
            result += theta_k.cos() * (v_k * v_k.transpose())
                + theta_k.sin() / theta_k * (a_v * v_k.transpose());
        }
    }

    result
}

// ============================================================
// G_2 group element operations
// ============================================================

/// Generate a random G_2 element near identity.
fn random_g2_near_identity(
    generators: &[Mat7; NUM_GENERATORS],
    epsilon: f64,
    rng: &mut impl Rng,
) -> Mat7 {
    let mut x = Mat7::zeros();
    for t in generators.iter() {
        let c: f64 = rng.sample::<f64, _>(StandardNormal) * epsilon;
        x += c * t;
    }
    expm_antisym7(&x)
}

/// Generate a random G_2 element by composing many small steps (for hot start).
fn random_g2_full(generators: &[Mat7; NUM_GENERATORS], rng: &mut impl Rng) -> Mat7 {
    let mut u = Mat7::identity();
    for _ in 0..20 {
        u = u * random_g2_near_identity(generators, 0.5, rng);
    }
    u
}

// ============================================================
// 4D Lattice
// ============================================================

/// Flat index for a lattice site (x0, x1, x2, x3) on an L^4 lattice.
#[inline]
fn site_index(x: [usize; NDIM], l: usize) -> usize {
    x[0] * l * l * l + x[1] * l * l + x[2] * l + x[3]
}

/// Flat index for a link: site_index * NDIM + mu
#[inline]
fn link_index(x: [usize; NDIM], mu: usize, l: usize) -> usize {
    site_index(x, l) * NDIM + mu
}

/// Shift site by +1 in direction mu with periodic BC.
#[inline]
fn shift_plus(x: [usize; NDIM], mu: usize, l: usize) -> [usize; NDIM] {
    let mut y = x;
    y[mu] = (y[mu] + 1) % l;
    y
}

/// Shift site by -1 in direction mu with periodic BC.
#[inline]
fn shift_minus(x: [usize; NDIM], mu: usize, l: usize) -> [usize; NDIM] {
    let mut y = x;
    y[mu] = (y[mu] + l - 1) % l;
    y
}

struct G2Lattice {
    l: usize,
    beta: f64,
    generators: [Mat7; NUM_GENERATORS],
    /// links[site_index * NDIM + mu] = U_mu(x), stored as flat Vec
    links: Vec<Mat7>,
}

impl G2Lattice {
    fn new(l: usize, beta: f64) -> Self {
        let generators = build_g2_generators();
        let n_links = l * l * l * l * NDIM;

        // Cold start: all links = identity
        let links = vec![Mat7::identity(); n_links];

        G2Lattice {
            l,
            beta,
            generators,
            links,
        }
    }

    fn hot_start(&mut self, rng: &mut impl Rng) {
        for link in self.links.iter_mut() {
            *link = random_g2_full(&self.generators, rng);
        }
    }

    #[inline]
    fn get_link(&self, x: [usize; NDIM], mu: usize) -> &Mat7 {
        &self.links[link_index(x, mu, self.l)]
    }

    #[inline]
    fn set_link(&mut self, x: [usize; NDIM], mu: usize, u: Mat7) {
        self.links[link_index(x, mu, self.l)] = u;
    }

    /// Compute the sum of 6 staples around the link U_mu(site).
    fn staple_sum(&self, site: [usize; NDIM], mu: usize) -> Mat7 {
        let l = self.l;
        let mut s = Mat7::zeros();

        for nu in 0..NDIM {
            if nu == mu {
                continue;
            }
            // Forward staple: U_nu(x+mu) * U_mu(x+nu)^T * U_nu(x)^T
            let x_mu = shift_plus(site, mu, l);
            let x_nu = shift_plus(site, nu, l);

            let u_nu_xmu = self.get_link(x_mu, nu);
            let u_mu_xnu = self.get_link(x_nu, mu);
            let u_nu_x = self.get_link(site, nu);

            s += u_nu_xmu * u_mu_xnu.transpose() * u_nu_x.transpose();

            // Backward staple: U_nu(x+mu-nu)^T * U_mu(x-nu)^T * U_nu(x-nu)
            let x_mu_mnu = shift_minus(x_mu, nu, l);
            let x_mnu = shift_minus(site, nu, l);

            let u_nu_xmu_mnu = self.get_link(x_mu_mnu, nu);
            let u_mu_xmnu = self.get_link(x_mnu, mu);
            let u_nu_xmnu = self.get_link(x_mnu, nu);

            s += u_nu_xmu_mnu.transpose() * u_mu_xmnu.transpose() * u_nu_xmnu;
        }

        s
    }

    /// Local Wilson action for link U at position (site, mu).
    /// S_local = -(beta/7) * Tr(U * K) where K = staple_sum
    #[inline]
    fn local_action(&self, site: [usize; NDIM], mu: usize, u: &Mat7) -> f64 {
        let k = self.staple_sum(site, mu);
        -(self.beta / 7.0) * (u * k).trace()
    }

    /// Single-link Metropolis update. Returns true if accepted.
    fn metropolis_update(
        &mut self,
        site: [usize; NDIM],
        mu: usize,
        epsilon: f64,
        rng: &mut impl Rng,
    ) -> bool {
        let u_old = *self.get_link(site, mu);

        // Precompute staple sum once (most expensive part)
        let k = self.staple_sum(site, mu);
        let s_old = -(self.beta / 7.0) * (u_old * k).trace();

        // Propose: U_new = R * U_old
        let r = random_g2_near_identity(&self.generators, epsilon, rng);
        let u_new = r * u_old;

        let s_new = -(self.beta / 7.0) * (u_new * k).trace();
        let ds = s_new - s_old;

        if ds < 0.0 || rng.gen::<f64>() < (-ds).exp() {
            self.set_link(site, mu, u_new);
            true
        } else {
            false
        }
    }

    /// One full sweep over all links. Returns acceptance rate.
    fn sweep(&mut self, epsilon: f64, rng: &mut impl Rng) -> f64 {
        let l = self.l;
        let mut accepted: u64 = 0;
        let mut total: u64 = 0;

        for x0 in 0..l {
            for x1 in 0..l {
                for x2 in 0..l {
                    for x3 in 0..l {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..NDIM {
                            if self.metropolis_update(site, mu, epsilon, rng) {
                                accepted += 1;
                            }
                            total += 1;
                        }
                    }
                }
            }
        }

        accepted as f64 / total as f64
    }

    /// Average plaquette: <P> = (1/7) <Re Tr(U_plaq)>
    fn plaquette(&self) -> f64 {
        let l = self.l;
        let mut p_sum = 0.0;
        let mut count: u64 = 0;

        for x0 in 0..l {
            for x1 in 0..l {
                for x2 in 0..l {
                    for x3 in 0..l {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..NDIM {
                            for nu in (mu + 1)..NDIM {
                                let x_mu = shift_plus(site, mu, l);
                                let x_nu = shift_plus(site, nu, l);

                                let u1 = self.get_link(site, mu);
                                let u2 = self.get_link(x_mu, nu);
                                let u3 = self.get_link(x_nu, mu);
                                let u4 = self.get_link(site, nu);

                                let plaq = u1 * u2 * u3.transpose() * u4.transpose();
                                p_sum += plaq.trace() / 7.0;
                                count += 1;
                            }
                        }
                    }
                }
            }
        }

        p_sum / count as f64
    }

    /// Average Polyakov loop (absolute value) in direction 0.
    fn polyakov_loop(&self) -> f64 {
        let l = self.l;
        let mut p_sum = 0.0;
        let mut count: u64 = 0;

        // Loop over spatial coordinates (directions 1,2,3)
        for x1 in 0..l {
            for x2 in 0..l {
                for x3 in 0..l {
                    let mut u = Mat7::identity();
                    for t in 0..l {
                        let site = [t, x1, x2, x3];
                        u = u * self.get_link(site, 0);
                    }
                    p_sum += (u.trace() / 7.0).abs();
                    count += 1;
                }
            }
        }

        p_sum / count as f64
    }
}

// ============================================================
// CLI
// ============================================================

#[derive(Parser)]
#[command(name = "g2_lattice")]
#[command(about = "G_2 Lattice Gauge Theory Monte Carlo (Metropolis)")]
struct Cli {
    /// Lattice size L (L^4 lattice)
    #[arg(long = "L", default_value_t = 4)]
    l: usize,

    /// Inverse coupling beta = 7/g^2
    #[arg(long, default_value_t = 10.0)]
    beta: f64,

    /// Thermalization sweeps
    #[arg(long = "n-therm", default_value_t = 500)]
    n_therm: usize,

    /// Measurement sweeps
    #[arg(long = "n-meas", default_value_t = 200)]
    n_meas: usize,

    /// Sweeps between measurements
    #[arg(long = "n-skip", default_value_t = 5)]
    n_skip: usize,

    /// Metropolis step size
    #[arg(long, default_value_t = 0.15)]
    epsilon: f64,

    /// Hot start (random links) instead of cold start
    #[arg(long)]
    hot: bool,
}

fn main() {
    let cli = Cli::parse();
    let l = cli.l;
    let beta = cli.beta;

    println!("# G2 Lattice Monte Carlo");
    println!(
        "# L={}, beta={:.4}, n_therm={}, n_meas={}",
        l, beta, cli.n_therm, cli.n_meas
    );
    println!("# beta = 7/g^2 -> g^2 = {:.6}", 7.0 / beta);
    println!("# epsilon = {:.4}", cli.epsilon);
    println!(
        "# start = {}",
        if cli.hot { "hot" } else { "cold" }
    );

    let t0 = Instant::now();

    // Build lattice
    eprintln!("Building G_2 generators (14 = dim g_2 in so(7))...");
    let mut lat = G2Lattice::new(l, beta);
    let mut rng = rand::thread_rng();

    if cli.hot {
        eprintln!("Hot start...");
        lat.hot_start(&mut rng);
    } else {
        eprintln!("Cold start (identity links)...");
    }

    eprintln!("Lattice initialized in {:.2}s", t0.elapsed().as_secs_f64());

    // Sanity check
    let p0 = lat.plaquette();
    eprintln!("Initial <P> = {:.6} (cold: should be 1.0)", p0);

    // Thermalization
    eprintln!(
        "\nThermalization ({} sweeps)...",
        cli.n_therm
    );
    let t_therm = Instant::now();
    for i in 0..cli.n_therm {
        let acc = lat.sweep(cli.epsilon, &mut rng);
        if (i + 1) % 20 == 0 {
            let p = lat.plaquette();
            eprintln!(
                "  sweep {:4}: <P> = {:.6}, acc = {:.3}",
                i + 1,
                p,
                acc
            );
        }
    }
    eprintln!(
        "Thermalization done in {:.1}s",
        t_therm.elapsed().as_secs_f64()
    );

    // Measurement
    eprintln!(
        "\nMeasurement ({} x {} sweeps)...",
        cli.n_meas, cli.n_skip
    );
    let t_meas = Instant::now();
    let mut plaq_values: Vec<f64> = Vec::with_capacity(cli.n_meas);
    let mut poly_values: Vec<f64> = Vec::with_capacity(cli.n_meas);

    for i in 0..cli.n_meas {
        for _ in 0..cli.n_skip {
            lat.sweep(cli.epsilon, &mut rng);
        }
        let p = lat.plaquette();
        let poly = lat.polyakov_loop();
        plaq_values.push(p);
        poly_values.push(poly);

        // Print every measurement to stdout for downstream processing
        println!(
            "sweep {}: P={:.6} acc=0.000 poly={:.6}",
            (cli.n_therm + (i + 1) * cli.n_skip),
            p,
            poly
        );

        if (i + 1) % 10 == 0 {
            eprintln!(
                "  meas {:4}: <P> = {:.6}, |L| = {:.6}",
                i + 1,
                p,
                poly
            );
        }
    }
    eprintln!(
        "Measurement done in {:.1}s",
        t_meas.elapsed().as_secs_f64()
    );

    // Statistics
    let n = plaq_values.len() as f64;
    let p_mean: f64 = plaq_values.iter().sum::<f64>() / n;
    let p_var: f64 = plaq_values.iter().map(|x| (x - p_mean).powi(2)).sum::<f64>() / (n - 1.0);
    let p_err = (p_var / n).sqrt();

    let poly_mean: f64 = poly_values.iter().sum::<f64>() / n;
    let poly_var: f64 = poly_values
        .iter()
        .map(|x| (x - poly_mean).powi(2))
        .sum::<f64>()
        / (n - 1.0);
    let poly_err = (poly_var / n).sqrt();

    println!(
        "RESULT: P={:.4} +/- {:.4} poly={:.4} +/- {:.4}",
        p_mean, p_err, poly_mean, poly_err
    );

    let total_time = t0.elapsed().as_secs_f64();
    let total_sweeps = cli.n_therm + cli.n_meas * cli.n_skip;
    eprintln!("\nTotal time: {:.1}s ({:.3}s/sweep)", total_time, total_time / total_sweeps as f64);
}
