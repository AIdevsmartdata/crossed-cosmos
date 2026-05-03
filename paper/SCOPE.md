# Scope and Limitations of the ECI Framework

*ECI v6.0.27 — Lecture (b): documenting bounded scope*
*Drafted 2026-05-03. Authoritative source: `scope_and_limitations.tex` (insertable into `eci.tex`).*

---

## One-paragraph summary

The **Entanglement–Complexity–Information (ECI)** programme is a
mathematical-physics framework in the post-CLPW algebraic-quantum-gravity
tradition. It constructs a **type-II_∞ von Neumann factor** for FRW
cosmological diamonds via a quantum-reference-frame crossed product
(Witten 2022; CLPW 2023), derives a **modular (Krylov) complexity** measure
on that algebra, and uses Bisognano–Wichmann theory and Hadamard-state
analysis to characterize which vacuum boundary conditions are algebraically
admissible near the Big Bang. The framework's value is structural and
exclusionary: it gives sharp results about **what is and is not
algebraically possible** in cosmological QFT on a fixed background, not
about fitting observational tensions or deriving particle masses.

---

## §1 What ECI claims and is positioned to prove

### Established results

| Result | Status | Caveat |
|---|---|---|
| FRW type-II_∞ crossed product (Theorems 3.5–3.6) | Algebraically established | FRW background fixed; full QG backreaction not addressed |
| Lemma 3.3 conformal pullback `U⁻¹ T^Mink_{00} U = a² 𝒯^FRW_{00}` | sympy-verified off-shell | Massless conformally-coupled scalar only |
| `K_FRW` closed form (R-piste 6) | ~80% paper-ready | Radiation-era diamond; Bisognano–Wichmann normalization structural, not fit |
| Krylov-Diameter Theorem 4: `(1/C_k) dC_k/dt = 1/R_proper + O(C_k⁻¹)` | Conditional | Conditional on Block A1 UOGH transfer from type-III_1 to type-II_∞ (unproven) |
| Algebraic Weyl Curvature Hypothesis T2-FRW | sympy-verified, 3 obstructions | Within Hollands–Wald Hadamard convention only |
| T2-Bianchi I | sympy-verified, 2 IR divergences | Vacuum, massless scalar; stiff-fluid extension open |
| Theorem T3 (algebraic arrow of time) | Derived from T2 | Arrow of time still requires Past Hypothesis as boundary condition; T3 gives algebraic correlate, not independent derivation |
| Levier 1B MCMC (H_0 = 67.67 ± 0.57 km/s/Mpc, ξ_χ null) | Observational MCMC result | NMC observational constraint, not algebraic theorem |

### What the positive results mean

Piste 1 gives a partial positive: the Krylov rate `(1/C_k) dC_k/dt` equals
`H(t)` **exactly** in the radiation era for a Hubble-horizon diamond, and
equals `1/(2t)` vs `2/(3t)` in the matter era (factor 1/2 discrepancy). The
match in the de Sitter / Hubble-horizon case is tautological by diamond
definition. The result is a **geometric identity** relating complexity growth
to the diamond's proper radius — not a derivation of cosmology from algebra.

---

## §2 What ECI explicitly does NOT claim: the NO-GO catalogue

The following results have been tested and closed. They are listed not as
defeats but as **calibration successes**: each closed avenue narrows ECI's
scope in a reproducible, documented way.

### Five Pistes — all tested, 1 partial positive, 4 negative/null

| Piste | Claim tested | Verdict | Reason |
|---|---|---|---|
| Piste 1 | `H = Krylov rate` (general) | Partial positive (radiation era only) | Matter-era off by factor 1/2; de Sitter tautological by diamond choice |
| Piste 2 | Era transitions = Jones–Longo subfactor inclusions | NEGATIVE | Jones index = 1 trivially (factors isomorphic at transition) |
| Piste 3 | Λ from modular relaxation steady-state | TAUTOLOGICAL | Type-II trace fixes relative scale only; 121-order normalization mismatch |
| Piste 4 | Riemann zeros as cosmological modular Hamiltonian spectrum | NO-GO | K_FRW has continuous spectrum; Riemann zeros are discrete |
| Piste 5 | SM field content from modular 2-categorical compatibility | NO-GO | Type-I sector has only inner modular automorphisms; SM gauge not extractable |

### Ten R-pistes — all tested, 1 positive byproduct, 9 negative/null

| R-piste | Claim tested | Verdict | Reason |
|---|---|---|---|
| R1 | Λ from T1↔T2 algebraic asymmetry | NUMEROLOGY | Post-hoc normalization; no structural derivation |
| R2 | H_0 from Krylov-Diameter Theorem 4 | POSITIVE BYPRODUCT (not H_0) | ⟨p_3⟩ closed form genuine; but Krylov rate = 1/R_proper ≠ H_0 in matter era |
| R3 | S_8 as BFV folium-projection ambiguity | KILLED by Verch 1994 | Local quasi-equivalence of all Hadamard states; no projection ambiguity within folium |
| R4 | SM 3 generations from Bianchi IX SU(2) Kasner axes | REFUTED | dim(su(2)) = 3 counts spatial isometry generators, not fermion generations |
| R5 | RH via Maass–Selberg + theta-correspondence | CONDITIONAL COMPANION | Downgraded from RH-proof; surviving claim is conditional spectral correspondence only |
| R6 | AdS/CFT in FRW II_∞ frame | CONDITIONAL COMPANION | Original framing falsified; surviving claim is structural compatibility with CLPW, not holographic dictionary |
| R7 | Hierarchy from c' modular trace ratios | NUMEROLOGY | Same arbitrary normalization as Piste 3 |
| R8 | Generation count from PSL(2,Z)\H Eisenstein/cusp sectors | REFUTED by Weyl law | Weyl law gives continuous eigenvalue density ~T log T, not finite count 3 |
| R9 | Dark matter from Bianchi VIII Mixmaster Kasner-bounce relics | KILLED by T2 | T2-Bianchi requires Hadamard state to exist at singularity; it does not |
| R10 | SM gauge from BKL ↔ E_10 Kac–Moody | NO-GO via DKN walls | BKL billiard walls encode E_10, not SU(3)×SU(2)×U(1) multiplets |

### The three explicit "we do not claim" statements

**1. No derivation of Λ.**
The observed value ρ_Λ/M_P⁴ ≈ 10⁻¹²¹ is not explained within ECI.
Three independent arithmetic checks each fail by 14–89 orders of magnitude.
The type-II tracial weight cannot determine an absolute energy density.

**2. No resolution of the H_0 tension.**
Levier 1B returns H_0 = 67.67 ± 0.57 km/s/Mpc (consistent with Planck),
4.5σ from SH0ES. The NMC sector (ξ_χ = −0.00003, 68% CI straddles zero)
produces weak/moderate evidence for ΛCDM over NMC. The Hubble tension is
**unresolved** by ECI. Algebraically, the Krylov rate is 1/R_proper, which
in the matter era gives 1/(3t), not H(t) = 2/(3t).

**3. No derivation of SM particle content.**
Piste 5 closes the modular-automorphism route. R4 closes the Bianchi IX
generation-counting route. R8 closes the modular-surface sector-counting
route. R10 closes the BKL/E_10 route. All four independent approaches
return NO-GO.

---

## §3 Open problems within ECI's scope

These are live research frontiers where the ECI apparatus has genuine traction.

| Problem | Status | Estimated effort |
|---|---|---|
| Block A1: unconditional UOGH on type-II_∞ KMS (b_n = πn proof) | B6 wave-3 in progress (restricted class); full closure open | 2 wk (restricted) / 2–3 mo (full) |
| Connes-embedding status of FRW II_∞ factor (likely hyperfinite by Connes–Takesaki 1977) | Not yet written up | 6–8 wk, math.OA note |
| T2-Bianchi V (negatively-curved spatial sections) | Conditional on Hadamard existence on H³ | 3–6 wk |
| T2-Bianchi IX (Mixmaster) | Requires BKL invariant-measure analysis | 4–8 wk |
| Algebraic WCH paper submission (T2-Bianchi I central result) | ~80% paper-ready | 2–3 wk polish |
| Bianconi 2025 PRD Comment (Lorentzian-signature gap; B8 in flight) | Draft exists | 1–2 wk |
| BEC analogue-FRW first experimental falsifier (Lemma 3.3 + Thm 4) | No co-author yet | 6–9 mo |

---

## §4 Open problems explicitly outside ECI's apparatus

| Problem | Reason ECI is silent |
|---|---|
| Λ ~ 10⁻¹²² (cosmological constant) | Type-II trace fixes relative scale only; no mechanism for 10⁻¹²¹ suppression |
| H_0 SH0ES tension (4.5σ, unresolved) | NMC sector null (Levier 1B); Krylov rate ≠ H_0 in matter era |
| SM particle content, gauge group | All four algebraic routes (Piste 5, R4, R8, R10) return NO-GO |
| S_8 KiDS vs Planck tension | R-piste S_8 NEGATIVE; NMC null at current MCMC sensitivity |
| Swampland / de Sitter stability | D8 gives cross-constraint only; ECI has no swampland prediction |
| JWST early massive galaxies (z > 10) | ECI operates on homogeneous isotropic diamonds; no coupling to halo/SF physics |
| W-mass, R(K), muon g-2 | No apparatus link; two of three anomalies resolved as of 2025–2026 |
| Dark matter direct-detection | A5 gives ΔN_eff(KK) constraint only; Bianchi VIII DM-relic route killed by T2 |
| Neutrino masses and mass ordering | No apparatus link |
| Arrow of time (independent derivation) | T3 gives algebraic correlate; Past Hypothesis still required as boundary condition |

---

## §5 Recommended reading on what ECI does not solve

- **Cosmological constant:** Weinberg (astro-ph/0005265); Bousso–Polchinski (hep-th/0004134). No algebraic-QFT paper derives the 121-order suppression.
- **Hubble tension:** Verde–Treu–Riess review (arXiv:1907.10625); EDE (Poulin et al. arXiv:1811.04083); NMC (Wolf–D'Amico–Pace arXiv:2504.07679, whose ξ_χ detection ECI Levier 1B does not reproduce).
- **Entropic gravity vs ECI algebraic NO-GO:** Bianconi (arXiv:2502.02661) proposes entropic gravity; the ECI B8 comment (in flight) is a mathematical objection, not a Λ-resolution.
- **NCG Standard Model:** Chamseddine–Connes 1997 (hep-th/9606001) generates the SM action from the spectral action, orthogonal to ECI's vacuum-state approach.
- **Selection principles and arrow of time:** Penrose (*Cycles of Time* 2010); Albert (*Time and Chance* 2000). T3 is algebraically sharper but does not replace the Past Hypothesis.
- **CLPW parent framework:** Chandrasekaran–Penington–Witten (arXiv:2206.10780); Witten (arXiv:2112.12828). These establish what the crossed-product construction can and cannot prove.
