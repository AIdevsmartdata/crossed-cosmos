#!/usr/bin/env python3
"""
H20 v2 + H21 v2 — detrend + Fourier + rational strobing per DS Bot proposal.

1. Refit κ_smooth(N) = α√N + β + γ·N^p using ALL 4 dense (5,6,7,8) plateaus
2. Compute residuals Δκ(N, L) per N for L=4,6,8,10 (12 data points)
3. Spectral check : the dominant frequency in Δκ vs r = dim(G)/L²
4. Rational strobing : pics at r = p/q simples

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import json
import numpy as np
from scipy.optimize import curve_fit


def extract_per_L(json_path):
    d = json.load(open(json_path))
    rows = []
    res = d.get('results', {})
    if isinstance(res, dict):
        for L_key, v in res.items():
            L = int(L_key) if isinstance(L_key, str) and L_key.isdigit() else v.get('L_x')
            if L is None: continue
            c = v.get('c_per_2D')
            cerr = v.get('c_err')
            if c is not None:
                rows.append((L, float(c), float(cerr if cerr else 0)))
    return rows


def main():
    files = {
        5: 'papers/2026-05-24-session/data/pc-maison-su56/jax_su5_THERM5000.json',
        7: 'papers/2026-05-24-session/data/pc-maison-su56/jax_su7_THERM5000_2026-05-26.json',
        8: 'papers/2026-05-24-session/data/pc-maison-su56/jax_su8_THERM5000_2026-05-26.json',
    }

    data = {}
    for N, f in files.items():
        try:
            rows = extract_per_L(f)
            data[N] = {}
            for L, c, cerr in rows:
                kappa = abs(c) / L
                kappa_err = cerr / L if L else 0
                data[N][L] = (kappa, max(kappa_err, 0.005))
        except Exception as e:
            print(f"SU({N}) extract err: {e}")
            continue

    # Step 1 : Compute "plateau" κ(N) = mean of L=8,10 (well-thermalized large L)
    print("=== Plateau values L>=8 ===")
    plateau = {}
    for N in sorted(data.keys()):
        vals = [data[N][L] for L in [8, 10] if L in data[N]]
        if vals:
            ws = np.array([1/v[1]**2 for v in vals])
            mean = np.sum([v[0]*w for v, w in zip(vals, ws)]) / np.sum(ws)
            err = 1/np.sqrt(np.sum(ws))
            plateau[N] = (mean, err)
            print(f"  SU({N}): plateau κ = {mean:.4f} ± {err:.4f}")

    # We also know SU(6) plateau = 0.810 from previous session (added by hand)
    plateau[6] = (0.810, 0.005)  # from session memory
    # SU(2), SU(3), SU(4) for dilute regime context
    plateau[2] = (0.508, 0.005)
    plateau[3] = (0.603, 0.005)
    plateau[4] = (0.633, 0.004)

    # Step 2 : Refit affine α√N + β on dense plateau (5,6,7,8)
    print("\n=== Affine fit κ = α√N + β on (5,6,7,8) plateau ===")
    Ns = np.array([5, 6, 7, 8])
    kappas = np.array([plateau[N][0] for N in Ns])
    kerrs = np.array([plateau[N][1] for N in Ns])
    def affine(N, alpha, beta):
        return alpha * np.sqrt(N) + beta
    popt, pcov = curve_fit(affine, Ns, kappas, p0=[0.5, -0.4],
                            sigma=kerrs, absolute_sigma=True)
    alpha_new, beta_new = popt
    perr = np.sqrt(np.diag(pcov))
    print(f"  α = {alpha_new:.4f} ± {perr[0]:.4f}")
    print(f"  β = {beta_new:.4f} ± {perr[1]:.4f}")
    chi2 = np.sum(((kappas - affine(Ns, *popt))/kerrs)**2)
    print(f"  χ²/dof = {chi2:.2f}/{len(Ns)-2}")
    for N in Ns:
        pred = affine(N, *popt)
        obs = plateau[N][0]
        err = plateau[N][1]
        print(f"  SU({N}): obs {obs:.4f}, pred {pred:.4f}, Δ={obs-pred:+.4f} ({(obs-pred)/err:+.1f}σ)")

    # Try α√N + β + γ/N
    print("\n=== Curvature fit κ = α√N + β + γ/N on (5,6,7,8) plateau ===")
    def curvature(N, alpha, beta, gamma):
        return alpha * np.sqrt(N) + beta + gamma/N
    try:
        popt2, pcov2 = curve_fit(curvature, Ns, kappas, p0=[0.5, -0.4, 0],
                                  sigma=kerrs, absolute_sigma=True)
        a, b, g = popt2
        perr2 = np.sqrt(np.diag(pcov2))
        print(f"  α = {a:.4f}, β = {b:.4f}, γ = {g:.4f}")
        chi2_2 = np.sum(((kappas - curvature(Ns, *popt2))/kerrs)**2)
        print(f"  χ²/dof = {chi2_2:.2f}/{len(Ns)-3}")
        for N in Ns:
            pred = curvature(N, *popt2)
            obs = plateau[N][0]
            err = plateau[N][1]
            print(f"  SU({N}): obs {obs:.4f}, pred {pred:.4f}, Δ={obs-pred:+.4f} ({(obs-pred)/err:+.1f}σ)")
        # Predictions
        for N_pred in [9, 10, 11, 12]:
            pred = curvature(N_pred, *popt2)
            pred_aff = affine(N_pred, *popt)
            print(f"  SU({N_pred}) pred (curv) = {pred:.4f}, (affine) = {pred_aff:.4f}")
    except Exception as e:
        print(f"Curvature fit fail: {e}")

    # Try α·N^p form
    print("\n=== Power-law fit κ = α·N^p + β on (5,6,7,8) ===")
    def powerlaw(N, alpha, p, beta):
        return alpha * N**p + beta
    try:
        popt3, pcov3 = curve_fit(powerlaw, Ns, kappas, p0=[0.5, 0.5, -0.4],
                                  sigma=kerrs, absolute_sigma=True)
        a, p, b = popt3
        perr3 = np.sqrt(np.diag(pcov3))
        print(f"  α = {a:.4f}, p = {p:.4f}, β = {b:.4f}")
        chi2_3 = np.sum(((kappas - powerlaw(Ns, *popt3))/kerrs)**2)
        print(f"  χ²/dof = {chi2_3:.2f}/{len(Ns)-3}")
        for N in Ns:
            pred = powerlaw(N, *popt3)
            obs = plateau[N][0]
            err = plateau[N][1]
            print(f"  SU({N}): obs {obs:.4f}, pred {pred:.4f}, Δ={obs-pred:+.4f}")
        # Predictions
        for N_pred in [9, 10, 11, 12]:
            pred = powerlaw(N_pred, *popt3)
            print(f"  SU({N_pred}) pred (power p={p:.3f}) = {pred:.4f}")
    except Exception as e:
        print(f"Power fit fail: {e}")

    # Step 3 : Detrend with curvature fit, look at per-L residuals
    print("\n=== Per-L residuals using curvature fit ===")
    print(f"{'N':<3} {'L':<3} {'ratio':<8} {'κ obs':<8} {'κ_curv':<8} {'Δκ':<10} {'σ':<5}")
    print("-" * 70)
    residuals = []
    for N in sorted(data.keys()):
        for L in sorted(data[N].keys()):
            kappa, kerr = data[N][L]
            kcurv = curvature(N, *popt2)
            delta = kappa - kcurv
            r = (N**2 - 1) / L**2
            residuals.append((N, L, r, delta, kerr))
            print(f"{N:<3} {L:<3} {r:<8.3f} {kappa:<8.4f} {kcurv:<8.4f} {delta:+.4f}    {delta/kerr:+.1f}")

    # H22 — check rational strobing
    print("\n=== H22 Rational strobing test ===")
    print("Hypothèse : Δκ extremums sur r = p/q simples ?")
    sorted_res = sorted(residuals, key=lambda x: x[2])
    rationals = [(1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (1, 1), (3, 2), (2, 1), (3, 1), (4, 1)]
    for p, q in rationals:
        r_target = p/q
        closest = min(sorted_res, key=lambda x: abs(x[2] - r_target))
        N, L, r, delta, kerr = closest
        if abs(r - r_target) < 0.3:
            print(f"  r = {p}/{q} = {r_target:.3f} : closest data SU({N}) L={L} r={r:.3f}, Δκ={delta:+.4f} ({delta/kerr:+.1f}σ)")


if __name__ == '__main__':
    main()
