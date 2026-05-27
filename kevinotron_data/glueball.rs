// observables/glueball.rs — Glueball correlators + APE smearing

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

pub fn plaquette_timeslice(lat: &Lattice4D, group: &dyn GaugeGroup, t: usize) -> f64 {
    let ls = lat.ls;
    let d = group.dim_fund() as f64;
    let mut sum = 0.0;
    let mut count = 0u64;

    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                // Spatial plaquettes at timeslice t
                for mu in 0..3 {
                    for nu in (mu + 1)..3 {
                        let site = [x0, x1, x2, t];
                        let u_mu = lat.get(site, mu);
                        let mut site_mu = site;
                        site_mu[mu] = (site_mu[mu] + 1) % ls;
                        let u_nu_at_mu = lat.get(site_mu, nu);
                        let mut site_nu = site;
                        site_nu[nu] = (site_nu[nu] + 1) % ls;
                        let u_mu_at_nu = lat.get(site_nu, mu);
                        let u_nu = lat.get(site, nu);

                        let prod = group.mul(u_mu, u_nu_at_mu);
                        let prod = group.mul(&prod, &group.dagger(u_mu_at_nu));
                        let plaq = group.mul(&prod, &group.dagger(u_nu));
                        sum += group.trace_re(&plaq) / d;
                        count += 1;
                    }
                }
            }
        }
    }
    sum / count as f64
}

pub fn glueball_correlator(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
) -> Vec<f64> {
    let lt = lat.lt;
    let mut o_t: Vec<f64> = (0..lt).map(|t| plaquette_timeslice(lat, group, t)).collect();

    let o_mean: f64 = o_t.iter().sum::<f64>() / lt as f64;
    for v in o_t.iter_mut() {
        *v -= o_mean;
    }

    // C(dt) = (1/Lt) sum_t O(t) * O(t + dt)
    let mut corr = vec![0.0; lt / 2 + 1];
    for dt in 0..=lt / 2 {
        let mut c = 0.0;
        for t in 0..lt {
            c += o_t[t] * o_t[(t + dt) % lt];
        }
        corr[dt] = c / lt as f64;
    }
    corr
}

pub fn effective_mass(corr: &[f64]) -> Vec<f64> {
    let mut m_eff = Vec::with_capacity(corr.len() - 1);
    for t in 0..corr.len() - 1 {
        if corr[t] > 0.0 && corr[t + 1] > 0.0 {
            m_eff.push((corr[t] / corr[t + 1]).ln());
        } else {
            m_eff.push(0.0);
        }
    }
    m_eff
}

pub fn ape_smear_step(lat: &mut Lattice4D, group: &dyn GaugeGroup, alpha_smear: f64) {
    let ls = lat.ls;
    let lt = lat.lt;
    let mut new_links = Vec::new();

    // Only smear spatial links (mu = 0, 1, 2)
    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [x0, x1, x2, x3];
                    for mu in 0..3 {
                        let u = lat.get(site, mu).to_vec();
                        let mut staple = group.zero();
                        for nu in 0..3 {
                            if nu == mu { continue; }
                            let sizes = [ls, ls, ls, lt];
                            // Forward staple
                            let mut s1 = site;
                            s1[mu] = (s1[mu] + 1) % sizes[mu];
                            let u_nu = lat.get(s1, nu);
                            let mut s2 = site;
                            s2[nu] = (s2[nu] + 1) % sizes[nu];
                            let u_mu_dag = group.dagger(lat.get(s2, mu));
                            let u_nu_dag = group.dagger(lat.get(site, nu));
                            let p = group.mul(u_nu, &u_mu_dag);
                            let p = group.mul(&p, &u_nu_dag);
                            staple = group.add(&staple, &p);
                            // Backward staple
                            let mut s3 = site;
                            s3[mu] = (s3[mu] + 1) % sizes[mu];
                            s3[nu] = (s3[nu] + sizes[nu] - 1) % sizes[nu];
                            let u_nu_dag2 = group.dagger(lat.get(s3, nu));
                            let mut s4 = site;
                            s4[nu] = (s4[nu] + sizes[nu] - 1) % sizes[nu];
                            let u_mu_dag2 = group.dagger(lat.get(s4, mu));
                            let u_nu2 = lat.get(s4, nu);
                            let p = group.mul(&u_nu_dag2, &u_mu_dag2);
                            let p = group.mul(&p, u_nu2);
                            staple = group.add(&staple, &p);
                        }
                        // U_new = (1-alpha)*U + alpha/4 * staple
                        let mut smeared = group.zero();
                        for i in 0..u.len() {
                            smeared[i] = (1.0 - alpha_smear) * u[i] + alpha_smear / 4.0 * staple[i];
                        }
                        let smeared = group.reproject(&smeared);
                        new_links.push((site, mu, smeared));
                    }
                }
            }
        }
    }

    for (site, mu, data) in new_links {
        lat.set(site, mu, &data);
    }
}
