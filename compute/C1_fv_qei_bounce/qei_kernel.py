"""Fewster-Verch QEI bound + bounce energy density on FRW past-light-cone diamonds.

Closed forms used:
- Hollands-Wald 2001 (CMP 223:289) — Hadamard parametrix subtraction.
- Fewster-Verch 2003 (CMP 240:329) — QEI lower bound -C / τ^4 in massless conformal scalar limit.
- ECI K_FRW lemma 3.3 — modular Hamiltonian on past-light-cone diamond.

The kernel computes, on a smearing-time grid τ ∈ [τ_min, τ_max]:
    E_smeared(τ) = ∫ ⟨T_00⟩_a(t) f_τ(t) dt,
    bound(τ) = - C_FV / τ^4
and reports the violation curve E_smeared(τ) - bound(τ).
"""
from __future__ import annotations
import jax
import jax.numpy as jnp
from jax import jit, vmap

# Fewster-Verch constant for massless conformally-coupled scalar (Eq. 4.7 of 2003 paper).
# C_FV = 1 / (16 π^2) for the standard normalisation.
C_FV = 1.0 / (16.0 * jnp.pi**2)


def gaussian_smearing(t: jnp.ndarray, tau: float) -> jnp.ndarray:
    """f_τ(t) = (1 / (τ √π)) exp(-t² / τ²) — peaked Gaussian, width τ."""
    return jnp.exp(-(t / tau) ** 2) / (tau * jnp.sqrt(jnp.pi))


@jit
def t00_renormalised(a_fn, t: jnp.ndarray, eps: float = 1e-3) -> jnp.ndarray:
    """Renormalised energy density ⟨T_00⟩ on FRW background a(t).

    Hollands-Wald Hadamard subtraction at leading order:
        ⟨T_00⟩_ren ≈ (1/120 π²) ((a''/a) - 2 (a'/a)²) + O(curvature²).
    Computed via finite differences for portability with arbitrary a_fn.
    """
    a_p = (a_fn(t + eps) - a_fn(t - eps)) / (2 * eps)
    a_pp = (a_fn(t + eps) - 2 * a_fn(t) + a_fn(t - eps)) / eps**2
    a_t = a_fn(t)
    return (1.0 / (120.0 * jnp.pi**2)) * (a_pp / a_t - 2.0 * (a_p / a_t) ** 2)


def smeared_energy(a_fn, tau: float, n_quad: int = 4096) -> jnp.ndarray:
    """E(τ) = ∫ ⟨T_00⟩_a(t) f_τ(t) dt — Gauss-Hermite-like quadrature."""
    t_grid = jnp.linspace(-6 * tau, 6 * tau, n_quad)
    weight = gaussian_smearing(t_grid, tau)
    integrand = t00_renormalised(a_fn, t_grid) * weight
    dt = t_grid[1] - t_grid[0]
    return jnp.sum(integrand) * dt


def fv_bound(tau: float) -> jnp.ndarray:
    """Fewster-Verch lower bound (massless conformal scalar)."""
    return -C_FV / tau**4


def violation_scan(a_fn, tau_grid: jnp.ndarray) -> dict:
    """Scan E_smeared(τ) and FV bound across τ_grid; report violations."""
    E = vmap(lambda t: smeared_energy(a_fn, t))(tau_grid)
    B = vmap(fv_bound)(tau_grid)
    return {
        "tau": tau_grid,
        "E_smeared": E,
        "fv_bound": B,
        "violation": E - B,  # negative means QEI is violated (E < bound)
        "is_violated": E < B,
    }
