#!/usr/bin/env python3
"""PySR hadronique : chercher patterns dans ratios sans dimension.

Features : κ, |Φ⁺|, D, N_c, α_EM, sin²θ_W, π, √2, ... (variables structurelles)
Targets : m_n/m_p, m_π/m_p, m_K/m_p, m_ρ/m_p, m_Δ/m_p, m_0++/m_p, m_2++/m_0++, etc.
"""
import numpy as np
import math
from pysr import PySRRegressor

# ==============================================================
# Features structurelles du framework
# ==============================================================
kappa = 1/6
alpha = 1 - kappa  # = 5/6
phi_plus = 3
D = 4
N_c = 3
alpha_EM = 1/137.036
sin2_theta_W = 0.2312
pi_const = math.pi
sqrt2 = math.sqrt(2)
sqrt3 = math.sqrt(3)
e_const = math.e

# ==============================================================
# Hadronic data (PDG 2024, MeV)
# ==============================================================
m_proton = 938.272
m_neutron = 939.565
m_pi_pm = 139.570
m_pi_0 = 134.977
m_K_pm = 493.677
m_K_0 = 497.611
m_eta = 547.862
m_rho = 775.26
m_omega = 782.65
m_phi_meson = 1019.46  # ss-bar
m_K_star = 891.66  # vector strange
m_Delta = 1232.0  # baryon resonance
m_Lambda = 1115.683
m_Sigma_p = 1189.37
m_Xi_0 = 1314.86
m_Omega_baryon = 1672.45
m_J_psi = 3096.9  # c-cbar
m_Upsilon = 9460.4  # b-bbar
m_glueball_0pp = 1730  # AT2021 lattice prediction (GeV → MeV factor: 1.73 GeV)
m_glueball_2pp = 2400  # AT2021 ≈ m_0++ · √2
m_glueball_0mp = 2595  # AT2021 ≈ m_0++ · 3/2

# Lattice quantities (in MeV, after fixing scale)
Lambda_QCD = 250  # MeV approx
sigma_tension = 440  # MeV (sqrt of tension)
f_pi = 92.4  # MeV (pion decay constant)
m_u_bare = 2.16
m_d_bare = 4.67
m_s_bare = 93.4
m_c_bare = 1270
m_b_bare = 4180
m_t_bare = 172570
m_electron = 0.5110
m_muon = 105.66
m_tau = 1776.86

# ==============================================================
# Build target ratios (dimensionless)
# ==============================================================
targets = [
    # Hadron mass ratios
    ("m_n/m_p", m_neutron/m_proton),                  # 1.00138 (small EM split)
    ("(m_n-m_p)/m_p", (m_neutron-m_proton)/m_proton), # 0.00138
    ("m_pi/m_p", m_pi_pm/m_proton),                   # 0.149
    ("m_K/m_p", m_K_pm/m_proton),                     # 0.526
    ("m_eta/m_p", m_eta/m_proton),                    # 0.584
    ("m_rho/m_p", m_rho/m_proton),                    # 0.826
    ("m_Delta/m_p", m_Delta/m_proton),                # 1.313
    ("m_Lambda/m_p", m_Lambda/m_proton),              # 1.189
    ("m_Omega_b/m_p", m_Omega_baryon/m_proton),       # 1.782
    # Meson ratios
    ("m_K/m_pi", m_K_pm/m_pi_pm),                     # 3.537
    ("m_eta/m_pi", m_eta/m_pi_pm),                    # 3.925
    ("m_rho/m_pi", m_rho/m_pi_pm),                    # 5.554
    ("m_K*/m_K", m_K_star/m_K_pm),                    # 1.806 (Regge tower)
    ("m_phi/m_omega", m_phi_meson/m_omega),           # 1.303 (s-quark)
    # Glueball
    ("m_2++/m_0++", m_glueball_2pp/m_glueball_0pp),   # ≈ √2 (already in framework!)
    ("m_0-+/m_0++", m_glueball_0mp/m_glueball_0pp),   # ≈ 3/2 (already!)
    # QCD scales
    ("m_p/Lambda_QCD", m_proton/Lambda_QCD),          # 3.753
    ("m_p/sigma_root", m_proton/sigma_tension),       # 2.13 (∝ AT2021 m/√σ)
    ("f_pi/m_p", f_pi/m_proton),                      # 0.0985
    ("f_pi/Lambda_QCD", f_pi/Lambda_QCD),             # 0.370
    # Charm/bottom states
    ("m_Jpsi/m_p", m_J_psi/m_proton),                 # 3.30
    ("m_Upsilon/m_p", m_Upsilon/m_proton),            # 10.08
]

print(f"Total targets : {len(targets)}")
print(f"\n{'Target':>20} {'Value':>10}")
for n, v in targets:
    print(f"{n:>20} {v:>10.6f}")

# ==============================================================
# Build feature matrix for PySR
# ==============================================================
# Strategy : feed κ as the single variable, with constants available implicitly
# PySR will combine κ with constants 1, 2, 3, π, √2, etc.

# For each target, we just give κ as the input feature
# and let PySR try to fit f(κ) = target
X = np.array([[kappa]] * len(targets))
y_vals = np.array([v for _, v in targets])

# Actually for proper PySR multi-target, we need separate fits per target
# Let me try a different angle : fit ALL targets with KEY features

# Treat each target as a separate datapoint
# Features per datapoint : add target-index info
# But that doesn't make physical sense.

# Better : fit each target with its own PySR run, look for the simplest formula
# with features {κ, α_EM, π, √2, √3, integers}

print("\n" + "="*78)
print("PySR run 1 : try to fit m_n/m_p with κ + α_EM")
print("="*78)

# m_n/m_p with feature κ and α_EM
# Quick approximation : m_n/m_p ≈ 1 + (m_d - m_u)/(m_p) - α_EM·constant
target_name, target_val = "m_n/m_p", m_neutron/m_proton
print(f"\nTarget {target_name} = {target_val:.6f}")
print(f"Naïve test : 1 + α_EM = {1 + alpha_EM:.6f}")
print(f"Naïve test : 1 + α_EM·(m_d-m_u)/m_p = {1 + alpha_EM*((m_d_bare-m_u_bare)/m_proton):.6f}")
print(f"Naïve test : 1 + (m_d-m_u)/m_p = {1 + (m_d_bare-m_u_bare)/m_proton:.6f}")
print(f"  → vraie origine = m_d > m_u + EM (mass différence quarks), pas κ")

# PySR symbolic regression
print(f"\n--- PySR on all 22 ratios with single var κ ---")
print(f"Target : ratio_i = f(κ) for i = 1..{len(targets)}")
print(f"(C'est test si une SEULE expression de κ peut reproduire tous les ratios)")

# Random feature matrix : each row is a different target, but only feature is κ (constant)
# That can't work because all rows are identical
# Instead : add a 'target index' as feature (artificial), see if PySR finds a relation

# Use index as feature (ratio order in PDG)
indices = np.array([[i] for i in range(len(targets))])
y_vals = np.array([v for _, v in targets])

# This is a degenerate case — PySR can't find a meaningful pattern this way
# Let's instead do individual fits for the ratios that might have κ-dependence

print(f"\nSkip blanket fit (insufficient feature variety).")
print(f"\nInstead : check specific candidates ratio-by-ratio")
print(f"{'-'*60}")

# Specific test : compute candidates with κ
candidates_kappa = [
    ("κ", kappa),
    ("1-κ", 1-kappa),
    ("κ²", kappa**2),
    ("1/(1-κ)", 1/(1-kappa)),
    ("1+κ", 1+kappa),
    ("κ·π", kappa*pi_const),
    ("κ·√2", kappa*sqrt2),
    ("√κ", math.sqrt(kappa)),
    ("1-κ²", 1-kappa**2),
    ("(1-κ)²", (1-kappa)**2),
    ("2(1-κ)/(1+κ)", 2*(1-kappa)/(1+kappa)),
    ("(1-κ)/κ", (1-kappa)/kappa),  # = 5
    ("π·(1-κ)/2", pi_const*(1-kappa)/2),
    ("α_EM/κ", alpha_EM/kappa),
    ("κ/α_EM", kappa/alpha_EM),
    ("√(2/3)", math.sqrt(2/3)),  # = σ_8
    ("(D-1)/(2D|Φ⁺|)", (D-1)/(2*D*phi_plus)),  # = λ_H
    ("2π·(1-κ)", 2*pi_const*(1-kappa)),
    ("|Φ⁺|·κ", phi_plus*kappa),
    ("D·κ", D*kappa),
]

print(f"\nCandidate κ-formulas with values :")
for n, v in candidates_kappa:
    print(f"  {n:>20} = {v:>10.5f}")

# Now for each target, find closest κ-formula
print(f"\n--- Per-target search ---")
print(f"{'Target':>20} {'Value':>10} | {'Best κ-formula':>20} {'Pred':>10} {'rel %':>8}")
print("-"*80)

for n, v in targets:
    best_diff = float('inf')
    best_name = ""
    best_pred = 0
    for cn, cv in candidates_kappa:
        diff = abs(v - cv)
        rel = abs(diff/v*100) if v != 0 else float('inf')
        if rel < best_diff:
            best_diff = rel
            best_name = cn
            best_pred = cv
    print(f"{n:>20} {v:>10.5f} | {best_name:>20} {best_pred:>10.5f} {best_diff:>7.2f}%")

# Now run PySR on those targets with single κ feature
# and constants {1, 2, 3, 4, π, √2}
print("\n" + "="*78)
print("PySR full run : per-target search with multiple features")
print("="*78)

# Better PySR setup : provide multiple features (κ, α_EM, etc.) as VECTOR, run on EACH target separately
# Then aggregate Pareto front per target

# Setup features (single row, all targets share)
# To do per-target search, we need at least 2 data points
# So we'll do this differently : use the 22 targets as separate scalar PySR problems

# Quick filter : keep targets where naive κ-formula gives <5% match
print(f"\nTargets that already match a simple κ-formula within 5% :")
for n, v in targets:
    for cn, cv in candidates_kappa:
        if abs((v-cv)/v*100) < 5:
            print(f"  {n} = {v:.4f} ≈ {cn} = {cv:.4f}  ({abs((v-cv)/v*100):.2f}%)")
            break

print(f"\nMatches at 1% :")
for n, v in targets:
    for cn, cv in candidates_kappa:
        if abs((v-cv)/v*100) < 1:
            print(f"  {n} = {v:.4f} ≈ {cn} = {cv:.4f}  ({abs((v-cv)/v*100):.2f}%)")
            break

# Try PySR scalar mode on the most promising ratio
print(f"\n--- PySR scalar fit attempts ---")

# Setup feature vector : multiple values of (κ, α_EM) creating fake variation
# We can't fit a single ratio with PySR easily, but can do model selection on tabulated candidates

# Build a feature table and fit cross-target patterns
# For each target, compute correlations with κ, log(κ), 1/κ, sqrt(κ) etc.
import numpy as np

# Convert targets to log-space for additive analysis
y_log = np.array([math.log(v) for _, v in targets if v > 0])
target_names = [n for n, v in targets if v > 0]

# Test : do log(ratio_i) cluster around multiples of log(2), log(3), log(π), log(κ) ?
log_features = {
    "log(2)": math.log(2),
    "log(3)": math.log(3),
    "log(π)": math.log(pi_const),
    "log(1/κ)": math.log(1/kappa),  # = log(6)
    "log(5/6)": math.log(5/6),
    "log(α_EM)": math.log(alpha_EM),
}

print(f"\nlog feature values :")
for n, v in log_features.items():
    print(f"  {n:>15} = {v:>10.5f}")

# For each target, decompose log(ratio) into sum of integer multiples of log features
# log(ratio) = a*log(2) + b*log(3) + c*log(π) + d*log(1/κ) + e*log(α_EM)
# Solve for (a,b,c,d,e) with LASSO or grid search

print(f"\nLook for log(target) ≈ integer combination of log(2), log(3), log(π) :")
for n, v in targets:
    if v <= 0:
        continue
    lv = math.log(v)
    best_combo = None
    best_diff = float('inf')
    for a in range(-3, 4):
        for b in range(-3, 4):
            for c in range(-2, 3):
                pred = a*math.log(2) + b*math.log(3) + c*math.log(pi_const)
                d = abs(pred - lv)
                if d < best_diff and abs(a)+abs(b)+abs(c) <= 4:
                    best_diff = d
                    best_combo = (a, b, c, pred)
    if best_combo and best_diff < 0.1:  # log diff < 0.1 means ratio diff < 10%
        a, b, c, pred = best_combo
        formula = f"2^{a}·3^{b}·π^{c}"
        rel_pct = abs((math.exp(pred) - v)/v*100)
        print(f"  {n:>20} {v:>10.4f} ≈ {formula:>15} = {math.exp(pred):>10.4f}  ({rel_pct:.2f}%)")

print("\nDONE.")
