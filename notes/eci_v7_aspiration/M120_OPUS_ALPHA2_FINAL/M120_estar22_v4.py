"""
M120 v4: HIGH PRECISION verification using larger R and smaller eps.

By BK 2010 Functional Equation (Prop 1.3 ii), at z=w=0:
    Gamma(s) K*_a(0,0,s) = A^{a+1-2s} Gamma(a+1-s) K*_a(0,0,a+1-s)

For (a, s) = (4, 2):
    K*_4(0,0,2) = (A * 2) * K*_4(0,0,3)   where A = 1/pi for Z[i]
                = (2/pi) K*_4(0,0,3)

So we want: K*_4(0,0,3) =? varpi^4 / (6 pi)
which makes K*_4(0,0,2) = varpi^4 / (3 pi^2).

In addition, we want a CHAIN:
  e*_{0,4}(0,0; Z[i]) = K*_4(0,0,4) = sum_{gamma!=0} 1/gamma^4 = varpi^4 / 15  (Hurwitz)
  e*_{2,2}(0,0; Z[i]) = K*_4(0,0,2) = (2/pi) K*_4(0,0,3) =? varpi^4 / (3 pi^2)
"""

from mpmath import mp, mpc, mpf, sqrt, pi, gamma as Gamma, exp, fabs, re, im

mp.dps = 60

gamma14 = Gamma(mpf(1)/4)
varpi = gamma14**2 / (2 * sqrt(2 * pi))


def K_star_a_at_s_Hecke(N, a, s, eps):
    """K*_a(0,0,s; Z[i]) with Gaussian regulator exp(-eps |gamma|^2)."""
    total = mpc(0)
    for m in range(-N, N+1):
        for n in range(-N, N+1):
            if m == 0 and n == 0:
                continue
            modg2 = m*m + n*n
            gbar_a = mpc(m, -n)**a
            summand = gbar_a / mpf(modg2)**s * exp(-eps * modg2)
            total += summand
    return total


# Strategy: Richardson-extrapolate K*_4(0,0,3) from eps -> 0+
print("="*70)
print("K*_4(0,0,3): Richardson extrapolation from Hecke regularization")
print("="*70)
target_K3 = varpi**4 / (6 * pi)
print(f"Target K*_4(0,0,3) = varpi^4 / (6 pi) = {target_K3}")
print()

# Use eps values: 1e-3, 1e-4 with appropriate R
# At eps = 10^-k, R should satisfy R^2 * eps > 60-70 for tail < 1e-30
# eps=10^-3: R > 250
# eps=10^-4: R > 800
# eps=10^-5: R > 2500 — too big for naive sum

# Use moderate eps and rely on the 1/eps -> 0 linear extrapolation.
results = {}
for eps_log in [-3, -4]:
    eps = mpf(10)**eps_log
    if eps_log == -3:
        R = 350
    else:
        R = 800
    val = K_star_a_at_s_Hecke(R, 4, 3, eps)
    results[eps_log] = val
    print(f"eps = 10^{eps_log}, R = {R}: K*_4(0,0,3) ~= {val.real}")
    print(f"   diff from target: {(val.real - target_K3)}")

# Linear extrapolation: f(eps) = f(0) + eps * f'(0) + ...
# From two points (eps1, v1), (eps2, v2): v0 = (v1*eps2 - v2*eps1) / (eps2 - eps1)
e1, e2 = mpf("1e-3"), mpf("1e-4")
v1, v2 = results[-3].real, results[-4].real
v0_extrap = (v1*e2 - v2*e1) / (e2 - e1)
print()
print(f"Linear extrapolation eps -> 0+:  K*_4(0,0,3) ~= {v0_extrap}")
print(f"Target:                                       {target_K3}")
print(f"Diff after extrapolation:                     {fabs(v0_extrap - target_K3)}")
print()

# Compute K*_4(0,0,2) via functional equation
K4_0_0_2 = (2/pi) * v0_extrap
target_K2 = varpi**4 / (3 * pi**2)
print(f"K*_4(0,0,2) via BK FE = (2/pi) * K*_4(0,0,3) = {K4_0_0_2}")
print(f"Target e*_{{2,2}}(0,0; Z[i]) = varpi^4/(3 pi^2) = {target_K2}")
print(f"Diff:                                         {fabs(K4_0_0_2 - target_K2)}")
print()

# Side check: e*_{0,4}(0,0; Z[i]) = K*_4(0,0,4) = sum 1/gamma^4 (Hurwitz, varpi^4 / 15)
# This is absolutely convergent.
print("="*70)
print("SANITY: e*_{0,4}(0,0; Z[i]) = K*_4(0,0,4) = varpi^4 / 15 (Hurwitz)")
print("="*70)
target_04 = varpi**4 / 15

# K*_4(0,0,4) = sum gammabar^4 / |gamma|^8
# But: sum 1/gamma^4 (Hurwitz) is what M116 cites.
# Compare:  e*_{0,4} = K*_{0+4}(0,0,4) ?
# By Def 1.5: e*_{a,b} = K*_{a+b}(0,0,b).
# So e*_{0,4} = K*_4(0,0,4) = sum gammabar^4/|gamma|^8 = sum gammabar^4/(gamma gammabar)^4
#                          = sum 1/gamma^4.
# YES!  The sums match.

est_04 = mpc(0)
N = 300
for m in range(-N, N+1):
    for n in range(-N, N+1):
        if m == 0 and n == 0:
            continue
        est_04 += 1 / mpc(m, n)**4
print(f"K*_4(0,0,4) (N={N}) = {est_04.real}")
print(f"Target = varpi^4/15 = {target_04}")
print(f"Diff: {fabs(est_04 - target_04)}")
