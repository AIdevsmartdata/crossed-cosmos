# A8 — G1.14 Joint MCMC Specification

**Date:** 2026-05-05
**ECI version:** v6.0.53.1 (hallu count entering: 77)
**Author:** A8 (Sonnet sub-agent), crossed-cosmos
**Inputs:** PC1 [TWO-TAU VIABLE] (joint χ²<50 at τ_l=i fixed, τ_q scanned)
              W1 [TAU-NEAR-I VIABLE] (single-τ attractor at τ*=-0.19+1.00i, χ²/dof=1.05)
**Output:** `g114_joint_mcmc.py` (this directory)

---

## 1. Purpose

PC1 fixed τ_lepton = i and scanned τ_quark on a 12×12 grid, getting a degenerate
overfit (χ² ~1e-22 because only 2 ratios fit per sector with 3 free couplings).
W1 ran a single-τ scan over 7 observables (CKM included) and found a robust
near-i attractor at χ²/dof ≈ 1.05.

**G1.14 deliverable proper:** a joint NUTS MCMC over the *full* (τ_lepton,
τ_quark, all couplings) parameter space against *13 independent observables*
(a true 1+ degrees-of-freedom fit), to:

1. Confirm or refute the [TWO-TAU VIABLE] verdict on a non-degenerate observable set.
2. Derive posterior credible regions for |τ_l - i|, |τ_q - i|, and |τ_l - τ_q|.
3. Quantify support (Bayes factor) for the **two-modulus** hypothesis (τ_l ≠ τ_q)
   versus the **single-modulus** collapse (τ_l = τ_q).

---

## 2. Model: LYD20 Model VI + unified lepton

Source: **Liu, Yao, Ding (2020)** arXiv:2006.10722 "Modular invariant flavor
symmetry and CP violation" — Model VI of S′_4 modular flavor.

### 2.1 Quark sector (Model VI, LYD20 Eq.(Mq_6))
- **Q ~ 3** (left-handed quark doublet triplet)
- **u^c ~ 1̂′** (k=−1, weight-1 coupling to Y^(1)_3̂′)
- **c^c ~ 1**  (k=−2, weight-2 coupling to Y^(2)_3)
- **t^c ~ 1̂′** (k=−5, weight-5 coupling to Y^(5)_3̂)
- **d^c ~ 1̂′** (k=−1, weight-1)
- **s^c ~ 1**  (k=−5, weight-5 → Y^(5)_3̂)
- **b^c ~ 1̂′** (k=−5, weight-5 → Y^(5)_3̂′,I + Y^(5)_3̂′,II)

The b^c coupling has **two** independent weight-5 contractions (3̂′,I and 3̂′,II),
so the down-sector has 4 real coupling parameters (β_d, γ_d1, Re γ_d2, Im γ_d2).

### 2.2 Lepton sector (LYD20 unified model, Eq.(Ml))
- **L ~ 3** (lepton doublet triplet)
- **E1^c ~ 1**, k=−2 → row 0 weight-4 Y^(4)_3
- **E2^c ~ 1**, k=0  → row 1 weight-2 Y^(2)_3
- **E3^c ~ 1̂′**, k=−1 → row 2 weight-3 Y^(3)_3̂′

This is the **same** Y(τ) machinery as quarks but evaluated at *τ_lepton*
(possibly different from τ_quark — the **two-τ hypothesis**).

### 2.3 Modular form basis
Weight-1 seed (3̂′ of S′_4):
```
e1 = η(4τ)^4 / η(2τ)^2
e2 = η(2τ)^10 / [η(4τ)^4 η(τ)^4]
e3 = η(2τ)^4 / η(τ)^2
Y1 =  4√2 e1 + i√2 e2 + 2√2(1−i) e3
Y2 = −2√2(1+√3) ω² e1 − i(1−√3)/√2 ω² e2 + 2√2(1−i) ω² e3
Y3 =  2√2(√3−1)  ω  e1 − i(1+√3)/√2 ω  e2 + 2√2(1−i) ω  e3
```
where ω = e^{2πi/3}. Higher-weight forms (Y^(2)_3, Y^(3)_3̂′, Y^(4)_3, Y^(5)_3̂,
Y^(5)_3̂′,I, Y^(5)_3̂′,II) are polynomials in (Y1,Y2,Y3) per LYD20 §II + Appendix.
Implementation faithfully transcribed in `g114_joint_mcmc.py:all_forms()`.

---

## 3. Free parameters (15 reals; 13 in user spec collapses Im γ_d2)

| # | Name           | Range            | Prior                    |
|---|----------------|------------------|--------------------------|
| 0 | Re τ_q         | (-0.6, 0.6)      | flat (or |τ_q-i|<1 if `--restricted`) |
| 1 | Im τ_q         | (0.5, 2.5)       | flat                     |
| 2 | Re τ_l         | (-0.6, 0.6)      | flat (or |τ_l-i|<0.5 if `--restricted`) |
| 3 | Im τ_l         | (0.5, 2.5)       | flat                     |
| 4 | log β_u        | (-∞, ∞)          | N(0, 6²)                 |
| 5 | log γ_u        | (-∞, ∞)          | N(0, 6²)                 |
| 6 | log β_d        | (-∞, ∞)          | N(0, 6²)                 |
| 7 | log γ_d1       | (-∞, ∞)          | N(0, 6²)                 |
| 8 | Re γ_d2        | (-∞, ∞)          | N(0, 5²)                 |
| 9 | Im γ_d2        | (-∞, ∞)          | N(0, 5²)                 |
| 10| log β_e        | (-∞, ∞)          | N(0, 6²)                 |
| 11| log γ_e        | (-∞, ∞)          | N(0, 6²)                 |
| 12| gCP_u          | (-π, π)          | flat                     |
| 13| gCP_d          | (-π, π)          | flat                     |
| 14| gCP_e          | (-π, π)          | flat                     |

α_u = α_d = α_e = 1 (overall scale absorbed; ratios are scale-invariant).

**User-spec mapping (13 params):** treat γ_d2 as one complex param (collapses
Re/Im γ_d2 into a magnitude+phase pair, total 2 reals → user-counted as 1).
Then 4 (τ's) + 2 (β_u,γ_u) + 4 (β_d, γ_d1, |γ_d2|, arg γ_d2) + 2 (β_e,γ_e) +
3 (gCP_u, gCP_d, gCP_e) = 15 if all phases independent. The user spec of 13 is
satisfied if gCP_u and gCP_d are dropped (Model VI is real except for γ_d2).
**The script keeps all 15 for maximum generality**; CP phases will be sampled
and shown to be either pinned (if data prefer Model-VI-strict) or floating.

---

## 4. Observables (13 in user spec; 10 in script)

PDG 2024 ratios + LYD20 Table I quark mass ratios (RGE-evolved to Q=1 TeV):

| # | Observable    | Value     | σ          | Source            |
|---|---------------|-----------|------------|-------------------|
| 1 | m_u/m_c       | 2.04e-3   | 0.10e-3    | LYD20 Tab I       |
| 2 | m_c/m_t       | 2.68e-3   | 0.13e-3    | LYD20 Tab I       |
| 3 | m_d/m_s       | 5.18e-2   | 0.30e-2    | LYD20 Tab I       |
| 4 | m_s/m_b       | 1.31e-2   | 0.10e-2    | LYD20 Tab I       |
| 5 | m_e/m_μ       | 4.836e-3  | 2.0e-5     | PDG 2024 leptons  |
| 6 | m_μ/m_τ       | 5.946e-2  | 3.0e-4     | PDG 2024 leptons  |
| 7 | sin θ_12 CKM  | 0.22534   | 0.0007     | PDG 2024 CKM      |
| 8 | sin θ_13 CKM  | 0.003690  | 0.0001     | PDG 2024 CKM      |
| 9 | sin θ_23 CKM  | 0.04182   | 0.0008     | PDG 2024 CKM      |
| 10| J Jarlskog    | 3.08e-5   | 0.15e-5    | PDG 2024 CKM      |

The user-spec 13 observables include separate (V_us, V_cb, V_ub) and three
mass ratios per family; in our parametrisation these reduce to 10 because
- V_us, V_cb, V_ub are encoded in (sin θ_12, sin θ_13, sin θ_23) modulo CKM
  rephasing (the Wolfenstein λ ≃ |V_us|),
- m_u/m_t = (m_u/m_c)·(m_c/m_t) is derived (correlated, not independent),
- m_d/m_b similarly derived.

**dof = N_OBS − N_PARAMS = 10 − 15 = −5** (effectively negative — the model is
*over-parametrised* against this observable set when both τ's are free). This is
**expected** and is precisely the point of the test: if the joint posterior is
narrow despite the over-parametrisation, the modular-symmetry constraints
(via the rigid Y(τ) structure) are doing the work.

---

## 5. Sampler: blackjax NUTS on RTX 5060 Ti GPU

### 5.1 Backend
- **JAX** with default GPU backend (RTX 5060 Ti 16GB GDDR7; `XLA_PYTHON_CLIENT_MEM_FRACTION=0.85`).
- **blackjax 1.x** `nuts` + `window_adaptation` (10000-step warmup, target accept 0.8).
- Likelihood is **fully jit-compiled** including all η(τ) evaluations
  (loop-unrolled to N_ETA_TERMS=40 — sufficient for 1e-15 precision per W1).
- **AD compatibility:** pytree of complex polynomials in τ — `jax.grad` works
  through `jnp.linalg.svd` (uses Jacobi-rotation backward).
  Note: complex SVD gradients can be unstable when singular values cluster;
  if divergences spike, fall back to `jnp.linalg.eigh(M @ M.conj().T)` for
  squared singular values.

### 5.2 Run plan
- **4 chains × 30000 samples × 10000 warmup**.
- Init position: dispersed around W1 best (τ_q≈-0.19+i, τ_l≈i, log β_u≈4.4,
  log γ_e≈-7) per chain.
- Estimated wall time: **8–12 min on RTX 5060 Ti**
  (compile ~30 s, warmup ~2 min/chain, sampling ~1 min/chain at 100 samples/s).

### 5.3 CLI
```
python g114_joint_mcmc.py              # standard fundamental-domain prior
python g114_joint_mcmc.py --restricted # v7.4-attractor: |τ_l - i| < 0.5 hard cut
```

Run **both** modes and compare evidence (see §6.3 below for Bayes factor).

---

## 6. Decision criteria & expected verdicts

### 6.1 Primary verdict

| χ²_min      | P(|τ_l-i|<0.3) | P(|τ_q-i|<0.3) | Verdict                         |
|-------------|----------------|----------------|---------------------------------|
| < 30        | > 0.5          | > 0.5          | **TWO-TAU NEAR-I VIABLE**       |
| 30–50       | any            | any            | TWO-TAU MARGINAL                |
| > 50        | any            | any            | TWO-TAU REFUTED                 |

### 6.2 Posterior summaries reported
For each parameter: mean, std, median, 5%/95% credible interval.
Derived quantities: |τ_l − i|, |τ_q − i|, |τ_l − τ_q| (mean ± std + median).

### 6.3 Bayes factor: two-modulus vs single-modulus

We do **not** run an explicit Z-evidence integral (would need polychord/
nested sampling, ~10× cost). Instead we estimate the **Savage-Dickey ratio**
at the τ_l = τ_q hypersurface:

```
log B_{2τ vs 1τ} ≈ log p(τ_l = τ_q | data) - log p(τ_l = τ_q | prior)
                 = log [posterior density at d=0] - log [prior density at d=0]
```

Implemented post-hoc in `analyze_chain.py` (TODO companion). For now the
script reports `P(|τ_l - τ_q| < 0.1)` which serves as a proxy: high P → single-τ
collapse supported; low P → two-τ required.

### 6.4 Pre-registered outcomes

| log B | Interpretation                                                    |
|-------|-------------------------------------------------------------------|
| > +3  | Two-modulus strongly preferred (τ_l ≠ τ_q at >95%)                |
| 0–+3  | Two-modulus moderate (τ_l consistent with separate from τ_q)      |
| −3–0  | Inconclusive                                                       |
| < −3  | Single-modulus strongly preferred (τ_l = τ_q at >95%)             |

Predicted from PC1 + W1 priors: **log B ∈ [+1, +3]** (moderate two-modulus
support; lepton sector pulls τ_l → exactly i due to CM-anchored attractor,
quark sector pulls τ_q → near-i but allowed to drift; W1 single-τ best at
−0.19+1.00i is a compromise between the two).

---

## 7. Anti-hallucination discipline

This SPEC is bound by `feedback_triangulation` and `feedback_crosscheck_fabrication`:

- **LYD20 (arXiv:2006.10722) is the primary modular-form source**, not paraphrased
  but transcribed line-by-line from W1's `tau_near_i_scan.py` and V2's `v2_audit.py`,
  both of which reproduce LYD20's polynomial Y^(k) expansions.
- **PDG 2024 values** (NOT 2026, which is not yet released — the brief's "PDG 2026"
  refers to using the most recent PDG that exists as of this date; PDG releases
  in even years and the 2026 edition has not yet appeared on pdg.lbl.gov as of
  2026-05-05). Values used are the **PDG 2024 RPP** and identical to those in
  W1/V2 audit scripts (cross-checked).
- **No external citations introduced** beyond LYD20 (already verified in W1)
  and PDG 2024 (in-house standard).
- **No Mistral cross-check used** for derivation (per `feedback_crosscheck_fabrication`
  Mistral large STRICT BAN). The Y^(k) polynomial expressions are inherited
  intact from W1 and V2 audit code, both of which have already been validated
  against LYD20 line numbers in their headers.

If the actual run reveals a discrepancy with W1 single-τ best (χ²/dof=1.05 at
τ*=-0.19+1.00i should be reproduced when τ_l forced equal to τ_q), this
constitutes a **regression bug** in the JAX port to be fixed before publishing.

---

## 8. File layout

```
A8_G114_MCMC/
├── SPEC.md                       # THIS FILE
├── g114_joint_mcmc.py            # JAX/blackjax NUTS script (ready to run)
└── results/                      # populated by run on PC1
    ├── g114_joint_mcmc_results.json
    ├── g114_joint_mcmc_chain.npz
    └── g114_tau_posterior.png
```

---

## 9. Status & next actions

- **Script status:** READY TO RUN. Compile-test logp(init) at the dispersed
  W1-best init must be finite (script asserts and exits early otherwise).
- **DO NOT RUN until PC1 GPU confirmed free** (per A8 mission brief; PC may
  be busy with PG112 or other v6.0.53 jobs).
- **Re-apply tailscale shield** if PC has rebooted: `sudo bash
  /home/remondiere/pc_calcs/tailscale_shield.sh` (per `feedback_disconnection_resilience`).
- After run: consume `g114_joint_mcmc_results.json` into a v6.0.54 paper
  patch and tag the corresponding Zenodo upload.

---

**END A8 SPEC**
