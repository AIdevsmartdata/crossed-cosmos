#!/usr/bin/env python3
"""Direct glueball mass m(0++) via Wilson loop correlator.

C(t) = ⟨W(0)·W(t)⟩_c où W = plaquette spatiale (smeared)
At large t : C(t) ~ exp(-m·t)
Extract m via effective mass m_eff(t) = log(C(t)/C(t+1))

NO FERMIONS — direct on existing HMC configs.
Standard lattice QCD glueball measurement.
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

def plaquette_at(links, x, mu, nu):
    """Compute single plaquette tr(U_p)/2 at site x in (mu, nu) plane."""
    L = links.shape[0]
    x_pm = list(x); x_pm[mu] = (x_pm[mu]+1) % L
    x_pn = list(x); x_pn[nu] = (x_pn[nu]+1) % L
    U1 = links[tuple(x) + (mu,)]
    U2 = links[tuple(x_pm) + (nu,)]
    U3 = su2_dag(links[tuple(x_pn) + (mu,)])
    U4 = su2_dag(links[tuple(x) + (nu,)])
    P = su2_mult(su2_mult(su2_mult(U1, U2), U3), U4)
    return P[..., 0]  # tr/2

def spatial_plaquette_correlator(configs, t_max=4):
    """Compute C(t) = ⟨W̄(0)·W̄(t)⟩_c where W̄ is averaged spatial plaq.
    
    W̄(t) = (1/V_spatial) Σ_(x,y,z) Σ_(i<j: spatial) tr(U_p(x,y,z,t))/2
    """
    n_configs = len(configs)
    L = configs[0].shape[0]
    
    # For each config, for each time slice, average spatial plaquette
    W_all = np.zeros((n_configs, L))  # W̄ at each time
    
    for c_idx, links in enumerate(configs):
        for t in range(L):
            total = 0.0; count = 0
            # Spatial plaquettes only : i, j in {0, 1, 2} (NOT t=3)
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        site = (x, y, z, t)
                        # Spatial plaquette (0,1), (0,2), (1,2)
                        for mu in range(3):
                            for nu in range(mu+1, 3):
                                total += plaquette_at(links, site, mu, nu)
                                count += 1
            W_all[c_idx, t] = total / count if count > 0 else 0
        if (c_idx+1) % 20 == 0:
            print(f"  Config {c_idx+1}/{n_configs}...")
    
    # Compute connected correlator : ⟨W(0)·W(t)⟩ - ⟨W⟩²
    W_mean = W_all.mean()
    C_t = np.zeros(L)
    for t in range(L):
        # Average over (s, s+t) pairs with periodic time
        prods = []
        for s in range(L):
            tau = (s + t) % L
            prods.extend(W_all[:, s] * W_all[:, tau])
        C_t[t] = np.mean(prods) - W_mean**2
    
    return C_t, W_all

def effective_mass(C_t):
    """m_eff(t) = log(C(t) / C(t+1))"""
    L = len(C_t)
    m_eff = np.zeros(L-1)
    for t in range(L-1):
        if C_t[t] > 0 and C_t[t+1] > 0:
            m_eff[t] = np.log(C_t[t] / C_t[t+1])
        else:
            m_eff[t] = np.nan
    return m_eff

# === MAIN ===
print("="*70)
print("Glueball 0++ mass via Wilson loop correlator")
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
    
    # Use up to 50 configs for speed
    n_use = min(50, len(configs))
    print(f"  β={beta} L={L} configs={n_use}")
    
    C_t, W_all = spatial_plaquette_correlator(configs[:n_use], t_max=L//2)
    
    print(f"  Plaquette mean : {W_all.mean():.4f}")
    print(f"  C(0) = {C_t[0]:.6f}")
    print(f"  C(1) = {C_t[1]:.6f}")
    print(f"  C(2) = {C_t[2]:.6f}")
    print(f"  C(3) = {C_t[3]:.6f}")
    
    m_eff = effective_mass(C_t)
    print(f"  m_eff(t) :")
    for t in range(min(4, len(m_eff))):
        print(f"    t={t} : {m_eff[t]:.4f}")
    
    # Best estimate of glueball mass : asymptotic m_eff
    valid_m = m_eff[~np.isnan(m_eff)]
    if len(valid_m) >= 2:
        m_gb = valid_m[1] if not np.isnan(valid_m[1]) else valid_m[0]
        print(f"  Estimate m(0++) lattice : {m_gb:.4f}")
        
        # Convert to physical via Bali a√σ
        a_sigma = {2.3: 0.5, 2.5: 0.3, 2.7: 0.2}.get(round(beta, 1), 0.3)
        m_over_sqrt_sigma = m_gb / a_sigma
        print(f"  m(0++)/√σ ≈ {m_over_sqrt_sigma:.3f}")
        print(f"  Framework predict SU(2) 0++ : 3.92")
        print(f"  Lucini-Teper 2001 : 3.78")
    
    results[str(beta)] = {
        'beta': beta, 'L': L, 'n_configs': n_use,
        'C_t': C_t.tolist(),
        'm_eff': [float(m) if not np.isnan(m) else None for m in m_eff],
        'plaq_mean': float(W_all.mean()),
    }

with open('results/glueball_correlator.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✓ Saved results/glueball_correlator.json")
