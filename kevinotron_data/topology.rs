// observables/topology.rs — Topological charge Q via clover definition

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

pub fn clover_fmunu(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    site: [usize; 4],
    mu: usize,
    nu: usize,
) -> Vec<f64> {
    let ls = lat.ls;
    let lt = lat.lt;
    let sizes = [ls, ls, ls, lt];

    // Four plaquettes around the site in the (mu,nu) plane
    // C_{mu,nu} = (1/8) * (P1 + P2 + P3 + P4 - P1† - P2† - P3† - P4†)
    let mut sum = group.zero();

    // P1: standard plaquette at (x, mu, nu)
    let p1 = plaquette_at(lat, group, site, mu, nu, sizes);
    sum = group.add(&sum, &p1);

    // P2: plaquette at (x-mu, mu, nu)
    let mut s2 = site;
    s2[mu] = (s2[mu] + sizes[mu] - 1) % sizes[mu];
    let p2 = plaquette_at(lat, group, s2, mu, nu, sizes);
    sum = group.add(&sum, &p2);

    // P3: plaquette at (x-nu, mu, nu)
    let mut s3 = site;
    s3[nu] = (s3[nu] + sizes[nu] - 1) % sizes[nu];
    let p3 = plaquette_at(lat, group, s3, mu, nu, sizes);
    sum = group.add(&sum, &p3);

    // P4: plaquette at (x-mu-nu, mu, nu)
    let mut s4 = site;
    s4[mu] = (s4[mu] + sizes[mu] - 1) % sizes[mu];
    s4[nu] = (s4[nu] + sizes[nu] - 1) % sizes[nu];
    let p4 = plaquette_at(lat, group, s4, mu, nu, sizes);
    sum = group.add(&sum, &p4);

    // Subtract daggers
    let d1 = group.dagger(&p1);
    let d2 = group.dagger(&p2);
    let d3 = group.dagger(&p3);
    let d4 = group.dagger(&p4);
    for i in 0..sum.len() {
        sum[i] = (sum[i] - d1[i] - d2[i] - d3[i] - d4[i]) / 8.0;
    }
    sum
}

fn plaquette_at(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    site: [usize; 4],
    mu: usize,
    nu: usize,
    sizes: [usize; 4],
) -> Vec<f64> {
    let u_mu = lat.get(site, mu);
    let mut s1 = site;
    s1[mu] = (s1[mu] + 1) % sizes[mu];
    let u_nu = lat.get(s1, nu);
    let mut s2 = site;
    s2[nu] = (s2[nu] + 1) % sizes[nu];
    let u_mu_dag = group.dagger(lat.get(s2, mu));
    let u_nu_dag = group.dagger(lat.get(site, nu));
    let p = group.mul(u_mu, u_nu);
    let p = group.mul(&p, &u_mu_dag);
    group.mul(&p, &u_nu_dag)
}

pub fn topological_charge(lat: &Lattice4D, group: &dyn GaugeGroup) -> f64 {
    let ls = lat.ls;
    let lt = lat.lt;
    let d = group.dim_fund() as f64;
    let mut q = 0.0;

    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [x0, x1, x2, x3];
                    // Q = (1/32π²) ε_{μνρσ} Tr(F_μν F_ρσ)
                    // = (1/32π²) * 2 * [Tr(F01 F23) - Tr(F02 F13) + Tr(F03 F12)]
                    let f01 = clover_fmunu(lat, group, site, 0, 1);
                    let f23 = clover_fmunu(lat, group, site, 2, 3);
                    let f02 = clover_fmunu(lat, group, site, 0, 2);
                    let f13 = clover_fmunu(lat, group, site, 1, 3);
                    let f03 = clover_fmunu(lat, group, site, 0, 3);
                    let f12 = clover_fmunu(lat, group, site, 1, 2);

                    let t1 = group.trace_re(&group.mul(&f01, &f23));
                    let t2 = group.trace_re(&group.mul(&f02, &f13));
                    let t3 = group.trace_re(&group.mul(&f03, &f12));

                    q += 2.0 * (t1 - t2 + t3);
                }
            }
        }
    }
    q / (32.0 * std::f64::consts::PI * std::f64::consts::PI)
}
