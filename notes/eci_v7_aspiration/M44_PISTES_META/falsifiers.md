---
name: M44 falsifier protocols — explicit CPU-hr triggers for 7 standing conjectures
description: F2 (5 CPU-hr) + F5 (20 CPU-hr) cheapest decisive falsifiers; can run within 1 week. Persisted by parent per M44 recommendation
type: project
---

# M44 — Falsifier protocols for 7 standing ECI conjectures

**Date:** 2026-05-06
**Source:** Sub-agent M44 Opus, Phase 3.G #3
**Discipline:** All protocols are EXPLICIT (computational/observational), with SUCCESS CRITERIA stated. No vague "test prediction X" phrasing.

## F2 — M13.1(c) F1 monotone v_2 (EXECUTED 2026-05-06: PASS)

**EXECUTED VERDICT (M47 Pipeline A v3, PARI/GP, 2026-05-06 14:08 CEST):**
- Anchor 4.5.b.a v_2(α_m^F1) = **{-3, -2, 0, +1} EXACTLY** confirmed via PARI mfinit + lfunmf
- Damerell ladder (1/10, 1/12, 1/24, 1/60) empirically verified — H7-A POSITIVE primary now confirmed
- Q(ω) CM (27.5.b.a): pattern DIVERGES — M44.1(a) Q(i)-specificity SURVIVES
- Level mixed-primes (100.5.b.a): pattern DIVERGES — M44.1(b) N=p² simply-ramified STRENGTHENED
- See F2v3_RESULTS.md in M47_PC_PIPELINES/pipeline_a/ for full table



**Conjecture under test**: F1-renormalised v_2(α_m^F1) = {-3,-2,0,+1} pattern is Steinberg-edge specific (only fires for a_{p²}=±p^((k-1)/2)).

**Protocol**:
1. LMFDB sweep — find any non-Steinberg CM weight-5 newform (e.g. Q(√-3) levels 9, 12 if listed in LMFDB CMF database)
2. Compute α_m^F1 = α_m · (-2^{m-1}) · (1+2^{m-3}) for m ∈ {1,2,3,4} via SageMath
3. Check v_2 monotone? (i.e. {-3,-2,0,+1}-style pattern)

**Falsifying outcome**: Monotone v_2 in non-Steinberg case ⇒ F1 not Steinberg-specific (broadens framework, weakens uniqueness claim of M22).

**Cost**: 5 CPU-hr SageMath / LMFDB. Local laptop.

## F5 — M28 anticyclotomic IMC paragraph (CHEAP: 20 CPU-hr) — **EXECUTED 2026-05-06: FALSIFIED**

**Conjecture under test**: M28 anticyclotomic IMC paragraph for f=4.5.b.a is logically valid (not just speculation).

**Protocol**:
1. Re-read Hsieh 2014 ***Documenta Math.*** vol. 19, 709-767 (NOT Compositio — original F5 metadata was wrong; M46 corrected) hypothesis list
2. Re-read Chida-Hsieh 2015 *Compositio* 151, 863-897 hypothesis list (arXiv:1304.3311)
3. Re-read Arnold 2007 *Crelle* 606, 41-78 hypothesis list
4. Re-read Pollack-Weston 2011 hypothesis list
5. If any explicitly excludes p ramified in K AND/OR k odd AND/OR supersingular: paragraph vacuous

**EXECUTED VERDICT (M46 sub-agent, 2026-05-06): FALSIFIED**
- Hsieh 2014 Theorem 1.3: *"p unramified in F/Q"* → EXCLUDES our p=2 ramified
- Chida-Hsieh 2015 Assumption 1.1(2)(3): p ordinary + p > k+1 → EXCLUDES p=2 (supersingular, p<k+1=6)
- Arnold 2007: p split in K + even weight → DOUBLE EXCLUSION (p=2 ramified, k=5 odd)
- Pollack-Weston 2011: N = N⁺N⁻ split/inert split, NO ramified slot → EXCLUDES N=4=2² ramified
- Kriz 2021: p-adic L-functions OK in supersingular ramified, but IMC theorem NOT established

**Outcome**: M28 paragraph replaced with honest [TBD: prove] framing requiring Kriz-style IMC extension. WIN for epistemic discipline.

**Cost**: 20 CPU-hr equivalent (~5min Opus M46 in practice). No actual compute, pure book triangulation.

## F1 — M13.1(a) FE-symmetric interpolation (50 CPU-hr)

**Conjecture under test**: L_2^±(f) is interpolation of (α_m + α_{k-m})/2 along anticyclotomic Z_2 tower for m ∈ {1,2,3,4} on Q(i).

**Protocol**:
1. Compute ∫_Γ χ_m dL_2^± via Bertolini-Darmon Heegner 2-adic distributions
2. Check if values match (α_m + α_{k-m})/2 within 2-adic precision 2^{-20}
3. m ∈ {1,2,3,4}; Γ = anticyclotomic Z_2 tower

**Falsifying outcome**: Discrepancy with v_2 ≥ 0 ⇒ FE-symmetrisation ansatz wrong; M13.1(a) needs reformulation.

**Cost**: 50 CPU-hr SageMath BD-machinery.

## F6 — M22 F1 v_2 ladder fingerprint (100 CPU-hr)

**Conjecture under test**: F1 v_2 = {-3,-2,0,+1} is the SCOPE fingerprint of M44.1 (necessary AND sufficient).

**Protocol**:
1. Run F1 across 50 small CM newforms in LMFDB
2. Tabulate v_2 patterns
3. Check if any non-(K=Q(i), N=p², k odd) case shows monotone v_2

**Falsifying outcome**: Any positive hit ⇒ M44.1 fingerprint claim weakens (broadens scope).

**Cost**: 100 CPU-hr SageMath sweep.

## F3 — M13.1(d) θ-critical Bellaïche-Stevens (200 CPU-hr)

**Conjecture under test**: f=4.5.b.a sits on θ-critical locus per BS arXiv:2403.16076.

**Protocol**:
1. Compute eigencurve slope at (4.5.b.a, p=2) via overconvergent modular symbols (Pollack-Stevens code)
2. Check if (4.5.b.a) sits on θ-critical locus per BS arXiv:2403.16076

**Falsifying outcome**: Off θ-critical locus ⇒ M13.1(d) speculation wrong.

**Cost**: 200 CPU-hr Pollack-Stevens.

## F4 — M27.1 KLZ Beilinson regulator (1000 CPU-hr — EXPENSIVE)

**Conjecture under test**: v_2(⟨r_D(ξ_m^KLZ), ω_f⟩_BDS / Ω_f) = v_2(α_m^ren) for m ∈ {1,2,3,4}.

**Protocol**:
1. Compute r_D(ξ_m^KLZ) / Ω_f via Brunault-Mellit motivic cohomology code
2. SageMath modular-symbols + KLZ §7.1 explicit reciprocity
3. Compare 2-adic valuations

**Falsifying outcome**: v_2(regulator) ≠ {-3,-2,0,+1} ⇒ M27.1 wrong.

**Cost**: 1000 CPU-hr — needs cluster or vast.ai. DEFER until F2 + F5 results in.

## F8 — ECI v7.4 lepton sector neutrino ordering at τ=i (50 CPU-hr) — NEW (M49 B5b)

**Conjecture under test**: ECI's lepton sector at τ=i implies a specific neutrino mass ordering.

**Protocol**:
1. SageMath compute the lepton sector mass matrix from ECI v7.4 modular forms at τ=i
2. Diagonalize and extract neutrino mass ordering
3. Compare with Tavartkiladze 2025 (arXiv:2512.24804) prediction: **inverted ordering at minimal Γ_2≃S_3 fixed-point τ=i**

**Falsifying outcome**:
- ECI v7.4 lepton predicts **inverted** ordering: independent corroboration with Tavartkiladze 2025 → strengthens v7.6 §10 unification claim
- ECI v7.4 lepton predicts **normal** ordering: tension with Tavartkiladze; ECI two-τ scheme is at a different fixed-point sub-class OR lepton sector needs revision

**Cost**: 50 CPU-hr SageMath modular-form package. Full local on PC (20 cores).

## F7 — H8' Cassini-wall ξ_χ KSTD26 (OBSERVATIONAL — FREE)

**Conjecture under test**: KSTD26 wall predicts Δγ < 5e-6 at PPN level; ξ_χ rail is consistent.

**Protocol**:
1. Wait for BepiColombo 2026+ PPN γ measurement
2. Compare measured Δγ vs predicted < 5e-6

**Falsifying outcome**: Δγ outside wall band (> 5e-5) ⇒ H8' postulate falsified.

**Cost**: observational ~free. Passive monitoring 2026-2027.

## Cheapest decisive battery (1 week local)

**F2 + F5** = 25 CPU-hr total. Decisive on M13.1(c) Steinberg-specificity AND M28 anticyclotomic paragraph viability.

Recommended sequence:
1. F5 first (book reading, no compute, 20 CPU-hr) — gates M28 paragraph viability
2. F2 second (LMFDB sweep + SageMath, 5 CPU-hr) — gates M13.1(c) and M44.1 scope
3. F1 if F5 + F2 both confirm (50 CPU-hr) — promotes M13.1(a) to higher confidence

## Discipline

- All protocols stated falsifiably with success/fail criteria
- No vague "validate prediction X" phrasing
- Costs based on M44 best-effort estimate; check before committing
