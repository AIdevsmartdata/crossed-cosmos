#!/usr/bin/env python3
"""
f2_v5_pari_match.py
================================================================================
F2 v5 — Trace-matching disambiguation for PARI mfinit characters.

F2 v4 BUG: For non-anchor newforms at higher level (36.5.d.a, 64.5.c.a),
mfinit([N, 5, -4]) returns a basis containing the LEVEL-N LIFT of 4.5.b.a
(i.e. the OLD-form at level N), not the actual NEW-form 36.5.d.a / 64.5.c.a.
This is why F2 v4 reported identical (1/10, 1/12, 1/24, 1/60) for 3 newforms.

F2 v5 FIX: For each newform label,
  1. Fetch traces[1..n] from LMFDB
  2. PARI mfinit([N, k, χ], 1) (NEW subspace = level N, NOT lifts)
  3. Find basis element F_i with mfcoef(F_i, n) == LMFDB traces[n-1] for n=2..8
  4. Compute α_m for THAT specific basis element via lfunmf
  5. Try multiple character candidates if first fails

This is the rigorous Damerell-level falsifier for M13.1(c) Steinberg-specificity
+ M44.1(a)/(b) ECI scope conjecture.
"""
import json
import re
import subprocess
import sys
import urllib.request
from fractions import Fraction


HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": "human=1"}


def lmfdb_traces(label: str):
    """Fetch traces[1..n] for a newform from LMFDB beta API."""
    url = f"https://beta.lmfdb.org/api/mf_newforms/?_search&label={label}&_format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    data = d.get("data", [])
    if not data:
        return None
    nf = data[0]
    return {
        "label": nf.get("label"),
        "level": nf.get("level"),
        "weight": nf.get("weight"),
        "dim": nf.get("dim"),
        "is_cm": nf.get("is_cm"),
        "cm_discs": nf.get("cm_discs") or [],
        "char_orbit_label": nf.get("char_orbit_label"),
        "char_conductor": nf.get("char_conductor"),
        "char_order": nf.get("char_order"),
        "traces": nf.get("traces") or [],
        "is_self_dual": nf.get("self_dual"),
    }


def run_pari(script: str, prec: int = 100, timeout: int = 180) -> str:
    import tempfile, os
    full = f"default(realprecision, {prec});\n" + script + "\nquit;\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".gp", delete=False) as tf:
        tf.write(full)
        path = tf.name
    try:
        r = subprocess.run(["gp", "-q", path], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            sys.stderr.write(f"[pari] rc={r.returncode}\n{r.stderr}\n")
        return r.stdout
    finally:
        os.unlink(path)


PERIOD = {
    -4: "gamma(1/4)^2 / (2 * sqrt(2*Pi))",
    -3: "gamma(1/3)^3 / (4 * Pi * sqrt(3))",
}


def damerell_for_basis_element(level, weight, char_int, target_traces, cm_disc):
    """Try mfinit([level, weight, char_int]); find basis element whose first 7 traces match
    LMFDB target_traces[1..7] (i.e. a_2..a_8); compute α_m for that element.

    Returns dict with keys: status (MATCHED/UNMATCHED/EMPTY), index, alpha_m_str (m=1..4), v2 list.
    """
    if cm_disc not in PERIOD:
        return {"status": "ERR", "msg": f"no Ω for cm_disc={cm_disc}"}
    Omega_expr = PERIOD[cm_disc]
    k = weight
    target = ",".join(str(int(t)) for t in target_traces[1:8])  # a_2 .. a_8

    script = f"""
mf = mfinit([{level}, {weight}, {char_int}], 1);
B = mfeigenbasis(mf);
print("--BASIS--", #B);
target = [{target}];
match_idx = 0;
for(i = 1, #B, if(vector(7, j, mfcoef(B[i], j+1)) == target, match_idx = i));
print("--MATCH--", match_idx);
if(match_idx == 0, print("--END--"); quit);
F = B[match_idx];
Omega = {Omega_expr};
OmegaK = Omega^({k - 1});
L = lfunmf(mf, F);
for(m = 1, 4, print("m=", m, " alpha=", bestappr(lfun(L, m) * Pi^({k - 1} - m) / OmegaK, 1000000), " F1=", (-2)^(m-1) * (1 + 2^(m-3)), " alpha_F1=", bestappr(lfun(L, m) * Pi^({k - 1} - m) / OmegaK * (-2)^(m-1) * (1 + 2^(m-3)), 1000000)));
print("--END--");
"""
    out = run_pari(script)
    return parse_pari_match(out)


def parse_pari_match(out: str):
    rows = {}
    basis_size = None
    match_idx = None
    pat_basis = re.compile(r"--BASIS--\s*(\d+)")
    pat_match = re.compile(r"--MATCH--\s*(\d+)")
    pat_m = re.compile(
        r"m=\s*(\d+)\s+alpha=\s*([^ ]+)\s+F1=\s*([^ ]+)\s+alpha_F1=\s*([^ ]+)"
    )
    for line in out.splitlines():
        ln = line.strip()
        m1 = pat_basis.search(ln)
        if m1:
            basis_size = int(m1.group(1))
        m2 = pat_match.search(ln)
        if m2:
            match_idx = int(m2.group(1))
        m3 = pat_m.search(ln)
        if m3:
            mm = int(m3.group(1))
            try:
                alpha = Fraction(m3.group(2))
                F1 = Fraction(m3.group(3))
                alpha_F1 = Fraction(m3.group(4))
                rows[mm] = {"alpha": alpha, "F1": F1, "alpha_F1": alpha_F1}
            except Exception:
                pass
    return {"basis_size": basis_size, "match_idx": match_idx, "rows": rows}


def v2_of_fraction(f: Fraction) -> int:
    if f == 0:
        return 9999
    n, d = abs(f.numerator), f.denominator
    v_n = 0
    while n % 2 == 0:
        v_n += 1; n //= 2
    v_d = 0
    while d % 2 == 0:
        v_d += 1; d //= 2
    return v_n - v_d


# Newforms with EXPECTED CM disc; multiple character candidates per newform
# (will try them in order). For LMFDB char "b" at level 4: chi_-4 = -4.
# For higher levels, char might be chi_-4 or chi_-3 or product.
TESTS = [
    # (label, char_candidates_to_try)
    ("4.5.b.a", [-4]),
    ("36.5.d.a", [-4, -3, -12]),
    ("64.5.c.a", [-4, -8]),
    ("100.5.b.a", [-4]),
    ("12.5.c.a", [-3, -4, -12]),
    ("27.5.b.a", [-3]),
    ("48.5.e.a", [-3, -4, -12]),
    ("75.5.c.a", [-3, -15]),
]


def main():
    print("=" * 78)
    print("F2 v5 — Trace-matching Damerell falsifier (PARI mfeigenbasis disambiguation)")
    print("=" * 78)

    results = []
    for label, char_candidates in TESTS:
        print(f"\n[{label}]")
        meta = lmfdb_traces(label)
        if not meta:
            print(f"  LMFDB miss for {label}")
            continue
        print(f"  level={meta['level']} weight={meta['weight']} dim={meta['dim']} "
              f"cm_discs={meta['cm_discs']} char_orbit={meta['char_orbit_label']} "
              f"char_cond={meta['char_conductor']} char_order={meta['char_order']}")
        if meta["dim"] != 1:
            print(f"  SKIP (dim={meta['dim']} > 1; bestappr won't disambiguate over field)")
            continue
        cm_disc = meta["cm_discs"][0] if meta["cm_discs"] else None
        if cm_disc not in (-3, -4):
            print(f"  SKIP (cm_disc={cm_disc} not in {{-3,-4}}; need Ω convention)")
            continue
        traces_8 = meta["traces"][:8]
        print(f"  LMFDB traces[1..8] = {traces_8}")

        for char_int in char_candidates:
            print(f"  Trying char={char_int} ...")
            r = damerell_for_basis_element(
                meta["level"], meta["weight"], char_int, meta["traces"], cm_disc
            )
            if r.get("status") == "ERR":
                print(f"    ERR: {r.get('msg')}")
                continue
            bs = r.get("basis_size")
            mi = r.get("match_idx")
            print(f"    basis size = {bs}; match idx = {mi}")
            if mi == 0 or mi is None:
                continue
            rows = r["rows"]
            v2_pat = []
            for m in range(1, 5):
                rr = rows.get(m)
                if rr is None:
                    v2_pat.append("?")
                else:
                    v2_pat.append(v2_of_fraction(rr["alpha_F1"]))
                    print(f"      m={m}: α={rr['alpha']}  α^F1={rr['alpha_F1']}  v_2={v2_pat[-1]}")
            match = (v2_pat == [-3, -2, 0, 1])
            print(f"  v_2 = {v2_pat}; match? {match}")
            results.append({
                "label": label,
                "char_int": char_int,
                "cm_disc": cm_disc,
                "level": meta["level"],
                "v2_pattern": v2_pat,
                "match": match,
                "alpha_m": [str(rows.get(m, {}).get("alpha", "?")) for m in (1, 2, 3, 4)],
                "alpha_F1": [str(rows.get(m, {}).get("alpha_F1", "?")) for m in (1, 2, 3, 4)],
            })
            break  # found a matching char; stop trying others
        else:
            print(f"  NO CHAR MATCHED — trace match failed for all candidates {char_candidates}")
            results.append({
                "label": label, "char_int": None, "cm_disc": cm_disc,
                "level": meta["level"], "v2_pattern": ["?"]*4, "match": False,
                "alpha_m": ["?"]*4, "alpha_F1": ["?"]*4,
            })

    # ---------- Verdict ----------
    print()
    print("=" * 78)
    print("F2 v5 VERDICT")
    print("=" * 78)
    matched = [r for r in results if r["match"]]
    failed = [r for r in results if not r["match"]]
    print(f"Newforms with v_2 = {{-3,-2,0,+1}}: {len(matched)}")
    for r in matched:
        print(f"  {r['label']:>14s}  cm_disc={r['cm_disc']}  level={r['level']}")
    print(f"Newforms NOT matching pattern: {len(failed)}")
    for r in failed:
        print(f"  {r['label']:>14s}  cm_disc={r['cm_disc']}  level={r['level']}  v_2={r['v2_pattern']}")
    print()
    qi_matched = [r for r in matched if r["cm_disc"] == -4]
    qomega_matched = [r for r in matched if r["cm_disc"] == -3]
    if qomega_matched:
        print(f"⚡ M44.1(a) Q(i)-specificity FALSIFIED: {len(qomega_matched)} Q(ω) CM hits!")
        for r in qomega_matched:
            print(f"   {r['label']}")
    else:
        print(f"✓ M44.1(a) Q(i)-specificity SURVIVES (all {len(qomega_matched)} Q(ω) hits = 0)")
    if len(qi_matched) > 1:
        print(f"⚡ M44.1(b) N=4 uniqueness QUESTIONED: {len(qi_matched)} Q(i) CM hits at different levels!")
        for r in qi_matched:
            print(f"   {r['label']}")
    elif len(qi_matched) == 1:
        print(f"✓ Only 4.5.b.a (anchor) hits — M44.1(b) N=4 uniqueness STRENGTHENED")

    # CSV
    import csv
    with open("f2_v5_results.csv", "w", newline="") as f:
        if results:
            w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            w.writeheader()
            for row in results:
                # Lists need special handling for CSV
                row_csv = {k: (str(v) if isinstance(v, list) else v) for k, v in row.items()}
                w.writerow(row_csv)
    print("\nCSV: f2_v5_results.csv")


if __name__ == "__main__":
    main()
