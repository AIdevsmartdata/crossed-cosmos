# dispatch_v2.md — How to launch pipeline_b_v2_nested_sampling.py on PC

Sub-agent M56, 2026-05-06. Launch ONLY after M50 NUTS job (`tmux v77ecicontest`)
has completed and `v77_ecicontest_results.npz` is saved.

---

## §1 Prerequisites

```bash
# On PC gamer (Tailscale 100.91.123.14)
source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate

# Install missing dependencies (dynesty, h5py)
pip install dynesty h5py   # scipy already present for ndtri

# Verify
python -c "import dynesty; print('dynesty', dynesty.__version__)"
# Expected: dynesty 2.1.x  (or later)

python -c "import h5py; print('h5py', h5py.__version__)"
```

---

## §2 Smoke test (2-5 min, safe to run immediately)

```bash
cd /home/remondiere/crossed-cosmos

python notes/eci_v7_aspiration/M56_NESTED_SAMPLING/pipeline_b_v2_nested_sampling.py \
    --smoke \
    --sampler dynesty

# Expected output:
# [v2-NS] SMOKE MODE: n_live=50, dlogz=2.0, 1 CPU
# [v2-NS] ECI-NMC log_Z = -XXX.X +/- Y.Y  (Ns)
# [v2-NS] Wolf-NMC log_Z = -YYY.Y +/- Z.Z  (Ns)
# [v2-NS] log_BF(ECI/Wolf) = +XX.X +/- Y.Y
# [v2-NS] saved: .../v77_v2_nested_results.h5
```

If smoke fails with ImportError: install the missing package (dynesty / h5py).
If smoke fails with a numerical -inf: check that DESI data fallback loaded OK
(it should always fall back to the hardcoded 7-bin values).

---

## §3 Full production run (tmux, 18 cores)

```bash
# Apply tailscale shield first (if PC was rebooted)
sudo bash /home/remondiere/pc_calcs/tailscale_shield.sh

tmux new-session -d -s v2ns \
  "cd /home/remondiere/crossed-cosmos && \
   source .venv-mcmc-bench/bin/activate && \
   python notes/eci_v7_aspiration/M56_NESTED_SAMPLING/pipeline_b_v2_nested_sampling.py \
     --sampler dynesty \
     --n_live 500 \
     --dlogz 0.5 \
     --n_cpus 18 \
     --seed 20260506 \
     --out /home/remondiere/crossed-cosmos/m47_pipelines/pipeline_b/v77_v2_nested_results.h5 \
   2>&1 | tee /home/remondiere/v2ns_run_$(date +%Y%m%d_%H%M).log"

tmux attach -t v2ns
# Detach: Ctrl-B D
```

Expected runtime: 3-5h (n_live=500, dlogz=0.5, 18 cores).

---

## §4 Publication-grade upgrade

Once fast run completes and log_Z_err < 0.3 on both variants:

```bash
python notes/eci_v7_aspiration/M56_NESTED_SAMPLING/pipeline_b_v2_nested_sampling.py \
    --sampler dynesty \
    --n_live 1000 \
    --dlogz 0.1 \
    --n_cpus 18 \
    --out /home/remondiere/crossed-cosmos/m47_pipelines/pipeline_b/v77_v2_paper_results.h5
```

Expected runtime: 10-18h. Run overnight in tmux.

---

## §5 Swap to ultranest (if dynesty sampling efficiency < 5%)

```bash
pip install ultranest

python notes/eci_v7_aspiration/M56_NESTED_SAMPLING/pipeline_b_v2_nested_sampling.py \
    --sampler ultranest \
    --n_live 400 \
    --dlogz 0.5 \
    --n_cpus 18
```

ultranest does not use multiprocessing.Pool in the same way as dynesty;
pass `--n_cpus 1` if ultranest raises parallelism errors, and let it use
its internal threading instead.

---

## §6 Reading results

```python
import h5py, numpy as np, json

with h5py.File("v77_v2_nested_results.h5", "r") as f:
    log_Z_eci  = f["eci_nmc"].attrs["log_Z"]
    log_Z_wolf = f["wolf_nmc"].attrs["log_Z"]
    log_BF     = f.attrs["log_BF"]
    log_BF_err = f.attrs["log_BF_err"]
    samples_eci  = f["eci_nmc/samples"][:]   # (N_eff, 10)
    meta = json.loads(f.attrs["meta"])

print(f"log_BF = {log_BF:.2f} +/- {log_BF_err:.2f}")
# For posterior plots: pip install anesthetic
# import anesthetic; s = anesthetic.NestedSamples(...)
```

---

## §7 Honest caveats before citing in paper

1. theta_* is EH+KMJ (3.1-sigma bias). Upgrade to classy for paper-grade CMB.
2. Wolf-NMC KG ODE not integrated. xi=2.31 contest is NMC-distance-only.
3. PR4 cov is diagonal. Cite Tristram 2024 arXiv:2309.10034 carefully.
4. Pantheon+ real cov needs /home/remondiere/data/pantheonplus/ to exist.
