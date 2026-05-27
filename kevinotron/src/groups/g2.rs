// kevinotron/src/groups/g2.rs
// G2 gauge group -- 14-dim exceptional, 7x7 real fundamental rep.
//
// Uses nalgebra for the exact expm (eigendecomposition of A^2)
// and polar decomposition re-projection onto SO(7).

use super::*;
use nalgebra::SMatrix;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

type Mat7 = SMatrix<f64, 7, 7>;

const SIGNED_TRIPLES: [(usize, usize, usize, f64); 7] = [
    (0, 1, 2, 1.0),
    (0, 3, 4, 1.0),
    (0, 5, 6, 1.0),
    (1, 3, 5, 1.0),
    (1, 4, 6, -1.0),
    (2, 3, 6, -1.0),
    (2, 4, 5, -1.0),
];

fn build_structure_constants() -> [[[f64; 7]; 7]; 7] {
    let mut f = [[[0.0f64; 7]; 7]; 7];
    for &(i, j, k, s) in &SIGNED_TRIPLES {
        f[i][j][k] = s;
        f[j][k][i] = s;
        f[k][i][j] = s;
        f[j][i][k] = -s;
        f[k][j][i] = -s;
        f[i][k][j] = -s;
    }
    f
}

fn build_generators() -> Vec<Mat7> {
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
    let n_p = pairs.len(); // 21

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
    assert_eq!(generators.len(), 14, "Expected 14 G2 generators, got {}", generators.len());
    generators
}

/// Exact matrix exponential for 7x7 real antisymmetric A.
/// Uses eigendecomposition of A^2 (symmetric negative semidefinite).
fn expm_antisym_exact(a: &Mat7) -> Mat7 {
    use nalgebra::SymmetricEigen;
    let a2 = a * a;
    let eigen = SymmetricEigen::new(a2);
    let eigenvalues = &eigen.eigenvalues;
    let eigenvectors = &eigen.eigenvectors;

    let mut result = Mat7::zeros();
    for k in 0..7 {
        let neg_lam2 = eigenvalues[k];
        let lam2 = (-neg_lam2).max(0.0);
        let lam = lam2.sqrt();
        let v = eigenvectors.column(k);

        if lam < 1e-14 {
            for i in 0..7 {
                for j in 0..7 {
                    result[(i, j)] += v[i] * v[j];
                }
            }
        } else {
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

/// Polar decomposition re-projection onto SO(7).
/// Newton iteration: X_{k+1} = 0.5 * (X_k + X_k^{-T})
fn polar_project_so7(u: &Mat7) -> Mat7 {
    let mut x = *u;
    for _ in 0..8 {
        let xt = x.transpose();
        match xt.try_inverse() {
            Some(xt_inv) => {
                let x_new = (x + xt_inv) * 0.5;
                let diff = (x_new - x).norm();
                x = x_new;
                if diff < 1e-14 {
                    break;
                }
            }
            None => return *u,
        }
    }
    if x.determinant() < 0.0 {
        for i in 0..7 {
            x[(i, 0)] = -x[(i, 0)];
        }
    }
    x
}

pub struct G2Group {
    generators: Vec<Mat7>,
}

impl G2Group {
    pub fn new() -> Self {
        G2Group {
            generators: build_generators(),
        }
    }

    fn mat7_to_flat(m: &Mat7) -> LinkData {
        let mut v = vec![0.0f64; 49];
        for i in 0..7 {
            for j in 0..7 {
                v[i * 7 + j] = m[(i, j)];
            }
        }
        v
    }

    fn flat_to_mat7(data: &[f64]) -> Mat7 {
        let mut m = Mat7::zeros();
        for i in 0..7 {
            for j in 0..7 {
                m[(i, j)] = data[i * 7 + j];
            }
        }
        m
    }
}

impl GaugeGroup for G2Group {
    fn name(&self) -> &str { "G2" }
    fn dim_fund(&self) -> usize { 7 }
    fn dim_adj(&self) -> usize { 14 }
    fn is_complex(&self) -> bool { false }
    fn beta_norm(&self) -> f64 { 7.0 }

    fn identity(&self) -> LinkData {
        rmat_identity(7)
    }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let mut x = Mat7::zeros();
        for g in &self.generators {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            x += g * c;
        }
        Self::mat7_to_flat(&expm_antisym_exact(&x))
    }

    fn dagger(&self, u: &[f64]) -> LinkData {
        rmat_transpose(u, 7)
    }

    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData {
        rmat_mul(a, b, 7)
    }

    fn trace_re(&self, u: &[f64]) -> f64 {
        rmat_trace(u, 7)
    }

    fn add(&self, a: &[f64], b: &[f64]) -> LinkData {
        rmat_add(a, b)
    }

    fn zero(&self) -> LinkData {
        rmat_zero(7)
    }

    fn reproject(&self, u: &[f64]) -> LinkData {
        let m = Self::flat_to_mat7(u);
        Self::mat7_to_flat(&polar_project_so7(&m))
    }
}
