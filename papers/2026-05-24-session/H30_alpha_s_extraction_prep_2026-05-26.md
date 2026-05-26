# H30 — α_s extraction from K41 prefactor in κ_EE(N) lattice SU(N) measurement

**Date** : 2026-05-26
**Status** : THEORY PREP (β-scan SU(6) running tonight)
**Prerequisite** : SU(6) β=10.8 (λ=20/3) and β=43.2 (λ=5/3) results

---

## 1. Setup

Empirical fit (N=5..8): **κ_EE(N) = 0.0193(4)·N^{5/3} + 0.421(10)** at λ_'t Hooft = g²N = 10/3.

K41 dimensional law: c_K41 ∝ ε^{2/3}, with ε = entanglement energy injection rate per unit boundary area. In Yang-Mills one-loop, ε ∝ g² (perturbative ε ~ g²·Λ⁴_UV by power counting, see App. A).

Two scenarios for the prefactor scaling:
- **S1 (linear in g²)** : c_K41(β) = c_univ · g²(β). Motivated by ε ∝ g² directly without cascade.
- **S2 (K41 strict, 2/3 power)** : c_K41(β) = c_univ · g^{4/3}(β) = c_univ · (g²)^{2/3}. Motivated by Kolmogorov ε^{2/3} dimensional law.
- **S3 (α_s scheme)** : c_K41 ∝ α_s = g²/(4π), equivalent up to constant to S1.

## 2. Numerical predictions at SU(6) β-scan points

At β=21.6, λ=10/3, g²=λ/N=10/18=0.5556. Measured c_K41 = 0.0193(4).

| β | λ | g² | g²/g²_ref | c_K41 (S1, ∝g²) | c_K41 (S2, ∝g^{4/3}) |
|---|---|----|-----------|-----------------|------------------------|
| 10.8 | 20/3 | 1.1111 | 2.0 | **0.0386** | **0.0306** |
| 21.6 | 10/3 | 0.5556 | 1.0 | 0.0193 (ref) | 0.0193 (ref) |
| 43.2 | 5/3 | 0.2778 | 0.5 | **0.00965** | **0.01217** |

**Discriminant ratio** (β=10.8 / β=43.2):
- S1: 4.00 (factor 4 in g²)
- S2: 2.52 (factor 2^{4/3})
- Statistical sensitivity needed : ±10% on each prefactor → ~1.5σ separation. Marginal ; need ≥3 N at each β to pin slope.

## 3. α_s extraction protocol

Once β-scan gives {c_K41(10.8), c_K41(21.6), c_K41(43.2)} :

(a) Fit c_K41(β) = A · (g²)^p, solve for p. p=1 → S1 ; p=2/3 → S2.
(b) Compute **g²_lattice(β)** via 1-loop : g²(β) = 2N/β (Wilson normalization). Convert to **α_s_MS̄** via β-shift (Lüscher-Weisz scheme conversion, factor ~1.1 at β~20).
(c) Set scale via Sommer parameter r_0 = 0.5 fm or direct string tension σ a²(β). For SU(6) β=21.6, a ≈ 0.10 fm (rough, needs MC measurement).
(d) Compare α_s(μ=1/a ≈ 2 GeV) extracted from c_K41 to PDG world average α_s(2 GeV) ≈ 0.30 (running from α_s(M_Z)=0.118).

**Sanity check** : at β=21.6, g²=0.556, α_s = 0.0442. If c_K41 = c_univ · α_s, then c_univ = 0.0193/0.0442 = **0.437**. This is O(1), dimensionally sensible. Note: 0.437 ≈ κ_∞ ≈ ζ(3)/√π = 0.6782 ? Off by factor ~1.5. Coincidence or signature ? **To test once β-scan lands**.

## 4. Systematic errors

1. **Lattice spacing a(β)** : λ fixed → a(β) varies (logarithmic, b_0=22 for SU(6)). At β=10.8, a ~ 2× larger (deep strong) → finite-a effects ~10%. At β=43.2, a ~ 0.5× (weak) → finite-V more dangerous.
2. **Finite-V** : L=4..10 at β=43.2 may not contain confining scale. Mitigation : extract κ_EE from N=5..8 trend at fixed L=10, keep L²/a² ≥ ξ²_glueball.
3. **Renormalization scheme** : Wilson gauge action ≠ MS̄. Conversion factor C_W→MS̄ = exp(-Λ_W/Λ_MS̄·...) ≈ 28 (SU(6) extrapolated from SU(3) ratio Λ_MS̄/Λ_Wilson = 28.81, Hasenfratz-Hasenfratz 1980).
4. **Higher-loop in b_0** : 2-loop b_1 = 102 N²/3 (SU(N)) shifts g²(μ) extraction by ~5% at β~20.

## 5. Bridge with Berges-Boguslavski-Schlichting-Venugopalan 2013

[arXiv:1303.5650] VERIFIED 2026-05-26. "Turbulent thermalization process in heavy-ion collisions at ultrarelativistic energies", J. Berges, K. Boguslavski, S. Schlichting, R. Venugopalan, Phys. Rev. D 89, 074011 (2014).

They find self-similar wave-turbulence cascade in real-time classical Yang-Mills with K41-like 5/3 exponent. Their prefactor c_BBSV depends on initial occupancy f_0 in over-occupied regime (f_0 ~ 1/α_s). Schematically c_BBSV ∝ α_s·f_0^{1/2} (from kinetic theory, Kurkela-Moore 1107.5050 to verify).

**Comparison** : our **static vacuum** measurement at λ=10/3 should match BBSV's **f_0 = 1/2** equivalent (vacuum fluctuations populate modes at f ~ 1 per loop in a²·g² units). Quantitative cross-check requires translating BBSV's IR scale Q_s to our lattice spacing a. Estimate: Q_s a ~ √λ → Q_s ~ √(10/3)/a ≈ 1.83/a, so at a=0.1 fm, Q_s ≈ 3.6 GeV. Their cascade window 0.1 Q_s < p < Q_s maps to our 0.5 GeV < 1/L < 4 GeV — overlapping with L=4..10 lattice modes.

## 6. Verified arXiv references

- [arXiv:1303.5650] **VERIFIED**. Berges, Boguslavski, Schlichting, Venugopalan, 2013/2014. K41 self-similar Yang-Mills thermalization.
- [arXiv:0802.4247] **VERIFIED**. Buividovich, Polikarpov, 2008. Numerical SU(2) lattice EE — methodological baseline for our κ_EE measurement.
- [arXiv:1107.5050] **TO VERIFY** Kurkela-Moore kinetic theory thermalization. Cited indirectly via BBSV.

## 7. Action items when β-scan lands tonight

1. Fit c_K41(β) at 3 points → extract p (linear vs 2/3).
2. If p ≈ 1 (S1) : ε ∝ g² directly, α_s extracted via c_K41 = c_univ · α_s with c_univ ~ 0.44.
3. If p ≈ 2/3 (S2) : K41 cascade confirmed, ε ∝ g² but enters via ε^{2/3} → cleaner connection to Kolmogorov.
4. **Adversarial null** : c_K41(β) independent of β → static EE prefactor is g-independent, K41 interpretation falsified. Memory : flag and document.
5. Cross-check with BBSV f_0 scaling : translate vacuum occupancy to BBSV regime.

---
**Decision tree pending β-scan** : 3 outcomes (S1 / S2 / null) → 3 sub-papers (linear, K41-strict, falsified-K41). All publishable.
