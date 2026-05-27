#!/usr/bin/env python3
"""Test metaselector Σ premiers + d_∂ = 2/3 + BG×HL fixed point."""
import numpy as np
from sympy import sieve

primes = list(sieve.primerange(2, 250))
cumsum = np.cumsum(primes[:30])

def check_against_primes(value, max_k=30):
    abs_v = abs(value)
    best = None
    for k in range(1, max_k):
        s = cumsum[k-1]
        delta = abs_v - s
        rel = abs(delta) / s if s > 0 else 1e10
        if best is None or rel < best[2]:
            best = (k, s, rel, delta)
    return best

print("=== BG×HL fixed point check d_∂=2/3, z=3 ===")
d_partial = 2/3
D_bulk = 4
d_s_BG = (D_bulk + d_partial) / 2
print(f"d_s(BG) = (D + d_∂)/2 = ({D_bulk}+{d_partial:.4f})/2 = {d_s_BG:.6f}")
print(f"d_s expected = 7/3 = {7/3:.6f}")
print(f"Match? Δ = {d_s_BG - 7/3:+.6f}")
print()
# Hořava : d_s = 1 + D/z
for z in [1, 3/2, 2, 3, 4]:
    d_s_HL = 1 + D_bulk/z
    print(f"  HL z={z:.2f} : d_s = 1+D/z = {d_s_HL:.4f}")
print()
print(f"For HL d_s = 7/3 : z = D/(d_s-1) = {D_bulk/(7/3-1):.6f} = 3 EXACT")
print()

print("=== Observable testbench Σ premiers ===")
observables = [
    ("ln(M_Pl/v)²", 2*np.log(2.435e18/246), 8, +1, "QCD adj"),
    ("ln(M_Pl/m_p)²", 2*np.log(2.435e18/0.938), None, +1, "?"),
    ("-ln(Λ/M_Pl⁴)", -np.log(1.105e-122), 14, +1, "G_2 adj"),
    ("-ln(η_B)", -np.log(6.12e-10), 21, +1, "b₂(K3)"),
    ("ln(α_em⁻¹)", np.log(137.036), None, +1, "?"),
    ("ln(m_t/m_e)", np.log(173570/0.000511), None, +1, "?"),
    ("ln(m_W/m_e)", np.log(80379/0.000511), None, +1, "?"),
    ("ln(v/m_Z)·2", 2*np.log(246/91.187), None, +1, "?"),
    ("ln(Σm_ν / 0.1 eV)·negative", -np.log(0.06/0.1) if True else None, None, -1, "?"),
    ("ln(m_b/m_e)", np.log(4180/0.000511), None, +1, "?"),
    ("ln(m_p/m_e)", np.log(0.938/0.000511), None, +1, "?"),
]

print(f"\n{'Observable':<26s} {'value':>10s} {'expect k':>10s} {'best k':>7s} {'Σ_k':>6s} {'rel%':>8s}")
for name, val, k_exp, sign, comment in observables:
    if val is None: continue
    target = abs(val)
    k_best, s_best, rel_best, delta = check_against_primes(target)
    verdict = "★★★" if rel_best < 0.005 else "★★" if rel_best < 0.02 else "★" if rel_best < 0.10 else ""
    k_match = "✓" if k_exp == k_best else ""
    expect_str = f"{k_exp}{k_match}" if k_exp else "?"
    print(f"{name:<26s} {target:>10.2f} {expect_str:>10s} {k_best:>7d} {s_best:>6d} {100*rel_best:>7.2f}% {verdict} {comment}")

# Universe selection
print("\n=== Universe selection algorithmic anthropic ===")
print("Hypothesis: ln(M_Pl/v) = Σ_8 premiers / 2 = 77/2")
print(f"  exp(77/2) = {np.exp(77/2):.3e}")
print(f"  M_Pl/v = 2.435e18/246 = {2.435e18/246:.3e}")
print(f"  Ratio match : {(np.exp(77/2)) / (2.435e18/246):.4f}")
print(f"  Relative error : {((np.exp(77/2)) / (2.435e18/246) - 1)*100:.2f}%")
print()
print("Alternatives:")
M_pl_v_obs = 2.435e18 / 246
for k in [3, 4, 5, 6, 7, 8, 9, 10, 14]:
    s = cumsum[k-1]
    M_pred = np.exp(s/2)
    delta_log = np.log10(M_pred/M_pl_v_obs)
    print(f"  k={k:2d}: Σ={s:3d}, exp(Σ/2)={M_pred:.2e}, log10(ratio) = {delta_log:+.2f}")

# d_∂ = 2/3 cross-check
print("\n=== d_∂ = 2/3 cross-checks ===")
print(f"d_∂ = 2/3 = {2/3:.6f}")
print(f"  vs Sierpinski gasket d_H = log3/log2 = {np.log(3)/np.log(2):.6f}")
print(f"  vs Cantor middle-third d_H = log2/log3 = {np.log(2)/np.log(3):.6f} ★ EXACT EQUAL ?!")
print(f"  Cantor d_H = {np.log(2)/np.log(3):.6f}, d_∂ predict = 2/3 = {2/3:.6f}")
print(f"  Cantor ≈ 0.6309, d_∂ = 0.6667. Difference = {0.6667-0.6309:.4f}")
print()
print("Closer rationals to Cantor d_H = log2/log3 ≈ 0.6309:")
for r in [(2,3,2/3), (5,8,5/8), (7,11,7/11), (12,19,12/19), (3,5,3/5)]:
    print(f"  {r[0]}/{r[1]} = {r[2]:.5f}, diff vs log2/log3 = {r[2]-np.log(2)/np.log(3):+.5f}")

# Σ premiers and ζ(s)
print("\n=== Σ premiers vs ζ(s) connection ===")
print("Theorem (Mertens) : Σ_{p≤x} 1/p ~ log log x")
print("Density theorem : prime counting π(x) ~ x/log x")
print("Sum of first k primes : Σ_k ~ k²/(2 log k) for large k")
print()
print(f"Asymptotic formula k²/(2 log k) vs actual cumsum:")
for k in [8, 14, 21]:
    asymp = k**2 / (2 * np.log(k))
    actual = cumsum[k-1]
    print(f"  k={k}: asymp={asymp:.1f}, actual={actual}, ratio={actual/asymp:.3f}")
