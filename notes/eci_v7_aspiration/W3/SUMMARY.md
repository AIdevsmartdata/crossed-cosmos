# W3: EHT BH Shadow — ECI Falsifiability Assessment

**Date:** 2026-05-04
**Analyst:** W3 sub-agent

---

## 1. Literature Search Results (Live-Fetched)

### Search 1 — EHT + ECI-specific terms
Queries: "EHT shadow ECI crossed product", "EHT modular flow black hole shadow", "type-II factor black hole shadow photon ring", "generalized second law type-II algebra shadow"
**Result: 0 hits.** No arXiv paper exists connecting ECI's algebraic structure (crossed products, type-II factors, modular flow) to any BH shadow or EHT observable.

### Search 2 — Adjacent frameworks (modified gravity BH shadows)
Papers that DO make EHT-testable shadow predictions from modified gravity:

- **arXiv:2601.05040** (Jan 2026) — F(R)-Euler-Heisenberg BH shadows vs. M87* EHT
- **arXiv:2410.09198** (Oct 2024) — Rotating quantum-corrected BHs (LQG-inspired), EHT constraints on α for M87*, Sgr A*
- **arXiv:2501.01308** (Jan 2025) — Effective LQG Kerr corrections, EHT shadow constraints; correction ζ (dimension: length), ratio ζ/M bounded by EHT
- **arXiv:2312.17724** — LQG quantum BH shadow, Barbero-Immirzi γ≈0.2375; shadow deviation = α/(6√3 M), negligible for macroscopic BHs
- **arXiv:2509.05594** (Sep 2025) — "Shadow spectroscopy" parametric framework; theory-agnostic metric deformations, no algebraic QFT structure
- **arXiv:2601.23012** (Jan 2026) — Scalar-tensor-vector gravity tested via photon rings

### Search 3 — DSSYK / Krylov / algebraic approaches + EHT
**Result: 0 hits.** No paper connects DSSYK, Krylov complexity, or operator-algebraic BH entropy (Witten crossed product, type-II∞) to photon orbit observables.

### Search 4 — Faulkner-Speranza (arXiv:2405.00847) + EHT
Confirmed: "Gravitational algebras and the generalized second law" by Faulkner & Speranza — derives GSL via crossed-product algebras on Killing horizons. **Makes zero observational predictions about shadow size or photon sphere.**

### Search 5 — DEHK (arXiv:2412.15502) + EHT
Confirmed: De Vuyst, Eccles, Hoehn, Kirklin — type-II crossed products for observer-dependent entropy. **No predictions for BH shadow or null geodesics.** Pure algebraic entropy formalism.

---

## 2. EHT Reference Measurements (Verified)

- **M87***: diameter 42 ± 3 μas — EHT Collaboration 2019 ApJL 875 L1 (arXiv:1906.11238)
- **Sgr A***: diameter 51.8 ± 2.3 μas — EHT Collaboration 2022 ApJL 930 L12

---

## 3. Physical Scale Analysis

### What modifies BH shadows?
EHT-testable shadow deviations arise when a theory introduces a **dimensional parameter** that modifies the metric at the photon sphere radius r_ph = 3M (Schwarzschild). The deviation scales as δr_sh/r_sh ~ (new parameter)/M.

### Examples of constrained parameters (from literature):
- LQG polymerization: ζ with dimension [length]; EHT constrains ζ/M ≲ O(1) (arXiv:2501.01308)
- Effective QG: shadow Rs = 3√3M·[1 - α/(162M²) + ...]; correction O(α/M²) (arXiv:2408.05569)
- F(R) gravity: additional scalar mode alters photon effective potential

In all viable models, the correction parameter must be **at most order M** in length to survive EHT. Genuine Planck-scale corrections (ζ ~ l_Planck) give δr_sh/r_sh ~ l_Planck/M ~ 10⁻⁴⁰ for Sgr A* — unobservable by 39 orders of magnitude.

### ECI's structural ratio ρ_p,k = k/(12(k+1))
This is a **pure dimensionless number** (0 < ρ < 1/12) characterizing the type-II trace in the algebraic diamond. It carries no length dimension. To modify the photon sphere one needs a dimensionful correction to the spacetime metric, e.g.:

  g_tt → -(1 - 2M/r)[1 + f(ρ_p,k)·(l²/r²) + ...]

where l is a new length scale. **ECI introduces no such length scale.** The type-II crossed-product structure characterizes how observer-dependent entropy is computed — it is a constraint on the algebra of observables, not a deformation of the background metric.

### Modular flow / KMS condition on Killing horizons
In the Hartle-Hawking state on a Schwarzschild background, modular flow IS the Killing time translation — already built into the classical geometry. It does not deform null geodesics; it identifies the vacuum thermal structure on the existing metric. ECI invoking this structure inherits the existing geometry without modifying photon orbits.

---

## 4. Verdict

**[STRUCTURAL CONNECTION ONLY — algebra-aligned but no quantitative test possible]**

ECI's algebraic foundation (type-II crossed products, Killing horizon GSL, modular flow KMS) is genuinely connected to BH thermodynamics at the conceptual level. However:

1. The connection is at the level of **entropy accounting**, not metric deformation.
2. ECI introduces **no new dimensional length scale** that could enter the photon sphere radius or shadow diameter formula.
3. ρ_p,k is dimensionless and cannot produce a δ(shadow diameter) in μas without a bridging length scale absent from the framework.
4. The closest literature (Faulkner-Speranza 2405.00847, DEHK 2412.15502, arXiv:2601.07915) confirms: all algebraic-type-II BH papers make zero EHT-testable predictions.
5. Gap: EHT resolution ≈ 10% of shadow size; Planck-scale correction to shadow ≈ 10⁻⁴⁰ — 39 orders of magnitude apart.

---

## 5. Recommendation

**Do not pursue EHT as an ECI falsifier.**

- The algebraic-QG layer is at the Planck scale; BH shadow is a classical-geometry observable at the BH mass scale.
- No derivation bridges ECI's ρ_p,k (dimensionless) to a photon-sphere shift (needs a length) without introducing physics beyond ECI's current scope.
- Existing quantum-gravity BH shadow tests (LQG, EQG, F(R)) all work by modifying the metric explicitly — ECI does not do this.

**Condition for future relevance:** If a later ECI derivation produces a **concrete metric ansatz** with a new length parameter (analogous to LQG polymerization scale), then EHT constraints could apply. Until then, EHT is not in ECI's falsification programme.

**Confirmed working falsifiers (prior campaigns):** DESI/Pantheon+ cosmological, BEC analog Hawking, FRB DM-z, JWST z>10 structure formation. EHT adds nothing at this stage.
