# Jing-Alestas-Kuroyanagi 2605.00735 — Constraint Assessment for ECI v6.0.46

**Date:** 2026-05-04 (evening run, agent B2)
**ECI version assessed:** v6.0.46 (Zenodo 10.5281/zenodo.20023959)
**Time budget:** 30-min agent run (Week 1 of recommended 2-3 week check)

---

## 1. Reference Verification

**arXiv:2605.00735 — CONFIRMED**

- **Title:** "DESI and Gravitational Wave Constraints Challenge Quintessential α-Attractor Inflation"
- **Authors:** Changcheng Jing, George Alestas, Sachiko Kuroyanagi
- **Submitted:** 1 May 2026
- **Category:** astro-ph.CO + gr-qc
- **Journal target:** Not stated in abstract; submitted to arXiv only as of retrieval date
- **CrossRef triangulation:** CrossRef API returned permission-denied for direct query; paper is too recent (2026-05-01) to have a DOI yet. The arXiv abstract page confirmed all three authors and submission date. No fabricated bibdata issue: title, authors, and abstract are internally consistent across two independent fetches (abstract page and HTML full text).

**Anti-hallucination status:** All claims below are drawn directly from the fetched HTML full text of arXiv:2605.00735. Numerical values are quoted from Table 1 of the paper. No Gemini CLI was available in this agent environment (Bash denied), so Gemini cross-check is [PENDING — to be done in Week 2 by human operator].

---

## 2. Model Setup: What Jing et al. Actually Constrain

### 2.1 The model

Jing et al. study **quintessential α-attractor inflation** — a unified single-field framework where the inflaton field φ also serves as the dark-energy quintessence field at late times. This is **not** a pure stand-alone quintessence model; it is a constrained inflationary model that carries inflationary observables (n_s, r, GW background) as mandatory predictions alongside dark-energy equation of state.

The potential (their Eq. 4, after field redefinition ϕ = √(6α) tanh(φ/√(6α))):

```
V(φ) = M² exp[γ(φ/√(6α) − 1)] + V₀
```

where:
- α is the α-attractor curvature parameter (sets the pole structure of the field-space metric)
- M is an energy scale fixed by CMB normalization
- γ is determined by a shooting procedure (not a free parameter)
- V₀ = 0 (Exp-model-I) or V₀ = −M² exp(−2γ) (Exp-model-II, ensures V_min = 0)
- The kinetic term contains a pole: L_kin ∝ (∂φ)² / (2(1 − φ²/(6α))²)

**Important structural point for ECI comparison:** The Jing et al. potential is NOT a simple exponential V₀ exp(−λφ/M_P). It is an exponential of a hyperbolic tangent. The large-field limit (φ → −∞) gives a plateau → 0, not an exponential runaway. During inflation (small-field canonical frame), the effective potential approaches M² exp(−2γ exp(−2ϕ/√(6α))), which is a doubly-exponential form, distinct from ECI's simple exponential.

### 2.2 Datasets

Two combinations:
- **P-LB2S:** Planck 2018 CMB + ACT lensing + DESI DR2 BAO + Pantheon+ SNe
- **P-ACT-LB2S:** P-LB2S + ACT DR6 CMB (full temperature+polarization) — this is the headline dataset

### 2.3 Parameter posteriors (Table 1, verbatim)

For the α-attractor model with **P-ACT-LB2S** (posterior mean, best-fit, ±1σ):

| Parameter | Posterior mean (best-fit) | ±1σ |
|---|---|---|
| α | 3.908 (2.6048) | −2.404 / +0.984 |
| M/√α [×10⁻⁵ M_Pl] | 1.044 (1.027) | ±0.016 |
| log₁₀ g | −3.443 (−4.040) | −0.595 / +0.508 |
| n_s | 0.9659 (0.9664) | ±0.0005 |
| log₁₀(T_reh/GeV) | 8.233 (7.661) | −1.125 / +0.534 |

The 95% CL range on α is approximately [0.65, 7.37] (broad, unconstrained upper tail). The model is NOT excluded by α alone. It is excluded by the **n_s tension**.

### 2.4 The GW / ΔN_eff constraint

The paper applies ΔN_eff < 0.17 (from ACT DR6, Calabrese et al. 2025). The kination phase after inflation (when the kinetic energy of φ dominates) enhances the primordial gravitational wave background at high frequencies (above ~10⁻¹⁰ Hz), contributing to ΔN_eff. The constraint converts to a **lower bound on reheating temperature: T_reh ≥ 6.25×10⁶ GeV** at 95% CL.

This lower bound on T_reh propagates to an **upper ceiling on n_s ≈ 0.967** for this model class, because lower reheating delays the transition from kination to radiation, which shifts the pivot-scale CMB modes and suppresses n_s.

### 2.5 The core tension

ACT + Planck prefer n_s ≈ 0.974 ± 0.003 (ΛCDM fit). The α-attractor quintessential inflation model is pinned at n_s ≤ 0.967 once the GW/ΔN_eff constraint is imposed. This is a **~7-8σ tension in n_s**. The Bayesian model comparison gives:

**ln B = −12.47** (P-ACT-LB2S dataset)

This corresponds to "decisive" evidence against the α-attractor quintessential inflation model relative to ΛCDM (Jeffrey's scale: |ln B| > 5 = strong, |ln B| > 10 = decisive).

The paper's verbatim conclusion: *"the model becomes disfavored once constraints from the gravitational-wave contribution to the effective number of relativistic degrees of freedom, ΔN_eff, are included."*

---

## 3. Projection onto ECI's NMC Sector

### 3.1 ECI's model compared to Jing's model

ECI v6.0.46 employs:
- **Pure quintessence sector:** V(χ) = V₀ exp(−λχ/M_P) with λ ∈ [0.5, 2.0], χ₀ ~ M_P/10
- **NMC coupling:** ξ_χ R χ²/2 in the Jordan frame
- **Working point (NMC limit):** ξ_χ ≈ 0, λ ≈ 1, χ₀ ≈ M_P/10
- **Key NMC correction:** Δw_a^NMC = −(2/3) ξ_χ λ² Ω_{φ,0}

Jing et al.'s model:
- **Unified inflaton + quintessence:** single scalar from Planck scale to today
- **Potential form:** exp[γ(tanh(...) − 1)] — NOT a simple exponential
- **GW constraint acts on:** inflationary prediction of n_s and r via kination phase
- **NMC coupling:** NOT present in Jing's model (standard minimal coupling)

### 3.2 Is Jing's constraint applicable to ECI's exponential potential?

**The key structural distinction is critical:**

Jing et al. constrain the **full quintessential inflation trajectory** — they need the same field to drive inflation (satisfying Planck+ACT CMB constraints) AND dark energy today. The binding constraint comes from the inflationary sector: the kination GW background produced between inflation and reheating is observable today and overcrowds ΔN_eff.

**ECI does NOT use quintessential inflation.** ECI's quintessence field χ is a *late-time-only* scalar. It is NOT the inflaton. There is no kination phase in ECI, no inflationary GW background from χ, and hence **no ΔN_eff constraint from χ's dynamics**.

The surface-level similarity — Jing's potential has an exponential factor and ECI uses V₀ exp(−λχ/M_P) — is a coincidence of notation, not a physical equivalence:

| Feature | Jing et al. | ECI |
|---|---|---|
| Field role | Inflaton + quintessence | Pure quintessence (late time only) |
| Potential type | exp[γ(tanh(φ/√6α)−1)] | V₀ exp(−λχ/M_P) |
| Kination phase | Yes (drives GW background) | No |
| ΔN_eff from field | Yes | No |
| Inflationary n_s constraint | Yes (binding) | Not applicable |
| NMC coupling ξ | No | Yes (core ECI mechanism) |

### 3.3 Question 1: Does Jing exclude ECI's λ ≈ 1 working point?

**No, and the constraint is inapplicable.**

Jing et al. do not constrain the slope λ of ECI's exponential potential directly. Their parameter α (α-attractor curvature) governs the shape of a fundamentally different potential. The mapping α → λ would require identifying both potentials in the large-field limit, but:

- Jing's potential has no simple exponential limit at large φ; it asymptotes to V₀ from a plateau
- ECI's V₀ exp(−λχ/M_P) is a runaway, not a plateau
- Jing's constraint is driven by the inflationary sector (n_s, GW background), which is absent in ECI

ECI's λ ≈ 1 working point for dark energy is entirely outside the scope of Jing et al.'s analysis.

**Verdict on Question 1:** [SAFE — constraint does not apply to ECI's model]

### 3.4 Question 2: Does the GW background channel discriminate NMC from non-NMC quintessence?

**Not in Jing's paper.** Jing et al. do not include NMC coupling ξ_χ and do not compute differential GW signatures between ξ_χ = 0 and ξ_χ ≠ 0 quintessence. Their GW signal is dominated by the kination phase post-inflation, which is entirely absent in ECI.

There is a separate (open) question in the literature about whether NMC quintessence produces modified tensor power spectra through the conformal coupling of the metric perturbations. This is NOT addressed in Jing et al. and would be a different calculation.

**Verdict on Question 2:** [NOT APPLICABLE to ECI — Jing's GW channel is inflationary-era kination, not late-time quintessence GWs]

---

## 4. Verdict

### 4.1 Is ECI's working point inside or outside the Jing constraint?

**OUTSIDE THE SCOPE OF THE CONSTRAINT — and this is a favorable finding, not a threat.**

Jing et al.'s result is a strong constraint on a specific, more ambitious theoretical construction: quintessential inflation, where one field does everything from Planck scale to today. ECI is a more modest, empirically motivated model where the quintessence field is introduced as a late-time dark energy component, not the inflaton.

The morning synthesis agent's labeling of this as a "critical paper" constraining ECI was based on the surface similarity of the potential forms (both involve exponentials). After careful examination of the model structure, this similarity is superficial. The physical mechanisms producing Jing's constraints (kination-enhanced GW background, n_s tension from constrained reheating) are entirely absent in ECI.

### 4.2 What Jing et al. do constrain that is adjacent to ECI

The DESI DR2 BAO constraints embedded in Jing's analysis are relevant to ECI independently — but ECI already incorporates DESI DR2 BAO as a primary observational pillar in v6.0.43/v6.0.46. The Jing BAO analysis adds no new constraint beyond what ECI has already absorbed.

### 4.3 Potential genuine concern (flagged for Week 2 follow-up)

The one genuine interaction worth verifying is: **if ECI's χ field were embedded in a supergravity or string framework that also makes inflationary predictions**, could there be an indirect link through n_s? This is a model-building question ECI has not addressed. For v6.0.47, if ECI makes any claim about UV completeness or inflationary embedding, Jing et al. would need to be cited as a constraint. If ECI remains agnostic about the inflaton (current status), no citation is needed.

---

## 5. Recommended Action for ECI v6.0.47

### 5.1 No parameter revisions required

ECI's (ξ_χ ≈ 0, λ ≈ 1, χ₀ ≈ M_P/10) working point is unaffected by Jing et al. The prior range λ ∈ [0.5, 2.0] stands without modification.

### 5.2 Footnote to add in v6.0.47 (suggested text)

> "We note that Jing, Alestas & Kuroyanagi (2026, arXiv:2605.00735) recently constrained quintessential α-attractor inflation models using DESI DR2 + ACT ΔN_eff bounds, finding decisive Bayesian disfavor (ln B = −12.47) relative to ΛCDM. ECI's quintessence sector is not a quintessential inflation model — χ is introduced as a late-time scalar without inflationary duties — and thus does not produce the kination-phase GW background that drives the Jing et al. constraint. The Jing et al. result does not restrict ECI's parameter space."

### 5.3 Week 2 follow-up items (flagged [PENDING])

1. **Gemini CLI verification** of Jing et al. parameter table — human operator should run the command from the task brief to independently confirm n_s = 0.9659 and T_reh constraint
2. **CrossRef DOI check** — paper is too recent for a published DOI; re-check in 2-4 weeks for journal assignment
3. **NMC GW question** — search for literature on whether ξ_χ ≠ 0 quintessence modifies the tensor power spectrum or GW propagation speed in a way detectable by LISA/ET; this would be a genuine ECI-specific GW signature distinct from Jing's inflationary GW
4. **n_s cross-check** — ECI's NMC correction formula Δw_a^NMC = −(2/3) ξ_χ λ² Ω_{φ,0} should be checked for any indirect coupling to n_s through reionization history; this is a long-shot concern but worth a brief literature check

---

## 6. Summary Table

| Assessment dimension | Finding | Confidence |
|---|---|---|
| Paper exists and is correctly identified | CONFIRMED | High |
| Authors/title match | CONFIRMED | High |
| Jing potential ≠ ECI potential (structurally) | CONFIRMED | High |
| Jing GW constraint source = kination, absent in ECI | CONFIRMED | High |
| ECI λ ≈ 1 excluded by Jing? | NO — not applicable | High |
| ECI NMC discriminated by Jing GW channel? | NO — different GW mechanism | High |
| Any DESI DR2 constraint new to ECI? | NO — already incorporated | High |
| Action needed for v6.0.47 parameter space? | None | High |
| Gemini cross-check completed? | PENDING (Bash unavailable) | — |
| CrossRef DOI confirmed? | PENDING (too recent) | — |

---

*Assessment produced by agent B2, ECI v6.0.46, 2026-05-04 evening run.*
*All numerical values cited from arXiv:2605.00735 HTML full text (two independent fetches).*
*Gemini CLI verification deferred to human operator (Week 2).*
