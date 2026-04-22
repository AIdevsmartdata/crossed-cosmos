"""
D12 — Exponential-potential attractor condition  α ≤ √2  (minimal coupling)
===========================================================================

Referee-facing symbolic derivation for paper §4 (v4.4): the late-time
scalar-field-dominated attractor of an exponential quintessence
potential

    V(χ)  =  V₀  exp( − α χ / M_P )

on a spatially-flat FRW background with Friedmann + Klein-Gordon, in
the minimally-coupled limit. Following Copeland, Liddle & Wands
(PRD 57, 4686, 1998) Table I, we derive the autonomous system for

    x ≡ χ̇ / (√6 M_P H),      y ≡ √V / (√3 M_P H)

its scalar-field-dominated fixed point, the corresponding equation of
state w_φ = p_φ/ρ_φ, and the acceleration threshold α² < 2 (i.e.
α < √2).

Subtle distinction documented here (and in the paper):
  – α → 0 gives a TRUE de Sitter attractor (w_φ = −1).
  – α < √2 gives an ACCELERATING scalar-field-dominated attractor
    (w_φ < −1/3), but w_φ = −1 + α²/3  is *not* exactly −1 unless α=0.
  – α = √2 is the marginal case w_φ = −1/3 (onset of acceleration).
  – α = √3 (i.e. α² = 3) is the onset of the matter-scaling solution.

The NMC generalisation of this attractor analysis is deferred to
future work (see paper §4 footnote); turning on ξ_χ couples R into
the KG equation and modifies x,y via the  −ξ_χ R χ  force term.

References
----------
  Copeland, Liddle, Wands, PRD 57, 4686 (1998)          [CLW, Table I]
  Halliwell, Phys. Lett. B 185, 341 (1987)              [original α<√2]
  Ferreira & Joyce, PRL 79, 4740 (1997); PRD 58, 023503
  Copeland, Sami, Tsujikawa, IJMPD 15, 1753 (2006), §4   [review]

Run
---
  python3 D12-alpha-attractor.py
"""
from __future__ import annotations

import os
import resource
os.environ.setdefault("OMP_NUM_THREADS", "2")
try:
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
except (ValueError, OSError):
    pass

import math
import sympy as sp
from sympy import symbols, sqrt, Rational, simplify, solve, Eq


def main() -> None:
    print("=" * 72)
    print("D12 — Exponential-potential attractor: α ≤ √2 (minimal coupling)")
    print("=" * 72)
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 1 — Friedmann + Klein-Gordon with V = V₀ exp(−α χ / M_P)
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 1 — Setup: Friedmann + KG on FRW with exponential V")
    print("-" * 72)

    t, H, chi, chi_dot, chi_ddot = symbols(
        r't H \chi \dot\chi \ddot\chi', real=True)
    alpha, MP, V0 = symbols(r'\alpha M_P V_0', positive=True)

    V   = V0 * sp.exp(-alpha * chi / MP)
    Vp  = sp.diff(V, chi)                        # = −α/M_P · V

    # scalar energy density & pressure (canonical minimal coupling)
    rho_phi = Rational(1, 2) * chi_dot**2 + V
    p_phi   = Rational(1, 2) * chi_dot**2 - V

    # Friedmann (scalar-only universe at the late-time attractor):
    # 3 M_P² H² = ρ_φ
    friedmann = sp.Eq(3 * MP**2 * H**2, rho_phi)
    # Klein-Gordon:  χ̈ + 3 H χ̇ + V'(χ) = 0
    kg        = sp.Eq(chi_ddot + 3 * H * chi_dot + Vp, 0)

    print("  V(χ)    = V₀ exp(−α χ / M_P)")
    print("  V'(χ)  = −(α/M_P) V")
    print("  ρ_φ    = ½ χ̇² + V")
    print("  p_φ    = ½ χ̇² − V")
    print("  Friedmann:  3 M_P² H² = ρ_φ")
    print("  KG:         χ̈ + 3 H χ̇ + V'(χ) = 0")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 2 — Autonomous (x, y) system (Copeland–Liddle–Wands 1998)
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 2 — Autonomous system (x, y) — Copeland–Liddle–Wands 1998")
    print("-" * 72)

    x, y = symbols('x y', real=True)
    # Definitions:  x = χ̇ / (√6 M_P H),  y = √V / (√3 M_P H)
    #
    # Then, using N = ln a as the time variable, CLW Table I:
    #    dx/dN = −3 x + (√6/2) α y² + (3/2) x [2 x²]               (scalar-dom.)
    #    dy/dN = −(√6/2) α x y        + (3/2) y [2 x²]
    #
    # In the scalar-field-dominated regime (x² + y² = 1 from Friedmann):
    #    dx/dN = −3 x + √6/2 · α y² + 3 x³
    #    dy/dN = −√6/2 · α x y       + 3 x² y
    dx_dN = -3 * x + sp.Rational(1, 1) * sp.sqrt(6) / 2 * alpha * y**2 + 3 * x**3
    dy_dN = -sp.sqrt(6) / 2 * alpha * x * y + 3 * x**2 * y

    print("  x ≡ χ̇ / (√6 M_P H)")
    print("  y ≡ √V / (√3 M_P H)")
    print("  Friedmann constraint (scalar-dominated):  x² + y² = 1")
    print()
    print("  dx/dN = ", sp.simplify(dx_dN))
    print("  dy/dN = ", sp.simplify(dy_dN))
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 3 — Scalar-field-dominated fixed point  x* = α/√6,  y* = √(1−α²/6)
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 3 — Scalar-field-dominated fixed point")
    print("-" * 72)

    # Require dx/dN = dy/dN = 0 with y > 0 (physical branch).
    # From dy/dN = y (−√6/2 · α x + 3 x²) = 0, with y > 0:
    #     3 x² = √6/2 · α x  ⇒  x = α / √6   (non-trivial root).
    # Plug into Friedmann x²+y²=1:  y² = 1 − α²/6.
    x_star = alpha / sp.sqrt(6)
    y_star = sp.sqrt(1 - alpha**2 / 6)
    print(f"  x*  =  α/√6          = {x_star}")
    print(f"  y*  =  √(1 − α²/6)   = {y_star}")
    print()

    # Verify it is indeed a fixed point of the autonomous system
    res_x = sp.simplify(dx_dN.subs({x: x_star, y: y_star}))
    res_y = sp.simplify(dy_dN.subs({x: x_star, y: y_star}))
    print(f"  dx/dN at (x*,y*) = {res_x}")
    print(f"  dy/dN at (x*,y*) = {res_y}")
    assert res_x == 0, f"dx/dN at fixed point must vanish, got {res_x}"
    assert res_y == 0, f"dy/dN at fixed point must vanish, got {res_y}"
    print("  ⇒ (α/√6, √(1−α²/6)) is a fixed point   ✓")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 4 — Equation of state at the fixed point:  w_φ = −1 + α²/3
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 4 — Equation of state at the scalar-dominated fixed point")
    print("-" * 72)

    # In CLW variables,  w_φ = (x² − y²)/(x² + y²) = x² − y²  (with x²+y²=1).
    w_phi_expr = x_star**2 - y_star**2
    w_phi = sp.simplify(w_phi_expr)
    print(f"  w_φ = x*² − y*² = {w_phi}")
    # Expected: −1 + α²/3
    expected = -1 + alpha**2 / 3
    diff = sp.simplify(w_phi - expected)
    assert diff == 0, f"w_φ mismatch: got {w_phi}, expected {expected}, "\
                      f"difference {diff}"
    print(f"  ⇒  w_φ = −1 + α²/3                 ✓")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 5 — Acceleration threshold  w_φ < −1/3  ⇔  α² < 2
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 5 — Acceleration threshold  w_φ < −1/3")
    print("-" * 72)
    print("  Universe accelerates iff total effective w < −1/3.")
    print("  At the scalar-dominated attractor, w_total = w_φ, so:")
    print("     w_φ  <  −1/3")
    print("     −1 + α²/3  <  −1/3")
    print("     α²  <  2")
    print("     |α|  <  √2  ≈ 1.41421356…")
    print()
    alpha_accel = sp.solve(sp.Eq(expected, -Rational(1, 3)), alpha)
    print(f"  Boundary (w_φ = −1/3)  ⇒  α  =  {alpha_accel}")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 6 — Subtle distinction: accelerating ≠ de Sitter
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 6 — Subtle distinction (documented in paper §4)")
    print("-" * 72)
    print("  – TRUE de Sitter (w_φ = −1)      ⇔  α = 0                (frozen V)")
    print("  – Accelerating attractor        ⇔  0 < α < √2")
    print("       w_φ = −1 + α²/3 ∈ (−1, −1/3)  — quintessence plateau")
    print("  – Marginal case (w_φ = −1/3)     ⇔  α = √2")
    print("  – Scaling-solution onset         ⇔  α = √3   (w_φ = 0, matter-like)")
    print()
    print("  ⇒ The threshold ‘α ≤ √2’ quoted in the paper is the")
    print("    ACCELERATING scalar-dominated attractor, not strictly de Sitter.")
    print("    The NMC generalisation (ξ_χ ≠ 0) is deferred to future work,")
    print("    see paper §4 footnote — turning on ξ_χ couples R into the KG")
    print("    equation and modifies the (x, y) fixed-point location.")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 7 — Numerical asserts at α ∈ {0, √2, √3}
    # ═══════════════════════════════════════════════════════════════════════
    print("PART 7 — Numerical cross-checks")
    print("-" * 72)

    cases = {
        "α = 0":   sp.Integer(0),
        "α = √2":  sp.sqrt(2),
        "α = √3":  sp.sqrt(3),
    }
    w_at = {}
    for label, a_val in cases.items():
        w_val = sp.simplify(expected.subs(alpha, a_val))
        w_at[label] = w_val
        print(f"  {label:8s}  →  w_φ = {w_val}  =  {float(w_val):+.6f}")
    print()

    # Asserts per plan
    assert sp.simplify(w_at["α = 0"] - (-1)) == 0, \
        f"α=0 must give w=−1, got {w_at['α = 0']}"
    assert sp.simplify(w_at["α = √2"] - (-Rational(1, 3))) == 0, \
        f"α=√2 must give w=−1/3, got {w_at['α = √2']}"
    assert sp.simplify(w_at["α = √3"] - 0) == 0, \
        f"α=√3 must give w=0, got {w_at['α = √3']}"
    print("  ✓ α=0   → w_φ = −1       (de Sitter)")
    print("  ✓ α=√2  → w_φ = −1/3     (marginal acceleration)")
    print("  ✓ α=√3  → w_φ =  0       (scaling-solution onset)")
    print()

    # Numerical value of √2 for reference
    print(f"  √2  =  {math.sqrt(2):.12f}")
    print(f"  √3  =  {math.sqrt(3):.12f}")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 72)
    print("Summary (LaTeX snippet for paper §4)")
    print("=" * 72)
    print(r"  V(\chi) = V_0\,e^{-\alpha\chi/M_P}, \qquad "
          r"w_\phi\big|_{\rm attr.} = -1 + \frac{\alpha^{2}}{3}.")
    print(r"  \text{Accelerating scalar-dominated attractor:}\ \alpha^{2}<2"
          r"\ (\alpha<\sqrt{2}).")
    print(r"  \text{True de Sitter:}\ \alpha=0.")
    print()
    print("Status: FUNCTIONAL — fixed point verified, w_φ cross-checked at "
          "α ∈ {0, √2, √3}, all asserts PASS. NMC extension deferred.")


if __name__ == "__main__":
    main()
