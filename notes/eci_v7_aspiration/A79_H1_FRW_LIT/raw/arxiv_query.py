#!/usr/bin/env python3
"""Live arXiv API queries for A79 H1 FRW lit review (post-CLPW 2024-2026)."""
import urllib.request, urllib.parse, time, re, json

UA = "A79-FRW-typeII-lit-review/1.0 (kevin.remondiere@gmail.com)"

def query(q, max_results=20, sortBy="submittedDate", sortOrder="descending"):
    url = ("https://export.arxiv.org/api/query?"
           + urllib.parse.urlencode({"search_query": q, "max_results": str(max_results),
                                     "sortBy": sortBy, "sortOrder": sortOrder}))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

def parse(xml):
    if not xml or xml.startswith("ERR"):
        return []
    entries = re.findall(r"<entry>(.*?)</entry>", xml, flags=re.S)
    out = []
    for e in entries:
        idm = re.search(r"<id>(.*?)</id>", e)
        tm = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        pm = re.search(r"<published>(.*?)</published>", e)
        am = re.findall(r"<name>(.*?)</name>", e)
        sm = re.search(r"<summary>(.*?)</summary>", e, flags=re.S)
        cat = re.search(r'primary_category[^/]*term="([^"]+)"', e)
        out.append({
            "id": idm.group(1) if idm else "",
            "title": (tm.group(1) if tm else "").strip().replace("\n", " "),
            "published": pm.group(1)[:10] if pm else "",
            "authors": am,
            "summary": (sm.group(1) if sm else "").strip().replace("\n", " "),
            "cat": cat.group(1) if cat else ""
        })
    return out

queries = [
    ("type II algebra cosmology",
     'all:"type II" AND all:cosmology AND cat:hep-th'),
    ("crossed product cosmology",
     'all:"crossed product" AND all:cosmology'),
    ("gravitational algebra observer",
     'all:"gravitational algebra" AND all:"observer"'),
    ("crossed product de Sitter 2024+",
     'all:"crossed product" AND all:"de Sitter" AND cat:hep-th'),
    ("Chandrasekaran follow-up",
     'au:Chandrasekaran AND cat:hep-th'),
    ("Witten algebra observer",
     'au:Witten AND all:"observer" AND all:algebra'),
    ("Faulkner Speranza followup",
     'au:Faulkner AND au:Speranza'),
    ("Penington algebra cosmology",
     'au:Penington AND cat:hep-th'),
    ("inflationary von Neumann",
     'all:"von Neumann" AND all:inflation'),
    ("intrinsic observer cosmology",
     'all:"intrinsic observer"'),
    ("Speranza algebra cosmology",
     'au:Speranza AND cat:hep-th'),
    ("Jefferson crossed product",
     'au:Jefferson AND all:"crossed product"'),
    ("modular Hamiltonian FRW",
     'all:"modular Hamiltonian" AND all:FRW'),
    ("modular flow cosmological",
     'all:"modular" AND all:cosmological AND all:algebra'),
    ("Klinger Leigh algebra",
     'au:Klinger AND au:Leigh'),
    ("Kudler-Flam crossed product",
     'au:"Kudler-Flam"'),
    ("Ali Ahmad Jefferson",
     'au:"Ali Ahmad"'),
    ("Gomez de Sitter crossed",
     'au:Gomez AND all:"crossed product"'),
    ("Frob modular de Sitter",
     'au:Fröb AND all:"de Sitter"'),
    ("De Vuyst Speranza",
     'au:"De Vuyst"'),
    ("Kawamoto inflation 2024+",
     'au:Kawamoto AND all:inflation'),
    ("Bahiru observer",
     'au:Bahiru'),
    ("type II_infty cosmology",
     'all:"II_\\infty" AND all:cosmology'),
    ("II_1 II_infty FRW",
     'all:"II_1" AND all:cosmolog'),
    ("FRW algebraic QFT",
     'all:FRW AND all:"algebraic QFT"'),
    ("Mertens Speranza",
     'au:Mertens AND all:algebra'),
    ("Witten 2024 cosmolog",
     'au:Witten AND all:cosmolog'),
    ("Penington 2024 cosmology",
     'au:Penington AND all:cosmolog'),
    ("Hollands Sanders algebra",
     'au:Hollands AND all:"de Sitter"'),
    ("Verch algebraic curved",
     'au:Verch AND all:"crossed product"'),
    ("Faulkner Hollands modular",
     'au:Faulkner AND all:modular'),
    ("Bisognano-Wichmann FRW",
     'all:"Bisognano" AND all:FRW'),
]

results = {}
all_lines = []
for label, q in queries:
    all_lines.append(f"\n=== QUERY: {label} ===\n   q={q}")
    xml = query(q, max_results=15)
    if xml.startswith("ERR"):
        all_lines.append(xml)
        continue
    ents = parse(xml)
    for e in ents:
        tag = "RECENT" if e["published"] >= "2024-01-01" else "older "
        all_lines.append(f"- [{tag}] {e['published']} | {e['id'].rsplit('/',1)[-1]:18s} | [{e['cat']}] {e['title'][:130]}")
        all_lines.append(f"   authors: {', '.join(e['authors'][:5])}")
    for e in ents:
        if e["published"] >= "2024-01-01":
            key = e["id"].rsplit("/",1)[-1].split("v")[0]
            if key not in results:
                results[key] = e
    time.sleep(3.2)

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/A79_H1_FRW_LIT/raw/arxiv_results.txt", "w") as f:
    f.write("\n".join(all_lines))

with open("/root/crossed-cosmos/notes/eci_v7_aspiration/A79_H1_FRW_LIT/raw/arxiv_recent.json", "w") as fj:
    json.dump(results, fj, indent=2)
print(f"done, {len(results)} unique 2024+ entries")
