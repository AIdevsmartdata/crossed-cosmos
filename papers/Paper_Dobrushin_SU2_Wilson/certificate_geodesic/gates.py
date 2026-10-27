"""Gates du certificat v2 (27/09/2026). Usage : gates.py G2|G3|G4|G5 --cap C --prec P
G2 : série d'un nœud par arb_series (cert_lien.py) == convolution de Cauchy EXPLICITE sur des listes Arb (sans arb_series,
     donc sans ctx.cap), tronquée à L. Attendu : boules chevauchantes pour les L coefficients (identité exacte en théorie).
G3 : variation en N (ordre de la série) de U(κ, α) = Σ_{j≤D} I_j κ^j / Σ_{j≤D} z_j κ^j, à κ = 1,18. Attendu (théorie) :
     |U_N − U_32| ≠ 0 (N est réellement utilisé), décroissant en N, du même ordre ou sous ε_N = 2κ^{N+1}ρ_N e^κ/√3
     (la correction de Poincaré, qui mesure ‖∇ψ − ∇ψ_N‖).
G4 : variation du nombre de nœuds NG, N = 16 : (a) NG = 22 vs 26, tous deux exacts pour j ≤ 41 ⟹ boules I_j chevauchantes
     j ≤ 41 ; (b) sensibilité : NG = 21 (exact pour j ≤ 39 seulement) vs 26 ⟹ désaccord attendu dès que le degré j+2 dépasse
     2·21−1 = 41 ; (c) reste de Taylor : Σ_{j=42}^{49} |I_j| K^{j−2} (ordres calculés par NG = 26, NON calculés par NG = 22)
     ≤ tailT(NG = 22).
G5 : U(κ, α) Arb vs grille flottante polaire (explore.py, série flottante d'ordre 40, 400×800). Attendu : écart ~1e-9
     (erreur de la grille + troncature N = 16), et NON 2,4e-6 (signature de la troncature κ¹⁰ de l'original).
"""
import sys, argparse
from flint import arb, arb_series, ctx
import cert_lien as cl

ap = argparse.ArgumentParser(); ap.add_argument("gate"); ap.add_argument("--cap", type=int, required=True)
ap.add_argument("--prec", type=int, required=True); a = ap.parse_args()
cl.fixe_contexte(a.cap, a.prec)
print(f"# gate {a.gate} ctx.cap={ctx.cap} ctx.prec={ctx.prec}")
PI = arb.pi()


def chevauche(x, y): return x.overlaps(y)


def U_de(pr, I, ka):
    return sum(I[j] * ka ** j for j in range(pr.L)) / sum(pr.zc[j] * ka ** j for j in range(pr.L))


if a.gate == "G2":
    pr = cl.Prep(16, 22, verbeux=False); L = pr.L
    def conv(u, v):
        return [sum((u[i] * v[j - i] for i in range(max(0, j - len(v) + 1), min(j, len(u) - 1) + 1)), arb(0)) for j in range(L)]
    def pad(u): return (list(u) + [arb(0)] * L)[:L]
    ok = True; pire = 0.0
    for al in (arb(0), arb("0.7"), PI / 2, arb("2.9")):
        ca, sa = al.cos(), al.sin()
        for (s, _), (tau, _) in ((pr.GL[0], pr.GL[5]), (pr.GL[10], pr.GL[21]), (pr.GL[17], pr.GL[3])):
            ref = pr.serie_noeud(ca, sa, s, tau)
            t = (1 - s * s).sqrt() * tau; x = ca * s - sa * t; y = sa * s + ca * t
            Ps = pad([pr.horner(c, x) for c in pr.Pa]); Hs = pad([pr.horner(c, x) for c in pr.Ha])
            Hd = pad([pr.horner(c, x) for c in pr.HDa])
            As = [Ps[j] * ca + Hd[j] * (sa * y) for j in range(L)]
            AA, HH, HA = conv(As, As), conv(Hs, Hs), conv(Hs, As)
            X2 = [AA[j] * (1 - x * x) + HH[j] * (sa * sa * (1 - y * y)) - HA[j] * (2 * x * y * sa) for j in range(L)]
            F = [X2[j] * arb(1.5) + ((1 - s * s) / 6 if j == 0 else 0) for j in range(L)]
            e = [arb(1)]
            for j in range(1, L): e.append(e[-1] * x / j)
            G = conv(F, e)
            for j in range(L):
                if not chevauche(ref[j], G[j]): ok = False; print("DESACCORD", float(al.mid()), j, ref[j], G[j])
                pire = max(pire, float(abs(ref[j].mid() - G[j].mid())))
            print(f"G2 α={float(al.mid()):.3f} s={float(s.mid()):+.4f} τ={float(tau.mid()):+.4f} : {L} coefficients chevauchants "
                  f"; |c_41| = {float(abs(G[41].mid())):.3e} ; |c_12| = {float(abs(G[12].mid())):.3e}", flush=True)
    print(f"G2 max |Δmid| = {pire:.2e}"); print("GATE_G2", "OK" if ok else "ECHEC"); sys.exit(0 if ok else 1)

if a.gate == "G3":
    ka = arb("1.18"); res = {}
    cfg = [(16, 22), (20, 26), (24, 30), (32, 40)]
    for al_name, al in (("0", arb(0)), ("pi/2", PI / 2), ("2.2", arb("2.2"))):
        for (N, NG) in cfg:
            pr = cl.Prep(N, NG, verbeux=False)
            U = U_de(pr, pr.integrale(al.cos(), al.sin()), ka)
            eps = 2 * ka ** (N + 1) * cl.A(pr.rhoN) * ka.exp() / arb(3).sqrt()
            res[(al_name, N)] = (U, eps)
            print(f"G3 α={al_name:5s} N={N:2d} NG={NG} U(1.18)={U.str(15)}  ε_N={float(eps.mid()):.2e}", flush=True)
    ok = True
    for al_name in ("0", "pi/2", "2.2"):
        U32 = res[(al_name, 32)][0]; prev = None
        for (N, _) in cfg[:-1]:
            U, eps = res[(al_name, N)]
            d = abs(float((U - U32).mid()))
            non_nul = not (U - U32).contains(0)
            sous_eps = d <= float(eps.upper())
            dec = prev is None or d <= prev
            ok &= non_nul and dec
            print(f"G3 α={al_name:5s} |U_{N} − U_32| = {d:.3e} (≠0 : {non_nul}) ; ≤ ε_{N} = {float(eps.mid()):.2e} : {sous_eps} ; "
                  f"décroissant : {dec}")
            prev = d
    print("GATE_G3", "OK" if ok else "ECHEC"); sys.exit(0 if ok else 1)

if a.gate == "G4":
    ok = True
    p22 = cl.Prep(16, 22, verbeux=False); p26 = cl.Prep(16, 26, verbeux=False)
    p21 = cl.Prep(16, 26, verbeux=False)          # même L = 50 que NG = 26, mais règle à 21 nœuds (exacte j ≤ 39)
    p21.GL = [arb.legendre_p_root(21, k, weight=True) for k in range(21)]
    K = cl.A(cl.K)
    for al in (arb(0), arb("1.0"), PI / 2, arb("2.6")):
        ca, sa = al.cos(), al.sin()
        I22, I26, I21 = p22.integrale(ca, sa), p26.integrale(ca, sa), p21.integrale(ca, sa)
        a_ok = all(I22[j].overlaps(I26[j]) for j in range(42))
        ok &= a_ok
        pairs = [j for j in range(0, 50, 2)]
        exact21 = all(I21[j].overlaps(I26[j]) for j in range(40))
        desac = [j for j in pairs if j >= 40 and not I21[j].overlaps(I26[j])]
        ok &= exact21
        queue = sum(abs(I26[j]) * K ** (j - 2) for j in range(42, 50))
        c_ok = queue.upper() <= p22.tailT.lower()
        ok &= c_ok
        print(f"G4 α={float(al.mid()):.3f} (a) NG22 vs NG26, j≤41 chevauchants : {a_ok} ; "
              f"(b) NG21 vs NG26 : j≤39 chevauchants {exact21}, ordres pairs en désaccord (j≥40) = {desac} "
              f"[|I40(21)−I40(26)| = {float(abs((I21[40]-I26[40]).mid())):.2e}, rayons {float(I21[40].rad()):.1e}] ; "
              f"(c) Σ_{{42..49}}|I_j|K^(j-2) = {float(queue.mid()):.3e} ≤ tailT(22) = {float(p22.tailT.mid()):.3e} : {c_ok}", flush=True)
    print("GATE_G4", "OK" if ok else "ECHEC"); sys.exit(0 if ok else 1)

if a.gate == "G5":
    import numpy as np
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        import explore
    pr = cl.Prep(16, 22, verbeux=False); pire = 0.0
    for al in (0.0, 1.0, float(np.pi / 2), 2.2):
        I = pr.integrale(arb(al).cos(), arb(al).sin())
        for k in (0.5, 1.0, 1.18):
            U = U_de(pr, I, arb(k))
            C_f, U_f = explore.quantities(k, al)
            d = abs(float(U.mid()) - U_f); pire = max(pire, d)
            print(f"G5 α={al:.4f} κ={k:4.2f} U_arb={float(U.mid()):.10f} (±{float(U.rad()):.1e}) U_grille={U_f:.10f} écart={d:.1e}", flush=True)
    ok = pire < 1e-7
    print(f"G5 écart max = {pire:.2e} (original : 2,4e-6)"); print("GATE_G5", "OK" if ok else "ECHEC"); sys.exit(0 if ok else 1)
print("gate inconnue"); sys.exit(2)
