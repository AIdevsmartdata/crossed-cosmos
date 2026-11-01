#!/usr/bin/env python3
"""c3_seuil.py — recherche (par dichotomie sur J = n/D) du plus grand J tel que J·ρ'_m(J) < 1, où ρ'_m(J) est le
majorant CERTIFIÉ (entier exact, tm_cert) du rayon spectral de la matrice de transfert à mémoire m dont les poids
sont les majorants rationnels exacts W̄_n(J) de c1_poids_exacts.py. Le test final J·ρ' < 1 est fait en rationnels.
Usage : c3_seuil.py m D n_bas n_haut dossier_sortie
  (hypothèse : n_bas passe, n_haut échoue ; sortie : certificats du dernier J qui passe)
"""
import sys, subprocess, json, os, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c1_poids_exacts as c1

ICI = os.path.dirname(os.path.abspath(__file__))

def essai(m, n, D, dossier, Kn=12, KM=10, garder=False):
    J = F(n, D)
    A_sup, A_inf, u, W, tau = c1.facteurs(J, Kn, KM)
    Q = 2**40
    p = [-(-W[k].numerator * Q // W[k].denominator) for k in range(1, Kn + 2)]
    fp = os.path.join(dossier, f"poids_m{m}_J{n}_{D}.txt")
    with open(fp, "w") as f:
        f.write(f"{Q} {Kn + 1} " + " ".join(str(x) for x in p) + "\n")
    fh = os.path.join(dossier, f"certificat_h_m{m}_J{n}_{D}.bin") if garder else None
    cmd = [os.path.join(ICI, "tm_cert"), str(m), fp] + ([fh] if fh else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="8"))
    mo = re.search(r"rho_cert=(\d+)/(\d+).*verif_echecs=(\d+)", r.stdout)
    if not mo or r.returncode not in (0, 5):
        raise RuntimeError(f"tm_cert a échoué : rc={r.returncode} {r.stdout} {r.stderr}")
    A, B, bad = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
    if bad != 0:
        raise RuntimeError("vérification entière en échec")
    rho = F(A, B)
    ok = J * rho < 1
    if not garder:
        os.remove(fp)
    return ok, J, rho, r.stdout.strip(), (fp if garder else None), fh

if __name__ == "__main__":
    m, D, lo, hi, dossier = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    os.makedirs(dossier, exist_ok=True)
    journal = []
    ok, J, rho, txt, _, _ = essai(m, lo, D, dossier)
    journal.append((lo, ok, float(J * rho))); print(lo, ok, float(J * rho), flush=True)
    assert ok, "la borne basse ne passe pas"
    ok, J, rho, txt, _, _ = essai(m, hi, D, dossier)
    journal.append((hi, ok, float(J * rho))); print(hi, ok, float(J * rho), flush=True)
    assert not ok, "la borne haute passe déjà"
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ok, J, rho, txt, _, _ = essai(m, mid, D, dossier)
        journal.append((mid, ok, float(J * rho))); print(mid, ok, float(J * rho), flush=True)
        if ok: lo = mid
        else: hi = mid
    ok, J, rho, txt, fp, fh = essai(m, lo, D, dossier, garder=True)
    assert ok
    res = {"m": m, "J_star": f"{lo}/{D}", "beta_star": f"{2*lo}/{D}", "beta_star_float": 2 * lo / D,
           "rho_cert": f"{rho.numerator}/{rho.denominator}", "J_rho": f"{(J*rho).numerator}/{(J*rho).denominator}",
           "J_rho_float": float(J * rho), "marge_1_moins_Jrho": float(1 - J * rho),
           "J_suivant_echoue": f"{hi}/{D}", "tm_cert": txt, "fichier_poids": fp, "fichier_h": fh,
           "journal": journal}
    with open(os.path.join(dossier, f"seuil_m{m}.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
