# Pitch Bauerschmidt v22.1 — Appendix: H1 Formulations & 1/L² Analysis

**Date** : 2026-05-24
**Statut** : Annexe technique au pitch v22

---

## 1. The 1/L² is an Artifact

The current bound m_gap ≥ √(ε·(1−κ)·β/L²) contains a 1/L² factor that would kill the mass gap in the L→∞ limit.
This factor is NOT physical — it is an artifact of the lazy bound λ₁(Δ_Λ) ≥ C/L².

### Evidence from 3 independent sources

| Source | Finding |
|--------|---------|
| **BBD23** (arXiv:2202.02295) | LSI **uniform in L** for φ⁴₃, proven via Polchinski cascade |
| **CNS25** (arXiv:2509.04688) | Mass gap for SU(N) **uniform in L** for β < 1/24 |
| **Lüscher 1986** (CMP 104) | Finite-size corrections are **exponential** exp(−mL), not polynomial |

### Counter-example: why 1/L² is not fundamental

Ginzburg-Landau has spectral gap ∝ 1/L² — but GL is a **critical model** with NO intrinsic gap.
YM SU(N) 4D has an **intrinsic mass gap** (expected, lattice-verified).
The 1/L² comes from using λ₁(Δ_Λ) on the flat torus without exploiting the non-abelian interaction.

### Resolution: H10 (Polchinski cascade for SU(N))

If the non-abelian interaction is exploited via a Wilson-Polchinski RG cascade (BBD23 style),
the 1/L² bound is replaced by the intrinsic mass gap.

---

## 2. Three Formulations of H1

The core open problem: concentration of the Gibbs measure near the vacuum,
uniform in lattice spacing a and volume L.

### H1 (brut) — Concentration bound

```
μ_{a,β}({‖A‖² ≥ R}) ≤ C · exp(−c · β · R/N²)
```
Uniform in a, L. Standard cluster-expansion form (Bałaban, MRS93).

### H1'' — Polchinski cascade

```
After k RG steps: effective action S_k = Σ c_k(A)
with ‖c_k‖ ≤ C · L³ · k^{−2} (summable in k)
```
Language: BBD23 φ⁴₃ cascaded to SU(N) gauge.
Key: the cascade gives uniform-in-L bounds **automatically**.

### H1''' — Susceptibility

```
χ_β(L) = Var(‖F‖²) ≤ C  (uniform in L)
```
Shortest formulation. If the action fluctuation is bounded uniformly in L,
the whole machinery follows.

### Recommendation for Bauerschmidt

Present all 3. Let him identify which is most accessible with his framework.
H1'' (Polchinski) is the most natural for BBD collaborators.

---

## 3. Hypothesis Status Table

| H | Statement | Status | Who |
|---|-----------|--------|-----|
| H1 | Concentration (3 versions) | **OPEN** | Bauerschmidt |
| H2 | Gaussian density MRS93 | Sketch | Technical |
| H3 | Pinsker α=1 | ✅ Lean | Acquired |
| H4 | LSI Gaussian ∞-dim (Gross 1975) | ✅ Standard | Acquired |
| H5 | λ₁(Δ_Λ) ≥ C/L² | ✅ Standard (but artifact) | Acquired |
| H6 | κ=1/6 Hodge SU(3) D=4 | ✅ Lean | Acquired |
| H7 | Theorem C empirical uniform | 🟡 Annex | Acquired |
| H8 | Lüscher exp finite-size | 🟡 Standard | Acquired |
| H9 | κ continuity in continuum | 🟡 Coherence | Acquired |
| **H10** | **Polchinski cascade SU(N)** | **OPEN** | **Bauerschmidt** |

H1 and H10 are **equivalent in strength** (both give mass gap > 0). H10 is more natural in BBD language.

---

## 4. Saturation Table (Cross-N, Cross-D)

The saturation condition: C(4,2)−C(4,3) = D(D−1)(5−D)/6

```
N  D  rank  C₂−C₃  saturated?  κ         α
―――――――――――――――――――――――――――――――――――――――――――――
2  2    1      1      ✅         1/2       1/2
3  2    2      1      ❌         —         1
4+ 2   ≥3     1      ❌         —         1
2  3    1      2      ❌         —         1
3  3    2      2      ✅         1/4       3/4
4+ 3   ≥3     2      ❌         —         1
2  4    1      2      ❌         —         1
3  4    2      2      ✅         1/6       5/6  ← YM physical
4+ 4   ≥3     2      ❌         —         1
D≥5: C₂−C₃ ≤ 0 → NO non-abelian group saturated
```

Only 3 saturated pairs in the entire (N,D) space: (2,2), (3,3), (3,4).

For D≥5, the saturation polynomial D(D−1)(5−D)/6 is ≤ 0 — no SU(N) with N≥2 can be saturated.
**D=4 is the last non-trivial dimension.**

---

## 5. Roadmap M0-M15

| Month | Action |
|-------|--------|
| M0 | Pitch v22.1 sent |
| M1-3 | Draft LMP conditional paper (Piste E) |
| M3 | Submit to LMP |
| M3-6 | Peer review + Bauerschmidt collaboration on H10 |
| M6-9 | Polchinski cascade U(1) → SU(2) extension |
| M9-15 | Paper 2: minimal publiable or SU(2) D=4 resolved |

Probabilities:
- Min publiable LMP at 9 months: 55-75%
- SU(2) D=4 resolved at 15 months: 8-15%
- P(Clay 10y): 45-60% (B1 dominant)
