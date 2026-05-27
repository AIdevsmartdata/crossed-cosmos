// kevinotron/src/groups/e6.rs
// E6 gauge group — 78-dim exceptional, 27x27 complex fundamental rep.
//
// E6 = Str_0(J3(O_C)), reduced structure algebra of the complexified
// exceptional Jordan algebra. 78 = 52 (Der) + 26 (L traceless).
//
// E6 ⊂ SU(27): complex unitary representation.
// h∨ = 12, |Φ⁺| = 36, |Z| = 3 (center Z₃, like SU(3)).
//
// Generators loaded from e6_generators.bin (78 × 27 × 27 × complex128).

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

const D: usize = 27;
const N_GEN: usize = 78;

pub struct E6Group {
    generators: Vec<Vec<f64>>, // N_GEN matrices, each 2*D*D f64 (complex, interleaved)
}

impl E6Group {
    pub fn new() -> Self {
        let gen_bytes = include_bytes!("../../e6_generators.bin");
        // 78 generators × 27 × 27 × complex128 (16 bytes per entry)
        assert_eq!(
            gen_bytes.len(),
            N_GEN * D * D * 16,
            "E6 generator file has wrong size"
        );

        let mut generators = Vec::with_capacity(N_GEN);
        for g in 0..N_GEN {
            let mut mat = vec![0.0f64; 2 * D * D];
            for i in 0..D {
                for j in 0..D {
                    let byte_offset = (g * D * D + i * D + j) * 16;
                    let re = f64::from_le_bytes([
                        gen_bytes[byte_offset], gen_bytes[byte_offset+1],
                        gen_bytes[byte_offset+2], gen_bytes[byte_offset+3],
                        gen_bytes[byte_offset+4], gen_bytes[byte_offset+5],
                        gen_bytes[byte_offset+6], gen_bytes[byte_offset+7],
                    ]);
                    let im = f64::from_le_bytes([
                        gen_bytes[byte_offset+8], gen_bytes[byte_offset+9],
                        gen_bytes[byte_offset+10], gen_bytes[byte_offset+11],
                        gen_bytes[byte_offset+12], gen_bytes[byte_offset+13],
                        gen_bytes[byte_offset+14], gen_bytes[byte_offset+15],
                    ]);
                    cset(&mut mat, D, i, j, re, im);
                }
            }
            generators.push(mat);
        }

        E6Group { generators }
    }
}

impl GaugeGroup for E6Group {
    fn name(&self) -> &str { "E6" }
    fn dim_fund(&self) -> usize { D }
    fn dim_adj(&self) -> usize { N_GEN }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { D as f64 }

    fn identity(&self) -> LinkData { cmat_identity(D) }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let mut x = cmat_zero(D);
        for g in &self.generators {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..(2 * D * D) {
                x[i] += c * g[i];
            }
        }
        let u = cmat_expm_taylor12(&x, D);
        cmat_unitarize(&u, D)
    }

    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, D) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, D) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, D) }
    fn trace_im(&self, u: &[f64]) -> f64 { cmat_trace_im(u, D) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, D) }
    fn zero(&self) -> LinkData { cmat_zero(D) }
    fn reproject(&self, u: &[f64]) -> LinkData { cmat_unitarize(u, D) }

    fn n_positive_roots(&self) -> usize { 36 }
    fn dual_coxeter(&self) -> usize { 12 }
    fn center_order(&self) -> usize { 3 }
}
