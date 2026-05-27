#!/usr/bin/env python3
"""
KEVINOTRON V2 — JAX Lattice Gauge EE Engine
=============================================
Sequential Metropolis (CPU-optimized) with JIT per-site operations.
For GPU, use config dump + spectral modules.

Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""

import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
from jax import jit, random
import numpy as np
import time
import argparse
import sys

print(f"JAX {jax.__version__}, x64={jax.config.jax_enable_x64}, devices: {jax.devices()}", file=sys.stderr)


# ============================================================
# GENERATORS
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
# ENGINE — JIT only per-site ops, Python loops for sweep
# ============================================================

class Kevinotron:
    def __init__(self, group, Ls, beta, alpha=0.0, eps=0.15):
        self.Ls = Ls
        self.Lt = 2 * Ls
        self.beta = beta
        self.alpha = alpha
        self.eps = eps
        self.group = group

        if group == 'g2':
            self.d = 7
            self.gens = jnp.array(build_g2_generators())
            self.beta_norm = 7.0
            self.is_complex = False
            self.links = jnp.tile(jnp.eye(7), (4, Ls, Ls, Ls, self.Lt, 1, 1))
        else:
            N = int(group[-1])
            self.d = N
            self.gens = jnp.array(build_sun_generators(N))
            self.beta_norm = float(N)
            self.is_complex = True
            self.links = jnp.tile(jnp.eye(N, dtype=jnp.complex128),
                                  (4, Ls, Ls, Ls, self.Lt, 1, 1))

        self.n_gens = self.gens.shape[0]
        self.e = jnp.eye(4, dtype=jnp.int32)
        self.sizes = jnp.array([Ls, Ls, Ls, self.Lt])
        self._compile_ops()

    def _compile_ops(self):
        d = self.d
        gens = self.gens
        eps = self.eps
        n_gens = self.n_gens

        if self.is_complex:
            @jit
            def rand_elem(key):
                omega = random.normal(key, (n_gens,)) * eps
                A = jnp.einsum('g,gij->ij', omega, gens)
                iA = -1j * A
                evals, evecs = jnp.linalg.eigh(iA)
                return (evecs * jnp.exp(1j * evals)) @ evecs.conj().T

            @jit
            def trace_re_uk(U, K):
                return jnp.trace(U @ K).real

            dag = lambda U: U.conj().T
        else:
            @jit
            def rand_elem(key):
                omega = random.normal(key, (n_gens,)) * eps
                A = jnp.einsum('g,gij->ij', omega, gens)
                iA = 1j * A.astype(jnp.complex128)
                evals, evecs = jnp.linalg.eigh(iA)
                return ((evecs * jnp.exp(-1j * evals)) @ evecs.conj().T).real

            @jit
            def trace_re_uk(U, K):
                return jnp.trace(U @ K)

            dag = lambda U: U.T

        self._rand_elem = rand_elem
        self._trace_re_uk = trace_re_uk
        self._dag = dag

    def staple_sum(self, s, mu):
        e, sizes, links = self.e, self.sizes, self.links
        d = self.d
        dag = self._dag

        s_mu = (s + e[mu]) % sizes

        if self.is_complex:
            K = jnp.zeros((d, d), dtype=jnp.complex128)
        else:
            K = jnp.zeros((d, d))

        for nu in range(4):
            if nu == mu:
                continue
            s_nu = (s + e[nu]) % sizes
            s_mu_nu_b = (s_mu - e[nu]) % sizes
            s_nu_b = (s - e[nu]) % sizes

            U1 = links[nu, s_mu[0], s_mu[1], s_mu[2], s_mu[3]]
            U2 = links[mu, s_nu[0], s_nu[1], s_nu[2], s_nu[3]]
            U3 = links[nu, s[0], s[1], s[2], s[3]]
            sp = U1 @ dag(U2) @ dag(U3)

            U4 = links[nu, s_mu_nu_b[0], s_mu_nu_b[1], s_mu_nu_b[2], s_mu_nu_b[3]]
            U5 = links[mu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]
            U6 = links[nu, s_nu_b[0], s_nu_b[1], s_nu_b[2], s_nu_b[3]]
            sn = dag(U4) @ dag(U5) @ U6

            K = K + sp + sn
        return K

    def sweep(self, key):
        Ls, Lt = self.Ls, self.Lt
        beta, beta_norm, alpha = self.beta, self.beta_norm, self.alpha
        n_accept = 0
        n_total = 0

        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        s = jnp.array([x0, x1, x2, x3])
                        for mu in range(4):
                            U_old = self.links[mu, x0, x1, x2, x3]
                            K = self.staple_sum(s, mu)

                            tr_old = float(self._trace_re_uk(U_old, K))
                            bdy = (mu == 0) and (x0 == Ls // 2 - 1)
                            S_old = -(beta / beta_norm) * tr_old
                            if bdy:
                                S_old *= (1.0 - alpha)

                            key, subkey = random.split(key)
                            U_new = self._rand_elem(subkey) @ U_old
                            tr_new = float(self._trace_re_uk(U_new, K))
                            S_new = -(beta / beta_norm) * tr_new
                            if bdy:
                                S_new *= (1.0 - alpha)

                            dS = S_new - S_old
                            key, akey = random.split(key)
                            if dS < 0 or float(random.uniform(akey)) < np.exp(min(-dS, 80)):
                                self.links = self.links.at[mu, x0, x1, x2, x3].set(U_new)
                                n_accept += 1
                            n_total += 1

        return key, n_accept / n_total

    def plaquette(self):
        Ls, Lt, d = self.Ls, self.Lt, self.d
        e, sizes, links = self.e, self.sizes, self.links
        dag = self._dag
        total = 0.0
        count = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        s = jnp.array([x0,x1,x2,x3])
                        for mu in range(4):
                            for nu in range(mu+1, 4):
                                s_mu = (s + e[mu]) % sizes
                                s_nu = (s + e[nu]) % sizes
                                P = (links[mu,x0,x1,x2,x3] @
                                     links[nu,s_mu[0],s_mu[1],s_mu[2],s_mu[3]] @
                                     dag(links[mu,s_nu[0],s_nu[1],s_nu[2],s_nu[3]]) @
                                     dag(links[nu,x0,x1,x2,x3]))
                                total += float(self._trace_re_uk(P, jnp.eye(d) if not self.is_complex else jnp.eye(d, dtype=jnp.complex128))) / d
                                count += 1
        return total / count

    def boundary_ds(self):
        Ls, Lt = self.Ls, self.Lt
        total = 0.0
        x0 = Ls // 2 - 1
        mu = 0
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    s = jnp.array([x0, x1, x2, x3])
                    U = self.links[mu, x0, x1, x2, x3]
                    K = self.staple_sum(s, mu)
                    total += float(self._trace_re_uk(U, K)) * (self.beta / self.beta_norm)
        return total

    def save_config(self, path):
        np.save(path, np.array(self.links))


def main():
    parser = argparse.ArgumentParser(description='Kevinotron V2')
    parser.add_argument('--group', choices=['su2','su3','su4','g2'], required=True)
    parser.add_argument('--ls', type=int, required=True)
    parser.add_argument('--beta', type=float, required=True)
    parser.add_argument('--alpha', type=float, default=None)
    parser.add_argument('--n-therm', type=int, default=500)
    parser.add_argument('--n-meas', type=int, default=200)
    parser.add_argument('--n-skip', type=int, default=5)
    parser.add_argument('--eps', type=float, default=0.15)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--plaq', action='store_true')
    parser.add_argument('--dump-config', type=str, default=None, help='Save config to .npy')
    args = parser.parse_args()

    lat = Kevinotron(args.group, args.ls, args.beta,
                     alpha=args.alpha if args.alpha is not None else 0.0,
                     eps=args.eps)
    key = random.PRNGKey(args.seed)

    if args.plaq:
        t0 = time.time()
        for sweep in range(args.n_therm):
            key, acc = lat.sweep(key)
            if (sweep+1) % 10 == 0:
                P = lat.plaquette()
                print(f"sweep {sweep+1}: P = {P:.6f}  acc={acc:.2f}  ({time.time()-t0:.1f}s)")
        if args.dump_config:
            lat.save_config(args.dump_config)
            print(f"Config saved to {args.dump_config}")
    elif args.alpha is not None:
        t0 = time.time()
        for sweep in range(args.n_therm):
            key, acc = lat.sweep(key)
            if (sweep+1) % 100 == 0:
                P = lat.plaquette()
                print(f"  therm {sweep+1}: P={P:.6f} acc={acc:.2f} ({time.time()-t0:.1f}s)",
                      file=sys.stderr)
        measurements = []
        for m in range(args.n_meas):
            for _ in range(args.n_skip):
                key, _ = lat.sweep(key)
            measurements.append(lat.boundary_ds())
            if (m+1) % 50 == 0:
                print(f"  meas {m+1}/{args.n_meas}", file=sys.stderr)
        mean = np.mean(measurements)
        err = np.std(measurements) / np.sqrt(len(measurements))
        print(f"ALPHA {args.alpha:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")
        if args.dump_config:
            lat.save_config(args.dump_config)
    else:
        alphas = np.linspace(0.0, 1.0, 11)
        for a in alphas:
            lat2 = Kevinotron(args.group, args.ls, args.beta, alpha=a, eps=args.eps)
            key2 = random.PRNGKey(args.seed + int(a*1000))
            for _ in range(args.n_therm):
                key2, _ = lat2.sweep(key2)
            measurements = []
            for m in range(args.n_meas):
                for _ in range(args.n_skip):
                    key2, _ = lat2.sweep(key2)
                measurements.append(lat2.boundary_ds())
            mean = np.mean(measurements)
            err = np.std(measurements) / np.sqrt(len(measurements))
            print(f"ALPHA {a:.3f}: dS/dalpha = {mean:.6f} +/- {err:.6f}")


if __name__ == '__main__':
    main()
