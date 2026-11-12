# Calcul numerique (pilote CentreZN, 12/11/2026) : constante r_{N,q}(T) et controles d'identites.
# r_{N,q}(T) = |sum_j w^{qj} exp(Re(w^j T))| / sum_j exp(Re(w^j T)),  w = exp(2 pi i / N).
# (1) sup sur le disque |T| <= kappa (grille polaire fine) compare a la valeur en T = kappa reel ;
# (2) borne grossiere 1 - exp(-2 kappa) ; (3) N = 2 : tanh ;
# (4) modele jouet exact : tore 2x2, fibre 1, groupe Z_M (N | M), controle de |Zhat_q| <= rho^4 Zhat_0 et de la formule de Fourier.
import numpy as np, itertools, json, math

def r(N, q, T):
    j = np.arange(N)
    w = np.exp(2j * np.pi * j / N)
    f = np.exp(np.real(np.multiply.outer(T, w)))           # shape (..., N)
    num = np.abs((f * (w ** q)).sum(-1))
    den = f.sum(-1)
    return num / den

out = {"sup_disque": [], "monotonie_rayon": [], "grossiere_ok": True, "N2_tanh_ecart_max": 0.0}
kappas = [0.05, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0]
nr, nphi = 400, 2001
for N in range(2, 9):
    for q in range(1, N):
        for k in kappas:
            rad = np.linspace(0, k, nr)
            phi = np.linspace(0, 2 * np.pi, nphi)
            T = np.multiply.outer(rad, np.exp(1j * phi))
            R = r(N, q, T)
            i, jj = np.unravel_index(np.argmax(R), R.shape)
            sup = float(R[i, jj]); rreal = float(r(N, q, np.array([k + 0j]))[0])
            crude = 1 - math.exp(-2 * k)
            if sup > crude + 1e-12:
                out["grossiere_ok"] = False
            # monotonie en |T| du max angulaire
            mx = R.max(axis=1)
            mono = bool(np.all(np.diff(mx) >= -1e-12))
            out["sup_disque"].append({"N": N, "q": q, "kappa": k, "sup": sup, "r_reel": rreal,
                                      "ecart": sup - rreal, "rayon_arg": float(rad[i]), "phi_arg": float(phi[jj]),
                                      "grossiere": crude})
            if not mono:
                out["monotonie_rayon"].append({"N": N, "q": q, "kappa": k})
            if N == 2:
                out["N2_tanh_ecart_max"] = max(out["N2_tanh_ecart_max"], abs(sup - math.tanh(k)))

# formule fermee N = 3, q = 1, T reel : (e^{3k/2}-1)/(e^{3k/2}+2)
out["N3_formule_ecart"] = max(abs(float(r(3, 1, np.array([k + 0j]))[0]) - (math.exp(1.5 * k) - 1) / (math.exp(1.5 * k) + 2)) for k in kappas)

# (4) modele jouet exact : tore 2x2 (8 aretes), fibre 1, groupe Z_M, centre engendre par z = M/N, chi(g) = exp(2 pi i g / M)
def jouet(M, N, beta, q, seed=0):
    rng = np.random.default_rng(seed)
    m = n = 2
    # aretes : H(i,j) indice 0..3, V(i,j) indice 4..7
    H = lambda i, j: (i % m) * n + (j % n)
    V = lambda i, j: 4 + (i % m) * n + (j % n)
    plaq = [(i, j) for i in range(m) for j in range(n)]
    c = rng.uniform(0.3, 1.0, size=4) * np.exp(1j * rng.uniform(0, 2 * np.pi, size=4))  # poids complexes |c| <= 1
    confs = np.array(list(itertools.product(range(M), repeat=8)))   # M^8
    hol = []
    for (i, j) in plaq:
        hol.append(confs[:, H(i, j)] + confs[:, V(i + 1, j)] - confs[:, H(i, j + 1)] - confs[:, V(i, j)])
    hol = np.array(hol) % M
    chi = np.exp(2j * np.pi * hol / M)          # shape (4, M^8)
    zeta = np.exp(2j * np.pi / N)
    Z = []
    for k in range(N):
        tw = np.ones(4, complex); tw[0] = zeta ** k
        S = np.real((beta * (c * tw)[:, None]) * chi).sum(0)
        Z.append(np.exp(S).mean())
    Z = np.array(Z)
    Zh = np.array([(zeta ** (qq * np.arange(N)) * Z).sum() for qq in range(N)])
    kap = beta * 1.0
    # rho exact sur le disque |T| <= beta (grille)
    rad = np.linspace(0, kap, 300); phi = np.linspace(0, 2 * np.pi, 1501)
    rho = float(r(N, q, np.multiply.outer(rad, np.exp(1j * phi))).max())
    return {"M": M, "N": N, "beta": beta, "q": q, "Z_k": [float(x) for x in Z],
            "ratio": float(abs(Zh[q]) / Zh[0].real), "rho^4": rho ** 4, "grossiere^4": (1 - math.exp(-2 * kap)) ** 4,
            "borne_ok": bool(abs(Zh[q]) <= rho ** 4 * Zh[0].real + 1e-12)}

out["jouets"] = [jouet(3, 3, 0.7, 1), jouet(3, 3, 2.0, 1), jouet(6, 3, 1.3, 2, seed=1), jouet(4, 4, 1.1, 2, seed=2),
                 jouet(4, 2, 0.9, 1, seed=3), jouet(5, 5, 1.7, 2, seed=4)]

# resume
pires = sorted(out["sup_disque"], key=lambda d: -d["ecart"])[:8]
print(json.dumps({"grossiere_ok": out["grossiere_ok"], "N2_tanh_ecart_max": out["N2_tanh_ecart_max"],
                  "N3_formule_ecart": out["N3_formule_ecart"], "nb_non_monotones": len(out["monotonie_rayon"]),
                  "non_monotones": out["monotonie_rayon"][:10], "plus_grands_ecarts_sup_moins_reel": pires,
                  "jouets": out["jouets"]}, indent=1))
tab = [d for d in out["sup_disque"] if d["kappa"] in (0.5, 2.0)]
for d in tab:
    print("N=%d q=%d kappa=%.2f sup=%.6f r(kappa)=%.6f ecart=%.2e |T|*=%.3f phi*=%.4f grossiere=%.6f" % (
        d["N"], d["q"], d["kappa"], d["sup"], d["r_reel"], d["ecart"], d["rayon_arg"], d["phi_arg"], d["grossiere"]))
