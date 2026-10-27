#!/usr/bin/env python3
# export_lean.py -- CH (chordal certificate) : JSON de cert_ch.py -> Donnees.lean (module KevYM.Certif.DobrushinCordale.Donnees).
# Arrondis SORTANTS a 2^-40 : lb vers le bas, h0/h1 vers le haut ; re-verification exacte (fractions) de h < lb
# et du chainage des boites [k0, k1] de 0 a K AVANT d'ecrire. Refuse tout JSON qui n'est pas ch-v1, cap < L, ou pas TOUTES_OK.
import json, sys, math, hashlib
from fractions import Fraction as F

src, dst = sys.argv[1], sys.argv[2]
j = json.load(open(src))
assert j["version"] == "ch-v1", "JSON non ch-v1 : refuse"
assert j["cap"] >= j["L"], "cap < L : refuse"
assert j["toutes_ok"] is True, "certificat pas TOUTES_OK : refuse"
S = 2 ** 40


def down(x):
    return F(math.floor(x * S), S)


def up(x):
    return F(math.ceil(x * S), S)


def q(x):
    return f"({x.numerator}:ℚ)/{x.denominator}" if x.denominator != 1 else f"({x.numerator}:ℚ)"


rows = []
prev = F(0)
for b in j["boites"]:
    k0, k1 = F(b["k0"]), F(b["k1"])
    lb, h0, h1 = down(F(b["LB_lo_exact"])), up(F(b["J0_hi_exact"])), up(F(b["J1_hi_exact"]))
    assert k0 == prev and k0 < k1, "chainage"
    assert h0 < lb and h1 < lb, "arrondi : la boite ne passe plus"
    prev = k1
    rows.append((k0, k1, lb, h0, h1))
assert prev == F(j["K"]), "la derniere boite ne finit pas en K"
sha_json = hashlib.sha256(open(src, "rb").read()).hexdigest()
pire = min(r[2] - max(r[3], r[4]) for r in rows)
with open(dst, "w") as f:
    f.write(f"""/-
  CH (28/09/2026) — DONNÉES générées par export_lean.py depuis {src.split('/')[-1]}
  (sha256 {sha_json[:16]}…). Certificat Arb : cert_ch.py (sha256 {j['script_sha256'][:16]}…),
  ctx.cap = {j['cap']}, ctx.prec = {j['prec']}, L = {j['L']} (garde : chaque série de longueur L), ordre D = {j['D']}
  (restes de Cauchy pour tous les ordres > D), NT = {j['NT']} sous-intervalles en y₁, NK = {j['NK']} boîtes en κ.
  Boîte = ⟨k0, k1, lb, h0, h1⟩ : sur κ ∈ [k0, k1], lb ≤ (E x₂² − Var x₁)/κ², J̃0 ≤ h0, J̃1 ≤ h1
  (arrondis sortants à 2^-40 ; pire écart lb − max(h0,h1) = {float(pire):.6e}).
-/
import KevYM.Certif.DobrushinCordale.Verif

namespace KevYM.Certif.DobrushinCordale

/-- borne supérieure du domaine en κ : K = 4/3 = 6 · (2/9). -/
def KC : ℚ := {q(F(j['K']))}

/-- boîtes certifiées (Arb), chaînées de 0 à KC. -/
def boites : List Boite := [
""")
    f.write(",\n".join(f"  ⟨{q(a)}, {q(b)}, {q(c)}, {q(d)}, {q(e)}⟩" for a, b, c, d, e in rows))
    f.write(f"""
]

theorem boites_length : boites.length = {len(rows)} := by decide +kernel

/-- Chaque boîte passe : `h0 < lb`, `h1 < lb`, `k0 ≤ k1` (évaluation noyau, rationnels exacts). -/
theorem boites_ok : boites.all Boite.ok = true := by decide +kernel

/-- Les boîtes se chaînent exactement de 0 à KC. -/
theorem boites_chaine : chaine boites 0 KC = true := by decide +kernel

end KevYM.Certif.DobrushinCordale
""")
print(f"export : {len(rows)} boites, pire lb - max(h) = {float(pire):.6e}, sha JSON {sha_json[:16]}")
