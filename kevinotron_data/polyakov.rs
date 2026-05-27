// observables/polyakov.rs — Polyakov loop measurement
//
// L(x) = (1/d_fund) Tr(prod_{t=0}^{Lt-1} U_3(x,t))
// Order parameter for deconfinement.

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;

pub struct PolyakovResult {
    pub re_mean: f64,
    pub im_mean: f64,
    pub modulus_mean: f64,
    pub susceptibility: f64,
}

pub fn measure_polyakov(lat: &Lattice4D, group: &dyn GaugeGroup) -> PolyakovResult {
    let ls = lat.ls;
    let lt = lat.lt;
    let d = group.dim_fund() as f64;
    let mut re_vals = Vec::with_capacity(ls * ls * ls);
    let mut im_vals = Vec::with_capacity(ls * ls * ls);

    for x0 in 0..ls {
        for x1 in 0..ls {
            for x2 in 0..ls {
                let mut prod = group.identity();
                for t in 0..lt {
                    let u = lat.get([x0, x1, x2, t], 3);
                    prod = group.mul(&prod, u);
                }
                re_vals.push(group.trace_re(&prod) / d);
                im_vals.push(group.trace_im(&prod) / d);
            }
        }
    }

    let n = re_vals.len() as f64;
    let re_mean: f64 = re_vals.iter().sum::<f64>() / n;
    let im_mean: f64 = im_vals.iter().sum::<f64>() / n;

    let mod_vals: Vec<f64> = re_vals.iter().zip(im_vals.iter())
        .map(|(r, i)| (r * r + i * i).sqrt())
        .collect();
    let modulus_mean: f64 = mod_vals.iter().sum::<f64>() / n;

    let mod2_mean: f64 = mod_vals.iter().map(|m| m * m).sum::<f64>() / n;
    let susceptibility = n * (mod2_mean - modulus_mean * modulus_mean);

    PolyakovResult {
        re_mean,
        im_mean,
        modulus_mean,
        susceptibility,
    }
}

pub fn binder_cumulant(mod_vals: &[f64]) -> f64 {
    let n = mod_vals.len() as f64;
    let m2: f64 = mod_vals.iter().map(|m| m * m).sum::<f64>() / n;
    let m4: f64 = mod_vals.iter().map(|m| m.powi(4)).sum::<f64>() / n;
    if m2.abs() < 1e-15 { return 0.0; }
    1.0 - m4 / (3.0 * m2 * m2)
}
