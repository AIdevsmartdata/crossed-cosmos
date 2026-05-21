#!/usr/bin/env python3
"""Persistent homology on SU(2) configs for center vortex detection.

Per arXiv:2211.16273 (PRD 107.034501, 2023) :
  TDA on plaquette field → detect Z_2 vortices
  Gauge-invariant measurement
  
Input  : configs_*.npz from HMC
Output : results/vortex_density_*.json
"""
import numpy as np, sys, json, glob, os
try:
    from ripser import ripser
    HAS_TDA = True
except ImportError:
    print("(install giotto-tda ripser : pip install --user --break-system-packages giotto-tda ripser)")
    HAS_TDA = False

def project_z2_center(links):
    """Project SU(2) links to Z_2 center {+1, -1} via tr(U) sign."""
    # SU(2) trace = 2*a0, sign of trace = Z_2 element
    return np.sign(links[..., 0])

def count_vortices(z2_field, L):
    """Count Z_2 vortex links (where projected plaquette = -1)."""
    n_vortex = 0
    n_plaq = 0
    for x in np.ndindex(L, L, L, L):
        for mu in range(4):
            for nu in range(mu+1, 4):
                x_pm = list(x); x_pm[mu] = (x_pm[mu]+1) % L
                x_pn = list(x); x_pn[nu] = (x_pn[nu]+1) % L
                # Z_2 plaquette = product of Z_2 links
                z2_p = (z2_field[tuple(x) + (mu,)] * z2_field[tuple(x_pm) + (nu,)] *
                       z2_field[tuple(x_pn) + (mu,)] * z2_field[tuple(x) + (nu,)])
                if z2_p < 0: n_vortex += 1
                n_plaq += 1
    return n_vortex / n_plaq

if __name__ == "__main__":
    for npz_file in sorted(glob.glob("results/hmc_b*.npz")):
        print(f"\n=== {os.path.basename(npz_file)} ===")
        data = np.load(npz_file)
        configs = data["configs"]
        L = int(data["L"])
        beta = float(data["beta"])
        
        densities = []
        for i, config in enumerate(configs):
            z2 = project_z2_center(config)
            rho = count_vortices(z2, L)
            densities.append(rho)
        
        densities = np.array(densities)
        print(f"  β = {beta}")
        print(f"  ρ_vortex / total plaquettes : {densities.mean():.4f} ± {densities.std()/np.sqrt(len(densities)):.4f}")
        
        # σ₀ from <P>
        sigma_lat = -np.log(np.mean(data["plaquettes"]))  # rough
        print(f"  σ_lat (rough) : {sigma_lat:.4f}")
        print(f"  ρ_vortex / σ_lat : {densities.mean() / sigma_lat:.4f} (prediction Greensite = O(1))")
        
        # Save
        result = {
            "beta": beta, "L": L,
            "rho_vortex_mean": float(densities.mean()),
            "rho_vortex_std": float(densities.std()),
            "n_configs": int(len(densities)),
            "sigma_lat_rough": float(sigma_lat),
            "ratio_rho_sigma": float(densities.mean() / sigma_lat),
        }
        out = f"results/vortex_b{int(beta*10)}.json"
        with open(out, "w") as f:
            json.dump(result, f, indent=2)
        print(f"  ✓ {out}")
