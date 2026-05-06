#!/usr/bin/env python3
"""
f2_pari_sweep.py
================================================================================
F2 v3 — TRUE Damerell-level falsifier for M13.1(c) Steinberg-specificity
Uses PARI/GP subprocess for L-value computation (NOT just LMFDB Hecke traces)
--------------------------------------------------------------------------------

Anchor verified 2026-05-06: 4.5.b.a gives α_m^F1 = (1/8, -1/4, 1/3, -2/5)
  → v_2 = {-3, -2, 0, +1} ✓

Tests:
  - Q(i) CM (cm_disc=-4): 4.5.b.a (anchor), 100.5.b.a (level promotion)
  - Q(ω) CM (cm_disc=-3): 27.5.b.a (different K) — does pattern survive?

FALSIFY: any non-Q(i) CM newform exhibiting v_2(α_m^F1) = {-3,-2,0,+1}
  ⇒ M44.1 condition (a) "K = Q(i)" weakens; framework broader than claimed.

PRESERVE: only Q(i) CM newforms exhibit pattern
  ⇒ M44.1(a) Steinberg-K-Q(i) specificity confirmed.
"""

import subprocess
import sys
import re
import csv
from fractions import Fraction


def run_pari(script: str, prec: int = 100) -> str:
    """Run a PARI/GP script via temp-file (avoids shell-quoting issues)."""
    import tempfile
    full = f"default(realprecision, {prec});\n" + script + "\nquit;\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".gp", delete=False) as tf:
        tf.write(full)
        path = tf.name
    try:
        r = subprocess.run(
            ["gp", "-q", path],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if r.returncode != 0:
            sys.stderr.write(f"[pari] rc={r.returncode}\n{r.stderr}\n")
        return r.stdout
    finally:
        import os
        os.unlink(path)


# Period conventions used by PARI's lfunmf normalisation.
# Q(i): Ω = Γ(1/4)² / (2√(2π))  (lemniscate constant)
# Q(ω): Ω = Γ(1/3)³ / (4π·√3)   (Chowla-Selberg analogue)
PARI_PERIOD = {
    -4: "gamma(1/4)^2 / (2 * sqrt(2*Pi))",
    -3: "gamma(1/3)^3 / (4 * Pi * sqrt(3))",
}


def damerell_ladder(level: int, weight: int, char: int, cm_disc: int):
    """Compute (α_m, α_m·F1, v_2) for m=1..4 via PARI. Returns dict."""
    if cm_disc not in PARI_PERIOD:
        return {"err": f"no Ω for disc={cm_disc}"}
    Omega_expr = PARI_PERIOD[cm_disc]
    k = weight
    # Single-statement for-loop body (PARI semicolons inside for() break parser)
    script = f"""
mf = mfinit([{level}, {weight}, {char}], 1);
B = mfbasis(mf);
if(#B == 0, print("EMPTY"); quit);
F = B[1];
Omega = {Omega_expr};
OmegaK = Omega^({k - 1});
L = lfunmf(mf, F);
print("--BEGIN--");
for(m = 1, 4, print("m=", m, " alpha=", bestappr(lfun(L, m) * Pi^({k - 1} - m) / OmegaK, 100000), " F1=", (-2)^(m-1) * (1 + 2^(m-3)), " alpha_F1=", bestappr(lfun(L, m) * Pi^({k - 1} - m) / OmegaK * (-2)^(m-1) * (1 + 2^(m-3)), 100000)));
print("--END--");
"""
    out = run_pari(script)
    return parse_pari_output(out)


def parse_pari_output(out: str):
    """Extract (alpha_m_rat, alpha_F1_rat) tuples from PARI output."""
    rows = {}
    pat = re.compile(
        r"m=\s*(\d+)\s+alpha=\s*(-?\d+/?\d*)\s+F1=\s*(-?\d+/?\d*)\s+alpha_F1=\s*(-?\d+/?\d*)"
    )
    for line in out.splitlines():
        m = pat.search(line.strip())
        if m:
            mm = int(m.group(1))
            alpha = Fraction(m.group(2))
            F1 = Fraction(m.group(3))
            alpha_F1 = Fraction(m.group(4))
            rows[mm] = {"alpha": alpha, "F1": F1, "alpha_F1": alpha_F1}
    return rows


def v2_of_fraction(f: Fraction) -> int:
    """Compute 2-adic valuation v_2 of a Fraction. Returns +∞ if zero."""
    if f == 0:
        return 9999
    n = f.numerator
    d = f.denominator
    v_n = 0
    nn = abs(n)
    while nn % 2 == 0:
        v_n += 1
        nn //= 2
    v_d = 0
    dd = d
    while dd % 2 == 0:
        v_d += 1
        dd //= 2
    return v_n - v_d


# ---------------------------------------------------------------------------
# Test list
# ---------------------------------------------------------------------------

TESTS = [
    # (label, level, weight, mfinit_char, cm_disc, comment)
    # Q(i) CM dim=1 newforms (LMFDB-confirmed)
    ("4.5.b.a", 4, 5, -4, -4, "ANCHOR — N=p²=2² simply ramified, Steinberg, dim=1"),
    ("36.5.d.a", 36, 5, -4, -4, "Q(i) level 4·9 mixed primes, a2=4, dim=1"),
    ("64.5.c.a", 64, 5, -4, -4, "Q(i) level 2⁶ pure power, NOT p² simply ramified, dim=1"),
    ("100.5.b.a", 100, 5, -4, -4, "Q(i) level 4·25 mixed primes, a2=4, dim=1"),
    # Q(ω) CM dim=1 newforms (LMFDB-confirmed)
    ("12.5.c.a", 12, 5, -3, -3, "Q(ω) level 4·3, dim=1"),
    ("27.5.b.a", 27, 5, -3, -3, "Q(ω) level 3³, dim=1"),
    ("48.5.e.a", 48, 5, -3, -3, "Q(ω) level 16·3, dim=1"),
    ("75.5.c.a", 75, 5, -3, -3, "Q(ω) level 3·25, dim=1"),
    ("75.5.c.b", 75, 5, -3, -3, "Q(ω) level 3·25, dim=1, second"),
]


def main():
    print("=" * 70)
    print("F2 v3 — Damerell-level F1 v_2 sweep via PARI/GP")
    print("=" * 70)
    print()

    results = []
    for label, level, weight, char, cm_disc, comment in TESTS:
        print(f"[{label}] {comment}")
        print(f"  mfinit([{level}, {weight}, {char}]); CM by disc {cm_disc}")
        rows = damerell_ladder(level, weight, char, cm_disc)
        if "err" in rows:
            print(f"  ERR: {rows['err']}")
            continue
        if not rows:
            print(f"  PARI returned no rows; check mfinit args / PARI L-precision")
            continue
        v2_pattern = []
        for m in range(1, 5):
            r = rows.get(m)
            if r is None:
                v2_pattern.append("?")
                continue
            v2 = v2_of_fraction(r["alpha_F1"])
            v2_pattern.append(v2)
            print(f"    m={m}: α={r['alpha']}  F1={r['F1']}  α^F1={r['alpha_F1']}  v_2={v2}")
        match = (v2_pattern == [-3, -2, 0, 1])
        print(f"  v_2 = {v2_pattern}  match {{-3,-2,0,+1}}? {match}")
        print()
        results.append({
            "label": label,
            "cm_disc": cm_disc,
            "v2_pattern": v2_pattern,
            "match": match,
            "alpha_1": str(rows.get(1, {}).get("alpha", "?")),
            "alpha_2": str(rows.get(2, {}).get("alpha", "?")),
            "alpha_3": str(rows.get(3, {}).get("alpha", "?")),
            "alpha_4": str(rows.get(4, {}).get("alpha", "?")),
            "alpha_F1_1": str(rows.get(1, {}).get("alpha_F1", "?")),
            "alpha_F1_2": str(rows.get(2, {}).get("alpha_F1", "?")),
            "alpha_F1_3": str(rows.get(3, {}).get("alpha_F1", "?")),
            "alpha_F1_4": str(rows.get(4, {}).get("alpha_F1", "?")),
        })

    # ---------------- VERDICT ----------------
    print("=" * 70)
    print("F2 v3 VERDICT")
    print("=" * 70)
    anchor_match = next(
        (r for r in results if r["label"] == "4.5.b.a"), None
    )
    if anchor_match is None:
        print("ANCHOR MISSING — can't verdict")
        return
    if not anchor_match["match"]:
        print(f"ANCHOR FAIL — 4.5.b.a v_2 = {anchor_match['v2_pattern']}, expected [-3,-2,0,+1]")
        print("Check Ω convention or mfinit char.")
        return
    print(f"ANCHOR PASS — 4.5.b.a v_2 = [-3,-2,0,+1] ✓")
    print()
    qi_other = [r for r in results if r["label"] != "4.5.b.a" and r["cm_disc"] == -4]
    qomega = [r for r in results if r["cm_disc"] == -3]
    print(f"Q(i) other CM newforms (level promotion test):")
    for r in qi_other:
        print(f"  {r['label']}: v_2 = {r['v2_pattern']}  match? {r['match']}")
    print(f"Q(ω) CM newforms (K-divergence test):")
    for r in qomega:
        print(f"  {r['label']}: v_2 = {r['v2_pattern']}  match? {r['match']}")
    print()
    qomega_match = [r for r in qomega if r["match"]]
    if qomega_match:
        print(f"⚡ FALSIFIED M44.1(a) Q(i)-specificity:")
        for r in qomega_match:
            print(f"   {r['label']} (CM disc {r['cm_disc']}) ALSO matches {{-3,-2,0,+1}}")
        print(f"   Framework is BROADER than claimed.")
    else:
        print(f"✓ M44.1(a) Q(i)-specificity SURVIVES — only Q(i) CM newforms hit pattern")
    print()
    print("CSV: f2_v3_results.csv")

    # Save CSV
    with open("f2_v3_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        for r in results:
            w.writerow(r)


if __name__ == "__main__":
    main()
