#!/usr/bin/env python3
"""PySR symbolic regression sur Δ(L) MK stochastic — chercher formule géométrique.

Hypothèses à tester :
  - Δ = C/L (géométrique pur, prédiction DS Bot+Kevin)
  - Δ = C/L^α (sub-linéaire empirique)
  - Δ = C/L + correction bulk
  - Δ = C·log(L)/L (correction log)
  - Δ = C·exp(-c·L) (exponentiel)

Inputs : data points (L, Δ) accumulés (L=4, 6, 8, 12, 16 après batterie + L=16).
Output : formule symbolique de plus basse complexité.
"""
import json, os, numpy as np


def load_all_results():
    """Aggregate Δ(L) from all available result files."""
    data = []

    # Baseline L=8 (PAIR 1) + L=12 (PAIR 2) from initial MK run
    try:
        with open("/root/cc-private/docs/session_2026-05-23/results/kolmogorov_v2_results.json") as f:
            pass  # this is the original CuPy v2, different format
    except: pass

    # Initial MK stochastic results
    try:
        with open("/tmp/voie1_calcs/results/migdal_kadanoff.json") as f:
            mk_base = json.load(f)
        for p in mk_base.get("pairs", []):
            data.append({
                "L": p["L_fine"], "Δ_MK_pct": p["delta_meanP_MK_pct"],
                "source": "initial_MK"
            })
    except Exception as e: print(f"MK base load fail: {e}")

    # Battery tests (L=4, L=6, MK_SWEEPS scan, β=20)
    try:
        with open("/tmp/voie1_calcs/results/mk_battery.json") as f:
            batt = json.load(f)
        for t in batt.get("tests", []):
            if t["test"] == "B_L_scan":
                data.append({
                    "L": t["L_fine"], "Δ_MK_pct": t["result"]["delta_meanP_MK_pct"],
                    "source": "battery_B"
                })
    except Exception as e: print(f"Battery load fail: {e}")

    # L=16 quick
    try:
        with open("/tmp/voie1_calcs/results/mk_L16_quick.json") as f:
            d16 = json.load(f)
        data.append({
            "L": d16["L_fine"], "Δ_MK_pct": d16["pair"]["delta_meanP_MK_pct"],
            "source": "L16_quick"
        })
    except Exception as e: print(f"L16 load fail: {e}")

    return data


def fit_candidate_formulas(L_arr, d_arr):
    """Compare 5 candidate formulas via χ² fit."""
    from scipy.optimize import curve_fit
    candidates = {
        "Δ = C/L":               (lambda L, C: C/L,                                       [10.0]),
        "Δ = C/L^α":             (lambda L, C, alpha: C/L**alpha,                         [10.0, 1.0]),
        "Δ = C·log(L)/L":        (lambda L, C: C*np.log(L)/L,                             [10.0]),
        "Δ = C/L + D/L²":        (lambda L, C, D: C/L + D/L**2,                           [10.0, 0.0]),
        "Δ = C·exp(-c·L)":       (lambda L, C, c: C*np.exp(-c*L),                         [10.0, 0.1]),
    }
    print(f"\n{'Formula':<25} {'χ²':>10} {'params':>40}")
    print(f"{'-'*80}")
    for name, (f, p0) in candidates.items():
        try:
            popt, _ = curve_fit(f, L_arr, d_arr, p0=p0)
            resid = d_arr - f(L_arr, *popt)
            chi2 = np.sum(resid**2)
            params_str = ", ".join([f"{p:.3f}" for p in popt])
            print(f"  {name:<25} {chi2:>10.3f} {params_str:>40}")
        except Exception as e:
            print(f"  {name:<25} FAIL {e}")


def try_pysr(L_arr, d_arr):
    """If PySR installed, run symbolic regression."""
    try:
        from pysr import PySRRegressor
    except ImportError:
        print("\n[PySR not installed — skip symbolic regression]")
        return
    model = PySRRegressor(
        niterations=40, populations=30, population_size=50,
        binary_operators=["+", "-", "*", "/", "^"],
        unary_operators=["log", "exp"],
        model_selection="best", progress=False, verbosity=0,
        constraints={"^": (-1, 2)},
        complexity_of_operators={"log": 2, "exp": 2, "^": 2},
        maxsize=15,
    )
    X = L_arr.reshape(-1, 1)
    y = d_arr
    model.fit(X, y, variable_names=["L"])
    print(f"\n{'='*78}")
    print(f"PySR top 5 expressions (sorted by score):")
    print(f"{'='*78}")
    print(model.equations_[['complexity', 'loss', 'equation']].head(5))


def main():
    print("="*78)
    print("PySR / symbolic regression analysis Δ(L) MK stochastic")
    print("="*78)

    data = load_all_results()
    if not data:
        print("No data loaded — wait for batterie + L=16 to finish first.")
        return
    print(f"\n{len(data)} datapoints loaded:")
    for d in data:
        print(f"  L={d['L']:>3}: Δ={d['Δ_MK_pct']:.2f}%  [{d['source']}]")

    L_arr = np.array([d["L"] for d in data], dtype=float)
    d_arr = np.array([d["Δ_MK_pct"] for d in data])

    # Sort
    idx = np.argsort(L_arr)
    L_arr = L_arr[idx]; d_arr = d_arr[idx]

    if len(L_arr) < 3:
        print(f"\n  Only {len(L_arr)} points — need ≥3 for meaningful fit.")
        return

    fit_candidate_formulas(L_arr, d_arr)
    try_pysr(L_arr, d_arr)

    # Save
    out = {"data": data, "fit_done": True}
    with open("/tmp/voie1_calcs/results/pysr_delta_L.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved /tmp/voie1_calcs/results/pysr_delta_L.json")


if __name__ == "__main__":
    main()
