"""Export des certificats (bornes sup rationnelles des coefficients de Φ(w), w = κ²) vers Lean.
Arrondi VERS LE HAUT sur la grille 2^-40, re-vérification exacte (Fractions) de la borne monotone, marges."""
import json, sys, math
from fractions import Fraction as Fr
src = sys.argv[1]; out = sys.argv[2]
d = json.load(open(src)); KW = Fr(d['K']) ** 2
# v2 : refuser tout JSON qui ne vient pas du cert_lien.py v2 à cap explicite suffisant
assert d.get('version') == 'v2-cap-explicite', "JSON pas issu de cert_lien.py v2"
assert d['cap'] >= d['L'] == d['D'] + 1, ("cap insuffisant", d['cap'], d['L'])
assert all(len(bx['his']) == d['D'] // 2 for bx in d['boites'])
def up(q, e=40): return Fr(math.ceil(q * 2 ** e), 2 ** e)
def bP(cs, a, b): return sum(max(c * a ** k, c * b ** k) for k, c in enumerate(cs))
boites = []; worst = None
for bx in d['boites']:
    assert bx['ok'] and bx['gate_E0'] and bx['gate_impairs']
    assert bx['pieces'] == [['0', str(KW)]], bx['pieces']
    cs = [up(Fr(h)) for h in bx['his']]
    v = bP(cs, Fr(0), KW); assert v < 0
    boites.append(cs); worst = v if worst is None or v > worst else worst
print(f"{len(boites)} boîtes ; w ∈ [0, {KW}] ; pire borne (la moins négative) = {float(worst):.6f}")
L = []
L.append("/-\n  C2 (27/09/2026) — DONNÉES générées par export_lean.py (v2) depuis " + src.split('/')[-1] + ".\n"
         f"  Certificat Arb : cert_lien.py v2, sha256 {d['script_sha256'][:16]}…, ctx.cap = {d['cap']}, ctx.prec = {d['prec']},\n"
         f"  N = {d['N']}, NG = {d['NG']}, ordres κ^0..κ^{d['D']} calculés (garde : chaque série de longueur {d['L']}), reste de Taylor ≥ κ^{d['D']+1}.\n"
         "  REMPLACE les données du commit 1f3ace0, fausses : ctx.cap = 10 (défaut python-flint) y tronquait les séries à κ⁹.\n"
         "  Boîte i : α ∈ [iπ/NB, (i+1)π/NB]. cs = bornes SUP rationnelles (Arb, arrondies vers le haut à 2^-40)\n"
         "  des coefficients de Φ(w) = Σ_k E_{2k+2} w^k (+ reste et correction dans le terme constant).\n-/")
L.append("import KevYM.Certif.DobrushinLien.Verif\n\nnamespace KevYM.Certif.DobrushinLien\n")
L.append(f"/-- borne supérieure de w = κ² : K² avec K = 59/50 ≥ 3π/8. -/\ndef KW : ℚ := {KW.numerator}/{KW.denominator}\n")
L.append("/-- coefficients certifiés, une liste par boîte en α. -/\ndef certs : List (List ℚ) := [")
for i, cs in enumerate(boites):
    L.append("  [" + ", ".join(f"({c.numerator}:ℚ)/{c.denominator}" for c in cs) + "]" + ("," if i < len(boites) - 1 else ""))
L.append("]\n")
L.append(f"theorem certs_length : certs.length = {len(boites)} := by decide +kernel\n")
L.append("/-- Chaque boîte passe la vérification (évaluation noyau, rationnels exacts). -/\n"
         "theorem certs_ok : certs.all (fun cs => decide (bP cs 0 0 KW < 0)) = true := by decide +kernel\n")
L.append("end KevYM.Certif.DobrushinLien")
open(out, 'w').write("\n".join(L) + "\n")
print("écrit", out)
