# BIPP closure: residual gaps + verification log

Working directory: `/tmp/agents_2026_05_03_closure_wave/G4_BIPP_plancherel/`
Date: 2026-05-03
Status: BIPP paper promoted from 5pp draft to 8-10pp submission-ready.

## 0. Deliverables

| File | Purpose |
|---|---|
| `note_updated.tex` | 8-10 pp updated note with Lemmas BIPP-1, BIPP-2, refined Theorem 3.4 |
| `sympy_bipp.py` | Plancherel rho-integral + Olver UV bound + FRW isotropic-limit sympy verification + mpmath@200dps numerics |
| `cover_letter_updated.txt` | Submission-ready cover letter (1-2 weeks polish, was 4-6 months) |
| `notes.md` | This file |

## 1. What was closed (load-bearing technical work)

### 1.1 Lemma BIPP-1: K_BI Plancherel convergence

**Statement.** For f ∈ C_c^∞(D_R), ‖K_BI[f]‖² = sum_k ∫₀^∞ ρ² dρ J_BN(k,ρ)² ‖K_BI^{(ρ,k)}[f]‖² < ∞. K_BI is essentially self-adjoint on C_c^∞(D_R).

**Proof outline (now in note_updated.tex §3.2):**
1. BN23 Schwartz-class spatial smearing: f ∈ C_c^∞(D_R) ⇒ hat f(η, vec k) ∈ S(R³) uniformly in η ∈ [η_c-R, η_c+R] (Reed-Simon I, Prop 7.1).
2. Olver UV bound on BN mode functions: T_k(t) = (2 ω_k)^{-1/2} exp(-i ∫ ω_k dt) (1 + O(k^{-1})) uniformly on compact t (BN23 §3.4 + Olver 1974).
3. Per-sector matrix element bound: ‖K_BI^{(ρ,k)}[f]‖² ≤ C(R) ρ²(1+ρ²)^{-N} |hat f(k)|² (Hislop-Longo 1982 modular spectral kernel + BN23 Hadamard property for J_BN(k,ρ) ∈ C_b).
4. Tonelli: ‖K_BI[f]‖² ≤ C(R) ‖f‖²_L² × ∫₀^∞ ρ⁴(1+ρ²)^{-N} dρ.
5. Closed-form: ∫₀^∞ ρ⁴(1+ρ²)^{-N} dρ = (1/2) B(5/2, N-5/2), finite for N > 5/2. Sympy: N=4 gives π/32 (verified to 200 dp by mpmath).
6. Essential self-adjointness: Nelson analytic-vector theorem (Reed-Simon II, Thm X.39) + C_c^∞(D_R) is a core for the BN-state KMS generator (BFV + Sahlmann-Verch 2001).

**Numerics (sympy_bipp.py Part IV, VI, VII):**
- ∫₀^∞ ρ⁴(1+ρ²)^{-4} dρ = π/32 ≈ 0.0981747... (sympy direct + Beta-function). Truncation at ρ_max=1000 gives rel err 3.4e-9.
- Test state f_test(η, vec x) = exp(-|x|²/R²) χ_{[η_c-R, η_c+R]}(η) at R=1: combined Plancherel ‖K_BI[f_test]‖² ≤ π⁵ R³ √(2π)/16 ≈ 47.94234... (mpmath@200dps).
- Spatial K-integral: ∫_{|k|<K_max} 4π k² |hat f(k)|² dk → 2 π⁴ R³ √(2π) ≈ 488.34 at K_max=10 to 18 dp.

### 1.2 Lemma BIPP-2: FRW reduction at boost-generator level

**Statement.** At a_1 = a_2 = a_3 = a (kinematic isotropic limit):
- (a) ω_k(t)² = m² + |vec k|²/a(t)² spherically symmetric (sympy-verified).
- (b) Plancherel measure ρ² J_BN(k,ρ) dρ d³k → ρ² J_FRW(|k|,ρ) dρ |k|² d|k|.
- (c) Per-sector generator K_BI^{(ρ,k)} = K_FRW^{(ρ,|k|)}.
- (d) Boost generator B_{12} = x_1 ∂_2 - x_2 ∂_1 is a Killing vector (sympy-verified: cos²θ + sin²θ = 1).
- (e) Sum over sectors: K_BI|_iso = K_FRW on C_c^∞(D_R), modulo unitary intertwiner.

**Caveat (Remark 3.5(ii) in note_updated.tex):** equality K_BI|_iso = K_FRW requires the BN-state-on-FRW to differ from the Olbermann state by a unitary that commutes with the modular flow. Existence follows from BFV local quasi-equivalence (both states Hadamard ⇒ unitarily equivalent on D_R); explicit closed form is left implicit. This is an honest residual gap — flagged explicitly in note_updated.tex Remark 3.5 and in the scope statement.

## 2. Reference verification (this round)

All references arXiv-API-verified or DOI-verified via WebFetch / WebSearch:

| Reference | Status | Resolved identifier |
|---|---|---|
| BN23 Banerjee-Niedermaier | OK (re-verified) | arXiv:2305.11388, JMP 64 (2023) 113503 |
| BFV03 Brunetti-Fredenhagen-Verch | OK (carried over) | arXiv:math-ph/0112041 |
| Witten 2022 | OK (carried over) | arXiv:2112.12828, JHEP 10 (2022) 008 |
| Connes 1973 | OK (carried over) | ASENS 6, DOI:10.24033/asens.1247 |
| Olbermann 2007 | OK (carried over) | arXiv:0704.2986 |
| Hislop-Longo 1982 | **NEW + VERIFIED** | CMP 84:71-85, DOI:10.1007/BF01208372 |
| Frob 2023 | **NEW + VERIFIED** | arXiv:2308.14797, JHEP 12 (2023) 074 |
| Sahlmann-Verch 2001 | **NEW + VERIFIED** | arXiv:math-ph/0008029, RMP 13:1203-1246 |
| Olver 1974 (book) | NEW (textbook, no arXiv) | Asymptotics and Special Functions, AP 1974, AKP reprint 1997 |
| Reed-Simon I, II | NEW (textbook, no arXiv) | Methods of Modern Math Phys, AP 1980/1975 |

**No hallucinations introduced this round.** F4's prior catches (Marcolli-van Suijlekom 1301.3480 not 1405.7860; SLE = States of Low Energy not Schramm-Loewner) preserved.

## 3. Sympy + mpmath verification log

`sympy_bipp.py` performs nine blocks of symbolic + numerical checks:

- **[Part I]** Build ω_k²(t) = m² + Σ k_i²/t^{2 p_i}, isotropic limit
  ω_k iso = m² + |k|²/t^{2 p_1}. **Verified.**
- **[Part II]** Olver-WKB leading: T_k(t) ~ (2 ω_k)^{-1/2} exp(-i ∫ ω_k dt), remainder O(k^{-1}). **Documented (BN23 §3.4 + Olver 1974).**
- **[Part III]** Plancherel measure dμ_BN(ρ, k) = ρ² J_BN(k,ρ) dρ d³k structure.
- **[Part IV]** ∫₀^∞ ρ⁴(1+ρ²)^{-4} dρ = π/32 = (1/2) B(5/2, 3/2). Sympy direct and Beta-function evaluations agree exactly. **Verified.**
- **[Part V]** Isotropic limit ω_k² spherical symmetric (diff = 0); SO(3)-rotation Killing (cos²+sin²=1); spatial 1D Fourier of exp(-x²/R²) = R √π exp(-R² k₁²/4); 3D tensoring gives spherically symmetric hat ψ. **Verified.**
- **[Part VI]** mpmath@200dps Plancherel rho-truncation: rho_max=1000 ⇒ rel err 3.4e-9. **Verified.**
- **[Part VII]** mpmath@200dps K-integral truncation: K_max=10 ⇒ matches 2 π⁴ R³ √(2π) to 18 dp. **Verified.**
- **[Part VIII]** FRW limit numerical match: S_BI = S_FRW = π⁵ R³ √(2π)/16 at Olver-leading order. **Verified.**

## 4. Residual mathematical gaps (after BIPP-1 + BIPP-2 closure)

### 4.1 BN-on-FRW vs Olbermann unitary intertwiner — IMPLICIT
The equality K_BI|_iso = K_FRW in Lemma BIPP-2(e) is up to a unitary
intertwiner U: H_BN-on-FRW → H_Olbermann that commutes with the modular
flow. Existence follows from BFV local quasi-equivalence (both states are
Hadamard, hence unitarily equivalent on the local diamond algebra). The
explicit closed form of U is NOT computed — it would require extending
BN23 §3.4 asymptotic to the conformal-vacuum boundary. **Flagged
explicitly in note_updated.tex Remark 3.5(ii) and §6.1.**

### 4.2 Non-perturbative vs perturbative trade-off
BIPP is non-perturbative (any Kasner, not only near-FRW), at the cost of
an implicit (Plancherel) rather than explicit (boost) modular Hamiltonian.
Connes 1973 cocycle Radon-Nikodym (D ω_BN : D ω_Mink)_t provides the
intertwiner for the perturbative regime ε_0 ≲ 10⁻⁵. **Now mentioned in
note_updated.tex §6.2.**

### 4.3 De Sitter cross-check — NOT carried out in detail
Frob 2023 (arXiv:2308.14797) computes K explicitly for de Sitter
diamonds. BIPP is consistent in the limit a_i(t) → e^{Ht}. We did NOT
carry out the explicit identification of spectral parameters. **Flagged
in note_updated.tex §6.5 as a sanity check available to the reader.**

### 4.4 Backreaction / BKL — out of scope
Free-field semiclassical Einstein equations drive BI → FRW (BKL-style).
Invisible to type classification, matters for entropy interpretation.
Same caveat as before.

## 5. What is NOT claimed (preserved from F4)

- **Not claimed:** SM derivation from ECI.
- **Not claimed:** cosmological constant from NCG.
- **Not claimed:** TOE-style unification of NCG + ECI.
- **Not claimed:** Lemma 3.3 extends to Bianchi-I (the opposite is shown,
  Lemma 4.2 / Cor 4.3 of note_updated.tex).
- **Not claimed:** the BN-state is the unique reference; it is one
  Hadamard-state choice.
- **Not claimed:** explicit closed form of the unitary intertwiner
  U: H_BN-on-FRW → H_Olbermann (exists by BFV but not computed).

## 6. Time-to-pub after closure

- **Before this round (F4 deliverable):** 4-6 months.
- **After this round (G4 closure):** 1-2 weeks editorial polish, 8-12 weeks referee + revisions, 3-4 months to acceptance.

The two named technical lemmas (BIPP-1 Plancherel convergence, BIPP-2 FRW
reduction at boost-generator level) were the gating items. Both are now
proven (BIPP-1 fully, BIPP-2 modulo BFV-implicit unitary intertwiner,
flagged honestly).

## 7. LaTeX compilation status

`pdflatex` not available in this sandbox (same as F4 round). The
`note_updated.tex` source uses only standard packages (amsmath, amsthm,
amssymb, mathtools, geometry, hyperref, cite). It should compile
cleanly on any TeX Live distribution. Sources of potential warnings:
- `\'E` accented characters in the bibliography ("Éc. Norm. Sup."): UTF-8 input, T1 font encoding — should be fine.
- No figures, no exotic packages, no custom fonts.

## 8. Cross-paper consistency

The companion FRW paper `paper/frw_typeII_note/` provides Theorem 3.5
(K_FRW Plancherel form). This BIPP paper extends it; the two should be
read together. Lemma BIPP-2(c) refers explicitly to
`\cite[Thm.~3.5]{ECI-FRW-note}`; the cross-reference is consistent with
the FRW paper as it stands.
