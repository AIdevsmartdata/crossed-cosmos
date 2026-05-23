"""Re-test SO(N) avec VRAI 't Hooft SO : β = 2(N-2)²/λ.

Catch : SU(N) utilise β = 2N²/λ (Casimir adjoint = 2N).
       SO(N) utilise β = 2(N-2)²/λ (Casimir adjoint = 2(N-2)).

Pour λ=0.8 :
  SO(3) : β = 2·1/0.8 = 2.5
  SO(4) : β = 2·4/0.8 = 10
  SO(5) : β = 2·9/0.8 = 22.5
  SO(6) : β = 2·16/0.8 = 40

Test :
  SO(6) à β=40 : si C_LSI ≈ 0.25 → convention rescued, Theorem C cross-groupe OK
  Si reste -20% → vrai effet non explicable par convention
"""
import numpy as np
import time
from scipy.linalg import expm


def small_random_SO_N(N, eps):
    A = np.random.randn(N, N) * eps
    A = 0.5 * (A - A.T)
    return expm(A)


def staple_4D_son(links, x0, x1, x2, x3, mu, L, N):
    stp = np.zeros((N, N))
    coord = (x0, x1, x2, x3)
    for nu in range(4):
        if nu == mu: continue
        coord_pm = list(coord); coord_pm[mu] = (coord_pm[mu]+1) % L
        coord_pn = list(coord); coord_pn[nu] = (coord_pn[nu]+1) % L
        U1 = links[coord_pm[0], coord_pm[1], coord_pm[2], coord_pm[3], nu]
        U2 = links[coord_pn[0], coord_pn[1], coord_pn[2], coord_pn[3], mu].T
        U3 = links[coord[0], coord[1], coord[2], coord[3], nu].T
        stp += U1 @ U2 @ U3
        coord_mn = list(coord); coord_mn[nu] = (coord_mn[nu]-1) % L
        coord_pm_mn = list(coord_pm); coord_pm_mn[nu] = (coord_pm_mn[nu]-1) % L
        U1b = links[coord_pm_mn[0], coord_pm_mn[1], coord_pm_mn[2], coord_pm_mn[3], nu].T
        U2b = links[coord_mn[0], coord_mn[1], coord_mn[2], coord_mn[3], mu].T
        U3b = links[coord_mn[0], coord_mn[1], coord_mn[2], coord_mn[3], nu]
        stp += U1b @ U2b @ U3b
    return stp


def sweep_4D_son(links, beta, L, eps, N):
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        U = links[x0,x1,x2,x3,mu].copy()
                        stp = staple_4D_son(links, x0,x1,x2,x3, mu, L, N)
                        R = small_random_SO_N(N, eps)
                        U_new = R @ U
                        tr_new = np.trace(U_new @ stp) / N
                        tr_old = np.trace(U @ stp) / N
                        dS = -beta * (tr_new - tr_old)
                        if dS < 0 or np.random.random() < np.exp(-dS):
                            links[x0,x1,x2,x3,mu] = U_new
    return links


def plaq_field_son_4D(links, L, N):
    P = np.zeros((L, L, L, L))
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U1 = links[x0, x1, x2, x3, 0]
                    U2 = links[(x0+1)%L, x1, x2, x3, 1]
                    U3 = links[x0, (x1+1)%L, x2, x3, 0].T
                    U4 = links[x0, x1, x2, x3, 1].T
                    Pmat = U1 @ U2 @ U3 @ U4
                    P[x0, x1, x2, x3] = np.trace(Pmat) / N
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


def main():
    np.random.seed(2047)
    L = 5
    n_therm = 60
    n_meas = 12

    print("=" * 78)
    print("RE-TEST SO(N) avec VRAI 't Hooft SO : β = 2(N-2)²/λ")
    print("=" * 78)
    print()
    print(f"Convention Casimir adjoint SO(N) = 2(N-2) (vs SU(N) = 2N)")
    print(f"λ=0.8 target :")
    print(f"  SO(4) β=10   (était 20  → λ_eff_old = 1.6)")
    print(f"  SO(5) β=22.5 (était 31.25 → λ_eff_old = 1.11)")
    print(f"  SO(6) β=40   (était 45  → λ_eff_old = 0.92)")
    print()

    tests = [
        (4, 10),
        (5, 22.5),
        (6, 40),
    ]

    results = {}
    for N, beta in tests:
        print(f"\n--- SO({N}) β={beta} ('t Hooft λ=0.8 correct, Casimir 2(N-2)) ---")
        rank = N // 2
        harm2 = 2  # D=4
        saturated = (rank == harm2)
        pred = 0.25 * (1 - 1/6) if saturated else 0.25
        eps = max(0.05, 0.3/np.sqrt(beta/(N-2)))

        links = np.zeros((L, L, L, L, 4, N, N))
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        for mu in range(4):
                            links[x0,x1,x2,x3,mu] = np.eye(N)
        t0 = time.time()
        for _ in range(n_therm):
            links = sweep_4D_son(links, beta, L, eps, N)

        P_all = np.zeros((n_meas, L, L, L, L))
        for c in range(n_meas):
            for _ in range(3):
                links = sweep_4D_son(links, beta, L, eps, N)
            P_all[c] = plaq_field_son_4D(links, L, N)
        C = C_LSI_proper(P_all)
        mP = float(np.mean(P_all))
        d = (C - pred)/pred * 100
        print(f"  rank={rank} ({'SATURÉ' if saturated else 'NON sat'}) prédit={pred:.4f}")
        print(f"  C_LSI={C:.4f}  ⟨P⟩={mP:.4f}  Δ={d:+.1f}%  t={time.time()-t0:.0f}s")
        results[N] = {"beta": beta, "C_LSI": float(C), "mean_P": mP,
                     "rank": rank, "saturated": saturated, "predicted": pred, "delta_pct": d}

    print()
    print("=" * 78)
    print("VERDICT — Theorem C cross-groupe avec VRAI 't Hooft SO")
    print("=" * 78)
    print()
    print(f"{'N':>3}{'rank':>5}{'sat':>5}{'β corr':>8}{'C_LSI':>10}{'pred':>10}{'Δ':>8}")
    for N, r in sorted(results.items()):
        print(f"{N:>3}{r['rank']:>5}{'OUI' if r['saturated'] else 'NON':>5}"
              f"{r['beta']:>8.1f}{r['C_LSI']:>10.4f}{r['predicted']:>10.4f}{f'{r['delta_pct']:+.1f}%':>8}")

    print()
    so6 = results[6]
    if abs(so6['delta_pct']) < 10:
        print(f"  ⭐⭐⭐ SO(6) RESCUED : Δ = {so6['delta_pct']:+.1f}% à β=40 (correct 't Hooft)")
        print(f"     ⟹ Biais précédent était convention SO mismatch (Casimir 2N vs 2(N-2))")
        print(f"     ⟹ Theorem C cross-groupe TIENT avec δ_{{rank, Harm²}} ✓")
    else:
        print(f"  🟡 SO(6) reste Δ={so6['delta_pct']:+.1f}% — biais SO réel au-delà de convention")

    import json
    with open("results/SO_correct_thooft.json", "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)
    print("\n💾 results/SO_correct_thooft.json")


if __name__ == "__main__":
    main()
