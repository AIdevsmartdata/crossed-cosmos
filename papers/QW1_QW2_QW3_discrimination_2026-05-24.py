#!/usr/bin/env python3
"""QW1 + QW2 + QW3 — Discrimination test κ_A (group) vs κ_B (dimension).

QW1 : verify |Φ⁺(SU(N))| = N(N-1)/2 + check coincidence κ_A(N) = κ_B(D)
QW2 : table α predicted for all testable (N,D) pairs
QW3 : solve D(D-1)(5-D)/6 = N-1 for N=2..6 (exhaustive saturation pairs)
"""
from fractions import Fraction
from math import comb

print("=" * 78)
print("QW1 — Coincidence κ_A(N) = κ_B(D) ⇔ N(N-1) = 2(D-1)")
print("=" * 78)
print("""
Interpretations of κ for saturated pairs:
  κ_A(N) := 1 / (2 |Φ⁺(SU(N))|) = 1 / (N(N-1))    (Lie algebra, group-theoretic)
  κ_B(D) := 1 / (2(D-1))                            (Hodge, dimension)

Coincidence requires : 2(D-1) = 2|Φ⁺| = N(N-1)
                     ⟺ D = N(N-1)/2 + 1 = C(N,2) + 1
""")
print(f"{'(N,D)':>8} | {'|Φ⁺|':>5} | {'N(N-1)':>7} | {'2(D-1)':>7} | {'Match?':>7} | {'κ_A':>10} | {'κ_B':>10}")
print("-" * 78)
sat_pairs = [(2,2), (3,3), (3,4), (4,4), (4,5), (5,5), (5,6), (6,6)]
divergences = []
for N, D in sat_pairs:
    phi_plus = N * (N-1) // 2
    a_side = N * (N-1)
    b_side = 2 * (D-1)
    kappa_A = Fraction(1, a_side) if a_side > 0 else Fraction(0)
    kappa_B = Fraction(1, b_side) if b_side > 0 else Fraction(0)
    match = "✅ YES" if a_side == b_side else "❌ DIV"
    if a_side != b_side:
        divergences.append((N, D, kappa_A, kappa_B))
    print(f"{f'({N},{D})':>8} | {phi_plus:>5} | {a_side:>7} | {b_side:>7} | {match:>7} | {str(kappa_A):>10} | {str(kappa_B):>10}")

print(f"\nDivergent pairs (where A vs B can be distinguished by α measurement):")
for N, D, kA, kB in divergences:
    aA = 1 - kA
    aB = 1 - kB
    print(f"  ({N},{D}) : α_A = {aA} = {float(aA):.4f},  α_B = {aB} = {float(aB):.4f},  gap = {abs(float(aA) - float(aB)):.4f}")

print("\n" + "=" * 78)
print("QW2 — Predicted α table for all (N,D) with N=2..6, D=2..6")
print("=" * 78)
print(f"\n{'(N,D)':>6} | {'rank=N-1':>10} | {'C(D,2)-C(D,3)':>14} | {'saturated?':>11} | {'α_A':>10} | {'α_B':>10} | {'disc':>6}")
print("-" * 80)

for N in range(2, 7):
    rank_N = N - 1
    for D in range(2, 7):
        C2 = comb(D, 2)
        C3 = comb(D, 3)
        sat = (rank_N == max(0, C2 - C3))
        if sat:
            phi_plus = N * (N-1) // 2
            kappa_A = Fraction(1, 2 * phi_plus)
            kappa_B = Fraction(1, 2 * (D-1))
            alpha_A = 1 - kappa_A
            alpha_B = 1 - kappa_B
            disc = abs(float(alpha_A) - float(alpha_B))
            sat_mark = "✅"
            disc_str = f"{disc:.4f}" if disc > 0 else "—"
            print(f"{f'({N},{D})':>6} | {rank_N:>10} | {C2-C3:>14} | {sat_mark:>11} | {str(alpha_A):>10} | {str(alpha_B):>10} | {disc_str:>6}")
        else:
            # Pinsker bound only, α = 1 trivial
            sat_mark = "❌ non"
            print(f"{f'({N},{D})':>6} | {rank_N:>10} | {C2-C3:>14} | {sat_mark:>11} | {'1 (Pinsker)':>10} | {'1 (Pinsker)':>10} | {'—':>6}")

print("\n" + "=" * 78)
print("QW3 — Exhaustive saturation pairs : solve D(D-1)(5-D)/6 = N-1, N=2..6")
print("=" * 78)
print(f"""
Polynomial p(D) = D(D-1)(5-D)/6 :
  D=2 : 2·1·3/6 = 1  → rank=1 ⇒ N=2 (SU(2))
  D=3 : 3·2·2/6 = 2  → rank=2 ⇒ N=3 (SU(3))
  D=4 : 4·3·1/6 = 2  → rank=2 ⇒ N=3 (SU(3))
  D=5 : 5·4·0/6 = 0  → rank=0 ⇒ N=1 trivial
  D≥6 : negative    → no non-abelian saturation

Saturated pairs (N,D) with N≥2 :
""")
for D in range(2, 11):
    val = D * (D-1) * (5-D) // 6
    if val == 0:
        marker = "trivial (rank=0)"
    elif val < 0:
        marker = f"negative ({val}) — no saturation"
    else:
        # rank = val ⇒ N = val + 1
        N = val + 1
        marker = f"⇒ SU({N}) saturated"
    print(f"  D={D:2} : p(D) = {val:3} | {marker}")

print(f"""
THE 3 SATURATED PAIRS in total (N,D) integer space :
  (SU(2), D=2)  — 2D YM heat kernel
  (SU(3), D=3)  — 3D test case ← discrimination point!
  (SU(3), D=4)  — physical QCD case (Clay)

No other (N,D) with N≥2, D≥2 satisfies rank(SU(N)) = D(D-1)(5-D)/6.
""")

print("=" * 78)
print("DISCRIMINATION TEST — what α(SU(3), D=3) will reveal")
print("=" * 78)
print(f"""
SU(3) D=3 is the ONLY pair where Interpretation A and B diverge :
  κ_A(SU(3)) = 1/(2·3)         = 1/6 ≈ 0.1667  → α_A = 5/6 ≈ 0.8333
  κ_B(D=3)   = 1/(2·(3-1))     = 1/4 = 0.2500  → α_B = 3/4 = 0.7500
  Gap : |α_A - α_B| = 1/12     ≈ 0.0833

This 8% gap is MEASURABLE with MK at β = 10-50 (where MK is reliable per T1 verdict
that β > 200 is contaminated).

Decision matrix from upcoming SU(3) D=3 HMC + MK measurement :
  α ≈ 0.75 ± 0.05  →  ✅ INTERPRETATION B wins (κ Hodge geometric, depends on D)
                       ⇒ H6 framework reformulation : κ purely topological
                       ⇒ H10 cible reste Polchinski cascade géométrique
  α ≈ 0.83 ± 0.05  →  ✅ INTERPRETATION A wins (κ Lie-algebraic, depends on N)
                       ⇒ H6 framework via |Φ⁺| group-theoretic
                       ⇒ H10 cible reformulé Peter-Weyl Schur-Weyl
  α ≈ 1.0 ± 0.05   →  ❌ Both fail : SU(3) D=3 not saturated in practice
                       ⇒ Framework limited to D=4 only
  α other          →  🟡 New physics or MK systematic

P(B wins) prior ~ 60% (κ·2(D-1) = 1 holds clean for 3/3 pairs A also passes (2,2) by coincidence)
P(A wins) prior ~ 30%
P(other)  prior ~ 10%

Cluster firm 725 STABLE.
""")
