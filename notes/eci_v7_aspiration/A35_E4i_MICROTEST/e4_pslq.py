"""
A35 — Micro-test (30-min budget): does E_4(i) ≈ 3·Γ(1/4)⁸/(2π)⁶ land near
the Sorbo-Peloso axion-gauge target ξ ~ 4-5 needed for LISA-detectable
chiral SGWB in anisotropic-inflation models?

Strategy:
  1. Compute E_4(τ=i) with mp.dps = 60 from the q-series
       E_4(τ) = 1 + 240 Σ_{n>=1} σ_3(n) q^n,  q = e^{2πiτ}
     At τ=i, q = e^{-2π} ≈ 0.00187, so a few hundred terms saturate dps=60.
  2. Verify the classical Chowla-Selberg / CM identity at τ=i:
       E_4(i) = 3 · Γ(1/4)^8 / (2π)^6
     (Note: the prompt heuristic mentions "1.4557·Γ(1/4)⁸/(2π)⁶"; this is
      a misremembering — the correct rational prefactor is 3.)
  3. Compute E_6(i) and Δ(i) from q-series; cross-check E_6(i) ≈ 0 by CM.
  4. Compare E_4(i) numerical value to ξ ~ 4-5 axion-gauge target. Test
     small-integer multiples (k·E_4(i), k=1..5) and natural rationals
     (3·E_4(i), π·E_4(i), √(6)·E_4(i), …).
  5. PSLQ search: try to find an integer relation
         a·ξ_target + b·E_4(i) + c·E_4(i)² + d·log E_4(i) + ...
     that produces ξ ≃ 4-5 from CM-anchored constants at τ=i. Bases include
     E_4(i), E_4(i)², log E_4(i), Γ(1/4), π, log 2, √6, Ω_K.

Verdict template:
  - ANALYTIC CONNECTION FOUND if a non-trivial PSLQ relation lands ξ ~ 4-5
    with small integer coefficients and residual < 10⁻⁵⁰.
  - EXHAUSTED otherwise.

Author: Sonnet sub-agent A35 (2026-05-05)
Hallu count entering: 78
"""

import mpmath as mp

DPS = 60
mp.mp.dps = DPS

# ---------------------------------------------------------------------------
# 1. q-series for E_4, E_6 at τ = i
# ---------------------------------------------------------------------------

def divisor_sigma(n, k):
    """sigma_k(n) = sum of d^k over divisors d of n."""
    s = 0
    for d in range(1, n + 1):
        if n % d == 0:
            s += d ** k
    return s

def eisenstein_q_series(tau, k, n_terms):
    """E_k(τ) for k in {4,6,8,...} via classical normalization
       E_k(τ) = 1 + (2k/B_k) * Σ σ_{k-1}(n) q^n,  q = exp(2πiτ).
       Coefficient table:
         k=4: 240
         k=6: -504
         k=8: 480
    """
    coeff = {4: mp.mpf(240), 6: mp.mpf(-504), 8: mp.mpf(480)}[k]
    q = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpc(1, 0)
    for n in range(1, n_terms + 1):
        s += coeff * divisor_sigma(n, k - 1) * q ** n
    return s

tau = mp.mpc(0, 1)
q = mp.exp(2 * mp.pi * 1j * tau)         # = e^{-2π}, real positive
print("=" * 72)
print("A35 — E_4(i) micro-test for A23 LISA bridge   (mpmath dps=%d)" % DPS)
print("=" * 72)
print()
print("τ        =", tau)
print("q=e^{2πiτ}=", mp.nstr(q, 30), "  (real, ≈ 0.00187)")
print()

# Number of q-series terms needed: q^N must be < 10^{-(DPS+10)}.
# log10(q) = -2π/log(10) ≈ -2.7287, so N ≈ (DPS+10)/2.7287 ≈ 26 terms suffice
# for DPS=60. Use 80 to be conservative + σ_3 grows, but is overwhelmed by q^n.
N_TERMS = 80
print("Computing E_4(i) from q-series with N =", N_TERMS, "terms ...")
E4_i = mp.re(eisenstein_q_series(tau, 4, N_TERMS))
print("E_4(i)   =", mp.nstr(E4_i, 55))
print()

print("Computing E_6(i) from q-series ...")
E6_i = mp.re(eisenstein_q_series(tau, 6, N_TERMS))
print("E_6(i)   =", mp.nstr(E6_i, 55))
print("|E_6(i)| =", mp.nstr(abs(E6_i), 10), "   (expected 0 by CM at τ=i)")
print()

# ---------------------------------------------------------------------------
# 2. Closed-form identity:  E_4(i) = 3 · Γ(1/4)^8 / (2π)^6
# ---------------------------------------------------------------------------
# Derivation (Chowla–Selberg specialized to K=Q(i), discriminant -4):
#   Ω_K := Γ(1/4)² / (2 √(2π))
#   For τ=i, ω_1 = 1, ω_2 = i. The Weierstrass invariant g_2 satisfies
#   g_2 = (4π^4/3) E_4(τ) · (1/ω_1)^4. At the lemniscatic point with
#   suitable normalization, g_2(i) = 4 ϖ^4 where ϖ = Γ(1/4)²/(2√(2π))·√π
#   = Γ(1/4)²/(2√2). Working through:
#     E_4(i) · (2π)^6 / 3  =  Γ(1/4)^8
#   Equivalently:
#     E_4(i) = 3 · Γ(1/4)^8 / (2π)^6
# This is a known classical identity (e.g., Zagier "Elliptic modular forms
# and their applications", 2008, formula in §1.6).
# ---------------------------------------------------------------------------

pi = mp.pi
gamma14 = mp.gamma(mp.mpf(1) / 4)

E4_closed = 3 * gamma14 ** 8 / (2 * pi) ** 6
print("=" * 72)
print("Test classical identity:  E_4(i) =? 3·Γ(1/4)^8 / (2π)^6")
print("=" * 72)
print("LHS (q-series)  :", mp.nstr(E4_i,      55))
print("RHS (closed)    :", mp.nstr(E4_closed, 55))
residual = E4_i - E4_closed
print("residual        :", mp.nstr(residual, 10))
print("ratio LHS/RHS   :", mp.nstr(E4_i / E4_closed, 30))
print()

# Also test the prompt's heuristic "1.4557·Γ(1/4)^8/(2π)^6": expect
#   1.4557·Γ(1/4)^8/(2π)^6 ≈ 1.4557 · (E4_i/3) ≈ 0.4852·E4_i  ≠ E4_i.
heuristic = mp.mpf("1.4557") * gamma14 ** 8 / (2 * pi) ** 6
print("Prompt heuristic 1.4557·Γ(1/4)^8/(2π)^6 =", mp.nstr(heuristic, 30))
print("→ off by factor", mp.nstr(E4_i / heuristic, 10),
      "(prompt mis-quoted; correct prefactor is 3, giving E_4(i)≈1.4557).")
print()

# ---------------------------------------------------------------------------
# 3. Δ(i) and j(i) cross-checks
# ---------------------------------------------------------------------------
# Δ(τ) = (E_4^3 - E_6^2)/1728 ; at τ=i, E_6(i)=0 ⇒ Δ(i) = E_4(i)^3 / 1728
# j(τ) = E_4^3 / Δ ; at τ=i, j(i) = 1728 (exact).
Delta_i_from_q = (E4_i ** 3 - E6_i ** 2) / 1728
j_i = E4_i ** 3 / Delta_i_from_q
print("=" * 72)
print("Δ(i), j(i) cross-checks")
print("=" * 72)
print("Δ(i) = (E_4^3 - E_6^2)/1728 =", mp.nstr(Delta_i_from_q, 40))
print("j(i)  = E_4^3 / Δ           =", mp.nstr(j_i, 40), "   (expected 1728)")
print("|j(i) - 1728|                =", mp.nstr(abs(j_i - 1728), 10))
print()

# Independent η(i) closed form: η(i) = Γ(1/4) / (2 π^{3/4})
# Convention: q-series Δ(τ) = q · Π(1-q^n)^{24} with q = e^{2πiτ}; equivalently
#   Δ(τ) = η(τ)^{24}.  At τ=i, Δ(i) = η(i)^{24} = Γ(1/4)^{24}/(2^{24} π^{18}).
# (No (2π)^{12} multiplier in the q-Eisenstein normalization used here.)
eta_i = gamma14 / (2 * mp.power(pi, mp.mpf(3) / 4))
Delta_i_closed = eta_i ** 24
print("Δ(i) closed η(i)^24         =", mp.nstr(Delta_i_closed, 40))
print("residual q-series vs closed :", mp.nstr(Delta_i_from_q - Delta_i_closed, 10))

# ---------------------------------------------------------------------------
# 4. Numerical E_4(i) vs Sorbo–Peloso target ξ ~ 4–5
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("E_4(i) vs Sorbo–Peloso target ξ ~ 4-5 (LISA chiral SGWB)")
print("=" * 72)
xi_lo = mp.mpf("4.0")
xi_hi = mp.mpf("5.0")
print("E_4(i)             =", mp.nstr(E4_i, 30))
print("ξ_target window    = [4, 5]")
print("E_4(i) / 4         =", mp.nstr(E4_i / 4, 10))
print("E_4(i) / 5         =", mp.nstr(E4_i / 5, 10))
print("→ ratio: ξ_target / E_4(i) ≈",
      mp.nstr(xi_lo / E4_i, 10), "to", mp.nstr(xi_hi / E4_i, 10))
print()
print("Small-integer multiples of E_4(i):")
for k in range(1, 6):
    val = k * E4_i
    print(f"  {k} · E_4(i) = {mp.nstr(val, 20)}    Δ(ξ_lo)={mp.nstr(val-xi_lo,6)}  Δ(ξ_hi)={mp.nstr(val-xi_hi,6)}")
print()
print("Natural rational/transcendental dressings:")
candidates = {
    "π · E_4(i)"       : pi * E4_i,
    "√6 · E_4(i)"      : mp.sqrt(6) * E4_i,
    "e · E_4(i)"       : mp.e * E4_i,
    "Γ(1/4) · E_4(i)"  : gamma14 * E4_i,
    "E_4(i)^2"         : E4_i ** 2,
    "E_4(i)^{4/3}"     : mp.power(E4_i, mp.mpf(4)/3),
    "log(E_4(i)+1)·10" : mp.log(E4_i + 1) * 10,
    "2π/E_4(i)"        : 2*pi/E4_i,
    "(2π)/√(E_4(i))"   : 2*pi/mp.sqrt(E4_i),
    "j(i)^{1/4}/E_4(i)": mp.power(1728, mp.mpf(1)/4)/E4_i,
}
for name, val in candidates.items():
    in_window = (xi_lo <= val <= xi_hi)
    flag = "  *** IN WINDOW ***" if in_window else ""
    print(f"  {name:25s} = {mp.nstr(val, 20)}{flag}")
print()

# ---------------------------------------------------------------------------
# 5. PSLQ integer-relation searches: can ξ_target ≃ 4 or 5 be obtained
#    as a small-integer combination of CM-anchored quantities at τ=i?
# ---------------------------------------------------------------------------

print("=" * 72)
print("PSLQ searches for ξ_target ~ 4-5 from CM constants at τ=i")
print("=" * 72)

def try_pslq(label, vec, max_coeff=500):
    print(f"\n[{label}]   basis size = {len(vec)}")
    try:
        rel = mp.pslq(vec, tol=mp.mpf(10) ** (-50), maxcoeff=max_coeff)
    except Exception as e:
        print("  PSLQ raised:", e)
        return None
    if rel is None:
        print("  PSLQ exhausted (no relation with |c|<=%d)" % max_coeff)
        return None
    s = mp.mpf(0)
    for c, v in zip(rel, vec):
        s += c * v
    print("  Relation:", rel)
    print("  Residual:", mp.nstr(s, 6))
    return rel

# Note: any basis containing both `1` and the integer `4` (or `5`) trivially
# yields the relation 4·1 − 1·4 = 0. To detect a *non-trivial* analytic
# connection we DROP the rational integer from the basis and instead test
# whether ξ_target is well-approximated by combinations of the period-ring
# constants {E_4(i), π, Γ(1/4), √6, Ω_K, log 2, ...}.  Equivalently we ask
# PSLQ whether there is a small-integer relation among
#   { ξ_target, E_4(i), π, Γ(1/4), ... }   that is NOT just  ξ_target = N·1.

xi4 = mp.mpf(4)
xi5 = mp.mpf(5)
sqrt6 = mp.sqrt(6)
log2 = mp.log(2)
Omega_K = gamma14 ** 2 / (2 * mp.sqrt(2 * pi))

# B1': ξ=4 vs {E_4(i), π, Γ(1/4)}  — NO `1` in basis (kills trivial rel)
B1 = [xi4, E4_i, pi, gamma14]
print("B1 labels: [4, E_4(i), π, Γ(1/4)]   (no `1`)")
try_pslq("B1: ξ=4 vs E_4(i),π,Γ(1/4)", B1, max_coeff=500)

# B2: ξ=5 vs same
B2 = [xi5, E4_i, pi, gamma14]
print("\nB2 labels: [5, E_4(i), π, Γ(1/4)]")
try_pslq("B2: ξ=5 vs E_4(i),π,Γ(1/4)", B2, max_coeff=500)

# B3: log basis — multiplicative; does log4 live in {log E_4(i), log π, log 2}?
B3 = [mp.log(xi4), mp.log(E4_i), mp.log(pi), log2]
print("\nB3 labels: [log4, log E_4(i), log π, log2]")
try_pslq("B3: multiplicative ξ=4", B3, max_coeff=500)
# Note: log4 = 2 log2 is trivially recovered.

# B4: log ξ=4 dropping log2 — kills trivial 2log2 relation
B4 = [mp.log(xi4), mp.log(gamma14), mp.log(pi), mp.log(E4_i)]
print("\nB4 labels: [log4, log Γ(1/4), log π, log E_4(i)]   (NO log2 — kills trivial)")
try_pslq("B4: log ξ=4 vs Γ(1/4),π,E_4(i)", B4, max_coeff=500)

# B5: linear, wider, NO `1` in basis
B5 = [xi4, E4_i, sqrt6, pi, gamma14, Omega_K]
print("\nB5 labels: [4, E_4(i), √6, π, Γ(1/4), Ω_K]   (no `1`)")
try_pslq("B5 linear", B5, max_coeff=1000)

# B6: ξ=5
B6 = [xi5, E4_i, sqrt6, pi, gamma14, Omega_K]
print("\nB6 labels: [5, E_4(i), √6, π, Γ(1/4), Ω_K]   (no `1`)")
try_pslq("B6 linear (ξ=5)", B6, max_coeff=1000)

# B7: ξ=4 vs polynomial in E_4(i), with `1` retained — test for
# small integer poly relating ξ to E_4(i). Allowed: ξ = N (trivial).
# So inspect what PSLQ returns at increasing maxcoeff to see if any
# *deeper* (non-trivial) relation exists.
B7 = [xi4, E4_i, E4_i ** 2, E4_i ** 3]
print("\nB7 labels: [4, E_4(i), E_4(i)^2, E_4(i)^3]   (no `1`; pure polynomial)")
try_pslq("B7 poly", B7, max_coeff=1000)

B8 = [xi5, E4_i, E4_i ** 2, E4_i ** 3]
print("\nB8 labels: [5, E_4(i), E_4(i)^2, E_4(i)^3]   (no `1`)")
try_pslq("B8 poly ξ=5", B8, max_coeff=1000)

# B9: deeper — multiplicative relation between ξ_target and π·E_4(i),
# 2π/E_4(i), since both landed in window [4,5] above. Are these
# *exactly* 4 or 5? PSLQ on (1, ξ, π·E_4(i)):
B9 = [mp.mpf(1), xi4, pi * E4_i]
print("\nB9 labels: [1, 4, π·E_4(i)]")
try_pslq("B9: is π·E_4(i) = 4 + small?", B9, max_coeff=10000)
# If π·E_4(i) were rational this would yield a relation; expect EXHAUSTED.

B10 = [mp.mpf(1), xi4, 2 * pi / E4_i]
print("\nB10 labels: [1, 4, 2π/E_4(i)]")
try_pslq("B10: is 2π/E_4(i) = 4 + small?", B10, max_coeff=10000)

# B11: linear basis spanning {E_4(i), 1/E_4(i), π, π·E_4(i), 2π/E_4(i), 4}
B11 = [xi4, E4_i, 1/E4_i, pi, pi * E4_i, 2*pi/E4_i]
print("\nB11 labels: [4, E_4(i), 1/E_4(i), π, π·E_4(i), 2π/E_4(i)]")
try_pslq("B11", B11, max_coeff=500)

# B12: same for ξ=5
B12 = [xi5, E4_i, 1/E4_i, pi, pi * E4_i, 2*pi/E4_i]
print("\nB12 labels: [5, E_4(i), 1/E_4(i), π, π·E_4(i), 2π/E_4(i)]")
try_pslq("B12 (ξ=5)", B12, max_coeff=500)

# B13: include j(i)^{1/4} = 1728^{1/4} (which is rational over Γ(1/4)·π via
# j(i) = E_4(i)^3 / Δ(i) = 1728), and ratio j(i)^{1/4}/E_4(i)
j_quarter = mp.power(1728, mp.mpf(1)/4)
B13 = [xi4, E4_i, pi, gamma14, j_quarter, j_quarter / E4_i]
print("\nB13 labels: [4, E_4(i), π, Γ(1/4), 1728^{1/4}, 1728^{1/4}/E_4(i)]")
try_pslq("B13: ξ=4 with j(i)^{1/4}", B13, max_coeff=500)

print()
print("=" * 72)
print("VERDICT BLOCK — see SUMMARY.md for narrative")
print("=" * 72)
print()
print("Headline numbers:")
print(f"  E_4(i)                        = {mp.nstr(E4_i, 30)}")
print(f"  3·Γ(1/4)^8/(2π)^6 (closed)    = {mp.nstr(E4_closed, 30)}")
print(f"  residual                      = {mp.nstr(E4_i - E4_closed, 6)}")
print(f"  ξ_target / E_4(i) (lo, hi)    = {mp.nstr(xi_lo/E4_i, 6)}, {mp.nstr(xi_hi/E4_i, 6)}")
print(f"  factor needed (multiplier)    ≈ {mp.nstr((xi_lo+xi_hi)/2/E4_i, 6)}")
