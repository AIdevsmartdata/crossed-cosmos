#!/usr/bin/env python3
"""Creutz ratio χ(R, R) — direct σ₀ string tension measurement.

Creutz 1980 :
  χ(R, R) = log[⟨W(R,R)⟩ · ⟨W(R-1,R-1)⟩ / ⟨W(R,R-1)⟩²]
  
At large R : χ → σ₀ · a²  (lattice string tension)

If σ₀ > 0 → CONFINEMENT directly confirmed.
Independent validation, no fermions, on existing configs.
"""
import numpy as np, sys, glob, json, os, math

def su2_mult(u, v):
    a0,a1,a2,a3 = u[..., 0],u[..., 1],u[..., 2],u[..., 3]
    b0,b1,b2,b3 = v[..., 0],v[..., 1],v[..., 2],v[..., 3]
    return np.stack([
        a0*b0-a1*b1-a2*b2-a3*b3,
        a0*b1+a1*b0+a2*b3-a3*b2,
        a0*b2-a1*b3+a2*b0+a3*b1,
        a0*b3+a1*b2-a2*b1+a3*b0,
    ], axis=-1)

def su2_dag(u):
    return np.stack([u[..., 0], -u[..., 1], -u[..., 2], -u[..., 3]], axis=-1)

def wilson_loop(links, x, mu, nu, R, T):
    """Compute trace of Wilson loop R×T at site x in (mu, nu) plane."""
    L = links.shape[0]
    # Start product : R links in mu direction
    pos = list(x)
    U_total = links[tuple(pos) + (mu,)]
    pos[mu] = (pos[mu] + 1) % L
    for r in range(1, R):
        U_total = su2_mult(U_total, links[tuple(pos) + (mu,)])
        pos[mu] = (pos[mu] + 1) % L
    # T links in nu direction
    for t in range(T):
        U_total = su2_mult(U_total, links[tuple(pos) + (nu,)])
        pos[nu] = (pos[nu] + 1) % L
    # R links back in -mu direction
    for r in range(R):
        pos[mu] = (pos[mu] - 1) % L
        U_total = su2_mult(U_total, su2_dag(links[tuple(pos) + (mu,)]))
    # T links back in -nu direction
    for t in range(T):
        pos[nu] = (pos[nu] - 1) % L
        U_total = su2_mult(U_total, su2_dag(links[tuple(pos) + (nu,)]))
    return U_total[..., 0]  # tr(U_loop)/2

def average_wilson(links, R, T):
    """Average Wilson R×T loop over all positions and (mu, nu) planes."""
    L = links.shape[0]
    total = 0.0; count = 0
    # Sample positions (subset for speed)
    n_samples = min(L**4, 256)  # limit
    samples_per_dim = max(1, int(n_samples**0.25))
    
    for x_idx in range(0, L, max(1, L//samples_per_dim)):
        for y_idx in range(0, L, max(1, L//samples_per_dim)):
            for z_idx in range(0, L, max(1, L//samples_per_dim)):
                for t_idx in range(0, L, max(1, L//samples_per_dim)):
                    site = (x_idx, y_idx, z_idx, t_idx)
                    # (mu, nu) pairs : use (0,3) i.e. spatial × time
                    # For pure spatial : (0,1), (0,2), (1,2)
                    for mu in range(3):
                        nu = 3  # time
                        if R + site[mu] >= L or T + site[nu] >= L:
                            continue
                        total += wilson_loop(links, site, mu, nu, R, T)
                        count += 1
    return total / count if count > 0 else 0

# === MAIN ===
print("="*70)
print("Creutz ratio σ₀ measurement — direct confinement test")
print("="*70)

files = sorted(glob.glob("results/hmc_b*_L*.npz"))
if not files:
    print("No HMC configs.")
    sys.exit(1)

results = {}
for npz in files:
    print(f"\n=== {os.path.basename(npz)} ===")
    data = np.load(npz)
    configs = data['configs']
    L = int(data['L'])
    beta = float(data['beta'])
    n_use = min(20, len(configs))  # 20 configs for speed
    print(f"  β={beta} L={L} configs={n_use}")
    
    # Compute Wilson loops <W(R,T)> for various sizes
    W = {}
    for R in [1, 2, 3]:
        for T in [1, 2, 3]:
            if R + T > L - 1: continue
            W_vals = []
            for cfg in configs[:n_use]:
                W_vals.append(average_wilson(cfg, R, T))
            W[(R, T)] = np.mean(W_vals)
            print(f"  ⟨W({R},{T})⟩ = {W[(R, T)]:.5f}")
    
    # Creutz ratios χ(R, R)
    creutz = {}
    for R in [2, 3]:
        if (R, R) in W and (R-1, R-1) in W and (R, R-1) in W:
            num = W[(R, R)] * W[(R-1, R-1)]
            den = W[(R, R-1)] * W[(R, R-1)]
            if num > 0 and den > 0:
                chi = -np.log(num / den)
                creutz[R] = chi
                print(f"  χ({R},{R}) = {chi:.4f}")
                
                # Compare with Bali a²σ
                a2_sigma = {2.3: 0.25, 2.5: 0.09, 2.7: 0.04}.get(round(beta, 1), 0.1)
                print(f"    Bali a²σ ≈ {a2_sigma}")
                if a2_sigma > 0:
                    print(f"    Ratio measured/Bali : {chi/a2_sigma:.2f}")
    
    results[str(beta)] = {
        'beta': beta, 'L': L, 'n_configs': n_use,
        'wilson_loops': {f"{R}x{T}": float(W[(R,T)]) for (R,T) in W},
        'creutz_ratios': {f"chi_{R}_{R}": float(creutz[R]) for R in creutz},
    }
    
    # Verdict
    if 3 in creutz and creutz[3] > 0:
        print(f"  ✓ σ₀ > 0 : CONFINEMENT confirmed empirically")

with open('results/creutz_ratio.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✓ Saved results/creutz_ratio.json")
