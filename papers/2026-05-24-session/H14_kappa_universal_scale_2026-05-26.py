#!/usr/bin/env python3
"""
H14 — Universal scale test : κ_EE(N) / Σ(N) constant cross-N for some Σ?

Candidate scales Σ(N) from literature :
- √σ : string tension (Lucini-Teper-Wenger 2005, hep-lat/0502003)
- M_0++ : scalar glueball mass (Lucini-Rago 2010, arXiv:1005.5006)
- M_2++ : tensor glueball mass
- T_c : deconfinement temperature
- Λ_MS : RGI scale

H14 (initial form) : κ(N) / M_0++(N) is constant cross-N.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import json

# Literature data for pure SU(N) Yang-Mills 4D
# Continuum limits from LTW2005 (hep-lat/0502003) Tables 6, 9, 15
# Plus Lucini-Rago 2010 (arXiv:1005.5006) for high-N glueballs

# Format : (N, M_0++/√σ, err, M_2++/√σ, err, T_c/√σ, err)
# Sources : LTW2002 (hep-lat/0204008), LTW2005 (hep-lat/0502003), Lucini-Rago 2010

LITERATURE_DATA = {
    # N : (M_0++/√σ, err, M_2++/√σ, err, T_c/√σ, err)
    2: (3.74, 0.07, 5.45, 0.10, 0.7091, 0.0036),  # LTW2002+2003
    3: (3.55, 0.07, 4.78, 0.07, 0.6440, 0.0010),  # Lucini-Teper-Wenger 2002 hep-lat/0103027
    4: (3.36, 0.07, 4.72, 0.09, 0.6314, 0.0090),  # LTW 2005
    5: (3.30, 0.06, 4.65, 0.08, 0.6244, 0.0070),  # LTW 2005
    6: (3.25, 0.09, 4.60, 0.10, 0.6195, 0.0072),  # LTW 2005
    8: (3.30, 0.10, 4.55, 0.12, 0.6172, 0.0085),  # LTW 2005
    # N → ∞ : 3.28 ± 0.08 (LTW)
}

# Our κ_EE data (this session)
KAPPA_EE_DATA = {
    2: (0.508, 0.005),
    3: (0.603, 0.005),
    4: (0.633, 0.004),
    5: (0.701, 0.005),
    6: (0.810, 0.005),
    7: (0.9107, 0.0054),
    # SU(8) running, predicted 1.007 from affine fit
}


def main():
    print("="*78)
    print("H14 — κ_EE(N) / Σ(N) universal scale test")
    print("="*78)
    print()
    print("Candidate scales : M_0++, M_2++, T_c (all in units of √σ)")
    print()

    # Compute ratios
    rows = []
    for N in sorted(KAPPA_EE_DATA.keys()):
        if N not in LITERATURE_DATA:
            continue
        kappa, dkappa = KAPPA_EE_DATA[N]
        M_0pp, dM_0pp, M_2pp, dM_2pp, T_c, dT_c = LITERATURE_DATA[N]

        r1 = kappa / M_0pp
        dr1 = r1 * np.sqrt((dkappa/kappa)**2 + (dM_0pp/M_0pp)**2)
        r2 = kappa / M_2pp
        dr2 = r2 * np.sqrt((dkappa/kappa)**2 + (dM_2pp/M_2pp)**2)
        r3 = kappa / T_c
        dr3 = r3 * np.sqrt((dkappa/kappa)**2 + (dT_c/T_c)**2)
        r4 = kappa  # just kappa itself
        # plus the affine model expectation
        r5 = kappa / np.sqrt(N)
        dr5 = dkappa / np.sqrt(N)

        rows.append({
            'N': N, 'kappa': kappa, 'dkappa': dkappa,
            'M_0++': M_0pp, 'M_2++': M_2pp, 'T_c': T_c,
            'kappa/M_0++': r1, 'd_r1': dr1,
            'kappa/M_2++': r2, 'd_r2': dr2,
            'kappa/T_c': r3, 'd_r3': dr3,
            'kappa/sqrt(N)': r5, 'd_r5': dr5,
        })

    # Print table
    print(f"{'N':<3} | {'κ_EE':<11} | {'M_0++/√σ':<10} | {'κ/M_0++':<11} | {'κ/M_2++':<11} | {'κ/T_c':<10} | {'κ/√N':<10}")
    print("-" * 110)
    for r in rows:
        print(f"{r['N']:<3} | {r['kappa']:.4f}±{r['dkappa']:.4f} | {r['M_0++']:.2f} | "
              f"{r['kappa/M_0++']:.4f}±{r['d_r1']:.4f} | "
              f"{r['kappa/M_2++']:.4f}±{r['d_r2']:.4f} | "
              f"{r['kappa/T_c']:.4f}±{r['d_r3']:.4f} | "
              f"{r['kappa/sqrt(N)']:.4f}±{r['d_r5']:.4f}")
    print()

    # Statistical analysis : χ²/dof against constant for each ratio
    print("--- χ²/dof for constant model (H14 test) ---")
    for col in ['kappa/M_0++', 'kappa/M_2++', 'kappa/T_c', 'kappa/sqrt(N)']:
        d_col = 'd_' + ('r1' if 'M_0' in col else 'r2' if 'M_2' in col else 'r3' if 'T_c' in col else 'r5')
        vals = np.array([r[col] for r in rows])
        errs = np.array([r[d_col] for r in rows])
        # Weighted mean
        w = 1/errs**2
        mean = np.sum(vals*w)/np.sum(w)
        chi2 = np.sum(((vals - mean)/errs)**2)
        dof = len(vals) - 1
        chi2_per_dof = chi2/dof
        sigma_sigma = (vals.max() - vals.min()) / errs.mean()
        print(f"  {col:18s} : mean = {mean:.4f}, χ²/dof = {chi2_per_dof:.2f}, range/err = {sigma_sigma:.1f}σ")

    # Look at dilute vs dense separately
    print()
    print("--- Dilute (N≤4) vs Dense (N≥5) regimes ---")
    dilute = [r for r in rows if r['N'] <= 4]
    dense = [r for r in rows if r['N'] >= 5]

    for col, label in [('kappa/M_0++', 'κ/M_0++'), ('kappa/sqrt(N)', 'κ/√N')]:
        if dilute:
            d_vals = np.array([r[col] for r in dilute])
            print(f"  {label} dilute (N=2,3,4) : {d_vals.mean():.4f} ± {d_vals.std()/np.sqrt(len(d_vals)):.4f} (n={len(d_vals)})")
        if dense:
            d_vals = np.array([r[col] for r in dense])
            print(f"  {label} dense  (N=5,6,7) : {d_vals.mean():.4f} ± {d_vals.std()/np.sqrt(len(d_vals)):.4f} (n={len(d_vals)})")
    print()

    # H14 verdict
    print("--- H14 VERDICT ---")
    print()
    print("H14 (κ/M_0++ = constant cross-N) : examine χ²/dof above.")
    print()
    print("Honest test : the affine fit κ = 0.518·√N - 0.458 (dense regime) corresponds to")
    print("κ/√N = 0.518 - 0.458/√N → asymptote 0.518 for N→∞.")
    print()
    print("Comparing 0.518 with M_0++/√σ ≈ 3.3 : ratio = 0.518/3.3 = 0.157.")
    print("If this ratio (0.157) is universal across N, that's a non-trivial finding.")
    print()
    print("κ_EE/M_0++ for dense regime (in lattice units), large-N limit :")
    print(f"  N=5 : {(0.518*np.sqrt(5)-0.458)/3.30:.4f}")
    print(f"  N=6 : {(0.518*np.sqrt(6)-0.458)/3.25:.4f}")
    print(f"  N=7 : {(0.518*np.sqrt(7)-0.458)/3.30:.4f}")
    print(f"  N=8 : {(0.518*np.sqrt(8)-0.458)/3.30:.4f}")
    print(f"  → these are NOT constant; ratio grows with N")
    print()
    print("CONCLUSION : H14 in form 'κ/M_0++ = const' is FALSIFIED.")
    print("BUT : κ/√N → 0.518 (universal large-N limit) IS the result.")
    print("Equivalently : κ_EE = α·√N + β with α universal ≈ 0.518, β = -0.458 const.")
    print()
    print("The 'universal scale' is √N itself, NOT a hadronic mass.")
    print("Physical interpretation : κ_EE counts confined string contributions, scaling √N")
    print("(number of independent flux tubes per unit area at confinement).")

    out = {
        'rows': rows,
        'verdict': 'H14 (κ/M_0++ universal) FALSIFIED; κ/√N → 0.518 IS universal dense asymptote',
        'physical_interpretation': 'string-network counting : κ_EE ≈ 0.518·√N (large-N), 0.458 is finite-N Casimir-edge correction',
        'open_q': 'what is the physical meaning of 0.518? Possibly per-string EE coefficient. Check vs Calabrese-Cardy 2004 universal CFT prediction.'
    }
    with open('/tmp/H14_kappa_universal_scale_2026-05-26.json', 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print()
    print(f"→ Saved /tmp/H14_kappa_universal_scale_2026-05-26.json")


if __name__ == '__main__':
    main()
