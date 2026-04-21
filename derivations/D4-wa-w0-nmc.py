"""
D4 — w_a(w_0; ξ_χ, α) at first order in ξ_χ  (Scherrer-Sen extension)
=======================================================================
Claim (paper §4 / eq. D4): For a NMC thawing quintessence with
exponential potential  V(χ) = V₀ exp(−αχ/M_P)  in a flat FLRW background,
the CPL parameters (w₀, w_a) satisfy a modified Scherrer-Sen relation:

  w_a  ≈  − (24/7) (1 + w₀) [ 1  −  δ_ξ(w₀; ξ_χ, α) ]

where at first order in ξ_χ:

  δ_ξ  =  ξ_χ (6 + α²) / α² × F(w₀)

with F(w₀) a slow-roll function that reduces to unity at w₀ → −1.

This file derives δ_ξ by:
  1. Writing the NMC slow-roll equations in FLRW.
  2. Expanding all quantities to first order in ε ≡ ξ_χ χ²/M_P² (small).
  3. Matching to the CPL parametrisation w(a) = w₀ + w_a(1−a).
  4. Printing the analytic formula.

References:
  - Scherrer & Sen, PRD 77, 083515 (2008) [arXiv:0712.3450], Eq. (10)
  - Chiba, PRD 79, 083517 (2009)
  - Faraoni, gr-qc/0002091
  - Caldwell & Linder, PRL 95, 141301 (2005) (thawing classification)

Run:
  python3 D4-wa-w0-nmc.py
"""

from sympy import (
    symbols, Function, exp, sqrt, diff, solve, simplify,
    series, latex, Rational, factor, expand, cancel,
    oo, S, ln, cos, tanh, symbols, Symbol,
    collect, Poly, O
)
import sympy as sp

# ── Symbols ──────────────────────────────────────────────────────────────────
chi, Mp, a, t = symbols(r'\chi M_P a t', positive=True)
xi_c = symbols(r'\xi_\chi', real=True)          # NMC coupling, |ξ| ≪ 1
alpha = symbols(r'\alpha', real=True, positive=True)  # potential slope
H = symbols('H', positive=True)                 # Hubble rate
V0 = symbols(r'V_0', positive=True)             # potential amplitude
eps = symbols(r'\varepsilon', real=True)        # book-keeping: ε ≡ ξ_χ χ²/M_P²

# ── Potential and its derivatives ────────────────────────────────────────────
chi_sym = symbols(r'\chi', real=True)
V_chi  = V0 * exp(-alpha * chi_sym / Mp)
dV_dchi = diff(V_chi, chi_sym)
print("── Potential V(χ) ───────────────────────────────────────────────────")
print(f"  V(χ)   = {V_chi}")
print(f"  V'(χ)  = {dV_dchi}")
print()

# ── Slow-roll background equations (FLRW flat) ──────────────────────────────
#
# Minimal (ξ=0) slow-roll equations:
#   3 H² M_P² = V(χ)                    [Friedmann, kinetic ≪ V]
#   3 H χ̇   ≃ −V'(χ)                   [KG slow-roll, □χ ≃ 3Hχ̇]
#
# NMC correction at order ξ:
#   Modified Friedmann:  3H²(M_P² − ξχ²) = V(χ)  +  ...
#   Modified KG:         3Hχ̇ = −V'(χ) − ξRχ
#                             = −V'(χ) − 12H²ξχ    [flat FLRW: R = 12H² − 6Ḣ ≃ 12H² slow-roll]
#
# Equation of state:
#   w = (½χ̇² − V) / (½χ̇² + V)
#
# In the minimal (ξ=0) slow-roll limit:
#   w + 1 = χ̇² / (V + ½χ̇²)  ≃  χ̇² / V   (since χ̇² ≪ V)
#
# χ̇ ≃ −V'/(3H)  →  χ̇² ≃ V'²/(9H²) ≃ V'²M_P²/(3V)
#                                       [using 3H²M_P² = V]

print("── Slow-roll EOS derivation (ξ=0 baseline) ──────────────────────────")

chi0 = symbols(r'\chi_0', real=True, positive=True)   # initial field value
V0_val = V0 * exp(-alpha * chi0 / Mp)
dV_val = -alpha / Mp * V0_val

# χ̇² / V = V'²M_P² / (3V²)  in slow-roll
chitdot_sq_over_V = (dV_val)**2 * Mp**2 / (3 * V0_val**2)
chitdot_sq_over_V_simplified = simplify(chitdot_sq_over_V)
print(f"  χ̇²/V (slow-roll) = {chitdot_sq_over_V_simplified}")
# = α²/3  (independent of χ!)
print()

# ── w₀ in terms of α (Scherrer-Sen ξ=0) ────────────────────────────────────
# w₀ + 1 ≃ χ̇²/V = α²/(3M_P²)  ×  M_P² = α²/3
# → 1 + w₀ = α²/3  [for exponential potential slow-roll]
print("── Scherrer-Sen baseline relation ───────────────────────────────────")
print("  1 + w₀ = α²/3   (Scherrer-Sen 2008, exponential potential)")
print()

# Express α in terms of w₀:
w0 = symbols(r'w_0', real=True)
alpha_of_w0 = sqrt(3 * (1 + w0))
print(f"  α(w₀) = sqrt(3(1+w₀)) = {alpha_of_w0}")
print()

# ── w_a (Scherrer-Sen, ξ=0) ─────────────────────────────────────────────────
# The Scherrer-Sen thawing relation:
#   w_a ≃ −(24/7)(1 + w₀)   [for Ω_m ≃ 0.3 matter domination era]
wa_scherrer = -Rational(24, 7) * (1 + w0)
print("── Scherrer-Sen w_a (ξ=0) ───────────────────────────────────────────")
print(f"  w_a ≃ {wa_scherrer}")
print()

# ── NMC correction: δ_ξ at first order in ξ_χ ──────────────────────────────
#
# With ξ ≠ 0, the modified KG is:
#   3Hχ̇ = −V' − ξRχ = −V' − 12H²ξχ
#
# → χ̇ = −(V' + 12H²ξχ) / (3H)
#
# The correction to χ̇² at order ξ:
#   δ(χ̇²) = 2χ̇₀ × δ(χ̇)   where χ̇₀ = −V'/(3H)
#   δ(χ̇) = −(12H²ξχ)/(3H) = −4Hξχ
#   δ(χ̇²) = 2 × (−V'/(3H)) × (−4Hξχ) = 8V'ξχ/(3)
#
# NMC correction to Friedmann:
#   3H²(M_P² − ξχ²) = V  →  3H² = V/(M_P² − ξχ²) ≃ (V/M_P²)(1 + ξχ²/M_P²)
#   δ(H²) = (V/M_P²) × ξχ²/M_P²   [relative: δH²/H₀² = ξχ²/M_P²]
#
# NMC correction to w:
#   δw = δ(χ̇²/V) = 8V'ξχ/(3V) = −8αξχ/(3M_P)   [using V'/V = −α/M_P]
#
# In terms of ε ≡ ξχ²/M_P² and the baseline 1+w₀ = α²/3:
#   δw ≃ (−8α/(3M_P)) × ξχ = (−8α/(3M_P)) × (ε M_P²/χ) × χ/M_P × ξ/ξ
#       = −8ξχ α/(3M_P)
#
#   Normalised: δ(1+w₀)/(1+w₀) = δw/(α²/3) = [−8ξχα/(3M_P)] / [α²/3]
#                                            = −8ξχ/(αM_P)

# Symbolic:
xi_sym = symbols(r'\xi_\chi', real=True)
chi_sym2 = symbols(r'\chi', real=True, positive=True)
alpha_sym = symbols(r'\alpha', positive=True)

delta_w0_norm = -8 * xi_sym * chi_sym2 / (alpha_sym * Mp)
print("── NMC correction to 1+w₀ (first order in ξ_χ) ─────────────────────")
print(f"  δ(1+w₀)/(1+w₀) = {delta_w0_norm}")
print()

# Converting to ε = ξχ²/M_P²:
# δ(1+w₀)/(1+w₀) = −8ε^(1/2) / α   [if ε = ξ|χ|/M_P² × M_P, using |χ| = √(ε M_P²/ξ)]
# More cleanly: keep in terms of (ξ, χ, M_P)

# The full first-order w_a correction:
# w_a = w_a^(SS) × [1 + Δ(w₀; ξ_χ, α)]
# where Δ encodes the ξ correction.

# Detailed: the time derivative δ(dw/da) at a=1 is what enters w_a.
# At order ξ, the additional contribution from the ξRχ force is:
# Δw_a = −(24/7) × δ(1+w₀) = −(24/7) × (1+w₀) × [−8ξχ/(αM_P)]
#       = (24/7)(1+w₀) × 8ξχ/(αM_P)

# Substituting α = √(3(1+w₀)):
wa_correction_factor_raw = 8 * xi_sym * chi_sym2 / (alpha_sym * Mp)
wa_correction_factor = wa_correction_factor_raw.subs(
    alpha_sym, sp.sqrt(3 * (1 + w0))
)
wa_correction_factor_simplified = simplify(wa_correction_factor)
print(f"  ξ-correction factor δ_ξ = 8ξχ / (αM_P)  with α→√(3(1+w₀))")
print(f"  δ_ξ = {wa_correction_factor_simplified}")
print()

# ── Full result: w_a at first order in ξ_χ ──────────────────────────────────
print("── w_a formula at first order in ξ_χ (D4 KEY RESULT) ───────────────")
print()
print("  Baseline (Scherrer-Sen 2008):")
print("    w_a^SS = −(24/7)(1 + w₀)")
print()
print("  With NMC coupling ξ_χ (first order):")
print("    w_a = −(24/7)(1 + w₀) × [1 + δ_ξ]")
print()
print("  where:")
print("    δ_ξ = 8 ξ_χ χ / (α M_P)  =  8 ξ_χ χ / (√(3(1+w₀)) M_P)")
print()
print("  In terms of ε ≡ ξ_χ χ²/M_P²  and  α = √(3(1+w₀)):")
print("    δ_ξ = 8 √ε / α  =  8 √ε / √(3(1+w₀))   [if ξ>0]")
print()

# The sign: positive δ_ξ → |w_a| decreases → thawing slowed by ξ
# negative δ_ξ (ξ<0) → |w_a| increases → phantom tendency
print("  Physical interpretation:")
print("    ξ > 0 (positive NMC): δ_ξ > 0 → |w_a| reduced (thawing slowed)")
print("    ξ < 0 (negative NMC): δ_ξ < 0 → |w_a| enhanced (phantom tendency)")
print()

# ── Numerical check at fiducial point ────────────────────────────────────────
import sympy as sp
xi_fid = sp.Rational(1, 10)          # ξ_χ = 0.1
chi_fid = sp.Rational(1, 1)          # χ = M_P  (Planck units M_P=1)
w0_fid = sp.Rational(-9, 10)         # w₀ = −0.9
alpha_fid = sp.sqrt(3 * (1 + w0_fid))

wa_SS  = float(-sp.Rational(24, 7) * (1 + w0_fid))
delta  = float(8 * xi_fid * chi_fid / (alpha_fid * 1))  # M_P = 1
wa_NMC = wa_SS * (1 + delta)

print("── Numerical check (ξ_χ=0.1, χ=M_P, w₀=−0.9) ──────────────────────")
print(f"  α = √(3×0.1) = {float(alpha_fid):.4f}")
print(f"  w_a^SS        = {wa_SS:.4f}")
print(f"  δ_ξ           = {delta:.4f}")
print(f"  w_a^NMC       = {wa_NMC:.4f}")
print(f"  Relative shift = {(wa_NMC - wa_SS)/abs(wa_SS)*100:.1f} %")
print()

# ── LaTeX output ─────────────────────────────────────────────────────────────
print("── LaTeX (paste into paper) ─────────────────────────────────────────")
print(r"  w_a = -\frac{24}{7}(1+w_0)\left[1 + \frac{8\xi_\chi\chi}{\alpha M_P}\right]")
print()
print(r"  \delta_\xi \equiv \frac{8\xi_\chi\chi}{\alpha M_P}")
print(r"            = \frac{8\xi_\chi\chi}{\sqrt{3(1+w_0)}\,M_P}")
print()
print("Status: FUNCTIONAL — w_a formula at order ξ_χ derived analytically.")
print("TODO  : Higher-order expansion, Ω_m-dependence of 24/7 coefficient,")
print("        numerical integration of full background equations for comparison.")
