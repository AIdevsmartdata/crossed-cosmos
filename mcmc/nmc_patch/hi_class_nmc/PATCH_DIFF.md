# NMC patch — human-readable diff

**Base**: hi_class_public upstream commit `50f447c` (Merge PR #15).
**Raw unified diff**: `PATCH_DIFF.diff` (195 lines, 2 files touched,
139 insertions, 2 deletions).

The modernized hi_class modularizes all modified-gravity code into
`gravity_smg/`. The `source/background.c` edits mentioned in the
original `NMC_patch_design.md` therefore landed in
`gravity_smg/gravity_models_smg.c` instead. `input_smg.c` does not
need a touch because the Horndeski parser lives in
`gravity_models_smg.c::gravity_models_gravity_properties_smg()`.

## 1. `include/background.h`

### 1a. Add `nonminimal_coupling` to the gravity-model enum (line 24)

Before (line 27–31):
```c
    galileon, nkgb,
    brans_dicke,
    quintessence_monomial, quintessence_tracker,
    alpha_attractor_canonical
};
```

After:
```c
    galileon, nkgb,
    brans_dicke,
    quintessence_monomial, quintessence_tracker,
    alpha_attractor_canonical,
    nonminimal_coupling
};

/** Potential form for the nonminimal_coupling (NMC) model. */
enum nmc_potential_form {nmc_V_monomial, nmc_V_exponential, nmc_V_cosine};
```

### 1b. Add `V_chi_form` field to `struct background` (around line 158)

Before:
```c
  enum gravity_model gravity_model_smg; /** Horndeski model */
  //   enum gravity_model_subclass gravity_submodel_smg;
  enum expansion_model expansion_model_smg;

  short initial_conditions_set_smg;
```

After:
```c
  enum gravity_model gravity_model_smg;
  //   enum gravity_model_subclass gravity_submodel_smg;
  enum expansion_model expansion_model_smg;
  enum nmc_potential_form V_chi_form; /**< potential form for NMC */

  short initial_conditions_set_smg;
```

## 2. `gravity_smg/gravity_models_smg.c`

### 2a. Parser block (inserted before `class_test(flag2==_FALSE_, …)` at line 490)

New ~60-line block — reads `parameters_smg` (5 entries) and the
optional `V_chi_form` keyword (`monomial` default, `exponential`, `cosine`),
sets `tuning_index_smg = 2` (V0) and the monomial tuning guess so that
at xi=0 the shooting problem is *identical* to quintessence_monomial.

The error-string at the subsequent `class_test` also gets
`'nonminimal_coupling'` appended to its list.

### 2b. Horndeski G_i case in `gravity_models_get_Gs_smg` (inserted before `return _SUCCESS_;` at line 773)

```c
else if (pba->gravity_model_smg == nonminimal_coupling) {
    double xi = pba->parameters_smg[0];
    double N  = pba->parameters_smg[1];
    double V0 = pba->parameters_smg[2];
    double V, V_phi, V_phiphi;
    double Hunits2 = pow(pba->H0/pba->h, 2.);

    if (pba->V_chi_form == nmc_V_monomial) {
        V        = V0 * Hunits2 * pow(phi, N);
        V_phi    = N * V0 * Hunits2 * pow(phi, N-1.);
        V_phiphi = N*(N-1.) * V0 * Hunits2 * pow(phi, N-2.);
    } else if (pba->V_chi_form == nmc_V_exponential) {
        V        = V0 * Hunits2 * exp(-N*phi);
        V_phi    = -N * V;
        V_phiphi =  N*N * V;
    } else { /* cosine */
        V        = V0 * Hunits2 * (1. + cos(N*phi));
        V_phi    = -V0 * Hunits2 * N * sin(N*phi);
        V_phiphi = -V0 * Hunits2 * N*N * cos(N*phi);
    }

    pgf->G2        = X - V;
    pgf->G2_X      = 1.;
    pgf->G2_phi    = -V_phi;
    pgf->G2_phiphi = -V_phiphi;

    /* G4 = 1/2 - xi phi^2 / 2 */
    pgf->DG4       = -0.5 * xi * phi * phi;
    pgf->G4        =  0.5 + pgf->DG4;
    pgf->G4_phi    = -xi * phi;
    pgf->G4_phiphi = -xi;
}
```

This is the physics heart of the patch. hi_class's existing
Horndeski machinery computes `M2_smg = 2 G4 = 1 - xi phi^2`,
alpha_B, alpha_M and the full perturbation coefficients from
these G_i's automatically.

### 2c. Initial-condition case in `gravity_models_initial_conditions_smg`
(inserted between `brans_dicke` and `nkgb`, around line 1214)

```c
case nonminimal_coupling:
    /* Match quintessence_monomial IC mapping */
    pvecback_integration[pba->index_bi_phi_smg] = pba->parameters_smg[4];
    pvecback_integration[pba->index_bi_phi_prime_smg] =
        pba->parameters_smg[3] * pba->H0;
    break;
```

### 2d. Diagnostic printout (after `case nkgb:` at line 1378)

```c
case nonminimal_coupling:
    printf("Modified gravity: nonminimal_coupling (xi R chi^2/2) ...\n");
    printf(" -> xi = %g, N/alpha = %g, V0 = %g, V0* = %g, "
           "phi_prime_ini = %g, phi_ini = %g, V_form=%d \n",
           pba->parameters_smg[0], pba->parameters_smg[1],
           pba->parameters_smg[2],
           pba->parameters_smg[2]*pow(pba->H0/pba->h,2),
           pba->parameters_smg[3], pba->parameters_smg[4],
           (int) pba->V_chi_form);
    break;
```

## Summary
| File                                  | + lines | - lines |
|---------------------------------------|---------|---------|
| `include/background.h`                | 6       | 1       |
| `gravity_smg/gravity_models_smg.c`    | 133     | 1       |
| **Total**                             | **139** | **2**   |

Falls under the 270-line design-doc budget because the code
reuses the existing Horndeski machinery for Euler–Lagrange
integration, M2_smg / alpha_i computation, perturbations, and
tuning/shooting.

## Not yet implemented (tracked in `learning_log.md`)
- Explicit `xi phi^2 < 1e-6` weak-coupling assert for the
  initial conditions (design §B.3).
- `G_eff(z, k)` output column (design §D) — hi_class already
  exports alpha_B, alpha_M, M2_smg; post-processing can derive
  G_eff externally.
- Tests E.2 (small-xi analytic match) and E.3 (xi = 0.1 sanity).
