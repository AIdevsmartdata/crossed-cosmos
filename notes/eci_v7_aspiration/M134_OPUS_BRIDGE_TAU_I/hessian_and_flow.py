#!/usr/bin/env python3
"""
M134 — Hessian and gradient flow analysis for V(tau) candidates.

Goal: For each candidate V(tau), compute
- Hessian at tau = i in (Re tau, Im tau) coordinates
- Eigenvalues of Hessian (mass^2 of the modulus around tau = i)
- Gradient direction at sample points around tau = i
- Determine basin of attraction toward tau = i under gradient flow

Modular invariance subtlety: A function on H/SL(2,Z) cannot be a polynomial in
tau alone; it must be SL(2,Z)-invariant. The natural Kahler-style action for a
modulus is:

    S = int d^4x sqrt(-g) [ (3/(Im tau)^2) (d tau)(d bar tau) - V(tau, bar tau) ]

The kinetic term comes from the Poincare metric on H. The gradient flow uses
the Kahler metric:

    G^{tau bar tau} = (Im tau)^2 / 3   (inverse Kahler metric, weight-2 modulus)

So d tau / dt = - G^{tau bar tau} * d V / d bar tau.

Real-coordinate physics: write tau = tau_1 + i tau_2 (tau_2 > 0).
Kahler metric in real coords:  g_{ij} = (3 / (2 tau_2^2)) delta_{ij}   (i,j in {1,2})
  -- this is just the Poincare half-plane metric (factor 3 = N=1 SUGRA convention).
Inverse: g^{ij} = (2 tau_2^2 / 3) delta_{ij}.

So mass^2 (canonically normalized) at tau = i (where tau_2 = 1):
    m^2 = g^{ij} d_i d_j V = (2/3) (d_1^2 V + d_2^2 V)
  evaluated at tau = i.

For a Kahler potential K = -3 log(-i(tau - bar tau)), one finds the
N=1 SUGRA scalar potential V_F = e^K (|D W|^2 - 3 |W|^2) where D = d_tau + (d_tau K).

We start with simple "toy" candidates V(tau, bar tau) (real) and compute:
  H_{ij} = d_i d_j V at tau = i

If H is positive-definite, tau = i is a local min.
"""

import mpmath as mp

mp.mp.dps = 40

I = mp.mpc(0, 1)


# ---------------------------------------------------------------------------
# Modular form numerics (recompute here)

def E4(tau, terms=300):
    qq = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpf(0)
    for n in range(1, terms):
        sigma3 = sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
        s += sigma3 * qq ** n
    return 1 + 240 * s


def E6(tau, terms=300):
    qq = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpf(0)
    for n in range(1, terms):
        sigma5 = sum(d ** 5 for d in range(1, n + 1) if n % d == 0)
        s += sigma5 * qq ** n
    return 1 - 504 * s


def Delta_(tau):
    return (E4(tau) ** 3 - E6(tau) ** 2) / 1728


def j_(tau):
    e4 = E4(tau)
    e6 = E6(tau)
    return 1728 * e4 ** 3 / (e4 ** 3 - e6 ** 2)


# ---------------------------------------------------------------------------
# Candidate potentials  V : H -> R+

def V1(tau):
    """V_1 = |j(tau) - 1728|^2"""
    return abs(j_(tau) - 1728) ** 2


def V2(tau):
    """V_2 = |E_6(tau)|^2 -- NOT a modular invariant, has weight (6,6) under SL(2,Z)"""
    return abs(E6(tau)) ** 2


def V_inv2(tau):
    """V_4 = |E_6|^2 / |Delta|  -- TRUE modular invariant (weight 0)
    Has order-2 zero at tau = i, finite everywhere on H."""
    return abs(E6(tau)) ** 2 / abs(Delta_(tau))


def V_inv3(tau):
    """V_5 = (|j - 1728|^2) / (1 + |j|^2)^c -- bounded modular invariant
    Use c=1 for now: regulates growth as Im tau -> 0 (cusp / SL2Z).
    """
    j = j_(tau)
    return abs(j - 1728) ** 2 / (1 + abs(j) ** 2)


def V_im_norm(tau):
    """V_im = |E_6|^2 (Im tau)^6 -- absolute-value-squared of weight-6 form
    times (Im tau)^6 so it becomes weight-0 (Petersson-like).
    THIS is the proper modular-invariant 'norm-squared' of E_6."""
    return abs(E6(tau)) ** 2 * mp.im(tau) ** 6


def V_pets_E4(tau):
    """V_E4 = |E_4|^2 (Im tau)^4 -- weight-0 invariant; finite at tau=i"""
    return abs(E4(tau)) ** 2 * mp.im(tau) ** 4


def V_eta(tau):
    """V_eta = |eta(tau)|^4 (Im tau) -- weight-0 invariant ('Petersson eta')
    eta has weight 1/2; |eta|^4 has weight 1+1=2; multiply by Im(tau)^2 not 1."""
    # Recompute eta
    qq = mp.exp(2 * mp.pi * 1j * tau)
    e = mp.mpf(1)
    for n in range(1, 100):
        e *= 1 - qq ** n
    eta = qq ** (mp.mpf(1) / 24) * e
    # |eta|^4 has weight 2 (since eta has weight 1/2), so to get weight-0 multiply by Im(tau)^2
    return abs(eta) ** 4 * mp.im(tau) ** 2


def V_racetrack(tau, A=1.0, B=2.0, a=1.0, b=2.0):
    """Racetrack-style toy potential:
       V = |A e^(i a tau) - B e^(i b tau)|^2  [non-perturbative gaugino condensate-like]
       Selected to have minimum at some tau = i*tau_2  but generally not at tau=i unless
       tuned. We tune A=B*(b/a)^? to put minimum at tau = i if possible.
    """
    return abs(A * mp.exp(1j * a * tau) - B * mp.exp(1j * b * tau)) ** 2


# ---------------------------------------------------------------------------
# Numerical Hessian wrt (Re tau, Im tau)

def hessian_real_coords(V, tau0, h=mp.mpf("1e-3")):
    """5-point stencil Hessian of V in real coords (x, y) where tau = x + i y."""
    x0 = mp.re(tau0)
    y0 = mp.im(tau0)

    def f(x, y):
        return mp.re(V(mp.mpc(x, y)))  # potential is real-valued on H

    # Pure xx
    Vxx = (f(x0 + h, y0) - 2 * f(x0, y0) + f(x0 - h, y0)) / h ** 2
    # Pure yy
    Vyy = (f(x0, y0 + h) - 2 * f(x0, y0) + f(x0, y0 - h)) / h ** 2
    # Mixed xy: 4-point
    Vxy = (
        f(x0 + h, y0 + h)
        - f(x0 + h, y0 - h)
        - f(x0 - h, y0 + h)
        + f(x0 - h, y0 - h)
    ) / (4 * h * h)
    return Vxx, Vyy, Vxy


def gradient_real(V, tau0, h=mp.mpf("1e-3")):
    x0 = mp.re(tau0)
    y0 = mp.im(tau0)

    def f(x, y):
        return mp.re(V(mp.mpc(x, y)))

    gx = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
    gy = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)
    return gx, gy


def analyze(name, V, taus_test=None, h=mp.mpf("1e-3")):
    print(f"\n{'='*70}\n{name}\n{'='*70}")
    # Hessian at tau = i
    Vxx, Vyy, Vxy = hessian_real_coords(V, I, h)
    print(f"V(i)         = {mp.nstr(mp.re(V(I)), 8)}")
    print(f"H_xx         = {mp.nstr(Vxx, 8)}")
    print(f"H_yy         = {mp.nstr(Vyy, 8)}")
    print(f"H_xy         = {mp.nstr(Vxy, 8)}")
    # Eigenvalues
    trace = Vxx + Vyy
    det = Vxx * Vyy - Vxy ** 2
    disc = (Vxx - Vyy) ** 2 + 4 * Vxy ** 2
    lam1 = (trace + mp.sqrt(disc)) / 2
    lam2 = (trace - mp.sqrt(disc)) / 2
    print(f"eigenvalues  = ({mp.nstr(lam1, 8)}, {mp.nstr(lam2, 8)})")
    print(f"det(H)       = {mp.nstr(det, 8)}")
    if mp.re(det) > 0 and mp.re(trace) > 0:
        print("  --> tau = i is a LOCAL MINIMUM (positive-definite Hessian)")
    elif mp.re(det) < 0:
        print("  --> tau = i is a SADDLE POINT")
    else:
        print("  --> degenerate (det ~ 0): higher-order analysis needed")

    # Mass^2 with Kahler metric g^{ij} = (2 tau_2^2 / 3) delta_{ij} at tau_2=1:
    # m^2 = g^{ij} H_{ij} = (2/3) (Vxx + Vyy)  [no off-diag in Kahler from Im tau alone]
    m_sq = mp.mpf(2) / 3 * (Vxx + Vyy)
    print(f"m^2 (Kahler) = (2/3)(H_xx+H_yy) = {mp.nstr(m_sq, 8)}")

    # Sample gradient at nearby points: does -grad V point toward tau=i?
    if taus_test is None:
        taus_test = [
            mp.mpc(0.05, 1.0),
            mp.mpc(-0.05, 1.0),
            mp.mpc(0.0, 1.05),
            mp.mpc(0.0, 0.95),
            mp.mpc(0.05, 1.05),
            mp.mpc(-0.05, 0.95),
        ]
    print("\nGradient flow check: -gradV at sample tau (should point toward i):")
    print(f"  {'tau':25s}  {'-gx':15s}  {'-gy':15s}  {'pts toward i?':15s}")
    for t in taus_test:
        gx, gy = gradient_real(V, t, h)
        # Direction toward tau=i is (-Re t, 1 - Im t)
        dx_to_i = -mp.re(t)
        dy_to_i = 1 - mp.im(t)
        # Cosine of angle between -grad and (toward i)
        norm_grad = mp.sqrt(gx ** 2 + gy ** 2)
        norm_dir = mp.sqrt(dx_to_i ** 2 + dy_to_i ** 2)
        if norm_grad > 0 and norm_dir > 0:
            cos_angle = (-gx * dx_to_i + -gy * dy_to_i) / (norm_grad * norm_dir)
        else:
            cos_angle = 0
        print(
            f"  {str(t):25s}  {mp.nstr(-gx, 5):15s}  {mp.nstr(-gy, 5):15s}  cos={mp.nstr(cos_angle, 5)}"
        )


def main():
    print("M134 -- Hessian + gradient flow for V(tau) candidates")
    print(f"Working at mp.dps = {mp.mp.dps}")

    # 1. V_1 = |j - 1728|^2
    analyze("V_1 = |j(tau) - 1728|^2  (Klein j-invariant deviation, NOT modular invariant under |.|^2)", V1)

    # 2. V_2 = |E_6|^2  (not modular invariant)
    analyze("V_2 = |E_6(tau)|^2  (weight-12 -- NOT invariant)", V2)

    # 3. V_inv2 = |E_6|^2 / |Delta|  (modular invariant)
    analyze("V_inv2 = |E_6|^2 / |Delta|  (TRUE SL(2,Z) invariant)", V_inv2)

    # 4. V_im_norm = |E_6|^2 (Im tau)^6 (Petersson norm of E_6)
    analyze("V_pets_E6 = |E_6|^2 (Im tau)^6  (Petersson-like norm of weight-6 form)", V_im_norm)

    # 5. V_pets_E4 -- check that this has minimum NOT at tau=i (since E_4(i) != 0)
    analyze("V_pets_E4 = |E_4|^2 (Im tau)^4  (Petersson norm of E_4) -- expect MIN at rho not at i", V_pets_E4)

    # 6. V_eta -- |eta|^4 (Im tau)^2  -- vanishes at cusp Im->infty, what about i?
    analyze("V_eta = |eta(tau)|^4 (Im tau)^2  (Petersson norm of eta squared)", V_eta)


if __name__ == "__main__":
    main()
