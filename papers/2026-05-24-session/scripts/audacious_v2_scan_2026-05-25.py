"""
AUDACIOUS v2 — scan exhaustif Σ premiers vs TOUS observables SM/cosmo
======================================================================
Tester si k = dim(X) pour X dans {SM gauge bosons, b_2(K3),
exceptional groups, fermions count} matche autres observables.
"""
import numpy as np
from math import log, log10, exp, pi, sqrt, atan, atan2

# ============================================================================
# Constants
# ============================================================================
v_GeV = 246.22
M_Pl = 1.22091e19
M_GUT = 2.0e16   # typical GUT scale
M_QCD = 0.2      # Λ_QCD GeV
T_CMB = 2.725e-13  # GeV (T = 2.725 K)
m_proton = 0.938272
m_neutron = 0.939565
G_F = 1.1664e-5  # GeV^-2

# Fermion masses (MS-bar)
masses = {
    'e':    0.51099895e-3, 'mu':  0.10565838, 'tau':  1.77686,
    'u':    2.16e-3,        'd':   4.67e-3,    's':    93.4e-3,
    'c':    1.27,           'b':   4.18,       't':    172.57,
}

# Bosons
mH = 125.10; mZ = 91.1876; mW = 80.377
sin2W = 0.23121; alpha_s = 0.1180
alpha_em_MZ = 1/127.952; alpha_em_0 = 1/137.036

# Cosmo
Omega_DM = 0.265; Omega_b = 0.0494
n_s = 0.9649; eta_B = 6.12e-10
Lambda_over_MP4 = 1.105e-122
H0 = 67.4 / 9.78e11  # H0 in GeV (67.4 km/s/Mpc -> 1.42e-42 GeV)

# Sommes premiers
def first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if all(num % p != 0 for p in primes if p*p <= num):
            primes.append(num)
        num += 1
    return primes

PRIMES_30 = first_n_primes(30)

# k -> Σ first k primes
def sum_primes_k(k):
    return sum(first_n_primes(k))

# ============================================================================
# Catalogue Σ premiers k=1..25
# ============================================================================
print("="*78)
print("CATALOGUE : Σ premiers pour k=1..30")
print("="*78)
print(f"{'k':>3s}  {'p_k':>4s}  {'Σ_k':>5s}   {'exp(±Σ)':>15s}  {'log10 exp(-Σ)':>15s}")
print("-"*60)
sum_table = {}
for k in range(1, 26):
    p_k = first_n_primes(k)[-1]
    s = sum_primes_k(k)
    sum_table[k] = s
    log10_em = -s/log(10)
    print(f"{k:3d}  {p_k:4d}  {s:5d}  log10(exp(-Σ)) = {log10_em:8.2f}")

# ============================================================================
# Match scan : pour chaque observable, find best k
# ============================================================================
print("\n" + "="*78)
print("SCAN : pour chaque observable, find best k tel que ±Σ_k ≈ ln(X)")
print("="*78)

candidates = {
    # Cosmo
    'Λ/M_Pl⁴':                Lambda_over_MP4,
    'η_B':                    eta_B,
    'H_0 (in M_Pl units)':    H0/M_Pl,
    'T_CMB / M_Pl':           T_CMB/M_Pl,
    'Ω_DM/Ω_total':           Omega_DM/(Omega_DM+Omega_b+0.685),

    # Particle scales
    'M_Pl²/v²':               (M_Pl/v_GeV)**2,
    'M_Pl/v':                 M_Pl/v_GeV,
    'M_Pl·v / m_H²':          M_Pl*v_GeV/mH**2,
    'M_Pl / m_H':             M_Pl/mH,
    'v/Λ_QCD':                v_GeV/M_QCD,
    'v/m_top':                v_GeV/172.57,
    'M_GUT/v':                M_GUT/v_GeV,
    'M_GUT/M_Pl':             M_GUT/M_Pl,
    'v · α_em':               v_GeV*alpha_em_0,

    # Couplages
    '1/α_s':                  1/alpha_s,
    '1/α_em(M_Z)':            1/alpha_em_MZ,
    '1/α_em(0)':              1/alpha_em_0,
    'sin²θ_W':                sin2W,
    'cos²θ_W':                1-sin2W,

    # Fermion ratios
    'm_e/v':                  masses['e']/v_GeV,
    'm_t/v':                  masses['t']/v_GeV,
    'm_e/m_t':                masses['e']/masses['t'],
    'm_τ/m_t':                masses['tau']/masses['t'],
    'm_b/m_t':                masses['b']/masses['t'],
    'm_u/m_d':                masses['u']/masses['d'],
}

# For each candidate, find best k s.t. exp(±Σ_k) ≈ value
def find_best_k(value, log_value):
    """Return (k_best, sign_best, err)"""
    best_k = None; best_err = 100; best_sign = '+'
    for k in range(1, 26):
        s = sum_table[k]
        for sgn in [+1, -1]:
            pred_log = sgn * s
            err = abs(pred_log - log_value)
            if err < best_err:
                best_err = err
                best_k = k
                best_sign = '+' if sgn > 0 else '-'
    return best_k, best_sign, best_err

print(f"\n{'Observable':<25s}  {'log obs':>9s}  {'best k':>7s} {'sign':>4s}  {'Σ_k':>4s}  {'err log':>8s}  {'value match':>12s}")
print("-"*100)
strong_matches = []
for name, val in candidates.items():
    if val <= 0:
        continue
    log_v = log(val)
    k, sgn, err = find_best_k(val, log_v)
    s = sum_table[k]
    sign_num = 1 if sgn == '+' else -1
    log_pred = sign_num * s
    err_log_value = abs(log_pred - log_v)
    err_pct = abs(err_log_value) * 100  # approx in log percentage
    flag = "★★" if err < 1 else ("★" if err < 3 else "")
    if err < 3:
        strong_matches.append((name, val, k, sgn, s, err, err_pct))
    if abs(log_v) > 0.5:  # skip tiny obs
        print(f"  {name:<25s}  {log_v:9.2f}  k={k:3d}    {sgn:>4s}  {s:4d}  {err:8.3f}  {err_pct:9.2f}%{flag}")

# ============================================================================
# Strong matches summary
# ============================================================================
print("\n" + "="*78)
print(f"STRONG MATCHES (err en log < 3) — {len(strong_matches)} observables")
print("="*78)
for name, val, k, sgn, s, err, err_pct in sorted(strong_matches, key=lambda x: x[5]):
    print(f"  {name:<25s} : obs = {val:.3e}, pred = exp({sgn}{s}) k={k}, err {err:.3f} log, {err_pct:.1f}% value")

# ============================================================================
# Test specific k values
# ============================================================================
print("\n" + "="*78)
print("TEST CIBLE : k = dim physique connue")
print("="*78)
dim_candidates = {
    'dim U(1)': 1,
    'dim SU(2)_L': 3,
    'dim SU(3)_QCD adjoint': 8,
    'dim SM gauge tot (8+3+1)': 12,
    'dim G_2': 14,
    'dim SU(4)': 15,
    'b_2(K3) - 1': 21,
    'b_2(K3)': 22,
    'Niemeier 24': 24,
    'dim SU(5)': 24,
    'dim F_4 - 2·something': 50,  # silly test
}

for label, k in dim_candidates.items():
    s = sum_table.get(k)
    if s:
        log10_neg = -s/log(10)
        log10_pos = s/log(10)
        print(f"  k = {k:2d} ({label:25s}) : Σ_k = {s:4d}, log10(exp(-Σ)) = {log10_neg:7.1f}, log10(exp(+Σ)) = {log10_pos:7.1f}")

# ============================================================================
# Sin²θ_W : pas de Σ premiers, test ratios κ
# ============================================================================
print("\n" + "="*78)
print("sin²θ_W via ratios κ : pas Σ premiers, autre pattern ?")
print("="*78)
kappa_inf = 1.2020569/sqrt(pi)
kappa_SU2 = 0.5080
kappa_SU3 = 0.6025

# sin²θ_W = g'²/(g²+g'²)
# Maybe sin²θ_W = κ(U(1))/(κ(SU(2)) + κ(U(1))) ?
# κ(U(1)) trivial in lattice (no entanglement)
# Try : sin²θ_W = (1 - κ(SU(2))/κ_∞) ?
val1 = 1 - kappa_SU2/kappa_inf
print(f"  sin²θ_W obs                       = {sin2W:.5f}")
print(f"  1 - κ(SU(2))/κ_∞ = 1 - 0.749       = {val1:.5f}  err {abs(val1-sin2W)/sin2W*100:.1f}%")
val2 = (kappa_inf - kappa_SU2)/kappa_inf  # same
val3 = (kappa_SU3 - kappa_SU2)/kappa_inf
print(f"  (κ(SU(3))-κ(SU(2)))/κ_∞ = 0.139    = {val3:.5f}  err {abs(val3-sin2W)/sin2W*100:.1f}%")
# κ_SU(4) - κ_SU(2)
kappa_SU4 = kappa_inf * (1-1/16)
val4 = (kappa_SU4 - kappa_SU2)/kappa_inf
print(f"  (κ(SU(4))-κ(SU(2)))/κ_∞            = {val4:.5f}  err {abs(val4-sin2W)/sin2W*100:.1f}%")
# 1 / (1 + κ_SU2 · N)
print(f"  3/13 (numerical match)             = {3/13:.5f}")
print(f"  sin²θ_W structurelle inconnue, mais 3/13 reste meilleur rationel")

# ============================================================================
# Yukawa hierarchy : ladder structure tests
# ============================================================================
print("\n" + "="*78)
print("Yukawa hiérarchie : tester structure ladder = a·gen + b·charge·color")
print("="*78)
import numpy as np
fermion_data = []
for f, m in masses.items():
    S_inst = -log(m/v_GeV)
    # T3, Y, Q, gen, color
    if f in ['e','mu','tau']:
        T3=-0.5; Y=-1; Q=-1
        gen = 1 if f=='e' else (2 if f=='mu' else 3)
        color = 1
    elif f in ['u','c','t']:
        T3=0.5; Y=1/6; Q=2/3
        gen = 1 if f=='u' else (2 if f=='c' else 3)
        color = 3
    else:
        T3=-0.5; Y=1/6; Q=-1/3
        gen = 1 if f=='d' else (2 if f=='s' else 3)
        color = 3
    fermion_data.append((f, S_inst, gen, Q, color))
    print(f"  {f:3s}: S={S_inst:6.3f}, gen={gen}, Q={Q:+.3f}, color={color}")

# Linear fit S_inst = a·gen + b·Q + c·color + d
X = np.array([(g, q, c, 1) for _, _, g, q, c in fermion_data])
y = np.array([s for _, s, _, _, _ in fermion_data])
coefs, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
a, b, c, d = coefs
y_pred = X @ coefs
residuals = y - y_pred
print(f"\n  Fit S_inst = a·gen + b·Q + c·color + d")
print(f"    a (gen)   = {a:.4f}")
print(f"    b (charge) = {b:.4f}")
print(f"    c (color) = {c:.4f}")
print(f"    d (intercept) = {d:.4f}")
print(f"  Residuals : max = {max(abs(residuals)):.3f}, RMS = {np.sqrt(np.mean(residuals**2)):.3f}")

# Look at the slope per generation per color
print(f"\n  Slope analysis :")
print(f"    For leptons (color=1): a + d at gen=1 = {a + d:.3f}, gen=3 = {3*a + d:.3f}")
print(f"    For quarks (color=3): a + d at gen=1 = {a + d:.3f}")

# Maybe simpler : S_inst = -log(m/v) = N + log(generation·factor)
# Or : geometric S_τ = 5, S_μ = 8, S_e = 13 (Fibonacci-like)
print(f"\n  Fibonacci check on lepton S_inst :")
S_τ = -log(masses['tau']/v_GeV)
S_μ = -log(masses['mu']/v_GeV)
S_e = -log(masses['e']/v_GeV)
print(f"    S_τ = {S_τ:.3f}, S_μ = {S_μ:.3f}, S_e = {S_e:.3f}")
print(f"    Differences : S_μ-S_τ = {S_μ-S_τ:.3f}, S_e-S_μ = {S_e-S_μ:.3f}, sum = {(S_μ-S_τ)+(S_e-S_μ):.3f}")
print(f"    Fibonacci 3,5,8 ? S_τ-3 = {S_τ-3:.3f}, S_μ-8 = {S_μ-8:.3f}")
print(f"    Or Pell 2,5,12 ?")

# ============================================================================
# Bonus : 1/α_em ≈ 137
# ============================================================================
print("\n" + "="*78)
print("Bonus : 1/α_em(0) = 137.036")
print("="*78)
inv_alpha = 137.036
print(f"  1/α_em(0) = {inv_alpha:.3f}")
print(f"  Candidats simples :")
for k in [12, 13, 14, 15, 16]:
    s = sum_table[k]
    print(f"    Σ_{k} premiers = {s}  err = {abs(s-inv_alpha):.1f}")
# Try with 2 dim
print(f"\n  Or 1/α_em = combination of κ_∞ etc :")
print(f"    8π³/3      = {8*pi**3/3:.3f}  err = {abs(8*pi**3/3-inv_alpha):.1f}")
print(f"    7³/2.5     = {7**3/2.5:.3f}")
print(f"    137 prime  → 1/α_em(0)=137.036 ≈ 137 ± 0.036")
print(f"    Coïncidence ?")

# ============================================================================
# Adversarial : sensibilité prime-sum patterns
# ============================================================================
print("\n" + "="*78)
print("ADVERSARIAL : sensibilité Σ_k premiers vs autres séquences")
print("="*78)
# Compare to triangular numbers, fibonacci, factorials
def triangular(k):
    return k*(k+1)//2

def fibonacci(k):
    if k <= 1: return k
    a, b = 0, 1
    for _ in range(k-1):
        a, b = b, a+b
    return b

print(f"\n  Compare different sequences at k=8, 14, 21 :")
for k in [8, 14, 21]:
    primes_sum = sum_table[k]
    tri = triangular(k)
    fib = fibonacci(k)
    print(f"    k={k:2d}: Σ premiers = {primes_sum:4d}, triangulaires = {tri:4d}, fibonacci = {fib:4d}")

# For each observable, which sequence fits best?
print(f"\n  Pour Λ : -ln(Λ/M_Pl⁴) = 281, Σ premiers k=14 = 281 EXACT")
print(f"    Triangulaire k=23 = 276 (off 5), k=24 = 300 (off 19)")
print(f"    Fibonacci k=13 = 233, k=14 = 377 → AUCUN match dans 1 OM")
print(f"    → Σ PREMIERS specifically matches Λ, pas triang/fib")

print(f"\n  Pour M_Pl²/v² : ln = 76.9, Σ premiers k=8 = 77 EXACT")
print(f"    Triangulaire k=12 = 78 (off 1), pas mal")
print(f"    Fibonacci k=11 = 89 (off 12)")
print(f"    → Σ premiers + triangulaire CO-incident à k=12 — moins distinctif")

print(f"""

CONCLUSION :
- Λ via Σ premiers k=14 = UNIQUE pattern (pas triang/fib)
- M_Pl²/v² via Σ premiers k=8 = co-incident avec triangulaire k=12
- η_B via 21 = b_2(K3)-1 = distinct, pas premiers nécessairement
""")
