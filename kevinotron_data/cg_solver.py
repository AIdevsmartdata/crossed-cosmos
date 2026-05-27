"""
cg_solver.py -- Conjugate Gradient solver for D^dag D x = b in JAX.

Two implementations:
  1. cg_solve_python: plain Python loop (for debugging, not JIT-compatible)
  2. cg_solve: jax.lax.while_loop based (fully JIT-compatible)

Both solve the normal equations for the Wilson-Dirac operator:
    D^dag D x = b
where D^dag = gamma5 D gamma5 (gamma5-hermiticity).

Usage:
    from cg_solver import cg_solve
    x, n_iter, rel_res = cg_solve(apply_A_fn, b, tol=1e-10, max_iter=5000)
"""
import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
from functools import partial

from wilson_dirac import apply_wilson_dirac, apply_gamma5, apply_ddag_d


# ---------------------------------------------------------------------------
# Generic CG with jax.lax.while_loop (JIT-compatible)
# ---------------------------------------------------------------------------

def cg_solve(apply_A, b, tol=1e-10, max_iter=5000):
    """Conjugate Gradient solver: A x = b where A is Hermitian positive definite.

    Uses jax.lax.while_loop so the entire solve can be JIT-compiled.
    No Python-level loop, no tracing issues.

    Args:
        apply_A: callable, x -> A @ x.  Must be JIT-compatible (pure JAX).
        b: right-hand side, any pytree of arrays (typically a single array).
        tol: relative residual tolerance ||r|| / ||b|| < tol.
        max_iter: maximum iterations.

    Returns:
        x: solution (same shape as b)
        n_iter: number of iterations (int scalar)
        rel_res: final relative residual (float scalar)
    """
    b = jnp.asarray(b, dtype=jnp.complex128)
    b_flat = b.ravel()
    n = b_flat.shape[0]

    b_norm2 = jnp.sum(jnp.conj(b_flat) * b_flat).real
    tol2 = tol * tol * b_norm2  # squared absolute tolerance

    x = jnp.zeros_like(b_flat)
    r = b_flat.copy()
    p = r.copy()
    rr = b_norm2

    # Wrap apply_A to handle flat vectors
    b_shape = b.shape

    def apply_A_flat(v):
        v_shaped = v.reshape(b_shape)
        Av = apply_A(v_shaped)
        return jnp.asarray(Av, dtype=jnp.complex128).ravel()

    # State: (x, r, p, rr, iteration)
    init_state = (x, r, p, rr, jnp.int32(0))

    def cond_fn(state):
        _, _, _, rr, it = state
        return jnp.logical_and(it < max_iter, rr > tol2)

    def body_fn(state):
        x, r, p, rr, it = state

        Ap = apply_A_flat(p)
        pAp = jnp.sum(jnp.conj(p) * Ap).real

        # Guard against zero denominator
        alpha = jnp.where(pAp > 1e-30, rr / pAp, 0.0)

        x_new = x + alpha * p
        r_new = r - alpha * Ap

        rr_new = jnp.sum(jnp.conj(r_new) * r_new).real

        beta = jnp.where(rr > 1e-30, rr_new / rr, 0.0)
        p_new = r_new + beta * p

        return (x_new, r_new, p_new, rr_new, it + 1)

    final_state = jax.lax.while_loop(cond_fn, body_fn, init_state)
    x_sol, r_final, _, rr_final, n_iter = final_state

    rel_res = jnp.sqrt(rr_final / jnp.maximum(b_norm2, 1e-30))

    return x_sol.reshape(b_shape), n_iter, rel_res


# ---------------------------------------------------------------------------
# Convenience wrappers for Wilson-Dirac
# ---------------------------------------------------------------------------

def cg_solve_wilson(U, b, mass, Ls, Lt, tol=1e-10, max_iter=5000):
    """Solve D^dag D x = b for Wilson-Dirac operator.

    Args:
        U: gauge field (4, Ls, Ls, Ls, Lt, Nc, Nc)
        b: right-hand side (Ls, Ls, Ls, Lt, 4, Nc)
        mass: bare quark mass
        Ls, Lt: lattice dimensions
        tol, max_iter: CG parameters

    Returns:
        x: solution (Ls, Ls, Ls, Lt, 4, Nc)
        n_iter: iterations
        rel_res: relative residual
    """
    def apply_A(psi):
        return apply_ddag_d(U, psi, mass, Ls, Lt)

    return cg_solve(apply_A, b, tol, max_iter)


def solve_dirac_wilson(U, b, mass, Ls, Lt, tol=1e-10, max_iter=5000):
    """Solve D x = b via normal equations: D^dag D x = D^dag b.

    Args:
        U, b, mass, Ls, Lt: as above
    Returns:
        x, n_iter, rel_res
    """
    from wilson_dirac import apply_ddag
    ddag_b = apply_ddag(U, b, mass, Ls, Lt)
    return cg_solve_wilson(U, ddag_b, mass, Ls, Lt, tol, max_iter)


# ---------------------------------------------------------------------------
# Python-loop CG (for debugging, not JIT-compatible)
# ---------------------------------------------------------------------------

def cg_solve_python(apply_A, b, tol=1e-10, max_iter=5000, verbose=False):
    """CG with plain Python loop. Useful for debugging and step-by-step inspection.

    Same interface as cg_solve but NOT JIT-compilable (uses Python control flow).
    """
    b = jnp.asarray(b, dtype=jnp.complex128)
    b_flat = b.ravel()
    b_norm2 = float(jnp.sum(jnp.conj(b_flat) * b_flat).real)

    if b_norm2 < 1e-30:
        return jnp.zeros_like(b), 0, 0.0

    b_shape = b.shape

    def apply_A_flat(v):
        return jnp.asarray(apply_A(v.reshape(b_shape))).ravel()

    x = jnp.zeros_like(b_flat)
    r = b_flat.copy()
    p = r.copy()
    rr = b_norm2

    for it in range(max_iter):
        Ap = apply_A_flat(p)
        pAp = float(jnp.sum(jnp.conj(p) * Ap).real)

        if abs(pAp) < 1e-30:
            break

        alpha = rr / pAp
        x = x + alpha * p
        r = r - alpha * Ap

        rr_new = float(jnp.sum(jnp.conj(r) * r).real)
        rel_res = (rr_new / b_norm2) ** 0.5

        if verbose and (it + 1) % 100 == 0:
            print(f"  CG iter {it+1}: rel_res = {rel_res:.4e}")

        if rel_res < tol:
            return x.reshape(b_shape), it + 1, rel_res

        beta = rr_new / rr
        p = r + beta * p
        rr = rr_new

    final_res = (rr / b_norm2) ** 0.5
    return x.reshape(b_shape), max_iter, final_res


# ---------------------------------------------------------------------------
# Multishift CG (for rational approximation / RHMC)
# ---------------------------------------------------------------------------

def multishift_cg(apply_A, b, shifts, tol=1e-10, max_iter=5000):
    """Multi-shift CG: solve (A + sigma_i) x_i = b for multiple shifts sigma_i.

    All solutions share the same Krylov space.
    Useful for RHMC where one needs (D^dag D + sigma)^{-1} b for many sigma values.

    Args:
        apply_A: callable, x -> A @ x (no shift)
        b: right-hand side
        shifts: list/array of shift values sigma_i >= 0
        tol, max_iter: CG parameters

    Returns:
        solutions: list of arrays, one per shift
        n_iter: iterations used
    """
    b = jnp.asarray(b, dtype=jnp.complex128)
    b_flat = b.ravel()
    b_shape = b.shape
    n_shifts = len(shifts)
    n = b_flat.shape[0]

    b_norm2 = float(jnp.sum(jnp.conj(b_flat) * b_flat).real)
    if b_norm2 < 1e-30:
        return [jnp.zeros_like(b) for _ in shifts], 0

    def apply_A_flat(v):
        return jnp.asarray(apply_A(v.reshape(b_shape))).ravel()

    # Initialize for base system (shift=0 conceptually, smallest shift)
    x = [jnp.zeros_like(b_flat) for _ in range(n_shifts)]
    r = b_flat.copy()
    p_base = r.copy()
    p = [r.copy() for _ in range(n_shifts)]
    rr = b_norm2
    zeta = [1.0 for _ in range(n_shifts)]
    zeta_old = [1.0 for _ in range(n_shifts)]
    alpha_base = 0.0
    beta_base = 0.0

    converged = [False] * n_shifts

    for it in range(max_iter):
        Ap = apply_A_flat(p_base)
        pAp = float(jnp.sum(jnp.conj(p_base) * Ap).real)

        if abs(pAp) < 1e-30:
            break

        alpha_base_new = rr / pAp

        # Update base solution
        r_new = r - alpha_base_new * Ap
        rr_new = float(jnp.sum(jnp.conj(r_new) * r_new).real)
        beta_base_new = rr_new / max(rr, 1e-30)

        # Update shifted solutions
        for s in range(n_shifts):
            if converged[s]:
                continue
            sigma = float(shifts[s])
            # Compute shifted zeta
            denom = (1.0 + alpha_base_new * sigma) * zeta[s] + \
                    alpha_base_new * beta_base * (zeta_old[s] - zeta[s])
            if abs(denom) < 1e-30:
                converged[s] = True
                continue
            zeta_new = zeta[s] * zeta_old[s] / denom
            alpha_s = alpha_base_new * zeta_new / zeta[s]
            beta_s = beta_base_new * (zeta_new / zeta[s]) ** 2

            x[s] = x[s] + alpha_s * p[s]
            p[s] = zeta_new * r_new + beta_s * p[s]
            zeta_old[s] = zeta[s]
            zeta[s] = zeta_new

            # Check convergence
            shift_res = abs(zeta_new) * (rr_new / b_norm2) ** 0.5
            if shift_res < tol:
                converged[s] = True

        r = r_new
        p_base = r + beta_base_new * p_base
        alpha_base = alpha_base_new
        beta_base = beta_base_new
        rr = rr_new

        if all(converged):
            return [xi.reshape(b_shape) for xi in x], it + 1

    return [xi.reshape(b_shape) for xi in x], max_iter


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=" * 70)
    print("CG solver test (jax.lax.while_loop)")
    print("=" * 70)

    Ls, Lt, Nc = 4, 8, 3
    mass = 0.5

    U = jnp.broadcast_to(
        jnp.eye(Nc, dtype=jnp.complex128),
        (4, Ls, Ls, Ls, Lt, Nc, Nc)
    ).copy()

    key = jax.random.PRNGKey(42)
    b = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64) + \
        1j * jax.random.normal(jax.random.PRNGKey(43), (Ls, Ls, Ls, Lt, 4, Nc),
                               dtype=jnp.float64)

    print(f"\nTest 1: CG with jax.lax.while_loop on D^dag D (free field)")
    x, n_iter, rel_res = cg_solve_wilson(U, b, mass, Ls, Lt, tol=1e-12)
    print(f"  Iterations: {n_iter}")
    print(f"  Relative residual: {rel_res:.4e}")
    # Verify
    Ax = apply_ddag_d(U, x, mass, Ls, Lt)
    err = float(jnp.max(jnp.abs(Ax - b)) / jnp.max(jnp.abs(b)))
    print(f"  Verification |Ax - b|/|b|: {err:.4e}  {'PASS' if err < 1e-8 else 'FAIL'}")

    print(f"\nTest 2: Python-loop CG (should give same result)")
    def apply_A(psi):
        return apply_ddag_d(U, psi, mass, Ls, Lt)
    x2, n_iter2, rel_res2 = cg_solve_python(apply_A, b, tol=1e-12, verbose=True)
    diff = float(jnp.max(jnp.abs(x - x2)))
    print(f"  Difference from while_loop CG: {diff:.4e}  {'PASS' if diff < 1e-8 else 'FAIL'}")

    print(f"\nTest 3: CG convergence vs mass")
    for m in [0.01, 0.05, 0.1, 0.5, 1.0]:
        x_m, n_it, rr = cg_solve_wilson(U, b, m, Ls, Lt, tol=1e-10)
        print(f"  m={m:.2f}: {n_it:>5d} iters, rel_res={rr:.2e}")

    print("=" * 70)
