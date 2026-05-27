"""
wilson_dirac.py — Wilson-Dirac operator on GPU via JAX.

D_W(x,y) = (4+m)δ_{xy} - ½Σ_μ [(1-γ_μ)U_μ(x)δ_{y,x+μ} + (1+γ_μ)U†_μ(y)δ_{y,x-μ}]

γ-matrices: chiral basis (γ₅ = diag(1,1,-1,-1))
γ₅-hermiticity: D† = γ₅ D γ₅

Spinor layout: [site, spinor, color] complex64/128
"""
import jax
import jax.numpy as jnp
import numpy as np
from functools import partial

# Gamma matrices (chiral basis, 4×4 complex)
GAMMA = jnp.array([
    # γ₁
    [[0,0,0,1j],[0,0,1j,0],[0,-1j,0,0],[-1j,0,0,0]],
    # γ₂
    [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]],
    # γ₃
    [[0,0,1j,0],[0,0,0,-1j],[-1j,0,0,0],[0,1j,0,0]],
    # γ₄ (temporal)
    [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]],
], dtype=jnp.complex128)

GAMMA5 = jnp.diag(jnp.array([1.0, 1.0, -1.0, -1.0], dtype=jnp.complex128))

# Projectors: P±_μ = (1 ± γ_μ) / 2
P_MINUS = jnp.array([(jnp.eye(4) - GAMMA[mu]) / 2 for mu in range(4)])  # (4, 4, 4)
P_PLUS = jnp.array([(jnp.eye(4) + GAMMA[mu]) / 2 for mu in range(4)])   # (4, 4, 4)


def apply_wilson_dirac(U, psi, mass, Ls, Lt):
    """Apply D_W to spinor field psi.
    
    Args:
        U: gauge field (4, Ls, Ls, Ls, Lt, Nc, Nc) complex
        psi: spinor field (Ls, Ls, Ls, Lt, 4, Nc) complex
        mass: quark mass
        Ls, Lt: lattice dimensions
    
    Returns:
        D_W psi: same shape as psi
    """
    Nc = U.shape[-1]
    result = (4.0 + mass) * psi  # diagonal term
    
    for mu in range(4):
        sizes = [Ls, Ls, Ls, Lt]
        
        # Forward: -½(1-γ_μ) U_μ(x) ψ(x+μ)
        psi_fwd = jnp.roll(psi, -1, axis=mu)  # ψ(x+μ)
        # U_μ(x) @ ψ(x+μ): contract color index
        U_psi_fwd = jnp.einsum('...ab,...sb->...sa', U[mu], psi_fwd)
        # Apply projector (1-γ_μ)/2 on spinor indices, then multiply by 2 and -½ = -1
        proj_fwd = jnp.einsum('ab,...bk->...ak', P_MINUS[mu], U_psi_fwd)
        result = result - proj_fwd  # -½ × 2 × P_minus = -P_minus
        
        # Backward: -½(1+γ_μ) U†_μ(x-μ) ψ(x-μ)
        psi_bwd = jnp.roll(psi, 1, axis=mu)  # ψ(x-μ)
        U_bwd = jnp.roll(U[mu], 1, axis=mu)  # U_μ(x-μ)
        U_dag_psi_bwd = jnp.einsum('...ba,...sb->...sa', jnp.conj(U_bwd), psi_bwd)
        proj_bwd = jnp.einsum('ab,...bk->...ak', P_PLUS[mu], U_dag_psi_bwd)
        result = result - proj_bwd
    
    return result


def apply_gamma5(psi):
    """Apply γ₅ = diag(1,1,-1,-1) to spinor."""
    return psi.at[..., 2:, :].multiply(-1)


def apply_ddag(U, psi, mass, Ls, Lt):
    """Apply D† = γ₅ D γ₅."""
    return apply_gamma5(apply_wilson_dirac(U, apply_gamma5(psi), mass, Ls, Lt))


def apply_ddag_d(U, psi, mass, Ls, Lt):
    """Apply D†D."""
    return apply_ddag(U, apply_wilson_dirac(U, psi, mass, Ls, Lt), mass, Ls, Lt)


def check_gamma5_hermiticity(U, mass, Ls, Lt):
    """Verify D† = γ₅ D γ₅ numerically."""
    Nc = U.shape[-1]
    key = jax.random.PRNGKey(42)
    psi = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc)) + \
          1j * jax.random.normal(jax.random.PRNGKey(43), (Ls, Ls, Ls, Lt, 4, Nc))
    chi = jax.random.normal(jax.random.PRNGKey(44), (Ls, Ls, Ls, Lt, 4, Nc)) + \
          1j * jax.random.normal(jax.random.PRNGKey(45), (Ls, Ls, Ls, Lt, 4, Nc))
    
    D_psi = apply_wilson_dirac(U, psi, mass, Ls, Lt)
    g5Dg5_chi = apply_gamma5(apply_wilson_dirac(U, apply_gamma5(chi), mass, Ls, Lt))
    
    lhs = jnp.sum(jnp.conj(chi) * D_psi).real
    rhs = jnp.sum(jnp.conj(g5Dg5_chi) * psi).real
    
    return float(jnp.abs(lhs - rhs) / jnp.abs(lhs))


if __name__ == '__main__':
    print("Testing Wilson-Dirac on GPU...")
    Ls, Lt, Nc = 4, 8, 3
    # Cold start (identity links)
    U = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), (4, Ls, Ls, Ls, Lt, Nc, Nc)).copy()
    
    err = check_gamma5_hermiticity(U, 0.1, Ls, Lt)
    print(f"γ₅-hermiticity error: {err:.2e}")
    assert err < 1e-12, f"γ₅-hermiticity FAILED: {err}"
    print("PASS")
