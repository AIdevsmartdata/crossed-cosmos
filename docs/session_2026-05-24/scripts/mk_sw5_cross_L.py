#!/usr/bin/env python3
"""MK sweeps=5 cross-L test — confirmer Conjecture C* en métrique C_LSI.

DS Bot finding : MK_SWEEPS=5 donne Δ C_LSI = 1.17% à L=8. Si confirmé cross-L avec
bars d'erreur précises → TIER 1 publishable Conjecture C* en C_LSI metric.

Tests (priorité):
  1. L=8 sw=5 n=100 (bootstrap précis ~30 min)
  2. L=12 sw=5 n=25 (cross-L ~15 min)
  3. L=16 sw=5 n=25 (cross-L confirmation ~40 min)
"""
import sys, os, time, json
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    BETA = 10.0
    MK_SWEEPS = 5
    OUT = "/tmp/voie1_calcs/results/mk_sw5_cross_L.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    results = {"tests": [], "MK_SWEEPS": MK_SWEEPS, "beta": BETA}
    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"=" * 78)
    print(f"MK sw={MK_SWEEPS} CROSS-L test (confirmer Conjecture C* en C_LSI metric)")
    print(f"GPU: {gpu}")
    print(f"=" * 78, flush=True)

    # Priority 1: L=8 sw=5 n=100 (bootstrap précis)
    print(f"\n[1/3] L=8 sw=5 n=100 (bootstrap précis)")
    t0 = time.time()
    pair = mk.run_pair(L_fine=8, BETA=BETA, n_therm=200, n_meas=100,
                        mk_sweeps=MK_SWEEPS, results_path=OUT)
    results["tests"].append({"L": 8, "n_meas": 100, "result": pair,
                              "wall_min": (time.time()-t0)/60})
    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"  L=8 n=100 sw=5: Δ⟨P⟩={pair['delta_meanP_MK_pct']:.2f}% ΔCLSI={pair['delta_CLSI_MK_pct']:.2f}%")

    # Priority 2: L=12 sw=5 n=25
    print(f"\n[2/3] L=12 sw=5 n=25")
    t0 = time.time()
    pair = mk.run_pair(L_fine=12, BETA=BETA, n_therm=200, n_meas=25,
                        mk_sweeps=MK_SWEEPS, results_path=OUT)
    results["tests"].append({"L": 12, "n_meas": 25, "result": pair,
                              "wall_min": (time.time()-t0)/60})
    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"  L=12 sw=5: Δ⟨P⟩={pair['delta_meanP_MK_pct']:.2f}% ΔCLSI={pair['delta_CLSI_MK_pct']:.2f}%")

    # Priority 3: L=16 sw=5 n=25
    print(f"\n[3/3] L=16 sw=5 n=25")
    t0 = time.time()
    pair = mk.run_pair(L_fine=16, BETA=BETA, n_therm=200, n_meas=25,
                        mk_sweeps=MK_SWEEPS, results_path=OUT)
    results["tests"].append({"L": 16, "n_meas": 25, "result": pair,
                              "wall_min": (time.time()-t0)/60})
    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"  L=16 sw=5: Δ⟨P⟩={pair['delta_meanP_MK_pct']:.2f}% ΔCLSI={pair['delta_CLSI_MK_pct']:.2f}%")

    # Final verdict
    print(f"\n{'='*78}")
    print(f"VERDICT — Conjecture C* en C_LSI metric")
    print(f"{'='*78}")
    print(f"  L=8 sw=5 n=100 : ΔCLSI = {results['tests'][0]['result']['delta_CLSI_MK_pct']:.2f}%")
    print(f"  L=12 sw=5 n=25 : ΔCLSI = {results['tests'][1]['result']['delta_CLSI_MK_pct']:.2f}%")
    print(f"  L=16 sw=5 n=25 : ΔCLSI = {results['tests'][2]['result']['delta_CLSI_MK_pct']:.2f}%")

    all_clsi = [t['result']['delta_CLSI_MK_pct'] for t in results['tests']]
    mean_clsi = sum(all_clsi) / len(all_clsi)
    print(f"\n  Mean Δ C_LSI MK_SWEEPS=5 cross-L = {mean_clsi:.2f}%")
    if mean_clsi < 3:
        print(f"  ⭐⭐⭐ Δ < 3% → Conjecture C* TIER 1 SUPPORTED en C_LSI")
    elif mean_clsi < 5:
        print(f"  ⭐ Δ < 5% → support partiel TIER 2")
    else:
        print(f"  🟡 Δ ≥ 5% → encore à raffiner")


if __name__ == "__main__":
    main()
