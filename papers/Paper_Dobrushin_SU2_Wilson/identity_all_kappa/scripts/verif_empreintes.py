#!/usr/bin/env python3
"""verif_empreintes.py -- controle d'integrite : chaque JSON de resultats/ qui porte un champ 'script_sha256' doit correspondre au script ACTUEL de scripts/
(le champ est calcule par le script au moment du run).  Verdict CALCULE ; code de sortie != 0 si un resultat provient d'une autre version du script."""
import json, os, sys, hashlib, glob
racine = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sha = {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest() for f in glob.glob(os.path.join(racine, "scripts", "*.py"))}
inv = {}
ok = True
# correspondance resultat -> script producteur
prod = {
    "xi_arb_4s3_20.json": "cert_xi_arb.py", "xi_mpiv_4s3_15.json": "cert_xi_mpiv.py", "xi_mpiv_15_18.json": "cert_xi_mpiv.py", "xi_mpiv_18_20.json": "cert_xi_mpiv.py",
    "ot_controle.json": "ot_controle.py", "synthese_ot.json": "synthese_ot.py", "ident_num_arb.json": "ident_num_arb.py", "ident_num_arb_alea.json": "ident_num_arb.py",
    "ident_num_mp.json": "ident_num_mp.py", "cert_delta_boites.json": "cert_delta_boites.py", "table_valeurs.json": "table_valeurs.py", "d7_limite.json": "d7_limite.py",
    "flux_champ_exact.json": "flux_champ_exact.py", "stress_chaine.json": "stress_chaine.py", "serie_identite_exacte.json": "serie_identite_exacte.py",
    "resume_arb.json": None, "resume_mpiv.json": None,
}
for fn in sorted(glob.glob(os.path.join(racine, "resultats", "*.json"))):
    nom = os.path.basename(fn)
    j = json.load(open(fn))
    s = j.get("script_sha256")
    if s is None:
        print(f"  (pas de champ script_sha256) {nom}")
        continue
    sc = prod.get(nom)
    if sc is None:
        print(f"  (producteur non declare) {nom}")
        continue
    bon = (s == sha[sc])
    ok = ok and bon
    print(f"  {'OK ' if bon else 'ECART'} {nom:32s} <- {sc}")
print("INTEGRITE DES RESULTATS : " + ("TOUS COHERENTS avec les scripts actuels" if ok else "ECHEC (voir ECART)"))
sys.exit(0 if ok else 1)
