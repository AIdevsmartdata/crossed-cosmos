# Adversarial review — v4.2.1 §3.5 + §3.6

**Reviewer**: independent adversarial agent (no prior context).
**Date**: 2026-04-22
**Commits attacked**:
- `1d74e17` v4.2.1:rewrite: §3.5 caveat 4 with real DR2+DESY5 covariance
- `4c31c76` v4.2.1:rewrite: §3.6 Swampland×NMC with c'=1/6 species scale
- `d3cf8df` v4.2.1:rewrite: predictions row 1b updated for DR2+DESY5 σ(w_a)=0.215
- `4cefeb6` v4.2.1:notes: vague 2 execution summary

## Verdict
SHIP

## Issues found
### CRITICAL (must fix before tag)
None.

### MAJOR (should fix before tag)
None.

### MINOR (can fix in v4.3 instead)
- **M1.** §3.6 contains zero active `\cite{}` calls; the two load-bearing references (Montero-Vafa-Valenzuela 2205.12293 and Anchordoqui-Antoniadis-Lüst 2306.16491) are cited by inline arXiv number with `% TODO-BIB` markers. Already flagged in `_v4.3_review_notes.md` §"Markers left in source". Must be promoted to real `\cite{}` before submission, but non-blocking for the v4.2.1 tag since the claim is verifiable from the arXiv IDs in-text.
- **M2.** `section_3_5_constraints.tex:90,113` refer to "DESI DR2 + CMB + DESY5" contours without a `\cite{DESY5}` (comment-only TODO-BIB at line 95). Minor — DESIDR2 citation is present and the DESY5 compilation is standard.
- **M3.** §3.5 Caveat 3 quotes "$\sigma(w_p)_\mathrm{pred}=0.0257$ vs quoted $0.024$, $\sim 7\%$ residual". The ratio is 7.1% — fine, but the residual is a covariance-reconstruction systematic that is not separately propagated into the 3.29σ figure. The caveat says it is "well below" the tension; quantitatively, a 7% widening of σ(w_a) would drop the Mahalanobis by roughly 3%, i.e. 3.29σ → ~3.19σ. Minor — unchanged conclusion.
- **M4.** Figure `D8-c-xi-overlap.pdf` still marks c'=0.05 as primary per the `% FIGURE-UPDATE-PENDING` marker, inconsistent with the boxed c'=1/6 text. Already flagged; deferred to v4.3.
- **M5.** §3.5 line 155: "band of half-width $\sim 4\%$ of $\sigma_{w_a}$". Exact value is 8.8e-3/0.215 = 4.09% (the text in row 1b and Caveat 4 both round to "$\sim 4\%$"). Consistent.

## Numerical re-derivations

All arithmetic was redone from scratch in Python (stdlib + numpy/scipy for linear algebra); results match the paper to the reported precision.

| Item | Claim | Recomputed | Verdict |
|---|---|---|---|
| 1. Λ = M_P (H₀/M_P)^(1/6) | 2.2×10⁸ GeV | 2.230×10⁸ GeV (H₀=67.4 km/s/Mpc ⇒ 1.438×10⁻⁴² GeV; M_P=2.435×10¹⁸ GeV) | ✓ |
| 2. (Λ/χ₀)² at χ₀=M_P/10 | 8.4×10⁻¹⁹ | 8.389×10⁻¹⁹ | ✓ |
| 3. log₁₀(2.4e−2 / 8.4e−19) | "16 orders" | 16.46 | ✓ |
| 4a. Scherrer–Sen Mahalanobis | 3.33σ | 3.321σ (min over w₀ of (Δ,Δ)·C⁻¹·(Δ,Δ)^T with w_a=−1.58(1+w_0)) | ✓ |
| 4b. ECI band Mahalanobis | 3.29σ | 3.279σ (min over (w₀,ξ) with \|ξ\|≤0.024) | ✓ |
| 4c. ΛCDM Mahalanobis (sanity) | — | 4.36σ | consistent with 2σ exclusion of ΛCDM in DR2+DESY5 |
| 5. Phantom crossing | DR2+DESY5 prefers w<−1 at high-z | w(a=0)=w₀+w_a=−1.61<−1; w₀=−0.752>−1 → crossing required | ✓ |
| 15. Row 1b "~4%" | 4% | 8.8e−3/0.215 = 4.09% | ✓ |
| — | B(0.7)=(8/√3)·A | 7.30 | 7.298 ✓ |
| — | Δw_a = B·ξ_max·√(1+w₀)·χ₀/M_P at w₀=−0.75 | 8.8×10⁻³ | 8.76×10⁻³ ✓ |

Covariance used: σ(w₀)=0.057, σ(w_a)=0.215, ρ=−0.89; mean (−0.752,−0.86). Condition number of C is modest; inversion stable.

## Citation audit

| Key | In eci.bib? | Supports claim? |
|---|---|---|
| BarceloVisser2000 | yes | accepted (no-ghost analysis — standard reference) |
| BertottiIessTortora2003 | yes | yes (Cassini γ−1 bound) |
| Biskupek2021 | yes | accepted (LLR Ġ/G) |
| DESIDR2 | yes | yes (Eq. 28 pivot data) |
| DESY5 | **no** | flagged as TODO-BIB at :95 — minor |
| PanYe2026 | yes | accepted (NMC thawing literature context) |
| ScherrerSen2008 | yes | yes (thawing track A=1.58) |
| Wolf2025 | yes | claim of ξ(χ₀/M_P)²≤6×10⁻⁶ attributed to "their Eq. (2)"; accepted — bib audit previously performed |
| Ye2025 | yes | accepted (NMC literature context) |
| Chiba1999 | yes | PPN \|ξ\|≲10⁻² for ξRχ² quintessence — matches abstract of gr-qc/9903094 as typically cited |
| Bedroya2025 | yes (but not cited in final §3.6 — removed per V1 audit) | n/a |

No missing `\cite` keys in live LaTeX; only comment-level TODO-BIB markers.

## Structural / logical checks

- **C6 (heuristic framing).** Word "heuristic" appears three times in §3.6 prose (lines 52, 61, Caveat 1), not merely in a `%` comment. Requirement met.
- **C7 (choice framing).** "Three resolutions compatible with the axioms... Our primary analysis proceeds under choice (i)" (lines 93–116). Clearly framed as model-building choice, not derivation.
- **C8 (Caveat 4 wording).** Prose states "not a specific failure of ECI" and "joint statement about the entire class of conservative (non-phantom) thawing models" — the weaker, correct claim. Does not overreach to "ECI is therefore fine".
- **C13 (consistency of (i)).** §3.5 nowhere invokes bulk/KK identification; coupling is treated as a 4D operator with cosmological χ₀. Consistent with choice (i) in §3.6.
- **C14 (Cassini vs ghost-crossing).** At ξ_max=2.4×10⁻² and χ₀=M_P/10, ξ_χ(χ₀/M_P)² ≤ 2.4×10⁻⁴. The prose correctly asserts this is far short of the O(1) needed for genuine phantom crossing under Barcelo-Visser. No sleight-of-hand.
- **C16 (same χ₀).** χ₀=M_P/10 used identically in §3.5 (line 51) and §3.6 (line 68). ✓
- **C17 (metric signature).** Kinetic and NMC signs compatible with mostly-plus. No inconsistency detected.

## Recommendations for tag

**SHIP.** Proceed to `v4.2.1` tag + release. All load-bearing numbers reproduce to stated precision; prose correctly frames the δM_P²≤Λ² condition as heuristic; Caveat 4 correctly distinguishes joint-thawing-problem from ECI-specific failure; citations resolvable. The six markers flagged in `_v4.3_review_notes.md` (TODO-BIB for DESY5 / Montero2022 / AAL2023 / DESIForecast; TODO-DERIV for D8 script; FIGURE-UPDATE-PENDING) are all known-and-tracked minor debt for v4.3 and do not affect the scientific claims of v4.2.1.
