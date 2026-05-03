"""Bounce-cosmology scale factors a(τ) used in the FV-QEI scan."""
from __future__ import annotations
import jax.numpy as jnp
from jax import jit


@jit
def a_lqc(tau: jnp.ndarray, *, rho_c: float = 1.0, w: float = 0.0) -> jnp.ndarray:
    """Loop-quantum-cosmology bounce profile (Ashtekar-Singh 2011, eq. 2.6).

    a(τ) = a_min * (1 + 6 ρ_c τ^2 / a_min^2)^{1/(2+w)}
    rho_c = critical Planck-density bounce density (in chosen units).
    w = matter equation of state (0 = dust).
    """
    a_min = 1.0
    return a_min * (1.0 + 6.0 * rho_c * tau**2 / a_min**2) ** (1.0 / (2.0 + w))


@jit
def a_pbb(tau: jnp.ndarray, *, alpha: float = 0.5) -> jnp.ndarray:
    """Pre-big-bang bouncing profile (Veneziano dilaton-driven).

    Branch-glued: a(τ) = (|τ|/τ_0)^α  for τ < 0  (super-inflation),
                  a(τ) = (τ/τ_0)^α     for τ > 0  (radiation-like).
    Smoothed via 1 + ε regulator near τ = 0.
    """
    tau_0 = 1.0
    eps = 1e-6
    return ((tau**2 + eps) / tau_0**2) ** (alpha / 2.0)


@jit
def a_matter_bounce(tau: jnp.ndarray, *, w: float = 0.0) -> jnp.ndarray:
    """Matter-bounce profile (Cai-Wilson-Easson-Brandenberger).

    a(τ) = a_min (1 + 9 H_b^2 τ^2 / a_min^2)^{1/(3(1+w))}.
    """
    a_min = 1.0
    H_b = 1.0
    return a_min * (1.0 + 9.0 * H_b**2 * tau**2 / a_min**2) ** (1.0 / (3.0 * (1.0 + w)))


def get_model(name: str):
    return {
        "loop_quantum": a_lqc,
        "pre_big_bang": a_pbb,
        "matter_bounce": a_matter_bounce,
    }[name]
