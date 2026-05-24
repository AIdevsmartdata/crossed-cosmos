#!/usr/bin/env python3
"""Test Koide formula généralisée pour TOUTES les familles de fermions.

K = (∑ m_i) / (∑ √m_i)²

Koide originel : K_leptons = 2/3 EXACT à 10⁻⁵
Hypothèse : K_X = f(κ) pour quarks up, down, neutrinos.
"""
import math
import numpy as np

kappa = 1/6
pi_const = math.pi

# PDG 2024 fermion masses (MeV)
# Leptons
m_e = 0.510999
m_mu = 105.6583755
m_tau = 1776.86

# Quark masses MS-bar (use consistent scale)
# At 2 GeV scale (most common)
m_u = 2.16    # MeV
m_d = 4.67
m_s = 93.4
# At 'pole' or running scale
m_c = 1270   # at m_c
m_b = 4180   # at m_b
m_t = 172690 # pole, GeV → MeV = 172.69 GeV

# Neutrinos: only mass-squared differences known
# Δm²_21 ≈ 7.5e-5 eV² (solar)
# Δm²_32 ≈ 2.5e-3 eV² (atmospheric)
# Absolute scale unknown, < 0.1 eV (KATRIN + cosmology)
# Use central NH (normal hierarchy) with m_lightest = 0
m_nu1 = 1e-6  # placeholder eV, m_lightest
m_nu2 = math.sqrt(7.5e-5)  # ≈ 0.00866 eV
m_nu3 = math.sqrt(2.5e-3)  # ≈ 0.05 eV
# Convert to MeV
m_nu1_MeV = m_nu1 * 1e-6
m_nu2_MeV = m_nu2 * 1e-6
m_nu3_MeV = m_nu3 * 1e-6

def koide(masses):
    """K = (sum m) / (sum sqrt(m))^2"""
    s = sum(masses)
    s_root = sum(math.sqrt(m) for m in masses if m > 0)
    return s / s_root**2

# ============================================================
# Test families
# ============================================================
families = {
    "Charged leptons (e, μ, τ)": [m_e, m_mu, m_tau],
    "Up-type quarks (u, c, t)": [m_u, m_c, m_t],
    "Down-type quarks (d, s, b)": [m_d, m_s, m_b],
    "Neutrinos (NH, m_1=0)": [1e-12, m_nu2_MeV, m_nu3_MeV],
    "Neutrinos (IH, m_3=0)": [m_nu2_MeV, m_nu3_MeV, 1e-12],  # actually different structure
    "All 6 leptons + neutrinos": [m_e, m_mu, m_tau, m_nu1_MeV, m_nu2_MeV, m_nu3_MeV],
    "All 6 quarks (u,d,c,s,t,b)": [m_u, m_d, m_c, m_s, m_t, m_b],
    "(u, c)": [m_u, m_c],
    "(d, s)": [m_d, m_s],
    "(c, b)": [m_c, m_b],
    "(s, b)": [m_s, m_b],
    "(u, t)": [m_u, m_t],
    "Generation 1 (u, d, e, nu_e)": [m_u, m_d, m_e, m_nu1_MeV],
    "Generation 2 (c, s, μ, nu_μ)": [m_c, m_s, m_mu, m_nu2_MeV],
    "Generation 3 (t, b, τ, nu_τ)": [m_t, m_b, m_tau, m_nu3_MeV],
    "Up-type + leptons": [m_u, m_c, m_t, m_e, m_mu, m_tau],
}

print("="*78)
print("KOIDE FORMULA TEST — generalized")
print("="*78)
print(f"\nκ = 1/6 = {kappa:.6f}")
print(f"4κ = 2/3 = {4*kappa:.6f}")

print(f"\n{'Family':>45} {'K = ∑m/(∑√m)²':>15} {'4κ ?':>8} {'rel %':>8}")
print("-"*90)

results = []
target_4k = 4*kappa
for name, masses in families.items():
    if len(masses) < 2:
        continue
    masses_pos = [m for m in masses if m > 0]
    if len(masses_pos) < 2:
        continue
    K = koide(masses_pos)
    rel_4k = abs(K - target_4k)/target_4k * 100 if target_4k > 0 else float('inf')
    flag = "✅" if rel_4k < 1 else "🟡" if rel_4k < 5 else "❌"
    print(f"{name:>45} {K:>15.6f} {target_4k:>8.4f} {rel_4k:>7.2f}% {flag}")
    results.append((name, K, rel_4k))

# Other κ-formulas for K
print(f"\n=== Other κ-formula candidates for K_family ===")
kappa_candidates = [
    ("2κ = 1/3", 2*kappa),
    ("3κ = 1/2", 3*kappa),
    ("4κ = 2/3", 4*kappa),
    ("5κ = 5/6 = 1-κ", 5*kappa),
    ("6κ = 1", 6*kappa),
    ("κ = 1/6", kappa),
    ("1-κ = 5/6", 1-kappa),
    ("1/2", 0.5),
    ("1/3", 1/3),
    ("2/3", 2/3),
    ("3/4", 0.75),
    ("5/8", 5/8),
    ("π/4", pi_const/4),
    ("π/5", pi_const/5),
    ("(1-κ)/2 = 5/12", (1-kappa)/2),
    ("(1+κ)/2 = 7/12", (1+kappa)/2),
    ("κ+1/2", kappa+0.5),
]

print(f"\n{'Family':>45} {'K':>10} {'Best formula':>15} {'Pred':>10} {'rel %':>8}")
print("-"*95)
for name, K, _ in results:
    best = (float('inf'), None, 0)
    for cn, cv in kappa_candidates:
        if cv <= 0: continue
        rel = abs(K - cv)/K * 100
        if rel < best[0]:
            best = (rel, cn, cv)
    print(f"{name:>45} {K:>10.5f} {best[1]:>15} {best[2]:>10.5f} {best[0]:>7.2f}%")

# Specific Koide test : (e, μ, τ) precision
print(f"\n=== KOIDE LEPTONS — high precision ===")
K_lep = koide([m_e, m_mu, m_tau])
print(f"K_leptons = {K_lep:.10f}")
print(f"2/3       = {2/3:.10f}")
print(f"4κ        = {4*kappa:.10f}")
print(f"Diff to 2/3 : {K_lep - 2/3:.2e} ({abs(K_lep - 2/3)/(2/3)*100:.6f}%)")
print(f"Diff to 4κ : {K_lep - 4*kappa:.2e} ({abs(K_lep - 4*kappa)/(4*kappa)*100:.6f}%)")

print(f"\n=== Resonance hadronic ratios — quick test ===")
# Famille mésons vecteurs
m_rho = 775.26
m_omega = 782.65
m_phi_meson = 1019.461
m_J_psi = 3096.9
m_psi_2S = 3686.097
m_Upsilon_1S = 9460.4
m_Upsilon_2S = 10023.26

resonances = [
    ("m_φ/m_ω = π(1-κ)/2 = 5π/12", m_phi_meson/m_omega, 5*pi_const/12),
    ("m_ψ(2S)/m_J/ψ = 1/(1-κ) = 6/5", m_psi_2S/m_J_psi, 6/5),
    ("m_Υ(2S)/m_Υ(1S) ≈ ?", m_Upsilon_2S/m_Upsilon_1S, None),
    ("m_J/ψ/m_p = π²/3", m_J_psi/938.272, pi_const**2/3),
    ("m_φ/m_p = π/(1-κ)/(?)", m_phi_meson/938.272, None),
    ("m_Δ/m_p = π(1-κ)/2", 1232.0/938.272, 5*pi_const/12),
    ("m_Δ/m_π = ?", 1232.0/139.570, None),
]

for name, val, pred in resonances:
    if pred:
        rel = abs(val - pred)/val*100
        flag = "✅" if rel < 1 else "🟡" if rel < 3 else "❌"
        print(f"  {name:>40} = {val:>8.4f} vs {pred:>8.4f} : {rel:>5.2f}% {flag}")
    else:
        print(f"  {name:>40} = {val:>8.4f} (no pred)")

print("\nDONE.")
