# ECI internal knowledge index

**Purpose.** Single point of truth for every derived number, adversarial
verdict, open caveat, and rejected approach in the ECI paper. Consult
before writing any claim.

**Last refresh.** 2026-04-21, covering repo state through commit `6b93377`
(v4.6 in progress, §3.7 perturbations landed).

**Read the `README.md` in this directory first if you are a new agent.**

---

## Section 1 — Derivation results (D1..D15)

Status legend: **PASS** = derivation complete, numerics & asserts green,
independent verification has landed where applicable. **PARTIAL** =
result holds in a restricted regime or relies on a heuristic that the
authors have flagged. **SCAFFOLD** = code/plan exists but the numerical
output has not been lifted into the paper as a load-bearing claim.

Confidence legend: **HIGH** = textbook, symbolically verified, or
independently cross-checked. **MEDIUM** = single-derivation, plausible,
no external cross-check. **LOW** = heuristic, flagged in the paper,
subject to O(1) uncertainty.

| ID | Claim (short) | Value (with error where available) | Status | File | Confidence |
|----|---------------|------------------------------------|--------|------|-----------|
| D1 | NMC Klein–Gordon background integration (ξχ² R/2) | scaffold — used as backbone for D4/D9/D13 | SCAFFOLD | `derivations/D1-kg-nmc.py`, `_results/D1-kg-nmc.log` | HIGH (code) |
| D2 | NMC stress-tensor T_μν^(χ) convention audit | Faraoni Eq. 2.12–2.13 sign convention `+ξ` on r.h.s. after transfer | PASS | `derivations/D2-stress-nmc.py`, `_results/D2-stress-nmc.log` | HIGH (symbolic, audited in `convention_audit.md`) |
| D3 | No-ghost kinetic matrix sign | `Q_T = (M_P² − ξχ²)/2 > 0` ⇒ `ξχ²/M_P² < 1` | PASS | `derivations/D3-noghost.py`, `_results/D3-noghost.log` | HIGH (textbook; Faraoni 2004 Eq. 2.16 reproduced symbolically) |
| D4 | NMC correction to matter-era Scherrer–Sen coefficient | `A(0)=24/7` recovered; `δ_ξ = 8ξχ/(αM_P)` heuristic | PASS | `derivations/D4-wa-w0-nmc.py`, `_results/D4-wa-w0-nmc.log` | MEDIUM (heuristic matter-era scaling; superseded by D9/D13 numerics) |
| D5 | Persistent-homology Euler characteristic pipeline | scaffold + figure `D5-euler-char.pdf`; paper §A6 quotes Matsubara form only | SCAFFOLD | `derivations/D5-persistent-homology.py`, `_results/D5-persistent-homology.log` | MEDIUM (code runs; quantitative result not lifted) |
| D6 | ΔN_eff from KK tower | scaffold — log only, no summary JSON, no paper row | SCAFFOLD | `derivations/D6-deltaNeff-kk.py`, `_results/D6-deltaNeff-kk.log` | LOW (unlifted; values not audited into paper) |
| D7 | PPN γ−1 for NMC, Cassini bound on ξ_χ | **\|ξ_χ\|(χ₀/M_P) ≤ 2.4×10⁻³**; at χ₀=M_P/10 ⇒ **\|ξ_χ\| ≤ 2.4×10⁻²** | PASS | `derivations/D7-report.md`, `derivations/D7-ppn-xi-bound.py` | HIGH (Chiba 1999 / Damour–Esposito-Farèse 1993 / Wolf 2025; symbolic ξ→0 limit checked; V6 cross-model DISAGREE on functional form resolved in our favour — see §4 below) |
| D7 | Scherrer–Sen NMC extension, analytic `B(Ω_Λ)` | `w_a = −A(Ω_Λ)(1+w₀) + B(Ω_Λ) ξ_χ √(1+w₀)(χ₀/M_P)`; `A(0.7)=1.58`, **`B(0.7)=7.30`** (heuristic `(8/√3)·A`) | PASS | `derivations/D7-report.md`, `D7-ppn-xi-bound.py` | MEDIUM (heuristic propagation from matter-era; validated by D9 numerically within 12.5 %, and by D13 flatter form; paper Caveat 2 flags this explicitly) |
| D7 | ECI half-band in w_a at χ₀=M_P/10, w₀=−0.75 | `Δw_a^ECI ≈ 8.8×10⁻³` = 4.09 % of σ(w_a)=0.215 (DR2+DESY5) | PASS | `D7-report.md`; cross-checked `_adversarial_review_v4_2_1.md` item 15 | HIGH (arithmetic, three-decimal agreement on independent re-derivation) |
| D8 | Swampland × NMC cross-constraint at c'=1/6 (species scale) | **`\|ξ_χ\| ≲ 8.4×10⁻¹⁹`** at χ₀=M_P/10, H₀=1.44×10⁻⁴² GeV, M_P=2.44×10¹⁸ GeV | PASS | `derivations/D8-report.md`, `D8-swampland-nmc-cross.py` | MEDIUM — arithmetic HIGH, but rests on **heuristic** `δM_P² ≤ Λ²` (labelled as such in §3.6 main text, not only in footnote); V6 agrees to within factor 2.5; V1 audited and forced relabelling (see §4) |
| D8 | Swampland × NMC at former value c'=0.05 | `\|ξ_χ\| ≲ 9.5×10⁻⁵` | **DEMOTED** (retained only as parenthetical comparison) | `D8-report.md` table, `section_3_6_swampland_cross.tex` parenthetical | LOW — c'=0.05 has no pedigree in the Dark-Dimension literature (V1 finding R2) |
| D9 | Numerical validation of B(0.7) via full NMC-KG integration | **`B_num = 8.21 ± 0.49`** vs `B_analytic = 7.30`, ratio 1.125 (within 30 % tolerance) | PASS | `derivations/D9-report.md`, `D9-wa-numerical.py`, `_results/D9-summary.json` | HIGH (independent scipy LSODA integration, 15 trajectories, all succeeded) |
| D9 | A(0.7) numerical vs Scherrer–Sen | `A_num = 1.478` vs `A_analytic = 1.58`, 6.4 % deviation | PASS | same | HIGH — deviation uniform across α, attributed to IC / CPL-fit window; immaterial for B slope |
| D9 | Local B(χ₀) non-linearity | `B_local ≈ 14, 9.5, 7.3` at χ₀/M_P = 0.05, 0.10, 0.20 | PASS (flagged) | `D9-report.md` "Caveat — χ₀ non-linearity" | MEDIUM — D7 analytic `Δw_a ∝ χ₀` exact-linearity is broken sub-leading; worst-case bumps the band by 12–30 % — does **not** change DR2/DR3 verdict |
| D10 | DESI DR2 DESY5 reconstructed 2×2 covariance | σ(w₀)=0.057, σ(w_a)=0.215 (sym), z_p=0.31, **ρ(w₀,w_a) = −0.893** (reconstructed via pivot identity) | PASS | `derivations/D10-report.md`, `D10-desi-covariance.py`, `_results/D10-summary.json` | HIGH — pivot-minimisation identity, reproduces published σ(w_p)=0.024 to 7 % (D10 0.0257, V2 0.0257); V2 independently reproduced ρ to 4 decimals |
| D10 | Mahalanobis distance of ECI NMC band from DR2+DESY5 mean | **`d_min = 3.29σ`** (2-dof), just inside the Scherrer–Sen locus at **3.33σ**; ΛCDM itself at 4.36σ | PASS | `D10-report.md`; V2 re-derivation matches to ≤ 0.01σ | HIGH |
| D10 | Old D7 mis-covariance value (superseded) | `d_old ≈ 0.79σ` under σ_wa=0.80 "inside-1σ" framing | **CORRECTED** — Caveat 4 of §3.5 re-written | `_v4.3_review_notes.md`; `_adversarial_review_v4_2_1.md` | HIGH (superseding claim; see §4) |
| D11 | No-ghost proof of Barcelo–Visser inequality | margin **0.99976** at Cassini fiducial (ξ=2.4×10⁻², χ=M_P/10); margin **≈ 1 − 8.4×10⁻²¹ ≈ 1** at Swampland fiducial | PASS | `derivations/D11-no-ghost-proof.py`, `_adversarial_review_v4_4_0.md` Part A | HIGH (5 PART asserts pass, sympy difference with Faraoni Eq. 2.16 = 0) |
| D12 | Exponential-potential attractor w_φ(α) | `w_φ(α=0)=−1`, `w_φ(α=√2)=−1/3`, `w_φ(α=√3)=0` — accelerating iff α²<2 | PASS | `derivations/D12-alpha-attractor.py`, `_adversarial_review_v4_4_0.md` Part B | HIGH (Copeland–Liddle–Wands 1998 Table I, Halliwell 1987) |
| D13 | Numerical `B(Ω_Λ)` on full NMC-KG background | `B_num = {9.00, 9.18, 9.05, 8.11}` at Ω_Λ={0.5,0.6,0.7,0.8}, σ≈1.1 per point | PASS | `derivations/D13-wa-numerical-full.py`, `_results/D13-summary.json` | HIGH numerics; MEDIUM interpretation — shape *flatter* than heuristic `(8/√3)·A={10.85,8.96,7.30,5.68}`; explicitly flagged in §3.5 Caveat 2 |
| D13 | A_num/A_analytic at Ω_Λ=0.7 | 1.34 vs 1.58 (15.3 % offset, purely multiplicative) | PASS | `_adversarial_review_v4_5_0.md` item 3 | MEDIUM — offset does **not** propagate into B slope (slope extraction is scale-invariant) |
| D13 | Cassini-rescaled worst-case Δw_a | `1.10×10⁻²` at w_loc=−0.9 → w₀=−0.75 after √((1+w₀)/(1+w_loc)) = 1.581 rescale | PASS | `_adversarial_review_v4_5_0.md` item 4 | HIGH (arithmetic exact) |
| D14 | Linear perturbation observables G_eff(k,a), η(k,a), fσ₈ | `G_eff/G_N − 1 = x + O(x²)`, `x ≡ ξχ²/M_P²`; `η − 1 = O(x²)`; max `\|Δfσ₈/fσ₈\| ≤ 0.41 %` at Cassini-saturated ξ | PASS | `derivations/D14-nmc-perturbations.py`, `_results/D14-summary.json`, `paper/section_3_7_perturbations.tex` | HIGH — BEFPS00 (gr-qc/0001066) sub-horizon quasi-static reproduction; below Euclid/LSST-Y10 1 %/bin target → **not detectable** in near-future LSS |
| D15 | Minimum chameleon-like screening profile for §3.6 Res(ii) | **α_min = 0.095**, **ρ_c,min = 1.33×10⁻⁸ g/cm³**; Θ(ρ_cluster)=0.985 | PASS | `derivations/D15-screening-profile.py`, `_results/D15-summary.json` | MEDIUM — **the chameleon parametrisation Θ(ρ)=exp[−(ρ/ρ_c)^α] is a choice, not a theorem**. Khoury–Weltman 2004 band [0.125, 0.333] brackets α_min, so structurally compatible; ρ_c is a fit to two ceiling-floor anchors, not derived from a UV theory |

### Notes on the table

- "HIGH" does **not** mean unassailable; it means "either textbook, symbolically
  verified, or independently reproduced by another agent / script to the
  precision quoted." Disagreements with external models (e.g. V6 Claim 1) are
  logged in §4 when they have been resolved in our favour.
- "MEDIUM" is used for single-derivation numerics and for heuristic
  propagations that the paper openly flags (not hidden).
- "LOW" is used where the result has been explicitly demoted or where
  no audit has landed. A LOW label is a flag to future agents to either
  upgrade the derivation or avoid the claim.
- `D5` and `D6` carry SCAFFOLD status: the code exists but no summary JSON is
  emitted and the paper does not rely on a specific numerical output from
  them. Either lift or retire before v5.0.

---

## Section 2 — Adversarial and peer-review log (chronological)

| Date | Reviewer | Target | Verdict | Critical findings | File |
|------|----------|--------|---------|-------------------|------|
| 2026-04-21 | V1 (Opus 4.7, independent) | D8 Swampland × NMC, §3.6 | **FRAGILE** | (1) c'=0.05 has no DD pedigree; correct species scale c'=1/6. (2) `Bedroya2025` → arXiv:2503.19898 is a DESI NMC paper, not a Swampland ref — **misattribution**. (3) `δM_P² ≤ Λ²` is heuristic, not a theorem. R1/R2/R3/R4 issued; ALL absorbed in v4.2.1. | `derivations/V1-D8-verification.md` |
| 2026-04-21 | V2 (Opus 4.7, independent) | D10 DR2 covariance reconstruction | **SOLID** | Re-extracted Eq. (28) + pivot from cached PDF; ρ reproduced to 4 decimals, Mahalanobis to ≤ 0.01σ. 7 % residual on σ(w_p)_pred honestly flagged. No published 2×2 cov file available. | `derivations/V2-D10-verification.md` |
| 2026-04-21 | V6 (Mistral Large) | Four D7/D8/D12 claims | **MIXED (tending SOLID)** | 3/4 full/partial agreement; Claim 1 (PPN γ−1) DISAGREE on functional form — Mistral's **linear-in-ξ** is the graviton-only dressing (Chiba 1999 / Faraoni 2000 literature backs **our quadratic**). Recommended Chiba cite added. | `derivations/V6-mistral-cross-check.md`, `derivations/V6-mistral-cross-check.py`, `_mistral_responses/claim_{1..4}.txt` |
| 2026-04-21 | V6b (Mistral Magistral-medium, reasoning) | Same four claims + CoT | scripts only, raw responses in `_mistral_responses/` | Not written up as a verdict file; used as a secondary read on V6. | `derivations/V6b-magistral-cross-check.py` |
| 2026-04-22 | Vx-adv v4.2.1 (Opus 4.7, independent; named reviewer id not recorded) | §3.5 caveat 4 + §3.6 c'=1/6 rewrite + row 1b | **SHIP** | 0 critical, 0 major, 5 minor (bib hygiene, figure update pending, 7 % σ(w_p) systematic noted as 3.29σ → ~3.19σ bound). All numerics reproduced independently in Python. | `paper/_adversarial_review_v4_2_1.md` |
| 2026-04-22 | Vx-adv v4.3.0 | Axioms + equations + conventions + bib polish (9 commits) | **FIX** (one 5-line patch) | Four orphaned bib entries (`AAL2023`, `DESY5`, `DESIForecast`, `Matsubara2003` where in-text was `% TODO-BIB` *comment*). No physics bugs. Post-patch: SHIP. | `paper/_adversarial_review_v4_3_0.md` |
| 2026-04-21 | Vx-adv v4.4.0 (Opus 4.7) | D11, D12, equation_map, convention_audit, literature_map (5 commits) | **SHIP** | 0 BLOCK, 0 MAJOR. 3 MINOR: stale v4.2.1 warnings in `literature_map.md`; "dS attractor α≤√2" loose phrasing (D12 self-flags); full `1+6ξ²χ²/(M_P²−ξχ²)` correction omitted (negligible at fiducial, appendix-worthy for v5.0). | `paper/_adversarial_review_v4_4_0.md` |
| 2026-04-21 | Peer v1 (Claude Opus 4.7 self + Gemini 2.5 Pro + Magistral-medium) | eci.pdf v4.4 | **MAJOR REVISIONS** (3/3 reviewers converge) | Weakest: **A3 cosmological transposition** (all three). Strongest: §3.5 NMC w_a phenomenology (Claude, Magistral) or §3.6 Swampland×NMC (Gemini). Suggested Q4 actions: joint χ²(ξ_χ,f_EDE), full linear perturbations, screening profile. | `paper/peer_pre_review.md` |
| 2026-04-21 | Peer v2 (GPT-5.4 + Gemini 3.1 Pro + Grok 4, via 1min.ai) | eci.pdf v4.5 (A3 dict landed) | **MAJOR REVISIONS** (3/3 reviewers converge) | Weakest still A3/toy-dictionary; GPT-5.4 asks to quarantine A3 out of the predictive core. Strongest: §3.6 Swampland×NMC (Gemini, GPT-5.4 — "the rare part that behaves like physics"); Grok picks f_EDE Hubble resolution. Q4 suggestions: full Jordan-frame perturbations (GPT-5.4 ⇒ D14 landed), min. screening profile (Gemini ⇒ D15 landed), closed-form w_a(w₀;ξ_χ) (Grok). | `paper/peer_pre_review_v2.md`, `paper/_peer_review_v2/*.md` |
| 2026-04-21 | V8-adv v4.5.0 (Opus 4.7 1M) | D13 + A3 toy-dictionary §5 landing (pre-tag) | **SHIP** | 0 BLOCK, 0 MAJOR. 1 MINOR: abstract still called A3 a "selection rule" while §5 had downgraded to "working conjecture with toy dictionary" — patched as v4.5.1 (commit `752408b`). Latex compiles 8 pages, 0 errors, 0 undefined refs. | `paper/_adversarial_review_v4_5_0.md` |
| 2026-04-21 | V10 (Magistral, adversarial) | Four fresh v4.6 prompts (D14 G_eff/η derivation, D14 fσ₈ shift, D15 screening minimum, A3 quarantine editorial decision) | **RAW claim-derivations, no verdict file written yet** | Claim 1 and Claim 2 both reproduce D14's leading-order G_eff/G_N − 1 = x with x ≡ ξχ²/M_P²; Claim 3 reproduces D15's two-anchor minimum. Claim 4 (A3 quarantine editorial decision) returns a qualitative "acceptable compromise, not a free pass". | `derivations/V10-magistral-adversarial.py`, `_mistral_responses/v10_claim_{1..4}.txt` |

### Reviewers V3, V5, V7 — not landed

No files named `V3-*.md`, `V5-*.md`, or `V7-*.md` exist in the repo.
Missing indices in the V-sequence are not silent failures; they are slots
that were planned and not executed. Do not infer a missing verdict from
their absence.

---

## Section 3 — Open caveats (what's still flagged)

**Legend.** `BLOCKING` = must be addressed before v5.0 submission.
`NON-BLOCKING` = tracked technical debt; does not hold back the tag.

### From live `.tex` markers (grep of `% TODO-BIB`, `% RAG-PENDING`, `% HEURISTIC`, `% TODO-DERIV`, `% FIGURE-UPDATE`, `% D10 CORRECTION`, `% TODO REMONDIERE`)

- `paper/eci.tex:68` — **`% RAG-PENDING resolved via algebraic derivation; see adversarial v4.3 re-check.`** (Montero2022 species-scale derivation). Reviewer Vx-adv v4.3.0 m3 asks for a one-line footnote, not blocking. **NON-BLOCKING.**
- `paper/section_3_6_swampland_cross.tex:39` — **`% TODO-DERIV: update D8 script for c'=1/6 primary case`** (flagged at v4.2.1, Vx-adv v4.2.1 M4). The c'=1/6 arithmetic is correct in the .tex body; the flag is about propagating to the D8 script as first-class. **NON-BLOCKING.**
- `paper/section_3_6_swampland_cross.tex:135` — **`% FIGURE-UPDATE-PENDING: regenerate for c'=1/6 as the primary marked`** (`D8-c-xi-overlap.pdf` still marks c'=0.05 as primary; Vx-adv v4.2.1 M4). **BLOCKING for v5.0** if the figure is kept in the published version — reader will see the wrong primary exponent.
- No `% HEURISTIC`, no live `% TODO REMONDIERE`, no live `% D10 CORRECTION` markers remain in the `.tex` sources as of HEAD. The `% D10 CORRECTION:` annotation referenced in `D10-report.md` §7 has been absorbed into the body text of Caveat 4 and is no longer tagged.

### From `paper/_v4.3_review_notes.md`

- σ(w_p) 7 % reconstruction residual ⇒ 3.29σ → ~3.19σ systematic if propagated
  fully. Flagged; not propagated into the headline number. **NON-BLOCKING** —
  does not change the "outside 2σ" conclusion.
- All V1 R1–R4 recommendations absorbed; no residual V1 item open.

### From `paper/_v4.5_A3_decision.md`

- A3 kept as axiom but §5 downgraded from "selection rule" to "working
  conjecture + toy dictionary". v4.6 step 1 (commit `775c184`) further
  quarantined §5 into **Appendix A "Speculative"**. Peer v2 converged on
  demanding exactly this; V10 Claim 4 notes the remedy is acceptable but
  not a blanket licence for speculative content elsewhere. **NON-BLOCKING**
  as of v4.6.

### Structural / open-science debt

- **No MCMC fit** on (ξ_χ, α, f_EDE, z_c) against DR2 BAO + Pantheon+ +
  Planck TT/TE/EE. Requested by all three peer-v1 reviewers (Claude Q4,
  Gemini Q4) and peer-v2 (GPT-5.4, Gemini, Grok). **BLOCKING** if the
  referee reads the paper as a quantitative dark-energy analysis;
  **NON-BLOCKING** under the EPJ C framework-paper genre declaration.
  Recommendation: state the scope limitation in the abstract before v5.0.
- **D11 full canonical-normalization factor** `1 + 6ξ²χ²/(M_P² − ξχ²)`
  not derived; negligible at fiducial (≈1.4×10⁻⁵) but a v5.0 robustness
  appendix is the honest fix. **NON-BLOCKING.**
- **D5 / D6 SCAFFOLD status**: no paper row depends on them today but the
  code sits unlifted. Either lift (with a D-report + summary JSON + audit)
  or delete before v5.0. **NON-BLOCKING but untidy.**
- **No published DESI DR2 2×2 covariance** — all three reconstructions
  (D10, V2, Vx-adv v4.2.1) rely on the pivot identity. If DESI later
  releases the real covariance and it differs meaningfully, the 3.29σ
  Mahalanobis number must be refreshed. **NON-BLOCKING, external
  dependency.**

### Count

**Open caveats: 8.** **Blocking v5.0: 1** (the `D8-c-xi-overlap.pdf`
figure primary-exponent update). Plus a **soft blocker** on the MCMC fit,
conditional on the referee's genre-reading of the paper.

---

## Section 4 — Known-wrong attempts / rejected approaches

These are things we tried and abandoned. Agents: do not re-propose without
an explicit new reason.

1. **Mistral Large's linear-in-ξ PPN formula (V6 Claim 1, DISAGREE).**
   Mistral derived `γ − 1 ≈ −ξ χ₀²/M_P²` via graviton-propagator dressing
   only (effective Planck mass in the Newtonian potential), yielding
   `\|ξ\| ≲ 4.4×10⁻³`. This is a known-incomplete sub-calculation: it
   omits the scalar-mediated fifth-force channel that enters the
   Damour–Esposito-Farèse 1993 / Chiba 1999 / Faraoni 2000 expression at
   O(ξ²). Our quadratic `γ − 1 = −4ξ²χ₀²/M_P²` is the canonical form.
   **Do not replace with the linear form.**

2. **`c' = 0.05` as the primary Swampland-cutoff exponent (V1 finding,
   REJECTED for v4.2.1).** c'=0.05 has no pedigree in the Dark-Dimension
   literature — it is borrowed from de-Sitter-slope / potential-slope
   bounds (Agrawal–Obied–Steinhardt–Vafa 1806.09718 style) that apply to
   `V ∼ e^{−c'χ/M_P}`, not to a species cutoff. The correct DD exponents
   are **c'_sp = 1/6** (species scale, Montero–Vafa–Valenzuela 2022) and
   **c'_KK = 1/2** (KK tower, Anchordoqui–Antoniadis–Lüst 2023). **v4.2.1
   uses c'=1/6 as primary**, with c'=0.05 demoted to a single
   parenthetical.

3. **`Bedroya2025` citation for the species-scale cutoff formula (V1
   finding, REJECTED).** The original attribution pointed at
   arXiv:2503.19898, which is a DESI DR2 NMC gravity paper, *not* a
   Swampland-species-scale reference. **Misattribution** — removed.
   Correct references now: Montero2022 (arXiv:2205.12293) + AAL2023
   (2306.16491).

4. **D7's original "inside the DR2 1σ contour" framing (D10 + V2,
   REJECTED).** D7 used an approximate diagonal-ish covariance
   (σ_w0=0.20, σ_wa=0.80, ρ=−0.80) that was **~4× too loose on σ_wa**
   and **~3.5× too loose on σ_w0**. Under the real DR2+DESY5 covariance
   the SS / ECI track lies **outside the 2σ contour (3.3σ)**, not inside
   1σ. The qualitative conclusion "ECI indistinguishable from minimal-
   coupling wCDM at DR2 precision" survives — but for the *opposite
   reason*: both are equally disfavoured at ~3σ under w₀-w_a CDM, not
   both in-tension with the data. Paper §3.5 Caveat 4 rewritten in
   v4.2.1.

5. **Orphaned bib entries from v4.3.0 (Vx-adv v4.3.0 M1, FIX-patched).**
   `AAL2023`, `DESY5`, `DESIForecast`, `Matsubara2003` were pushed into
   `eci.bib` before having `\cite{}` call-sites in `eci.tex`. BibTeX does
   not warn on orphans. The v4.3.0 FIX patch either wired each to the
   correct call-site or deleted the entry. Do not add bib entries before
   the call-site lands in the `.tex` source.

6. **V1 bug in D8 narrative (self-caught).** D8-report.md §3 states
   `δM_P² ≤ Λ²` as a theorem-like condition. V1 pointed out it is at
   best an order-of-magnitude EFT estimate. §3.6 now states "heuristic"
   three times in prose (lines 52, 61, Caveat 1), not just in a `%`
   comment. **Do not upgrade the heuristic status** without a genuine
   EFT-matching derivation.

7. **A3 as a "selection rule" in the abstract (V8-adv MINOR, FIXED in
   v4.5.1).** The abstract description "Cryptographic Censorship as a
   selection rule on admissible bulk geometries" was stronger than §5
   deserved after the toy-dictionary downgrade. Replaced with "working
   conjecture whose cosmological transposition is made explicit via a
   toy dictionary … (§5)". Commit `752408b`. Further quarantined to
   Appendix A in v4.6 (`775c184`).

8. **"dS attractor for α ≤ √2" loose phrasing (D12 self-flag + Vx-adv
   v4.4.0 MINOR 2).** α=√2 is the **accelerating** boundary (w_φ=−1/3),
   not the de Sitter point (w_φ=−1, α=0). §3.3 to be tightened in v5.0
   to "accelerating (quintessence) attractor for α<√2, de-Sitter limit
   α→0". Non-blocking but do not reintroduce the loose form.

9. **Stale `literature_map.md` warnings about `Bedroya2025` / `Matsubara2003`
   bib-key state (Vx-adv v4.4.0 MAJOR 11, FIXED in v4.5 cleanup).** Those
   warnings referred to pre-v4.2.1 bib state; they had been resolved but
   the `literature_map.md` prose was not updated. Document hygiene, not
   a content defect. Do not re-propagate the warnings.

10. **Attempting to claim A3 implies a cosmological k-design theorem
    (peer v1 + v2 consensus, REJECTED).** No pseudo-Riemannian analogue
    for one-sided modular reconstruction is known. All three v2 peer
    models (GPT-5.4, Gemini 3.1 Pro, Grok 4) plus all three v1 peers
    converged on this being the paper's single weakest element. The
    current toy-dictionary-in-Appendix-A framing is the minimum
    defensible posture. **Do not re-inflate A3's cosmological claims
    in the main body.**

---

*Generated 2026-04-21 by internal-rag aggregation agent. No `.tex`,
`.bib`, or `.py` files modified. Sources: `derivations/D*-report.md`,
`derivations/_results/D*-summary.json`, `derivations/V{1,2,6,6b,10}-*`,
`paper/_adversarial_review_v4_{2_1,3_0,4_0,5_0}.md`,
`paper/peer_pre_review{,_v2}.md`, `paper/_peer_review_v2/*.md`,
`paper/_v4.3_review_notes.md`, `paper/_v4.5_A3_decision.md`,
`paper/docs/REVIEW_NOTES.md`, live `.tex` marker grep.*
