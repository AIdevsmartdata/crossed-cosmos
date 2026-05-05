# Cover letter v2 — v7.4 amendment to Letters in Mathematical Physics

**To:** Editorial Board, Letters in Mathematical Physics
**From:** Kévin Remondière (independent researcher, Tarbes, France)
**Subject:** Submission — *ECI v7.4 amendment (v2): τ as a CM-anchored attractor, the Damerell-ladder Cardy/CKM bridge H₇', and a CSD(1+√6) Littlest Modular Seesaw at K = ℚ(i)*
**Date:** 2026-05-05

Dear Editors,

I submit for your consideration the enclosed short note (14–16 pages, math-ph) recording the v7.3 → v7.4 amendment of the Extended Cosmological Index (ECI) research programme, integrated with six audit/calculation follow-ups (sub-agent waves 4–5, May 2026: A14, A16, A17, A22, A24, A26, plus the A18 / hallu #78 anti-fabrication correction).

## Why LMP rather than CMP

I considered both LMP and *Communications in Mathematical Physics*. I selected **LMP** for three reasons:

1. **Length.** The result is a single rational ladder (1/10, 1/12, 1/24, 1/60) for the algebraic parts of the integer critical L-values of one specific CM newform (LMFDB 4.5.b.a, CM by ℚ(i), weight 5), with parameter-free Cardy hits at c = 1 (free boson) and c = 1/2 (Ising). Three independent K = ℚ(i) probes (CSD(1+√6) Littlest Modular Seesaw with DUNE 2030+ δ_CP = −87° falsifier; two numerological CKM alignments; G1.12.B SU(5) + 45_H proton-decay campaign with M1+M2 PASS) are cross-cutting tests. The argument fits comfortably in 14–16 pages without expansion; CMP papers in this area typically run 30–60 pages.

2. **Dual-axiom revision format with one open question.** The contribution comprises axiom H₅' replacing H₅ (relaxation of the strict S-fixed-point assumption to a CM-anchored attractor, |τ − i| ≲ 0.2, supported by a 30 × 30 χ² scan with χ²/dof = 1.05) and axiom H₇' replacing H₇ (integer-point Damerell ladder + Bertolini–Darmon–Prasanna anti-cyclotomic complement). Theorem 4.1 (Bernoulli-anchored Cardy hit, α₂ = B₂/2 = 1/12 = ρ_Cardy(c=1)) is a small but proved result embedded in the H₇' axiom, with companion α₃ = 1/24 = ρ_Cardy(c=1/2) forced by the Γ functional equation. The two unfit central charges c = 7/10 (tricritical Ising) and c = 4/5 (tetracritical Potts) are the only open question, with two discriminating scenarios proposed (BDP p-adic vs second-form anchor). LMP routinely accepts this "result + flagged open question" format; CMP tends to require fully-proved theorems with no companion conjectures.

3. **Cross-disciplinary readership.** The note bridges critical L-values of CM modular forms (Damerell 1971, Shimura 1976, Harder–Schappacher 1986, Bertolini–Darmon–Prasanna 2013) and 2D CFT Cardy density at minimal-model central charges. LMP's mixed pure-math / mathematical-physics readership matches this scope exactly.

## Key claims

1. **Refutation of v7.3 H₇** (audit G1.15, Zenodo DOI 10.5281/zenodo.20030684, repository commit 6.0.53, 2026-05-05): the original axiom required L-value algebraicity at the half-integer s = k/2 = 5/2 for an odd-weight CM form, outside the Damerell–Shimura–Deligne archimedean algebraicity domain (Proposition 1).

2. **H₇' (primary): integer-point Damerell ladder.** L(f, m) · π^(4−m) / Ω_K⁴ ∈ {1/10, 1/12, 1/24, 1/60} for m ∈ {1, 2, 3, 4}, with the LMFDB CM newform 4.5.b.a and Chowla–Selberg period Ω_K = Γ(1/4)² / (2√(2π)). Computed by mpmath at dps = 60 via the Iwaniec–Kowalski approximate functional equation, with sanity check L(f, 5/2) = 0.5200744676… reproducing the LMFDB cached value exactly. The ladder is the standard Eisenstein–Kronecker ladder for a weight-5 CM-by-ℚ(i) newform: α₁ = 1/10 is the lemniscatic Hurwitz number H₄ (Hurwitz 1899), α₂ = 1/12 = B₂/2 is the Bernoulli value transported to ℚ(i) via Chowla–Selberg, with (α₃, α₄) = (α₂/2, α₁/6) forced by the Γ functional equation L(f, s) ↔ L(f, 5−s).

3. **One Bernoulli-anchored Cardy hit + Γ-shadow** (Theorem 4.1): the genuine parameter-free coincidence is α₂ = B₂/2 = 1/12 = ρ_Cardy(c=1) for the free boson (Tonks–Girardeau lab realisation); the Ising α₃ = 1/24 = ρ_Cardy(c=1/2) is its automatic Γ-shadow under the functional equation. The strength of the bridge is correspondingly half the v7.3 prospectus, but anchored on a textbook Bernoulli identity.

4. **H₅' (CM-anchored attractor): χ² scan finds τ\* = −0.1897 + 1.0034 i** with χ²/dof = 1.05 over seven fermion observables (W1, PC compute, 2026-05-05; cosmopower-jax, 386 predictions/s, RTX 5060 Ti), a factor ~3 closer to the S-fixed point τ = i than the LYD20 published best fit τ = −0.21 + 1.52 i.

5. **Three independent K = ℚ(i) follow-up probes**:
   1. CSD(1+√6) Littlest Modular Seesaw at strict τ_S = i (Ding–King–Liu–Lu Case B; de Medeiros Varzielas–King–Levy): NO + m₁ = 0 + δ_CP ≈ −87°, DUNE 2030+ ±15° falsifier;
   2. two numerological CKM alignments on the Damerell ladder (|V_us| = 9/40 to 0.015σ; |V_cb|² = 1/600 to 0.024σ), explicitly flagged as having empirical multiplicative coefficients, NA62 + FLAG-2027 / Belle II run 3 falsifiers;
   3. G1.12.B SU(5) + 45_H modular-flavour proton-decay campaign (six milestones, M1+M2 PASS, M3–M6 forecast 3.5–5 sub-agent months), parameter-free B(p → e⁺π⁰) / B(p → K⁺ν̄) ∈ [0.3, 3] Hyper-K + DUNE 2030+ falsifier.

6. **Honest caveats fully integrated.** Three negative results sit front and centre:
   1. √6 in the CSD(1+√6) alignment is Galois-rational, NOT period-anchored (PSLQ exhausted at dps = 60, |c| ≤ 500, in seven Chowla–Selberg bases; Remark 6.x);
   2. the W1 attractor τ\* does NOT accommodate the LYD20 unified-model lepton sector (24.5σ pull on sin² θ₁₃; Section 8 "Caveat" with two non-exclusive readings: two-tau reformulation τ_q ≠ τ_l, or LYD20-too-restrictive); v7.4.1 binary decision deferred to the next 64-observable refit;
   3. the empirical multiplicative coefficients (9/4, 1) in the CKM alignments are not structurally derived (Remark 7.x).

## Companion submissions in this volume

- **V2 no-go theorem** ("A no-go theorem for the Cabibbo angle in S'_4 modular flavour models at τ = i") in parallel preparation for LMP; it motivates the H₅ → H₅' relaxation by establishing that the strict τ = i ansatz forces sin θ_C ≤ 0.005 in LYD20 Model VI, a factor ~45 below experiment.
- **Cardy-bridge constructive note** on the explicit Damerell–Cardy correspondence (in preparation, target: LMP).
- **P-NT (parity-nontrivial) note on hatted weight-5 multiplets** (in preparation, target: BLMS).

I would be happy for any subset to be considered jointly by the same editor.

## Anti-fabrication assurances

The ECI project has a documented history of LLM-assisted citation hallucinations (current counter: 81, with hallu #78 "Wang–Zhang to Antusch–Hinze–Saad" caught and recorded explicitly in Section 9.1 of the manuscript). Every arXiv ID and journal reference in the bibliography of the enclosed v2 manuscript was live-verified against the arXiv API on 2026-05-05; verifications are recorded as commented-out remarks in the .tex source. Two sub-agent A37 catches made on this verification pass were:

- **LMS22 (arXiv:2211.00654)** authorship corrected from sole-author "S. F. King" to its actual three-author form "de Medeiros Varzielas, King, Levy".
- **DUNE24** bibitem text was rewired from arXiv:2403.18502 (which is Domingo et al., "A Novel Proton Decay Signature at DUNE, JUNO, and Hyper-K", a real but distinct paper) to the actually-intended DUNE Long-Baseline EPJC 80, 978 (2020) at arXiv:2006.16043. Both are kept as separate bibitems.

## Conflict of interest

None.

## Suggested referees

**Modular flavour:**
- G.-J. Ding (USTC) — co-author LYD20 (arXiv:2006.10722) and DKLL19 (arXiv:1910.03460), the two load-bearing modular-flavour inputs.
- S. F. King (Southampton) — co-author LMS22 (arXiv:2211.00654), CSD(1+√6) Littlest Modular Seesaw and Chen–King–Medina–Valle (arXiv:2312.09255).
- S. T. Petcov (SISSA) — co-author NPP20 (arXiv:2006.03058), the double-cover S₄ paper underpinning the S'₄ structure.
- F. Feruglio (Padova) — founder of the modular flavour programme.

**2D CFT and L-functions:**
- J. L. Cardy (Oxford / Berkeley) — the Cardy density bridge.
- E. Perlmutter (IPhT Saclay) — author of the degree-4 L-function approach (arXiv:2509.21672) cited as the H₇-B backup route.

**GUT proton decay:**
- K. M. Patel (PRL Ahmedabad) — co-author of PatelShukla23 (arXiv:2310.16563) used in G1.12.B M3.

**CM modular forms:**
- A. Booker (Bristol) — LMFDB co-developer; computational expert on critical L-values of CM newforms.
- S. Lemurell (Chalmers) — LMFDB CM-newform tables.
- K. Prasanna (Michigan) — co-author of the Bertolini–Darmon–Prasanna anti-cyclotomic p-adic L-function construction (Duke Math J 162, 2013) used in axiom H₇' BDP complement.

Thank you for considering this submission.

Sincerely,

Kévin Remondière
Tarbes, France
kevin.remondiere@gmail.com
GitHub: AIdevsmartdata/crossed-cosmos
ORCID: (in progress, will be supplied at acceptance)
Repository snapshot: Zenodo DOI 10.5281/zenodo.20030684 (v6.0.53, 2026-05-05, 06:00 UTC)
[or 10.5281/zenodo.20036808 for v6.0.53.2/.3 if pushed since A28 SUMMARY — Kevin to confirm]
