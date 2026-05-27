#!/usr/bin/env python3
"""
KEVINOTRON FAST — JAX/GPU Lattice Gauge EE Engine
===================================================
Checkerboard-parallel Metropolis for GPU acceleration.
SU(2), SU(3), SU(4), G₂ via vectorized operations.

All patches from Rust Kevinotron integrated:
- Bryant 3-form G₂ generators (SVD, correct signs)
- Tr(U·K) Wilson action (NOT Tr(U·K†))
- β=7/g² for G₂
- eigh exact expm
- A = 2L³ area normalization (4D spatial cut)

Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""

import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
from jax import jit, vmap, random
import numpy as np
import time
import argparse
import sys

print(f"JAX {jax.__version__}, x64={jax.config.jax_enable_x64}, devices: {jax.devices()}", file=sys.stderr)

# ============================================================
# GENERATORS (numpy, computed once)
# ============================================================

def build_g2_generators():
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
            if i==p: v+=f[q,j,k]
            if i==q: v-=f[p,j,k]
            if j==p: v+=f[i,q,k]
            if j==q: v-=f[i,p,k]
            if k==p: v+=f[i,j,q]
            if k==q: v-=f[i,j,p]
            M[ti,gi]=v
    _,S,Vt = np.linalg.svd(M, full_matrices=True)
    gens = []
    for r in range(21):
        if (S[r] < 1e-10) if r < len(S) else True:
            g = np.zeros((7,7))
            for idx,(p,q) in enumerate(pairs):
                g[p,q]=Vt[r,idx]; g[q,p]=-Vt[r,idx]
            gsq = np.sum(g*g)
            norm = np.sqrt(max(-gsq, 0.0))
            if norm > 1e-10:
                g *= np.sqrt(2.0)/norm
            gens.append(g)
    assert len(gens)==14
    return np.array(gens, dtype=np.float64)

def build_sun_generators(N):
    gens = []
    for j in range(N):
        for k in range(j+1,N):
            g = np.zeros((N,N), dtype=np.complex128)
            g[j,k]=0.5j; g[k,j]=0.5j
            gens.append(g)
    for j in range(N):
        for k in range(j+1,N):
            g = np.zeros((N,N), dtype=np.complex128)
            g[j,k]=0.5; g[k,j]=-0.5
            gens.append(g)
    for l in range(1,N):
        g = np.zeros((N,N), dtype=np.complex128)
        s = np.sqrt(1.0/(2*l*(l+1)))
        for j in range(l): g[j,j]=1j*s
        g[l,l] = -1j*l*s
        gens.append(g)
    assert len(gens)==N*N-1
    return np.array(gens)


# ============================================================
# CORE OPERATIONS — pure JAX, JIT-friendly
# ============================================================

def make_engine(group_name, Ls, beta, alpha=0.0, eps=0.15):
    """Build all JIT-compiled functions for a given group and lattice."""
    Lt = 2 * Ls
    is_g2 = group_name == 'g2'

    if is_g2:
        gens_np = build_g2_generators()
        d = 7
        beta_norm = 7.0
    else:
        N = int(group_name[-1])
        gens_np = build_sun_generators(N)
        d = N
        beta_norm = float(N)

    gens = jnp.array(gens_np)
    n_gens = gens.shape[0]

    # All site coordinates: (Ls, Ls, Ls, Lt) lattice
    # Precompute even/odd site lists for checkerboard
    sites_even = []
    sites_odd = []
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    if (x0+x1+x2+x3) % 2 == 0:
                        sites_even.append([x0,x1,x2,x3])
                    else:
                        sites_odd.append([x0,x1,x2,x3])
    sites_even = jnp.array(sites_even, dtype=jnp.int32)
    sites_odd = jnp.array(sites_odd, dtype=jnp.int32)
    n_even = len(sites_even)
    n_odd = len(sites_odd)

    # Shift vectors
    e = jnp.eye(4, dtype=jnp.int32)
    sizes = jnp.array([Ls, Ls, Ls, Lt])

    # ---- Random group element (single) ----
    def _rand_g2(key):
        omega = random.normal(key, (n_gens,)) * eps
        A = jnp.einsum('g,gij->ij', omega, gens)
        iA = 1j * A
        evals, evecs = jnp.linalg.eigh(iA)
        return ((evecs * jnp.exp(-1j * evals)) @ evecs.conj().T).real

    def _rand_sun(key):
        omega = random.normal(key, (n_gens,)) * eps
        A = jnp.einsum('g,gij->ij', omega, gens)
        iA = -1j * A
        evals, evecs = jnp.linalg.eigh(iA)
        return (evecs * jnp.exp(1j * evals)) @ evecs.conj().T

    rand_element = jit(_rand_g2) if is_g2 else jit(_rand_sun)

    # ---- Batch random elements ----
    batch_rand = jit(vmap(lambda key: rand_element(key)))

    # ---- Dagger ----
    if is_g2:
        dag = lambda U: U.T
        batch_dag = lambda U: jnp.swapaxes(U, -2, -1)
    else:
        dag = lambda U: U.conj().T
        batch_dag = lambda U: jnp.conj(jnp.swapaxes(U, -2, -1))

    # ---- Trace Re ----
    if is_g2:
        trace_re = lambda U: jnp.trace(U)
    else:
        trace_re = lambda U: jnp.trace(U).real

    # ---- Staple at single site ----
    @jit
    def staple_sum(links, s, mu):
        s_mu = (s + e[mu]) % sizes
        if is_g2:
            K = jnp.zeros((d,d))
        else:
            K = jnp.zeros((d,d), dtype=jnp.complex128)

        for nu in range(4):
            if nu == mu:
                continue
            s_nu = (s + e[nu]) % sizes
            s_mu_nu_b = (s_mu - e[nu]) % sizes
            s_nu_b = (s - e[nu]) % sizes

            U_nu_smu = links[nu, s_mu[0], s_mu[1], s_mu[2], s_mu[3]]
            U_mu_snu = links[mu, s_nu[0], s_nu[1], s_nu[2], s_nu[3]]
            U_nu_s   = links[nu, s[0], s[1], s[2], s[3]]
            sp = U_nu_smu @ dag(U_mu_snu) @ dag(U_nu_s)

            U_nu_smunub = links[nu, s_mu_nu_b[0], s_mu_nu_b[1], s_mu_nu_b[2], s_mu_nu_b[3]]
            U_mu_snub   = links[mu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]
            U_nu_snub   = links[nu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]
            sn = dag(U_nu_smunub) @ dag(U_mu_snub) @ U_nu_snub

            K = K + sp + sn
        return K

    # ---- Full sweep for one direction mu, one parity ----
    @jit
    def half_sweep_mu(links, sites, mu, keys):
        """Update all sites of one parity in direction mu."""
        n_sites = sites.shape[0]

        def update_one(i, carry):
            links = carry
            s = sites[i]
            key = keys[i]

            U_old = links[mu, s[0], s[1], s[2], s[3]]
            K = staple_sum(links, s, mu)

            tr_old = trace_re(U_old @ K)
            bdy = (mu == 0) & (s[0] == Ls // 2 - 1)
            S_old = -(beta / beta_norm) * tr_old
            S_old = jnp.where(bdy, (1.0 - alpha) * S_old, S_old)

            U_new = rand_element(key) @ U_old
            tr_new = trace_re(U_new @ K)
            S_new = -(beta / beta_norm) * tr_new
            S_new = jnp.where(bdy, (1.0 - alpha) * S_new, S_new)

            dS = S_new - S_old
            _, accept_key = random.split(key)
            accept = (dS < 0.0) | (random.uniform(accept_key) < jnp.exp(jnp.minimum(-dS, 80.0)))

            U_upd = jnp.where(accept, U_new, U_old)
            links = links.at[mu, s[0], s[1], s[2], s[3]].set(U_upd)
            return links

        links = jax.lax.fori_loop(0, n_sites, update_one, links)
        return links

    # ---- Full sweep ----
    @jit
    def full_sweep(links, key):
        for mu in range(4):
            key, k1, k2 = random.split(key, 3)
            keys_even = random.split(k1, n_even)
            links = half_sweep_mu(links, sites_even, mu, keys_even)
            keys_odd = random.split(k2, n_odd)
            links = half_sweep_mu(links, sites_odd, mu, keys_odd)
        return links, key

    # ---- Plaquette ----
    @jit
    def plaquette_avg(links):
        total = 0.0
        count = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        s = jnp.array([x0,x1,x2,x3])
                        for mu in range(4):
                            for nu in range(mu+1,4):
                                s_mu = (s+e[mu])%sizes
                                s_nu = (s+e[nu])%sizes
                                U1 = links[mu,s[0],s[1],s[2],s[3]]
                                U2 = links[nu,s_mu[0],s_mu[1],s_mu[2],s_mu[3]]
                                U3 = links[mu,s_nu[0],s_nu[1],s_nu[2],s_nu[3]]
                                U4 = links[nu,s[0],s[1],s[2],s[3]]
                                P = U1 @ U2 @ dag(U3) @ dag(U4)
                                total = total + trace_re(P)/d
                                count += 1
        return total/count

    # ---- Boundary action sum (dS/dα) ----
    @jit
    def boundary_ds(links):
        total = 0.0
        x0 = Ls//2-1
        mu = 0
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    s = jnp.array([x0,x1,x2,x3])
                    U = links[mu,s[0],s[1],s[2],s[3]]
                    K = staple_sum(links, s, mu)
                    total = total + (beta/beta_norm)*trace_re(U@K)
        return total

    # ---- Cold start ----
    def init_cold():
        if is_g2:
            return jnp.tile(jnp.eye(d), (4,Ls,Ls,Ls,Lt,1,1))
        else:
            return jnp.tile(jnp.eye(d,dtype=jnp.complex128), (4,Ls,Ls,Ls,Lt,1,1))

    return {
        'full_sweep': full_sweep,
        'plaquette_avg': plaquette_avg,
        'boundary_ds': boundary_ds,
        'init_cold': init_cold,
        'n_even': n_even,
        'n_odd': n_odd,
    }


# ============================================================
# SIMULATION
# ============================================================

def run_single_alpha(group, Ls, beta, alpha, n_therm=500, n_meas=200,
                     n_skip=5, eps=0.15, seed=42):
    eng = make_engine(group, Ls, beta, alpha, eps)
    links = eng['init_cold']()
    key = random.PRNGKey(seed + int(alpha * 1000))

    t0 = time.time()
    print(f"  JIT compiling...", file=sys.stderr, end=' ', flush=True)
    links, key = eng['full_sweep'](links, key)
    jax.block_until_ready(links)
    print(f"done ({time.time()-t0:.1f}s)", file=sys.stderr)

    t0 = time.time()
    for sweep in range(1, n_therm):
        links, key = eng['full_sweep'](links, key)
        if sweep % 100 == 0:
            jax.block_until_ready(links)
            P = float(eng['plaquette_avg'](links))
            print(f"  therm {sweep}/{n_therm}: P={P:.6f} ({time.time()-t0:.1f}s)", file=sys.stderr)

    measurements = []
    for m in range(n_meas):
        for _ in range(n_skip):
            links, key = eng['full_sweep'](links, key)
        jax.block_until_ready(links)
        ds = float(eng['boundary_ds'](links))
        measurements.append(ds)
        if (m+1) % 50 == 0:
            print(f"  meas {m+1}/{n_meas}", file=sys.stderr)

    mean = np.mean(measurements)
    err = np.std(measurements) / np.sqrt(len(measurements))
    return mean, err


def main():
    parser = argparse.ArgumentParser(description='Kevinotron FAST — JAX/GPU EE')
    parser.add_argument('--group', choices=['su2','su3','su4','g2'], required=True)
    parser.add_argument('--ls', type=int, required=True)
    parser.add_argument('--beta', type=float, required=True)
    parser.add_argument('--alpha', type=float, default=None)
    parser.add_argument('--n-therm', type=int, default=500)
    parser.add_argument('--n-meas', type=int, default=200)
    parser.add_argument('--n-skip', type=int, default=5)
    parser.add_argument('--eps', type=float, default=0.15)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--plaq', action='store_true', help='Plaquette only')
    args = parser.parse_args()

    print(f"Kevinotron: {args.group}, L={args.ls}, β={args.beta}", file=sys.stderr)

    if args.plaq:
        eng = make_engine(args.group, args.ls, args.beta, 0.0, args.eps)
        links = eng['init_cold']()
        key = random.PRNGKey(args.seed)
        t0 = time.time()
        for sweep in range(args.n_therm):
            links, key = eng['full_sweep'](links, key)
            if (sweep+1) % 10 == 0:
                jax.block_until_ready(links)
                P = float(eng['plaquette_avg'](links))
                print(f"sweep {sweep+1}: P = {P:.6f}  ({time.time()-t0:.1f}s)")
    elif args.alpha is not None:
        mean, err = run_single_alpha(
            args.group, args.ls, args.beta, args.alpha,
            n_therm=args.n_therm, n_meas=args.n_meas,
            n_skip=args.n_skip, eps=args.eps, seed=args.seed
        )
        print(f"ALPHA {args.alpha:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")
    else:
        alphas = np.linspace(0.0, 1.0, 11)
        results = []
        for a in alphas:
            mean, err = run_single_alpha(
                args.group, args.ls, args.beta, a,
                n_therm=args.n_therm, n_meas=args.n_meas,
                n_skip=args.n_skip, eps=args.eps, seed=args.seed
            )
            print(f"ALPHA {a:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")
            results.append((a, mean, err))
        alphas_a = np.array([r[0] for r in results])
        ds_a = np.array([r[1] for r in results])
        S2 = np.trapezoid(ds_a, alphas_a)
        A = 2 * args.ls**3
        print(f"\nS₂ = {S2:.4f}, A = {A}, S₂/A = {S2/A:.4f}")


if __name__ == '__main__':
    main()
