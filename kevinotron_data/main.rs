// kevinotron/src/main.rs
// Unified lattice gauge theory EE engine.
//
// Usage:
//   kevinotron --group g2 --ls 8 --beta 10.0 --alpha 0.5
//   kevinotron --group su3 --ls 8 --beta 6.06 --full-ee
//   kevinotron --group g2 --ls 4 --beta 10.0 --full-ee --dump-config
//   kevinotron --group sp4 --ls 4 --beta 8.0 --full-ee --parallel-alpha
//   kevinotron --group so7 --ls 4 --beta 10.0 --alpha 0.0
//
// Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)

mod groups;
mod lattice;
mod io;
mod fermion;
mod solver;
mod thermal;
mod hmc;
mod observables;

use groups::GaugeGroup;
use groups::g2::G2Group;
use groups::so7::SO7Group;
use groups::sp4::SP4Group;
use groups::su2::SU2Group;
use groups::su3::SU3Group;
use groups::su4::SU4Group;
use groups::su5::SU5Group;
use groups::u1::U1Group;
use groups::f4::F4Group;
use groups::e6::E6Group;
use lattice::Lattice4D;
use crate::observables::polyakov;
use crate::observables::glueball;
use crate::observables::topology;
use crate::observables::glueball_gevp;
use clap::Parser;
use std::time::Instant;

#[derive(Parser)]
#[command(name = "kevinotron", about = "Unified Lattice Gauge Theory EE Engine")]
struct Args {
    /// Gauge group: u1, g2, su2, su3, su4, su5, sp4, so7
    #[arg(long)]
    group: String,

    /// Spatial lattice size L
    #[arg(long)]
    ls: usize,

    /// Temporal lattice size (default: 2*ls)
    #[arg(long, default_value = "0")]
    lt: usize,

    /// Inverse coupling beta
    #[arg(long)]
    beta: f64,

    /// Single alpha value (if not --full-ee)
    #[arg(long)]
    alpha: Option<f64>,

    /// Run full EE with 11 alpha-points + trapezoidal integration
    #[arg(long)]
    full_ee: bool,

    /// Number of alpha-points for full EE
    #[arg(long, default_value = "11")]
    n_alpha: usize,

    /// Parallelize alpha-points across rayon threads (default: true)
    #[arg(long, default_value = "true")]
    parallel_alpha: bool,

    /// Disable parallel alpha (sequential)
    #[arg(long)]
    no_parallel: bool,

    /// Number of bootstrap resamples for error estimation
    #[arg(long, default_value = "200")]
    n_bootstrap: usize,

    /// Thermalization sweeps
    #[arg(long, default_value = "500")]
    n_therm: usize,

    /// Measurement sweeps
    #[arg(long, default_value = "200")]
    n_meas: usize,

    /// Sweeps between measurements
    #[arg(long, default_value = "5")]
    n_skip: usize,

    /// Metropolis step size
    #[arg(long, default_value = "0.15")]
    epsilon: f64,

    /// Re-orthogonalize every N sweeps (0 = never)
    #[arg(long, default_value = "10")]
    reortho_interval: usize,

    /// Dump thermalized config as .npy (alpha=0 only if --full-ee)
    #[arg(long)]
    dump_config: bool,

    /// Run cold-start validation before measurement (P=1.0 check)
    #[arg(long, default_value = "true")]
    validate: bool,

    /// Skip validation (dangerous)
    #[arg(long)]
    no_validate: bool,

    /// Measure Polyakov loop
    #[arg(long)]
    polyakov_scan: bool,

    /// Measure glueball correlator
    #[arg(long)]
    glueball: bool,

    /// Measure glueball with GEVP (multi-smearing-level correlator matrix)
    #[arg(long)]
    glueball_gevp: bool,

    /// Measure topological charge
    #[arg(long)]
    topo_charge: bool,

    /// Check Wilson-Dirac γ₅-hermiticity
    #[arg(long)]
    fermion_check: bool,

    /// Quark mass for fermion operator
    #[arg(long, default_value = "0.1")]
    quark_mass: f64,

    /// Run HMC trajectories (pure gauge)
    #[arg(long)]
    hmc_run: bool,

    /// HMC leapfrog steps per trajectory
    #[arg(long, default_value = "20")]
    hmc_steps: usize,

    /// HMC step size
    #[arg(long, default_value = "0.1")]
    hmc_dt: f64,

    /// Number of HMC trajectories
    #[arg(long, default_value = "100")]
    hmc_traj: usize,

    /// Run thermal scan (Polyakov loop vs Lt)
    #[arg(long)]
    thermal: bool,

    /// Output .dat file for raw measurements (default: auto-name)
    #[arg(long, default_value = "")]
    output: String,

    /// Save structured JSON results (for --full-ee)
    #[arg(long, default_value = "")]
    json_output: String,

    /// Calibrate string tension sigma*a^2 via Wilson loops + Creutz ratios
    #[arg(long)]
    calibrate: bool,

    /// Maximum Wilson loop extent R,T = 1..max_loop (default: 6)
    #[arg(long, default_value = "6")]
    max_loop: usize,
}

/// Result of a single alpha-point measurement (mean, err, raw measurements).
#[allow(dead_code)]
struct AlphaResult {
    alpha: f64,
    mean: f64,
    err: f64,
    measurements: Vec<f64>,
}

/// Run a single alpha-point measurement.
fn run_single_alpha(
    group: &dyn GaugeGroup,
    args: &Args,
    alpha: f64,
    alpha_idx: usize,
    dat_path: &str,
) -> AlphaResult {
    let lt = if args.lt == 0 { 2 * args.ls } else { args.lt };
    let mut lat = Lattice4D::new(group, args.ls, lt, args.beta);
    let mut rng = rand::thread_rng();
    let mut sweep_count = 0usize;

    eprintln!("# --- alpha={:.3} ({}/{}) ---", alpha, alpha_idx + 1, args.n_alpha);

    // Thermalization
    let t_therm = Instant::now();
    for s in 0..args.n_therm {
        lat.sweep_alpha(group, alpha, args.epsilon, &mut rng);
        sweep_count += 1;
        if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
            lat.reproject_all(group);
        }
        if (s + 1) % 100 == 0 {
            let p = lat.plaquette(group);
            eprintln!("# therm {:4}: P={:.6}", s + 1, p);
        }
    }
    let therm_time = t_therm.elapsed().as_secs_f64();
    eprintln!(
        "# Therm done in {:.1}s ({:.3}s/sweep)",
        therm_time,
        therm_time / args.n_therm as f64
    );

    // Dump config at alpha=0
    if args.dump_config && alpha_idx == 0 {
        let config_path = format!(
            "config_{}_L{}_beta{:.1}.npy",
            group.name().to_lowercase().replace("(", "").replace(")", ""),
            args.ls,
            args.beta
        );
        eprintln!("# Dumping config to {}", config_path);
        if let Err(e) = io::dump_config_npy(&lat, group, &config_path) {
            eprintln!("# WARNING: config dump failed: {}", e);
        }
    }

    // Measurements
    let mut measurements = Vec::with_capacity(args.n_meas);
    let t_meas = Instant::now();
    for m in 0..args.n_meas {
        for _ in 0..args.n_skip {
            lat.sweep_alpha(group, alpha, args.epsilon, &mut rng);
            sweep_count += 1;
            if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
                lat.reproject_all(group);
            }
        }
        let val = lat.measure_ds_dalpha(group);
        measurements.push(val);

        if (m + 1) % 50 == 0 {
            let running_mean: f64 =
                measurements.iter().sum::<f64>() / measurements.len() as f64;
            eprintln!(
                "# meas {:4}: dS/da = {:.2} (running mean {:.2})",
                m + 1, val, running_mean
            );
        }
    }
    let meas_time = t_meas.elapsed().as_secs_f64();
    eprintln!("# Meas done in {:.1}s", meas_time);

    let mean: f64 = measurements.iter().sum::<f64>() / measurements.len() as f64;
    let var: f64 = measurements
        .iter()
        .map(|x| (x - mean).powi(2))
        .sum::<f64>()
        / measurements.len() as f64;
    let err = (var / measurements.len() as f64).sqrt();

    // Write raw measurements
    if !dat_path.is_empty() {
        let lt = if args.lt == 0 { 2 * args.ls } else { args.lt };
        if let Err(e) = io::write_measurements_dat(
            dat_path,
            group.name(),
            args.ls,
            lt,
            args.beta,
            alpha_idx,
            alpha,
            &measurements,
        ) {
            eprintln!("# WARNING: failed to write .dat: {}", e);
        }
    }

    println!("ALPHA {:.3}: dS/dalpha = {:.6} +/- {:.6}", alpha, mean, err);

    AlphaResult { alpha, mean, err, measurements }
}

/// Bootstrap error on trapezoidal integral.
/// Given per-alpha measurements, resample each alpha-point's measurements,
/// recompute means, integrate, and report std of the integral.
fn bootstrap_integral(
    alphas: &[f64],
    all_measurements: &[Vec<f64>],
    n_bootstrap: usize,
) -> (f64, f64) {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    let n_alpha = alphas.len();

    let mut bootstrap_s2 = Vec::with_capacity(n_bootstrap);

    for _ in 0..n_bootstrap {
        // Resample each alpha-point's measurements with replacement
        let mut resampled_means = Vec::with_capacity(n_alpha);
        for meas in all_measurements {
            let n = meas.len();
            if n == 0 {
                resampled_means.push(0.0);
                continue;
            }
            let mut sum = 0.0;
            for _ in 0..n {
                let idx = rng.gen_range(0..n);
                sum += meas[idx];
            }
            resampled_means.push(sum / n as f64);
        }

        // Trapezoidal integration
        let mut s2 = 0.0;
        for i in 0..(n_alpha - 1) {
            let da = alphas[i + 1] - alphas[i];
            s2 += da * 0.5 * (resampled_means[i] + resampled_means[i + 1]);
        }
        bootstrap_s2.push(s2);
    }

    let bs_mean: f64 = bootstrap_s2.iter().sum::<f64>() / n_bootstrap as f64;
    let bs_var: f64 = bootstrap_s2
        .iter()
        .map(|x| (x - bs_mean).powi(2))
        .sum::<f64>()
        / (n_bootstrap - 1) as f64;
    let bs_err = bs_var.sqrt();

    (bs_mean, bs_err)
}

/// Write structured JSON results for full-EE run.
fn write_json_results(
    path: &str,
    group_name: &str,
    ls: usize,
    lt: usize,
    beta: f64,
    alphas: &[f64],
    ds_means: &[f64],
    ds_errs: &[f64],
    s2: f64,
    s2_err: f64,
    s2_bootstrap_err: f64,
    area: f64,
) -> std::io::Result<()> {
    use std::io::Write;
    let mut f = std::fs::File::create(path)?;
    write!(f, "{{\n")?;
    write!(f, "  \"kevinotron_version\": \"1.1.0\",\n")?;
    write!(f, "  \"group\": \"{}\",\n", group_name)?;
    write!(f, "  \"ls\": {},\n", ls)?;
    write!(f, "  \"lt\": {},\n", lt)?;
    write!(f, "  \"beta\": {},\n", beta)?;
    write!(f, "  \"n_alpha\": {},\n", alphas.len())?;
    write!(f, "  \"area\": {},\n", area)?;
    write!(f, "  \"s2\": {},\n", s2)?;
    write!(f, "  \"s2_err_propagated\": {},\n", s2_err)?;
    write!(f, "  \"s2_err_bootstrap\": {},\n", s2_bootstrap_err)?;
    write!(f, "  \"s2_over_area\": {},\n", s2 / area)?;
    write!(f, "  \"s2_over_area_err\": {},\n", s2_bootstrap_err / area)?;
    write!(f, "  \"alphas\": [")?;
    for (i, a) in alphas.iter().enumerate() {
        if i > 0 { write!(f, ", ")?; }
        write!(f, "{:.6}", a)?;
    }
    write!(f, "],\n")?;
    write!(f, "  \"ds_means\": [")?;
    for (i, v) in ds_means.iter().enumerate() {
        if i > 0 { write!(f, ", ")?; }
        write!(f, "{:.6}", v)?;
    }
    write!(f, "],\n")?;
    write!(f, "  \"ds_errs\": [")?;
    for (i, v) in ds_errs.iter().enumerate() {
        if i > 0 { write!(f, ", ")?; }
        write!(f, "{:.6}", v)?;
    }
    write!(f, "]\n")?;
    write!(f, "}}\n")?;
    Ok(())
}

/// Run string tension calibration: thermalise, measure Wilson loops, compute Creutz ratios.
fn run_calibrate(group: &dyn GaugeGroup, args: &Args, lt: usize) {
    use observables::{avg_wilson_loop, creutz_ratio};
    use observables::creutz::creutz_ratio_err;

    let mut lat = Lattice4D::new(group, args.ls, lt, args.beta);
    let mut rng = rand::thread_rng();
    let max_r = args.max_loop.min(args.ls); // don't exceed lattice size

    eprintln!("# CALIBRATE mode: measuring W(R,T) for R,T = 1..{}", max_r);
    eprintln!("# Thermalising {} sweeps ...", args.n_therm);

    // Thermalization (alpha = 0 = undeformed action)
    let mut sweep_count = 0usize;
    for s in 0..args.n_therm {
        lat.sweep_alpha(group, 0.0, args.epsilon, &mut rng);
        sweep_count += 1;
        if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
            lat.reproject_all(group);
        }
        if (s + 1) % 100 == 0 {
            let p = lat.plaquette(group);
            eprintln!("# therm {:4}: P={:.6}", s + 1, p);
        }
    }

    // Measure Wilson loops: accumulate per-config values for jackknife
    let n_meas = args.n_meas;
    let n_skip = args.n_skip;

    // Store per-config Wilson loop values: w_configs[r][t][config_idx]
    let mut w_configs: Vec<Vec<Vec<f64>>> = vec![vec![Vec::new(); max_r + 1]; max_r + 1];

    eprintln!("# Measuring {} configs (skip {}) ...", n_meas, n_skip);

    for m in 0..n_meas {
        for _ in 0..n_skip {
            lat.sweep_alpha(group, 0.0, args.epsilon, &mut rng);
            sweep_count += 1;
            if args.reortho_interval > 0 && sweep_count % args.reortho_interval == 0 {
                lat.reproject_all(group);
            }
        }

        // Measure all Wilson loops on this config
        for r in 1..=max_r {
            for t in r..=max_r {
                let (w, _) = avg_wilson_loop(&lat, group, r, t);
                w_configs[r][t].push(w);
                if t != r {
                    w_configs[t][r].push(w); // W(R,T) = W(T,R) by symmetry
                }
            }
        }

        if (m + 1) % 50 == 0 {
            let p = lat.plaquette(group);
            eprintln!("# config {:4}/{}: P={:.6}", m + 1, n_meas, p);
        }
    }

    // Compute means and errors for each (R, T)
    let mut w_mean = vec![vec![0.0f64; max_r + 1]; max_r + 1];
    let mut w_err = vec![vec![0.0f64; max_r + 1]; max_r + 1];

    println!();
    println!("# ======================================");
    println!("# WILSON LOOPS: {} at beta={}", group.name(), args.beta);
    println!("# L={}, Lt={}, {} configs", args.ls, lt, n_meas);
    println!("# ======================================");
    println!("# {:>3} {:>3} {:>14} {:>14}", "R", "T", "W(R,T)", "err");

    for r in 1..=max_r {
        for t in 1..=max_r {
            let vals = &w_configs[r][t];
            if vals.is_empty() { continue; }
            let n = vals.len() as f64;
            let mean = vals.iter().sum::<f64>() / n;
            let var = vals.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / n;
            let err = (var / n).sqrt();
            w_mean[r][t] = mean;
            w_err[r][t] = err;
            println!("W {:3} {:3}   {: >14.8} {: >14.8}", r, t, mean, err);
        }
    }

    // Creutz ratios chi(I,I) for I = 2..max_r
    println!();
    println!("# ======================================");
    println!("# CREUTZ RATIOS: sigma*a^2 estimates");
    println!("# ======================================");
    println!("# {:>3} {:>3} {:>14} {:>14}", "I", "J", "chi(I,J)", "err");

    for i in 2..=max_r {
        for j in i..=max_r {
            let wij   = w_mean[i][j];
            let wi1j1 = w_mean[i - 1][j - 1];
            let wij1  = w_mean[i][j - 1];
            let wi1j  = w_mean[i - 1][j];

            let chi = creutz_ratio(wij, wi1j1, wij1, wi1j);
            let chi_err = creutz_ratio_err(
                wij,   w_err[i][j],
                wi1j1, w_err[i - 1][j - 1],
                wij1,  w_err[i][j - 1],
                wi1j,  w_err[i - 1][j],
            );

            let tag = if i == j { " <-- sigma*a^2" } else { "" };
            println!("CHI {:3} {:3}   {: >14.8} {: >14.8}{}", i, j, chi, chi_err, tag);

            if i == j {
                println!("SIGMA_A2 = {:.6} +/- {:.6} at beta={:.2} [chi({},{})]",
                    chi, chi_err, args.beta, i, j);
            }
        }
    }

    println!();
    // Summary: best estimate from largest diagonal Creutz ratio with finite value
    let mut best_i = 0;
    let mut best_chi = f64::NAN;
    let mut best_err = f64::NAN;
    for i in (2..=max_r).rev() {
        let wij   = w_mean[i][i];
        let wi1j1 = w_mean[i - 1][i - 1];
        let wij1  = w_mean[i][i - 1];
        let wi1j  = w_mean[i - 1][i];
        let chi = creutz_ratio(wij, wi1j1, wij1, wi1j);
        if chi.is_finite() {
            best_chi = chi;
            best_err = creutz_ratio_err(
                wij,   w_err[i][i],
                wi1j1, w_err[i - 1][i - 1],
                wij1,  w_err[i][i - 1],
                wi1j,  w_err[i - 1][i],
            );
            best_i = i;
            break;
        }
    }

    if best_i > 0 {
        println!("# ======================================");
        println!("# BEST ESTIMATE (largest finite chi(I,I)):");
        println!("SIGMA_A2_BEST = {:.6} +/- {:.6} at beta={:.2} [chi({},{})]",
            best_chi, best_err, args.beta, best_i, best_i);
        println!("# ======================================");
    } else {
        println!("# WARNING: no finite Creutz ratio found — increase stats or beta");
    }
}

fn main() {
    let args = Args::parse();

    // Dispatch group
    let group: Box<dyn GaugeGroup> = match args.group.to_lowercase().as_str() {
        "u1" => Box::new(U1Group::new()),
        "g2" => Box::new(G2Group::new()),
        "su2" => Box::new(SU2Group::new()),
        "su3" => Box::new(SU3Group::new()),
        "su4" => Box::new(SU4Group::new()),
        "su5" => Box::new(SU5Group::new()),
        "sp4" => Box::new(SP4Group::new()),
        "so7" => Box::new(SO7Group::new()),
        "f4" => Box::new(F4Group::new()),
        "e6" => Box::new(E6Group::new()),
        _ => {
            eprintln!("ERROR: unknown group '{}'. Use: u1, g2, su2, su3, su4, su5, sp4, so7, f4, e6", args.group);
            std::process::exit(1);
        }
    };
    let group_ref: &dyn GaugeGroup = group.as_ref();

    let lt = if args.lt == 0 { 2 * args.ls } else { args.lt };

    eprintln!("# KEVINOTRON v2.1 -- {} EE Engine (9 groups)", group_ref.name());

    // === MANDATORY COLD-START VALIDATION ===
    if !args.no_validate {
        let mut lat_cold = Lattice4D::new(group_ref, args.ls, lt, args.beta);
        let p_cold = lat_cold.plaquette(group_ref);
        if (p_cold - 1.0).abs() > 0.01 {
            eprintln!("# *** VALIDATION FAILED: cold start P={:.6} (expected 1.0) ***", p_cold);
            eprintln!("# *** This indicates a bug in the group implementation. Aborting. ***");
            std::process::exit(2);
        }
        eprintln!("# VALIDATE: cold start P={:.6} OK", p_cold);

        // Quick 20-sweep thermalization check
        let mut rng_val = rand::thread_rng();
        for _ in 0..20 {
            lat_cold.sweep_alpha(group_ref, 0.0, args.epsilon, &mut rng_val);
        }
        let p_hot = lat_cold.plaquette(group_ref);
        eprintln!("# VALIDATE: 20-sweep P={:.6} (should be < 1.0)", p_hot);
        if p_hot > 0.999 {
            eprintln!("# *** WARNING: plaquette not thermalizing. Check epsilon. ***");
        }
    }
    eprintln!("# Ls={}, Lt={}, beta={}", args.ls, lt, args.beta);
    eprintln!("# dim_fund={}, dim_adj={}, is_complex={}", group_ref.dim_fund(), group_ref.dim_adj(), group_ref.is_complex());
    eprintln!("# n_therm={}, n_meas={}, n_skip={}, epsilon={}", args.n_therm, args.n_meas, args.n_skip, args.epsilon);

    let t0 = Instant::now();

    let dat_path = if args.output.is_empty() {
        let gname = group_ref.name().to_lowercase().replace("(", "").replace(")", "");
        format!("{}_ee_L{}_beta{:.2}.dat", gname, args.ls, args.beta)
    } else {
        args.output.clone()
    };

    if args.hmc_run {
        let cfg = hmc::HmcConfig {
            n_steps: args.hmc_steps,
            dt: args.hmc_dt,
            beta: args.beta,
        };
        let mut lat_hmc = Lattice4D::new(group_ref, args.ls, lt, args.beta);
        let mut rng_hmc = rand::thread_rng();
        let mut n_accept = 0usize;
        for traj in 0..args.hmc_traj {
            let (accepted, dh) = hmc::hmc_trajectory(
                &mut lat_hmc, group_ref, &cfg, &mut rng_hmc);
            if accepted { n_accept += 1; }
            if (traj + 1) % 10 == 0 {
                let p = lat_hmc.plaquette(group_ref);
                eprintln!("# HMC traj {}: dH={:.4} acc={}/{} P={:.6}",
                    traj+1, dh, n_accept, traj+1, p);
            }
        }
        let acc_rate = n_accept as f64 / args.hmc_traj as f64;
        eprintln!("# HMC done: {}/{} accepted ({:.1}%)",
            n_accept, args.hmc_traj, 100.0 * acc_rate);
    } else if args.thermal {
        let lt_vals: Vec<usize> = vec![2, 3, 4, 5, 6, 8, 10, 12];
        let results = thermal::thermal_scan(
            group_ref, args.ls, args.beta, &lt_vals,
            args.n_therm, args.n_meas, args.n_skip, args.epsilon,
        );
        println!("# THERMAL SCAN: {} Lt values", results.len());
        println!("Lt  |L|       chi       P");
        for r in &results {
            println!("{:<4} {:.6} {:.6} {:.6}",
                r.lt, r.polyakov_mod, r.susceptibility, r.plaquette);
        }
        let total = t0.elapsed().as_secs_f64();
        eprintln!("# Thermal scan done in {:.1}s", total);
    } else if args.calibrate {
        run_calibrate(group_ref, &args, lt);
        let total = t0.elapsed().as_secs_f64();
        eprintln!("# Total calibration time: {:.1}s", total);
    } else if args.full_ee {
        // Full EE: scan alpha = 0, 1/(n-1), ..., 1
        let n_alpha = args.n_alpha;
        let mut alphas = Vec::with_capacity(n_alpha);
        let mut ds_means = Vec::with_capacity(n_alpha);
        let mut ds_errs = Vec::with_capacity(n_alpha);
        let mut all_measurements: Vec<Vec<f64>> = Vec::with_capacity(n_alpha);

        for i in 0..n_alpha {
            let alpha = if n_alpha > 1 {
                i as f64 / (n_alpha - 1) as f64
            } else {
                0.0
            };
            alphas.push(alpha);
        }

        if args.parallel_alpha && !args.no_parallel && n_alpha > 1 {
            // Parallel alpha-points via rayon
            eprintln!("# Running {} alpha-points in parallel (rayon)", n_alpha);
            use rayon::prelude::*;

            let results: Vec<AlphaResult> = alphas
                .par_iter()
                .enumerate()
                .map(|(i, &alpha)| {
                    run_single_alpha(group_ref, &args, alpha, i, &dat_path)
                })
                .collect();

            for r in results {
                ds_means.push(r.mean);
                ds_errs.push(r.err);
                all_measurements.push(r.measurements);
            }
        } else {
            // Sequential alpha-points
            for i in 0..n_alpha {
                let r = run_single_alpha(group_ref, &args, alphas[i], i, &dat_path);
                ds_means.push(r.mean);
                ds_errs.push(r.err);
                all_measurements.push(r.measurements);
            }
        }

        // Trapezoidal integration
        let mut s2 = 0.0;
        let mut s2_err_sq = 0.0;
        for i in 0..(n_alpha - 1) {
            let da = alphas[i + 1] - alphas[i];
            s2 += da * 0.5 * (ds_means[i] + ds_means[i + 1]);
            s2_err_sq += (da * 0.5).powi(2) * (ds_errs[i].powi(2) + ds_errs[i + 1].powi(2));
        }
        let s2_err = s2_err_sq.sqrt();

        // Bootstrap error estimation
        let (bs_s2, bs_err) = bootstrap_integral(&alphas, &all_measurements, args.n_bootstrap);

        let area = (args.ls as f64).powi(2) * lt as f64;
        let n_bdy = args.ls * args.ls * lt;

        println!();
        println!("# ============================");
        println!("# RESULTS: {} EE", group_ref.name());
        println!("# ============================");
        println!("RESULT: S2={:.6} +/- {:.6}", s2, s2_err);
        println!("RESULT: S2_bootstrap={:.6} +/- {:.6}", bs_s2, bs_err);
        println!("RESULT: S2/area={:.6} +/- {:.6}", s2 / area, bs_err / area);
        println!("RESULT: n_boundary_links={}", n_bdy);
        println!("RESULT: area={:.0}", area);

        // === Additional observables (on a fresh thermalized config) ===
        if args.polyakov_scan || args.topo_charge || args.glueball || args.glueball_gevp || args.fermion_check {
            eprintln!("# --- Additional observables ---");
            let mut lat_obs = Lattice4D::new(group_ref, args.ls, lt, args.beta);
            let mut rng_obs = rand::thread_rng();
            for _ in 0..args.n_therm {
                lat_obs.sweep_alpha(group_ref, 0.0, args.epsilon, &mut rng_obs);
            }
            if args.polyakov_scan {
                let poly = polyakov::measure_polyakov(&lat_obs, group_ref);
                eprintln!("# POLYAKOV: Re={:.6} Im={:.6} |L|={:.6} chi={:.6}",
                    poly.re_mean, poly.im_mean, poly.modulus_mean, poly.susceptibility);
            }
            if args.topo_charge {
                let q = topology::topological_charge(&lat_obs, group_ref);
                eprintln!("# TOPO: Q={:.6}", q);
            }
            if args.glueball {
                // Accumulate correlators over multiple configs for signal
                let n_glueball_meas = 500;
                let n_smear_steps = 20;
                let alpha_smear = 0.5;
                let lt_obs = if args.lt == 0 { 2 * args.ls } else { args.lt };
                let mut avg_corr = vec![0.0f64; lt_obs / 2 + 1];
                
                eprintln!("# GLUEBALL: {} measurements × {} APE smear steps", n_glueball_meas, n_smear_steps);
                for meas in 0..n_glueball_meas {
                    // Thermalize between measurements
                    for _ in 0..10 {
                        lat_obs.sweep_alpha(group_ref, 0.0, args.epsilon, &mut rng_obs);
                    }
                    
                    // APE smear a COPY (don't modify the config for future sweeps)
                    let mut lat_smeared = lat_obs.clone();
                    for _ in 0..n_smear_steps {
                        glueball::ape_smear_step(&mut lat_smeared, group_ref, alpha_smear);
                    }
                    
                    // Measure on smeared config
                    let corr = glueball::glueball_correlator(&lat_smeared, group_ref);
                    for t in 0..avg_corr.len().min(corr.len()) {
                        avg_corr[t] += corr[t];
                    }
                }
                
                // Average
                for c in avg_corr.iter_mut() {
                    *c /= n_glueball_meas as f64;
                }
                
                // Effective mass with |C(t)| to handle sign fluctuations
                let mut m_eff = Vec::new();
                for t in 0..avg_corr.len() - 1 {
                    let c_t = avg_corr[t].abs();
                    let c_t1 = avg_corr[t + 1].abs();
                    if c_t > 1e-30 && c_t1 > 1e-30 {
                        m_eff.push((c_t / c_t1).ln());
                    } else {
                        m_eff.push(0.0);
                    }
                }
                
                eprintln!("# GLUEBALL: C(t) = {:?}", &avg_corr[..avg_corr.len().min(6)]);
                eprintln!("# GLUEBALL: m_eff = {:?}", &m_eff[..m_eff.len().min(5)]);
                if m_eff.len() >= 3 {
                    let m_plateau = (m_eff[1] + m_eff[2]) / 2.0;
                    eprintln!("# GLUEBALL: m_0++ × a ≈ {:.4} (from m_eff plateau t=1,2)", m_plateau);
                }
            }
            if args.glueball_gevp {
                // GEVP: multi-smearing-level correlator matrix
                let smear_levels = vec![0usize, 5, 10, 20, 30];
                let n_ops = smear_levels.len();
                let n_meas = 500;
                let alpha_smear = 0.5;
                let lt_obs = if args.lt == 0 { 2 * args.ls } else { args.lt };
                let n_t = lt_obs / 2 + 1;
                
                // Accumulate cross-correlator matrix
                let mut avg_corr = vec![vec![0.0f64; n_ops * n_ops]; n_t];
                
                eprintln!("# GLUEBALL-GEVP: {} ops × {} measurements, smear levels {:?}",
                    n_ops, n_meas, smear_levels);
                for meas in 0..n_meas {
                    for _ in 0..10 {
                        lat_obs.sweep_alpha(group_ref, 0.0, args.epsilon, &mut rng_obs);
                    }
                    let smeared = glueball_gevp::build_smeared_lattices(
                        &lat_obs, group_ref, &smear_levels, alpha_smear);
                    let c = glueball_gevp::correlator_matrix(&smeared, group_ref);
                    for t in 0..n_t {
                        for k in 0..n_ops*n_ops {
                            avg_corr[t][k] += c[t][k];
                        }
                    }
                    if (meas + 1) % 100 == 0 {
                        eprintln!("#   meas {}/{}", meas + 1, n_meas);
                    }
                }
                for t in 0..n_t {
                    for k in 0..n_ops*n_ops {
                        avg_corr[t][k] /= n_meas as f64;
                    }
                }
                
                // Output matrix for Python GEVP solver
                eprintln!("# GLUEBALL-GEVP: matrix C(t) for t=0..{}", n_t-1);
                for t in 0..n_t.min(8) {
                    eprintln!("# C({}) =", t);
                    for i in 0..n_ops {
                        let row: Vec<String> = (0..n_ops).map(|j|
                            format!("{:>12.4e}", avg_corr[t][i*n_ops+j])).collect();
                        eprintln!("#   {}", row.join(" "));
                    }
                }
                
                // Solve GEVP in Rust → m_0++ directly
                let eigs = glueball_gevp::solve_gevp(&avg_corr, n_ops, 1);
                let m_eff = glueball_gevp::effective_masses_gevp(&eigs);
                eprintln!("# GEVP eigenvalues λ_n(t):");
                for t in 0..eigs.len().min(6) {
                    let row: Vec<String> = eigs[t].iter().map(|x| format!("{:>11.4e}", x)).collect();
                    eprintln!("#   t={}: {}", t, row.join(" "));
                }
                eprintln!("# GEVP effective masses m_n(t):");
                for t in 0..m_eff.len().min(5) {
                    let row: Vec<String> = m_eff[t].iter().map(|x| {
                        if x.is_nan() { "    NaN ".to_string() } else { format!("{:>8.4}", x) }
                    }).collect();
                    eprintln!("#   t={}→{}: {}", t, t+1, row.join(" "));
                }
                if m_eff.len() >= 3 {
                    // Ground state plateau from t=2,3
                    let m0_pl = (m_eff[1][0] + m_eff[2][0]) / 2.0;
                    eprintln!("# GEVP: m_0++ × a (ground state plateau t=2,3) = {:.4}", m0_pl);
                    if m_eff.len() >= 4 {
                        // Excited state
                        let m1_pl = (m_eff[1][1] + m_eff[2][1]) / 2.0;
                        eprintln!("# GEVP: m_1++ × a (first excited)             = {:.4}", m1_pl);
                    }
                }
                
                // Save to JSON for Python GEVP
                let json_path = format!("glueball_gevp_{}_L{}_beta{:.2}.json",
                    group_ref.name().to_lowercase().replace("(","").replace(")",""),
                    args.ls, args.beta);
                let mut json = String::from("{\"n_ops\": ");
                json.push_str(&format!("{}, \"smear_levels\": {:?}, \"n_t\": {}, \"correlator\": [",
                    n_ops, smear_levels, n_t));
                for (t, row) in avg_corr.iter().enumerate() {
                    if t > 0 { json.push_str(", "); }
                    json.push('[');
                    let entries: Vec<String> = row.iter().map(|x| format!("{:.6e}", x)).collect();
                    json.push_str(&entries.join(", "));
                    json.push(']');
                }
                json.push_str("]}");
                std::fs::write(&json_path, json).ok();
                eprintln!("# GLUEBALL-GEVP: saved to {}", json_path);
            }
            if args.fermion_check {
                let g5h = fermion::check_gamma5_hermiticity(&lat_obs, group_ref, args.quark_mass);
                eprintln!("# FERMION: g5-hermiticity = {:.2e}", g5h);
                let n_dof = args.ls * args.ls * args.ls * lt * 4 * 2 * group_ref.dim_fund();
                let b_vec: Vec<f64> = (0..n_dof).map(|i| ((i * 7 + 3) % 100) as f64 / 100.0 - 0.5).collect();
                let (_, iters, res) = solver::cg_solve(&lat_obs, group_ref, args.quark_mass, &b_vec, 1e-8, 500);
                eprintln!("# FERMION: CG {} iters, residual {:.2e}", iters, res);
            }
        }

        // Write JSON results
        let json_path = if args.json_output.is_empty() {
            let gname = group_ref.name().to_lowercase().replace("(", "").replace(")", "");
            format!("{}_ee_L{}_beta{:.2}.json", gname, args.ls, args.beta)
        } else {
            args.json_output.clone()
        };
        if let Err(e) = write_json_results(
            &json_path,
            group_ref.name(),
            args.ls,
            lt,
            args.beta,
            &alphas,
            &ds_means,
            &ds_errs,
            s2,
            s2_err,
            bs_err,
            area,
        ) {
            eprintln!("# WARNING: failed to write JSON: {}", e);
        } else {
            eprintln!("# JSON results written to {}", json_path);
        }

        let total = t0.elapsed().as_secs_f64();
        let total_sweeps = n_alpha as f64 * (args.n_therm + args.n_meas * args.n_skip) as f64;
        eprintln!(
            "# Total: {:.1}s = {:.2}h, {:.4}s/sweep (avg over {} sweeps)",
            total, total / 3600.0, total / total_sweeps, total_sweeps as u64
        );
    } else if let Some(alpha) = args.alpha {
        // Single alpha-point
        run_single_alpha(group_ref, &args, alpha, 0, &dat_path);
        let total = t0.elapsed().as_secs_f64();
        eprintln!("# Total time: {:.1}s", total);
    } else {
        eprintln!("ERROR: specify --alpha <val> or --full-ee");
        std::process::exit(1);
    }
}
