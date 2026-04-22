#!/usr/bin/env python3
"""
bench_baseline.py — 100-evaluation wall-clock benchmark for the
Plik-lite Cobaya configuration used in ECI v4.

Methodology
-----------
We build a Cobaya `model` (no sampler) and invoke
    model.logposterior(sample, cached=False)
100 times with small random jitter around the reference point, recording
wall-clock per call. The first two calls are treated as warm-up (CLASS's
spline caches settle) and discarded.

Threads capped at 2 via OMP_NUM_THREADS before importing CLASS (leaves
headroom for other agents sharing the box, matches job spec).

Usage:
    python mcmc/benchmark/bench_baseline.py [--n 100] [--out TAG]
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

# Must be set BEFORE numpy/CLASS import.
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
PACKAGES = REPO / "mcmc" / "packages"
RAW = REPO / "mcmc" / "benchmark" / "_raw_timings"
RAW.mkdir(parents=True, exist_ok=True)


# Cobaya info — matches eci_nmc.yaml but:
#   * uses vanilla `classy` (no NMC patch keys; those are a no-op on the
#     vanilla build for the benchmark itself)
#   * Plik-lite only (skips full TTTEEE — the job spec decision)
#   * no sampler (we drive model.logposterior directly)
def build_info():
    return {
        "theory": {
            "classy": {
                "ignore_obsolete": True,  # hi_class_nmc self-reports v3.2.3
                "extra_args": {
                    "output": "tCl,pCl,lCl,mPk",
                    "lensing": "yes",
                    "N_ur": 2.0328,
                    "N_ncdm": 1,
                    "m_ncdm": 0.06,
                    # w0wa CPL fluid (w0, wa come from sampled params below).
                    "Omega_Lambda": 0,
                    "use_ppf": "yes",
                },
            }
        },
        "likelihood": {
            "planck_2018_lowl.TT": None,
            "planck_2018_lowl.EE": None,
            "planck_2018_highl_plik.TTTEEE_lite": None,
            "bao.desi_dr2.desi_bao_all": None,
            "sn.pantheonplus": None,
        },
        "params": {
            "H0":        {"prior": {"min": 55, "max": 85},  "ref": 67.4,   "proposal": 0.5},
            "omega_b":   {"prior": {"min": 0.017, "max": 0.027}, "ref": 0.02237, "proposal": 1.5e-4},
            "omega_cdm": {"prior": {"min": 0.09, "max": 0.15},   "ref": 0.1200,  "proposal": 1.2e-3},
            "n_s":       {"prior": {"min": 0.9, "max": 1.05},    "ref": 0.9649,  "proposal": 4.2e-3},
            "logA":      {"prior": {"min": 2.5, "max": 3.5},     "ref": 3.044,   "proposal": 0.014,
                          "drop": True, "latex": r"\log(10^{10} A_\mathrm{s})"},
            "A_s":       {"value": "lambda logA: 1e-10*np.exp(logA)"},
            "tau_reio":  {"prior": {"min": 0.02, "max": 0.12},   "ref": 0.0544,  "proposal": 0.0073},
            "w0_fld":    {"prior": {"min": -1.2, "max": -0.5},   "ref": -1.0,    "proposal": 0.05},
            "wa_fld":    {"prior": {"min": -2.0, "max": 0.0},    "ref": 0.0,     "proposal": 0.1},
        },
        "packages_path": str(PACKAGES),
        "debug": False,
        "stop_at_error": True,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100, help="number of evaluations")
    ap.add_argument("--out", default="baseline", help="tag for raw-timing file")
    ap.add_argument("--seed", type=int, default=20260422)
    args = ap.parse_args()

    from cobaya.model import get_model  # noqa: E402

    info = build_info()
    print(f"[bench] building Cobaya model (OMP_NUM_THREADS={os.environ['OMP_NUM_THREADS']})...", flush=True)
    t_build0 = time.perf_counter()
    model = get_model(info)
    t_build1 = time.perf_counter()
    print(f"[bench] model built in {t_build1 - t_build0:.2f}s", flush=True)

    rng = np.random.default_rng(args.seed)
    sampled = list(model.parameterization.sampled_params())
    # Reference point: use Cobaya's own reference sampler once, then jitter
    # by 10% of proposal width around it.
    ref = np.asarray(model.prior.reference(random_state=rng))
    # Build proposal vector: explicit values for our cosmo params, small
    # default (1% of prior width) for likelihood nuisance (A_planck, etc.).
    proposals = []
    for name in sampled:
        p = info["params"].get(name, {})
        if isinstance(p, dict) and "proposal" in p:
            proposals.append(float(p["proposal"]))
        else:
            lo, hi = model.prior.bounds(confidence_for_unbounded=0.9999)[sampled.index(name)]
            proposals.append(0.01 * (hi - lo))
    proposals = np.asarray(proposals)

    timings = []
    logps = []
    warmup = 2
    total = args.n + warmup
    print(f"[bench] running {total} evals ({warmup} warmup + {args.n} measured)...", flush=True)

    attempts = 0
    measured = 0
    max_attempts = total * 5
    while measured < args.n and attempts < max_attempts:
        attempts += 1
        jitter = rng.normal(0.0, 0.05, size=len(ref)) * proposals
        point = ref + jitter
        t0 = time.perf_counter()
        logp = model.logposterior(dict(zip(sampled, point)), cached=False)
        t1 = time.perf_counter()
        dt = t1 - t0
        lp = float(logp.logpost)
        # skip prior-rejected points (CLASS never called → ~microseconds)
        if not np.isfinite(lp):
            print(f"[bench] skip  {attempts:3d}  prior-reject  dt={dt*1000:.2f}ms", flush=True)
            continue
        if measured < warmup:
            tag = "warm"
        else:
            tag = "meas"
            timings.append(dt)
            logps.append(lp)
        print(f"[bench] {tag}  {measured:3d}  dt={dt*1000:.1f}ms  logpost={lp:.3f}", flush=True)
        measured += 1

    t = np.asarray(timings)
    stats = {
        "n": len(t),
        "min_s":    float(t.min()),
        "median_s": float(np.median(t)),
        "mean_s":   float(t.mean()),
        "p95_s":    float(np.quantile(t, 0.95)),
        "max_s":    float(t.max()),
        "std_s":    float(t.std(ddof=1)),
        "omp_threads": int(os.environ["OMP_NUM_THREADS"]),
        "cpu":      "i5-14600KF",
        "compile":  "-O3 -march=native -mavx2 -mtune=native -flto",
        "likelihoods": list(info["likelihood"].keys()),
    }
    print("\n[bench] === summary ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    out_txt = RAW / f"{args.out}.txt"
    out_json = RAW / f"{args.out}.json"
    with out_txt.open("w") as f:
        f.write(f"# bench_baseline.py — {args.out}\n")
        f.write(f"# date: {time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
        f.write(f"# stats: {json.dumps(stats, indent=2)}\n")
        f.write("# idx  seconds\n")
        for i, dt in enumerate(t):
            f.write(f"{i:4d}  {dt:.6f}\n")
    with out_json.open("w") as f:
        json.dump(stats, f, indent=2)

    print(f"[bench] wrote {out_txt}  and  {out_json}")


if __name__ == "__main__":
    main()
