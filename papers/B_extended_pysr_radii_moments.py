#!/usr/bin/env python3
"""B — Extended PySR pattern search : hadronic radii, magnetic moments,
decay widths, coupling constants, mixing angles."""
import numpy as np
import math
import random

kappa = 1/6
alpha = 5/6
pi_const = math.pi
e_const = math.e
sqrt2 = math.sqrt(2)

# ==============================================================
# NEW DATA — radii, moments, decay constants, couplings, mixings
# ==============================================================
hadron_observables = {
    # Charge radii (fm)
    "r_p_E": 0.8409,         # proton charge radius PDG 2024 (CODATA)
    "r_p_M": 0.851,          # proton magnetic radius
    "r_n_E_sq_neg": -0.1161, # neutron charge radius squared (fm²), negative
    "r_pi_E": 0.659,         # pion charge radius
    "r_K_E": 0.581,          # kaon charge radius
    "r_D_E": 0.490,          # D meson (charm)
    # Magnetic moments (μ_N)
    "mu_p": 2.79285,
    "mu_n": -1.91304,
    "mu_Lambda": -0.613,
    "mu_Sigma_p": 2.458,
    "mu_Sigma_m": -1.160,
    "mu_Xi_0": -1.250,
    "mu_Xi_m": -0.6507,
    "mu_Omega": -2.02,
    # Axial coupling, decay constants
    "g_A": 1.2754,           # nucleon axial vector
    "g_V": 1.0,              # vector by CVC
    "g_A_g_V": 1.2754,       # ratio
    "f_pi": 92.4,            # MeV
    "f_K": 110.4,            # MeV
    "f_pi_f_K": 92.4/110.4,  # 0.837
    "f_K_f_pi": 110.4/92.4,  # 1.194
    # Quark condensate (cubic)
    "qqbar_root3": -253,     # ⟨qq̄⟩^(1/3) MeV
    # CKM angles + magnitudes
    "Vud": 0.97370,
    "Vus": 0.22501,
    "Vcb": 0.04183,
    "Vub": 0.00377,
    "sin_theta_C": 0.22501,  # Cabibbo
    "sin_theta_W_sq": 0.2312, # Weinberg
    # PMNS angles (sin² of mixing angles)
    "sin2_theta12_pmns": 0.307,
    "sin2_theta23_pmns": 0.561,
    "sin2_theta13_pmns": 0.022,
    # Pion decay width and lifetime
    # tau_pi+ ~ 2.6e-8 s, dimensionless tau · m / hbar = 5.6e7
    # Gamma_pi0 ~ 7.5 eV
    "Gamma_pi0_eV": 7.5,
    # J/psi total width
    "Gamma_Jpsi_MeV": 0.0929,
    # Wilson coefficients
    "alpha_s_MZ": 0.1179,
    "alpha_EM_inv": 137.036,
    "sin2_theta_W_running": 0.23857,
    # Bjorken x ratios in DIS — skip
    # Gluon fraction of proton momentum at low x : ~0.42
    "xg_proton": 0.42,
    # Pion mass squared / quark condensate ratio (GMOR relation)
    "GMOR_ratio": 139.570**2 / (2 * 7 * 0.92 * 92.4**2),  # m_π²/((mu+md)/2 · 2 · <qq>/f_π²)
}

# Build all useful pairwise + identity ratios
# For radii : ratio r_a/r_b
# For moments : μ_p/μ_n, μ_n/μ_Λ, etc.
# For decay : Gamma ratios
# Single values that should equal κ-formulas

print("="*78)
print("EXTENDED PATTERN HUNT — radii, moments, couplings, mixings")
print("="*78)

# Build candidate set (same as before but cleaner)
candidates_pure = []
for n_name, n_val in [("π", pi_const), ("e", e_const), ("√2", sqrt2),
                       ("π²", pi_const**2), ("2π", 2*pi_const),
                       ("π/2", pi_const/2), ("π/3", pi_const/3),
                       ("π/4", pi_const/4), ("π/6", pi_const/6),
                       ("π²/3", pi_const**2/3), ("π²/6", pi_const**2/6)]:
    candidates_pure.append((n_name, n_val))
for a in range(1, 11):
    for b in range(1, 11):
        if a == b: continue
        candidates_pure.append((f"{a}/{b}", a/b))
        if 0.1 < a/b < 10:
            candidates_pure.append((f"√({a}/{b})", math.sqrt(a/b)))

candidates_kappa = [
    ("κ", kappa),
    ("1-κ", alpha),
    ("1+κ", 1+kappa),
    ("κ·π", kappa*pi_const),
    ("(1-κ)·π", alpha*pi_const),
    ("(1-κ)·π/2", alpha*pi_const/2),
    ("(1+κ)·π/2", (1+kappa)*pi_const/2),
    ("π/(1-κ)", pi_const/alpha),       # 6π/5
    ("π/(1+κ)", pi_const/(1+kappa)),   # 6π/7
    ("π²/(1-κ)", pi_const**2/alpha),
    ("π²·κ", pi_const**2*kappa),
    ("1/(1-κ)", 1/alpha),
    ("κ/(1-κ)", kappa/alpha),
    ("(1-κ)/κ", alpha/kappa),
    ("(1+κ)/(1-κ)", (1+kappa)/alpha),
    ("(1-κ)²", alpha**2),
    ("1-κ²", 1-kappa**2),
    ("(1-κ)/(1+κ)", alpha/(1+kappa)),
    ("2κ/(1-κ)", 2*kappa/alpha),       # 2/5
    ("κ·(1-κ)", kappa*alpha),           # 5/36
    ("√κ", math.sqrt(kappa)),
    ("√(1-κ)", math.sqrt(alpha)),
    ("κ²", kappa**2),
    ("(1-κ)³", alpha**3),
    ("π·κ²", pi_const*kappa**2),
    ("2(1-κ)/(1+κ)", 2*alpha/(1+kappa)),
    ("3(1-κ)/2", 1.5*alpha),
    ("(1-κ)/3", alpha/3),
    ("(1-κ)/π", alpha/pi_const),
    ("(1+κ)/π", (1+kappa)/pi_const),
    ("κ·π²/3", kappa*pi_const**2/3),
    ("(1-κ)·π/3", alpha*pi_const/3),
    ("(1-κ)·π²/3", alpha*pi_const**2/3),
]

# Dedupe
seen = set()
candidates_kappa_d = []
for n, v in candidates_kappa:
    k = round(v, 5)
    if k not in seen:
        seen.add(k)
        candidates_kappa_d.append((n, v))
candidates_kappa = candidates_kappa_d

print(f"\nκ-candidates : {len(candidates_kappa)}")
print(f"pure candidates : {len(candidates_pure)}")

# Test each hadron observable directly + as ratios
print(f"\n=== Direct observables (single value) ===")
print(f"{'Observable':>20} {'Value':>12} {'Best κ formula':>20} {'%':>6} {'Best pure':>20} {'%':>6}")
print("-"*100)
struct_findings = []
for obs_name, obs_val in hadron_observables.items():
    if obs_val == 0:
        continue
    val = abs(obs_val)
    # Best κ match
    best_k = (float('inf'), None, 0)
    for cn, cv in candidates_kappa:
        if cv <= 0: continue
        rel = abs(val - cv)/val*100
        if rel < best_k[0]:
            best_k = (rel, cn, cv)
    # Best pure
    best_p = (float('inf'), None, 0)
    for cn, cv in candidates_pure:
        if cv <= 0: continue
        rel = abs(val - cv)/val*100
        if rel < best_p[0]:
            best_p = (rel, cn, cv)
    print(f"{obs_name:>20} {obs_val:>12.5f} {best_k[1]:>20} {best_k[0]:>5.2f}% {best_p[1]:>20} {best_p[0]:>5.2f}%")
    if best_k[0] < 0.5 and best_p[0] > best_k[0] + 1:
        struct_findings.append((obs_name, obs_val, best_k[1], best_k[2], best_k[0]))

print(f"\n=== STRUCTURAL κ-FINDINGS (κ wins by >1% over pure rational) ===")
print(f"\n{'Observable':>20} {'Value':>12} {'κ formula':>20} {'Pred':>12} {'%':>6}")
print("-"*75)
for o, v, f, fv, p in sorted(struct_findings, key=lambda x: x[4]):
    print(f"{o:>20} {v:>12.5f} {f:>20} {fv:>12.5f} {p:>5.2f}%")

# Build pairwise ratios for moments and radii (separately)
print(f"\n=== PAIRWISE RATIOS — magnetic moments ===")
moments = ["mu_p", "mu_n", "mu_Lambda", "mu_Sigma_p", "mu_Sigma_m",
           "mu_Xi_0", "mu_Xi_m", "mu_Omega"]
moment_ratios = []
for i, m1 in enumerate(moments):
    for j, m2 in enumerate(moments):
        if i >= j: continue
        v1 = hadron_observables[m1]
        v2 = hadron_observables[m2]
        if v2 == 0: continue
        r = v1/v2
        if r < 0:
            r = -r  # work with absolute values
        if 0.05 < r < 200:
            moment_ratios.append((f"|{m1}/{m2}|", r))

print(f"\n{len(moment_ratios)} moment ratios :")
for n, v in moment_ratios:
    best_k = (float('inf'), None)
    for cn, cv in candidates_kappa:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_k[0]:
            best_k = (rel, cn)
    best_p = (float('inf'), None)
    for cn, cv in candidates_pure:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_p[0]:
            best_p = (rel, cn)
    print(f"  {n:>25} = {v:>8.4f}  → κ:{best_k[1]:>15} ({best_k[0]:.2f}%)  pure:{best_p[1]:>10} ({best_p[0]:.2f}%)")

# Radii ratios
print(f"\n=== PAIRWISE RATIOS — radii ===")
radii = ["r_p_E", "r_p_M", "r_pi_E", "r_K_E", "r_D_E"]
radii_ratios = []
for i, r1 in enumerate(radii):
    for j, r2 in enumerate(radii):
        if i == j: continue
        v1 = hadron_observables[r1]
        v2 = hadron_observables[r2]
        if v1 > v2:
            radii_ratios.append((f"{r1}/{r2}", v1/v2))

print(f"\n{len(radii_ratios)} radii ratios :")
for n, v in radii_ratios:
    best_k = (float('inf'), None)
    for cn, cv in candidates_kappa:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_k[0]:
            best_k = (rel, cn)
    best_p = (float('inf'), None)
    for cn, cv in candidates_pure:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_p[0]:
            best_p = (rel, cn)
    print(f"  {n:>15} = {v:>8.4f}  → κ:{best_k[1]:>15} ({best_k[0]:.2f}%)  pure:{best_p[1]:>10} ({best_p[0]:.2f}%)")

# CKM matrix elements
print(f"\n=== CKM matrix elements ===")
ckm = ["Vud", "Vus", "Vcb", "Vub"]
for c in ckm:
    v = hadron_observables[c]
    best_k = (float('inf'), None)
    for cn, cv in candidates_kappa:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_k[0]:
            best_k = (rel, cn)
    best_p = (float('inf'), None)
    for cn, cv in candidates_pure:
        if cv <= 0: continue
        rel = abs(v - cv)/v*100
        if rel < best_p[0]:
            best_p = (rel, cn)
    print(f"  {c:>15} = {v:>8.5f}  → κ:{best_k[1]:>15} ({best_k[0]:.2f}%)  pure:{best_p[1]:>10} ({best_p[0]:.2f}%)")

print("\nDONE.")
