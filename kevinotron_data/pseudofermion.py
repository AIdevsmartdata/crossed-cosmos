from cg_solver import cg_solve_wilson
"""Pseudofermion field generation and force computation."""
import jax
import jax.numpy as jnp
from wilson_dirac import apply_wilson_dirac, apply_ddag, apply_gamma5


def generate_pseudofermion(U, mass, Ls, Lt, key):
    """Generate pseudofermion φ = D η where η ~ N(0,1).
    
    The pseudofermion action is S_pf = φ†(D†D)⁻¹φ = η†η.
    So generating φ = D η gives the correct distribution.
    """
    Nc = U.shape[-1]
    eta = jax.random.normal(key, (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64) + \
          1j * jax.random.normal(jax.random.fold_in(key, 1), (Ls, Ls, Ls, Lt, 4, Nc), dtype=jnp.float64)
    eta = eta / jnp.sqrt(2.0)  # normalize
    
    phi = apply_wilson_dirac(U, eta, mass, Ls, Lt)
    return phi, eta

def fermion_action(U, phi, mass, Ls, Lt):
    """Compute S_pf = φ†(D†D)⁻¹φ via CG."""
    x, n_iter, res = cg_solve_wilson(U, phi, mass, Ls, Lt, tol=1e-10)
    # S = φ† x where D†D x = φ, so x = (D†D)⁻¹ φ
    S = jnp.sum(jnp.conj(phi) * x).real
    return float(S), n_iter, res

def fermion_force(U, phi, mass, Ls, Lt):
    """Compute dS_pf/dU for the HMC force.
    
    dS_pf/dU_μ(x) = -χ†(x) (1-γ_μ) ψ(x+μ) × U_μ(x)†
                     +ψ†(x+μ) (1+γ_μ) χ(x) × U_μ(x)†
    
    where ψ = (D†D)⁻¹ φ and χ = D ψ.
    
    Returns: force field (4, Ls, Ls, Ls, Lt, Nc, Nc) complex anti-Hermitian
    """
    Nc = U.shape[-1]
    
    # Solve (D†D) ψ = φ
    psi, _, _ = cg_solve_wilson(U, phi, mass, Ls, Lt, tol=1e-10)
    
    # χ = D ψ
    chi = apply_wilson_dirac(U, psi, mass, Ls, Lt)
    
    # Force for each direction μ
    force = jnp.zeros_like(U)
    
    for mu in range(4):
        # ψ(x+μ)
        psi_fwd = jnp.roll(psi, -1, axis=mu)
        chi_fwd = jnp.roll(chi, -1, axis=mu)
        
        from wilson_dirac import P_MINUS, P_PLUS
        
        # Term 1: -χ†(x) P_minus_μ ψ(x+μ) ⊗ [projected onto color matrix]
        # F_μ(x)_{ab} = -Σ_s χ*(x,s,a) [P_minus ψ_fwd](s,b) + h.c.-like terms
        
        # P_minus ψ_fwd: (Ls,Ls,Ls,Lt,4,Nc) contracted with P_minus on spinor
        Pm_psi = jnp.einsum('ab,...bk->...ak', P_MINUS[mu], psi_fwd)
        Pp_chi = jnp.einsum('ab,...bk->...ak', P_PLUS[mu], chi)
        
        # Outer product in color space: χ†(x) ⊗ [P_minus ψ(x+μ)]
        # → (Nc, Nc) matrix at each site
        f1 = -jnp.einsum('...sa,...sb->...ab', jnp.conj(chi), Pm_psi)
        
        # Term 2: reverse direction
        Pm_chi_fwd = jnp.einsum('ab,...bk->...ak', P_MINUS[mu], chi_fwd)
        f2 = jnp.einsum('...sa,...sb->...ab', jnp.conj(psi), Pm_chi_fwd)
        
        # Multiply by U†: force acts on momentum, not directly on U
        # Actually the force is dS/d(U†) which contributes to the momentum update
        f_mu = (f1 + f2)
        
        # Project to anti-Hermitian traceless
        f_ah = (f_mu - jnp.conj(jnp.swapaxes(f_mu, -2, -1))) / 2
        tr = jnp.trace(f_ah, axis1=-2, axis2=-1)[..., None, None] / Nc
        f_ah = f_ah - tr * jnp.eye(Nc)
        
        force = force.at[mu].set(f_ah)
    
    return force
