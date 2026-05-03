# CCM 2511.22755 ↔ HY 2502.02661 — Four-Gap Closure Assessment

**Date**: 2026-05-03. **Companion**: `/tmp/CCM_BIX_dictionary_max.{py,tex}`.
**PDFs read live**: `/tmp/papers/HY_2502.02661.pdf`, `/tmp/papers/CCM_2511.22755.pdf`.
**Sympy**: 1.12, all checks pass.

## Verbatim citations (HTML-fetched this session)

**HY eq. (37)**, §4.2: `D ψ = i(x dψ/dx + Δ ψ)`, Δ = ½ + iε.
**HY §4.3**: *"in a basis of dilatation eigenstates the wavefunction is
proportional to the L-function along the critical axis and hence vanishes
at the nontrivial zeros."*
**HY §6** (attributed to Connes): *"a minus sign in the asymptotic formula
for the density of zeros suggests that the zeros should be interpreted as
an absorption spectrum."*

**CCM eq. (5.14)**: `D_log^(λ) = -i u ∂/∂u`, on L²([λ⁻¹,λ], du/u), periodic BC.
**CCM Thm 1.1(i)**: `D_log^(λ,N) = D_log^(λ) - |D_log^(λ) ξ⟩⟨δ_N|`.
**CCM Thm 1.1(ii)**: `det_reg(D_log^(λ,N) - z) = -i λ^(-iz) ξ̂(z)`.
**CCM Thm 1.1(iii)**: zeros of ξ̂ are real and equal spec(D_log^(λ,N)).
**CCM §4.2 Euler product**: cutoff at primes p ≤ x = λ² (verified algebraically:
exp(L)=λ² for L=2 log λ).

## arXiv-API triangulation

- HY arXiv:2502.02661v2 (JHEP 07(2025)281), CCM arXiv:2511.22755v1 (2025-11-27): both VERIFIED via PDF + API.
- **NEW**: DCHY arXiv:2507.08788 (5d BKL, July 2025): VERIFIED, does NOT cite CCM.
- "Perlmutter zeta 2025": UNVERIFIED, no matching ID — flagged Bing hallucination.
- Cross-search "CCM AND Hartnoll", "zeta spectral triple AND Bianchi", "BKL AND Riemann zeros": **0 hits**.

## Gap-by-gap verdict

### (a) HY's L = wavefunction overlap, NOT D_HY eigenvalue — **ESSENTIAL**

HY explicitly identifies φ(t) := ⟨ψ_t | ψ⟩ ∝ L(½+it) as a Mellin overlap
(eq. 45). Sympy verifies that ψ_t = x^(-Δ-it) IS a D_HY eigenstate with
eigenvalue t∈ℝ — so spec(D_HY)=ℝ continuous. Riemann zeros γ_n are nodes
of the overlap, **not** in spec(D_HY). DCHY 2507.08788 was inspected (HTML
fetch); it extends to 5d via Bianchi groups PSL(2,𝒪) and Maass forms but
**does not** introduce any operator with discrete Hilbert-Pólya spectrum.
**No inversion formula exists in either paper.** Reroute must come from
CCM side, not HY side.

### (b) CCM rank-one perturbation as B-IX modular cocycle — **PARTIALLY OPEN**

CCM's P = |D_log ξ⟩⟨δ_N| is rank-one but **static** (no t-dependence), so
not a Connes 1-cocycle of the BFV modular flow as written. Reparameterising
by τ = log λ, sympy shows the leading-order eigenvalue shift δ(τ) = 1/(2τ)
satisfies the harmonic-mean composition law
δ(τ+σ) = δ(τ)δ(σ)/(δ(τ)+δ(σ)) — **necessary but not sufficient** for a
1-cocycle. The bottleneck is the ξ-vector: CCM defines it via the Weil
quadratic form Q_W^N (number-theoretic), with no known geometric realisation
on B-IX minisuperspace. ~1 month for a candidate cocycle, several months
for rigour.

### (c) Dictionary CCM perturbation ↔ HY modular constraint — **DRAFTED, MISMATCHED**

**No published dictionary** (arXiv API: zero hits across three relevant
queries). Drafted dictionary in script §(c). **Key obstruction discovered**:
Weyl law for cusp forms on PSL(2,ℤ)\ℍ is N(T)~T²/12, but Riemann zeros
density is N(T)~T log(T/2π)/(2π) — **different scaling**. So
"cusp-form spectrum = Riemann zeros" is wrong; the dictionary needs to
restrict to a **subset** of cusp forms (or pick out the Eisenstein
contribution). 1-2 months to draft, >1 year for rigour.

### (d) WDW vs BFV folium framework gap — **DEEPEST, NOT INTRACTABLE**

Three bridges examined:
- **(d.1) Second-quantize WDW**: FAILS (1-d vs ℵ₀-d Hilbert spaces).
- **(d.2) Chrono-projection**: PARTIAL. Sympy: Mellin transform of the
  Kasner-pullback two-point function `w(s₁,s₂) ~ 1/(s₁s₂)` produces
  Γ(½-it)/Γ(3/2-it) — exactly HY's dilation basis. So a chrono-projection
  exists in principle.
- **(d.3) Plancherel on PSL(2,ℤ)\ℍ**: MOST PROMISING. The BFV-folium
  modular Hilbert space (after BKL truncation) decomposes as
  L²_cusp ⊕ L²_resid ⊕ L²_Eisenstein. The Eisenstein sector has spectral
  measure on Re(s)=½ and its functional equation involves ζ(s) directly.
  CCM's "rank-one perturbation over p ≤ λ²" likely corresponds to
  restricting to Eisenstein series with conductor ≤ λ². 2-3 months for
  draft, 1-2 years for rigour.

## Honest triage

| Gap | Closeable in | Notes |
|-----|--------------|-------|
| (a) | **intractable** at HY-side | Reroute via CCM dilation/Eisenstein |
| (b) | **1 month** (draft) | Need ξ as automorphic Maass form |
| (c) | **1-2 months** (draft) / >1y rigour | Subset-of-cusp-form selection required |
| (d) | **2-3 months** (draft) / 1-2y rigour | Plancherel-Eisenstein bridge is the key |

## Time-to-publication

- **1 week**: refined NO-GO on (a) — Comment on HY.
- **1 month**: (b) + draft (c) — preprint with conditionals.
- **6 months**: (b)+(c)+(d) drafted — JHEP companion, conditional on
  Hadamard existence on B-IX (open since T2-Bianchi IX).
- **1.5-2 years**: full rigour.

**Recommended**: 6-month preprint. Position as a *conditional dictionary*
between CCM's restricted-Euler-product perturbation and Eisenstein sectors
of BFV-folium modular data on Bianchi IX. List (a) as known obstruction;
(d.3) as the substantive contribution. Do NOT claim RH.
