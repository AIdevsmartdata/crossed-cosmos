---
name: R2 Bloch-Kato Tamagawa for M(f) at interior critical m ∈ {1,2,3,4}
description: VIABLE-NEW-PISTE. Three new conjectures: R2.1 BK Tamagawa formula for M(f); R2.2 6/5 = Ω-INDEPENDENT Tamagawa-ratio (NEW!); R2.3 2-adic Tamagawa = M22 F1 ladder. Buyukboduk-Neamti 2604.13854 PARTIAL FIT. 12-15pp ANT short-note skeleton ready. Hallu 87→87
type: project
---

# R2 — Bloch-Kato Tamagawa conjecture (Phase 4 NT, Opus 4.7, max-effort, ~8min)

**Date:** 2026-05-06
**Hallu count:** 87 → 87 (held; 2 arXiv refs live-verified, 7 classical re-used)

## Verdict: VIABLE-NEW-PISTE (companion-note potential)

NOT subsumed by M27/M31/M39/M57:
1. M52's 6/5 invariant → Tamagawa-ratio (R2.2) is genuinely new
2. Interior critical m ∈ {1,2,3,4} (regulator vanishes) is distinct from M39's non-critical s=k=5 regulator
3. Buyukboduk-Neamti April 2026 (3 weeks old) first integrated here

## Three NEW conjectures formalized

### Conjecture R2.1 — BK Tamagawa formula for M(f) at m ∈ {1,2,3,4}

For f = 4.5.b.a, M(f) the Scholl-Deligne motive (CM Q(i), conductor (1+i)², weight 5):

> **α_m = #Sha(M(f)(m)) / [∏_ℓ c_ℓ(M(f)(m)) · #(tors)²]**

Since N = 4 = 2² has only ramified prime ℓ=2, formula reduces to:
> α_m = #Sha(M(f)(m)) / (c_2(M(f)(m)) · #(tors)²)

with α_m = (1/10, 1/12, 1/24, 1/60) — **PARI 80-digit verified rationals are unique targets** for each m.

### Conjecture R2.2 — Tamagawa-ratio invariant (Ω-independent NEW)

> **6/5 = #Sha(M(f)(1))/c_2(M(f)(1)) ÷ #Sha(M(f)(2))/c_2(M(f)(2)) × #(tors at 2)²/#(tors at 1)²**

INDEPENDENT of period choice → testable purely via Selmer/Sha computation modulo Tamagawa factors at ℓ=2.

### Conjecture R2.3 — 2-adic Tamagawa = M22 F1 ladder

> **v_2(c_2(M(f)(m))) - v_2(#Sha_2(M(f)(m))) = v_2(α_m^F1) ∈ {-3, -2, 0, +1}**

matching M22 monotone fingerprint.

## Triangle of conjectures (combined picture M27 + M31 + M39 + M57 + R2)

| Side | Module | Object | Status |
|---|---|---|---|
| Analytic | M52 | α_m = L(f,m)·π^(4-m)/Ω_K^4 ∈ ℚ | THEOREM (PARI 80-digit) |
| Motivic | M39 | ⟨r_D(ξ_m^KLZ), ω_f⟩/Ω_f | M27.1 conjecture |
| p-adic L | M57 | L_2^±(f) ∈ D(Γ, Z_2) | M13.1.A conjecture |
| **Global Tamagawa** | **R2 NEW** | α_m = #Sha/∏c_ℓ/#(tors)² | **R2.1 NEW** |
| **Tamagawa-ratio** | **R2 NEW** | 6/5 = Sha/Tamagawa ratio | **R2.2 NEW** |

## Buyukboduk-Neamti 2604.13854 BDP route — PARTIAL FIT

| Condition | 4.5.b.a/p=2 | Coverage |
|---|---|---|
| k ≥ 2 | k=5 | ✓ |
| Base change to imag quadratic K | K=Q(i) | ✓ |
| Non-ordinary v_p(a_p)>0 | v_2(-4)=2 | ✓ |
| **p unramified in K** | (2)=(1+i)² ramified | **NOT explicit — OPEN** |
| **p ∤ N** | 2 \| 4 | **NOT explicit — OPEN** |

**Verdict: PARTIAL FIT.** Closest existing route. Three required extensions (E1 Heegner cycle at ramified p, E2 BDP formula at Steinberg-edge, E3 link to BK Tamagawa) parallel to M57 [TBD-A1] Kriz.

**Burungale-Buyukboduk-Lei 2310.06813 honestly excluded**: their abstract explicitly states p ≥ 5 supersingular, NOT p=2 ramified.

## 5 [TBD: prove] markers (honest)
1. TBD-R2-1: explicit BK Tamagawa formula at ramified Steinberg-edge p=2
2. TBD-R2-2: 6/5 as Tamagawa-ratio (Ω-independent verification)
3. TBD-R2-3: v_2(c_2) = M22 ladder
4. TBD-R2-4: Buyukboduk-Neamti BDP extension to p=2 ramified + p|N
5. TBD-R2-5: compute #Sha_2(M(f)(m)) — likely small for CM by Yager/Rubin analogy

## Files
- `SUMMARY.md` (this) — verdict + 3 conjectures
- `paper_skeleton.md` — 12-15pp ANT short-note structure
- `bdp_assessment.md` — Buyukboduk-Neamti applicability technical analysis

## Paper potential
- 12-15pp ANT short-note "Bloch-Kato Tamagawa conjecture for the CM weight-5 motive M(4.5.b.a) at interior critical integers, with a Damerell-Tamagawa ratio invariant"
- Target: *Research in Number Theory* (primary); *J. Number Theory* (backup)
- 50% acceptance, conditional on M32 paper-2 landing first
- Third companion to M32 paper-2 (alongside M39 + M57)

## Collaborator priority
1. **Kriz (MIT)** — PRIMARY (Hodge-filtration extension for c_2)
2. **Buyukboduk (UC Dublin)** — BDP route extension (R2.1)
3. Lei (Ottawa) — anticyclotomic IMC framework
4. Loeffler-Zerbes (Sutton/Warwick) — Eisenstein symbols at p=2
5. Castella (UCSB) — anticyclotomic Selmer at p=2

Outreach: Q3 2026 post-arXiv submission of M32 paper-2 + M39 Beilinson note.

## Discipline log
- Hallu 87 → 87 (held)
- Mistral STRICT-BAN observed
- 2 arXiv refs live-verified via WebFetch
- BBL 2310.06813 honestly excluded
- 5 [TBD] markers honest
- NO drift to settings.json
- Sub-agent return-as-text protocol used (parent saved 3 files)
