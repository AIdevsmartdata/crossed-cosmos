#!/usr/bin/env python3
"""gates_mpiv.py -- gates de l'implementation independante cert_xi_mpiv.py (mpmath.iv).  Verdicts CALCULES.
  P1 : prec in {128, 192, 256}  -> memes verdicts (OK) sur deux plages ;
  N1 : N = 3 -> REFUSE (garde N + 2 <= kappa) ; prec = 40 -> le verdict reste SOUND (arithmetique d'intervalles : la precision n'affecte que la largeur),
       il n'y a pas de garde de precision minimale dans cette implementation (contrairement a cert_xi_arb.py) ;
  S1 : sabotage : partie positive de Xi multipliee par 3 -> ECHEC (le certificat n'est pas decoratif) ;
  H1 : kappa = 30 (hors portee) -> ECHEC ;
  C1 : accord avec l'implementation Arb : sur les memes plages, les deux certifient (verdict identique) et les majorants Xi_hi/P0 sont du meme ordre
       (ecart absolu max < 0,2 : partitions et inflations differentes).
"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join(HERE, "cert_xi_mpiv.py")
AR = os.path.join(HERE, "cert_xi_arb.py")
PY = sys.executable

def run(script, args):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "o.json")
        p = subprocess.run([PY, script] + args + ["--out", out], capture_output=True, text=True)
        js = json.load(open(out)) if os.path.exists(out) else None
        return p.returncode, js, p.stdout + p.stderr

def pire(js):
    v = js["pire_ratio"]
    return float(v)

def main():
    v = {}
    plages = [("4/3", "103/75"), ("5", "126/25")]
    ok = True
    for (a, b) in plages:
        res = []
        for pr in (128, 192, 256):
            rc, js, _ = run(MP, ["--NT", "200", "--k0", a, "--k1", b, "--NK", "6", "--procs", "2", "--prec", str(pr)])
            ok = ok and rc == 0 and js["toutes_ok"]
            res.append(pire(js))
        ok = ok and (max(res) - min(res) < 1e-6)
    v["P1_precision_stable"] = bool(ok)
    print(f"P1 prec in {{128,192,256}} : verdicts OK et pire rapport stable -> {ok}")
    r40, j40, _ = run(MP, ["--NT", "100", "--k0", "5", "--k1", "126/25", "--NK", "2", "--procs", "1", "--prec", "40"])
    rN, _, oN = run(MP, ["--NT", "100", "--k0", "5", "--k1", "126/25", "--NK", "2", "--procs", "1", "--N", "3"])
    # prec = 40 : un verdict positif est legitime ; on verifie seulement que la marge majoree n'est PAS meilleure qu'a haute precision (monotonie de l'enclosure)
    rh, jh_, _ = run(MP, ["--NT", "100", "--k0", "5", "--k1", "126/25", "--NK", "2", "--procs", "1", "--prec", "128"])
    n1 = (rN != 0) and (j40 is not None) and (jh_ is not None) and (pire(j40) >= pire(jh_) - 1e-12)
    v["N1_refus_et_monotonie_precision"] = bool(n1)
    print(f"N1 N=3 refuse (code {rN}) ; prec=40 : pire rapport {pire(j40):+.4f} >= {pire(jh_):+.4f} (prec=128) -> {n1}")
    rs, js, _ = run(MP, ["--NT", "200", "--k0", "4/3", "--k1", "103/75", "--NK", "4", "--procs", "2", "--scale", "3"])
    s1 = (rs != 0) and js is not None and (not js["toutes_ok"])
    v["S1_sabotage_echoue"] = bool(s1)
    print(f"S1 partie positive x3 : le certificat ECHOUE -> {s1}")
    rh, jh, _ = run(MP, ["--NT", "200", "--k0", "30", "--k1", "30.02", "--NK", "4", "--procs", "2"])
    h1 = (rh != 0) and jh is not None and (not jh["toutes_ok"])
    v["H1_hors_portee_echoue"] = bool(h1)
    print(f"H1 kappa=30 : ECHEC attendu -> {h1}")
    c1 = True
    ecarts = []
    for (a, b) in plages + [("10", "251/25")]:
        rm, jm, _ = run(MP, ["--NT", "250", "--k0", a, "--k1", b, "--NK", "10", "--procs", "2"])
        ra, ja, _ = run(AR, ["--NT", "400", "--k0", a, "--k1", b, "--NK", "10", "--procs", "2"])
        c1 = c1 and rm == 0 and ra == 0 and jm["toutes_ok"] and ja["toutes_ok"]
        ecarts.append(abs(pire(jm) - pire(ja)))
    c1 = c1 and max(ecarts) < 0.2
    v["C1_accord_arb_mpiv"] = bool(c1)
    print(f"C1 accord Arb / mpmath.iv (memes plages) : ecarts absolus des pires rapports {['%.3f' % e for e in ecarts]} -> {c1}")
    print(json.dumps(v))
    tout = all(v.values())
    print("GATES MPIV : " + ("TOUS REUSSIS" if tout else "ECHEC"))
    sys.exit(0 if tout else 1)

if __name__ == "__main__":
    main()
