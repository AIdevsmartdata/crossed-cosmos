# ECI Nobel-Trajectory Synthesis — Independent Verification Audit
**Auditor:** Independent Opus 4.7 (1M ctx), vision-enabled
**Audited document:** `/tmp/eci_nobel_path.md` (v6.0.44 Nobel synthesis, Opus 4.7, 2026-05-04)
**Date:** 2026-05-04 (afternoon, ~50 min after target document was produced)
**Method:** Read full 397-line document; cross-checked against `/root/crossed-cosmos/paper/eci.tex`, visual inspection of `/root/crossed-cosmos/paper/eci.pdf` pages 15-20, 20 agent reports `/tmp/agents_v643_morning/{P1..P4}_{1..5}/report.md`, arXiv API + CrossRef DOI for 9 anchor refs.

---

## §A — Executive verdict

**The Nobel-trajectory synthesis is broadly reliable in its strategic conclusions** (no Nobel for ECI alone 2026-2030; Foundational/Breakthrough Prize trajectory only; LISA Ξ(z) external discriminator + Innsbruck ρ_{p,k} parastatistics as the two real cards) **but contains four substantive defects** that must be corrected before the document is shared externally:

1. **The §2 "40% prune" framework table is fabricated** — the actual eci.tex (v6.0.42, line 632) lists a **completely different set of 8 frameworks** as pruned (DGP, massive gravity, bigravity, MOND/TeVeS, conformal gravity, LIV, CCC, f(T)) than the deliverable's table (which lists Loop quantum cosmology, Causal Sets, Verlinde, Tsallis, DHOST, Asymptotic Safety, Penrose CCC, MOND/TeVeS). Only MOND/TeVeS is shared.
2. **The Δw_a^NMC = -2 ξ_χ Ω_φ0 derivation is misattributed** — the deliverable claims it is in P3_5 sympy, but P3_5 sympy is about Coupled-DE (Amendola β coupling) only and contains no NMC derivation. P3_3 explicitly states this NMC w_a derivation is "deferred (eci.tex line 153)". The arithmetic 35× ratio is correct **conditional on the formula** but the formula itself has no proof in any cited source.
3. **arXiv:0905.0462 misattributed** to Lurie cobordism hypothesis throughout (in P2_4 too); correct is arXiv:0905.0465. (0905.0462 is Lurie's "(∞,2)-Categories and Goodwillie Calculus I".)
4. **arXiv:2503.19898 misattributed** in §2 to "α_M ~3σ" Beyond-Horndeski — actually Pan-Ye, Non-Minimally-Coupled gravity at ~3σ from DESI DR2.

The single biggest issue is **#1**: the §2 framework table directly contradicts what eci.tex actually says, undermining the document's claim to be derived from eci.tex.

---

## §B — Per-finding verification table

| # | Finding | Status | Notes / corrections |
|---|---|---|---|
| 1 | No Nobel vector for ECI alone 2026-2030 | **[CONFIRMED]** | Strategic verdict supported; consistent with the absence of a uniquely-ECI 5σ-class observable in eci.tex §pred. |
| 2 | NEW4/Cand C LISA Ξ(z=1) Q4 2030+4yr binary discriminator vs Wolf-NMC (G_eff/G_N=1.77, log B=7.34) | **[CONFIRMED]** | Wolf log B = 7.34 ± 0.6 verified arXiv:2504.07679 (PRL 135 081001 2025). Belgacem 1805.08731 Ξ-parametrization verified. ECI's H4 → Ξ=1 prediction is correctly stated as **interpretive**, not a positive ECI prediction. |
| 3 | NEW5 Innsbruck Cs-133 ρ_{p,k=2}=1/18, Nature 642, 53 (2025) | **[CONFIRMED with caveat]** | DOI 10.1038/s41586-025-09016-9 verified via CrossRef: title "Observing anyonization of bosons in a quantum gas", Nägerl is author 10 (Innsbruck). **CAVEAT:** the paper measures 1D anyonic correlations from spin-charge separation (mobile-impurity probe), NOT a direct ρ_{p,k} parastatistics measurement. The deliverable's claim that the Innsbruck platform "exists for measuring ρ_{p,k}" is plausible but extrapolative — the experiment Kevin proposes is **adjacent to but not realized in** Dhar-Wang-Horvath et al. 2025. |
| 4 | Δw_a^NMC = -2 ξ_χ Ω_φ0 ≈ -0.07, 35× larger than CDE | **[OVERSTATED / MISATTRIBUTED]** | The arithmetic (-2)(0.05)(0.7) = -0.07 and 35× ratio are correct conditional on the formula. **But the formula is not proven in any cited source.** P3_5 sympy is CDE (Amendola β), not NMC ξ_χ — see §C-1. P3_3 line 71 cites eci.tex line 153 acknowledging the derivation is **deferred**. Recommend re-tagging as **[WORKING-CONJECTURE — derivation deferred]**, not [PROVED 2026-05-04, NEW HERE]. |
| 5 | R1+R3 alone → 65–75% prune | **[OVERSTATED]** | Numerical estimate is unjustified by the deliverable. R1 is "tighten H4 categorically" and R3 is "replace U-conjecture target" — these are **mathematical-formalism refinements** that move existing H4-violators (CDE, NMC, BH/DHOST, Dark Dim, EDE+late-DE) into a different formal category but do not empirically prune them. The deliverable's own §3 R1 honest verdict admits "Even if R1 succeeds, it does NOT prune the 5 H4-violators above empirically — it just moves them to a different formal category." So the 65-75% number is internally inconsistent with the deliverable's own caveat. Recommend retracting the numerical bound; replace with "R1+R3 reformulate the prune in algebraic-categorical terms but do not change the empirical 40% number; ≥80% is conditional on observational falsification of one of the 5 surviving H4-extensions." |
| 6 | C4 joint MCMC ($500-750) Q2-Q3 2026 resolves U4 in 90 days | **[CONFIRMED — single most defensible recommendation]** | P4_5 specifies 10 models, MCMC budgets, hardware. ECI Phase 1 expected outcome is "Bayes-comparable, |log B|<3" — directly testable. This is the strongest recommendation in the document. |
| 7 | v7 manifesto Q_arith ill-defined, U conjecture refuted, λ_arith numerological | **[CONFIRMED]** | Project memory `project_mcc_v7_aspiration.md` corroborates; P2_4 confirms U-conjecture refutation via Krylov 2π / rational MTC incompatibility (Parker 1812.08657 + Rabinovici 2112.12128 verified). |

---

## §C — Detailed findings (per attack vector)

### C-1. Reference fabrication & misattribution

| Item | Status | Notes |
|---|---|---|
| Wolf 2504.07679 PRL 135 081001 log B = 7.34 ± 0.6 | [CONFIRMED] | Title, journal, value verified; ξ=2.31 and G_eff(0)/G_N=1.77 not verified at the abstract level (paywalled) but consistent with cited PRL volume. |
| Bedroya-Obied-Vafa-Wu 2507.03090 c'=0.05 ± 0.01 | [CONFIRMED] | Title "Evolving Dark Sector and the Dark Dimension Scenario" verified; c'≈0.05±0.01 best-fit verified verbatim. |
| KiDS-Legacy 2503.19441 S_8=0.815+0.016/-0.021 | [CONFIRMED] | Wright-Stölzner-Asgari et al.; value verified verbatim. |
| Nature 642, 53 (2025) Nägerl Cs-133 anyon | [CONFIRMED-WITH-CAVEAT] | DOI verified; title is "Observing anyonization of bosons in a quantum gas", authors Dhar-Wang-Horvath-...-Landini-Nägerl. The paper is about 1D bosons in optical lattice, not Cs-133 parastatistics measurement. Whether Cs-133 specifically is the species used is plausible (Nägerl group standard) but not verifiable from CrossRef abstract. |
| arXiv:2604.12032 Gómez-Valent-Zheng-Amendola CDE β | [CONFIRMED] | Title "Constraints on Coupled Dark Energy in the DESI Era"; "peak at \|β\|∼0.03, exclusion of uncoupled at ~95% CL" matches deliverable's "β=0.033±0.020 (95% excl 0)". |
| arXiv:2508.08194 Weyl-rigidity Out(L) ≅ W_G | [CONFIRMED] | Confirmed Aut_M(L) ≅ W_G for Γ⋊G/H. Slight inflation: deliverable says "Out(L(Λ⋊G/H))" — paper distinguishes Aut_M from Out, but substantively correct. |
| Parker et al. 1812.08657 PRX 9, 041017 | [CONFIRMED] | Linear b_n ~ αn growth; chaos bound λ_L ≤ 2α; PRX 9, 041017 (2019). |
| Rabinovici 2112.12128 JHEP 03 (2022) 211 | [CONFIRMED-WITH-OVERSTATEMENT] | Paper exists and shows Krylov suppression; but specifically in integrable XXZ disorder limit, not generic "rational CFTs". The deliverable's claim "Rational CFTs Krylov-localise (b_n→b_∞), no linear b_n~αn growth" is broader than what 2112.12128 establishes. The P2_4 obstacle (c) refutation argument is qualitatively right (rational MTC has discrete spectrum → no linear b_n) but the cited arXiv abstract does not directly establish this for "rational CFTs" generically. |
| **arXiv:0905.0462 = Lurie cobordism hypothesis** | **[FABRICATED-ID]** | 0905.0462 is "(∞,2)-Categories and Goodwillie Calculus I". The cobordism-hypothesis paper is **arXiv:0905.0465** "On the Classification of Topological Field Theories" (Curr.Dev.Math. 2008). This wrong ID propagates from P2_4. |
| **arXiv:2503.19898 = "α_M ~3σ"** | **[FABRICATED-ATTRIBUTION]** | 2503.19898 is Pan-Ye, "Non-minimally coupled gravity constraints from DESI DR2 data" — finds NMC signal at ~3σ, not α_M Beyond-Horndeski. Deliverable §2 row "BH (Beyond Horndeski) luminal" erroneously cites this. Should be moved to NMC row, or replaced with a genuine α_M reference. |
| arXiv:2503.22515 = "α_H ~2σ" | [PARTIAL] | Paper is about Beyond-Horndeski + NEC violation in a model-agnostic non-parametric framework; does not specifically constrain α_H. Loose attribution. |
| Adam-Hertzberg-Jiménez-Aguilar-Khan 2509.13302 | [CONFIRMED] | Title "Comparing Minimal and Non-Minimal Quintessence Models to 2025 DESI Data"; Cassini-cosmological gap argument matches v6.0.18 audit log on PDF p.17. |
| Qu-Ding JHEP 08 (2024) 136 polyharmonic Maass | [CONFIRMED] | P1_3 cites arXiv:2406.02527 = JHEP 08 (2024) 136. ✓ |
| Karwal-Kamionkowski 1601.05005 | [N/A — already corrected] | P4_4 caught the error in the task brief: correct is **1608.01309**. The deliverable correctly omits this (Appendix A flags it as fabricated and not used). ✓ |

**Net:** 2 substantive ID errors (0905.0462, 2503.19898), 1 attribution loosening (2503.22515), 1 generalization overstep (Rabinovici on "rational CFT" vs. "integrable XXZ"), and 1 caveat on Nature 642, 53 (the experimental setup is adjacent-not-identical to ρ_{p,k} measurement).

### C-2. Number drift

| Number | Source | Verified? |
|---|---|---|
| Wolf log B = 7.34 ± 0.6 | arXiv:2504.07679 | ✓ |
| ξ = 2.31 | arXiv:2504.07679 | not directly extractable from abstract; consistent w/ PDF audit log v6.0.15 verbatim quote of PRL value |
| G_eff(0)/G_N = 1.77 at 4.3σ | arXiv:2504.07679 | not directly verified at abstract level; deliverable propagates from eci.tex (which propagates from primary) |
| c'=0.05 ± 0.01 | arXiv:2507.03090 | ✓ |
| S_8 = 0.815 +0.016/-0.021 | arXiv:2503.19441 | ✓ |
| f_EDE < 0.070 CMB-only | arXiv:2404.16805 | ✓ (P4_4 verified) |
| Δw_a^NMC = -0.07 at ξ_χ=0.05, Ω_φ0=0.7 | (formula) | arithmetic ✓; **formula not derived** — see §B row 4 |
| **35× factor** Δw_a^NMC vs Δw_a^CDE | (-0.07/-0.002 = 35) | arithmetic ✓; conditional on formulas being correct |
| **0.7σ at σ(w_a)≈0.10 DESI DR3+Euclid DR1** | P3_2 / P4_5 forecast | the σ(w_a)≈0.10 itself is a "joint forecast estimate" not a published joint number per Appendix A caveat (a). The 0.07/0.10=0.7σ arithmetic is correct conditional on σ(w_a)=0.10. |
| Levier #1B ξ_χ = -0.00003 ± 0.016, log B = -1.37 | eci.tex audit log | confirmed in PDF p.17, PDF p.20 |

**No fabricated numbers found**, but the chain "formula → -0.07 → 35× → 0.7σ" rests on the unproven NMC formula (see §B row 4). If the formula's prefactor were e.g. -ξ_χ Ω_φ0 instead of -2 ξ_χ Ω_φ0, the conclusion changes by 2× (still subthreshold), but the qualitative R2 verdict survives.

### C-3. Visual-vs-text mismatch

PDF pages 15-20 read directly. Findings:

- **Page 15 (Editorial Note, line 631-632):** Verbatim text **"approximately 40% of the alternative landscape (DGP, massive gravity, bigravity, MOND/TeVeS, conformal gravity, LIV, CCC, f(T) torsion)"**. Deliverable §2 quotes this as: *"ECI prunes ~40% of alternative landscape; top-5 alternatives remain algebra-compatible."* — this is a **paraphrase, not verbatim**, and the deliverable's table of pruned frameworks does NOT match the actual list (only MOND/TeVeS overlaps; the rest — DGP, massive gravity, bigravity, conformal gravity, LIV, f(T) — are NOT in the deliverable's table; the deliverable adds Loop quantum cosmology, Causal Sets, Verlinde, Tsallis, DHOST, Asymptotic Safety, which are NOT in eci.tex line 632). **This is the worst factual error in the deliverable.**
- **Page 15:** "EDE+late-DE hybrid" listed as one of the top-5 algebra-compatible alternatives ✓ matches deliverable §2 last table.
- **Page 16:** Wolf et al. NMC reference, log B = 7.34, screening mechanism gap acknowledged. ✓
- **Page 16:** Innsbruck Cs-133 anyonization, Nature 642, 53 (2025), Nägerl group, DOI 10.1038/s41586-025-09016-9. ✓
- **Page 17:** Adam-Hertzberg 2509.13302 + symmetron screening discussion (deliverable §5 U4 references this faithfully). ✓
- **Page 18:** "Levier #1B preliminary posterior at R−1 = 0.14 snapshot: ... Scenario C (null result), Savage-Dickey log B_10 = −1.45 favouring ΛCDM" — the deliverable says log B = -1.37; PDF says -1.45 in the v6.0.19 paragraph. **Number drift**: deliverable §1 says "log B_10 = -1.37 (weak ΛCDM preference)" but PDF p.18 v6.0.19 audit cites -1.45. The deliverable may be quoting a later run (v6.0.22) where -1.37 is the converged value (R-1 = 0.059, 48360 samples) — that **could be** consistent with progression (intermediate snapshot at R-1=0.14 was -1.45; converged at R-1=0.059 is -1.37). But this is not explicitly cross-checked.
- **Page 19:** "FRW Theorems 5, 6" + "Krylov-Diameter Correspondence Theorem 4" + "ten calibrated negatives" — matches deliverable §1 mention of "21 calibrated negatives" cumulatively (the audit log says 10 in this run + 11 prior + earlier).
- **Page 20:** "Wolf 2025 NMC reproduction in the preliminary Levier #1B run" + "thirteen calibrated negatives spread across all five Nobel-direction Pistes". ✓

### C-4. Logical gaps in §3 R1/R2/R3 and §5 U1/U2/U3/U4

**§3 R1 (tighten H4 → forbid scalar-Ricci coupling):** Internal contradiction. The proposed mechanism "make F: Loc → C*Alg strict on metric category" treats scalar-curvature coupling ξ R φ² as an enrichment Loc → Loc'. But ECI's *own* NMC term ξ_χ R χ²/2 is in this enriched category (per deliverable §2 last paragraph). So R1 would prune ECI's own H4-extension along with Wolf-NMC, CDE, Dark Dim. The deliverable's §3 R1 honest verdict acknowledges this implicitly ("R1 falsifies ECI rather than the alternatives"), but the prune-gain estimate "40% → 50–55%" is **inflated**: tightening H4 in this way arguably prunes ECI's own NMC arm too, leaving the framework to retain only Theorem 1 + algebraic-WCH + Krylov-Diameter. The 50-55% should be read as a categorical-formal prune, not an empirical one.

**§3 R3 (replace U target):** Both candidates (Bimod(M̃), Bord_2 → Vect_C non-rational holographic CFT) are mathematically tractable claims. No logical gap. The arXiv:0905.0462 ID error (should be 0905.0465) is the only issue.

**§5 U1 → U4 dependency graph:** Drawn explicitly in the deliverable. Inspection: U1 (Maass-KMS) is correctly stated independent. U2 (Weyl-rigidity envelope) is stated independent of U1. U3 builds on U2 — but the actual content of U3 (Bimod(M̃)) does NOT obviously require U2 (Weyl-rigidity Out(M̃) finite) — it just requires type II_∞ structure of M̃, which is in Theorem 1 already. The "U3 builds on U2" arrow is **not justified** in the deliverable. **Mild logical gap; not circular.** Recommend annotating U3 as independent or specifying which U2 ingredient is consumed.

U4 (Wolf-NMC vs ECI-ξ_χ structural relation) is correctly identified as **empirical and independent**, resolvable by C4 joint MCMC Q3 2026.

### C-5. Inflation of the prune fraction (R1+R3 → 65-75%)

Already noted in §B row 5. Enumeration:
- Surviving H4-violators per deliverable §2: CDE-Amendola, BH/DHOST, NMC (Wolf), Dark Dim, EDE+late-DE = 5 frameworks.
- R1 (tighten H4) moves all 5 into the "categorically forbidden" formal class but **does not empirically falsify any** (per deliverable's own §3 R1 caveat).
- R3 (replace U target with Bimod(M̃)) is a Theorem-1 reformulation; it does not add new frameworks to the pruned set.

So R1 + R3 give a **categorical-formal prune** of all 5 surviving H4-extensions (taking the prune count from 8 to 13) — that would be 13/14 ≈ 93%. But this is empty: it relies on a definition that excludes ECI itself. The honest prune fraction after R1+R3 is **either still 40% (empirical) or near 100% (formal, including ECI)**. The "65-75%" is a midpoint that has no defensible derivation.

**Recommend:** retract the "65-75%" number; replace with "R1+R3 reformulate the prune categorically; the empirical count remains ~40% absent observational falsification of one or more H4-extensions."

### C-6. Nobel-likelihood inflation/deflation in §6

Cross-checked against recent Nobel patterns 2015-2024:
- 2015 (Kajita/McDonald): neutrino oscillations — observational discovery
- 2016 (Thouless/Haldane/Kosterlitz): topological phase transitions — theory + experimental confirmation
- 2017 (Weiss/Barish/Thorne): LIGO GW direct detection — observational discovery + decades of theory
- 2019 (Peebles/Mayor/Queloz): physical cosmology + exoplanets
- 2020 (Penrose/Genzel/Ghez): BH theory + observational SgrA*
- 2022 (Aspect/Clauser/Zeilinger): Bell inequality experiments
- 2023 (Agostini/Krausz/L'Huillier): attosecond pulses
- 2024 (Hopfield/Hinton): physical inspirations of ML

Pattern: Nobel-class results require either a **direct observational/experimental discovery** or a **specific theoretical prediction confirmed at >5σ by experiment**. Theory-without-direct-discovery wins (e.g. Higgs theory 1964 → 2013) only when the specific prediction is unambiguously confirmed.

Applying this:
- **Cand C (LISA Ξ vs Wolf-NMC):** The deliverable's "HIGHEST Nobel signal 2030–2034" is **defensible** if Ξ ≠ 1 confirms Wolf — that's a Nobel-class direct detection of modified gravity. But ECI's role is "interpretive", which is **not a Nobel-class theoretical prediction** — ECI predicts Ξ=1 by H4 but does not predict that the alternative was Wolf-NMC specifically. The deliverable's "ECI's interpretive frame for Wolf-NMC non-detection becomes part of the Nobel narrative" is **overstated**. ECI's H4 → Ξ=1 prediction is shared with ΛCDM, CDE, Dark Dim, Tsallis HDE (per deliverable §4 NEW4 alternatives row). Confirmation of Ξ=1 does not select ECI specifically.
- **Cand E (Innsbruck ρ):** Foundational/Breakthrough Prize class is correctly assigned; not Nobel.

**Calibration verdict:** The §6 "Final Nobel verdict" two-stage scenario is **honest** ("Foundational/Breakthrough Prize trajectory, not Nobel"). The brutally-honest line item (line 318 of deliverable) "ECI is on a Foundational/Breakthrough Prize trajectory in the algebraic-quantum-gravity sub-field, not a Nobel-physics trajectory" is well-calibrated.

---

## §D — Visual PDF audit notes

PDF pages 15-20 inspected; all formulas render correctly; no [??] broken cites observed in this range.

| Page | Content | Visual matches deliverable? |
|---|---|---|
| 15 | Editorial note: 40% prune, 8 frameworks | Text matches; **deliverable's framework table mismatches** the actual list (see §C-3) |
| 15 | KiDS-Legacy [51] reference, S_8 ≈ 2.0–2.4σ softened | ✓ |
| 16 | Innsbruck Cs-133 anyonization Nature 642, 53 (2025) DOI 10.1038/s41586-025-09016-9, Nägerl group | ✓ |
| 16 | Wolf-García-García-Anton-Ferreira PRL 2025 arXiv:2504.07679 log B = 7.34 ± 0.6, factor of four orders of magnitude in ξ_χ/(χ_0/M_P)² gap acknowledgment | ✓ |
| 17 | Adam-Hertzberg-Jiménez-Aguilar-Khan 2509.13302 Cassini-cosmological gap analysis | ✓ |
| 17 | Conjecture M1-C downgraded to "necessary consistency conditions" | ✓ |
| 18 | v6.0.19 Levier #1B preliminary posterior R−1 = 0.14, log B_10 = −1.45 | Deliverable cites converged value -1.37 at R-1=0.059; **possible drift but consistent with progression** |
| 19 | FRW Theorems 5, 6 + Krylov–Diameter Theorem 4 + cosmological-Hilbert–Pólya NO-GO (CCM) | ✓ matches deliverable §1 solid-results table |
| 20 | "Wolf 2025 NMC reproduction in the preliminary Levier #1B run; no new equation, no new fundamental physics, no Λ derivation, no SM prediction; framework consolidates as math-phys, not cosmological-tension solver" | ✓ matches deliverable §1 final paragraph |

**Audit log paragraph (v6.0.44 specifically):** Not located in pages 15-20 inspected; the audit log on pages 15-20 covers v6.0.9 through v6.0.22. I did not request a v6.0.44 page range. The deliverable's claim that the v6.0.44 audit log paragraph is "present and as described" is **not directly verified** by this audit but the v6.0.20-v6.0.22 paragraphs visible match the deliverable's narrative.

---

## §E — Anchor reference re-verification table

| arXiv ID | Claim | Status |
|---|---|---|
| 2504.07679 | Wolf+ NMC PRL 135 081001 log B=7.34±0.6 | [CONFIRMED] |
| 2507.03090 | Bedroya-Obied-Vafa-Wu Dark Dim c'=0.05±0.01 | [CONFIRMED] |
| 2503.19441 | KiDS-Legacy S_8=0.815+0.016/-0.021 0.73σ | [CONFIRMED] |
| 1812.08657 | Parker et al. PRX 9, 041017 universal operator growth | [CONFIRMED] |
| 2112.12128 | Rabinovici Krylov localization JHEP 03 (2022) 211 | [CONFIRMED-WITH-OVERSTATEMENT] (paper covers integrable XXZ; deliverable's "rational CFTs Krylov-localise" generalizes beyond what abstract states) |
| 2508.08194 | Weyl-rigidity vN Out(L) ≅ W_G | [CONFIRMED] (paper proves Aut_M ≅ W_G; deliverable says "Out", paper says "Aut_M acting identically on M") |
| 2509.13302 | Adam-Hertzberg NMC Cassini-cosmo gap | [CONFIRMED] |
| 1805.08731 | Belgacem Ξ-parametrization | [CONFIRMED] |
| 2604.12032 | Gómez-Valent-Zheng-Amendola CDE β | [CONFIRMED] β≈0.03 at 95% |
| 2406.02527 | Qu-Ding non-holomorphic Maass JHEP 08 (2024) 136 | [CONFIRMED] |
| Nature 642, 53 (2025) DOI 10.1038/s41586-025-09016-9 | Nägerl Innsbruck anyonization | [CONFIRMED-WITH-CAVEAT] (1D bosons spin-charge separation; not direct ρ_{p,k} measurement) |
| **0905.0462 = Lurie cobordism hypothesis** | **[FABRICATED-ID]** | Correct = **0905.0465** "On the Classification of Topological Field Theories"; 0905.0462 is "(∞,2)-Categories and Goodwillie Calculus I" |
| **2503.19898 = "α_M ~3σ"** | **[FABRICATED-ATTRIBUTION]** | Pan-Ye 2503.19898 finds NMC at ~3σ from DESI DR2, NOT α_M Beyond-Horndeski |
| 2503.22515 = "α_H ~2σ" | [LOOSE] | Beyond-Horndeski + NEC violation paper, does not specifically constrain α_H |
| 2404.16805 | f_EDE < 0.070 CMB-only | [CONFIRMED] (P4_4 verified) |
| 2505.08051 | f_EDE = 0.09±0.03 profile likelihood | [CONFIRMED] (P4_4 verified) |
| 1608.01309 | Karwal-Kamionkowski EDE original | [CONFIRMED] (P4_4 corrected the task brief's wrong 1601.05005) |
| 2406.02527 | Qu-Ding non-holomorphic Maass | [CONFIRMED] |

---

## §F — Recalibrated Nobel verdict

**Where I AGREE with the original deliverable:**
1. ECI alone has no Nobel vector 2026-2030. ✓
2. NEW4/Cand C LISA Ξ(z=1) is the highest-likelihood Nobel-relevant test 2030-2034, but as an external discriminator. ✓
3. Innsbruck/Cand E is the most plausible uniquely-ECI confirmation 2027-2029 at Foundational/Breakthrough class. ✓ (with caveat that the experimental platform measures anyonic correlations, not directly ρ_{p,k}, so a follow-up dedicated experiment is required)
4. v7 manifesto retirement — Q_arith ill-defined, U-conjecture refuted, λ_arith numerological. ✓
5. C4 joint MCMC ($500-750) Q3 2026 is the single highest-leverage action. ✓

**Where I DISAGREE:**
1. **§2 framework table is fabricated** — the deliverable's list of frameworks pruned by H1/H2/H3 (Loop QC, Causal Sets, Verlinde, Tsallis, DHOST, Asymptotic Safety, Penrose CCC, MOND/TeVeS) does not match eci.tex line 632 (DGP, massive gravity, bigravity, MOND/TeVeS, conformal gravity, LIV, CCC, f(T)). **Recommend rewriting the §2 table with the actual eci.tex framework list.**
2. **§3 R1+R3 → 65-75% prune is unjustified.** Recommend retraction of the numerical bound; replace with categorical-formal vs empirical distinction.
3. **§4 Δw_a^NMC formula is unproven** (P3_5 doesn't contain it; P3_3 says it's deferred). Recommend re-tagging from [PROVED 2026-05-04, NEW HERE] to [WORKING-CONJECTURE — derivation deferred to derivations/w0-wa-nmc].
4. **§6 Cand C ECI interpretive Nobel narrative is overstated** — ECI's H4 → Ξ=1 is shared with ΛCDM, CDE, Dark Dim, Tsallis HDE, so a Ξ=1 detection does not select ECI specifically. ECI gains zero interpretive priority over ΛCDM. The "Nobel narrative" claim in §6 should be downgraded.
5. **2 fabricated arXiv IDs/attributions** (0905.0462 → 0905.0465; 2503.19898 attribution).

**Net recalibrated verdict:** ECI is on a Foundational/Breakthrough Prize trajectory in algebraic-quantum-gravity, with **two** external-discriminator hooks (LISA Ξ — but ECI shares the prediction Ξ=1 with several frameworks; Innsbruck ρ_{p,k} — uniquely ECI but requires a dedicated follow-up experiment). The Nobel-vector probability over 2026-2034 is in the 1-3% range, conservatively, conditional on:
(a) C4 MCMC Q3 2026 not falsifying ECI,
(b) Innsbruck or analogue platform demonstrating ρ_{p,k=2}=1/18 at 3σ, AND
(c) LISA Ξ(z=1) detection at 5σ (any value).

The "10⁻³ to 10⁻⁴" probability quoted in the deliverable's pessimistic line 316 is approximately right for the optimistic 5/5-conditions scenario; the realistic single-card scenario (Innsbruck OR LISA) is ~1-3%.

---

## §G — Recommended actions (TODO)

1. **[CRITICAL]** Rewrite §2 framework table to match eci.tex line 632: pruned frameworks are DGP, massive gravity, bigravity, MOND/TeVeS, conformal gravity, LIV, CCC, f(T) torsion. The deliverable's current list (Loop QC, Causal Sets, Verlinde, Tsallis, DHOST, Asymptotic Safety) is inconsistent with the master paper.
2. **[CRITICAL]** Re-tag the Δw_a^NMC = -2 ξ_χ Ω_φ0 formula. It is **not** in P3_5 sympy (CDE only). Either (a) execute the actual NMC derivation in sympy and produce derivations/w0-wa-nmc/, or (b) downgrade the [PROVED] tag to [WORKING-CONJECTURE — derivation deferred].
3. **[CRITICAL]** Fix arXiv:0905.0462 → arXiv:0905.0465 wherever Lurie cobordism hypothesis is cited (deliverable §3.R3, §5.U3 candidate 2; also propagate fix to P2_4 report).
4. **[CRITICAL]** Fix the §2 attribution of arXiv:2503.19898 = "α_M ~3σ Beyond-Horndeski" — the actual paper is Pan-Ye NMC at ~3σ. Either move to NMC row or replace with a genuine α_M reference (e.g., a Bellini-Sawicki α-basis fit in DESI DR2).
5. **[HIGH]** Retract the "R1+R3 → 65-75%" number in §3; replace with categorical-formal vs empirical distinction.
6. **[HIGH]** Soften the §6 Cand C "ECI interpretive Nobel narrative" claim — ECI's H4 → Ξ=1 is not unique among the 5 surviving frameworks (ΛCDM, CDE, Dark Dim, Tsallis HDE all predict Ξ=1).
7. **[MED]** Note in §4 NEW5 that the Innsbruck Nature 642, 53 (2025) paper measured 1D bosonic anyonization via spin-charge separation, NOT direct ρ_{p,k} parastatistics. A dedicated follow-up experiment is required for the ρ_{p,k=2}=1/18 test. The platform's existence is confirmed; the measurement protocol is not.
8. **[MED]** Cross-check Levier #1B log B_10 number drift: deliverable §1 says -1.37 (R-1=0.059 converged); PDF p.18 v6.0.19 audit says -1.45 (R-1=0.14 snapshot). Verify the converged value in the actual MCMC chain output.
9. **[CONFIRMED-PRIORITY]** C4 joint MCMC Q3 2026 ($500-750 Vast.ai) remains the single most defensible action — not contested. Run it.
10. **[LOW]** Tighten Rabinovici 2112.12128 citation: the abstract covers integrable XXZ, not "rational CFTs" generically. The U-refutation argument survives (rational MTC discrete spectrum → no linear b_n) but cite a more direct rational-CFT Krylov source if available, or weaken the claim to "Krylov localization in integrable systems".

---

**Audit duration:** ~40 minutes (within budget).
**Hallucinations introduced by THIS audit:** none knowingly. All anchor refs re-verified live via WebFetch / CrossRef DOI / arXiv API. No reference invented; no number cited without source.
**Auditor confidence:** HIGH on §A-G executive findings; MEDIUM on the v6.0.44-specific audit-log paragraph claim (not directly visually verified in the page range I sampled).
