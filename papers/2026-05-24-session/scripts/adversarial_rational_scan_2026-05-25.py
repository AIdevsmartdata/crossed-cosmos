"""
Adversarial test : sont les 20+ matches SM significatifs ou random chance ?
============================================================================
Methode : pour chaque cible SM, on tire N_random valeurs aléatoires uniformes
dans [0, max(SM)] et on compte combien matchent à <0.3% une simple rationnelle p/q
avec p,q ∈ {1..30}. Si la fraction obs est >> fraction random, c'est significatif.

Auteur : Kevin Remondiere
"""
import numpy as np
from math import gcd

np.random.seed(42)

# Build rationals catalog (p/q with p,q in 1..30, gcd=1, q>=2)
def build_rationals(p_max=30, q_max=30):
    rats = set()
    for q in range(2, q_max+1):
        for p in range(1, p_max+1):
            if gcd(p, q) == 1:
                rats.add(p/q)
    return sorted(rats)

# Plus κ(SU(N)) for N=2..10
def kappa_set(kappa_inf=0.67819):
    return [(1 - 1/N**2) for N in range(2, 11)] + [kappa_inf*(1 - 1/N**2) for N in range(2,11)]

# Plus roots and trig values
def special_set():
    PI = np.pi
    return [PI/2, PI/3, PI/4, PI/5, PI/6, PI/8, PI/12,
            1/PI, 2/PI, 1/np.sqrt(PI), np.sqrt(PI),
            np.log(2), np.log(3), 1/np.e,
            (1+np.sqrt(5))/2, np.sqrt(2)/2,
            0.67819, 1.20206/np.sqrt(PI)]

ALL_RATIONALS = build_rationals(p_max=30, q_max=30)
ALL_KAPPA = kappa_set()
ALL_SPECIAL = special_set()
ALL_CANDIDATES = sorted(set(ALL_RATIONALS + ALL_KAPPA + ALL_SPECIAL))

print(f"Total candidates : rationals={len(ALL_RATIONALS)}, kappa={len(ALL_KAPPA)}, special={len(ALL_SPECIAL)}")
print(f"Total unique     : {len(ALL_CANDIDATES)}")

def matches_simple(target, max_err=0.003):
    """Return list of matches at max_err precision"""
    matches = []
    for c in ALL_CANDIDATES:
        if c > 0 and abs(c - target)/target < max_err:
            matches.append(c)
    return matches

# ============================================================================
# Test des cibles SM observées
# ============================================================================
SM_TARGETS = {
    'm_H/v':       0.50808,
    'm_Z/v':       0.37035,
    'm_W/v':       0.32644,
    '(m_W/m_Z)²':  0.77695,
    '(m_H/m_Z)²':  1.88210,
    '(m_t/m_Z)²':  3.58145,
    'sin²θ_W':     0.23121,
    'sin θ_W':     0.48084,
    'cos²θ_W':     0.76879,
    'α_s':         0.118,
    'y_top':       0.99119,
    'A_CKM':       0.826,
    'A_CKM²':      0.6823,
    'η_bar':       0.348,
    'ρ_bar':       0.159,
    'sin δ_CKM':   0.91212,
    'cos δ_CKM':   0.40992,
    'sin²θ₂₃':     0.57131,
    'sin²θ₁₂':     0.30319,
    'sin²θ₁₃':     0.022,
    'θ₂₃/π':       0.27278,
    'n_s':         0.9649,
    'Ω_DM/Ω_b':    5.36,
    'Ω_b/Ω_DM':    0.18657,
}

print(f"\n{'='*78}")
print(f"OBSERVED — matches à <0.3% sur {len(SM_TARGETS)} cibles SM")
print('='*78)
obs_with_match = 0
match_counts = []
for name, val in SM_TARGETS.items():
    matches = matches_simple(val, max_err=0.003)
    if matches:
        obs_with_match += 1
        match_counts.append(len(matches))
        best = min(matches, key=lambda c: abs(c-val)/val)
        err = abs(best-val)/val * 100
        print(f"  {name:15s} : {val:.5f} → match {best:.5f} ({err:.3f}%, {len(matches)} candidates)")
    else:
        print(f"  {name:15s} : {val:.5f} → NO MATCH")

print(f"\n→ {obs_with_match}/{len(SM_TARGETS)} cibles matchent <0.3%")
print(f"→ moyenne matches/cible : {np.mean(match_counts):.1f}")

# ============================================================================
# Test random : tirages uniformes
# ============================================================================
print(f"\n{'='*78}")
print(f"ADVERSARIAL — random uniform [0, 5.5] vs même catalogue")
print('='*78)

n_trials = 100000
n_matches_random = 0
for _ in range(n_trials):
    # Random val in same range as SM (0 to ~6)
    val = np.random.uniform(0.02, 5.5)
    matches = matches_simple(val, max_err=0.003)
    if matches:
        n_matches_random += 1

frac_random = n_matches_random / n_trials
print(f"  Random uniform : {n_matches_random}/{n_trials} = {frac_random*100:.2f}%")
print(f"  Expected matches on {len(SM_TARGETS)} cibles si aléatoire : {frac_random*len(SM_TARGETS):.1f}")
print(f"  OBSERVED matches : {obs_with_match}")
print(f"  Excess : {obs_with_match - frac_random*len(SM_TARGETS):.1f}σ-ish")

# Z-score (rough): observed - expected, std = sqrt(expected*(1-frac))
exp = frac_random * len(SM_TARGETS)
std = np.sqrt(len(SM_TARGETS) * frac_random * (1-frac_random))
z = (obs_with_match - exp) / std if std > 0 else 0
print(f"  Z-score (Gaussian approx) : {z:.2f}σ")

# ============================================================================
# Plus précis : test par cible avec random AUTOUR de chaque cible
# ============================================================================
print(f"\n{'='*78}")
print(f"PER-TARGET RANDOM : pour chaque val SM, tirer random et compter ranges")
print('='*78)

n_per = 1000
significant_targets = []
for name, val in SM_TARGETS.items():
    # Match obs precision
    obs_matches = matches_simple(val, max_err=0.003)
    n_obs = len(obs_matches)
    # Random in [0.5*val, 1.5*val]
    random_n = []
    for _ in range(n_per):
        rval = np.random.uniform(0.5*val, 1.5*val)
        random_n.append(len(matches_simple(rval, max_err=0.003)))
    avg_random = np.mean(random_n)
    if n_obs > 0:
        ratio = n_obs / avg_random if avg_random > 0 else float('inf')
        if avg_random < 0.5 and n_obs >= 1:
            significant_targets.append(name)
            sig_marker = "★"
        else:
            sig_marker = ""
        print(f"  {sig_marker} {name:15s} : obs n_match={n_obs}, random avg={avg_random:.2f}, ratio={ratio:.2f}")

print(f"\n★ Sig (random avg <0.5) : {len(significant_targets)} cibles : {significant_targets}")

# ============================================================================
# Final : matches NOT explained by random (smaller error threshold)
# ============================================================================
print(f"\n{'='*78}")
print(f"STRICT — matches à <0.1% (true tightening)")
print('='*78)

strict_matches = []
for name, val in SM_TARGETS.items():
    matches = matches_simple(val, max_err=0.001)
    if matches:
        best = min(matches, key=lambda c: abs(c-val)/val)
        err = abs(best-val)/val * 100
        strict_matches.append((name, val, best, err))
        print(f"  {name:15s} : {val:.5f} → {best:.5f} (Δ={err:.3f}%)")

print(f"\n→ {len(strict_matches)} cibles matchent <0.1% (TIER 1 candidates)")
# Random check at this strict level
n_random_strict = 0
for _ in range(n_trials):
    val = np.random.uniform(0.02, 5.5)
    if matches_simple(val, max_err=0.001):
        n_random_strict += 1
print(f"  Random fraction <0.1% : {n_random_strict/n_trials*100:.2f}%")
print(f"  Expected on {len(SM_TARGETS)} : {n_random_strict/n_trials*len(SM_TARGETS):.2f}")
print(f"  Observed                    : {len(strict_matches)}")
exp_s = n_random_strict/n_trials*len(SM_TARGETS)
std_s = np.sqrt(len(SM_TARGETS) * (n_random_strict/n_trials) * (1-n_random_strict/n_trials))
z_strict = (len(strict_matches) - exp_s) / std_s if std_s > 0 else 0
print(f"  Z-score                     : {z_strict:.2f}σ")

print(f"\n{'='*78}")
print("VERDICT")
print('='*78)
if z_strict > 3:
    print(f"  ★★★ HIGHLY SIGNIFICANT : {z_strict:.1f}σ at <0.1% precision")
    print("      Les matches SM ne sont PAS expliqués par chance.")
else:
    print(f"  Modeste : Z={z_strict:.1f}σ — partial significance")
    print(f"  Top strict matches restent les meilleurs candidats")
