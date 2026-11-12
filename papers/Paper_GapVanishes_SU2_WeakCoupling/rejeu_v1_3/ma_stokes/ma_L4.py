# Seconde implantation INDEPENDANTE du test de l'appendice de Stokes (app:stokes), ecrite a partir du seul texte de l'appendice
# et de PREREG_stokes.md (conventions, seuils). Auteur : agent de montage Sonnet 5.5, 12/11/2026. N'a pas lu le code d'Opus.
import itertools, random, json, sys, time
from collections import deque
import numpy as np

L = 4
NCONF = 100
SEED = 20261112
rng_py = random.Random(SEED)

def addv(x, mu, s): y = list(x); y[mu] += s; return tuple(y)
def inQ(x): return all(0 <= c <= L for c in x)

VERTS = list(itertools.product(range(L + 1), repeat=4))
LINKS = [(x, mu) for x in VERTS for mu in range(4) if x[mu] < L]
LID = {l: i for i, l in enumerate(LINKS)}

def stepinfo(x, y):
    d = [y[k] - x[k] for k in range(4)]
    nz = [k for k in range(4) if d[k]]
    assert len(nz) == 1 and abs(d[nz[0]]) == 1, (x, y)
    mu = nz[0]
    return (LID[(x, mu)], 1) if d[mu] == 1 else (LID[(y, mu)], -1)

# ---------- groupes : deux "algebres de test" avec la meme interface -------------
class Add:   # version additive exacte en entiers : un groupe abelien (Z^k), holonomie = vecteur d'entiers
    def __init__(self, nforms=20):
        r = np.random.default_rng(SEED)
        self.c = r.integers(-10**6, 10**6 + 1, size=(len(LINKS), nforms)).astype(object)  # python ints
        self.nf = nforms
    def one(self): return np.zeros(self.nf, dtype=object)
    def link(self, i, s): return self.c[i] if s == 1 else -self.c[i]
    def mul(self, a, b): return a + b
    def inv(self, a): return -a
    def dist(self, a, b): return int(max(abs(x) for x in (a - b)))

class SU2:
    def __init__(self, n, dtype=np.complex128):
        r = np.random.default_rng(SEED + 1)
        q = r.normal(size=(len(LINKS), n, 4)); q /= np.linalg.norm(q, axis=-1, keepdims=True)
        U = np.zeros((len(LINKS), n, 2, 2), dtype=dtype)
        U[..., 0, 0] = q[..., 0] + 1j * q[..., 1]; U[..., 0, 1] = q[..., 2] + 1j * q[..., 3]
        U[..., 1, 0] = -q[..., 2] + 1j * q[..., 3]; U[..., 1, 1] = q[..., 0] - 1j * q[..., 1]
        self.U = U; self.n = n
        self.Id = np.broadcast_to(np.eye(2, dtype=dtype), (n, 2, 2)).copy()
    def one(self): return self.Id
    def link(self, i, s): return self.U[i] if s == 1 else np.conj(np.swapaxes(self.U[i], -1, -2))
    def mul(self, a, b): return a @ b
    def inv(self, a): return np.conj(np.swapaxes(a, -1, -2))
    def dist(self, a, b): return float(np.max(np.linalg.norm((a - b).reshape(a.shape[0], 4), axis=1)))  # op-norm = Frobenius/sqrt2 for SU(2) diff? use below
    def dist_op(self, a, b):
        d = a - b
        s = np.linalg.svd(d, compute_uv=False)
        return float(np.max(s))

def hol(G, vs):
    h = G.one()
    for a, b in zip(vs, vs[1:]):
        i, s = stepinfo(a, b); h = G.mul(h, G.link(i, s))
    return h

def plaq(G, z, mu, nu):
    return G.mul(G.mul(G.link(LID[(z, mu)], 1), G.link(LID[(addv(z, mu, 1), nu)], 1)),
                 G.mul(G.link(LID[(addv(z, nu, 1), mu)], -1), G.link(LID[(z, nu)], -1)))

# ---------- l'algorithme de l'appendice ------------
def straight_down(v, j):
    """s_j(v) : de v a pi_j v, direction -e_j ; liste de sommets."""
    out = [v]
    while out[-1][j] > 0: out.append(addv(out[-1], j, -1))
    return out

def contract(loop, G, mode="normal", check_steps=False):
    """loop : liste de sommets, fermee. Renvoie la liste des carres (z, mu, nu, eps, V) dans l'ordre s=1..N, N, et le produit reconstitue.
    mode = 'normal' ou un temoin negatif : 'sign', 'omit', 'noT', 'rev'."""
    assert loop[0] == loop[-1]
    v0 = loop[0]
    # R : sommets de v0 a la base courante ; inner : sommets du lacet interieur
    R = [v0]; inner = list(loop)
    squares = []; N = 0
    Pprod = G.one()
    # etat du chemin complet pour les verifications pas a pas : R + inner + R^{-1}
    def full(R, pref, rest):
        # pref : sommets du prefixe (a partir de base), rest : sommets restants a partir du dernier de pref
        return R[:-1] + pref + rest[1:] + R[::-1][1:] if rest else R[:-1] + pref + R[::-1][1:]
    for j in range(4):
        base = inner[0]
        # prefixe : s_j(base) ... on part de s_j(base) s_j(base)^{-1} (retour de base inclus)
        sdown = straight_down(base, j)           # base -> pi base
        pref = list(sdown)                        # chemin jusqu'a pi base
        pref += sdown[::-1][1:]                   # s^{-1} : pi base -> base
        # pile des holonomies cumulees de R + pref
        full_pref = R[:-1] + pref                 # depuis v0
        st = [G.one()]
        for a, b in zip(full_pref, full_pref[1:]):
            i, s = stepinfo(a, b); st.append(G.mul(st[-1], G.link(i, s)))
        cur = full_pref                           # sommets
        # edges de inner
        edges = list(zip(inner, inner[1:]))
        nxt_inner = [sdown[-1]]
        for k, (v, w) in enumerate(edges):
            d = [w[m] - v[m] for m in range(4)]
            nz = [m for m in range(4) if d[m]]
            i_dir = nz[0]; eps = d[i_dir]
            h = v[j]
            assert cur[-1] == v
            if i_dir == j:
                # arete parallele : s(v)^{-1} e -> s(w)^{-1} (annulation successive, pas de carre)
                for _ in range(h): cur.pop(); st.pop()
                # maintenant cur[-1] = pi v ; remonter jusqu'a w = v +- e_j puis ... on ajoute s(w)^{-1}
                sw = straight_down(w, j)
                for u in sw[::-1][1:]:
                    i2, s2 = stepinfo(cur[-1], u); cur.append(u); st.append(G.mul(st[-1], G.link(i2, s2)))
                # pi e constante : pas d'arete dans le lacet projete
                continue
            # arete transverse : u_0 = (v,w) ; faire les carres r = 1..h dans cet ordre
            # chemin courant : cur (finit en v), puis P_{r-1} = d_1^v..d_{r-1}^v u_{r-1} (d_{r-1}^w)^{-1}..(d_1^w)^{-1}
            # On construit en place : on ajoute d_r^v, puis u_r ; le reste (d^w)^{-1} est stocke dans 'tail'
            tail = []      # liste de sommets de la queue (d^w)^{-1}...(d^1w)^{-1}, a partir de w^{(r-1)} vers w
            vr = v; wr = w
            for r in range(1, h + 1):
                vn = addv(vr, j, -1); wn = addv(wr, j, -1)
                # alpha = cur (finit en vr) ; C_r = u_{r-1} d^w_r u_r^{-1} (d^v_r)^{-1} depuis vr
                C = [vr, wr, wn, vn, vr]
                lo_i = min(v[i_dir], w[i_dir])
                z = list(vr); z[i_dir] = lo_i; z[j] = vr[j] - 1; z = tuple(z)
                tr = []
                for q_, x in enumerate(C):
                    tr.append(x)
                    if x == z: break
                # carre p_r : mu<nu = (min(i,j), max(i,j)), coin bas z
                mu, nu = (i_dir, j) if i_dir < j else (j, i_dir)
                e_sign = (-eps if i_dir < j else eps)
                squares.append((z, mu, nu, e_sign))
                N += 1
                # V_s = U(alpha) U(t_s)
                Ua = st[-1]
                Ut = hol(G, tr)
                V = G.mul(Ua, Ut)
                if mode == "noT": V = Ua
                Up = plaq(G, z, mu, nu)
                es = e_sign if mode != "sign" else -e_sign
                Up_e = Up if es == 1 else G.inv(Up)
                if mode != "omit":
                    term = G.mul(G.mul(V, Up_e), G.inv(V))
                    Pprod = G.mul(term, Pprod) if mode == "rev" else G.mul(Pprod, term)
                if check_steps:
                    pass
                # effectuer le remplacement : ajouter d_r^v au prefixe, la queue gagne d_r^w^{-1}
                i2, s2 = stepinfo(vr, vn); cur.append(vn); st.append(G.mul(st[-1], G.link(i2, s2)))
                tail.insert(0, wr)   # (d_r^w)^{-1} va de wn a wr : on stocke wr en tete
                vr, wr = vn, wn
            # maintenant : cur finit en v^{(h)}=pi v ; ajouter u_h = (vr, wr) puis la queue (d^w)^{-1}...
            i2, s2 = stepinfo(vr, wr); cur.append(wr); st.append(G.mul(st[-1], G.link(i2, s2)))
            for u in tail:
                i2, s2 = stepinfo(cur[-1], u); cur.append(u); st.append(G.mul(st[-1], G.link(i2, s2)))
            assert cur[-1] == w
            # annuler s(v)^{-1} s(v) : le prefixe contient s(v)^{-1} (h pas montants) suivi de s(v) (h pas descendants)
            # (le lacet 'inner' actuel contient deja pi e ; on retire les h aller-retours)
            # positions : les 2h sommets apres le sommet pi v au milieu de la jonction
            # le chemin cur = ... [pi v] up^h(=s(v)^-1) down^h(=d^v_1..d^v_h) [pi v] u_h ...
            # on enleve l'aller-retour
            # retrouver l'index de jonction : cur a la forme A + up + down + rest, avec len(up)=len(down)=h
            tot = len(cur)
            rest_len = 1 + len(tail)   # u_h + queue : nombre de pas apres la fin des d^v
            end_down = tot - 1 - rest_len           # index du dernier sommet des d^v (=pi v)
            start_up = end_down - 2 * h             # index du sommet pi v avant la montee
            assert cur[start_up] == cur[end_down]
            del cur[start_up + 1:end_down + 1]; del st[start_up + 1:end_down + 1]
            nxt_inner.append(wr_proj(w, j))
        # fin du balayage : cur finit en pi base + ... s^{-1}
        # nxt_inner = sommets projetes (avec doublons pour aretes constantes) ; supprimer les doublons consecutifs
        ninner = [nxt_inner[0]]
        for x in nxt_inner[1:]:
            if x != ninner[-1]: ninner.append(x)
        # le lacet projete part de pi base
        R = R + sdown[1:]
        inner = ninner if len(ninner) > 1 else [ninner[0]]
    # reste : R R^{-1} ; inner doit etre constant
    assert len(inner) == 1, inner
    return squares, N, Pprod

def wr_proj(w, j):
    y = list(w); y[j] = 0; return tuple(y)

def tree_loops(parent, order, root):
    # lacets c_e = (root ->T x) e (y ->T root) pour chaque lien et orientation
    def path_to(x):
        p = [x]
        while p[-1] != root: p.append(parent[p[-1]])
        return p[::-1]   # root -> x
    cache = {x: path_to(x) for x in VERTS}
    loops = []
    for (x, mu) in LINKS:
        y = addv(x, mu, 1)
        for (a, b) in ((x, y), (y, x)):
            loops.append(cache[a] + cache[b][::-1])
    return loops

def spanning_tree(kind, seed):
    r = random.Random(seed)
    root = (0,) * 4 if kind != "bfs_c" else tuple([L // 2] * 4)
    nb = lambda x: [addv(x, m, s) for m in range(4) for s in (1, -1) if inQ(addv(x, m, s))]
    parent = {root: root}
    if kind in ("bfs", "bfs_c"):
        dq = deque([root])
        while dq:
            x = dq.popleft()
            for y in nb(x):
                if y not in parent: parent[y] = x; dq.append(y)
    elif kind == "dfs":
        stack = [root]
        while stack:
            x = stack[-1]
            ns = [y for y in nb(x) if y not in parent]
            if not ns: stack.pop(); continue
            y = r.choice(ns); parent[y] = x; stack.append(y)
    elif kind == "kruskal":
        edges = [(x, addv(x, m, 1)) for (x, m) in LINKS]; r.shuffle(edges)
        uf = {x: x for x in VERTS}
        def f(x):
            while uf[x] != x: uf[x] = uf[uf[x]]; x = uf[x]
            return x
        adj = {x: [] for x in VERTS}
        for a, b in edges:
            if f(a) != f(b): uf[f(a)] = f(b); adj[a].append(b); adj[b].append(a)
        dq = deque([root])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in parent: parent[y] = x; dq.append(y)
    return parent, root

def all_closed_paths(base, length):
    out = []
    def rec(p):
        if len(p) - 1 == length:
            if p[-1] == base: out.append(list(p))
            return
        # elagage : distance de Manhattan restante
        rem = length - (len(p) - 1)
        if sum(abs(p[-1][k] - base[k]) for k in range(4)) > rem: return
        for m in range(4):
            for s in (1, -1):
                y = addv(p[-1], m, s)
                if inQ(y): p.append(y); rec(p); p.pop()
    rec([base]); return out

def rand_closed(r, maxlen=16):
    x = tuple(r.randrange(L + 1) for _ in range(4)); p = [x]
    n = r.randrange(1, maxlen // 2 + 1)
    while len(p) - 1 < n:
        m = r.randrange(4); s = r.choice((1, -1)); y = addv(p[-1], m, s)
        if inQ(y): p.append(y)
    # retour par plus court chemin aleatoire
    while p[-1] != p[0]:
        cand = []
        for m in range(4):
            if p[-1][m] != p[0][m]: cand.append(m)
        m = r.choice(cand); s = 1 if p[0][m] > p[-1][m] else -1
        p.append(addv(p[-1], m, s))
    return p

def counts_formula(loop):
    # (St.2) : somme sur j, sur les aretes du lacet projete lambda_j transverses a j, de la coordonnee j de depart
    N = 0
    lam = list(loop)
    for j in range(4):
        for a, b in zip(lam, lam[1:]):
            d = [b[k] - a[k] for k in range(4)]
            nz = [k for k in range(4) if d[k]]
            if nz and nz[0] != j: N += a[j]
        lam2 = []
        for x in lam:
            y = list(x); y[j] = 0; y = tuple(y)
            if not lam2 or lam2[-1] != y: lam2.append(y)
        lam = lam2
    return N

def run():
    t0 = time.time()
    res = {"L": L, "nconf": NCONF}
    loops = []
    base_list = [(0,) * 4, (1,) * 4]
    for base in base_list:
        for ln in (2, 4, 6): loops += [("closed%d" % ln, p) for p in all_closed_paths(base, ln)]
    r = random.Random(SEED); loops += [("rand", rand_closed(r)) for _ in range(1000)]
    for kind in ("bfs", "bfs_c", "kruskal"):
        par, root = spanning_tree(kind, SEED)
        loops += [("tree_" + kind, l) for l in tree_loops(par, None, root)]
    res["nloops"] = len(loops)
    # ---- ADD : exact ----
    A = Add(); worst_add = 0; nbad = 0; Nmax = {}; viol_count = 0; viol_box = 0; viol_N = 0
    famN = {}
    for fam, lp in loops:
        sq, N, P = contract(lp, A)
        # equation exacte : holonomie du lacet = somme eps * dc
        direct = hol(A, lp)
        dd = A.dist(direct, P)
        worst_add = max(worst_add, dd)
        if dd != 0: nbad += 1
        # carres dans la boite
        for (z, mu, nu, e) in sq:
            for c in (z, addv(z, mu, 1), addv(z, nu, 1), addv(addv(z, mu, 1), nu, 1)):
                if not inQ(c): viol_box += 1
        if N != counts_formula(lp): viol_count += 1
        ell = [0] * 4
        for a, b in zip(lp, lp[1:]):
            for k in range(4):
                if a[k] != b[k]: ell[k] += 1
        if N > L * sum(i * ell[i] for i in range(4)): viol_N += 1
        famN[fam] = max(famN.get(fam, 0), N)
    res["ADD"] = {"ecart_max": worst_add, "boucles_en_ecart": nbad, "violation_compte_St2": viol_count, "carres_hors_boite": viol_box,
                  "N>L*sum(i*l_i)": viol_N, "Nmax_par_famille": famN}
    # temoins negatifs additifs
    neg = {}
    for mode in ("sign", "omit", "noT", "rev"):
        bad = 0; tot = 0
        for fam, lp in loops[: 3000]:
            sq, N, P = contract(lp, A, mode=mode)
            tot += 1
            if A.dist(hol(A, lp), P) != 0: bad += 1
        neg[mode] = [bad, tot]
    res["ADD_temoins_negatifs(detectes/total)"] = neg
    print(json.dumps(res, default=str), flush=True)
    # ---- SU(2) ----
    S = SU2(NCONF)
    worst = {}
    nstep = 0
    for fam, lp in loops:
        if fam.startswith("tree_dfs"): continue   # reprises separement
        sq, N, P = contract(lp, S)
        d = S.dist_op(hol(S, lp), P)
        worst[fam] = max(worst.get(fam, 0.0), d)
    res["SU2_double"] = {"residu_max_par_famille": worst, "residu_max": max(worst.values())}
    # temoins negatifs SU(2)
    neg = {}
    S2 = SU2(50)
    for mode in ("sign", "omit", "noT", "rev"):
        vals = []
        for fam, lp in loops[: 3000: 7]:
            sq, N, P = contract(lp, S2, mode=mode)
            vals.append(S2.dist_op(hol(S2, lp), P))
        neg[mode] = {"max": max(vals), "median": float(np.median(vals)), "frac>1e-3": float(np.mean(np.array(vals) > 1e-3))}
    res["SU2_temoins_negatifs"] = neg
    res["temps_s"] = time.time() - t0
    print("FINAL " + json.dumps(res, default=str), flush=True)

run()
