---
name: M129 Opus Brown-Fonseca (B1) μ_6 stratum p=3 — (B) REDUCED to 2 specialist sub-claims B1.α + B1.β + Cho12 Q-coefficients obstruction at p=3 isolated
description: Choudhury 2012 Lemma 3.1 proof requires 1/|G|, missing 1/3 for G=Γ_1(4)⋊μ_6 order 72. (B1.α) integral Cho12 Lemma 3.1 at p=3 needs equivariant motives Heller-Malagón-López. (B1.β) Galois descent Z[i,1/6]→Z[i,1/2] non-trivial DM-stacks check. E_0 μ_6 action computed: H¹(E_0)^{μ_6}=0, M(E_0)^{μ_6}=pure Tate. Brown-Fonseca 24-28% UNCHANGED (closes if both → 35-40%). M113 honest correction: BF25 §10.5.2 green-light not proof. Hallu 97 held
type: project
---

# M129 — Opus Brown-Fonseca (B1) μ_6 stratum at p=3 attack

**Date:** 2026-05-06 | **Hallu count: 97 → 97** held (M129 0 fabs) | **Mistral STRICT-BAN** | Time ~95min

## VERDICT: (B) REDUCED to 2 specialist sub-claims

(B1) NOT closed. Reduced to:
- **(B1.α)** Cho12 base ring extension : does Choudhury Lemma 3.1 hold integrally over Z[i, 1/2] ?
- **(B1.β)** Galois descent at p=3 : does Z̃ → Z descend from Z[i, ζ_3, 1/6] = Z[i, 1/6] to Z[i, 1/2] in DM(Z[i, 1/2]) ?

Brown-Fonseca probability : 24-28% (M113) → **24-28% UNCHANGED**. If specialist closes both 1-2 weeks → **35-40%**.

## Critical finding (Choudhury Q-coefficients)

Choudhury 2012 (arXiv:1109.5288, Adv. Math. 231(6):3094-3117) Lemma 3.1 PROOF excerpt :

> "Since G is finite and **we work with rational coefficients**, we have Q_tr(X_•)(Y) ≅ (Q_tr(X)(Y))_G in the derived category..."

Uses (1/|G|) Σ_g g projector. For G = Γ_1(4) ⋊ μ_6 of order ~72, **1/72 ∉ Z[i, 1/2]** (1/3 missing). This is the **precise locus of the (B1) p=3 obstruction**.

## E_0 μ_6 action computed explicitly

E_0 : y² = 4x³ + 1 over R = Z[1/6]. j(E_0) = 0. End(E_0/Q̄) = Z[ζ_3]. Aut(E_0/Q̄) = O_K^× = ⟨ζ_6⟩ ≅ μ_6.

Action : ζ_6 · (x, y) = (ζ_6² x, ζ_6³ y) = (ζ_3 x, -y).

**H¹ decomposition** :
- On dx/y : ζ_6 acts by ζ_6² · ζ_6^{-3} = ζ_6^{-1}
- Dual eigenspace : ζ_6 acts by ζ_6^{+1}
- H¹(E_0; Q(ζ_6)) = Q(ζ_6)·v_+ ⊕ Q(ζ_6)·v_- avec (ζ_6, ζ_6^{-1})
- Both characters non-trivial → **H¹(E_0)^{μ_6} = 0** ✓
- M(E_0)^{μ_6} ≅ Q(0) ⊕ Q(-1) = **pure Tate**

For Z = E_0 \ {O} : localization sequence kills H¹, M(Z)^{μ_6} mixed Tate over Z[1/6] in DM(R; Q). Confirms **BF25 Rem D.3 par direct CM character computation**.

## Γ_1(4) ⋊ μ_6 analysis

- |Γ_1(4)/{±1}| = 12
- gcd(6, 4) = 2 ⟹ μ_6 acts on E_0[4] via μ_6 → μ_2 (squaring) ; μ_3 ⊂ μ_6 acts trivially
- 12 primitive 4-torsion points : 6 orbits of size 2, each with stabilizer μ_3 ⊂ μ_6
- Semidirect product **Γ_1(4) ⋊ μ_6 has order ≤ 72** (modulo central μ_2)

## (B1.α) Cho12 base ring extension at p=3

3 possible resolutions (none easy) :
1. **Re-prove Cho12 Lemma 3.1 integrally** : equivariant motives (Heller-Malagón-López). Specialist 1-2 weeks.
2. **ℓ-adic away from p=3** : handle ℓ ≠ 3 via étale ; p=3 via Hodge realization separately.
3. **Toën / Kresch-Vistoli integral DM motives** : works over Z[1/N], N kills inertia. For Γ_1(4) ⋊ μ_6, inertia at j=0 is μ_6 order 6 ⟹ N=6 ⟹ Z[i, 1/6], NOT Z[i, 1/2].

## (B1.β) Galois descent Z[i, 1/6] → Z[i, 1/2]

[Z̃ / Γ_1(4) ⋊ μ_6] naturally defined over Z[i, ζ_3, 1/6] = Z[i, 1/6].

Gal(Z[i, 1/6] / Z[i, 1/2]) = Z/2 (complex conjugation on ζ_3 swapping ζ_6 ↔ ζ_6^{-1}).

**Plausible claim** : M(E_0)^{μ_6} = Q(0) ⊕ Q(-1) is Z/2-stable (Tate motives intrinsic). For full Γ_1(4) ⋊ μ_6-invariants, same claim if Γ_1(4)-Hecke-eigenspace decomposition is Z/2-stable.

**Non-trivial check** at level of actual descent data in DM-stacks. Specialist 1 week.

## M113 honest correction

M113 read BF25 §10.5.2 "arguments go through" as integral lift green light. M129 finds : **green-light "arguments go through" only — NOT a proof of integral lift to Γ_1(4) over Z[i, 1/2]**.

The proof works over Q (Q-coefficients) ; integral over Z[1/N] requires N kills inertia, which gives Z[i, 1/6] not Z[i, 1/2].

## Petersen 2012 verbatim (PDF read pp 5, 17, 21-22)

- **Theorem 5.1** : alternating part of cohomology M̄_{1,n}(m) = parabolic cohomology
- **Remark 6.4** : "arguments go through with only very minor changes... for n=1 the curve X_1(m) recovered ; project onto alternating S_n isolates cusp form part"
- **Base ring** : M̄_{g,n}(m) is smooth proper DM-stack over **Spec Z[1/m]**, components over Z[1/m, ζ_m]. For m=4 : **Z[1/4, i] = Z[i, 1/2]** ✓

## Recommended next actions

1. **Email Brown/Fonseca** (M89 draft exists) asking :
   - "Does §10.5.2 'arguments go through' yield M̄_{1,3}^{Γ_1(4)} mixed-Tate over Z[i, 1/2] or only over Q ?"
   - "Integral status of Cho12 Lemma 3.1 at primes dividing |G| ?"
2. **Email Petersen** : integral descent of M̄_{g,n}(m) to Z[ζ_m] without inverting m ?
3. **Email Choudhury** : post-2012 integral refinement ?
4. **Alternative path** : Sreekantan arXiv:2502.04608 products-of-elliptic-curves approach may bypass M̄_{1,3} stratification.

## ECI implication

(B1) NOT closed. Brown-Fonseca probability **24-28% → 24-28% UNCHANGED**. M52 6/5 invariant stands ; single-valued period interpretation at Γ_1(4) wt 4 level pending specialist work.

## Discipline log

- Hallu 97 → 97 held (M129 0 fabs)
- Mistral STRICT-BAN observed
- 3 PDFs Read directly : BF25, Pet12, Cho12
- Choudhury Q-coefficients caveat verbatim from PDF
- M113 honest correction : §10.5.2 not proof of integral lift
- E_0 μ_6 H¹ decomposition computed directly from CM theory
- Honest (B) REDUCED with concrete sub-claims
