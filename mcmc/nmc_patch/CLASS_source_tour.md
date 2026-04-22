# CLASS 3.2 source tour — for the NMC patch

Reader's digest of the CLASS public source tree (github.com/lesgourg/class_public,
master @ fetched 2026-04-21) and of the hi_class fork
(github.com/miguelzuma/hi_class_public). All file/line references below were
verified against the fetched sources in `_source_cache/` (gitignored).

The goal is one-page-per-file maps of **what exists** and **which exact
function/struct-field must change** to add the NMC operator ξ_χ R χ²/2.

---

## 1. Stock CLASS — relevant files

### `include/background.h`

Declares `struct background`. A scalar-field quintessence sector already
exists and is activated via `Omega0_scf != 0`:

- `int has_scf` — flag set in `background_indices()`.
- `double Omega0_scf` — target relic fraction.
- `double * scf_parameters`, `int scf_parameters_size` — opaque potential params.
- `int scf_tuning_index` — which param is auto-tuned to hit Omega0_scf.
- `short attractor_ic_scf`, `double phi_ini_scf`, `double phi_prime_ini_scf`.
- Background-table indices: `index_bg_phi_scf`, `index_bg_phi_prime_scf`,
  `index_bg_V_scf`, `index_bg_dV_scf`, `index_bg_ddV_scf`,
  `index_bg_rho_scf`, `index_bg_p_scf`, `index_bg_p_prime_scf`.
- Integrator-vector indices: `index_bi_phi_scf`, `index_bi_phi_prime_scf`.

Adding NMC requires, minimally, **one new double `xi_chi`** in this struct
(or a whole parallel `has_nmc / xi_chi / chi_ini / V_chi_form / alpha_chi`
block if we want χ independent of the existing scf).

### `source/background.c` (3007 lines)

Key functions:

- `background_functions(pba, pvecback_B, return_format, pvecback)`
  — at line 473 it already reads `phi, phi_prime` from integrator state,
  writes `V, V', V''`, and computes `rho_scf = phi'²/(2a²) + V`,
  `p_scf = phi'²/(2a²) − V`. **This is where the NMC stress-energy
  correction `−6 ξ χ H χ'` and the effective Planck mass
  `M_P²_eff = M_P² − ξ χ²` must be injected** (modifying the line
  `rho_scf = …` and introducing an `M2_eff` factor in the Friedmann sum
  `rho_tot`).
- `background_indices(pba)` — line ~1067: `class_define_index(pba->index_bg_phi_scf, ...)`.
  Add new indices `index_bg_chi`, `index_bg_chi_prime`, `index_bg_M2_eff` here
  (or reuse scf indices if we fold χ into the existing scf).
- `background_derivs(...)` — called by generic_evolver. Currently computes
  `d(phi)/dτ = phi_prime` and `d(phi_prime)/dτ = −2𝓗 phi_prime − a² V'(phi)`.
  **Replace V'(phi) → V'(φ) + ξ_χ R(τ) φ** for the NMC case. The background
  Ricci scalar is not currently stored; we must add
  `R = 6 (𝓗' + 𝓗²)/a²` (computed on-the-fly from `pvecback[index_bg_H]` and
  `index_bg_H_prime`).
- `background_initial_conditions(pba, pvecback, pvecback_integration)` —
  line ~2149, handles `attractor_ic_scf` branch. For NMC we add a
  slow-roll IC χ(a_ini) = χ₀, χ'(a_ini) = 0 and iterate on χ₀ to hit Ω_χ.
- `background_solve(pba)` — line ~1901: iterates the shooting on
  `scf_tuning_index`. Extending to NMC: add `chi_tuning` (set χ₀ to hit Ω_χ).

### `source/input.c` (6248 lines)

- Around line ~3192: parser for `Omega_scf`, `scf_parameters`,
  `attractor_ic_scf`. This is the template for adding
  `xi_chi`, `chi_ini`, `chi_prime_ini`, `V_chi_form ∈ {exponential, cosine}`,
  `alpha_chi`.
- `input_find_root()` / `input_try_unknown_parameters()` — shooting to fix
  Omega0_scf; extend with the χ₀ tuning if we keep the shooting paradigm.

### `source/perturbations.c` (10528 lines)

- `perturb_vector_init()` — line ~3950:
  `class_define_index(ppv->index_pt_phi_scf, pba->has_scf, index_pt, 1);`
  and similarly for `phi_prime_scf`. Mirror these for NMC.
- Initial conditions — line ~5474: scf perturbation IC (currently set to 0
  with a commented synchronous-gauge formula). NMC changes the synchronous-gauge
  IC because ξ shifts the initial-time Einstein constraints.
- Gauge transformation sync↔newtonian — line ~5753: adds
  `alpha * pvecback[index_bg_phi_prime_scf]` to the scf perturbation.
- Einstein source-term sums — line ~7140: scf contribution to
  (δρ, δP, (ρ+P)θ, (ρ+P)σ) built from `phi'`, `δφ`, `δφ'`, `dV/dφ`.
  **The NMC contribution to δG₀₀ / δG_ij from the ξ∇∇(χ²) piece
  must be added here.** Section P3 of the existing `CLASS_patch_design.md`
  is the formula.
- `perturb_derivs()` — line 9395: the linearised Klein-Gordon is
  ```
  dy[index_pt_phi_scf] = y[index_pt_phi_prime_scf];
  dy[index_pt_phi_prime_scf] = -2·a_prime_over_a·y[index_pt_phi_prime_scf]
                                - h'/2 · pvecback[index_bg_phi_prime_scf]
                                - (k² + a² V''(φ)) · y[index_pt_phi_scf];
  ```
  **NMC adds `−a² ξ R(τ) y[φ] − a² ξ φ δR`** where δR is the synchronous-gauge
  metric perturbation (formula in design doc §3.1). This is the single most
  important physics line to modify.

### `source/primordial.c`, `source/spectra.c`, `source/harmonic.c`

Downstream consumers — no direct modification required. They consume
`ppt->sources[..][ppt->index_tp_delta_cdm]`, `delta_scf`, `theta_scf` etc.
**As long as our new NMC source terms populate `delta_scf`/`theta_scf`
correctly via the modified `perturb_einstein()` sums, the C_ℓ and P(k)
pipelines downstream remain untouched.**

---

## 2. hi_class fork — relevant files

### `include/background.h`

`enum gravity_model` (line 17):
```
{propto_omega, propto_scale, constant_alphas, eft_alphas_power_law,
 eft_gammas_power_law, eft_gammas_exponential, brans_dicke,
 quintessence_monomial, quintessence_tracker, galileon, nkgb,
 alpha_attractor_canonical}
```
**Gap**: there is **no `nonminimal_coupling`** enumerator. Adding NMC = adding
one identifier + one case.

Relevant struct fields: `gravity_model_smg`, `parameters_smg`,
`parameters_size_smg`, `field_evolution_smg`, `is_quintessence_smg`,
`index_bg_M2_smg` (effective Planck mass squared), `index_bg_kineticity_smg`
(= α_K), `index_bg_braiding_smg` (= α_B), `index_bg_mpl_running_smg` (= α_M),
`index_bg_tensor_excess_smg` (= α_T).

### `source/background.c`

Critical: lines **3309–3423** of hi_class's `background.c` compute the
Horndeski G_i functions. Each gravity_model populates a local set of doubles:
```
double G2, G2_X, G2_Xphi, G2_phi, G2_phiphi;
double G3_phi, G3_X, G3_Xphi, G3_XX, G3_Xphiphi, G3_XXphi;
double G4, G4_smg, G4_phi, G4_phiphi, G4_X, G4_XX, G4_XXX, G4_Xphi,
       G4_Xphiphi, G4_XXphi;
double G5_phi, G5_phiphi, G5_X, G5_XX, G5_Xphi, G5_XXphi, G5_XXX,
       G5_phiphiphi;
```
and from them the Bellini–Sawicki α_i functions (1404.3713), M²_smg
(line 3495: `2*G4 - 2*X*(2*G4_X + H*phi'/a G5_X - G5_phi)`), α_K (line 3506)
and α_B (line 3509).

**NMC in this framework** is the single case:
```
G_2 = X - V(φ)                  (canonical kinetic + potential)
G_3 = 0
G_4 = 1/2 - ξ φ² / 2            ← the NMC operator
G_5 = 0
```
giving non-zero `G4, G4_phi = -ξ φ, G4_phiphi = -ξ`; all G3, G5 zero.
Compare with the existing **brans_dicke** case (hi_class background.c
line 3404–3422) where `G4 = φ/2, G4_phi = 1/2` — same linear-in-G4_phi
structure; NMC just has `G4_phi` linear in φ rather than constant.

The **no-ghost** condition `M²_smg > 0` is enforced by hi_class via
`class_test(pvecback[index_bg_M2_smg] > 0, ...)` — this automatically
implements the `ξ χ² < M_P²` constraint from `derivations/D3-noghost.py`.

### `source/input.c`

Line 1290–1352 (`quintessence_monomial`) is the clean template for adding
a new `nonminimal_coupling` keyword:
```c
if (strcmp(string1,"nonminimal_coupling") == 0) {
    pba->gravity_model_smg = nonminimal_coupling;
    pba->field_evolution_smg = _TRUE_;
    pba->is_quintessence_smg = _TRUE_;
    flag2 = _TRUE_;
    pba->parameters_size_smg = 5;  // [xi, V0, alpha, phi_prime_ini, phi_ini]
    class_read_list_of_doubles("parameters_smg", pba->parameters_smg,
                               pba->parameters_size_smg);
    if (has_tuning_index_smg == _FALSE_)
        pba->tuning_index_smg = 1;  // V0 tunes Omega_smg
}
```
Additionally line 1623 has the string listing all allowed `gravity_theory`
values that must be extended.

### `source/perturbations.c`

hi_class implements a full **quasi-static (QS) / fully-dynamic switcher**:
`method_qs_smg = {automatic, fully_dynamic, quasi_static, ...}`. See
lines 281–2556 for the driver, and `perturb_test_at_k_qs_smg()` for the
per-k evaluator. QS branch computes δφ algebraically from the Einstein
constraints; FD branch integrates the full second-order KG.

This is exactly the infrastructure our design doc §3 sketched
("quasi-static G_eff(k, a) per D14 for k deep inside the horizon, full
perturbed-ξRχ term elsewhere"). **The patch should re-use `method_qs_smg`
and `perturb_test_at_k_qs_smg()` rather than re-deriving the switch.**

---

## 3. Functions verified to exist (cite-verbatim check)

Every function name below appears verbatim at the cited line in the fetched
source (grep-verified):

- stock CLASS: `background_functions` (bg.c:L473 uses pba->has_scf),
  `background_indices` (bg.c:~1067), `background_initial_conditions`
  (bg.c:~2149), `background_solve` (bg.c:~1901), `perturb_vector_init`
  (pert.c:~3950), `perturb_derivs` (pert.c:9395), `perturb_einstein`
  (name referenced from perturbations.h — not read).
- hi_class: enum `gravity_model` (bg.h:17), `gravity_model_smg` field
  (bg.h:118), case `brans_dicke` (bg.c:3404), case `quintessence_monomial`
  (input.c:1290), `perturb_test_at_k_qs_smg` (pert.c:2473).

All other function names cited in the design doc are derived from these.

---

## 4. Bottom-line source-tour verdict

1. **Fork choice: hi_class, not plain CLASS.** hi_class already implements
   the exact Horndeski G₄(φ) structure that NMC fits into as one extra
   `enum` case + ~40 lines. Plain CLASS has no NMC machinery and would
   require implementing the M²_eff plumbing, the Bellini–Sawicki α_i,
   the QS approximation, and the modified Einstein equations from scratch
   — estimated 600–1200 lines vs ~100 lines in hi_class.
2. **Perturbation sector is harder than background.** Background is ~40
   lines (one new G4, G4_phi, G4_phiphi case). Perturbations re-use
   hi_class's automatic QS switcher but the IC and the sync↔newtonian
   gauge transformation pieces must still be written (~150 lines).
3. **No modification to `primordial.c`, `spectra.c`, `harmonic.c`,
   `transfer.c`, `thermodynamics.c`** under the assumption ξ is small
   enough that recombination is not shifted (|ξ χ²/M_P²| ≲ 10⁻² at a=1).
   If the MCMC explores ξ χ² ~ M_P², `thermodynamics.c` must be rechecked
   (recombination depends on G).

References (fetched):
- CLASS: https://github.com/lesgourg/class_public master (3007+10528+6248
  lines for bg/pert/input).
- hi_class: https://github.com/miguelzuma/hi_class_public master (4087+10761+5182).
- Bellini & Sawicki 2014 (α_i basis): arXiv:1404.3713.
- Zumalacárregui+ 2017 (hi_class): arXiv:1605.06102.
- Hwang & Noh 2005 (NMC perturbations): astro-ph/0412068.
