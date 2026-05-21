#!/usr/bin/env python3
"""SU(2) Wilson HMC with proper staple (no shortcuts).
Generates configs for downstream analysis.
Time : ~5-30 min on consumer CPU.
"""
import numpy as np, sys, time, argparse, os

# Quaternion SU(2) ops
def su2_mult(u, v):
    a0,a1,a2,a3 = u[..., 0],u[..., 1],u[..., 2],u[..., 3]
    b0,b1,b2,b3 = v[..., 0],v[..., 1],v[..., 2],v[..., 3]
    return np.stack([
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    ], axis=-1)

def su2_dagger(u):
    return np.stack([u[..., 0], -u[..., 1], -u[..., 2], -u[..., 3]], axis=-1)

def staple(links, x, mu, L):
    """Compute SU(2) staple at site x direction mu."""
    stp = np.zeros(4)
    for nu in range(4):
        if nu == mu: continue
        x_p_mu = list(x); x_p_mu[mu] = (x_p_mu[mu]+1) % L
        x_p_nu = list(x); x_p_nu[nu] = (x_p_nu[nu]+1) % L
        x_m_nu = list(x); x_m_nu[nu] = (x_m_nu[nu]-1) % L
        x_p_mu_m_nu = list(x_p_mu); x_p_mu_m_nu[nu] = (x_p_mu_m_nu[nu]-1) % L
        
        # +nu staple: U(x+mu, nu) U†(x+nu, mu) U†(x, nu)
        s1 = su2_mult(
            su2_mult(links[tuple(x_p_mu) + (nu,)], su2_dagger(links[tuple(x_p_nu) + (mu,)])),
            su2_dagger(links[tuple(x) + (nu,)])
        )
        # -nu staple: U†(x+mu-nu, nu) U†(x-nu, mu) U(x-nu, nu)
        s2 = su2_mult(
            su2_mult(su2_dagger(links[tuple(x_p_mu_m_nu) + (nu,)]), su2_dagger(links[tuple(x_m_nu) + (mu,)])),
            links[tuple(x_m_nu) + (nu,)]
        )
        stp = stp + s1 + s2
    return stp

def metropolis_link(links, x, mu, beta, L, eps=0.3):
    """Metropolis update with proper staple."""
    U = links[tuple(x) + (mu,)]
    stp = staple(links, x, mu, L)
    
    # Trial U_new = R · U with random R
    R = np.random.randn(4) * eps
    R[0] = 1 + R[0]*0.1
    R = R / np.linalg.norm(R)
    U_new = su2_mult(R, U)
    
    # Action change
    dS = -beta/2 * (su2_mult(U_new, stp)[0] - su2_mult(U, stp)[0])
    if dS < 0 or np.random.rand() < np.exp(-dS):
        links[tuple(x) + (mu,)] = U_new
        return 1
    return 0

def sweep(links, beta, L):
    n_acc, n_try = 0, 0
    for x in np.ndindex(L, L, L, L):
        for mu in range(4):
            n_acc += metropolis_link(links, x, mu, beta, L)
            n_try += 1
    return n_acc / n_try

def average_plaquette(links, L):
    total, n = 0.0, 0
    for x in np.ndindex(L, L, L, L):
        for mu in range(4):
            for nu in range(mu+1, 4):
                x_pm = list(x); x_pm[mu] = (x_pm[mu]+1) % L
                x_pn = list(x); x_pn[nu] = (x_pn[nu]+1) % L
                U1 = links[tuple(x) + (mu,)]
                U2 = links[tuple(x_pm) + (nu,)]
                U3 = su2_dagger(links[tuple(x_pn) + (mu,)])
                U4 = su2_dagger(links[tuple(x) + (nu,)])
                P = su2_mult(su2_mult(su2_mult(U1, U2), U3), U4)
                total += P[0]
                n += 1
    return total / n

def polyakov_loop(links, L):
    """⟨P⟩ at each spatial site, averaged."""
    total = 0.0
    n = 0
    for x in np.ndindex(L, L, L):
        # Trace product around time direction
        P = links[x + (0, 0,)].copy()  # mu=0 = time
        for t in range(1, L):
            x_t = (x[0], x[1], x[2], t)
            P = su2_mult(P, links[x_t + (0,)])
        # Polyakov loop = tr(P) = 2*P[0]
        total += 2*P[0]
        n += 1
    return total / n

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--beta", type=float, default=2.5)
    parser.add_argument("--n_configs", type=int, default=200)
    parser.add_argument("--thermalize", type=int, default=100)
    parser.add_argument("--measure_every", type=int, default=5)
    parser.add_argument("--output", default="configs_su2.npz")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    np.random.seed(args.seed)
    L = args.L
    print(f"SU(2) HMC : L={L}, β={args.beta}, configs={args.n_configs}")
    
    # Cold start
    links = np.zeros((L, L, L, L, 4, 4))
    links[..., 0] = 1.0
    
    t0 = time.time()
    print(f"\nThermalize {args.thermalize} sweeps...")
    for i in range(args.thermalize):
        acc = sweep(links, args.beta, L)
        if i % 20 == 0:
            pl = average_plaquette(links, L)
            print(f"  Sweep {i}: <P>={pl:.4f}, acc={acc:.2f}, t={time.time()-t0:.0f}s")
    
    print(f"\nMeasure {args.n_configs} configs...")
    configs = []
    plaqs = []
    polyak = []
    for i in range(args.n_configs * args.measure_every):
        sweep(links, args.beta, L)
        if i % args.measure_every == 0:
            configs.append(links.copy())
            plaqs.append(average_plaquette(links, L))
            polyak.append(polyakov_loop(links, L))
            if len(configs) % 20 == 0:
                print(f"  Config {len(configs)}: <P>={plaqs[-1]:.4f}, ⟨Poly⟩={polyak[-1]:.4f}")
    
    configs = np.array(configs)
    plaqs = np.array(plaqs)
    polyak = np.array(polyak)
    
    print(f"\nMean <P> = {plaqs.mean():.5f} ± {plaqs.std()/np.sqrt(len(plaqs)):.5f}")
    print(f"Mean ⟨Polyakov⟩ = {polyak.mean():.5f} ± {polyak.std()/np.sqrt(len(polyak)):.5f}")
    print(f"|⟨Polyakov⟩| = {abs(polyak.mean()):.5f}")
    print(f"  Expected confined β=2.5 : |⟨P⟩| ~ 0 (small)")
    
    np.savez(args.output, configs=configs, plaquettes=plaqs, polyakov=polyak,
             L=L, beta=args.beta, n_configs=len(configs))
    print(f"\n✓ Saved to {args.output} ({os.path.getsize(args.output)/1e6:.1f} MB)")
    print(f"Total time : {time.time()-t0:.0f}s")
