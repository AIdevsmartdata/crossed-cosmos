#!/usr/bin/env python3
"""
M143 / Step 1 -- Reduce King-King best-fit tau_Q = 0.0361 + 2.352 i to the
fundamental domain F = { |Re tau| <= 1/2, |tau| >= 1 } of SL(2,Z).

If tau_Q already in F, we then compute high-precision values of:
  j(tau_Q), Delta(tau_Q), eta^2(tau_Q), E_4(tau_Q), E_6(tau_Q)

and look for algebraic relations / CM signatures.

Verifies tau_Q is the K-K Table 6 best-fit (Re=0.0361, Im=2.353 reported in M140
SUMMARY -- but Table 5 says 0.0361 + 2.352i. We use 2.352 as primary.)
"""

import mpmath as mp

mp.mp.dps = 40

N_TERMS = 300


def eta(tau):
    """Dedekind eta(tau) = q^{1/24} prod_{n>=1} (1 - q^n), q = exp(2 pi i tau)."""
    q = mp.exp(2j * mp.pi * tau)
    prod = mp.mpf(1)
    for n in range(1, N_TERMS):
        prod *= 1 - q**n
    return q**(mp.mpf(1) / 24) * prod


def E4(tau):
    """Eisenstein E_4(tau) = 1 + 240 sum_{n>=1} sigma_3(n) q^n."""
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        # sigma_3(n) = sum_{d | n} d^3
        sig = sum(d**3 for d in range(1, n + 1) if n % d == 0)
        s += sig * q**n
    return 1 + 240 * s


def E6(tau):
    """Eisenstein E_6(tau) = 1 - 504 sum_{n>=1} sigma_5(n) q^n."""
    q = mp.exp(2j * mp.pi * tau)
    s = mp.mpc(0, 0)
    for n in range(1, N_TERMS):
        sig = sum(d**5 for d in range(1, n + 1) if n % d == 0)
        s += sig * q**n
    return 1 - 504 * s


def j_invariant(tau):
    """j = 1728 E_4^3 / (E_4^3 - E_6^2)."""
    e4 = E4(tau)
    e6 = E6(tau)
    Delta = (e4**3 - e6**2) / 1728
    return e4**3 / Delta * 1


def Delta_func(tau):
    """Discriminant Delta = eta^{24} = (E_4^3 - E_6^2)/1728."""
    e = eta(tau)
    return e**24


def reduce_to_F(tau):
    """Reduce tau to fundamental domain via SL(2,Z) actions T (T tau = tau+1)
    and S (S tau = -1/tau). Returns (tau_red, list of operations)."""
    operations = []
    z = mp.mpc(tau)
    max_iter = 200
    it = 0
    while it < max_iter:
        # T-step: shift Re z to [-1/2, 1/2)
        re = mp.re(z)
        n = int(mp.floor(re + mp.mpf("0.5")))
        if n != 0:
            z = z - n
            operations.append(("T", -n))
        # S-step: if |z| < 1, replace z -> -1/z
        if abs(z) < 1 - mp.mpf("1e-30"):
            z = -1 / z
            operations.append(("S", None))
        else:
            break
        it += 1
    return z, operations


print("=" * 70)
print("M143 / Step 1 -- Fundamental domain reduction of K-K tau_Q")
print("=" * 70)
print()

tau_Q = mp.mpc("0.0361", "2.352")
print(f"K-K best-fit tau_Q = {tau_Q}")
print(f"  Re tau_Q = {mp.re(tau_Q)},  Im tau_Q = {mp.im(tau_Q)}")
print(f"  |tau_Q| = {abs(tau_Q)}")

tau_red, ops = reduce_to_F(tau_Q)
print(f"\nFundamental domain reduction:")
print(f"  ops = {ops}")
print(f"  reduced tau_Q = {tau_red}")
print(f"  Already in F? {abs(mp.re(tau_red)) <= mp.mpf('0.5') + 1e-10 and abs(tau_red) >= 1 - 1e-10}")

# Note: |tau_Q| = sqrt(0.036^2 + 2.352^2) >= 2.35 > 1, |Re tau_Q| <= 0.5  ==> already in F.

print()
print("=" * 70)
print("Modular invariants at tau_Q (mpmath dps=40, q-series N=300)")
print("=" * 70)

print("\nNote: q = exp(2 pi i tau_Q), |q| = exp(-2 pi Im tau_Q) =", float(mp.exp(-2 * mp.pi * mp.im(tau_Q))))

j_val = j_invariant(tau_Q)
print(f"\nj(tau_Q) = {j_val}")
print(f"  Re j = {mp.re(j_val)}")
print(f"  Im j = {mp.im(j_val)}")
print(f"  |j|  = {abs(j_val)}")

e4_val = E4(tau_Q)
e6_val = E6(tau_Q)
print(f"\nE_4(tau_Q) = {e4_val}")
print(f"  |E_4| = {abs(e4_val)}")
print(f"E_6(tau_Q) = {e6_val}")
print(f"  |E_6| = {abs(e6_val)}")

eta_val = eta(tau_Q)
eta2 = eta_val**2
print(f"\neta(tau_Q) = {eta_val}")
print(f"eta^2(tau_Q) = {eta2}")
print(f"  |eta|^2 = {abs(eta2)}")
Delta_val = Delta_func(tau_Q)
print(f"\nDelta(tau_Q) = {Delta_val}")
print(f"  |Delta| = {abs(Delta_val)}")

# CM signatures: for CM tau_0 corresponding to Q(sqrt(-d)) with class h(K)=1,
# j(tau_0) is an algebraic INTEGER, in particular real.
# Famous values:
#   j(i)            = 1728     (d=1)
#   j(rho)          = 0        (d=3, rho = exp(2pi i/3))
#   j(i sqrt 2)     = 8000
#   j((1+i sqrt 7)/2)  = -3375
#   j(i sqrt 3) BUT must reduce to F first
#   j((1+i sqrt 11)/2) = -32768
#   j((1+i sqrt 19)/2) = -884736
#   j((1+i sqrt 43)/2) = -884736000
#   j((1+i sqrt 67)/2) = -147197952000
#   j((1+i sqrt 163)/2) = -262537412640768000

print("\n" + "=" * 70)
print("Compare j(tau_Q) to class-number-1 imaginary quadratic CM values")
print("=" * 70)
cm_table = [
    ("Q(i),       d=1",  mp.mpc(0, 1),                                 1728),
    ("Q(rho),     d=3",  mp.exp(2j * mp.pi / 3),                       0),
    ("Q(sqrt-2),  d=2",  mp.mpc(0, mp.sqrt(2)),                        8000),
    ("Q(sqrt-7),  d=7",  (1 + 1j * mp.sqrt(7)) / 2,                    -3375),
    ("Q(sqrt-11), d=11", (1 + 1j * mp.sqrt(11)) / 2,                   -32768),
    ("Q(sqrt-19), d=19", (1 + 1j * mp.sqrt(19)) / 2,                   -884736),
    ("Q(sqrt-43), d=43", (1 + 1j * mp.sqrt(43)) / 2,                   -884736000),
    ("Q(sqrt-67), d=67", (1 + 1j * mp.sqrt(67)) / 2,                   -147197952000),
    ("Q(sqrt-163),d=163",(1 + 1j * mp.sqrt(163)) / 2,                  -262537412640768000),
]
for label, tau_cm, j_cm_known in cm_table:
    print(f"  {label}: tau_CM = {mp.nstr(tau_cm, 6)}  Im={mp.im(tau_cm)}  j_known = {j_cm_known}")

# Check: how far is tau_Q from each CM point under SL(2,Z)?
# CM points are countable -- their orbits cover h(K) points. For h=1, just one orbit per K.
# Most stringent test: distance |tau_Q - tau_CM|.
print("\nDistance |tau_Q - tau_CM| (smaller = candidate match):")
for label, tau_cm, _ in cm_table:
    d = abs(tau_Q - tau_cm)
    print(f"  {label}: dist = {mp.nstr(d, 6)}")

# Better test: compare j(tau_Q) directly:
print("\nComparison of computed j values (CM check):")
for label, tau_cm, j_cm_known in cm_table:
    # only sensible if Im tau_cm > 0
    j_cm_computed = j_invariant(tau_cm)
    diff = abs(j_val - j_cm_computed)
    print(f"  {label}: j_computed = {mp.nstr(j_cm_computed, 8)}, |j_tauQ - j_CM| = {mp.nstr(diff, 6)}")
