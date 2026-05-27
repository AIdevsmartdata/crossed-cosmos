// g2_analyze — G_2 lattice EE analysis binary
//
// Reads g2_ee log files, performs:
//   - Trapezoidal alpha-integration per L
//   - Jackknife error estimation on S_2
//   - Multi-L fit: S_2/Area = a_div + kappa/L + c/L^2
//   - Comparison to 4 kappa_EE predictions with tension in sigma
//
// Usage:
//   g2_analyze --ee g2_ee_L4_beta10.0.log g2_ee_L6_beta10.0.log g2_ee_L8_beta10.log
//
// Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)

use clap::Parser;
use std::fs;

// ============================================================
// Predictions for kappa_EE(G_2)
// ============================================================

const ZETA3: f64 = 1.2020569031595942;
const SQRT_PI: f64 = 1.7724538509055159;
const KAPPA_INF: f64 = ZETA3 / SQRT_PI; // 0.67819...

struct Prediction {
    name: &'static str,
    value: f64,
    description: &'static str,
}

fn predictions() -> Vec<Prediction> {
    vec![
        Prediction {
            name: "P1_SU3_rank",
            value: (1.0 - 1.0 / 9.0) * KAPPA_INF,
            description: "(1-1/N^2)*zeta(3)/sqrt(pi), N=rank+1=3",
        },
        Prediction {
            name: "P2_dim_law",
            value: (1.0 - 1.0 / 14.0) * KAPPA_INF,
            description: "(1-1/dim)*zeta(3)/sqrt(pi), dim=14",
        },
        Prediction {
            name: "P3_sqrt_N",
            value: 0.518 * (2.0_f64).sqrt() - 0.458,
            description: "0.518*sqrt(rank)-0.458, rank=2",
        },
        Prediction {
            name: "P4_kappa_FP",
            value: 1.0 / 12.0,
            description: "kappa_FP = 1/(2|Phi+|) = 1/12",
        },
    ]
}

// ============================================================
// Log parsing
// ============================================================

#[derive(Debug, Clone)]
struct AlphaPoint {
    alpha: f64,
    ds_mean: f64,
    ds_err: f64,
    raw_measurements: Vec<f64>, // from .dat files if available
}

#[derive(Debug, Clone)]
struct EEData {
    ls: usize,
    lt: usize,
    beta: f64,
    alpha_points: Vec<AlphaPoint>,
    s2_reported: Option<f64>,
    s2_err_reported: Option<f64>,
    area: Option<f64>,
    source_file: String,
}

fn parse_ee_log(path: &str) -> Result<EEData, String> {
    let content = fs::read_to_string(path)
        .map_err(|e| format!("Cannot read {}: {}", path, e))?;

    let mut ls: Option<usize> = None;
    let mut lt: Option<usize> = None;
    let mut beta: Option<f64> = None;
    let mut alpha_points: Vec<AlphaPoint> = Vec::new();
    let mut s2_reported: Option<f64> = None;
    let mut s2_err_reported: Option<f64> = None;
    let mut area: Option<f64> = None;

    for line in content.lines() {
        let line = line.trim();

        // Parse header: "# Ls=8, Lt=16, beta=10"
        if line.starts_with("# Ls=") {
            for part in line.split(',') {
                let part = part.trim().trim_start_matches("# ");
                if let Some(v) = part.strip_prefix("Ls=") {
                    ls = v.parse().ok();
                } else if let Some(v) = part.strip_prefix("Lt=") {
                    lt = v.parse().ok();
                } else if let Some(v) = part.strip_prefix("beta=") {
                    beta = v.parse().ok();
                }
            }
        }

        // Parse alpha measurements: "ALPHA 0.100: dS/dalpha = 123.456 +/- 0.789"
        if line.starts_with("ALPHA") {
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() >= 6 {
                let alpha_str = parts[1].trim_end_matches(':');
                if let (Ok(a), Ok(ds), Ok(err)) = (
                    alpha_str.parse::<f64>(),
                    parts[3].parse::<f64>(),
                    parts[5].parse::<f64>(),
                ) {
                    alpha_points.push(AlphaPoint {
                        alpha: a,
                        ds_mean: ds,
                        ds_err: err,
                        raw_measurements: Vec::new(),
                    });
                }
            }
        }

        // Parse result: "RESULT: S2=123.456 +/- 0.789"
        if line.starts_with("RESULT: S2=") {
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() >= 4 {
                if let Some(v) = parts[1].strip_prefix("S2=") {
                    s2_reported = v.parse().ok();
                }
                s2_err_reported = parts[3].parse().ok();
            }
        }

        // Parse area: "RESULT: area=512"
        if line.starts_with("RESULT: area=") {
            if let Some(v) = line.strip_prefix("RESULT: area=") {
                area = v.trim().parse().ok();
            }
        }
    }

    // Also try loading .dat file for raw measurements (g2_ee_v2 output)
    let dat_path = path.replace(".log", ".dat");
    if let Ok(dat_content) = fs::read_to_string(&dat_path) {
        load_raw_measurements(&dat_content, &mut alpha_points);
    }

    let ls = ls.ok_or_else(|| format!("{}: missing Ls", path))?;
    let lt = lt.ok_or_else(|| format!("{}: missing Lt", path))?;
    let beta = beta.ok_or_else(|| format!("{}: missing beta", path))?;

    if alpha_points.is_empty() {
        return Err(format!("{}: no ALPHA lines found", path));
    }

    // Sort by alpha
    alpha_points.sort_by(|a, b| a.alpha.partial_cmp(&b.alpha).unwrap());

    Ok(EEData {
        ls,
        lt,
        beta,
        alpha_points,
        s2_reported,
        s2_err_reported,
        area,
        source_file: path.to_string(),
    })
}

fn load_raw_measurements(dat_content: &str, alpha_points: &mut [AlphaPoint]) {
    // .dat format: "alpha_idx config_idx dS_dalpha_value"
    for line in dat_content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() >= 3 {
            if let (Ok(a_idx), Ok(val)) = (
                parts[0].parse::<usize>(),
                parts[2].parse::<f64>(),
            ) {
                if a_idx < alpha_points.len() {
                    alpha_points[a_idx].raw_measurements.push(val);
                }
            }
        }
    }
}

// ============================================================
// Integration and error analysis
// ============================================================

/// Trapezoidal integration of dS/dalpha over alpha in [0, 1]
fn trapezoidal_integrate(points: &[AlphaPoint]) -> (f64, f64) {
    let n = points.len();
    if n < 2 {
        return (0.0, 0.0);
    }
    let mut s2 = 0.0;
    let mut err_sq = 0.0;
    for i in 0..(n - 1) {
        let da = points[i + 1].alpha - points[i].alpha;
        s2 += da * 0.5 * (points[i].ds_mean + points[i + 1].ds_mean);
        err_sq += (da * 0.5).powi(2) * (points[i].ds_err.powi(2) + points[i + 1].ds_err.powi(2));
    }
    (s2, err_sq.sqrt())
}

/// Jackknife error estimation on S_2 from raw per-config measurements.
/// Each jackknife sample drops one config across ALL alpha points,
/// recomputes per-alpha means, then integrates.
fn jackknife_s2(points: &[AlphaPoint]) -> Option<(f64, f64)> {
    // Check all alpha points have the same number of raw measurements
    let n_meas = points[0].raw_measurements.len();
    if n_meas < 3 {
        return None;
    }
    for p in points {
        if p.raw_measurements.len() != n_meas {
            return None; // cannot do correlated jackknife
        }
    }

    // Full-sample S_2
    let full_means: Vec<f64> = points
        .iter()
        .map(|p| p.raw_measurements.iter().sum::<f64>() / n_meas as f64)
        .collect();

    let mut full_s2 = 0.0;
    for i in 0..(points.len() - 1) {
        let da = points[i + 1].alpha - points[i].alpha;
        full_s2 += da * 0.5 * (full_means[i] + full_means[i + 1]);
    }

    // Jackknife resamples: drop config j
    let n = n_meas;
    let mut jk_s2 = Vec::with_capacity(n);
    for j in 0..n {
        let jk_means: Vec<f64> = points
            .iter()
            .map(|p| {
                let sum: f64 = p.raw_measurements.iter().sum::<f64>() - p.raw_measurements[j];
                sum / (n - 1) as f64
            })
            .collect();

        let mut s2_j = 0.0;
        for i in 0..(points.len() - 1) {
            let da = points[i + 1].alpha - points[i].alpha;
            s2_j += da * 0.5 * (jk_means[i] + jk_means[i + 1]);
        }
        jk_s2.push(s2_j);
    }

    let jk_mean = jk_s2.iter().sum::<f64>() / n as f64;
    let jk_var = jk_s2.iter().map(|x| (x - jk_mean).powi(2)).sum::<f64>()
        * (n - 1) as f64 / n as f64;
    let jk_err = jk_var.sqrt();

    Some((full_s2, jk_err))
}

// ============================================================
// Multi-L kappa extraction via least-squares fit
// ============================================================

struct FitResult {
    kappa: f64,
    kappa_err: f64,
    a_div: f64,
    chi2: f64,
    dof: usize,
    method: &'static str,
}

/// Fit S_2/Area = a + kappa/L + c/L^2 via weighted least squares.
/// For the geometry: Area = L^2 * T with T = Lt.
///
/// With >= 3 data points: quadratic fit (a + b/L + c/L^2)
/// With 2 data points: linear fit (a + b/L)
///
/// Returns kappa (the 1/L coefficient = universal sub-leading).
fn fit_kappa(data_list: &[(f64, f64, f64)]) -> Option<FitResult> {
    // data_list entries: (L, s2_per_area, s2_per_area_err)
    let n = data_list.len();
    if n < 2 {
        return None;
    }

    if n >= 3 {
        // Weighted least squares: y = a + b*x + c*x^2 where x = 1/L
        fit_quadratic(data_list)
    } else {
        // Two points: y = a + b*x
        fit_linear(data_list)
    }
}

fn fit_linear(data: &[(f64, f64, f64)]) -> Option<FitResult> {
    // y = a + b*x, x = 1/L, weighted by 1/sigma^2
    let n = data.len();
    if n < 2 {
        return None;
    }

    let mut sw = 0.0;
    let mut swx = 0.0;
    let mut swy = 0.0;
    let mut swxx = 0.0;
    let mut swxy = 0.0;

    for &(l, y, yerr) in data {
        let x = 1.0 / l;
        let w = 1.0 / (yerr * yerr);
        sw += w;
        swx += w * x;
        swy += w * y;
        swxx += w * x * x;
        swxy += w * x * y;
    }

    let det = sw * swxx - swx * swx;
    if det.abs() < 1e-30 {
        return None;
    }

    let a = (swxx * swy - swx * swxy) / det;
    let b = (sw * swxy - swx * swy) / det;

    let var_b = sw / det;
    let b_err = (1.0 / var_b).sqrt();

    // Chi-squared
    let mut chi2 = 0.0;
    for &(l, y, yerr) in data {
        let x = 1.0 / l;
        let resid = y - a - b * x;
        chi2 += (resid / yerr).powi(2);
    }

    let dof = if n > 2 { n - 2 } else { 0 };

    Some(FitResult {
        kappa: b,
        kappa_err: b_err,
        a_div: a,
        chi2,
        dof,
        method: "linear (a + kappa/L)",
    })
}

fn fit_quadratic(data: &[(f64, f64, f64)]) -> Option<FitResult> {
    // y = a + b*x + c*x^2, x = 1/L, weighted
    // Normal equations: (X^T W X) beta = X^T W y
    let n = data.len();
    if n < 3 {
        return None;
    }

    // Build 3x3 system
    let mut xtw_x = [[0.0f64; 3]; 3];
    let mut xtw_y = [0.0f64; 3];

    for &(l, y, yerr) in data {
        let x = 1.0 / l;
        let w = 1.0 / (yerr * yerr);
        let xp = [1.0, x, x * x]; // basis: 1, 1/L, 1/L^2
        for i in 0..3 {
            for j in 0..3 {
                xtw_x[i][j] += w * xp[i] * xp[j];
            }
            xtw_y[i] += w * xp[i] * y;
        }
    }

    // Solve 3x3 by Cramer's rule
    let beta = solve_3x3(&xtw_x, &xtw_y)?;
    let cov = invert_3x3(&xtw_x)?;

    let a = beta[0];
    let b = beta[1]; // kappa
    let b_err = cov[1][1].sqrt();

    let mut chi2 = 0.0;
    for &(l, y, yerr) in data {
        let x = 1.0 / l;
        let resid = y - a - b * x - beta[2] * x * x;
        chi2 += (resid / yerr).powi(2);
    }

    let dof = if n > 3 { n - 3 } else { 0 };

    Some(FitResult {
        kappa: b,
        kappa_err: b_err,
        a_div: a,
        chi2,
        dof,
        method: "quadratic (a + kappa/L + c/L^2)",
    })
}

fn det_3x3(m: &[[f64; 3]; 3]) -> f64 {
    m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
}

fn solve_3x3(a: &[[f64; 3]; 3], b: &[f64; 3]) -> Option<[f64; 3]> {
    let d = det_3x3(a);
    if d.abs() < 1e-30 {
        return None;
    }
    let mut result = [0.0; 3];
    for col in 0..3 {
        let mut m = *a;
        for row in 0..3 {
            m[row][col] = b[row];
        }
        result[col] = det_3x3(&m) / d;
    }
    Some(result)
}

fn invert_3x3(m: &[[f64; 3]; 3]) -> Option<[[f64; 3]; 3]> {
    let d = det_3x3(m);
    if d.abs() < 1e-30 {
        return None;
    }
    let mut inv = [[0.0f64; 3]; 3];
    // Cofactor matrix transposed / det
    inv[0][0] = (m[1][1] * m[2][2] - m[1][2] * m[2][1]) / d;
    inv[0][1] = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / d;
    inv[0][2] = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / d;
    inv[1][0] = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) / d;
    inv[1][1] = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / d;
    inv[1][2] = (m[0][2] * m[1][0] - m[0][0] * m[1][2]) / d;
    inv[2][0] = (m[1][0] * m[2][1] - m[1][1] * m[2][0]) / d;
    inv[2][1] = (m[0][1] * m[2][0] - m[0][0] * m[2][1]) / d;
    inv[2][2] = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) / d;
    Some(inv)
}

// ============================================================
// Sanity checks
// ============================================================

fn run_sanity_checks(data: &EEData) {
    println!("  Sanity checks:");

    // Check alpha=0 exists
    let has_a0 = data.alpha_points.first().map_or(false, |p| p.alpha.abs() < 1e-6);
    println!(
        "    [{}] alpha=0 point present",
        if has_a0 { "OK" } else { "WARN" }
    );

    // Check alpha=1 exists
    let has_a1 = data
        .alpha_points
        .last()
        .map_or(false, |p| (p.alpha - 1.0).abs() < 1e-6);
    println!(
        "    [{}] alpha=1 point present",
        if has_a1 { "OK" } else { "WARN" }
    );

    // Monotonicity: dS/dalpha should generally decrease or stay similar
    let n = data.alpha_points.len();
    if n >= 3 {
        let first = data.alpha_points[0].ds_mean;
        let last = data.alpha_points[n - 1].ds_mean;
        // Just check endpoints, don't require strict monotonicity
        println!(
            "    [INFO] dS/dalpha: {:.2} (alpha=0) -> {:.2} (alpha=1)",
            first, last
        );
    }

    // Check number of alpha points
    println!(
        "    [{}] n_alpha = {} (need >= 11 for precision)",
        if n >= 11 { "OK" } else { "WARN" },
        n
    );

    // Check raw measurements available
    let has_raw = data.alpha_points.iter().any(|p| !p.raw_measurements.is_empty());
    println!(
        "    [{}] Raw measurements for jackknife: {}",
        if has_raw { "OK" } else { "INFO" },
        if has_raw { "available" } else { "not found (using propagated errors)" }
    );
}

// ============================================================
// CLI
// ============================================================

#[derive(Parser)]
#[command(name = "g2_analyze", about = "G_2 Lattice EE Analysis")]
struct Args {
    /// EE log files to analyze (from g2_ee or g2_ee_v2)
    #[arg(long = "ee", num_args = 1..)]
    ee_files: Vec<String>,

    /// Print prediction scenarios and exit
    #[arg(long)]
    scenarios: bool,

    /// Verbose output (print alpha-by-alpha details)
    #[arg(long, short)]
    verbose: bool,
}

// ============================================================
// Main
// ============================================================

fn main() {
    let args = Args::parse();

    if args.scenarios {
        print_scenarios();
        return;
    }

    if args.ee_files.is_empty() {
        eprintln!("Error: no log files provided. Use --ee <file1> <file2> ...");
        std::process::exit(1);
    }

    println!("================================================================");
    println!("  G_2 Lattice EE Analysis — kappa_EE Extraction");
    println!("================================================================");
    println!();

    let preds = predictions();
    println!("Target predictions:");
    for p in &preds {
        println!("  {:16} = {:.4}  ({})", p.name, p.value, p.description);
    }
    println!();

    // Parse all log files
    let mut all_data: Vec<EEData> = Vec::new();
    for path in &args.ee_files {
        match parse_ee_log(path) {
            Ok(data) => {
                println!("Loaded: {} (Ls={}, Lt={}, beta={:.1}, {} alpha-points)",
                         path, data.ls, data.lt, data.beta, data.alpha_points.len());
                all_data.push(data);
            }
            Err(e) => {
                eprintln!("WARNING: {}", e);
            }
        }
    }

    if all_data.is_empty() {
        eprintln!("Error: no valid log files loaded.");
        std::process::exit(1);
    }

    // Sort by L
    all_data.sort_by_key(|d| d.ls);

    println!();
    println!("================================================================");
    println!("  Per-L Analysis");
    println!("================================================================");

    // Per-L analysis: integrate and compute S_2
    let mut fit_points: Vec<(f64, f64, f64)> = Vec::new(); // (L, S2/Area, err)

    for data in &all_data {
        println!();
        println!("--- Ls={}, Lt={}, beta={:.1} ({}) ---",
                 data.ls, data.lt, data.beta, data.source_file);

        run_sanity_checks(data);

        // Alpha integration: compute S_2
        let (s2_trap, s2_trap_err) = trapezoidal_integrate(&data.alpha_points);

        // Try jackknife if raw data available
        let (s2, s2_err, method) = match jackknife_s2(&data.alpha_points) {
            Some((s2_jk, s2_jk_err)) => {
                println!("  Jackknife: S_2 = {:.4} +/- {:.4} ({} configs)",
                         s2_jk, s2_jk_err, data.alpha_points[0].raw_measurements.len());
                println!("  Trapez:    S_2 = {:.4} +/- {:.4} (propagated)",
                         s2_trap, s2_trap_err);
                (s2_jk, s2_jk_err, "jackknife")
            }
            None => {
                println!("  Trapez:    S_2 = {:.4} +/- {:.4} (propagated)",
                         s2_trap, s2_trap_err);
                (s2_trap, s2_trap_err, "propagated")
            }
        };

        // Cross-check with reported S_2 if available
        if let (Some(s2r), Some(s2r_err)) = (data.s2_reported, data.s2_err_reported) {
            let diff = (s2 - s2r).abs();
            let status = if diff < 3.0 * s2_err.max(s2r_err) { "OK" } else { "MISMATCH" };
            println!("  Reported:  S_2 = {:.4} +/- {:.4} [{}]", s2r, s2r_err, status);
        }

        let area = data.area.unwrap_or((data.ls as f64).powi(2) * data.lt as f64);
        let s2_per_area = s2 / area;
        let s2_per_area_err = s2_err / area;

        println!("  Area = {:.0}", area);
        println!("  S_2/Area = {:.6} +/- {:.6} ({})", s2_per_area, s2_per_area_err, method);

        if args.verbose {
            println!("  Alpha-by-alpha:");
            for p in &data.alpha_points {
                let raw_str = if !p.raw_measurements.is_empty() {
                    format!(" [n={}]", p.raw_measurements.len())
                } else {
                    String::new()
                };
                println!("    alpha={:.3}: dS/dalpha = {:12.4} +/- {:8.4}{}",
                         p.alpha, p.ds_mean, p.ds_err, raw_str);
            }
        }

        fit_points.push((data.ls as f64, s2_per_area, s2_per_area_err));
    }

    // Multi-L kappa extraction
    println!();
    println!("================================================================");
    println!("  Multi-L kappa_EE Extraction");
    println!("================================================================");
    println!();

    if fit_points.len() < 2 {
        println!("  Need >= 2 L values for kappa extraction.");
        println!("  Available: {} L value(s)", fit_points.len());
        if let Some(&(l, s2a, s2a_err)) = fit_points.first() {
            println!();
            println!("  Single-L estimate (includes UV divergence, NOT universal):");
            println!("    kappa_raw(L={}) = {:.4} +/- {:.4}", l as usize, s2a, s2a_err);
            println!();
            compare_to_predictions(s2a, s2a_err, &preds, true);
        }
        return;
    }

    println!("  Fit points (S_2/Area vs 1/L):");
    for &(l, s2a, s2a_err) in &fit_points {
        println!("    L={:2}: S_2/Area = {:.6} +/- {:.6}  (1/L = {:.4})",
                 l as usize, s2a, s2a_err, 1.0 / l);
    }
    println!();

    match fit_kappa(&fit_points) {
        Some(fit) => {
            println!("  Fit method: {}", fit.method);
            println!("  a_div (UV divergent) = {:.6}", fit.a_div);
            if fit.dof > 0 {
                println!("  chi^2/dof = {:.2}/{} = {:.2}", fit.chi2, fit.dof, fit.chi2 / fit.dof as f64);
            }
            println!();
            println!("  ========================================");
            println!("  kappa_EE(G_2) = {:.4} +/- {:.4}", fit.kappa, fit.kappa_err);
            println!("  ========================================");
            println!();

            compare_to_predictions(fit.kappa, fit.kappa_err, &preds, false);

            // Summary verdict
            let mut best_name = "";
            let mut best_tension = f64::MAX;
            for p in &preds {
                let t = (fit.kappa - p.value).abs() / fit.kappa_err;
                if t < best_tension {
                    best_tension = t;
                    best_name = p.name;
                }
            }
            println!();
            println!("  VERDICT: Best match = {} ({:.1}sigma)", best_name, best_tension);
            if best_tension < 1.0 {
                println!("  Status: CONSISTENT (< 1sigma)");
            } else if best_tension < 2.0 {
                println!("  Status: COMPATIBLE (< 2sigma)");
            } else if best_tension < 3.0 {
                println!("  Status: TENSION ({:.1}sigma)", best_tension);
            } else {
                println!("  Status: EXCLUDED at {:.1}sigma", best_tension);
            }
        }
        None => {
            println!("  Fit FAILED (singular matrix or insufficient data).");
        }
    }

    println!();
    println!("================================================================");
    println!("  Systematic Error Budget");
    println!("================================================================");
    println!();

    // Finite volume
    if fit_points.len() >= 2 {
        let s2a_largest = fit_points.last().unwrap().1;
        let s2a_second = fit_points[fit_points.len() - 2].1;
        let fv_syst = (s2a_largest - s2a_second).abs();
        println!("  Finite volume (|S2/A(Lmax) - S2/A(Lmax-1)|): {:.6}", fv_syst);
    }

    // Taylor expm truncation
    let eps = 0.15;
    let taylor_err = (eps * (14.0_f64).sqrt()).powi(8) / 40320.0;
    println!("  Taylor expm (order 7) per step: {:.2e}", taylor_err);
    println!("  Note: v2 uses exact eigh, eliminating this systematic");

    // Discretization
    let mut betas: Vec<f64> = all_data.iter().map(|d| d.beta).collect();
    betas.sort_by(|a, b| a.partial_cmp(b).unwrap());
    betas.dedup_by(|a, b| (*a - *b).abs() < 1e-6);
    if betas.len() < 2 {
        println!("  Discretization: need multi-beta analysis (only beta={:.1})", betas[0]);
    }

    println!();
    println!("Done.");
}

fn compare_to_predictions(kappa: f64, kappa_err: f64, preds: &[Prediction], is_raw: bool) {
    let label = if is_raw { "kappa_raw" } else { "kappa_EE" };
    println!("  Comparison to predictions ({} = {:.4} +/- {:.4}):", label, kappa, kappa_err);
    println!("  {:-<64}", "");
    println!("  {:16} {:>8} {:>12} {:>10} {:>10}",
             "Prediction", "Value", "Difference", "Tension", "Status");
    println!("  {:-<64}", "");

    for p in preds {
        let diff = kappa - p.value;
        let tension = if kappa_err > 0.0 {
            diff.abs() / kappa_err
        } else {
            f64::INFINITY
        };
        let status = if tension < 1.0 {
            "OK"
        } else if tension < 2.0 {
            "compat"
        } else if tension < 3.0 {
            "tension"
        } else {
            "EXCLUDED"
        };
        println!("  {:16} {:8.4} {:+12.4} {:8.1}sigma  {:>10}",
                 p.name, p.value, diff, tension, status);
    }
    println!("  {:-<64}", "");
}

fn print_scenarios() {
    println!(r#"
================================================================
  EXPECTED SCENARIOS FOR kappa_EE(G_2)
================================================================

SCENARIO A: kappa ~ 0.60 +/- 0.02 (P1 or P2)
  -> G_2 follows same EE law as SU(N<=4)
  -> Paper: "Universal EE in exceptional gauge theories"
  -> Impact: HIGH — confirms zeta(3)/sqrt(pi) universality
  -> Caveat: cannot distinguish P1 (0.603) from P2 (0.630)
     at L=8. Need L=12,16 for that.

SCENARIO B: kappa ~ 0.28 +/- 0.03 (P3)
  -> G_2 follows sqrt(rank) scaling like SU(N>=5)
  -> Paper: "Non-universal EE: rank dependence"
  -> Impact: MEDIUM — extends sqrt(N) regime to exceptionals

SCENARIO C: kappa ~ 0.08 +/- 0.01 (P4)
  -> G_2 matches Faddeev-Popov convention kappa_FP = 1/12
  -> Paper: "EE as FP determinant measure"
  -> Impact: HIGH — connects EE to gauge-fixing geometry

SCENARIO D: kappa != any prediction
  -> New physics! G_2 has its own EE coefficient
  -> Paper: "First measurement of EE in G_2 gauge theory"
  -> Impact: MEDIUM — establishes baseline, falsifies models

MOST LIKELY: A or B based on SU(N) precedent
  G_2 rank=2, closest to SU(3) in complexity
  But exceptional -> could break SU(N) pattern
"#);
}
