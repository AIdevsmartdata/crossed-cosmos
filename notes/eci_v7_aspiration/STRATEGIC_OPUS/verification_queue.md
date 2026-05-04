# Appendix — Verification Queue (post-v6.0.49)

Companion to `STRATEGIC_SYNTHESIS.md` §5. Detailed queue of 22 items requiring re-verification before any v6.0.50 release. Format: ITEM / SOURCE-LOCATION / VERIFICATION-METHOD / TIME-BUDGET / RISK-IF-WRONG / CURRENT-STATUS.

---

## Tier 1 — Load-bearing for theorems (re-verify within 1 week)

| # | Item | Where in repo | Method | Budget | Risk if wrong | Current |
|---|---|---|---|---|---|---|
| 1 | CLPW2023 = arXiv:2206.10780 type-II∞ | eci.tex axiom A1 + eci.bib | arXiv API + abstract pdftotext | 30 min | A1 collapses; entire framework | LIKELY OK (cited everywhere) |
| 2 | DEHK 2412.15502 QRF functoriality | eci.tex A1 + Theorem 1 | arXiv PDF + manual §6.3 read | 1 hr | A1 functoriality + Mistral §6.3 fn 12 claim | OK abstract; §6.3 fn 12 INCONCLUSIVE per I6 |
| 3 | Faulkner-Speranza 2405.00847 modular GSL | eci.tex §sec:mss-shadow + eci.bib | arXiv PDF | 30 min | M4 conjecture collapses | CONFIRMED CORRECT (v6.0.48 catch was misattribution to 2305.01696, fixed) |
| 4 | NPP20 2006.03058 Appendix D weight-5 hatted formulas | H2/build_2hat_prime_5.py | independent OCR (Marker / GROBID) + page-screenshot | 4 hr | S1 collapses; S2 collapses | RECONSTRUCTED FROM PDF; one independent re-extraction recommended |
| 5 | LYD20 2006.10722 Model VI rep + Y1,Y2,Y3 weight-1 forms | V1/audit_v1b.py + V2/v2_audit.py | independent re-derivation by separate sub-agent | 2 hr | V2 no-go collapses; H3 Yukawa collapses | CONFIRMED by V1+V2 independent audits |

## Tier 2 — Unique to ECI (re-verify within 2 weeks)

| # | Item | Where | Method | Budget | Risk |
|---|---|---|---|---|---|
| 6 | LMFDB 4.5.b.a Hecke char polynomials | G1.6 sign_resolution.md | SageMath if available; LMFDB browser otherwise | 1 hr | S1 first identification weakens |
| 7 | LMFDB 16.5.c.a 11/11 primes to Sturm B=10 | v6.0.49 commit msg | LMFDB browser direct (Bash WebFetch was blocked in some agents) | 2 hr | S1 second identification weakens |
| 8 | Wang-Zhang 2510.01312 Tables 1-2 (2-loop SM RGE calibration) | G19/g19_final.py | re-fetch arXiv HTML | 1 hr | G1.9 calibration weakens; v7 RGE chain weakens |
| 9 | Wolf 2025 ξ=2.31, log B=7.34, G_eff/G_N=1.77 | A4 + eci.tex §3.5 | WebFetch arXiv HTML + manual PDF | 2 hr | P1 framing weakens |
| 10 | Karam 2510.14941 Palatini NMC log B=5.52, neg ξ | v6.0.48 audit point (vi) | WebFetch + abstract quote | 1 hr | P1 "loophole bridge" weakens |
| 11 | Karam 2604.16226 (second Palatini paper) | v6.0.48 audit point (vi) | arXiv API existence check + abstract | 30 min | bib reference might be wrong |
| 12 | Hu-Wang-Hua 2508.01759 ">3σ NMC preferred" precise statement | v6.0.48 catch #60 + audit log | abstract quote, distinguish "NMC vs ΛCDM" from "Wolf-ξ=2.31 specifically" | 1 hr | F2 framing in v7 manifesto weakens |
| 13 | CCM 2511.22755 Zeta Spectral Triples precision figures (10^-55, primes ≤ 13, 10^-1235) | memory project_mcc_v7_aspiration.md | pdftotext grep on intro body | 30 min | §3.1.1 RH-bridge note (if pursued) weakens |

## Tier 3 — Changed meaning post-v7 refutation (re-verify within 4 weeks)

| # | Item | Where | Method | Budget | Risk |
|---|---|---|---|---|---|
| 14 | All 13 refs in §3.5 NMC-PPN | paper/section_3_5_constraints.tex | per-ref arXiv API + abstract spot-check | 4 hr | ξ_χ Cassini bound weakens |
| 15 | All 8 refs in §3.6 Swampland×NMC | paper/section_3_6_swampland_cross.tex | same | 3 hr | Dark Dimension c' bounds drift |
| 16 | All 11 refs in §3.7 perturbations | paper/section_3_7_perturbations.tex | same | 4 hr | f_NL + structure-formation NMC corrections drift |
| 17 | eci.bib comments (Wolf, Karam, Hu, Bella, AxiCLASS, Wang-Zhang) | eci.bib | spot-check each comment field for Mistral fabrication | 2 hr | bib commentary may carry hallucination |
| 18 | 14-prime λ(p) sequence for 2̂(5) | v6.0.48 audit log point (vii) | independent sympy re-run with N=2000 | 4 hr | S2 sub-algebra closure to p=113 weakens |
| 19 | Innsbruck Cs-133 anyonization Nature 642, 53 (2025) DOI 10.1038/s41586-025-09016-9 / arXiv:2412.21131 | §3.9 falsification targets | DOI + arXiv API | 30 min | P1 outreach weakens |
| 20 | DESI DR2 2503.14738 PRD 112, 083515 — precise σ figure for flat-ΛCDM disfavour | §sec:editorial | arXiv abstract + journal PDF | 1 hr | "3.1-4.2σ" headline number drifts |
| 21 | KiDS-Legacy S_8 = 0.815 +0.016/-0.021 at 0.73σ from Planck | mcmc/cobaya_nmc/eci_kids_s8.py + v6.0.44 patch | arXiv 2503.19441 abstract + paper | 1 hr | structure-formation prune-analysis weakens |
| 22 | Iguri-Trinchero math-ph/0211026 J.Stat.Phys. 2003 — intermediate values genuinely differ from k/(k+1) | eci.tex §3.9 lines 309-318 | arXiv PDF + numerical check at k=2 | 2 hr | para-fermion theorem novelty claim weakens |

---

## Total budget for full Tier 1+2+3 audit

- Tier 1: ~8 hours
- Tier 2: ~10 hours
- Tier 3: ~22 hours
- **Total: ~40 hours = 1 work week of 1 dedicated Sonnet-grade auditor** (compute cost ~$50-80 in Sonnet calls + ~$10 in WebFetch)

This is **strongly recommended** before v6.0.50 release.

---

## Empirical reliability table (from v6.0.40-49 catches)

Cumulative hallucinations: 67. Source breakdown:

| Source of hallucination | Count | Example |
|---|---|---|
| Mistral large-latest fabrication-on-demand | 7 | KiDS-Legacy fabricated arXiv ID, Wolf log B sign-flip, FS misattribution to 2305.01696, Q2 fabrication, S'_4 Q1 mislabel, Longo 2020 fabrication, Witten 2021 fabrication |
| WebFetch summary-table inversion | 3 | LMFDB 4.5.b.a a(13) and a(29) sign-flips (caught G1.6) |
| Sub-agent fabrication to match cross-check | 3 | Brown 1981 Trans.AMS 266 p.91, Sorkin 1987 IJMPD CrossRef-404, Pan-Yang 1804.05064 |
| Author training-knowledge over-citation | 5 | Devastato PRD ID, Karwal-Kamionkowski ID, Dark Dimension ID, KSTTT 1908 ID, KiDS-Legacy 3σ |
| OCR / multi-column scrambling | 2 | NPP20 App D formulas (caught H2 + cross-checks) |
| Author cherry-pick / interpretation drift | 2 | G1.7 "3% at y_t(M_GUT)=1.0" cherry-pick (caught G1.8); Hu et al. >3σ misattribution |
| Author irrep fabrication | 1 | S'_4 4̂ and 2̂' irreps that don't exist (caught H2 self-correction) |
| Magistral mislabel-on-demand | 1 | S'_4 Q1 mislabel (caught v6.0.47) |

**Pattern**: ~50% of catches are LLM-generated (Mistral 7 + WebFetch 3 + sub-agent fabrication 3 + Magistral 1 = 14/67 = 21%); 30% are author-induced (training-knowledge over-citation 5 + cherry-pick 2 + irrep fabrication 1 = 8/67 = 12%); the rest are tool/OCR artefacts. **Mistral is the single largest LLM-source of hallucinations** (7/14 of LLM catches = 50%) and should be **strict-banned** from any verification chain going forward.

---

## Recommended hallucination-prevention protocol for v6.0.50+

Per claim that propagates to manuscript body:

1. **arXiv API existence check** (mandatory; ~30 sec)
2. **abstract quote verification** (mandatory; ~2 min)
3. **for numerical claims**: independent sympy/derivation by *different* sub-agent (~5 min)
4. **for theorem statements**: hostile-reviewer audit by Opus self-audit + 1 Sonnet (~10 min)
5. **for any claim cited from Mistral**: re-verify via Gemini CLI or strike (~3 min)
6. **for any claim from a "convenient" reference (i.e., one that perfectly answers the question)**: extra suspicion, double-verify

Per published version (Zenodo + GitHub release):
- Full Tier 1+2+3 verification queue (~40 hours / ~$80 compute)
- Public hallucination ledger update
- 1-week post-release community-feedback window before any follow-up claims

Cost-benefit: ~$100 of verification + 1 work week of auditor time per Zenodo version, vs the reputational cost of a public retraction. Strongly favourable.
