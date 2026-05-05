# REWORK_NOTES — modular_shadow_LMP v1 → v2

**Date:** 2026-05-05 evening
**Owner:** A27 (Sonnet sub-agent, hallu count 78 entering / 78 exiting — no fresh fabrications)
**Inputs:** A11 SUMMARY (BOUND vs SATURATION split), A19 SUMMARY (BEC falsifier 288 ± 82 s⁻¹), v1 source (553 lines).
**Output:** `modular_shadow_LMP_v2.tex` (this directory) + this notes file.
**Discipline:** Mistral large STRICT BAN respected. All arXiv IDs live-verified via WebFetch (Anthropic native), 2026-05-05.

## Why a v2

A11 audit (2026-05-05 mid-day) refuted the **converse** of the v1 "Modular Shadow Conjecture" (saturation ⇔ type-II∞ chaos): three free-QFT / integrability counter-examples saturate the same kinematic ceiling without underlying chaos. v1 framed saturation as the central object; v2 splits it cleanly into a **provable bound** (Theorem 1) and a **downgraded saturation conjecture** (Conj. 1, kept as plausible sufficient direction only).

A19 audit (same day) identified a concrete BEC observable as a one-sided falsifier on Kolobov 2021 data: Γ_meas ≤ (288 ± 82) s⁻¹.

Concurrent independent work by Vardian (arXiv:2602.02675, Feb 2026) on modular Krylov + boundary area operator forced a comparison and scope-clarification section. Live-verified single-author hep-th, AdS/CFT scope.

## Structural changes v1 → v2

| § | v1 (553 lines, "saturation" framing) | v2 (target 6-10 LMP pages, "bound" framing) |
|---|---|---|
| Title | "ECI saturation as modular shadow of MSS chaos bound" | "A modular Lyapunov bound for finite-rank type-II∞ crossed-product algebras" |
| Abstract | proposes Modular Shadow **Conjecture** (saturation) | proves **Theorem** (bound); saturation is a separate downgraded conjecture |
| §1 | Background (MSS / Krylov / crossed-products / KMS β=2π) | Intro: bound theorem motivation + Vardian as concurrent independent work + organisation |
| §2 | "The Modular Shadow Conjecture" (saturation, conjectural) | Setup: type-II∞ crossed product + finite-rank truncation + modular Krylov complexity definitions |
| §3 | Verification on tractable models (Rindler, SYK) | **BOUND theorem** with full proof sketch (Parker eq. + BW theorem + Hankel moment) |
| §4 | Implications (algebra-type classification) | **Saturation as conjecture** (free-QFT counter-ex preclude converse) — explicitly downgraded; FS24 over-attribution erratum here |
| §5 | Open Questions | **Application: BEC Kolobov 2021 falsifier** Γ_meas ≤ (288 ± 82) s⁻¹ (A19 prediction) |
| §6 | (none) | **Discussion: Vardian comparison**, AdS/CFT vs dS/type-II∞ scope split |
| §7 | (none) | **Outlook**: lifting the truncation, dS, Bianchi IX, Connes-Størmer, FS bridge, Vardian unification |

## Key technical decisions

1. **Theorem statement (§3)**: states $b_n \le n\pi/\beta + o(n)$ on truncation, gives $\lambda_K^{\rm mod} \le 2\pi/\beta$. Proof in three steps: (i) Parker tridiagonal inequality (algebraic, on KMS-GNS), (ii) BW moment bound via Hankel-determinant inversion of $\sinh^{-\Delta}$ kernel, (iii) combine. **No chaos/holography/large-N input.**

2. **Saturation conjecture (§4) downgraded**: kept as plausible sufficient direction only ("type-II∞ at β=2π ⇒ saturation"), with explicit acknowledgement that the converse is refuted by Avdoshkin-Dymarsky 1911.09672, Camargo 2212.14702, Sreeram 2503.03400.

3. **FS24 erratum (§4 closing paragraph)**: explicit acknowledgement that v1 over-attributed the $S_{\rm gen} \leftrightarrow \mathcal{C}_K^{\rm mod}$ identification to FS24. FS24 derives crossed-product $S_{\rm gen}$ and proves the GSL; **does not** explicitly identify $S_{\rm gen}$ with modular Krylov complexity. Bridge is an ECI working conjecture.

4. **Vardian framing (§6)**: presented as **concurrent independent work** with **complementary scope** (AdS/CFT boundary area operator vs our intrinsic finite-rank truncation Lyapunov bound). Three explicit comparison axes: holographic context, object of study, claim type. Avoids any priority dispute and respects the live-verified scope split.

5. **BEC falsifier (§5)**: A19's BOUND form Γ_meas ≤ Γ_bound (robust to integrability counter-examples) replaces v1's tacit saturation prediction. Uses Kolobov 2021 dataset directly (re-analysis of existing 124-day, 97k-rep data, no new experiments).

## arXiv IDs live-verified this session (2026-05-05)

All via WebFetch (Anthropic native; no Mistral). New verifications this session marked ★; carry-over from A11/A19 unmarked.

| Tag | arXiv | Verified content (re-checked or carry-over) |
|---|---|---|
| MSS2016 | 1503.01409 | "A bound on chaos" |
| Parker2019 | 1812.08657 | universal operator-growth hypothesis |
| Caputa2024 | 2306.14732 | Krylov of modular Hamiltonian, PRD 109 086004 |
| Witten2022 | 2112.12828 | gravity and the crossed product |
| CLPW2023 | 2206.10780 | dS observable algebra |
| FaulknerSperanza2024 | 2405.00847 | crossed-product S_gen + GSL (FS24 erratum acknowledged) |
| DEHK2025a | 2412.15502 | observer-dependent gravitational entropy |
| DEHK2025b | 2405.00114 | gravitational entropy is observer-dependent |
| HellerPapalini2024 | 2412.17785 | Krylov spread complexity beyond JT |
| **Vardian2026** ★ | **2602.02675** | **Modular Krylov as boundary probe of area op (single-author hep-th, Feb 2026)** |
| **AvdoshkinDymarsky2019** ★ | **1911.09672** | **Euclidean operator growth and quantum chaos (Phys Rev Research 2 043234)** |
| **Camargo2023** ★ | **2212.14702** | **Krylov in free/interacting scalar QFT (JHEP 05(2023)226)** |
| **Sreeram2025** ★ | **2503.03400** | **Krylov dependence on initial operator/state (PRE 112 L032203)** |
| **Kolobov2021** ★ | **1910.09363** | **stationary spontaneous Hawking + time evolution analogue BH (Nat Phys 17 362)** |
| **Steinhauer2019** ★ | **1809.00913** | **thermal Hawking at T_H in analogue BH (Nature 569 688)** |
| Solnyshkov2026 | 2603.01664 | polariton analog BH merger (carry-over A19) |
| ChandranFischer2026 | 2604.02075 | UV-finite volume negativity (carry-over A19) |
| BisognanoWichmann1976 | (J Math Phys 17 303) | classical reference, no arXiv |
| ConnesRovelli1994 | (CQG 11 2899) | classical reference, no arXiv |
| TorresPatrick2017 | (Nat Phys 13 833) | rotational superradiant vortex (carry-over A19) |
| ECI_v6 | Zenodo 10.5281/zenodo.20030684 | ECI v6.0.53 record |

**Six new arXiv IDs live-verified this session (★).** Zero fabrications.

## What I deliberately did NOT do

- Did NOT promise $S_{\rm gen} \leftrightarrow \mathcal{C}_K^{\rm mod}$ identity (FS24 doesn't say it; ECI conjecture only).
- Did NOT use Mistral large for any verification (strict ban respected).
- Did NOT overwrite v1; v2 is a new file as instructed.
- Did NOT promote saturation back to a theorem.
- Did NOT claim Vardian-priority — explicitly framed as concurrent independent work with complementary scope.
- Did NOT add author names (preserved "(Author names to be determined)" placeholder from v1).

## Word/length sanity check

The v2 file is approximately 600 lines of LaTeX (counting bibliography, comments, theorem environments). Body content (intro through outlook) is ~430 lines of prose + math, mapping to ~7-8 LMP printed pages, in target range (6-10).

## Suggested next steps for parent (Kevin)

1. Compile v2 with pdflatex, eyeball for overfull boxes / missing references.
2. Decide author list (currently placeholder).
3. Consider whether to keep the BEC §5 in this LMP submission or split into a companion (LMP audience may prefer pure math-ph; the falsifier could go to a Phys Rev D Letter instead).
4. If keeping BEC §5: contact Steinhauer group to discuss re-analysis of 2021 dataset (or commission an independent re-analysis with the existing public data).
5. Compare against Vardian 2602.02675 in detail — read Vardian's full PDF and check whether Vardian's boundary modular Lanczos $b_n$ slopes coincide with $\pi/\beta$ on the AdS/CFT side; if so, there is a unification opportunity for v3.

## Discipline log

- 6 new arXiv refs WebFetch-verified this session (no Mistral).
- 0 fabrications introduced.
- v1 errors corrected: HellerPapalini description, FS24 over-attribution.
- Vardian scoop pre-empted by explicit concurrent-work framing in abstract + intro + §6.
- Hallu count exit: **78** (held at entry value).
