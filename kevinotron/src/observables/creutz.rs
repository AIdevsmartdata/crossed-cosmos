// kevinotron/src/observables/creutz.rs
// Creutz ratios for string tension extraction.
//
// chi(I, J) = -ln( W(I,J) * W(I-1,J-1) / (W(I,J-1) * W(I-1,J)) )
//
// For I = J and large enough, chi(I,I) -> sigma * a^2 (string tension in lattice units).

/// Compute Creutz ratio chi(I, J).
///
/// Arguments are the four Wilson loop expectation values:
///   w_ij     = <W(I, J)>
///   w_i1j1   = <W(I-1, J-1)>
///   w_ij1    = <W(I, J-1)>
///   w_i1j    = <W(I-1, J)>
///
/// Returns chi = -ln( w_ij * w_i1j1 / (w_ij1 * w_i1j) )
///
/// If any Wilson loop is non-positive (noise), returns NaN.
pub fn creutz_ratio(w_ij: f64, w_i1j1: f64, w_ij1: f64, w_i1j: f64) -> f64 {
    let numer = w_ij * w_i1j1;
    let denom = w_ij1 * w_i1j;
    if numer <= 0.0 || denom <= 0.0 {
        return f64::NAN;
    }
    -(numer / denom).ln()
}

/// Estimate error on Creutz ratio via error propagation from Wilson loop errors.
///
/// delta_chi = sqrt( (dw_ij/w_ij)^2 + (dw_i1j1/w_i1j1)^2
///                 + (dw_ij1/w_ij1)^2 + (dw_i1j/w_i1j)^2 )
pub fn creutz_ratio_err(
    w_ij: f64, dw_ij: f64,
    w_i1j1: f64, dw_i1j1: f64,
    w_ij1: f64, dw_ij1: f64,
    w_i1j: f64, dw_i1j: f64,
) -> f64 {
    if w_ij.abs() < 1e-30 || w_i1j1.abs() < 1e-30
        || w_ij1.abs() < 1e-30 || w_i1j.abs() < 1e-30
    {
        return f64::NAN;
    }
    let s = (dw_ij / w_ij).powi(2)
        + (dw_i1j1 / w_i1j1).powi(2)
        + (dw_ij1 / w_ij1).powi(2)
        + (dw_i1j / w_i1j).powi(2);
    s.sqrt()
}
