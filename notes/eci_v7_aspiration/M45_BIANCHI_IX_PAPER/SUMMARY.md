---
name: M45 — Bianchi IX × type-II_∞ Modular Shadow paper draft
description: Conjecture-paper draft v0.1 (12pp, Comm. Math. Phys.) per M42 S1 VIABLE-NEW-PISTE. λ_K^mod ≤ 2π × π²/(6 log 2) = π³/(3 log 2) ≈ 14.907. 14 refs verified. 6 [TBD: prove]. Hallu 86→86
type: project
---

# M45 — Bianchi IX Modular Shadow paper (Phase 3.G #1, Opus, ~8min)

**Date:** 2026-05-06
**Owner:** Sub-agent M45 (Opus 4.7, max-effort math-physics)
**Hallu count:** 86 → 86 (held; 14 arXiv WebFetch-verified, 0 fabrication, 6+ false-positive guesses caught & discarded)
**Status:** DRAFT v0.1 complete, NOT submission-ready (6 [TBD: prove] markers explicit)

## Files

| File | Purpose | Status |
|---|---|---|
| `bianchi_ix_modular_shadow.tex` | Main 12pp draft, Comm. Math. Phys. target | DRAFT v0.1 written (~470 lines) |
| `SUMMARY.md` | This file | parent saved |
| `falsifier_protocol.md` | Numerical falsifier (compute λ_BKL, verify Krylov rate) | parent saved |
| `outreach_strategy.md` | Marcolli + Speranza email drafts | parent saved (DO NOT SEND until W3) |

## Key conjecture (M45.1)

For Bianchi IX vacuum spacetime in BKL/Mixmaster phase, wedge-complement observer algebra A_obs admits type-II_∞ representation (Speranza 2025 crossed product), with modular flow rate
> **λ_mod = 2π × λ_BKL**

where **λ_BKL = h_KS(σ_Gauss) = π²/(6 log 2) ≈ 2.3731** is the Kolmogorov-Sinai entropy of the Manin-Marcolli (2015) Gauss-shift symbolic dynamics.

This identifies a Maldacena-Shenker-Stanford-style Krylov complexity bound:
> **C_K^mod(s) ≤ A · cosh(2π × λ_BKL × s)**, ceiling 2π × λ_BKL = π³/(3 log 2) ≈ **14.907**

Predicted intrinsic Hawking-like inverse temperature: **β_eff = 12 log 2 / π ≈ 2.6479**

## 14 verified arXiv refs (WebFetch 2026-05-06)

| ID | Authors | Used in |
|---|---|---|
| 1503.01409 | Maldacena-Shenker-Stanford | §1, §5 |
| 1812.08657 | Parker-Cao-Avdoshkin-Scaffidi-Altman | §5 |
| 1504.04005 | Manin-Marcolli (BKL ↔ X(2)) | §2, §4 |
| 1511.05321 | Fan-Fathizadeh-Marcolli | §2, §6 |
| 2112.12828 | Witten (Gravity & crossed product) | §2, §4 |
| 2406.01669 | Kudler-Flam-Leutheusser-Satishchandran (FLRW obs algebra) | §4 |
| 2504.07630 | Speranza (intrinsic cosmological observer) | §2, §4 |
| 2306.14732 | Caputa-Magán-Patramanis-Tonni | §5 |
| 2206.10780 | Chandrasekaran-Longo-Penington-Witten | §2, §4 |
| gr-qc/9612066 | Cornish-Levin (Mixmaster Farey Tale) | §2, §7 |
| 0901.0806 | Heinzle-Uggla (BIX attractor theorem) | §1, §6 |
| 1803.04993 | Witten (entanglement QFT notes) | §2 |
| hep-th/0212256 | Damour-Henneaux-Nicolai (Cosmological Billiards) | §2 |
| 2203.03534 | Bhattacharjee-Cao-Nandy-Pathak (counter-example) | §5 |

False-positive arXiv IDs caught and discarded: 2208.07845, gr-qc/9405015, 2301.04146, 0907.0540, 0908.0563, 0712.1995, 2110.05683, 2212.14593, 2206.00027.

## 6 [TBD: prove] markers (honest)

| Marker | Section | What needs proof |
|---|---|---|
| TBD-1 | §4.1 | Wedge algebra A_obs is type-III_1 (no global boost Killing on BIX) |
| TBD-2 | §4.2 | Speranza 2025 crossed-product transfers to Misner volume τ |
| TBD-3 | §4.3 | Modular automorphism σ_t = MM geodesic flow on X(2) (up to inner aut) |
| TBD-4 | §4.4 | Bisognano-Wichmann β=2π normalisation in Bianchi IX |
| TBD-5 | §5 | Linear Lanczos slope α = π λ_BKL transposition |
| TBD-6 | §5 | von Neumann coupling proportionality constant |

## Risk profile

- Step A (§4.1, Gauss-AWCH ↔ III_1): MEDIUM
- Step B (§4.2, Speranza transfer): MEDIUM-HIGH (no global Misner time)
- Step C (§4.3, flow id): MEDIUM-HIGH
- Step D (§4.4-5, MSS bound): HIGH (physics-style conjecture)

## Cross-relation to portfolio

- Paper #4 (Modular Shadow LMP v2.5, 19pp): this is the **Bianchi-IX-anisotropic generalization**
- Paper #5 (AWCH Bianchi IX Lemma A.1): natural **operator-algebra companion**
- M28 RH closure stands: gravity II_∞ ≠ spectral II_∞
- M32 paper-2 (CKM): orthogonal sector

## Next steps

- W1-W2: §4.1 detail (Gauss-AWCH identification rigorous)
- W3: Marcolli outreach (email gated by §4.1 detail + F1 numerics)
- W4: Speranza outreach + cross-check transfer to Misner τ
- W5-W6: F2 Bianchi IX WDW Krylov rate numerical (RTX 5060 Ti, 2-6h)

Submission target: **Comm. Math. Phys.** Note (12pp), or *Annales Henri Poincaré*.

## Discipline log
- 0 fabrications; Mistral STRICT-BAN; NO drift to settings.json
- 14 refs WebFetch-verified; ≥6 false-positives discarded
- All [TBD: prove] markers explicit
- Compile not attempted by sub-agent (Bash blocked); parent will verify
