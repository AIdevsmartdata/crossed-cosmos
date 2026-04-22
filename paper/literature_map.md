# Literature map — ECI v4.4

For each axiom claim (§1, A1..A6) and each phenomenology claim
(§3.1..§3.5, §3.6) in `paper/eci.tex` + `section_3_5_constraints.tex` +
`section_3_6_swampland_cross.tex`: the primary reference (original paper
establishing the claim) and a recent review / follow-up.

Sources cross-checked against `paper/eci.bib` (bibkey column) and
`paper/_rag/INDEX.md` (verbatim-passage-verified where a `✓` appears
in the Notes column).

---

## Axioms (§1)

| section | claim | primary ref | cited as | recent review / follow-up | notes |
|---|---|---|---|---|---|
| A1 | Type-II von Neumann algebra (II_1 for dS static patch, II_∞ for Schwarzschild–dS) via QRF crossed product; S_gen = A/(4 G_N) + S_matter | Chandrasekaran–Longo–Penington–Witten 2023 (arXiv:2206.10780) | \cite{CLPW2023} | De Vuyst–Eccles–Höhn–Kirklin 2024 (arXiv:2412.15502), DEHK 2025 (arXiv:2503.14454) | ✓ RAG INDEX has CLPW verbatim passage for II_1 / S_gen formula. \cite{DEHK2025a,DEHK2025b} in bib. |
| A2 | Einstein eqs from δQ = T_U δS_gen on local Rindler horizons; GSL | Jacobson 1995 (gr-qc/9504004) | \cite{Jacobson1995} | Faulkner–Speranza 2024 (non-perturbative GSL), Kirklin 2025 | \cite{FaulknerSperanza2024,Kirklin2025} in bib. No RAG cache entry for Jacobson1995 (standard reference — no issue). |
| A3 | Cryptographic Censorship: ε-approximate k-design ⇒ horizon in bulk (conjecture, original proof in AdS/CFT) | Engelhardt–Folkestad–Levine–Verheijden–Yang 2024 (arXiv:2402.03425) | \cite{CryptoCensorship} | Ma–Huang 2025 on PRUs | ✓ RAG INDEX has the primary passage. Paper itself flags A3 as "working conjecture" for the cosmological extension — honest. |
| A3 (PRU existence) | Effective pseudorandom unitaries exist | Ma & Huang 2025 | \cite{MaHuang2025} | Haferkamp 2022 | \cite{Haferkamp2022} in bib as support. |
| A4 (φ: axion-like EDE) | V_φ = m² f² [1 − cos(φ/f)]³, z_c ~ 3500 | Poulin–Smith–Karwal–Kamionkowski 2019 (arXiv:1811.04083) | \cite{Poulin2019} | Poulin–Smith 2026 (arXiv:2505.08051); ACT DR6 results in Calabrese2025 | ✓ RAG INDEX has Poulin2019 verbatim. |
| A4 (χ: NMC thawing quintessence) | V_χ = V_0 e^{−αχ/M_P} + ξ_χ R χ²/2 | Ye et al. 2025 (arXiv:2407.15832) [DESI hint]; NMC framework to Faraoni 2004; PPN to Chiba 1999 (gr-qc/9903094) | \cite{Ye2025,Wolf2025,PanYe2026,Faraoni2004,Chiba1999} | Pan–Ye 2026 (arXiv:2503.19898), Wolf et al. 2025 (arXiv:2504.07679) | ✓ All three in RAG. |
| A4 (EDE–thawing degeneracy) | Joint (φ,χ) prior degenerate in BAO+SN | Wang & Piao 2025 | \cite{WangPiao2025} | — | In bib. Not in RAG cache, but claim is cited correctly to a primary source. |
| A5 | Dark Dimension species-scale cutoff Λ_sp(H) = M_P (H/M_P)^{c'}, c' = 1/6 | Montero–Vafa–Valenzuela 2022 (arXiv:2205.12293) | \cite{Montero2022} | Anchordoqui–Antoniadis–Lüst 2023 (arXiv:2306.16491), AAL 2025 (arXiv:2501.11690), Bedroya et al. 2025 (arXiv:2507.03090 — "Evolving Dark Sector") | ✓ RAG has Montero2022 species-scale passage verbatim. \cite{AAL2023,AAL2025} and \cite{Bedroya2025} in bib. NOTE: `Bedroya2025` bibkey currently points to arXiv:2503.19898, which is actually **Pan & Ye** — the V1 attribution warning in RAG INDEX is confirmed. v4.3 bib audit reported this cleaned; re-verify in v4.5. |
| A5 (de Sitter slope) | c' ≃ 0.05 de-Sitter-conjecture convention (used for comparison only) | Ooguri–Vafa 2007 (hep-th/0605264), Obied–Ooguri–Spodyneiko–Vafa 2018 (arXiv:1806.08362) | \cite{OoguriVafa2007,AAL2025} | Bedroya–Vafa 2019 (TCC, arXiv:1909.11063) | ✓ RAG has OoguriVafa2007 + OOSV2018 verbatim. (BedroyaVafa2019 also cached.) |
| A5 (N_eff bound) | N_eff = 2.86 ± 0.13 from ACT DR6 | Calabrese et al. 2025 (DR6 extended cosmology; arXiv in RAG as DEHK2025b = 2503.14454) | \cite{Calabrese2025} | — | In bib. \cite{DEHK2025b} is the DR6 paper (same collaboration output). |
| A6 | PH_k topological-data diagnostic of f_NL; at leading order reduces to Matsubara genus H_3(ν) shift | Matsubara 2003 (genus statistic; correct arXiv ID UNLOCATED — see below) | \cite{Matsubara2003} | Yip–Biagetti–Starck 2024 (arXiv:2403.13985), Calles 2025 | ✓ Yip2024 in RAG. **FLAG**: `Matsubara2003` primary ref has a known arXiv-ID problem (RAG INDEX: user-provided `astro-ph/0305472` is a different paper, Rossa & Dettmar). The bibkey and journal (Matsubara ApJ 584, 1–33, 2003) are consistent with the correct physics paper; the `eprint` field in `eci.bib` should be cross-checked or removed until the correct ID is located. This is the single unresolved bib-ID issue in the literature map. |

---

## Phenomenology (§3.1 – §3.6)

### §3.1 — DESI DR2 dark energy

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| DESI DR2 w_0 ≈ −0.75, w_a ≈ −0.86, 2.6–3.9σ preference over ΛCDM | DESI Collaboration 2024 (arXiv:2503.14738) | \cite{DESIDR2} | — | ✓ RAG has DESIDR2 verbatim. |
| NMC thawing crosses w = −1 without ghost | Barceló & Visser 2000 (no-ghost phantom crossing) | \cite{BarceloVisser2000} | — | In bib. |
| Scherrer–Sen w_a/(1+w_0) ∈ [−1.5, 0] at minimal coupling | Scherrer & Sen 2008 (arXiv:0712.3450) | \cite{ScherrerSen2008} | — | ✓ RAG has ScherrerSen2008 verbatim. |
| NMC slope must be computed numerically | Sánchez 2025 | \cite{Sanchez2025} | — | In bib. Not in RAG; cited as secondary. |
| NMC DESI DR1 phantom-crossing hint | Ye et al. 2025 (arXiv:2407.15832) | \cite{Ye2025} | Pan & Ye 2026 (arXiv:2503.19898), Wolf 2025 (arXiv:2504.07679) | ✓ All three in RAG. |

### §3.2 — Hubble tension

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| EDE resolves H_0 tension, f_EDE = 0.09 ± 0.03 | Poulin–Smith–Karwal–Kamionkowski 2019 (arXiv:1811.04083) | \cite{Poulin2019,PoulinSmith2026} | Poulin–Smith 2026 (arXiv:2505.08051) | ✓ both in RAG. |
| ACT DR6 + DESI DR2 + Planck + Pantheon+ combined H_0 = 71.0 ± 1.1 km/s/Mpc | Calabrese et al. (ACT DR6 extended cosmology) | \cite{Calabrese2025} | — | In bib; overlaps with DEHK2025b. |

### §3.3 — Cosmological constant

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| Exponential V_χ = V_0 e^{−αχ/M_P} has dS attractor for α ≤ √2 | Halliwell 1987; Copeland–Liddle–Wands 1998 | \cite{Halliwell1987,CopelandLiddleWands1998} | — | In bib (Halliwell1987 added in v4.3 per bib audit). v4.4 plan schedules D12 attractor script. |
| Swampland Distance Conjecture compatibility | Ooguri–Vafa 2007 (hep-th/0605264) | \cite{OoguriVafa2007} | — | ✓ RAG. |

### §3.4 — Dark matter

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| Dark Dimension KK tower as DM candidate, m ~ meV, ℓ ∈ [0.1, 10] μm | Montero et al. 2022 (arXiv:2205.12293) | \cite{Montero2022,AAL2023} | AAL 2023 (arXiv:2306.16491), AAL 2025 (arXiv:2501.11690) | ✓ Montero2022 RAG passage directly gives ℓ ~ 10⁻⁶ m. |
| ACT DR6 fifth-force / N_eff constraint | Calabrese 2025 | \cite{Calabrese2025} | — | In bib. |
| LLR Ġ/G = (−5.0 ± 9.6)×10⁻¹⁵ yr⁻¹ | Biskupek–Müller–Torre 2021 | \cite{Biskupek2021} | — | In bib. |

### §3.5 — Solar-system + DESI constraints on ξ_χ (`section_3_5_constraints.tex`)

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| γ−1 from NMC scalar-tensor; PPN γ−1 = −F'²/[ZF + (3/2)F'²] | Damour–Esposito-Farèse 1993 (PRL 70, 2220) and DEF 1996 (PRD 54, 1474; arXiv:gr-qc/9602056); also Chiba 2003 (Phys. Lett. B 575, 1); Hwang–Noh 2005 (PRD 71, 063536) | \cite{DamourEspositoFarese1993} (in bib) | — | ✓ DEF1996PRD in RAG. DEF1993PRL has no arXiv — paywalled PRL; framework is fully in DEF1996PRD. Consistent with our §3.5 line-20 prose citation. |
| Chiba 1999 NMC-PPN bound |ξ| ≲ 10⁻² | Chiba 1999 (arXiv:gr-qc/9903094) | \cite{Chiba1999} | — | ✓ RAG has Chiba1999 verbatim including exactly this bound statement. |
| Cassini |γ−1| ≲ 2.3×10⁻⁵ | Bertotti–Iess–Tortora 2003 | \cite{BertottiIessTortora2003} | — | In bib. |
| Thawing-quintessence slow-roll w(a) ∝ CPL | Scherrer & Sen 2008 (arXiv:0712.3450) | \cite{ScherrerSen2008} | — | ✓ RAG. |
| DESI DR2 covariance (σ_w0, σ_wa, ρ) reconstruction via pivot identity | DESI Collaboration 2024 (arXiv:2503.14738) | \cite{DESIDR2} | — | ✓ RAG; reconstruction procedure in D10. |
| DESY5 SNe combination | DESY5 collaboration | \cite{DESY5} | — | In bib. |
| DESI DR3 forecast σ(w_a) ~ 0.07 | DESI forecast document | \cite{DESIForecast} | — | In bib. |
| NMC Bayes factor log(B) = 7.34 ± 0.6 favouring non-minimal coupling | Wolf et al. 2025 (arXiv:2504.07679) | \cite{Wolf2025} | — | ✓ RAG. |
| Pan–Ye NMC DESI DR2 3σ signal | Pan & Ye 2026 (arXiv:2503.19898) | \cite{PanYe2026} | — | ✓ RAG (same PDF as Bedroya2025). |

### §3.6 — Swampland × NMC cross-constraint (`section_3_6_swampland_cross.tex`)

| claim | primary ref | cited as | recent | notes |
|---|---|---|---|---|
| Species-scale cutoff Λ ~ M_P (H/M_P)^{c'} | Montero–Vafa–Valenzuela 2022 (arXiv:2205.12293) | \cite{Montero2022} | Anchordoqui–Antoniadis–Lüst 2023 (arXiv:2306.16491) | ✓ RAG Montero2022 Eq. 2.2 passage verified. |
| AAL low-scale gravity refinement | AAL 2023 | \cite{AAL2023} | — | ✓ RAG. |
| Bedroya "evolving dark sector" cross-check | Bedroya et al. 2025 (arXiv:2507.03090) | (original paper uses \cite{Bedroya2025}; V1-D8 audit flagged the bibkey → wrong arXiv ID 2503.19898; HISTORICAL: paper footer now notes "Bedroya2025 removed per V1-D8 audit") | — | **FLAG**: §3.6 prose comment (line 164) states the erroneous citation was removed. Verify in v4.5 that no active `\cite{Bedroya2025}` remains in §3.6 body. A grep (2026-04-22) confirms `Bedroya2025` is only cited in `eci.tex` main-body (§ A5), not in section_3_6 main body — the comment-block residual is a historical note. OK. |

---

## Summary

- Claims mapped: **29** (A1..A6 with sub-claims = 11; §3.1 = 5; §3.2 = 2; §3.3 = 2; §3.4 = 3; §3.5 = 9; §3.6 = 3 — counts inclusive of sub-items listed above).
- Claims with a primary reference present in `eci.bib`: **29 / 29** (100%).
- Claims with verbatim RAG-confirmed passage: **~20** (all domains where the
  RAG INDEX was built in v4.2.1).
- Flags (not missing refs, but bibkey/ID hygiene):
  1. `Matsubara2003` — bibkey correct, but the arXiv eprint field may
     mis-point to Rossa & Dettmar (RAG INDEX warning). **Priority: LOW**;
     paper-year-journal fields are correct.
  2. `Bedroya2025` — bibkey currently maps to arXiv:2503.19898 which is
     actually Pan & Ye (NMC DESI). Both §3.6 prose and v4.3 bib audit
     flag this. The comment block in section_3_6 says the erroneous
     citation was removed from §3.6 body; the key still appears in
     §A5 prose and needs a bib-side repoint to `Bedroya2025DS` = arXiv:2507.03090
     ("Evolving Dark Sector"). **Priority: MEDIUM** for v4.5.
  3. No other claim lacks a primary reference.

### Recommendations for v4.5

1. **Repoint `Bedroya2025` bibkey** in `eci.bib` from arXiv:2503.19898 to
   arXiv:2507.03090 ("Evolving Dark Sector"), OR rename the key to
   `Bedroya2025DS` and update the §A5 `\cite{Bedroya2025}` accordingly
   (the task spec forbids editing `eci.bib` in this audit pass, so this
   is deferred to v4.5).
2. **Verify `Matsubara2003` arXiv eprint field**; if incorrect, remove the
   `eprint` entry but keep journal/year/DOI.
3. Optional: add a RAG-cache entry for `Jacobson1995`, `BarceloVisser2000`,
   and `Halliwell1987` to close the verbatim-passage coverage gap for
   A2 and §3.3.
4. Optional: pull `DEF1993PRL` from the American Physical Society via DOI
   to the RAG cache (paywalled, but short; the framework already has
   verbatim coverage through DEF1996PRD).
