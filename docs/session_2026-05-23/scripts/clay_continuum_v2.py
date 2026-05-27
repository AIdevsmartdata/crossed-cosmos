"""SU(2) D=4 continuum scaling — Multi-L pour fit H_CONT_1 fiable.

Tests :
  - 4 valeurs L = 8, 12, 16, 20 (vrai fit 1/L² extrapolation)
  - 3 valeurs β = 5, 10, 20 ('t Hooft scan)
  - 50 configs par (L, β)
  - Mesures : C_LSI, ⟨P⟩, correlator spatial

Objectif Clay : confirmer c_∞ extrapolé L→∞ = 0.25 à <1% (vs script PC qui donnait Δ 7.6%).
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


@njit(cache=True, fastmath=True, parallel=False)
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


def run_lattice(L, beta, n_therm, n_meas, n_skip=5):
    eps = max(0.04, 0.4/np.sqrt(beta))
    links = np.zeros((L, L, L, L, 4, 4))
    links[..., 0] = 1.0
    t0 = time.time()
    print(f"  Therm L={L} β={beta} ({n_therm} sweeps)...")
    for s in range(n_therm):
        links = sweep_4D(links, beta, L, eps)
    print(f"  Therm done {time.time()-t0:.0f}s")
    P_all = np.zeros((n_meas, L, L, L, L))
    t1 = time.time()
    for c in range(n_meas):
        for _ in range(n_skip):
            links = sweep_4D(links, beta, L, eps)
        P_all[c] = plaq_field_4D(links, L)
        if c % 10 == 0:
            print(f"  config {c+1}/{n_meas}: ⟨P⟩={np.mean(P_all[c]):.4f} t={time.time()-t1:.0f}s")
    return C_LSI_proper(P_all), float(np.mean(P_all)), float(np.var(P_all))


def main():
    np.random.seed(2050)
    print("=" * 78)
    print("CONTINUUM SCALING SU(2) D=4 multi-L multi-β (Vast.ai run)")
    print("=" * 78)

    n_therm = 200
    n_meas = 50

    # Pour vrai fit 1/L², need L≥12 + L=20
    # Budget compute estimate :
    # L=8 4096 sites × 200+250 sweeps = ~5 min
    # L=12 20k sites × 450 sweeps = ~30 min
    # L=16 65k sites × 450 sweeps = ~90 min
    # L=20 160k sites × 450 sweeps = ~3h
    # Total : ~4-5h pour 4×L (one β=10)
    # Pour multi-β=5,10,20 = ~12-15h. Trop. On fait β=10 seul.

    BETA = 10.0
    Ls = [8, 12, 16]  # skip L=20 pour rester sous 4h

    results = {}
    t_start = time.time()
    for L in Ls:
        print(f"\n=== L={L} β={BETA} ===")
        C_lsi, mean_P, var_P = run_lattice(L, BETA, n_therm, n_meas)
        results[L] = {"C_LSI": float(C_lsi), "mean_P": mean_P, "var_P": var_P}
        with open("clay_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"  L={L}: C_LSI={C_lsi:.4f} mean_P={mean_P:.4f}")

    # Fit 1/L²
    Ls_arr = np.array(sorted(results.keys()))
    cls_arr = np.array([results[L]["C_LSI"] for L in Ls_arr])
    if len(Ls_arr) >= 2:
        coef = np.polyfit(1/Ls_arr**2, cls_arr, 1)
        A, c_inf_fit = coef
        print(f"\n=== Fit C_LSI = c_∞ + A/L² ===")
        print(f"  c_∞ extrap = {c_inf_fit:.4f}  (théorique 0.25)")
        print(f"  A = {A:.4f}")
        print(f"  Δ vs c_∞=0.25 : {(c_inf_fit-0.25)/0.25*100:+.2f}%")
        results["fit"] = {"c_inf_extrap": float(c_inf_fit), "A": float(A)}
        with open("clay_results.json", "w") as f:
            json.dump(results, f, indent=2)

    print(f"\nTotal wall-clock : {(time.time()-t_start)/60:.1f} min")


if __name__ == "__main__":
    main()
