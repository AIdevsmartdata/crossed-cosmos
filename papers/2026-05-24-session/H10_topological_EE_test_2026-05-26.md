# H10 — Topological entanglement entropy γ for SU(N) lattice (dense regime test)

**Date** : 2026-05-26
**Context** : κ_EE crossover N=4-5 in 4D pure YM. Dense regime (N≥5) hypothesized as **topologically ordered confined string-net**.
**Hypothesis H10** : γ(N) = 0 for N≤4, γ(N) > 0 for N≥5 (Kitaev-Preskill universal additive constant).

---

## 1. Theoretical γ predictions (heuristic flux-tube string-net)

Topological EE definition (Kitaev-Preskill 2006) for 2+1D :
S(disc) = α·L − γ + O(1/L), γ = ln D where D = √Σ_i d_i² (total quantum dimension).

**For 4D YM** : γ extracted from S(slab thickness L) once area subtracted (Donnelly 2014 review framework; Aoki et al. 2015 replica formula extension).

Heuristic for SU(N) confined phase (flux tube condensate, N distinct k-strings labeled by N-ality):
- D ~ √(N quantum dimensions for k=0..N−1 reps, each d_k = 1 for centre Z_N anyons)
- D = √N → **γ = ½ ln N** (centre-symmetric topological order)

| N | (1−1/N²)·ζ(3)/√π | 0.518√N − 0.458 | γ predicted (½ ln N) |
|---|------------------|-----------------|----------------------|
| 2 | 0.509 (dilute)   | 0.275           | **0** (Abelian-like) |
| 3 | 0.603            | 0.439           | **0** (still dilute glue) |
| 4 | 0.636            | 0.578           | **0** (boundary)      |
| 5 | (0.651, dilute formula) | 0.700    | **0.805**            |
| 6 | (0.660)          | 0.811           | **0.896**            |
| 7 | (0.665)          | 0.913           | **0.973**            |
| 8 | (0.670)          | 1.007           | **1.040**            |

Caveat : SU(N) pure 4D YM has no exact Z_N 1-form symmetry breaking in confined phase (Wilson centre-symmetric); 4D topological order is more subtle than 2+1D Kitaev model. γ = ½ ln N is a string-condensate heuristic, NOT a derivation.

Alternative model — string-net with k-string tensions σ_k ≠ σ_1 (Casimir scaling):
- For SU(N), N distinct k-string sectors → D_eff = √N still, γ = ½ ln N
- Sine-law scaling σ_k = σ_1·sin(πk/N)/sin(π/N) preserves this count.

## 2. Literature verification (all arXiv IDs checked via WebFetch)

| Claimed ID | Status | Actual paper |
|---|---|---|
| **cond-mat/0510092** | **FAIL** — Jizba-Arimitsu, "Information theory for q-nonextensive statistics" (NOT Kitaev-Preskill) | n/a |
| **hep-th/0510092** | **OK** | Kitaev-Preskill "Topological entanglement entropy", PRL 96 (2006) |
| **cond-mat/0510613** | **OK** | Levin-Wen "Detecting topological order in a ground state wave function" |
| **arXiv:1412.1895** | **PARTIAL** — Donnelly-Wall "Entanglement entropy of electromagnetic edge modes" — *continuum* Maxwell, NOT lattice gauge theory directly | Use for edge-mode formalism only |
| **arXiv:1502.04267** | **OK** | Aoki, Iritani, Nozaki, Numasawa, Shiba, Tasaki "On the definition of entanglement entropy in lattice gauge theories" (extended Hilbert space, abelian+non-abelian, Z_N topological) |
| **arXiv:0905.2562** | **OK** | Casini-Huerta "Entanglement entropy in free quantum field theory" (review) |
| **arXiv:0802.4247** | **OK** | Buividovich-Polikarpov "Numerical study of entanglement entropy in SU(2) lattice gauge theory" |

**ANTI-FAB FLAG** : The user's input cited `cond-mat/0510092` for Kitaev-Preskill; correct ID is **hep-th/0510092**. The cond-mat number maps to an unrelated q-statistics paper. Also note: paper title for Aoki et al. given in user input ("Aoki-Iritani-Lin-Matsuda") differs from actual author list ("Aoki, Iritani, Nozaki, Numasawa, Shiba, Tasaki") — propagated mis-attribution.

**No prior measurement of γ found for SU(N≥3) 4D pure YM at lattice.** Buividovich-Polikarpov 2008 measured S(L) area-law for SU(2) only (no γ extraction). Donnelly 2014 lattice review (arXiv:1406.7304, separate from 1412.1895) discusses gauge edge modes contributing finite log term that mimics γ — this is a **systematic to subtract** before claiming topological γ.

## 3. JAX lattice protocol (modify BP2008b FAST V3)

Base file : `/root/cc-private/papers/2026-05-24-session/scripts/jax_su2_EE_BP2008b_FAST_2026-05-25.py`
SU(N) ports already exist for N=3,4,5 (`jax_su3/4/5_EE_BP2008b_2026-05-25.py`).

**Kitaev-Preskill tri-partition (3+1D analog with 3D spatial slice)** :
On L³ spatial slice, define 4 cubic regions inside a large region R :
- A : cube of side r at position (0,0,0)
- B : cube at (r,0,0)
- C : cube at (0,r,0)
- AB, BC, AC, ABC : unions

Then γ = S_A + S_B + S_C − S_AB − S_BC − S_AC + S_ABC.

For each subregion, run independent BP2008b α-integration measurement on the **same gauge configuration ensemble** (correlated sampling → variance reduction).

**Concrete changes to FAST V3 script** :
1. Replace single `A_spatial_mask` with **7 masks** {A, B, C, AB, BC, AC, ABC}.
2. Loop measure α-integration for each mask, reuse thermalized configs (only α-deformation depends on mask) → cost = 7× single measurement.
3. Subtract area-law contribution from each S using known κ(N) (already measured this session for N=2,3,4,5,6).
4. Combine via KP linear combination → γ_KP.

**Simpler alternative — Levin-Wen geometry (cond-mat/0510613)** :
4 partitions on annulus, 2 linear combinations cancel area, perimeter, corner terms separately. Stronger signal but more involved boundary geometry on cubic lattice.

**Cost estimate** : 1 KP measurement at L=8, N=5, β=2.4 ≈ 7 × (single BP2008b run) ≈ 7 × 30 min = 3.5 h per (N, L). For N ∈ {2,3,5,6,8}, L ∈ {6, 8} → ~35 h total on 1 GPU. Feasible.

**Edge-mode subtraction** : following Donnelly 2014 (lattice review), the extended-Hilbert-space EE contains ln(dim G) per boundary plaquette = ln(N²−1) per site × |∂A|. This **is part of the area term**, so it cancels in KP combination. But there is a **log-corner term** (Casini-Huerta corner anomaly) that does NOT cancel in tri-partition geometry — needs explicit numerical check via Levin-Wen geometry which kills it.

## 4. Predictions

| Quantity | H10 prediction | If γ=0 ∀N | If γ≠0 ∀N | Discriminating |
|---|---|---|---|---|
| γ(SU(2)) | 0 | 0 | ≠0 | weakly |
| γ(SU(3)) | 0 | 0 | ≠0 | weakly |
| γ(SU(4)) | 0 (boundary) | 0 | ≠0 | crucial |
| γ(SU(5)) | 0.81 | 0 | ≠0 | **crucial** |
| γ(SU(6)) | 0.90 | 0 | ≠0 | **crucial** |
| γ(SU(8)) | 1.04 | 0 | ≠0 | **crucial** |

**Discriminant** : ratio γ(6)/γ(5) = 0.90/0.81 = 1.11 in H10 (½ ln N law).
If measured ratio matches 1.11 ± 0.05 → strong evidence for centre-symmetric string-net topological order.

## 5. Verdict prelim

**P(H10 strict ½ ln N) = 20-30%** — speculative; no prior literature finds γ ≠ 0 in 4D pure YM.

**P(H10 weak — γ jumps from 0 to nonzero somewhere in N=4-6)** = 40-55% — physically motivated by the empirical κ crossover and confined string condensate intuition.

**Key risk** : the gauge edge-mode contribution can fake a γ if subtraction is imperfect. Aoki et al. 2015 extended-Hilbert-space framework provides the clean definition needed.

**Recommended next step** : execute KP protocol on SU(2) first as **null calibration** (must yield γ=0 within errors) before measuring SU(5,6,8). Budget : ~10 h GPU SU(2) calibration + ~25 h SU(5,6) measurements. Cluster 733 has capacity.

**Falsifiability** : a clean γ(2)=γ(3)=γ(4)=0 vs γ(5,6,8) > 0 at >3σ would be **discovery-grade evidence** for a deconfined-to-topologically-ordered transition in N. Conversely, γ=0 for all N falsifies H10 and supports "dense regime = renormalized non-topological string condensate".

**Status** : H10 testable, theoretically motivated by crossover, protocol concrete, falsification clean. Not currently in any published lattice study.
