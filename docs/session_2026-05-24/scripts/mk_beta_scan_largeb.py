#!/usr/bin/env python3
"""H_β∞ test : MK sw=5 L=8 cross-β = 50, 100, 200.

Si convergence Gaussienne avec β grand → Gap 1 fermé empiriquement.
Cible : TV → 0 (Δ⟨P⟩ block vs coarse → 0).
"""
import sys, os, time, json
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    OUT = "/tmp/voie1_calcs/results/mk_beta_scan.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    results = {"tests": []}
    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"=" * 78)
    print(f"H_β∞ TEST — MK sw=5 L=8 cross-β = 50, 100, 200")
    print(f"GPU: {gpu}")
    print(f"=" * 78, flush=True)

    for BETA in [50.0, 100.0, 200.0]:
        print(f"\n[β={BETA}] L=8 sw=5 n=25", flush=True)
        t0 = time.time()
        try:
            pair = mk.run_pair(L_fine=8, BETA=BETA, n_therm=300, n_meas=25,
                                mk_sweeps=5, results_path=OUT)
            results["tests"].append({"beta": BETA, "result": pair, "wall_min": (time.time()-t0)/60})
            with open(OUT, "w") as f: json.dump(results, f, indent=2)
            print(f"  β={BETA}: Δ⟨P⟩MK={pair['delta_meanP_MK_pct']:.2f}% ΔCLSI={pair['delta_CLSI_MK_pct']:.2f}%")
        except Exception as e:
            print(f"  ERROR β={BETA}: {e}")

    # Verdict
    print(f"\n{'='*78}")
    print(f"VERDICT H_β∞")
    print(f"{'='*78}")
    print(f"  Trend Δ⟨P⟩ MK avec β :")
    print(f"  β=10 (reference) : 5.89% (PAIR 1)")
    for t in results["tests"]:
        print(f"  β={t['beta']:.0f}: Δ⟨P⟩={t['result']['delta_meanP_MK_pct']:.2f}% ΔCLSI={t['result']['delta_CLSI_MK_pct']:.2f}%")

    if results["tests"]:
        last = results["tests"][-1]
        if last["result"]["delta_meanP_MK_pct"] < 1:
            print(f"\n  ⭐⭐⭐ Δ < 1% à β grand → Gaussian limit confirmée → Gap 1 fermé empiriquement")
        elif last["result"]["delta_meanP_MK_pct"] < 3:
            print(f"\n  ⭐ Δ < 3% à β grand → convergence vers Gaussian")
        else:
            print(f"\n  🟡 Δ encore >3% à β grand → mécanisme à raffiner")

    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
