# Manual launch fallback — Kevin self-serve

Sub-agent M47, 2026-05-06. Use this if `dispatch.sh` cannot SSH (Tailscale re-auth state).

## Step 0 — re-shield Tailscale (after PC reboot)

```bash
sudo bash /home/remondiere/pc_calcs/tailscale_shield.sh
tailscale status                # should show 100.91.123.14 connected
```

If Tailscale needs re-auth: open the URL it prints, log in via Google, then re-run shield.

## Step 1 — get the M47 pipeline files onto PC

From VPS (when SSH works): `dispatch.sh --only-scp`

OR manually (PC has internet): clone from GitHub once Kevin pushes the M47 directory.
Until then, copy the 7 files locally:

```
SUMMARY.md
dispatch.sh
manual_launch.md                       <-- you are here
pipeline_a/f2_sage_sweep.sage
pipeline_a/expected_results.md
pipeline_b/v77_class_pipeline.py
pipeline_b/v77_setup_notes.md
```

Target directory on PC: `/home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES/`

## Step 2 — verify Python + sympy (Pipeline A; NO SageMath needed)

Per `CRITICAL_UPDATE_M47.md`: PC has no SageMath. Use the venv's Python + sympy.

```bash
source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate
python -c "import sympy, urllib.request, multiprocessing; print('sympy', sympy.__version__)"
```

Expected: `sympy 1.14.x`. If missing: `pip install sympy>=1.14 requests`.

## Step 3 — launch Pipeline A (F2 python sweep)

```bash
cd /home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES/pipeline_a
source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate

# parse-check (quick)
python -c "import ast; ast.parse(open('f2_python_sweep.py').read()); print('PARSE OK')"

# launch in tmux
tmux new -s f2py \
   "source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate && \
    python f2_python_sweep.py 2>&1 | tee f2_sweep_$(date +%Y%m%d_%H%M).log"
```

Detach: `Ctrl-b d`. Reattach: `tmux attach -t f2py`.

Expected runtime: 15-30 min wallclock (LMFDB REST API throttle is the bottleneck;
PC's 20 cores are not the limit). 8 workers polite to LMFDB.
Output: `f2_sweep_results.csv` (10 rows + header).

After completion, examine `f2_sweep_results.csv` -- look for the verdict line at end of stdout.

The `.sage` file in the same directory (`f2_sage_sweep.sage`) is kept as
**logic-reference only**; do NOT try to run it (no SageMath on PC).

## Step 4 — verify Pipeline B venv (only after A in)

```bash
cd /home/remondiere/crossed-cosmos
source .venv-mcmc-bench/bin/activate
python -c "import jax, blackjax, cosmopower_jax; \
  print('jax', jax.__version__); print('bj', blackjax.__version__); \
  print('cpj', cosmopower_jax.__version__)"
```

Expected: `jax 0.10.x  bj 1.5  cpj 0.5.5`.

If `import cosmopower_jax` fails on `named_shape`: re-apply patch.
File: `.venv-mcmc-bench/lib/python3.11/site-packages/jax/_src/core.py` line ~2445.
Add before `ShapedArray(...)`: `kwargs.pop("named_shape", None)`.

## Step 5 — smoke test Pipeline B (1-2 min)

```bash
cd /home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES/pipeline_b
python v77_class_pipeline.py --smoke
```

Expect: ~50 samples per chain, log_BF printed, .npz written. If smoke crashes,
check the printed traceback against `v77_setup_notes.md` "Honest caveats".

## Step 6 — launch Pipeline B full run

```bash
tmux new -s v77 \
   "cd /home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES/pipeline_b && \
    source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate && \
    python v77_class_pipeline.py --frontend cosmopower \
       --n_warmup 5000 --n_samples 5000 --n_chains 4 \
       2>&1 | tee v77_run_$(date +%Y%m%d_%H%M).log"
```

Detach with `Ctrl-b d`. Expected runtime: 2-4 hours on RTX 5060 Ti with cosmopower-jax.

## Step 7 — checkpoint to GitHub + Zenodo

Per memory note (disconnection resilience): after each major run, push checkpoint:

```bash
cd /home/remondiere/crossed-cosmos
git add notes/eci_v7_aspiration/M47_PC_PIPELINES/
git commit -m "M47 F2 + v7.7 results"
git push
```

Then Zenodo deposit via `/root/zenodo_deposit.py` from VPS (token at
`/root/.config/zenodo/token`, scope `deposit:write`).

## Trouble shooting

| Symptom                                   | Fix                                               |
|-------------------------------------------|---------------------------------------------------|
| `urllib HTTPError` from LMFDB             | wait 60 s, LMFDB rate-limit; rerun                |
| `Newforms(level=N, weight=5)` empty       | LMFDB has no such form; remove from `SWEEP_LABELS`|
| `cosmopower_jax import` `named_shape`     | re-apply JAX patch (see Step 4)                  |
| GPU OOM in NUTS                           | reduce n_chains to 2                             |
| `H_nmc` returns NaN at high z             | clamp `xi_chi` prior more tightly                |
