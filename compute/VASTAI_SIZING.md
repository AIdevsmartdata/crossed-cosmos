# Vast.ai sizing reference for the ECI numerical campaign

Sizes refer to Vast.ai instance specs as of 2026-05. Prices fluctuate ±30% on the spot market.

## Recommended profiles

### Profile S — single Tier-1 paper, dev
- **Instance**: 16 vCPU + 1× RTX 4090 24 GB or RTX 6000 Ada 48 GB
- **Price**: $0.30–0.50 / hour
- **Use for**: C1, C2, C5 prototyping
- **Wall-time budget**: 24-48 h × $0.40 = $10-20

### Profile M — Tier-1 production
- **Instance**: 32 vCPU + 1× A6000 48 GB or L40S 48 GB
- **Price**: $0.50–0.90 / hour
- **Use for**: C1 production (full bounce-model scan), C2 production, C3 medium-N (≤2^17)
- **Wall-time budget**: 48-72 h × $0.70 = $35-50 per item

### Profile L — multi-model MCMC + large MERA
- **Instance**: 64 vCPU + 4× A100 80 GB (PCIe) — DDR5 256 GB host RAM
- **Price**: $4–6 / hour
- **Use for**: C4 joint-MCMC (10 models in parallel), C3 large-N (2^18-2^20)
- **Wall-time budget**: 5-7 days × $5 = $600-1000

### Profile XL — only with strong reason
- **Instance**: 4× H100 80 GB SXM
- **Price**: $8–15 / hour
- **Use for**: only if profile L cannot finish in <2 weeks
- Typically not needed for our items

## Recommended booking sequence

1. **Day 1** — Profile S, 24h ($10) — bootstrap + run C1 prototype + C2 prototype
2. **Day 2** — Profile M, 48h ($35) — production C1 + C2; first DMRG runs N=2^14, 2^15
3. **Day 3-4** — Profile M, 72h ($50) — C5 production + start C3 N=2^16
4. **Week 2** — Profile L, 5 days ($600) — joint MCMC C4 if first 3 papers are landing
5. Total budget for entire campaign Tier-1: **~$700-1000**

## Setup time

`bash setup-vastai.sh` finishes in ~12-15 min on a fresh image (depends on AxiCLASS compile). If pip-cached, ~6 min.

## Critical Docker / MPI quirks

Already encoded in `scripts/vastai/launch-mcmc.sh`:
- `--bind-to none`
- `--mca btl_vader_single_copy_mechanism none`
- `--oversubscribe`
- Use `python -m cobaya run` (NOT the `cobaya-run` wrapper) — wrapper breaks MPI rank detection
- `set +e + nohup + setsid + < /dev/null` for SSH-survivable background

## What NOT to do

- Don't book Profile XL "just in case". Profile L is enough for everything we currently need.
- Don't book a 4×H100 unless you have a clear 5-day production plan ready (not for prototyping).
- Don't forget to `vastai stop instance <ID>` when done. Idle GPU instances burn $5+/hour.
- Don't run `apt upgrade` on rented instances — wastes setup time, sometimes breaks CUDA.

## Cost guardrails

Set up Vast.ai email alerts at $50, $200, $500, $1000 thresholds before starting. Keep a running spreadsheet of {item, instance, hours, $-cost, output} in `compute/_runs.csv`.
