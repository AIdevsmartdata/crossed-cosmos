#!/usr/bin/env python3
"""T1 — Extend β-scan to β=300, 500, 1000 to test α=5/6 convergence.
Reuse mk_beta_scan_largeb.py structure, append to existing results.
"""
import sys, os, time, json
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    OUT = "/tmp/voie1_calcs/results/mk_beta_extend.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    # Read existing results
    existing = []
    existing_path = "/tmp/voie1_calcs/results/mk_beta_scan.json"
    if os.path.exists(existing_path):
        with open(existing_path) as f:
            data = json.load(f)
        existing = data.get("tests", [])
    print(f"Existing β-scan : {[t['beta'] for t in existing]}")
    print(f"Existing Δ⟨P⟩MK%: {[round(t['result']['delta_meanP_MK_pct'], 2) for t in existing]}")

    results = {"tests": list(existing)}
    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"=" * 78)
    print(f"T1 — EXTEND β-scan β=300, 500, 1000 (SU(2) D=4 L=8 sw=5)")
    print(f"GPU: {gpu}")
    print(f"=" * 78, flush=True)

    NEW_BETAS = [300.0, 500.0, 1000.0]
    for BETA in NEW_BETAS:
        print(f"\n[β={BETA}] L=8 sw=5 n=25", flush=True)
        t0 = time.time()
        try:
            pair = mk.run_pair(L_fine=8, BETA=BETA, n_therm=300, n_meas=25,
                                mk_sweeps=5, results_path=OUT)
            results["tests"].append({"beta": BETA, "result": pair, "wall_min": (time.time()-t0)/60})
            with open(OUT, "w") as f: json.dump(results, f, indent=2)
            print(f"  β={BETA}: Δ⟨P⟩MK={pair['delta_meanP_MK_pct']:.3f}% "
                  f"ΔCLSI={pair['delta_CLSI_MK_pct']:.3f}%")
        except Exception as e:
            print(f"  ERROR β={BETA}: {e}")

    # Final fit
    import numpy as np
    print(f"\n{'='*78}\nFIT FINAL α (9 points si tout livré)\n{'='*78}")
    betas = []
    deltas = []
    for t in results["tests"]:
        betas.append(t.get("beta") if "beta" in t else t["result"]["beta"])
        deltas.append(t["result"]["delta_meanP_MK_pct"]/100)
    betas = np.array(betas)
    deltas = np.array(deltas)
    print(f"β all      : {betas}")
    print(f"Δ all (%)  : {deltas*100}")
    if len(betas) >= 4:
        slope, _ = np.polyfit(np.log(betas), np.log(deltas), 1)
        alpha = -slope
        print(f"\nFit log-log α = {alpha:.4f}")
        print(f"vs 5/6 = {5/6:.4f} → écart {abs(alpha-5/6)/(5/6)*100:.2f}%")
        print(f"vs Pinsker α=1 → écart {abs(alpha-1)*100:.2f}%")

    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
