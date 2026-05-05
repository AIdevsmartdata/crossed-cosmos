---
name: A78 H6 χ_4 nebentypus relaxation stress-test
description: Stress-test of H6 linchpin via χ_3, χ_5, χ_7, χ_8, χ_11, χ_12, χ_15, χ_24 alternatives — H6 ROBUSTE by elimination across 3 independent structural filters
type: project
---

# A78 — H6 χ_4 nebentypus relaxation stress-test

**Date:** 2026-05-05 night (Wave 12 Phase 1)
**Owner:** Sonnet sub-agent
**Hallu count entering / leaving:** 85 / 85 (held; 0 fabricated bibdata; LMFDB live-fetched)

## Verdict
**H6 ROBUSTE par élimination** (closer to ROBUSTE than PRIVILEGED, with one honest caveat).

H6 = `{T(p) : p ≡ 1 mod 4}` via χ_4 nebentypus → K=Q(i), 4.5.b.a, τ=i — is the **ONLY** relaxation candidate among {χ_3, χ_4, χ_5, χ_7, χ_8, χ_11, χ_12, χ_15, χ_24} that simultaneously clears all three load-bearing structural filters.

## 3 filtres indépendants
| Filtre | Méthode | Élimine |
|---|---|---|
| **T1 Damerell ladder** | A5 mp.dps=60 PSLQ : α_2=1/12 only at K=Q(i) ; ailleurs Bernoulli-Hurwitz K-spécifiques (64/35, 9/5, 18/11, 4/5) | tous sauf Q(i) |
| **T2 SL(2,Z) elliptic-fixed-point** (sympy-vérifié, **universel anchor-indép**) | Exactement 2 orbits {i, ω} ; aucun χ_d pour d ∈ {2,5,6,7,11,15,...} produit SL(2,Z)-elliptic | χ_5, χ_7, χ_8, χ_11, χ_15, χ_24 |
| **T3 DKLL19 CSD(1+√6) alignment** (A14) | Y_3^(2)(τ=i) = (1, 1+√6, 1-√6) ; Y_3^(2)(τ=ω) = (0,1,0) collapse | τ=ω → King 2022 2-RH-ν seesaw refuté |

**5/5 sympy tests pass; assertion `arithmetic_pass == ['chi_4']` holds.**

## Counterfactual : si H6 ARBITRAIRE quelle alt prévaut ?
**χ_3 / Q(√-3) at τ=ω** est le SEUL "second-place" :
- ✅ Clear T2 (KW dS-trap admits τ=ω)
- ❌ FAILS T1 (α_2 = √3/45 ≠ 1/12)
- ❌ FAILS T3 (Y_3^(2)(ω) collapse, NPP20 sin²θ_13 = 1/2 vs PDG-2024 0.0220 → **>>5σ refuted**)

Même en counterfactual, χ_3 perd décisivement sur lepton cross-check.

## Impact sur 5 papers SUBMISSION-READY si linchpin tombe
**Dans le monde réel H6-ROBUSTE : ZÉRO impact.**

Counterfactual H6-ARBITRAIRE (si χ_3 avait passé) :
| Paper | Impact |
|---|---|
| P-NT BLMS | Mineure — abstract amendment ("HH = {T(p):p≡1 mod 4} one of multiple Hecke restrictions") |
| v7.4 LMP | **Substantial rewrite** — CM-anchor framing change "τ=i" → "τ ∈ {i, ω}" |
| ER=EPR LMP | **Unaffected** (operator-algebra, not modular-flavour) |
| Modular Shadow LMP | Substantial revision (parallel τ=ω construction needed) |
| Cardy LMP | Claim weakens "thin coincidence" → "thinner-than-thin"; formal statement still true |

**Aucune retraction outright dans aucun monde.**

## v7.5 §3 H6 wording proposal
Replace "ESTABLISHED" tag with:
> "**PRIVILEGED-BY-CONVERGENCE**; verified to p ≤ 113 directly + cross-χ relaxation rejected (A78)"

Honest framing : H6 wins by **elimination via 3 independently motivated structural constraints**, NOT by a single closed theorem.

## Caveats résiduels (load-bearing)
- **T1 partial circularity** : α_1 = 1/10 IS the K=Q(i) normalisation (Hurwitz). "α_2 = 1/12 only at Q(i)" is Hurwitz-relative, NOT absolute. (Already flagged in A5.)
- **T2 universel** : SL(2,Z) elliptic classification IS anchor-independent — c'est le genuine non-tautologique filter qui kills 6 χ_d.
- **T3 NPP20 fit at τ=ω** : run as cross-product-of-alignment-vectors PROXY, not full NPP20 code ; collapse qualitatif unambiguous, exact χ² deferred.
- **χ_5, χ_15, χ_24** : h(K) > 1, A5 Hurwitz anchor not extended ; T2 makes T1 status moot for them.
- **LMFDB rate-limited** sur 11.5.b.a et char_order=4 search this round ; non-blocking.

## Files (agent wrote)
- `sympy_test.py` (reproducible, 5/5 tests pass)
- `alternative_chains_table.md` (χ_3...χ_24 master table avec K, LMFDB label, τ_S, α_2, DKLL19 alignment, lepton verdict)

## Discipline log
- 0 fabrications introduced
- LMFDB live-fetched 4 newform pages + 1 search
- A5/A14/A47 references already upstream-verified
- Mistral NOT used
