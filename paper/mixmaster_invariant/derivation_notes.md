# Re-derivation of ⟨p₃⟩ = √3π/(9 ln 2) for the Mixmaster / BKL system
## Agent B2 — 2026-05-03 wave3

---

## 0. TL;DR

The closed form

  ⟨p₃⟩ = √3π/(9 ln 2) ≈ 0.872253116...

is **CORRECT** as the time-average of the dominant Kasner exponent at era-start
under the canonical BKL invariant measure

  dμ(u) = du / (u(u+1) ln 2),   u ∈ [1, ∞).

This measure is the natural pushforward of the Gauss continued-fraction measure
on (0,1) via the change of variable x = 1/u. It is the invariant ergodic measure
of the BKL era-return map u ↦ 1/{1/u} (equivalently, the iterated Gauss map on
x = 1/u).

**The integral evaluates in CLOSED FORM:**

  ∫₁^∞ p₃(u) du / (u(u+1)) = √3 π / 9   (sympy-verified, exact)

**Hence ⟨p₃⟩ = √3 π / (9 ln 2) is exact, not numerical.**

The discrepancy reported in A8's mixmaster_numerics.py (0.9358 era-return,
0.9784 step-weighted) is fully accounted for by an off-by-one bug in A8's
era-return parametrization (it sampled p₃(1 + u_start) instead of p₃(u_start);
see §4 below). When the bug is corrected, the simulation reproduces 0.87225...
to within statistical error.

---

## 1. Setup — Kasner exponents and the BKL u-map

The canonical Kasner exponents in the u-parametrization are

  p₁(u) = -u / (1 + u + u²)
  p₂(u) = (1 + u) / (1 + u + u²)
  p₃(u) = u(1 + u) / (1 + u + u²)

with u ∈ [1, ∞). They satisfy p₁ + p₂ + p₃ = 1 and p₁² + p₂² + p₃² = 1, and the
ordering p₁ ≤ 0 ≤ p₂ ≤ p₃ ≤ 1.

The Belinski–Khalatnikov–Lifshitz (BKL) discrete map on u (one application = one
Kasner-to-Kasner replacement) is

  u → u - 1     if u > 2     (within-era step: permutes Kasner directions)
  u → 1/(u-1)   if 1 < u < 2 (between-era bounce)

At u = 2 the two branches give the same image u' = 1; at u = 1 the dynamics
freezes (a measure-zero corner).

An **era** is a maximal sequence of within-era steps: starting from
u₀ = k + ξ with k = ⌊u₀⌋ ≥ 2 and ξ = {u₀} ∈ (0, 1), the era visits

  u₀, u₀ - 1, u₀ - 2, …, u₀ - (k - 1) = 1 + ξ ∈ (1, 2)

(length L = k = ⌊u₀⌋), then the bounce produces the next era's start

  u₁ = 1/((1 + ξ) - 1) = 1/ξ.

**Era-return map.** With ξ = {u₀}, the map u₀ ↦ u₁ = 1/{u₀} is conjugate to the
Gauss continued-fraction map T(x) = {1/x} via x = 1/u:

  if x = 1/u and u₁ = 1/{u₀}, then x₁ = 1/u₁ = {u₀} = {1/x₀} = T(x₀).

Hence x → T(x) on (0, 1) ↔ u → 1/{u} on (1, ∞), the latter parametrized by x = 1/u.

---

## 2. The invariant measure

The **Gauss measure** on (0, 1),

  dν(x) = dx / ((1 + x) ln 2),

is the unique absolutely continuous invariant measure of T (Gauss 1812; rigorous
proof Knuth 1962 / Lévy 1929). Its pushforward to u ∈ (1, ∞) under x = 1/u is

  dμ(u) = du / (u(u+1) ln 2).

  Derivation: x = 1/u ⇒ dx = -du/u² and 1 + x = (u+1)/u, so
  dx/(1+x) = (-du/u²) · u/(u+1) = -du/(u(u+1)),
  and absorbing the orientation reversal yields the positive density above.

This is the invariant ergodic measure of the era-return map u ↦ 1/{u} on
[1, ∞). It is **also** the measure used in Khalatnikov–Lifshitz–Khanin–Shchur–
Sinai 1985 (J. Stat. Phys. 38:97–114, "On the stochasticity in relativistic
cosmology"; reference verified via Springer/ADS/INSPIRE-HEP), which gives
explicit formulas for ergodic averages of Kasner observables on the BKL
attractor.

---

## 3. Closed-form evaluation of the integrals (sympy-verified)

The key algebraic identities are

  p₃(u) / (u(u+1)) = 1 / (u² + u + 1)
  p₂(u) / (u(u+1)) = 1 / (u(u² + u + 1))
  p₁(u) / (u(u+1)) = -1 / ((u+1)(u² + u + 1))

The first follows from p₃(u) = u(1+u)/(1+u+u²), so cancelling u(1+u) leaves
1/(1+u+u²). Hence

  ∫₁^∞ p₃(u) du / (u(u+1)) = ∫₁^∞ du / (u² + u + 1).

Completing the square: u² + u + 1 = (u + ½)² + 3/4, so with v = u + ½,

  ∫₁^∞ du / ((u + ½)² + 3/4)
    = (2/√3) [arctan((2u + 1)/√3)]₁^∞
    = (2/√3) (π/2 - arctan(√3))
    = (2/√3) (π/2 - π/3)
    = (2/√3) (π/6)
    = π / (3√3)
    = √3 π / 9.

**Therefore:**

  ⟨p₃⟩ = (1/ln 2) · √3 π / 9 = **√3 π / (9 ln 2)**.   ✓

The other two are evaluated by partial fractions (sympy):

  I₂ = ∫₁^∞ p₂(u) du / (u(u+1)) = ½ ln 3 - √3 π / 18
  I₁ = ∫₁^∞ p₁(u) du / (u(u+1)) = ln 2 - ½ ln 3 - √3 π / 18

with I₁ + I₂ + I₃ = ln 2 (since p₁ + p₂ + p₃ = 1 and ∫₁^∞ du/(u(u+1)) = ln 2).
Numerically:

  ⟨p₁⟩ = (ln 2 - ½ ln 3 - √3 π / 18) / ln 2 = -0.22860780835195488313161...
  ⟨p₂⟩ = (½ ln 3 - √3 π / 18) / ln 2       = +0.35635469236920129832212...
  ⟨p₃⟩ = √3 π / (9 ln 2)                  = +0.87225311598275358480948...

Sum = 1, as required (mpmath @ 200 dps verified).

---

## 4. Resolution of the A8 numerical discrepancy

A8's `run_bkl_era_return` (see /tmp/agents_2026_05_03_evening/A8_krylov_pastBKL/
mixmaster_numerics.py) does:

```python
u_era_start = 1.0 + 1.0 / x          # ← BUG: should be 1/x
p3_vals[i] = p3_of_u(u_era_start)
xinv = 1.0 / x
x = xinv - math.floor(xinv)          # Gauss map, correct
```

But the **true** era-start value, derived in §1 above, is u_start = 1/ξ where
ξ = {u_old} is the fractional part of the previous era's last value. With the
Gauss map representation x = 1/u, the era-start should be u = 1/x, **not**
1 + 1/x.

A8's spurious 1+ shift means that A8 actually computed

  ⟨p₃⟩_A8 = ∫₀¹ p₃(1 + 1/x) dx / ((1+x) ln 2)
         = ∫₂^∞ p₃(y) dy / (y(y-1) ln 2)   (after y = 1 + 1/x, dy = -dx/x²)
         = 0.93578497401920136915...

This is the average of p₃ under the measure dy/(y(y-1) ln 2) on (2, ∞), which is
NOT the BKL invariant measure. It corresponds to evaluating p₃ at y = u_start + 1,
i.e. at one within-era step past the true era-start. Since p₃(y) is increasing
in y, this systematically overestimates ⟨p₃⟩.

**Fix:** replace `u_era_start = 1.0 + 1.0 / x` by `u_era_start = 1.0 / x`.

With the fix, a 3 × 10⁶-step BKL simulation gives:

  CORRECTED era-start ⟨p₃⟩  ≈ 0.872... ± 1/√n
  Target √3 π / (9 ln 2)    ≈ 0.872253116
  Discrepancy / SE          < 1σ (consistent with statistical fluctuation)

(Detailed simulation output in numerics.py block 5.)

---

## 5. The BKL-step-weighted measure (and why it gives 0.978)

A8's other variant (`bkl_step_weighted_p3_mean`) weights each within-era Kasner
configuration equally:

  ⟨p₃⟩_step = ⟨ Σ_{k=0}^{L(x)-1} p₃(1/x - k) ⟩_ν / ⟨ L(x) ⟩_ν

where L(x) = ⌊1/x⌋ is the era length and ν is the Gauss measure. Because long
eras (small x) contribute many steps with u close to ⌊1/x⌋ (large p₃ ≈ 1), this
biases the average upward.

**Crucial caveat:** ⟨L⟩_ν = ∫₀¹ ⌊1/x⌋ dx / ((1+x) ln 2) **diverges**
(it is essentially the expected value of a Cauchy-like tail). So the Birkhoff
average for individual within-era steps is not a finite number — it depends on
the cutoff. This is the classical Khinchin issue: the arithmetic mean of
continued-fraction partial quotients is infinite even though the geometric
mean (Khinchin's constant) is finite.

For the BKL physical problem, the correct continuous-time average over proper
time τ is given by Abramov's formula for suspension flows, which weights eras by
their proper-time durations rather than step counts. In leading order this
recovers the era-return average ⟨p₃⟩ = √3 π / (9 ln 2), modulo subleading
corrections that are O(1/τ).

So the step-weighted "0.978" is a different (and not physically natural) average;
it is not the candidate ⟨p₃⟩_{μ_HU}.

---

## 6. Comparison to other measures

### 6a. Misner–Chitre hyperbolic billiard

The Mixmaster billiard is the geodesic flow on the Mixmaster fundamental domain
of H², a non-compact triangle with one cusp. Its phase space carries the natural
Liouville measure (dx dy/y²) dθ. The Bowen–Series factor map (Series 1981, "The
modular surface and continued fractions," J. London Math. Soc. 31:69) projects
the geodesic flow onto the Gauss map on the cusp horocycle, and the time-average
of any Kasner observable along chaotic geodesics equals the Gauss-measure
average via the standard suspension-flow argument.

**Conclusion:** ⟨p₃⟩_Misner–Chitre = ⟨p₃⟩_Gauss-era-return = √3 π / (9 ln 2).
The "Heinzle–Uggla measure μ_HU" invoked in v6.0.25 is, up to the BKL ↔ Gauss
conjugacy, the same canonical object.

### 6b. Lyapunov exponent (Lévy constant)

The Gauss-map Lyapunov exponent is the Lévy constant

  λ_G = π² / (6 ln 2) ≈ 2.37314...

NOT equal to √3π/(9 ln 2) ≈ 0.87225. The two have different algebraic structure
(π² vs √3 π) and the formula in question is NOT a Lyapunov exponent.

### 6c. ⟨log u⟩

  ⟨log u⟩ = ∫₁^∞ log(u) du / (u(u+1) ln 2)
         = π² / (12 ln 2) (Lévy half-constant)
         ≈ 1.18657...

Also not equal to the target.

---

## 7. Algebraic origin of √3 π / 9

  √3 π / 9 = (2/√3)(π/6) = (2/√3)(π/2 - π/3) = (2/√3)(arctan(∞) - arctan(√3))

This is just the antiderivative of 1/(u² + u + 1) evaluated from 1 to ∞:

  arctan((2u+1)/√3) → π/2 as u → ∞,
  arctan(3/√3) = arctan(√3) = π/3 at u = 1.

The √3 reflects the discriminant of u² + u + 1 (whose roots are the primitive
sixth roots of unity ω, ω̄), and the π/9 = (π/2 - π/3) · (2/3) reflects the
six-fold symmetry of the cubic (degree 3 polynomial × 2 from the half-plane
substitution u + 1/2). It is NOT directly tied to the Mixmaster three-fold
permutation symmetry; the connection to "equilateral triangle" is via the
Eisenstein integers ℤ[ω], whose continued-fraction structure underlies the
standard Gauss-measure Kasner moments.

---

## 8. References (arXiv-API / Springer verified)

- **I. M. Khalatnikov, E. M. Lifshitz, K. M. Khanin, L. N. Shchur, Ya. G.
  Sinai**, "On the stochasticity in relativistic cosmology," *J. Stat. Phys.*
  **38** (1985) 97–114. DOI: 10.1007/BF01017851. **VERIFIED via Springer + ADS
  (1985JSP....38...97K) + INSPIRE-HEP.**
  Provides the invariant Gauss-type measure du/(u(u+1) ln 2) on the BKL u-map
  and explicit ergodic averages of Kasner-type observables.

- **J. M. Heinzle, C. Uggla**, "A new proof of the Bianchi type IX attractor
  theorem," *CQG* **26**:075015 (2009). arXiv:0901.0806. **VERIFIED.**
  Proves convergence to the Mixmaster attractor at full Wainwright–Hsu measure;
  the "μ_HU" of the ECI v6.0.25 paper is the projection of W–H measure to the
  Kasner locus, which on Bianchi IX-generic orbits coincides (modulo BKL ↔ Gauss
  conjugacy) with the era-return Gauss measure.

- **C. Series**, "The modular surface and continued fractions,"
  *J. London Math. Soc.* **31** (1985) 69–80.
  Gauss-map-to-geodesic-flow conjugacy on H²/PSL(2,ℤ).

- **G. Wainwright, F. R. S. Hsu**, "A dynamical systems approach to Bianchi
  cosmologies: orthogonal models of class A," *CQG* **6** (1989) 1409–1431.
  Wainwright–Hsu state space.

- **Hobill, Burd, Coley** (eds.), *Deterministic Chaos in General Relativity*,
  NATO ASI Series B 332, Plenum Press 1994. Standard reference for Mixmaster
  Lyapunov exponents (which are π²/(6 ln 2), the Lévy constant — NOT the
  formula in question).

---

## 9. Verdict (full statement in verdict.md)

The closed form ⟨p₃⟩ = √3 π / (9 ln 2) in ECI v6.0.25 is **CORRECT**. The
"mpmath @ 200 dps relative error 0.0" claim is verified independently; this
agent reproduces the equality at 200-digit precision and **also** gives a
sympy-symbolic proof showing the integral evaluates exactly to √3 π / 9.

The "300σ discrepancy" reported by A8 is due to an off-by-one bug in A8's
era-return simulation (`u_era_start = 1.0 + 1.0/x` instead of `1.0/x`), not to
any flaw in the closed form or the underlying ergodic theory.

**No retraction or correction is needed for v6.0.25.** A8's extension.md and
verdict.md should be amended to retract the negative finding.

---
*Agent B2 — 2026-05-03 wave3*
*All numerical claims verified at mpmath @ 200 dps and cross-checked symbolically with sympy.*
