# W4 — G1.12 and G1.14 Assessment
**Date**: 2026-05-04 | **Agent**: claude-sonnet-4-6

---

## Context

H3 GUT-scale ratio: y_c/y_t = 2.725e-3 (LYD20 Model VI, tau=i). SM 2-loop target (Wang-Zhang 2025, arXiv:2510.01312): 3.256e-3. Gap = +19.5% needed at GUT scale.

---

## G1.12 — GUT Threshold Corrections

### Mechanism

In non-SUSY SU(5), 1-loop matching at M_GUT modifies Y_d = Y_e^T to Y_d = Y_e^T + DeltaY via colored Higgs triplet T (3,1,-1/3) loops — functions f[M_T^2,0] and h[M_T^2,0]. Source: Patel & Shukla 2023 (arXiv:2310.16563, PRD 109, 015007 — LIVE-VERIFIED). The 3rd-generation down-type correction (y_b/y_tau: unity to ~2/3) requires 30-40% shifts, achieved when one scalar mass departs from M_GUT by up to ~13 orders of magnitude. Antusch & Spinrath 2008 (arXiv:0804.0717, PRD 78, 075020 — LIVE-VERIFIED) confirm SUSY threshold corrections give "significant" enlargement of GUT-scale Yukawa ranges.

### Critical caveat for y_c/y_t

The +19.5% gap is in the UP-TYPE sector. In minimal SU(5) with 5_H only, Y_u^GUT = Y_u^SM at tree level (symmetric matrix, no lepton-quark cross-contamination). Colored triplet corrections to Y_u are suppressed. A **45_H extension is required** to generate corrections to (Y_u)_22/(Y_u)_33 of the correct sign and magnitude. The exact threshold formula for this entry is [I-DO-NOT-KNOW] without explicit computation.

### Verdict G1.12

**[INCONCLUSIVE — depends on specific embedding, needs choice + computation]**

+19.5% is within the natural range of GUT threshold corrections (30-40% seen for 3rd-gen down-type). Sign is achievable but requires non-minimal Higgs sector (5_H + 45_H). Risk: modular structure of LYD20 must survive coupling to 45_H. Timeline: 3-6 months.

---

## G1.14 — Two-tau Picture

### Published precedents (all LIVE-VERIFIED)

1. **arXiv:2209.08796** (Tanimoto & Yamamoto, JHEP 01(2023)036): Flipped SU(5) + A4. Introduces two independent moduli tau_q, tau_l. chi^2 drops from 282.4 (single tau) to 95 (two-tau). Explicitly discusses "possible ways to assign different moduli values for quarks and leptons in modular GUT scheme."

2. **arXiv:2212.10666** (Ding et al. 2022): A4 with THREE moduli (tau_l, tau_nu, tau_q). Fixed-point assignments: tau=i for leptons (A4->Z2), tau=e^{i2pi/3} for quarks (A4->Z3). Motivation is explicit: "three moduli naturally obtained in orbifold compactification of T^6/Gamma" — string-theoretic.

3. **arXiv:2310.10369** (2023): Multiple-modulus stabilisation. Shows dS minima at tau=i and omega simultaneously via non-perturbative effects. Provides dynamical mechanism for fixing two moduli at CM points.

### ECI compatibility

- tau_lepton = i is the exact lepton-sector fixed point used in 2212.10666 (A4->Z2). ECI's CM anchor via Q(i) is a theoretically stronger motivation for the same choice.
- tau_quark = -0.21+1.52i (LYD20-best) is not a CM point, but data-driven moduli away from fixed points are standard in 2209.08796.
- The Q(i) CM anchor for representations 3-hat, 2(5) applies to the lepton sector only. Quark sector loses algebraic anchor but gains data-driven fit quality. This split is precedented and publishable.

### Is two-tau novel or ad hoc?

NOT novel — precedented since 2022 by at least 2 independent published models with string-theoretic motivation. ECI's distinguishing contribution: first to combine two-tau split with explicit CM-algebraic anchor (Q(i)) providing theoretical motivation for tau_lepton = i. This is a **feature**.

### Verdict G1.14

**[TWO-TAU PROPOSED IN LITERATURE — ECI fits in, possibly publishable as variation]**

Two-tau/multi-moduli is standard since 2022. ECI's tau_lepton = i aligns with the literature's lepton-sector fixed point. The CM anchor survives the split. Main open question: stabilisation of tau_quark (tractable via arXiv:2310.10369).

---

## Recommended Next Gate

1. **G1.14 first** (2-3 months): cite 2209.08796 + 2212.10666 as precedent; specify modular group for quark sector at tau_quark; verify LYD20 fit at tau_quark = -0.21+1.52i for quarks alone.
2. **G1.12 parallel** (3-6 months): commit to 5_H + 45_H embedding, compute threshold correction to (Y_u)_22/(Y_u)_33.
3. Read W1 (G1.13) before final gate — if tau-near-i resolves the gap, G1.14 + G1.12 become supporting structure.
G1.14 and G1.12 are **compatible**: a two-tau GUT model with thresholds is coherent. Begin both tracks.

---

## Anti-Hallucination Register

| Claim | Status |
|---|---|
| arXiv:2209.08796 | LIVE-VERIFIED |
| arXiv:2212.10666 | LIVE-VERIFIED |
| arXiv:2310.10369 | LIVE-VERIFIED |
| arXiv:2310.16563 (PRD 109, 015007) | LIVE-VERIFIED |
| arXiv:0804.0717 (PRD 78, 075020) | LIVE-VERIFIED |
| "Hall-Sarid 1993 PRD 48 1066" | NOT VERIFIED — not used |
| "Babu-Mohapatra-Pelaggi-Trippe 2017" | NOT VERIFIED — likely fabricated; not used |
| Exact threshold formula (Y_u)_22/(Y_u)_33 | [I-DO-NOT-KNOW] |
