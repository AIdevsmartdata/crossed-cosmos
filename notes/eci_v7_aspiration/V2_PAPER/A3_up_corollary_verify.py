#!/usr/bin/env python3
"""
A3 verification — Opus claim that in LYD20 Model VI at tau = i,
the c^c row (weight 2) and t^c row (weight 5, 3̂ multiplet) of M_u
are EXACTLY orthogonal in C^3.

Method:
  At tau = i, Lemma 1 of v2_no_go_paper.tex gives Y_j^(k)(i) = e^{i k pi/4} a_j^(k)
  with a_j^(k) ∈ R.  Since each polynomial Y^(k)_n is a homogeneous degree-k
  polynomial in (Y1, Y2, Y3), every component of every multiplet at tau=i
  carries the same phase e^{i k pi/4} times a real number computable from
  the real seeds a1, a2, a3 (with a1^2 + 2 a2 a3 = 0).

  Cosine of angle in C^3:
       cos(theta) = <v, w> / (||v|| ||w||)
  with <v,w> = sum_i conj(v_i) w_i.

  For row_c = e^{i pi/2} (b3, b5, b4)  (b's real)
      row_t = e^{i 5pi/4} (c3, c5, c4) (c's real)
  one has  <row_c, row_t> = e^{i 3pi/4} * (b3 c3 + b5 c5 + b4 c4).
  So |cos theta| = |b . c| / (||b|| ||c||) where the dot is the
  REAL Euclidean inner product.

  The Opus orthogonality claim is therefore:
       b . c == 0    in R[a1, a2, a3] / <a1^2 + 2 a2 a3>.

  This script computes b . c symbolically and reduces it modulo the ideal.
"""

import sympy as sp


def main() -> None:
    a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)

    # Real seeds at tau=i (after stripping the common phase e^{i pi/4})
    Y1, Y2, Y3 = a1, a2, a3

    # ---- Weight-2 triplet (3 of S'_4) — c^c row of M_u in column order
    #      (Y2_3, Y2_5, Y2_4)  per LYD20 Mq_6, lines 1379-1384
    b3 = 2*Y1**2 - 2*Y2*Y3
    b5 = 2*Y2**2 - 2*Y1*Y3
    b4 = 2*Y3**2 - 2*Y1*Y2

    # ---- Weight-5 triplet (3̂ of S'_4) — t^c row of M_u in column order
    #      (Y5_3, Y5_5, Y5_4)  per LYD20 Mq_6, lines 1379-1384
    c3 = 18 * Y1**2 * (-Y2**3 + Y3**3)
    c5 = (-4*Y1**4*Y3 - 4*Y1*(Y3**4 - 5*Y2**3*Y3)
          - 14*Y1**3*Y2**2 + 4*Y2**2*(Y2**3 + Y3**3)
          - 6*Y1**2*Y2*Y3**2)
    c4 = (4*Y1**4*Y2 + 4*Y1*(Y2**4 - 5*Y2*Y3**3)
          + 14*Y1**3*Y3**2 - 4*Y3**2*(Y2**3 + Y3**3)
          + 6*Y1**2*Y2**2*Y3)

    # ---- Real dot product b . c (this controls |cos theta|)
    dot = sp.expand(b3*c3 + b5*c5 + b4*c4)
    print("b . c =", dot)

    # ---- Reduce modulo the S'_4 algebra constraint a1^2 + 2 a2 a3 = 0
    # i.e. groebner reduce dot in R[a1,a2,a3] / <a1^2 + 2 a2 a3>
    constraint = a1**2 + 2*a2*a3
    # Use a Groebner basis with lex ordering, eliminating a1
    G = sp.groebner([constraint], a1, a2, a3, order='lex')
    dot_reduced = sp.reduced(dot, G, order='lex')[1]
    dot_reduced = sp.expand(dot_reduced)
    print("\nb . c reduced mod (a1^2 + 2 a2 a3):")
    print("  =", dot_reduced)
    print("  factored:", sp.factor(dot_reduced))

    # ---- Norms (also reduced)
    norm_b_sq = sp.expand(b3**2 + b5**2 + b4**2)
    norm_c_sq = sp.expand(c3**2 + c5**2 + c4**2)
    nb_red = sp.expand(sp.reduced(norm_b_sq, G, order='lex')[1])
    nc_red = sp.expand(sp.reduced(norm_c_sq, G, order='lex')[1])
    print("\n||b||^2 reduced =", sp.factor(nb_red))
    print("||c||^2 reduced =", sp.factor(nc_red))

    # ---- |cos theta|^2
    if dot_reduced == 0:
        print("\n>>> b . c == 0 EXACTLY in R[a1,a2,a3]/<a1^2+2a2a3>")
        print(">>> => cos(theta) = 0  EXACTLY  (rows ORTHOGONAL in C^3)")
        verdict = "OPEN"
    else:
        # Compute |cos|^2 = (b.c)^2 / (||b||^2 ||c||^2)
        cos_sq = sp.simplify(dot_reduced**2 / (nb_red * nc_red))
        print("\n|cos theta|^2 =", cos_sq)
        # Numerical sanity check at a generic real solution of constraint
        # take a2 = 1, a3 = 1, then a1^2 = -2 → a1 imaginary; not allowed
        # Use the actual numerical seed at tau=i: Y1≈real, Y2,Y3 satisfy ratio
        # From v2_audit.py phase analysis, real seeds satisfy a1^2+2 a2 a3 = 0
        # with a3/a1 ≈ 2.224, a2/a1 ≈ -0.225 → a1=1, a2=-0.225, a3=2.224
        # Check: 1 + 2 * (-0.225)(2.224) = 1 - 1.0008 ≈ 0 ✓
        num = float(cos_sq.subs({a1: 1, a2: sp.Rational(-225, 1000),
                                 a3: sp.Rational(2224, 1000)}))
        print("  numerical |cos|^2 at LYD20 ratios ≈", num)
        verdict = "CLOSED" if num > 1e-6 else "OPEN (numerically-verified-only)"

    print(f"\nVERDICT: {verdict}")

    # ----- Numerical sanity check using the actual eta-quotient seeds at tau=i
    print("\n" + "=" * 60)
    print("Numerical cross-check (Dedekind eta seeds at tau=i, 200 terms)")
    print("=" * 60)
    import sys
    sys.path.insert(0, '/root/crossed-cosmos/notes/eci_v7_aspiration/V2')
    from v2_audit import weight1_forms, all_forms
    import numpy as np
    Y1n, Y2n, Y3n = weight1_forms(1j, n_terms=200)
    fn = all_forms(Y1n, Y2n, Y3n)
    v_c = np.array([fn['Y2_3'], fn['Y2_5'], fn['Y2_4']])
    v_t = np.array([fn['Y5_3'], fn['Y5_5'], fn['Y5_4']])
    inner = np.vdot(v_c, v_t)
    nb = np.linalg.norm(v_c); nt = np.linalg.norm(v_t)
    cosv = inner / (nb * nt)
    print(f"  Y1^2 + 2 Y2 Y3 = {Y1n**2 + 2*Y2n*Y3n:.3e}  (algebra constraint)")
    print(f"  c^c row phases: {[round(np.angle(x)*180/np.pi,2) for x in v_c]}")
    print(f"  t^c row phases: {[round(np.angle(x)*180/np.pi,2) for x in v_t]}")
    print(f"  cos(theta)     = {cosv:.6e}")
    print(f"  |cos(theta)|   = {abs(cosv):.6e}")
    print(f"  |cos(theta)|^2 = {abs(cosv)**2:.6e}")
    print(f"  theta (deg)    = {np.arccos(min(abs(cosv),1.0))*180/np.pi:.6f}")


if __name__ == '__main__':
    main()
