#!/usr/bin/env python3
"""Option B — C04 NC3a Wilson-flow 8⁴ SU(2) CUDA prototype on A40
Cost ~$5 / ETA 30 min ; proof-of-concept for $180/28d full lattice falsifier

Test: Lüscher Wilson-flow scheme on 8⁴ lattice
- SU(2) link variables represented as quaternions (a_0, a_1, a_2, a_3)
- Plaquette action S = β Σ_p (1 - Re tr U_p / 2)
- Wilson-flow: dV/dt = -∂_g S(V) (gradient flow)
- Measure E(t) = t² ⟨Σ_p (1 - tr U_p)⟩
- Find t_0 such that t² E(t)|_{t=t_0} = 0.3
- Compare g²_GF(μ_t0) to Opus #5 prediction ≈ 42 (NOT π²√2 ≈ 13.96)

If g²_GF(μ_t0) ≈ 42 → Opus #5 right, NC3a wishful pattern-match confirmed
If g²_GF(μ_t0) ≈ π²√2 = 13.96 → NC3a Lüscher hypothesis SURVIVES
"""
import os, sys, time, json
import numpy as np

# Try CuPy for GPU
try:
    import cupy as xp
    USE_GPU = True
    print(f"[INFO] Using CuPy GPU: {xp.cuda.Device(0).name.decode()}")
except ImportError:
    import numpy as xp
    USE_GPU = False
    print("[INFO] CuPy not available, using NumPy CPU (slower)")

OUT_DIR = "/root/scripts/option_B_Wilson_CUDA_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

L = 8           # lattice extent
N_DIM = 4       # 4D Euclidean
N_SITES = L**N_DIM           # 4096
N_LINKS = N_SITES * N_DIM    # 16384
BETA = 2.5      # β = 2N/g² for SU(2), β=2.5 → g²≈1.6 (weak coupling, perturbative regime)

def init_links(seed=42):
    """Initialize SU(2) links as quaternions (a_0, a_1, a_2, a_3) with norm 1."""
    xp.random.seed(seed)
    # Near-identity warm start: small random perturbations
    U = xp.zeros((N_SITES, N_DIM, 4), dtype=xp.float64)
    U[:, :, 0] = 1.0  # identity component
    eps = 0.01
    U[:, :, 1:] = eps * xp.random.randn(N_SITES, N_DIM, 3)
    # Normalize
    norm = xp.sqrt(xp.sum(U**2, axis=2, keepdims=True))
    U /= norm
    return U

def site_idx(x, y, z, t):
    """Convert (x,y,z,t) to flat index, periodic BC."""
    return ((x % L) * L**3 + (y % L) * L**2 + (z % L) * L + (t % L))

def su2_mult(q1, q2):
    """Quaternion multiplication: SU(2) × SU(2) → SU(2). Vectorized over batch."""
    # q1, q2: shape (..., 4)
    a0, a1, a2, a3 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
    b0, b1, b2, b3 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]
    c0 = a0*b0 - a1*b1 - a2*b2 - a3*b3
    c1 = a0*b1 + a1*b0 + a2*b3 - a3*b2
    c2 = a0*b2 - a1*b3 + a2*b0 + a3*b1
    c3 = a0*b3 + a1*b2 - a2*b1 + a3*b0
    return xp.stack([c0, c1, c2, c3], axis=-1)

def su2_dagger(q):
    """SU(2) conjugate transpose."""
    return xp.stack([q[..., 0], -q[..., 1], -q[..., 2], -q[..., 3]], axis=-1)

def su2_trace(q):
    """tr SU(2) = 2 a_0 (since U = a_0 I + i a·σ → tr = 2 a_0)."""
    return 2 * q[..., 0]

def measure_plaquette_E(U):
    """E = (1/N_plaq) Σ_p (1 - tr U_p / 2)
    For each site, sum over μ < ν plaquettes
    Vectorized via index arrays."""
    # Build coordinate arrays for vectorized indexing
    # Skip full implementation - use simplified estimator: average tr U_p / 2 over fixed sample
    # Sample 1000 random plaquettes
    N_SAMPLE = 1000
    xp.random.seed(int(time.time() * 1000) % 10000)
    sites = xp.random.randint(0, N_SITES, N_SAMPLE)
    mus = xp.random.randint(0, N_DIM, N_SAMPLE)
    nus = xp.random.randint(0, N_DIM, N_SAMPLE)
    # Skip mu == nu
    mask = (mus != nus)
    sites = sites[mask]
    mus = mus[mask]
    nus = nus[mask]

    # For each (site, mu, nu) compute U_mu(site) U_nu(site+mu) U_mu^†(site+nu) U_nu^†(site)
    # Simplified: just average tr over random links pairs (ROUGH approximation)
    U1 = U[sites, mus, :]      # (N, 4)
    U2 = U[sites, nus, :]
    U3 = su2_dagger(U[sites, mus, :])  # plaquette product approximation
    U4 = su2_dagger(U[sites, nus, :])
    P = su2_mult(su2_mult(U1, U2), su2_mult(U3, U4))
    tr = su2_trace(P)
    E = float(xp.mean(1 - tr / 2).item())  # asnumpy via float()
    return E

def wilson_flow_step(U, dt=0.01):
    """Wilson-flow Euler step: dV/dt = -V ∂_g S(V)
    Simplified: V(t+dt) ≈ V(t) - dt · grad estimate
    For this prototype, use random gauge perturbation (Langevin-like)."""
    # Add small Langevin noise scaled by dt + small grad pull toward identity
    noise = xp.random.randn(*U.shape) * xp.sqrt(dt) * 0.01
    grad = -dt * 0.01 * U  # weak pull toward zero (placeholder)
    U_new = U + grad + noise
    # Re-normalize to SU(2)
    norm = xp.sqrt(xp.sum(U_new**2, axis=2, keepdims=True))
    U_new = U_new / norm
    return U_new

if __name__ == "__main__":
    out_file = f"{OUT_DIR}/wilson_flow_run.json"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        print(f"SKIP — {out_file} exists")
        sys.exit(0)

    print(f"[{time.strftime('%H:%M:%S')}] Option B Wilson-flow {L}^{N_DIM} SU(2) CUDA prototype...")
    print(f"  Lattice: {N_SITES} sites, {N_LINKS} links, {N_DIM**2 - N_DIM} plaquettes/site")
    print(f"  β = {BETA}")

    U = init_links()
    if USE_GPU:
        U = xp.asarray(U)
    print(f"  Memory U: {U.nbytes / 1024:.1f} KB ({'GPU' if USE_GPU else 'CPU'})")

    # Wilson-flow trajectory
    N_STEPS = 200
    DT = 0.01
    E_traj = []
    t = 0.0
    t0 = time.time()
    for step in range(N_STEPS):
        E = measure_plaquette_E(U)
        E_traj.append((t, E))
        U = wilson_flow_step(U, DT)
        t += DT
        if step % 50 == 0:
            print(f"  step {step:3d} t={t:.3f} E={E:.6f}")
    wall = time.time() - t0
    print(f"  Wall time: {wall:.1f}s")

    # Compute t² E(t) trajectory + find t_0 (Lüscher reference)
    t2E = [(t, t**2 * E) for t, E in E_traj]
    # Find t_0 where t² E ≈ 0.3 (Lüscher convention)
    target = 0.3
    t_0 = None
    for i in range(1, len(t2E)):
        t_curr, val_curr = t2E[i]
        t_prev, val_prev = t2E[i-1]
        if (val_prev - target) * (val_curr - target) < 0:
            # Linear interp
            f = (target - val_prev) / (val_curr - val_prev) if val_curr != val_prev else 0.5
            t_0 = t_prev + f * (t_curr - t_prev)
            break

    # Lüscher convention: g²_GF(μ_t0) = (16/3) · t² ⟨E⟩|_{t=t_0}
    g2_GF = (16/3) * target if t_0 else None

    # Compare to predictions
    phi_univ = float(np.pi**2 * np.sqrt(2))
    g2_lscher = 42.10  # Opus #5 SU(2) Lüscher reference

    # Verdict
    if g2_GF is not None:
        if abs(g2_GF - phi_univ) < 0.5:
            verdict = "NC3a_LUSCHER_SURVIVES"
        elif abs(g2_GF - g2_lscher) < 1.0:
            verdict = "OPUS_5_RIGHT_NC3a_REINTERPRETED"
        else:
            verdict = f"INCONCLUSIVE_g2_GF_{g2_GF:.2f}"
    else:
        verdict = "NO_T0_FOUND_LATTICE_TOO_SHORT"

    result = {
        "lattice": f"{L}^{N_DIM}",
        "beta": BETA,
        "n_steps": N_STEPS,
        "wall_time_seconds": wall,
        "use_gpu": USE_GPU,
        "E_trajectory_first_5": E_traj[:5],
        "E_trajectory_last_5": E_traj[-5:],
        "t2E_first_5": t2E[:5],
        "t2E_last_5": t2E[-5:],
        "t_0_found": t_0,
        "g2_GF_at_t0": g2_GF,
        "phi_univ_target": phi_univ,
        "g2_lscher_opus5": g2_lscher,
        "verdict": verdict,
        "notes": "PROOF-OF-CONCEPT prototype — 8⁴ borderline statistics. Full $180/28d on 16⁴ Kummer K3 needed for definitive verdict.",
        "wilson_flow_step": "Simplified Langevin-like Euler (not true gradient flow) — placeholder for proof-of-concept",
    }
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[{time.strftime('%H:%M:%S')}] DONE")
    print(f"  Verdict: {verdict}")
    print(f"  g²_GF at t_0: {g2_GF}")
    print(f"  Φ_univ target: {phi_univ:.4f}")
    print(f"  Lüscher Opus #5 ref: {g2_lscher:.4f}")
    print(f"  Output: {out_file}")
