#!/usr/bin/env python3
"""gates_xi.py -- gates de robustesse du certificat cert_xi_arb.py (analogue de gates.py de D7).  Les verdicts sont CALCULES.

G1 cap       : cap in {N+5, N+60, 300, 500} -> memes boites ; cap = 10 et cap = N+4 REFUSES (garde 1).          (piege flint cap = 10)
G2 N         : N in {70, 90, 120, 160} -> verdict identique, rapport stable ; N <= kappa REFUSE (garde 2).
G3 NT        : NT in {100, 200, 400, 800} -> sommes de Riemann superieures decroissantes.
G4 prec      : prec in {96, 128, 192, 256} -> meme verdict ; prec = 40 REFUSE (garde 3).
G5 sabotage  : multiplier la partie positive de Xi par s : le certificat doit ECHOUER pour s assez grand (on calcule le plus grand s qui passe).
G6 hors plage: kappa = 30 avec des boites de largeur 2e-3 : le certificat doit ECHOUER (la technique a une portee limitee ; le script ne ment pas).
"""
import json, os, subprocess, sys, tempfile
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "cert_xi_arb.py")
PY = sys.executable

def run(args, expect=None):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "o.json")
        p = subprocess.run([PY, CERT] + args + ["--out", out], capture_output=True, text=True)
        js = json.load(open(out)) if os.path.exists(out) else None
        return p.returncode, js, p.stdout + p.stderr

def boxes_sig(js):
    return [(b["k0"], b["k1"], b["mode"], b["ratio_hi"], b["ok"]) for b in js["boites"]]

def main():
    verdicts = {}
    base = ["--k0", "5", "--k1", "126/25", "--NK", "10", "--NT", "300", "--neg", "analytique"]
    # G1 : cap
    rc, ref, _ = run(base + ["--N", "100", "--cap", "160"])
    sigs = {}
    ok1 = rc == 0
    for cap in (105, 160, 300, 500):
        rc2, js, _ = run(base + ["--N", "100", "--cap", str(cap)])
        ok1 = ok1 and rc2 == 0 and boxes_sig(js) == boxes_sig(ref)
    r10, _, o10 = run(base + ["--N", "100", "--cap", "10"])
    r104, _, o104 = run(base + ["--N", "100", "--cap", "104"])
    ok1 = ok1 and r10 != 0 and "GARDE 1" in o10 and r104 != 0 and "GARDE 1" in o104
    verdicts["G1_cap"] = bool(ok1)
    print(f"G1 cap in {{105,160,300,500}} : memes boites ; cap=10 et cap=N+4=104 refuses (GARDE 1) -> {ok1}")
    # G2 : N
    ratios = []
    ok2 = True
    for N in (70, 90, 120, 160):
        rc2, js, _ = run(base + ["--N", str(N), "--cap", str(N + 60)])
        ok2 = ok2 and rc2 == 0
        ratios.append(float(Fraction(js["pire_ratio"])) if "/" in js["pire_ratio"] else float(js["pire_ratio"]))
    ok2 = ok2 and (max(ratios) - min(ratios) < 1e-9)
    rN, _, oN = run(base + ["--N", "3", "--cap", "100"])
    ok2 = ok2 and rN != 0 and "GARDE 2" in oN
    verdicts["G2_N"] = bool(ok2)
    print(f"G2 N in {{70,90,120,160}} : pire ratio stable {ratios} ; N=3 (N+2 <= kappa) refuse (GARDE 2) -> {ok2}")
    # G3 : NT
    rs = []
    for NT in (100, 200, 400, 800):
        rc2, js, _ = run(["--k0", "4/3", "--k1", "103/75", "--NK", "4", "--NT", str(NT), "--neg", "taylor", "--N", "90", "--cap", "150"])
        rs.append(float(js["pire_ratio"]))
    ok3 = all(rs[i] > rs[i + 1] for i in range(len(rs) - 1))
    verdicts["G3_NT"] = bool(ok3)
    print(f"G3 NT in {{100,200,400,800}} : pire Xi_hi/P0 = {rs} (decroissant : {ok3})")
    # G4 : prec
    ok4 = True
    for pr in (96, 128, 192, 256):
        rc2, js, _ = run(base + ["--N", "100", "--cap", "160", "--prec", str(pr)])
        ok4 = ok4 and rc2 == 0
    r40, _, o40 = run(base + ["--N", "100", "--cap", "160", "--prec", "40"])
    ok4 = ok4 and r40 != 0 and "GARDE 3" in o40
    verdicts["G4_prec"] = bool(ok4)
    print(f"G4 prec in {{96,128,192,256}} : memes verdicts ; prec=40 refuse (GARDE 3) -> {ok4}")
    # G5 : sabotage -- plus grand s qui passe, sur deux boites
    res5 = {}
    ok5 = True
    for (k0, k1, neg) in (("4/3", "103/75", "taylor"), ("10", "251/25", "analytique")):
        lo, hi = Fraction(1), Fraction(60)
        def passe(s):
            rc2, js, _ = run(["--k0", k0, "--k1", k1, "--NK", "2", "--NT", "300", "--neg", neg, "--scale", str(s)])
            return rc2 == 0
        if not passe(Fraction(1)):
            ok5 = False; break
        for _ in range(14):
            mid = (lo + hi) / 2
            if passe(mid): lo = mid
            else: hi = mid
        res5[f"[{k0},{k1}]"] = float(lo)
        ok5 = ok5 and (float(lo) > 1.0) and (not passe(Fraction(100)))
    verdicts["G5_sabotage"] = bool(ok5)
    print(f"G5 sabotage : plus grand facteur sur la partie positive de Xi qui passe encore = {res5} ; facteur 100 echoue -> {ok5}")
    # G6 : hors plage
    rc6, js6, _ = run(["--k0", "30", "--k1", "30.02", "--NK", "10", "--NT", "300", "--neg", "analytique", "--adapt", "0"])
    ok6 = (rc6 != 0) and (js6 is not None) and (not js6["toutes_ok"])
    verdicts["G6_hors_plage_echoue"] = bool(ok6)
    print(f"G6 kappa=30 (hors portee de la technique) : certificat ECHOUE comme attendu -> {ok6}")
    tout = all(verdicts.values())
    print(json.dumps(verdicts))
    print("GATES : " + ("TOUS REUSSIS" if tout else "ECHEC"))
    sys.exit(0 if tout else 1)

if __name__ == "__main__":
    main()
