# YM Toolkit — PC gamer pipeline

## Quick start
```bash
./run_all.sh        # Launch full pipeline (background)
./status.sh         # Check status anytime
```

## Files
- `0_framework_check.py` : algebraic verification (30s)
- `1_hmc_su2.py` : Wilson HMC SU(2) sampler
- `3_persistent_homology.py` : Z_2 vortex detection from configs
- `run_all.sh` : orchestrator
- `status.sh` : status dashboard
- `logs/` : process logs
- `results/` : data outputs (.npz, .json)

## Pipeline phases
1. HMC generates SU(2) configs at β=2.3, 2.5, 2.7
2. PySR runs symbolic regression on AT2021 spectrum
3. Once configs ready : persistent homology vortex density
4. Compare ρ_vortex/σ₀ cross-β → confinement signature

## Predictions to test
- ⟨Polyakov⟩ → 0 in confined phase
- ρ_vortex/σ₀ ~ O(1) (Greensite)
- Crossover β_c ~ 2.3 (SU(2) deconfinement)
