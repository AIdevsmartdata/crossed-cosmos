// kevinotron/src/groups/su2.rs
// SU(2) gauge group -- 2x2 complex unitary, det=1.
//
// Cayley-Klein parametrization: U = a0*I + i*a*sigma
// where a0^2 + |a|^2 = 1.
// Stored as 2*2*2 = 8 f64 (re,im interleaved).

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct SU2Group;

impl SU2Group {
    pub fn new() -> Self { SU2Group }
}

/// Generate SU(2) generators: T_a = i*sigma_a/2 (anti-Hermitian).
fn su2_generators() -> Vec<Vec<f64>> {
    // sigma_1 = [[0,1],[1,0]]
    // T_1 = i*sigma_1/2 → re: [[0,0],[0,0]], im: [[0,0.5],[0.5,0]]
    let mut t1 = cmat_zero(2);
    cset(&mut t1, 2, 0, 1, 0.0, 0.5);
    cset(&mut t1, 2, 1, 0, 0.0, 0.5);

    // sigma_2 = [[0,-i],[i,0]]
    // T_2 = i*sigma_2/2 → re: [[0,0.5],[-0.5,0]], im: [[0,0],[0,0]]
    let mut t2 = cmat_zero(2);
    cset(&mut t2, 2, 0, 1, 0.5, 0.0);
    cset(&mut t2, 2, 1, 0, -0.5, 0.0);

    // sigma_3 = [[1,0],[0,-1]]
    // T_3 = i*sigma_3/2 → re: [[0,0],[0,0]], im: [[0.5,0],[0,-0.5]]
    let mut t3 = cmat_zero(2);
    cset(&mut t3, 2, 0, 0, 0.0, 0.5);
    cset(&mut t3, 2, 1, 1, 0.0, -0.5);

    vec![t1, t2, t3]
}

impl GaugeGroup for SU2Group {
    fn name(&self) -> &str { "SU(2)" }
    fn dim_fund(&self) -> usize { 2 }
    fn dim_adj(&self) -> usize { 3 }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { 2.0 }

    fn identity(&self) -> LinkData { cmat_identity(2) }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let gens = su2_generators();
        let mut a = cmat_zero(2);
        for g in &gens {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..a.len() {
                a[i] += g[i] * c;
            }
        }
        let u = cmat_expm_taylor12(&a, 2);
        cmat_unitarize(&u, 2)
    }

    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, 2) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, 2) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, 2) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, 2) }
    fn zero(&self) -> LinkData { cmat_zero(2) }

    fn reproject(&self, u: &[f64]) -> LinkData {
        cmat_unitarize(u, 2)
    }
}
