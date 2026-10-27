#!/usr/bin/env python3
"""Contrôle indépendant — recalcul EXACT des coefficients E_j(α) du certificat géodésique.

Aucun import du code du certificat. Aucune quadrature, aucune arb_series : arithmétique rationnelle exacte (fractions).
Méthode :
 1. séries p_n, h_n, m_n re-dérivées des EDO par résolution d'un SYSTÈME LINÉAIRE (Gauss en rationnels) à chaque ordre
      p : (1-x²)p_n' - 3x p_n - m_n = -x δ_{n0} - (1-x²) p_{n-1}
      h : (1-x²)h_n'' - 5x h_n' - 3 h_n = -δ_{n0} - (1-x²) h_{n-1}' + x h_{n-1}
 2. A(κ) = (3/2)|∇ψ_N|² + (1-s²)/6 écrit comme  c²·Q_cc + cσ·Q_cs + σ²·Q_ss + Q_1, chaque Q = f0(x) + y f1(x) + y² f2(x)
    (c = cos α, σ = sin α, s = c x + σ y) ;
 3. moments EXACTS  M_{a,b}(c,σ) = ∫_{-1}^1∫_{-1}^1 x^a y^b ds dτ,  x = c s - σ t, y = σ s + c t, t = √(1-s²) τ,
    via ∫∫ s^m t^n = [m,n pairs] · 2/(n+1) · B((m+1)/2, n/2+1)  (rationnel) ;
 4. I_j(c) = Λ(Σ_{i≤min(j,2N)} A_i x^{j-i}/(j-i)!), puis σ² → 1 - c² : I_j ∈ ℚ[c] EXACT ;
    E_j(c) = I_j(c) - (8/(9π))·π/(4^k k!(k+1)!) [j = 2k] = I_j(c) - 8/(9·4^k k!(k+1)!)  ∈ ℚ[c].
Sortie : JSON {j: [coefficients rationnels de E_j en puissances croissantes de c]}.
"""
import sys, json, time
from fractions import Fraction as F
from math import comb, factorial

# ---------- polynômes univariés (listes, puissances croissantes) ----------
def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0: a.pop()
    return a
def padd(*ps):
    n = max(len(p) for p in ps); r = [F(0)] * n
    for p in ps:
        for i, c in enumerate(p): r[i] += c
    return r
def pmul(a, b):
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def psc(k, a): return [k * c for c in a]
def pder(a): return [i * a[i] for i in range(1, len(a))] or [F(0)]
X = [F(0), F(1)]; ONE_M_X2 = [F(1), F(0), F(-1)]

def gauss_solve(Amat, b):
    n = len(Amat); m = len(Amat[0])
    M = [row[:] + [bb] for row, bb in zip(Amat, b)]
    piv_cols = []; r = 0
    for col in range(m):
        pr = next((i for i in range(r, n) if M[i][col] != 0), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for i in range(n):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [vi - f * vr for vi, vr in zip(M[i], M[r])]
        piv_cols.append(col); r += 1
    assert r == m, ("système singulier", r, m)
    for i in range(r, n): assert M[i][-1] == 0, "système incompatible"
    sol = [F(0)] * m
    for i, col in enumerate(piv_cols): sol[col] = M[i][-1]
    return sol

def series(N):
    P, H, M = [], [], []
    for n in range(N + 1):
        # --- p_n : inconnues a_0..a_n, m_n ; équations sur x^0..x^{n+1}
        rhs = [F(0), F(-1)] if n == 0 else psc(-1, pmul(ONE_M_X2, P[n - 1]))
        assert all(c == 0 for c in rhs[n + 2:]), 'degré rhs p'
        rhs = (rhs + [F(0)] * (n + 2))[:n + 2]
        cols = []
        for k in range(n + 1):
            e = [F(0)] * (n + 2)
            dk = [F(0)] * (k + 1); dk[k] = F(1)
            img = padd(pmul(ONE_M_X2, pder(dk)), psc(-3, pmul(X, dk)))
            for i, c in enumerate(img):
                if c != 0: e[i] += c
            cols.append(e)
        em = [F(0)] * (n + 2); em[0] = F(-1); cols.append(em)
        Amat = [[cols[c][r] for c in range(n + 2)] for r in range(n + 2)]
        sol = gauss_solve(Amat, rhs[:n + 2])
        P.append(sol[:n + 1]); M.append(sol[n + 1])
        # contrôle : résidu exact nul
        chk = padd(pmul(ONE_M_X2, pder(P[n])), psc(-3, pmul(X, P[n])), [-M[n]], psc(-1, rhs))
        assert all(c == 0 for c in chk)
        # --- h_n : inconnues b_0..b_n
        rh = [F(-1)] if n == 0 else padd(psc(-1, pmul(ONE_M_X2, pder(H[n - 1]))), pmul(X, H[n - 1]))
        assert all(c == 0 for c in rh[n + 1:]), 'degré rhs h'
        rh = (rh + [F(0)] * (n + 1))[:n + 1]
        cols = []
        for k in range(n + 1):
            dk = [F(0)] * (k + 1); dk[k] = F(1)
            img = padd(pmul(ONE_M_X2, pder(pder(dk))), psc(-5, pmul(X, pder(dk))), psc(-3, dk))
            e = [F(0)] * (n + 1)
            for i, c in enumerate(img):
                if c != 0: e[i] += c
            cols.append(e)
        Amat = [[cols[c][r] for c in range(n + 1)] for r in range(n + 1)]
        H.append(gauss_solve(Amat, rh))
        chk = padd(pmul(ONE_M_X2, pder(pder(H[n]))), psc(-5, pmul(X, pder(H[n]))), psc(-3, H[n]), psc(-1, rh))
        assert all(c == 0 for c in chk)
    return P, H, M

# ---------- A_i structuré : dict (pref, b) -> poly en x ; pref ∈ {cc, cs, ss, 1} ----------
def build_A(N):
    P, H, M = series(N)
    HD = [pder(h) for h in H]
    A = []
    for i in range(2 * N + 1):
        rng = [(a, i - a) for a in range(max(0, i - N), min(i, N) + 1)]
        pp = padd([F(0)], *[pmul(P[a], P[b]) for a, b in rng])
        phd = padd([F(0)], *[pmul(P[a], HD[b]) for a, b in rng])
        hp = padd([F(0)], *[pmul(H[a], P[b]) for a, b in rng])
        hdhd = padd([F(0)], *[pmul(HD[a], HD[b]) for a, b in rng])
        hh = padd([F(0)], *[pmul(H[a], H[b]) for a, b in rng])
        hhd = padd([F(0)], *[pmul(H[a], HD[b]) for a, b in rng])
        d = {}
        def add(key, poly):
            d[key] = padd(d.get(key, [F(0)]), poly)
        # X2 = c² (1-x²)PP + cσ [2y(1-x²)P H' - 2xy H P] + σ² [y²(1-x²)H'H' + (1-y²)HH - 2x y² H H']
        add(("cc", 0), pmul(ONE_M_X2, pp))
        add(("cs", 1), padd(psc(2, pmul(ONE_M_X2, phd)), psc(-2, pmul(X, hp))))
        add(("ss", 2), pmul(ONE_M_X2, hdhd))
        add(("ss", 0), hh); add(("ss", 2), psc(-1, hh))
        add(("ss", 2), psc(-2, pmul(X, hhd)))
        for k in list(d): d[k] = psc(F(3, 2), d[k])
        if i == 0:   # (1 - s²)/6 = (1 - c²x² - 2cσ x y - σ² y²)/6
            add(("1", 0), [F(1, 6)]); add(("cc", 0), [F(0), F(0), F(-1, 6)])
            add(("cs", 1), [F(0), F(-2, 6)]); add(("ss", 2), [F(-1, 6)])
        A.append(d)
    return A, (P, H, M)

# ---------- moments exacts ----------
def beta_half(m, k):
    """∫_{-1}^1 s^m (1-s²)^k ds = B((m+1)/2, k+1) pour m pair."""
    if m % 2: return F(0)
    a = F(m + 1, 2); r = F(factorial(k))
    for i in range(k + 1): r /= (a + i)
    return r
_J = {}
def J(m, n):
    if (m, n) not in _J:
        _J[(m, n)] = F(0) if (m % 2 or n % 2) else F(2, n + 1) * beta_half(m, n // 2)
    return _J[(m, n)]
_M = {}
def Mab(a, b):
    """∫∫ x^a y^b ds dτ comme dict {(k,l): coeff} pour c^k σ^l."""
    if (a, b) in _M: return _M[(a, b)]
    d = {}
    for p in range(a + 1):
        for q in range(b + 1):
            jj = J(p + q, (a - p) + (b - q))
            if jj == 0: continue
            key = (p + (b - q), (a - p) + q)
            d[key] = d.get(key, F(0)) + comb(a, p) * (-1) ** (a - p) * comb(b, q) * jj
    _M[(a, b)] = d
    return d
PREF = {"cc": (2, 0), "cs": (1, 1), "ss": (0, 2), "1": (0, 0)}
_OMC = {0: [F(1)]}
def omc2(m):
    if m not in _OMC: _OMC[m] = pmul(omc2(m - 1), [F(1), F(0), F(-1)])
    return _OMC[m]
def to_c(dct):
    """dict (k,l) -> poly en c, σ^l → (1-c²)^{l/2} ; exige l pair."""
    r = [F(0)]
    for (k, l), v in dct.items():
        if v == 0: continue
        assert l % 2 == 0, ("puissance impaire de σ", k, l)
        r = padd(r, psc(v, [F(0)] * k + omc2(l // 2)))
    return trim(r)

def I_j(A, j, N):
    acc = {}
    for i in range(min(j, 2 * N) + 1):
        f = F(1, factorial(j - i))
        for (pref, b), poly in A[i].items():
            pk, pl = PREF[pref]
            for a0, co in enumerate(poly):
                if co == 0: continue
                a = a0 + (j - i)
                for (k, l), v in Mab(a, b).items():
                    key = (k + pk, l + pl)
                    acc[key] = acc.get(key, F(0)) + co * f * v
    return to_c(acc)

def E_j(A, j, N):
    I = I_j(A, j, N)
    if j % 2 == 0:
        k = j // 2
        I = padd(I, [-F(8, 9 * 4 ** k * factorial(k) * factorial(k + 1))])
    return trim(I)

if __name__ == "__main__":
    N = int(sys.argv[1]); JMAX = int(sys.argv[2]); out = sys.argv[3]
    t0 = time.time()
    A, (P, H, M) = build_A(N)
    print(f"# N={N} séries OK ({time.time()-t0:.1f}s) ; m_1..m_4 = {[str(m) for m in M[1:5]]}")
    res = {}
    for j in range(JMAX + 1):
        e = E_j(A, j, N)
        res[j] = [str(c) for c in e]
        z = all(c == 0 for c in e)
        print(f"j={j:2d} deg={len(e)-1:2d} {'NUL EXACT' if z else ''} E_j(c=0)={float(e[0]):+.6e} E_j(1)={float(sum(e)):+.6e} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(dict(N=N, JMAX=JMAX, E=res, p=[[str(c) for c in p] for p in P], h=[[str(c) for c in h] for h in H],
                   m=[str(m) for m in M]), open(out, "w"))
    print("écrit", out)
