// thermal.rs — Finite temperature scan via Polyakov loop
//
// Temperature T = 1/(a × Lt). At fixed β (fixed a), varying Lt scans T.
// Deconfinement: |L| jumps from ~0 to ~1 at T_c.
//
// SU(N): first-order transition (N≥3), second-order (N=2)
// G₂, F₄, E₆: crossover (trivial center) or first-order (Z₃ for E₆)

use crate::groups::GaugeGroup;
use crate::lattice::Lattice4D;
use crate::observables::polyakov;

pub struct ThermalResult {
    pub lt: usize,
    pub polyakov_re: f64,
    pub polyakov_im: f64,
    pub polyakov_mod: f64,
    pub susceptibility: f64,
    pub plaquette: f64,
}

pub fn thermal_scan(
    group: &dyn GaugeGroup,
    ls: usize,
    beta: f64,
    lt_values: &[usize],
    n_therm: usize,
    n_meas: usize,
    n_skip: usize,
    epsilon: f64,
) -> Vec<ThermalResult> {
    let mut results = Vec::new();

    for &lt in lt_values {
        eprintln!("# T-scan: Lt={} (T ∝ 1/Lt)", lt);
        let mut lat = Lattice4D::new(group, ls, lt, beta);
        let mut rng = rand::thread_rng();

        // Thermalize
        for sweep in 0..n_therm {
            lat.sweep_alpha(group, 0.0, epsilon, &mut rng);
            if sweep > 0 && sweep % 10 == 0 {
                lat.reproject_all(group);
            }
        }

        // Measure
        let mut poly_re_sum = 0.0;
        let mut poly_im_sum = 0.0;
        let mut poly_mod_sum = 0.0;
        let mut poly_mod2_sum = 0.0;
        let mut plaq_sum = 0.0;

        for _ in 0..n_meas {
            for _ in 0..n_skip {
                lat.sweep_alpha(group, 0.0, epsilon, &mut rng);
            }
            let p = polyakov::measure_polyakov(&lat, group);
            poly_re_sum += p.re_mean;
            poly_im_sum += p.im_mean;
            poly_mod_sum += p.modulus_mean;
            poly_mod2_sum += p.modulus_mean * p.modulus_mean;
            plaq_sum += lat.plaquette(group);
        }

        let n = n_meas as f64;
        let poly_mod_mean = poly_mod_sum / n;
        let vol = (ls * ls * ls) as f64;
        let chi = vol * (poly_mod2_sum / n - poly_mod_mean * poly_mod_mean);

        results.push(ThermalResult {
            lt,
            polyakov_re: poly_re_sum / n,
            polyakov_im: poly_im_sum / n,
            polyakov_mod: poly_mod_mean,
            susceptibility: chi,
            plaquette: plaq_sum / n,
        });

        eprintln!("# Lt={}: |L|={:.6} chi={:.4} P={:.6}",
            lt, poly_mod_mean, chi, plaq_sum / n);
    }

    results
}
