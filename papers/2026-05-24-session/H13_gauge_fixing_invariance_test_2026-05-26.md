# H13 — Gauge-fixing invariance of the SU(N) lattice EE crossover at N=4-5

**Date**: 2026-05-26
**Hypothesis tested**: The N=4-5 crossover in κ_EE measured via BP2008b is an artifact of the gauge-fixing/Hilbert-space prescription, not a physical ground-state feature.

---

## 1. Theoretical setup — gauge-invariance of EE on a lattice

In a non-abelian lattice gauge theory the physical Hilbert space **H_phys** is the subspace of the link Hilbert space **H_link** = ⊗_ℓ L²(G) satisfying Gauss's law at every site. **H_phys does not factorize** across a spatial bipartition (A, A^c), because gauge transformations on the entangling surface ∂A are correlated across both regions. Consequently, the reduced density matrix ρ_A — and the Renyi/von-Neumann EE — are **not uniquely defined**; one must specify an *embedding* of H_phys into a factorizable space.

Three inequivalent prescriptions exist:

1. **Extended Hilbert space (eHS)** — Buividovich-Polikarpov, Donnelly, Aoki et al.: embed H_phys ↪ H_link, define ρ_A from the unconstrained link algebra. This is what **BP2008b uses**. Yields a positive "boundary symmetry term" log(dim G)·|∂A|/a² that is N-dependent.

2. **Algebraic / electric center (CHR)** — Casini-Huerta-Rosabal 1312.1183: split the gauge-invariant operator algebra A by its center (electric flux through ∂A). EE = classical Shannon entropy of flux sectors + sum of weighted entropies inside each sector. **No log(dim G) boundary term**.

3. **Magnetic center**: dual choice; gives yet another value.

The three differ by a **boundary term** ∝ |∂A|; their universal pieces (relative entropy, mutual information, leading area-law coefficient up to a known shift) agree in the continuum limit (CHR Sec. 5; Soni-Trivedi Sec. 4).

---

## 2. Verified references

| arXiv ID | Author / Title | Status |
|---|---|---|
| **1109.0036** | Donnelly, *Decomposition of EE in lattice gauge theory* (2011) | VERIFIED — replaces user-cited 0802.0246 (= Thill 2008, unrelated, **FLAGGED FAB**) |
| **1412.1895** | Donnelly-Wall, *EE of electromagnetic edge modes* (PRL 2015) | VERIFIED — replaces user-cited 1212.1244 (= Grønbech-Jensen-Farago Verlet/Langevin, **FLAGGED FAB**) |
| **1506.05792** | Donnelly-Wall, *Geometric entropy and edge modes of EM field* (2015) | VERIFIED (alternate) |
| **1312.1183** | Casini-Huerta-Rosabal, *Remarks on EE for gauge fields* (PRD 2014) | VERIFIED |
| **1502.04267** | Aoki-Iritani-Nozaki-Numasawa-Shiba-Tasaki, *On the definition of EE in lattice gauge theories* (2015) | VERIFIED |
| **1510.07455** | Soni-Trivedi, *Aspects of EE for gauge theories* (JHEP 2016) | VERIFIED |
| **1501.02593** | Ghosh-Soni-Trivedi, *On the EE for gauge theories* (JHEP 2015) | VERIFIED |
| **0802.4247** | Buividovich-Polikarpov, *Numerical study of EE in SU(2) lattice GT* (2008) | VERIFIED |

**Anti-fab flag**: two user-supplied IDs (0802.0246, 1212.1244) point to unrelated papers and have been **replaced** with the correct identifiers above.

---

## 3. Does the crossover depend on the prescription?

**Key observation from the literature** (CHR §3, Aoki et al. §IV, Soni-Trivedi §2.3):

The **difference** between eHS and algebraic EE for region A is

  ΔS_eHS-alg(A) = log(dim G) · N_∂ − ⟨log(dim R)⟩

where N_∂ is the number of links crossing ∂A and R runs over irreps weighted by the electric-flux distribution. For G = SU(N), dim G = N²−1, so the eHS prescription adds an **N²-scaling** boundary term that the algebraic prescription does not.

**Consequence for κ_EE(N)** = leading area-law coefficient:

- In **eHS (BP2008b)**: κ_EE includes the full electric-flux boundary contribution. Its N-dependence mixes (i) physical bulk vacuum structure with (ii) a kinematic log(N²−1)/a² piece.
- In **algebraic**: the kinematic piece is **subtracted**; one isolates the physical bulk entropy.

The **N=4-5 crossover** (memory entry: dilute→dense regime, b_0 = 11N/(48π²)) is driven by the running 't Hooft coupling λ = g²N, i.e., by a **bulk** effect (UV/IR filter scale L_c(N) = exp(24π²/(11Nλ))). The kinematic eHS boundary term is **smooth in N** (proportional to log(N²−1)) and **cannot produce a crossover**.

Therefore: **H13 is most likely FALSE** at first order. The boundary term shifts κ_EE by an N-monotonic, smooth amount; the non-monotonic crossover behavior survives the subtraction.

**However**, a subtle caveat: BP2008b's α-integration replica trick mixes bulk and boundary contributions non-trivially at finite β. Two β-regimes (perturbative N≤4 vs confining √N for N≥5, per the memory) could in principle interact differently with the boundary kinematics. A direct test is mandatory.

---

## 4. Numerical protocol — algebraic EE in JAX

**Code changes** (extending current BP2008b JAX pipeline):

1. **Replace** the deformed-boundary partition-function ratio with explicit **electric-flux sector decomposition** on ∂A: enumerate irreps R of SU(N) with Casimir ≤ Λ_cutoff, weight each by partition function in fixed-flux sector.
2. **Algebraic EE** = − Σ_R p_R log p_R + Σ_R p_R · S_bulk(R), where p_R is the boundary-flux distribution.
3. Run at **β** in physical regime, **L = 6,8,10**, **N = 3, 4, 5, 6** (skip SU(2): degenerate, skip SU(7): cost).

**Cost estimate**:
- SU(N) irrep enumeration up to dim ≤ 50: ~O(N²) sectors.
- Each sector requires one HMC ensemble with constrained flux: ~5× cost of standard run.
- Total ~5×4 = **20× current BP2008b cost** for the comparison set.
- On Vast.AI ssh8 baseline ~3h per (N, L) → **~24h GPU** for the cross-prescription comparison.

**Decision tree**:
- If κ_EE^alg(N) shows crossover at **same N≈4-5** → physical, H13 REJECTED.
- If crossover shifts to **different N** → gauge-fixing dependent, H13 partially supported.
- If crossover **disappears** in algebraic → BP2008b artifact, H13 STRONGLY SUPPORTED.

---

## 5. Interpretation impact

- **If gauge-invariant** (likely): the crossover is a genuine phase-boundary signature in N-space, supporting the two-regime picture (perturbative vs √N confining). H10, H11 retain physical meaning.
- **If gauge-fixing dependent**: κ_EE(N) loses status as a universal observable; m_H = κ(SU(2))·v and y_top² = κ(SU(8))/κ_∞ would be **convention-dependent identities** rather than fundamental relations. P(ECI) would drop ~15-20pp.

---

## 6. Preliminary verdict

**Crossover is LIKELY GAUGE-INVARIANT** (~70-80% probability), because:
1. The boundary term log(N²−1) is **smooth and monotonic** in N — incompatible with a sharp crossover at N=4-5.
2. The crossover scale L_c(N) derives from the bulk **β-function**, which is gauge-invariant by Slavnov-Taylor.
3. CHR §5: leading area-law coefficient agrees across prescriptions up to a **known finite shift** in the continuum limit.

**However**, the explicit algebraic computation is **not optional**: at finite lattice spacing and finite β, the eHS-algebraic gap is O(1) per boundary plaquette and could in principle hide a sub-leading crossover artifact. The ~24h GPU test is the cleanest way to retire the hypothesis.

**Recommendation**: schedule algebraic-EE run **N=3,4,5,6 × L=6,8** as next milestone after current SU(7) THERM5000 completes. Cost-benefit favorable (P=20-30% of surprise outcome that would invalidate κ_EE-based identities).

---

**End H13 analysis — references verified, anti-fab clean, 2 user IDs FLAGGED and corrected.**
