---
name: A70 Likelihood specification — ECI-vs-Wolf Bayes contest
description: Bayesian likelihood design resolving the KG-CPL structural mismatch; two valid contest framings
type: project
---

# A70 — Likelihood specification: ECI-vs-Wolf 2025 head-to-head Bayes contest

**Date:** 2026-05-05 night (Wave 12 Phase 1)
**Owner:** Sonnet sub-agent A70
**Hallu count entering / leaving:** 85 / 85
**Sources read:** A69 SUMMARY + lagrangian.tex, A56 SUMMARY, A64 design + skeleton py, A73 SUMMARY, A25 SUMMARY

---

## Verdict

**Recommend BOTH framings, with Framing A as the publishable primary and
Framing B as a diagnostic / robustness check.**

The structural mismatch (A56) is decisive:

| Quantity         | Wolf 2025           | ECI (Cassini-clean)     |
|------------------|---------------------|-------------------------|
| ξ fitted         | 2.31 (+0.75/−0.34)  | ~0.001 (informative)    |
| Domain           | CPL-effective       | KG-physical             |
| KG stability     | FAILS (φ→287 runaway) | PASSES (ξ < ξ_crit_+≈0.20) |
| Cassini          | New physics needed  | Automatic               |
| RG trajectory    | [TBD: not computed] | ξ(M_GUT)=−0.029, stable |

A naive single-likelihood MCMC declaring Wolf winner by log B would be
statistically invalid: Wolf's ξ=2.31 lives in CPL-effective space, not
KG-physical space.

---

## Framing A — "KG-physics consistency gate" (PRIMARY, publishable)

**Question:** Does Wolf-NMC, confined to the KG-physical domain
ξ ∈ [−5, +0.20], fit BAO+SNe+CMB better than ΛCDM? Does it beat ECI?

**Physical basis:** No model sample is allowed to produce KG runaway
(F(φ) → 0, φ divergent). A per-sample ODE integration acts as a gate:
logL = −∞ on runaway. Potential-agnostic — does not assume A56's
exponential-V ξ_crit transfers to Wolf's quadratic V.

**Anticipated result (H_A0 pre-registered):**
Wolf-KG-restricted log B vs ΛCDM < +1 (loses claimed H₀ tension resolution).

---

## Framing B — "CPL-effective phenomenological contest" (SECONDARY, diagnostic)

Both sides report (w₀, wₐ) at EFT-fluid level. ECI ξ~0.001 → w(z) ≈ −1
(near-ΛCDM). Wolf ξ=2.31 → richer w(z) shape. Quantifies phenomenological
cost of ECI's Cassini-clean constraint. Appendix only.

---

## Pre-registered hypotheses (frozen)

| Hyp     | Criterion                                      | Interpretation                              |
|---------|------------------------------------------------|---------------------------------------------|
| H_A0    | Wolf-KG-restricted log B(vs ΛCDM) < 0          | Wolf loses physical gate; ECI superior      |
| H_A1    | Wolf-KG-restricted log B(vs ΛCDM) > +3         | Wolf survives; Cassini screening is real    |
| H_ECI   | log B(ECI vs ΛCDM) ∈ [−3, +1]                 | ECI consistent with A41 baseline (−1.37)   |
| H_B     | ECI CPL Δχ²/dof vs Wolf-CPL < 1                | ECI competitive at EFT level                |
| H_sanity| Wolf-KG posterior ξ peaks at ξ ≪ 2.31         | Validates non-trivial KG gate               |

---

## Dataset configuration

Per A69 (live-verified corrections to A4):
1. Planck 2018 Plik TT+TE+EE (NOT PR4 NPIPE)
2. DESI DR2 BAO (arXiv:2503.14738) — 7 z-bins
3. Pantheon+ SN-Ia (2022) — marginalize M_B
4. ACT DR6 lensing — A_lens constraint

---

## Sampler recommendation

**Framing A primary:** PolyChord (matches Wolf method; gives log Z directly).
**Framing B + cross-check:** NUTS via numpyro + cosmopower-jax emulator
(A25 stack + NEW extended emulator, finished tonight 2026-05-05).
**Bayes factor:** PolyChord log Z primary; TI 16-temp cross-check.

---

## Files in this directory
- `SUMMARY.md` — verdict + framing rationale
- `likelihood_spec.md` — full mathematical spec, priors table, dataset spec
- `sampler_pseudocode.py` — pipeline skeleton for A71 PC GPU run

## Discipline log
- Hallu count: 85 entering → 85 leaving.
- 3 explicit [TBD] markers placed (Cooke 2018 BBN ref; Brout 2022 Pantheon+ arXiv ID; ACT DR6 A_lens values) rather than fabricating.
- 0 new fabrications. Mistral NOT used.
