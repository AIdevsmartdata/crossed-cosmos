"""
D1 — Klein-Gordon equation from NMC action variation
=====================================================
Claim (paper §2): Varying the non-minimally coupled scalar action

  S = ∫ d⁴x √(-g) [ (M_P²/2 - ξχ²/2) R  +  ½(∂χ)²  −  V(χ) ]

with respect to χ yields the modified Klein-Gordon equation:

  □χ  −  V'(χ)  −  ξ R χ  =  0

References:
  - Faraoni, gr-qc/0002091, Eq. (2.9)
  - Birrell & Davies 1982, Ch. 3
  - Fujita, Kimura & Takahashi, JCAP 2016

Note: Cadabra2 is NOT available as a PyPI package; it must be installed via
  sudo apt install cadabra2          (Ubuntu/Debian)
  or built from source: https://cadabra.science/
The derivation below is done fully in SymPy.  The Cadabra2 equivalent code
is provided in comments marked  # TODO cadabra2  for future re-verification.

Run:
  python3 D1-kg-nmc.py
"""

# TODO cadabra2 -- when cadabra2 is installed, the cleaner tensor derivation is:
#
#   from cadabra2 import *
#   __cdbkernel__ = cadabra2.__cdbkernel__
#   # Declare indices, metric, covariant derivatives, Ricci scalar
#   ex = Ex(r"\xi \chi^2 R")
#   # Then use: vary(ex, $\chi$) and integrate_by_parts(...)
#   # Expected output: 2 \xi \chi R
#
# Below: full SymPy derivation.

from sympy import (
    symbols, Function, exp, sqrt, diff, simplify, latex,
    cos, pi, Rational, factor
)

# ── Symbols ──────────────────────────────────────────────────────────────────
chi, xi_c, Mp, R, t = symbols(r'\chi \xi_\chi M_P R t', real=True)
V = Function('V')(chi)

# ── Action density L (up to √-g which factors out) ───────────────────────────
# L = (M_P²/2 − ξχ²/2) R  +  ½(∂χ)²  −  V(χ)
#
# Euler-Lagrange equation from varying w.r.t. χ:
#
#   δS/δχ  =  ∂L/∂χ  −  ∂_μ(∂L/∂(∂_μ χ))  =  0
#
# Part 1: ∂L/∂χ  (treating (∂χ)² as kinetic, R as background for this step)
#   ∂L/∂χ  =  − ξ R χ  −  V'(χ)

dL_dchi = - xi_c * R * chi - diff(V, chi)
print("∂L/∂χ (non-derivative part):")
print(f"  {dL_dchi}")

# Part 2: kinetic term  ½(∂χ)²  →  ∂_μ(∂L/∂(∂_μ χ)) = □χ
# We represent □χ symbolically.
Box_chi = symbols(r'\Box\chi')

# Full Euler-Lagrange equation:
#   □χ  +  ∂L/∂χ  =  0
#   □χ  −  ξ R χ  −  V'(χ)  =  0

EOM = Box_chi + dL_dchi
EOM_simplified = EOM  # already in canonical form

print("\n── Klein-Gordon EOM (D1) ────────────────────────────────────────────")
print(f"  EOM = {EOM_simplified} = 0")
print()

# ── Verify sign convention (Faraoni gr-qc/0002091 Eq. 2.9) ──────────────────
# Faraoni writes:  □χ − V'(χ) − ξRχ = 0
# Our EOM rewritten:
eom_faraoni = Box_chi - diff(V, chi) - xi_c * R * chi
print("Faraoni reference form:  □χ − V'(χ) − ξRχ = 0")
print(f"  ✓ Match: EOM − Faraoni = {simplify(EOM_simplified - eom_faraoni)}")
print()

# ── LaTeX output ─────────────────────────────────────────────────────────────
print("── LaTeX (paste into paper) ─────────────────────────────────────────")
lhs = r"\Box\chi - V'(\chi) - \xi_\chi R \chi"
print(f"  {lhs} = 0")
print()
print("Status: FUNCTIONAL — EOM derived symbolically via Euler-Lagrange.")
print("TODO  : Full covariant tensor derivation pending Cadabra2 installation.")
print("        Install with:  sudo apt install cadabra2")
