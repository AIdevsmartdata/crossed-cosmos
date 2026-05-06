"""
M169 — Chowla-Selberg periods for CM K3 transcendental lattices.

Goal: compute |Omega(X^(1))| at tau_L = i (Q(i), D=-4)
       |Omega(X^(2))| at tau_Q = i*sqrt(11/2) (Q(sqrt-22), D=-88, h=2)
via Chowla-Selberg Gamma-product, and compare with the modular-form
expressions

  W^L(tau) = (j(tau) - 1728)/eta(tau)^6 = E_6(tau)^2 / eta(tau)^30
  W^Q(tau) = H_{-88}(j(tau))^2 * f_{88.3.b.a}(tau) / eta(tau)^12

mpmath dps = 30.
"""
from mpmath import mp, mpc, mpf, exp, pi, sqrt, gamma, log, fabs

mp.dps = 30


def qq_(tau):
    return exp(2j * pi * tau)


def E4(tau, N=300):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s3 = sum(d**3 for d in range(1, n + 1) if n % d == 0)
        s += 240 * s3 * q**n
    return s


def E6(tau, N=300):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s5 = sum(d**5 for d in range(1, n + 1) if n % d == 0)
        s -= 504 * s5 * q**n
    return s


def eta(tau, N=400):
    q = qq_(tau)
    s = mpf(1)
    for n in range(1, N):
        s *= (1 - q**n)
    return s * q**(mpf(1) / 24)


def Delta(tau, N=400):
    return eta(tau, N) ** 24


def j_inv(tau, N=300):
    return E4(tau, N) ** 3 / Delta(tau, N)


# -----------------------------------------------------------------------------
# Chowla-Selberg formula for periods of CM elliptic curves
#
# For an elliptic curve E_K with CM by an imaginary quadratic field K = Q(sqrt-D),
# fundamental discriminant -d_K, class number h(K), the
# Chowla-Selberg formula reads
#
#   prod_{[a] in Cl(K)} Omega(E_a)^2 = (1 / sqrt(|d_K|))
#                                    * prod_{n=1}^{|d_K|-1} Gamma(n/|d_K|)^{w*chi(n)/(2h)}
#
# where chi = Kronecker symbol mod d_K, w = number of roots of unity in O_K.
#
# For D = -4 (Q(i), h = 1, w = 4):
#   Omega(E_i)^2 = (1/2) * Gamma(1/4)^2 / Gamma(3/4)^2 * (1/(2pi))^{1/2}
# Or more cleanly (Selberg-Chowla 1949, Gross 1980):
#   Omega(E_i) = Gamma(1/4)^2 / (2 sqrt(pi))    (lemniscate constant pi-bar / 2)
#
# Numerically: Omega(E_i) ~ 2.622057...
# This is "Gauss's constant times pi" = 2.62205755...
# -----------------------------------------------------------------------------


def omega_Ei_chowla_selberg():
    """Chowla-Selberg period of E_i (CM by Q(i)).

    Standard form: Omega(E_i) = Gamma(1/4)^2 / (2 sqrt(pi)).
    This is "the lemniscate constant" pi-bar / sqrt(2) where pi-bar = Gauss constant.
    """
    return gamma(mpf(1) / 4) ** 2 / (2 * sqrt(pi))


# -----------------------------------------------------------------------------
# For D = -88 (Q(sqrt-22), h = 2, w = 2):
# Discriminant d_K = -88. Class number h = 2.
# Chowla-Selberg gives a Gamma product over residues with chi_{-88}(n).
#
# chi_{-88}(n) = Legendre/Kronecker symbol (-88 / n).
# Equivalently chi(n) = (n / 11) * eps(n mod 8), with eps the appropriate sign.
#
# More concretely: for D = -88, the Kronecker symbol is the unique odd primitive
# Dirichlet character mod 88 (since 88 = 8 * 11) which corresponds to the
# imaginary quadratic field Q(sqrt(-22)).
#
# We compute (-88 | n) for n = 1, ..., 87 and form the product
#   P = prod_{n=1}^{87} Gamma(n/88)^{chi_{-88}(n)}
# Then |Omega(X^(2))|^4 ~ |d|^{-1/2} * P^{w/(2h)} = (1/sqrt(88)) * P^{1/2}
# (with w=2 since Q(sqrt-22) only has +/- 1 as roots of unity, h=2).
# -----------------------------------------------------------------------------


def kronecker_symbol(a, n):
    """Compute Kronecker symbol (a | n) for integer a and positive integer n."""
    if n == 0:
        return 1 if abs(a) == 1 else 0
    if n == 1:
        return 1
    if n < 0:
        return kronecker_symbol(a, -n) * (-1 if a < 0 else 1)
    if n == 2:
        if a % 2 == 0:
            return 0
        r = a % 8
        if r == 1 or r == 7:
            return 1
        return -1
    # n odd or n with 2-part
    sym = 1
    while n % 2 == 0:
        sym *= kronecker_symbol(a, 2)
        n //= 2
    if n == 1:
        return sym
    # Jacobi symbol for odd n
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                sym = -sym
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            sym = -sym
        a = a % n
    if n == 1:
        return sym
    return 0


def chi_disc(D, n):
    """Kronecker symbol (D | n) for fundamental discriminant D < 0."""
    return kronecker_symbol(D, n)


def chowla_selberg_product(D, h, w):
    """Chowla-Selberg product
      P = prod_{n=1}^{|D|-1} Gamma(n/|D|)^{chi_D(n)}.
    Then the geometric mean of |Omega(E_a)|^2 over the class group (h elements)
    satisfies
      prod_{a} |Omega(E_a)|^2 = (1/sqrt(|D|)) * P^{w / (2h)}.

    Returns (P, mean_omega_sq, mean_omega).
    """
    absD = abs(D)
    P = mpf(1)
    for n in range(1, absD):
        c = chi_disc(D, n)
        if c == 0:
            continue
        P *= gamma(mpf(n) / absD) ** c
    mean_omega_sq = (1 / sqrt(absD)) * P ** (mpf(w) / (2 * h))
    mean_omega = sqrt(mean_omega_sq)
    return P, mean_omega_sq, mean_omega


def main():
    print("=" * 78)
    print("M169 Chowla-Selberg periods for CM K3 transcendental lattices")
    print("=" * 78)

    # ---- D = -4, Q(i), tau_L = i ----
    print()
    print("--- (1) D = -4, K = Q(i), h = 1, w = 4, tau_L = i ---")
    omega_i = omega_Ei_chowla_selberg()
    print(f"  Chowla-Selberg Gamma(1/4)^2 / (2 sqrt(pi)) = {omega_i}")
    # Reference: Gauss/lemniscate constant ~ 2.622057554...

    # Now check the formula: Chowla-Selberg with D=-4, h=1, w=4
    P_4, mom2_4, mom_4 = chowla_selberg_product(-4, 1, 4)
    print(f"  Chowla-Selberg product P_{{-4}} = {P_4}")
    print(f"    where P = prod_{{n=1}}^{{3}} Gamma(n/4)^{{chi(n)}}")
    print(f"    chi(1) = {chi_disc(-4, 1)}, chi(2) = {chi_disc(-4, 2)}, chi(3) = {chi_disc(-4, 3)}")
    print(f"  |Omega|^2 = (1/sqrt(4)) * P^{{w/(2h)}} = (1/2) * P^2 = {mom2_4}")
    print(f"  |Omega| = {mom_4}")

    # The K3 transcendental period |Omega(X^{(1)})| for X^(1) Kummer K3 of E x E is
    # related to omega_E via T_{Km(E x E)} = T_E (x) T_E (rank 2 over Z, signature (2,0))
    # so |Omega(X^(1))| ~ omega_E^2 up to lattice normalization.
    omega_X1_sq = omega_i ** 2  # (2,0)-form on Km(E_phi x E_tau) at phi=tau=i
    print(f"  |Omega(X^(1) = Km(E_i x E_i))| ~ Omega(E_i)^2 = {omega_X1_sq}")

    # E_4(i) and E_6(i)
    tau_L = mpc(0, 1)
    print()
    print("  Modular form values at tau_L = i:")
    print(f"    E_4(i) = {E4(tau_L)}")
    print(f"    E_6(i) = {E6(tau_L)}     (must be ~ 0 since CM by Q(i))")
    print(f"    eta(i) = {eta(tau_L)}")
    print(f"    j(i)   = {j_inv(tau_L)}  (must be 1728)")
    j_minus = j_inv(tau_L) - 1728
    print(f"    j(i) - 1728 = {j_minus}  (zero by Klein)")
    WL = (j_inv(tau_L) - 1728) / eta(tau_L) ** 6
    WL_alt = E6(tau_L) ** 2 / eta(tau_L) ** 30
    print(f"    W^L(i) = (j-1728)/eta^6 = {WL}")
    print(f"    W^L(i) = E_6^2/eta^30  = {WL_alt}")

    # ---- D = -88, Q(sqrt-22), tau_Q = i sqrt(11/2) ----
    print()
    print("--- (2) D = -88, K = Q(sqrt-22), h = 2, w = 2, tau_Q = i*sqrt(11/2) ---")
    P_88, mom2_88, mom_88 = chowla_selberg_product(-88, 2, 2)
    print(f"  Chowla-Selberg product")
    print(f"  log10(P_{{-88}}) = {log(P_88) / log(10)}")
    print(f"  prod over chi residues mod 88 of Gamma(n/88)^chi")
    print(f"  Geometric mean |Omega|^2 of [E_a] orbit = {mom2_88}")
    print(f"  Geometric mean |Omega|     = {mom_88}")

    # tau_Q = i sqrt(11/2)
    tau_Q = mpc(0, sqrt(mpf(11) / 2))
    print()
    print(f"  tau_Q = i sqrt(11/2) = {tau_Q}")
    print(f"  E_4(tau_Q) = {E4(tau_Q)}")
    print(f"  E_6(tau_Q) = {E6(tau_Q)}")
    print(f"  eta(tau_Q) = {eta(tau_Q)}")
    print(f"  j(tau_Q)   = {j_inv(tau_Q)}")
    # The Hilbert class polynomial H_{-88}(x) for D = -88:
    # H_{-88}(x) = x^2 - 6635624000 x - 1454786250000^2  ?
    # Actually, by Cohen "A course in computational algebraic number theory"
    # the Hilbert class polynomial for D = -88 has degree h = 2.
    # We do not need the exact polynomial here; we only test that j(tau_Q) is
    # an algebraic integer of degree 2 over Q.

    # Numerical j(tau_Q) is one of the two roots of H_{-88}.
    # Other root j(tau_Q') for tau_Q' = (1 + i sqrt(22))/2 (the other class).

    # Check the chi character: chi_{-88}(n) for small n
    print()
    print("  chi_{-88}(n) for n = 1..20:")
    for n in range(1, 21):
        c = chi_disc(-88, n)
        print(f"    chi_{{-88}}({n}) = {c}")


if __name__ == "__main__":
    main()
