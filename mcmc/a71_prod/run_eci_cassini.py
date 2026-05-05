"""
A71 — Production run: ECI-Cassini CPL-effective NUTS.

Configuration: 4 chains × 8000 samples × 4000 warmup (per A70 spec).
Model: eci_cassini_cpl_model (9 params; cosmopower-jax emulator).

PREREQUISITES (must be done before launching):
  1. Emulator pkls present:
       /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl
       /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl
  2. JAX named_shape patch applied (done at import by emulators.py).
  3. Smoke test passed (see smoke_test.py).
  4. [TBD: locate real DESI DR2 data file and Pantheon+ mu_obs + cov_inv]

Usage (on PC from crossed-cosmos repo root):
  source .venv-mcmc-bench/bin/activate
  python -m mcmc.a71_prod.run_eci_cassini \\
    --chains 4 --warmup 4000 --samples 8000 \\
    --output /home/remondiere/pc_calcs/A71/eci_run_01/

DO NOT RUN on VPS — requires RTX 5060 Ti + pkls at PC paths.

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.
"""

import argparse
import json
import os
import sys
import time
import warnings

# Apply JAX named_shape patch at script entry (before emulators import)
def _patch_jax():
    try:
        import jax._src.core as c
        if not getattr(c, "_a71_named_shape_patch_applied", False):
            orig = c.ShapedArray.update
            def patched(self, **kw):
                kw.pop("named_shape", None)
                return orig(self, **kw)
            c.ShapedArray.update = patched
            c._a71_named_shape_patch_applied = True
    except Exception as e:
        print(f"[run_eci] WARNING: JAX patch failed: {e}", file=sys.stderr)

_patch_jax()

import jax
import jax.numpy as jnp
import numpyro
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from mcmc.a71_prod import emulators
from mcmc.a71_prod.numpyro_models import eci_cassini_cpl_model, make_nuts_mcmc
from numpyro.diagnostics import effective_sample_size, split_gelman_rubin


def run_eci_production(
    n_chains: int = 4,
    n_warmup: int = 4000,
    n_samples: int = 8000,
    chain_method: str = "parallel",
    output_dir: str | None = None,
    emulator_dir: str = "/home/remondiere/pc_calcs/cosmopower_nmc_emulator",
    data_dict: dict | None = None,
) -> dict:
    """
    Run ECI-Cassini CPL-effective NUTS production chain.

    Args:
      n_chains, n_warmup, n_samples: MCMC configuration
      chain_method: "parallel" (GPU default) or "sequential" (fallback)
      output_dir: directory to save samples.npz + diagnostics.json
      emulator_dir: directory containing nmc_kg_w.pkl and nmc_kg_logH.pkl
      data_dict: optional custom data dict; if None, uses synthetic + hardcoded

    Returns:
      dict with diagnostics and file paths
    """
    if output_dir is None:
        output_dir = os.path.join(_HERE, "_results", "eci_run_01")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[run_eci] ====== A71 ECI-Cassini CPL Production Run ======")
    print(f"[run_eci] Chains={n_chains}, warmup={n_warmup}, samples={n_samples}")
    print(f"[run_eci] JAX devices: {jax.devices()}")
    print(f"[run_eci] Output: {output_dir}")

    # -----------------------------------------------------------------------
    # STEP 1 — Load emulators
    # -----------------------------------------------------------------------
    w_pkl    = os.path.join(emulator_dir, "nmc_kg_w.pkl")
    logH_pkl = os.path.join(emulator_dir, "nmc_kg_logH.pkl")

    print(f"[run_eci] Loading emulators from {emulator_dir} ...")
    emulators.load_emulators(w_pkl=w_pkl, logH_pkl=logH_pkl)
    emulators.smoke_check(verbose=True)
    print("[run_eci] Emulators loaded and smoke-checked OK.")

    # -----------------------------------------------------------------------
    # STEP 2 — Build and run MCMC
    # -----------------------------------------------------------------------
    mcmc = make_nuts_mcmc(
        model=eci_cassini_cpl_model,
        n_chains=n_chains,
        n_warmup=n_warmup,
        n_samples=n_samples,
        target_accept_prob=0.85,
        chain_method=chain_method,
        progress_bar=True,
    )

    rng_key = jax.random.PRNGKey(20260506)
    t0 = time.perf_counter()

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            mcmc.run(rng_key, data_dict)
    except Exception as e:
        if "parallel" in chain_method:
            print(f"[run_eci] Parallel failed ({e}). Retrying sequential...")
            mcmc_seq = make_nuts_mcmc(
                model=eci_cassini_cpl_model,
                n_chains=n_chains,
                n_warmup=n_warmup,
                n_samples=n_samples,
                chain_method="sequential",
                progress_bar=True,
            )
            mcmc_seq.run(rng_key, data_dict)
            mcmc = mcmc_seq
        else:
            raise

    elapsed = time.perf_counter() - t0
    print(f"[run_eci] MCMC done in {elapsed:.0f}s ({elapsed/3600:.2f}h)")

    # -----------------------------------------------------------------------
    # STEP 3 — Diagnostics
    # -----------------------------------------------------------------------
    samples = mcmc.get_samples(group_by_chain=True)
    flat    = mcmc.get_samples()

    param_names = list(samples.keys())
    r_hat_values, ess_values, posteriors = {}, {}, {}

    for pname in param_names:
        arr  = samples[pname]
        rhat = float(split_gelman_rubin(arr))
        ess  = float(effective_sample_size(arr))
        r_hat_values[pname] = rhat
        ess_values[pname]   = ess
        farr = np.array(flat[pname])
        posteriors[pname] = {
            "median": float(np.median(farr)),
            "mean":   float(np.mean(farr)),
            "std":    float(np.std(farr)),
            "p16":    float(np.percentile(farr, 16)),
            "p84":    float(np.percentile(farr, 84)),
        }

    r_hat_max = max(r_hat_values.values())
    ess_min   = min(ess_values.values())

    print(f"\n[run_eci] Convergence: R̂_max={r_hat_max:.4f}, ESS_min={ess_min:.0f}")
    print(f"\n[run_eci] Posterior summaries:")
    for pname in param_names:
        p = posteriors[pname]
        print(f"  {pname:<20} {p['median']:>10.5f} ± {p['std']:.5f}")

    # -----------------------------------------------------------------------
    # STEP 4 — Gate check (A70 Table sanity)
    # -----------------------------------------------------------------------
    verdict = "CONVERGED" if (r_hat_max < 1.01 and ess_min > 400) else (
              "MARGINAL"  if (r_hat_max < 1.05 and ess_min > 100) else "NOT_CONVERGED"
    )
    print(f"\n[run_eci] Verdict: {verdict}")
    if verdict == "NOT_CONVERGED":
        print("[run_eci] WARNING: R̂ > 1.05 or ESS < 100. DO NOT report H_ECI.")

    # -----------------------------------------------------------------------
    # STEP 5 — Save
    # -----------------------------------------------------------------------
    # Save samples
    samples_path = os.path.join(output_dir, "eci_samples.npz")
    np.savez(samples_path, **{k: np.array(v) for k, v in flat.items()})
    print(f"[run_eci] Samples saved: {samples_path}")

    # Save diagnostics
    diag = {
        "verdict": verdict,
        "r_hat": r_hat_values,
        "r_hat_max": r_hat_max,
        "ess": ess_values,
        "ess_min": ess_min,
        "posteriors": posteriors,
        "run_config": {
            "model": "eci_cassini_cpl_model",
            "n_chains": n_chains,
            "n_warmup": n_warmup,
            "n_samples": n_samples,
            "chain_method": chain_method,
            "elapsed_sec": elapsed,
        },
        "meta": {
            "jax_version": jax.__version__,
            "jax_devices": [str(d) for d in jax.devices()],
            "emulator_dir": emulator_dir,
            "_data_note": "[TBD: confirm real vs synthetic data used]",
        },
    }
    diag_path = os.path.join(output_dir, "eci_diagnostics.json")
    with open(diag_path, "w") as f:
        json.dump(diag, f, indent=2)
    print(f"[run_eci] Diagnostics saved: {diag_path}")

    return diag


# =========================================================================
# Entry point
# =========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A71 ECI-Cassini CPL production NUTS run"
    )
    parser.add_argument("--chains",       type=int, default=4)
    parser.add_argument("--warmup",       type=int, default=4000)
    parser.add_argument("--samples",      type=int, default=8000)
    parser.add_argument("--chain-method", type=str, default="parallel",
                        choices=["parallel", "sequential", "vectorized"])
    parser.add_argument("--output",       type=str, default=None)
    parser.add_argument("--emu-dir",      type=str,
                        default="/home/remondiere/pc_calcs/cosmopower_nmc_emulator")
    args = parser.parse_args()

    run_eci_production(
        n_chains=args.chains,
        n_warmup=args.warmup,
        n_samples=args.samples,
        chain_method=args.chain_method,
        output_dir=args.output,
        emulator_dir=args.emu_dir,
    )
