#!/usr/bin/env python3
"""
KEVINOTRON — JAX/GPU Lattice Gauge Theory EE Engine
=====================================================
4D Wilson gauge theory: SU(2), SU(3), SU(4), G₂
Entanglement entropy via BP2008b α-integration (replica trick)
Metropolis with checkerboard parallelism for GPU

Kévin Rémondière (ORCID 0009-0008-2443-7166)

PATCHES INTEGRATED:
- Bryant 3-form with correct signs (-e^{257}, -e^{347}, -e^{356})
- SVD null space for G₂ generators (14 exact from 35×21 constraint)
- Tr(U·K) NOT Tr(U·K†) in Wilson action
- β = 7/g² for G₂ (not 2N/g²)
- eigh exact expm (not Taylor or Rodrigues)
- Entangling surface A = 2L³ (temporal cut, 4D)
- Boundary detection: mu=0 AND x[0]=L//2-1
"""

import jax
import jax.numpy as jnp
from jax import jit, vmap, lax, random
from functools import partial
import numpy as np
import time
import argparse
import sys

print(f"JAX {jax.__version__}, devices: {jax.devices()}")


# ============================================================
# G₂ GENERATORS — 14 antisymmetric 7×7 real via SVD
# ============================================================

def build_g2_generators_np():
    """Build 14 generators of g₂ ⊂ so(7) via Bryant 3-form SVD.
    Bryant convention: φ = e^{123}+e^{145}+e^{167}+e^{246}-e^{257}-e^{347}-e^{356}
    """
    signed_triples = [
        (0,1,2,1.0),(0,3,4,1.0),(0,5,6,1.0),(1,3,5,1.0),
        (1,4,6,-1.0),(2,3,6,-1.0),(2,4,5,-1.0),
    ]
    f = np.zeros((7,7,7))
    for i,j,k,s in signed_triples:
        f[i,j,k]=s; f[j,k,i]=s; f[k,i,j]=s
        f[j,i,k]=-s; f[k,j,i]=-s; f[i,k,j]=-s

    triples = [(i,j,k) for i in range(7) for j in range(i+1,7) for k in range(j+1,7)]
    pairs = [(p,q) for p in range(7) for q in range(p+1,7)]

    M = np.zeros((35,21))
    for ti,(i,j,k) in enumerate(triples):
        for gi,(p,q) in enumerate(pairs):
            v = 0.0
            if i==p: v += f[q,j,k]
            if i==q: v -= f[p,j,k]
            if j==p: v += f[i,q,k]
            if j==q: v -= f[i,p,k]
            if k==p: v += f[i,j,q]
            if k==q: v -= f[i,j,p]
            M[ti,gi] = v

    U, S, Vt = np.linalg.svd(M, full_matrices=True)
    gens = []
    for r in range(21):
        if (S[r] < 1e-10) if r < len(S) else True:
            g = np.zeros((7,7))
            for idx,(p,q) in enumerate(pairs):
                g[p,q] = Vt[r,idx]
                g[q,p] = -Vt[r,idx]
            gsq = np.sum(g * g)
            norm = np.sqrt(max(-gsq, 0.0))
            if norm > 1e-10:
                g *= np.sqrt(2.0) / norm
            gens.append(g)
    assert len(gens) == 14, f"Expected 14 generators, got {len(gens)}"
    return np.array(gens)  # (14, 7, 7)


# ============================================================
# SU(N) GENERATORS — Gell-Mann basis
# ============================================================

def build_sun_generators_np(N):
    """Build N²-1 generators of su(N) as anti-Hermitian N×N complex matrices.
    T_a = i λ_a / 2 where λ_a are generalized Gell-Mann matrices.
    """
    gens = []
    # Symmetric off-diagonal (N(N-1)/2)
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N, N), dtype=np.complex128)
            g[j,k] = 0.5j
            g[k,j] = 0.5j
            gens.append(g)
    # Anti-symmetric off-diagonal (N(N-1)/2)
    for j in range(N):
        for k in range(j+1, N):
            g = np.zeros((N, N), dtype=np.complex128)
            g[j,k] = 0.5
            g[k,j] = -0.5
            gens.append(g)
    # Diagonal (N-1)
    for l in range(1, N):
        g = np.zeros((N, N), dtype=np.complex128)
        s = np.sqrt(1.0 / (2*l*(l+1)))
        for j in range(l):
            g[j,j] = 1j * s
        g[l,l] = -1j * l * s
        gens.append(g)
    assert len(gens) == N*N - 1, f"Expected {N*N-1} generators, got {len(gens)}"
    return np.array(gens)  # (N²-1, N, N) complex


# ============================================================
# MATRIX EXPONENTIAL — exact via eigh
# ============================================================

@jit
def expm_antiherm_complex(A):
    """exp(A) for anti-Hermitian complex matrix via eigh."""
    iA = -1j * A
    evals, evecs = jnp.linalg.eigh(iA)
    return (evecs * jnp.exp(1j * evals)) @ evecs.conj().T

@jit
def expm_antisym_real(A):
    """exp(A) for antisymmetric real matrix via eigh of iA."""
    N = A.shape[0]
    iA = 1j * A
    evals, evecs = jnp.linalg.eigh(iA)
    result = (evecs * jnp.exp(-1j * evals)) @ evecs.conj().T
    return result.real


# ============================================================
# GROUP-SPECIFIC OPERATIONS
# ============================================================

class G2Config:
    dim_rep = 7
    dim_adj = 14
    C2 = 4
    center_order = 1
    is_complex = False
    name = "G2"

    def __init__(self):
        self.gens = jnp.array(build_g2_generators_np())

    def random_element(self, key, eps):
        omega = random.normal(key, (14,)) * eps
        A = jnp.einsum('g,gij->ij', omega, self.gens)
        return expm_antisym_real(A)

    def identity(self):
        return jnp.eye(7)

    def mul(self, U, V):
        return U @ V

    def dagger(self, U):
        return U.T

    def trace_re(self, U):
        return jnp.trace(U)

    def beta_norm(self):
        return 7.0


class SUNConfig:
    is_complex = True

    def __init__(self, N):
        self.N = N
        self.dim_rep = N
        self.dim_adj = N * N - 1
        self.C2 = N
        self.center_order = N
        self.name = f"SU({N})"
        self.gens = jnp.array(build_sun_generators_np(N))

    def random_element(self, key, eps):
        omega = random.normal(key, (self.dim_adj,)) * eps
        A = jnp.einsum('g,gij->ij', omega, self.gens)
        return expm_antiherm_complex(A)

    def identity(self):
        return jnp.eye(self.dim_rep, dtype=jnp.complex128)

    def mul(self, U, V):
        return U @ V

    def dagger(self, U):
        return U.conj().T

    def trace_re(self, U):
        return jnp.trace(U).real

    def beta_norm(self):
        return float(self.dim_rep)


# ============================================================
# LATTICE ENGINE (JAX-compatible)
# ============================================================

def make_lattice_fns(group, Ls, Lt, beta, alpha=0.0):
    """Create JIT-compiled lattice functions for the given group."""
    d = group.dim_rep
    beta_norm = group.beta_norm()

    def init_cold():
        if group.is_complex:
            return jnp.tile(jnp.eye(d, dtype=jnp.complex128), (4, Ls, Ls, Ls, Lt, 1, 1))
        else:
            return jnp.tile(jnp.eye(d), (4, Ls, Ls, Ls, Lt, 1, 1))

    def shift_idx(s, mu, d_shift):
        sizes = jnp.array([Ls, Ls, Ls, Lt])
        return (s + d_shift * jnp.eye(4, dtype=jnp.int32)[mu]) % sizes

    @jit
    def get_link(links, s, mu):
        return links[mu, s[0], s[1], s[2], s[3]]

    @jit
    def staple_sum(links, s, mu):
        """Sum of 6 staples (3 positive + 3 negative plaquettes)."""
        if group.is_complex:
            K = jnp.zeros((d, d), dtype=jnp.complex128)
        else:
            K = jnp.zeros((d, d))

        sizes = jnp.array([Ls, Ls, Ls, Lt])
        s_mu = (s + jnp.eye(4, dtype=jnp.int32)[mu]) % sizes

        def add_staple(K, nu):
            s_nu = (s + jnp.eye(4, dtype=jnp.int32)[nu]) % sizes
            s_mu_nu_back = (s_mu - jnp.eye(4, dtype=jnp.int32)[nu]) % sizes
            s_nu_back = (s - jnp.eye(4, dtype=jnp.int32)[nu]) % sizes

            U_nu_at_smu = links[nu, s_mu[0], s_mu[1], s_mu[2], s_mu[3]]
            U_mu_at_snu = links[mu, s_nu[0], s_nu[1], s_nu[2], s_nu[3]]
            U_nu_at_s = links[nu, s[0], s[1], s[2], s[3]]

            if group.is_complex:
                staple_pos = U_nu_at_smu @ U_mu_at_snu.conj().T @ U_nu_at_s.conj().T
            else:
                staple_pos = U_nu_at_smu @ U_mu_at_snu.T @ U_nu_at_s.T

            U_nu_at_smunub = links[nu, s_mu_nu_back[0], s_mu_nu_back[1], s_mu_nu_back[2], s_mu_nu_back[3]]
            U_mu_at_snub = links[mu, s_nu_back[0], s_nu_back[1], s_nu_back[2], s_nu_back[3]]
            U_nu_at_snub = links[nu, s_nu_back[0], s_nu_back[1], s_nu_back[2], s_nu_back[3]]

            if group.is_complex:
                staple_neg = U_nu_at_smunub.conj().T @ U_mu_at_snub.conj().T @ U_nu_at_snub
            else:
                staple_neg = U_nu_at_smunub.T @ U_mu_at_snub.T @ U_nu_at_snub

            return K + staple_pos + staple_neg

        for nu in range(4):
            K = jax.lax.cond(nu != mu, lambda K: add_staple(K, nu), lambda K: K, K)

        return K

    @jit
    def local_action(U_link, K, is_boundary):
        """Wilson action contribution: -(β/d_R) Re Tr(U·K)."""
        if group.is_complex:
            tr = jnp.trace(U_link @ K).real
        else:
            tr = jnp.trace(U_link @ K)
        base = -(beta / beta_norm) * tr
        return jnp.where(is_boundary, (1.0 - alpha) * base, base)

    @jit
    def is_boundary(s, mu):
        """Boundary link: mu=0 AND x[0] = Ls//2 - 1."""
        return (mu == 0) & (s[0] == Ls // 2 - 1)

    @jit
    def metropolis_update_site(links, s, mu, key, eps):
        """Single-site Metropolis update."""
        U_old = links[mu, s[0], s[1], s[2], s[3]]
        K = staple_sum(links, s, mu)
        bdy = is_boundary(s, mu)
        S_old = local_action(U_old, K, bdy)

        U_new = group.random_element(key, eps) @ U_old
        S_new = local_action(U_new, K, bdy)

        dS = S_new - S_old
        key2, accept_key = random.split(key)
        accept = (dS < 0.0) | (random.uniform(accept_key) < jnp.exp(-dS))

        U_updated = jnp.where(accept, U_new, U_old)
        links = links.at[mu, s[0], s[1], s[2], s[3]].set(U_updated)
        return links, accept

    @jit
    def plaquette_avg(links):
        """Average plaquette ⟨(1/d_R) Re Tr U_plaq⟩."""
        total = 0.0
        count = 0
        sizes = jnp.array([Ls, Ls, Ls, Lt])
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        s = jnp.array([x0, x1, x2, x3])
                        for mu in range(4):
                            for nu in range(mu+1, 4):
                                s_mu = (s + jnp.eye(4, dtype=jnp.int32)[mu]) % sizes
                                s_nu = (s + jnp.eye(4, dtype=jnp.int32)[nu]) % sizes
                                U1 = links[mu, s[0], s[1], s[2], s[3]]
                                U2 = links[nu, s_mu[0], s_mu[1], s_mu[2], s_mu[3]]
                                U3 = links[mu, s_nu[0], s_nu[1], s_nu[2], s_nu[3]]
                                U4 = links[nu, s[0], s[1], s[2], s[3]]
                                if group.is_complex:
                                    P = U1 @ U2 @ U3.conj().T @ U4.conj().T
                                    total += jnp.trace(P).real / d
                                else:
                                    P = U1 @ U2 @ U3.T @ U4.T
                                    total += jnp.trace(P) / d
                                count += 1
        return total / count

    @jit
    def boundary_action_sum(links):
        """Sum of boundary link actions dS/dα = Σ_{bdy links} (β/d_R) Re Tr(U·K)."""
        total = 0.0
        sizes = jnp.array([Ls, Ls, Ls, Lt])
        x0 = Ls // 2 - 1
        mu = 0
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    s = jnp.array([x0, x1, x2, x3])
                    U = links[mu, s[0], s[1], s[2], s[3]]
                    K = staple_sum(links, s, mu)
                    if group.is_complex:
                        tr = jnp.trace(U @ K).real
                    else:
                        tr = jnp.trace(U @ K)
                    total += (beta / beta_norm) * tr
        return total

    return {
        'init_cold': init_cold,
        'metropolis_update_site': metropolis_update_site,
        'plaquette_avg': plaquette_avg,
        'boundary_action_sum': boundary_action_sum,
        'staple_sum': staple_sum,
    }


# ============================================================
# SIMULATION ENGINE
# ============================================================

def run_ee_single_alpha(group, Ls, beta, alpha, n_therm=500, n_meas=200,
                        n_skip=5, eps=0.15, seed=42):
    """Run EE measurement for a single α value. Direct port of Rust g2_ee_single."""
    Lt = 2 * Ls
    fns = make_lattice_fns(group, Ls, Lt, beta, alpha)

    links = fns['init_cold']()
    key = random.PRNGKey(seed + int(alpha * 1000))

    # Thermalization
    t0 = time.time()
    for sweep in range(n_therm):
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        s = jnp.array([x0, x1, x2, x3])
                        for mu in range(4):
                            key, subkey = random.split(key)
                            links, _ = fns['metropolis_update_site'](links, s, mu, subkey, eps)
        if (sweep + 1) % 100 == 0:
            P = float(fns['plaquette_avg'](links))
            elapsed = time.time() - t0
            print(f"  therm {sweep+1}/{n_therm}: ⟨P⟩={P:.6f} ({elapsed:.1f}s)", file=sys.stderr)

    # Measurements
    measurements = []
    for m in range(n_meas):
        for _ in range(n_skip):
            for x0 in range(Ls):
                for x1 in range(Ls):
                    for x2 in range(Ls):
                        for x3 in range(Lt):
                            s = jnp.array([x0, x1, x2, x3])
                            for mu in range(4):
                                key, subkey = random.split(key)
                                links, _ = fns['metropolis_update_site'](links, s, mu, subkey, eps)
        ds = float(fns['boundary_action_sum'](links))
        measurements.append(ds)

    mean = np.mean(measurements)
    err = np.std(measurements) / np.sqrt(len(measurements))
    return mean, err


def run_full_ee(group, Ls, beta, n_alpha=11, **kwargs):
    """Run full EE measurement with trapezoidal α-integration."""
    alphas = np.linspace(0.0, 1.0, n_alpha)
    results = []

    for a in alphas:
        mean, err = run_ee_single_alpha(group, Ls, beta, a, **kwargs)
        print(f"ALPHA {a:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")
        results.append((a, mean, err))

    # Trapezoidal integration
    alphas_arr = np.array([r[0] for r in results])
    ds_arr = np.array([r[1] for r in results])
    S2 = np.trapezoid(ds_arr, alphas_arr)
    A = 2 * Ls**3
    S2_over_A = S2 / A

    print(f"\nS₂ = {S2:.4f}")
    print(f"A = 2L³ = {A}")
    print(f"S₂/A = {S2_over_A:.4f}")
    return S2_over_A


# ============================================================
# FAST ENGINE — Scan-based sweep (no Python loops per site)
# ============================================================

def make_fast_sweep(group, Ls, Lt, beta, alpha, eps):
    """Create a JIT-compiled full sweep using lax.fori_loop."""
    d = group.dim_rep
    beta_norm = group.beta_norm()
    N_sites = Ls * Ls * Ls * Lt * 4
    sizes = jnp.array([Ls, Ls, Ls, Lt])

    def decode_site(flat_idx):
        mu = flat_idx % 4
        rem = flat_idx // 4
        x3 = rem % Lt
        rem = rem // Lt
        x2 = rem % Ls
        rem = rem // Ls
        x1 = rem % Ls
        x0 = rem // Ls
        return jnp.array([x0, x1, x2, x3]), mu

    @jit
    def sweep_body(i, state):
        links, key, n_accept = state
        key, subkey = random.split(key)
        s, mu = decode_site(i)

        U_old = links[mu, s[0], s[1], s[2], s[3]]

        # Staple sum (unrolled for JIT)
        if group.is_complex:
            K = jnp.zeros((d, d), dtype=jnp.complex128)
        else:
            K = jnp.zeros((d, d))

        s_mu = (s + jnp.eye(4, dtype=jnp.int32)[mu]) % sizes

        for nu in range(4):
            def add_nu(K, nu=nu):
                s_nu = (s + jnp.eye(4, dtype=jnp.int32)[nu]) % sizes
                s_mu_nu_b = (s_mu - jnp.eye(4, dtype=jnp.int32)[nu]) % sizes
                s_nu_b = (s - jnp.eye(4, dtype=jnp.int32)[nu]) % sizes

                U1 = links[nu, s_mu[0], s_mu[1], s_mu[2], s_mu[3]]
                U2 = links[mu, s_nu[0], s_nu[1], s_nu[2], s_nu[3]]
                U3 = links[nu, s[0], s[1], s[2], s[3]]

                U4 = links[nu, s_mu_nu_b[0], s_mu_nu_b[1], s_mu_nu_b[2], s_mu_nu_b[3]]
                U5 = links[mu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]
                U6 = links[nu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]

                if group.is_complex:
                    sp = U1 @ U2.conj().T @ U3.conj().T
                    sn = U4.conj().T @ U5.conj().T @ U6
                else:
                    sp = U1 @ U2.T @ U3.T
                    sn = U4.T @ U5.T @ U6

                return K + sp + sn

            K = jax.lax.cond(nu != mu, add_nu, lambda K: K, K)

        # Action
        bdy = (mu == 0) & (s[0] == Ls // 2 - 1)
        if group.is_complex:
            tr_old = jnp.trace(U_old @ K).real
        else:
            tr_old = jnp.trace(U_old @ K)
        S_old = -(beta / beta_norm) * tr_old
        S_old = jnp.where(bdy, (1.0 - alpha) * S_old, S_old)

        # Propose
        U_new = group.random_element(subkey, eps) @ U_old
        if group.is_complex:
            tr_new = jnp.trace(U_new @ K).real
        else:
            tr_new = jnp.trace(U_new @ K)
        S_new = -(beta / beta_norm) * tr_new
        S_new = jnp.where(bdy, (1.0 - alpha) * S_new, S_new)

        dS = S_new - S_old
        key, accept_key = random.split(key)
        accept = (dS < 0.0) | (random.uniform(accept_key) < jnp.exp(-dS))

        U_upd = jnp.where(accept, U_new, U_old)
        links = links.at[mu, s[0], s[1], s[2], s[3]].set(U_upd)
        n_accept = n_accept + accept.astype(jnp.int32)

        return links, key, n_accept

    @jit
    def full_sweep(links, key):
        links, key, n_accept = lax.fori_loop(0, N_sites, sweep_body, (links, key, 0))
        return links, key, n_accept

    return full_sweep


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Kevinotron — JAX/GPU Lattice Gauge EE')
    parser.add_argument('--group', choices=['su2','su3','su4','g2'], required=True)
    parser.add_argument('--ls', type=int, required=True, help='Spatial lattice size')
    parser.add_argument('--beta', type=float, required=True)
    parser.add_argument('--alpha', type=float, default=None, help='Single α (if not set, run full EE)')
    parser.add_argument('--n-therm', type=int, default=500)
    parser.add_argument('--n-meas', type=int, default=200)
    parser.add_argument('--n-skip', type=int, default=5)
    parser.add_argument('--eps', type=float, default=0.15)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--fast', action='store_true', help='Use lax.fori_loop sweep (slower JIT, faster run)')
    parser.add_argument('--plaquette-only', action='store_true', help='Just thermalize and measure ⟨P⟩')
    args = parser.parse_args()

    if args.group == 'g2':
        group = G2Config()
    elif args.group == 'su2':
        group = SUNConfig(2)
    elif args.group == 'su3':
        group = SUNConfig(3)
    elif args.group == 'su4':
        group = SUNConfig(4)

    print(f"Kevinotron: {group.name}, L={args.ls}, β={args.beta}", file=sys.stderr)

    if args.plaquette_only:
        Lt = 2 * args.ls
        fns = make_lattice_fns(group, args.ls, Lt, args.beta, 0.0)
        links = fns['init_cold']()
        key = random.PRNGKey(args.seed)
        for sweep in range(args.n_therm):
            for x0 in range(args.ls):
                for x1 in range(args.ls):
                    for x2 in range(args.ls):
                        for x3 in range(Lt):
                            s = jnp.array([x0, x1, x2, x3])
                            for mu in range(4):
                                key, subkey = random.split(key)
                                links, _ = fns['metropolis_update_site'](links, s, mu, subkey, args.eps)
            if (sweep + 1) % 50 == 0:
                P = float(fns['plaquette_avg'](links))
                print(f"sweep {sweep+1}: ⟨P⟩ = {P:.6f}")
    elif args.alpha is not None:
        mean, err = run_ee_single_alpha(
            group, args.ls, args.beta, args.alpha,
            n_therm=args.n_therm, n_meas=args.n_meas,
            n_skip=args.n_skip, eps=args.eps, seed=args.seed
        )
        print(f"ALPHA {args.alpha:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")
    else:
        S2_A = run_full_ee(
            group, args.ls, args.beta,
            n_therm=args.n_therm, n_meas=args.n_meas,
            n_skip=args.n_skip, eps=args.eps
        )


if __name__ == '__main__':
    main()
