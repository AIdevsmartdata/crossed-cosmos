"""A72 OPTIMIZED — Damerell ladder extension null test.

Optimization vs null_test.py:
  - mp.dps = 30 (sufficient for sigma<0.3 cut; was 60 = 4x slower per op)
  - Build invariants ONCE with mpmath, convert to float64 immediately
  - Hit-counting uses pure numpy (numpy ops ~1000x faster than mpmath)
  - Pre-compute rational quotient table (q_table) once
  - multiprocessing.Pool over 512 trials
  - Reduced max_num=max_den=12 (was 15), max_sum=18 (was 20)

Expected runtime: <2 min on 8-core VPS or <30s on 12-core PC.

Hallu count entering: 85.   Mistral STRICT-BAN.
"""

import json
import os
import random
import time
from math import gcd
from multiprocessing import Pool, cpu_count

import numpy as np
from mpmath import mp, mpf, sqrt, pi, gamma, fabs

mp.dps = 30

# ----------------------------------------------------------------------------
# 1. Algebraic ingredients — computed ONCE with mpmath
# ----------------------------------------------------------------------------

Omega_K = float(gamma(mpf(1) / 4) ** 2 / (2 * sqrt(2 * pi)))  # ~2.6220575...
PI = float(pi)

# Damerell ladder rationals
ALPHA = {1: 1.0/10, 2: 1.0/12, 3: 1.0/24, 4: 1.0/60}

# Hecke eigenvalues from LMFDB 4.5.b.a (split primes)
HECKE_TRACES = {1: 1, 2: -4, 3: 0, 4: 16, 5: -14, 6: 0, 7: 0, 8: -64,
                9: 81, 10: 56, 11: 0, 12: 0, 13: -238, 14: 0, 15: 0}
LAMBDA = {p: HECKE_TRACES[p] / p**2 for p in (2, 5, 13)}


# ----------------------------------------------------------------------------
# 2. Observables — float64
# ----------------------------------------------------------------------------
OBS = {
    # PMNS (NuFit-5.3, NO with SK atmo, 2024-07)
    "sin2_th12":  (0.307,    0.013),
    "sin2_th23":  (0.572,    0.018),
    "sin2_th13":  (0.02203,  0.00056),
    "delta_CP":   (-1.20,    0.30),
    "th12":       (0.5840,   0.0140),
    "th23":       (0.8595,   0.0188),
    "th13":       (0.1496,   0.0019),
    "J_PMNS":     (0.0322,   0.0080),
    "J_CKM":      (3.18e-5,  0.15e-5),
    "Sigma_mnu":  (0.067,    0.020),
    "ratio_dmsq": (0.02951,  0.0009),
    "mu_md":      (0.474,    0.060),
    "ms_md":      (27.33,    0.67),
    "mc_ms":      (11.76,    0.05),
    "mb_mc":      (3.596,    0.020),
    "mt_mb":      (39.62,    0.45),
    "yu_yt":      (1.33e-5,  0.20e-5),
    "yc_yt":      (7.83e-3,  0.10e-3),
    "yd_yb":      (1.117e-3, 0.080e-3),
    "ys_yb":      (0.02234,  0.0008),
}
OBS_NAMES = list(OBS.keys())
OBS_VALS = np.array([OBS[k][0] for k in OBS_NAMES])
OBS_SIGS = np.array([OBS[k][1] for k in OBS_NAMES])


# ----------------------------------------------------------------------------
# 3. Pre-computed rational quotient table
# ----------------------------------------------------------------------------
def build_q_table(max_num=12, max_den=12, max_sum=18, q_norm_max=1.25):
    qs = []
    labels = []
    for den in range(1, max_den + 1):
        for num in range(1, max_num + 1):
            if num + den > max_sum or gcd(num, den) != 1:
                continue
            for sign in (1, -1):
                q = sign * num / den
                if abs(q) > q_norm_max:
                    continue
                qs.append(q)
                labels.append(f"{sign*num}/{den}")
    return np.array(qs), labels

Q_TABLE_LAX, Q_LABELS_LAX = build_q_table(12, 12, 18, q_norm_max=1.25)
Q_TABLE_STRICT, Q_LABELS_STRICT = build_q_table(12, 12, 18, q_norm_max=1.0)


# ----------------------------------------------------------------------------
# 4. Build invariants (float64)
# ----------------------------------------------------------------------------
def build_invariants(alpha, lam):
    """Return (names_list, values_array)."""
    names = []
    values = []

    for m, v in alpha.items():
        names.append(f"alpha_{m}")
        values.append(v)

    for i in range(1, 5):
        for j in range(1, 5):
            if i == j: continue
            names.append(f"alpha_{i}/alpha_{j}")
            values.append(alpha[i] / alpha[j])

    for i in range(1, 5):
        for j in range(i, 5):
            names.append(f"alpha_{i}*alpha_{j}")
            values.append(alpha[i] * alpha[j])

    seen = set()
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                key = tuple(sorted([i, j, k]))
                if key in seen: continue
                seen.add(key)
                names.append(f"alpha_{key[0]}*alpha_{key[1]}*alpha_{key[2]}")
                values.append(alpha[key[0]] * alpha[key[1]] * alpha[key[2]])

    for m in range(1, 5):
        for k in (-3, -2, -1, 1, 2, 3):
            names.append(f"alpha_{m}*pi^{k}")
            values.append(alpha[m] * PI ** k)

    for m in range(1, 5):
        for n in (2, 5, 13):
            names.append(f"alpha_{m}*sqrt({n})")
            values.append(alpha[m] * np.sqrt(n))

    for m in range(1, 5):
        for p, lp in lam.items():
            names.append(f"alpha_{m}*|lambda_{p}|")
            values.append(alpha[m] * abs(lp))

    for m in range(1, 5):
        names.append(f"4*alpha_{m}")
        values.append(4 * alpha[m])
        names.append(f"alpha_{m}/4")
        values.append(alpha[m] / 4)

    for m in range(1, 5):
        names.append(f"alpha_{m}^2")
        values.append(alpha[m] ** 2)

    for i in range(1, 5):
        for j in range(i, 5):
            for k in (-2, -1, 1, 2):
                names.append(f"alpha_{i}*alpha_{j}*pi^{k}")
                values.append(alpha[i] * alpha[j] * PI ** k)

    for k in (1, 2, 3, 4):
        names.append(f"Omega_K^4/pi^{k}")
        values.append(Omega_K**4 / PI**k)

    return names, np.array(values)


# ----------------------------------------------------------------------------
# 5. Vectorized hit-counting
# ----------------------------------------------------------------------------
def count_hits_fast(values, q_table, sigma_thresh=0.5):
    """For each (inv, obs) pair, find best q · inv hit |obs - q·inv|/sigma < thresh.

    Vectorized via broadcasting:
       inv_array shape (N_inv,)
       q_table shape (Q,)
       obs_vals shape (M,), obs_sigs shape (M,)

    Returns total hit count + list of (inv_idx, obs_idx, q_idx, sigma_dist).
    """
    # exclude zero invariants
    nonzero = np.abs(values) > 1e-20
    vals = values[nonzero]

    # predicted = q * inv  shape (N_inv, Q)
    pred = vals[:, None] * q_table[None, :]  # (N_inv, Q)

    # sigma_dist = |obs - q·inv| / sigma  shape (N_inv, Q, M)
    diff = np.abs(pred[:, :, None] - OBS_VALS[None, None, :]) / OBS_SIGS[None, None, :]

    # Hits: where sigma_dist < thresh
    hits_mask = diff < sigma_thresh  # (N_inv, Q, M)
    total = int(hits_mask.sum())
    return total


# ----------------------------------------------------------------------------
# 6. Random ladder
# ----------------------------------------------------------------------------
def random_ladder(rng, alpha_target):
    out = {}
    for m, target in alpha_target.items():
        for _ in range(2000):
            den = rng.randint(5, 100)
            num = rng.randint(1, den)
            v = num / den
            if 0.5 * target < v < 2 * target:
                out[m] = v
                break
        else:
            out[m] = num / den
    return out


def random_lambdas(rng):
    return {p: rng.randint(1, 99) / 100 * (-1 if rng.random() < 0.5 else 1)
            for p in (2, 5, 13)}


# ----------------------------------------------------------------------------
# 7. Single trial worker
# ----------------------------------------------------------------------------
def trial_worker(seed):
    rng = random.Random(seed)
    a_rand = random_ladder(rng, ALPHA)
    l_rand = random_lambdas(rng)
    _, vals = build_invariants(a_rand, l_rand)
    n_h = count_hits_fast(vals, Q_TABLE_LAX, sigma_thresh=0.5)
    n_s = count_hits_fast(vals, Q_TABLE_STRICT, sigma_thresh=0.3)
    return n_h, n_s


# ----------------------------------------------------------------------------
# 8. Main
# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 78)
    print("A72 OPTIMIZED — Damerell ladder extension null test")
    print(f"  mp.dps was 30 (build only); main loop = numpy float64")
    print(f"  CPU cores available: {cpu_count()}")
    print("=" * 78)

    # Q(i) ladder + Hecke eigenvalues
    names_Qi, vals_Qi = build_invariants(ALPHA, LAMBDA)
    n_Qi = len(vals_Qi)
    print(f"\nQ(i) invariants: {n_Qi} structured candidates")
    print(f"  Q-table lax (|q|<=5/4): {len(Q_TABLE_LAX)} quotients")
    print(f"  Q-table strict (|q|<=1): {len(Q_TABLE_STRICT)} quotients")

    n_hits_Qi = count_hits_fast(vals_Qi, Q_TABLE_LAX, sigma_thresh=0.5)
    n_strict_Qi = count_hits_fast(vals_Qi, Q_TABLE_STRICT, sigma_thresh=0.3)
    print(f"  Q(i) HITS lax    (sigma<0.5, |q|<=5/4): {n_hits_Qi}")
    print(f"  Q(i) HITS strict (sigma<0.3, |q|<=1):   {n_strict_Qi}")

    # Null test
    n_trials = 512
    print(f"\nNull test: {n_trials} random rational-ladder trials")

    base_seed = 20260505
    seeds = [base_seed + i for i in range(n_trials)]

    n_workers = max(1, cpu_count() - 1)
    print(f"  multiprocessing pool: {n_workers} workers")

    with Pool(processes=n_workers) as pool:
        results = pool.map(trial_worker, seeds)

    null_lax = sorted([r[0] for r in results])
    null_strict = sorted([r[1] for r in results])

    def stats(arr):
        a = np.array(arr)
        return {"mean": float(a.mean()), "sd": float(a.std()),
                "median": float(np.median(a)),
                "p95": float(np.percentile(a, 95)),
                "p99": float(np.percentile(a, 99)),
                "min": int(a.min()), "max": int(a.max())}

    s_lax = stats(null_lax)
    s_strict = stats(null_strict)

    sigma_lax = (n_hits_Qi - s_lax["mean"]) / s_lax["sd"] if s_lax["sd"] > 0 else float("inf")
    sigma_strict = (n_strict_Qi - s_strict["mean"]) / s_strict["sd"] if s_strict["sd"] > 0 else float("inf")

    tail_lax = sum(1 for x in null_lax if x >= n_hits_Qi) / n_trials
    tail_strict = sum(1 for x in null_strict if x >= n_strict_Qi) / n_trials

    print("\n" + "=" * 78)
    print("NULL DISTRIBUTION (lax, sigma<0.5, |q|<=5/4)")
    print(f"  mean +/- sd = {s_lax['mean']:.1f} +/- {s_lax['sd']:.1f}")
    print(f"  median={s_lax['median']:.0f}, p95={s_lax['p95']:.0f}, p99={s_lax['p99']:.0f}")
    print(f"  Q(i) hits = {n_hits_Qi},  sigma vs mean = {sigma_lax:+.2f}")
    print(f"  P(null >= Q(i)) = {tail_lax:.4f}")

    print("\nNULL DISTRIBUTION (strict, sigma<0.3, |q|<=1)")
    print(f"  mean +/- sd = {s_strict['mean']:.2f} +/- {s_strict['sd']:.2f}")
    print(f"  median={s_strict['median']:.0f}, p95={s_strict['p95']:.0f}, p99={s_strict['p99']:.0f}")
    print(f"  Q(i) hits = {n_strict_Qi},  sigma vs mean = {sigma_strict:+.2f}")
    print(f"  P(null >= Q(i)) = {tail_strict:.4f}")

    out = {
        "mp_dps_build_phase": 30,
        "n_invariants_Qi": n_Qi,
        "n_hits_Qi_lax": n_hits_Qi,
        "n_hits_Qi_strict": n_strict_Qi,
        "null": {
            "n_trials": n_trials,
            "lax":    {"counts": null_lax, **s_lax,
                       "sigma_vs_mean": sigma_lax, "tail_prob": tail_lax},
            "strict": {"counts": null_strict, **s_strict,
                       "sigma_vs_mean": sigma_strict, "tail_prob": tail_strict},
        },
        "elapsed_sec": time.time() - t0,
    }
    out_path = os.path.join(os.path.dirname(__file__), "null_test_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {out_path}")
    print(f"Elapsed: {time.time()-t0:.1f}s")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    if sigma_strict > 3:
        verdict = "STRONG"
    elif sigma_strict > 2:
        verdict = "MEDIUM"
    elif sigma_strict > 1:
        verdict = "WEAK"
    else:
        verdict = "DEAD-END (consistent with random)"
    print(f"  Strict-cut sigma vs random: {sigma_strict:+.2f}  ->  {verdict}")
    print(f"  Lax-cut    sigma vs random: {sigma_lax:+.2f}")
    print(f"  Tail-prob (strict): {tail_strict*100:.1f}%")


if __name__ == "__main__":
    main()
