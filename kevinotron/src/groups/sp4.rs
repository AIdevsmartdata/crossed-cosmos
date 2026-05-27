// kevinotron/src/groups/sp4.rs
// Sp(4) gauge group -- 10-dim compact symplectic, 4x4 complex fundamental rep.
//
// Sp(4) = { U in U(4) : U^T J U = J }  where J = [[0, I_2], [-I_2, 0]]
// Lie algebra sp(4): anti-Hermitian X with X^T J + J X = 0
// dim(sp(4)) = 10
// beta_norm = d_fund = 4  (C_2(adj) = 3)
//
// Generators: 10 anti-Hermitian 4x4 complex matrices satisfying sp(4) constraint.
//   - 4 symmetric off-diagonal (real part)
//   - 4 antisymmetric off-diagonal (imaginary part)
//   - 1 diagonal traceless (Cartan)
//   - 1 additional from symplectic constraint
//
// Actually built systematically: X in sp(4) iff X = [[A, B], [C, -A^T]]
// with B = B^T, C = C^T, and X anti-Hermitian.
// This means A^dag = A^T (i.e., A^* = A so A is real? No.)
// More carefully: X anti-Hermitian means X^dag = -X.
// X^T J + J X = 0 means X^T = -J X J^{-1} = J X J.
//
// We build the 10 generators explicitly.
//
// Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)

use super::*;
use rand::Rng;
use rand::RngCore;
use rand_distr::StandardNormal;

pub struct SP4Group {
    generators: Vec<Vec<f64>>,
}

impl SP4Group {
    pub fn new() -> Self {
        SP4Group {
            generators: sp4_generators(),
        }
    }
}

/// Build the symplectic form J = [[0, I_2], [-I_2, 0]] as 4x4 complex (flat).
fn symplectic_j() -> Vec<f64> {
    let mut j = cmat_zero(4);
    // J[0,2] = 1, J[1,3] = 1, J[2,0] = -1, J[3,1] = -1
    cset(&mut j, 4, 0, 2, 1.0, 0.0);
    cset(&mut j, 4, 1, 3, 1.0, 0.0);
    cset(&mut j, 4, 2, 0, -1.0, 0.0);
    cset(&mut j, 4, 3, 1, -1.0, 0.0);
    j
}

/// Build 10 generators of sp(4) as anti-Hermitian 4x4 complex matrices.
///
/// Constraint: X^T J + J X = 0  AND  X^dag = -X
///
/// A basis for sp(4) (compact form, anti-Hermitian):
///   Block form X = [[A, B], [C, -A^T]]
///   with A anti-Hermitian 2x2, B = B^T and B^dag = C  (so C = B^T* = B^* since B=B^T)
///   Actually for compact sp: B is symmetric and purely imaginary (iB_real with B_real symmetric real).
///   We build them explicitly.
fn sp4_generators() -> Vec<Vec<f64>> {
    let n = 4;
    let mut candidates = Vec::new();

    // Strategy: enumerate anti-Hermitian 4x4 matrices and check sp(4) constraint.
    // For efficiency, build from known structure.
    //
    // sp(4) generators in compact (anti-Hermitian) form:
    //
    // Type 1: Block-diagonal from su(2) in upper-left + corresponding lower-right
    //   T_a = [[sigma_a, 0], [0, -sigma_a^T]]  (times i/2 for anti-Hermitian)
    //   This gives 3 generators.
    //
    // Type 2: Off-diagonal symmetric blocks
    //   [[0, B], [B^*, 0]]  with B symmetric, and the whole thing anti-Hermitian
    //   B = i*S where S is real symmetric 2x2 => 3 generators (S_11, S_22, S_12=S_21)
    //
    // Type 3: Off-diagonal antisymmetric blocks
    //   [[0, B], [-B^*, 0]]  with B antisymmetric, anti-Hermitian overall
    //   B = i*A where A real antisymmetric 2x2 => 1 generator
    //
    // Type 4: Diagonal traceless with sp constraint
    //   [[D, 0], [0, -D^T]]  with D diagonal pure imaginary traceless
    //   But D already covered in Type 1 (T_3 is diagonal).
    //   Additional: D = diag(i/2, i/2) in upper, diag(-i/2, -i/2) in lower
    //   This is proportional to i*I/2 in each block => trace = 0 total? Yes: i/2+i/2-i/2-i/2=0.
    //   But this is just i*(I_2 block diagonal - ...) = part of u(1)? Check sp constraint.

    // Let me just build all 10 systematically.

    // --- Type 1: su(2) embedded in upper-left block ---
    // T1: [[0, i/2], [i/2, 0]] in 2x2 => 4x4 [[T, 0], [0, -T^T]]
    {
        let mut g = cmat_zero(n);
        // upper-left block: i*sigma_1/2
        cset(&mut g, n, 0, 1, 0.0, 0.5);
        cset(&mut g, n, 1, 0, 0.0, 0.5);
        // lower-right block: -T^T = -i*sigma_1^T/2 = -i*sigma_1/2
        cset(&mut g, n, 2, 3, 0.0, -0.5);
        cset(&mut g, n, 3, 2, 0.0, -0.5);
        candidates.push(g);
    }

    // T2: [[0, 1/2], [-1/2, 0]] in upper, -T^T in lower
    {
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 1, 0.5, 0.0);
        cset(&mut g, n, 1, 0, -0.5, 0.0);
        // -T^T: T = [[0,1/2],[-1/2,0]], T^T = [[0,-1/2],[1/2,0]], -T^T = [[0,1/2],[-1/2,0]]
        cset(&mut g, n, 2, 3, 0.5, 0.0);
        cset(&mut g, n, 3, 2, -0.5, 0.0);
        candidates.push(g);
    }

    // T3: diag(i/2, -i/2) in upper, diag(-i/2, i/2) in lower
    {
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 0, 0.0, 0.5);
        cset(&mut g, n, 1, 1, 0.0, -0.5);
        cset(&mut g, n, 2, 2, 0.0, -0.5);
        cset(&mut g, n, 3, 3, 0.0, 0.5);
        candidates.push(g);
    }

    // --- Type 2: Off-diagonal with symmetric B = i*S (real symmetric S) ---
    // [[0, B], [C, 0]] anti-Hermitian => C = -B^dag
    // sp constraint X^T J + JX = 0 => B must satisfy certain symmetry.
    // For [[0, B], [C, 0]]: X^T = [[0, C^T], [B^T, 0]]
    // X^T J = [[0, C^T], [B^T, 0]] [[0,I],[-I,0]] = [[-C^T, 0], [0, B^T]]
    // JX = [[0,I],[-I,0]] [[0,B],[C,0]] = [[C, 0], [0, -B]]
    // Sum = [[C - C^T, 0], [0, B^T - B]] = 0 => C = C^T and B = B^T
    // Also anti-Hermitian: X^dag = [[0, C^dag], [B^dag, 0]] = -X = [[0, -B], [-C, 0]]
    // => C^dag = -B, B^dag = -C => C = -B^dag
    // Combined with C = C^T: (-B^dag)^T = -B^* = C = C^T = (-B^dag)^T OK self-consistent.
    // And B = B^T.
    // So B is symmetric and C = -B^dag (which is also symmetric since B^dag^T = B^* and B=B^T => B^*=B^dag^T).
    //
    // B symmetric 2x2 complex: B = [[b11, b12], [b12, b22]]
    // Anti-Hermitian constraint on X: the (0,2) block is B, (2,0) block is C = -B^dag
    // For anti-Hermitian X: X_{ij}^* = -X_{ji}
    // X[0,2] = B[0,0] = b11, X[2,0] = C[0,0] = -b11^*
    // X[0,2]^* = b11^* should equal -X[2,0] = b11^* ✓
    // So b11 can be anything. But X is anti-Hermitian means each B entry:
    // X[0,2] = b11 and X[2,0] = -b11^* => anti-Hermitian requires b11^* = b11^* ✓ always true for off-diagonal blocks.
    //
    // Degrees of freedom: B symmetric complex 2x2 = 3 complex = 6 real params.
    // But we need anti-Hermitian overall. The block structure already ensures it via C = -B^dag.
    // So 6 real generators from off-diagonal blocks.

    // B = [[1,0],[0,0]] * i/sqrt(2) (imaginary symmetric)
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        // B[0,0] = i*s => g[0,2]
        cset(&mut g, n, 0, 2, 0.0, s);
        // C = -B^dag => C[0,0] = -(-i*s) = i*s => g[2,0]
        cset(&mut g, n, 2, 0, 0.0, s);
        candidates.push(g);
    }

    // B = [[0,0],[0,1]] * i/sqrt(2)
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 1, 3, 0.0, s);
        cset(&mut g, n, 3, 1, 0.0, s);
        candidates.push(g);
    }

    // B = [[0,1],[1,0]] * i/sqrt(2)  (symmetric off-diagonal imaginary)
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 3, 0.0, s);
        cset(&mut g, n, 1, 2, 0.0, s);
        cset(&mut g, n, 2, 1, 0.0, s);
        cset(&mut g, n, 3, 0, 0.0, s);
        candidates.push(g);
    }

    // B = [[1,0],[0,0]] * 1/sqrt(2) (real symmetric) => B real symmetric, C = -B^dag = -B^T = -B
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 2, s, 0.0);
        cset(&mut g, n, 2, 0, -s, 0.0);
        candidates.push(g);
    }

    // B = [[0,0],[0,1]] real symmetric
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 1, 3, s, 0.0);
        cset(&mut g, n, 3, 1, -s, 0.0);
        candidates.push(g);
    }

    // B = [[0,1],[1,0]] real symmetric off-diagonal
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 3, s, 0.0);
        cset(&mut g, n, 1, 2, s, 0.0);
        cset(&mut g, n, 2, 1, -s, 0.0);
        cset(&mut g, n, 3, 0, -s, 0.0);
        candidates.push(g);
    }

    // --- Type 4: Additional diagonal ---
    // diag(i/2, i/2, -i/2, -i/2) : trace = 0, check sp constraint
    // X = diag(ia, ia, -ia, -ia) with a = 1/2
    // X^T = X (diagonal), J = [[0,I],[-I,0]]
    // X^T J + JX = XJ + JX = ?
    // XJ: row 0: (ia)(J row 0) = ia*(0,0,1,0) = (0,0,ia,0)
    //     row 1: ia*(0,0,0,1) = (0,0,0,ia)
    //     row 2: -ia*(-1,0,0,0) = (ia,0,0,0)
    //     row 3: -ia*(0,-1,0,0) = (0,ia,0,0)
    // JX: row 0 of J is (0,0,1,0), times X columns: (0,0,-ia,0)... wait
    // J[0,:] = (0,0,1,0), so (JX)[0,j] = X[2,j] = {-ia if j=2, else 0}
    // Actually JX[i,j] = sum_k J[i,k] X[k,j]. Since X is diagonal, JX[i,j] = J[i,j] X[j,j].
    // XJ[i,j] = X[i,i] J[i,j].
    // XJ + JX: [i,j] = (X[i,i] + X[j,j]) J[i,j]
    // For this to be 0: whenever J[i,j] != 0, need X[i,i] + X[j,j] = 0.
    // J[0,2]=1: X[0,0]+X[2,2] = ia + (-ia) = 0 ✓
    // J[1,3]=1: X[1,1]+X[3,3] = ia + (-ia) = 0 ✓
    // J[2,0]=-1: X[2,2]+X[0,0] = 0 ✓
    // J[3,1]=-1: X[3,3]+X[1,1] = 0 ✓
    // Good! This is a valid sp(4) generator.
    {
        let s = 0.5;
        let mut g = cmat_zero(n);
        cset(&mut g, n, 0, 0, 0.0, s);
        cset(&mut g, n, 1, 1, 0.0, s);
        cset(&mut g, n, 2, 2, 0.0, -s);
        cset(&mut g, n, 3, 3, 0.0, -s);
        candidates.push(g);
    }

    // Verify we have 10
    assert_eq!(candidates.len(), 10, "Expected 10 Sp(4) generators, got {}", candidates.len());

    // Verify anti-Hermitian and sp(4) constraint for each generator
    let j = symplectic_j();
    for (idx, g) in candidates.iter().enumerate() {
        // Check anti-Hermitian: g + g^dag = 0
        let gd = cmat_dagger(g, n);
        let sum = cmat_add(g, &gd, n);
        let norm_ah: f64 = sum.iter().map(|x| x * x).sum::<f64>();
        assert!(norm_ah < 1e-14, "Generator {} not anti-Hermitian (norm={})", idx, norm_ah);

        // Check X^T J + J X = 0
        // X^T = transpose (not conjugate transpose)
        let gt = cmat_transpose_no_conj(g, n);
        let gtj = cmat_mul(&gt, &j, n);
        let jg = cmat_mul(&j, g, n);
        let sp_sum = cmat_add(&gtj, &jg, n);
        let norm_sp: f64 = sp_sum.iter().map(|x| x * x).sum::<f64>();
        assert!(norm_sp < 1e-14, "Generator {} fails sp(4) constraint (norm={})", idx, norm_sp);
    }

    // Normalize: Tr(T_a T_b) = -delta_ab / 2
    let mut normalized = Vec::new();
    for g in &candidates {
        let g2 = cmat_mul(g, g, n);
        let tr = cmat_trace_re(&g2, n); // Should be negative
        let target = -0.5; // Tr(T^2) = -1/2
        let scale = (target / tr).abs().sqrt();
        let g_scaled: Vec<f64> = g.iter().map(|x| x * scale).collect();
        normalized.push(g_scaled);
    }

    normalized
}

/// Transpose without complex conjugation (just swap indices).
fn cmat_transpose_no_conj(a: &[f64], n: usize) -> LinkData {
    let mut t = vec![0.0f64; 2 * n * n];
    for i in 0..n {
        for j in 0..n {
            let (re, im) = cget(a, n, i, j);
            cset(&mut t, n, j, i, re, im);
        }
    }
    t
}

/// Reproject onto Sp(4): Gram-Schmidt unitarize, then enforce symplectic constraint.
/// Uses iterative projection: U -> U, then adjust to satisfy U^T J U = J.
fn sp4_reproject(u: &[f64]) -> LinkData {
    let n = 4;
    // First unitarize
    let mut w = cmat_unitarize(u, n);

    // Iterative symplectic projection (Newton-like):
    // If U^T J U ≈ J, then U_new = U * (3I - U^T J U J^{-1}) / 2
    // is closer to Sp(4). Repeat a few times.
    let j = symplectic_j();
    // J^{-1} = J^T = -J (since J is antisymmetric and J^2 = -I)
    let j_inv: Vec<f64> = j.iter().map(|x| -x).collect();

    for _ in 0..5 {
        let wt = cmat_transpose_no_conj(&w, n);
        let wtj = cmat_mul(&wt, &j, n);
        let wtjw = cmat_mul(&wtj, &w, n);
        // Check convergence: wtjw should be J
        let diff: f64 = wtjw.iter().zip(j.iter()).map(|(a, b)| (a - b).powi(2)).sum::<f64>();
        if diff < 1e-24 {
            break;
        }
        // Correction: w_new = w * (3I - wtjw * J^{-1}) / 2
        let wtjw_jinv = cmat_mul(&wtjw, &j_inv, n);
        let three_i = {
            let mut m = cmat_identity(n);
            for i in 0..2*n*n { m[i] *= 3.0; }
            m
        };
        let corr: Vec<f64> = three_i.iter().zip(wtjw_jinv.iter()).map(|(a, b)| (a - b) * 0.5).collect();
        w = cmat_mul(&w, &corr, n);
        // Re-unitarize after correction
        w = cmat_unitarize(&w, n);
    }

    w
}

impl GaugeGroup for SP4Group {
    fn name(&self) -> &str { "Sp(4)" }
    fn dim_fund(&self) -> usize { 4 }
    fn dim_adj(&self) -> usize { 10 }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { 4.0 } // d_fund = 4

    fn identity(&self) -> LinkData { cmat_identity(4) }

    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let mut a = cmat_zero(4);
        for g in &self.generators {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..a.len() {
                a[i] += g[i] * c;
            }
        }
        let u = cmat_expm_taylor12(&a, 4);
        sp4_reproject(&u)
    }

    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, 4) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, 4) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, 4) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, 4) }
    fn zero(&self) -> LinkData { cmat_zero(4) }

    fn reproject(&self, u: &[f64]) -> LinkData {
        sp4_reproject(u)
    }
}
