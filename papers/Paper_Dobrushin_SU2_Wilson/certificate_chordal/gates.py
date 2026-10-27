#!/usr/bin/env python3
# gates.py -- CH (chordal certificate) : gates cap / N (= D) / quadrature (NT) / prec / NK autour de cert_ch.py.
# Chaque run est un sous-processus ; son RC et son log sont conserves. Une gate de stabilite doit BOUGER
# quand le parametre change (sinon le parametre n'est pas utilise).
import subprocess, json, sys, os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
JS = os.path.join(HERE, "out", "gates")
LG = os.path.join(HERE, "logs", "gates")
os.makedirs(JS, exist_ok=True)
os.makedirs(LG, exist_ok=True)
ECHECS = []


def run(nom, args, rc_attendu=0):
    out = os.path.join(JS, nom + ".json")
    log = os.path.join(LG, nom + ".log")
    cmd = [PY, os.path.join(HERE, "cert_ch.py")] + args + ["--out", out]
    with open(log, "w") as f:
        rc = subprocess.run(["nice", "-n", "5"] + cmd, stdout=f, stderr=subprocess.STDOUT).returncode
    txt = open(log).read()
    ok = (rc == rc_attendu)
    print(f"  run {nom:34s} RC={rc} (attendu {rc_attendu}) {'OK' if ok else 'ECHEC'}"
          + ("" if rc == 0 else "  | " + [l for l in txt.splitlines() if l.strip()][-1][:150]))
    if not ok:
        ECHECS.append(nom)
    return (json.load(open(out)) if rc == 0 else None), txt


def boites(j):
    return [(b["k0"], b["k1"], b["LB"], b["J0"], b["J1"], b["m"], b["marge"]) for b in j["boites"]]


def mid(s):
    return float(s.strip("[").split(" ")[0])


def pire(j):
    b = min(j["boites"], key=lambda b: mid(b["marge"]))
    return b["k0"], b["k1"], mid(b["marge"])


base = ["--prec", "128", "--NT", "1024", "--NK", "256"]

print("G1 cap : cap >= L = 85 => boites identiques ; cap < L => refus")
res = {}
for cap in (85, 100, 200, 300):
    j, _ = run(f"G1_cap{cap}", ["--D", "80", "--cap", str(cap)] + base)
    res[cap] = j
ident = all(boites(res[c]) == boites(res[200]) for c in (85, 100, 300))
print(f"  boites identiques pour cap 85/100/200/300 : {ident}")
if not ident:
    ECHECS.append("G1_ident")
run("G1_refus_garde1_cap10", ["--D", "80", "--cap", "10"] + base, rc_attendu=1)
run("G1_refus_garde1_cap84", ["--D", "80", "--cap", "84"] + base, rc_attendu=1)
_, t10 = run("G1_refus_garde2_cap10", ["--D", "80", "--cap", "10", "--sans-garde-cap"] + base, rc_attendu=1)
_, t84 = run("G1_refus_garde2_cap84", ["--D", "80", "--cap", "84", "--sans-garde-cap"] + base, rc_attendu=1)
for nom, t in (("cap10", t10), ("cap84", t84)):
    g2 = "GARDE 2" in t
    print(f"  garde 2 declenchee ({nom}, garde 1 desactivee) : {g2}")
    if not g2:
        ECHECS.append("G1_garde2_" + nom)

print("G3 N (ordre D) : 40 / 60 / 80 / 100 ; la borne doit bouger (restes) puis se stabiliser")
resD = {}
for D in (40, 60, 80, 100):
    j, _ = run(f"G3_D{D}", ["--D", str(D), "--cap", "200"] + base)
    resD[D] = j
for D in (40, 60, 80, 100):
    j = resD[D]
    last = j["boites"][-1]
    print(f"  D={D:3d} toutes_ok={j['toutes_ok']}  derniere boite J0={mid(last['J0']):.9e} J1={mid(last['J1']):.9e} "
          f"LB={mid(last['LB']):.9e} reste At={last['restes']['At']:.2e} reste N={last['restes']['N']:.2e}  pire={pire(j)}")
d4060 = abs(mid(resD[40]["boites"][-1]["J0"]) - mid(resD[60]["boites"][-1]["J0"]))
d80100 = abs(mid(resD[80]["boites"][-1]["J0"]) - mid(resD[100]["boites"][-1]["J0"]))
print(f"  |J0(40)-J0(60)| = {d4060:.3e} ; |J0(80)-J0(100)| = {d80100:.3e} (doit decroitre, et etre non nul a 40/60)")
if not (d4060 > 0 and d80100 < d4060):
    ECHECS.append("G3_mouvement")

print("G4 quadrature NT : 256 / 512 / 1024 / 2048 ; majorants decroissants (somme de Riemann superieure)")
resT = {}
for NT in (256, 512, 1024, 2048):
    j, _ = run(f"G4_NT{NT}", ["--D", "80", "--cap", "200", "--prec", "128", "--NT", str(NT), "--NK", "64"])
    resT[NT] = j
for k in (0, 32, 63):
    row = [(mid(resT[NT]["boites"][k]["J0"]), mid(resT[NT]["boites"][k]["J1"])) for NT in (256, 512, 1024, 2048)]
    dec = all(row[i][0] > row[i + 1][0] and row[i][1] > row[i + 1][1] for i in range(3))
    print(f"  boite {k:2d} [{resT[256]['boites'][k]['k0']},{resT[256]['boites'][k]['k1']}] J0: "
          + " > ".join(f"{r[0]:.6e}" for r in row) + " ; J1: " + " > ".join(f"{r[1]:.6e}" for r in row) + f"  decroissant={dec}")
    if not dec:
        ECHECS.append(f"G4_boite{k}")

print("G5 prec : 128 contre 192 (meme D/NT/NK)")
j192, _ = run("G5_p192", ["--D", "80", "--cap", "200", "--prec", "192", "--NT", "1024", "--NK", "256"])
dmax = max(abs(mid(a["J1"]) - mid(b["J1"])) for a, b in zip(res[200]["boites"], j192["boites"]))
print(f"  max |J1(p128) - J1(p192)| = {dmax:.3e} ; toutes_ok p192 = {j192['toutes_ok']}")

print("G7 NK : 64 / 128 / 512")
for NK in (64, 128, 512):
    j, _ = run(f"G7_NK{NK}", ["--D", "80", "--cap", "200", "--prec", "128", "--NT", "1024", "--NK", str(NK)])
    print(f"  NK={NK} toutes_ok={j['toutes_ok']} pire={pire(j)}")

print("\nECHECS :", ECHECS if ECHECS else "aucun")
sys.exit(1 if ECHECS else 0)
