// hmc.rs — Hybrid Monte Carlo (CORRECTED)
//
// KEY MATH:
// Momenta π ∈ Lie algebra (anti-Hermitian traceless for SU(N), antisymmetric for SO/G₂/F₄)
// Kinetic energy: T = -Tr(π²) (positive since π anti-Hermitian)
// Gauge force: F = project_to_algebra(-(β/d) × U × staple_sum)
//   For SU(N): F = (V - V†)/2 - Tr(V-V†)/(2N) I where V = (β/N) U K
//   For real:  F = (V - V^T)/2 where V = (β/d) U K
// Update: U_new = exp(dt × π) × U_old (π is already in the algebra)

use crate::groups::{GaugeGroup, LinkData, RngWrapper};
use crate::lattice::Lattice4D;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct HmcConfig {
    pub n_steps: usize,
    pub dt: f64,
    pub beta: f64,
}

/// Generate random momentum in the Lie algebra
/// Complex groups: π = anti-Hermitian traceless (2*d*d f64)
/// Real groups: π = antisymmetric (d*d f64)
fn random_algebra_element(group: &dyn GaugeGroup, rng: &mut dyn RngCore) -> LinkData {
    // Use random_near_id with large epsilon, then take log ≈ the algebra element
    // Actually simpler: generate random anti-Hermitian traceless matrix directly
    let d = group.dim_fund();
    let mut w = RngWrapper(rng);

    if group.is_complex() {
        let mut m = vec![0.0f64; 2 * d * d];
        // Fill upper triangle with random complex, reflect to lower
        for i in 0..d {
            for j in (i + 1)..d {
                let re: f64 = w.sample::<f64, _>(StandardNormal);
                let im: f64 = w.sample::<f64, _>(StandardNormal);
                let idx_ij = 2 * (i * d + j);
                let idx_ji = 2 * (j * d + i);
                // Anti-Hermitian: M_ij = a+ib, M_ji = -a+ib (so M† = -M)
                m[idx_ij] = re;        // Re M_ij
                m[idx_ij + 1] = im;    // Im M_ij
                m[idx_ji] = -re;       // Re M_ji = -Re M_ij
                m[idx_ji + 1] = im;    // Im M_ji = Im M_ij (since conj swap + negate)
            }
            // Diagonal: purely imaginary for anti-Hermitian
            let diag_val: f64 = w.sample::<f64, _>(StandardNormal);
            m[2 * (i * d + i) + 1] = diag_val; // Im M_ii
        }
        // Make traceless: subtract Tr(M)/d from diagonal
        let mut tr_im = 0.0;
        for i in 0..d {
            tr_im += m[2 * (i * d + i) + 1];
        }
        tr_im /= d as f64;
        for i in 0..d {
            m[2 * (i * d + i) + 1] -= tr_im;
        }
        m
    } else {
        let mut m = vec![0.0f64; d * d];
        // Antisymmetric: M_ij = -M_ji
        for i in 0..d {
            for j in (i + 1)..d {
                let val: f64 = w.sample::<f64, _>(StandardNormal);
                m[i * d + j] = val;
                m[j * d + i] = -val;
            }
        }
        m
    }
}

/// Kinetic energy: T = -Tr(π²) for anti-Hermitian π
/// For complex: -Tr(π²) = -Σ_{ij} π_ij π_ji = -Σ_ij π_ij (-π_ij*) = Σ |π_ij|²
/// For real: -Tr(π²) = -Σ_ij π_ij π_ji = Σ_ij π_ij² (antisymmetric)
fn kinetic_energy(momenta: &[LinkData], is_complex: bool) -> f64 {
    let mut t = 0.0;
    for p in momenta {
        if is_complex {
            // -Tr(π²) = Σ |π_ij|² = Σ (re² + im²)
            for &x in p.iter() {
                t += x * x;
            }
        } else {
            // -Tr(π²) = 2 Σ_{i<j} π_ij² (each off-diag appears twice with opposite sign)
            for &x in p.iter() {
                t += x * x;
            }
        }
    }
    0.5 * t
}

/// Project V = (β/d) U K onto the Lie algebra
/// Complex: Ta(V) = (V - V†)/2 - Tr(V-V†)/(2d) I
/// Real: Ta(V) = (V - V^T)/2
fn project_force(group: &dyn GaugeGroup, v: &[f64]) -> LinkData {
    let d = group.dim_fund();

    if group.is_complex() {
        let mut f = vec![0.0f64; 2 * d * d];
        // V† stored as conjugate transpose
        let v_dag = crate::groups::cmat_dagger(v, d);
        // (V - V†)/2
        for i in 0..f.len() {
            f[i] = 0.5 * (v[i] - v_dag[i]);
        }
        // Subtract trace
        let mut tr_re = 0.0;
        let mut tr_im = 0.0;
        for i in 0..d {
            let idx = 2 * (i * d + i);
            tr_re += f[idx];
            tr_im += f[idx + 1];
        }
        tr_re /= d as f64;
        tr_im /= d as f64;
        for i in 0..d {
            let idx = 2 * (i * d + i);
            f[idx] -= tr_re;
            f[idx + 1] -= tr_im;
        }
        f
    } else {
        let mut f = vec![0.0f64; d * d];
        // (V - V^T)/2
        for i in 0..d {
            for j in 0..d {
                f[i * d + j] = 0.5 * (v[i * d + j] - v[j * d + i]);
            }
        }
        f
    }
}

/// Gauge action
fn gauge_action(lat: &Lattice4D, group: &dyn GaugeGroup, beta: f64) -> f64 {
    let p = lat.plaquette(group);
    let d = group.dim_fund() as f64;
    let n_plaq = 6 * lat.ls.pow(3) * lat.lt;
    beta * n_plaq as f64 * (1.0 - p)
}


/// Update all momenta: p -= dt × F(U)
fn update_momenta(
    lat: &Lattice4D,
    momenta: &mut [LinkData],
    group: &dyn GaugeGroup,
    beta_d: f64,
    dt: f64,
) {
    let ls = lat.ls; let lt = lat.lt;
    let mut idx = 0;
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    for mu in 0..4 {
                        let site = [x0,x1,x2,x3];
                        let u = lat.get(site, mu);
                        let k = lat.staple_sum(group, site, mu);
                        let mut v = group.mul(u, &k);
                        for x in v.iter_mut() { *x *= beta_d; }
                        let f = project_force(group, &v);
                        for i in 0..momenta[idx].len() {
                            momenta[idx][i] -= dt * f[i];
                        }
                        idx += 1;
                    }
                }
            }
        }
    }
}

/// Update all links: U = exp(dt × π) × U
fn update_links(
    lat: &mut Lattice4D,
    momenta: &[LinkData],
    group: &dyn GaugeGroup,
    dt: f64,
) {
    let ls = lat.ls; let lt = lat.lt;
    let d = group.dim_fund();
    let is_complex = group.is_complex();
    let mut idx = 0;
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    for mu in 0..4 {
                        let site = [x0,x1,x2,x3];
                        let u = lat.get(site, mu).to_vec();
                        let p = &momenta[idx];
                        // exp(dt π) via Taylor-12 (matching Metropolis precision)
                        let exp_p;
                        if is_complex {
                            let mut s = p.clone();
                            for x in s.iter_mut() { *x *= dt; }
                            exp_p = crate::groups::cmat_expm_taylor12(&s, d);
                        } else {
                            // Real groups: Taylor-12 manually
                            let mut s = p.clone();
                            for x in s.iter_mut() { *x *= dt; }
                            let mut sum = crate::groups::rmat_identity(d);
                            let mut pow = crate::groups::rmat_identity(d);
                            for k in 1..=12 {
                                pow = crate::groups::rmat_mul(&pow, &s, d);
                                let inv_k = 1.0 / k as f64;
                                for i in 0..pow.len() { pow[i] *= inv_k; }
                                for i in 0..sum.len() { sum[i] += pow[i]; }
                            }
                            exp_p = sum;
                        }
                        let u_new = if is_complex {
                            crate::groups::cmat_mul(&exp_p, &u, d)
                        } else {
                            crate::groups::rmat_mul(&exp_p, &u, d)
                        };
                        lat.set(site, mu, &group.reproject(&u_new));
                        idx += 1;
                    }
                }
            }
        }
    }
}

/// One HMC trajectory
pub fn hmc_trajectory(
    lat: &mut Lattice4D,
    group: &dyn GaugeGroup,
    cfg: &HmcConfig,
    rng: &mut dyn RngCore,
) -> (bool, f64) {
    let ls = lat.ls;
    let lt = lat.lt;
    let n_links = 4 * ls * ls * ls * lt;
    let is_complex = group.is_complex();
    let beta_d = cfg.beta / group.beta_norm();

    // Save old config
    let mut old_links = Vec::with_capacity(n_links);
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    for mu in 0..4 {
                        old_links.push(lat.get([x0,x1,x2,x3], mu).to_vec());
                    }
                }
            }
        }
    }

    // Generate algebra momenta
    let mut momenta: Vec<LinkData> = (0..n_links)
        .map(|_| random_algebra_element(group, rng))
        .collect();

    // Initial Hamiltonian
    let t_old = kinetic_energy(&momenta, is_complex);
    let s_old = gauge_action(lat, group, cfg.beta);
    let h_old = t_old + s_old;

    // Leapfrog: proper V-V-T-V-V scheme (Verlet)
    // Step 0: half-step momenta
    update_momenta(lat, &mut momenta, group, beta_d, 0.5 * cfg.dt);
    
    // Steps 1..n-1: full link + full momenta
    for _step in 0..cfg.n_steps - 1 {
        update_links(lat, &momenta, group, cfg.dt);
        update_momenta(lat, &mut momenta, group, beta_d, cfg.dt);
    }
    
    // Final: full link + half momenta
    update_links(lat, &momenta, group, cfg.dt);
    update_momenta(lat, &mut momenta, group, beta_d, 0.5 * cfg.dt);

    // Final Hamiltonian
    let t_new = kinetic_energy(&momenta, is_complex);
    let s_new = gauge_action(lat, group, cfg.beta);
    let h_new = t_new + s_new;
    let delta_h = h_new - h_old;

    // WARNING: HMC is only correct for groups where the full anti-Hermitian
    // traceless (complex) or antisymmetric (real) space IS the Lie algebra.
    // This holds for SU(N) and SO(N), but NOT for G₂⊂SO(7), Sp(4)⊂SU(4),
    // F₄⊂SO(26), E₆⊂SU(27). For these groups, use Metropolis mode instead.
    // TODO: implement group-specific algebra projection using stored generators.

    // Accept/reject
    let mut w = RngWrapper(rng);
    let r: f64 = w.gen();
    let accepted = r < (-delta_h).exp().min(1.0);

    if !accepted {
        let mut link_idx = 0;
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        for mu in 0..4 {
                            lat.set([x0,x1,x2,x3], mu, &old_links[link_idx]);
                            link_idx += 1;
                        }
                    }
                }
            }
        }
    }

    (accepted, delta_h)
}
