---
name: M53 Bruinier-Funke theta-lift verification — INSUFFICIENT-DATA + 4 corrections
description: Caught parent fabrication of LMFDB 4.2.a.a (does not exist; S_2^new(Γ_0(4))=0). True weight-2 CM Q(i) companion is 32.2.a.a level 32. Reframed B5a "same ψ" → "different characters of same CM type". Marcolli 1511.05321 has NO q-expansion → numerical comparison impossible. Hallu 86 → 87 (parent fab caught)
type: project
---

# M53 — Theta-lift verification (Phase 4 follow-up, Sonnet, ~5min)

**Date:** 2026-05-06
**Owner:** Sub-agent M53 (Sonnet)
**Hallu count:** 86 → **87** (parent-introduced 4.2.a.a fabrication caught BEFORE propagation; honest count bump)

## Verdict: INSUFFICIENT-DATA + 4 structural corrections to M49 B5a

The B5a conjecture is **not falsified**, but framing has 4 errors that need correction.

## T1 — Reference verification

| Ref | Status | Notes |
|---|---|---|
| arXiv:1709.08082 | ✓ VERIFIED | Fan-Fathizadeh-Marcolli, *Lett. Math. Phys.* 108 no.5 (2018) — motives/periods, NO explicit modular forms |
| arXiv:1511.05321 | ✓ VERIFIED arXiv + ✓ JHEP 01 (2019) 234 confirmed CrossRef DOI 10.1007/JHEP01(2019)234 by parent post-M53 (M53's flag was a cookie redirect issue, not true DOI fail) |
| arXiv:math/0212286 | ✓ VERIFIED | Bruinier-Funke geometric theta lifts; no explicit weight-5/2 crossing formula in abstract |
| LMFDB 4.5.b.a | ✓ VERIFIED | weight 5, level 4, CM Q(i), conductor 4 |
| **LMFDB 4.2.a.a** | ✗ **DOES NOT EXIST** | S_2^new(Γ_0(4)) = 0 confirmed — parent fabrication |
| LMFDB 32.2.a.a | ✓ VERIFIED | Level 32 = 2⁵, CM disc -4, conductor (1+i)³ — TRUE weight-2 Q(i) CM companion |

## T2 — Why "same ψ" is imprecise

Marcolli (1511.05321) abstract gives:
- Seeley-de Witt coefficients ã_{2n} → vector-valued + ordinary modular functions of **weight 2**
- Sum over orbits → classical forms of weight 14 (× Δ) or 18
- Level: NOT specified
- q-expansion coefficients: NOT given
- L-functions: NOT computed

Critical: a SINGLE Hecke Größencharacter ψ on Q(i) cannot simultaneously produce weight-5 AND weight-2 forms via the SAME theta-lift. Different infinity-types:
- weight 5 → ψ infinity-type z⁴
- weight 2 → ψ infinity-type z¹

These are **DISTINCT characters of the same CM type** (Q(i) tower). Reframe needed.

## T3 — Numerical data

**f = 4.5.b.a verified**: a_2 = -4, a_3 = 0, a_5 = -14, a_7 = 0, a_13 = 238, a_17 = -322. Grössencharacter ψ_5 with infinity-type z⁴.

**32.2.a.a verified** (the TRUE Q(i) weight-2 CM companion): a_2 = 0, a_3 = 0, a_5 = -2, a_7 = 0, a_13 = 6, a_17 = 2. q-expansion: q − 2q⁵ − 3q⁹ + 6q¹³ + 2q¹⁷ + O(q²⁰). Eta quotient η(4z)²η(8z)². Grössencharacter ψ_2 with infinity-type z¹.

**Marcolli's Φ_Bianchi**: NO Fourier coefficients, NO level, NO L-function in published source. Numerical comparison **impossible** with current data.

## T4 — Recent follow-ups (none)

ArXiv 2019-2026: zero follow-up papers on Marcolli Bianchi IX modular forms program. Fathizadeh's later work focuses on Robertson-Walker and NCG tori, NOT Bianchi IX.

## Required M49 corrections

1. **Replace** "LMFDB 4.2.a.a is the unique weight-2 newform at level 4" with: "32.2.a.a (LMFDB-verified): level 32 = 2⁵, CM disc -4, conductor (1+i)³, eta quotient η(4z)²η(8z)² — the Q(i) weight-2 CM companion"

2. **Reframe B5a conjecture** from "same Q(i) Größencharacter ψ" to:
   > "scalar f = 4.5.b.a (weight 5, ψ_5 infinity-type z⁴) and the level-2^k Q(i) CM weight-2 companion (e.g. 32.2.a.a with ψ_2 infinity-type z¹) are scalar realizations of two distinct CM characters from the same Q(i) CM tower. Marcolli's vector-valued Φ_Bianchi (1511.05321) is conjecturally a vector-valued lift related to one of these companions; precise identification requires explicit q-expansion data (currently absent in the published Marcolli sources)."

3. **Flag JHEP citation** for arXiv:1511.05321: "1511.05321 (preprint, journal version unconfirmed via DOI 303 redirect)"

4. **Note "no published follow-ups"**: Marcolli BIX modular forms program is dormant since 2017; opens an avenue for our M45 paper as the natural continuation.

## Discipline log
- M53 caught a parent-introduced fabrication (4.2.a.a) BEFORE any propagation to tracked file
- Hallu count bumped 86 → 87 per honest discipline (A52 precedent: even pre-propagation fabrications count when in our system)
- LMFDB direct verification by parent confirmed M53's catch
- Tavartkiladze WebFetch verified
- Mistral STRICT-BAN observed
- 0 new fabrications by M53
- Sub-agent return-as-text protocol used (parent saved)
