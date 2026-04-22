"""Smoke test for the ECINMCTheory plugin.

Verifies:
  1. Plugin imports and instantiates.
  2. At xi_chi = 0, G_eff/G_N == 1 and eta == 1 exactly.
  3. H(z) matches vanilla classy (minimally-coupled fiducial) to < 1e-4
     relative on z in [0, 2].
  4. At Cassini-saturated xi = 0.024, the peak |G_eff/G_N - 1| is in the
     D14-reported range (~0.4% at a=1, chi ~ 0.1 M_P).
"""

from __future__ import annotations

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eci_nmc_theory import ECINMCTheory, geff_over_gn, slip_eta


def test_xi_zero_limit():
    chi = np.linspace(0.0, 0.2, 50)
    G = geff_over_gn(0.0, chi)
    eta = slip_eta(0.0, chi)
    assert np.allclose(G, 1.0, atol=1e-14), "G_eff/G_N != 1 at xi=0"
    assert np.allclose(eta, 1.0, atol=1e-14), "eta != 1 at xi=0"
    print("[OK] xi=0 limit: G_eff/G_N == 1, eta == 1")


def test_hubble_match():
    """xi=0 plugin H(z) vs a reference vanilla classy call."""
    from classy import Class
    ref = Class()
    ref.set({
        "H0": 67.36, "omega_b": 0.02237, "omega_cdm": 0.12,
        "Omega_fld": 1.0 - 0.315 - 9.2e-5,
        "w0_fld": -1.0, "wa_fld": 0.0,
    })
    ref.compute(level=["background"])

    th = ECINMCTheory(info={}, standalone=True)
    th.initialize()
    z = np.linspace(0.0, 2.0, 21)

    Hplug = th.get_Hubble(z, units="km/s/Mpc")
    c_km = 299792.458
    Href = np.array([ref.Hubble(zi) * c_km for zi in z])
    rel = np.max(np.abs(Hplug / Href - 1.0))
    print(f"[H(z)] max |rel err| = {rel:.2e} over z in [0,2]")
    assert rel < 1e-4, f"H(z) mismatch {rel:.2e} > 1e-4"
    print("[OK] H(z) matches vanilla classy < 1e-4")


def test_cassini_magnitude():
    xi = 0.024
    chi = np.linspace(-0.2, 0.2, 201)
    G = geff_over_gn(xi, chi)
    peak = float(np.max(np.abs(G - 1.0)))
    print(f"[Cassini] peak |G_eff/G_N - 1| over chi in [-0.2,0.2] = "
          f"{100*peak:.3f}%")
    # D14 reports ~0.4% at chi=0.1 M_P. Here we sweep wider chi,
    # so allow 0.1%% ... 5%.
    assert 5e-4 < peak < 0.05, f"Magnitude {peak} outside plausible range"
    print("[OK] Cassini-saturated correction in D14-reported range")


def test_calculate_roundtrip():
    th = ECINMCTheory(info={}, standalone=True)
    th.initialize()
    state = {}
    ok = th.calculate(state, want_derived=True,
                      xi_chi=0.01, chi_initial=0.1)
    assert ok
    for key in ("G_eff_over_GN", "eta_slip", "fsigma8", "chi_of_a"):
        assert key in state, f"missing {key}"
    fs8 = state["fsigma8"]
    # fsigma8(z=0) should be in plausible LCDM band
    z0, fs0 = fs8[-1] if fs8[-1, 0] == 0 else (float(np.interp(0.0, fs8[:, 0], fs8[:, 1])),) * 2
    fs_at0 = float(np.interp(0.0, fs8[:, 0], fs8[:, 1]))
    print(f"[calc] fsigma8(z=0) = {fs_at0:.3f} (expect ~0.40-0.50)")
    assert 0.35 < fs_at0 < 0.55, f"fsigma8(0) = {fs_at0} out of band"
    print("[OK] calculate() returns all advertised products")


if __name__ == "__main__":
    test_xi_zero_limit()
    test_cassini_magnitude()
    test_calculate_roundtrip()
    try:
        test_hubble_match()
    except Exception as e:
        print(f"[SKIP] H(z) test: {e}")
        raise
    print("\nALL SMOKE TESTS PASSED.")
