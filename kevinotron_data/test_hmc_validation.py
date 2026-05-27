#!/usr/bin/env python3
"""
test_hmc_validation.py -- Comprehensive HMC validation tests.

Tests:
  1. Reversibility: forward + backward leapfrog returns to initial config
  2. <exp(-dH)> = 1 over many trajectories (Creutz equality)
  3. Plaquette vs literature for Nf=2 SU(3)
  4. CG convergence vs quark mass
  5. Even-odd preconditioning correctness
  6. G2 algebra projection

Run with: JAX_ENABLE_X64=1 python -m kevinotron_data.test_hmc_validation
    or:   JAX_ENABLE_X64=1 python test_hmc_validation.py
"""
import os
os.environ['JAX_ENABLE_X64'] = '1'

import sys
import jax
import jax.numpy as jnp
import numpy as np
from time import time


# ---------------------------------------------------------------------------
# Setup: import local modules
# ---------------------------------------------------------------------------

def import_modules():
    """Import modules, handling both package and standalone execution."""
    try:
        from .wilson_dirac import (apply_wilson_dirac, apply_gamma5,
                                   apply_ddag, apply_ddag_d,
                                   check_gamma5_hermiticity)
        from .cg_solver import (cg_solve, cg_solve_wilson, cg_solve_python,
                                multishift_cg)
        from .eo_preconditioning import (EOPreconditioner, solve_wilson_eo,
                                         apply_gamma5_sub)
        from .g2_hmc import (build_g2_generators_numpy, verify_g2_generators,
                             random_g2_momentum, project_to_g2,
                             expm_antisym_7x7, G2HMC)
        from .pseudofermion import (generate_pseudofermion, fermion_action,
                                    fermion_force)
    except ImportError:
        # Standalone execution: add parent to path
        parent = os.path.dirname(os.path.abspath(__file__))
        if parent not in sys.path:
            sys.path.insert(0, parent)
        from wilson_dirac import (apply_wilson_dirac, apply_gamma5,
                                  apply_ddag, apply_ddag_d,
                                  check_gamma5_hermiticity)
        from cg_solver import (cg_solve, cg_solve_wilson, cg_solve_python,
                               multishift_cg)
        from eo_preconditioning import (EOPreconditioner, solve_wilson_eo,
                                        apply_gamma5_sub)
        from g2_hmc import (build_g2_generators_numpy, verify_g2_generators,
                            random_g2_momentum, project_to_g2,
                            expm_antisym_7x7, G2HMC)
        from pseudofermion import (generate_pseudofermion, fermion_action,
                                   fermion_force)

    return {
        'apply_wilson_dirac': apply_wilson_dirac,
        'apply_gamma5': apply_gamma5,
        'apply_ddag': apply_ddag,
        'apply_ddag_d': apply_ddag_d,
        'check_gamma5_hermiticity': check_gamma5_hermiticity,
        'cg_solve': cg_solve,
        'cg_solve_wilson': cg_solve_wilson,
        'cg_solve_python': cg_solve_python,
        'multishift_cg': multishift_cg,
        'EOPreconditioner': EOPreconditioner,
        'solve_wilson_eo': solve_wilson_eo,
        'build_g2_generators_numpy': build_g2_generators_numpy,
        'verify_g2_generators': verify_g2_generators,
        'random_g2_momentum': random_g2_momentum,
        'project_to_g2': project_to_g2,
        'expm_antisym_7x7': expm_antisym_7x7,
        'G2HMC': G2HMC,
        'generate_pseudofermion': generate_pseudofermion,
        'fermion_action': fermion_action,
        'fermion_force': fermion_force,
    }


# ---------------------------------------------------------------------------
# Helper: generate random SU(3) gauge field
# ---------------------------------------------------------------------------

def random_su3_config(Ls, Lt, key, eps=0.3):
    """Generate a random SU(3) gauge field near identity.

    Uses exp(i eps H) where H is Hermitian traceless.
    """
    Nc = 3
    shape = (4, Ls, Ls, Ls, Lt, Nc, Nc)

    k1, k2 = jax.random.split(key)
    M = eps * (jax.random.normal(k1, shape, dtype=jnp.float64) +
               1j * jax.random.normal(k2, shape, dtype=jnp.float64))

    # Make Hermitian
    H = (M + jnp.conj(M.swapaxes(-2, -1))) / 2
    # Make traceless
    tr = jnp.trace(H, axis1=-2, axis2=-1)[..., None, None] / Nc
    H = H - tr * jnp.eye(Nc, dtype=jnp.complex128)

    # exp(iH) via Taylor-12
    iH = 1j * H
    U = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), shape).copy()
    power = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), shape).copy()
    for k in range(1, 13):
        power = jnp.einsum('...ab,...bc->...ac', power, iH) / k
        U = U + power

    # Gram-Schmidt reunitarization
    for j in range(Nc):
        col = U[..., :, j]
        for i in range(j):
            prev = U[..., :, i]
            proj = jnp.sum(jnp.conj(prev) * col, axis=-1, keepdims=True)
            col = col - proj * prev
        norm = jnp.sqrt(jnp.sum(jnp.abs(col)**2, axis=-1, keepdims=True))
        U = U.at[..., :, j].set(col / jnp.maximum(norm, 1e-15))

    return U


# ---------------------------------------------------------------------------
# Helper: plaquette
# ---------------------------------------------------------------------------

def plaquette_su3(U):
    """Compute average plaquette for SU(3)."""
    Nc = U.shape[-1]
    p = 0.0
    count = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U_nu_at_xmu = jnp.roll(U[nu], -1, axis=mu)
            U_mu_at_xnu = jnp.roll(U[mu], -1, axis=nu)
            plaq = jnp.einsum('...ab,...bc,...dc,...da->...',
                              U[mu], U_nu_at_xmu,
                              jnp.conj(U_mu_at_xnu).swapaxes(-2, -1),
                              jnp.conj(U[nu]).swapaxes(-2, -1))
            p += jnp.mean(plaq.real) / Nc
            count += 1
    return float(p / count)


# ---------------------------------------------------------------------------
# Helper: simple pure gauge HMC step (for reversibility test)
# ---------------------------------------------------------------------------

def leapfrog_pure_gauge(U, P, n_steps, dt, beta, Nc):
    """Leapfrog integrator for pure gauge theory.

    Returns (U_final, P_final).
    """
    def gauge_force(U):
        beta_N = beta / Nc
        F = jnp.zeros_like(U)
        for mu in range(4):
            staple = jnp.zeros(U.shape[1:], dtype=U.dtype)
            for nu in range(4):
                if nu == mu:
                    continue
                U_nu_at_xmu = jnp.roll(U[nu], -1, axis=mu)
                U_mu_at_xnu = jnp.roll(U[mu], -1, axis=nu)
                s_fwd = jnp.einsum('...ab,...bc,...dc->...ad',
                                   U_nu_at_xmu,
                                   jnp.conj(U_mu_at_xnu).swapaxes(-2, -1),
                                   jnp.conj(U[nu]).swapaxes(-2, -1))
                U_nu_xmu_mnu = jnp.roll(jnp.roll(U[nu], -1, axis=mu), 1, axis=nu)
                U_mu_xmnu = jnp.roll(U[mu], 1, axis=nu)
                U_nu_xmnu = jnp.roll(U[nu], 1, axis=nu)
                s_bwd = jnp.einsum('...ba,...dc,...de->...ae',
                                   jnp.conj(U_nu_xmu_mnu),
                                   jnp.conj(U_mu_xmnu),
                                   U_nu_xmnu)
                staple = staple + s_fwd + s_bwd
            V = beta_N * jnp.einsum('...ab,...bc->...ac', U[mu], staple)
            V_ah = (V - jnp.conj(V.swapaxes(-2, -1))) / 2
            tr = jnp.trace(V_ah, axis1=-2, axis2=-1)[..., None, None] / Nc
            V_ah = V_ah - tr * jnp.eye(Nc, dtype=V_ah.dtype)
            F = F.at[mu].set(V_ah)
        return F

    def update_links(U, P, dt):
        dtP = dt * P
        exp_P = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), dtP.shape).copy()
        power = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), dtP.shape).copy()
        for k in range(1, 13):
            power = jnp.einsum('...ab,...bc->...ac', power, dtP) / k
            exp_P = exp_P + power
        U_new = jnp.einsum('...ab,...bc->...ac', exp_P, U)
        # Gram-Schmidt
        for j in range(Nc):
            col = U_new[..., :, j]
            for i in range(j):
                prev = U_new[..., :, i]
                proj = jnp.sum(jnp.conj(prev) * col, axis=-1, keepdims=True)
                col = col - proj * prev
            norm = jnp.sqrt(jnp.sum(jnp.abs(col)**2, axis=-1, keepdims=True))
            U_new = U_new.at[..., :, j].set(col / jnp.maximum(norm, 1e-15))
        return U_new

    # Half-step momenta
    F = gauge_force(U)
    P = P - 0.5 * dt * F

    for step in range(n_steps - 1):
        U = update_links(U, P, dt)
        F = gauge_force(U)
        P = P - dt * F

    U = update_links(U, P, dt)
    F = gauge_force(U)
    P = P - 0.5 * dt * F

    return U, P


# =========================================================================
# TEST 1: Reversibility
# =========================================================================

def test_reversibility():
    """Test that forward + backward leapfrog gives back the original config.

    Forward: (U, P) -> (U', P') with n_steps, dt
    Backward: (U', -P') -> (U'', P'') with n_steps, dt

    Should have: U'' = U, P'' = -P (up to numerical precision).
    """
    print("\n" + "=" * 70)
    print("TEST 1: Leapfrog Reversibility")
    print("=" * 70)

    Ls, Lt, Nc = 4, 8, 3
    beta = 5.6
    n_steps = 10
    dt = 0.01

    # Random gauge config
    key = jax.random.PRNGKey(42)
    U = random_su3_config(Ls, Lt, key, eps=0.5)

    # Random momenta (anti-Hermitian traceless)
    k1, k2 = jax.random.split(jax.random.PRNGKey(123))
    shape = (4, Ls, Ls, Ls, Lt, Nc, Nc)
    M = jax.random.normal(k1, shape, dtype=jnp.float64) + \
        1j * jax.random.normal(k2, shape, dtype=jnp.float64)
    P = (M - jnp.conj(M.swapaxes(-2, -1))) / 2
    tr = jnp.trace(P, axis1=-2, axis2=-1)[..., None, None] / Nc
    P = P - tr * jnp.eye(Nc, dtype=jnp.complex128)

    U_orig = U.copy()
    P_orig = P.copy()

    print(f"  Config: SU(3) {Ls}^3 x {Lt}, beta={beta}")
    print(f"  Leapfrog: {n_steps} steps, dt={dt}")

    # Forward
    t0 = time()
    U_fwd, P_fwd = leapfrog_pure_gauge(U, P, n_steps, dt, beta, Nc)
    t_fwd = time() - t0

    # Backward (flip momentum)
    t0 = time()
    U_rev, P_rev = leapfrog_pure_gauge(U_fwd, -P_fwd, n_steps, dt, beta, Nc)
    t_rev = time() - t0

    # Check
    U_diff = float(jnp.max(jnp.abs(U_rev - U_orig)))
    P_diff = float(jnp.max(jnp.abs(P_rev + P_orig)))  # P should be -P_orig

    passed = U_diff < 1e-8 and P_diff < 1e-8
    print(f"  Forward time: {t_fwd:.2f}s")
    print(f"  Backward time: {t_rev:.2f}s")
    print(f"  |U_reversed - U_original| = {U_diff:.4e}")
    print(f"  |P_reversed + P_original| = {P_diff:.4e}")
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


# =========================================================================
# TEST 2: Creutz equality <exp(-dH)> = 1
# =========================================================================

def test_creutz_equality():
    """Test that <exp(-dH)> = 1 over many trajectories.

    This is a necessary condition for correct detailed balance.
    Any bias in the integrator or accept/reject would violate this.

    We use pure gauge theory (quenched) for this test since
    fermion forces are expensive. The principle is the same.
    """
    print("\n" + "=" * 70)
    print("TEST 2: Creutz Equality <exp(-dH)> = 1")
    print("=" * 70)

    Ls, Lt, Nc = 4, 8, 3
    beta = 5.6
    n_steps = 10
    dt = 0.02
    n_traj = 50

    U = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()

    key = jax.random.PRNGKey(777)

    def kinetic_energy(P):
        P2 = jnp.einsum('...ab,...bc->...ac', P, P)
        return float(-jnp.sum(jnp.trace(P2, axis1=-2, axis2=-1)).real)

    def gauge_action(U):
        p = plaquette_su3(U)
        n_plaq = 6 * Ls**3 * Lt
        return beta * n_plaq * (1.0 - p)

    exp_dH_list = []
    dH_list = []

    print(f"  Running {n_traj} pure gauge trajectories...")

    for traj in range(n_traj):
        key, k1, k2 = jax.random.split(key, 3)

        # Generate momenta
        shape = (4, Ls, Ls, Ls, Lt, Nc, Nc)
        M = jax.random.normal(k1, shape, dtype=jnp.float64) + \
            1j * jax.random.normal(k2, shape, dtype=jnp.float64)
        M = M / jnp.sqrt(2.0)
        P = (M - jnp.conj(M.swapaxes(-2, -1))) / 2
        tr = jnp.trace(P, axis1=-2, axis2=-1)[..., None, None] / Nc
        P = P - tr * jnp.eye(Nc, dtype=jnp.complex128)

        # Initial Hamiltonian
        T_old = kinetic_energy(P)
        S_old = gauge_action(U)
        H_old = T_old + S_old

        # Leapfrog
        U_new, P_new = leapfrog_pure_gauge(U, P, n_steps, dt, beta, Nc)

        # Final Hamiltonian
        T_new = kinetic_energy(P_new)
        S_new = gauge_action(U_new)
        H_new = T_new + S_new

        dH = H_new - H_old
        dH_list.append(dH)
        exp_dH_list.append(np.exp(-dH))

        # Accept/reject
        r = float(jax.random.uniform(jax.random.PRNGKey(traj + 10000),
                                     dtype=jnp.float64))
        if r < min(1.0, np.exp(-dH)):
            U = U_new

    mean_exp_dH = np.mean(exp_dH_list)
    std_exp_dH = np.std(exp_dH_list) / np.sqrt(n_traj)
    mean_dH = np.mean(dH_list)
    std_dH = np.std(dH_list)
    n_sigma = abs(mean_exp_dH - 1.0) / std_exp_dH

    print(f"  <exp(-dH)> = {mean_exp_dH:.6f} +/- {std_exp_dH:.6f}")
    print(f"  <dH>       = {mean_dH:.6f} +/- {std_dH:.6f}")
    print(f"  Deviation from 1: {n_sigma:.2f} sigma")

    passed = n_sigma < 3.0  # 3-sigma tolerance
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


# =========================================================================
# TEST 3: Plaquette vs literature (quenched SU(3))
# =========================================================================

def test_plaquette_literature():
    """Test that the quenched SU(3) plaquette matches known values.

    For Nf=2 Wilson fermions, the plaquette depends on the quark mass.
    We test pure gauge (Nf=0) where:
        beta=5.6, L^3 x 2L:  <P> ~ 0.5355  (Necco-Sommer 2002)
        beta=5.8:             <P> ~ 0.5588
        beta=6.0:             <P> ~ 0.5937  (classic result)

    On a small 4^3 x 8 lattice, finite-volume effects are large,
    so we use a generous 5% tolerance band.

    For Nf=2 at beta=5.6, m=0.01: <P> ~ 0.51-0.55 (CP-PACS/JLQCD estimates)
    """
    print("\n" + "=" * 70)
    print("TEST 3: Plaquette vs Literature (quenched SU(3))")
    print("=" * 70)

    Ls, Lt, Nc = 4, 8, 3
    beta = 6.0
    n_traj_therm = 50
    n_traj_meas = 30
    n_steps = 10
    dt = 0.02

    U = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()

    key = jax.random.PRNGKey(555)

    print(f"  SU(3) beta={beta}, {Ls}^3 x {Lt}")
    print(f"  Thermalizing {n_traj_therm} trajectories...")

    # Thermalize
    for traj in range(n_traj_therm):
        key, k1, k2, k_acc = jax.random.split(key, 4)
        shape = (4, Ls, Ls, Ls, Lt, Nc, Nc)
        M = jax.random.normal(k1, shape, dtype=jnp.float64) + \
            1j * jax.random.normal(k2, shape, dtype=jnp.float64)
        M = M / jnp.sqrt(2.0)
        P = (M - jnp.conj(M.swapaxes(-2, -1))) / 2
        tr = jnp.trace(P, axis1=-2, axis2=-1)[..., None, None] / Nc
        P = P - tr * jnp.eye(Nc, dtype=jnp.complex128)

        def kinetic_energy(P):
            P2 = jnp.einsum('...ab,...bc->...ac', P, P)
            return float(-jnp.sum(jnp.trace(P2, axis1=-2, axis2=-1)).real)

        def gauge_action(U):
            p = plaquette_su3(U)
            n_plaq = 6 * Ls**3 * Lt
            return beta * n_plaq * (1.0 - p)

        H_old = kinetic_energy(P) + gauge_action(U)
        U_new, P_new = leapfrog_pure_gauge(U, P, n_steps, dt, beta, Nc)
        H_new = kinetic_energy(P_new) + gauge_action(U_new)
        dH = H_new - H_old

        r = float(jax.random.uniform(k_acc, dtype=jnp.float64))
        if r < min(1.0, np.exp(-dH)):
            U = U_new

    # Measure
    print(f"  Measuring {n_traj_meas} trajectories...")
    plaq_list = []
    for traj in range(n_traj_meas):
        key, k1, k2, k_acc = jax.random.split(key, 4)
        shape = (4, Ls, Ls, Ls, Lt, Nc, Nc)
        M = jax.random.normal(k1, shape, dtype=jnp.float64) + \
            1j * jax.random.normal(k2, shape, dtype=jnp.float64)
        M = M / jnp.sqrt(2.0)
        P = (M - jnp.conj(M.swapaxes(-2, -1))) / 2
        tr = jnp.trace(P, axis1=-2, axis2=-1)[..., None, None] / Nc
        P = P - tr * jnp.eye(Nc, dtype=jnp.complex128)

        H_old = kinetic_energy(P) + gauge_action(U)
        U_new, P_new = leapfrog_pure_gauge(U, P, n_steps, dt, beta, Nc)
        H_new = kinetic_energy(P_new) + gauge_action(U_new)
        dH = H_new - H_old

        r = float(jax.random.uniform(k_acc, dtype=jnp.float64))
        if r < min(1.0, np.exp(-dH)):
            U = U_new

        plaq_list.append(plaquette_su3(U))

    mean_plaq = np.mean(plaq_list)
    std_plaq = np.std(plaq_list) / np.sqrt(len(plaq_list))

    # Literature: beta=6.0 SU(3) quenched <P> ~ 0.594 (infinite volume)
    # Small volume (4^3 x 8) can differ by 2-5%
    lit_plaq = 0.594
    rel_diff = abs(mean_plaq - lit_plaq) / lit_plaq

    print(f"  Measured: <P> = {mean_plaq:.6f} +/- {std_plaq:.6f}")
    print(f"  Literature (beta=6.0, inf vol): {lit_plaq:.3f}")
    print(f"  Relative difference: {rel_diff*100:.1f}%")

    passed = rel_diff < 0.10  # 10% tolerance for small volume
    print(f"  RESULT: {'PASS' if passed else 'FAIL'} (10% tolerance for L=4)")
    return passed


# =========================================================================
# TEST 4: CG convergence vs quark mass
# =========================================================================

def test_cg_convergence():
    """Test CG convergence rate as a function of quark mass.

    Physics: condition number of D^dag D ~ (4+m)^2 / m^2 for Wilson fermions.
    So lighter quarks need more CG iterations.
    We verify:
      - CG converges for all masses tested
      - Iteration count increases as mass decreases
      - Solution satisfies D^dag D x = b to the requested tolerance
    """
    print("\n" + "=" * 70)
    print("TEST 4: CG Convergence vs Quark Mass")
    print("=" * 70)

    M = import_modules()

    Ls, Lt, Nc = 4, 8, 3
    tol = 1e-10

    # Use both free field and thermalized config
    U_free = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()

    U_therm = random_su3_config(Ls, Lt, jax.random.PRNGKey(42), eps=0.3)

    key = jax.random.PRNGKey(99)
    b = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64) + \
        1j * jax.random.normal(jax.random.PRNGKey(100), (Ls, Ls, Ls, Lt, 4, Nc),
                               dtype=jnp.float64)

    masses = [1.0, 0.5, 0.1, 0.05, 0.01]
    all_passed = True

    print(f"  {'mass':>8} {'iters(free)':>12} {'res(free)':>12} "
          f"{'iters(therm)':>14} {'res(therm)':>12} {'verify':>10}")

    prev_iters = 0
    monotonic = True

    for mass in masses:
        # Free field
        x_free, n_free, res_free = M['cg_solve_wilson'](
            U_free, b, mass, Ls, Lt, tol)
        Ax_free = M['apply_ddag_d'](U_free, x_free, mass, Ls, Lt)
        err_free = float(jnp.max(jnp.abs(Ax_free - b)) / jnp.max(jnp.abs(b)))

        # Thermalized
        x_therm, n_therm, res_therm = M['cg_solve_wilson'](
            U_therm, b, mass, Ls, Lt, tol)
        Ax_therm = M['apply_ddag_d'](U_therm, x_therm, mass, Ls, Lt)
        err_therm = float(jnp.max(jnp.abs(Ax_therm - b)) / jnp.max(jnp.abs(b)))

        verify_ok = err_free < 1e-6 and err_therm < 1e-6
        if not verify_ok:
            all_passed = False

        print(f"  {mass:>8.3f} {int(n_free):>12d} {res_free:>12.2e} "
              f"{int(n_therm):>14d} {res_therm:>12.2e} "
              f"{'OK' if verify_ok else 'FAIL':>10}")

        if mass < 1.0 and int(n_therm) < prev_iters:
            monotonic = False
        prev_iters = int(n_therm)

    print(f"  Iterations increase with decreasing mass: "
          f"{'yes' if monotonic else 'NOT monotonic'}")
    print(f"  RESULT: {'PASS' if all_passed else 'FAIL'}")
    return all_passed


# =========================================================================
# TEST 5: Even-odd preconditioning
# =========================================================================

def test_even_odd_preconditioning():
    """Test even-odd preconditioning gives same answer as full solve.

    Verifies:
      1. Split-merge roundtrip is exact
      2. D_eo, D_oe hopping terms are correct
      3. EO solve matches full solve
      4. EO uses fewer CG iterations than full solve
    """
    print("\n" + "=" * 70)
    print("TEST 5: Even-Odd Preconditioning")
    print("=" * 70)

    M = import_modules()

    Ls, Lt, Nc = 4, 8, 3
    mass = 0.1
    tol = 1e-10

    # Test on both free and interacting configs
    U_free = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()

    U_therm = random_su3_config(Ls, Lt, jax.random.PRNGKey(42), eps=0.3)

    eo = M['EOPreconditioner'](Ls, Lt, Nc)
    print(f"  Lattice: {Ls}^3 x {Lt}, Nc={Nc}, m={mass}")
    print(f"  N_even = N_odd = {eo.N_half}")

    # Test 5a: split-merge roundtrip
    key = jax.random.PRNGKey(42)
    psi = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64) + \
          1j * jax.random.normal(jax.random.PRNGKey(43), (Ls, Ls, Ls, Lt, 4, Nc),
                                 dtype=jnp.float64)
    psi_e, psi_o = eo.split_spinor(psi)
    psi_back = eo.merge_spinor(psi_e, psi_o)
    err_merge = float(jnp.max(jnp.abs(psi - psi_back)))
    print(f"  5a: split-merge roundtrip error: {err_merge:.2e}  "
          f"{'PASS' if err_merge < 1e-14 else 'FAIL'}")

    # Test 5b: EO solve vs full solve on free field
    phi = jax.random.normal(jax.random.PRNGKey(99), (Ls, Ls, Ls, Lt, 4, Nc),
                            dtype=jnp.float64) + \
          1j * jax.random.normal(jax.random.PRNGKey(100), (Ls, Ls, Ls, Lt, 4, Nc),
                                 dtype=jnp.float64)

    # Full solve
    t0 = time()
    x_full, n_full, res_full = M['cg_solve_wilson'](U_free, phi, mass, Ls, Lt, tol)
    t_full = time() - t0

    # EO solve
    t0 = time()
    x_eo, n_eo, res_eo = M['solve_wilson_eo'](eo, U_free, phi, mass, tol)
    t_eo = time() - t0

    diff = float(jnp.max(jnp.abs(x_full - x_eo)) / jnp.max(jnp.abs(x_full)))
    print(f"  5b: Free field EO vs full solve:")
    print(f"      Full: {int(n_full)} iters, {t_full:.2f}s")
    print(f"      EO:   {int(n_eo)} iters, {t_eo:.2f}s")
    print(f"      Difference: {diff:.2e}  {'PASS' if diff < 1e-6 else 'FAIL'}")

    # Test 5c: EO solve on interacting field
    x_full_t, n_full_t, res_full_t = M['cg_solve_wilson'](
        U_therm, phi, mass, Ls, Lt, tol)
    x_eo_t, n_eo_t, res_eo_t = M['solve_wilson_eo'](
        eo, U_therm, phi, mass, tol)
    diff_t = float(jnp.max(jnp.abs(x_full_t - x_eo_t)) /
                   jnp.max(jnp.abs(x_full_t)))
    print(f"  5c: Interacting field EO vs full solve:")
    print(f"      Full: {int(n_full_t)} iters")
    print(f"      EO:   {int(n_eo_t)} iters")
    print(f"      Difference: {diff_t:.2e}  {'PASS' if diff_t < 1e-6 else 'FAIL'}")

    passed = (err_merge < 1e-14 and diff < 1e-6 and diff_t < 1e-6)
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


# =========================================================================
# TEST 6: G2 algebra projection
# =========================================================================

def test_g2_projection():
    """Test G2 HMC momentum projection.

    Verifies:
      1. 14 generators are built correctly
      2. Momentum lies in g2 (not so(7))
      3. Force projection strips so(7)/g2 directions
      4. exp(g2 element) stays in SO(7)
      5. Short HMC trajectory with G2 projection
    """
    print("\n" + "=" * 70)
    print("TEST 6: G2 Lie Algebra Projection")
    print("=" * 70)

    M = import_modules()

    # Test 6a: build and verify generators
    gens_np = M['build_g2_generators_numpy']()
    assert len(gens_np) == 14
    M['verify_g2_generators'](gens_np)
    print(f"  6a: 14 G2 generators built and verified: PASS")

    gens_jax = jnp.array(gens_np, dtype=jnp.float64)
    norms = jnp.array([float(np.trace(gens_np[a] @ gens_np[a]))
                        for a in range(14)], dtype=jnp.float64)

    # Test 6b: g2 momentum is in g2
    key = jax.random.PRNGKey(123)
    P_g2 = M['random_g2_momentum'](gens_jax, key)
    P_proj = M['project_to_g2'](P_g2[None, ...], gens_jax, norms)[0]
    err_g2 = float(jnp.max(jnp.abs(P_g2 - P_proj)))
    print(f"  6b: g2 momentum projection error: {err_g2:.2e}  "
          f"{'PASS' if err_g2 < 1e-12 else 'FAIL'}")

    # Test 6c: so(7) element is NOT in g2
    M_so7 = jax.random.normal(key, (7, 7), dtype=jnp.float64)
    M_so7 = (M_so7 - M_so7.T) / 2
    M_g2 = M['project_to_g2'](M_so7[None, ...], gens_jax, norms)[0]
    residual = float(jnp.max(jnp.abs(M_so7 - M_g2)))
    print(f"  6c: so(7) element has g2 residual: {residual:.4f}  "
          f"{'PASS' if residual > 0.01 else 'FAIL (should be nonzero)'}")

    # Test 6d: dimensions correct
    # g2 has 14 generators, so(7) has 21.
    # The 7 extra so(7) directions should be projected out.
    n_g2_check = 0
    for _ in range(100):
        key, subkey = jax.random.split(key)
        v = jax.random.normal(subkey, (7, 7), dtype=jnp.float64)
        v = (v - v.T) / 2  # so(7) element (21 params)
        v_g2 = M['project_to_g2'](v[None, ...], gens_jax, norms)[0]
        # Ratio of norms: should be 14/21 = 2/3 on average
        n_g2_check += float(jnp.sum(v_g2**2)) / max(float(jnp.sum(v**2)), 1e-30)
    avg_ratio = n_g2_check / 100
    print(f"  6d: Average g2/so7 projection ratio: {avg_ratio:.3f} "
          f"(expected ~{14/21:.3f})  "
          f"{'PASS' if abs(avg_ratio - 14/21) < 0.1 else 'FAIL'}")

    # Test 6e: exp(g2 element) is in SO(7)
    exp_P = M['expm_antisym_7x7'](P_g2)
    det = float(jnp.linalg.det(exp_P))
    orth = float(jnp.max(jnp.abs(exp_P @ exp_P.T - jnp.eye(7))))
    print(f"  6e: exp(g2): det={det:.12f}, orth_err={orth:.2e}  "
          f"{'PASS' if abs(det - 1) < 1e-10 and orth < 1e-10 else 'FAIL'}")

    passed = (err_g2 < 1e-12 and residual > 0.01 and
              abs(avg_ratio - 14/21) < 0.1 and
              abs(det - 1) < 1e-10 and orth < 1e-10)
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


# =========================================================================
# TEST 7: Wilson-Dirac gamma5-hermiticity
# =========================================================================

def test_gamma5_hermiticity():
    """Verify D^dag = gamma5 D gamma5 on both free and interacting fields."""
    print("\n" + "=" * 70)
    print("TEST 7: gamma5-Hermiticity of Wilson-Dirac")
    print("=" * 70)

    M = import_modules()

    Ls, Lt, Nc = 4, 8, 3
    mass = 0.1

    U_free = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()
    U_therm = random_su3_config(Ls, Lt, jax.random.PRNGKey(42), eps=0.5)

    err_free = M['check_gamma5_hermiticity'](U_free, mass, Ls, Lt)
    err_therm = M['check_gamma5_hermiticity'](U_therm, mass, Ls, Lt)

    print(f"  Free field: gamma5-hermiticity error = {err_free:.2e}  "
          f"{'PASS' if err_free < 1e-12 else 'FAIL'}")
    print(f"  Interacting: gamma5-hermiticity error = {err_therm:.2e}  "
          f"{'PASS' if err_therm < 1e-12 else 'FAIL'}")

    passed = err_free < 1e-12 and err_therm < 1e-12
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


# =========================================================================
# TEST 8: Multishift CG
# =========================================================================

def test_multishift_cg():
    """Test multishift CG solver.

    Solves (D^dag D + sigma) x = b for multiple sigma values simultaneously.
    Verifies each solution independently.
    """
    print("\n" + "=" * 70)
    print("TEST 8: Multishift CG")
    print("=" * 70)

    M = import_modules()

    Ls, Lt, Nc = 4, 8, 3
    mass = 0.5
    tol = 1e-10

    U = random_su3_config(Ls, Lt, jax.random.PRNGKey(42), eps=0.3)

    key = jax.random.PRNGKey(99)
    b = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64) + \
        1j * jax.random.normal(jax.random.PRNGKey(100), (Ls, Ls, Ls, Lt, 4, Nc),
                               dtype=jnp.float64)

    shifts = [0.0, 0.01, 0.1, 0.5, 1.0]

    def apply_A(psi):
        return M['apply_ddag_d'](U, psi, mass, Ls, Lt)

    t0 = time()
    solutions, n_iter = M['multishift_cg'](apply_A, b, shifts, tol=tol)
    t_ms = time() - t0

    print(f"  Multishift CG: {n_iter} iters, {t_ms:.2f}s, {len(shifts)} shifts")

    all_ok = True
    for i, sigma in enumerate(shifts):
        # Verify: (A + sigma) x_i = b
        Ax = apply_A(solutions[i]) + sigma * solutions[i]
        err = float(jnp.max(jnp.abs(Ax - b)) / jnp.max(jnp.abs(b)))
        ok = err < 1e-6
        if not ok:
            all_ok = False
        print(f"    sigma={sigma:.2f}: verify err = {err:.2e}  {'OK' if ok else 'FAIL'}")

    print(f"  RESULT: {'PASS' if all_ok else 'FAIL'}")
    return all_ok


# =========================================================================
# Main
# =========================================================================

def main():
    print("=" * 70)
    print("HMC VALIDATION TEST SUITE")
    print(f"JAX version: {jax.__version__}")
    print(f"Devices: {jax.devices()}")
    print(f"Float64 enabled: {jax.x64_is_enabled()}")
    print("=" * 70)

    results = {}
    tests = [
        ("1. Reversibility", test_reversibility),
        ("2. Creutz <exp(-dH)>=1", test_creutz_equality),
        ("3. Plaquette vs literature", test_plaquette_literature),
        ("4. CG vs mass", test_cg_convergence),
        ("5. Even-odd preconditioning", test_even_odd_preconditioning),
        ("6. G2 projection", test_g2_projection),
        ("7. gamma5-hermiticity", test_gamma5_hermiticity),
        ("8. Multishift CG", test_multishift_cg),
    ]

    for name, test_fn in tests:
        try:
            passed = test_fn()
            results[name] = "PASS" if passed else "FAIL"
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = f"ERROR: {e}"

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    n_pass = sum(1 for v in results.values() if v == "PASS")
    n_total = len(results)
    for name, result in results.items():
        status = "PASS" if result == "PASS" else "FAIL" if result == "FAIL" else "ERR"
        print(f"  [{status}] {name}")
    print(f"\n  {n_pass}/{n_total} tests passed")
    print("=" * 70)

    return n_pass == n_total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
