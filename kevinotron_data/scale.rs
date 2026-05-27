// observables/scale.rs — Scale setting via string tension
//
// sigma * a^2 from Creutz ratios at multiple beta values.

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

pub fn static_potential(lat: &Lattice4D, group: &dyn GaugeGroup, r_max: usize) -> Vec<f64> {
    let ls = lat.ls;
    let lt = lat.lt;
    let d = group.dim_fund() as f64;
    let mut potential = vec![0.0; r_max];

    for r in 1..=r_max {
        let t_max = lt / 2;
        let mut w_sum = 0.0;
        let mut count = 0u64;

        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [0, x1, x2, x3];
                    // Wilson loop R x T in the (0, 3) plane
                    // Build the rectangular path
                    if r <= ls / 2 {
                        for t in 1..=t_max.min(4) {
                            let w = wilson_loop_rt(lat, group, site, 0, 3, r, t);
                            w_sum += w / d;
                            count += 1;
                        }
                    }
                }
            }
        }
        if count > 0 {
            potential[r - 1] = -(w_sum / count as f64).ln();
        }
    }
    potential
}

fn wilson_loop_rt(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    start: [usize; 4],
    mu: usize,
    nu: usize,
    r: usize,
    t: usize,
) -> f64 {
    let ls = lat.ls;
    let lt = lat.lt;
    let sizes = [ls, ls, ls, lt];

    // Bottom: R links in mu direction
    let mut prod = group.identity();
    let mut site = start;
    for _ in 0..r {
        let u = lat.get(site, mu);
        prod = group.mul(&prod, u);
        site[mu] = (site[mu] + 1) % sizes[mu];
    }
    // Right: T links in nu direction
    for _ in 0..t {
        let u = lat.get(site, nu);
        prod = group.mul(&prod, u);
        site[nu] = (site[nu] + 1) % sizes[nu];
    }
    // Top: R links backward in mu direction
    for _ in 0..r {
        site[mu] = (site[mu] + sizes[mu] - 1) % sizes[mu];
        let u = lat.get(site, mu);
        prod = group.mul(&prod, &group.dagger(u));
    }
    // Left: T links backward in nu direction
    for _ in 0..t {
        site[nu] = (site[nu] + sizes[nu] - 1) % sizes[nu];
        let u = lat.get(site, nu);
        prod = group.mul(&prod, &group.dagger(u));
    }

    group.trace_re(&prod)
}
