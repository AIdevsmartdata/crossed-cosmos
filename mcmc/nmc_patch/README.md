# CLASS NMC patch — status & source-file map

**Status: DESIGN DOC. No code committed here.**

This directory will eventually hold a patch against CLASS 3.2+ that adds the
non-minimal coupling term  ξ_χ R χ²/2  to the background + linear-perturbation
equations, so that the MCMC parameter `nmc_xi_chi` in `../params/eci_nmc.yaml`
actually modifies the predicted CMB / matter power spectra.

Until that patch exists and is applied to the CLASS build used by Cobaya,
**`nmc_xi_chi` is a no-op and its posterior is the prior**.

## Equations to add

See `CLASS_patch_design.md` in this directory. They are the linearised
versions of the Klein-Gordon equation and stress-energy tensor derived in
the project's `derivations/`:

- `derivations/D1-kg-nmc.py`  →  □χ − V'(χ) − ξ_χ R χ = 0
- `derivations/D2-stress-nmc.py` → T_μν^(χ) including ξ[G_μν χ² + g_μν □χ² − ∇_μ∇_ν χ²]

## CLASS source files that must be modified

| CLASS file                        | What to add                                             |
|-----------------------------------|---------------------------------------------------------|
| `include/background.h`            | new struct fields: `xi_chi`, `chi`, `chi_prime`         |
| `source/input.c`                  | parser for `nmc_xi_chi` input key                       |
| `source/background.c`             | χ background ODE with ξRχ source; effective M_P²_eff    |
| `include/perturbations.h`         | add χ perturbation δχ, δχ' to y-vector                  |
| `source/perturbations.c`          | linearised KG eq for δχ; NMC contributions to δT_μν     |
| `source/thermodynamics.c`         | (only if ξ large enough to shift recombination)         |

Typical diff size (by analogy with similar extensions): ~600–1200 lines.

## Precedent

The reference implementation is **EFTCAMB** (Hu, Raveri, Frusciante, Silvestri
2014; arXiv:1405.3590), which adds EFT-of-DE operators including the
non-minimal-coupling term Ω(a) R/2 on top of CAMB. Porting that machinery to
CLASS has been done independently in:

- **hi_class** (Zumalacárregui+ 2017, arXiv:1605.06102) — Horndeski in CLASS,
  covers NMC as the G4(φ) = M_P²/2 − ξφ²/2 special case.
- **CLASS_EDE** (Hill+ 2020, arXiv:2003.07355) — for the f_EDE sector only.

**The pragmatic path** is: start from `hi_class`, restrict the Horndeski
parameter space to pure ξχ²R NMC, and expose `xi_chi` as the single new
input. This avoids re-deriving/re-coding the perturbation equations from
scratch. Budget: ~2 weeks of focussed work.

## TODO

- [ ] Clone `hi_class` master into a sibling `class_nmc/` directory.
- [ ] Restrict input parser to a single `xi_chi` knob (hide αM, αB, αK, αT).
- [ ] Add unit test: ξ_χ = 0 must reproduce stock CLASS C_ℓ bit-for-bit.
- [ ] Add unit test: small ξ_χ = 10⁻³ must match analytic linear-response
      result from `derivations/D4-wa-w0-nmc.py`.
- [ ] Commit as `nmc_patch/class_nmc.patch` (unified diff against CLASS 3.2).
- [ ] Point `theory.classy.path` in `../params/eci_nmc.yaml` at the patched
      build.
