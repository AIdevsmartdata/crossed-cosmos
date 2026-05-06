---
name: M48 doublon check — 5 ECI results vs 2024-2026 arXiv state-of-art
description: Aucun duplicate. R1 Bianchi II_∞ et R5 B-ratio = OVERLAP-PARTIAL (citer cousins). R2 GAP-CONFIRMED. R3 + R4 NEW. 18 arXiv refs WebFetch-verified. Hallu 86 unchanged
type: project
---

# M48 — State-of-art doublon check (Phase 4 prep, Opus, ~15min)

**Date:** 2026-05-06
**Owner:** Sub-agent M48 (Opus 4.7, max-effort literature scout, ~15min)
**Hallu count:** 86 → 86 (no fab; 18 refs WebFetch-verified)

## Verdict table

| # | ECI Result | Verdict | Cousin (verified) |
|---|---|---|---|
| **R1** | Bianchi IX × II_∞ Modular Shadow + Krylov bound, λ_BKL = π²/(6 log 2) | **NEW** + **OVERLAP-PARTIAL** | Hartnoll-De Clerck-Santos arXiv:2312.11622 (JHEP07(2024)202) — Γ(2) arithmetic chaos AdS Mixmaster interior, BUT no type-II_∞ crossed product, NO Krylov bound, NO our specific λ_BKL |
| **R2** | F5 falsifier: anticycl IMC frameworks all exclude p=2 ramified k odd | **GAP-CONFIRMED** | 5 frameworks (Sano 2510.01601, Longo-Pati-Vigni 2603.22483, Lee 2508.05861, Isik 2412.10980, 2503.00247) ALL exclude our case |
| **R3** | Damerell ladder (1/10, 1/12, 1/24, 1/60) for f=4.5.b.a m∈{1,2,3,4} | **NEW-COMPUTATION** of classical theory | LMFDB tabule L(5/2) ≈ 0.5200 only; Kings-Sprang arXiv:2511.05198, 2406.06148 prove general algebraicity but NO explicit ladder for 4.5.b.a |
| **R4** | Meta-conjecture M44.1: ECI scope (Q(d=1,3) class h=1, N=p² ramified, k odd, ψ ∞-type (k-1, 0)) | **NEW** | No "uniqueness theorem CM newform Q(i) weight 5" in 2024-2026 lit |
| **R5** | proton decay B = 1.077 vanilla S'_4 SU(5) at τ=i, κ_u-INDEPENDENT | **NEW-PARAMETER-FREE** + **OVERLAP-PARTIAL** | arXiv:2503.12594 Nonholomorphic A_4 SU(5) (JHEP Jan 2026): A_4 NOT S'_4, no τ=i, no e+π⁰/K+ν̄ ratio. King-Zhou 2103.02633, Varzielas-Paiva 2604.01422 not equivalent. |

## Submit-readiness assessment

| Paper | Status |
|---|---|
| P-NT BLMS | **READY** (+R2 footnote citing Sano/Lee/Isik/LPV/2503.00247) |
| v7.4 LMP | **READY** (+R3 cite Kings-Sprang 2511.05198, 2406.06148) |
| ER=EPR LMP | **READY** (independent of these 5 results) |
| Modular Shadow LMP | **READY** (+R1 cite Hartnoll 2312.11622 prominently, +Speranza, +Requardt, +note 2511.17711 Krylov FRW only) |
| Cardy LMP | **READY** (independent) |
| Proton-decay PRD | **READY** (+R5 cite 2503.12594 framework-level distinction) |
| Bianchi IX (M45) | **READY** (+R1 prominent Hartnoll citation in §1) |
| Leptogenesis CSD LMP | **READY** (independent) |
| Cassini PRD | **READY** (independent) |

## Required citation additions

### Modular Shadow LMP v2.5 §1 + §6
> "*Note*: arithmetic-chaos approach to AdS black-hole interior via the Γ(2) modular surface has been pursued by Hartnoll, De Clerck, and Santos [JHEP 07 (2024) 202, arXiv:2312.11622]. Their work establishes the same arithmetic substrate (BKL ↔ Gauss shift) but does not employ type-II_∞ crossed-product algebras nor compute Krylov-complexity bounds; our framework completes that quantum-information dimension."

### M45 Bianchi IX paper §1
> "Hartnoll-De Clerck-Santos (2024) studied AdS Mixmaster chaos via Γ(2) arithmetic substrate (arXiv:2312.11622), focusing on Hamiltonian quantization eigenvalues. Our framework provides the natural type-II_∞ + Krylov-complexity completion of that program."

### v7.4 LMP §6 / paper-2 §6 Outlook (M28 replacement paragraph extension)
Add citations:
- Sano arXiv:2510.01601 (Tamagawa anticyclotomic, p split k even)
- Lee arXiv:2508.05861 (CM Euler systems, odd p ordinary)
- Isik arXiv:2412.10980 (Hecke chars ordinary primes)
- Longo-Pati-Vigni arXiv:2603.22483 (anticyclotomic IMC, odd p ordinary even k≥4)
- arXiv:2503.00247 (congruent modular forms anticyclotomic)

### Proton-decay PRD §6 Discussion
> "Among contemporary modular-flavor SU(5) frameworks, the closest is the Nonholomorphic A_4 SU(5) construction of arXiv:2503.12594 (JHEP Jan 2026). However, that work uses A_4 (not S'_4) and does not evaluate the proton-decay ratio at the modular fixed point τ=i; the κ_u-INDEPENDENT prediction B = f^{uu}(τ=i)/f^{uc}(τ=i) = 1.077 is therefore specific to the present S'_4 framework."

## Discipline log
- 0 fabrications
- 18 arXiv refs WebFetch-verified
- Mistral STRICT-BAN observed
- ~15min sub-agent runtime
- Sub-agent return-as-text protocol used (parent saved)
- Cross-check vs M27/M28/M37/M39/M40/M42/M44 closures: no conflicts

## Honesty
**No result is a duplicate**. Two are OVERLAP-PARTIAL at framework/substrate level only:
- R1: arithmetic substrate (Γ(2) modular surface ↔ Mixmaster) shared with Hartnoll, but operator-algebra completion specific to ECI
- R5: modular flavor + SU(5) general framework shared with arXiv:2503.12594, but specific group (S'_4 vs A_4) and evaluation point (τ=i vs none) differ

Two GAP-CONFIRMED:
- R2: F5 falsifier verdict matches recent literature thoroughly

Two NEW:
- R3: explicit Damerell ladder rationals (LMFDB has L(5/2) only)
- R4: Meta-conjecture M44.1 scope statement
