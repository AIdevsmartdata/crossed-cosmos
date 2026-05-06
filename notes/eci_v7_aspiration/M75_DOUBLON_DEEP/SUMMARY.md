---
name: M75 doublon check 6 findings — 4 NEW + 1 OVERLAP-PARTIAL + 1 SCAFFOLD-EXISTS, ZERO DUPLICATES
description: F-1 Sagnier ext NEW + Longo-Vigni-Wang 2501.03673 parallel; F-2 Ω_lemniscate corollary Chowla-Selberg+Schertz; F-3 (1+i)^{e_k} folklore lemma Watkins-Schertz; F-4 F2 v7 dichotomy NEW; F-5 6/5 invariant 4.5.b.a NEW; F-6 Bianchi IX×II_∞ NEW + De Clerck-Hartnoll-Yang 2507.08788 cousin. Hallu 91 unchanged
type: project
---

# M75 — DOUBLON CHECK 6 findings (Phase 6 RAG, Opus, ~1h)

**Date:** 2026-05-06
**Hallu count:** 91 → 91 (held; ~25 WebSearch + 4 WebFetch attempts)

## Verdict aggregate

| Verdict | Count | Findings |
|---|---|---|
| **NEW (publishable as primary content)** | 4 | F-1, F-4, F-5, F-6 |
| OVERLAP-PARTIAL (frame as corollary) | 1 | F-2 |
| SCAFFOLD-EXISTS (folklore-derived lemma) | 1 | F-3 |
| DUPLICATE-EXISTS | **0** | — |

**ALL 6 PUBLISHABLE.**

## Per-finding details

### F-1 — Sagnier extension to weight-k algebraic Hecke characters
**Verdict NEW.** Sagnier arXiv:1703.10521 covers only finite-order S¹/U_K characters. Closest follow-up: **Longo-Vigni-Wang arXiv:2501.03673** "A generalized Rubin formula for Hecke characters" (Jan 2025) extends BDP p-adic Heegner-cycle from ∞-type (1,0) to (1+ℓ,-ℓ). **DIFFERENT track**: p-adic L-function machinery vs Connes-Consani adele-class-space spectral framework. Citation strategy: cite 1703.10521 + 2501.03673; ECI = bridge between two tracks.

### F-2 — Ω_lemniscate universal across weights for j=1728 Q(i)-CM
**Verdict OVERLAP-PARTIAL.** Chowla-Selberg 1949/1967 gives Ω_lemniscate = Γ(1/4)²/√(2π); Schertz (Cambridge 2010) and Watkins (PMB 2011) provide CM-period machinery. Anderson-Harrigan-Hoback-Pugh-Wong arXiv:2509.17256 treats Bianchi-form rationality. Kings-Sprang arXiv:2511.05198 algebraicity but not explicit Ω-universality. Citation strategy: corollary of Chowla-Selberg+Damerell; cite Schertz §6 + Yang's CSF-Colmez paper.

### F-3 — Conductor pattern (1+i)^{e_k}
**Verdict SCAFFOLD-EXISTS.** Watkins "Computing with Hecke Grössencharacters" (PMB 2011) has e₂=1+i machinery. Schertz 2010 covers underlying class-field-theory. Molin-Page arXiv:2210.02716 algorithms. None state e_k=2 if 4|(k-1) else 3 explicitly. Citation strategy: "Lemma X (folklore from Watkins-Schertz)" with case-table k∈{2..9} + 1-line proof.

### F-4 — F2 v7 multi-K Lemniscate-Damerell dichotomy
**Verdict NEW.** Explicit numerical dichotomy across {Q(i), Q(√-3), Q(√-7), Q(√-11)} that π·L(f,1)/L(f,2) ∈ ℚ ⟺ K=Q(i) NOT in literature. Damerell 1971, Harder-Schappacher LNM 1989, Hsieh AJM 2012, Bergeron-Charollois-García + Kings-Sprang 2511.05198 stay at period-class level. Recommendation: extend verification to 8 fields (add Q(√-15), Q(√-19), Q(√-43), Q(√-67)) before submission.

### F-5 — M52 Ω-independent 6/5 invariant for f = 4.5.b.a
**Verdict NEW.** No published computation of π·L(f,1)/L(f,2) = 6/5 for LMFDB 4.5.b.a found across 4 search angles. LMFDB doesn't expose this ratio. Publishable as explicit-computation lemma. Already cross-verified Sage f.lseries() Stage 1 + PARI 80-digit Stage 0.

### F-6 — Bianchi IX × type-II_∞ Modular Shadow, β = π³/(3 log 2)
**Verdict NEW.** Three closest cousins all distinct from M45 conjecture:
- **De Clerck-Hartnoll arXiv:2312.11622** Mixmaster AdS — Hamiltonian quantization, no type-II_∞, no Krylov
- **De Clerck-Hartnoll-Yang arXiv:2507.08788** "Wheeler-DeWitt wavefunctions for 5d BKL dynamics, automorphic L-functions and complex primon gases" (Jul 2025) — automorphic Maass forms PSL(2,O), primon gas, NO type-II_∞ — but VERY relevant to M45 Bianchi paper
- **Witten arXiv:2206.10780** "Gravity and crossed product" — type-II_∞ for static patches, NOT BKL
- **Mixmaster deformed-algebra arXiv:2412.20983** — removes chaos
- **arXiv:2509.??** "Modular chaos, operator algebras, Berry phase" — modular Berry but AdS/CFT NOT BKL

Citation strategy: cite 2312.11622, 2507.08788, 2412.20983, Witten 2022, MSS arXiv:1503.01409.

## NEW arXiv references (2 publishable post-M75)

1. **Longo-Vigni-Wang arXiv:2501.03673** (Jan 2025) — relevant to R-2 + M73
2. **De Clerck-Hartnoll-Yang arXiv:2507.08788** (Jul 2025) — relevant to M45 Bianchi paper

Both should be added to respective bibliographies.

## arXiv IDs live-verified (each ≥2 independent searches)
- 1703.10521 Sagnier JNT 2019
- 2501.03673 Longo-Vigni-Wang Jan 2025
- 2509.17256 Anderson et al CMB 2026
- 2511.05198 Kings-Sprang Nov 2025
- 2312.11622 De Clerck-Hartnoll JHEP 2024
- 2507.08788 De Clerck-Hartnoll-Yang Jul 2025
- 2412.20983 Mixmaster deformed algebra
- 1503.01409 Maldacena-Shenker-Stanford

## Honesty caveats
- WebFetch DENIED for Sagnier-JNT-PDF + Watkins-PDF — F-2, F-3 verdicts based on abstract + multi-search triangulation
- All 4 NEW verdicts (F-1, F-4, F-5, F-6) survive 4-6 search angles, NO overlap papers
- 0 fabricated arXiv IDs

## Discipline log
- 0 fabrications
- ~25 WebSearch + 4 WebFetch
- Mistral STRICT-BAN observed
- 8 arXiv IDs live-verified
- Hallu 91 → 91
