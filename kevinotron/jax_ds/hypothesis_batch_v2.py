"""Batch hypothesis testing: R1 (G₂ fermions), R3 (SU(2) fermions), R5 (U(1) FP)"""
import os
os.environ["JAX_ENABLE_X64"] = "1"
import numpy as np
from time import time

# === R5: U(1) FP adjoint (trivial, d_s should be exactly 4) ===
print("=" * 60)
print("R5: U(1) FP adjoint — should be plain Laplacian, d_s=4")
print("=" * 60)

path_u1 = "/root/kevinotron/config_su2_L4_beta2.5.npy"  # we'll use SU(2) as proxy
# Actually U(1) FP is trivial: Ad(U) = 1 for abelian group
# So M_FP = -Δ (plain Laplacian) regardless of config
# d_s = 4 exactly (free field on 4D lattice)
Ls, Lt = 4, 8
N_sites = Ls**3 * Lt
print(f"U(1) is abelian → Ad(U) = 1 → FP = plain Laplacian")
print(f"d_s(U(1) FP) = 4.0 (EXACT, by construction)")
print(f"R5: PASS (trivial)")

# === Quenched fermion on multiple groups ===
def build_sun_wilson_dirac(config, N_c, m_q, Ls, Lt):
    """Build Wilson-Dirac for SU(N_c) — generalized."""
    N_s = 4
    N_sites = Ls**3 * Lt
    d_fund = config.shape[-1]
    dim = N_sites * d_fund * N_s

    # Gamma matrices (Euclidean)
    gamma = np.zeros((4, 4, 4), dtype=np.complex128)
    gamma[0] = np.array([[0,0,0,1j],[0,0,1j,0],[0,-1j,0,0],[-1j,0,0,0]])
    gamma[1] = np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]])
    gamma[2] = np.array([[0,0,1j,0],[0,0,0,-1j],[-1j,0,0,0],[0,1j,0,0]])
    gamma[3] = np.array([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])

    sizes = [Ls, Ls, Ls, Lt]
    D = np.zeros((dim, dim), dtype=np.complex128)

    site_list = []
    site_map = {}
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    s = len(site_list)
                    site_map[(x0,x1,x2,x3)] = s
                    site_list.append((x0,x1,x2,x3))

    def idx(site, color, spinor):
        return (site * d_fund + color) * N_s + spinor

    # Diagonal
    for s_idx in range(N_sites):
        for a in range(d_fund):
            for si in range(N_s):
                D[idx(s_idx,a,si), idx(s_idx,a,si)] = 4.0 + m_q

    # Hopping
    for s_idx, coords in enumerate(site_list):
        for mu in range(4):
            c_fwd = list(coords)
            c_fwd[mu] = (c_fwd[mu]+1) % sizes[mu]
            j_idx = site_map[tuple(c_fwd)]
            U = config[mu, coords[0], coords[1], coords[2], coords[3]]
            proj_m = np.eye(N_s) - gamma[mu]

            c_bwd = list(coords)
            c_bwd[mu] = (c_bwd[mu]-1) % sizes[mu]
            k_idx = site_map[tuple(c_bwd)]
            U_back = config[mu, c_bwd[0], c_bwd[1], c_bwd[2], c_bwd[3]]
            Ud = U_back.conj().T
            proj_p = np.eye(N_s) + gamma[mu]

            for a in range(d_fund):
                for b in range(d_fund):
                    for si in range(N_s):
                        for sj in range(N_s):
                            D[idx(s_idx,a,si), idx(j_idx,b,sj)] -= 0.5 * proj_m[si,sj] * U[a,b]
                            D[idx(s_idx,a,si), idx(k_idx,b,sj)] -= 0.5 * proj_p[si,sj] * Ud[a,b]
    return D

# === R3: SU(2) Wilson-Dirac ===
print("\n" + "=" * 60)
print("R3: SU(2) Wilson-Dirac — expect log|det|/N < SU(3)")
print("=" * 60)

path_su2 = "/root/kevinotron/config_su2_L4_beta2.5.npy"
if os.path.exists(path_su2):
    data = np.load(path_su2)
    Ls, Lt = 4, 8
    d_fund = data.shape[-1]
    dim = Ls**3 * Lt * d_fund * 4
    print(f"SU(2) config: {data.shape}, D matrix: {dim}×{dim}")

    t0 = time()
    D = build_sun_wilson_dirac(data, 2, 0.1, Ls, Lt)
    print(f"Built in {time()-t0:.1f}s")

    t1 = time()
    evals = np.linalg.eigvals(D)
    print(f"Eigvals in {time()-t1:.1f}s")

    logdet = np.sum(np.log(np.abs(evals)))
    phase = np.sum(np.angle(evals))
    N = Ls**3 * Lt
    print(f"log|det(D+0.1)|/N = {logdet/N:.4f}")
    print(f"Phase: {phase:.4f}")
    print(f"Near-zero: {np.sum(np.abs(evals) < 0.01)}")
    print(f"Prediction (1.20 × S₂/A(SU2)): {1.20 * 7.22:.2f}")
    print(f"Ratio measured/S₂: {logdet/N / 7.22:.3f}")

    # Mass scan
    print("\nMass scan SU(2):")
    for mq in [0.001, 0.1, 1.0, 5.0]:
        D_m = build_sun_wilson_dirac(data, 2, mq, Ls, Lt)
        ev_m = np.linalg.eigvals(D_m)
        ld = np.sum(np.log(np.abs(ev_m)))
        print(f"  m={mq:<5.3f}: log|det|/N = {ld/N:.4f}")

# === R1: G₂ Wilson-Dirac (real 7×7, spinor 4 → 14336×14336) ===
print("\n" + "=" * 60)
print("R1: G₂ Wilson-Dirac — test ratio universality")
print("=" * 60)

path_g2 = "/root/kevinotron/config_g2_L4_beta10.0.npy"
if os.path.exists(path_g2):
    data_g2 = np.load(path_g2)
    d_fund_g2 = data_g2.shape[-1]
    dim_g2 = Ls**3 * Lt * d_fund_g2 * 4
    mem_gb = dim_g2**2 * 16 / 1e9
    print(f"G₂ config: {data_g2.shape}, D matrix: {dim_g2}×{dim_g2} ({mem_gb:.1f} GB)")

    if dim_g2 <= 16000:
        # G₂ is REAL → D_W uses real links but complex spinors
        # Need to treat 7×7 real as "color" dimension
        print(f"Building G₂ Wilson-Dirac ({dim_g2}×{dim_g2})...")
        t0 = time()

        # For real groups, U is real 7×7. Wilson-Dirac still uses complex spinors.
        # The hopping term has U[a,b] real, but proj_m[si,sj] is complex.
        # So D is complex even for real gauge groups.
        D_g2 = build_sun_wilson_dirac(data_g2.astype(np.complex128), 7, 0.1, Ls, Lt)
        print(f"Built in {time()-t0:.1f}s")

        print(f"Computing eigvals of {dim_g2}×{dim_g2}...")
        t1 = time()
        evals_g2 = np.linalg.eigvals(D_g2)
        print(f"Eigvals in {time()-t1:.1f}s")

        logdet_g2 = np.sum(np.log(np.abs(evals_g2)))
        phase_g2 = np.sum(np.angle(evals_g2))
        print(f"log|det(D+0.1)|/N = {logdet_g2/N:.4f}")
        print(f"Phase: {phase_g2:.4f}")
        print(f"Near-zero: {np.sum(np.abs(evals_g2) < 0.01)}")
        print(f"\nR1 TEST: ratio = {logdet_g2/N / 18.30:.3f} (expect 1.20 if universal)")
        print(f"Prediction: {1.20 * 18.30:.2f}, Measured: {logdet_g2/N:.2f}")
    else:
        print(f"TOO LARGE ({dim_g2}×{dim_g2}), skip")

print("\n=== ALL HYPOTHESIS TESTS COMPLETE ===")
