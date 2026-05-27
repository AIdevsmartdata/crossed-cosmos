// kevinotron/src/lattice.rs
// 4D lattice L^3 x T with gauge links and Metropolis sweeps.
// Generic over GaugeGroup trait.

use crate::groups::{GaugeGroup, LinkData};
use rand::{Rng, RngCore};

/// Lattice4D owns all link variables and performs sweeps.
#[derive(Clone)]
pub struct Lattice4D {
    pub ls: usize,
    pub lt: usize,
    pub beta: f64,
    pub links: Vec<f64>, // flat: all links contiguous
    link_size: usize,     // f64 per link matrix
}

impl Lattice4D {
    /// Create a cold-start lattice (all links = identity).
    pub fn new(group: &dyn GaugeGroup, ls: usize, lt: usize, beta: f64) -> Self {
        let link_size = group.link_size();
        let n_links = ls * ls * ls * lt * 4;
        let id = group.identity();
        let mut links = vec![0.0f64; n_links * link_size];
        for i in 0..n_links {
            let offset = i * link_size;
            links[offset..offset + link_size].copy_from_slice(&id);
        }
        Lattice4D { ls, lt, beta, links, link_size }
    }

    #[inline]
    fn size(&self, d: usize) -> usize {
        if d < 3 { self.ls } else { self.lt }
    }

    #[inline]
    fn idx(&self, s: [usize; 4], mu: usize) -> usize {
        let flat = ((s[0] * self.ls + s[1]) * self.ls + s[2]) * self.lt + s[3];
        (flat * 4 + mu) * self.link_size
    }

    #[inline]
    fn shift(&self, s: [usize; 4], mu: usize, dir: i32) -> [usize; 4] {
        let mut r = s;
        let sz = self.size(mu);
        r[mu] = ((r[mu] as i32 + dir).rem_euclid(sz as i32)) as usize;
        r
    }

    /// Get link slice at site s, direction mu.
    #[inline]
    pub fn get(&self, s: [usize; 4], mu: usize) -> &[f64] {
        let i = self.idx(s, mu);
        &self.links[i..i + self.link_size]
    }

    /// Set link at site s, direction mu.
    #[inline]
    pub fn set(&mut self, s: [usize; 4], mu: usize, data: &[f64]) {
        let i = self.idx(s, mu);
        self.links[i..i + self.link_size].copy_from_slice(data);
    }

    /// Compute staple sum K(x, mu) = sum over nu!=mu of forward+backward staples.
    pub fn staple_sum(&self, group: &dyn GaugeGroup, site: [usize; 4], mu: usize) -> LinkData {
        let mut k = group.zero();
        for nu in 0..4 {
            if nu == mu { continue; }
            let x_mu = self.shift(site, mu, 1);
            let x_nu = self.shift(site, nu, 1);

            // Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
            let fwd = group.mul(
                &group.mul(
                    self.get(x_mu, nu),
                    &group.dagger(self.get(x_nu, mu)),
                ),
                &group.dagger(self.get(site, nu)),
            );
            k = group.add(&k, &fwd);

            // Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
            let x_mu_mnu = self.shift(x_mu, nu, -1);
            let x_mnu = self.shift(site, nu, -1);
            let bwd = group.mul(
                &group.mul(
                    &group.dagger(self.get(x_mu_mnu, nu)),
                    &group.dagger(self.get(x_mnu, mu)),
                ),
                self.get(x_mnu, nu),
            );
            k = group.add(&k, &bwd);
        }
        k
    }

    /// Is this link on the entangling boundary?
    /// Boundary: mu=0 and x[0] = ls/2 - 1
    #[inline]
    pub fn is_boundary(&self, site: [usize; 4], mu: usize) -> bool {
        mu == 0 && site[0] == self.ls / 2 - 1
    }

    /// One full Metropolis sweep with alpha-deformed action on boundary links.
    /// Returns acceptance rate.
    pub fn sweep_alpha(
        &mut self,
        group: &dyn GaugeGroup,
        alpha: f64,
        epsilon: f64,
        rng: &mut impl Rng,
    ) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let beta_over_d = self.beta / group.beta_norm();
        let mut accepted = 0u64;
        let mut total = 0u64;

        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..4 {
                            let u_old = self.get(site, mu).to_vec();
                            let k = self.staple_sum(group, site, mu);
                            let uk = group.mul(&u_old, &k);
                            let base_old = -beta_over_d * group.trace_re(&uk);
                            let s_old = if self.is_boundary(site, mu) {
                                (1.0 - alpha) * base_old
                            } else {
                                base_old
                            };

                            let r = group.random_near_id(epsilon, rng as &mut dyn RngCore);
                            let u_new = group.mul(&r, &u_old);
                            let uk_new = group.mul(&u_new, &k);
                            let base_new = -beta_over_d * group.trace_re(&uk_new);
                            let s_new = if self.is_boundary(site, mu) {
                                (1.0 - alpha) * base_new
                            } else {
                                base_new
                            };

                            let ds = s_new - s_old;
                            if ds < 0.0 || rng.gen::<f64>() < (-ds).exp() {
                                self.set(site, mu, &u_new);
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

    /// Measure dS/dalpha = -sum_{boundary links} (beta/d) Re Tr(U*K)
    pub fn measure_ds_dalpha(&self, group: &dyn GaugeGroup) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let beta_over_d = self.beta / group.beta_norm();
        let mut ds = 0.0;
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [ls / 2 - 1, x1, x2, x3];
                    let u = self.get(site, 0);
                    let k = self.staple_sum(group, site, 0);
                    let uk = group.mul(u, &k);
                    let base = -beta_over_d * group.trace_re(&uk);
                    ds += base;
                }
            }
        }
        -ds
    }

    /// Average plaquette (1/d_fund) Re Tr(U_plaq).
    pub fn plaquette(&self, group: &dyn GaugeGroup) -> f64 {
        let ls = self.ls;
        let lt = self.lt;
        let d = group.dim_fund() as f64;
        let mut p = 0.0;
        let mut count = 0u64;
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..4 {
                            for nu in (mu + 1)..4 {
                                let x_mu = self.shift(site, mu, 1);
                                let x_nu = self.shift(site, nu, 1);
                                let plaq = group.mul(
                                    &group.mul(
                                        self.get(site, mu),
                                        self.get(x_mu, nu),
                                    ),
                                    &group.mul(
                                        &group.dagger(self.get(x_nu, mu)),
                                        &group.dagger(self.get(site, nu)),
                                    ),
                                );
                                p += group.trace_re(&plaq) / d;
                                count += 1;
                            }
                        }
                    }
                }
            }
        }
        p / count as f64
    }

    /// Re-project all links onto the group manifold.
    pub fn reproject_all(&mut self, group: &dyn GaugeGroup) {
        let ls = self.ls;
        let lt = self.lt;
        for x0 in 0..ls {
            for x1 in 0..ls {
                for x2 in 0..ls {
                    for x3 in 0..lt {
                        let site = [x0, x1, x2, x3];
                        for mu in 0..4 {
                            let u = self.get(site, mu).to_vec();
                            let u_proj = group.reproject(&u);
                            self.set(site, mu, &u_proj);
                        }
                    }
                }
            }
        }
    }

    /// Total number of link variables
    pub fn n_links(&self) -> usize {
        self.ls * self.ls * self.ls * self.lt * 4
    }

    /// Get all links as a flat f64 slice (for npy dump)
    pub fn links_raw(&self) -> &[f64] {
        &self.links
    }
}
