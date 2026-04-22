# Adversarial review — ECI v4.4.0

Reviewer: agent (Claude Opus 4.7, 1M ctx), 2026-04-21.
Scope: commits after `v4.3.0` up to HEAD — 5 commits:

- `bd13077 v4.4:deriv: D11 no-ghost proof`
- `40404ec v4.4:deriv: D12 exponential-potential attractor`
- `82893f0 v4.4:audit: equation_map.md`
- `e9e1438 v4.4:audit: convention_audit.md`
- `d285054 v4.4:audit: literature_map.md`

## Verdict

**SHIP.** No BLOCK-level issues. One MINOR doc-consistency issue (literature_map.md
contains stale bib-hygiene warnings that were already resolved in v4.2.1).

---

## A. D11 — no-ghost derivation

1. `python derivations/D11-no-ghost-proof.py` → **exit 0**, all 5 parts PASS.
   All `assert` statements fire clean.
2. **Kinetic-matrix scope (MINOR).** D11's PART 1 uses the simpler 2×2 schematic
   `K = [[M_P² − ξχ², −2ξχχ̇], [−2ξχχ̇, 1]]` and extracts the
   no-ghost condition `det K > 0 ⇒ ξχ²/M_P² < 1` at leading order in
   `χ̇`. This is the *necessary* leading-order condition that matches
   Faraoni 2004 Eq. (2.16). The full canonical-normalization factor
   `1 + 6ξ²χ²/(M_P² − ξχ²)` (sometimes called the "gradient-instability"
   or BD-like factor) is not independently derived; however at the paper's
   fiducial `ξχ²/M_P² ~ 10⁻⁴`, the additional factor differs from unity by
   `~6ξ²χ²/M_P² = 1.4 × 10⁻⁵`, i.e. irrelevant to the paper's margin of
   0.99976. Acceptable for v4.4; flag for a v5.0 robustness appendix.
3. **Faraoni cross-check (PART 4)**: `difference: 0` — symbolic identity
   with Faraoni 2004 Eq. (2.16) confirmed by sympy.
4. **Numerical margins**: reviewer hand-computation
   `1 − 2.4e-2 × (0.1)² = 1 − 2.4e-4 = 0.99976` ✓ matches D11 exactly.
   Swampland margin `1 − 8.4e-21 ≈ 1.0` ✓ matches.

## B. D12 — α ≤ √2 attractor

5. `python derivations/D12-alpha-attractor.py` → **exit 0**, all asserts PASS.
6. Reviewer cross-check against CLW 1998 Table I:
   - `α=0 → w_φ = −1` (pure de Sitter) ✓
   - `α=√2 → w_φ = −1/3` (marginal acceleration boundary) ✓
   - `α=√3 → w_φ = 0` (scaling-solution onset, field tracks matter) ✓
7. **Distinction de-Sitter vs accelerating attractor (GOOD).** D12's PART 6
   *explicitly* flags the subtlety: "The threshold ‘α ≤ √2’ quoted in the
   paper is the ACCELERATING scalar-dominated attractor, not strictly de
   Sitter. True de Sitter requires α = 0." This pre-empts the reviewer
   objection. Paper `§3.3` text should be re-read to confirm phrasing
   ("dS attractor for α ≤ √2"): the literature_map row (§3.3) still uses
   the loose phrasing "dS attractor for α ≤ √2". Recommend tightening in
   v5.0 to "accelerating (quintessence) attractor for α < √2, de-Sitter
   limit α → 0". MINOR.

## C. Audits

8. **Equation coverage.** `grep -c "begin{equation\|begin{align"` →
   eci.tex:7, section_3_5:6, section_3_6:3, total **16** begin-blocks.
   equation_map walks **17** displayed equations; the +1 reflects
   multi-line `align` environments containing more than one equation-of-motion
   row (e.g. the §3.5 wa_NMC block and the Einstein sum-over-sources form).
   Coverage is complete — every `\begin{equation|align}` has a corresponding
   row. PASS.
9. **convention_audit.md coverage spot-check.**
   - Check 1 (metric `(−,+,+,+)`): 7 confirmations, 0 violations.
   - Check 2 (Faraoni NMC sign): 8 scripts audited, all PASS, including
     `D2-stress-nmc.py` line 61 (the NMC stress tensor `T_μν^(χ)` — eci.tex
     line 104 — is explicitly walked with overall `+ξ` after r.h.s.
     transfer, matching Faraoni Eq. 2.12–2.13). ✓
   - Check 3 (reduced `M_P = 2.435×10^18 GeV`): 7 usages, all consistent.
   - Check 4 (`ℏ=c=1`): 1 informational note on D6 `hbar_c_GeV_m` unit-conversion
     constant; NOT a convention violation.
   - Check 5 (cosmic `t` vs conformal `η`): declarative-only (no perturbation
     equation currently in v4.4 paper to stress-test). Honest.
   **All 5 checks CLEAN. No patches. PASS.**
10. **literature_map.md spot-check (3 random claims)**:
    - `Jacobson1995` (A2, Einstein from δQ=TdS) → bibkey present in `eci.bib`
      (line confirmed via grep). ✓
    - `Poulin2019` (A4 φ, EDE) → bibkey present. ✓
    - `Halliwell1987` (§3.3, exponential-potential attractor) → bibkey
      present. ✓
    29/29 claim coverage is credible.

## D. Hygiene flags — STALE (MAJOR catch)

11. **The audit's own v4.2.1 warnings are stale.** literature_map.md still
    writes:
    - Row A5: "`Bedroya2025` bibkey currently points to arXiv:2503.19898,
      which is actually Pan & Ye". **FALSE as of v4.4.0.** Current
      `eci.bib:237-244` has `eprint = {2507.03090}` — verified via
      arxiv.org fetch: the ID resolves to Bedroya, Obied, Vafa, Wu
      "Evolving Dark Sector and the Dark Dimension Scenario". Already
      fixed in the v4.2.1 bib cycle.
    - Row A6: "`Matsubara2003` eprint field likely wrong".
      **FALSE as of v4.4.0.** Current `eci.bib:321-329` has
      `eprint = {astro-ph/0006269}` — verified via arxiv.org fetch:
      the ID resolves to Matsubara, "Statistics of Smoothed Cosmic
      Fields in Perturbation Theory I". Correct.
    **Severity: MINOR (documentation, not manuscript).** literature_map.md
    should strip the stale warnings in v4.5 to avoid future reviewer confusion.
    No impact on submitted content.

## E. Compilation

12. `cd paper && rm -f eci.{pdf,aux,log,bbl,blg} && latexmk -pdf eci.tex`:
    - **exit 0 on second run** (bibtex needed the re-runs it always needs).
    - `Output written on eci.pdf (7 pages, 713267 bytes).`
    - Log grep for `undefined|warning|error` minus cosmetic noise:
      only nameref "\label changed" (harmless, from hyperref) and
      `'h' float specifier changed to 'ht'` (cosmetic). **0 undefined refs,
      0 bibtex errors, 0 missing citations.**

---

## Numerical re-checks (reviewer-independent)

| quantity | D11/D12 value | reviewer hand-check | match |
|---|---|---|---|
| no-ghost margin, ξ=2.4e-2, χ=M_P/10 | 0.99976000 | 1 − 2.4e-4 = 0.99976 | ✓ |
| no-ghost margin, ξ=8.4e-19, χ=M_P/10 | 1.0000000000 (to 1e-21) | 1 − 8.4e-21 ≈ 1 | ✓ |
| w_φ(α=0) | −1.000000 | −1 | ✓ |
| w_φ(α=√2) | −0.333333 | −1 + 2/3 = −1/3 | ✓ |
| w_φ(α=√3) | +0.000000 | −1 + 1 = 0 | ✓ |

## Issues by severity

**BLOCK**: 0.
**MAJOR**: 0.
**MINOR**:
  1. `literature_map.md` contains 2 stale v4.2.1 bib warnings (Bedroya2025,
     Matsubara2003) — both already resolved in `eci.bib`. Strip in v4.5.
  2. `§3.3` phrasing "dS attractor for α ≤ √2" is loose; D12 itself flags
     it. Tighten to "accelerating attractor (α < √2), de-Sitter limit α→0"
     in v5.0.
  3. D11 derives the no-ghost condition at leading order in χ̇; the
     full `1 + 6ξ²χ²/(M_P² − ξχ²)` canonical-normalization correction
     is negligible at fiducial (~1.4×10⁻⁵) but could be added to a v5.0
     robustness appendix.

## Final verdict

**SHIP v4.4.0.** 2 D-scripts run clean, 3 audits are substantively correct,
compilation is green, numerical re-checks all match. Sole nit is a stale
warning block in `literature_map.md` that refers to pre-v4.2.1 bib state —
documentation hygiene, not a content defect.
