# C4 — Joint MCMC across 10 cosmological models on Planck PR4 + DESI DR2 + ...

**Goal.** Bayesian model comparison ECI vs ΛCDM vs 8 alternatives (top-5 from W1 ΛCDM-alternatives review + 3 reference models). Produces evidence ratios log B_{model,ΛCDM} on combined dataset.

This builds on Levier #1 plan (`~/Bureau/eci-levier1-*-2026-05-02.md`) and the existing Cobaya infra in `/root/crossed-cosmos/mcmc/`. The new component is the multi-model evidence comparison; Levier #1 was just ECI vs ΛCDM single-model fit.

**Models.**
1. ΛCDM (baseline)
2. ECI (with ξ_χ free parameter)
3. Coupled-DE Amendola-type (top-1 alternative per W1)
4. BH/DHOST scalar-tensor (top-2 W1)
5. Holographic-DE Tsallis (top-3 W1)
6. Dark-Dimension swampland quintessence (top-4 W1)
7. EDE+late-DE hybrid (top-5 W1)
8. f(R) Hu-Sawicki
9. DGP brane
10. Sterile-ν

**Datasets.** Planck PR4, DESI DR2 BAO, DES Y6, Pantheon+, KiDS-1000 Legacy.

**Stack.** AxiCLASS / hi_class_public Boltzmann + Cobaya MCMC + cosmopower-jax NN emulator (~100× speedup if grid covers ECI subspace) + PolyChord nested sampling for log-evidence.

**Scale.**
- Per-model MCMC: ~10⁴ CPU-h × 10 models = 10⁵ CPU-h total
- On Vast.ai 64-core × 4×A100: ~5-7 days wall
- Estimated cost: $500-1000

**Reproduction.**
```bash
cd $REPO/compute/C4_joint_mcmc
# Generate 10 model YAMLs
python make_yamls.py --output yamls/

# Run all 10 in parallel via tmux
for m in lcdm eci coupled_de bh_dhost holo_tsallis dark_dim ede_hybrid fr_hs dgp sterile_nu; do
    tmux new-session -d -s mcmc_$m \
        "bash $REPO/scripts/vastai/launch-mcmc.sh yamls/${m}.yaml --packages-path packages"
done

# After convergence (R-1 < 0.05):
python compute_evidence.py chains/*/  --output results/log_evidence.csv
python plot_corner.py chains/eci/  chains/lcdm/  chains/coupled_de/
```

**Output paper target.** `paper/joint_mcmc_10models/` — major numerical paper, 15-25 pp, target PRD or JCAP. This is THE observational paper for ECI v6.0.42 / v7 transition.

**Theory anchor for model #3 (coupled-DE):** Amendola 1999 (PRD 60:043501, [astro-ph/9904120](https://arxiv.org/abs/astro-ph/9904120)).

## Layout

- `make_yamls.py` — generate Cobaya YAML per model with consistent priors (TODO)
- `compute_evidence.py` — extract log-evidence from PolyChord output (TODO)
- `plot_corner.py` — joint corner plots ECI vs top-5 alternatives (TODO)
- `priors/` — model-specific prior dicts
- `chains/` — MCMC output (gitignored, ~10 GB)
- `results/` — distilled evidence ratios + summary stats
