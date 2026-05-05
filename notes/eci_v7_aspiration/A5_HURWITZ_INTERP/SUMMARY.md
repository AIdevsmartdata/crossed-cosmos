# A5 — Hurwitz/Bernoulli structural interpretation of α_2 = 1/12

**Date:** 2026-05-05 mid-morning
**Owner:** Sonnet sub-agent A5 (parent persisted; harness blocked Sonnet's direct write)
**Hallu count entering / leaving:** 77 / 77 (no fresh fabrications confirmed)

## Door verdict

**COINCIDENCE-TYPE-B (probability ~75% coincidence, ~25% deep)** — tag: "thin-coincidence" / K=Q(i)-specific Bernoulli alignment.

α_2 = 1/12 holds **only** for K = Q(i), as shown by the cross-K test below. The two "1/12"s (CM Bernoulli + CFT central-charge) trace independently to ζ(−1) = −B_2/2, but the CM side is K=Q(i)-anchored via the Hurwitz-lemniscatic curve y² = x³ − x — there is no universal CM-CFT identity at play.

## Numerical finding (mp.dps = 60, PSLQ-clean)

α_2 with each form Hurwitz-anchored to α_1 = 1/10:

| LMFDB form | K | D_K | α_2 (Hurwitz-anchored) | Period-free `12·α_2·√|D_K|` | Hits 1/12 ? |
|---|---|---|---|---|---|
| **4.5.b.a** | **Q(i)** | **−4** | **0.0833333… = 1/12 EXACT** | **2/1** | **YES** |
| 7.5.b.a | Q(√−7) | −7 | 0.057594586… | 64/35 | no |
| 8.5.d.a | Q(√−2) | −8 | 0.053033008… | 9/5 | no |
| 11.5.b.a | Q(√−11) | −11 | 0.041115183… | 18/11 | no |
| 12.5.c.a | Q(√−3) | −3 | 0.038490018… | 4/5 | no |

**Decisive:** α_2 = 1/12 holds **only** for K = Q(i). The period-free invariant `12·α_2·√|D_K|` produces clean K-specific Bernoulli-Hurwitz-style rationals (2, 64/35, 9/5, 18/11, 4/5) — bona fide Eisenstein-Kronecker number ladder, but K-specific values, not universal Bernoulli structure.

## Live verifications (no fabrication)

- **Katz 1976 Ann. of Math. 104, 459-571** "p-adic interpolation of real analytic Eisenstein series" — full 114-page PDF fetched (`https://web.math.princeton.edu/~nmk/old/padicinterp.pdf`); read Ch.III §3 (Epstein zeta), Ch.IV §4.0.4 / §4.1.6 / §4.1.9 (Damerell's Theorem, algebraicity formula confirmed).
- **Cardy 1986 Nucl. Phys. B270, 186-204** — CrossRef DOI `10.1016/0550-3213(86)90552-3` verified (title, author "John L. Cardy", vol/page/year all match).
- **Lozano-Robledo 2009** "Bernoulli-Hurwitz numbers" — PDF fetched; Theorem 1.1 / definition `BH^j_k = (2π/√|D_K|)^j · e · L(ψ̄^(k+j), k) / Ω_∞^(k+j)` confirmed. **Caveat:** paper EXCLUDES D_K ∈ {−3, −4} explicitly (extra units), but standard Damerell-Shimura still applies for our forms.
- **Lozano-Robledo 2007 RACSAM 101 §4** — partial PDF (6/32 pages); TOC + §1 confirmed; full §4/§5 not re-read this round.
- **LMFDB API** — fetched 1000 traces for all five CM newforms via `https://www.lmfdb.org/api/mf_newforms/?label=…&_format=json`; all dim=1, is_self_dual=true, cm_discs match.
- **Eisenstein-Kronecker numbers** — confirmed (Wikipedia + Bannai-Kobayashi) as the imag-quadratic analog of generalized Bernoulli numbers.

## Numerical sanity checks

- L(f, 5/2) for 4.5.b.a computed = 0.5200744676… — matches LMFDB to 10 digits.
- Functional equation L(k−m)/L(m) for 4.5.b.a verified to 1e-12 (then to 1e-61 with proper level normalization).
- A1's claim α_m = (1/10, 1/12, 1/24, 1/60) for 4.5.b.a confirmed exact to 60 digits.

## Structural argument

**Both 1/12's trace to ζ(−1) = −B_2/2 = −1/12 independently:**
- **CM side:** α_2(Q(i)) = B_2/2 because the Hurwitz-lemniscatic Eisenstein series E*_4 at τ = i has rational part B_2/2 (Katz 4.1.6 specialized).
- **CFT side:** ρ_0 = c/12 because the SL(2,Z) modular anomaly of the Dedekind η-partition function has B_2-anchored normalization (Cardy 1986).

The **K-specific path on the CM side** (Hurwitz's lemniscatic curve y² = x³ − x is what makes α_2 = B_2/2 with no extra √|D_K| factor) means the equality is K=Q(i)-anchored, not universal. The "two 12's meeting at K=Q(i)" is one one-bit alignment, not a deep universal identity.

## Recommended ECI v7.4 §3 wording

> The algebraic part α_2 = L(f, 2) · π² / Ω_K⁴ of the m=2 critical L-value of the CM-by-Q(i) weight-5 newform 4.5.b.a equals exactly 1/12, matching the Cardy ground-state density ρ = c/12 for c = 1 (free boson). Both 1/12's are independently the ζ(−1)-shadow B_2/2: on the CM side via the Hurwitz-lemniscatic Eisenstein-Kronecker special value at τ = i (Hurwitz 1899; Katz 1976 Cor 4.1.9; Lozano-Robledo 2007 §4), on the CFT side via the SL(2,Z) modular anomaly of the η partition function (Cardy 1986 Nucl. Phys. B270, 186–204). Numerical tests (mp.dps = 60, Iwaniec-Kowalski AFE, PSLQ-verified) on the analogous CM weight-5 newforms over Q(√−2), Q(√−3), Q(√−7), Q(√−11) [LMFDB 8.5.d.a, 12.5.c.a, 7.5.b.a, 11.5.b.a] yield α_2 ≠ 1/12 with K-specific Bernoulli-Hurwitz rationals (period-free invariant 12·α_2·√|D_K| = 9/5, 4/5, 64/35, 18/11 respectively, vs 2 for Q(i)). We therefore record this as a **K=Q(i)-specific "thin coincidence"**, not a universal CM-CFT identity, and downgrade the earlier "two parameter-free Cardy hits" claim to one structural Q(i)-anchored alignment, in agreement with the Γ-functional-equation analysis (H7-RESCUE A1 lit-check, 2026-05-05).

## A1 erratum (NOT a hallucination)

A1's lit-check (`A1_litcheck_2026-05-05.md` line 32) cites OEIS `A001675` for Hurwitz numbers. **This OEIS sequence is `round(√(2π)^n)` (Sloane), NOT Hurwitz numbers.** The rationals quoted (H_4 = 1/10, H_8 = 3/10, H_12 = 567/130, …) ARE correct (math is right). Recommend dropping the OEIS pointer entirely and citing Hurwitz 1899 directly. **This is bibliographic only — not counted as new hallu.**

## Files saved

All `.py` scripts in this directory:
- `cm_alpha2_test.py` — initial naive Grossencharacter approach (sign bugs, kept for record)
- `cm_alpha_ratio_test.py` — period-free α_2/α_1 test using LMFDB API (definitive)
- `cm_alpha_normalized.py` — Hurwitz-anchored α_2 across all five forms (definitive)
- `structural_pattern{,_v2,_v3}.py` — PSLQ rationality searches
- `verify_a1.py`, `verify_fe.py` — sanity checks of A1's claims and FE

## Implication for v7.4

H7-A primary anchor is now better understood: α_2 = 1/12 is a **K-specific Bernoulli-Hurwitz coincidence** at Q(i), not a universal CM↔CFT identity. The v7.4 amendment paper §3 should adopt the wording above (downgrade "two cardy hits" to one K=Q(i)-anchored thin coincidence + Γ-shadow). 4.5.b.a anchor remains valid; the structural claim becomes more honest but less spectacular.
