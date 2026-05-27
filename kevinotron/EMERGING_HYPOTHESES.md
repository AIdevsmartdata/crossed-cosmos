# Kevinotron — Emerging Hypotheses Map
# Kévin Rémondière (ORCID 0009-0008-2443-7166)
# 2026-05-28 (from session 2026-05-27)

## THE FORMULA (established, R²=0.997, 7 groups)
```
S₂/A = c·(β − |Φ⁺|) − log(β − 1 − |Φ⁺|) − C₂
```
Three terms, three physics:
- c·(β − |Φ⁺|): bare coupling minus ghost modes (Weyl integration formula)
- −log(β − 1 − |Φ⁺|): FP determinant (spectral ζ'(0))
- −C₂: one-loop self-energy (Killing form curvature)

## HYPOTHESIS MAP — 4 categories

### A. FORMULA EXTENSIONS (derive more from the same formula)

**A1. Mass gap from FP spectrum**
- log det(M_FP) = S₂/A (our formula)
- λ_min(M_FP) → m(0⁺⁺) glueball mass
- Relation: m²a² ~ λ_min ~ (β − 1 − |Φ⁺|)^{-1} × exp(−something)
- TEST: extract λ_min from JAX GPU diag → compare m(0⁺⁺)/√σ with literature
- Current: λ_min(G₂, cov.Lap) = 1.055 → m/√σ ≈ 4.5
- Need: same for SU(3) → compare with 3.55 (Morningstar-Peardon)
- Status: TESTABLE NOW (configs dumped, GPU ready)

**A2. Deconfinement temperature from β_crit**
- β_crit = 1 + |Φ⁺| is where log diverges → phase transition
- Hypothesis: T_c/√σ ∝ 1/β_crit or function thereof
- Data: SU(2) β_crit=2, T_c/√σ≈0.69; SU(3) β_crit=4, T_c/√σ≈0.63; G₂ β_crit=7, T_c/√σ≈0.86
- TEST: plot T_c/√σ vs β_crit for known groups
- Status: PURE CALCULATION on literature data

**A3. Continuum limit structure**
- Subtracted EE: S₂_phys = S₂/A − c·(β−|Φ⁺|) = −log(β−1−|Φ⁺|) − C₂
- This should have a continuum limit (no UV divergence)
- For SU(N): S₂_phys = −log(β−1−N(N−1)/2) − N
- TEST: measure at multiple β for SU(3) and check S₂_phys converges
- Status: NEEDS 4 RUNS at β=5.8, 6.0, 6.2, 6.4

**A4. Large-N limit**
- At fixed 't Hooft λ = β/N²: S₂/A ~ c·(λ−1/2)·N² + O(N)
- N² scaling = planar limit of entanglement
- TEST: SU(5) at β=25 (λ=1) vs SU(3) at β=9 (λ=1)
- Status: SU(5) IMPLEMENTED, need matched λ run

### B. CROSS-SECTOR CONNECTIONS (Kevinotron ↔ ECI ↔ Big Table)

**B1. κ_EE from the formula**
- κ_EE(N) = S₂/A at matched σa² normalized by v
- m_H = κ(SU(2))·v was our TIER 1 result (0.016%)
- NEW: κ(N) = [c·(β_N−|Φ⁺_N|) − log(β_N−1−|Φ⁺_N|) − N] / normalization
- This gives κ as a function of Lie algebra data + a single β matching
- TEST: does the formula reproduce κ(SU(2))=0.508, κ(SU(3))=0.603?
- Status: PURE CALCULATION

**B2. Higgs mass from root counting**
- m_H = κ(SU(2))·v = 0.508 × 246.22 = 125.08 GeV
- |Φ⁺(SU(2))| = 1 (the simplest root system)
- Hypothesis: m_H encodes the fact that SU(2)_L has exactly ONE positive root
- The "1" in β−|Φ⁺|=β−1 for SU(2) is the Higgs counting
- TEST: derive κ(SU(2)) = (c·(β₀−1)−log(β₀−2)−2)/normalization analytically
- Status: SPECULATIVE but calculable

**B3. Dark matter mass from G₂ formula**
- G₂ dark glueball mass ∝ λ_min(FP, G₂) / √σ_dark
- Our GPU measurement: m/√σ ≈ 4.5 for G₂
- If σ_dark ~ σ_QCD × (Λ_dark/Λ_QCD)²: m_dark ~ 4.5 × √σ_dark
- For Λ_dark ~ 1 GeV: m_dark ~ 2-5 GeV (self-consistent with DM)
- TEST: refine with FP adjoint operator on GPU
- Status: SPECULATIVE, needs FP adjoint (7168×7168)

### C. SPECTRAL GEOMETRY (GPU-driven discovery)

**C1. d_s spectral dimension classification**
- Measured: d_s(G₂, cov.Lap, mid-t) = 5.06
- Predicted for FP adjoint: d_s < 4 (ghost sector is "lower-dimensional")
- Hypothesis: d_s(FP, G) depends on Dynkin type, not just dim
- TEST: measure d_s(FP) for SU(2), SU(3), G₂ on GPU
- Need: Ad(U) construction for each group (~50 lines JAX)
- Status: TESTABLE THIS WEEK

**C2. Eigenvalue density → root system geometry**
- The eigenvalue density ρ(λ) of the covariant Laplacian encodes the gauge group
- For free Laplacian: ρ(λ) = universal (lattice artifact)
- For interacting: ρ(λ) depends on the group → can we read off |Φ⁺| from ρ?
- TEST: compare ρ(λ) between SU(3) and G₂ at same σa²
- Status: CONFIGS READY, pure GPU analysis

**C3. Entanglement spectrum → topological order**
- The full spectrum of ρ_A (not just S₂ = −log Tr ρ²) encodes topological data
- For Z(G)≠{1}: the entanglement spectrum should show |Z|-fold degeneracies
- For G₂ (Z={1}): no degeneracies → simpler spectrum
- TEST: extract entanglement spectrum from replica trick (needs Renyi-n for n>2)
- Status: NEEDS NEW CODE (Renyi-n for general n)

### D. HOLOGRAPHIC AND GRAVITATIONAL (speculative)

**D1. Hawking-Page without black hole**
- β_crit = 1 + |Φ⁺| is a phase transition in the bulk dual
- For G₂: β_crit = 7, far from the simulation window
- The log divergence at β_crit is a condensation of center vortices (for SU(N))
- For G₂ (no center): the transition is driven by MONOPOLES, not vortices
- TEST: measure Polyakov loop susceptibility near β_crit for G₂
- Status: TESTABLE with Kevinotron (add Polyakov loop observable)

**D2. G_N hierarchy from the formula**
- G_N(EW)/G_N(QCD) = S₂(SU(3))/S₂(SU(2)) = 14.12/7.44 = 1.90
- The weak force contributes ~2× more to gravity per unit area than QCD
- Is this related to the hierarchy v/Λ_QCD ~ 10³?
- TEST: compute G_N ratios at matched physical scale (not bare β)
- Status: HIGHLY SPECULATIVE, needs matched σa² for all sectors

**D3. Entropy ↔ gravity coupling for the SM**
- If all SM gauge groups contribute additively to G_N:
- 1/G_N ∝ S₂(SU(3)) + S₂(SU(2)) + S₂(U(1))_EM
- U(1) is abelian → |Φ⁺| = 0, C₂ = 0 → S₂(U(1)) = c·β_EM
- This gives a PREDICTION for G_N from gauge group data alone
- TEST: compute and compare with known G_N = 6.674×10⁻¹¹
- Status: HIGHLY SPECULATIVE, many assumptions

## CONNECTION TO DECODER GRAPH

The Decoder Graph v3 (37 nodes, 42 edges) maps ECI anchors:
- Node "κ_EE" connects to: m_H (via κ·v), Rabenstein (via (N²-1)(1-κ)), Big Table
- Node "G₂ dark" connects to: DM density, glueball mass, BBN constraints
- Node "Donnelly-Wall" connects to: center Z(G), superselection, edge modes

NEW CONNECTIONS from Kevinotron:
- "PySR formula" → Faddeev-Popov determinant → Mass Gap (Clay Millennium)
- "|Φ⁺| counting" → Weyl integration → Langlands program (root systems)
- "β_crit" → deconfinement T_c → finite-T phase transitions
- "d_s(GPU)" → spectral geometry → quantum gravity models
- "G_N holographic" → Ryu-Takayanagi → AdS/CFT for pure gauge

## PRIORITY ACTIONS (next session)

1. A1 + C1: FP adjoint d_s on GPU for SU(2,3) + G₂ (30 min each)
2. A2: T_c vs β_crit plot (10 min calculation)
3. B1: κ_EE from formula (10 min calculation)
4. A3: SU(3) β-scan for continuum check (4 runs, ~2h)
5. H5 from HYPOTHESES_TO_TEST.md (FP adjoint spectrum)
