# ---- stokes_lib.py : exécution littérale de l'appendice app:stokes de la note v1.2 (12/11/2026) ----
# Conventions : voir PREREG_stokes.md. Ce fichier est concaténé en tête de chaque lancement (le bac à sable ne prend qu'un fichier).
import itertools, random, json, sys, time
import numpy as np

def setup(Lbox):
    global L, VERTS, LINKS, LID, NV
    L = Lbox
    VERTS = list(itertools.product(range(L + 1), repeat=4))
    LINKS = [(x, mu) for x in VERTS for mu in range(4) if x[mu] < L]
    LID = {l: i for i, l in enumerate(LINKS)}
    NV = len(VERTS)

def add(x, mu, s):
    y = list(x); y[mu] += s; return tuple(y)

def inbox(x):
    return all(0 <= c <= L for c in x)

def step(x, y):
    """(indice du lien, signe) pour le pas x -> y."""
    d = [y[k] - x[k] for k in range(4)]
    nz = [k for k in range(4) if d[k] != 0]
    if not (len(nz) == 1 and abs(d[nz[0]]) == 1):
        raise ValueError("pas non élémentaire %r -> %r" % (x, y))
    mu = nz[0]
    if d[mu] == 1:
        return LID[(x, mu)], +1
    return LID[(y, mu)], -1

def is_path(P):
    for a, b in zip(P, P[1:]):
        step(a, b)
        if not (inbox(a) and inbox(b)):
            return False
    return True

def free_reduce(P):
    """Réduction libre (suppression des allers-retours) d'un chemin donné par ses sommets."""
    out = []
    for v in P:
        if len(out) >= 2 and out[-2] == v:
            out.pop()
        else:
            out.append(v)
    return out

def plaq_path(z, mu, nu):
    a = add(z, mu, 1); b = add(a, nu, 1); c = add(z, nu, 1)
    return [z, a, b, c, z]

def s_down(v, j):
    P = [v]; x = v
    while x[j] > 0:
        x = add(x, j, -1); P.append(x)
    return P

def proj(v, j):
    y = list(v); y[j] = 0; return tuple(y)

# ------------------------------------------------------------------------------------------------------------
# L'algorithme de l'appendice, exécuté sur le chemin GLOBAL G (liste littérale de sommets).
# Chaque remplacement élémentaire enregistre : la plaquette p_s = (z, mu, nu), le signe eps_s, le préfixe littéral alpha_s
# (= G[:idx+1] au moment du remplacement), le chemin t_s, le carré C_s, l'ancien et le nouveau chemin (si demandé).
# ------------------------------------------------------------------------------------------------------------
class Rec:
    __slots__ = ("p", "eps", "alpha", "t", "C", "Gold", "Gnew", "S_list", "tail")

def decompose(gamma, keep_paths=False, mutate=None):
    """gamma : boucle (liste de sommets, gamma[0] == gamma[-1]).
    Renvoie (records, events, info). events = liste d'opérations sans carré (allers-retours) avec (Gold, Gnew) si keep_paths."""
    assert gamma[0] == gamma[-1]
    assert is_path(gamma)
    v0 = gamma[0]
    R = [v0]
    lam = list(gamma)
    G = list(gamma)
    recs, events = [], []
    info = {"t_const": 0, "t_len": {}, "outside": 0, "Nformula": 0}
    for j in range(4):
        assert G == R + lam[1:] + R[::-1][1:], "invariant des balayages violé avant le balayage %d" % j
        u = lam
        q = len(u) - 1
        u0 = u[0]
        sd0 = s_down(u0, j)
        pos = len(R) - 1                       # indice de u0 dans G
        Gold = G
        G = G[:pos] + sd0 + sd0[::-1][1:] + G[pos + 1:]   # insertion de l'aller-retour s_j(u0) s_j(u0)^{-1}
        if keep_paths:
            events.append(("insert", Gold, list(G)))
        S_list = R[:-1] + sd0                  # partie stable : R . s_j(u0) . (arêtes projetées) ; finit en pi_j u_k
        cur = pos + 2 * (len(sd0) - 1)         # indice de u_k (= u0) dans G
        assert G[cur] == u0
        for k in range(q):
            uk, uk1 = u[k], u[k + 1]
            assert G[cur] == uk and G[cur + 1] == uk1, "arête courante mal placée"
            d = [uk1[m] - uk[m] for m in range(4)]
            i = [m for m in range(4) if d[m] != 0][0]
            sig = d[i]
            h = uk[j]
            sdk = s_down(uk, j)
            tail0 = sdk[::-1]                  # s_j(u_k)^{-1} : de pi_j u_k à u_k
            assert G[:cur + 1] == S_list[:-1] + tail0, "préfixe littéral différent de partie stable + s_j(u_k)^{-1}"
            if i != j:
                # arête transverse : h carrés, dans l'ordre r = 1..h
                idx = cur
                for r in range(1, h + 1):
                    vr1 = add(uk, j, -(r - 1)); wr1 = add(uk1, j, -(r - 1))
                    vr = add(uk, j, -r); wr = add(uk1, j, -r)
                    assert G[idx] == vr1 and G[idx + 1] == wr1
                    Gold = G
                    alpha = G[:idx + 1]
                    G = G[:idx] + [vr1, vr, wr, wr1] + G[idx + 2:]
                    C = [vr1, wr1, wr, vr, vr1]
                    z = list(vr); z[i] = min(vr[i], wr[i]); z = tuple(z)   # coin inférieur dans les coordonnées (i, j)
                    for x in C:
                        if not inbox(x):
                            info["outside"] += 1
                    k0 = C.index(z)                # premier passage en z_r
                    t = C[:k0 + 1]
                    if k0 == 0:
                        info["t_const"] += 1
                    info["t_len"][k0] = info["t_len"].get(k0, 0) + 1
                    mu, nu = min(i, j), max(i, j)
                    eps = -sig if i < j else sig
                    rec = Rec()
                    rec.p = (z, mu, nu); rec.eps = eps; rec.alpha = alpha; rec.t = t; rec.C = C
                    rec.S_list = S_list; rec.tail = tail0 + [add(uk, j, -m) for m in range(1, r)]
                    assert alpha == S_list[:-1] + rec.tail, "préfixe alpha_s différent de sa décomposition"
                    rec.Gold = Gold if keep_paths else None
                    rec.Gnew = list(G) if keep_paths else None
                    recs.append(rec)
                    idx += 1
                # suppression de s_j(u_k)^{-1} s_j(u_k) autour de u_k (indice cur)
                Gold = G
                for _ in range(h):
                    assert G[cur - 1] == G[cur + 1]
                    G = G[:cur] + G[cur + 2:]
                    cur -= 1
                if keep_paths and h > 0:
                    events.append(("cancel", Gold, list(G)))
                # maintenant G[cur] = pi_j u_k, puis pi_j u_{k+1}, puis s_j(u_{k+1})^{-1}
                S_list = S_list + [proj(uk1, j)]
                cur = cur + 1 + h
                assert G[cur] == uk1
            else:
                # arête parallèle à j : remplacée par s_j(u_k) s_j(u_{k+1})^{-1}, sans carré
                Gold = G
                G = G[:cur] + sdk + s_down(uk1, j)[::-1][1:] + G[cur + 2:]
                if keep_paths:
                    events.append(("parallel", Gold, list(G)))
                Gold = G
                hh = len(sdk) - 1
                for _ in range(hh):
                    assert G[cur - 1] == G[cur + 1]
                    G = G[:cur] + G[cur + 2:]
                    cur -= 1
                if keep_paths and hh > 0:
                    events.append(("cancel", Gold, list(G)))
                cur = cur + (uk1[j])            # remonte de pi_j u_{k+1} à u_{k+1}
                assert G[cur] == uk1
        # fin du balayage j : R_{j+1} = R_j s_j(u0), lambda_{j+1} = pi_j lambda_j (arêtes constantes supprimées)
        Rn = R + sd0[1:]
        lp = [proj(x, j) for x in u]
        ln = [lp[0]]
        for x in lp[1:]:
            if x != ln[-1]:
                ln.append(x)
        R, lam = Rn, ln
        assert G == R + lam[1:] + R[::-1][1:], "invariant des balayages violé après le balayage %d" % j
    assert lam == [(0, 0, 0, 0)], "la boucle intérieure n'est pas constante après 4 balayages"
    assert free_reduce(G) == [v0], "le chemin final ne se réduit pas au chemin vide"
    return recs, events, info

def N_formula(gamma):
    """Première ligne de (St.2) : somme sur j des coordonnées j de départ des arêtes transverses de lambda_j."""
    lam = list(gamma); N = 0
    for j in range(4):
        for a, b in zip(lam, lam[1:]):
            d = [b[m] - a[m] for m in range(4)]
            i = [m for m in range(4) if d[m] != 0][0]
            if i != j:
                N += a[j]
        lp = [proj(x, j) for x in lam]
        ln = [lp[0]]
        for x in lp[1:]:
            if x != ln[-1]:
                ln.append(x)
        lam = ln
    return N

def dir_counts(gamma):
    c = [0, 0, 0, 0]
    for a, b in zip(gamma, gamma[1:]):
        d = [b[m] - a[m] for m in range(4)]
        c[[m for m in range(4) if d[m] != 0][0]] += 1
    return c

# ------------------------------------------------------------------------------------------------------------
# Additif (entiers exacts)
# ------------------------------------------------------------------------------------------------------------
def path_int(P, c):
    s = 0
    for a, b in zip(P, P[1:]):
        l, sg = step(a, b)
        s += sg * c[l]
    return s

def curl(p, c):
    z, mu, nu = p
    return path_int(plaq_path(z, mu, nu), c)

# ------------------------------------------------------------------------------------------------------------
# SU(2) : U = [[A, B], [-conj(B), conj(A)]] ; tableaux sur les configurations
# ------------------------------------------------------------------------------------------------------------
def haar(nconf, rng, dtype=np.float64):
    x = rng.standard_normal((len(LINKS), nconf, 4))
    x /= np.sqrt((x ** 2).sum(axis=2, keepdims=True))
    ct = np.complex128 if dtype == np.float64 else np.clongdouble
    x = x.astype(dtype)
    A = (x[..., 0] + 1j * x[..., 3]).astype(ct)
    B = (x[..., 2] + 1j * x[..., 1]).astype(ct)
    return A, B

def mul(X, Y):
    A1, B1 = X; A2, B2 = Y
    return (A1 * A2 - B1 * np.conj(B2), A1 * B2 + B1 * np.conj(A2))

def inv(X):
    A, B = X
    return (np.conj(A), -B)

def ident(nconf, ct):
    return (np.ones(nconf, dtype=ct), np.zeros(nconf, dtype=ct))

def link_step(cfg, a, b):
    l, sg = step(a, b)
    X = (cfg[0][l], cfg[1][l])
    return X if sg == 1 else inv(X)

def hol(P, cfg):
    nconf = cfg[0].shape[1]
    X = ident(nconf, cfg[0].dtype)
    for a, b in zip(P, P[1:]):
        X = mul(X, link_step(cfg, a, b))
    return X

def opnorm_diff(X, Y):
    return np.sqrt(np.abs(X[0] - Y[0]) ** 2 + np.abs(X[1] - Y[1]) ** 2)

def plaq_table(cfg):
    T = {}
    for (x, mu) in LINKS:
        pass
    for z in VERTS:
        for mu in range(4):
            for nu in range(mu + 1, 4):
                if z[mu] < L and z[nu] < L:
                    T[(z, mu, nu)] = hol(plaq_path(z, mu, nu), cfg)
    return T

def check_su2(gamma, recs, cfg, PT, mutant=None):
    """Résidu max sur les configurations de U(gamma) - prod_s V_s U_p^eps V_s^{-1}, V_s = U(alpha_s) U(t_s).
    U(alpha_s) = U(partie stable) . U(queue littérale) ; la partie stable est mise à jour arête par arête, et l'on VÉRIFIE
    que la nouvelle partie stable prolonge littéralement l'ancienne d'un sommet (sinon recalcul complet)."""
    nconf = cfg[0].shape[1]
    ct = cfg[0].dtype
    Ug = hol(gamma, cfg)
    prod = ident(nconf, ct)
    prev_list, prev_hol = None, None
    order = list(range(len(recs)))
    if mutant == "reverse":
        order = order[::-1]
    for s in order:
        rc = recs[s]
        Sl = rc.S_list
        if Sl is not prev_list:
            if prev_list is not None and len(Sl) == len(prev_list) + 1 and Sl[:-1] == prev_list:
                prev_hol = mul(prev_hol, link_step(cfg, prev_list[-1], Sl[-1]))
            else:
                prev_hol = hol(Sl, cfg)
            prev_list = Sl
        Ua = mul(prev_hol, hol(rc.tail, cfg)) if len(rc.tail) > 1 else prev_hol
        V = Ua if mutant == "no_t" else mul(Ua, hol(rc.t, cfg))
        Up = PT[rc.p]
        e = rc.eps
        if mutant == "flip" and s == len(recs) // 2:
            e = -e
        if mutant == "drop" and s == len(recs) // 2:
            continue
        F = Up if e == 1 else inv(Up)
        prod = mul(prod, mul(mul(V, F), inv(V)))
    return float(np.max(opnorm_diff(Ug, prod)))

def check_steps(recs, events, cfg):
    """Contrôle pas à pas littéral : U(Gold) = V U_p^eps V^{-1} U(Gnew) à chaque carré ; U inchangé à chaque aller-retour."""
    worst = 0.0
    for rc in recs:
        V = mul(hol(rc.alpha, cfg), hol(rc.t, cfg))
        z, mu, nu = rc.p
        Up = hol(plaq_path(z, mu, nu), cfg)
        F = Up if rc.eps == 1 else inv(Up)
        lhs = hol(rc.Gold, cfg)
        rhs = mul(mul(mul(V, F), inv(V)), hol(rc.Gnew, cfg))
        worst = max(worst, float(np.max(opnorm_diff(lhs, rhs))))
        # identité de rotation : U(C) = U(t) U_p^eps U(t)^{-1}
        UC = hol(rc.C, cfg)
        Ut = hol(rc.t, cfg)
        worst = max(worst, float(np.max(opnorm_diff(UC, mul(mul(Ut, F), inv(Ut))))))
    for kind, Go, Gn in events:
        worst = max(worst, float(np.max(opnorm_diff(hol(Go, cfg), hol(Gn, cfg)))))
    return worst

def delta(X):
    return np.arccos(np.clip(np.real(X[0]), -1.0, 1.0))

# ------------------------------------------------------------------------------------------------------------
# Boucles
# ------------------------------------------------------------------------------------------------------------
def nbrs(x):
    out = []
    for mu in range(4):
        for s in (1, -1):
            y = add(x, mu, s)
            if inbox(y):
                out.append(y)
    return out

def closed_walks(base, maxlen):
    res = []
    def rec(P):
        if len(P) - 1 > 0 and P[-1] == base:
            res.append(list(P))
        if len(P) - 1 == maxlen:
            return
        # élagage : il faut pouvoir revenir
        rem = maxlen - (len(P) - 1)
        for y in nbrs(P[-1]):
            dist = sum(abs(y[m] - base[m]) for m in range(4))
            if dist <= rem - 1:
                P.append(y); rec(P); P.pop()
    rec([base])
    return res

def tree_paths(parent, root):
    """chemin de la racine à x dans l'arbre (liste de sommets)."""
    memo = {root: [root]}
    def path(x):
        if x in memo:
            return memo[x]
        p = path(parent[x]) + [x]
        memo[x] = p
        return p
    return path

def tree_loops(parent, root):
    path = tree_paths(parent, root)
    loops = []
    for (x, mu) in LINKS:
        y = add(x, mu, 1)
        for (a, b) in ((x, y), (y, x)):
            loops.append(path(a) + path(b)[::-1])
    return loops

def tree_note(n):
    """T1 : chaînes temporelles T_I + arbre BFS de la coquille T_S (racine = centre de la face inférieure). Boîte [0,2n]^4."""
    c = n
    def shell(x):
        return max(abs(x[m] - c) for m in range(4)) == n
    root = (0, c, c, c)
    parent = {}
    # BFS de la coquille
    from collections import deque
    seen = {root}; dq = deque([root])
    while dq:
        x = dq.popleft()
        for y in nbrs(x):
            if shell(y) and y not in seen:
                seen.add(y); parent[y] = x; dq.append(y)
    # chaînes temporelles : (t, xb) -> (t+1, xb) pour |xb - c| <= n-1, t de 0 à 2n-2
    for x in VERTS:
        if not shell(x):
            assert x[0] >= 1
            parent[x] = add(x, 0, -1)
    assert len(parent) == NV - 1
    return parent, root

def tree_random(rng_py):
    edges = [(x, add(x, mu, 1)) for (x, mu) in LINKS]
    rng_py.shuffle(edges)
    uf = {v: v for v in VERTS}
    def find(a):
        while uf[a] != a:
            uf[a] = uf[uf[a]]; a = uf[a]
        return a
    adj = {v: [] for v in VERTS}
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            uf[ra] = rb; adj[a].append(b); adj[b].append(a)
    root = VERTS[rng_py.randrange(NV)]
    parent = {}; stack = [root]; seen = {root}
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); parent[y] = x; stack.append(y)
    assert len(parent) == NV - 1
    return parent, root

def tree_dfs(rng_py):
    root = VERTS[rng_py.randrange(NV)]
    parent = {}; seen = {root}
    sys.setrecursionlimit(100000)
    stack = [(root, iter(sorted(nbrs(root), key=lambda _: rng_py.random())))]
    while stack:
        x, it = stack[-1]
        nxt = None
        for y in it:
            if y not in seen:
                nxt = y; break
        if nxt is None:
            stack.pop(); continue
        seen.add(nxt); parent[nxt] = x
        stack.append((nxt, iter(sorted(nbrs(nxt), key=lambda _: rng_py.random()))))
    assert len(parent) == NV - 1
    return parent, root

def random_loops(m, rng_py):
    out = []
    while len(out) < m:
        base = VERTS[rng_py.randrange(NV)]
        k = rng_py.randint(1, 8)
        P = [base]
        for _ in range(k):
            P.append(rng_py.choice(nbrs(P[-1])))
        # retour par un plus court chemin aléatoire
        x = P[-1]
        while x != base:
            moves = []
            for mu in range(4):
                if x[mu] < base[mu]: moves.append((mu, 1))
                if x[mu] > base[mu]: moves.append((mu, -1))
            mu, s = rng_py.choice(moves)
            x = add(x, mu, s); P.append(x)
        if len(P) >= 3:
            out.append(P)
    return out

# ======================= RUN 1 : additif exact, comptes, boîte, témoins négatifs ; arbre court n = 1..5 =======================
T0 = time.time()
out = {"run": "run1_additif_comptes", "eps_longdouble": float(np.finfo(np.longdouble).eps)}
setup(2)
rng_py = random.Random(20261112)
fams = {}
fams["exh_0000"] = closed_walks((0, 0, 0, 0), 6)
fams["exh_1111"] = closed_walks((1, 1, 1, 1), 6)
P1, r1 = tree_note(1); P2, r2 = tree_random(random.Random(7)); P3, r3 = tree_dfs(random.Random(11))
fams["tree_T1_note"] = tree_loops(P1, r1)
fams["tree_T2_random"] = tree_loops(P2, r2)
fams["tree_T3_dfs"] = tree_loops(P3, r3)
fams["random16"] = random_loops(1000, random.Random(99))
forms = [[rng_py.randint(-10**6, 10**6) for _ in LINKS] for _ in range(20)]
Vn = (L + 1) ** 4
An = 6 * L * L * (2 * Vn - 1)
summ = {}
first_fail = None
for name, loops in fams.items():
    st = {"loops": len(loops), "add_fail": 0, "count_fail": 0, "N_gt_3Ll": 0, "N_gt_An": 0, "len_gt_2V-1": 0,
          "outside": 0, "t_const": 0, "t_len": {}, "maxN": 0, "maxlen": 0, "N_zero": 0}
    for g in loops:
        recs, ev, info = decompose(g)
        N = len(recs)
        st["maxN"] = max(st["maxN"], N); st["maxlen"] = max(st["maxlen"], len(g) - 1)
        if N == 0: st["N_zero"] += 1
        st["outside"] += info["outside"]; st["t_const"] += info["t_const"]
        for k, v in info["t_len"].items():
            st["t_len"][k] = st["t_len"].get(k, 0) + v
        if N != N_formula(g):
            st["count_fail"] += 1
        dc = dir_counts(g)
        if N > L * sum(i * dc[i] for i in range(4)) or N > 3 * L * (len(g) - 1):
            st["N_gt_3Ll"] += 1
        if name.startswith("tree"):
            if len(g) - 1 > 2 * Vn - 1: st["len_gt_2V-1"] += 1
            if N > An: st["N_gt_An"] += 1
        for c in forms:
            lhs = path_int(g, c)
            rhs = sum(rc.eps * curl(rc.p, c) for rc in recs)
            if lhs != rhs:
                st["add_fail"] += 1
                if first_fail is None:
                    first_fail = {"family": name, "loop": g, "lhs": lhs, "rhs": rhs}
                break
    st["t_len"] = {str(k): v for k, v in sorted(st["t_len"].items())}
    summ[name] = st
out["L=2"] = summ
out["A_n(L=2)"] = An
out["first_additive_failure"] = first_fail
# témoins négatifs additifs (doivent échouer)
neg = {"flip": 0, "drop": 0, "tested": 0}
for g in fams["tree_T3_dfs"][:200] + fams["random16"][:200]:
    recs, ev, info = decompose(g)
    if len(recs) == 0:
        continue
    neg["tested"] += 1
    c = forms[0]
    lhs = path_int(g, c)
    s = len(recs) // 2
    rhs_flip = sum((-rc.eps if k == s else rc.eps) * curl(rc.p, c) for k, rc in enumerate(recs))
    rhs_drop = sum(rc.eps * curl(rc.p, c) for k, rc in enumerate(recs) if k != s)
    neg["flip"] += (lhs != rhs_flip); neg["drop"] += (lhs != rhs_drop)
out["negative_controls_additive_detected"] = neg
out["t_run1a"] = round(time.time() - T0, 1)

# ---- arbre court T1 (chaînes temporelles + BFS de coquille) pour n = 1..5 : longueur des boucles d'arbre et N (formule) ----
short = {}
for n in range(1, 6):
    setup(2 * n)
    P, r = tree_note(n)
    path = tree_paths(P, r)
    maxlen = 0; maxN = 0; depth = 0
    for x in VERTS:
        depth = max(depth, len(path(x)) - 1)
    for (x, mu) in LINKS:
        y = add(x, mu, 1)
        for (a, b) in ((x, y), (y, x)):
            g = path(a) + path(b)[::-1]
            maxlen = max(maxlen, len(g) - 1)
            maxN = max(maxN, N_formula(g))
    short[n] = {"depth": depth, "max_loop_len": maxlen, "bound_14n-1": 14 * n - 1, "max_N": maxN,
                "bound_6n(14n-1)": 6 * n * (14 * n - 1), "A_n_note": 6 * (2 * n) ** 2 * (2 * (2 * n + 1) ** 4 - 1)}
    if time.time() - T0 > 420:
        break
out["short_tree"] = short
# ---- n = 2 : algorithme littéral sur toutes les boucles de T1, compte = formule et additif exact ----
setup(4)
P, r = tree_note(2)
loops = tree_loops(P, r)
f2 = [random.Random(5).randint(-10**6, 10**6) for _ in LINKS]
bad = 0; badc = 0; outside = 0; done = 0
for g in loops:
    recs, ev, info = decompose(g)
    outside += info["outside"]
    if len(recs) != N_formula(g): badc += 1
    if path_int(g, f2) != sum(rc.eps * curl(rc.p, f2) for rc in recs): bad += 1
    done += 1
    if time.time() - T0 > 560:
        break
out["n2_T1_literal"] = {"loops_done": done, "of": len(loops), "count_fail": badc, "add_fail": bad, "outside": outside}
out["t_total"] = round(time.time() - T0, 1)
print(json.dumps(out))
