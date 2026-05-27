// kevinotron/src/groups/so7.rs
// SO(7) gauge group -- 21-dim orthogonal, 7x7 real fundamental rep.
//
// SO(7) = { U in GL(7,R) : U^T U = I, det(U) = 1 }
// Lie algebra so(7): 7x7 real antisymmetric matrices, dim = 7*6/2 = 21
// Generators: e_ij - e_ji for i < j (antisymmetric basis)
// beta_norm = d_fund = 7  (C_2(adj) = 5)
//
// Uses the same polar decomposition reproject as G2 (which is a subgroup of SO(7)).
// Matrix exponential via eigendecomposition of A^2 (same as G2).
//
// Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)

use super::*;
use nalgebra::SMatrix;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

type Mat7 = SMatrix<f64, 7, 7>;

/// Build 21 generators of so(7): antisymmetric matrices e_ij - e_ji for i < j.
/// Normalized so that Tr(T_a T_b) = -delta_ab / 2.
fn so7_generators() -> Vec<Mat7> {
    let mut gens = Vec::with_capacity(21);
    for i in 0..7 {
        for j in (i + 1)..7 {
            let mut g = Mat7::zeros();
            // e_ij - e_ji: g[i,j] = 1, g[j,i] = -1
            // Tr(g^2) = Tr of matrix with g[i,j]*g[j,i] + g[j,i]*g[i,j] on diagonal
            //         = -2  (since g[i,j]=1, g[j,i]=-1, contribution -1 at [i,i] and -1 at [j,j])
            // We want Tr(T^2) = -1/2, so scale by 1/2
            g[(i, j)] = 0.5;
            g[(j, i)] = -0.5;
            // Check: Tr(g^2) = 2 * (0.5 * (-0.5)) = -0.5 ✓
            gens.push(g);
        }
    }
    assert_eq!(gens.len(), 21, "Expected 21 SO(7) generators, got {}", gens.len());
    gens
}

/// Exact matrix exponential for 7x7 real antisymmetric A.
/// Uses eigendecomposition of A^2 (symmetric negative semidefinite).
/// Same algorithm as G2.
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
            // exp(0) = 1 contribution
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
/// Same algorithm as G2.
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
    // Ensure det = +1
    if x.determinant() < 0.0 {
        for i in 0..7 {
            x[(i, 0)] = -x[(i, 0)];
        }
    }
    x
}

pub struct SO7Group {
    generators: Vec<Mat7>,
}

impl SO7Group {
    pub fn new() -> Self {
        SO7Group {
            generators: so7_generators(),
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

impl GaugeGroup for SO7Group {
    fn name(&self) -> &str { "SO(7)" }
    fn dim_fund(&self) -> usize { 7 }
    fn dim_adj(&self) -> usize { 21 }
    fn is_complex(&self) -> bool { false }
    fn beta_norm(&self) -> f64 { 7.0 } // d_fund = 7

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
