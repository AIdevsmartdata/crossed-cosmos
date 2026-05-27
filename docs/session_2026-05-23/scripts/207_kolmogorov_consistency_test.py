"""Test EMPIRIQUE Conjecture C* (Lemme G1.1(c) Opus Einstein) :
projective consistency $(\rho_{a,a'})_* \mu_{a'} = \mu_a$ au vrai 't Hooft scaling.

Méthodologie :
1. HMC SU(2) D=4 L_fine=12 β=10 → μ_fine (100 configs)
2. Block-spin 2×2×2×2 → champs sur L_coarse=6
3. HMC SU(2) D=4 L_coarse=6 β=10 (même 't Hooft β) → μ_coarse
4. Compare statistiques : ⟨P⟩, var(P), C_LSI(block) vs C_LSI(coarse)
5. Δ = |C_LSI_block - C_LSI_coarse| / C_LSI_coarse

Si Δ < 5% au lieu de Δ 9.5% précédent (H_B1) → support fort Conjecture C*.
Si Δ → 0 dans la limite L_fine → ∞ → Conjecture C* exacte.

Output : results/kolmogorov_consistency.json
"""
import numpy as np
import time, json
from numba import njit


@njit(cache=True, fastmath=True)
def su2_mult(u, v):
    return np.array([
        u[0]*v[0]-u[1]*v[1]-u[2]*v[2]-u[3]*v[3],
        u[0]*v[1]+u[1]*v[0]+u[2]*v[3]-u[3]*v[2],
        u[0]*v[2]-u[1]*v[3]+u[2]*v[0]+u[3]*v[1],
        u[0]*v[3]+u[1]*v[2]-u[2]*v[1]+u[3]*v[0],
    ])

@njit(cache=True, fastmath=True)
def su2_dag(u): return np.array([u[0], -u[1], -u[2], -u[3]])

@njit(cache=True, fastmath=True)
def half_tr_mult(u, v):
    return u[0]*v[0] - u[1]*v[1] - u[2]*v[2] - u[3]*v[3]


@njit(cache=True)
def staple_4D(links, x0, x1, x2, x3, mu, L):
    stp = np.zeros(4)
    coord = np.array([x0, x1, x2, x3])
    for nu in range(4):
        if nu == mu: continue
        xpm = coord.copy(); xpm[mu] = (xpm[mu]+1) % L
        xpn = coord.copy(); xpn[nu] = (xpn[nu]+1) % L
        u1 = links[xpm[0],xpm[1],xpm[2],xpm[3], nu]
        u2 = su2_dag(links[xpn[0],xpn[1],xpn[2],xpn[3], mu])
        u3 = su2_dag(links[coord[0],coord[1],coord[2],coord[3], nu])
        s1 = su2_mult(su2_mult(u1, u2), u3)
        xmn = coord.copy(); xmn[nu] = (xmn[nu]-1) % L
        xpm_mn = xpm.copy(); xpm_mn[nu] = (xpm_mn[nu]-1) % L
        u1b = su2_dag(links[xpm_mn[0],xpm_mn[1],xpm_mn[2],xpm_mn[3], nu])
        u2b = su2_dag(links[xmn[0],xmn[1],xmn[2],xmn[3], mu])
        u3b = links[xmn[0],xmn[1],xmn[2],xmn[3], nu]
        s2 = su2_mult(su2_mult(u1b, u2b), u3b)
        stp = stp + s1 + s2
    return stp


@njit(cache=True, fastmath=True)
def sweep_4D(links, beta, L, eps):
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        U = links[x0,x1,x2,x3,mu].copy()
                        stp = staple_4D(links, x0,x1,x2,x3, mu, L)
                        R = np.random.randn(4) * eps
                        R[0] = 1.0 + R[0] * 0.1
                        n = np.sqrt(R[0]**2+R[1]**2+R[2]**2+R[3]**2)
                        R = R/n
                        U_new = su2_mult(R, U)
                        tr_new = half_tr_mult(U_new, stp)
                        tr_old = half_tr_mult(U, stp)
                        dS = -beta * (tr_new - tr_old)
                        if dS < 0 or np.random.random() < np.exp(-dS):
                            links[x0,x1,x2,x3,mu] = U_new
    return links


@njit(cache=True, fastmath=True)
def plaq_field_4D(links, L):
    P = np.zeros((L, L, L, L))
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U1 = links[x0,x1,x2,x3, 0]
                    U2 = links[(x0+1)%L,x1,x2,x3, 1]
                    U3 = su2_dag(links[x0,(x1+1)%L,x2,x3, 0])
                    U4 = su2_dag(links[x0,x1,x2,x3, 1])
                    Pv = su2_mult(su2_mult(su2_mult(U1,U2),U3),U4)
                    P[x0,x1,x2,x3] = Pv[0]
    return P


@njit(cache=True)
def block_spin_2x_4D(links_fine, L_fine, L_coarse):
    """Block-spin map : fine links L_fine → coarse links L_coarse=L_fine/2.

    For each coarse edge of length 2 in direction mu, multiply the 2 fine
    SU(2) links along the straight path. Returns coarse links array.
    """
    links_coarse = np.zeros((L_coarse, L_coarse, L_coarse, L_coarse, 4, 4))
    links_coarse[..., 0] = 1.0  # init identity
    for X0 in range(L_coarse):
        for X1 in range(L_coarse):
            for X2 in range(L_coarse):
                for X3 in range(L_coarse):
                    for mu in range(4):
                        # Coarse edge from (2X0, 2X1, 2X2, 2X3) along mu, length 2
                        x_fine_start = np.array([2*X0, 2*X1, 2*X2, 2*X3])
                        # First fine link at x_fine_start in direction mu
                        U1 = links_fine[x_fine_start[0], x_fine_start[1],
                                        x_fine_start[2], x_fine_start[3], mu]
                        # Second fine link at x_fine_start + e_mu in direction mu
                        x_fine_mid = x_fine_start.copy()
                        x_fine_mid[mu] = (x_fine_mid[mu] + 1) % L_fine
                        U2 = links_fine[x_fine_mid[0], x_fine_mid[1],
                                        x_fine_mid[2], x_fine_mid[3], mu]
                        # Coarse link = U1 * U2 (product along path)
                        U_coarse = su2_mult(U1, U2)
                        # Project back to SU(2) (normalize)
                        nrm = np.sqrt(U_coarse[0]**2 + U_coarse[1]**2 +
                                      U_coarse[2]**2 + U_coarse[3]**2)
                        if nrm > 1e-10:
                            U_coarse = U_coarse / nrm
                        links_coarse[X0, X1, X2, X3, mu] = U_coarse
    return links_coarse


def C_LSI_proper(P_all):
    mean_P = np.mean(P_all)
    f = (P_all - mean_P) ** 2
    f2 = f.flatten() ** 2 + 1e-12
    E_f2 = np.mean(f2)
    ent = np.mean(f2 * np.log(f2)) - E_f2 * np.log(E_f2)
    grad_sq = 0.0
    for axis in range(1, 5):
        f_shift = np.roll(f, -1, axis=axis)
        grad_sq += np.mean((f_shift - f) ** 2)
    return ent / (2 * grad_sq) if grad_sq > 0 else None


def run_hmc_4D(L, beta, n_therm, n_meas, n_skip=5, seed=2070):
    np.random.seed(seed)
    eps = max(0.04, 0.4/np.sqrt(beta))
    links = np.zeros((L, L, L, L, 4, 4))
    links[..., 0] = 1.0
    t0 = time.time()
    print(f"  Therm L={L} β={beta} ({n_therm} sweeps)...", flush=True)
    for s in range(n_therm):
        links = sweep_4D(links, beta, L, eps)
    print(f"  Therm done {time.time()-t0:.0f}s, ⟨P⟩={np.mean(plaq_field_4D(links, L)):.4f}", flush=True)
    return links, eps


def measure_configs(links_init, beta, L, n_meas, eps, n_skip=5, do_block_spin=False, L_coarse=None):
    links = links_init.copy()
    P_all = np.zeros((n_meas, L, L, L, L))
    P_block_all = None
    if do_block_spin:
        P_block_all = np.zeros((n_meas, L_coarse, L_coarse, L_coarse, L_coarse))
    t1 = time.time()
    for c in range(n_meas):
        for _ in range(n_skip):
            links = sweep_4D(links, beta, L, eps)
        P_all[c] = plaq_field_4D(links, L)
        if do_block_spin:
            links_coarse = block_spin_2x_4D(links, L, L_coarse)
            P_block_all[c] = plaq_field_4D(links_coarse, L_coarse)
        if c % 10 == 0:
            extra = f" ⟨P_block⟩={np.mean(P_block_all[c]):.4f}" if do_block_spin else ""
            print(f"  config {c+1}/{n_meas}: ⟨P⟩={np.mean(P_all[c]):.4f}{extra} t={time.time()-t1:.0f}s", flush=True)
    return P_all, P_block_all


def main():
    print("=" * 78)
    print("TEST EMPIRIQUE Conjecture C* (Lemme G1.1(c) Opus Einstein)")
    print("Projective consistency ρ_*(μ_fine) =? μ_coarse au vrai 't Hooft β fixé")
    print("=" * 78)

    BETA = 10.0  # 't Hooft β=10 fixed cross-scales
    n_therm = 300
    n_meas = 50

    results = {"beta": BETA, "n_meas": n_meas, "pairs": []}

    # PAIR 1 : L_fine=8, L_coarse=4 (rapide, baseline)
    print("\n" + "─" * 78)
    print("PAIRE 1 : L_fine=8 → L_coarse=4 (block-spin 2×)")
    print("─" * 78)
    t0 = time.time()

    L_fine = 8
    L_coarse = 4

    print(f"\n=== HMC fine L={L_fine} β={BETA} ===", flush=True)
    links_fine, eps_fine = run_hmc_4D(L_fine, BETA, n_therm, n_meas, seed=2070)
    P_fine, P_block = measure_configs(links_fine, BETA, L_fine, n_meas, eps_fine,
                                        do_block_spin=True, L_coarse=L_coarse)

    print(f"\n=== HMC direct coarse L={L_coarse} β={BETA} ===", flush=True)
    links_coarse, eps_coarse = run_hmc_4D(L_coarse, BETA, n_therm, n_meas, seed=2071)
    P_coarse, _ = measure_configs(links_coarse, BETA, L_coarse, n_meas, eps_coarse)

    C_lsi_fine = C_LSI_proper(P_fine)
    C_lsi_block = C_LSI_proper(P_block)
    C_lsi_coarse = C_LSI_proper(P_coarse)
    mean_P_fine = float(np.mean(P_fine))
    mean_P_block = float(np.mean(P_block))
    mean_P_coarse = float(np.mean(P_coarse))
    var_P_block = float(np.var(P_block))
    var_P_coarse = float(np.var(P_coarse))

    delta_clsi = abs(C_lsi_block - C_lsi_coarse) / C_lsi_coarse * 100
    delta_meanP = abs(mean_P_block - mean_P_coarse) / mean_P_coarse * 100
    delta_varP = abs(var_P_block - var_P_coarse) / var_P_coarse * 100

    pair_result = {
        "L_fine": L_fine, "L_coarse": L_coarse,
        "C_LSI_fine": float(C_lsi_fine),
        "C_LSI_blockspin": float(C_lsi_block),
        "C_LSI_coarse_direct": float(C_lsi_coarse),
        "mean_P_fine": mean_P_fine,
        "mean_P_block": mean_P_block,
        "mean_P_coarse": mean_P_coarse,
        "var_P_block": var_P_block,
        "var_P_coarse": var_P_coarse,
        "delta_CLSI_pct": float(delta_clsi),
        "delta_meanP_pct": float(delta_meanP),
        "delta_varP_pct": float(delta_varP),
        "wall_clock_min": (time.time()-t0)/60,
    }
    results["pairs"].append(pair_result)

    with open("/tmp/voie1_calcs/results/kolmogorov_consistency.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n  ⟨P⟩ fine        = {mean_P_fine:.4f}")
    print(f"  ⟨P⟩ block-spin  = {mean_P_block:.4f}")
    print(f"  ⟨P⟩ coarse dir. = {mean_P_coarse:.4f}")
    print(f"  Δ ⟨P⟩ = {delta_meanP:.2f}%")
    print(f"\n  C_LSI fine          = {C_lsi_fine:.4f}")
    print(f"  C_LSI block-spinned = {C_lsi_block:.4f}")
    print(f"  C_LSI coarse direct = {C_lsi_coarse:.4f}")
    print(f"  Δ C_LSI (KEY) = {delta_clsi:.2f}%")
    print(f"  Δ var(P) = {delta_varP:.2f}%")

    # PAIR 2 : L_fine=12, L_coarse=6 (plus précis)
    print("\n" + "─" * 78)
    print("PAIRE 2 : L_fine=12 → L_coarse=6 (block-spin 2×)")
    print("─" * 78)
    t0 = time.time()

    L_fine = 12
    L_coarse = 6
    n_meas_p2 = 30  # plus court pour gagner temps

    print(f"\n=== HMC fine L={L_fine} β={BETA} ===", flush=True)
    links_fine, eps_fine = run_hmc_4D(L_fine, BETA, n_therm, n_meas_p2, seed=2080)
    P_fine, P_block = measure_configs(links_fine, BETA, L_fine, n_meas_p2, eps_fine,
                                        do_block_spin=True, L_coarse=L_coarse)

    print(f"\n=== HMC direct coarse L={L_coarse} β={BETA} ===", flush=True)
    links_coarse, eps_coarse = run_hmc_4D(L_coarse, BETA, n_therm, n_meas_p2, seed=2081)
    P_coarse, _ = measure_configs(links_coarse, BETA, L_coarse, n_meas_p2, eps_coarse)

    C_lsi_fine = C_LSI_proper(P_fine)
    C_lsi_block = C_LSI_proper(P_block)
    C_lsi_coarse = C_LSI_proper(P_coarse)
    mean_P_fine = float(np.mean(P_fine))
    mean_P_block = float(np.mean(P_block))
    mean_P_coarse = float(np.mean(P_coarse))
    var_P_block = float(np.var(P_block))
    var_P_coarse = float(np.var(P_coarse))

    delta_clsi = abs(C_lsi_block - C_lsi_coarse) / C_lsi_coarse * 100
    delta_meanP = abs(mean_P_block - mean_P_coarse) / mean_P_coarse * 100
    delta_varP = abs(var_P_block - var_P_coarse) / var_P_coarse * 100

    pair_result = {
        "L_fine": L_fine, "L_coarse": L_coarse,
        "n_meas": n_meas_p2,
        "C_LSI_fine": float(C_lsi_fine),
        "C_LSI_blockspin": float(C_lsi_block),
        "C_LSI_coarse_direct": float(C_lsi_coarse),
        "mean_P_fine": mean_P_fine,
        "mean_P_block": mean_P_block,
        "mean_P_coarse": mean_P_coarse,
        "var_P_block": var_P_block,
        "var_P_coarse": var_P_coarse,
        "delta_CLSI_pct": float(delta_clsi),
        "delta_meanP_pct": float(delta_meanP),
        "delta_varP_pct": float(delta_varP),
        "wall_clock_min": (time.time()-t0)/60,
    }
    results["pairs"].append(pair_result)

    with open("/tmp/voie1_calcs/results/kolmogorov_consistency.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n  ⟨P⟩ fine        = {mean_P_fine:.4f}")
    print(f"  ⟨P⟩ block-spin  = {mean_P_block:.4f}")
    print(f"  ⟨P⟩ coarse dir. = {mean_P_coarse:.4f}")
    print(f"  Δ ⟨P⟩ = {delta_meanP:.2f}%")
    print(f"\n  C_LSI fine          = {C_lsi_fine:.4f}")
    print(f"  C_LSI block-spinned = {C_lsi_block:.4f}")
    print(f"  C_LSI coarse direct = {C_lsi_coarse:.4f}")
    print(f"  Δ C_LSI (KEY) = {delta_clsi:.2f}%")
    print(f"  Δ var(P) = {delta_varP:.2f}%")

    # VERDICT
    print("\n" + "=" * 78)
    print("VERDICT — Conjecture C* support empirique")
    print("=" * 78)
    print()
    print(f"  Précédent H_B1 script 165 : Δ 9.5%")
    print(f"  PAIRE 1 (L8→L4) :  Δ C_LSI = {results['pairs'][0]['delta_CLSI_pct']:.2f}%")
    print(f"  PAIRE 2 (L12→L6) : Δ C_LSI = {results['pairs'][1]['delta_CLSI_pct']:.2f}%")
    print()
    mean_delta = np.mean([p['delta_CLSI_pct'] for p in results['pairs']])
    print(f"  Mean Δ C_LSI cross-paires = {mean_delta:.2f}%")
    if mean_delta < 5:
        print(f"  ⭐⭐⭐ Conjecture C* SUPPORTÉE FORT (<5%) — projective consistency proche exacte")
    elif mean_delta < 10:
        print(f"  ⭐ Conjecture C* SUPPORTÉE (≈10%) — cohérent H_B1 précédent")
    else:
        print(f"  🟡 Δ {mean_delta:.1f}% — Conjecture C* non confirmée à cette échelle")

    # Trend L_fine → ∞
    if len(results['pairs']) >= 2:
        d1 = results['pairs'][0]['delta_CLSI_pct']
        d2 = results['pairs'][1]['delta_CLSI_pct']
        if d2 < d1:
            print(f"  📉 Δ décroît avec L_fine (d1={d1:.2f}%, d2={d2:.2f}%) → cohérent Conjecture C* exacte limite")
        else:
            print(f"  📈 Δ ne décroît pas avec L_fine (d1={d1:.2f}%, d2={d2:.2f}%) → biais structurel finite-L")

    results["verdict"] = {
        "mean_delta_CLSI_pct": float(mean_delta),
        "prev_HB1_delta_pct": 9.5,
        "improvement": float((9.5 - mean_delta)/9.5*100) if mean_delta < 9.5 else 0,
    }

    with open("/tmp/voie1_calcs/results/kolmogorov_consistency.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 results/kolmogorov_consistency.json")


if __name__ == "__main__":
    main()
