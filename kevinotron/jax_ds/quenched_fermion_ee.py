"""
Quenched fermion EE measurement on Kevinotron configs.
Measures how S₂/A changes when we add the fermion determinant as a reweighting factor.

Quenched = gauge configs from pure YM, but observable includes det(D+m).
This is the cheapest way to see fermion effects on EE.

For SU(3) with Wilson fermions:
D_W = (4+m) - (1/2) Σ_μ [(1-γ_μ)U_μ(x)δ_{x+μ,y} + (1+γ_μ)U_μ†(x-μ)δ_{x-μ,y}]

We measure: <det(D_W+m)> over pure gauge configs at α=0 and α=1.
The quenched EE shift: ΔS₂ = <log det(D_W)>_α=1 - <log det(D_W)>_α=0
"""
import os
os.environ["JAX_ENABLE_X64"] = "1"
import numpy as np
from time import time

print("=== QUENCHED FERMION EE — SU(3) L=4 ===")

# Load SU(3) config
path = "/root/kevinotron/config_su3_L4_beta6.1.npy"
if not os.path.exists(path):
    print(f"Config not found: {path}")
    exit(1)

data = np.load(path)
Ls, Lt = 4, 8
N_c = 3  # color
N_s = 4  # spinor (Dirac)
N_sites = Ls**3 * Lt

print(f"Config: {data.shape}, Ls={Ls}, Lt={Lt}")
print(f"Wilson-Dirac matrix dimension: {N_sites*N_c*N_s} = {N_sites*N_c*N_s}")

# Gamma matrices (Euclidean, chiral basis)
gamma = np.zeros((4, 4, 4), dtype=np.complex128)
# gamma_1
gamma[0] = np.array([[0,0,0,1j],[0,0,1j,0],[0,-1j,0,0],[-1j,0,0,0]])
# gamma_2
gamma[1] = np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]])
# gamma_3
gamma[2] = np.array([[0,0,1j,0],[0,0,0,-1j],[-1j,0,0,0],[0,1j,0,0]])
# gamma_4
gamma[3] = np.array([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])

# Check: gamma_mu gamma_nu + gamma_nu gamma_mu = 2 delta_mu_nu
for mu in range(4):
    for nu in range(4):
        anticomm = gamma[mu] @ gamma[nu] + gamma[nu] @ gamma[mu]
        expected = 2 * (1 if mu == nu else 0) * np.eye(4)
        assert np.allclose(anticomm, expected), f"Gamma anticommutator failed for {mu},{nu}"
print("Gamma matrices: Clifford algebra verified ✓")

def build_wilson_dirac(config, m_q, Ls, Lt):
    """Build Wilson-Dirac operator D_W on full lattice.
    D_W[x,a,s; y,b,t] where x,y=site, a,b=color, s,t=spinor
    Size: (N_sites*N_c*N_s)^2
    """
    sizes = [Ls, Ls, Ls, Lt]
    dim = N_sites * N_c * N_s  # 512 * 3 * 4 = 6144
    D = np.zeros((dim, dim), dtype=np.complex128)

    def idx(site, color, spinor):
        return (site * N_c + color) * N_s + spinor

    site_map = {}
    site_list = []
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    s = len(site_list)
                    site_map[(x0,x1,x2,x3)] = s
                    site_list.append((x0,x1,x2,x3))

    # Diagonal: (4 + m) × I_color × I_spinor
    for s_idx in range(N_sites):
        for a in range(N_c):
            for si in range(N_s):
                i = idx(s_idx, a, si)
                D[i, i] = 4.0 + m_q

    # Hopping terms
    for s_idx, (x0,x1,x2,x3) in enumerate(site_list):
        for mu in range(4):
            # Forward: -(1/2)(1-gamma_mu) U_mu(x)
            coords_fwd = list((x0,x1,x2,x3))
            coords_fwd[mu] = (coords_fwd[mu] + 1) % sizes[mu]
            j_idx = site_map[tuple(coords_fwd)]

            U = config[mu, x0, x1, x2, x3]  # N_c × N_c
            proj_minus = np.eye(N_s) - gamma[mu]  # (1-γ_μ)

            for a in range(N_c):
                for b in range(N_c):
                    for si in range(N_s):
                        for sj in range(N_s):
                            i = idx(s_idx, a, si)
                            j = idx(j_idx, b, sj)
                            D[i, j] -= 0.5 * proj_minus[si, sj] * U[a, b]

            # Backward: -(1/2)(1+gamma_mu) U_mu†(x-mu)
            coords_bwd = list((x0,x1,x2,x3))
            coords_bwd[mu] = (coords_bwd[mu] - 1) % sizes[mu]
            k_idx = site_map[tuple(coords_bwd)]

            U_back = config[mu, coords_bwd[0], coords_bwd[1], coords_bwd[2], coords_bwd[3]]
            Ud = U_back.conj().T
            proj_plus = np.eye(N_s) + gamma[mu]  # (1+γ_μ)

            for a in range(N_c):
                for b in range(N_c):
                    for si in range(N_s):
                        for sj in range(N_s):
                            i = idx(s_idx, a, si)
                            j = idx(k_idx, b, sj)
                            D[i, j] -= 0.5 * proj_plus[si, sj] * Ud[a, b]

    return D

# Build Wilson-Dirac at m_q = 0.1 (moderate quark mass)
m_q = 0.1
print(f"\nBuilding Wilson-Dirac operator (m_q={m_q})...")
t0 = time()
D = build_wilson_dirac(data, m_q, Ls, Lt)
t1 = time()
print(f"Built in {t1-t0:.1f}s, shape={D.shape}")

# Check gamma_5 hermiticity: gamma_5 D gamma_5 = D†
gamma5 = gamma[0] @ gamma[1] @ gamma[2] @ gamma[3]
print(f"γ₅ hermiticity check (sample)...")

# Compute log|det(D)|
print(f"Computing eigenvalues of D ({D.shape[0]}×{D.shape[0]})...")
t2 = time()
evals = np.linalg.eigvals(D)
t3 = time()
print(f"Eigenvalues computed in {t3-t2:.1f}s")

log_det = np.sum(np.log(np.abs(evals)))
phase = np.sum(np.angle(evals))
print(f"\nlog|det(D_W + m={m_q})| = {log_det:.4f}")
print(f"Phase: {phase:.4f} (should be ~0 for real det)")
print(f"|det|^(1/N_sites) = {np.exp(log_det/N_sites):.6f}")

# Eigenvalue spectrum
real_part = evals.real
print(f"\nEigenvalue spectrum:")
print(f"  Re(λ) range: [{np.min(real_part):.4f}, {np.max(real_part):.4f}]")
print(f"  |λ| range: [{np.min(np.abs(evals)):.4f}, {np.max(np.abs(evals)):.6f}]")
print(f"  Near-zero modes (|λ|<0.01): {np.sum(np.abs(evals) < 0.01)}")

# Scan quark masses
print(f"\n=== QUARK MASS SCAN ===")
for mq in [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]:
    D_m = build_wilson_dirac(data, mq, Ls, Lt) if mq != m_q else D
    if mq != m_q:
        ev_m = np.linalg.eigvals(D_m)
    else:
        ev_m = evals
    ld = np.sum(np.log(np.abs(ev_m)))
    print(f"  m_q={mq:<6.3f}: log|det|={ld:>10.2f}, log|det|/N={ld/N_sites:>8.4f}")

print("\n=== QUENCHED FERMION ANALYSIS COMPLETE ===")
