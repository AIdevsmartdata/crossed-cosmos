# F1 BEC Steinhauer — Research Notes
## Date: 2026-05-03

---

## 1. arXiv Search Results: Steinhauer-group 2024–2026

### Searches performed (via export.arxiv.org API, 2026-05-03)

**Query A:** `au:steinhauer AND (ti:hawking OR ti:sonic OR ti:analogue OR ti:black)`  
- Total results: 13
- 2024–2026 papers with Steinhauer as author: **2**
  - arXiv:2407.00448 (Keshet, Shemesh, Steinhauer 2024): "The ringdown-Hawking radiation connection in real and analogue black holes" — NOT about BEC saturation envelope
  - arXiv:2503.01029 (Steinhauer 2025): "Finding quasinormal modes directly from the boundary conditions in a Schwarzschild black hole" — pure GR, no BEC content
  - arXiv:2509.02676 (Steinhauer, Destounis, Brito 2025): "Overdamped quasibound states inside a Schwarzschild black hole" — pure GR, no BEC content

**Query B:** `ti:"analogue black hole" OR ti:"sonic black hole"`, 2024–2026  
- 16 results; none from Steinhauer group; none mention 'saturation envelope'
- Notable recent papers (not Steinhauer):
  - arXiv:2604.12800 (Solidoro, Völkel, Weinfurtner 2026): spectroscopy of analogue BHs using simulation-based inference
  - arXiv:2604.02075 (Chandran, Fischer 2026): volume-law entanglement negativity from Hawking radiation of analogue BHs
  - arXiv:2407.00448 (Keshet et al. 2024): ringdown-Hawking connection

**Query C:** `au:munoz_de_nova AND (ti:hawking OR ti:analogue)`  
- 7 results; most recent 2024 paper is arXiv:2406.10027 (resonant analogue configurations)
- arXiv:2507.10862 (Munoz de Nova, Sols 2025): "Hawking time crystals" — interesting but no saturation envelope

**Query D:** `ti:"BEC" AND (ti:"Hawking" OR ti:"sonic horizon")`, 2024–2026  
- 1 result: arXiv:2410.02700 (Anderson, Balbinot, Dudley, Fabbri 2024): BEC acoustic BH correlation functions

### VERDICT on Steinhauer-group 2025–2026 Saturation Envelope
**CONFIRMED NOT FOUND.** The C agent's flag is correct. There is no arXiv-accessible paper from the Steinhauer group (Technion, Tel Aviv) reporting a '2025–2026 saturation envelope' for BEC analogue Hawking radiation. The group's 2024–2026 output has pivoted to pure GR (quasinormal modes, overdamped states), with one ringdown-analogue connection paper.

---

## 2. ECI v6.0.10 "8.29% Saturation" — Retraction Candidate

**FLAGGED FOR v6.0.30 RETRACTION.**

The claim: *"ρ ≈ 8.29% at leading order, consistent across three Steinhauer datasets within 1–10% correction envelope"*

Evidence of unverifiability:
1. No Steinhauer paper uses the term "saturation envelope" on arXiv
2. No ECI paper defines what "ρ" measures in Steinhauer units
3. The three datasets (2014 NPhys, 2016 NPhys, 2019 Nature) do not report a dimensionless ratio ρ that could equal 8.29%
4. Searches across all analogue gravity literature find no such benchmark

**Action required:** Remove this claim from ECI v6.0.30. It should not appear in any submitted paper.

---

## 3. Citation Verification (arXiv-verified)

| Ref | arXiv ID | Title | Verified? |
|-----|----------|-------|-----------|
| Steinhauer 2016 | 1510.00621 | Observation of quantum Hawking radiation | YES |
| Steinhauer 2019 | 1809.00913 | Thermal Hawking radiation at T_H | YES |
| Steinhauer/Kolobov 2021 | 1910.09363 | Stationary spontaneous HR, time evolution | YES |
| Witten 2022 | 2112.12828 | Gravity and the Crossed Product | YES |
| Caputa-Magan-Patramanis-Tonni 2023 | 2306.14732 | Krylov complexity of modular Hamiltonian | YES |
| Hartnoll-Yang 2025 | 2502.02661 | Conformal Primon Gas (BKL) | YES |
| Delhom-Giacomelli 2025 | 2512.14209 | Analogue gravity with BECs (lecture notes) | YES |
| Vardian 2026 | 2602.02675 | Modular Krylov Complexity, area operator | YES |
| Chandran-Fischer 2026 | 2604.02075 | Volume-law entanglement negativity, analogue BHs | YES |
| Unruh 1981 | PRL 46, 1351 | Sonic black holes (no arXiv — pre-arXiv) | NOT ON ARXIV |
| Maldacena-Shenker-Stanford (MSS) 2016 | 1503.01409 | A bound on chaos | YES |

### MSS paper verification
arXiv:1503.01409 — "A bound on chaos" by Juan Maldacena, Stephen H. Shenker, Douglas Stanford.
VERIFIED via arXiv API 2026-05-03. (Note: author surname is Stanford, not "Stankovics" — the latter is a hallucination.)

---

## 4. Numerical Results (from sympy_check.py)

All computed at Steinhauer 2019 parameters (T_H = 0.35 ± 0.10 nK):

| Quantity | Value | Unit |
|----------|-------|------|
| Acoustic surface gravity κ | 2.879 × 10² | rad/s |
| Modular Lyapunov exponent λ_L^sonic | 2.879 × 10² | s⁻¹ |
| Krylov saturation time t_K = 1/λ_L | 3473 | μs |
| t_K (1-sigma range) | [2701, 4863] | μs |
| Characteristic frequency ν_char = k_B T_H / h | 7.3 | Hz |
| Period of characteristic mode | 137 | ms |

**Key observation:** The characteristic frequency (~7 Hz) is well below the typical phonon detection bandwidth in Steinhauer's setup (~1 kHz). The Krylov saturation timescale (~3.5 ms) is, however, well within the BEC coherence lifetime (typically 10–100 ms for rubidium condensates).

---

## 5. Krylov-Diameter Theorem Conjecture — Honest Assessment

The ECI Krylov-Diameter Theorem (Theorem 4 of krylov_diameter/) predicts:
```
dC_k/dt |_{horizon} = 1 / R_proper(η_c)
```

For the BEC analogue:
- R_proper → healing length ξ ~ 0.5 μm (UV cutoff scale)
- c_s / ξ ~ 10³ s⁻¹ (estimated λ_L)
- Corresponding T_H ~ 1.2 nK

Steinhauer measured T_H = 0.35 nK, a factor of **~3.5× lower**.

**Conclusion:** The naive KD conjecture (R_proper = ξ) misses by ~3.5× . This is expected: the actual surface gravity κ depends on the velocity field profile at the horizon, not just the healing length. A flow-profile-specific calculation is needed. The KD conjecture is order-of-magnitude correct but cannot serve as a precision test.

---

## 6. Algebraic Structure: BEC Observer Algebra

**Type III₁ → Type II_∞ crossed product:**

The BEC phonon algebra on the subsonic region (exterior of sonic black hole) is type III₁ in the thermodynamic/infinite-volume limit:
- The KMS state on phonons at T_H is a thermal state with no ground state
- The modular operator Δ_ψ is unbounded in both directions
- This is the analogue of the Rindler/black hole vacuum in QFT

The crossed product with modular flow R → type II_∞, following Witten 2112.12828.

**Key distinction from actual gravity:**
- The BEC has a UV cutoff at the healing length ξ (trans-Planckian analog is ABSENT)
- Phonon dispersion is relativistic (linear) only for k << 1/ξ
- For k ~ 1/ξ, the dispersion becomes quadratic (Bogoliubov): ω² = c_s²k² + (ħk²/2m)²
- This modifies the type structure: the true BEC algebra at finite ξ is type I (finite-dimensional modes)
- Only in the limit ξ → 0 (continuum limit) does the full type III₁ structure emerge

**Verch folium question:**
The BEC quasi-vacuum is NOT in the same folium as the conformal vacuum. The Bogoliubov vacuum (ground state of BdG Hamiltonian) is unitarily inequivalent to the Minkowski vacuum at the horizon scale. However, for long-wavelength phonons (k << 1/ξ), the two states share the same KMS structure at T_H, which is what matters for Krylov complexity.

---

## 7. Trans-Planckian Problem in BEC Analogue

**Jacobson 1991 (PRL 67, 1486):** In real black holes, Hawking radiation would require trans-Planckian frequencies near the horizon — a severe theoretical problem.

**BEC resolution:** The BEC naturally provides a UV cutoff at ξ. Phonons with k ~ 1/ξ have quadratic dispersion and do NOT produce Hawking radiation. This is the key advantage of the BEC analogue:
- The BEC evades the trans-Planckian problem by construction
- Hawking radiation comes only from modes with k << 1/ξ (linear dispersion regime)
- The Steinhauer 2019 measurement explicitly operates in this regime

**Implication for Krylov complexity:**
- The Krylov complexity of BEC phonons is INFRARED-dominated (k << 1/ξ)
- The UV divergence of the modular Hamiltonian is regulated by ξ
- This means t_K = 1/λ_L is genuinely measurable; it does not require UV completion

---

## 8. Gaps and Required Follow-up

1. **Steinhauer group direct contact:** No 2025–2026 saturation data on arXiv. Need to contact group at Technion (jef.steinhauer@physics.technion.ac.il) or check Nature Physics preprint server directly.

2. **g^(n)(t, t+τ) measurement protocol:** The ECI prediction (Gamma = λ_L^sonic in the phonon two-point function) requires measuring the DECAY RATE of the second-order coherence g^(2)(τ) as a function of τ. Steinhauer 2019 measures correlations but not the temporal decay rate in this specific form.

3. **MSS bound applicability:** The MSS bound λ_L ≤ 2πT applies to quantum many-body systems with a gravity dual. The BEC phonon system has no known gravity dual at finite ξ. The saturation λ_L = 2πT_H would require showing the BEC phonon system is maximally chaotic.

4. **Hartnoll-Yang BKL connection:** arXiv:2502.02661 discusses BKL dynamics near singularities, not sonic horizons. The claimed 'lift to BEC analogue near horizon' is not established and should not be cited without further analysis.

5. **Munoz de Nova 2025 (Hawking time crystals):** arXiv:2507.10862 proposes a Hawking time crystal via spontaneous Floquet state. This could provide a new experimental signature complementary to ECI predictions. Investigate.

---

## 9. What Would Actually Falsify ECI Here

ECI would be FALSIFIED by the BEC experiment if:
1. The phonon two-point function g^(2)(τ) decays with a rate Γ significantly different from λ_L^sonic = 2πk_B T_H / ħ (measured independently from thermality)
2. The Krylov complexity of phonon excitations shows SUB-linear growth at late times (contradicting modular Lyapunov saturation)
3. The type II_∞ crossed product structure predicts a specific entanglement scaling that contradicts the Chandran-Fischer 2026 volume-law result (arXiv:2604.02075)

ECI would have NON-TRIVIAL SUPPORT if:
- The temporal decay rate Γ of g^(2)(τ) matches λ_L^sonic independently of the thermality measurement
- This cross-check has NOT been performed by any group as of 2026-05-03
