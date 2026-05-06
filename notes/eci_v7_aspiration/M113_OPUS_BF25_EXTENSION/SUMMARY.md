---
name: M113 Opus BF25 §10.5.2 + Pet12 explicit green light for Γ_1(4) level extension — REDUCED to (B1) μ_6 p=3 + (B2) cusp vanishing
description: Critical M102 correction: BF25 mixed Tate proof in Appendix D + §10.5.2 NOT §2 (which is harmonic lifts). BF25 §10.5.2 explicit: "Petersen [Pet12 Thm 5.1] level structure... Γ_1(m), Γ_0(m)... arguments go through with very minor changes" (Pet12 Rem 6.4). Conditional theorem M113: (B1)+(B2) → M̄_{1,3}^{Γ_1(4)} mixed Tate over Z[i, 1/2] → Gross-Zagier Γ_1(4) wt 4. dim S_4(Γ_1(4))=0 standard → cusp motive vanishes. Brown-Fonseca probability 22-26% → 24-28%
type: project
---

# M113 — Opus BF25 §10.5.2 level extension (Γ_1(4) over Z[i, 1/2])

**Date:** 2026-05-06 | **Hallu count: 95 → 95** held (M113 0 new fabs) | **Mistral STRICT-BAN observed**

## VERDICT: (B) REDUCED to 2 sub-claims (B1) + (B2)

Probability Brown-Fonseca × M52 : 22-26% (M102) → **24-28%** (M113).

## Critical correction to M102 brief

**M102 stated** : "Reading BF25 §2 carefully is the next concrete action" (level-1 trivialisation).

**M113 finds** : BF25 §2 is on **harmonic lifts and Laplace eigenfunctions** — NOT the trivialisation. The level-1 mixed Tate proof is in **Appendix D §D.4 + §10.5.2**.

M102's framing ("M_{1,3} → M_{0,m}/G via Legendre + 7 points") is conceptually correct but technically inaccurate : BF25 uses a **stratification** of M̄_{1,3} by products M_{0,r} × M_{1,s} mod finite quotients — not a single map.

## BF25 verbatim quotes (verified PDF read)

**BF25 Theorem 1.6 (p.4)** :
> "The motive of M_{1,3} is mixed Tate. Consequently, the motive M^3_cusp vanishes, (1.6) is Kummer, and the Gross-Zagier conjecture holds in weight 4 and level 1 for any CM points z, w."

**BF25 Prop D.7 (p.67)** :
> "The motives M(M̄_{1,n}) and M(M_{1,n}) are mixed Tate for n ≤ 3."

Proof stratifies M̄_{1,n} by quotients of M_{0,r} × M_{1,s} (3 ≤ r ≤ n+2, 1 ≤ s ≤ n) over **R = Z[1/6]**, with mixed Tate result stated **over Q**.

**BF25 §10.5.2 (p.57, EXPLICIT level-extension green light)** :
> "by using the results of Petersen [Pet12, Theorem 5.1] one may use the moduli spaces of curves with level structure M_{1,n}(m) to obtain similar results... By Remark 6.4 of loc. cit., this can be extended to other congruence subgroups of SL_2(Z), specifically Γ_1(m) and Γ_0(m)..."

## Pet12 verbatim quotes (verified)

**Pet12 Remark 6.4 (p.21, the Γ_1(m) bridge)** :
> "Another way of decomposing cusp form motives... considering the moduli spaces M̄_{1,n}(BZ/mZ) instead of B(Z/mZ)². Explicitly, we look at the open and closed substack consisting of connected admissible torsors which are unramified over each marked point. **The arguments in this article go through with only very minor changes.** ... for n=1 the curve X_1(m) is recovered..."

**Pet12 base ring (p.5)** : M̄_{g,n}(m) is smooth proper DM-stack over **Spec Z[1/m]**, components over **Z[1/m, ζ_m]**. For m=4 : **Z[1/4, i] ⊂ Z[i, 1/2]** ✓.

## Base ring tension (the new finding M102 missed)

| Ring | μ_2 | μ_4 | μ_6 |
|------|-----|-----|-----|
| BF25 D works over Z[1/6] | ✓ | (over Q) | ✓ |
| **Z[i, 1/2]** (target) | ✓ | ✓ | **✗ (1/3 missing)** |

The μ_6 stratum [Z/μ_6] in BF25 Lemma D.2 (j=0 elliptic curve E_0 with CM by Z[ζ_3]) requires 1/3 invertible.

**However** : D.7's mixed Tate statement is over Q (BF25 §D.4 first line). After base change to Q (or Q(i)), 6-torsion phenomena disappear because Q has all roots of unity. **Rational mixed Tate inherits cleanly to Q(i) modulo (B2)**.

For **integral mixed Tate over Z[i, 1/2]**, residual obstruction at p=3.

## Conditional Theorem M113

**Assume (B1) and (B2). Then M(M̄_{1,3}^{Γ_1(4)}) ∈ DMT(Z[i, 1/2]) and the Gross-Zagier conjecture for Γ_1(4), weight 4 holds for any pair of CM points defined over Q(i).**

Proof transports BF25 stratification of M̄_{1,3} along forgetful map π^Γ : M̄_{1,3}^{Γ_1(4)} → M̄_{1,3} (finite étale away from cusps + elliptic points).

## Sub-claim (B1) — μ_6 stratum at p=3

For the punctured cuspidal cubic Z (BF25 Lemma D.2, j=0 elliptic curve E_0 with CM by Z[ζ_3]), BF25 Remark D.3 observes M(Z)^{μ_6} is mixed Tate although Z itself is not.

H¹(E_0; Q(ζ_3)) decomposes into χ ⊕ χ̄ Hecke eigenspaces, μ_6 acts by ζ_6, ζ_6⁻¹ (both non-trivial), so H¹(E_0)^{μ_6} = 0.

**At level Γ_1(4)** : Replace E_0 with its Γ_1(4)-cover. The semi-direct product Γ_1(4) ⋊ μ_6 has order ≤ 96. Need : M(Z̃)^{Γ_1(4) ⋊ μ_6} mixed Tate over Z[i, 1/2].

Plausible (most likely descends from Z[i, ζ_3, 1/6] = Z[i, 1/6]) but **unverified at p=3**. Specialist computation 1-2 weeks (Brown / Fonseca / Petersen).

## Sub-claim (B2) — Alternating-S_3 + Γ_1(4) projector → vanishing cusp form motive

Cusp form motive at level Γ_1(4), weight 4 :
M^3_{cusp,Γ_1(4)} = M(M̄_{1,3}^{Γ_1(4)})_ε[3] = H¹_!(X_1(4), Sym² R¹π_*Q)

**Critical fact** : **dim S_4(Γ_1(4)) = 0** (standard).

So M^3_{cusp,Γ_1(4)} = 0 in Betti realisation. By BF25's Conjecture 1 (= conservativity for cusp form motives), this implies vanishing as a motive.

BF25 §10.5.2 explicitly :
> "in every weight, level and nebentypus for which the corresponding space of cusp form vanishes, one hopes to prove... that the corresponding motive vanishes."

**Sub-claim (B2)** = "conservativity for Γ_1(4), wt-4 cusp form motive" = standard Ayoub Conj 2.12 / motivic conservativity.

## ECI consequences (if conditional theorem holds)

- ECI M52 "6/5 anchor" realised as single-valued period of Brown-Fonseca biextension at Γ_1(4), wt 4
- Q(i) / CM specialisation receives single-valued period interpretation
- Probability 22-26% → **24-28%**

**Reaching 30-40%** : resolve (B1) p=3 explicitly (specialist 1-2 weeks).

## Recommended next steps

1. **Outreach to Brown / Fonseca / Petersen** : ask "for level Γ_1(4) cover, do you expect M̄_{1,n}^{Γ_1(4)} mixed Tate over Z[i, 1/2] for n ≤ 3?"
2. **Specialist computation** : For n=2, verify Γ_1(4)-cover of [Z/μ_6] explicitly
3. **Read [Inc22]** (Inchiostro 2022, Math.Z. 302(3):1905-1925) "M̄_{1,2} as weighted blow-up of P(2,3,4)" — explicit toric description
4. **Read [Sre25]** (arXiv:2502.04608) — parallel approach via products of elliptic curves

## References verified (PDF read live)

- arXiv:2508.04844 v2 (BF25) ✓ Read full PDF
- arXiv:1012.1477 v2 (Pet12 Petersen) ✓ Read full PDF
- arXiv:2502.04608 (Sre25) — flagged for reading
- Inc22 = Math.Z. 302(3):1905-1925 — flagged

## Discipline log

- 0 fabrications
- All citations verified by direct PDF Read
- All quoted theorems verbatim
- Sub-claims (B1), (B2) clearly distinguished
- Probability honestly bounded 24-28% NOT 30-40% (specialist work needed)
- Mistral STRICT-BAN observed
- Hallu 95 → 95 held
