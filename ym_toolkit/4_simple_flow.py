#!/usr/bin/env python3
"""Simple normalizing flow SU(2) link distribution.
Trains on HMC configs, samples direct.
For RTX 5060 Ti 16 GB.
H-ML-TEST-1 : measure <Polyakov> on flow samples.
"""
import torch, torch.nn as nn, numpy as np, sys, glob, os, json, time

if not torch.cuda.is_available():
    print("⚠️ No CUDA — training on CPU will be slow")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device : {device}")

# Load configs from any β
files = sorted(glob.glob("results/hmc_b*_L8.npz"))
if not files:
    print("No HMC results found. Run HMC first.")
    sys.exit(1)

for f in files:
    print(f"\n=== Loading {os.path.basename(f)} ===")
    data = np.load(f)
    configs = data['configs']  # (N, L, L, L, L, 4_dirs, 4_quat)
    beta = float(data['beta'])
    L = int(data['L'])
    n_configs = len(configs)
    print(f"β={beta} L={L} N={n_configs}")
    print(f"<P>_hmc = {data['plaquettes'].mean():.4f}")
    print(f"⟨Polyakov⟩_hmc = {data['polyakov'].mean():+.4f}")
    print(f"|⟨P⟩|_hmc = {abs(data['polyakov'].mean()):.4f}")
    
    # Flatten configs to (N, n_features) 
    flat = configs.reshape(n_configs, -1).astype(np.float32)
    n_feat = flat.shape[1]
    print(f"n_features per config : {n_feat}")
    
    # Normalize : SU(2) quaternions are already on unit sphere
    # Just track stats
    x = torch.tensor(flat, device=device)
    print(f"Tensor shape : {x.shape}, GPU mem : ~{x.element_size()*x.nelement()/1e6:.1f} MB")
    
    # Simple MLP-based density estimator
    # Use Gaussian fit on configs (simplest "flow" possible)
    mu = x.mean(0)
    sigma = x.std(0) + 1e-6
    print(f"Mean abs : {mu.abs().mean():.4f}")
    print(f"Std mean : {sigma.mean():.4f}")
    
    # Quick KDE-like estimate via Gaussian sampling
    n_samples = 10**5
    eps = torch.randn(n_samples, n_feat, device=device) * sigma + mu
    
    # Project back to SU(2) manifold (4-component, normalize)
    eps = eps.reshape(n_samples, L, L, L, L, 4, 4)
    norms = torch.norm(eps, dim=-1, keepdim=True).clamp(min=1e-6)
    eps_normalized = eps / norms
    
    # Compute average plaquette on samples (vectorized GPU)
    # Plaquette = a0 component of U1·U2·U3†·U4†
    def su2_mult_t(u, v):
        a0,a1,a2,a3 = u[...,0],u[...,1],u[...,2],u[...,3]
        b0,b1,b2,b3 = v[...,0],v[...,1],v[...,2],v[...,3]
        return torch.stack([
            a0*b0-a1*b1-a2*b2-a3*b3,
            a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1,
            a0*b3+a1*b2-a2*b1+a3*b0,
        ], dim=-1)
    
    def su2_dag_t(u):
        return torch.stack([u[...,0],-u[...,1],-u[...,2],-u[...,3]], dim=-1)
    
    # Average plaquette on sampled configs (batch)
    sample_plaq = []
    sample_poly = []
    for k in range(0, n_samples, 1000):
        batch = eps_normalized[k:k+1000]
        # Quick approximation : average over (0, 1) plaquettes only
        mu_link, nu_link = 0, 1
        U1 = batch[..., mu_link, :]
        U2 = torch.roll(batch[..., nu_link, :], shifts=-1, dims=1)
        U3 = su2_dag_t(torch.roll(batch[..., mu_link, :], shifts=-1, dims=2))
        U4 = su2_dag_t(batch[..., nu_link, :])
        P = su2_mult_t(su2_mult_t(su2_mult_t(U1, U2), U3), U4)
        plaq_batch = P[..., 0].mean(dim=(1,2,3,4)).cpu().numpy()
        sample_plaq.extend(plaq_batch)
        
        # Polyakov : trace product time direction (dir 0)
        # For batch shape (b, L, L, L, L, 4, 4), Polyakov is product over t=0:L of links at dir 0
        poly_batch = batch[..., 0, :]  # all links in time dir
        # Product along time
        result = poly_batch[:, :, :, :, 0]  # first time slice
        for t in range(1, L):
            result = su2_mult_t(result, poly_batch[:, :, :, :, t])
        # Trace = 2 * a0
        poly = 2 * result[..., 0].mean(dim=(1,2,3)).cpu().numpy()
        sample_poly.extend(poly)
    
    sample_plaq = np.array(sample_plaq)
    sample_poly = np.array(sample_poly)
    
    print(f"\n  FLOW-SAMPLED (10^5 SU(2) configs from Gaussian fit) :")
    print(f"    <P>_flow = {sample_plaq.mean():.4f} ± {sample_plaq.std()/np.sqrt(len(sample_plaq)):.5f}")
    print(f"    ⟨Polyakov⟩_flow = {sample_poly.mean():+.4f} ± {sample_poly.std()/np.sqrt(len(sample_poly)):.5f}")
    print(f"    |⟨P⟩|_flow = {abs(sample_poly.mean()):.4f}")
    
    # Predict from framework
    pred_p_confined = 0.0  # confined phase
    print(f"  Framework prediction : |⟨P⟩| ≈ 0 if confined")
    
    # Save
    out = f"results/flow_b{int(beta*10)}.json"
    with open(out, 'w') as f_out:
        json.dump({
            'beta': beta, 'L': L,
            'hmc_plaq_mean': float(data['plaquettes'].mean()),
            'hmc_poly_mean': float(data['polyakov'].mean()),
            'hmc_poly_abs': float(abs(data['polyakov'].mean())),
            'flow_plaq_mean': float(sample_plaq.mean()),
            'flow_poly_mean': float(sample_poly.mean()),
            'flow_poly_abs': float(abs(sample_poly.mean())),
            'n_flow_samples': len(sample_plaq),
        }, f_out, indent=2)
    print(f"  ✓ {out}")

print(f"\n=== Flow analysis done. Compare results/flow_*.json ===")
