// kevinotron/src/groups/su3.rs
// SU(3) gauge group -- 3x3 complex unitary, det=1.
// Gell-Mann generators T_a = i*lambda_a/2 (anti-Hermitian).
// Taylor-12 expm + Gram-Schmidt unitarization.

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct SU3Group;

impl SU3Group {
    pub fn new() -> Self { SU3Group }
}

/// Build 8 generators of su(3) as anti-Hermitian 3x3 complex matrices.
fn su3_generators() -> Vec<Vec<f64>> {
    let n = 3;
    let mut gens = Vec::new();

    // Symmetric off-diagonal: N(N-1)/2 = 3
    for j in 0..n {
        for k in (j + 1)..n {
            let mut g = cmat_zero(n);
            cset(&mut g, n, j, k, 0.0, 0.5);
            cset(&mut g, n, k, j, 0.0, 0.5);
            gens.push(g);
        }
    }
    // Anti-symmetric off-diagonal: 3
    for j in 0..n {
        for k in (j + 1)..n {
            let mut g = cmat_zero(n);
            cset(&mut g, n, j, k, 0.5, 0.0);
            cset(&mut g, n, k, j, -0.5, 0.0);
            gens.push(g);
        }
    }
    // Diagonal: N-1 = 2
    for l in 1..n {
        let mut g = cmat_zero(n);
        let s = (1.0 / (2.0 * l as f64 * (l + 1) as f64)).sqrt();
        for j in 0..l {
            cset(&mut g, n, j, j, 0.0, s);
        }
        cset(&mut g, n, l, l, 0.0, -(l as f64) * s);
        gens.push(g);
    }

    assert_eq!(gens.len(), 8, "Expected 8 SU(3) generators");
    gens
}

impl GaugeGroup for SU3Group {
    fn name(&self) -> &str { "SU(3)" }
    fn dim_fund(&self) -> usize { 3 }
    fn dim_adj(&self) -> usize { 8 }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { 3.0 }

    fn identity(&self) -> LinkData { cmat_identity(3) }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let gens = su3_generators();
        let mut a = cmat_zero(3);
        for g in &gens {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..a.len() {
                a[i] += g[i] * c;
            }
        }
        let u = cmat_expm_taylor12(&a, 3);
        cmat_unitarize(&u, 3)
    }

    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, 3) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, 3) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, 3) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, 3) }
    fn zero(&self) -> LinkData { cmat_zero(3) }

    fn reproject(&self, u: &[f64]) -> LinkData {
        cmat_unitarize(u, 3)
    }
}
