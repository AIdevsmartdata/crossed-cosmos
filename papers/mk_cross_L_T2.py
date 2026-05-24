#!/usr/bin/env python3
"""T2 — Cross-L scan β=50 fixed, L=12, 16, 24 to test volume independence of α.

Si α est volume-indépendant (claim théorique), Δ⟨P⟩MK doit suivre une loi
indépendante de L (modulo corrections finite-size). Test critique pour
notre framework (uniformité OW alleged).
"""
import sys, os, time, json
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    OUT = "/tmp/voie1_calcs/results/mk_cross_L_T2.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    results = {"tests": []}
    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"=" * 78)
    print(f"T2 — CROSS-L scan β=50 (SU(2) D=4 sw=5)")
    print(f"GPU: {gpu}")
    print(f"=" * 78, flush=True)

    BETA = 50.0
    for L in [12, 16, 24]:
        if L > 16:
            n_meas = 15
            n_therm = 200
        elif L == 16:
            n_meas = 20
            n_therm = 250
        else:
            n_meas = 25
            n_therm = 300

        print(f"\n[L={L} β={BETA}] sw=5 n_meas={n_meas}", flush=True)
        t0 = time.time()
        try:
            pair = mk.run_pair(L_fine=L, BETA=BETA, n_therm=n_therm, n_meas=n_meas,
                                mk_sweeps=5, results_path=OUT)
            results["tests"].append({"L": L, "result": pair, "wall_min": (time.time()-t0)/60})
            with open(OUT, "w") as f: json.dump(results, f, indent=2)
            print(f"  L={L}: Δ⟨P⟩MK={pair['delta_meanP_MK_pct']:.3f}% "
                  f"ΔCLSI={pair['delta_CLSI_MK_pct']:.3f}% "
                  f"wall={(time.time()-t0)/60:.1f}min")
        except Exception as e:
            print(f"  ERROR L={L}: {e}")
            import traceback
            traceback.print_exc()

    # Verdict
    print(f"\n{'='*78}")
    print(f"VERDICT T2 — Volume independence test")
    print(f"{'='*78}")
    print(f"  L=8 baseline (β=50) : 1.52% (from mk_beta_scan)")
    for t in results["tests"]:
        print(f"  L={t['L']}: Δ⟨P⟩MK={t['result']['delta_meanP_MK_pct']:.3f}%")

    print(f"\n  Si Δ stable cross-L → α volume-indep CONFIRMED")
    print(f"  Si Δ grows with L → α volume-dependent (theoretical claim FALSIFIED)")

    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
