# Vast.ai Deployment — ECI NMC MCMC Run

Owner-facing runbook for renting an EPYC spot instance on Vast.ai and running
the ECI / hi\_class Plik-lite MCMC chain end-to-end. Target wall-clock 3.6 h,
budget ~$5. Last updated 2026-04-21.

## 0. Prerequisites (one-time)

- Vast.ai account with ≥$10 credits and billing email verified.
- SSH keypair on local machine (`~/.ssh/id_ed25519.pub`). Upload the **public**
  key to https://cloud.vast.ai/account/ → "SSH Keys".
- Local clone of `crossed-cosmos` so you can `scp` results back.

## 1. Instance selection

Open https://cloud.vast.ai/create/ and set filters:

| Field | Value |
|-------|-------|
| Machine type tab | **CPU** (not GPU) |
| CPU cores | ≥ 48 physical (96 threads) |
| RAM | ≥ 128 GB |
| Disk space | ≥ 80 GB (Planck 2018 ≈ 5 GB + packages + chains) |
| Spot | **Interruptible** (3–5× cheaper than on-demand) |
| Region | EU preferred (lower latency for SSH + rsync) |
| Max $/h | **0.80** |

Preferred SKU order:

1. **AMD EPYC 9965 (Zen 5 Turin, 192 threads)** — matches the benchmark
   target. Typical spot ≈ $0.50–0.80/h.
2. AMD EPYC 9654 (Genoa, 96 cores / 192 threads) — fallback.
3. AMD EPYC 7763 (Milan, 64c/128t) — last resort; expect ~1.5× wall-clock.

Sort by `$/DLP` ascending, then pick the cheapest row matching the CPU filter
with ≥ 99 % reliability score.

### Image

In the "Instance Configuration" panel:

- **Template**: `nvidia/cuda:12.5.0-devel-ubuntu22.04` — ships with `gcc`,
  `gfortran`, build-essential. The CUDA libs are unused but do no harm. ≈2 GB
  pull, fastest clean start.
- Alternative clean: `ubuntu:24.04` — smaller but you pay the `apt-get` tax
  twice (once for build-essential, once for gfortran).
- Avoid the `pytorch/*` images: large (~8 GB) and pin a conflicting numpy.

### On-start script

Paste the full content of `mcmc/deploy/vast_ai_on_create.sh` into the
"On-start Script" textbox. The script will:

1. `apt-get install` build deps + OpenMPI + tmux.
2. Clone `crossed-cosmos` into `/root/eci`.
3. Create `.venv-mcmc` with **numpy==1.26.4** (hi\_class Cython is incompatible
   with numpy 2.x — see benchmark report §4.2).
4. Build CLASS with **explicit `-fopenmp`** (CLASS Makefile defaults to
   `-pthread` only, which does NOT enable OpenMP — see benchmark §4.3).
5. Install Cobaya packages (Planck 2018 + DESI DR2 + Pantheon+).

Set **Disk**: 80 GB. **SSH key**: auto-injected from account settings.

### Budget guardrail

Dashboard → Billing → "Max Spend Cap" → **$10**. Hard-stops billing at 2×
expected cost, protects against runaway spot hours if you forget to tear down.

## 2. First SSH

Once the instance shows "running" (≈3–5 min), the on-start script is still
executing. Click "Connect" → copy the `ssh -p <port> root@<IP>` command.

```bash
ssh -p 12345 root@ssh4.vast.ai
# wait for on-create to finish — tail it:
tail -f /var/log/onstart.log
```

When you see `>>> Vast.ai on-create complete.` the environment is ready.

## 3. Launch MCMC

```bash
tmux new -s mcmc
cd /root/eci
bash mcmc/deploy/run_vast.sh
# detach: Ctrl-b d
```

The launcher runs `mpirun -np 8` with 2 OMP threads per chain (16 threads
engaged, 176 spare for CLASS internal OMP via `OMP_NUM_THREADS` cascades).
Cobaya checkpoints **every 30 min** by default — spot preemption wastes at
most half an hour.

Reattach at any time with `tmux a -t mcmc`.

## 4. Monitoring

- Convergence: `tail -f chains/run_*.log | grep -E 'R-1|Progress'`
- CPU: `htop` (install via `apt-get install htop` if missing)
- Disk: `df -h /root` — chains grow ~50 MB/h, 80 GB is plenty.

Optional incremental off-site backup (recommended for spot runs):

```bash
export BACKUP_TARGET='user@storagebox.your-server.de:eci-chains/'
# or 's3://my-bucket/eci/' if you have awscli + creds
(crontab -l 2>/dev/null; echo '*/30 * * * * /root/eci/mcmc/deploy/checkpoint_rsync.sh') | crontab -
```

The rsync script is idempotent; lost-spot + resumed-instance handles cleanly.

## 5. Spot interruption recovery

If Vast.ai kills the instance:

1. Re-create an identical instance (same template + on-start script).
2. Restore chains from backup target: `rsync -av $BACKUP_TARGET /root/eci/chains/`
3. Re-run `bash mcmc/deploy/run_vast.sh` — Cobaya auto-resumes from the last
   checkpoint (detects `chains/*.checkpoint` and continues).

Expected loss per preemption: ≤ 30 min of compute.

## 6. Completion & teardown

When `R-1 < 0.01` on all sampled params (usually 3.5–4 h wall-clock):

```bash
# inside tmux on the instance
cd /root/eci
TS=$(date -Iseconds | tr ':' '-')
tar czf chains_${TS}.tar.gz chains/
sha256sum chains_${TS}.tar.gz > chains_${TS}.sha256
```

From local:

```bash
scp -P <port> root@<IP>:/root/eci/chains_*.tar.gz ./
scp -P <port> root@<IP>:/root/eci/chains_*.sha256 ./
sha256sum -c chains_*.sha256
```

Then follow `mcmc/deploy/teardown_checklist.md` before terminating.

## 7. Cost tracking

Every rental, append a row to `mcmc/deploy/_rental_log.md`:
`date | target | $/h | duration | wallclock | $total | result | notes`.

Target for first EPYC 9965 run:
- $0.60/h × 3.6 h + 10 % overhead = **~$2.40**.
- Safety cap at $10 leaves room for a full re-run if the first attempt bricks.

## 8. Known gotchas

- **numpy 2 breakage**: if you ever upgrade, re-pin `numpy==1.26.4`; hi\_class
  Cython ABI hardcodes numpy 1.x C-API.
- **OpenMP silent-off**: if CLASS runs at 100 % of **one** core only, you
  forgot `OMPFLAG=-fopenmp` (see on-create script — CFLAGS alone is not
  enough, the Makefile reads `OMPFLAG` separately).
- **Plik-lite only**: the YAML (`eci_nmc_optimized.yaml`) targets Plik-lite —
  10× faster than full Plik with 95 % of the constraining power. Do not swap
  to the full likelihood without re-budgeting.
- **`--bind-to none` is mandatory** for `mpirun` on Vast.ai — most hosts run
  inside cgroups that reject hard affinity binding.

## 9. Quick reference

| Task | Command |
|------|---------|
| SSH in | `ssh -p <port> root@<IP>` |
| Tail setup log | `tail -f /var/log/onstart.log` |
| Attach run | `tmux a -t mcmc` |
| Force checkpoint | `Ctrl-C` in tmux — Cobaya writes checkpoint on SIGINT |
| Resume | `bash mcmc/deploy/run_vast.sh` (auto-detects) |
| Pull chains | `scp -P <port> root@<IP>:/root/eci/chains_*.tar.gz .` |
