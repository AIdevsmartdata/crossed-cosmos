"""
The ratio L_partial(K3, 3) / L_pure_algebraic ≈ 0.783
Compare to ECI constants.
"""

import numpy as np
from mpmath import mp, mpf, zeta as mpzeta, pi as mppi
mp.dps = 30

ratio_real = 0.7830
print(f"Real ratio L_partial / L_alg = {ratio_real}")
print()
print("Compare to ECI constants:")
print(f"  ζ(3)/√π = {float(mpzeta(3) / mppi.sqrt()):.4f}  [κ_∞ candidate]")
print(f"  κ_lattice from BP2008b ≈ 0.5065  [κ(SU(2))]")
print(f"  3/4 = {3/4}")
print(f"  5/6 = {5/6:.4f}")
print(f"  4/5 = {4/5}")
print(f"  7/9 = {7/9:.4f}")
print(f"  1 - 2/9 = {1 - 2/9:.4f}")
print(f"  Catalan = 0.9160")
print(f"  ζ(3)/2 = {float(mpzeta(3))/2:.4f}")
print()
print(f"Best ratio match: 7/9 = {7/9:.4f}  (off {abs(7/9 - ratio_real)*100:.2f}%)")
print(f"                  ζ(3)/√π = {float(mpzeta(3)/mppi.sqrt()):.4f}  (off {abs(float(mpzeta(3)/mppi.sqrt()) - ratio_real)*100:.2f}%)")
print()

# Maybe the proper ratio is e^{-1/something}
# log(0.783) = -0.245
# = -log(1.278)
# 1.278 ≈ ? 4/π = 1.273, π/√6 = 1.283
print(f"log ratio = {np.log(ratio_real):.4f}")
print(f"4/π = {4/np.pi:.4f}")
print(f"Compare e^{{-0.245}} = {np.exp(-0.245):.4f}")
print(f"π/4 = {np.pi/4:.4f}, e^{{-π/12}} = {np.exp(-np.pi/12):.4f}")
print()
print("No clean match. Ratio 0.7830 is empirical, not theoretically motivated.")
print()

# Even simpler: directly compute L_partial(K3, 3) for VARIOUS truncations
# and see how it changes
data_fermat = [(3,6),(5,-26),(7,14),(11,22),(13,-42),(17,310),(19,38),(23,46),(29,-74),(31,62),(37,-218),(41,838),(43,86),(47,94)]

def L_quad(data, s, kmax=None):
    log_L = 0.0
    use_data = data[:kmax] if kmax else data
    for p, a_p in use_data:
        T = p**(-s)
        L_p = 1 - a_p * T + p**2 * T**2
        if L_p <= 0: return None
        log_L -= np.log(L_p)
    return np.exp(log_L)

print("Convergence of L_partial(K3, s=3) as we add more primes:")
for kmax in range(1, 15):
    val = L_quad(data_fermat, 3, kmax)
    primes_used = [p for p, _ in data_fermat[:kmax]]
    print(f"  Primes 3..{primes_used[-1]}: L_partial = {val:.6f}")

# Try other "natural" s values
print()
print("L_partial(K3, s) at various s:")
for s in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    val = L_quad(data_fermat, s)
    print(f"  s={s}: {val:.6f}" if val is not None else f"  s={s}: undefined")

print()
print("="*70)
print("Final verdict on H1 ζ(3) coincidence:")
print("="*70)
print("L_partial(K3, 3) ≈ 1.18-1.21 depending on truncation/approx.")
print("ζ(3) = 1.2021 is in this range.")
print("But adversarial null says random a_p sequences give similar values 3-4% of time.")
print()
print("=> H1 ζ(3) connection: PLAUSIBLE NUMERICAL HINT, NOT RIGOROUSLY ESTABLISHED.")
print("   Need higher-order L_p coefficients OR analytical proof.")
print()
print("ECI κ_∞ = ζ(3)/√π = 0.6782 candidate STILL motivated, but not derived here.")
