#!/usr/bin/env python3
"""MK stochastic L=24 et n=100 bootstrap — Phase 2 raffinement.

Test 1 : L=24 → L=12 (4ème point fit log-log α, ETA ~2h)
Test 2 : L=8 n=100 (bars d'erreur < 2%, ETA ~20 min)
"""
import sys, os, time, json
import numpy as np
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    BETA = 10.0
    OUT = "/tmp/voie1_calcs/results/mk_L24_n100.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    results = {"tests": []}
    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"=" * 78)
    print(f"PHASE 2 — L=24 + n=100 raffinement (GPU: {gpu})")
    print(f"=" * 78, flush=True)

    # === Test 1 : n=100 L=8 (bars d'erreur paper) ===
    print(f"\n[1/2] n=100 L=8 (bars d'erreur < 2%)")
    t0 = time.time()
    pair_n100 = mk.run_pair(L_fine=8, BETA=BETA, n_therm=200, n_meas=100,
                              mk_sweeps=1, results_path=OUT)
    results["tests"].append({"test": "n100_L8", "result": pair_n100,
                              "wall_min": (time.time()-t0)/60})
    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"  L=8 n=100 Δ={pair_n100['delta_meanP_MK_pct']:.2f}%  t={(time.time()-t0)/60:.1f}min")

    # === Test 2 : L=24 → L=12 (4ème point log-log) ===
    print(f"\n[2/2] L=24 → L=12 (4ème point α fit)")
    print(f"  ETA: ~2h (HMC L=24 ~4× L=16)", flush=True)
    t0 = time.time()
    pair_L24 = mk.run_pair(L_fine=24, BETA=BETA, n_therm=150, n_meas=20,
                            mk_sweeps=1, results_path=OUT)
    results["tests"].append({"test": "L24", "result": pair_L24,
                              "wall_min": (time.time()-t0)/60})
    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"  L=24 Δ={pair_L24['delta_meanP_MK_pct']:.2f}%  t={(time.time()-t0)/60:.1f}min")

    print(f"\n{'='*78}")
    print(f"PHASE 2 DONE — résultats /tmp/voie1_calcs/results/mk_L24_n100.json")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
