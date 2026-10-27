#!/usr/bin/env python3
"""C2 — Certification (Arb) de sup_{κ∈[0,K], v} D(κ,v) ≤ 8/(9π) − c κ²  —  VERSION v2 CORRIGÉE (27/09/2026, tâche CERT).

Original : chantiers/suite_outils_20260927/C2/scripts/cert_lien.py (sha256 5726251791…, copie dans ../orig/).
DÉFAUT CORRIGÉ (trouvé par V-C2) : l'original ne fixait pas `ctx.cap` ; python-flint 0.9.0 a `ctx.cap = 10` par défaut, et
tout produit d'`arb_series` est tronqué à min(prec_a, prec_b, ctx.cap) coefficients ⟹ les ordres κ¹⁰..κ^D n'étaient ni
intégrés ni majorés (le reste de Taylor ne couvrait que j ≥ D+1). Dans cette version :
  (a) ctx.cap et ctx.prec sont des ARGUMENTS OBLIGATOIRES, fixés explicitement puis relus ;
  (b) GARDE 1 : cap ≥ L = D+1 (sinon refus) ;
  (c) GARDE 2 : chaque série construite et chaque produit ont une longueur (`.prec`) EXACTEMENT égale à L — assertion.
      (NB : `arb_series.coeffs()` supprime les zéros de fin, d'où l'assertion sur `.prec` et le remplissage explicite) ;
  (d) le reste de Taylor couvre exactement les ordres j ≥ D+1, qui sont les SEULS non calculés une fois (c) vérifiée.

D(κ,v) = sup_{f 1-Lip} Cov_{q_κ}(f, u·v),  q_κ ∝ e^{κ u·ŝ} sur S³.
  D ≤ E|∇ψ|,  ∇ψ = X_N + ∇φ,  E|X_N| ≤ U_N := E[(|X_N|²/ρ + ρ)/2] (AM-GM, ρ = sinγ/3),  E|∇φ| ≤ ε_N.
  U_N·Z = ∫∫_{[-1,1]²} [(3/2)|X_N|² + (1-s²)/6] e^{κx} ds dτ,   Z = π Σ_k (κ²/4)^k/(k!(k+1)!).
  Coefficient de κ^j : intégrale d'un polynôme de degré ≤ j+2 en (s,τ) ⟹ Gauss–Legendre NG nœuds EXACT pour j ≤ D = 2NG−3.
Sortie : bornes sup des E_{2k}(α) de Δ = (U_N + ε − C0) Z = κ² Φ(κ²), et Φ < 0 sur w ∈ [0, K²] (borne monotone = Lean bP).

Usage : cert_lien.py N NG NB --cap CAP --prec PREC --out FICHIER.json [--ia0 i --ia1 j] [--tous-E] [--sans-garde-cap]
  --sans-garde-cap : désactive la GARDE 1 (sert UNIQUEMENT au gate qui vérifie que la GARDE 2 attrape la troncature).
"""
import sys, json, time, hashlib, argparse
from fractions import Fraction as Fr
from flint import arb, arb_series, fmpq, ctx
from serie import series, deriv, polyadd, mulx, scal, one_m_x2

K = Fr(118, 100)                   # κ_max ≥ 6·(π/16) = 3π/8 = 1.17809...


def A(q): return arb(fmpq(q.numerator, q.denominator))
def l1(poly): return sum(abs(c) for c in poly)


def fixe_contexte(cap, prec):
    ctx.cap = int(cap); ctx.prec = int(prec)
    assert ctx.cap == int(cap) and ctx.prec == int(prec), ("ctx non fixé", ctx.cap, ctx.prec)


class Prep:
    """Tout ce qui ne dépend pas de la boîte en α. Exige que fixe_contexte ait été appelé."""

    def __init__(self, N, NG, garde_cap=True, verbeux=True):
        self.N, self.NG = N, NG
        self.D = D = 2 * NG - 3        # ordre max en κ intégré EXACTEMENT par Gauss (degré j+2 ≤ 2NG-1)
        self.L = L = D + 1             # nombre de coefficients calculés : κ^0 .. κ^D
        assert D >= 2 * N, "il faut D >= 2N (A(κ) est de degré 2N ; le reste de Taylor suppose i ≤ D)"
        if garde_cap:
            assert ctx.cap >= L, f"GARDE 1 : ctx.cap = {ctx.cap} < L = {L} : les produits de séries seraient tronqués"
        self.PI = PI = arb.pi(); self.C0 = 8 / (9 * PI)
        P, H, M = series(N)
        for n in range(N + 1):
            for k, c in enumerate(P[n]):
                assert c == 0 or (k - n) % 2 == 0, ("parité p", n, k)
            for k, c in enumerate(H[n]):
                assert c == 0 or (k - n) % 2 == 0, ("parité h", n, k)
            assert M[n] == 0 or n % 2 == 1
        HD = [deriv(h) for h in H]
        Pl1 = [l1(p) for p in P]; Hl1 = [l1(h) for h in H]; HDl1 = [l1(h) for h in HD]
        # résidu R' = κ^{N+1}[cα(1-x²)p_N + sα y((1-x²)h_N' - x h_N)]
        self.rhoN = rhoN = l1(one_m_x2(P[N])) + l1(polyadd(one_m_x2(HD[N]), scal(-1, mulx(H[N]))))
        # sup|A_i| : coefficient d'ordre i (0 ≤ i ≤ 2N) de A(κ) = (3/2)|X_N|² + (1-s²)/6 ; |x|,|y|,|cα|,|sα| ≤ 1
        supA = []
        for i in range(2 * N + 1):
            t = Fr(0)
            for a in range(max(0, i - N), min(i, N) + 1):
                b = i - a
                t += (Pl1[a] + HDl1[a]) * (Pl1[b] + HDl1[b]) + Hl1[a] * Hl1[b] + 2 * Hl1[a] * (Pl1[b] + HDl1[b])
            supA.append(Fr(3, 2) * t + (Fr(1, 6) if i == 0 else 0))
        self.supA = supA
        Ka = A(K)
        # RESTE DE TAYLOR : ordres j ≥ D+1 = TOUS les ordres non calculés (les ordres 0..D le sont, GARDE 2).
        # coefficient κ^j de A(κ)e^{κx} = Σ_{i≤min(j,2N)} A_i x^{j-i}/(j-i)! ; Σ_{j≥D+1} ≤ Σ_i |A_i| κ^{D+1} e^κ/(D+1-i)!
        # (car Σ_{m≥M} κ^m/m! ≤ κ^M e^κ/M!) ; aire du carré (s,τ) = 4 ; divisé par κ², croissant en κ ⟹ évalué en κ = K.
        self.tailT = sum(A(supA[i]) / arb.fac_ui(D + 1 - i) for i in range(2 * N + 1)) * 4 * Ka ** (D - 1) * Ka.exp()
        ZK = PI * sum((Ka * Ka / 4) ** k / (arb.fac_ui(k) * arb.fac_ui(k + 1)) for k in range(60)) * 2  # Z(K) ≤ 2·S_60
        self.epsC = 2 * Ka ** (N - 1) * A(rhoN) * Ka.exp() * ZK / arb(3).sqrt()      # ε·Z/κ² majoré en κ = K
        self.CST = self.tailT + self.epsC
        zc = [arb(0)] * L
        for k in range(D // 2 + 1):
            zc[2 * k] = PI / (arb(4) ** k * arb.fac_ui(k) * arb.fac_ui(k + 1))
        self.zc = zc
        self.GL = [arb.legendre_p_root(NG, k, weight=True) for k in range(NG)]
        self.Pa = [[A(c) for c in p] for p in P]; self.Ha = [[A(c) for c in h] for h in H]
        self.HDa = [[A(c) for c in h] for h in HD]
        self.n_series_verifiees = 0
        if verbeux:
            print(f"# N={N} NG={NG} D={D} L={L} K={K} ctx.cap={ctx.cap} ctx.prec={ctx.prec}")
            print("# parités exactes p_n, h_n ~ (-1)^n et m_n = 0 pour n pair : OK [calcul exact]")
            print(f"# rho_N = {float(rhoN):.3e} ; reste Taylor (ordres ≥ {D+1})/κ² ≤ {self.tailT.upper()} ; "
                  f"correction ε·Z/κ² ≤ {self.epsC.upper()}")

    def S(self, s):
        """GARDE 2 : toute série manipulée a exactement L coefficients de précision."""
        assert s.prec == self.L, f"GARDE 2 : série de longueur {s.prec} ≠ L = {self.L} (troncature ctx.cap = {ctx.cap} ?)"
        self.n_series_verifiees += 1
        return s

    @staticmethod
    def horner(cs, x):
        r = arb(0)
        for c in reversed(cs): r = r * x + c
        return r

    def serie_noeud(self, ca, sa, s, tau):
        """Série en κ (longueur L) de F = [(3/2)|X_N|² + (1-s²)/6] e^{κx} au point (s, τ) ; liste de L arb."""
        L, S, hz = self.L, self.S, self.horner
        rt = (1 - s * s).sqrt()
        t = rt * tau
        x = ca * s - sa * t; y = sa * s + ca * t
        Ps = S(arb_series([hz(c, x) for c in self.Pa], prec=L))
        Hs = S(arb_series([hz(c, x) for c in self.Ha], prec=L))
        Hd = S(arb_series([hz(c, x) for c in self.HDa], prec=L))
        Aser = S(Ps * ca + Hd * (sa * y))
        AA = S(Aser * Aser); HH = S(Hs * Hs); HA = S(Hs * Aser)
        X2 = S(AA * (1 - x * x) + HH * (sa * sa * (1 - y * y)) - HA * (2 * x * y * sa))
        F = S(X2 * arb(1.5) + arb_series([(1 - s * s) / 6], prec=L))
        e = [arb(1)]
        for j in range(1, L): e.append(e[-1] * x / j)
        F = S(F * S(arb_series(e, prec=L)))
        cf = F.coeffs()
        assert len(cf) <= L, ("coeffs trop longs", len(cf), L)
        return list(cf) + [arb(0)] * (L - len(cf))

    def integrale(self, ca, sa):
        L = self.L
        tot = [arb(0)] * L
        for (s, ws) in self.GL:
            for (tau, wt) in self.GL:
                cf = self.serie_noeud(ca, sa, s, tau)
                w = ws * wt
                for j in range(L): tot[j] += w * cf[j]
        return tot


def borne_monotone(his, wa, wb):
    """Σ_k max(hi_k wa^k, hi_k wb^k) (w ≥ 0) : majorant de Σ e_k w^k si e_k ≤ hi_k. Rationnels exacts."""
    return sum(max(h * wa ** k, h * wb ** k) for k, h in enumerate(his))


def arb_upper_fr(a):
    u = a.upper(); m, e = u.man_exp()
    m = int(m); e = int(e)
    return Fr(m) * (Fr(2) ** e if e >= 0 else Fr(1, 2 ** (-e)))


def boite_alpha(pr, ia, NB):
    PI = pr.PI
    alo = PI * ia / NB; ahi = PI * (ia + 1) / NB
    al = (alo + ahi) / 2; al = arb(al.mid(), ((ahi - alo) / 2).upper() + al.rad())
    return alo, ahi, al


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int); ap.add_argument("NG", type=int); ap.add_argument("NB", type=int)
    ap.add_argument("--cap", type=int, required=True); ap.add_argument("--prec", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ia0", type=int, default=0); ap.add_argument("--ia1", type=int, default=None)
    ap.add_argument("--tous-E", action="store_true", help="exporter aussi toutes les boules E_j (gates)")
    ap.add_argument("--sans-garde-cap", action="store_true")
    a = ap.parse_args()
    fixe_contexte(a.cap, a.prec)
    sha = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    print(f"# script sha256 = {sha}")
    pr = Prep(a.N, a.NG, garde_cap=not a.sans_garde_cap)
    N, NG, NB, D, L = a.N, a.NG, a.NB, pr.D, pr.L
    IA1 = NB if a.ia1 is None else a.ia1
    KW = K * K
    res = []; t0 = time.time()
    for ia in range(a.ia0, IA1):
        alo, ahi, al = boite_alpha(pr, ia, NB)
        ca, sa = al.cos(), al.sin()
        I = pr.integrale(ca, sa)
        E = [I[j] - pr.C0 * pr.zc[j] for j in range(L)]
        g0 = E[0].contains(0) and I[0].contains(arb(8) / 9)
        godd = all(E[j].contains(0) for j in range(1, L, 2))
        his = [arb_upper_fr(E[2 * k]) for k in range(1, D // 2 + 1)]
        his[0] += arb_upper_fr(pr.CST)
        pieces = [(Fr(0), KW)]; ok = []; fail = False
        while pieces:
            wa, wb = pieces.pop()
            b = borne_monotone(his, wa, wb)
            if b < 0: ok.append((wa, wb))
            elif wb - wa < Fr(1, 10 ** 4): fail = True; break
            else:
                wm = (wa + wb) / 2; pieces += [(wa, wm), (wm, wb)]
        bmon = borne_monotone(his, Fr(0), KW)
        r = dict(ia=ia, gate_E0=g0, gate_impairs=godd, E2=[E[2].mid().str(8), float(E[2].rad())],
                 E4=E[4].str(6), his=[str(h) for h in his], borne_monotone=str(bmon),
                 pieces=[(str(x), str(y)) for x, y in sorted(ok)], ok=(not fail) and g0 and godd)
        if a.tous_E:
            r["E_tous"] = [[e.mid().str(30, radius=False), e.rad().str(5, radius=False)] for e in E]
        res.append(r)
        print(f"ia={ia:4d} α∈[{float(alo.mid()):.4f},{float(ahi.mid()):.4f}] E2={float(E[2].mid()):+.5f}±{float(E[2].rad()):.1e} "
              f"E4={float(E[4].mid()):+.2e}±{float(E[4].rad()):.1e} gates E0={g0} impairs={godd} "
              f"borne={float(bmon):+.8f} morceaux_w={len(ok)} OK={r['ok']} ({time.time()-t0:.0f}s)", flush=True)
    print(f"# séries vérifiées par la GARDE 2 : {pr.n_series_verifiees}")
    json.dump(dict(version="v2-cap-explicite", script_sha256=sha, cap=ctx.cap, prec=ctx.prec, N=N, NG=NG, D=D, L=L, NB=NB,
                   K=str(K), CST=pr.CST.str(10), tailT=pr.tailT.str(10), epsC=pr.epsC.str(10), boites=res),
              open(a.out, "w"), indent=0)
    print("TOUTES_OK" if all(r['ok'] for r in res) else "ECHEC")


if __name__ == "__main__":
    main()
