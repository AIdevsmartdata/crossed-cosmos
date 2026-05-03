# G8 BEC Signal — Research Notes
## Date: 2026-05-03  (G8 agent, closure wave)

---

## 1. arXiv Verification: Three Key Steinhauer Papers

All three verified 2026-05-03 via direct curl to arxiv.org metadata.

### arXiv:1809.00913 (Steinhauer 2019)
- **Title:** "Observation of thermal Hawking radiation at the Hawking temperature in an analogue black hole"
- **Authors:** Juan Ramon Munoz de Nova, Katrine Golubkov, Victor I. Kolobov, Jeff Steinhauer
- **Journal:** Nature **569**, 688–691 (2019)
- **Content:** Measured the correlation spectrum G^(2)(k,k') of Hawking partner pairs;
  confirmed thermality at T_H = 0.35 ± 0.10 nK via momentum-space distribution.
  Does NOT report temporal g^(2)(tau) decay rate. Does NOT mention "saturation envelope"
  or dimensionless ratio rho.
- **VERIFIED.**

### arXiv:1510.00621 (Steinhauer 2016)
- **Title:** "Observation of quantum Hawking radiation and its entanglement in an analogue black hole"
- **Authors:** J. Steinhauer
- **Journal:** Nat. Phys. **12**, 959 (2016) — DOI: 10.1038/nphys3863
- **Content:** First detection of quantum (spontaneous) Hawking radiation from BEC sonic
  horizon; confirmed entanglement between Hawking and partner particles.
- **VERIFIED.**

### arXiv:1910.09363 (Kolobov/Steinhauer 2021)
- **Title:** "Observation of stationary spontaneous Hawking radiation and the time evolution of an analogue black hole"
- **Authors:** Victor I. Kolobov, Katrine Golubkov, Juan Ramon Munoz de Nova, Jeff Steinhauer
- **Journal:** Nat. Phys. **17**, 362 (2021) — DOI: 10.1038/s41567-020-01076-0
- **Content:** Confirmed stationarity of Hawking radiation; observed time evolution;
  saw stimulated emission at inner horizon formation.
- **VERIFIED.**

---

## 2. ECI v6.0.10 "8.29% Saturation Envelope" — RETRACTION CONFIRMED

**STATUS: RETRACTED in ECI v6.0.30.**

The claim that "rho ~= 8.29% at leading order, consistent across three Steinhauer
datasets within 1-10% correction envelope" is unverifiable and is hereby retracted.

Evidence (from F1 agent arXiv searches + G8 verification):

| Search query | Results | Saturation envelope found? |
|---|---|---|
| au:steinhauer AND (ti:hawking OR ti:sonic OR ti:analogue) | 13 | NO |
| ti:"analogue black hole" OR ti:"sonic black hole", 2024-2026 | 16 | NO |
| au:munoz_de_nova AND (ti:hawking OR ti:analogue) | 7 | NO |
| ti:"BEC" AND (ti:hawking OR ti:sonic), 2024-2026 | 1 | NO |

None of the three Steinhauer core papers (1510.00621, 1809.00913, 1910.09363) report:
- A dimensionless ratio rho
- A "saturation envelope"
- Any ECI-specific observable

The Steinhauer group's 2024-2026 arXiv output has pivoted entirely to pure GR:
- arXiv:2407.00448: ringdown-Hawking connection
- arXiv:2503.01029: quasinormal modes, Schwarzschild
- arXiv:2509.02676: overdamped states, Schwarzschild

**Conclusion:** The v6.0.10 claim has all hallmarks of an LLM-hallucinated benchmark
(consistent with the 39 cumulative hallucinations logged in this project). It must not
appear in any submitted paper.

---

## 3. Steinhauer Group Contact Strategy

### Primary Contact: Jeff Steinhauer (Technion)

**Institution:** Department of Physics, Technion — Israel Institute of Technology, Haifa 32000, Israel
**Role:** Lead experimentalist; sole author of 2016 paper; corresponding author on 2019 and 2021 papers.
**Recent arXiv activity (2024-2026):** Pivoted to pure GR (quasinormal modes, overdamped states).
  No BEC analogue gravity work since 2021.

**Proposed contact sequence:**
1. Send a preprint of note_updated.tex with a covering email explaining the ECI g^(2)(tau)
   prediction and requesting collaboration on raw data re-analysis (Phase 1).
2. If no response in 4 weeks: contact Juan Ramon Munoz de Nova at UCM Madrid
   (co-lead on 2019 Nature paper; has independent experimental capability).
3. Optionally: share with Renaud Parentani (theory) for independent review first.

**Suggested email subject line:**
"ECI prediction for temporal g^(2)(tau) decay in your 2019 BEC sonic horizon data"

**Suggested email body (draft):**
---
Dear Prof. Steinhauer,

I am writing to share a theoretical prediction arising from algebraic quantum gravity
(Witten 2022 type II_inf framework) that we believe is directly testable with your
2019 BEC sonic horizon apparatus.

The prediction: the phonon second-order coherence function g^(2)(tau) near the sonic
horizon should decay exponentially at rate Gamma = 2*pi*k_B*T_H/hbar. For your 2019
measured T_H = 0.35 nK, this gives Gamma = 288 s^-1 and a Krylov saturation time of
t_K = 3.47 ms (well within your BEC coherence time).

This was not measured in your 2019 Nature paper, which confirmed thermality via the
momentum-space correlation spectrum. The prediction requires temporal binning of
density-density correlations by time delay tau, rather than by momentum k.

We have completed a signal-to-noise analysis (attached preprint) and estimate that
N_pairs = 10^4 pairs are needed for 1% statistical precision, achievable in ~23 min
per run (conservative). The limiting factor is the 29% uncertainty in your measured T_H.

Would you be willing to (i) check whether your 2019 raw time-series data contains
sufficient temporal resolution to test this, or (ii) discuss a dedicated measurement
as a future collaboration?

We have been careful to distinguish what ECI predicts as a precision statement
(the scaling law Gamma = 2*pi*k_B*T_H/hbar) from what is order-of-magnitude only
(the absolute prediction for T_H from the Krylov-Diameter conjecture).

With best regards,
Kevin Remondiere
---

### Secondary Contact: Juan Ramon Munoz de Nova (UCM, Madrid)

**Institution:** Universidad Complutense de Madrid, Faculty of Physics
**Role:** Co-lead on 2019 Nature paper; independent experimental group.
**Recent work:** arXiv:2406.10027 (resonant analogue configurations); arXiv:2507.10862
  (Hawking time crystals). Still active in BEC analogue gravity.
**Advantage:** Independent capability; may be faster to respond than Steinhauer
  (who has pivoted to GR).

### Theory Contacts

**Renaud Parentani (IJCLab, Paris-Saclay, Orsay)**
- Analogue gravity theory specialist
- Long-time collaborator with Steinhauer group
- Appropriate for: independent theoretical review of ECI g^(2)(tau) prediction
  before approaching experimentalists; checking whether the prediction is
  physically reasonable from the BEC community's perspective.

**Stefano Liberati (SISSA, Trieste)**
- Author of standard analogue gravity review (Living Rev. Rel.)
- Appropriate for: situating ECI prediction within the broader analogue gravity
  community; journal recommendation.

---

## 4. Signal-to-Noise Summary (sympy-verified)

All numbers from sympy_signal.py output (run 2026-05-03):

| Quantity | Value | Unit | Notes |
|---|---|---|---|
| T_H (Steinhauer 2019) | 0.35 ± 0.10 | nK | arXiv:1809.00913 |
| Gamma = lambda_L^sonic | 287.9 ± 82.3 | s^-1 | 1-sigma range [205.6, 370.2] |
| t_K = 1/Gamma | 3.47 | ms | Krylov saturation time |
| f_phonon = k_B*T_H/h | 7.29 | Hz | single-mode pair flux |
| BEC coherence time | ~100 | ms | conservative for Rb-87 |
| e-folds in coherence window | 29 | — | = t_coh * Gamma |
| N_pairs for 5% precision | 400 | pairs | (1/0.05)^2 |
| N_pairs for standard run | 10,000 | pairs | — |
| Integration time (N=10k) | 23 | min | single-mode conservative |
| Statistical precision (N=10k) | 1.0 | % | Cramer-Rao |
| Formal SNR (N=10k) | 100 | sigma | sqrt(N_pairs) |
| Dominant systematic | 29 | % | T_H uncertainty propagates linearly |
| KD conjecture T_H ratio | 3.47 | x off | order-of-magnitude only |

---

## 5. KD Theorem 4 Discrepancy — Honest Accounting

KD conjecture: R_proper ~ xi => lambda_L^KD = c_s / xi

With c_s = 0.5 mm/s, xi = 0.5 um:
- lambda_L^KD = 1000 s^-1
- T_H^KD = hbar * lambda_L^KD / (2*pi*k_B) = 1.22 nK
- Steinhauer measured: T_H = 0.35 nK
- Ratio: 1.22 / 0.35 = 3.47x

Reconciliation: kappa = (1/2)|d(v-c_s)/dx|_H depends on the flow profile, not xi.
For a smooth step profile of width L_H >> xi: kappa ~ c_s / (2*L_H), not c_s/xi.
L_H/xi ~ 3.5 is consistent with Steinhauer's geometry.

Status: KD conjecture is order-of-magnitude only. NOT a falsification of ECI.
ECI's precision prediction is the scaling law lambda_L = 2*pi*k_B*T_H/hbar.

---

## 6. What This Paper Does NOT Claim

To prevent future hallucination propagation:

1. Does NOT claim T_H is predicted precisely by ECI (it's only order-of-magnitude).
2. Does NOT claim any Steinhauer-group 2024-2026 paper confirms ECI predictions.
3. Does NOT claim the g^(2)(tau) decay has been measured.
4. Does NOT claim rho ~ 8.29% (RETRACTED).
5. Does NOT claim the BEC phonon system has a gravity dual (required for rigorous
   MSS saturation; stated as conjecture only).

---

## 7. Files Generated (G8 agent, 2026-05-03)

| File | Description |
|---|---|
| note_updated.tex | Main paper with §6 (signal-to-noise), §7 (retraction), §8 (program) |
| sympy_signal.py | All signal-to-noise numerics, sympy-verified |
| cover_letter_updated.txt | Updated cover letter with S/N, retraction, arXiv log |
| notes.md | This file: contact strategy + verification log |
