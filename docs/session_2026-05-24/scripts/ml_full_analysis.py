#!/usr/bin/env python3
"""ML + PySR full analysis on all MK data — Phase 1.

Inputs : tous les JSON /tmp/voie1_calcs/results/
Tests :
  (A) Δ(sweeps) à L=8 : fit modèle relaxation exp Δ_0·exp(-sw/τ) + Δ_∞
  (B) Δ(L) cross-L à sw=1 : fit C/L^α, plateau, C/L+D/L²
  (C) PySR symbolic regression : laisse découvrir
"""
import json, os, sys
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

R = Path("/tmp/voie1_calcs/results")


def load_all_data():
    """Aggregate all MK datapoints (L, sweeps, β, Δ⟨P⟩, ΔC_LSI, n_meas)."""
    data = []

    # Initial MK PAIR 1 (L=8 sw=1) + PAIR 2 (L=12 sw=1)
    try:
        d = json.loads((R / "migdal_kadanoff.json").read_text())
        for p in d.get("pairs", []):
            data.append({
                "L": p["L_fine"], "sweeps": p["mk_sweeps"], "beta": p["beta"],
                "n_meas": p["n_meas"], "delta_P": p["delta_meanP_MK_pct"],
                "delta_CLSI": p["delta_CLSI_MK_pct"], "src": "initial",
                "var_P_MK": p.get("var_P_MK"), "var_P_coarse": p.get("var_P_coarse"),
            })
    except Exception as e: print(f"  initial MK fail: {e}")

    # Battery tests : MK_SWEEPS scan L=8
    try:
        d = json.loads((R / "mk_battery.json").read_text())
        for t in d.get("tests", []):
            r = t.get("result", {})
            if t.get("test") == "A_MK_SWEEPS":
                data.append({
                    "L": 8, "sweeps": t["n_sweeps"], "beta": 10.0,
                    "n_meas": r.get("n_meas", 25),
                    "delta_P": r["delta_meanP_MK_pct"],
                    "delta_CLSI": r["delta_CLSI_MK_pct"], "src": "battery_A",
                    "var_P_MK": r.get("var_P_MK"), "var_P_coarse": r.get("var_P_coarse"),
                })
    except Exception as e: print(f"  battery fail: {e}")

    # L=4 + L=6 quick
    try:
        d = json.loads((R / "mk_L4_L6.json").read_text())
        for t in d.get("tests", []):
            r = t.get("result", {})
            if "delta_meanP_MK_pct" in r:
                data.append({
                    "L": t["L_fine"], "sweeps": 1, "beta": 10.0,
                    "n_meas": r.get("n_meas", 25),
                    "delta_P": r["delta_meanP_MK_pct"],
                    "delta_CLSI": r["delta_CLSI_MK_pct"], "src": "L4_L6",
                    "var_P_MK": r.get("var_P_MK"), "var_P_coarse": r.get("var_P_coarse"),
                })
    except Exception as e: print(f"  L4_L6 fail: {e}")

    # L=16 quick
    try:
        d = json.loads((R / "mk_L16_quick.json").read_text())
        p = d.get("pair", {})
        if p:
            data.append({
                "L": p["L_fine"], "sweeps": p["mk_sweeps"], "beta": p["beta"],
                "n_meas": p["n_meas"],
                "delta_P": p["delta_meanP_MK_pct"], "delta_CLSI": p["delta_CLSI_MK_pct"],
                "src": "L16", "var_P_MK": p.get("var_P_MK"),
                "var_P_coarse": p.get("var_P_coarse"),
            })
    except Exception as e: print(f"  L16 fail: {e}")

    return data


def fit_exp_relaxation(sweeps, delta):
    """Fit Δ(sweeps) = Δ_0 · exp(-sweeps/τ) + Δ_∞."""
    def model(sw, D0, tau, Dinf):
        return D0 * np.exp(-sw/tau) + Dinf
    try:
        popt, pcov = curve_fit(model, sweeps, delta, p0=[10.0, 2.0, 0.0],
                                bounds=([0, 0.1, -10], [50, 20, 20]))
        D0, tau, Dinf = popt
        sigma = np.sqrt(np.diag(pcov))
        resid = delta - model(sweeps, *popt)
        chi2 = np.sum(resid**2)
        return {"D0": D0, "tau": tau, "Dinf": Dinf,
                "sigma_D0": sigma[0], "sigma_tau": sigma[1], "sigma_Dinf": sigma[2],
                "chi2": chi2}
    except Exception as e:
        return {"error": str(e)}


def fit_L_scaling(L, delta):
    """Fit Δ(L) = C/L^α and other candidates."""
    L = np.asarray(L, dtype=float); delta = np.asarray(delta)
    candidates = {
        "Δ=C/L":                  (lambda L, C: C/L,                          [10.0]),
        "Δ=C/L^α":                (lambda L, C, a: C/L**a,                    [10.0, 1.0]),
        "Δ=C·log(L)/L":           (lambda L, C: C*np.log(L)/L,                [10.0]),
        "Δ=C/L+D/L²":             (lambda L, C, D: C/L + D/L**2,              [10.0, 0.0]),
        "Δ=plateau (const)":      (lambda L, C: C * np.ones_like(L),          [5.0]),
        "Δ=plateau+drift/L":      (lambda L, A, B: A + B/L,                   [5.0, 0.0]),
    }
    results = {}
    for name, (f, p0) in candidates.items():
        try:
            popt, pcov = curve_fit(f, L, delta, p0=p0)
            resid = delta - f(L, *popt)
            chi2 = np.sum(resid**2)
            r2 = 1 - chi2 / np.sum((delta - delta.mean())**2)
            sigma = np.sqrt(np.diag(pcov)) if len(p0) == len(np.diag(pcov)) else None
            results[name] = {"params": popt.tolist(), "chi2": float(chi2),
                              "r2": float(r2), "sigma": sigma.tolist() if sigma is not None else None}
        except Exception as e:
            results[name] = {"error": str(e)}
    return results


def main():
    print("="*78)
    print("ML + PySR full analysis MK data")
    print("="*78)

    data = load_all_data()
    print(f"\n{len(data)} datapoints :")
    print(f"  {'L':>3} {'sw':>3} {'β':>4} {'n':>4}  {'ΔP %':>7}  {'ΔCLSI %':>9}  {'src':<12}")
    for d in data:
        print(f"  {d['L']:>3} {d['sweeps']:>3} {d['beta']:>4} {d['n_meas']:>4}  "
              f"{d['delta_P']:>7.2f}  {d['delta_CLSI']:>9.2f}  {d['src']:<12}")

    # ====================================================================
    # (A) Δ(sweeps) à L=8
    # ====================================================================
    print(f"\n{'='*78}")
    print(f"(A) Δ(sweeps) à L=8 — fit relaxation exp")
    print(f"{'='*78}")
    sw_data = [(d["sweeps"], d["delta_P"], d["delta_CLSI"]) for d in data if d["L"] == 8]
    sw_data.sort()
    sweeps = np.array([s[0] for s in sw_data], dtype=float)
    dP = np.array([s[1] for s in sw_data])
    dC = np.array([s[2] for s in sw_data])

    print(f"\n  Data sweeps (L=8) :")
    for sw, p, c in sw_data:
        print(f"    sw={sw}: ΔP={p:.2f}% ΔCLSI={c:.2f}%")

    if len(sweeps) >= 3:
        print(f"\n  Fit ΔP(sweeps) = D₀·exp(-sw/τ) + D_∞:")
        fit_P = fit_exp_relaxation(sweeps, dP)
        if "error" not in fit_P:
            print(f"    D₀ = {fit_P['D0']:.2f} ± {fit_P['sigma_D0']:.2f}")
            print(f"    τ  = {fit_P['tau']:.2f} ± {fit_P['sigma_tau']:.2f}")
            print(f"    D_∞ = {fit_P['Dinf']:.2f} ± {fit_P['sigma_Dinf']:.2f}")
            print(f"    χ² = {fit_P['chi2']:.4f}")
        else:
            print(f"    ERROR: {fit_P['error']}")

        print(f"\n  Fit ΔCLSI(sweeps) = D₀·exp(-sw/τ) + D_∞:")
        fit_C = fit_exp_relaxation(sweeps, dC)
        if "error" not in fit_C:
            print(f"    D₀ = {fit_C['D0']:.2f} ± {fit_C['sigma_D0']:.2f}")
            print(f"    τ  = {fit_C['tau']:.2f} ± {fit_C['sigma_tau']:.2f}")
            print(f"    D_∞ = {fit_C['Dinf']:.2f} ± {fit_C['sigma_Dinf']:.2f}")
            print(f"    χ² = {fit_C['chi2']:.4f}")
            if fit_C['Dinf'] < 2.0 and fit_C['Dinf'] - 2*fit_C['sigma_Dinf'] < 0:
                print(f"    ⭐⭐⭐ D_∞ < 2% AND compatible 0 (2σ)")
                print(f"        → Conjecture C* en CLSI metric SUPPORTED empirically")
            elif fit_C['Dinf'] < 3.0:
                print(f"    ⭐ D_∞ < 3% — support partiel")

    # ====================================================================
    # (B) Δ(L) cross-L à sw=1
    # ====================================================================
    print(f"\n{'='*78}")
    print(f"(B) Δ(L) cross-L à sw=1 — fit géométrique vs plateau")
    print(f"{'='*78}")
    L_data = [(d["L"], d["delta_P"], d["delta_CLSI"]) for d in data if d["sweeps"] == 1]
    L_data.sort()
    print(f"\n  Data sw=1 cross-L:")
    for L, p, c in L_data:
        print(f"    L={L}: ΔP={p:.2f}% ΔCLSI={c:.2f}%")

    if len(L_data) >= 3:
        L_arr = np.array([L for L, _, _ in L_data], dtype=float)
        dP_arr = np.array([p for _, p, _ in L_data])

        print(f"\n  Fit candidates pour ΔP(L) sw=1:")
        fits = fit_L_scaling(L_arr, dP_arr)
        print(f"  {'Model':<25} {'χ²':>8} {'R²':>8} {'params':<30}")
        for name, f in sorted(fits.items(), key=lambda x: x[1].get("chi2", 1e9)):
            if "error" in f:
                print(f"  {name:<25} ERROR")
            else:
                params_str = ", ".join([f"{p:.3f}" for p in f["params"]])
                print(f"  {name:<25} {f['chi2']:>8.3f} {f['r2']:>8.3f}  {params_str}")

    # ====================================================================
    # (C) PySR symbolic — Δ(L, sweeps)
    # ====================================================================
    print(f"\n{'='*78}")
    print(f"(C) PySR symbolic regression Δ(L, sweeps)")
    print(f"{'='*78}")
    try:
        from pysr import PySRRegressor
        # All data : ΔP comme target, features (L, sweeps)
        X = np.array([[d["L"], d["sweeps"]] for d in data], dtype=float)
        y_P = np.array([d["delta_P"] for d in data])
        y_C = np.array([d["delta_CLSI"] for d in data])

        print(f"  ΔP fit (n={len(y_P)}):")
        model_P = PySRRegressor(
            niterations=30, populations=20, population_size=40,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["exp", "log"],
            model_selection="best", progress=False, verbosity=0,
            constraints={"^": (-1, 2)}, maxsize=12,
        )
        model_P.fit(X, y_P, variable_names=["L", "sweeps"])
        print(f"  Top 5 expressions ΔP:")
        for i, row in model_P.equations_[['complexity', 'loss', 'equation']].head(5).iterrows():
            print(f"    [{row['complexity']:>2}] loss={row['loss']:.4f}  {row['equation']}")

        print(f"\n  ΔCLSI fit (n={len(y_C)}):")
        model_C = PySRRegressor(
            niterations=30, populations=20, population_size=40,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["exp", "log"],
            model_selection="best", progress=False, verbosity=0, maxsize=12,
        )
        model_C.fit(X, y_C, variable_names=["L", "sweeps"])
        print(f"  Top 5 expressions ΔCLSI:")
        for i, row in model_C.equations_[['complexity', 'loss', 'equation']].head(5).iterrows():
            print(f"    [{row['complexity']:>2}] loss={row['loss']:.4f}  {row['equation']}")

    except Exception as e:
        print(f"  PySR error: {e}")
        import traceback; traceback.print_exc()

    # Save aggregated
    OUT = R / "ml_full_analysis.json"
    with open(OUT, "w") as f:
        json.dump({"data": data, "n_datapoints": len(data)}, f, indent=2)
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
