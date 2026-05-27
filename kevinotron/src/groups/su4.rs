// kevinotron/src/groups/su4.rs
// SU(4) gauge group -- 4x4 complex unitary, det=1.
// 15 generators (generalized Gell-Mann).
// Taylor-12 expm + Gram-Schmidt unitarization.

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct SU4Group;

impl SU4Group {
    pub fn new() -> Self { SU4Group }
}

/// Build 15 generators of su(4).
fn su4_generators() -> Vec<Vec<f64>> {
    let n = 4;
    let mut gens = Vec::new();

    // Symmetric off-diagonal: N(N-1)/2 = 6
    for j in 0..n {
        for k in (j + 1)..n {
            let mut g = cmat_zero(n);
            cset(&mut g, n, j, k, 0.0, 0.5);
            cset(&mut g, n, k, j, 0.0, 0.5);
            gens.push(g);
        }
    }
    // Anti-symmetric off-diagonal: 6
    for j in 0..n {
        for k in (j + 1)..n {
            let mut g = cmat_zero(n);
            cset(&mut g, n, j, k, 0.5, 0.0);
            cset(&mut g, n, k, j, -0.5, 0.0);
            gens.push(g);
        }
    }
    // Diagonal: N-1 = 3
    for l in 1..n {
        let mut g = cmat_zero(n);
        let s = (1.0 / (2.0 * l as f64 * (l + 1) as f64)).sqrt();
        for j in 0..l {
            cset(&mut g, n, j, j, 0.0, s);
        }
        cset(&mut g, n, l, l, 0.0, -(l as f64) * s);
        gens.push(g);
    }

    assert_eq!(gens.len(), 15, "Expected 15 SU(4) generators");
    gens
}

impl GaugeGroup for SU4Group {
    fn name(&self) -> &str { "SU(4)" }
    fn dim_fund(&self) -> usize { 4 }
    fn dim_adj(&self) -> usize { 15 }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { 4.0 }

    fn identity(&self) -> LinkData { cmat_identity(4) }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let gens = su4_generators();
        let mut a = cmat_zero(4);
        for g in &gens {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..a.len() {
                a[i] += g[i] * c;
            }
        }
        let u = cmat_expm_taylor12(&a, 4);
        cmat_unitarize(&u, 4)
    }

    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, 4) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, 4) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, 4) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, 4) }
    fn zero(&self) -> LinkData { cmat_zero(4) }

    fn reproject(&self, u: &[f64]) -> LinkData {
        cmat_unitarize(u, 4)
    }
}
