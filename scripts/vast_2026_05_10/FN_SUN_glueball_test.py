#!/usr/bin/env python3
"""F(N) Theorem C.6 multi-N glueball verification (Opus #7 TOP-3 bridge 7/10)
Cost: ~$3 / ETA 2 min
F(N) = (1+0.8/N²) / (1+0.8/9) — predicted at PUSH-2 ; verify across SU(2-10)
Compare to Lucini-Teper-Wenger 1102.3340 + Bali-Bornyakov 1503.04960 lattice values"""
import os, time, json

# Lattice glueball mass m_0++ in units of sqrt(σ) (string tension)
# Source: Lucini-Teper-Wenger "Glueballs and string tensions in SU(N) gauge theories" 2010
# Bali-Bornyakov "Continuum limit of glueball masses" 2015
# Values from PUSH-2 4-anchor lattice
LATTICE_DATA = {
    2: {"m_glueball_sqrt_sigma": 3.78, "err": 0.04, "src": "Teper 1992"},  # SU(2)
    3: {"m_glueball_sqrt_sigma": 3.56, "err": 0.05, "src": "Lucini-Teper 2001"},  # SU(3)
    4: {"m_glueball_sqrt_sigma": 3.45, "err": 0.06, "src": "Lucini-Teper 2004"},  # SU(4)
    5: {"m_glueball_sqrt_sigma": 3.40, "err": 0.07, "src": "Lucini-Teper 2010"},  # SU(5)
    # SU(6,7,8) needed - extrapolation
    6: None, 7: None, 8: None, 10: None,
}

import math

def F_N(N, c=0.80):
    """F(N) = (1 + c/N²) / (1 + c/9) — c = 0.80 't Hooft per PUSH-2"""
    return (1 + c/N**2) / (1 + c/9)

def predicted_glueball(N, c=0.80, m_inf=3.36):
    """Predicted m_0++/sqrt(σ) at large N, with F(N) correction"""
    return m_inf * F_N(N, c)

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] F(N) SU(N) glueball test")
    print(f"  Formula: m_0++(N)/sqrt(σ) = m_inf * F(N), F(N)=(1+0.8/N²)/(1+0.8/9)")
    print(f"  PUSH-2 c=0.80 't Hooft, m_inf ≈ 3.36 (extracted)")
    print()

    print(f"{'N':>3} | {'F(N)':>7} | {'Predicted m/sqrt(σ)':>20} | {'Lattice':>20} | {'Δ%':>6}")
    print("-" * 80)

    chi2 = 0.0
    n_test = 0
    results = {}
    for N in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
        fn = F_N(N)
        pred = predicted_glueball(N)
        lattice = LATTICE_DATA.get(N)
        if lattice and lattice.get("m_glueball_sqrt_sigma"):
            obs = lattice["m_glueball_sqrt_sigma"]
            err = lattice["err"]
            delta_pct = abs(pred - obs) / obs * 100
            sigma_dev = abs(pred - obs) / err
            chi2 += sigma_dev ** 2
            n_test += 1
            results[N] = {"F": fn, "predicted": pred, "lattice": obs, "err": err,
                         "delta_pct": delta_pct, "sigma_dev": sigma_dev}
            verdict = "✅" if delta_pct < 5 else "⚠️" if delta_pct < 10 else "❌"
            print(f"{N:>3} | {fn:>7.4f} | {pred:>20.3f} | {obs:>14.3f}±{err:.2f} | {delta_pct:>5.1f}% {verdict}")
        else:
            results[N] = {"F": fn, "predicted": pred, "lattice": None}
            print(f"{N:>3} | {fn:>7.4f} | {pred:>20.3f} | {'PREDICTION ONLY':>20} | {'-':>6}")

    print()
    print(f"χ² = {chi2:.3f} on {n_test} anchors (≤4 = within 1σ collectively, ≤9 = within 3σ)")
    if n_test > 0:
        print(f"Verdict: F(N) formula {'PROVED-EMPIRICAL' if chi2 < 9 else 'TENSION'} at {n_test}/4 anchors")

    # Multi-N predictions for SU(6,7,8,9,10) - to be tested with future lattice campaigns
    print(f"\n=== PREDICTIONS for SU(6-10) ===")
    print(f"Lucini-Teper-Wenger style large-N campaign would test these:")
    for N in [6, 7, 8, 9, 10]:
        print(f"  SU({N}): m_0++/sqrt(σ) = {predicted_glueball(N):.3f} ± O(0.1)  [F({N}) = {F_N(N):.4f}]")

    OUT_DIR = "/root/scripts/FN_glueball_outputs"
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f"{OUT_DIR}/results.json", "w") as f:
        json.dump({"chi2": chi2, "n_test": n_test, "results": {str(k): v for k, v in results.items()}}, f, indent=2)
    print(f"\nDone: {OUT_DIR}/results.json")
