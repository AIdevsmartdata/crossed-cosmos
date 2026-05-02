# Honest reality check — cosmological constant and arrow-of-time claims
**ECI Audit — 2026-05-02**
**Auditor:** Sonnet sub-agent, sandbox-isolated, with sympy/python arithmetic and direct arXiv API verification
**Commissioning context:** A long Mistral output had proposed (a) a derivation of ρ_Λ / M_P⁴ ≈ 8×10⁻¹²¹ from three independent approaches (NCG cutoff, E₈, ECI internal), and (b) an emergent arrow of time from `dt = (dC_k/dτ_R) dτ_R`. This audit was commissioned to verify the arithmetic before any of it leaks into a paper.

**Verdict (TL;DR):** Both claims are off the table. The three cosmo-const "approaches" fail arithmetic by 14–89 orders of magnitude — they are not three independent confirmations, they are three unrelated wrong numbers post-hoc compared to the target value. The arrow-of-time formula reduces to `dt = dC_k` by the chain rule and is a re-parameterisation identity, not a derivation; the direction is installed by the low-complexity initial condition (Past Hypothesis), not derived from the dynamics. The four publishable Leviers (MCMC joint, Nägerl anyonic, Steinhauer BEC, M1 conditional → M1-C) remain the correct focus.

---

## 1. Cosmological constant — arithmetic verification

All three approaches computed with Python 3.12 `math` module (IEEE 754 double precision).

### Approach (a) — NCG spectral cutoff: `Λ⁴ exp(−Λ²)`, `Λ = M_P / √(8π)`

```
Lambda                       = 0.19947114020071635
Lambda^2                     = 0.03978873577297384
Lambda^4                     = 0.00158314349441153
exp(-Lambda^2)               = 0.96099244103328330
Lambda^4 * exp(-Lambda^2)    = 1.52138893120049652 × 10⁻³
log10(result)                = −2.82
```
**Claimed: ~10⁻¹²¹. Actual: ~1.5 × 10⁻³. Off by 118 orders of magnitude.** No mechanism within Connes–Chamseddine spectral action (hep-th/9606001) produces 10⁻¹²¹ suppression; the spectral action *generates* a Λ⁴ cosmological term (the problem's source), it does not resolve it. The exponential damping at this Λ barely moves the needle (`exp(−0.040) ≈ 0.961`).

### Approach (b) — E₈: `exp(−π²/α_{E₈}) M_P⁴`, `α_{E₈} = 1/25`

```
α_{E₈}                       = 0.04
exponent                     = −π²/0.04 = −π²·25 = −246.74
exp(−π²·25)                  = 6.95 × 10⁻¹⁰⁸
log10(result)                = −107.16
```
**Claimed: ~10⁻¹²². Actual: ~7 × 10⁻¹⁰⁸. Off by 14 orders.** `α_{E₈} = 1/25` is post-hoc curve-fit, not derived from E₈ representation theory. Without a moduli-stabilisation mechanism and a specification of which E₈ instanton process is invoked, the formula is unmoored.

### Approach (c) — ECI internal: `κ_R / C_k^max`, `κ_R ~ H_0`, `C_k^max ~ exp(S_gen_max)`, `S_gen_max ~ 10⁹⁰`

```
H_0 in Planck units          ~ 10⁻⁶¹
log10(exp(S_gen_max))        = S_gen_max / ln(10) ≈ 4.34 × 10⁸⁹
log10(H_0 / exp(S_gen_max))  ~ −61 − 4.34×10⁸⁹  ≈  −4.34 × 10⁸⁹

Python: math.exp(-1e90) = 0.0   (IEEE 754 underflow)
```
**Claimed: ~1.22 × 10⁻¹²¹. Actual: 10^(−4.34×10⁸⁹). Underflows to identically zero.** This is not "off by a few orders" — the *exponent of the exponent* is 10⁸⁹. Mistral conflated `S_gen_max ~ 10⁹⁰` (a dimensionless entropy) with something that produces 10⁻¹²¹ when used as an exponent. The two are numerically incommensurable.

**Verdict on Claim 1:** All three approaches fail arithmetic by 14–89 orders of magnitude. They are not independent confirmations — they are three unrelated wrong numbers that coincidentally bracket 10⁻¹²¹. This is numerology, not derivation. Any competent cosmology/HEP referee will catch this immediately and the credibility of the whole submission would suffer.

---

## 2. Arrow of time — the tautology in `dt = (dC_k/dτ_R) dτ_R`

By the chain rule `(dC_k / dτ_R) dτ_R = dC_k`. The proposed equation collapses to `dt = dC_k`, i.e., physical time is *defined* to be proportional to complexity growth. This is a re-parameterisation. Re-parameterisations are symmetric under `t → −t` whenever `C_k` is replaced by any monotone function of `|t|`; they carry no information about which direction time actually flows. The equation is valid in both temporal directions unless the boundary condition at the initial moment is separately specified to break the symmetry.

To actually derive an arrow from complexity, one would need:
1. an explanation of why `C_k` is monotonically *increasing* — which requires a low-complexity initial condition (Past Hypothesis, Albert 2000; Penrose Weyl curvature hypothesis);
2. a justification for selecting the increasing branch — requiring either a CPT-breaking boundary condition or anthropic reasoning;
3. a connection from `C_k` to thermodynamic entropy `S` so that `dC_k/dt > 0` implies `dS/dt > 0`.

None of these appear in Mistral's presentation. The formula `dt = dC_k` is as informative as `dt = dS` when one defines the clock by entropy growth: the arrow is installed *by hand* via the initial condition, not derived from the dynamics.

**Verdict on Claim 2:** Tautology. The arrow of time is presupposed in the low-complexity boundary condition, not derived from this equation.

---

## 3. Honest state of the art (verified citations only)

### 3a. Cosmological constant
- S. Weinberg, *Rev. Mod. Phys.* **61**, 1 (1989) — pre-arXiv. Verified later treatment: S. Weinberg, "The Cosmological Constant Problems," **arXiv:astro-ph/0005265** (2000) — abstract retrieved. Conclusion: no known symmetry argument explains Λ's smallness; anthropic selection within a large landscape is the most conservative viable hypothesis.
- R. Bousso & J. Polchinski, "Quantization of Four-form Fluxes and Dynamical Neutralization of the Cosmological Constant," **arXiv:hep-th/0004134** (2000) — the canonical landscape mechanism, requires accepting the string landscape and anthropic reasoning.
- A. Chamseddine & A. Connes, "The Spectral Action Principle," **arXiv:hep-th/9606001** (1997) — produces SM + Einstein–Weyl gravity, *generates* a cosmological term ~ Λ⁴. **No published spectral-action paper derives an O(1) prefactor cancelling 121 orders of magnitude.**
- G. Obied, H. Ooguri, L. Spodyneiko, C. Vafa, "De Sitter Space and the Swampland," **arXiv:1806.08362** (2018) — conjectures de Sitter vacua are absent from the string landscape, *sharpening* rather than resolving the problem.

Currently viable lines: Bousso–Polchinski landscape + anthropic selection; swampland constraints; novel symmetry arguments (no successful candidate as of 2026). NCG- and E₈-numerology routes are not considered viable directions in the current community.

### 3b. Arrow of time
- D. Z. Albert, *Time and Chance* (Harvard, 2000): the thermodynamic arrow requires the **Past Hypothesis** — a posited low-entropy initial condition — as a fundamental postulate, not a theorem. It is a boundary condition on the dynamics. (Pre-arXiv, journal/book reference.)
- B. Loewer, "Determinism and Chance," *Studies in History and Philosophy of Modern Physics* **32**, 609–620 (2001) — makes the probabilistic structure explicit.
- R. Penrose, *Cycles of Time* (2010): Weyl-curvature hypothesis as the geometrical correlate of the Past Hypothesis — a conjecture, not a theorem.
- In algebraic QFT, Tomita–Takesaki modular theory defines an intrinsic one-parameter automorphism group (modular flow) for any von Neumann algebra in a cyclic-separating state. Mathematically rigorous, but **runs in both temporal directions**; a preferred arrow requires additional physical input. As of 2026, no paper in algebraic QFT derives the thermodynamic arrow from first principles without an asymmetric boundary condition.
- "Ciolli–Longo–Ruzzi 2024" cited in the original briefing was **not retrievable via arXiv API search** and is excluded here. Do not cite it without independent verification.
- Complexity-based approaches (Krylov/spread complexity) are legitimate measures of scrambling but require the same Past Hypothesis input as the thermodynamic approach: assuming low initial complexity restates rather than explains the problem.

---

## 4. Recommendations for ECI papers

**Cosmo const.** v5/v6/v7-note must **not** claim ECI contributes a derivation of `ρ_Λ / M_P⁴ ≈ 10⁻¹²¹`. Any competent referee catches this in 30 seconds.

**Arrow of time.** Must **not** present `dt = (dC_k/dτ_R) dτ_R` as derivation of emergent time direction.

**Paste-ready §Limits sentences (verbatim usable):**

> *"The ECI framework does not address the cosmological constant problem; the observed value `ρ_Λ / M_P⁴ ≈ 10⁻¹²¹` remains unexplained within this formalism, and no such claim is made here."*

> *"The complexity clock `dτ_C := dC_k` defines a monotone re-parameterisation of proper time conditional on a low-complexity initial state; it does not derive the direction of time independently of that boundary condition, and we do not claim otherwise."*

> *"Explanations of `ρ_Λ` and of the thermodynamic arrow of time lie outside the present scope and would require connections to quantum gravity and cosmological boundary conditions not established in this work."*

---

*Arithmetic: Python 3.12 math module, IEEE 754 double precision. ArXiv IDs verified by direct query to `export.arxiv.org/api`. Weinberg 1989 *Rev. Mod. Phys.* predates arXiv; cited by journal reference only. "Ciolli–Longo–Ruzzi 2024" not retrieved; excluded.*
