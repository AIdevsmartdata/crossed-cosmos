#!/usr/bin/env python3
"""
H37 — Investigation profonde de sin²θ_W = 3/13.

WHY 13 ?

Hypothèses :
1. 13 = b_2(K3) - 9 = 22 - 9 = 13
2. 13 = rank(E_6) + rank(E_7) = 6 + 7
3. 13 = dim_fund + dim_adj + rank = 3 + 8 + 2 = 13 (SU(3))
4. 13 = nombre de générateurs distincts (trivial + 3 + 8 + 1) = 13
5. 13 = 6ème nombre premier

WHY 3 ?
1. 3 = N_c (couleurs)
2. 3 = rank SU(3) + 1 = 2 + 1
3. 3 = generations SM
4. 3 = dim_fund(SU(3))

Cross-check : autres ratios SM avec /13 ?

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np

# SM constants (PDG 2024)
SIN2_THETA_W_MS = 0.23121
SIN2_THETA_W_OS = 1 - (80.379/91.1876)**2  # on-shell
ALPHA_S_MZ = 0.1179
ALPHA_EM_MZ = 1/127.951
M_W = 80.379
M_Z = 91.1876
M_H = 125.10
V_HIGGS = 246.22
M_T = 172.57
M_B = 4.18

# Lattice anchors
KAPPA_FP_SU2 = 0.5
KAPPA_FP_SU3 = 1/6
KAPPA_EE_SU2 = 0.508
KAPPA_EE_SU3 = 0.603
KAPPA_INF = 1.2020569 / np.sqrt(np.pi)

print("="*70)
print("H37 — Investigation 3/13 sin²θ_W mystery")
print("="*70)

print(f"\nMesures observées :")
print(f"  sin²θ_W (MS-bar) = {SIN2_THETA_W_MS:.5f}")
print(f"  sin²θ_W (on-shell) = {SIN2_THETA_W_OS:.5f}")
print(f"  3/13 = {3/13:.5f}")
print(f"    vs MS-bar : Δ = {(3/13-SIN2_THETA_W_MS)/SIN2_THETA_W_MS*100:+.3f}%")
print(f"    vs on-shell : Δ = {(3/13-SIN2_THETA_W_OS)/SIN2_THETA_W_OS*100:+.3f}%")
print(f"  cos²θ_W = 10/13 = {10/13:.5f}")
print(f"    obs (1-sin²) = {1-SIN2_THETA_W_MS:.5f}, Δ = {(10/13-(1-SIN2_THETA_W_MS))/(1-SIN2_THETA_W_MS)*100:+.3f}%")
print()

# Why 13 ?
print("--- Hypothèses pour 13 ---")
print(f"  H_a : 13 = dim_fund SU(3) + dim_adj SU(3) + rank SU(3) = 3 + 8 + 2 = {3+8+2}")
print(f"  H_b : 13 = b_2(K3) - 9 = 22 - 9 = {22-9}  (avec 9 = dim_anti-fund + adj + 0)")
print(f"  H_c : 13 = rank E_6 + rank E_7 = 6 + 7 = {6+7}")
print(f"  H_d : 13 = 6th prime")
print(f"  H_e : 13 = N(N²-1)/N for N=4: 4·15/4 = 15 (no)")
print()

# 3 = N_c or fund SU(3)
print("--- Hypothèses pour 3 ---")
print(f"  3 = dim_fund(SU(3)) — couleurs quarks")
print(f"  3 = nombre de générations SM")
print(f"  3 = rank(SU(3)) + 1")
print()

print("--- Interprétation H_a ---")
print(f"  Si 13 = dim_fund(SU(3)) + dim_adj(SU(3)) + rank(SU(3)) = 3+8+2 :")
print(f"    sin²θ_W = 3/13 = dim_fund / (dim_fund + dim_adj + rank)")
print(f"    = fraction de 'matière fondamentale' dans le total SU(3) state-space")
print(f"  ")
print(f"    Plausible — c'est analogue à dimension d'un sous-secteur")
print()

# Other ratios with q=13
print("--- Cherchons d'autres ratios SM /13 ---")
candidates = [
    ('α_s(M_Z)', ALPHA_S_MZ),
    ('α_em(M_Z)', ALPHA_EM_MZ),
    ('m_W/m_Z', M_W/M_Z),
    ('m_W/m_t', M_W/M_T),
    ('m_b/m_t', M_B/M_T),
    ('m_H/m_W', M_H/M_W),
    ('m_Z/v', M_Z/V_HIGGS),
    ('m_H/v', M_H/V_HIGGS),
    ('(m_W/m_Z)²', (M_W/M_Z)**2),
    ('cos²θ_W', 1-SIN2_THETA_W_MS),
    ('cos⁴θ_W', (1-SIN2_THETA_W_MS)**2),
]
for label, val in candidates:
    n_best = round(val * 13)
    if n_best > 0:
        ratio = n_best / 13
        diff = (ratio - val)/val * 100
        if abs(diff) < 5:
            print(f"  {label} = {val:.4f} ≈ {n_best}/13 = {ratio:.4f}  Δ={diff:+.2f}%")

# What gives 11.46/13 ?
print()
print("--- m_W/m_Z ≈ 11.46/13 ? ---")
print(f"  m_W/m_Z = {M_W/M_Z:.4f}")
print(f"  Try 0.882 = 8/9.07 hmm")
print(f"  cos θ_W = {np.cos(np.arcsin(np.sqrt(SIN2_THETA_W_MS))):.4f}")
print(f"  √(10/13) = {np.sqrt(10/13):.4f}")
print(f"  m_W/m_Z = cos θ_W = √(1-sin²) = √(10/13) = {np.sqrt(10/13):.4f}")
print(f"    obs m_W/m_Z = {M_W/M_Z:.4f}")
print(f"    diff = {(np.sqrt(10/13)-M_W/M_Z)/(M_W/M_Z)*100:.3f}%")
print()

# Test : if sin²θ_W = 3/13, then m_W/m_Z = √(10/13)
print("--- Cohérence interne : si sin²θ_W = 3/13 ---")
sin2W_pred = 3/13
cos2W_pred = 10/13
print(f"  Predicted sin²θ_W = {sin2W_pred:.5f} vs obs {SIN2_THETA_W_MS:.5f} = {(sin2W_pred-SIN2_THETA_W_MS)/SIN2_THETA_W_MS*100:+.3f}%")
print(f"  Predicted cos²θ_W = {cos2W_pred:.5f} vs obs {1-SIN2_THETA_W_MS:.5f} = {(cos2W_pred-(1-SIN2_THETA_W_MS))/(1-SIN2_THETA_W_MS)*100:+.3f}%")
print(f"  Predicted m_W/m_Z = √(10/13) = {np.sqrt(10/13):.5f} vs obs {M_W/M_Z:.5f}")
print(f"  Predicted (m_W/m_Z)² = 10/13 = {10/13:.5f} vs obs {(M_W/M_Z)**2:.5f}")
print(f"    Note : (m_W/m_Z)² = 0.7770, while 10/13 = 0.7692 — Δ = 1%")
print(f"    Donc sin²θ_W on-shell = 1 - (m_W/m_Z)² = 0.2230, pas 3/13 = 0.2308")
print()

# Examine relation cos²θ_W = ρ_param × something?
print("--- ρ parameter : ρ = m_W²/(m_Z²·cos²θ_W) = ? ---")
sin2_eff = 0.23156  # effective leptonic
cos2_eff = 1 - sin2_eff
rho = (M_W/M_Z)**2 / cos2_eff
print(f"  ρ = {rho:.5f}  (obs ≈ 1.00038 from electroweak fits)")
print(f"  Si sin²θ_W = 3/13 et ρ=1 exactement :")
print(f"    (m_W/m_Z)² = 10/13 → 0.7692 vs obs (kin) 0.7770")
print(f"    Discrepancy ~1% = radiative corrections (oblique parameters T, S)")
print()
print("CONCLUSION : sin²θ_W = 3/13 vaut pour MS-bar scheme, pas on-shell.")
print("Le 13 = 3+8+2 = dim SU(3)(fund) + dim SU(3)(adj) + rank SU(3).")
print("Le 3 = fraction fondamentale = sin²θ_W.")
print("Le 10 = adj + rank = 8 + 2 = fraction des dof non-fundamental.")
print()

# Predictions if 3/13 universal
print("--- Predictions si interpretation H_a correcte ---")
print(f"  Pour SU(N) hypothétique :")
for N in [2, 3, 4, 5, 6]:
    d_fund = N
    d_adj = N**2 - 1
    rank = N - 1
    total = d_fund + d_adj + rank
    frac = d_fund / total
    print(f"    SU({N}) : 'sin²θ' = {d_fund}/{total} = {frac:.5f}")
print()
print(f"  Si la formule sin²θ = dim_fund/(dim_fund + dim_adj + rank) tient,")
print(f"  alors SU(2) groupe faible donnerait 'sin²θ' = 2/(2+3+1) = 2/6 = 1/3 = 0.333")
print(f"  Mais sin²θ_W observe est 0.231 — donc N=3 (SU(3) couleur), pas SU(2)_L")
print(f"  Cela suggère que sin²θ_W est dicté par le secteur COULEUR, pas EW directement.")
