# Levier #1B — 10-param NMC+w0wa joint fit, no EDE, no c'_DD

**Status as of 2026-05-02:** drafted, not yet launched. AxiCLASS shooting bug (post-FP-patch, unrelated to F6) blocks the full Levier #1 12-param. This 10-param subset is an intermediate that does NOT depend on AxiCLASS.

## What this is

A reproduction-and-extension of Wolf et al. 2025 PRL (arXiv:2504.07679, "Assessing cosmological evidence for non-minimal coupling", `log B = 7.34 ± 0.6` for NMC vs ΛCDM on Planck PR4 + DR2 BAO + Pantheon+) with:
- Same NMC plugin (`eci_nmc_theory.ECINMCTheory`) used in v5/v50plusS8
- Same theory backend (vanilla CLASS 3.3.4)
- Planck 2018 plik TTTEEE+lowl+lensing (Planck PR4 NPIPE not yet wired in this YAML; CMB constraint on ξ_χ should be similar)
- Plus KiDS-1000 S₈ Gaussian prior (the v50plusS8 ablation showed this tightens H_0/w_0/w_a but doesn't constrain ξ_χ on its own)
- Cassini wall ON: |ξ_χ|·(χ_0/M_P)² < 6·10⁻⁶ (Bertotti-Iess-Tortora 2003 bound, χ_0/M_P = 0.1 fiducial)

10 sampled parameters: H_0, ω_b, ω_cdm, n_s, ln(10¹⁰A_s), τ_reio, w_0_fld, w_a_fld, ξ_χ, χ_initial.

## What this is NOT

- No EDE (f_EDE, log10z_c, θ_i): AxiCLASS shooting failures (`fzero_Newton` singular matrix) block the EDE parameterisation on Zen 3 even after the FP boundary-check tolerance fix. The EDE shooting bug is a separate issue that needs deeper AxiCLASS / Newton-solver investigation. Documented in `scripts/vastai/axiclass-fp-fix-README.md` "What this does NOT fix".
- No c'_DD (Dark Dimension): the eci_nmc_theory plugin does not currently couple `c'_DD` to `N_ur` (the N_eff freeze-in calculation N4 in the triage doc is the proper treatment). Including c'_DD as a sampled parameter without modeling its physical effect would only test the ACT DR6 likelihood penalty, which is not informative.

## Launch

```bash
# On Vast.ai instance, in /root/crossed-cosmos
# 1. install Planck data if not already present
cobaya-install planck_2018_lowl.TT planck_2018_lowl.EE planck_2018_highl_plik.TTTEEE planck_2018_lensing -p mcmc/packages

# 2. launch
bash scripts/vastai/launch-mcmc.sh \
    mcmc/chains/eci_levier1B_run1/eci_levier1B.yaml \
    --packages-path mcmc/packages
```

## Walltime + cost

Planck adds the full lensed CMB power spectrum (~2700 multipoles), pushing CLASS from ~4 calls/sec down to ~0.4-0.7 calls/sec. With 4 chains × 32 OMP threads on EPYC 7V13 (Vast.ai contract 36023758, $0.42/h):
- Validation (4 × 5k samples): ~3-5 hours, $1-2
- Production (Rminus1 < 0.02, ~10k samples per chain): ~6-12 hours, $2.5-5

## Discriminator decision tree

After the run converges:

| Outcome | Interpretation | Next step |
|---|---|---|
| `ξ_χ ≠ 0 at ≥2σ` AND H_0 retreats AND S_8 retreats | Independent reproduction + KiDS extension of Wolf 2025 | PRD letter draft |
| Only H_0 retreats (S_8 doesn't, or ξ_χ inconclusive) | Standard EDE-or-DM regime expected | Carry KiDS prior into v8-bis; consider switching to a different observational stack |
| Neither tension reduced AND ξ_χ consistent with zero | NMC alone + Planck + KiDS doesn't help | Confirms motivation for full Levier #1 with EDE; renew effort on AxiCLASS shooting fix |

## Files

- `mcmc/chains/eci_levier1B_run1/eci_levier1B.yaml` — the YAML
- `mcmc/cobaya_nmc/eci_kids_s8.py` — KiDS likelihood + Cassini wall + (unused) ACT penalty
- `mcmc/cobaya_nmc/eci_nmc_theory.py` — NMC theory plugin
- `notes/posterior_v50plusS8_vs_v5_2026-05-02.md` — ablation that motivated this run
- `scripts/vastai/launch-mcmc.sh` — Docker-friendly mpirun wrapper
- `scripts/vastai/axiclass-fp-fix-README.md` — why we're not on AxiCLASS yet (EDE blocker)
