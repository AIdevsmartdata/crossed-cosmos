# H46 + H48 — Hausdorff / spectral dimension of Ω̄ (Gribov-Zwanziger FMR)

Date: 2026-05-26.

## 1. Weyl law

On a smooth d-dim Riemannian manifold, the spectral counting of −Δ obeys
  N(λ) ~ c · Vol · λ^{d/2}  ⇒  ρ(λ) ~ λ^{d/2−1}.
On a fractal, d is replaced by the **spectral dimension** d_s (possibly non-integer, d_s ≤ d_H).

## 2. Naive dim(𝒜/𝒢), SU(N), 4D L⁴ lattice

- dim 𝒜 = (N²−1)·D·L^D (D=4)
- dim 𝒢 = (N²−1)·L^D (local gauge per site, mod center)
- naive Coulomb slice: dim(𝒜/𝒢) = (N²−1)(D−1)L^D = **3(N²−1)L^D**.

SU(2), L=8: 36 864. SU(3), L=8: 98 304. Ambient before Gribov restriction.

## 3. Why Ω̄ has lower effective dimension

(a) **Horizon condition.** At ∂Ω, λ_1(M_FP)→0; Zwanziger's horizon function concentrates the measure on a codim-1 stratification.
(b) **Self-similar copies.** Cucchieri (1998) shows typical configs sit *very close* to ∂Ω̄ — boundary-dominated, signature of fractal support d_H < d_ambient.
(c) **Singer/DZ obstruction.** No continuous global gauge section ⇒ Ω̄ is stratified with corners; measure concentrates on a stratum of positive codimension.

These justify d_H(Ω̄) < dim(𝒜/𝒢)_naive but do **not fix a numerical value**.

## 4. Connection to K41 5/3 (H46)

κ_EE(N) ~ N^{5/3} scales in **color/representation**, not space. Spatial route: Alexander–Orbach
  d_s = 2 d_H / d_w.
- **H46 strong:** if d_w/d_H = 6/5 on ∂Ω̄, then **d_s = 10/3 ≈ 3.33** — would tie K41 inertial scaling to 4-niveau Bakry–Émery (KR-FP-Hess).
- **H46 weak:** d_s = 4 bulk, 5/3 is purely color-space, no spatial echo.

No rigorous derivation either way exists. H46 is a *conjecture*.

## 5. Literature: is N(λ) measured?

- **Greensite–Olejník–Zwanziger 2005** (hep-lat/0509054): ρ_FP(λ) measured Coulomb gauge SU(2), L=12–24. Observe **near-zero enhancement** vs perturbative free Laplacian (which gives ρ~λ). Qualitatively ρ(0⁺) ≠ 0 in confined phase → d_s → 2 from below (ρ ~ const ⇔ d_s = 2). **No published fitted exponent in abstract.**
- **Nakagawa–Nakamura–Saito–Toki 2007** (hep-lat/0702002, Phys.Rev.D75:014508): SU(3) confirms low-λ ρ grows with volume in confinement. **No power-law α in abstract.**
- **Cucchieri–Mendes 2013** (1308.1283, PRD88 114501): bound ghost propagator by 2 smallest λ_i; configs cluster near ∂Ω; **no global ρ(λ) ~ λ^α fit published.**

So no clean published d_s for Δ_FP on Ω̄. The qualitative datum ρ(0⁺) > 0 is consistent with **d_s ≈ 2** (Coulomb SU(2)), which would **falsify H46 strong (10/3)** if quantitatively confirmed.

## 6. Proposed protocol on existing configs

Reuse JAX SU(N) thermalized ensembles (post Metropolis K† fix):
1. Build sparse M_FP Coulomb (existing KR-FP-3 code).
2. Lanczos 200–500 lowest λ (JAX `lobpcg`).
3. Log-log fit ρ ~ λ^α on λ ∈ [λ_1, 10λ_1].
4. d_s = 2(α+1).
5. SU(2,3,4), L=8,12,16, β at const physical volume.

Cost: 4–8 h ssh8.

## 7. Verdict

- **H46 (d_s = 10/3):** plausible but **unsupported**; lattice hint (Greensite et al.) points to d_s ≈ 2, in tension. Status: **conjectural, leaning falsified.** P = **15–25 %**.
- **H48 (ρ ~ λ^{d_s/2−1}):** the generic Weyl-on-fractal form. **Tautologically valid** once d_s is defined; empirical content is the fitted α. P = **70–85 %** as ansatz; gives no value by itself.

## 8. Verified arXiv references

1. **hep-lat/9711024** — A. Cucchieri, "Numerical Study of the Fundamental Modular Region in the Minimal Landau Gauge", Nucl.Phys.B521 (1998) 365. Verified.
2. **hep-lat/0509054** — Greensite, Olejník, Zwanziger, "Gribov horizon under the (lattice) microscope", PoS LAT2005 (2005) 293. Verified.
3. **1308.1283** — Cucchieri, Mendes, "Ghost sector and geometry in minimal Landau gauge…", Phys.Rev.D88 (2013) 114501. Verified.

Supplementary verified: **hep-lat/0702002** (Nakagawa et al., PRD75:014508), **1311.4699** (Cucchieri–Mendes Lattice 2013 proc).

Unverified: Zwanziger 1996 Phys.Lett.B 367 374 (no clean arXiv match returned); Dell'Antonio–Zwanziger 1991 CMP 138, 291 (pre-arXiv-routine; not found as preprint).

## Bottom line

Naive dim(𝒜/𝒢) = 3(N²−1)L⁴; Gribov restriction shrinks d_H via horizon + copies + Singer obstruction, but published data **do not fix d_s quantitatively**. H46 strong (d_s = 10/3) is non-trivial but **in tension** with Greensite et al.'s qualitative ρ(0⁺) > 0 (suggesting d_s ≈ 2 in confined SU(2) Coulomb). H48 is the correct Weyl-on-fractal *form*; predictive content = the fitted α. **Next action:** §6 protocol on existing thermalized configs, 4–8 h, decisive for H46.
