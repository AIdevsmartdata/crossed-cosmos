# Lemme QSigma : decroissance de c(0) - <v, Pi_m v> pour la boite B_m (projecteur sur d(1-formes portees par E_m)), m = 2..MMAX.
# Gradient conjugue sur le systeme normal (singulier mais compatible) D^T D a = D^T v, a porte par E_m. Bac a sable.
import numpy as np, json, time
T0 = time.time()
c0 = 1.1377494917
pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def run(m, tol=1e-13, maxit=20000):
    N = 2*m + 1                      # sites -m..m ; indice = x + m
    idx = np.arange(N)
    X = np.meshgrid(idx, idx, idx, idx, indexing="ij")
    inner = np.ones((N,)*4, bool)
    for a in range(4):
        inner &= (X[a] >= 1) & (X[a] <= N-2)        # B_{m-1}
    # lien (x, mu) existe si x_mu <= N-2 ; dans E_m si x ou x+e_mu dans B_{m-1}
    mask = []
    for mu in range(4):
        ex = X[mu] <= N-2
        up = np.zeros_like(inner); sl = [slice(None)]*4; sl2 = [slice(None)]*4
        sl[mu] = slice(0, N-1); sl2[mu] = slice(1, N)
        up[tuple(sl)] = inner[tuple(sl2)]
        mask.append(ex & (inner | up))
    def sh(A, mu, s):              # A(x + s e_mu), zero hors grille
        B = np.zeros_like(A); sl = [slice(None)]*4; sl2 = [slice(None)]*4
        if s == 1:
            sl[mu] = slice(0, N-1); sl2[mu] = slice(1, N)
        else:
            sl[mu] = slice(1, N); sl2[mu] = slice(0, N-1)
        B[tuple(sl)] = A[tuple(sl2)]; return B
    def Dop(A):                    # F_{mu nu}(x) = A_nu(x+e_mu) - A_nu(x) - A_mu(x+e_nu) + A_mu(x)
        return [sh(A[nu], mu, 1) - A[nu] - sh(A[mu], nu, 1) + A[mu] for (mu, nu) in pairs]
    def DT(F):
        A = [np.zeros((N,)*4) for _ in range(4)]
        for k, (mu, nu) in enumerate(pairs):
            A[nu] += sh(F[k], mu, -1) - F[k]
            A[mu] += -sh(F[k], nu, -1) + F[k]
        return [A[a]*mask[a] for a in range(4)]
    v = [np.zeros((N,)*4) for _ in pairs]
    v[3][m, m, m, m] = 1.0; v[3][m, m+1, m, m] = -1.0          # (0;12) - (e1;12)
    b = DT(v)
    x = [np.zeros_like(bb) for bb in b]
    r = [bb.copy() for bb in b]; p = [rr.copy() for rr in r]
    rs = sum((rr*rr).sum() for rr in r); rs0 = rs
    it = 0
    while it < maxit and rs > tol**2*rs0:
        Ap = DT(Dop(p))
        al = rs/sum((pp*aa).sum() for pp, aa in zip(p, Ap))
        x = [xx + al*pp for xx, pp in zip(x, p)]
        r = [rr - al*aa for rr, aa in zip(r, Ap)]
        rn = sum((rr*rr).sum() for rr in r)
        p = [rr + (rn/rs)*pp for rr, pp in zip(r, p)]
        rs = rn; it += 1
    Fx = Dop(x)
    val = sum((vv*ff).sum() for vv, ff in zip(v, Fx))
    return val, it
out = {"c0": c0, "rows": []}
for m in range(2, 19):
    val, it = run(m)
    out["rows"].append({"m": m, "vPi_v": val, "gap": c0 - val, "bound_408/(m-4)^2": (408/(m-4)**2 if m > 4 else None), "iters": it,
                        "t": round(time.time()-T0, 1)})
    if time.time() - T0 > 1700:
        break
rows = out["rows"]
for a, b2 in zip(rows, rows[1:]):
    if a["gap"] > 0 and b2["gap"] > 0:
        b2["local_slope"] = -np.log(b2["gap"]/a["gap"])/np.log(b2["m"]/a["m"])
print(json.dumps(out))
