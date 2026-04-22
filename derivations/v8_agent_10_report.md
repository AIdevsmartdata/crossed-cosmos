# V8-Agent-10: Bures Distance ↔ Brown-Susskind Complexity

**Verdict: NO-SIMPLE-RELATION**

## Setup

- 3+3 qubit XXZ system (DIM=64), β=1 thermal state ρ_β
- Perturbed Hamiltonian H' = H_XXZ + λ·V_boundary (λ=0.3, boundary XXZ coupling between R and R' edge sites)
- ρ_R(τ) = Tr_{R'}[exp(-iH'τ) ρ_β exp(+iH'τ)]
- d_B(ρ_R(0), ρ_R(τ)): Bures distance via scipy.linalg.sqrtm
- C_BS(τ): Nielsen purity-proxy complexity = 1/Tr(ρ_R(τ)²)

## Results

| Quantity | Value |
|---|---|
| β (power-law exponent) | 0.141 ± 0.069 |
| R² (power-law fit) | 0.071 |
| R² (linear β=1) | −0.954 |

## Analysis

The Bures distance d_B and the complexity change ΔC_BS oscillate incoherently
as functions of τ. Purity (C_BS proxy) is invariant under the *full* unitary
evolution — it only changes due to the partial trace, which creates mixing/
demixing oscillations that are out of phase with d_B. The power-law fit
R²=0.07 is not statistically significant; the linear fit R²<0 is actively
wrong. β=0.14 is far from 1 and has large uncertainty.

## Interpretation

The Bures metric is a canonical distance on density matrices (sensitive to
eigenvalue changes AND eigenvector rotations), while C_BS ≈ 1/purity tracks
only eigenvalue mixing. Under modular flow of a perturbed Hamiltonian, these
two quantities evolve along different geometric directions in state space. The
analogy Bures-geodesic ≅ C_k (to leading order, linearly) is **not supported**
in this 3+3 qubit XXZ model.

**VERDICT: NO-SIMPLE-RELATION**
