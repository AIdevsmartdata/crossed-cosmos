# ECI v6 — External Deep-Audit Archive (Claude.ai, 2026-04)

**Purpose.** Reference document for all subsequent v6 agents. Summarises the external
Claude.ai deep-audit of the proposed composite ECI v6 equation.

**Overall verdict.** Composite scoop risk **1.5–2 / 5** (low).
The full composite equation has no published occurrence; individual pieces have
near neighbours but none combine complexity geometry, persistent homology, and
observer-dependent modular flow as a differential *equality* for generalised entropy.

---

## 1. The equation

```
  dS_gen[R]                                              
  ─────────  =  κ_R · C_k[ρ_R(τ)] · Θ( PH_k[δn(τ)] )
    dτ_R                                                 
```

Differential equality for the rate of generalised entropy associated with a
subregion `R`, taken along its modular (Connes–Tomita–Takesaki) flow.

---

## 2. Component definitions

| Symbol | Meaning |
|---|---|
| `τ_R` | Modular proper time of region `R` (Connes–Tomita–Takesaki flow). |
| `κ_R` | Observer-dependent entropic conductance, units `[nat · t⁻¹]` (nat per modular e-fold). Owner decision 2026-04-22: adopt `κ_R ≡ 2π T_R` (Tomita–Takesaki modular temperature); reduces to `H` at de Sitter Gibbons–Hawking. [Prior draft said `nat · t⁻²` — **corrected per Claude+Adversarial cross-check**.] |
| `C_k[ρ_R(τ)]` | `k`-design complexity of the reduced state `ρ_R` (Ma–Huang PRU sense). |
| `Θ(·)` | Chameleon-like activator `exp[-(PH_k/PH_c)^α]`, with `α = 0.095`. |
| `PH_k[δn]` | Persistent-homology Betti number of order `k` on the density field `δn(τ)`. |

Two bibliographic flags raised by Claude.ai that turned out to be non-issues:
- CryptoCensorship arXiv ID is indeed `2402.03425` (already correct in our `eci.bib`).
- Heller–Papalini–Schuhmann `2412.17785` (PRL 135 151602) is not cited; not relevant.

---

## 3. Per-component scoop-risk table

| Component | Closest published predecessor | Risk 0–5 |
|---|---|---|
| `dS_gen/dτ_R =` source equality | Wall 2011; Faulkner–Speranza 2024 (inequalities only) | 1.5 |
| `κ_R` observer-dependent conductance | DEHK 2024–2025 (static form only) | 1.0 |
| `C_k` `k`-design complexity as multiplicative source | No explicit coupling published | 1.5 |
| `C_K` Krylov variant | Fan 2022: `Ṡ_K ≈ Ċ_K/C_K` (logarithmic) | **3.5** |
| `Θ(PH_k)` topological activator | Not published | 0 |
| Chameleon `exp[-(PH/PH_c)^α]`, `α = 0.095` | Khoury–Weltman `α = 1` standard | 1.0 |
| Observer-dep of the temporal derivative | Not published | 0.5 |
| **Complete composite equation** | **No occurrence found** | **1.5** |

The `C_K` Krylov variant is the *only* component where a genuinely close precursor
exists (Fan 2022). We must demarcate quantitatively from the logarithmic form.

---

## 4. Five confirmed originality gaps

1. **Differential equality** for `dS_gen/dτ_R` with a positive source term, versus
   the monotone *inequality* (GSL-style) in Wall / Faulkner–Speranza / Kirklin.
2. **`k`-design complexity as the source** — not geometric shear (Eling–Guedens–
   Jacobson), not logarithmic (Fan 2022).
3. **Persistent-homology `PH_k` topological activation** inserted into a
   horizon-entropy ODE.
4. **Observer dependence of a temporal derivative** — DEHK only cover the static
   theorem; the flow-level statement is new.
5. **Chameleon exponent `α = 0.095`** — departs from Khoury–Weltman `α = 1`;
   possible anchor in Barrow-entropy `Δ ≲ 0.1`.

---

## 5. Obligatory citation list (47 references)

### 5.1 Differential GSL / modular / Type II
- Wall 2011 — `arXiv:1105.3445`, PRD 85 104049.
- Eling–Guedens–Jacobson 2006 — `arXiv:gr-qc/0602001`, PRL 96 121301.
  Closest formal precursor: `dS = δQ/T + d_i S`.
- CLPW 2023 — Type II crossed-product algebras.
- DEHK 2024–2025 — observer-dependent entropy (static).
- Faulkner–Speranza 2024 — modular inequalities.
- Kirklin 2025 — differential GSL refinements.
- Witten 2023 — gravity + Type II framework.
- Connes–Rovelli 1994 — CQG 11 2899, thermal modular time origin.

### 5.2 Krylov complexity & entropy (tight precursor zone)
- Fan 2022 — JHEP 08 232. `|∂_t S_K| ≤ 2 b₁ ΔS_K` — tightest Krylov precursor.
- Barbón–Rabinovici–Shir–Sinha 2019 — `arXiv:1907.05393`, JHEP 10 264.
  `S_K ∼ ln C_K`.
- Caputa–Magán–Patramanis–Tonni 2024 — `arXiv:2306.14732`, PRD 109 086004.
  Modular flow × Krylov complexity; `λ_L^mod = 2π`.

### 5.3 Complexity growth
- Brown–Susskind 2018 — `arXiv:1701.01107`, PRD 97 086015. 2nd law of complexity.
- Haferkamp et al. 2022 — `arXiv:2106.05305`, Nat. Phys. 18 528. Linear growth.
- Schuster–Haferkamp–Huang 2025 — `arXiv:2407.07754`, Science. Short-depth PRU.
- Ma–Huang 2025 — `arXiv:2410.10116`, STOC. PRU existence.
- Engelhardt et al. — CryptoCensorship, `arXiv:2402.03425`.

### 5.4 Computation / thread geometry
- Pedraza–Russo–Svesko–Weller-Davies 2022 — `arXiv:2106.12585`, JHEP 02 (2022) 093.
  Lorentzian threads.
- Carrasco–Pedraza–Svesko–Weller-Davies 2023 — `arXiv:2306.08503`, JHEP 09 167.
  Gravity from optimised computation.
- Bianconi 2025 — `arXiv:2408.14391`, PRD 111 066001. Gravity from entropy.
  **Notational collision on `Θ` — flag in draft.**

### 5.5 Persistent homology / cosmology
- Yip–Biagetti–Cole–Viswanathan–Shiu 2024 — `arXiv:2403.13985`, JCAP 09 034.
  PH_k cosmology pipeline.
- Biagetti–Cole–Shiu 2021 — `arXiv:2009.04819`, JCAP 04 061. Foundations.
- Wilding et al. 2021 — MNRAS 507 2968. Observational PH_k.
- Heydenreich et al. 2022 — A&A 667 A125, `arXiv:2204.11831`.
- Pranav 2024 — A&A 681 A41, `arXiv:2308.10738`. 3.9σ CMB loops.
- Rucco et al. — DOI `10.1007/s10844-017-0473-4`. Persistent entropy.

### 5.6 Chameleon / modified entropy
- Khoury–Weltman 2004 — `astro-ph/0309300`, PRL 93 171104. Chameleon.
- Burrage–Sakstein 2018 — Living Rev. Rel. 21 1. Review.
- Barrow 2020 — PLB 808 135643. Fractal entropy `Δ ~ 0.1`; candidate anchor for
  `α = 0.095`.

### 5.7 Predictive / learning thermodynamics
- Still–Sivak–Bell–Crooks 2012 — PRL 109 120604.
- Still 2020 — PRL 124 050601. Predictive info-bottleneck.
- Goldt–Seifert 2017 — PRL 118 010601. Learning bound.
- Wolpert 2019 — J. Phys. A 52 193001. Stochastic computation.
- Bialek–Nemenman–Tishby 2001 — Neural Comput. 13 2409. Predictive information.

### 5.8 Ancestral thermodynamic / entropic gravity
- Jacobson 1995 — `gr-qc/9504004`.
- Jacobson 2016 — `arXiv:1505.04753`.
- Verlinde 2011 — `arXiv:1001.0785`.
- Verlinde 2017 — `arXiv:1611.02269`.
- Barbour–Koslowski–Mercati 2014 — PRL 113 181101. Shape-complexity arrow.

Total: 47 entries (some 5.x subsections share items; canonical list in
`v6_citations_needed.md`).

---

## 6. Surveillance targets (6–18 month scoop horizon)

1. **Pedraza–Svesko–Weller-Davies** (gravity-from-computation) — most likely to
   derive a time-dependent form.
2. **Bianconi** (gravity-from-entropy) — could extend to temporal derivatives;
   already uses a symbol `Θ`, watch for notational overlap.
3. **Caputa–del Campo–Nandy** (Krylov reviews) — may publish a linear
   intermediate-regime `Ṡ ∝ C`.

---

## 7. Editorial strategy

- Frame as a **non-equilibrium extension of the Eling–Guedens–Jacobson schema**:
  specify `d_i S` via Nielsen–Brown–Susskind–Haferkamp complexity geometry,
  Yip 2024 topological modulation, and Khoury–Weltman chameleon activation.
- Demarcate *quantitatively* from Fan 2022 logarithmic Krylov form.
- Keep the JEPA / LeCun analogy as a **programmatic conjecture**, not a formal
  extension.
- Target journals: **JCAP** (cosmology-leaning), **PRD** (gravity-leaning), or
  **JHEP** (QG-leaning), depending on the balance at submission.
- **Fast arXiv deposit for priority.**

---

## 8. Next steps for the v6 investigation (added by archive agent)

### 8.1 Derivation attempts
- Derive the equality from a Jacobson-type local Clausius argument with an
  explicit internal-production term `d_i S = κ_R C_k Θ(PH_k) dτ_R`.
- Check consistency with Wall's differential GSL in the inequality limit
  (`Θ → 1`, `C_k` constant).
- Attempt a Fan-2022 reduction: show that `C_k → ln C_K` recovers the logarithmic
  Krylov law in a well-defined regime.

### 8.2 Adversarial probes
- Stress-test the observer-dependence of `dτ_R` under a Type II crossed product;
  verify that `κ_R` transforms covariantly.
- Search for a counter-example where `PH_k → 0` must not trivially kill
  `dS_gen/dτ_R` (risk of over-killing vacuum contributions).
- Check that the chameleon activator does not reintroduce a fifth-force
  pathology at cosmological scales.

### 8.3 Dimensional analysis agenda
- Confirm `[κ_R] = nat · t⁻¹` across the three target regimes (near-horizon QFT,
  cosmological coarse-grained, laboratory analogue). **Adopted form**: `κ_R ≡ 2π T_R`
  (Tomita–Takesaki modular temperature), reducing to `H` at de Sitter Gibbons–Hawking.
- Verify `C_k` is dimensionless in the Ma–Huang PRU normalisation.
- Check that `PH_k/PH_c` is genuinely scale-free, so `α = 0.095` is a pure number.
- Cross-validate `α = 0.095` against Barrow `Δ ≲ 0.1` within `1σ` of current
  observational bounds.

### 8.4 Drafting order
1. Lock `v6_citations_needed.md` → feed to bib-adding agent.
2. Produce a dimensional-analysis memo.
3. Derive the equality (sec 8.1) before writing any `eci.tex` prose.
4. Only then touch `eci.tex`.
