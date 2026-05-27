// kevinotron/src/observables/wilson.rs
// Wilson loop W(R x T) measurement on Lattice4D.
//
// W(R,T) = (1/d_fund) Re Tr( U_bottom * U_right * U_top^dag * U_left^dag )
//
// where the path is a rectangle of extent R in direction mu and T in direction nu.

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

/// Shift site by +1 or -1 in direction mu with periodic BCs.
#[inline]
fn shift(lat: &Lattice4D, s: [usize; 4], mu: usize, dir: i32) -> [usize; 4] {
    let mut r = s;
    let sz = if mu < 3 { lat.ls } else { lat.lt };
    r[mu] = ((r[mu] as i32 + dir).rem_euclid(sz as i32)) as usize;
    r
}

/// Compute a single Wilson loop W(R x T) in the (mu, nu) plane starting at site.
///
/// Path: R links forward in mu, T links forward in nu,
///       R links backward in mu (daggered), T links backward in nu (daggered).
///
/// Returns (1/d_fund) Re Tr(product).
pub fn wilson_loop(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    site: [usize; 4],
    mu: usize,
    nu: usize,
    r: usize,
    t: usize,
) -> f64 {
    let mut prod = group.identity();
    let mut pos = site;

    // Bottom edge: R links in direction mu
    for _ in 0..r {
        let u = lat.get(pos, mu);
        prod = group.mul(&prod, u);
        pos = shift(lat, pos, mu, 1);
    }

    // Right edge: T links in direction nu
    for _ in 0..t {
        let u = lat.get(pos, nu);
        prod = group.mul(&prod, u);
        pos = shift(lat, pos, nu, 1);
    }

    // Top edge: R links backward in direction mu (daggered)
    for _ in 0..r {
        pos = shift(lat, pos, mu, -1);
        let u = lat.get(pos, mu);
        prod = group.mul(&prod, &group.dagger(u));
    }

    // Left edge: T links backward in direction nu (daggered)
    for _ in 0..t {
        pos = shift(lat, pos, nu, -1);
        let u = lat.get(pos, nu);
        prod = group.mul(&prod, &group.dagger(u));
    }

    group.trace_re(&prod) / group.dim_fund() as f64
}

/// Average Wilson loop W(R x T) over all sites and all (mu < nu) planes.
/// Returns (mean, stderr).
pub fn avg_wilson_loop(
    lat: &Lattice4D,
    group: &dyn GaugeGroup,
    r: usize,
    t: usize,
) -> (f64, f64) {
    let ls = lat.ls;
    let lt = lat.lt;
    let mut sum = 0.0;
    let mut sum2 = 0.0;
    let mut count = 0u64;

    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                for x3 in 0..lt {
                    let site = [x0, x1, x2, x3];
                    for mu in 0..4 {
                        for nu in (mu + 1)..4 {
                            let w = wilson_loop(lat, group, site, mu, nu, r, t);
                            sum += w;
                            sum2 += w * w;
                            count += 1;
                            // Also measure transposed orientation in same plane
                            if r != t {
                                let w2 = wilson_loop(lat, group, site, nu, mu, r, t);
                                sum += w2;
                                sum2 += w2 * w2;
                                count += 1;
                            }
                        }
                    }
                }
            }
        }
    }

    let n = count as f64;
    let mean = sum / n;
    let var = sum2 / n - mean * mean;
    let err = (var.max(0.0) / n).sqrt();

    (mean, err)
}
