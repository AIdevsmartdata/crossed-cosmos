"""Test prédiction loi C_LSI(G,D) = c_∞ · f(π_1(G)).

Sp(2) = matrices 4×4 complexes U·J·U^T = J (symplectique compacte).
- dim = 10
- rank = 2 (= dim Harm²(D=4) → SATURÉ)
- π_1(Sp(N)) = 0 (simply connected)

Prédiction (loi Kevin/DS Bot) :
- f(π_1=0) = 1 (pas de biais quotient comme SO)
- Saturation rank=2 → κ=1/6
- C_LSI prédit = c_∞ · (1 - 1/6) = 0.25 · 5/6 = 0.2083

Si SP(2) ≈ 0.21 → loi f(π_1) confirmée (pas SO biais)
Si SP(2) ≈ 0.19 (comme SO) → biais structurel différent, loi à raffiner
"""
import numpy as np
import time
from scipy.linalg import expm


def random_sp2N_init(N):
    """Identity matrix as start."""
    return np.eye(2*N, dtype=complex)


def make_J(N):
    """Symplectic form J = block_diag([[0, I_N], [-I_N, 0]])."""
    J = np.zeros((2*N, 2*N), dtype=complex)
    J[:N, N:] = np.eye(N)
    J[N:, :N] = -np.eye(N)
    return J


def small_random_sp2N(N, eps, J):
    """Random Sp(N) infinitesimal generator + exp.

    sp(N) algebra : X = [[A, B], [C, -A^T]] with B=B^T, C=C^T (over complex anti-Hermitian).
    For unitary Sp(N) (USp(2N)) : X anti-Hermitian and J·X = X^T·J (or similar).
    Simpler : X = i·H where H is Hermitian and J·H + H^T·J = 0.
    Equivalently H = [[A, B], [B^†, -A^T]] with A=A^†, B=B^T.
    """
    # Generate A : N×N Hermitian
    A_re = np.random.randn(N, N) * eps
    A_im = np.random.randn(N, N) * eps
    A = (A_re + 1j*A_im) / np.sqrt(2)
    A = 0.5*(A + A.conj().T)  # Hermitian
    # Generate B : N×N symmetric complex
    B_re = np.random.randn(N, N) * eps
    B_im = np.random.randn(N, N) * eps
    B = (B_re + 1j*B_im) / np.sqrt(2)
    B = 0.5*(B + B.T)  # symmetric (not Hermitian)
    # Construct H = [[A, B], [B^*, -A^T]]
    H = np.zeros((2*N, 2*N), dtype=complex)
    H[:N, :N] = A
    H[:N, N:] = B
    H[N:, :N] = B.conj()
    H[N:, N:] = -A.T
    # exp(i*H) is Sp(N) (USp)
    return expm(1j * H)


def staple_4D_sp(links, x0, x1, x2, x3, mu, L, N2):
    """Staple sum for Sp link at (x, mu). N2 = 2*N matrix size."""
    stp = np.zeros((N2, N2), dtype=complex)
    coord = (x0, x1, x2, x3)
    for nu in range(4):
        if nu == mu: continue
        coord_pm = list(coord); coord_pm[mu] = (coord_pm[mu]+1) % L
        coord_pn = list(coord); coord_pn[nu] = (coord_pn[nu]+1) % L
        U1 = links[coord_pm[0], coord_pm[1], coord_pm[2], coord_pm[3], nu]
        U2 = links[coord_pn[0], coord_pn[1], coord_pn[2], coord_pn[3], mu].conj().T
        U3 = links[coord[0], coord[1], coord[2], coord[3], nu].conj().T
        stp += U1 @ U2 @ U3
        coord_mn = list(coord); coord_mn[nu] = (coord_mn[nu]-1) % L
        coord_pm_mn = list(coord_pm); coord_pm_mn[nu] = (coord_pm_mn[nu]-1) % L
        U1b = links[coord_pm_mn[0], coord_pm_mn[1], coord_pm_mn[2], coord_pm_mn[3], nu].conj().T
        U2b = links[coord_mn[0], coord_mn[1], coord_mn[2], coord_mn[3], mu].conj().T
        U3b = links[coord_mn[0], coord_mn[1], coord_mn[2], coord_mn[3], nu]
        stp += U1b @ U2b @ U3b
    return stp


def sweep_4D_sp(links, beta, L, eps, N, J):
    N2 = 2*N
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        U = links[x0,x1,x2,x3,mu].copy()
                        stp = staple_4D_sp(links, x0,x1,x2,x3, mu, L, N2)
                        R = small_random_sp2N(N, eps, J)
                        U_new = R @ U
                        tr_new = np.real(np.trace(U_new @ stp)) / N2
                        tr_old = np.real(np.trace(U @ stp)) / N2
                        dS = -beta * (tr_new - tr_old)
                        if dS < 0 or np.random.random() < np.exp(-dS):
                            links[x0,x1,x2,x3,mu] = U_new
    return links


def plaq_field_sp_4D(links, L, N2):
    P = np.zeros((L, L, L, L))
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    U1 = links[x0, x1, x2, x3, 0]
                    U2 = links[(x0+1)%L, x1, x2, x3, 1]
                    U3 = links[x0, (x1+1)%L, x2, x3, 0].conj().T
                    U4 = links[x0, x1, x2, x3, 1].conj().T
                    Pmat = U1 @ U2 @ U3 @ U4
                    P[x0, x1, x2, x3] = np.real(np.trace(Pmat)) / N2
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
    np.random.seed(2048)
    N = 2  # Sp(2) = matrices 4×4 complexes symplectiques
    N2 = 2*N
    L = 5
    # 't Hooft scaling Sp(N) : Casimir adjoint Sp(N) = N+1
    # β = 2(N+1)²/λ? Or β = 2N²·something... convention plus complexe pour Sp
    # Simplification : utiliser β=10 standard pour comparaison directe SU(2) baseline
    # Plus rigoureux : β = 2N(2N+1)/λ ? Pour Sp(2) N2=4 : β = 2·4·5/0.8 = 50
    beta = 50.0  # tentative 't Hooft Sp(2)
    eps = 0.12
    n_therm = 50
    n_meas = 10

    print("=" * 78)
    print("TEST loi f(π_1(G)) : Wilson Sp(2) D=4")
    print("=" * 78)
    print()
    print(f"Sp(2) : dim=10, rank=2, π_1(Sp(N))=0 (simply connected)")
    print(f"Prédiction loi f(π_1):")
    print(f"  - f(π_1=0) = 1 (PAS de biais quotient comme SO)")
    print(f"  - rank=2 = Harm²(D=4) → SATURÉ κ=1/6")
    print(f"  - C_LSI = c_∞(D=4) · 5/6 = 0.25 · 5/6 = 0.2083")
    print()
    print(f"Run β={beta} L={L} n_meas={n_meas}...")

    J = make_J(N)
    links = np.zeros((L, L, L, L, 4, N2, N2), dtype=complex)
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        links[x0,x1,x2,x3,mu] = np.eye(N2, dtype=complex)

    t0 = time.time()
    for s in range(n_therm):
        links = sweep_4D_sp(links, beta, L, eps, N, J)
        if s % 15 == 0:
            P = plaq_field_sp_4D(links, L, N2)
            print(f"  sweep {s+1}: ⟨P⟩={np.mean(P):.4f} t={time.time()-t0:.0f}s")

    print(f"Therm done t={time.time()-t0:.0f}s")
    t1 = time.time()
    P_all = np.zeros((n_meas, L, L, L, L))
    for c in range(n_meas):
        for _ in range(3):
            links = sweep_4D_sp(links, beta, L, eps, N, J)
        P_all[c] = plaq_field_sp_4D(links, L, N2)
        if c % 3 == 0:
            print(f"  config {c+1}: ⟨P⟩={np.mean(P_all[c]):.4f} t={time.time()-t1:.0f}s")

    C_lsi = C_LSI_proper(P_all)
    mP = float(np.mean(P_all))

    print()
    print("=" * 78)
    print("VERDICT — loi f(π_1(G))")
    print("=" * 78)
    print()
    print(f"Wilson Sp(2) D=4 L={L} β={beta} n_meas={n_meas} :")
    print(f"  ⟨P⟩  = {mP:.4f}")
    print(f"  C_LSI = {C_lsi:.4f}")
    print()
    print(f"  Prédit f(π_1=0)·κ_sat = 1 · 0.2083 (rank=2 saturé sans quotient) : Δ = {(C_lsi - 0.2083)/0.2083*100:+.1f}%")
    print(f"  Si biais SO Z_2 quotient appliqué (0.78·0.2083=0.163) : Δ = {(C_lsi - 0.163)/0.163*100:+.1f}%")
    print()
    print(f"Comparaison cross-groupe (même rank=2 saturé) :")
    print(f"  SU(3) D=4 π_1=0 : 0.210 ✓ (≈ 0.2083)")
    print(f"  SO(5) D=4 π_1=Z_2 : 0.199 (-22% si pas saturé, mais saturé prédit)")
    print(f"  Sp(2) D=4 π_1=0 : {C_lsi:.3f} ← NOUVEAU")
    print()
    if abs(C_lsi - 0.2083)/0.2083 < 0.15:
        print(f"  ⭐ Loi f(π_1=0)=1 CONFIRMÉE : Sp(2) ≈ SU(3) saturé κ=1/6")
        print(f"     ⟹ Le biais SO vient bien du quotient Z_2 (H_SO3 confirmé)")
    elif abs(C_lsi - 0.163)/0.163 < 0.10:
        print(f"  ⚠️ Sp(2) montre biais analogue à SO — loi f(π_1) à raffiner")
    else:
        print(f"  🟡 résultat intermédiaire")

    import json
    with open("results/Sp2_pi1_test.json", "w") as f:
        json.dump({
            "N": N, "dim_matrix": N2, "L": L, "beta": beta,
            "n_therm": n_therm, "n_meas": n_meas,
            "C_LSI": float(C_lsi), "mean_P": mP,
            "pred_f_pi1_0_saturated": 0.2083,
            "delta_vs_pred_pct": float((C_lsi - 0.2083)/0.2083*100),
        }, f, indent=2)
    print("\n💾 results/Sp2_pi1_test.json")


if __name__ == "__main__":
    main()
