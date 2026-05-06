"""
xi_crit_formula.py — Evaluable script for ξ_crit_+ upper bound (analytical, linearized).

Usage:
    python3 xi_crit_formula.py
    python3 xi_crit_formula.py --lam 1.0 --phi0 0.10 --Om 0.30

Author: M4 sub-agent (Sonnet 4.6), ECI v6.0.53.3+, 2026-05-06.
Physics: linearized KG + Friedmann around slow-roll attractor, NMC Jordan frame.
Verified: sympy algebra + numpy integration (see xi_crit_analysis.py for full derivation).

CAVEAT: The analytical bound xi_crit_analytic is ~2x the empirical A56 value.
        Use with caution — see SUMMARY.md for full discussion.
        Status: NUMERICAL-AGREEMENT-ONLY (not a tight analytical proof).
"""

import argparse
import numpy as np

# --------------------------------------------------------------------------
# ANALYTICAL FORMULA (sympy-derived, see xi_crit_analysis.py Section 3-9)
# --------------------------------------------------------------------------
#
# Linearized KG + Friedmann in N = ln(a) time, Jordan frame, NMC with
# F(phi) = M_P^2 + xi phi^2 (code convention: xi > 0 destabilizing).
#
# Effective squared mass of field perturbations:
#   M^2_eff(N) = 6*(2 + s_H(N)) * xi  -  9 * lam^2 * (V(N)/H(N)^2)
#
# where:
#   s_H(N) = d ln H / dN  (= -3/2 MD, 0 LD, -2 RD)
#   V/H^2 = 3 * Omega_phi(N)   [from modified Friedmann]
#   R/H^2 = 6*(2 + s_H)       [FRW Ricci scalar in N-time]
#
# Note: R = 0 in radiation domination => NMC coupling is inactive there.
#
# Runaway criterion:
#   integral_{N_init}^{N_f} mu_+(N) dN  >  ln(phi_crit / phi_0)
#   where:
#     mu_+(N) = 0.5 * [-(3+s_H) + sqrt((3+s_H)^2 + 4*M^2_eff)]  if M^2>0, else 0
#     phi_crit = 1/sqrt(xi)   [Friedmann denominator collapse boundary]
#
# Eigenvalue formula (sympy-verified, Section 6):
#   Stability matrix A = [[0, 1], [M^2, -(3+s_H)]]
#   Characteristic polynomial: mu^2 + (3+s_H)*mu - M^2 = 0
#   mu_pm = 0.5 * [-(3+s_H) +/- sqrt((3+s_H)^2 + 4*M^2)]
#   Runaway iff mu_+ > 0  iff  M^2 > 0  (for s_H > -3, holds all epochs).
# --------------------------------------------------------------------------


def compute_background(N_arr, Omega_m0=0.30, Omega_L0=0.70, Or0=4.18e-5):
    """
    Flat LCDM background: H^2 / H0^2 = Omega_m a^{-3} + Omega_L + Or a^{-4}.
    Returns (s_H_arr, H2_arr) over N_arr.
    """
    a_arr = np.exp(N_arr)
    H2_arr = Omega_m0 * a_arr**(-3) + Omega_L0 + Or0 * a_arr**(-4)
    # s_H = d(lnH)/dN = (1/(2H^2)) * dH^2/dN
    s_H_arr = (-1.5 * Omega_m0 * a_arr**(-3) - 2.0 * Or0 * a_arr**(-4)) / H2_arr
    return s_H_arr, H2_arr


def compute_Omega_phi(N_arr, phi0, lam, H2_arr):
    """
    Approximate Omega_phi(N) for slow-roll ECI exponential potential.
    Closure condition: V0_norm * exp(-lam*phi0) / H0^2 = Omega_L0  (at N=0).
    Approximation: phi ~ phi0 = const (slow roll, valid for phi small).
    Returns V/H^2 array.
    """
    # Omega_L0 set by closure at N=0 (a=1): H2(N=0) = Omega_m0 + Omega_L0 + Or0
    # V(phi) = V0 exp(-lam phi), with phi ~ phi0 (slow roll)
    # Closure: V0 * exp(-lam*phi0) / H0^2 = Omega_L0
    Omega_L0 = H2_arr[-1] - 0.30 - 4.18e-5  # Omega_L at N=0
    Omega_L0 = max(Omega_L0, 0.01)
    V0_norm = Omega_L0 * np.exp(lam * phi0)  # in H0^2 units
    Vn_arr = V0_norm * np.exp(-lam * phi0)   # phi = phi0 = const (slow roll)
    # V/H^2:
    V_over_H2_arr = Vn_arr / H2_arr
    return V_over_H2_arr


def compute_M2_eff(xi, lam, N_arr, s_H_arr, V_over_H2_arr):
    """
    Effective squared mass of scalar perturbations:
      M^2_eff = 6*(2+s_H)*xi - 9*lam^2 * (V/H^2)
    """
    R_over_H2_arr = 6.0 * (2.0 + s_H_arr)
    M2_arr = xi * R_over_H2_arr - 9.0 * lam**2 * V_over_H2_arr
    return M2_arr


def compute_growth_integral(xi, lam, phi0, N_init=-6.0, N_final=0.0,
                             N_pts=2000, Omega_m0=0.30):
    """
    Integrate accumulated growth rate mu_+(N) over cosmic trajectory.
    Returns (integral_mu, phi_final, phi_crit, is_runaway).
    """
    N_arr = np.linspace(N_init, N_final, N_pts)
    Omega_L0 = 1.0 - Omega_m0 - 4.18e-5
    s_H_arr, H2_arr = compute_background(N_arr, Omega_m0=Omega_m0,
                                          Omega_L0=Omega_L0)
    V_over_H2_arr = compute_Omega_phi(N_arr, phi0, lam, H2_arr)
    M2_arr = compute_M2_eff(xi, lam, N_arr, s_H_arr, V_over_H2_arr)
    friction_arr = 3.0 + s_H_arr

    # Growing eigenvalue (only where M^2 > 0):
    disc = np.maximum(friction_arr**2 + 4.0 * M2_arr, 0.0)
    mu_plus_arr = np.where(M2_arr > 0,
                           0.5 * (-friction_arr + np.sqrt(disc)),
                           0.0)
    integral_mu = float(np.trapz(mu_plus_arr, N_arr))
    phi_final = phi0 * np.exp(integral_mu)
    phi_crit = 1.0 / np.sqrt(max(xi, 1e-12))
    is_runaway = phi_final > phi_crit

    return integral_mu, phi_final, phi_crit, is_runaway


def xi_crit_formula_simple(lam, Omega_phi=0.70, s_H=-0.5):
    """
    Simple closed-form xi_crit from instantaneous instability condition M^2=0:
      xi_crit = (3/2) * lam^2 * Omega_phi / (2 + s_H)
    This is an UPPER BOUND at the epoch where xi_crit is maximum.
    The actual threshold requires growth-integral criterion (see xi_crit_numerical below).

    Parameters
    ----------
    lam : float — exponential potential slope
    Omega_phi : float — dark energy fraction at the epoch (default: today, 0.70)
    s_H : float — d(lnH)/dN at the epoch (default: -0.5, MD-LD transition)

    Returns
    -------
    xi_crit_simple : float
    """
    return 1.5 * lam**2 * Omega_phi / (2.0 + s_H)


def xi_crit_numerical(lam, phi0, Omega_m0=0.30, N_init=-6.0, N_final=0.0,
                       verbose=True):
    """
    Numerically find xi_crit_+ via bisection on the growth-integral criterion.
    Uses linearized model (slow-roll phi ~ phi0 = const approximation).

    Returns xi_crit_+ such that phi_final(xi_crit_+) = phi_crit(xi_crit_+).

    DISCLAIMER: Factor ~2 overestimate relative to A56 empirical due to
    linearization approximations. See SUMMARY.md.
    """
    lo, hi = 1e-4, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        _, pf, pc, is_runaway = compute_growth_integral(
            mid, lam, phi0, N_init=N_init, N_final=N_final, Omega_m0=Omega_m0)
        if is_runaway:
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) < 1e-6:
            break

    xi_c = 0.5 * (lo + hi)
    if verbose:
        _, pf, pc, _ = compute_growth_integral(
            xi_c, lam, phi0, N_init=N_init, N_final=N_final, Omega_m0=Omega_m0)
        print(f"  xi_crit_numerical = {xi_c:.4f}")
        print(f"  phi_final = {pf:.4f}, phi_crit = {pc:.4f}  (should be ~equal)")
        print(f"  [Note: A56 empirical ≈ 0.20 for lam~1, phi0=0.10]")
    return xi_c


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Compute analytical xi_crit_+ for NMC KG + exponential potential.")
    parser.add_argument("--lam", type=float, default=1.0,
                        help="Exponential potential slope lambda (default: 1.0)")
    parser.add_argument("--phi0", type=float, default=0.10,
                        help="Initial phi in M_P units (default: 0.10)")
    parser.add_argument("--Om", type=float, default=0.30,
                        help="Omega_matter today (default: 0.30)")
    parser.add_argument("--N_init", type=float, default=-6.0,
                        help="Start of integration in N=ln(a) (default: -6.0)")
    args = parser.parse_args()

    print("=" * 65)
    print("xi_crit ANALYTICAL FORMULA (M4, ECI v6.0.53.3+)")
    print("=" * 65)
    print(f"  Parameters: lam={args.lam}, phi0={args.phi0}, Omega_m={args.Om}")
    print()

    print("1. SIMPLE CLOSED-FORM BOUNDS (instantaneous instability, M^2=0):")
    print("   Epoch              | s_H   | Omega_phi | xi_crit_simple")
    print("   -------------------|-------|-----------|---------------")
    epochs = [
        ("Radiation (R=0)",     -2.0,  1e-4),
        ("Early MD",            -1.5,  0.010),
        ("Late MD",             -1.0,  0.10),
        ("MD-LD transition",    -0.5,  0.40),
        ("Lambda-dom (today)",   0.0,  0.70),
    ]
    for name, sH, Ophi in epochs:
        if 2 + sH <= 0:
            xc = float('inf')
            print(f"   {name:20s}| {sH:+5.1f} | {Ophi:.3f}     | inf (R=0, no NMC)")
        else:
            xc = 1.5 * args.lam**2 * Ophi / (2.0 + sH)
            print(f"   {name:20s}| {sH:+5.1f} | {Ophi:.3f}     | {xc:.4f}")

    print()
    print("   Lower bound on xi_crit (onset of formal instability, late MD):")
    xc_lower = 1.5 * args.lam**2 * 0.10 / (2.0 - 1.0)
    print(f"   xi_crit_lower (late MD, Omega_phi=0.10) = {xc_lower:.4f}")
    print()

    print("2. GROWTH-INTEGRAL xi_crit (linearized, bisection over 6 e-folds):")
    xi_c = xi_crit_numerical(args.lam, args.phi0, Omega_m0=args.Om,
                              N_init=args.N_init, verbose=True)

    print()
    print("3. SCAN OVER xi (lam={}, phi0={}):".format(args.lam, args.phi0))
    print("   xi    | int(mu+)dN | phi_final | phi_crit  | Status")
    print("   ------|------------|-----------|-----------|-------")
    xi_vals = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 1.0]
    for xi_val in xi_vals:
        ig, pf, pc, runaway = compute_growth_integral(
            xi_val, args.lam, args.phi0, N_init=args.N_init, Omega_m0=args.Om)
        status = "RUNAWAY" if runaway else "OK"
        print(f"   {xi_val:.2f}  | {ig:10.3f} | {pf:9.4f} | {pc:9.3f} | {status}")

    print()
    print("4. ECI FIDUCIAL CHECK:")
    print("   ECI Cassini-clean: xi ~ 0.001 => well inside stable regime.")
    ig_eci, pf_eci, pc_eci, _ = compute_growth_integral(
        0.001, args.lam, args.phi0, N_init=args.N_init, Omega_m0=args.Om)
    print(f"   xi=0.001: int(mu+)dN={ig_eci:.6f}, phi_final={pf_eci:.6f}  (phi_crit={pc_eci:.1f})")
    print(f"   => phi grows by factor {np.exp(ig_eci):.4f} (negligible, deeply stable)")

    print()
    print("5. COMPARISON WITH A56 EMPIRICAL:")
    print(f"   A56 empirical xi_crit_+ ≈ 0.20 (lam=1, phi0=0.10)")
    print(f"   Analytical (linearized): xi_crit_analytic = {xi_c:.4f}")
    print(f"   Ratio: {xi_c/0.20:.2f}x  [discrepancy factor]")
    print()
    print("   VERDICT: NUMERICAL-AGREEMENT-ONLY")
    print("   Analytical gives correct ORDER OF MAGNITUDE but ~2x overestimate.")
    print("   Linearization (phi=const slow-roll) misses nonlinear feedback.")
    print("   A56 full nonlinear ODE is the reliable criterion.")
    print()
    print("   FORMULA SUMMARY (symbolic, sympy-verified):")
    print("   M^2_eff = [6*(2+s_H)] * xi  -  [9*lam^2] * (V/H^2)")
    print("   xi_crit_closed = (3*lam^2 * Omega_phi) / (2*(2+s_H))")
    print("   mu_pm = 0.5*[-(3+s_H) +/- sqrt((3+s_H)^2 + 4*M^2_eff)]")
    print("   Runaway: int_N mu_+ dN > ln(1/(sqrt(xi)*phi0))")
    print("=" * 65)


if __name__ == "__main__":
    main()
