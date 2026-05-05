"""A72 — Damerell ladder extension: invariants additionnels K=Q(i).

Building on A62 (V_cb^2=1/600 RETIRED, |V_us|=9/40 weakened to 1.7σ-vs-random),
this script extends the algebraic invariant set to lepton-sector observables
(PMNS angles, Jarlskog-leptonic, Σm_ν, quark-mass ratios) and performs a
512-trial random-rational null test with controlled bias.

Hallu count entering: 85.   mp.dps=60.   Mistral large STRICT-BAN.

Algebraic pistes (NON arbitrary):
  P1. Damerell ladder L(f,m)·π^(4-m)/Ω_K^4 = {1/10, 1/12, 1/24, 1/60}.
      L(f,1) = 1/10·Ω_K^4/π^3, with Ω_K = Γ(1/4)^2/(2√(2π)) for K=Q(i).
  P2. Class number h(Q(i))=1, disc -4, w_K=4 units.
  P3. χ_4 nebentypus values {0, ±1, ±i}.
  P4. Hecke eigenvalues a_p (LMFDB 4.5.b.a): a_2=-4, a_3=0, a_5=-14, a_7=0,
      a_11=0, a_13=-238, a_17=...; CM gives a_p=0 for p≡3 mod 4 (inert).
  P5. CM-by-Q(i): split-prime Hecke characters ψ : O_K -> C^*.
  P6. Damerell ladder ratios: r_m/r_n.

Observables (PDG-2024 / HFLAV-2025 / NuFit-5.3):
  - PMNS solar/atm/reactor angles (sin^2)
  - PMNS δ_CP (NuFit-5.3 normal ordering)
  - Jarlskog J_PMNS, J_CKM
  - Σm_ν (Planck+BAO+DESI 2024 ≤ 0.072 eV; A14 prediction 65-69 meV)
  - Quark mass ratios MS-bar at μ=2 GeV (PDG-2024)

All multiplicative coefficients (e.g. 9/4 for V_us) remain EMPIRICAL — A62
established that K=Q(i) ladder ≈ random (1.7σ).  A72 asks: do the new
algebraic invariants (Petersson, Hecke-eigenvalue rationals, χ_4 phases)
yield candidates that *survive* a stricter null test (512 trials, max_q=15
instead of A62's max_sum=30 lax screen) with sigma<0.5σ + multiplicative
coefficient |q| ≤ 5/4 (= "tight" structurally)?
"""

import json
import os
import random
import time
from fractions import Fraction
from math import gcd

from mpmath import mp, mpf, sqrt, pi, gamma, fabs, log, exp, mpc

mp.dps = 60

# ----------------------------------------------------------------------------
# 1. Algebraic ingredients at K=Q(i)
# ----------------------------------------------------------------------------

# Chowla-Selberg period for Q(i)
Omega_K = gamma(mpf(1) / 4) ** 2 / (2 * sqrt(2 * pi))

# Damerell ladder rationals (verified A1+A5+A17 to 60 digits)
ALPHA = {
    1: mpf(1) / 10,   # m=1 critical L-value rational
    2: mpf(1) / 12,
    3: mpf(1) / 24,
    4: mpf(1) / 60,
}

# Reconstructed L(f, m) values via Damerell:  L(f,m) = α_m · Ω_K^4 / π^(4-m)
def L_value(m):
    return ALPHA[m] * Omega_K**4 / pi ** (4 - m)

# Hecke eigenvalues from LMFDB 4.5.b.a
# (verified live-fetched 2026-05-05)
HECKE_TRACES = {
    # n -> a_n   (n=1..15)
    1: 1, 2: -4, 3: 0, 4: 16, 5: -14, 6: 0, 7: 0, 8: -64, 9: 81, 10: 56,
    11: 0, 12: 0, 13: -238, 14: 0, 15: 0,
}
# Split primes p ≡ 1 mod 4 with non-zero a_p, normalised
# a_p = ψ(p) + bar(ψ)(p) for ψ Hecke char of Q(i).  |a_p| ≤ 2 p^((k-1)/2) = 2 p^2.
# Normalised eigenvalues λ_p = a_p / p^2:
LAMBDA = {p: mpf(HECKE_TRACES[p]) / p ** 2
          for p in (2, 5, 13)}  # split or ramified, non-zero
# w_K = 4 units (1, i, -1, -i)  → factor of 4 ubiquitous in Hecke L(s,ψ)

# χ_4 nebentypus values:  χ(0,2)=0, χ(1)=1, χ(3)=-1.  |χ| ∈ {0, 1}.

# ----------------------------------------------------------------------------
# 2. Observables (PDG-2024 / HFLAV-2025 / NuFit-5.3 NO+SK 2024)
# ----------------------------------------------------------------------------
# Format: name -> (central, sigma)
OBS = {
    # PMNS (NuFit-5.3, NO, with SK atmo, 2024-07 update)
    "sin2_th12":    (mpf("0.307"),  mpf("0.013")),
    "sin2_th23":    (mpf("0.572"),  mpf("0.018")),
    "sin2_th13":    (mpf("0.02203"),mpf("0.00056")),
    "delta_CP":     (mpf("-1.20"),  mpf("0.30")),    # rad (1σ NO)
    "th12":         (mpf("0.5840"), mpf("0.0140")),  # rad
    "th23":         (mpf("0.8595"), mpf("0.0188")),  # rad
    "th13":         (mpf("0.1496"), mpf("0.0019")),  # rad

    # Jarlskog
    "J_PMNS":       (mpf("0.0322"), mpf("0.0080")),  # NuFit central, large σ
    "J_CKM":        (mpf("3.18e-5"),mpf("0.15e-5")),

    # Neutrino-mass sum (Planck+DESI+BAO 2024 95%CL UL ~0.072; A14 lower-band 65-69 meV)
    # Use central = lower-band midpoint 0.067 eV ± 0.020 (broad)
    "Sigma_mnu":    (mpf("0.067"),  mpf("0.020")),
    # Δm²_21 / Δm²_31  (NuFit-5.3 NO)
    "ratio_dmsq":   (mpf("0.02951"),mpf("0.0009")),  # 7.41e-5 / 2.511e-3

    # Quark MS-bar mass ratios at μ=2 GeV (PDG-2024)
    # m_u/m_d = 0.474 (-0.074,+0.056) (lattice avg)
    "mu_md":        (mpf("0.474"),  mpf("0.060")),
    # m_s/m_d = 27.33 ± 0.67
    "ms_md":        (mpf("27.33"),  mpf("0.67")),
    # m_c/m_s = 11.76 ± 0.05  (PDG2024)
    "mc_ms":        (mpf("11.76"),  mpf("0.05")),
    # m_b/m_c = 4.578/1.273 = 3.596 ± 0.020 (combine PDG)
    "mb_mc":        (mpf("3.596"),  mpf("0.020")),
    # m_t/m_b at 2GeV: pole 172.6 / 4.18 ~ 41.3, but use MS-bar m_t(m_t)/m_b(m_b)
    "mt_mb":        (mpf("39.62"),  mpf("0.45")),
    # y_u / y_t:  m_u(2GeV)/m_t(m_t) ~ 2.16e-3 / 162.5 = 1.33e-5
    "yu_yt":        (mpf("1.33e-5"),mpf("0.20e-5")),
    # y_c / y_t: 1.273 / 162.5 = 7.83e-3
    "yc_yt":        (mpf("7.83e-3"),mpf("0.10e-3")),
    # y_d / y_b: 4.67e-3 / 4.18 = 1.117e-3
    "yd_yb":        (mpf("1.117e-3"),mpf("0.080e-3")),
    # y_s / y_b: 0.0934 / 4.18 = 0.02234
    "ys_yb":        (mpf("0.02234"),mpf("0.0008")),
}


# ----------------------------------------------------------------------------
# 3. Build candidate invariants from K=Q(i) algebraic ingredients
# ----------------------------------------------------------------------------
def build_invariants(alpha, lam):
    """Return list of (name, value) pairs.

    Structurally derived expressions ONLY — pures of:
       α_m, α_m·α_n, α_m/α_n, α_m·π^k, α_m·sqrt(n),
       λ_p Hecke-normalised, products α_m·λ_p,
       χ_4 phases (-1, +1) — sign carriers, not multiplied separately,
       w_K = 4 (unit count), h_K = 1 (class number),
       Damerell ratios.
    """
    inv = []

    # Pure ladder
    for m, v in alpha.items():
        inv.append((f"alpha_{m}", v))

    # Ladder ratios
    for i in range(1, 5):
        for j in range(1, 5):
            if i == j: continue
            inv.append((f"alpha_{i}/alpha_{j}", alpha[i] / alpha[j]))

    # Pairwise products (i ≤ j)
    for i in range(1, 5):
        for j in range(i, 5):
            inv.append((f"alpha_{i}*alpha_{j}", alpha[i] * alpha[j]))

    # Triples (sorted)
    seen = set()
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                key = tuple(sorted([i, j, k]))
                if key in seen: continue
                seen.add(key)
                inv.append((f"alpha_{key[0]}*alpha_{key[1]}*alpha_{key[2]}",
                            alpha[key[0]] * alpha[key[1]] * alpha[key[2]]))

    # α_m × π^k (k ∈ {-3..3} but excl 0)
    for m in range(1, 5):
        for k in (-3, -2, -1, 1, 2, 3):
            inv.append((f"alpha_{m}*pi^{k}", alpha[m] * pi ** k))

    # α_m × √n  (small n; only those of arithmetic interest at Q(i): n=2 from
    # 2-ramification, n = 5,13 from split primes)
    for m in range(1, 5):
        for n in (2, 5, 13):
            inv.append((f"alpha_{m}*sqrt({n})", alpha[m] * sqrt(mpf(n))))

    # α_m × |λ_p| (Hecke-normalised eigenvalue at split prime p)
    for m in range(1, 5):
        for p, lp in lam.items():
            inv.append((f"alpha_{m}*|lambda_{p}|", alpha[m] * fabs(lp)))

    # α_m × w_K = 4 α_m, h_K=1 already absorbed
    for m in range(1, 5):
        inv.append((f"4*alpha_{m}",   4 * alpha[m]))   # w_K factor
        inv.append((f"alpha_{m}/4",   alpha[m] / 4))   # 1/w_K

    # α_m^2 (squared)
    for m in range(1, 5):
        inv.append((f"alpha_{m}^2", alpha[m] ** 2))

    # α_m·α_n·π^k  pairs with mod-π
    for i in range(1, 5):
        for j in range(i, 5):
            for k in (-2, -1, 1, 2):
                inv.append((f"alpha_{i}*alpha_{j}*pi^{k}",
                            alpha[i] * alpha[j] * pi ** k))

    # Ω_K^4 / π^k variants (re-encoding Damerell explicitly)
    for k in (1, 2, 3, 4):
        inv.append((f"Omega_K^4/pi^{k}", Omega_K**4 / pi**k))

    return inv


# ----------------------------------------------------------------------------
# 4. Best small-q rational match for given expression vs given target
# ----------------------------------------------------------------------------
def best_q_match(expr_value, target_val, target_sig,
                 max_num=15, max_den=15, max_sum=20, sigma_thresh=0.5,
                 q_norm_max=mpf("1.25")):
    """Return list of (q, sigma_dist) hits within sigma_thresh AND |q| ≤ q_norm_max.

    The 'q_norm_max' cut filters out trivial scalings (e.g. q = 100·something);
    we want STRUCTURAL matches: q small near unity.
    """
    hits = []
    if fabs(expr_value) < mpf("1e-20"):
        return hits
    for den in range(1, max_den + 1):
        for num in range(1, max_num + 1):
            if num + den > max_sum or gcd(num, den) != 1:
                continue
            for sign in (1, -1):
                q = sign * mpf(num) / mpf(den)
                if fabs(q) > q_norm_max:
                    continue
                pred = q * expr_value
                sd = float(fabs(pred - target_val) / target_sig)
                if sd < sigma_thresh:
                    hits.append((f"{sign*num}/{den}", sd, float(pred)))
    return hits


# ----------------------------------------------------------------------------
# 5. Random ladder generator for null-test
# ----------------------------------------------------------------------------
def random_ladder(rng, alpha_target):
    """Generate a random rational 'ladder' with same magnitudes as alpha_target."""
    out = {}
    for m, v_target in alpha_target.items():
        target = float(v_target)
        # rational with denominator 5..100, value within [0.5, 2] of target
        for _ in range(2000):
            den = rng.randint(5, 100)
            num = rng.randint(1, den)
            v = num / den
            if 0.5 * target < v < 2 * target:
                out[m] = mpf(num) / mpf(den)
                break
        else:
            out[m] = mpf(num) / mpf(den)
    return out


def random_lambdas(rng):
    """Random Hecke-like eigenvalues |λ_p| ∈ (0, 1)."""
    return {p: mpf(rng.randint(1, 99)) / mpf(100) * (-1 if rng.random() < 0.5 else 1)
            for p in (2, 5, 13)}


# ----------------------------------------------------------------------------
# 6. Count hits across observables for a given invariant set
# ----------------------------------------------------------------------------
def count_hits(invariants, sigma_thresh=0.5, q_norm_max=mpf("1.25")):
    """Aggregate count of (target, invariant, q) triples passing thresholds."""
    total = 0
    detail = []
    for inv_name, inv_val in invariants:
        for tgt_name, (val, sig) in OBS.items():
            hits = best_q_match(inv_val, val, sig,
                                max_num=15, max_den=15, max_sum=20,
                                sigma_thresh=sigma_thresh,
                                q_norm_max=q_norm_max)
            for q, sd, pred in hits:
                total += 1
                detail.append({"target": tgt_name, "invariant": inv_name,
                                "q": q, "sigma": sd, "predicted": pred,
                                "observed": float(val), "obs_sigma": float(sig)})
    return total, detail


# ----------------------------------------------------------------------------
# 7. Main null test
# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 78)
    print("A72 — Damerell ladder extension, K=Q(i), invariants additionnels")
    print(f"mp.dps = {mp.dps},  obs count = {len(OBS)}")
    print("=" * 78)

    # === Q(i) ladder + Hecke eigenvalues ===
    invariants_Qi = build_invariants(ALPHA, LAMBDA)
    n_Qi = len(invariants_Qi)
    print(f"\nQ(i) invariants: {n_Qi} structured candidates")

    # Stricter screen than A62: |q| ≤ 5/4, σ < 0.5
    n_hits_Qi, detail_Qi = count_hits(invariants_Qi,
                                       sigma_thresh=mpf("0.5"),
                                       q_norm_max=mpf("1.25"))
    print(f"  HITS (|q| ≤ 5/4, σ < 0.5):   {n_hits_Qi}")

    # Tighter (|q| ≤ 1, σ < 0.3) for headline
    n_strict_Qi, detail_strict_Qi = count_hits(invariants_Qi,
                                                 sigma_thresh=mpf("0.3"),
                                                 q_norm_max=mpf("1.0"))
    print(f"  STRICT HITS (|q| ≤ 1, σ < 0.3): {n_strict_Qi}")

    # === Null test: 512 random rational-ladder trials ===
    n_trials = 512
    print(f"\nNull test: {n_trials} random rational-ladder trials")
    print(f"  (denom ∈ [5,100], magnitudes within ×2 of α_m, λ_p uniform on (-1,1))")

    rng = random.Random(20260505)
    null_counts = []
    null_strict = []
    for trial in range(n_trials):
        a_rand = random_ladder(rng, ALPHA)
        l_rand = random_lambdas(rng)
        inv_r = build_invariants(a_rand, l_rand)
        n_h, _ = count_hits(inv_r,
                            sigma_thresh=mpf("0.5"),
                            q_norm_max=mpf("1.25"))
        n_s, _ = count_hits(inv_r,
                            sigma_thresh=mpf("0.3"),
                            q_norm_max=mpf("1.0"))
        null_counts.append(n_h)
        null_strict.append(n_s)
        if (trial + 1) % 64 == 0:
            print(f"    trial {trial+1}/{n_trials}: n_h={n_h}, n_s={n_s}, "
                  f"elapsed={time.time()-t0:.1f}s")

    null_counts.sort()
    null_strict.sort()

    def stats(arr):
        n = len(arr)
        mean = sum(arr) / n
        var = sum((x - mean) ** 2 for x in arr) / n
        sd = var ** 0.5
        med = arr[n // 2]
        p95 = arr[int(0.95 * n)]
        p99 = arr[int(0.99 * n)]
        return {"mean": mean, "sd": sd, "median": med, "p95": p95, "p99": p99,
                "min": arr[0], "max": arr[-1]}

    s = stats(null_counts)
    ss = stats(null_strict)

    # Sigma vs null mean
    sigma_lax = (n_hits_Qi - s["mean"]) / s["sd"] if s["sd"] > 0 else float("inf")
    sigma_strict = (n_strict_Qi - ss["mean"]) / ss["sd"] if ss["sd"] > 0 else float("inf")

    # Tail prob (one-sided, # of null trials with hits >= Q(i))
    tail_lax = sum(1 for x in null_counts if x >= n_hits_Qi) / n_trials
    tail_strict = sum(1 for x in null_strict if x >= n_strict_Qi) / n_trials

    print("\n" + "=" * 78)
    print("NULL DISTRIBUTION (lax cut, σ<0.5, |q|≤5/4)")
    print(f"  mean ± sd = {s['mean']:.1f} ± {s['sd']:.1f}")
    print(f"  median    = {s['median']}, p95 = {s['p95']}, p99 = {s['p99']}, "
          f"min/max = {s['min']}/{s['max']}")
    print(f"  Q(i) hits  = {n_hits_Qi}")
    print(f"  σ vs mean  = {sigma_lax:+.2f}")
    print(f"  P(null ≥ Q(i)) = {tail_lax:.4f}")
    print()
    print("NULL DISTRIBUTION (strict cut, σ<0.3, |q|≤1)")
    print(f"  mean ± sd = {ss['mean']:.2f} ± {ss['sd']:.2f}")
    print(f"  median    = {ss['median']}, p95 = {ss['p95']}, p99 = {ss['p99']}, "
          f"min/max = {ss['min']}/{ss['max']}")
    print(f"  Q(i) hits  = {n_strict_Qi}")
    print(f"  σ vs mean  = {sigma_strict:+.2f}")
    print(f"  P(null ≥ Q(i)) = {tail_strict:.4f}")
    print()

    # Write detail json + null results
    out = {
        "mp_dps": mp.dps,
        "n_invariants_Qi": n_Qi,
        "n_hits_Qi_lax":    n_hits_Qi,
        "n_hits_Qi_strict": n_strict_Qi,
        "null": {
            "n_trials": n_trials,
            "lax":    {"counts": null_counts, **s,
                       "sigma_vs_mean": sigma_lax,
                       "tail_prob":     tail_lax},
            "strict": {"counts": null_strict, **ss,
                       "sigma_vs_mean": sigma_strict,
                       "tail_prob":     tail_strict},
        },
        "Qi_hits_lax":    detail_Qi,
        "Qi_hits_strict": detail_strict_Qi,
        "elapsed_sec": time.time() - t0,
    }
    out_path = os.path.join(os.path.dirname(__file__), "null_test_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"Wrote {out_path}")
    print(f"Elapsed: {time.time()-t0:.1f}s")

    # Verdict
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
        verdict = "DEAD-END"
    print(f"  Strict-cut σ vs random:  {sigma_strict:+.2f}  →  {verdict}")
    print(f"  Lax-cut    σ vs random:  {sigma_lax:+.2f}")
    print(f"  Tail-prob (strict):  {tail_strict*100:.1f}%")


if __name__ == "__main__":
    main()
