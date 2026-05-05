"""
A71 — Smoke test: ΛCDM NUTS on RTX 5060 Ti.

Runs: lcdm_model, 4 chains × 1000 samples × 1000 warmup.
Checks: R̂ < 1.05 and ESS > 100 per parameter.
Saves: smoke_test_results.json in same directory.

Usage:
  python smoke_test.py [--chains 4] [--warmup 1000] [--samples 1000]
                       [--chain-method parallel] [--output results.json]

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.
"""

import argparse
import json
import os
import sys
import time
import warnings

# Suppress Python-level warnings about synthetic data during smoke test
warnings.filterwarnings("ignore", category=UserWarning)

# =========================================================================
# SECTION 0 — Apply JAX named_shape patch at script entry
# (Belt-and-suspenders: emulators.py also applies it, but smoke test
#  doesn't import emulators, so we patch here independently)
# =========================================================================
def _patch_jax_named_shape():
    """Apply JAX named_shape patch per reference_jax_patch.md."""
    try:
        import jax._src.core as _jax_core
        if getattr(_jax_core, "_a71_named_shape_patch_applied", False):
            return
        _orig = _jax_core.ShapedArray.update
        def _patched(self, **kwargs):
            kwargs.pop("named_shape", None)
            return _orig(self, **kwargs)
        _jax_core.ShapedArray.update = _patched
        _jax_core._a71_named_shape_patch_applied = True
    except Exception as e:
        print(f"[smoke_test] WARNING: JAX patch failed: {e}", file=sys.stderr)


_patch_jax_named_shape()

# =========================================================================
# SECTION 1 — Imports (after patch)
# =========================================================================
import jax
import jax.numpy as jnp
import numpyro
from numpyro.infer import MCMC, NUTS
from numpyro.diagnostics import effective_sample_size, split_gelman_rubin

# Local imports
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from mcmc.a71_prod.numpyro_models import lcdm_model, make_nuts_mcmc

# =========================================================================
# SECTION 2 — Smoke test runner
# =========================================================================

def run_smoke_test(
    n_chains: int = 4,
    n_warmup: int = 1000,
    n_samples: int = 1000,
    chain_method: str = "parallel",
    output_path: str | None = None,
    data_dict: dict | None = None,
) -> dict:
    """
    Run ΛCDM NUTS smoke test. Returns results dict.

    Args:
      n_chains: number of NUTS chains (4 for smoke test, 8 for production)
      n_warmup: warmup steps per chain
      n_samples: sampling steps per chain
      chain_method: "parallel" (GPU) or "sequential" (fallback)
      output_path: if given, save JSON results here
      data_dict: optional custom data dict (uses synthetic if None)

    Returns:
      dict with R̂, ESS, posterior medians, pass/fail verdict
    """
    print(f"\n[smoke_test] ====== A71 ΛCDM NUTS Smoke Test ======")
    print(f"[smoke_test] Chains={n_chains}, warmup={n_warmup}, samples={n_samples}")
    print(f"[smoke_test] chain_method={chain_method}")
    print(f"[smoke_test] JAX devices: {jax.devices()}")
    print(f"[smoke_test] JAX version: {jax.__version__}")

    # Set JAX to use 64-bit floats for numerical stability
    # Note: numpyro works with 32-bit; leave as default unless NaN issues arise
    # jax.config.update("jax_enable_x64", True)

    t0 = time.perf_counter()

    # Build MCMC
    mcmc = make_nuts_mcmc(
        model=lcdm_model,
        n_chains=n_chains,
        n_warmup=n_warmup,
        n_samples=n_samples,
        target_accept_prob=0.85,
        chain_method=chain_method,
        progress_bar=True,
    )

    # Run
    rng_key = jax.random.PRNGKey(20260505)
    try:
        mcmc.run(rng_key, data_dict)
    except Exception as e:
        if "parallel" in chain_method and ("named_shape" in str(e) or "vmap" in str(e).lower()):
            print(f"\n[smoke_test] FALLBACK: parallel chain_method failed ({e}). "
                  f"Retrying with sequential...", file=sys.stderr)
            mcmc_seq = make_nuts_mcmc(
                model=lcdm_model,
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

    # -----------------------------------------------------------------------
    # SECTION 3 — Convergence diagnostics
    # -----------------------------------------------------------------------
    samples = mcmc.get_samples(group_by_chain=True)
    # samples: dict {param: (n_chains, n_samples)}

    param_names = list(samples.keys())
    print(f"\n[smoke_test] Parameters: {param_names}")

    # Compute R̂ and ESS per parameter
    r_hat_values = {}
    ess_values   = {}

    for pname in param_names:
        chain_arr = samples[pname]   # shape: (n_chains, n_samples)
        # split_gelman_rubin expects shape (n_chains, n_samples)
        rhat = float(split_gelman_rubin(chain_arr))
        ess  = float(effective_sample_size(chain_arr))
        r_hat_values[pname] = rhat
        ess_values[pname]   = ess

    r_hat_max = max(r_hat_values.values())
    ess_min   = min(ess_values.values())

    # -----------------------------------------------------------------------
    # SECTION 4 — Posterior medians
    # -----------------------------------------------------------------------
    flat_samples = mcmc.get_samples()  # shape (n_chains * n_samples,)
    posteriors = {}
    for pname in param_names:
        arr = flat_samples[pname]
        import numpy as np
        posteriors[pname] = {
            "median": float(np.median(arr)),
            "mean": float(np.mean(arr)),
            "std":  float(np.std(arr)),
            "p16":  float(np.percentile(arr, 16)),
            "p84":  float(np.percentile(arr, 84)),
        }

    # Print table
    print(f"\n[smoke_test] Posterior medians:")
    print(f"  {'Param':<20} {'Median':>10} {'±σ':>8}  R̂={r_hat_max:.4f}  ESS_min={ess_min:.0f}")
    print(f"  {'-'*55}")
    for pname in param_names:
        p = posteriors[pname]
        rh = r_hat_values[pname]
        es = ess_values[pname]
        print(f"  {pname:<20} {p['median']:>10.5f} {p['std']:>8.5f}  R̂={rh:.4f}  ESS={es:.0f}")

    # -----------------------------------------------------------------------
    # SECTION 5 — Pass/Fail verdict
    # -----------------------------------------------------------------------
    pass_rhat = r_hat_max < 1.05
    pass_ess  = ess_min > 100.0
    verdict = "PASS" if (pass_rhat and pass_ess) else "FAIL"

    print(f"\n[smoke_test] ===== VERDICT: {verdict} =====")
    print(f"  R̂ max = {r_hat_max:.4f}  (< 1.05 required: {'OK' if pass_rhat else 'FAIL'})")
    print(f"  ESS min = {ess_min:.0f}  (> 100 required: {'OK' if pass_ess else 'FAIL'})")
    print(f"  Elapsed: {elapsed:.1f}s")

    if not pass_rhat:
        print("[smoke_test] WARNING: R̂ > 1.05 — chains not converged. "
              "Try more warmup or sequential chain_method.")
    if not pass_ess:
        print("[smoke_test] WARNING: ESS < 100 — poor mixing. "
              "Try more samples or different step size.")

    # -----------------------------------------------------------------------
    # SECTION 6 — Save results
    # -----------------------------------------------------------------------
    results = {
        "verdict": verdict,
        "r_hat": r_hat_values,
        "r_hat_max": r_hat_max,
        "ess": ess_values,
        "ess_min": ess_min,
        "pass_rhat": pass_rhat,
        "pass_ess": pass_ess,
        "posteriors": posteriors,
        "run_config": {
            "n_chains": n_chains,
            "n_warmup": n_warmup,
            "n_samples": n_samples,
            "chain_method": chain_method,
            "elapsed_sec": elapsed,
        },
        "meta": {
            "model": "lcdm_model",
            "jax_version": jax.__version__,
            "jax_devices": [str(d) for d in jax.devices()],
            "data": "synthetic" if data_dict is None else "provided",
            "_note": (
                "Smoke test uses synthetic SNe data and hardcoded DESI DR2 Table 1 values. "
                "[TBD: rerun with real data before production use]"
            ),
        },
    }

    if output_path is None:
        output_path = os.path.join(_HERE, "smoke_test_results.json")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[smoke_test] Results saved to: {output_path}")

    return results


# =========================================================================
# SECTION 7 — Entry point
# =========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A71 ΛCDM NUTS smoke test on RTX 5060 Ti"
    )
    parser.add_argument("--chains",       type=int,   default=4,
                        help="Number of NUTS chains (default: 4)")
    parser.add_argument("--warmup",       type=int,   default=1000,
                        help="Warmup steps per chain (default: 1000)")
    parser.add_argument("--samples",      type=int,   default=1000,
                        help="Sampling steps per chain (default: 1000)")
    parser.add_argument("--chain-method", type=str,   default="parallel",
                        choices=["parallel", "sequential", "vectorized"],
                        help="numpyro chain_method (default: parallel)")
    parser.add_argument("--output",       type=str,   default=None,
                        help="Output JSON path (default: smoke_test_results.json)")
    args = parser.parse_args()

    results = run_smoke_test(
        n_chains=args.chains,
        n_warmup=args.warmup,
        n_samples=args.samples,
        chain_method=args.chain_method,
        output_path=args.output,
    )

    sys.exit(0 if results["verdict"] == "PASS" else 1)
