# Adversarial review — v4.3.0 (axioms + equations + conventions + bib polish)

**Commits attacked** (9, in order):
- `f62ea1d` v4.3: add conventions subsection
- `5d0152c` v4.3: A5 carries species-scale equation
- `e8b8767` v4.3: A4 amendment — chi is 4D effective, decoupling choice flagged
- `d95c52b` v4.3: A6 carries Matsubara-Yip Euler-char equation
- `aa46ed3` v4.3: no-ghost prose derivation from kinetic matrix
- `4675b05` v4.3: alpha <= sqrt(2) attractor prose line
- `f3b114c` v4.3: docs — append v4.3.0 axioms+equations+conventions summary to REVIEW_NOTES
- `f0d3f2c` v4.3:bib: add 6 entries + DOI upgrades for Calabrese2025/Calles2025
- `28746a3` v4.3:bib: add Halliwell1987 + regenerate audit (0 critical, 1 minor)

**Date**: 2026-04-22.
**Reviewer**: adversarial agent (Opus 4.7, 1M).

## Verdict

**FIX** — ship-blockers are cosmetic, not physics, but four bib entries are orphaned (never `\cite{}`-d) and one `% TODO-BIB: Matsubara2003` comment sits next to an equation the cite was supposed to cover. Fixable in a single 5-line patch. No critical errors of physics, derivation, or citation attribution.

## Issues

### CRITICAL
_None._ All four new equations (A5 species scale, A6 Matsubara-Yip, no-ghost, α≤√2) match standard references (Montero2022 Eq. 2.2 → algebra ✓; D3-noghost.py ✓; Halliwell1987 ✓) or are honestly flagged with `% RAG-PENDING`.

### MAJOR

**M1 — Orphaned bib entries.** Four of the seven new `eci.bib` entries are never cited by `\cite{}` anywhere in `paper/eci.tex`:

| key | status |
|---|---|
| `AAL2023` | in `.bib` only, never `\cite`-d (only `AAL2025` is cited, line 68) |
| `DESY5` | in `.bib` only, never `\cite`-d (paper line 142 writes "DR2+DESY5" as bare text) |
| `DESIForecast` | in `.bib` only, never `\cite`-d |
| `Matsubara2003` | in `.bib` only; `eci.tex:78` leaves `% TODO-BIB: Matsubara2003` as *comment* instead of `~\cite{Matsubara2003}` at the end of the A6 sentence |

BibTeX does not emit a warning for unused entries (only for missing ones), so this passed the audit silently — but (a) the `.bib` now carries three fabricated-intent DES/DESI entries that are never referenced, which is sloppy, and (b) the A6 equation is textually *uncited* because the intended Matsubara attribution is still a `% TODO-BIB` comment. Replace the comment on line 78 with `~\cite{Matsubara2003}` before the period.

**M2 — `AAL2023` author mismatch vs. user's original attribution.** The bib note honestly flags "third author is Cunat, not L\"ust". Since this key is never cited (see M1), no in-text mismatch arises — but the key is also now dead weight. Either `\cite{AAL2023}` somewhere (§3.6 is the natural host, the SM-landscape paper IS the relevant follow-up) or drop the entry.

### MINOR

**m1 — Forward reference `\S3.6` is hardcoded text, not `\ref`.** Line 57 (A4) and line 68 (A5) write "\S3.6" literally. `section_3_6_swampland_cross.tex` carries no `\label` such as `sec:swampland_nmc_cross`. If anyone ever re-orders sections (e.g. Hubble tension moved), the "§3.6" text will lie silently. Low risk for v4.3.0, should be labelled in v4.4.

**m2 — `% TODO-BIB: Halliwell1987` comment on line 122 is stale.** The cite is resolved (`\cite{Halliwell1987,CopelandLiddleWands1998}` is present on the same line and `Halliwell1987` was added to the bib in commit `28746a3`). Drop the `% TODO-BIB` marker or audit will keep re-flagging it.

**m3 — A5 Montero2022 re-derivation is correct but unstated.** The paper writes `Λ_sp(H) = M_P (H/M_P)^{c'}` with c'=1/6, flagged as derived from Montero Eq. 2.2 via `H²~Λ/M_P²`. Arithmetic check: M̂ ~ Λ^(1/12) M_P^(2/3) → Λ ~ H² M_P² → M̂ ~ H^(1/6) M_P^(1/6) M_P^(2/3) = M_P (H/M_P)^(1/6). ✓. Fine as a RAG-PENDING, but a one-line footnote "(derived from Montero 2022 Eq. 2.2 via H²M_P² ~ Λ)" would pre-empt a referee.

**m4 — A6 Matsubara equation: H_3 vs. H_2 choice is convention-dependent.** The paper writes `H_3(ν)φ(ν)` with prefactor `S_3/6`. Matsubara 2003 (astro-ph/0006269) gives skewness corrections with Hermite index depending on which Minkowski functional (V_0,V_1,V_2,V_3) is meant. For the Euler characteristic / genus (3D), leading f_NL shift involves H_3 (and H_1 at subleading) — defensible. The paper should specify "in 3D on super-level sets" explicitly to lock the convention.

**m5 — `Montero2022` journal volume is `02`.** The bib entry uses `volume = {02}` (JHEP style) — correct per DOI `10.1007/JHEP02(2023)022` but bibtex warning "missing number" appears for 5 new entries (Montero2022, Calabrese2025, Calles2025, AAL2023 not warned because it has number). Cosmetic apsrev4-2.bst quirk, not a bug.

**m6 — Bib audit claims "0 critical, 1 minor" but does not flag the M1 orphans.** The audit reports only Crossref/arXiv resolution, not `\cite`-coverage. Consider extending `bib_audit.md` script to cross-check `\citation{}` in `.aux` against `.bib` keys.

## Numerical / equation re-derivations

### A5 species scale (c' = 1/6)
Montero–Vafa–Valenzuela (arXiv:2205.12293), abstract/§5: species scale `M̂ ~ Λ^(1/12) M_P^(2/3)`.
Friedmann on dS-like background: H² = Λ/(3M_P²) → Λ = 3 H² M_P² ~ H² M_P².
Substitute: M̂ ~ (H² M_P²)^(1/12) · M_P^(2/3) = H^(1/6) M_P^(1/6+2/3) = H^(1/6) M_P^(5/6) = M_P · (H/M_P)^(1/6). ✓
Paper equation matches.

### A6 Matsubara–Yip Euler characteristic
Leading-order NG shift of genus statistic (Matsubara 2003):
`Δ⟨V_3⟩ = (σ_0 S_3 f_NL / 6) H_3(ν) φ(ν) + O(σ_0²)`
Paper equation matches (modulo unspecified dimension). ✓ Sign: f_NL > 0 → positive skewness → shift H_3(ν)φ(ν) positive at ν > √3, negative in between — correct qualitative sign structure.

### No-ghost
`D3-noghost.py` line 20: `Q_T = (M_P² − ξχ²)/2 > 0` → paper condition `ξχ²/M_P² < 1` identical. Kinetic matrix `det K = M_P_eff²/2 − ξ²χ²` at leading order (paper line 110) matches D3 line 58. ✓ Faraoni factor-of-2 worry is unfounded because paper uses the weaker `Q_T > 0` form, not the full `det K > 0`.

### α ≤ √2 exponential-quintessence attractor
For V = V₀ exp(−αχ/M_P) in reduced-Planck: scalar-dominated attractor has
w_φ = −1 + α²/3; accelerating (w < −1/3) iff α² < 2, i.e. α < √2. ✓
This is Halliwell 1987 + Copeland–Liddle–Wands 1998 Table 1. Correct.

## Citation audit

| new key | DOI valid? | arXiv resolves? | claim in-text? | verified |
|---|---|---|---|---|
| `Montero2022` | 10.1007/JHEP02(2023)022 ✓ | 2205.12293 ✓ | A5, line 68 | YES |
| `AAL2023` | 10.1103/PhysRevD.109.016028 ✓ | 2306.16491 ✓ | **NO — orphaned** | FAIL (M1) |
| `Matsubara2003` | 10.1086/345521 ✓ | astro-ph/0006269 ✓ (WebFetch confirmed Minkowski/genus) | **NO — only in `% TODO-BIB` comment, line 78** | FAIL (M1) |
| `Halliwell1987` | 10.1016/0370-2693(87)91011-2 ✓ | n/a (pre-arXiv) | line 122 | YES |
| `CopelandLiddleWands1998` | 10.1103/PhysRevD.57.4686 ✓ | gr-qc/9711068 ✓ | line 122 | YES |
| `DESY5` | 10.3847/2041-8213/ad6f9f ✓ (WebFetch confirmed) | 2401.02929 ✓ | **NO — "DR2+DESY5" is bare text, line 142** | FAIL (M1) |
| `DESIForecast` | arXiv-only (2016) ✓ | 1611.00036 ✓ | **NO — orphaned** | FAIL (M1) |
| `Calabrese2025` DOI upgrade | 10.1088/1475-7516/2025/11/063 ✓ | 2503.14454 ✓ | line 72, 129 | YES |
| `Calles2025` DOI upgrade | 10.1088/1475-7516/2025/09/064 ✓ | 2412.15405 ✓ | line 76 | YES |

**Net**: 5/9 verified + in-text; 4/9 orphaned. No fabrications, no mis-attributions — just dead entries.

## Convention consistency

- **Signature `(−,+,+,+)`** declared line 61. Action line 80 uses `√(−g)` and `−½(∂φ)²` — consistent with mostly-plus ✓.
- **Faraoni ξ sign**: Lagrangian `−½ξRχ²`, EOM `+ξRχ` declared line 61. Existing EOM in §2 (line ~92): `Box χ − V' − ξ R χ = 0` — wait, let me re-check. `grep` of scalar EOM: the original paper text (unchanged) has `\Box \chi - V_\chi' - \xi_\chi R \chi = 0` — so `−ξRχ` on the LHS, i.e. `+ξRχ` term after moving to RHS. Convention line 61 says "appears as `+ξRχ` in the scalar field equation" — **consistent** with the form `Box χ = V' + ξRχ`. No sign bug.
- **Reduced Planck `M_P = 2.435e18 GeV`** declared line 61. Appears identically at line 124. `grep -E '1\.22|M_P\^2 *= *1/G'` → no hits. No unreduced Planck leaks. ✓

## Compilation & hygiene

- `latexmk -pdf -interaction=nonstopmode eci.tex` → 0 errors, 0 undefined refs, 0 undefined cites.
- BibTeX: 10 "missing number" warnings (apsrev4-2 cosmetic, pre-existing pattern, not v4.3 regression).
- LaTeX warnings: 1 `'h' → 'ht'` float specifier (cosmetic, pre-existing).
- hyperref unicode: accepted per v4.2.1 policy.
- Pages: 7 (within 6–7 target). File size: 712 KB (within ~600 KB target ±). ✓
- Remaining markers: `% TODO-BIB:` × 3 (Montero2022, Matsubara2003, Halliwell1987 — of which Matsubara2003 is a live bug, see M1), `% RAG-PENDING:` × 2 (A5 derivation, A6 Hermite form — documented), `% source:` × 2 (clean forward-links to derivations). Halliwell1987 TODO is now stale (m2).

## Recommendations for tag

**FIX** — one-commit patch, then SHIP v4.3.0.

Required edits (mechanical, no physics):
1. `eci.tex:78` — replace `% TODO-BIB: Matsubara2003` with `~\cite{Matsubara2003}` before the period.
2. `eci.tex:122` — delete the stale `% TODO-BIB: Halliwell1987` comment.
3. `eci.tex:~142` — add `~\cite{DESY5}` after the first textual "DESY5" (line 142), and `~\cite{DESIForecast}` at an appropriate DESI-forecast mention (line 142 "DESI DR3 forecast").
4. `eci.tex:~68` — add `~\cite{AAL2023}` alongside `AAL2025` where the SM-landscape aspect of the Dark Dimension is invoked (optional; otherwise drop `AAL2023` from bib).

After these 3–4 single-line edits, recompile, re-run bib audit script (extended to cross-check `.aux` citation coverage if feasible), then tag `v4.3.0` and release. No physics is broken. No re-derivation is required.

If the `AAL2023` cite-site is not found, delete the bib entry in the same fix-commit to keep bib discipline. Same with any of `DESY5`/`DESIForecast` if the citation spot is judged redundant.

## Re-run 2026-04-22 (post-fix)

**Fix commits landed:**
- `b7510da` — v4.3: fix V5-adv findings (4 orphan bib + 3 stale TODO-BIB)
- `4633ce8` — v4.3: clean trailing TODO-BIB in section_3_6 comment block

**Grep matrix:**
| Check | Expected | Found |
|---|---|---|
| `TODO-BIB\|RAG-PENDING` across `paper/*.tex` | only 1 historical "RAG-PENDING resolved" note | 1 (eci.tex:68, intentional) |
| `\cite{AAL2023}` | ≥1 in eci.tex (§A5) and §3.6 | eci.tex: 1 (§A5, combined with Montero2022); section_3_6: 1 (line 20) — total 2 sites |
| `\cite{DESY5}` + `\cite{DESIForecast}` + `\cite{Matsubara2003}` | each ≥1 | DESY5: 1 (§3.5), DESIForecast: 1 (§3.5), Matsubara2003: 1 (§A6 line 78) — total 3 |

**Compilation:** `latexmk -pdf` clean. 7 pages, 713,267 bytes (was ~712 KB). 0 undefined refs, 0 missing citations, 0 bibtex warnings. Single benign `LaTeX Warning: 'h' float specifier changed to 'ht'` (pre-existing, non-blocking).

**§A5 / §A6 / §3.6 prose check:**
- eci.tex:68 — derivation snippet `M_* ~ Λ^{1/12} M_P^{2/3}` with `H^2 ~ Λ/M_P^2` gives species-scale exponent, cites Montero2022+AAL2023 as primary (c'=1/6) and AAL2025+OoguriVafa2007 as comparison (c'≈0.05). Grammatical, accurate, self-contained.
- eci.tex:78 — adds 3D super-level-set specification with `H_3`, `σ_0`, `S_3^prim`, Gaussian density `φ`, cites Matsubara2003 + Yip2024/Calles2025 refinement. Correct.
- section_3_6:19-25 — Dark Dimension (Montero2022) + low-scale gravity variant (AAL2023) cited at first mention; species scale log-distance parametrisation with c'=1/6 stated cleanly. Correct.

**Verdict: SHIP**

All V5-adv M1+M2 findings resolved. Zero critical, zero major, zero new regressions. Minor items (style) remain optional and non-blocking. Owner may tag v4.3.0.
