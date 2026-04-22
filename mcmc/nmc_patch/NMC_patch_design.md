# NMC patch design — concrete implementation plan

**Target fork**: hi_class (github.com/miguelzuma/hi_class_public, master).
**Rationale**: hi_class already implements the Horndeski G₂…G₅ framework
that embeds ξ_χ R χ²/2 as the single case G₄ = 1/2 − ξφ²/2. See
`CLASS_source_tour.md` §2. The patch is ~100 lines of C plus ~50 lines of
input parsing + documentation.

This document is **novice-ready at the function-and-line level**: an agent
(or human) who has never read CLASS before can follow it as a checklist.

---

## Section A — Background module

### A.1 New enumerator

`include/background.h` line 17 (verbatim enum contents):
```
enum gravity_model {propto_omega, propto_scale,
    constant_alphas, eft_alphas_power_law,
    eft_gammas_power_law, eft_gammas_exponential,
    brans_dicke,
    quintessence_monomial, quintessence_tracker,
    galileon, nkgb,
    alpha_attractor_canonical,
    nonminimal_coupling                           /* ← ADD */
};
```

### A.2 New background-table indices

Keep using hi_class's `index_bg_phi_smg`, `index_bg_phi_prime_smg`,
`index_bg_M2_smg`, etc. — do NOT add parallel `_chi` indices. χ is
identified with φ_smg. This keeps the patch minimal.

### A.3 Horndeski coefficients for NMC — the one new case in
`source/background.c` (insert after the `brans_dicke` block at line 3422):

```c
else if (pba->gravity_model_smg == nonminimal_coupling) {

    /* Action: S = ∫ d⁴x √(-g) [ (M_P² − ξ φ²)/2 · R + ½ (∂φ)² − V(φ) ]
       ECI axiom A4, with M_P ≡ 1 in CLASS internal units.
       Parameters:
         parameters_smg[0] = xi_chi     (dimensionless, can be ± )
         parameters_smg[1] = V0         (potential amplitude, H0² units)
         parameters_smg[2] = alpha_chi  (potential shape parameter)
         parameters_smg[3] = phi_prime_ini
         parameters_smg[4] = phi_ini
         pba->V_chi_form   = exponential | cosine   (new enum, see §C)
    */
    double xi      = pba->parameters_smg[0];
    double V0      = pba->parameters_smg[1];
    double alpha   = pba->parameters_smg[2];

    /* Potential */
    double V, V_phi, V_phiphi;
    if (pba->V_chi_form == V_exponential) {
        V        =  V0 * exp(-alpha * phi);
        V_phi    = -alpha * V;
        V_phiphi =  alpha * alpha * V;
    } else { /* V_cosine:  V0 * (1 + cos(alpha φ)) */
        V        =  V0 * (1. + cos(alpha*phi));
        V_phi    = -V0 * alpha * sin(alpha*phi);
        V_phiphi = -V0 * alpha*alpha * cos(alpha*phi);
    }

    /* G_2 = X - V(φ)   (canonical kinetic + V) */
    G2       =  X - V;
    G2_X     =  1.;
    G2_phi   = -V_phi;
    G2_phiphi= -V_phiphi;

    /* G_3 = 0 */
    /* G_5 = 0 */

    /* G_4 = 1/2 - ξ φ²/2   (NMC term) */
    G4_smg     = -0.5 * xi * phi * phi;
    G4         =  0.5 + G4_smg;
    G4_phi     = -xi * phi;
    G4_phiphi  = -xi;
    /* G4_X = G4_XX = … = 0 (no X-dependence in G4) */
}
```

Once these G_i's are populated, hi_class's existing machinery
(lines 3462–3530) computes `M2_smg = 2·G4 + …`, α_K, α_B, α_M automatically.

For the NMC case:
- `M2_smg = 2·G4 = 1 − ξ φ²` ✓ matches derivation D3.
- `α_B = −2 H⁻¹ φ'/a · G4_phi / M²_smg = 2 ξ φ φ'/(a H (1−ξφ²))` ✓
- `α_M = (dM²/d ln a)/M² = −2ξ φ φ'/[aH(1−ξφ²)]` ✓
- `α_K = 2X / M² · G2_X / something` (canonical kinetic limit).
- `α_T = 0` (no disformal piece, so tensor speed = c). Required by
  GW170817; automatic.

### A.4 Klein-Gordon evolution

hi_class's `background_derivs()` already integrates the full Horndeski
KG equation derived from the Euler–Lagrange of `G2 + G3 + G4 + G5`. For
our NMC case with G_3 = G_5 = 0, the background KG reduces to:
```
φ'' + 2𝓗 φ' + a² V'(φ) + a² ξ R φ = 0
R = 6(𝓗' + 𝓗²)/a²
```
(Design §2.2 in the existing CLASS_patch_design.md.) **No new ODE code
needed** — hi_class's existing Euler–Lagrange solver handles it once
G4_phi = −ξφ is non-zero.

### A.5 Initial conditions and shooting

Extend `background_initial_conditions()` (hi_class bg.c:~2267):
- New branch for `nonminimal_coupling`: φ_ini = parameters_smg[4],
  φ'_ini = parameters_smg[3] · a_ini · H0.
- Shooting via existing `tuning_index_smg`: default `tuning_index_smg = 1`
  (V0 adjusts to hit Omega0_smg). Same template as `quintessence_monomial`
  (input.c:1332).

---

## Section B — Perturbation module

### B.1 Re-use the existing hi_class perturbation code

hi_class implements the **full linearised Horndeski perturbation** for any
gravity_model. The δφ_smg EOM in `perturb_derivs()` already includes the
G4_phi, G4_phiphi contributions. **So for NMC we write ZERO new lines in
the core ODE.** We only need to verify (regression test §E) that the
existing code compiles and runs for the new `nonminimal_coupling` case.

### B.2 Quasi-static approximation

hi_class's `perturb_test_at_k_qs_smg()` (pert.c:2473) decides per mode
whether to use QS or fully-dynamic. For NMC with small ξ (ξ ~ 10⁻³–10⁻¹),
QS is valid for k > a H (sub-horizon). The effective Newton constant is
```
G_eff(k, a)/G_N = (1 + α_T) / M²_smg · [ 1 + (α_B + α_M)² · k²/(… k² terms) ]
```
— exactly the D14 formula from derivation `D4-wa-w0-nmc.py`. hi_class
computes this internally; we just expose it via new output column
`G_eff_smg` (see §D).

### B.3 Initial conditions for δφ_smg

Currently set to 0 in synchronous gauge (CLASS convention). For NMC this
is fine as long as ξ φ²_ini ≪ 1 (weak-coupling IC). **Add a runtime
`class_test`** that φ_ini² · |ξ| < 10⁻⁶ at a_ini, otherwise fall back
to attractor IC. (New ~5 lines in `background_initial_conditions`.)

---

## Section C — Input parser

### C.1 New `.ini` keys

In `source/input.c`, after the `quintessence_monomial` block
(hi_class input.c:1352):

```c
if (strcmp(string1,"nonminimal_coupling") == 0) {
    pba->gravity_model_smg = nonminimal_coupling;
    pba->field_evolution_smg = _TRUE_;
    pba->is_quintessence_smg = _TRUE_;
    flag2 = _TRUE_;

    pba->parameters_size_smg = 5;
    class_read_list_of_doubles("parameters_smg",
                               pba->parameters_smg,
                               pba->parameters_size_smg);

    /* Potential form */
    class_call(parser_read_string(pfc, "V_chi_form", &string2, &flag3,
                                  errmsg), errmsg, errmsg);
    if ((flag3 == _TRUE_) && (strstr(string2,"cosine") != NULL))
        pba->V_chi_form = V_cosine;
    else
        pba->V_chi_form = V_exponential;  /* default */

    if (has_tuning_index_smg == _FALSE_)
        pba->tuning_index_smg = 1;  /* tune V0 to hit Omega0_smg */
}
```

Also extend the error message at line 1623 to mention `nonminimal_coupling`.

### C.2 Convenience aliases

The project-level `.ini`/Cobaya YAML can expose friendlier names that the
harness maps to `parameters_smg`:
```
gravity_model = nonminimal_coupling
xi_chi        = 0.01              → parameters_smg[0]
V0_chi        = 1e-4              → parameters_smg[1]
alpha_chi     = 0.5               → parameters_smg[2]
chi_prime_ini = 0                 → parameters_smg[3]
chi_ini       = 0.1               → parameters_smg[4]
V_chi_form    = exponential
```

---

## Section D — Output hooks

Add new columns to CLASS's background and perturbations output files
(so MontePython / Cobaya likelihoods can consume them without a custom
likelihood code):

- `source/background.c` → add `class_store_columntitle` entries for
  `M2_eff`, `xi_chi_Rchi2` (the action-density diagnostic),
  `w_eff(z)`, `H(z)` (already exported).
- `source/perturbations.c` → add `G_eff(z, k)/G_N` and `η(z, k) = Φ/Ψ`
  (anisotropic stress slip). hi_class exports `M2_smg`, `alpha_M`, `alpha_B`
  but **not the scalar-sector G_eff as a single number**. Add ~30 lines
  to compute it from the existing α_i and export.

---

## Section E — Regression tests

Two required tests, both in `test/` as new `test_nmc_*.c` harnesses
invoking `class` on a generated `.ini`:

### E.1 ξ = 0 must reduce to vanilla quintessence

Compare CLASS run with
```
gravity_model = nonminimal_coupling
parameters_smg = 0.0, 1e-4, 0.5, 0., 0.1
```
vs CLASS run with
```
gravity_model = quintessence_monomial
parameters_smg = 1, 1e-4, 0., 0.1
```
Pass criterion:
- `|H(z) − H_ref(z)| / H_ref(z) < 1e-4` for z ∈ [0, 3000] (100-point grid).
- `|C_ℓ^TT − C_ℓ^TT,ref| / C_ℓ^TT,ref < 1e-4` for ℓ ∈ [2, 2500].
- `|P(k)/P_ref(k) − 1| < 1e-4` for k ∈ [1e-4, 1] h/Mpc.

### E.2 Small ξ = 10⁻³ must match analytic linear-response

Use the analytic `D4-wa-w0-nmc.py` result for (w₀, w_a) as a function of ξ.
For ξ = 10⁻³ expect Δw₀ = −2.1 × 10⁻⁴, Δw_a = +4.8 × 10⁻⁴ (derivation D4).
Pass criterion: CLASS-reconstructed w(z) at z ∈ {0, 0.5, 1.0, 2.0} matches
the analytic (w₀ + w_a z/(1+z)) form to 5 × 10⁻⁵.

### E.3 ξ large (= 0.1) sanity

No analytic reference — run and check `M²_smg > 0` at all a (no-ghost),
`C_ℓ^TT` smooth (no acoustic-scale discontinuity from the numerical
integration), and `G_eff(z=0, k=0.1 h/Mpc)/G_N ∈ [0.95, 1.05]`.

---

## Section F — Build & integration

- Apply as a unified diff `nmc_patch.diff` against hi_class commit
  pinned in `mcmc/nmc_patch/HI_CLASS_COMMIT` (to be filled when we pick
  a version).
- Compile with `make class` inside hi_class root. Output: `class` binary
  and `classy` python wrapper.
- Point `theory.classy.path` in `mcmc/params/eci_nmc.yaml` at the patched
  build.

---

## Section G — Explicit expected diff stats

| File                   | Lines added | Lines modified |
|------------------------|-------------|----------------|
| include/background.h   | 3           | 1 (enum)       |
| source/background.c    | ~50         | ~5             |
| source/input.c         | ~30         | 2              |
| source/perturbations.c | ~30 (output only) | 0        |
| test/test_nmc_zeta0.c  | ~80 (new)   | 0              |
| test/test_nmc_small.c  | ~80 (new)   | 0              |
| **Total**              | **~270**    | **~8**         |

Compare with the README.md's prior estimate of "600–1200 lines" — the
actual cost is lower because hi_class's G_i framework absorbs most of
the physics.

---

## Section H — Items requiring human verification

1. Sign convention: CLASS internal uses `metric signature = (−,+,+,+)` and
   `φ` dimensionless. Must verify that our ξ has the same sign as in
   `derivations/D1-kg-nmc.py` (the derivation uses M_P explicit).
2. `perturb_test_at_k_qs_smg()` returns `qs_smg_fd_0..fd_3` states — must
   manually verify the NMC case selects the correct FD state at early
   times (radiation domination).
3. hi_class's `quintessence_w_safe_smg` flag — unclear whether it applies
   to NMC (protects against w → −1 crossing divergences). Run a test with
   it on/off.
