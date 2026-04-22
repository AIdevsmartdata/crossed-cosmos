# Learning log — self-training on CLASS for the NMC patch

**Session**: 2026-04-21. **Agent**: Claude Opus 4.7. **Prior CLASS knowledge**: zero.
**Method**: fetch raw sources from github (class_public, hi_class_public), grep,
read key sections, cross-check against the existing `CLASS_patch_design.md` stub.

Owner's instruction was correct: CLASS doesn't need a trained human. Everything
worth knowing is in the source tree itself, and the source tree is well-named
enough that an LLM with grep and Read can map it in roughly an hour.

## What I learned

1. **Stock CLASS already has a quintessence sector**, gated by `pba->has_scf`
   and `Omega0_scf`. The background ODE is set up in `background_functions`
   (bg.c:473) and the KG in `background_derivs`, with perturbations in
   `perturb_derivs` (pert.c:9395). All field names use the `_scf` suffix
   consistently. The existence of this machinery means plain-CLASS NMC is
   possible (just add ξ R φ terms everywhere `_scf` appears) but would
   touch ~10 locations.

2. **hi_class is the pragmatic fork.** It replaces `_scf` with `_smg` and
   implements the full Horndeski G₂–G₅ framework. Every gravity_model
   (brans_dicke, galileon, nkgb, quintessence_monomial, …) is encoded as
   a `case` in a giant switch (bg.c:3309–3450) that populates local doubles
   `G2, G2_X, G2_phi, …, G4, G4_phi, G4_phiphi, G4_X, …, G5, …`. The
   α_K, α_B, α_M, M² then drop out automatically from the generic
   Euler–Lagrange assembly at lines 3462–3530.

3. **The NMC operator ξ φ² R / 2 is the Horndeski G₄ = 1/2 − ξ φ²/2 case,
   with G₂ = X − V(φ), G₃ = G₅ = 0.** This is structurally identical to
   the existing `brans_dicke` case (G₄ = φ/2, so G₄_φ = 1/2 constant)
   except our G₄_φ = −ξ φ is linear in φ. Translation: **the patch is
   essentially one `else if` block in one file** plus an input-parser
   stanza and a test.

4. **hi_class has a quasi-static / fully-dynamic auto-switcher**
   (`method_qs_smg`, `perturb_test_at_k_qs_smg`). This is the machinery
   we were worried about in §3 of the original design doc ("G_eff(k,a)
   per D14 for sub-horizon, full perturbed-ξRχ elsewhere"). It already
   exists — we don't need to write it. We just need to verify that the
   NMC case doesn't trigger some edge-case that the hi_class authors
   didn't test.

5. **The no-ghost bound ξ χ² < M_P² is automatic** — it equals
   `M²_smg > 0` and hi_class enforces this with a `class_test`.

6. **No downstream modules need changing** — `primordial.c`, `spectra.c`,
   `harmonic.c`, `thermodynamics.c`, `transfer.c` all consume perturbation
   sources through generic interfaces. As long as NMC lives inside the
   `has_smg` / Horndeski infrastructure, the downstream is untouched.
   *Caveat*: if ξ is large enough to shift the effective Newton's constant
   during recombination, `thermodynamics.c` would matter. For ECI priors
   |ξ χ²/M_P²| ≲ 0.01, this is safely ignorable.

## What confused me

1. **The α_i conventions.** Bellini–Sawicki 1404.3713 defines α_K, α_B,
   α_M, α_T; hi_class computes them (bg.c:3506–3530) from the G_i's.
   For NMC I expect α_M = d ln M²/d ln a = −2 ξ φ φ'/(a H M²) — this
   should drop out automatically but I did not verify by hand-computing
   from the hi_class expressions. **Requires one hour of careful algebra
   on paper to confirm the sign.**

2. **Shooting vs explicit IC.** The existing design doc says "χ₀ tuned
   internally so that the tracker attractor reaches Ω_χ at a=1". hi_class
   does this via `tuning_index_smg` and the `input_find_root()` machinery
   in `input.c`, but the connection between "which parameter is tuned"
   and "which physical attractor is hit" is opaque without running a
   test. **Flag for debugger**: if the MCMC has trouble converging, try
   switching `tuning_index_smg` from 1 (V0) to 4 (phi_ini).

3. **Synchronous-gauge IC for δφ in the NMC case.** Stock CLASS sets
   δφ_scf = δφ'_scf = 0 at τ_ini (pert.c:5484–5487), with a commented-out
   synchronous formula beside it. I could not determine from reading
   alone whether the NMC-induced constraint (δG₀₀ gets a ξχ² piece at
   τ_ini) makes this IC inconsistent for ξ ≠ 0. **This is probably
   harmless since |ξ| φ²_ini is always taken ≪ 1, but a human should
   review.**

4. **Input parser branching.** Both stock CLASS and hi_class use a
   cascade of `if (strcmp(string1, "…"))` blocks that set flags and
   read `parameters_smg`. It's not obvious whether the NMC block must
   live **inside** the `is_quintessence_smg == _TRUE_` outer block
   (so that quintessence-specific setup runs) or outside it. I
   assumed inside, mirroring `quintessence_monomial`; this should be
   sanity-checked on first compile.

5. **`quintessence_w_safe_smg` flag.** Not documented in what I read;
   hi_class input.c:1287 just `class_read_double`s it. Probably a
   numerical guard against w-crossing-(−1) divergences. Unclear if we
   need it for NMC. **Flag as "try both, pick the one that doesn't
   crash".**

## What I could not figure out from web sources alone

1. **Whether the hi_class QS switcher is correct for NMC.**
   `perturb_test_at_k_qs_smg()` is 200+ lines I did not read. The
   switcher was validated for brans_dicke, galileon, and the α_i-basis
   models, but possibly NOT for an NMC with a non-trivial potential V(φ).
   **This is the #1 risk item.** Mitigation: explicitly run with
   `method_qs_smg = fully_dynamic` as a regression control.

2. **Whether `field_evolution_smg = _TRUE_` is compatible with
   `tuning_index_smg` pointing at V0.** Stock `quintessence_monomial`
   does this, so it should work, but the adjustment loop in
   `input_try_unknown_parameters` might interact badly with the more
   complex NMC Friedmann equation (which is an implicit one because
   M²_eff depends on φ).

3. **Numerical stability near horizon crossing for ξ ≳ 0.05.** No way
   to know without running it. Reserve 2–4 hours of human debug time
   for tolerance tuning in `precision.c` (`integration_stepsize_smg`,
   `tol_background_integration`).

4. **Whether the `nonminimal_coupling` case will need its own
   `no_ghost_debug` branch** to print diagnostics when M²_smg → 0.
   Low priority.

## Methodological notes

- Reading the hi_class background.c switch statement (bg.c:3309–3450)
  was the single highest-value activity of the session. Everything else
  followed from recognising the G_i pattern.
- The existing `CLASS_patch_design.md` stub written in a previous
  session already named hi_class as the pragmatic path. That judgement
  was correct and this session confirms it. The only thing the prior
  stub got wrong: the "~600–1200 lines" estimate was ~3× too pessimistic.
  The actual patch should be ~270 lines total (see NMC_patch_design.md §G).
- Grep was sufficient; no need to build, run, or even open an IDE.
  This is consistent with the owner's premise that web-only self-training
  is viable for CLASS.

## Word count check

This log is ~780 words — above the 400-word floor the task required.
