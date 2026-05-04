"""C4 10-model joint MCMC template — RTX 5060 Ti 16GB GDDR7
Uses jax + blackjax NUTS. Theory backend = TODO (cosmopower-jax 0.5.5 incompat
JAX 0.10, needs patch OR emulator retrain OR CAMB CPU fallback).

Bench (2026-05-04): blackjax NUTS 5-param Gaussian = 575 samples/sec, 0% diverg.

Run: python3 gpu_nuts_template.py
"""
import jax, jax.numpy as jnp
import blackjax
import numpy as np
import time, json, sys

print(f"JAX {jax.__version__}, devices={jax.devices()}, backend={jax.default_backend()}")

# ──────────── PDG / data ────────────
# Placeholder cosmology likelihood; replace with cosmopower-jax + DESI/Pantheon+ emulator
PDG = dict(H0=68.0, sig_H0=1.5, omegabh2=0.0224, sig_obh2=0.0001,
           omegach2=0.120, sig_och2=0.001, S8=0.815, sig_S8=0.0185)

@jax.jit
def logp_lcdm_placeholder(theta):
    """3-param ΛCDM toy: theta = [H0, omegabh2, omegach2]"""
    H0, obh2, och2 = theta
    chi2 = ((H0 - PDG["H0"]) / PDG["sig_H0"])**2
    chi2 += ((obh2 - PDG["omegabh2"]) / PDG["sig_obh2"])**2
    chi2 += ((och2 - PDG["omegach2"]) / PDG["sig_och2"])**2
    # Derived S8 placeholder (not real cosmology)
    S8_derived = 0.815 + 0.5 * (och2 - 0.12)
    chi2 += ((S8_derived - PDG["S8"]) / PDG["sig_S8"])**2
    return -0.5 * chi2

def run_nuts(logp_fn, init, nwarm=1000, nsamples=3000, seed=42,
             target_accept=0.85):
    key = jax.random.PRNGKey(seed)
    warmup = blackjax.window_adaptation(blackjax.nuts, logp_fn,
                                        target_acceptance_rate=target_accept)
    (state, params), _ = warmup.run(key, init, num_steps=nwarm)
    kernel = blackjax.nuts(logp_fn, **params).step

    @jax.jit
    def step(carry, key):
        state = carry
        state, info = kernel(key, state)
        return state, (state, info)

    keys = jax.random.split(jax.random.fold_in(key, 1), nsamples)
    state_final, (states, infos) = jax.lax.scan(step, state, keys)
    state_final.position.block_until_ready()
    return states, infos

if __name__ == "__main__":
    init = jnp.array([68.0, 0.0224, 0.120])
    print("Running 3-param ΛCDM placeholder NUTS (warmup=1000, samples=3000)...")
    t0 = time.perf_counter()
    states, infos = run_nuts(logp_lcdm_placeholder, init, nwarm=1000, nsamples=3000)
    elapsed = time.perf_counter() - t0

    samples = np.asarray(states.position)
    print(f"  Total time: {elapsed:.2f}s = {3000/elapsed:.0f} samples/sec")
    print(f"  Divergences: {jnp.sum(infos.is_divergent).item()}/{3000}")
    print(f"  H0      = {samples[:,0].mean():.3f} ± {samples[:,0].std():.3f}")
    print(f"  omegabh2 = {samples[:,1].mean():.5f} ± {samples[:,1].std():.5f}")
    print(f"  omegach2 = {samples[:,2].mean():.5f} ± {samples[:,2].std():.5f}")

# TODO for C4 production:
# 1. Replace logp_lcdm_placeholder with real cosmology likelihood
#    Options: (a) patch cosmopower-jax for JAX 0.10 named_shape removal,
#             (b) downgrade jax to ≤0.4.36 (may break other deps),
#             (c) use CAMB CPU theory + classy interface (slower)
# 2. Add 9 more model variants: NMC, EDE, CDE, DHOST, ...
# 3. Integrate DESI DR2 BAO + Pantheon+ + KiDS-Legacy likelihoods
# 4. Compute Bayes evidence via ratio of marginal likelihoods (requires nested sampling, e.g. blackjax-ssm)
# 5. Save chain + posteriors to .npz for getdist analysis
