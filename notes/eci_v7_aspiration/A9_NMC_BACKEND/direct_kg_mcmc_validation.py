"""
A9 — Direct-KG MCMC validation (no emulator needed)

Validates the *physics fix* — independent of cosmopower-jax — by running a
classical Metropolis MCMC where each likelihood evaluation calls the actual
Klein-Gordon ODE integrator. Slow (≈0.1 s/sample × 5000 samples = 8 min)
but uses zero machine learning. Pure numerical verdict on whether the
H0 ≈ 64-65 artefact in C4 v5 OVERNIGHT was caused by the closed-form w(z).

Comparison protocol:
  1. SAME data: DESI DR2 BAO LRG2 (z=0.51) + BBN ω_b h².
  2. SAME prior box: xi ∈ [-0.10, 0.10], lam ∈ [0.05, 3.0], etc.
  3. RUN: H_KG = direct KG; H_closed = C4 v5 OVERNIGHT closed-form (re-implemented here).
  4. COMPARE: ECI_NMC posterior on H0 from each.

If H_KG > 66.5: ARTEFACT RESOLVED (closed-form w(z) was the bug).
If H_KG ≈ 64-65: NOT THE CULPRIT (problem is in BAO data interpretation).

Output: /home/remondiere/pc_calcs/cosmopower_nmc_emulator/direct_kg_validation.json
        OR /tmp/direct_kg_validation.json if PC dir absent.

Author: A9, ECI v6.0.53.1, 2026-05-05.
"""
import os, sys, time, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nmc_kg_backend import solve_kg, Z_GRID, N_Z

# -------------------------------------------------------------------
# DESI DR2 BAO LRG2 (z=0.51) — from arXiv:2503.14738 Table I
# Same as in C4 v5 OVERNIGHT.
# -------------------------------------------------------------------
Z_BAO = 0.51
DM_RD_OBS, DM_RD_ERR = 13.62, 0.25
DH_RD_OBS, DH_RD_ERR = 20.98, 0.61
OBH2_BBN, OBH2_ERR = 0.0224, 0.0005
OR_H2 = 4.18e-5
C_KMS = 2.998e5

def r_d_eisenstein_hu(obh2, oc_h2):
    om_h2 = obh2 + oc_h2
    return 55.154 * np.exp(-72.3 * 0.0006**2) / obh2**0.12807 / om_h2**0.25351


# -------------------------------------------------------------------
# Closed-form w(z) (Wolf-CPL approximation as used in C4 v5 OVERNIGHT)
#   w(a) = -1 + (lam²/3) Ω_φ(a) + (2/3) ξ λ χ(a)/M_P
# with χ(a) ≈ χ_0 + λ Ω_φ,0 (a-1)  [linearised around a=1]
# H(z) computed from algebraic Friedmann assuming Ω_φ closure.
# This implementation reproduces C4 v5 OVERNIGHT's reasoning (artefact source).
# -------------------------------------------------------------------
def closed_form_H_w(theta):
    xi, lam, phi0, ob_h2, oc_h2, h = theta
    om_h2 = ob_h2 + oc_h2
    Om = om_h2 / h**2
    Or = OR_H2 / h**2
    Ophi0 = 1.0 - Om - Or
    if Ophi0 < 0.05:
        return None, None
    a = 1.0 / (1.0 + Z_GRID)
    # Closed-form Ω_φ(a): (very crude; what C4 v5 used)
    # Solve x²(a) = Ω_m a^-3 + Ω_r a^-4 + Ω_φ * (rho_φ(a)/rho_φ0)
    # where rho_φ(a)/rho_φ0 = exp[3 ∫_a^1 (1+w(a'))/a' da']
    # For thawing w ≈ -1 + small, take rho_φ(a)/rho_φ0 ≈ a^{-3(1+w0)} (CPL extrapolation)
    chi_a = phi0 + lam * Ophi0 * (a - 1.0)
    w_a = -1.0 + (lam**2 / 3.0) * Ophi0 + (2.0/3.0) * xi * lam * chi_a
    w0 = w_a[0]
    rho_phi_ratio = a**(-3 * (1.0 + w0))
    x2 = Om * a**(-3) + Or * a**(-4) + Ophi0 * rho_phi_ratio
    H_arr = np.sqrt(x2) * h * 100.0
    return H_arr, w_a


# -------------------------------------------------------------------
# Likelihood (works for both modes)
# -------------------------------------------------------------------
def loglike_from_Hw(H_arr, w_arr, theta):
    if H_arr is None or np.any(~np.isfinite(H_arr)) or H_arr[0] < 30 or H_arr[0] > 100:
        return -1e10
    xi, lam, phi0, ob_h2, oc_h2, h = theta
    # Comoving distance to z_BAO via trapezoidal integration on Z_GRID
    invH = 1.0 / H_arr
    dz = np.diff(Z_GRID)
    seg = 0.5 * (invH[1:] + invH[:-1]) * dz
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    d_M = C_KMS * np.interp(Z_BAO, Z_GRID, cum)
    H_at = np.interp(Z_BAO, Z_GRID, H_arr)
    d_H = C_KMS / H_at
    r_d = r_d_eisenstein_hu(ob_h2, oc_h2)
    chi2 = ((d_M / r_d - DM_RD_OBS) / DM_RD_ERR) ** 2
    chi2 += ((d_H / r_d - DH_RD_OBS) / DH_RD_ERR) ** 2
    chi2 += ((ob_h2 - OBH2_BBN) / OBH2_ERR) ** 2
    return -0.5 * chi2


def logprior(theta):
    xi, lam, phi0, ob_h2, oc_h2, h = theta
    if not (-0.10 < xi < 0.10): return -np.inf
    if not (0.05 < lam < 3.0): return -np.inf
    if not (0.01 < phi0 < 0.30): return -np.inf
    if not (0.018 < ob_h2 < 0.026): return -np.inf
    if not (0.095 < oc_h2 < 0.140): return -np.inf
    if not (0.55 < h < 0.80): return -np.inf
    return 0.0


def logpost_kg(theta):
    if not np.isfinite(logprior(theta)):
        return -np.inf
    xi, lam, phi0, ob_h2, oc_h2, h = theta
    om_h2 = ob_h2 + oc_h2
    try:
        _, w, H, ok, _ = solve_kg(xi, lam, phi0, om_h2, OR_H2, h)
        if not ok:
            return -1e10
    except Exception:
        return -1e10
    return loglike_from_Hw(H, w, theta)


def logpost_closed(theta):
    if not np.isfinite(logprior(theta)):
        return -np.inf
    H, w = closed_form_H_w(theta)
    return loglike_from_Hw(H, w, theta)


# -------------------------------------------------------------------
# Adaptive Metropolis MCMC (numpy only, no JAX)
# -------------------------------------------------------------------
def run_metropolis(logpost_fn, init, n_samples=5000, n_burn=1500, seed=20260505,
                   prop_scale=None, label=""):
    rng = np.random.default_rng(seed)
    if prop_scale is None:
        prop_scale = np.array([0.005, 0.10, 0.02, 0.0005, 0.003, 0.015])
    chain = np.zeros((n_samples, 6))
    cur = np.array(init)
    cur_lp = logpost_fn(cur)
    if not np.isfinite(cur_lp):
        raise ValueError(f"[{label}] init not in support")
    n_accept = 0
    n_total = 0
    t0 = time.perf_counter()
    last_print = t0
    # Adapt proposal during burn-in
    for i in range(n_burn + n_samples):
        prop = cur + rng.normal(size=6) * prop_scale
        prop_lp = logpost_fn(prop)
        n_total += 1
        if np.log(rng.random()) < prop_lp - cur_lp:
            cur = prop
            cur_lp = prop_lp
            n_accept += 1
        if i >= n_burn:
            chain[i - n_burn] = cur
        # Adaptive scaling during burn
        if i < n_burn and (i + 1) % 200 == 0:
            acc = n_accept / n_total
            if acc < 0.15: prop_scale *= 0.7
            elif acc > 0.45: prop_scale *= 1.3
            n_accept = 0; n_total = 0
        if time.perf_counter() - last_print > 30:
            elapsed = time.perf_counter() - t0
            done = i + 1
            total = n_burn + n_samples
            print(f"  [{label}][{time.strftime('%H:%M:%S')}] {done}/{total} "
                  f"acc={n_accept/max(n_total,1):.2f} "
                  f"rate={done/elapsed:.1f}/s "
                  f"ETA={(total-done)/max(done/elapsed,1e-6)/60:.1f}min", flush=True)
            last_print = time.perf_counter()
    return chain


def summarise(chain, name):
    names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]
    summary = {}
    print(f"\n[{name}] Posterior summary:")
    for i, p in enumerate(names):
        m = float(np.mean(chain[:, i]))
        s = float(np.std(chain[:, i]))
        p16 = float(np.percentile(chain[:, i], 16))
        p84 = float(np.percentile(chain[:, i], 84))
        summary[p] = {"mean": m, "std": s, "p16": p16, "p84": p84}
        print(f"  {p:>15}: {m:9.5f} ± {s:8.5f}  [{p16:9.5f}, {p84:9.5f}]")
    H0 = chain[:, -1] * 100
    summary["H0_kmsMpc"] = {
        "mean": float(H0.mean()), "std": float(H0.std()),
        "p16": float(np.percentile(H0, 16)), "p84": float(np.percentile(H0, 84))
    }
    print(f"  {'H0_kmsMpc':>15}: {H0.mean():9.3f} ± {H0.std():8.3f} "
          f"[{np.percentile(H0,16):9.3f}, {np.percentile(H0,84):9.3f}]")
    return summary


def main():
    print(f"[{time.strftime('%H:%M:%S')}] A9 Direct-KG validation MCMC")
    print(f"  Data: DESI DR2 BAO LRG2 (z=0.51) + BBN ω_b h²")
    print(f"  Model: ECI_NMC (xi, lambda, phi0, omega_b_h2, omega_c_h2, h)")
    print(f"  N_samples=4000 + 1200 burn  (each mode)")

    init = [0.0, 1.0, 0.10, 0.0224, 0.120, 0.67]

    print(f"\n--- MODE 1: closed-form w(z) (C4 v5 OVERNIGHT replication) ---")
    t0 = time.perf_counter()
    chain_closed = run_metropolis(logpost_closed, init,
                                   n_samples=4000, n_burn=1200,
                                   label="closed", seed=20260505)
    t_closed = time.perf_counter() - t0
    sum_closed = summarise(chain_closed, "CLOSED-FORM")
    print(f"  Time: {t_closed:.1f}s")

    print(f"\n--- MODE 2: full Klein-Gordon backend ---")
    t0 = time.perf_counter()
    chain_kg = run_metropolis(logpost_kg, init,
                              n_samples=4000, n_burn=1200,
                              label="KG", seed=20260505)
    t_kg = time.perf_counter() - t0
    sum_kg = summarise(chain_kg, "KG-BACKEND")
    print(f"  Time: {t_kg:.1f}s")

    # Compare
    print(f"\n=== HEAD-TO-HEAD H₀ COMPARISON ===")
    h0_closed = sum_closed["H0_kmsMpc"]["mean"]
    h0_kg     = sum_kg["H0_kmsMpc"]["mean"]
    s_closed  = sum_closed["H0_kmsMpc"]["std"]
    s_kg      = sum_kg["H0_kmsMpc"]["std"]
    print(f"  Closed-form: H₀ = {h0_closed:.2f} ± {s_closed:.2f} km/s/Mpc")
    print(f"  KG backend:  H₀ = {h0_kg:.2f} ± {s_kg:.2f} km/s/Mpc")
    print(f"  ΔH₀ = {h0_kg - h0_closed:+.2f} km/s/Mpc")
    print(f"  C4 v5 OVERNIGHT (reference): H₀_ECI_NMC = 64.04 ± 2.95 km/s/Mpc")

    if h0_kg > 66.5 and h0_closed < 66.0:
        verdict = "ARTEFACT RESOLVED — KG recovers H₀≈67-69, closed-form gave artefactual ≈64-65"
    elif abs(h0_kg - h0_closed) < 1.0:
        verdict = ("ARTEFACT NOT FROM CLOSED-FORM — both methods give similar H₀; "
                   "the BAO subset itself prefers low H₀, full DESI+SN+CMB needed")
    elif h0_kg > 66.5:
        verdict = ("PARTIAL RESOLUTION — KG H₀ in expected range; closed-form had "
                   "compounding bias from poor w(z)+H(z) coupling")
    else:
        verdict = ("UNCLEAR — neither method recovers ≈67-69; deeper data investigation")
    print(f"\nVERDICT: {verdict}")

    out = {
        "version": "A9-direct-kg-validation-v1",
        "data": {
            "z_bao": Z_BAO,
            "dM_rd": [DM_RD_OBS, DM_RD_ERR],
            "dH_rd": [DH_RD_OBS, DH_RD_ERR],
            "obh2_bbn": [OBH2_BBN, OBH2_ERR],
        },
        "model": "ECI_NMC (Faraoni convention, perturbative xi)",
        "n_samples": 4000,
        "n_burn": 1200,
        "closed_form": sum_closed,
        "kg_backend": sum_kg,
        "delta_H0": h0_kg - h0_closed,
        "verdict": verdict,
        "elapsed_closed_sec": t_closed,
        "elapsed_kg_sec": t_kg,
        "c4_v5_overnight_reference": {
            "H0_ECI_NMC_mean": 64.04, "H0_ECI_NMC_std": 2.95,
            "source": "/root/crossed-cosmos/compute/C4_joint_mcmc/results/c4_v5_overnight_results.json",
        },
    }
    out_dir = "/home/remondiere/pc_calcs/cosmopower_nmc_emulator"
    if not os.path.isdir(out_dir):
        out_dir = "/tmp"
    out_path = os.path.join(out_dir, "direct_kg_validation.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved: {out_path}")
    return out


if __name__ == "__main__":
    main()
