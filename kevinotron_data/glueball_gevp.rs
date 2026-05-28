// observables/glueball_gevp.rs — Multi-operator glueball correlator matrix
//
// GEVP: C(t) v_n(t,t₀) = λ_n(t,t₀) C(t₀) v_n
// Operators: same shape (plaquette) at MULTIPLE APE smearing levels
// This gives different overlaps with ground vs excited states
//
// Output: C_ij(t) matrix for Python GEVP solver

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;
use crate::observables::glueball::{plaquette_timeslice, ape_smear_step};

/// Build N operators by APE smearing at different levels
/// Returns: smeared_lattices[i] = lattice after smear_levels[i] APE steps
pub fn build_smeared_lattices(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    smear_levels: &[usize],
    alpha_smear: f64,
) -> Vec<Lattice4D> {
    let max_level = *smear_levels.iter().max().unwrap();
    let mut current = lat.clone();
    let mut result = Vec::with_capacity(smear_levels.len());
    
    let mut next_level_idx = 0;
    // Check if 0 is in smear_levels
    if smear_levels.contains(&0) {
        result.push(current.clone());
        next_level_idx = 1;
    }
    
    for step in 1..=max_level {
        ape_smear_step(&mut current, group, alpha_smear);
        if next_level_idx < smear_levels.len() && smear_levels[next_level_idx] == step {
            result.push(current.clone());
            next_level_idx += 1;
        }
    }
    result
}

/// Compute cross-correlator matrix C_ij(t) for multiple operators
/// Operators are plaquette at different smearing levels.
/// Returns: matrix[t][i*N+j] = <O_i(t) O_j(0)> - <O_i><O_j>
pub fn correlator_matrix(
    smeared_lats: &[Lattice4D],
    group: &dyn GaugeGroup,
) -> Vec<Vec<f64>> {
    let n_ops = smeared_lats.len();
    let lt = smeared_lats[0].lt;
    
    // Compute O_i(t) for each operator at each timeslice
    let mut o_t: Vec<Vec<f64>> = Vec::with_capacity(n_ops);
    for lat in smeared_lats {
        let mut o = Vec::with_capacity(lt);
        for t in 0..lt {
            o.push(plaquette_timeslice(lat, group, t));
        }
        // Subtract mean
        let mean: f64 = o.iter().sum::<f64>() / lt as f64;
        for v in o.iter_mut() { *v -= mean; }
        o_t.push(o);
    }
    
    // Cross-correlator C_ij(dt) = (1/Lt) sum_t O_i(t) * O_j(t+dt)
    let n_t = lt / 2 + 1;
    let mut corr = vec![vec![0.0f64; n_ops * n_ops]; n_t];
    for dt in 0..n_t {
        for i in 0..n_ops {
            for j in 0..n_ops {
                let mut c = 0.0;
                for t in 0..lt {
                    c += o_t[i][t] * o_t[j][(t + dt) % lt];
                }
                corr[dt][i * n_ops + j] = c / lt as f64;
            }
        }
    }
    corr
}


// ═══════════════════════════════════════════════════════════
// GEVP SOLVER (Rust) — solves C(t) v = λ C(t₀) v
// Method: Cholesky decomposition L L^T = C(t₀), then symmetric eigenvalue
//         of M = L^{-1} C(t) L^{-T}.
// ═══════════════════════════════════════════════════════════

use nalgebra::{DMatrix, DVector, SymmetricEigen};

/// Solve GEVP for all timeslices.
/// Input: corr[t] = flat row-major n×n correlator matrix at time t
/// Returns: eigenvalues[t] = sorted descending (largest = ground state)
pub fn solve_gevp(corr: &[Vec<f64>], n_ops: usize, t0: usize) -> Vec<Vec<f64>> {
    let n_t = corr.len();
    let mut result = vec![vec![0.0f64; n_ops]; n_t];

    // Build C(t0) and symmetrize
    let mut c_t0 = DMatrix::<f64>::zeros(n_ops, n_ops);
    for i in 0..n_ops {
        for j in 0..n_ops {
            c_t0[(i, j)] = 0.5 * (corr[t0][i * n_ops + j] + corr[t0][j * n_ops + i]);
        }
    }

    // Cholesky C(t0) = L L^T (add regularization if needed)
    let cholesky = match c_t0.clone().cholesky() {
        Some(c) => c,
        None => {
            // Regularize
            let mut reg = c_t0.clone();
            for i in 0..n_ops { reg[(i, i)] += 1e-12; }
            match reg.cholesky() {
                Some(c) => c,
                None => {
                    eprintln!("# GEVP: Cholesky failed for t0={}", t0);
                    return result;
                }
            }
        }
    };
    let l = cholesky.l();
    let l_inv = match l.clone().try_inverse() {
        Some(inv) => inv,
        None => {
            eprintln!("# GEVP: L inversion failed");
            return result;
        }
    };

    // For each t, compute M = L^{-1} C(t) L^{-T} and eigenvalues
    for t in 0..n_t {
        let mut c_t = DMatrix::<f64>::zeros(n_ops, n_ops);
        for i in 0..n_ops {
            for j in 0..n_ops {
                c_t[(i, j)] = 0.5 * (corr[t][i * n_ops + j] + corr[t][j * n_ops + i]);
            }
        }
        let m = &l_inv * &c_t * l_inv.transpose();
        // Symmetrize for numerical safety
        let m_sym = (&m + m.transpose()) * 0.5;
        let eigen = SymmetricEigen::new(m_sym);
        let mut evs: Vec<f64> = eigen.eigenvalues.iter().copied().collect();
        evs.sort_by(|a, b| b.partial_cmp(a).unwrap());
        for n in 0..n_ops {
            result[t][n] = evs[n];
        }
    }
    result
}

/// Effective masses: m_n(t) = -log(λ_n(t)/λ_n(t-1))
pub fn effective_masses_gevp(eigenvalues: &[Vec<f64>]) -> Vec<Vec<f64>> {
    let n_t = eigenvalues.len();
    let n_ops = eigenvalues[0].len();
    let mut m_eff = vec![vec![0.0f64; n_ops]; n_t - 1];
    for t in 1..n_t {
        for n in 0..n_ops {
            let l_curr = eigenvalues[t][n];
            let l_prev = eigenvalues[t - 1][n];
            if l_curr > 0.0 && l_prev > 0.0 {
                m_eff[t - 1][n] = -(l_curr / l_prev).ln();
            } else {
                m_eff[t - 1][n] = f64::NAN;
            }
        }
    }
    m_eff
}
