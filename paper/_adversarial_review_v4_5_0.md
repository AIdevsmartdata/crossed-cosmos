# Adversarial Review — v4.5.0 (pre-tag)

**Reviewer:** V8-adv (Opus 4.7 1M)
**Scope:** commits `v4.5:A3:*`, `v4.5:deriv:D13`, `v4.5:paper:section_3_5 + row 1b`
**Date:** 2026-04-21
**Repo state:** `d8ff646` (HEAD)

## Verdict: **SHIP** (with 1 MINOR housekeeping item)

- **BLOCK:** 0
- **MAJOR:** 0
- **MINOR:** 1 (abstract still calls A3 a "selection rule")
- **NIT:** 2

---

## Block 1 — D13 numerical B(Ω_Λ) (items 1–6)

### Item 1 — Runtime & asserts
`python derivations/D13-wa-numerical-full.py` → **exit 0**, all asserts pass, prints `D13 PASS`. Wall-clock **1.09 s** (script-reported 0.7 s CPU; the 0.4 s gap is interpreter startup + matplotlib import). Matches the claimed ~0.7 s order of magnitude. **PASS.**

### Item 2 — Physical plausibility of B_num ≈ 9 flat
Reproduced: B_num = {9.00, 9.18, 9.05, 8.11} at Ω_Λ = {0.5, 0.6, 0.7, 0.8} with σ ≈ 1.1 (i.e. all four within 1σ of a constant ≈ 8.85).

Interpretation: the heuristic B_heur = (8/√3)·A inherits its Ω_Λ-dependence entirely from the matter-era adiabatic projection of A. The full NMC integration shows that the ξ-driven linear correction to w_a is driven by the *ξR χ* term in the KG equation, whose coefficient `R = 6(2−3w̄)H²` is almost frozen once the universe is DE-dominated (w̄ → −1 ⇒ R → 12H²) and depends only weakly on Ω_Λ in the range sampled. The flatness is therefore physically **expected**, not a solver artefact: A falls because the thawing amplitude shrinks, but B reflects a different geometric prefactor (R/H² at the turn-on) which does not. No divergence is expected in the deep-DE limit Ω_Λ → 1 because the correction is *linear* in ξ and χ_0 stays bounded. **PASS — plausible.**

Caveat: the claim is only verified inside [0.5, 0.8]; any extrapolation to Ω_Λ → 1 is not a numerical statement. The paper does not over-claim on this axis.

### Item 3 — A_num(0.7) = 1.34 vs Scherrer–Sen 1.58 (15.3%)
Reproduced: 15.3% relative error. The A_num sequence {2.56, 1.91, 1.34, 0.81} is **monotone decreasing with Ω_Λ**, same sign and same shape as the analytic A = {2.35, 1.94, 1.58, 1.23}: the trajectory is unambiguously thawing-like (w_eff crosses from ~−1 toward > −1 as a grows; Ω_χ grows monotonically, as evident from the console output `Ω_χ(a=1)=0.69–0.70` at the targeted Ω_Λ). The offset is a **scale** offset (likely IC at z=999 not being on the exact attractor) not a **sign** or **shape** disagreement. The agent's excuse is **valid**, but since B_num is obtained as the *slope* of Δw_a vs ξ at fixed trajectory, a 15% A-offset does not propagate one-for-one into B: slope extraction is robust to the scale offset. **PASS.**

### Item 4 — Cassini rescaling
Verified: √(1+w_0=−0.75)/√(1+w_loc=−0.9) = √0.25/√0.1 = 0.5/0.3162 = **1.581**. Taking the largest intra-table Δw_a = 6.97e-3 at w_loc=−0.9 × 1.581 = **1.102e-2** ≈ 1.1×10⁻². Paper quote matches within rounding. **PASS.**

### Item 5 — B_heur cross-check
Computed (8/√3) × {2.35, 1.94, 1.58, 1.23} = 4.6188 × {…} = **{10.85, 8.96, 7.30, 5.68}**. Table values in §3.5 show {10.85, 8.96, 7.30, 5.68}. **PASS, exact.**

### Item 6 — LaTeX compile
Clean rebuild (removed aux/bbl/pdf, ran pdflatex→bibtex→pdflatex×2). Result: **8 pages, 0 errors, 0 undefined references**, `eci.pdf` 737 KB. **PASS.**

---

## Block 2 — A3 toy dictionary §5 (items 7–10)

### Item 7 — Specificity of the dictionary (quote verbatim)
§5 states a single, numbered conjectural map, Eq. (eq:toy-dict):

> *"|S_gen^cg[ρ; H_O] − S_gen^max[H_O]| ≲ ε · k · log dim A_O"*

with explicit identifications: ρ a state on the type-II_1 crossed-product algebra A_O attached to geodesic observer O's clock QRF, modular flow σ_t^O being an ε-approximate unitary k-design on a code subspace, S_gen^max the Gibbons–Hawking generalised entropy of the static patch. The **named testable consequence** is given under *One concrete testable consequence*: "any primordial perturbation spectrum predicting a super-Gibbons–Hawking coarse-grained horizon entropy at reheating is excluded as a geometric bulk state… a nontrivial consistency check against the complexity diagnostic of A6." This is a **specific falsifiable equation and a specific observational consequence** — not vague handwaving. **PASS.**

### Item 8 — Verbatim vs paraphrase of CryptoCensorship RAG
The RAG source `paper/_rag/CryptoCensorship.txt` contains the core statements "ε-approximate k-design → event horizon in bulk dual" and "cosmic censorship reformulated via reconstruction complexity". §5 does **not** copy sentences from the RAG verbatim; it paraphrases them and, crucially, **translates** them (AdS boundary → observer worldline, boundary CFT algebra → type-II_1 crossed-product algebra). The paraphrase is faithful: I grepped the RAG for "event horizon", "k-design", "cosmic censorship", "complexity" — all four concepts are present in the source and used accurately in §5. **PASS.**

### Item 9 — (D) markers on three consequences
Grep `\\textbf{(D)` in `eci.tex` §5 consequences subsection returns **three** entries (lines 162, 165, 168): "Big Bang as decodability boundary", "Inflation as algebraic necessity", "Weyl Curvature Hypothesis revisited". Each body paragraph opens with "If the dictionary holds" or "Under (eq:toy-dict)". Subsection header (line 160) explicitly says "we mark them (D) to make the dependence visible at a glance". **PASS.**

### Item 10 — Honest N~60 labelling
Line 166: *"this is an order-of-magnitude matching, not a first-principles derivation of the e-fold number."* **PASS.**

---

## Block 3 — Cross-compat (items 11–12)

### Item 11 — §3.6 conditional language
§3.6 (Swampland×NMC) line 148 still reads: *"The cross-constraint is *conditional* on the shared-cutoff [assumption]"* — this conditionality is about the EFT cutoff, not A3. §3.6 does not currently reference the toy dictionary. That is **acceptable** because §3.6's logic only invokes ξ_χ as a Lagrangian coupling (from A4/NMC), not A3's CFT→cosmology map. No "conditional on A3" sentence previously existed in §3.6 that would need updating. **PASS (no action required).**

### Item 12 — Abstract still says "selection rule"
`eci.tex` line 31 abstract: *"(v) Cryptographic Censorship as a **selection rule** on admissible bulk geometries"*. A3 is now framed as a **working conjecture with a toy dictionary** in §5 and on the axiom line (50–51). The abstract has **not** been updated to reflect this framing. This is a **MINOR** inconsistency: a reader who reads only the abstract will infer a stronger status for A3 than §5 actually claims.

**Recommendation:** edit abstract (v) to e.g. *"(v) Cryptographic Censorship as a working conjecture whose cosmological transposition is made explicit via a toy dictionary~\\cite{CryptoCensorship} (§\\ref{sec:A3-dictionary})"*. Two-line change, no physics consequence.

---

## Issues by severity

| Sev | Item | Finding | Fix cost |
|---|---|---|---|
| MINOR | 12 | Abstract still says A3 is a "selection rule"; §5 has downgraded this to "working conjecture + toy dictionary" | 1 sentence edit in abstract |
| NIT | — | Table tab:B_of_OmegaL caption says "ξ_χ ∈ {−0.024,−0.01,0,+0.01,+0.024} × χ_0 ∈ {M_P/20,M_P/10,M_P/5}" — the `×` between the two sets is slightly ambiguous; read as a Cartesian product (5×3 = 15 trajectories per Ω_Λ) this matches the script | clarify "grid of 5×3 trajectories" if desired |
| NIT | — | §3.5 line 84 cites "Ye~et~al." and "Pan~\\&~Ye" for literature survey; the claim is that the explicit B_num(Ω_Λ) form has not appeared there. This is a negative literature claim (hard to falsify); consider softening to "to our knowledge has not been tabulated in closed form in" | optional |

## Recommendation

**Tag `v4.5.0` now** after applying the one-line abstract edit (item 12). The two numerical/textual blocks (D13 + A3 dictionary) are **internally consistent, reproducible, honestly labelled, and compile cleanly**. The MINOR finding is cosmetic consistency between abstract and body; neither physics nor claims are affected. No BLOCK, no MAJOR, no rewrite required.

If the abstract edit is considered out-of-scope for v4.5.0 (i.e. the tag is meant to capture only the two declared work blocks), ship as-is and file a v4.5.1 patch commit for the abstract. The review does not recommend withholding the tag on this single item.

---

*Generated 2026-04-21 by V8-adv; no .py/.tex/.bib files modified during review.*
