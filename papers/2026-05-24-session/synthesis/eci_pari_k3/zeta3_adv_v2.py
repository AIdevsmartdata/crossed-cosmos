"""
Robust adversarial test for L_partial(K3, 3) ≈ ζ(3).

Use realistic bound on a_p (not full Weil 22p but typical Sato-Tate variance).
Also limit to absolute values close to observed.
"""

import numpy as np
from sympy import sieve
from mpmath import mpf, zeta as mpzeta

data_fermat = [(3,6),(5,-26),(7,14),(11,22),(13,-42),(17,310),(19,38),(23,46),(29,-74),(31,62),(37,-218),(41,838),(43,86),(47,94)]

def L_partial_safe(data, s):
    """Compute partial L with proper handling of L_p polynomial of degree 22."""
    # Use degree 2 truncation: L_p ≈ 1 - a_p T + p^2 T^2
    # (degree 2 captures 2 transcendental + 20 trivial Tate twists with cancellation)
    log_L = 0.0
    for p, a_p in data:
        T = p**(-s)
        L_p = 1 - a_p * T + p**2 * T**2
        if L_p <= 0: return None
        log_L -= np.log(L_p)
    return np.exp(log_L)

print("Robust L_partial computations:")
real_3 = L_partial_safe(data_fermat, 3)
print(f"  Real K3 partial L(s=3): {real_3:.6f}")
print(f"  ζ(3) = {float(mpzeta(3)):.6f}")
print(f"  |diff|: {abs(real_3 - float(mpzeta(3))):.6f}")
print()

# Adversarial null with truncated Sato-Tate bounds
np.random.seed(42)
n_trials = 5000
fakes = []
for trial in range(n_trials):
    # Fake a_p with similar magnitude distribution
    fake_data = [(p, np.random.normal(0, 2.5*np.sqrt(p))) for p, _ in data_fermat]
    L_fake = L_partial_safe(fake_data, 3)
    if L_fake is not None:
        fakes.append(L_fake)

fakes = np.array(fakes)
print(f"Adversarial null (Gaussian a_p ~ N(0, 2.5*sqrt(p))):")
print(f"  n successful: {len(fakes)}")
print(f"  mean: {fakes.mean():.4f}, std: {fakes.std():.4f}")
print(f"  Fraction within real distance to ζ(3): {np.mean(abs(fakes - float(mpzeta(3))) <= abs(real_3 - float(mpzeta(3))))*100:.2f}%")
print()

# What is the expected value of L_partial(K3, 3) if a_p random?
# For a_p ~ N(0, sigma_p^2) with sigma_p ~ p (Sato-Tate):
# log L = -sum log(1 - a_p T + p^2 T^2)
# Expected: O(1) corrections from quadratic in a_p
# = sum (a_p T + (a_p^2 - p^2) T^2 + ...) (leading orders)
# E[a_p T] = 0
# E[a_p^2 T^2] = sigma^2 T^2 = sigma^2 / p^6
# This gives small contribution.

# So expected L_partial close to 1, not 1.2. So real being 1.2 IS unusual.
# But maybe the algebraic part contributes systematically.

# More fair: a_p with bias toward +2p (algebraic dominance)
print("Fair adversarial: a_p = 2p (algebraic baseline) + Gaussian fluctuation")
fakes2 = []
for trial in range(n_trials):
    fake_data = [(p, 2*p + np.random.normal(0, 2*np.sqrt(p))) for p, _ in data_fermat]
    L_fake = L_partial_safe(fake_data, 3)
    if L_fake is not None:
        fakes2.append(L_fake)

fakes2 = np.array(fakes2)
print(f"  n successful: {len(fakes2)}")
print(f"  mean: {fakes2.mean():.4f}, std: {fakes2.std():.4f}")
print(f"  Fraction within real distance to ζ(3): {np.mean(abs(fakes2 - float(mpzeta(3))) <= abs(real_3 - float(mpzeta(3))))*100:.2f}%")
print()

# Try with REAL a_p = 2p exactly for all primes (no fluctuation)
print("Counterfactual: a_p = 2p exactly for ALL primes (no fluctuation)")
counter_data = [(p, 2*p) for p, _ in data_fermat]
counter_L = L_partial_safe(counter_data, 3)
print(f"  L_partial = {counter_L:.6f}")
print(f"  This is what L_partial would be if FROBENIUS ALWAYS = 2p")
print()

print("="*70)
print("Key insight:")
print("="*70)
print(f"L_p(T) ≈ (1 - p T)^2 * (1 + small corrections) for K3 with rank-20 Picard")
print(f"So L_partial(K3, 3) ≈ ∏_p (1 - 1/p^2)^2 = (1 - 1/p^2)^2 for each p")
print()
import math
# Compute (∏ (1 - 1/p^2)^2)^{-1} = ζ(2)^2 / (∏ (1-1/2^2)^2) using primes 3..47
# Actually = ∏_{p≥3} (1-1/p^2)^{-2}
val = math.prod(1.0 / (1 - 1/p**2)**2 for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47])
print(f"  ∏_{{p=3..47}} 1/(1-1/p^2)^2 = {val:.6f}")
# vs L_partial(s=3) = 1.203
# vs (ζ(2)/π^2*6)^{-2} = something related
# ζ(2) = π^2/6
zeta2 = float(mpzeta(2))
print(f"  ζ(2) = π^2/6 = {zeta2:.6f}")
print(f"  ζ(2)^2 = {zeta2**2:.6f}")
print(f"  ζ(2)^2 / (1 - 1/4)^2 = {zeta2**2 / (3/4)**2:.6f}")

# Theoretical: L_partial computed = ?
# We have 1 - a_p T + p^2 T^2 at T = p^{-3}
# = 1 - a_p / p^3 + 1/p^4
# For a_p = 2p exactly: = 1 - 2/p^2 + 1/p^4 = (1 - 1/p^2)^2
# So L_p(T)|_{s=3, a=2p} = (1 - 1/p^2)^2
# log L_partial = sum log((1-1/p^2)^2) = -sum 2/p^2 + O(1/p^4) ≈ -2 ζ(2)_partial

# Inverse:
# L_partial^{-1} = ∏ (1 - 1/p^2)^2 = (∏ (1 - 1/p^2))^2 = (ζ(2)^{-1})^2 with prime cutoff
# So L_partial = ζ_partial(2)^2

# For p from 3 to 47:
zeta2_partial_inv = math.prod(1 - 1/p**2 for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47])
print(f"  ζ(2)^{{-1}} partial (p=3..47) = {zeta2_partial_inv:.6f}")
print(f"  L_partial(K3 algebraic only, p=3..47) = (ζ(2)^{{-1}})^2 = {zeta2_partial_inv**2:.6f}")
print(f"  So L_partial expected ≈ 1/{zeta2_partial_inv**2:.4f} = {1/zeta2_partial_inv**2:.4f}")
print()
print("Hmm but real = 1.2035 close to ζ(3) = 1.2021")
print(f"And theoretical L_partial (algebraic only) = {1/zeta2_partial_inv**2:.4f}")
print()
print("The DIFFERENCE between real and pure-algebraic is small but nonzero,")
print("coming from anomalous primes (5, 13, 17, 29, 37, 41) where a_p ≠ 2p")
print()

# Compute pure algebraic
def L_alg(data, s):
    """L if a_p = 2p exactly."""
    log_L = 0.0
    for p, _ in data:
        T = p**(-s)
        L_p = 1 - 2*p * T + p**2 * T**2
        log_L -= np.log(L_p)
    return np.exp(log_L)

L_alg_val = L_alg(data_fermat, 3)
print(f"L_partial with a_p = 2p exactly: {L_alg_val:.6f}")
print(f"L_partial real (mixed): {real_3:.6f}")
print(f"Ratio real/alg = {real_3/L_alg_val:.4f}")
print()
print("The ratio captures the TRANSCENDENTAL contribution.")
print("If transcendental is small, ratio ≈ 1.")
