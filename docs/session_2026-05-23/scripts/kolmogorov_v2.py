#!/usr/bin/env python3
"""Test Kolmogorov consistency Conjecture C* (Opus Einstein) v2.

Uses validated CuPy HMC engine su2_hmc_v3.SU2HMC.

Test : at fixed true 't Hooft beta=10, compare
  mu_block = block-spin(mu_fine)  vs  mu_coarse_direct

If C_LSI(block) ~ C_LSI(coarse) <5% -> support Conjecture C*.
"""
import sys, os, time, json
import numpy as np
import cupy as cp

sys.path.insert(0, os.path.expanduser("~/.openclaw/workspaces/vast"))
from su2_hmc_v3 import SU2HMC, random_su2, su2_mul, su2_dagger, project_su2


def block_spin_links(U_fine_flat, L_fine, ndim=4):
    """Block-spin 2:1 in all directions. Multiply pairs of fine links along path."""
    L_coarse = L_fine // 2
    V_fine = L_fine ** ndim
    V_coarse = L_coarse ** ndim

    def fine_idx(x0, x1, x2, x3):
        return ((x0 * L_fine + x1) * L_fine + x2) * L_fine + x3

    def coarse_idx(X0, X1, X2, X3):
        return ((X0 * L_coarse + X1) * L_coarse + X2) * L_coarse + X3

    U_coarse = cp.zeros((ndim * V_coarse, 2, 2), dtype=U_fine_flat.dtype)

    for mu in range(ndim):
        for X0 in range(L_coarse):
            for X1 in range(L_coarse):
                for X2 in range(L_coarse):
                    for X3 in range(L_coarse):
                        x0, x1, x2, x3 = 2*X0, 2*X1, 2*X2, 2*X3
                        f1 = fine_idx(x0, x1, x2, x3)
                        xs = [x0, x1, x2, x3]
                        xs[mu] = (xs[mu] + 1) % L_fine
                        f2 = fine_idx(xs[0], xs[1], xs[2], xs[3])
                        U1 = U_fine_flat[mu * V_fine + f1]
                        U2 = U_fine_flat[mu * V_fine + f2]
                        Uprod = su2_mul(U1[None, ...], U2[None, ...])[0]
                        Uprod = project_su2(Uprod)
                        c_site = coarse_idx(X0, X1, X2, X3)
                        U_coarse[mu * V_coarse + c_site] = Uprod
    return U_coarse


def compute_plaquette_field_4D(hmc):
    """Return per-site plaquette mean (averaged over 6 mu<nu pairs)."""
    L = hmc.L
    V = hmc.volume
    ndim = hmc.ndim
    sites = cp.arange(V, dtype=cp.int32)
    P_field = cp.zeros(V, dtype=cp.float32)
    n_pairs = 0
    for mu in range(ndim):
        for nu in range(mu+1, ndim):
            x_mu = hmc.nbr[mu, 0, sites]
            x_nu = hmc.nbr[nu, 0, sites]
            P = su2_mul(hmc.U[mu*V + sites], hmc.U[nu*V + x_mu])
            P = su2_mul(P, su2_dagger(hmc.U[mu*V + x_nu]))
            P = su2_mul(P, su2_dagger(hmc.U[nu*V + sites]))
            P_field += 0.5 * (P[..., 0, 0].real + P[..., 1, 1].real)
            n_pairs += 1
    P_field /= n_pairs
    return cp.asnumpy(P_field).reshape((L,)*ndim)


def C_LSI_proper(P_all):
    P_all = np.asarray(P_all)
    mean_P = np.mean(P_all)
    f = (P_all - mean_P) ** 2
    f2 = f.flatten() ** 2 + 1e-12
    E_f2 = np.mean(f2)
    ent = np.mean(f2 * np.log(f2)) - E_f2 * np.log(E_f2)
    grad_sq = 0.0
    for axis in range(1, P_all.ndim):
        f_shift = np.roll(f, -1, axis=axis)
        grad_sq += np.mean((f_shift - f) ** 2)
    return float(ent / (2 * grad_sq)) if grad_sq > 0 else None


def run_hmc_and_measure(L, beta, n_therm, n_meas, n_steps=30, tau=1.0,
                         do_blockspin=False, seed_offset=0):
    cp.random.seed(2026 + seed_offset)
    hmc = SU2HMC(L, beta, nsteps=n_steps, tau=tau)
    t0 = time.time()
    print(f"  Therm L={L} beta={beta} ({n_therm} traj)...", flush=True)
    acc = 0
    for i in range(n_therm):
        a, dH, p = hmc.hmc_step()
        if a: acc += 1
    print(f"    therm done {time.time()-t0:.0f}s P_avg={hmc.compute_plaquette():.4f} acc={acc/n_therm:.2f}", flush=True)
    P_fields = []
    P_block_fields = []
    t1 = time.time()
    for i in range(n_meas):
        for _ in range(3):
            hmc.hmc_step()
        P_fields.append(compute_plaquette_field_4D(hmc))
        if do_blockspin:
            U_coarse = block_spin_links(hmc.U, L)
            L_c = L // 2
            hmc_c = SU2HMC(L_c, beta, nsteps=n_steps, tau=tau)
            hmc_c.U = U_coarse
            P_block_fields.append(compute_plaquette_field_4D(hmc_c))
        if (i+1) % 5 == 0:
            extra = f" P_block_avg={float(np.mean(P_block_fields[-1])):.4f}" if do_blockspin else ""
            print(f"    meas {i+1}/{n_meas}: P_avg={float(np.mean(P_fields[-1])):.4f}{extra} t={time.time()-t1:.0f}s", flush=True)
    return P_fields, P_block_fields


def main():
    BETA = 10.0
    n_therm = 200
    n_meas = 30

    print("="*78)
    print("TEST KOLMOGOROV CONSISTENCY (Conjecture C* Opus Einstein) v2")
    print("PC gamer RTX 5060 Ti - CuPy validated HMC")
    print("="*78)

    results = {"beta": BETA, "n_meas": n_meas, "pairs": []}

    print(f"\n=== PAIRE 1 : L_fine=8 -> L_coarse=4 ===", flush=True)

    print("\n[1/2] HMC fine L=8 beta=10 + block-spin", flush=True)
    P_fine, P_block = run_hmc_and_measure(8, BETA, n_therm, n_meas,
                                            do_blockspin=True, seed_offset=10)

    print("\n[2/2] HMC direct coarse L=4 beta=10", flush=True)
    P_coarse, _ = run_hmc_and_measure(4, BETA, n_therm, n_meas,
                                        do_blockspin=False, seed_offset=20)

    P_fine_arr = np.array([np.asarray(p) for p in P_fine])
    P_block_arr = np.array([np.asarray(p) for p in P_block])
    P_coarse_arr = np.array([np.asarray(p) for p in P_coarse])

    C_lsi_fine = C_LSI_proper(P_fine_arr)
    C_lsi_block = C_LSI_proper(P_block_arr)
    C_lsi_coarse = C_LSI_proper(P_coarse_arr)
    mean_P_fine = float(np.mean(P_fine_arr))
    mean_P_block = float(np.mean(P_block_arr))
    mean_P_coarse = float(np.mean(P_coarse_arr))
    var_P_block = float(np.var(P_block_arr))
    var_P_coarse = float(np.var(P_coarse_arr))

    delta_clsi = abs(C_lsi_block - C_lsi_coarse) / C_lsi_coarse * 100
    delta_meanP = abs(mean_P_block - mean_P_coarse) / mean_P_coarse * 100
    delta_varP = abs(var_P_block - var_P_coarse) / var_P_coarse * 100

    pair = {
        "L_fine": 8, "L_coarse": 4, "beta": BETA, "n_meas": n_meas,
        "C_LSI_fine": C_lsi_fine, "C_LSI_block": C_lsi_block, "C_LSI_coarse_direct": C_lsi_coarse,
        "mean_P_fine": mean_P_fine, "mean_P_block": mean_P_block, "mean_P_coarse": mean_P_coarse,
        "var_P_block": var_P_block, "var_P_coarse": var_P_coarse,
        "delta_CLSI_pct": delta_clsi, "delta_meanP_pct": delta_meanP, "delta_varP_pct": delta_varP,
    }
    results["pairs"].append(pair)

    with open("/tmp/kolmogorov_v2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print()
    print("="*78)
    print(f"RESULTAT PAIRE 1 (L=8 -> L=4) :")
    print("="*78)
    print(f"  P_avg fine        = {mean_P_fine:.4f}  (attendu ~ 0.67 si beta=10)")
    print(f"  P_avg block-spin  = {mean_P_block:.4f}")
    print(f"  P_avg coarse dir. = {mean_P_coarse:.4f}")
    print(f"  Delta P_avg = {delta_meanP:.2f}%")
    print()
    print(f"  C_LSI fine          = {C_lsi_fine:.4f}")
    print(f"  C_LSI block-spinned = {C_lsi_block:.4f}")
    print(f"  C_LSI coarse direct = {C_lsi_coarse:.4f}")
    print(f"  Delta C_LSI (KEY) = {delta_clsi:.2f}%")
    print(f"  Delta var(P) = {delta_varP:.2f}%")
    print()
    print(f"  H_B1 precedent : Delta 9.5%")
    if delta_clsi < 5:
        print(f"  *** Delta {delta_clsi:.1f}% < 5% - Conjecture C* SUPPORTEE FORT")
    elif delta_clsi < 10:
        print(f"  * Delta {delta_clsi:.1f}% - coherent H_B1")
    else:
        print(f"  ? Delta {delta_clsi:.1f}% > 10% - Conjecture C* non resserree")

    results["verdict"] = {"mean_delta_pct": delta_clsi, "expected_avgP_at_b10": 0.67}
    with open("/tmp/kolmogorov_v2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults: /tmp/kolmogorov_v2_results.json")


if __name__ == "__main__":
    main()
