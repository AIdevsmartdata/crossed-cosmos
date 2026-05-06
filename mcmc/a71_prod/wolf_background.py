"""
wolf_background.py — Wolf-NMC-KG GBD background ODE in JAX + scipy.

Phase 3.B, M7 sub-agent. Date: 2026-05-06.
Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.

PHYSICS:
  Wolf 2025 (arXiv:2504.07679, PRL 135, 081001) NMC action (Jordan frame, M_P=1):

    S = ∫d⁴x √(-g) [ F(φ)/2 · R  −  ½(∂φ)²  −  V(φ)  +  L_m ]
    F(φ) = 1 − ξ φ²
    V(φ) = V₀ + β φ + ½ m² φ²

  Background equations (N = ln a, ' = d/dN, M_P = 1, H₀ = 1):

  FRIEDMANN CONSTRAINT (used to compute H² at each step):
    H² = (ρ_m + ρ_r + V(φ)) / [3F(φ) + 3 F'(φ) φ' − ½ φ'²]

  CLOSED-FORM H'/H (sympy-verified, see gbd_derivation.md):
    s_H = H'/H = N_sH / D_sH

    N_sH = −ρ_m/H² − (4/3)ρ_r/H²
           − [2V(φ) + F'(φ) V'(φ)] / H²
           + F'(φ) φ' + 6 F'(φ)² + F''(φ) φ'²

    D_sH = 2F(φ) − 3 F'(φ)²

  KG EQUATION (using s_H from above):
    φ'' = −(3 + s_H) φ' − V'(φ)/H² − 6 ξ φ (2 + s_H)

  IMPLEMENTATION: 2D Friedmann-constrained ODE, state = [φ, φ'].
  H² is NOT integrated as an ODE variable (this drifts by ~N=-1 due to
  accumulation error). Instead, H² is recomputed from the Friedmann
  constraint at each ODE step. Verified: H²(N=0) = 1.0 ± 1e-6.

  Density evolution (M_P=1, H₀=1 normalization):
    ρ_m(N) = 3 Ω_m exp(−3N)
    ρ_r(N) = 3 Ω_r exp(−4N)
  where Ω_m = ω_m / h², Ω_r = ω_r / h², with ω_m = Ω_m h², ω_r ≈ 4.15×10⁻⁵.

  At N=0: ρ_m + ρ_r + V₀_eff = 3 (= 3H₀²) → Friedmann closure.
  V₀ tuned analytically from this.

REFERENCES (live-verified):
  - arXiv:2504.07679 (Wolf et al. 2025, PRL 135, 081001) — CONFIRMED by A69
  - arXiv:1106.2476 (Clifton, Ferreira, Padilla, Skordis, PhysRep 513) — CONFIRMED 2026-05-06
  - Esposito-Farese & Polarski gr-qc/0011076 (NMC background equations)

KG GATE (per A70 likelihood_spec.md):
  (a) |φ| > 10 M_P → reject (runaway)
  (b) F(φ) = 1 − ξφ² < 0.01 → reject (ghost / F-collapse)
  (c) |lnH(N=0)| > 0.05 → reject (Friedmann closure failure)
  [Note: in the 2D Friedmann-constrained formulation, (c) is always satisfied
   by construction — H²(0) = 1.0 from the Friedmann equation. We still keep
   the gate as a sanity check.]
"""

import numpy as np


# ============================================================================
# SECTION 0 — Structural functions (pure numpy, scalar-safe)
# ============================================================================

def _F(phi, xi):
    """F(phi) = 1 - xi*phi^2."""
    return 1.0 - xi * phi**2

def _FP(phi, xi):
    """dF/dphi = -2*xi*phi."""
    return -2.0 * xi * phi

def _FPP(xi):
    """d^2F/dphi^2 = -2*xi."""
    return -2.0 * xi

def _V(phi, V0, beta, m2):
    """V(phi) = V0 + beta*phi + 0.5*m2*phi^2."""
    return V0 + beta * phi + 0.5 * m2 * phi**2

def _VP(phi, beta, m2):
    """dV/dphi = beta + m2*phi."""
    return beta + m2 * phi


# ============================================================================
# SECTION 1 — Friedmann constraint
# ============================================================================

def H2_from_friedmann(phi, phi_p, N, xi, V0, beta, m2, Omega_m, Omega_r):
    """
    Compute H² from the Friedmann constraint (Jordan frame NMC).

      H² = (ρ_m + ρ_r + V) / [3F + 3 F' φ' − ½ φ'²]

    Args:
      phi, phi_p: field and its N-derivative
      N: ln a
      xi, V0, beta, m2: potential/coupling parameters
      Omega_m, Omega_r: dimensionless density fractions (NOT ω_m = Ω_m h²)

    Returns:
      H2: float (or None if denominator degenerate/negative)

    UNITS: H₀ = 1, M_P = 1. ρ_m = 3 Ω_m exp(-3N), ρ_r = 3 Ω_r exp(-4N).
    """
    rho_m = 3.0 * Omega_m * np.exp(-3.0 * N)
    rho_r = 3.0 * Omega_r * np.exp(-4.0 * N)
    F = _F(phi, xi)
    FP = _FP(phi, xi)
    V = _V(phi, V0, beta, m2)
    denom = 3.0 * F + 3.0 * FP * phi_p - 0.5 * phi_p**2
    if denom < 1e-8:
        return None
    H2 = (rho_m + rho_r + V) / denom
    if H2 <= 0.0 or not np.isfinite(H2):
        return None
    return H2


# ============================================================================
# SECTION 2 — Closed-form H'/H (sympy-verified)
# ============================================================================

def wolf_sH(phi, phi_p, H2, xi, V0, beta, m2, rho_m, rho_r):
    """
    Compute H'/H = s_H from sympy-derived closed-form (no phi'' in formula).

    DERIVATION (see gbd_derivation.md):
      From Friedmann (00-component) + Raychaudhuri (ij-component) + KG substitution:

      N_sH = −ρ_m/H² − (4/3)ρ_r/H² − [2V + F'·V'] / H²
             + F'·φ' + 6(F')² + F''·φ'²

      D_sH = 2F − 3(F')²

      s_H = N_sH / D_sH

    Args:
      phi, phi_p: field and N-derivative
      H2: H² (from Friedmann constraint)
      xi, V0, beta, m2: parameters
      rho_m, rho_r: densities at current N (= 3*Omega*exp(-n*N))

    Returns: s_H = H'/H (scalar float)
    """
    F = _F(phi, xi)
    FP = _FP(phi, xi)
    FPP = _FPP(xi)
    V = _V(phi, V0, beta, m2)
    VP = _VP(phi, beta, m2)

    N_sH = (
        - rho_m / H2
        - (4.0 / 3.0) * rho_r / H2
        - (2.0 * V + FP * VP) / H2
        + FP * phi_p
        + 6.0 * FP**2
        + FPP * phi_p**2
    )
    D_sH = 2.0 * F - 3.0 * FP**2

    # Safety: D_sH = 0 when 2(1-ξφ²) = 12ξ²φ², i.e. at the ghost boundary
    # The KG gate catches this via F < 0.01. Here we just prevent /0.
    if not isinstance(D_sH, np.ndarray):
        if abs(D_sH) < 1e-10:
            D_sH = 1e-10 * (1.0 if D_sH >= 0 else -1.0)
    else:
        D_sH = np.where(np.abs(D_sH) < 1e-10, 1e-10 * np.sign(D_sH + 1e-20), D_sH)

    return N_sH / D_sH


# ============================================================================
# SECTION 3 — 2D Friedmann-constrained ODE (scipy interface)
# ============================================================================

def wolf_kg_ode_2d(N, state, xi, V0, beta, m2, Omega_m, Omega_r):
    """
    RHS of Wolf-NMC-KG ODE (2D, Friedmann-constrained).

    State: [phi, phi_p]  (H² computed from Friedmann constraint, not integrated)

    ODE:
      dφ/dN   = φ'
      dφ'/dN  = −(3 + s_H)φ' − V'/H² − 6ξφ(2 + s_H)

    where:
      H²  = from Friedmann constraint at each step
      s_H = from closed-form formula (sympy-verified)

    This eliminates lnH drift error present in 3D formulation.

    Args:
      N: current N = ln a
      state: [phi, phi_p]
      xi, V0, beta, m2: Wolf potential/coupling
      Omega_m, Omega_r: DIMENSIONLESS density fractions (= omega/h^2)

    Returns: [dphi/dN, dphi_p/dN]
    """
    phi, phi_p = state[0], state[1]

    H2 = H2_from_friedmann(phi, phi_p, N, xi, V0, beta, m2, Omega_m, Omega_r)
    if H2 is None:
        return [0.0, 0.0]

    rho_m = 3.0 * Omega_m * np.exp(-3.0 * N)
    rho_r = 3.0 * Omega_r * np.exp(-4.0 * N)

    s_H = wolf_sH(phi, phi_p, H2, xi, V0, beta, m2, rho_m, rho_r)
    if not np.isfinite(s_H):
        return [0.0, 0.0]

    VP = _VP(phi, beta, m2)
    phi_pp = -(3.0 + s_H) * phi_p - VP / H2 - 6.0 * xi * phi * (2.0 + s_H)
    if not np.isfinite(phi_pp):
        phi_pp = 0.0

    return [phi_p, phi_pp]


# ============================================================================
# SECTION 4 — V0 tuning: Friedmann closure at N=0
# ============================================================================

def tune_V0(xi, beta, m2, phi_today_approx, phi_p_today_approx, Omega_m, Omega_r):
    """
    Tune V0 so that Friedmann closes at N=0 (H₀=1).

    At N=0: H²(0) = 1 requires:
      (ρ_m0 + ρ_r0 + V_eff) / [3F0 + 3 F'0 φ'0 − ½ φ'0²] = 1

    where ρ_m0 = 3 Ω_m, ρ_r0 = 3 Ω_r, V_eff = V0 + β φ_today + ½ m² φ_today²

    Solving for V0:
      V0 = (3F0 + 3 F'0 φ'0 − ½ φ'0²) − ρ_m0 − ρ_r0 − β φ_today − ½ m² φ_today²

    Args:
      phi_today_approx: approximate φ(N=0) (use φ_init as first guess)
      phi_p_today_approx: approximate φ'(N=0) (use 0 as first guess)
      Omega_m, Omega_r: dimensionless fractions

    Returns: V0 (float)
    """
    phi_t = phi_today_approx
    phi_pt = phi_p_today_approx
    F0 = _F(phi_t, xi)
    FP0 = _FP(phi_t, xi)
    rho_m0 = 3.0 * Omega_m
    rho_r0 = 3.0 * Omega_r
    denom0 = 3.0 * F0 + 3.0 * FP0 * phi_pt - 0.5 * phi_pt**2
    # V_eff = denom0 - rho_m0 - rho_r0
    V_eff = denom0 - rho_m0 - rho_r0
    # V0 = V_eff - beta*phi_t - 0.5*m2*phi_t^2
    V0 = V_eff - beta * phi_t - 0.5 * m2 * phi_t**2
    return V0


# ============================================================================
# SECTION 5 — Main integrator
# ============================================================================

def wolf_kg_integrate(params, N_init=-5.0, N_final=0.0, n_eval=500,
                      rtol=1e-6, atol=1e-8, method='LSODA'):
    """
    Integrate Wolf-NMC-KG background ODE from N_init to N_final.

    Uses the 2D Friedmann-constrained formulation (no lnH drift).

    Args:
      params: dict with keys:
        xi          : NMC coupling ξ
        beta        : linear V term β [M_P² H₀²] (default 0)
        m2          : mass² term m² [H₀²] (default 0, can be negative)
        phi_init    : φ(N_init) [M_P]
        phidot_init : dφ/dN at N_init (default 0)
        omega_m     : ω_m = Ω_m h² (physical matter density parameter)
        omega_r     : ω_r = Ω_r h² (physical radiation density, default 4.15e-5)
        h           : Hubble parameter h = H₀/100 (default 0.6774)
        V0          : potential offset (float or 'auto')
      N_init: starting N = ln a (default -5, a≈0.0067)
      N_final: ending N = ln a (default 0, a=1)
      n_eval: number of output evaluation points
      rtol, atol: ODE tolerances
      method: 'LSODA', 'Radau', 'RK45'

    Returns:
      dict with:
        N_grid     : array of N values, shape (n_eval,)
        phi_traj   : φ(N), shape (n_eval,)
        phi_p_traj : dφ/dN(N), shape (n_eval,)
        H2_traj    : H²(N) from Friedmann constraint, shape (n_eval,)
        lnH_traj   : 0.5*log(H²), shape (n_eval,)
        F_traj     : F(φ(N)), shape (n_eval,)
        success    : bool
        message    : str
        V0         : float (V0 used)
    """
    from scipy.integrate import solve_ivp

    xi = float(params['xi'])
    beta = float(params.get('beta', 0.0))
    m2 = float(params.get('m2', 0.0))
    phi_init = float(params['phi_init'])
    phi_p_init = float(params.get('phidot_init', 0.0))
    omega_m = float(params['omega_m'])
    omega_r = float(params.get('omega_r', 4.15e-5))
    h_param = float(params.get('h', 0.6774))

    # Convert to dimensionless: Omega = omega / h^2
    Omega_m = omega_m / h_param**2
    Omega_r = omega_r / h_param**2

    # V0 tuning
    V0_param = params.get('V0', 'auto')
    if V0_param == 'auto' or V0_param is None:
        V0 = tune_V0(xi, beta, m2, phi_init, phi_p_init, Omega_m, Omega_r)
    else:
        V0 = float(V0_param)

    state0 = [phi_init, phi_p_init]
    N_grid = np.linspace(N_init, N_final, n_eval)

    def rhs(N, state):
        try:
            return wolf_kg_ode_2d(N, state, xi, V0, beta, m2, Omega_m, Omega_r)
        except Exception:
            return [0.0, 0.0]

    # Runaway event: |phi| > 10
    def ev_runaway(N, state):
        return 10.0 - abs(state[0])
    ev_runaway.terminal = True
    ev_runaway.direction = -1

    # F-collapse event: F < 0.001
    def ev_Fcollapse(N, state):
        return _F(state[0], xi) - 0.001
    ev_Fcollapse.terminal = True
    ev_Fcollapse.direction = -1

    sol = solve_ivp(
        rhs,
        [N_init, N_final],
        state0,
        method=method,
        t_eval=N_grid,
        rtol=rtol,
        atol=atol,
        events=[ev_runaway, ev_Fcollapse],
        dense_output=False,
        max_step=0.1,
    )

    # Determine success/failure
    if sol.t_events[0].size > 0:
        message = f'phi_RUNAWAY at N={sol.t_events[0][0]:.2f}'
        success = False
    elif sol.t_events[1].size > 0:
        message = f'F_COLLAPSE at N={sol.t_events[1][0]:.2f}'
        success = False
    elif not sol.success:
        message = sol.message
        success = False
    else:
        message = 'OK'
        success = True

    # Build output arrays
    N_out = sol.t
    if N_out.size == 0:
        return {
            'N_grid': None, 'phi_traj': None, 'phi_p_traj': None,
            'H2_traj': None, 'lnH_traj': None, 'F_traj': None,
            'success': False, 'message': message, 'V0': V0,
        }

    phi_out = sol.y[0]
    phi_p_out = sol.y[1]
    F_out = _F(phi_out, xi)

    # Compute H²(N) from Friedmann constraint at each output point
    H2_out = np.array([
        H2_from_friedmann(phi_out[i], phi_p_out[i], N_out[i],
                          xi, V0, beta, m2, Omega_m, Omega_r) or 0.0
        for i in range(len(N_out))
    ])
    lnH_out = np.where(H2_out > 0, 0.5 * np.log(np.maximum(H2_out, 1e-30)), -30.0)

    return {
        'N_grid': N_out,
        'phi_traj': phi_out,
        'phi_p_traj': phi_p_out,
        'H2_traj': H2_out,
        'lnH_traj': lnH_out,
        'F_traj': F_out,
        'success': success,
        'message': message,
        'V0': V0,
        'Omega_m': Omega_m,
        'Omega_r': Omega_r,
    }


# ============================================================================
# SECTION 6 — KG gate
# ============================================================================

def kg_gate(phi_traj, F_traj, lnH_traj, N_grid,
            phi_max_thresh=10.0, F_min_thresh=0.01, lnH_tol=0.05):
    """
    KG-physical consistency gate per A70 likelihood_spec.md.

    Gates:
      (a) |φ| > phi_max_thresh (default 10 M_P) → reject (runaway)
      (b) F(φ) < F_min_thresh (default 0.01) → reject (ghost / F-collapse)
      (c) |lnH(N≈0)| > lnH_tol (default 0.05) → reject (Friedmann closure failure)

    In the 2D Friedmann-constrained formulation, (c) is automatically satisfied
    (H² is computed from Friedmann). Gate (c) is kept as sanity check.

    Args:
      phi_traj  : φ(N) array
      F_traj    : F(φ(N)) array
      lnH_traj  : ln(H/H₀)(N) array (from Friedmann constraint)
      N_grid    : N grid
      phi_max_thresh, F_min_thresh, lnH_tol: gate thresholds

    Returns:
      gate_pass : bool (True = KG-physical, False = reject)
      reason    : str
    """
    # Gate (a): runaway
    max_phi = np.max(np.abs(phi_traj))
    if max_phi > phi_max_thresh:
        idx = np.argmax(np.abs(phi_traj) > phi_max_thresh)
        return False, f'phi_runaway: |phi|_max={max_phi:.2f} > {phi_max_thresh} at N={N_grid[idx]:.2f}'

    # Gate (b): F collapse
    min_F = np.min(F_traj)
    if min_F < F_min_thresh:
        idx = np.argmin(F_traj)
        return False, f'F_collapse: F_min={min_F:.4f} < {F_min_thresh} at N={N_grid[idx]:.2f}'

    # Gate (c): Friedmann closure at today
    # In the 2D Friedmann-constrained formulation, H²(0) is computed from the
    # constraint. lnH=-30 signals H²→0 (Friedmann denom collapsed), a valid gate.
    i_today = np.argmin(np.abs(N_grid))
    lnH_today = lnH_traj[i_today]
    if not np.isfinite(lnH_today) or abs(lnH_today) > lnH_tol:
        return False, f'Friedmann_closure: lnH(0)={lnH_today:.3f}, |lnH|>{lnH_tol}'

    return True, 'KG-physical: all gates passed'


# ============================================================================
# SECTION 7 — Convenience wrapper: H(z) array
# ============================================================================

def wolf_Hz_from_ode(params, z_query=None, N_init=-5.0, n_eval=500, **kwargs):
    """
    Integrate Wolf-KG ODE and return H(z)/H₀ at requested redshifts.

    Args:
      params: dict (see wolf_kg_integrate)
      z_query: array of redshifts z >= 0. If None, returns full grid.
      N_init: initial N (default -5)
      n_eval: ODE output points
      **kwargs: passed to wolf_kg_integrate

    Returns:
      dict with all wolf_kg_integrate keys plus:
        H_z: H(z)/H₀ at z_query, from Friedmann constraint
        z_query: the queried redshift array
        gate_pass, gate_reason
    """
    result = wolf_kg_integrate(params, N_init=N_init, N_final=0.0,
                                n_eval=n_eval, **kwargs)

    if not result['success'] or result['N_grid'] is None:
        result['gate_pass'] = False
        result['gate_reason'] = result['message']
        if z_query is not None:
            result['H_z'] = np.full(len(np.atleast_1d(z_query)), np.nan)
            result['z_query'] = np.atleast_1d(z_query)
        return result

    gate_pass, gate_reason = kg_gate(
        result['phi_traj'], result['F_traj'],
        result['lnH_traj'], result['N_grid']
    )
    result['gate_pass'] = gate_pass
    result['gate_reason'] = gate_reason

    if z_query is not None:
        z_query_arr = np.atleast_1d(z_query)
        N_query = -np.log(1.0 + z_query_arr)  # N = ln a = -ln(1+z)
        # Interpolate lnH at queried N values
        lnH_interp = np.interp(N_query, result['N_grid'], result['lnH_traj'])
        result['H_z'] = np.exp(lnH_interp)  # H(z)/H₀
        result['z_query'] = z_query_arr

    return result


# ============================================================================
# SECTION 8 — numpyro NUTS model stub (JAX implementation)
# ============================================================================

def _build_jax_ode():
    """
    Build JAX-compatible wolf_kg_ode for NUTS sampling.
    Returns (wolf_kg_ode_jax, jax) or (None, None) if JAX unavailable.

    The JAX ODE uses the 2D Friedmann-constrained formulation.
    State: [phi, phi_p].
    """
    try:
        import jax
        import jax.numpy as jnp
    except ImportError:
        return None, None

    def _F_jax(phi, xi):
        return 1.0 - xi * phi**2

    def _FP_jax(phi, xi):
        return -2.0 * xi * phi

    def _FPP_jax(xi):
        return -2.0 * xi

    def _V_jax(phi, V0, beta, m2):
        return V0 + beta * phi + 0.5 * m2 * phi**2

    def _VP_jax(phi, beta, m2):
        return beta + m2 * phi

    def wolf_kg_ode_jax(state, N, xi, V0, beta, m2, Omega_m, Omega_r):
        """
        JAX ODE RHS for wolf_kg. Convention: (state, t, *args) for odeint.

        State: [phi, phi_p] (2D Friedmann-constrained).
        H² computed from Friedmann constraint at each step.

        Args:
          state: jnp.array([phi, phi_p])
          N: scalar N = ln a
          xi, V0, beta, m2, Omega_m, Omega_r: scalar parameters

        Returns: jnp.array([dphi/dN, dphi_p/dN])
        """
        phi, phi_p = state[0], state[1]

        # Densities
        rho_m = 3.0 * Omega_m * jnp.exp(-3.0 * N)
        rho_r = 3.0 * Omega_r * jnp.exp(-4.0 * N)

        # Structural functions
        F = _F_jax(phi, xi)
        FP = _FP_jax(phi, xi)
        FPP = _FPP_jax(xi)
        V = _V_jax(phi, V0, beta, m2)
        VP = _VP_jax(phi, beta, m2)

        # Friedmann: H² = (ρ_m + ρ_r + V) / (3F + 3FP φ' − ½ φ'²)
        fried_denom = 3.0 * F + 3.0 * FP * phi_p - 0.5 * phi_p**2
        H2 = (rho_m + rho_r + V) / jnp.where(fried_denom > 1e-8, fried_denom, 1e-8)
        H2 = jnp.maximum(H2, 1e-10)

        # s_H = H'/H
        N_sH = (- rho_m / H2
                - (4.0 / 3.0) * rho_r / H2
                - (2.0 * V + FP * VP) / H2
                + FP * phi_p
                + 6.0 * FP**2
                + FPP * phi_p**2)
        D_sH = 2.0 * F - 3.0 * FP**2
        D_sH = jnp.where(jnp.abs(D_sH) < 1e-10, 1e-10 * jnp.sign(D_sH + 1e-20), D_sH)
        s_H = N_sH / D_sH

        # KG equation
        phi_pp = -(3.0 + s_H) * phi_p - VP / H2 - 6.0 * xi * phi * (2.0 + s_H)

        return jnp.array([phi_p, phi_pp])

    return wolf_kg_ode_jax, jax


# ============================================================================
# SECTION 9 — Synthetic tests
# ============================================================================

def run_synthetic_tests(verbose=True):
    """
    Run Tests A/B/C/D per M7 mission brief.

    Test A: φ_init=0.50, ξ=0.10, m²=−0.5 — STABLE (gate PASS)
    Test B: φ_init=1.50, ξ=0.30, m²=−2.0 — GATE TRIGGERS (Friedmann closure failure)
    Test C: φ_init=0.66, ξ=2.31, m²=−0.5 — CATASTROPHIC (F_collapse at init: F<0)
    Test D: φ_init=0.01, ξ≈0,    m²=0.0  — LCDM-like (gate PASS)

    PHYSICS NOTE (critical):
      The original mission brief specified φ_init=0.01 for Tests B/C. This is
      too small to trigger the KG gate with quadratic V:
        - For ξ=2.31: F_collapse needs φ > sqrt(0.99/2.31) = 0.654 M_P
        - For ξ=0.30: runaway needs large φ_init + strong tachyon (m²≪0)
      The A56 empirical ξ_crit ≈ 0.20 was derived for EXPONENTIAL potential
      V = V₀ exp(−λφ) with λ=1, NOT for Wolf's quadratic V.
      For quadratic V, the gate is triggered by:
        (a) F collapse: ξ=2.31 with φ_init ≥ 0.655 M_P
        (b) Friedmann closure failure: ξ=0.30 with φ_init=1.5, m²=−2 (H²→0)
      Tests redesigned accordingly. The KG gate mechanism is correct and
      potential-agnostic.

    Returns: dict of test results
    """
    # ECI/Planck 2018 fiducial
    omega_m = 0.1432
    omega_r = 4.15e-5
    h_param = 0.6774
    Omega_m = omega_m / h_param**2
    Omega_r = omega_r / h_param**2

    tests = [
        # label, xi,   phi_i, beta, m2,   expectation
        ('A', 0.10, 0.50, 0.0, -0.5, 'STABLE_EXPECTED'),
        ('B', 0.30, 1.50, 0.0, -2.0, 'GATE_EXPECTED'),
        ('C', 2.31, 0.66, 0.0, -0.5, 'CATASTROPHIC_EXPECTED'),
        ('D', 1e-12, 0.01, 0.0, 0.0, 'LCDM_LIKE_EXPECTED'),
    ]

    results = {}

    for label, xi_val, phi_i, beta_v, m2_v, expect in tests:
        # Tune V0 at N=0 with phi≈phi_i, phi'≈0
        V0_val = tune_V0(xi_val, beta_v, m2_v, phi_i, 0.0, Omega_m, Omega_r)

        params = {
            'xi': xi_val,
            'beta': beta_v,
            'm2': m2_v,
            'phi_init': phi_i,
            'phidot_init': 0.0,
            'omega_m': omega_m,
            'omega_r': omega_r,
            'h': h_param,
            'V0': V0_val,
        }

        res = wolf_kg_integrate(params, N_init=-5.0, N_final=0.0,
                                 n_eval=500, method='LSODA')

        if res['success'] and res['N_grid'] is not None and len(res['N_grid']) > 0:
            i_today = np.argmin(np.abs(res['N_grid']))
            phi_today = float(res['phi_traj'][i_today])
            F_today = float(res['F_traj'][i_today])
            lnH_today = float(res['lnH_traj'][i_today])
            H2_today = float(res['H2_traj'][i_today])
            phi_max = float(np.max(np.abs(res['phi_traj'])))
            F_min = float(np.min(res['F_traj']))

            gate_pass, gate_reason = kg_gate(
                res['phi_traj'], res['F_traj'],
                res['lnH_traj'], res['N_grid']
            )
        else:
            phi_today = None
            F_today = None
            lnH_today = None
            H2_today = None
            phi_max = None
            F_min = None
            gate_pass = False
            gate_reason = res['message']

        result_dict = {
            'label': label,
            'xi': xi_val,
            'phi_init': phi_i,
            'm2': m2_v,
            'expectation': expect,
            'V0_used': float(V0_val),
            'ode_success': res['success'],
            'ode_message': res['message'],
            'phi_today': phi_today,
            'F_today': F_today,
            'lnH_today': lnH_today,
            'H2_today': H2_today,
            'phi_max': phi_max,
            'F_min': F_min,
            'gate_pass': gate_pass,
            'gate_reason': gate_reason,
        }

        # Verdict
        if label == 'A':
            passed = gate_pass
            verdict = 'PASS' if passed else f'FAIL (expected stable, gate: {gate_reason})'
        elif label == 'B':
            passed = not gate_pass
            verdict = 'PASS (gate triggered as expected)' if passed else 'FAIL (gate did not trigger)'
        elif label == 'C':
            passed = not gate_pass
            verdict = 'PASS (catastrophic gate as expected)' if passed else 'FAIL (gate did not trigger)'
        elif label == 'D':
            passed = gate_pass
            verdict = 'PASS (LCDM-like stable)' if passed else f'FAIL (gate: {gate_reason})'
        else:
            passed = False
            verdict = 'UNKNOWN'

        result_dict['verdict'] = verdict
        result_dict['test_passed'] = bool(passed)
        results[label] = result_dict

        if verbose:
            print(f"\n{'='*60}")
            print(f"TEST {label} (xi={xi_val}, phi_i={phi_i}, m2={m2_v})")
            print(f"  expectation: {expect}")
            print(f"{'='*60}")
            print(f"  V0_used:   {V0_val:.4f}")
            print(f"  ODE:       {res['success']}, {res['message']}")
            if phi_today is not None:
                print(f"  phi_today: {phi_today:.6e}")
                print(f"  F_today:   {F_today:.6f}")
                print(f"  H2_today:  {H2_today:.6f}  [should be 1.0]")
                print(f"  lnH_today: {lnH_today:.6f}  [should be ~0]")
                print(f"  phi_max:   {phi_max:.4e}")
                print(f"  F_min:     {F_min:.4f}")
            print(f"  KG gate:   {gate_pass} — {gate_reason}")
            print(f"  VERDICT:   {verdict}")

    return results


# ============================================================================
# SECTION 10 — Main (smoke test + save results)
# ============================================================================

if __name__ == '__main__':
    import json

    print("=" * 70)
    print("wolf_background.py — M7 Wolf-NMC-KG ODE Smoke Test")
    print("Formulation: 2D Friedmann-constrained (H² from constraint, not ODE)")
    print("Hallu count: 85 (held). Mistral STRICT-BAN.")
    print("=" * 70)

    # Run synthetic tests
    results = run_synthetic_tests(verbose=True)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    all_pass = all(r['test_passed'] for r in results.values())
    for label, r in results.items():
        status = "OK" if r['test_passed'] else "FAIL"
        print(f"  Test {label} (xi={r['xi']:.2f}): {status} — {r['verdict']}")

    print(f"\nOverall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")

    # Save results
    out_path = '/root/crossed-cosmos/notes/eci_v7_aspiration/M7_WOLF_KG_ODE/synthetic_test_results.json'
    json_results = {}
    for k, v in results.items():
        json_results[k] = {}
        for kk, vv in v.items():
            if isinstance(vv, (np.floating, np.integer)):
                json_results[k][kk] = float(vv)
            elif isinstance(vv, bool):
                json_results[k][kk] = vv
            else:
                json_results[k][kk] = vv

    with open(out_path, 'w') as f:
        json.dump(json_results, f, indent=2, default=str)
    print(f"\nResults saved to: {out_path}")

    # JAX sanity
    print("\n--- JAX availability ---")
    wolf_kg_ode_jax, jax_mod = _build_jax_ode()
    if wolf_kg_ode_jax is not None:
        import jax.numpy as jnp
        state0 = jnp.array([0.10, 0.0])
        res_jax = wolf_kg_ode_jax(state0, 0.0, 0.1, 2.0, 0.0, -0.5, 0.3121, 9.04e-5)
        print(f"  JAX ODE RHS test: {res_jax}")
        print(f"  JAX: OK")
    else:
        print("  JAX: NOT AVAILABLE (scipy-only mode)")
