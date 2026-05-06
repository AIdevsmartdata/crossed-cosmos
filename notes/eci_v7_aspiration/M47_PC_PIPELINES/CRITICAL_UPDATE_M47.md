# CRITICAL UPDATE M47 — PC tooling confirmed by parent (2026-05-06 13:45 CEST)

If you (sub-agent M47) read this BEFORE finishing your write tasks, adjust accordingly:

## Hard facts (verified by parent SSH probe)
- **NO SageMath on PC OR VPS** — do NOT write `.sage` files
- **Use Python + sympy 1.14 + requests** instead. Pure Python, no Sage.
- **PC venv `/home/remondiere/crossed-cosmos/.venv-mcmc-bench`** confirmed has:
  - sympy 1.14.0
  - requests 2.33.1
  - JAX 0.10 (with named_shape patch applied)
  - blackjax 1.5
  - cosmopower-jax 0.5.5
- **Tailscale SSH WORKING** as of now (user re-auth done at 13:44 CEST)
- PC has 20 P-cores + RTX 5060 Ti 15.7 GB free

## Adjustments to your plan
1. F2 script filename: `f2_python_sweep.py` (NOT `.sage`)
2. F2 implementation: **LMFDB JSON REST API** (https://www.lmfdb.org/api/) for newform queries. Sympy QQ_2 / valuation for v_2 computation. Multiprocessing.Pool with 18 workers for parallel sweep.
3. v7.7 CLASS pipeline: prefer **cosmopower-jax** fallback over full CLASS Boltzmann (already trained, ~386 predictions/sec on this GPU). If cosmopower-jax doesn't cover the parameter space needed, use classy-szbut document complexity.
4. Dispatch: SSH to `remondiere@100.91.123.14` works. `dispatch.sh` can scp + ssh exec directly.

If you've already finished with `.sage`, that's OK — parent will rewrite in Python. Just make the LOGIC clear.
