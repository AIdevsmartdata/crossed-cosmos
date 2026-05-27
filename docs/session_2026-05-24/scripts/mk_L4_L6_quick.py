#!/usr/bin/env python3
"""MK L=4→L=2 et L=6→L=3 quick tests — points additionnels fit log-log."""
import sys, os, time, json
import cupy as cp

sys.path.insert(0, "/tmp")
import importlib.util
spec = importlib.util.spec_from_file_location("mk", "/tmp/migdal_kadanoff_stochastic.py")
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)


def main():
    BETA = 10.0
    OUT = "/tmp/voie1_calcs/results/mk_L4_L6.json"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    results = {"tests": []}
    print(f"=" * 78)
    print(f"MK L=4 + L=6 quick tests (points additionnels fit log-log)")
    print(f"=" * 78, flush=True)

    for L_f in [4, 6]:
        print(f"\n[L={L_f}→L={L_f//2}]", flush=True)
        t0 = time.time()
        try:
            pair = mk.run_pair(L_fine=L_f, BETA=BETA, n_therm=150, n_meas=25,
                                mk_sweeps=1, results_path=OUT)
            results["tests"].append({"L_fine": L_f, "result": pair,
                                      "wall_s": time.time()-t0})
            with open(OUT, "w") as f: json.dump(results, f, indent=2)
            print(f"  L={L_f} Δ={pair['delta_meanP_MK_pct']:.2f}%  t={(time.time()-t0)/60:.1f}min")
        except Exception as e:
            print(f"  ERROR L={L_f}: {e}")
            results["tests"].append({"L_fine": L_f, "error": str(e)})

    with open(OUT, "w") as f: json.dump(results, f, indent=2)
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
