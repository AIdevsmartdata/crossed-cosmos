"""
M96 — Bridge Sampling for Bayes Factors: 5 cosmological models
===============================================================
ECI v6.0.53 / 2026-05-06

Models:
  1. LCDM            (3 params: H0, obh2, och2)
  2. ECI-NMC Cassini (5 params: + xi, lambda;  |xi| <= 0.024)
  3. Wolf-NMC free   (5 params: + xi, lambda;  |xi| <= 10)
  4. Karam-Palatini  (6 params: + xi, lambda, xi_eff_factor)
  5. DESI w0-wa      (5 params: + w0, wa)

Method: Manual Meng-Wong (1996) iterative bridge sampling.
  - No log_prob stored in chains → reconstruct log-posterior from
    c4_v5_overnight.py likelihood functions (inlined here).
  - Proposal q(θ): Gaussian fit to 2nd half of each chain (training split).
  - Bridge equation (Meng-Wong eq. 2, iterative until |Δlog Z| < 1e-4):
        r_{t+1} = (1/n1) Σ_{i∈chain}  [l(θ_i)π(θ_i) / (s1*l(θ_i)π(θ_i) + s2*Z_t*q(θ_i))]
                / (1/n2) Σ_{j∈q-samples} [q(θ_j) / (s1*l(θ_j)π(θ_j) + s2*Z_t*q(θ_j))]
    where s1 = n1/(n1+n2), s2 = n2/(n1+n2), Z_t = r_t

Numerics: log-space arithmetic throughout; scipy.stats for Gaussian proposal.

Outputs to stdout (redirected to bridge_5models.log by caller).

Note on divergence rates: ECI/Wolf/Karam/DESI chains had 38-75% NUTS
divergences (poor sampler geometry), which reduces bridge sampling reliability.
Flag raised in output table.

Reference: Meng, X.-L. & Wong, W. H. (1996), Statistica Sinica 6, 831-860.
"""

from __future__ import annotations
import time
import json
import sys
import numpy as np
from scipy.stats import multivariate_normal
from scipy.special import logsumexp

CHAINS_DIR = "/home/remondiere/pc_calcs"
RESULTS_JSON = f"{CHAINS_DIR}/c4_v5_overnight_results.json"

# ─────────────────────────────────────────────────────────────────────────────
# Reproduce likelihood from c4_v5_overnight.py (pure numpy, no JAX needed)
# ─────────────────────────────────────────────────────────────────────────────
C_LIGHT = 2.998e5

# DESI DR2 BAO data (from c4_v5_overnight.py)
DESI_z   = np.array([0.295, 0.510, 0.510, 0.706, 0.706, 0.930, 0.930,
                     1.317, 1.317, 1.491, 1.491, 2.330, 2.330])
DESI_val = np.array([7.94, 13.59, 21.92, 17.36, 19.86, 21.71, 17.78,
                     27.79, 13.83, 26.07, 14.18, 39.71, 8.52])
DESI_kind = np.array([0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])  # DV=0,DM=1,DH=2
DESI_sig  = np.array([0.075, 0.176, 0.34, 0.146, 0.343, 0.282, 0.310,
                      0.694, 0.395, 0.738, 0.353, 0.876, 0.183])


def rd_aubourg15(ombh2: float, omch2: float) -> float:
    """Sound horizon via Aubourg+2015 eq.16 with ν correction."""
    om_nu_h2 = 0.000645
    omcb_h2 = ombh2 + omch2
    return 55.154 * np.exp(-72.3 * (om_nu_h2 + 0.0006)**2) / (
        omcb_h2**0.25351 * ombh2**0.12807
    )


def _comoving(z: float, H0: float, om: float, H_fn, *extra, n: int = 64) -> float:
    z_grid = np.linspace(0.0, z, n + 1)
    Hg = H_fn(z_grid, H0, om, *extra)
    weights = np.ones(n + 1)
    weights[1:-1:2] = 4.0
    weights[2:-1:2] = 2.0
    weights[0] = weights[-1] = 1.0
    return C_LIGHT * (z / (3 * n)) * np.sum(weights / Hg)


def bao_chi2(theta: np.ndarray, H_fn, n_extra: int) -> float:
    H0, obh2, och2 = theta[0], theta[1], theta[2]
    extra = tuple(theta[3 + i] for i in range(n_extra))
    h = H0 / 100.0
    om = (obh2 + och2) / h**2
    rd = rd_aubourg15(obh2, och2)
    chi = 0.0
    for i in range(len(DESI_z)):
        z = DESI_z[i]
        kind = DESI_kind[i]
        DM = _comoving(z, H0, om, H_fn, *extra)
        DH = C_LIGHT / H_fn(np.array([z]), H0, om, *extra)[0]
        DV = (DM**2 * z * DH)**(1.0 / 3.0)
        pred = {0: DV / rd, 1: DM / rd, 2: DH / rd}[kind]
        chi += ((DESI_val[i] - pred) / DESI_sig[i])**2
    # BBN prior
    chi += ((obh2 - 0.0224) / 0.0014)**2
    return float(chi)


# ── H(z) functions ────────────────────────────────────────────────────────────

def H_lcdm(z, H0, om):
    return H0 * np.sqrt(om * (1.0 + z)**3 + (1.0 - om))


def H_eci(z, H0, om, xi, lam):
    OmL = 1.0 - om
    Omphi = OmL / (om * (1.0 + z)**3 + OmL)
    w_eff = -1.0 + (lam**2 / 3.0) * Omphi - (2.0 / 3.0) * xi * lam**2 * Omphi
    return H0 * np.sqrt(om * (1.0 + z)**3 + OmL * (1.0 + z)**(3.0 * (1.0 + w_eff)))


def H_palatini(z, H0, om, xi, lam, xi_eff_factor):
    OmL = 1.0 - om
    Omphi = OmL / (om * (1.0 + z)**3 + OmL)
    xi_palatini = xi * xi_eff_factor
    w_eff = -1.0 + (lam**2 / 3.0) * Omphi - (2.0 / 3.0) * xi_palatini * lam**2 * Omphi
    return H0 * np.sqrt(om * (1.0 + z)**3 + OmL * (1.0 + z)**(3.0 * (1.0 + w_eff)))


def H_w0wa(z, H0, om, w0, wa):
    OmL = 1.0 - om
    a = 1.0 / (1.0 + z)
    rho_de = OmL * a**(-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
    return H0 * np.sqrt(om * (1.0 + z)**3 + rho_de)


# ── Prior checks (return True if OUTSIDE prior) ──────────────────────────────

def prior_bad_base(theta: np.ndarray) -> bool:
    H0, obh2, och2 = theta[0], theta[1], theta[2]
    return bool((H0 < 50) or (H0 > 90) or
                (obh2 < 0.015) or (obh2 > 0.030) or
                (och2 < 0.08) or (och2 > 0.18))


PRIOR_EXTRA = {
    "LCDM":           lambda *e: False,
    "ECI_NMC_Cassini": lambda xi, lam: (abs(xi) > 0.024) or (lam < 0) or (lam > 5),
    "Wolf_NMC_free":   lambda xi, lam: (abs(xi) > 10) or (lam < 0) or (lam > 5),
    "Karam_Palatini":  lambda xi, lam, xief: (abs(xi) > 10) or (lam < 0) or (lam > 5) or (xief < 0) or (xief > 1),
    "DESI_w0wa":       lambda w0, wa: (w0 < -3) or (w0 > 0) or (abs(wa) > 3),
}

H_FNS = {
    "LCDM":           (H_lcdm, 0),
    "ECI_NMC_Cassini": (H_eci, 2),
    "Wolf_NMC_free":   (H_eci, 2),
    "Karam_Palatini":  (H_palatini, 3),
    "DESI_w0wa":       (H_w0wa, 2),
}

PARAM_NAMES = {
    "LCDM":           ["H0", "obh2", "och2"],
    "ECI_NMC_Cassini": ["H0", "obh2", "och2", "xi", "lambda"],
    "Wolf_NMC_free":   ["H0", "obh2", "och2", "xi", "lambda"],
    "Karam_Palatini":  ["H0", "obh2", "och2", "xi", "lambda", "xi_eff_factor"],
    "DESI_w0wa":       ["H0", "obh2", "och2", "w0", "wa"],
}

CHAIN_FILES = {
    "LCDM":           "c4_v5_lcdm_chain.npz",
    "ECI_NMC_Cassini": "c4_v5_eci_nmc_cassini_chain.npz",
    "Wolf_NMC_free":   "c4_v5_wolf_nmc_free_chain.npz",
    "Karam_Palatini":  "c4_v5_karam_palatini_chain.npz",
    "DESI_w0wa":       "c4_v5_desi_w0wa_chain.npz",
}


def log_prior_volume(name: str) -> float:
    """log(volume of prior box) = Σ log(Δθ_i). Flat uniform priors."""
    # Base: H0 (40), obh2 (0.015), och2 (0.10)
    log_vol = np.log(40.0) + np.log(0.015) + np.log(0.10)
    extras = {
        "LCDM":            0.0,
        "ECI_NMC_Cassini": np.log(0.048) + np.log(5.0),   # xi in [-0.024,0.024], lam in [0,5]
        "Wolf_NMC_free":   np.log(20.0)  + np.log(5.0),   # xi in [-10,10], lam in [0,5]
        "Karam_Palatini":  np.log(20.0)  + np.log(5.0) + np.log(1.0),  # +xi_eff in [0,1]
        "DESI_w0wa":       np.log(3.0)   + np.log(6.0),   # w0 in [-3,0], wa in [-3,3]
    }
    return log_vol + extras[name]


def make_logpost(name: str):
    """Return vectorised log-posterior function (per sample, scalar output)."""
    H_fn, n_extra = H_FNS[name]
    prior_extra = PRIOR_EXTRA[name]
    lv = log_prior_volume(name)  # normalisation: -log(prior volume) enters

    def logpost_single(theta: np.ndarray) -> float:
        if prior_bad_base(theta):
            return -np.inf
        extra = tuple(theta[3 + i] for i in range(n_extra))
        if prior_extra(*extra):
            return -np.inf
        try:
            chi2 = bao_chi2(theta, H_fn, n_extra)
            if not np.isfinite(chi2):
                return -np.inf
            return float(-0.5 * chi2) - lv  # log(L * pi) where pi = 1/V_prior
        except Exception:
            return -np.inf

    def logpost_batch(samples: np.ndarray) -> np.ndarray:
        out = np.empty(len(samples))
        for i, s in enumerate(samples):
            out[i] = logpost_single(s)
        return out

    return logpost_batch


# ─────────────────────────────────────────────────────────────────────────────
# Bridge sampling — Meng-Wong (1996) iterative estimator
# ─────────────────────────────────────────────────────────────────────────────

def fit_gaussian_proposal(samples: np.ndarray) -> multivariate_normal:
    """Fit multivariate Gaussian to samples (for proposal density q)."""
    mu = samples.mean(axis=0)
    cov = np.cov(samples.T)
    if samples.shape[1] == 1:
        cov = np.array([[cov]])
    # Regularise for numerical stability
    cov += np.eye(cov.shape[0]) * 1e-8
    return multivariate_normal(mean=mu, cov=cov, allow_singular=False)


def bridge_sampling(
    chain: np.ndarray,
    logpost_fn,
    n_proposal_samples: int = 50000,
    n_iter: int = 1000,
    tol: float = 1e-4,
    rng_seed: int = 42,
) -> dict:
    """
    Meng-Wong (1996) iterative bridge sampling for log Z.

    Split chain: 1st half = test set (E_chain estimates), 2nd half = train set
    (fit proposal q). Draw n_proposal_samples from q.

    Returns dict with log_Z, se_log_Z, n_iter_converged.
    """
    rng = np.random.default_rng(rng_seed)
    n = len(chain)
    n1 = n // 2          # chain test set
    n2 = n_proposal_samples

    # Training split: fit proposal
    train_samples = chain[n // 2:]
    test_samples  = chain[:n // 2]

    print(f"  Fitting Gaussian proposal on {len(train_samples)} samples...", flush=True)
    proposal = fit_gaussian_proposal(train_samples)

    # Draw from proposal
    print(f"  Drawing {n2} samples from proposal...", flush=True)
    q_samples = proposal.rvs(size=n2, random_state=rng)
    if q_samples.ndim == 1:
        q_samples = q_samples[:, None]

    # Evaluate log-posteriors
    print(f"  Evaluating log-posterior on {n1} chain samples...", flush=True)
    t0 = time.time()
    lp_chain = logpost_fn(test_samples)     # (n1,)
    print(f"    Done in {time.time()-t0:.1f}s; finite={np.isfinite(lp_chain).sum()}/{n1}", flush=True)

    print(f"  Evaluating log-posterior on {n2} proposal samples...", flush=True)
    t0 = time.time()
    lp_q = logpost_fn(q_samples)            # (n2,)
    print(f"    Done in {time.time()-t0:.1f}s; finite={np.isfinite(lp_q).sum()}/{n2}", flush=True)

    # Proposal log-density
    lq_chain = proposal.logpdf(test_samples)  # log q(θ) for chain samples
    lq_q     = proposal.logpdf(q_samples)     # log q(θ) for proposal samples

    # Remove infs from logpost
    valid_chain = np.isfinite(lp_chain)
    valid_q     = np.isfinite(lp_q)
    n1_eff = valid_chain.sum()
    n2_eff = valid_q.sum()

    if n1_eff < 100 or n2_eff < 100:
        return {"log_Z": np.nan, "se_log_Z": np.nan, "n_iter": 0,
                "note": f"Too few finite logpost values: chain={n1_eff}, q={n2_eff}"}

    lp_chain = lp_chain[valid_chain]
    lq_chain = lq_chain[valid_chain]
    lp_q     = lp_q[valid_q]
    lq_q     = lq_q[valid_q]

    # Meng-Wong iterative bridge equation (log-space)
    # s1 = n1/(n1+n2), s2 = n2/(n1+n2) — importance weights
    s1 = n1_eff / (n1_eff + n2_eff)
    s2 = n2_eff / (n1_eff + n2_eff)

    log_Z = 0.0  # initial estimate

    for it in range(n_iter):
        # Numerator:   (1/n1) Σ_{chain} lp(θ) / [s1*lp(θ)*pi + s2*Z*q(θ)]
        # In log:  lp_chain - log(s1*exp(lp_chain) + s2*exp(log_Z + lq_chain))
        log_num_terms = lp_chain - np.logaddexp(
            np.log(s1) + lp_chain,
            np.log(s2) + log_Z + lq_chain
        )
        log_num = logsumexp(log_num_terms) - np.log(n1_eff)

        # Denominator: (1/n2) Σ_{q} q(θ) / [s1*lp(θ)*pi + s2*Z*q(θ)]
        # = (1/n2) Σ exp(lq_q - log(...))
        log_den_terms = lq_q - np.logaddexp(
            np.log(s1) + lp_q,
            np.log(s2) + log_Z + lq_q
        )
        log_den = logsumexp(log_den_terms) - np.log(n2_eff)

        log_Z_new = log_num - log_den

        delta = abs(log_Z_new - log_Z)
        log_Z = log_Z_new

        if it < 5 or it % 50 == 0:
            print(f"    iter {it:4d}: log Z = {log_Z:.4f} (delta={delta:.2e})", flush=True)
        if delta < tol:
            print(f"    Converged at iter {it} (delta={delta:.2e})", flush=True)
            break

    # Bootstrap SE estimate (50 bootstrap resamples for speed)
    se_estimates = []
    for _ in range(50):
        idx_c = rng.integers(0, n1_eff, size=n1_eff)
        idx_q = rng.integers(0, n2_eff, size=n2_eff)
        lpc_b = lp_chain[idx_c]; lqc_b = lq_chain[idx_c]
        lpq_b = lp_q[idx_q];     lqq_b = lq_q[idx_q]
        log_Z_b = log_Z
        for _ in range(30):
            lnum = logsumexp(lpc_b - np.logaddexp(np.log(s1)+lpc_b, np.log(s2)+log_Z_b+lqc_b)) - np.log(n1_eff)
            lden = logsumexp(lqq_b - np.logaddexp(np.log(s1)+lpq_b, np.log(s2)+log_Z_b+lqq_b)) - np.log(n2_eff)
            log_Z_b = lnum - lden
        se_estimates.append(log_Z_b)
    se_log_Z = float(np.std(se_estimates))

    return {
        "log_Z": float(log_Z),
        "se_log_Z": se_log_Z,
        "n_iter": it + 1,
        "n1_eff": int(n1_eff),
        "n2_eff": int(n2_eff),
        "note": "OK",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("M96 — Bridge Sampling Bayes Factors: 5 Cosmological Models")
    print(f"Run date: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 70)

    # Load overnight results for divergence rate info
    with open(RESULTS_JSON) as f:
        overnight = json.load(f)

    model_names = [
        "LCDM", "ECI_NMC_Cassini", "Wolf_NMC_free", "Karam_Palatini", "DESI_w0wa"
    ]
    # Friendly names
    display_names = {
        "LCDM":           "ΛCDM",
        "ECI_NMC_Cassini": "ECI-NMC (Cassini)",
        "Wolf_NMC_free":   "Wolf-NMC (free ξ)",
        "Karam_Palatini":  "Karam-Palatini",
        "DESI_w0wa":       "DESI w₀wₐ",
    }

    results = {}

    for name in model_names:
        print(f"\n{'─'*60}")
        print(f"MODEL: {display_names[name]}  ({name})")
        print(f"{'─'*60}")

        # Load chain
        chain_path = f"{CHAINS_DIR}/{CHAIN_FILES[name]}"
        chain = np.load(chain_path)["samples"]
        div_rate = overnight.get(name, {}).get("div_rate_pct", float("nan"))
        print(f"  Chain: {chain.shape}, divergence rate: {div_rate:.1f}%")

        # Build logposterior
        logpost_fn = make_logpost(name)

        # Run bridge sampling
        print(f"  Starting bridge sampling...", flush=True)
        t0 = time.time()
        bs = bridge_sampling(chain, logpost_fn, n_proposal_samples=20000)
        elapsed = time.time() - t0
        print(f"  Elapsed: {elapsed:.1f}s")
        print(f"  log Z = {bs['log_Z']:.4f} ± {bs['se_log_Z']:.4f}  [{bs.get('note','')}]")

        results[name] = {
            "display_name": display_names[name],
            "log_Z": bs["log_Z"],
            "se_log_Z": bs["se_log_Z"],
            "n_iter": bs.get("n_iter", 0),
            "n1_eff": bs.get("n1_eff", 0),
            "n2_eff": bs.get("n2_eff", 0),
            "div_rate_pct": div_rate,
            "note": bs.get("note", ""),
            "n_params": chain.shape[1],
        }

    # ── Summary table ────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY: log Z (evidence) per model")
    print("=" * 70)
    lz_ref = results["LCDM"]["log_Z"]
    print(f"{'Model':<22} {'log Z':>10} {'±':>6} {'2Δln BF':>10} {'Jeffreys':>12} {'div%':>6} {'warn':>6}")
    print("-" * 70)
    for name in model_names:
        r = results[name]
        lz = r["log_Z"]
        se = r["se_log_Z"]
        # 2 * ln BF relative to ΛCDM
        two_delta_lnBF = 2.0 * (lz - lz_ref)
        # Jeffreys scale for |ln BF|
        lnBF = lz - lz_ref
        if abs(lnBF) < 1.0:
            jeff = "inconclusive"
        elif abs(lnBF) < 2.5:
            jeff = "weak"
        elif abs(lnBF) < 5.0:
            jeff = "moderate"
        else:
            jeff = "strong"
        warn = "DIVERG" if r["div_rate_pct"] > 30 else ""
        print(f"{r['display_name']:<22} {lz:>10.3f} {se:>6.3f} {two_delta_lnBF:>10.3f} {jeff:>12} {r['div_rate_pct']:>6.1f} {warn:>6}")

    print("\nBayes Factors BF(M / ΛCDM) = exp(log Z_M - log Z_ΛCDM):")
    print(f"{'Model':<22} {'ln BF':>10} {'BF':>12} {'Interpretation'}")
    print("-" * 70)
    for name in model_names[1:]:
        r = results[name]
        lnBF = r["log_Z"] - lz_ref
        BF = np.exp(np.clip(lnBF, -100, 100))
        if abs(lnBF) < 1.0:
            interp = "inconclusive"
        elif lnBF > 0:
            interp = f"favours {r['display_name']}" if abs(lnBF) >= 1.0 else "inconclusive"
        else:
            interp = "favours ΛCDM"
        print(f"{r['display_name']:<22} {lnBF:>10.3f} {BF:>12.4f}  {interp}")

    # ── Parameter constraints ─────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("POSTERIOR PARAMETER CONSTRAINTS (mean ± std, from overnight_results.json)")
    print("=" * 70)
    for name in model_names:
        r_on = overnight.get(name, {})
        print(f"\n{display_names[name]} ({name}, div={r_on.get('div_rate_pct',0):.1f}%):")
        for pname, pval in r_on.get("posteriors", {}).items():
            print(f"  {pname:18s}: {pval['mean']:.5g} ± {pval['std']:.5g}  "
                  f"[{pval['p16']:.5g}, {pval['p84']:.5g}]")

    # ── Save results JSON ─────────────────────────────────────────────────────
    out_path = "/home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M96_BAYES_FACTORS/bridge_results.json"
    import os
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[saved] {out_path}")

    print("\n[done] M96 bridge sampling complete.")
    return results


if __name__ == "__main__":
    main()
