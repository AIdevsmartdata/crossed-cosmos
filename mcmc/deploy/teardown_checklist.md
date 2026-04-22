# Vast.ai Teardown Checklist — ECI MCMC

Run through this in order **every time** a rental ends. Skipping steps will
either lose data or keep billing the card.

## 1. Final chains retrieval

On the Vast.ai instance (inside tmux, after `cobaya-run` exits cleanly or
`R-1 < 0.01`):

```bash
cd /root/eci
TS=$(date -Iseconds | tr ':' '-')
tar czf chains_${TS}.tar.gz chains/
sha256sum chains_${TS}.tar.gz > chains_${TS}.sha256
```

From local workstation:

```bash
scp -P <port> root@<IP>:/root/eci/chains_*.tar.gz ./
scp -P <port> root@<IP>:/root/eci/chains_*.sha256 ./
```

- [ ] Tarball copied to local machine.
- [ ] `.sha256` copied.

## 2. Checksum verification

```bash
sha256sum -c chains_*.sha256
```

- [ ] Output shows `OK` for every file. If not, re-run `scp`; do NOT proceed.

## 3. Off-site copy (durability)

- [ ] Second copy uploaded to one of: Hetzner Storage Box, rsync.net, S3,
      local NAS — **not** the same disk as the working copy.

## 4. Quick sanity check of results

```bash
tar tzf chains_*.tar.gz | head
# Expect: chains/<prefix>.1.txt, .2.txt, ..., .input.yaml, .updated.yaml, .checkpoint
```

- [ ] At least one `.N.txt` per MPI rank present.
- [ ] `.checkpoint` file exists (Cobaya resume marker).
- [ ] Last 10 lines of `chains/run_*.log` show `R-1` ≤ target (0.01 for
      production, 0.1 for exploratory).

## 5. Cost logging

Append a row to `mcmc/deploy/_rental_log.md`:

```
| YYYY-MM-DD | eci_nmc_optimized | $/h | duration | wallclock | $total | OK/FAIL | notes |
```

- [ ] Row appended and committed locally.

## 6. Terminate instance

https://cloud.vast.ai/instances/ → locate instance → **Destroy** (not "Stop"
— Stop still bills for disk).

- [ ] Instance disappears from the list.
- [ ] Dashboard "Current spend rate" returns to $0.00/h.
- [ ] Billing page shows the final charge matching the log entry (±10 %).

## 7. Credentials hygiene

- [ ] Remove the instance's host entry from `~/.ssh/known_hosts` so the next
      rental at a recycled IP does not trip the HostKey warning:
      `ssh-keygen -R '[ssh4.vast.ai]:<port>'`
- [ ] If `BACKUP_TARGET` used SSH, the instance's private key is gone with
      the instance — nothing to rotate.

## 8. Post-mortem (if FAIL)

If the run did not reach convergence:

- [ ] Capture the last 500 lines of `chains/run_*.log` into the rental log
      `notes` column.
- [ ] Note cause: spot preemption / OOM / OMP misconfig / YAML error.
- [ ] Open an issue or add a line in `mcmc/benchmark/REPORT.md` if the cause
      is a new systemic constraint.
