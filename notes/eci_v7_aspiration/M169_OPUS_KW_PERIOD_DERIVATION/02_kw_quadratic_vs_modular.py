"""
M169 — Compare Kanno-Watari quadratic mass-form W (eq. 53) vs ECI v9 modular form
W_ECI = c_L (j-1728)/eta^6 + c_Q H_{-88}^2 f / eta^12.

Kanno-Watari eq. (53):
  W ~ - G_(20)(02) / (2C^(2)) * (t^(2), t^(2))_{T_X^(2)}
      - G^c.c. / (2C^(1)) * (t^(1), t^(1))_{T_X^(1)}
      + sum_{a=3}^{n} sigma_a(G_(20)(02)) * t^(1)_a * t^(2)_a

where t^(i) are *fluctuation coordinates* in M_cpx around the CM point z_(i)=z^*_(i),
NOT the global modular variable tau_(i).

The CM point sits at v_(20)^(i) (the (2,0) form). Eq. (48):
  Omega_{X^(i)} = v_(20)^(i) + t^(i) - (t^(i), t^(i))/(2C^(i)) v_(02)^(i)

so the modular variable tau parametrizes the position in D(T_0^(i)).
For T_X = T_0 = rank-2 lattice (attractive K3), the period domain D(T_0^(i)) is
H_+ U H_- (two upper half-planes) and tau is the standard upper half plane modulus.

The key question for (D)->(B) closure:
  Does the W_ECI modular form, when EXPANDED to quadratic order in delta tau
  around tau = tau_*, reproduce the KW quadratic form (eq. 53)?

If yes, then ECI v9 is the modular CONTINUATION of the KW local quadratic form to
the full SL(2,Z)-orbit, and we have a coefficient identification.

If no, then ECI v9 differs from KW even at quadratic order, and the embedding
is purely vacuum-locus.
"""
from mpmath import mp, mpc, mpf, exp, pi, sqrt, gamma, log, fabs, diff

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


def j_inv(tau, N=300):
    return E4(tau, N) ** 3 / eta(tau, N) ** 24


def W_L(tau):
    """W^L(tau) = (j - 1728) / eta^6, weight -3."""
    return (j_inv(tau) - 1728) / eta(tau) ** 6


def main():
    print("=" * 78)
    print("M169 KW quadratic-mass-form vs ECI v9 modular form")
    print("=" * 78)
    print()

    tau_L = mpc(0, 1)
    print("--- W^L expansion around tau = i ---")
    print(f"  tau = i = {tau_L}")
    print(f"  W^L(i) = {W_L(tau_L)}")

    eps = mpf("1e-6")
    # First derivative
    dW_dtau_re = (W_L(tau_L + eps) - W_L(tau_L - eps)) / (2 * eps)
    dW_dtau_im = (W_L(tau_L + 1j * eps) - W_L(tau_L - 1j * eps)) / (2j * eps)
    print(f"  dW^L/dtau at i (Re, Im method): {dW_dtau_re}, {dW_dtau_im}")
    # CM weight argument: (j-1728)/eta^6 has weight -3, so under tau -> S(tau) = -1/tau,
    # near i, (-1)^(-3) = -1, so W^L(i) is fixed by S only if W^L(i) = 0. Already verified.
    # First derivative under tau -> tau* = i, derivative also has CM constraint.
    # The Klein identity (j-1728) ~ E_6^2 means W^L = E_6^2 / eta^30, so first derivative
    # of E_6^2 vanishes at i since E_6(i) = 0 (double zero of E_6^2).
    # Hence W^L(i+delta) ~ delta^2 * (eta^{-30}) * E_6'(i)^2 + O(delta^3)
    # i.e. quadratic vanishing.

    # Second derivative
    d2W_dtau2 = (W_L(tau_L + eps) - 2 * W_L(tau_L) + W_L(tau_L - eps)) / eps**2
    print(f"  d^2 W^L / dtau^2 at i = {d2W_dtau2}")

    # Test: W^L(i + delta) ~ (1/2) * d2W * delta^2  ?
    delta = mpf("0.001")
    WL_at_pert = W_L(tau_L + delta)
    quadratic_predict = mpf(1)/2 * d2W_dtau2 * delta**2
    print(f"  delta = {delta}:")
    print(f"  W^L(i + delta)        = {WL_at_pert}")
    print(f"  (1/2) d^2W * delta^2  = {quadratic_predict}")
    print(f"  ratio                  = {WL_at_pert / quadratic_predict}")

    # E_6'(i) = derivative of E_6 at i
    dE6 = (E6(tau_L + eps) - E6(tau_L - eps)) / (2 * eps)
    print(f"  E_6'(i) = {dE6}")

    # eta(i) is real and positive
    eta_i = eta(tau_L)
    print(f"  eta(i) = {eta_i}")
    # W^L = E_6^2 / eta^30, so near tau = i (with E_6(i) = 0):
    # W^L ~ (E_6'(i) * delta)^2 / eta(i)^30
    pred_from_E6 = (dE6 * delta) ** 2 / eta_i ** 30
    print(f"  Predicted W^L(i+delta) from E_6 expansion = {pred_from_E6}")
    print(f"  ratio with actual                          = {WL_at_pert / pred_from_E6}")

    print()
    print("--- Interpretation ---")
    print()
    print("The Klein identity W^L = E_6^2 / eta^30 implies that near tau = i, where")
    print("E_6 has a SIMPLE zero, W^L has a DOUBLE zero with quadratic expansion")
    print("  W^L(i + delta) ~ (E_6'(i))^2 * delta^2 / eta(i)^30.")
    print()
    print("Compared with KW eq. (53):")
    print("  W_KW ~ - G_(20)(02) / (2 C^(2)) (t^(2), t^(2)) - c.c. (t^(1), t^(1))")
    print("         + sum_a sigma_a(G_(20)(02)) t^(1)_a t^(2)_a")
    print()
    print("This is QUADRATIC IN FLUCTUATIONS t^(i) around the CM vacuum,")
    print("matching the structure of ECI v9 W^L if we identify")
    print("  G_(20)(02) ~ (E_6'(i))^2 / (eta(i))^30 * normalisation")
    print("  t^(1) ~ delta tau_L, t^(2) ~ delta tau_Q")
    print()
    print("BUT: KW has NO sum-vs-product structure; eq. (53) is purely TENSORIAL")
    print("on T_X^(1) (x) T_X^(2). It writes a quadratic form on the 2 + 2 = 4")
    print("dimensional moduli (t^(1), t^(2)) coupling them through")
    print("  G_(20)(02) and its Galois conjugates.")
    print()
    print("ECI v9 W^L + W^Q is a SUM of independent functions on tau_L and tau_Q.")
    print("This is COMPATIBLE with KW eq. (53) ONLY at vacuum (where the cross")
    print("terms vanish identically because t^(1) = t^(2) = 0), but the FULL EFT")
    print("extension is DIFFERENT from KW: KW has cross-terms t^(1)_a t^(2)_a")
    print("with Galois-conjugate flux coefficients sigma_a(G_(20)(02)).")
    print()
    print("=> KW (53) and ECI v9 sum-W are DIFFERENT EFTs around the CM vacuum;")
    print("   they coincide only at tau_L = i, tau_Q = i sqrt(11/2)")
    print("   (= the CM/vacuum point itself).")


if __name__ == "__main__":
    main()
