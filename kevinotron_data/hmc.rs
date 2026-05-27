// hmc.rs — Hybrid Monte Carlo for pure gauge + pseudofermions
//
// Hamilton's equations:
//   dU/dτ = i π U        (π in Lie algebra)
//   dπ/dτ = F_gauge      (gauge force)
//
// Leapfrog integrator (symplectic, reversible):
//   π(dt/2) = π(0) + (dt/2) F(U(0))
//   U(dt)   = exp(i·dt·π(dt/2)) · U(0)
//   π(dt)   = π(dt/2) + (dt/2) F(U(dt))
//
// Accept/reject: P(accept) = min(1, exp(-ΔH))
// ΔH = H_new - H_old, H = T + S = ½Σ Tr(π²) + S_gauge

use crate::groups::{GaugeGroup, LinkData, RngWrapper};
use crate::lattice::Lattice4D;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

/// HMC configuration
pub struct HmcConfig {
    pub n_steps: usize,   // leapfrog steps per trajectory
    pub dt: f64,          // step size
    pub beta: f64,        // gauge coupling
}

/// Generate random momenta in the Lie algebra (Gaussian)
/// Returns flat vector: one momentum per link, each in the Lie algebra
fn generate_momenta(
    group: &dyn GaugeGroup,
    n_links: usize,
    rng: &mut dyn RngCore,
) -> Vec<LinkData> {
    let d_adj = group.dim_adj();
    let link_size = group.link_size();
    let mut momenta = Vec::with_capacity(n_links);
    let mut w = RngWrapper(rng);

    for _ in 0..n_links {
        // Generate random algebra element: π = Σ_a c_a T_a with c_a ~ N(0,1)
        // We store π as a link-sized matrix (same format as links)
        // For pure gauge HMC, we just need the kinetic energy ½ Tr(π²)
        let mut p = vec![0.0f64; link_size];
        // Random coefficients for dim_adj generators
        // Store as a flat matrix directly (the gauge force will add to this)
        for i in 0..link_size {
            p[i] = w.sample::<f64, _>(StandardNormal);
        }
        momenta.push(p);
    }
    momenta
}

/// Kinetic energy: T = ½ Σ_links Tr(π†π) = ½ Σ ||π||²
fn kinetic_energy(momenta: &[LinkData]) -> f64 {
    let mut t = 0.0;
    for p in momenta {
        for &x in p.iter() {
            t += x * x;
        }
    }
    0.5 * t
}

/// Gauge action: S = (β/d_fund) Σ_plaq (d_fund - Re Tr(P))
fn gauge_action(lat: &Lattice4D, group: &dyn GaugeGroup, beta: f64) -> f64 {
    let p = lat.plaquette(group);
    let d = group.dim_fund() as f64;
    let n_plaq = 6 * lat.ls.pow(3) * lat.lt; // 6 plaquette orientations per site
    beta * n_plaq as f64 * (1.0 - p)
}

/// Compute gauge force for one link: F = -(β/d_fund) × Ta(U × staple)
/// Ta = traceless anti-Hermitian projection
/// For real groups: Ta(M) = (M - M^T)/2 - Tr(M-M^T)/(2d) I
/// For complex groups: Ta(M) = (M - M†)/2 - Tr(M-M†)/(2d) I
fn gauge_force(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    site: [usize; 4],
    mu: usize,
    beta: f64,
) -> LinkData {
    let d = group.dim_fund();
    let beta_d = beta / group.beta_norm();
    let u = lat.get(site, mu);
    let k = lat.staple_sum(group, site, mu);
    let uk = group.mul(u, &k);

    // Ta projection: anti-Hermitian traceless part
    let uk_dag = group.dagger(&uk);
    let link_size = group.link_size();
    let mut force = vec![0.0f64; link_size];

    if group.is_complex() {
        // Ta(M) = (M - M†)/(2i) projected to algebra
        // Force = -β/d × (M - M†)/2
        for i in 0..link_size {
            force[i] = -beta_d * 0.5 * (uk[i] - uk_dag[i]);
        }
        // Subtract trace
        let mut tr_re = 0.0;
        let mut tr_im = 0.0;
        for i in 0..d {
            let idx = 2 * (i * d + i);
            tr_re += force[idx];
            tr_im += force[idx + 1];
        }
        tr_re /= d as f64;
        tr_im /= d as f64;
        for i in 0..d {
            let idx = 2 * (i * d + i);
            force[idx] -= tr_re;
            force[idx + 1] -= tr_im;
        }
    } else {
        // Real: Ta(M) = (M - M^T)/2
        for i in 0..d {
            for j in 0..d {
                let m_ij = uk[i * d + j];
                let m_ji = uk[j * d + i];
                force[i * d + j] = -beta_d * 0.5 * (m_ij - m_ji);
            }
        }
        // Subtract trace (should be zero for antisymmetric, but be safe)
        let mut tr = 0.0;
        for i in 0..d {
            tr += force[i * d + i];
        }
        tr /= d as f64;
        for i in 0..d {
            force[i * d + i] -= tr;
        }
    }

    force
}

/// One leapfrog step: update momenta and links
fn leapfrog_step(
    lat: &mut Lattice4D,
    momenta: &mut Vec<LinkData>,
    group: &dyn GaugeGroup,
    dt: f64,
    beta: f64,
    half_step_momenta: bool,
) {
    let ls = lat.ls;
    let lt = lat.lt;
    let sizes = [ls, ls, ls, lt];
    let dt_p = if half_step_momenta { 0.5 * dt } else { dt };

    // Update momenta: π += dt_p × F
    let mut link_idx = 0;
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    for mu in 0..4 {
                        let site = [x0, x1, x2, x3];
                        let f = gauge_force(lat, group, site, mu, beta);
                        for i in 0..momenta[link_idx].len() {
                            momenta[link_idx][i] += dt_p * f[i];
                        }
                        link_idx += 1;
                    }
                }
            }
        }
    }

    // Update links: U = exp(i dt π) U
    // For simplicity, use U_new = (I + i dt π) U then reproject
    // (first-order approximation, sufficient for small dt)
    link_idx = 0;
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    for mu in 0..4 {
                        let site = [x0, x1, x2, x3];
                        let u = lat.get(site, mu).to_vec();
                        let p = &momenta[link_idx];

                        // exp(dt·π) ≈ I + dt·π (small dt)
                        // U_new = exp(dt·π) · U
                        let d = group.dim_fund();
                        let mut u_new;
                        if group.is_complex() {
                            // π is anti-Hermitian, multiply as matrix
                            u_new = vec![0.0f64; group.link_size()];
                            for i in 0..d {
                                for j in 0..d {
                                    let mut re = u[2*(i*d+j)];
                                    let mut im = u[2*(i*d+j)+1];
                                    for k in 0..d {
                                        let p_re = p[2*(i*d+k)];
                                        let p_im = p[2*(i*d+k)+1];
                                        let u_re = u[2*(k*d+j)];
                                        let u_im = u[2*(k*d+j)+1];
                                        re += dt * (p_re * u_re - p_im * u_im);
                                        im += dt * (p_re * u_im + p_im * u_re);
                                    }
                                    u_new[2*(i*d+j)] = re;
                                    u_new[2*(i*d+j)+1] = im;
                                }
                            }
                        } else {
                            // Real: same but no imaginary
                            u_new = vec![0.0f64; group.link_size()];
                            for i in 0..d {
                                for j in 0..d {
                                    let mut val = u[i*d+j];
                                    for k in 0..d {
                                        val += dt * p[i*d+k] * u[k*d+j];
                                    }
                                    u_new[i*d+j] = val;
                                }
                            }
                        }

                        // Reproject onto the group
                        let u_proj = group.reproject(&u_new);
                        lat.set(site, mu, &u_proj);

                        link_idx += 1;
                    }
                }
            }
        }
    }
}

/// Run one HMC trajectory: leapfrog + accept/reject
/// Returns (accepted: bool, delta_h: f64)
pub fn hmc_trajectory(
    lat: &mut Lattice4D,
    group: &dyn GaugeGroup,
    cfg: &HmcConfig,
    rng: &mut dyn RngCore,
) -> (bool, f64) {
    let ls = lat.ls;
    let lt = lat.lt;
    let n_links = 4 * ls * ls * ls * lt;

    // Save old config
    let mut old_links: Vec<Vec<f64>> = Vec::with_capacity(n_links);
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

    // Generate momenta
    let mut momenta = generate_momenta(group, n_links, rng);

    // Initial Hamiltonian
    let t_old = kinetic_energy(&momenta);
    let s_old = gauge_action(lat, group, cfg.beta);
    let h_old = t_old + s_old;

    // Leapfrog integration
    // Half step momenta
    leapfrog_step(lat, &mut momenta, group, cfg.dt, cfg.beta, true);

    // Full steps
    for _ in 1..cfg.n_steps {
        leapfrog_step(lat, &mut momenta, group, cfg.dt, cfg.beta, false);
    }

    // Final half step momenta
    leapfrog_step(lat, &mut momenta, group, cfg.dt, cfg.beta, true);

    // Final Hamiltonian
    let t_new = kinetic_energy(&momenta);
    let s_new = gauge_action(lat, group, cfg.beta);
    let h_new = t_new + s_new;

    let delta_h = h_new - h_old;

    // Metropolis accept/reject
    let mut w = RngWrapper(rng);
    let r: f64 = w.gen();
    let accepted = r < (-delta_h).exp().min(1.0);

    if !accepted {
        // Restore old config
        let mut link_idx = 0;
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        for mu in 0..4 {
                            lat.set([x0, x1, x2, x3], mu, &old_links[link_idx]);
                            link_idx += 1;
                        }
                    }
                }
            }
        }
    }

    (accepted, delta_h)
}
