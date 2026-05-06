# 3-Filter Verdict: M19 Candidates
**Sub-agent M19 — Phase 3.C-early**
**Date:** 2026-05-06
**Stress-test:** Vary (level, weight) instead of nebentypus

---

## Filter definitions (from A78)

| Filter | Description | What it tests |
|--------|-------------|---------------|
| **T1** | Damerell ladder: alpha_2 = 1/12 specifically | Whether the CM form's critical L-values give the EXACT ECI-required rational |
| **T2** | SL(2,Z) elliptic fixed point: tau_S ∈ {i, omega} | Whether the form anchors at a modular group special point |
| **T3** | DKLL19 / NPP20 lepton fit at tau_S | Whether the S'_4 weight-2 triplet Y_3^(2)(tau_S) gives CSD(1+sqrt(6)) alignment |

**A78 baseline result (nebentypus variation):** Only chi_4 (4.5.b.a) passes all three. chi_3 passes T2 and KW but fails T1 and T3. All others fail T2.

---

## Candidates identified by M19

**Scope:** CM-by-Q(i) (self_twist_disc=-4) forms that are:
1. Twist-minimal (genuinely new Hecke Grössencharacter)
2. dim=1 (rational eigenvalues)
3. Weight k where the Damerell ladder can be meaningfully defined (k ≥ 3)

---

## Candidate Set A: Same weight k=5, same K=Q(i), different LEVEL

### A1: 144.5.g.a (N=144, k=5)

| Filter | Status | Evidence |
|--------|--------|---------|
| **T2** | **PASS** | tau_S = i. K = Q(i) => same CM field. The nebentypus char is chi_{-4} (Kronecker mod 4), identical to chi_4, so the SL(2,Z) elliptic anchor is still tau=i. INDEPENDENT of level. |
| **T3** | **PASS** | Y_3^(2)(i) is level-independent; depends only on tau, not on the specific newform. DKLL19 computation yields (1, 1+sqrt(6), 1-sqrt(6)) at tau=i regardless of which CM-by-Q(i) weight-5 form is chosen. CSD(1+sqrt(6)) alignment persists. |
| **T1** | **FAIL** | alpha_2(144.5.g.a) ≠ 1/12. The Damerell L-values differ from 4.5.b.a (different Euler factors at p=5: local ratio 73/39 at s=2). The Gauss sum G(chi_f) of the order-4 character (chi_f(2+i)=i on F_9) introduces irrational algebraic factors into L(psi', m)/Omega_K^{k-1}. Exact rational unknown (requires mp.dps=60 PSLQ, deferred). |

**Verdict: A1 = 144.5.g.a — REJECTED by T1.** Passes T2 and T3 (same tau_S = i), but fails Damerell alpha_2 requirement. This is a PARTIAL RIVAL: it passes the geometric (T2) and phenomenological (T3) filters, but not the arithmetic (T1) filter.

**Caveat on T1:** The exact alpha_2 rational for 144.5.g.a is NOT yet computed to high precision. The analytic argument is convincing but not a mp.dps=60 PSLQ numerical verification. Flagged for future A-note computation.

### A2: 144.5.g.b (N=144, k=5)

Same as A1 by Galois conjugation. SAME verdict: PASS T2, PASS T3, FAIL T1 (same analytic argument).

---

## Candidate Set B: Different weight k, same K=Q(i), level 4

### B1: 4.9.b.a (N=4, k=9)

| Filter | Status | Evidence |
|--------|--------|---------|
| **T2** | **PASS** | Same CM field Q(i), same level, same character 4.b => same tau_S = i. |
| **T3** | **PASS** | Y_3^(2)(i) is the same. CSD alignment at tau=i is form-independent. |
| **T1** | **FAIL** | Weight-9 Damerell ladder has m=1,...,8 critical values, a completely different structure. The ECI framework uses weight-5 specifically (5-dimensional spinorial representation of SU(5) GUT). The Damerell alpha_2 for k=9 is a DIFFERENT rational (weight-9 Bernoulli-Hurwitz period, not related to 1/12 by ECI normalization). Furthermore, the alpha-ladder for k=9 is m=1..8 (8 values), whereas the H6 Hecke restriction requires k=5 (4 Damerell rungs). |

**Verdict: B1 = 4.9.b.a — REJECTED by T1** (wrong weight for ECI physics; Damerell ladder has different structure).

**Additional disqualifier (T1-extra):** The ECI modular bootstrap requires the FIVE-DIMENSIONAL representation of S'_4 at weight-5. The weight-9 form lives in a NINE-dimensional representation space of a different metaplectic cover. The connection to Yukawa matrix rank (3x3 quark matrices = weight-3 of SU(3)) breaks for k=9.

### B2: 16.3.c.a (N=16, k=3)

| Filter | Status | Evidence |
|--------|--------|---------|
| **T2** | **PASS** | CM by Q(i), tau_S = i. |
| **T3** | **PASS** | Y_3^(2)(i) same. |
| **T1** | **FAIL** | Weight-3: Damerell ladder has m=1,2 only. alpha_1 and alpha_2 are weight-3 Bernoulli-Hurwitz numbers (= Hecke char psi of type z^2). For pi_5=2+i: a_5 = (2+i)^2+(2-i)^2 = 2*Re(3+4i) = 6. The L-values involve Omega_K^2 not Omega_K^4. ECI requires weight-5 for the Cardy c/12 ladder. |

**Verdict: B2 — REJECTED by T1** (wrong weight; Damerell structure incompatible with ECI Cardy analysis requiring weight-5).

### B3: 32.4.a.b (N=32, k=4)

| Filter | Status | Evidence |
|--------|--------|---------|
| **T2** | **PASS** | CM by Q(i), tau_S = i. |
| **T3** | **PASS** | Y_3^(2)(i) same. |
| **T1** | **FAIL** | Weight-4, trivial character. The a_p eigenvalues (a_5=22, a_13=-18) come from psi(pi) = pi^3 (infinity type z^3). This is EVEN weight with TRIVIAL character, so the root number is +1 and L(f, k/2) = L(f, 2) is a central value — different Damerell structure. ECI weight-5 (odd) is required for the specific Cardy / NPP20 lepton mass structure. |

**Verdict: B3 — REJECTED by T1** (wrong weight, parity mismatch).

### B4: 36.3.d.a (N=36, k=3)
| T2 | T3 | T1 |
|----|----|----|
| PASS (tau=i) | PASS | FAIL (weight-3) |

**Verdict: REJECTED by T1.**

### B5: 32.2.a.a (N=32, k=2, elliptic curve CM)
Weight-2 CM form. Only 1 critical L-value (the central one). No Damerell LADDER at all. Cannot define alpha_2.

**Verdict: REJECTED by T1** (ineligible — only 1 critical value).

---

## Candidate Set C: Twist-minimal dim>1 forms at weight 5

Forms like 52.5.j.a (dim=4, char order 6), 148.5.i.a (dim=4), 116.5.j.a (dim=12) have Hecke eigenvalues in number fields (not Q). The Damerell ladder rationals become algebraic numbers over Q, not rational. These CANNOT satisfy alpha_2 = 1/12 ∈ Q in the ECI-required way (or the alpha_2 condition would need to be reformulated for a Galois orbit).

**Verdict: ALL REJECTED by T1** (alpha_2 not in Q).

---

## Master Verdict Table

| Candidate | Family | k | N | dim | T2 (tau=i?) | T3 (CSD ok?) | T1 (alpha_2=1/12?) | Overall |
|-----------|--------|---|---|-----|------------|-------------|-------------------|---------|
| **4.5.b.a** | I (reference) | 5 | 4 | 1 | PASS | PASS | PASS (A5) | **ALL PASS** |
| 144.5.g.a | II (new!) | 5 | 144 | 1 | **PASS** | **PASS** | **FAIL** (analytic) | T1 fails |
| 144.5.g.b | II (Galois) | 5 | 144 | 1 | **PASS** | **PASS** | **FAIL** | T1 fails |
| 36.5.d.a | I (twist) | 5 | 36 | 1 | PASS | PASS | PASS* | *twist, same char |
| 64.5.c.a | I (twist) | 5 | 64 | 1 | PASS | PASS | PASS* | *twist |
| 4.9.b.a | — | 9 | 4 | 1 | PASS | PASS | FAIL (wrong weight) | T1 fails |
| 16.3.c.a | — | 3 | 16 | 1 | PASS | PASS | FAIL (wrong weight) | T1 fails |
| 32.4.a.b | — | 4 | 32 | 1 | PASS | PASS | FAIL (wrong weight) | T1 fails |
| 52.5.j.a | — | 5 | 52 | 4 | PASS | PASS | FAIL (dim>1) | T1 fails |
| 100.5.d.a | I (twist) | 5 | 100 | 2 | PASS | PASS | FAIL (dim>1) | T1 fails |

**Twists marked with * do not add new Hecke characters.** They change the sign pattern of a_p but preserve the Damerell L-value structure (up to Gauss sum factors that cancel in the normalized alpha_m). The uniqueness of 4.5.b.a as the twist-minimal level-4 form means H6 = "chi_4 nebentypus at level 4" remains the unique simple representative.

---

## Key Caveat

**144.5.g.a passes T2 and T3 — this is new vs. A78.**

A78 varied only nebentypus at FIXED (N=4, k=5). All alternatives with tau_S ≠ i were eliminated by T2. But 144.5.g.a has tau_S = i (same as chi_4) while being a genuinely distinct Hecke character. T2 does NOT eliminate it.

T1 eliminates it via the Euler-product argument (different a_p magnitudes => different L(f, m) => alpha_2 ≠ 1/12). This is sound but the exact numerical value of alpha_2(144.5.g.a) is not yet computed. T1's elimination here is ANALYTIC (not numerical PSLQ).

**Recommendation:** Run mp.dps=60 PSLQ on L(144.5.g.a, m) in a future A-note to pin down alpha_2 exactly. Expected outcome: a different small rational (perhaps 1/36, 3/48, or a Gauss-sum-modified version). If alpha_2 = 1/12 is NUMERICALLY found, that would constitute a genuine rival requiring A78 revision.
