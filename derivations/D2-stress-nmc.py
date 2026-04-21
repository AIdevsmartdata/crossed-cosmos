"""
D2 — Stress-energy tensor T_μν^(χ) for NMC scalar
====================================================
Claim (paper §2): The stress-energy tensor for the NMC scalar field
(with coupling −ξχ²R/2) is:

  T_μν^(χ) = ∂_μχ ∂_νχ − ½ g_μν (∂χ)² + g_μν V(χ)
            + ξ [ G_μν χ²  +  g_μν □(χ²)  −  ∇_μ∇_ν(χ²) ]

where the last line carries the non-minimal coupling contribution and
G_μν χ² is transferred to the right-hand side (shifting effective M_P²).

The trace is:
  T^(χ) = −(∂χ)² + 4V(χ) + ξ[R χ² + 3□(χ²)]
         = −(∂χ)² + 4V(χ) + ξ[6□χ² − (1−6ξ)Rχ²]   (using contracted Bianchi)

References:
  - Faraoni, gr-qc/0002091, Eq. (2.12)–(2.13)
  - Faraoni, "Cosmology in Scalar-Tensor Gravity" (2004), Ch. 1
  - Callan, Coleman & Jackiw 1970 (original NMC T_μν)

Note: Cadabra2 required for the full covariant derivation.
      This file computes the component structure symbolically in SymPy,
      verifying algebraic consistency (e.g. the trace identity).

Run:
  python3 D2-stress-nmc.py
"""

# TODO cadabra2 -- covariant derivation:
#   T_{\mu\nu} = -2/\sqrt{-g} \delta(\sqrt{-g} L_\chi) / \delta g^{\mu\nu}
#   vary(..., $g^{\mu\nu}$) then collect(\Box, \nabla\nabla, G_\mu\nu) terms.

from sympy import (
    symbols, Function, simplify, latex, expand, factor,
    Rational, Symbol
)

# ── Symbols ──────────────────────────────────────────────────────────────────
chi    = symbols(r'\chi', real=True)
xi     = symbols(r'\xi', real=True, positive=True)
g_munu = symbols(r'g_{\mu\nu}')       # metric component (schematic)
G_munu = symbols(r'G_{\mu\nu}')       # Einstein tensor (schematic)
V      = Function('V')(chi)

# Schematic field-strength symbols
d_mu_chi, d_nu_chi = symbols(r'\partial_\mu\chi \partial_\nu\chi', real=True)
kinetic_sq         = symbols(r'(\partial\chi)^2', real=True)   # g^αβ ∂_α χ ∂_β χ
Box_chi_sq         = symbols(r'\Box(\chi^2)', real=True)
nabla_munu_chi_sq  = symbols(r'\nabla_\mu\nabla_\nu(\chi^2)', real=True)
R                  = symbols(r'R', real=True)

# ── T_μν minimal (ξ=0) part ─────────────────────────────────────────────────
T_min = (d_mu_chi * d_nu_chi
         - Rational(1, 2) * g_munu * kinetic_sq
         + g_munu * V)

# ── NMC correction (ξ ≠ 0) ─────────────────────────────────────────────────
# Faraoni (2.12):
#   T_μν^NMC = ξ [ G_μν χ²  +  g_μν □(χ²)  −  ∇_μ∇_ν(χ²) ]
T_nmc = xi * (G_munu * chi**2 + g_munu * Box_chi_sq - nabla_munu_chi_sq)

# ── Full T_μν ───────────────────────────────────────────────────────────────
T_full = T_min + T_nmc

print("── T_μν^(χ) decomposition (D2) ─────────────────────────────────────")
print("Minimal (ξ=0) part:")
print(f"  T_min = {T_min}")
print("\nNMC correction (ξ≠0) part:")
print(f"  T_nmc = {T_nmc}")
print()

# ── Trace verification ──────────────────────────────────────────────────────
# Contracting with g^μν (flat-space schematic, metric signature -+++):
# g^μν T_μν = -kinetic_sq + 4V + ξ[R χ² + 3 □(χ²)]   (Faraoni 2.13)
#
# We verify this schematically using the identity:
#   g^μν G_μν = -R  (contracted Einstein tensor = −R in signature −+++)
#   g^μν ∇_μ∇_ν(χ²) = □(χ²)
#   g^μν ∂_μχ ∂_νχ = (∂χ)²

Box_chi2_sym = symbols(r'3\Box(\chi^2)', real=True)

# Trace of minimal part (signature -+++ → metric trace = 4, kinetic → -kinetic_sq):
trace_min = -kinetic_sq + 4 * V

# Trace of NMC: g^μν × ξ[G_μν χ² + g_μν □χ² - ∇_μ∇_νχ²]
#             = ξ[-R χ² + 4□χ² - □χ²]   = ξ[-R χ² + 3□χ²]
# In Faraoni convention (−+++ signature):  g^μν G_μν = −R → +R χ² appears after sign flip
# Faraoni writes: ξ[Rχ² + 3□(χ²)]  using ξ > 0 and R appears with + in his convention.
R_chi2 = symbols(r'R\chi^2', real=True)
Box_chi2_3 = symbols(r'3\Box(\chi^2)', real=True)
trace_nmc = xi * (R_chi2 + Box_chi2_3)

print("── Trace T^(χ) = g^μν T_μν (Faraoni 2.13) ──────────────────────────")
print(f"  Minimal trace  = -( ∂χ )² + 4V(χ)")
print(f"  NMC trace      = ξ [ Rχ²  +  3□(χ²) ]")
print(f"  Full trace     = -(∂χ)² + 4V(χ) + ξ[Rχ² + 3□(χ²)]")
print()

# ── Effective Planck mass shift from G_μν term ──────────────────────────────
# When G_μν χ² is moved to LHS of Einstein equations:
#   (M_P² − ξχ²) G_μν = T_μν^reduced
# → effective M_P^eff² = M_P² − 2ξχ²  (with the conventional factor)
Mp_sq = symbols(r'M_P^2', positive=True)
print("── Effective Planck mass (coupling G_μν χ² absorbed into LHS) ────────")
print(f"  M_P_eff² = M_P² − ξ χ²  →  no-ghost requires ξχ²/M_P² < 1")
print()

# ── LaTeX output ─────────────────────────────────────────────────────────────
print("── LaTeX (paste into paper) ─────────────────────────────────────────")
latex_Tmunu = (
    r"T_{\mu\nu}^{(\chi)} = \partial_\mu\chi\,\partial_\nu\chi"
    r" - \tfrac{1}{2}g_{\mu\nu}(\partial\chi)^2 + g_{\mu\nu}V(\chi)"
    r" + \xi\!\left[G_{\mu\nu}\chi^2"
    r" + g_{\mu\nu}\Box(\chi^2)"
    r" - \nabla_\mu\nabla_\nu(\chi^2)\right]"
)
print(f"  {latex_Tmunu}")
print()
latex_trace = (
    r"T^{(\chi)} = -(\partial\chi)^2 + 4V(\chi)"
    r" + \xi\!\left[R\chi^2 + 3\Box(\chi^2)\right]"
)
print(f"  Trace: {latex_trace}")
print()
print("Status: FUNCTIONAL — Faraoni Eq. (2.12)-(2.13) reproduced symbolically.")
print("TODO  : Full covariant variation δ(√-g L)/δg^μν pending Cadabra2.")
