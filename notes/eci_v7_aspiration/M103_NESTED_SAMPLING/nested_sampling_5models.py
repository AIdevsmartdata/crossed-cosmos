"""M103 NESTED SAMPLING — 5 cosmological models
Proper Bayesian evidence via dynesty (Speagle 2019, arXiv:1904.02180, MNRAS staa278).

Models:
  1. LCDM          — ndim=3  (H0, obh2, och2)
  2. ECI_NMC       — ndim=5  (H0, obh2, och2, xi, lambda)  [Cassini prior |xi|<0.024]
  3. Wolf_NMC      — ndim=5  (H0, obh2, och2, xi, lambda)  [free xi, |xi|<10]
  4. Karam_Palatini — ndim=6  (H0, obh2, och2, xi, lambda, xi_eff_factor)
  5. DESI_w0wa     — ndim=5  (H0, obh2, och2, w0, wa)

Motivation: M96 NUTS chains had 38-75% divergence rates for BSM models → evidences
unreliable. Nested sampling is divergence-free and yields proper log Z ± σ.

Runtime estimate: ~1-3h per model with nlive=500, 5 models in parallel → ~3h wall-clock.
Hardware: RTX 5060 Ti PC, 20 CPU cores.

Output: /home/remondiere/pc_calcs/ns_{MODEL}_result.pkl for each model.

References:
  - dynesty: Speagle (2019) arXiv:1904.02180, MNRAS staa278
  - Likelihood/prior definitions inherited from c4_v5_overnight.py (M96)
"""

import numpy as np
import pickle
import time
import os
import sys
from multiprocessing import Pool

try:
    import dynesty
    from dynesty import NestedSampler, DynamicNestedSampler
    from dynesty import utils as dyfunc
    print(f"dynesty {dynesty.__version__} loaded", flush=True)
except ImportError:
    raise ImportError("Install dynesty: pip install dynesty  (arXiv:1904.02180)")

# ---------------------------------------------------------------------------
# Physical constants and DESI DR1 data (identical to c4_v5_overnight.py)
# ---------------------------------------------------------------------------
C_LIGHT = 2.998e5  # km/s

DESI_z    = np.array([0.295, 0.510, 0.510, 0.706, 0.706, 0.930, 0.930,
                      1.317, 1.317, 1.491, 1.491, 2.330, 2.330])
DESI_val  = np.array([7.94, 13.59, 21.92, 17.36, 19.86, 21.71, 17.78,
                      27.79, 13.83, 26.07, 14.18, 39.71, 8.52])
DESI_kind = np.array([0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])  # 0=DV, 1=DM, 2=DH
DESI_sig  = np.array([0.075, 0.176, 0.34, 0.146, 0.343, 0.282, 0.310,
                      0.694, 0.395, 0.738, 0.353, 0.876, 0.183])

# ---------------------------------------------------------------------------
# Sound horizon (Aubourg et al. 2015 fitting formula)
# ---------------------------------------------------------------------------
def rd_aubourg15(ombh2, omch2):
    om_nu_h2 = 0.000645
    omcb_h2 = ombh2 + omch2
    return 55.154 * np.exp(-72.3 * (om_nu_h2 + 0.0006)**2) / (
        omcb_h2**0.25351 * ombh2**0.12807)

# ---------------------------------------------------------------------------
# Comoving distance via Simpson integration (numpy, CPU-only — no JAX needed)
# ---------------------------------------------------------------------------
def comoving_distance(z, H_fn, H0, om, extra, n=128):
    """Returns D_C(z) in Mpc using Simpson's rule."""
    z_arr = np.linspace(0.0, z, n + 1)
    integrand = 1.0 / H_fn(z_arr, H0, om, *extra)
    # Simpson weights
    w = np.ones(n + 1)
    w[1:-1:2] = 4.0
    w[2:-2:2] = 2.0
    return C_LIGHT * (z / (3 * n)) * np.dot(w, integrand)

# ---------------------------------------------------------------------------
# Hubble functions — pure numpy, scalar-friendly
# ---------------------------------------------------------------------------
def H_lcdm(z, H0, om):
    return H0 * np.sqrt(om * (1 + z)**3 + (1 - om))

def H_eci(z, H0, om, xi, lam):
    OmL = 1 - om
    Omphi = OmL / (om * (1 + z)**3 + OmL)
    w_eff = -1.0 + (lam**2 / 3.0) * Omphi - (2.0/3.0) * xi * lam**2 * Omphi
    return H0 * np.sqrt(om * (1 + z)**3 + OmL * (1 + z)**(3.0 * (1 + w_eff)))

def H_palatini(z, H0, om, xi, lam, xi_eff_factor):
    OmL = 1 - om
    Omphi = OmL / (om * (1 + z)**3 + OmL)
    xi_pal = xi * xi_eff_factor
    w_eff = -1.0 + (lam**2 / 3.0) * Omphi - (2.0/3.0) * xi_pal * lam**2 * Omphi
    return H0 * np.sqrt(om * (1 + z)**3 + OmL * (1 + z)**(3.0 * (1 + w_eff)))

def H_w0wa(z, H0, om, w0, wa):
    OmL = 1 - om
    a = 1.0 / (1.0 + z)
    rho_de = OmL * a**(-3.0 * (1 + w0 + wa)) * np.exp(-3.0 * wa * (1 - a))
    return H0 * np.sqrt(om * (1 + z)**3 + rho_de)

# ---------------------------------------------------------------------------
# Chi-squared (DESI + BBN prior)
# ---------------------------------------------------------------------------
def chi2_general(theta, H_fn, extra_slice):
    H0, obh2, och2 = theta[0], theta[1], theta[2]
    extra = tuple(theta[extra_slice])
    h = H0 / 100.0
    om = (obh2 + och2) / h**2
    rd = rd_aubourg15(obh2, och2)
    chi = 0.0
    for i in range(13):
        z = DESI_z[i]
        kind = DESI_kind[i]
        DM = comoving_distance(z, H_fn, H0, om, extra)
        DH = C_LIGHT / H_fn(z, H0, om, *extra)
        DV = (DM**2 * z * DH)**(1.0/3.0)
        if kind == 0:
            pred = DV / rd
        elif kind == 1:
            pred = DM / rd
        else:
            pred = DH / rd
        chi += ((DESI_val[i] - pred) / DESI_sig[i])**2
    chi += ((obh2 - 0.0224) / 0.0014)**2  # BBN prior on obh2
    return chi

# ---------------------------------------------------------------------------
# Log-likelihood wrappers (no prior here — priors go in prior_transform)
# ---------------------------------------------------------------------------
def loglike_lcdm(theta):
    try:
        H0, obh2, och2 = theta
        # Sanity guard (extra safety inside likelihood)
        if H0 < 40 or H0 > 100 or obh2 <= 0 or och2 <= 0:
            return -1e30
        return -0.5 * chi2_general(theta, H_lcdm, slice(3, 3))
    except Exception:
        return -1e30

def loglike_eci(theta):
    try:
        return -0.5 * chi2_general(theta, H_eci, slice(3, 5))
    except Exception:
        return -1e30

def loglike_wolf(theta):
    try:
        return -0.5 * chi2_general(theta, H_eci, slice(3, 5))
    except Exception:
        return -1e30

def loglike_palatini(theta):
    try:
        return -0.5 * chi2_general(theta, H_palatini, slice(3, 6))
    except Exception:
        return -1e30

def loglike_w0wa(theta):
    try:
        return -0.5 * chi2_general(theta, H_w0wa, slice(3, 5))
    except Exception:
        return -1e30

# ---------------------------------------------------------------------------
# Prior transforms: unit hypercube [0,1]^n → physical parameter space
# Each prior_transform(u) maps uniform[0,1]^n to the physical prior.
# Flat priors on all parameters (uniform); BBN obh2 Gaussian enters likelihood.
# ---------------------------------------------------------------------------
def prior_lcdm(u):
    """LCDM: H0 in [50,90], obh2 in [0.015,0.030], och2 in [0.080,0.180]"""
    theta = np.empty(3)
    theta[0] = 50.0 + 40.0 * u[0]       # H0
    theta[1] = 0.015 + 0.015 * u[1]     # obh2
    theta[2] = 0.080 + 0.100 * u[2]     # och2
    return theta

def prior_eci(u):
    """ECI-NMC: Cassini-clean |xi|<0.024, lambda in [0,5]"""
    theta = np.empty(5)
    theta[0] = 50.0 + 40.0 * u[0]       # H0
    theta[1] = 0.015 + 0.015 * u[1]     # obh2
    theta[2] = 0.080 + 0.100 * u[2]     # och2
    theta[3] = -0.024 + 0.048 * u[3]    # xi in [-0.024, +0.024] (Cassini)
    theta[4] = 0.0 + 5.0 * u[4]         # lambda in [0, 5]
    return theta

def prior_wolf(u):
    """Wolf-NMC: free xi in [-10, 10], lambda in [0,5]"""
    theta = np.empty(5)
    theta[0] = 50.0 + 40.0 * u[0]       # H0
    theta[1] = 0.015 + 0.015 * u[1]     # obh2
    theta[2] = 0.080 + 0.100 * u[2]     # och2
    theta[3] = -10.0 + 20.0 * u[3]      # xi in [-10, +10] (Wolf: free)
    theta[4] = 0.0 + 5.0 * u[4]         # lambda in [0, 5]
    return theta

def prior_palatini(u):
    """Karam-Palatini: xi in [-10,10], lambda in [0,5], xi_eff in [0,1]"""
    theta = np.empty(6)
    theta[0] = 50.0 + 40.0 * u[0]       # H0
    theta[1] = 0.015 + 0.015 * u[1]     # obh2
    theta[2] = 0.080 + 0.100 * u[2]     # och2
    theta[3] = -10.0 + 20.0 * u[3]      # xi
    theta[4] = 0.0 + 5.0 * u[4]         # lambda
    theta[5] = 0.0 + 1.0 * u[5]         # xi_eff_factor in [0,1]
    return theta

def prior_w0wa(u):
    """DESI w0wa: w0 in [-3,0], wa in [-3,3]"""
    theta = np.empty(5)
    theta[0] = 50.0 + 40.0 * u[0]       # H0
    theta[1] = 0.015 + 0.015 * u[1]     # obh2
    theta[2] = 0.080 + 0.100 * u[2]     # och2
    theta[3] = -3.0 + 3.0 * u[3]        # w0 in [-3, 0]
    theta[4] = -3.0 + 6.0 * u[4]        # wa in [-3, +3]
    return theta

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------
MODELS = [
    {
        "name": "LCDM",
        "ndim": 3,
        "loglike": loglike_lcdm,
        "prior_transform": prior_lcdm,
        "param_names": ["H0", "obh2", "och2"],
        "nlive": 500,
    },
    {
        "name": "ECI_NMC",
        "ndim": 5,
        "loglike": loglike_eci,
        "prior_transform": prior_eci,
        "param_names": ["H0", "obh2", "och2", "xi", "lambda"],
        "nlive": 600,
    },
    {
        "name": "Wolf_NMC",
        "ndim": 5,
        "loglike": loglike_wolf,
        "prior_transform": prior_wolf,
        "param_names": ["H0", "obh2", "och2", "xi", "lambda"],
        "nlive": 600,
    },
    {
        "name": "Karam_Palatini",
        "ndim": 6,
        "loglike": loglike_palatini,
        "prior_transform": prior_palatini,
        "param_names": ["H0", "obh2", "och2", "xi", "lambda", "xi_eff_factor"],
        "nlive": 700,
    },
    {
        "name": "DESI_w0wa",
        "ndim": 5,
        "loglike": loglike_w0wa,
        "prior_transform": prior_w0wa,
        "param_names": ["H0", "obh2", "och2", "w0", "wa"],
        "nlive": 600,
    },
]

# ---------------------------------------------------------------------------
# Worker function for multiprocessing — runs one model
# ---------------------------------------------------------------------------
RESULT_DIR = "/home/remondiere/pc_calcs"

def run_one_model(model_dict):
    """Run nested sampling for one model. Called in subprocess."""
    import signal
    # Ignore SIGINT in workers (parent handles it)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    name = model_dict["name"]
    ndim = model_dict["ndim"]
    loglike = model_dict["loglike"]
    prior_transform = model_dict["prior_transform"]
    param_names = model_dict["param_names"]
    nlive = model_dict["nlive"]

    out_path = os.path.join(RESULT_DIR, f"ns_{name}_result.pkl")

    # Resume if already complete
    if os.path.exists(out_path):
        try:
            with open(out_path, "rb") as f:
                prev = pickle.load(f)
            if prev.get("status") == "complete":
                print(f"[{name}] RESUME: already complete, skipping.", flush=True)
                return prev
        except Exception:
            pass

    print(f"[{name}] Starting nested sampling (nlive={nlive}, ndim={ndim})", flush=True)
    t0 = time.perf_counter()

    try:
        # Use 'multi' (MultiEllipsoid) bounding for efficiency with >3 dims
        # Use 'rwalk' (random walk) sampling — robust for correlated posteriors
        sampler = NestedSampler(
            loglike,
            prior_transform,
            ndim,
            nlive=nlive,
            bound="multi",
            sample="rwalk",
            rstate=np.random.default_rng(42 + ndim),
        )

        # Progress callback: print every 5000 function evaluations
        dlogz_target = 0.01  # convergence threshold
        print_every = 5000   # ncalls between progress prints

        class ProgressPrinter:
            def __init__(self):
                self.last_ncall = 0
            def __call__(self, results_dict):
                ncall = results_dict.get("ncall", 0)
                if ncall - self.last_ncall >= print_every:
                    logz = results_dict.get("logz", float("nan"))
                    logz_err = results_dict.get("logzerr", float("nan"))
                    dlogz = results_dict.get("delta_logz", float("nan"))
                    elapsed = time.perf_counter() - t0
                    print(f"[{name}] ncall={ncall:8d}  logZ={logz:.4f}±{logz_err:.4f}"
                          f"  dlogZ={dlogz:.4f}  elapsed={elapsed:.1f}s", flush=True)
                    self.last_ncall = ncall
                    # Checkpoint
                    ckpt = {
                        "name": name, "status": "running",
                        "ncall": ncall, "logz": float(logz),
                        "logz_err": float(logz_err), "elapsed_sec": float(elapsed),
                    }
                    try:
                        with open(out_path + ".ckpt", "wb") as f:
                            pickle.dump(ckpt, f)
                    except Exception:
                        pass

        pp = ProgressPrinter()

        # Single call — dynesty manages convergence internally via dlogz threshold
        sampler.run_nested(
            dlogz=dlogz_target,
            add_live=True,
            print_progress=False,
        )
        # Print final state
        res_tmp = sampler.results
        elapsed = time.perf_counter() - t0
        print(f"[{name}] CONVERGED: logZ={res_tmp.logz[-1]:.4f}±{res_tmp.logzerr[-1]:.4f}"
              f"  niter={res_tmp.niter}  elapsed={elapsed:.1f}s", flush=True)

        res = sampler.results
        elapsed = time.perf_counter() - t0

        # Extract results
        logz_final = float(res.logz[-1])
        logz_err_final = float(res.logzerr[-1])
        n_iter = int(res.niter)

        # Posterior summary (equal-weight resampling)
        weights = np.exp(res.logwt - res.logz[-1])
        weights /= weights.sum()
        samples = res.samples  # shape (n_iter, ndim)

        posterior_means = {}
        posterior_stds = {}
        posterior_medians = {}
        for i, pname in enumerate(param_names):
            s = samples[:, i]
            posterior_means[pname] = float(np.average(s, weights=weights))
            posterior_stds[pname] = float(
                np.sqrt(np.average((s - posterior_means[pname])**2, weights=weights)))
            # Weighted median via sorted CDF
            sort_idx = np.argsort(s)
            cdf = np.cumsum(weights[sort_idx])
            posterior_medians[pname] = float(s[sort_idx[np.searchsorted(cdf, 0.5)]])

        result = {
            "name": name,
            "status": "complete",
            "logz": logz_final,
            "logz_err": logz_err_final,
            "n_iter": n_iter,
            "nlive": nlive,
            "ndim": ndim,
            "param_names": param_names,
            "elapsed_sec": elapsed,
            "posterior_means": posterior_means,
            "posterior_stds": posterior_stds,
            "posterior_medians": posterior_medians,
            "dynesty_results": res,  # full Results object for further analysis
        }

        with open(out_path, "wb") as f:
            pickle.dump(result, f)

        print(f"[{name}] DONE: logZ = {logz_final:.4f} ± {logz_err_final:.4f}"
              f"  niter={n_iter}  elapsed={elapsed:.1f}s", flush=True)
        print(f"[{name}] Saved to {out_path}", flush=True)

        # Remove checkpoint if it exists
        ckpt_path = out_path + ".ckpt"
        if os.path.exists(ckpt_path):
            os.remove(ckpt_path)

        return result

    except Exception as e:
        import traceback
        elapsed = time.perf_counter() - t0
        tb = traceback.format_exc()
        print(f"[{name}] ERROR after {elapsed:.1f}s: {e}", flush=True)
        print(tb, flush=True)
        err_result = {
            "name": name,
            "status": "error",
            "error": str(e),
            "traceback": tb,
            "elapsed_sec": elapsed,
        }
        with open(out_path + ".error", "wb") as f:
            pickle.dump(err_result, f)
        return err_result

# ---------------------------------------------------------------------------
# Main — run all 5 models in parallel (5 processes, one per model)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70, flush=True)
    print(f"M103 NESTED SAMPLING — 5 models — {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"dynesty {dynesty.__version__}  numpy {np.__version__}", flush=True)
    print(f"Results → {RESULT_DIR}/ns_{{MODEL}}_result.pkl", flush=True)
    print("=" * 70, flush=True)

    # Check which models still need running
    pending = []
    for m in MODELS:
        out_path = os.path.join(RESULT_DIR, f"ns_{m['name']}_result.pkl")
        if os.path.exists(out_path):
            try:
                with open(out_path, "rb") as f:
                    prev = pickle.load(f)
                if prev.get("status") == "complete":
                    logz = prev["logz"]
                    logz_err = prev["logz_err"]
                    print(f"  [{m['name']}] already complete: logZ={logz:.4f}±{logz_err:.4f}", flush=True)
                    continue
            except Exception:
                pass
        pending.append(m)

    if not pending:
        print("All models already complete. Run compute_bayes_factors.py.", flush=True)
        sys.exit(0)

    print(f"\nRunning {len(pending)} models in parallel (up to 5 processes):", flush=True)
    for m in pending:
        print(f"  - {m['name']}  ndim={m['ndim']}  nlive={m['nlive']}", flush=True)
    print(flush=True)

    t_global = time.perf_counter()

    # Use 5 processes (one per model) — each model is CPU-only numpy, safe to fork
    n_procs = min(len(pending), 5)
    with Pool(processes=n_procs) as pool:
        results = pool.map(run_one_model, pending)

    elapsed_total = time.perf_counter() - t_global
    print("\n" + "=" * 70, flush=True)
    print(f"ALL DONE — total elapsed: {elapsed_total:.1f}s = {elapsed_total/3600:.2f}h", flush=True)
    print("=" * 70, flush=True)

    # Quick summary table
    print(f"\n{'Model':<20} {'logZ':>10} {'±err':>8} {'niter':>8} {'elapsed':>10}", flush=True)
    print("-" * 60, flush=True)
    for r in results:
        if r.get("status") == "complete":
            print(f"{r['name']:<20} {r['logz']:>10.4f} {r['logz_err']:>8.4f}"
                  f" {r['n_iter']:>8d} {r['elapsed_sec']:>9.1f}s", flush=True)
        else:
            print(f"{r['name']:<20}  ERROR: {r.get('error','?')[:40]}", flush=True)

    print("\nNext step: python compute_bayes_factors.py", flush=True)
