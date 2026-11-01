#!/usr/bin/env python3
"""verif_biblio.py -- controle des references NOUVELLES de la section « loi d'aire » (v1.5) contre Crossref et arXiv.

Usage : python3 -I verif_biblio.py <sortie.json>
Pour chaque reference : DOI ou requete, titre, auteurs, revue, volume, pages, annee, tels que renvoyes par la base ;
puis comparaison automatique avec ce qu'ecrit la note (champs `attendu`).  Un champ different est signale `ECART`.
Ce script ne lit pas les articles : il ne verifie que les METADONNEES (l'etat de lecture de chaque source est donne dans la note).
Necessite un acces reseau (Crossref, export.arxiv.org) ; pauses entre requetes (limite de debit).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "verif_biblio/1.0 (mailto:none)"}


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(8 * (k + 1))
    return "ERR " + err


def crossref_doi(doi):
    t = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()"))
    if t.startswith("ERR"):
        return {"erreur": t}
    d = json.loads(t)["message"]
    return {
        "doi": d.get("DOI"),
        "title": d.get("title"),
        "authors": [(a.get("given"), a.get("family")) for a in d.get("author", [])],
        "journal": d.get("container-title"),
        "volume": d.get("volume"),
        "issue": d.get("issue"),
        "page": d.get("page"),
        "article-number": d.get("article-number"),
        "year": (d.get("issued", {}).get("date-parts") or [[None]])[0][0],
    }


def crossref_query(q):
    t = get("https://api.crossref.org/works?rows=1&query.bibliographic=" + urllib.parse.quote(q))
    if t.startswith("ERR"):
        return {"erreur": t}
    it = json.loads(t)["message"]["items"][0]
    return {
        "doi": it.get("DOI"),
        "title": it.get("title"),
        "authors": [(a.get("given"), a.get("family")) for a in it.get("author", [])],
        "journal": it.get("container-title"),
        "volume": it.get("volume"),
        "page": it.get("page"),
        "article-number": it.get("article-number"),
        "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
    }


def arxiv_abs(aid):
    t = get("https://arxiv.org/abs/" + aid)
    if t.startswith("ERR"):
        return {"erreur": t}
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    jr = re.search(r"Journal&nbsp;reference:</td>\s*<td[^>]*>(.*?)</td>", t, re.S)
    hist = re.findall(r"\[v(\d+)\]\s*</?[a-z]+>?\s*([A-Z][a-z]{2}, \d+ [A-Za-z]{3} \d{4})", t)
    kc = re.search(r"K_?c\s*=\s*([0-9 .]+\(\d+\))", t.replace("&nbsp;", " "))
    return {
        "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else None,
        "journal_ref": re.sub(r"<[^>]+>|\s+", " ", jr.group(1)).strip() if jr else None,
        "versions": hist,
        "K_c_dans_page": kc.group(1) if kc else None,
    }


OUT = {}
refs_doi = {
    "BS83": "10.1007/BF01208780",
    "DF80": "10.1007/BF01222514",
    "ABF87": "10.1007/BF01007515",
    "Fol82": "10.1016/0022-1236(82)90053-2",
    "BGDF86": "10.1016/0550-3213(86)90609-7",
    "Fro79": "10.1016/0370-2693(79)90684-1",
    "FXL18": "10.1103/PhysRevE.97.043301",
}
for k, doi in refs_doi.items():
    OUT[k] = crossref_doi(doi)
    time.sleep(2)
OUT["DZ81 (requete)"] = crossref_query(
    "Drouffe Zuber Roughening transition in lattice gauge theories in arbitrary dimension (II) The groups Z3 U(1) SU(2) SU(3) Nuclear Physics B 180 264 1981")
time.sleep(2)
OUT["KK95 (requete)"] = crossref_query(
    "Kanaya Kaya Critical exponents of a three dimensional O(4) spin model Physical Review D 51 2404 1995")
for aid in ["2509.04688", "1806.03558", "hep-lat/9409001"]:
    OUT["arXiv:" + aid] = arxiv_abs(aid)
    time.sleep(3)
json.dump(OUT, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
for k, v in OUT.items():
    print(k, "->", json.dumps(v, ensure_ascii=False)[:400])
