"""
D6 — ΔN_eff from Kaluza-Klein graviton tower
=============================================
Claim (paper §5): A compact extra dimension of size ℓ with c' KK graviton
modes in equilibrium at the electroweak phase transition contributes:

  ΔN_eff^KK = c' × (43/4)^(4/3) × (g_*s(T_KK) / g_*s(T_0))^(-4/3)
             × (T_KK / T_ν,0)^4 × ρ_KK / ρ_γ

In the minimal estimate where KK modes thermalise at T ~ 1/ℓ and decouple
as non-relativistic species at  m_KK ≡ 1/ℓ >> T_BBN:

  ΔN_eff ≈  (c' / g_s,dec^(4/3)) × (g_s,dec / g_s,0)^(4/3) × (43/4)^(4/3) / (7/8 × (4/11)^(4/3))

But more carefully, for a gravi-ton tower with  g_KK = 2(2+1) = 6  dof
per mode, radiating like radiation at T_dec >> T_BBN:

  ΔN_eff = c' × (g_KK / g_ν) × (T_KK / T_ν)^4 × (7/8)^{-1}

where g_ν = 2×(7/8) = 7/4 per neutrino species.

We compute this numerically and compare to the ACT DR6 bound:
  N_eff^ACT = 2.86 ± 0.13   [ACT DR6 2025, arXiv:2503.14454]
  N_eff^SM = 3.044
  → ΔN_eff < 3.044 − 2.86 + 2×0.13 = 0.454  (2σ upper bound on NP)
  or more conservatively: ΔN_eff^NP < 0.184 at 1σ from ACT central value.

References:
  - ACT DR6: Madhavacheril et al. 2024 / Louis et al. 2025 [arXiv:2503.14454]
  - Arkani-Hamed, Dimopoulos, Dvali (ADD), Phys.Lett.B 1998
  - Hannestad, Raffelt, JCAP 2003
  - Kolb & Turner "Early Universe" §3 (entropy/dof counting)

Run:
  python3 D6-deltaNeff-kk.py
"""

from sympy import (
    symbols, Rational, sqrt, exp, pi, integrate, oo,
    simplify, latex, lambdify, S, Abs, factor
)
import sympy as sp
import math

# ── SM degrees of freedom at key epochs ──────────────────────────────────────
# g_*s counts entropy dof.  Standard values:
g_s_EW   = 106.75    # at T ~ 100 GeV (electroweak, full SM)
g_s_QCD  = 61.75     # at T ~ 150 MeV (just above QCD transition, approx)
g_s_BBN  = 10.75     # at T ~ 1 MeV   (e+e- still relativistic)
g_s_0    = 3.909     # today (photons + 3ν)  = 2 + 6×(7/8) = 2 + 21/4 = 43/4...
# Actually: g_s,0 = 2 + (21/4) × (4/11) = nope.
# Standard: g_s,0 = (43/11) after e+e- annihilation → use 43/11 numerically.
g_s_0_exact = 43.0 / 11.0   # 3.909

# ── Symbols ──────────────────────────────────────────────────────────────────
c_prime  = symbols(r"c'", positive=True, integer=True)  # number of KK modes
ell      = symbols(r'\ell', positive=True)              # extra-dim size [m]
T_dec    = symbols(r'T_\mathrm{dec}', positive=True)    # KK decoupling temperature

# ── ΔN_eff formula ───────────────────────────────────────────────────────────
#
# Boltzmann factor for entropy dilution: when a species with g_d dof decouples
# at T_dec and entropy is subsequently heated to T_0, its temperature today is:
#
#   (T_KK / T_ν)  =  (g_s,dec / g_s,today)^(1/3)  ×  (T_ν,today / T_ν,today)  ← trivially 1
#
# More precisely, using the standard formula:
#   ΔN_eff = g_KK × (2/7) × (g_s,dec / g_s,0)^(-4/3) × (43/4)^(4/3)
#             ↑ dof correction    ↑ entropy dilution
#
# Derivation:
#   ρ_KK / ρ_γ^today  =  (π²/30) × g_KK × T_KK^4  /  (π²/30) × 2 × T_γ^4
#   ΔN_eff  =  (8/7) × ρ_KK / ρ_γ   (definition via neutrino normalisation)
#            = (8/7) × (g_KK/2) × (T_KK/T_γ)^4
#            = (4g_KK/7) × (T_KK/T_γ)^4
#
# where T_KK/T_γ = (g_s,0 / g_s,dec)^(1/3) × (T_γ/T_ν)^(-1) × (T_γ/T_ν)
#     = (g_s,0 / g_s,dec)^(1/3)  [if KK decoupled before e+e- annihilation]
# So:
#   T_KK / T_γ = (g_s,0 / g_s,dec)^(1/3)

def delta_Neff_single_mode(g_kk, g_s_dec, g_s_today=g_s_0_exact):
    """ΔN_eff from one tower of KK gravitons with g_kk dof, decoupling at g_s_dec."""
    T_ratio = (g_s_today / g_s_dec) ** (1.0/3.0)
    delta = (4.0 * g_kk / 7.0) * T_ratio**4
    return delta

print("── ΔN_eff from KK graviton tower (D6) ──────────────────────────────")
print()

# Per KK mode: spin-2 graviton has 2(2J+1)=5 dof in 4D, but for massless limit
# and considering massive KK: 5 polarisations.
# However, for a bulk graviton in 5D: 5 dof per mode.
# Conservative: use g_KK = 2 (like a massless graviton, helicities ±2)
g_kk_values = {
    "massless limit (g=2)": 2,
    "massive KK spin-2 (g=5)": 5,
    "graviton + dilaton (g=7)": 7
}

epochs = {
    "EW (T~100 GeV, g_s=106.75)": g_s_EW,
    "QCD (T~150 MeV, g_s=61.75)":  g_s_QCD,
    "BBN (T~1 MeV,   g_s=10.75)":  g_s_BBN,
}

# ACT DR6 bounds
Neff_SM  = 3.044
Neff_ACT = 2.86
sigma_ACT = 0.13
dNeff_1sigma = Neff_SM - Neff_ACT                  # = 0.184
dNeff_2sigma = Neff_SM - (Neff_ACT - 2 * sigma_ACT)  # = 0.444  (SM vs ACT-2σ lower)

print(f"ACT DR6 central:   N_eff = {Neff_ACT} ± {sigma_ACT}")
print(f"SM prediction:     N_eff = {Neff_SM}")
print(f"  → ΔN_eff < {dNeff_1sigma:.3f}  (1σ, from SM)")
print(f"  → ΔN_eff < {dNeff_2sigma:.3f}  (2σ, ACT lower edge vs SM)")
print()

print(f"{'Epoch':>38}  {'g_s,dec':>8}", end="")
for label in g_kk_values:
    print(f"  {'ΔN_eff('+label+')':>28}", end="")
print()
print("-" * 130)

for epoch_label, g_s_dec in epochs.items():
    print(f"  {epoch_label:>36}  {g_s_dec:>8.2f}", end="")
    for label, g_kk in g_kk_values.items():
        dN = delta_Neff_single_mode(g_kk, g_s_dec)
        flag = " ✓" if dN < dNeff_1sigma else (" ⚠" if dN < dNeff_2sigma else " ✗")
        print(f"  {dN:>8.4f}{flag:>2}             ", end="")
    print()

print()
print("  ✓ = within 1σ ACT bound  |  ⚠ = within 2σ  |  ✗ = excluded")
print()

# ── Grid over c' (number of modes) ──────────────────────────────────────────
print("── ΔN_eff vs c' (g_KK=5, decoupling at EW scale) ───────────────────")
g_kk = 5
g_s_dec = g_s_EW
dN_single = delta_Neff_single_mode(g_kk, g_s_dec)
print(f"  ΔN_eff per mode = {dN_single:.5f}")
print()

c_max_1sigma = int(dNeff_1sigma / dN_single)
c_max_2sigma = int(dNeff_2sigma / dN_single)
print(f"  Max c' at 1σ: {c_max_1sigma}  (ΔN_eff = {c_max_1sigma * dN_single:.3f})")
print(f"  Max c' at 2σ: {c_max_2sigma}  (ΔN_eff = {c_max_2sigma * dN_single:.3f})")
print()

print(f"  {'c_prime':>8}  {'ΔN_eff':>10}  {'ACT 1σ bound':>14}  {'ACT 2σ bound':>14}")
for c in range(1, 12):
    dN = c * dN_single
    ok1 = "OK" if dN < dNeff_1sigma else "---"
    ok2 = "OK" if dN < dNeff_2sigma else "---"
    print(f"  {c:>8}  {dN:>10.4f}  {ok1:>14}  {ok2:>14}")

print()

# ── KK mass / extra dimension size constraint ────────────────────────────────
print("── Constraint on ℓ from ΔN_eff bound ───────────────────────────────")
print()
print("  For the KK tower to be thermalised at T_dec, we need m_KK ~ 1/ℓ ~ T_dec.")
print("  m_KK^(1) ≡ ħc / ℓ  →  ℓ = ħc / T_dec")
print()
# T_dec in EW: ~ 100 GeV → m_KK ~ 100 GeV → ℓ ~ 2e-18 m
hbar_c_GeV_m = 1.973e-16   # ħc in GeV·m
T_EW_GeV = 100.0           # GeV
ell_EW = hbar_c_GeV_m / T_EW_GeV
print(f"  T_dec ~ 100 GeV  →  ℓ ~ {ell_EW:.2e} m  ({ell_EW*1e15:.2f} fm)")
print()
T_QCD_GeV = 0.15  # 150 MeV
ell_QCD = hbar_c_GeV_m / T_QCD_GeV
print(f"  T_dec ~ 150 MeV  →  ℓ ~ {ell_QCD:.2e} m  ({ell_QCD*1e15:.1f} fm)")
print()

# ── Analytic ΔN_eff formula ───────────────────────────────────────────────────
print("── Analytic formula (D6) ────────────────────────────────────────────")
print()
print("  ΔN_eff = c' × (4/7) × g_KK × (g_{s,0} / g_{s,dec})^{4/3}")
print()
print("  with g_{s,0} = 43/11,  g_{s,dec} = g_*(T_KK)")
print()

# Symbolic version
g_s_today_sym = sp.Rational(43, 11)
g_s_dec_sym   = symbols(r'g_{*s}(T_\mathrm{dec})', positive=True)
g_KK_sym      = symbols(r'g_\mathrm{KK}', positive=True)
c_sym         = symbols(r"c'", positive=True)

dNeff_sym = c_sym * sp.Rational(4, 7) * g_KK_sym * (g_s_today_sym / g_s_dec_sym) ** sp.Rational(4, 3)
print(f"  Symbolic: ΔN_eff = {dNeff_sym}")
print()

# ── LaTeX output ─────────────────────────────────────────────────────────────
print("── LaTeX (paste into paper) ─────────────────────────────────────────")
print(r"  \Delta N_\mathrm{eff}^{\mathrm{KK}}")
print(r"  = c' \cdot \frac{4\,g_\mathrm{KK}}{7}")
print(r"    \left(\frac{43/11}{g_{*s}(T_\mathrm{dec})}\right)^{4/3}")
print()
print(r"  \text{ACT DR6 bound (2025): } \Delta N_\mathrm{eff} < 0.184\,(1\sigma),\ 0.444\,(2\sigma)")
print()
print("Status: FUNCTIONAL — ΔN_eff computed for full (c', g_KK, g_s,dec) grid.")
print("        ACT DR6 bounds applied, max c' per scenario tabulated.")
print("TODO  : Non-equilibrium production rate, Boltzmann integral over")
print("        KK spectrum, finite-ℓ corrections to g_* counting.")
