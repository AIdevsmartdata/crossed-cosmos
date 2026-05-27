"""
hmc.py — Full HMC with dynamical Wilson fermions on GPU.

Architecture:
  1. Generate gauge momenta (anti-Hermitian traceless)
  2. Generate pseudofermion φ = D η
  3. Leapfrog: alternate momentum + link updates with gauge + fermion forces
  4. Accept/reject via exp(-ΔH)
"""
import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
import numpy as np
from time import time

from .wilson_dirac import apply_wilson_dirac, GAMMA5
from .cg_solver import cg_solve
from .pseudofermion import generate_pseudofermion, fermion_action, fermion_force


class HMC:
    def __init__(self, Nc=3, Ls=4, Lt=None, beta=6.0, mass=0.1, n_flavors=2,
                 n_steps=20, dt=0.01):
        self.Nc = Nc
        self.Ls = Ls
        self.Lt = Lt or 2 * Ls
        self.beta = beta
        self.mass = mass
        self.n_flavors = n_flavors
        self.n_steps = n_steps
        self.dt = dt
        
        print(f"HMC: SU({Nc}) Ls={Ls} Lt={self.Lt} β={beta} m={mass} Nf={n_flavors}")
        print(f"     dt={dt} n_steps={n_steps} traj_length={dt*n_steps:.2f}")
    
    def cold_start(self):
        """Initialize identity gauge field."""
        U = jnp.broadcast_to(
            jnp.eye(self.Nc, dtype=jnp.complex128),
            (4, self.Ls, self.Ls, self.Ls, self.Lt, self.Nc, self.Nc)
        ).copy()
        return U
    
    def plaquette(self, U):
        """Average plaquette."""
        p = 0.0
        count = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                U_mu = U[mu]
                U_nu = U[nu]
                U_mu_shifted = jnp.roll(U_mu, -1, axis=nu)  # U_μ(x+ν)  -- wait, wrong
                # Actually need U_ν(x+μ), U_μ(x+ν), etc.
                U_nu_at_xmu = jnp.roll(U_nu, -1, axis=mu)  # U_ν(x+μ)
                U_mu_at_xnu = jnp.roll(U_mu, -1, axis=nu)  # U_μ(x+ν)
                
                plaq = jnp.einsum('...ab,...bc,...dc,...da->...', 
                                  U_mu, U_nu_at_xmu, 
                                  jnp.conj(U_mu_at_xnu).swapaxes(-2,-1),
                                  jnp.conj(U_nu).swapaxes(-2,-1))
                p += jnp.mean(plaq.real) / self.Nc
                count += 1
        return float(p / count)
    
    def gauge_action(self, U):
        """S_gauge = (β/Nc) Σ (Nc - Re Tr P)."""
        p = self.plaquette(U)
        n_plaq = 6 * self.Ls**3 * self.Lt
        return self.beta * n_plaq * (1.0 - p)
    
    def random_momenta(self, key):
        """Generate random anti-Hermitian traceless momenta."""
        shape = (4, self.Ls, self.Ls, self.Ls, self.Lt, self.Nc, self.Nc)
        Nc = self.Nc
        
        # Random complex matrix
        k1, k2 = jax.random.split(key)
        M = jax.random.normal(k1, shape, dtype=jnp.float64) + \
            1j * jax.random.normal(k2, shape, dtype=jnp.float64)
        M = M / jnp.sqrt(2.0)
        
        # Anti-Hermitian: (M - M†)/2
        M = (M - jnp.conj(M.swapaxes(-2, -1))) / 2
        
        # Traceless
        tr = jnp.trace(M, axis1=-2, axis2=-1)[..., None, None] / Nc
        M = M - tr * jnp.eye(Nc, dtype=jnp.complex128)
        
        return M
    
    def kinetic_energy(self, P):
        """T = -Tr(P²) summed over all links."""
        P2 = jnp.einsum('...ab,...bc->...ac', P, P)
        return float(-jnp.sum(jnp.trace(P2, axis1=-2, axis2=-1)).real)
    
    def gauge_force(self, U):
        """F_gauge = -(β/Nc) × Ta(U × staple_sum)."""
        Nc = self.Nc
        beta_N = self.beta / Nc
        F = jnp.zeros_like(U)
        
        for mu in range(4):
            staple = jnp.zeros((self.Ls, self.Ls, self.Ls, self.Lt, Nc, Nc), 
                              dtype=jnp.complex128)
            for nu in range(4):
                if nu == mu:
                    continue
                # Forward staple
                U_nu_at_xmu = jnp.roll(U[nu], -1, axis=mu)
                U_mu_at_xnu = jnp.roll(U[mu], -1, axis=nu)
                s_fwd = jnp.einsum('...ab,...bc,...dc->...ad',
                                   U_nu_at_xmu,
                                   jnp.conj(U_mu_at_xnu).swapaxes(-2,-1),
                                   jnp.conj(U[nu]).swapaxes(-2,-1))
                
                # Backward staple
                U_nu_at_xmu_mnu = jnp.roll(jnp.roll(U[nu], -1, axis=mu), 1, axis=nu)
                U_mu_at_xmnu = jnp.roll(U[mu], 1, axis=nu)
                U_nu_at_xmnu = jnp.roll(U[nu], 1, axis=nu)
                s_bwd = jnp.einsum('...ba,...dc,...cd->...ad',
                                   jnp.conj(U_nu_at_xmu_mnu),
                                   jnp.conj(U_mu_at_xmnu),
                                   U_nu_at_xmnu)  # this needs fixing
                # Actually: U†_ν(x+μ-ν) × U†_μ(x-ν) × U_ν(x-ν)
                s_bwd = jnp.einsum('...ba,...dc,...de->...ae',
                                   jnp.conj(U_nu_at_xmu_mnu),
                                   jnp.conj(U_mu_at_xmnu),
                                   U_nu_at_xmnu)
                
                staple = staple + s_fwd + s_bwd
            
            V = jnp.einsum('...ab,...bc->...ac', U[mu], staple)
            V = V * beta_N
            
            # Anti-Hermitian traceless projection
            V_ah = (V - jnp.conj(V.swapaxes(-2,-1))) / 2
            tr = jnp.trace(V_ah, axis1=-2, axis2=-1)[..., None, None] / Nc
            V_ah = V_ah - tr * jnp.eye(Nc, dtype=jnp.complex128)
            
            F = F.at[mu].set(V_ah)
        
        return F
    
    def update_momenta(self, P, F_gauge, F_ferm, dt):
        """P -= dt × (F_gauge + F_ferm)."""
        return P - dt * (F_gauge + F_ferm)
    
    def update_links(self, U, P, dt):
        """U = expm(dt × P) × U."""
        Nc = self.Nc
        dtP = dt * P
        # Taylor-12 expm
        exp_P = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), dtP.shape).copy()
        power = jnp.broadcast_to(jnp.eye(Nc, dtype=jnp.complex128), dtP.shape).copy()
        for k in range(1, 13):
            power = jnp.einsum('...ab,...bc->...ac', power, dtP) / k
            exp_P = exp_P + power
        
        U_new = jnp.einsum('...ab,...bc->...ac', exp_P, U)
        
        # Reunitarize (Gram-Schmidt)
        for j in range(Nc):
            col = U_new[..., :, j]
            for i in range(j):
                prev = U_new[..., :, i]
                proj = jnp.sum(jnp.conj(prev) * col, axis=-1, keepdims=True)
                col = col - proj * prev
            norm = jnp.sqrt(jnp.sum(jnp.abs(col)**2, axis=-1, keepdims=True))
            U_new = U_new.at[..., :, j].set(col / jnp.maximum(norm, 1e-15))
        
        # Fix det = 1 (approximate)
        return U_new
    
    def trajectory(self, U, key):
        """One HMC trajectory with gauge + fermion forces."""
        k1, k2, k3 = jax.random.split(key, 3)
        
        U_old = U.copy()
        
        # Generate momenta
        P = self.random_momenta(k1)
        
        # Generate pseudofermion
        phi, _ = generate_pseudofermion(U, self.mass, self.Ls, self.Lt, k2)
        
        # Initial Hamiltonian
        T_old = self.kinetic_energy(P)
        S_gauge_old = self.gauge_action(U)
        S_ferm_old, _, _ = fermion_action(U, phi, self.mass, self.Ls, self.Lt)
        H_old = T_old + S_gauge_old + S_ferm_old
        
        # Leapfrog
        F_gauge = self.gauge_force(U)
        F_ferm = fermion_force(U, phi, self.mass, self.Ls, self.Lt)
        
        # Half step momenta
        P = self.update_momenta(P, F_gauge, F_ferm, 0.5 * self.dt)
        
        for step in range(self.n_steps - 1):
            U = self.update_links(U, P, self.dt)
            F_gauge = self.gauge_force(U)
            F_ferm = fermion_force(U, phi, self.mass, self.Ls, self.Lt)
            P = self.update_momenta(P, F_gauge, F_ferm, self.dt)
        
        U = self.update_links(U, P, self.dt)
        F_gauge = self.gauge_force(U)
        F_ferm = fermion_force(U, phi, self.mass, self.Ls, self.Lt)
        P = self.update_momenta(P, F_gauge, F_ferm, 0.5 * self.dt)
        
        # Final Hamiltonian
        T_new = self.kinetic_energy(P)
        S_gauge_new = self.gauge_action(U)
        S_ferm_new, _, _ = fermion_action(U, phi, self.mass, self.Ls, self.Lt)
        H_new = T_new + S_gauge_new + S_ferm_new
        
        dH = H_new - H_old
        
        # Accept/reject
        r = jax.random.uniform(k3, dtype=jnp.float64)
        accepted = float(r) < min(1.0, np.exp(-dH))
        
        if not accepted:
            U = U_old
        
        return U, accepted, dH
    
    def generate(self, n_traj=100, n_therm=50):
        """Run HMC and return thermalized configurations."""
        U = self.cold_start()
        key = jax.random.PRNGKey(42)
        
        n_accept = 0
        for traj in range(n_traj):
            key, subkey = jax.random.split(key)
            t0 = time()
            U, accepted, dH = self.trajectory(U, subkey)
            dt_wall = time() - t0
            
            if accepted:
                n_accept += 1
            
            if (traj + 1) % 5 == 0:
                p = self.plaquette(U)
                print(f"  traj {traj+1:>4}: dH={dH:>+8.4f} "
                      f"acc={n_accept}/{traj+1} ({100*n_accept/(traj+1):.0f}%) "
                      f"P={p:.6f} [{dt_wall:.1f}s]")
        
        print(f"HMC done: {n_accept}/{n_traj} accepted ({100*n_accept/n_traj:.0f}%)")
        return U


if __name__ == '__main__':
    hmc = HMC(Nc=3, Ls=4, beta=5.6, mass=0.5, n_steps=10, dt=0.01)
    U = hmc.generate(n_traj=20, n_therm=0)
