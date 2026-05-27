// solver.rs — Conjugate Gradient solver for D†D x = b
//
// For Wilson-Dirac: D†D is Hermitian positive definite (for m > 0),
// so CG converges. D itself is not Hermitian but γ₅-Hermitian.
//
// CG solves: A x = b where A = D†D (apply D then D†)
// Convergence: ||r||² / ||b||² < tol²

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;
use crate::fermion::{apply_wilson_dirac, apply_gamma5};

/// Complex inner product <a, b> = Σ a_i * b_i (real vectors, no conjugation needed
/// since we store real/imag interleaved and both a,b are real-valued flat vectors)
fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn norm2(a: &[f64]) -> f64 {
    dot(a, a)
}

/// Apply D†D to a vector: D† = γ₅ D γ₅ (γ₅-hermiticity)
/// So D†D ψ = γ₅ D γ₅ D ψ
fn apply_ddag_d(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    mass: f64,
    psi: &[f64],
) -> Vec<f64> {
    let d = group.dim_fund();
    let d_psi = apply_wilson_dirac(lat, group, mass, psi);
    let g5_d_psi = apply_gamma5(&d_psi, d);
    let d_g5_d_psi = apply_wilson_dirac(lat, group, mass, &g5_d_psi);
    apply_gamma5(&d_g5_d_psi, d)
}

/// Conjugate Gradient solver for D†D x = b
/// Returns (solution, iterations, final_residual)
pub fn cg_solve(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    mass: f64,
    b: &[f64],
    tol: f64,
    max_iter: usize,
) -> (Vec<f64>, usize, f64) {
    let n = b.len();
    let mut x = vec![0.0f64; n];
    let mut r = b.to_vec(); // r = b - A*x = b (since x=0)
    let mut p = r.clone();
    let mut rr = norm2(&r);
    let b_norm2 = norm2(b);

    if b_norm2 < 1e-30 {
        return (x, 0, 0.0);
    }

    for iter in 0..max_iter {
        let ap = apply_ddag_d(lat, group, mass, &p);
        let pap = dot(&p, &ap);

        if pap.abs() < 1e-30 {
            break;
        }

        let alpha = rr / pap;

        // x = x + alpha * p
        for i in 0..n {
            x[i] += alpha * p[i];
        }

        // r = r - alpha * Ap
        for i in 0..n {
            r[i] -= alpha * ap[i];
        }

        let rr_new = norm2(&r);
        let rel_res = (rr_new / b_norm2).sqrt();

        if rel_res < tol {
            return (x, iter + 1, rel_res);
        }

        let beta = rr_new / rr;
        // p = r + beta * p
        for i in 0..n {
            p[i] = r[i] + beta * p[i];
        }

        rr = rr_new;
    }

    let final_res = (norm2(&r) / b_norm2).sqrt();
    (x, max_iter, final_res)
}

/// Solve D x = b using D†D: first solve D†D y = D† b, then x = y
/// (since D†D y = D†b → D (Dy) = D(D†D y) = D(D†b) but simpler: x = D⁻¹b)
/// Actually: solve D†D x = D†b, then Dx = D(D†D)⁻¹ D†b = b ✓
pub fn solve_dirac(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    mass: f64,
    b: &[f64],
    tol: f64,
    max_iter: usize,
) -> (Vec<f64>, usize, f64) {
    let d = group.dim_fund();
    // D†b = γ₅ D γ₅ b
    let g5_b = apply_gamma5(b, d);
    let d_g5_b = apply_wilson_dirac(lat, group, mass, &g5_b);
    let ddag_b = apply_gamma5(&d_g5_b, d);

    cg_solve(lat, group, mass, &ddag_b, tol, max_iter)
}
