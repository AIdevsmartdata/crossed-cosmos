// fermion.rs — Wilson-Dirac operator for lattice fermions
//
// D_W(x,y) = (4+m) δ_{xy} - ½ Σ_μ [(1-γ_μ) U_μ(x) δ_{y,x+μ} + (1+γ_μ) U†_μ(y) δ_{y,x-μ}]
//
// γ-matrices: Euclidean, Hermitian, {γ_μ, γ_ν} = 2δ_{μν}
// γ₅ = γ₀ γ₁ γ₂ γ₃
//
// Spinor: ψ(x) has 4 spinor × d_fund color components per site
// Total vector dimension: N_sites × 4 × d_fund
//
// Property: D† = γ₅ D γ₅ (γ₅-hermiticity)

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

/// Euclidean gamma matrices (chiral/DeGrand-Rossi basis)
/// Each gamma is 4×4 stored as [row][col] complex (re, im)
/// γ_μ Hermitian: γ_μ† = γ_μ
/// {γ_μ, γ_ν} = 2δ_{μν}

// γ₄ (temporal, Gattringer-Lang convention: γ₅ = γ₁γ₂γ₃γ₄ = diag(1,1,-1,-1))
// γ₄ = [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
const GAMMA0: [[f64; 8]; 4] = [
    [0.0,0.0, 0.0,0.0, 1.0,0.0, 0.0,0.0],
    [0.0,0.0, 0.0,0.0, 0.0,0.0, 1.0,0.0],
    [1.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0],
    [0.0,0.0, 1.0,0.0, 0.0,0.0, 0.0,0.0],
];

// γ₁ = [[0,0,0,i],[0,0,i,0],[0,-i,0,0],[-i,0,0,0]]
const GAMMA1: [[f64; 8]; 4] = [
    [0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,1.0],
    [0.0,0.0, 0.0,0.0, 0.0,1.0, 0.0,0.0],
    [0.0,0.0, 0.0,-1.0, 0.0,0.0, 0.0,0.0],
    [0.0,-1.0, 0.0,0.0, 0.0,0.0, 0.0,0.0],
];

// γ₂ = [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
const GAMMA2: [[f64; 8]; 4] = [
    [0.0,0.0, 0.0,0.0, 0.0,0.0,-1.0,0.0],
    [0.0,0.0, 0.0,0.0, 1.0,0.0, 0.0,0.0],
    [0.0,0.0, 1.0,0.0, 0.0,0.0, 0.0,0.0],
    [-1.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0],
];

// γ₃ = [[0,0,i,0],[0,0,0,-i],[-i,0,0,0],[0,i,0,0]]
const GAMMA3: [[f64; 8]; 4] = [
    [0.0,0.0, 0.0,0.0, 0.0,1.0, 0.0,0.0],
    [0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,-1.0],
    [0.0,-1.0, 0.0,0.0, 0.0,0.0, 0.0,0.0],
    [0.0,0.0, 0.0,1.0, 0.0,0.0, 0.0,0.0],
];

const GAMMAS: [&[[f64; 8]; 4]; 4] = [&GAMMA0, &GAMMA1, &GAMMA2, &GAMMA3];

/// Get complex entry (re, im) of gamma_mu[alpha][beta]
#[inline]
fn gamma_entry(mu: usize, alpha: usize, beta: usize) -> (f64, f64) {
    let row = GAMMAS[mu][alpha];
    (row[2 * beta], row[2 * beta + 1])
}

/// Apply Wilson-Dirac operator: result = D_W * psi
/// psi layout: [site][spinor][color] as flat Vec<f64> with complex interleaving
/// site index: x0*Ls^2*Lt + ... (same as lattice.rs)
/// spinor: 0..3
/// color: 0..d_fund-1, complex (re,im)
///
/// Total length: N_sites * 4 * 2 * d_fund
pub fn apply_wilson_dirac(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    mass: f64,
    psi: &[f64],
) -> Vec<f64> {
    let ls = lat.ls;
    let lt = lat.lt;
    let d = group.dim_fund();
    let is_complex_group = group.is_complex();
    let n_sites = ls * ls * ls * lt;
    let site_dof = 4 * 2 * d; // 4 spinor × complex × d_fund
    let sizes = [ls, ls, ls, lt];

    assert_eq!(psi.len(), n_sites * site_dof, "psi has wrong length");
    let mut result = vec![0.0f64; psi.len()];

    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [x0, x1, x2, x3];
                    let idx = ((x0 * ls + x1) * ls + x2) * lt + x3;
                    let ri = idx * site_dof;

                    // Mass + Wilson term: (4 + m) δ_{xy}
                    for s in 0..site_dof {
                        result[ri + s] += (4.0 + mass) * psi[ri + s];
                    }

                    // Hopping terms: -½ Σ_μ [...]
                    for mu in 0..4 {
                        // Forward: -½ (1 - γ_μ) U_μ(x) ψ(x+μ)
                        let mut fwd = site;
                        fwd[mu] = (fwd[mu] + 1) % sizes[mu];
                        let fwd_idx = ((fwd[0]*ls + fwd[1])*ls + fwd[2])*lt + fwd[3];
                        let u_fwd = lat.get(site, mu);

                        // Backward: -½ (1 + γ_μ) U†_μ(x-μ) ψ(x-μ)
                        let mut bwd = site;
                        bwd[mu] = (bwd[mu] + sizes[mu] - 1) % sizes[mu];
                        let bwd_idx = ((bwd[0]*ls + bwd[1])*ls + bwd[2])*lt + bwd[3];
                        let u_bwd_dag = group.dagger(lat.get(bwd, mu));

                        for alpha in 0..4 {
                            for beta in 0..4 {
                                let (gre, gim) = gamma_entry(mu, alpha, beta);

                                // (1 - γ_μ)_{αβ} = δ_{αβ} - γ_μ_{αβ}
                                let pminus_re = if alpha == beta { 1.0 } else { 0.0 } - gre;
                                let pminus_im = -gim;

                                // (1 + γ_μ)_{αβ} = δ_{αβ} + γ_μ_{αβ}
                                let pplus_re = if alpha == beta { 1.0 } else { 0.0 } + gre;
                                let pplus_im = gim;

                                if pminus_re.abs() < 1e-15 && pminus_im.abs() < 1e-15
                                    && pplus_re.abs() < 1e-15 && pplus_im.abs() < 1e-15 {
                                    continue;
                                }

                                // Color contraction: U_{ab} ψ_b
                                for a in 0..d {
                                    let res_offset = ri + alpha * 2 * d + 2 * a;

                                    for b in 0..d {
                                        // Get U_{ab} and ψ_b at the neighbor
                                        let (u_re, u_im, psi_fwd_re, psi_fwd_im,
                                             ud_re, ud_im, psi_bwd_re, psi_bwd_im);

                                        if is_complex_group {
                                            let ui = 2 * (a * d + b);
                                            u_re = u_fwd[ui];
                                            u_im = u_fwd[ui + 1];
                                            ud_re = u_bwd_dag[ui];
                                            ud_im = u_bwd_dag[ui + 1];
                                        } else {
                                            u_re = u_fwd[a * d + b];
                                            u_im = 0.0;
                                            ud_re = u_bwd_dag[a * d + b];
                                            ud_im = 0.0;
                                        }

                                        let psi_fwd_offset = fwd_idx * site_dof + beta * 2 * d + 2 * b;
                                        psi_fwd_re = psi[psi_fwd_offset];
                                        psi_fwd_im = psi[psi_fwd_offset + 1];

                                        let psi_bwd_offset = bwd_idx * site_dof + beta * 2 * d + 2 * b;
                                        psi_bwd_re = psi[psi_bwd_offset];
                                        psi_bwd_im = psi[psi_bwd_offset + 1];

                                        // Forward: -½ (1-γ)_{αβ} U_{ab} ψ_b(x+μ)
                                        // (pminus)(U·ψ) complex multiply
                                        let upsi_fwd_re = u_re * psi_fwd_re - u_im * psi_fwd_im;
                                        let upsi_fwd_im = u_re * psi_fwd_im + u_im * psi_fwd_re;
                                        let fwd_contrib_re = pminus_re * upsi_fwd_re - pminus_im * upsi_fwd_im;
                                        let fwd_contrib_im = pminus_re * upsi_fwd_im + pminus_im * upsi_fwd_re;

                                        // Backward: -½ (1+γ)_{αβ} U†_{ab} ψ_b(x-μ)
                                        let upsi_bwd_re = ud_re * psi_bwd_re - ud_im * psi_bwd_im;
                                        let upsi_bwd_im = ud_re * psi_bwd_im + ud_im * psi_bwd_re;
                                        let bwd_contrib_re = pplus_re * upsi_bwd_re - pplus_im * upsi_bwd_im;
                                        let bwd_contrib_im = pplus_re * upsi_bwd_im + pplus_im * upsi_bwd_re;

                                        result[res_offset] -= 0.5 * (fwd_contrib_re + bwd_contrib_re);
                                        result[res_offset + 1] -= 0.5 * (fwd_contrib_im + bwd_contrib_im);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    result
}

/// Apply γ₅ to a spinor: γ₅ = diag(1,1,-1,-1) in chiral basis
pub fn apply_gamma5(psi: &[f64], d: usize) -> Vec<f64> {
    let site_dof = 4 * 2 * d;
    let n_sites = psi.len() / site_dof;
    let mut result = psi.to_vec();
    for site in 0..n_sites {
        let ri = site * site_dof;
        // spinor 2 and 3 get minus sign
        for s in 2..4 {
            for c in 0..(2 * d) {
                result[ri + s * 2 * d + c] = -result[ri + s * 2 * d + c];
            }
        }
    }
    result
}

/// Check γ₅-hermiticity: D† = γ₅ D γ₅
/// Returns max |D†ψ - γ₅ D γ₅ ψ| for a random ψ
pub fn check_gamma5_hermiticity(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    mass: f64,
) -> f64 {
    let d = group.dim_fund();
    let n = lat.ls * lat.ls * lat.ls * lat.lt * 4 * 2 * d;

    // Random spinor
    let mut rng = rand::thread_rng();
    use rand::Rng;
    let psi: Vec<f64> = (0..n).map(|_| rng.gen::<f64>() - 0.5).collect();
    let chi: Vec<f64> = (0..n).map(|_| rng.gen::<f64>() - 0.5).collect();

    // <chi, D psi> vs <D†chi, psi> = <γ₅ D γ₅ chi, psi>
    let d_psi = apply_wilson_dirac(lat, group, mass, &psi);
    let g5_chi = apply_gamma5(&chi, d);
    let d_g5_chi = apply_wilson_dirac(lat, group, mass, &g5_chi);
    let g5_d_g5_chi = apply_gamma5(&d_g5_chi, d);

    // <chi, D psi>
    let lhs: f64 = chi.iter().zip(d_psi.iter()).map(|(a, b)| a * b).sum();
    // <γ₅ D γ₅ chi, psi>
    let rhs: f64 = g5_d_g5_chi.iter().zip(psi.iter()).map(|(a, b)| a * b).sum();

    (lhs - rhs).abs() / lhs.abs().max(1e-15)
}
