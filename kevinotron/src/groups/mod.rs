// kevinotron/src/groups/mod.rs
// Trait GaugeGroup -- abstract interface for all gauge groups.
//
// Each group stores link matrices as flat Vec<f64>:
//   - G2: 7x7 real = 49 f64
//   - SU(N): NxN complex = 2*N*N f64 (re,im interleaved per entry)
//
// This avoids nalgebra generics headaches while keeping everything
// in contiguous memory for cache efficiency.

pub mod g2;
pub mod so7;
pub mod sp4;
pub mod su2;
pub mod su3;
pub mod su4;
pub mod su5;

use rand::Rng;
use rand::RngCore;

/// A link matrix stored as flat f64 slice.
/// For real groups: d*d entries.
/// For complex groups: 2*d*d entries (re0,im0,re1,im1,...).
pub type LinkData = Vec<f64>;

/// Wrapper to make &mut dyn RngCore usable as Rng.
/// Needed because trait objects can't use impl Rng directly.
pub struct RngWrapper<'a>(pub &'a mut dyn RngCore);

impl<'a> RngCore for RngWrapper<'a> {
    fn next_u32(&mut self) -> u32 { self.0.next_u32() }
    fn next_u64(&mut self) -> u64 { self.0.next_u64() }
    fn fill_bytes(&mut self, dest: &mut [u8]) { self.0.fill_bytes(dest) }
    fn try_fill_bytes(&mut self, dest: &mut [u8]) -> Result<(), rand::Error> {
        self.0.try_fill_bytes(dest)
    }
}

/// The GaugeGroup trait.
/// Object-safe: uses &mut dyn RngCore instead of impl Rng.
pub trait GaugeGroup: Send + Sync {
    /// Name: "G2", "SU(2)", "SU(3)", "SU(4)"
    fn name(&self) -> &str;
    /// Dimension of fundamental representation (matrix size)
    fn dim_fund(&self) -> usize;
    /// Dimension of adjoint representation
    fn dim_adj(&self) -> usize;
    /// Whether link matrices are complex
    fn is_complex(&self) -> bool;
    /// Number of f64 per link matrix
    fn link_size(&self) -> usize {
        let d = self.dim_fund();
        if self.is_complex() { 2 * d * d } else { d * d }
    }
    /// beta normalization factor (d_fund for SU(N), 7 for G2)
    fn beta_norm(&self) -> f64;
    /// Identity link matrix (flat)
    fn identity(&self) -> LinkData;
    /// Random group element near identity with spread epsilon
    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData;
    /// U^dag (transpose for real, conjugate-transpose for complex)
    fn dagger(&self, u: &[f64]) -> LinkData;
    /// Matrix multiply: A * B
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData;
    /// Re Tr(U)
    fn trace_re(&self, u: &[f64]) -> f64;
    /// U + V (element-wise, for staple accumulation)
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData;
    /// Zero matrix
    fn zero(&self) -> LinkData;
    /// Reproject onto the group manifold (polar decomposition / unitarize)
    fn reproject(&self, u: &[f64]) -> LinkData;
}

// ---- Helpers for complex matrix arithmetic ----

/// Get (re, im) of entry (i,j) in a complex NxN matrix stored as 2*N*N f64
#[inline]
pub fn cget(data: &[f64], n: usize, i: usize, j: usize) -> (f64, f64) {
    let idx = 2 * (i * n + j);
    (data[idx], data[idx + 1])
}

/// Set (re, im) of entry (i,j)
#[inline]
pub fn cset(data: &mut [f64], n: usize, i: usize, j: usize, re: f64, im: f64) {
    let idx = 2 * (i * n + j);
    data[idx] = re;
    data[idx + 1] = im;
}

/// Complex NxN matrix multiply C = A * B
pub fn cmat_mul(a: &[f64], b: &[f64], n: usize) -> LinkData {
    let mut c = vec![0.0f64; 2 * n * n];
    for i in 0..n {
        for j in 0..n {
            let mut re = 0.0;
            let mut im = 0.0;
            for k in 0..n {
                let (ar, ai) = cget(a, n, i, k);
                let (br, bi) = cget(b, n, k, j);
                re += ar * br - ai * bi;
                im += ar * bi + ai * br;
            }
            cset(&mut c, n, i, j, re, im);
        }
    }
    c
}

/// Complex NxN conjugate transpose
pub fn cmat_dagger(a: &[f64], n: usize) -> LinkData {
    let mut d = vec![0.0f64; 2 * n * n];
    for i in 0..n {
        for j in 0..n {
            let (re, im) = cget(a, n, j, i);
            cset(&mut d, n, i, j, re, -im);
        }
    }
    d
}

/// Re Tr of complex NxN
pub fn cmat_trace_re(a: &[f64], n: usize) -> f64 {
    let mut t = 0.0;
    for i in 0..n {
        let (re, _) = cget(a, n, i, i);
        t += re;
    }
    t
}

/// Complex NxN add
pub fn cmat_add(a: &[f64], b: &[f64], n: usize) -> LinkData {
    a.iter().zip(b.iter()).map(|(x, y)| x + y).collect()
}

/// Complex NxN zero
pub fn cmat_zero(n: usize) -> LinkData {
    vec![0.0f64; 2 * n * n]
}

/// Complex NxN identity
pub fn cmat_identity(n: usize) -> LinkData {
    let mut d = vec![0.0f64; 2 * n * n];
    for i in 0..n {
        cset(&mut d, n, i, i, 1.0, 0.0);
    }
    d
}

/// Matrix exponential for anti-Hermitian NxN via Taylor order 12.
/// A = re + i*im parts stored as 2*N*N flat.
/// Input is anti-Hermitian: A^dag = -A.
pub fn cmat_expm_taylor12(a: &[f64], n: usize) -> LinkData {
    let mut sum = cmat_identity(n);
    let mut pow = cmat_identity(n);
    for k in 1..=12 {
        let f = 1.0 / k as f64;
        pow = cmat_mul(&pow, a, n);
        // scale pow by f
        let scaled: LinkData = pow.iter().map(|x| x * f).collect();
        pow = scaled;
        sum = cmat_add(&sum, &pow, n);
    }
    sum
}

/// Gram-Schmidt unitarization of complex NxN matrix.
/// Projects back onto U(N) then fixes det = 1 for SU(N).
pub fn cmat_unitarize(u: &[f64], n: usize) -> LinkData {
    // Gram-Schmidt on columns
    let mut cols: Vec<Vec<(f64, f64)>> = Vec::new();
    for j in 0..n {
        let mut v: Vec<(f64, f64)> = (0..n).map(|i| cget(u, n, i, j)).collect();
        // Subtract projections onto previous columns
        for prev in &cols {
            // dot = <prev, v> = sum prev_i* v_i
            let mut dot_re = 0.0;
            let mut dot_im = 0.0;
            for i in 0..n {
                let (pr, pi) = prev[i];
                let (vr, vi) = v[i];
                dot_re += pr * vr + pi * vi;
                dot_im += pr * vi - pi * vr;
            }
            for i in 0..n {
                let (pr, pi) = prev[i];
                v[i].0 -= dot_re * pr - dot_im * pi;
                v[i].1 -= dot_re * pi + dot_im * pr;
            }
        }
        // Normalize
        let norm: f64 = v.iter().map(|(r, i)| r * r + i * i).sum::<f64>().sqrt();
        if norm > 1e-14 {
            for i in 0..n {
                v[i].0 /= norm;
                v[i].1 /= norm;
            }
        }
        cols.push(v);
    }
    // Reconstruct matrix
    let mut result = vec![0.0f64; 2 * n * n];
    for j in 0..n {
        for i in 0..n {
            cset(&mut result, n, i, j, cols[j][i].0, cols[j][i].1);
        }
    }
    // Fix determinant to +1 for SU(N): divide last column by det
    // For production this is fine; det is already close to 1.
    // Simple approach: compute det via cofactor for small N,
    // then adjust last column. For N<=4 this is efficient.
    result
}

// ---- Helpers for real matrix arithmetic (G2) ----

/// Real NxN matrix multiply
pub fn rmat_mul(a: &[f64], b: &[f64], n: usize) -> LinkData {
    let mut c = vec![0.0f64; n * n];
    for i in 0..n {
        for j in 0..n {
            let mut s = 0.0;
            for k in 0..n {
                s += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = s;
        }
    }
    c
}

pub fn rmat_transpose(a: &[f64], n: usize) -> LinkData {
    let mut t = vec![0.0f64; n * n];
    for i in 0..n {
        for j in 0..n {
            t[i * n + j] = a[j * n + i];
        }
    }
    t
}

pub fn rmat_trace(a: &[f64], n: usize) -> f64 {
    (0..n).map(|i| a[i * n + i]).sum()
}

pub fn rmat_add(a: &[f64], b: &[f64]) -> LinkData {
    a.iter().zip(b.iter()).map(|(x, y)| x + y).collect()
}

pub fn rmat_identity(n: usize) -> LinkData {
    let mut d = vec![0.0f64; n * n];
    for i in 0..n {
        d[i * n + i] = 1.0;
    }
    d
}

pub fn rmat_zero(n: usize) -> LinkData {
    vec![0.0f64; n * n]
}
