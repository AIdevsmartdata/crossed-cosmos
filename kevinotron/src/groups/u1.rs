// kevinotron/src/groups/u1.rs
// U(1) gauge group -- 1x1 complex phases e^{iθ}.
//
// The simplest gauge group: a single complex number with |z|=1.
// Stored as 2 f64 (re, im) = complex flat storage with n=1.
//
// Properties:
//   dim_fund = 1  (1x1 matrix = just a phase)
//   dim_adj  = 1  (one generator: i)
//   beta_norm = 1.0
//   |Φ⁺| = 0     (abelian group, no positive roots)
//   C₂ = 0        (abelian, Casimir = 0)
//   Generator: T = i (the imaginary unit)
//   Random element near identity: e^{iεη} where η ~ N(0,1)
//   Plaquette: Re(U₁ U₂ U₃* U₄*) same as SU(N) with * = conjugate

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct U1Group;

impl U1Group {
    pub fn new() -> Self { U1Group }
}

impl GaugeGroup for U1Group {
    fn name(&self) -> &str { "U(1)" }
    fn dim_fund(&self) -> usize { 1 }
    fn dim_adj(&self) -> usize { 1 }
    fn is_complex(&self) -> bool { true }
    // beta_norm = 1 for U(1): S = -β Σ Re(U_plaq), with Re(plaquette)/1 = cos(θ_plaq)
    fn beta_norm(&self) -> f64 { 1.0 }

    // Identity: (1, 0) = re=1, im=0
    fn identity(&self) -> LinkData {
        cmat_identity(1)
    }

    // Random element near identity: e^{iεη} = (cos(εη), sin(εη))
    // Uses the complex flat storage (n=1): [re, im]
    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let eta: f64 = w.sample::<f64, _>(StandardNormal);
        let theta = epsilon * eta;
        // Multiply identity (1,0) by e^{iθ}: just (cos θ, sin θ)
        // But we want a small perturbation, so we compose with identity:
        // result = identity * e^{iθ} = e^{iθ}
        // Then reproject to |z|=1 (already normalized)
        vec![theta.cos(), theta.sin()]
    }

    // Dagger = complex conjugate: (re, -im)
    fn dagger(&self, u: &[f64]) -> LinkData {
        cmat_dagger(u, 1)
    }

    // Multiply: complex multiplication (a+ib)(c+id) = (ac-bd, ad+bc)
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData {
        cmat_mul(a, b, 1)
    }

    // Re Tr(U) = re part of U (since 1x1 trace is just the element)
    fn trace_re(&self, u: &[f64]) -> f64 {
        cmat_trace_re(u, 1)
    }

    // Element-wise add (for staple accumulation)
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData {
        cmat_add(a, b, 1)
    }

    // Zero element
    fn zero(&self) -> LinkData {
        cmat_zero(1)
    }

    // Reproject to U(1): normalize to unit circle
    fn reproject(&self, u: &[f64]) -> LinkData {
        let re = u[0];
        let im = u[1];
        let norm = (re * re + im * im).sqrt();
        if norm > 1e-14 {
            vec![re / norm, im / norm]
        } else {
            // Degenerate: return identity
            vec![1.0, 0.0]
        }
    }
}
