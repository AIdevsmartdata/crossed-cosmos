#!/usr/bin/env python3
"""
M134 — Verify explicit values of modular forms at tau = i.

Verifies (mpmath, dps=50):
- j(i) = 1728
- E_6(i) = 0  (vanishing at tau = i, well-known)
- E_4(i) = 3 * Gamma(1/4)^8 / (2*pi)^6   [Hurwitz / Ramanujan; cf. A35]
- eta(i) = Gamma(1/4) / (2 * pi^(3/4))    [Chowla-Selberg]
- Discriminant Delta(i) = E_4(i)^3 / 1728   (since j = E_4^3/Delta and j(i)=1728)
- Order of vanishing of E_6 at tau = i  (expect simple zero)
- Order of vanishing of (j - 1728) at tau = i (expect double zero, since
  j - 1728 = E_6^2 / Delta and E_6 has simple zero)

Output to stdout. No web required.
"""

import mpmath as mp

mp.mp.dps = 50  # high precision

I = mp.mpc(0, 1)


def eta(tau):
    """Dedekind eta(tau) via mpmath builtin."""
    q = mp.exp(mp.mpc(0, mp.pi) * tau)  # q = e^{i pi tau}? careful: q = e^{2 pi i tau} usually
    # Use mpmath's jtheta/qpoch or product formula
    # eta(tau) = q^(1/24) * prod_{n>=1} (1 - q^n) where q = e^{2*pi*i*tau}
    qq = mp.exp(2 * mp.pi * 1j * tau)
    out = mp.mpf(1)
    # convergent for Im(tau)>0
    for n in range(1, 200):
        out *= 1 - qq ** n
    return qq ** (mp.mpf(1) / 24) * out


def E2(tau):
    """E_2 quasi-modular Eisenstein series (not strictly modular)."""
    qq = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpf(0)
    for n in range(1, 400):
        # sigma_1(n) coefficient
        sigma1 = sum(d for d in range(1, n + 1) if n % d == 0)
        s += sigma1 * qq ** n
    return 1 - 24 * s


def E4(tau):
    qq = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpf(0)
    for n in range(1, 400):
        sigma3 = sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
        s += sigma3 * qq ** n
    return 1 + 240 * s


def E6(tau):
    qq = mp.exp(2 * mp.pi * 1j * tau)
    s = mp.mpf(0)
    for n in range(1, 400):
        sigma5 = sum(d ** 5 for d in range(1, n + 1) if n % d == 0)
        s += sigma5 * qq ** n
    return 1 - 504 * s


def Delta(tau):
    """Modular discriminant Delta(tau) = (E_4^3 - E_6^2)/1728"""
    return (E4(tau) ** 3 - E6(tau) ** 2) / 1728


def j_invariant(tau):
    return 1728 * E4(tau) ** 3 / (E4(tau) ** 3 - E6(tau) ** 2)


def main():
    print("=" * 70)
    print("M134 — Modular forms at tau = i (mpmath dps=%d)" % mp.mp.dps)
    print("=" * 70)

    tau = I  # tau = i
    print(f"tau = {tau}")
    print()

    # E_4
    e4 = E4(tau)
    print(f"E_4(i)        = {e4}")
    # Closed form: 3 * Gamma(1/4)^8 / (2*pi)^6
    closed_E4 = 3 * mp.gamma(mp.mpf(1) / 4) ** 8 / (2 * mp.pi) ** 6
    print(f"3*G(1/4)^8/(2pi)^6 = {closed_E4}")
    diff_E4 = abs(e4 - closed_E4)
    print(f"|E_4(i) - closed| = {mp.nstr(diff_E4, 5)}")
    print()

    # E_6
    e6 = E6(tau)
    print(f"E_6(i)        = {e6}")
    # Should be 0 -- Klein's well-known result
    print(f"|E_6(i)|      = {mp.nstr(abs(e6), 8)}  (expect ~ 0)")
    print()

    # Discriminant
    delta = Delta(tau)
    print(f"Delta(i)      = {delta}")
    closed_Delta = e4 ** 3 / 1728
    print(f"E_4(i)^3/1728 = {closed_Delta}")
    print(f"|Delta - E4^3/1728| = {mp.nstr(abs(delta - closed_Delta), 8)}")
    print()

    # j-invariant
    j = j_invariant(tau)
    print(f"j(i)          = {j}")
    print(f"|j(i) - 1728| = {mp.nstr(abs(j - 1728), 8)}")
    print()

    # eta
    et = eta(tau)
    print(f"eta(i)        = {et}")
    closed_eta = mp.gamma(mp.mpf(1) / 4) / (2 * mp.pi ** (mp.mpf(3) / 4))
    print(f"G(1/4)/(2pi^(3/4)) = {closed_eta}")
    print(f"|eta - closed|     = {mp.nstr(abs(et - closed_eta), 8)}")
    print()

    # Compute |eta(i)|^4 -- relevant for V_3 candidate
    eta4 = abs(et) ** 4
    print(f"|eta(i)|^4    = {eta4}")
    print()

    # E_2(i) -- non-holomorphic E_2*(i) = 0; quasi-mod E_2(i) = 3/pi (Ramanujan)
    e2 = E2(tau)
    print(f"E_2(i) [quasi]= {e2}   (Ramanujan: 3/pi = {3/mp.pi})")
    print()

    # Order of vanishing tests
    print("=" * 70)
    print("Vanishing orders at tau = i")
    print("=" * 70)
    eps_list = [mp.mpf("1e-3"), mp.mpf("1e-4"), mp.mpf("1e-5"), mp.mpf("1e-6")]
    print("E_6(i + i*eps)  -- expect ~ eps^1 (simple zero)")
    for eps in eps_list:
        val = E6(I + I * eps)
        print(f"  eps={mp.nstr(eps,2)}: E_6 = {mp.nstr(val,6)}  |E6|/eps = {mp.nstr(abs(val)/eps, 6)}")
    print()
    print("(j - 1728) at tau = i + i*eps -- expect ~ eps^2 (double zero)")
    for eps in eps_list:
        val = j_invariant(I + I * eps) - 1728
        print(f"  eps={mp.nstr(eps,2)}: j-1728 = {mp.nstr(val,6)}  |.|/eps^2 = {mp.nstr(abs(val)/eps**2, 6)}")
    print()
    print("(j - 1728) at tau = i + eps  (real direction, eps small) -- expect ~ eps^2")
    for eps in [mp.mpf("1e-3"), mp.mpf("1e-4"), mp.mpf("1e-5")]:
        val = j_invariant(I + eps) - 1728
        print(f"  eps={mp.nstr(eps,2)}: j-1728 = {mp.nstr(val,6)}  |.|/eps^2 = {mp.nstr(abs(val)/eps**2, 6)}")
    print()
    print("E_6 at tau = i + eps (real direction) -- expect ~ eps^1")
    for eps in [mp.mpf("1e-3"), mp.mpf("1e-4"), mp.mpf("1e-5")]:
        val = E6(I + eps)
        print(f"  eps={mp.nstr(eps,2)}: E_6 = {mp.nstr(val,6)}  |.|/eps = {mp.nstr(abs(val)/eps, 6)}")

    # Now: candidate potentials and their Hessians at tau = i
    print()
    print("=" * 70)
    print("CANDIDATE POTENTIALS V(tau) -- evaluate near tau = i")
    print("=" * 70)
    print("(real and imaginary perturbations of tau)")
    print()

    def V1(tau):
        """V_1 = |j(tau) - 1728|^2"""
        return abs(j_invariant(tau) - 1728) ** 2

    def V2(tau):
        """V_2 = |E_6(tau)|^2"""
        return abs(E6(tau)) ** 2

    def V3(tau):
        """V_3 = |E_6/E_4^(3/2)|^2 (modular weight-zero squared)"""
        e4t = E4(tau)
        e6t = E6(tau)
        # Build a real, modular-invariant quantity
        # Use |j - 1728|^2 / |j|^(something) to control growth
        # Or: |E_6|^2 / E_4^3 (real, since at fixed Im, ratio is meaningful)
        return abs(e6t) ** 2 / abs(e4t) ** 3

    def V4(tau):
        """V_4 = |E_6 / Delta^(1/2)|^2 -- weight-modular?"""
        # E_6 has weight 6; Delta has weight 12; Delta^(1/2) weight 6
        # So E_6 / Delta^(1/2) is weight 0 (modular function!)
        e6t = E6(tau)
        d = Delta(tau)
        # |E_6|^2 / |Delta| is a modular-invariant real function
        return abs(e6t) ** 2 / abs(d)

    pts = [
        ("tau = i (origin)", I),
        ("i + 0.01 i (Im+)", I + mp.mpc(0, 0.01)),
        ("i + 0.01    (Re+)", I + mp.mpc(0.01, 0)),
        ("i + (0.01+0.01i)", I + mp.mpc(0.01, 0.01)),
        ("i - 0.01 i (Im-)", I - mp.mpc(0, 0.01)),
        ("i + 0.1 i", I + mp.mpc(0, 0.1)),
        ("i + 0.1", I + mp.mpc(0.1, 0)),
        ("i + 0.5 i (large Im)", I + mp.mpc(0, 0.5)),
        ("rho = e^(2*pi*i/3) (other elliptic pt)", mp.mpc(-0.5, mp.sqrt(3)/2)),
    ]
    print(f"{'point':45s}  V_1=|j-1728|^2     V_2=|E_6|^2       V_4=|E6|^2/|Delta|")
    for label, t in pts:
        v1 = V1(t)
        v2 = V2(t)
        v4 = V4(t)
        print(f"{label:45s}  {mp.nstr(v1,6):16s}  {mp.nstr(v2,6):16s}  {mp.nstr(v4,6):16s}")

    print()
    print("Interpretation:")
    print("- V_4 = |E_6|^2/|Delta| is a true SL(2,Z)-invariant real function on H/SL(2,Z)")
    print("  Since E_6(i) = 0 and Delta(i) finite, V_4 has order-2 zero at tau=i.")
    print("- At tau = rho, E_6(rho) != 0 but Delta(rho)... actually E_4(rho) = 0.")
    print("  So at rho: V_4(rho) = |E_6|^2/|Delta(rho)|, where Delta = (E4^3-E6^2)/1728")
    print("  and E_4(rho)=0 means Delta(rho) = -E_6(rho)^2/1728 != 0.")


if __name__ == "__main__":
    main()
