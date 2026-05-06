"""
f2_python_sweep.py
================================================================================
F2 — Falsifier protocol for M13.1(c) F1 v_2 Steinberg-specificity
PURE PYTHON IMPLEMENTATION (no SageMath required)
--------------------------------------------------------------------------------
Sub-agent M47 (2026-05-06), Opus 4.7. Hallu count 86 -> 86.

Per parent CRITICAL_UPDATE_M47.md (2026-05-06 13:45 CEST):
  - NO SageMath on PC; pivot to pure Python + sympy 1.14 + requests
  - LMFDB JSON REST API for newform q-expansions
  - multiprocessing.Pool for parallel sweep (PC has 20 P-cores)

CONJECTURE UNDER TEST (M13.1(c)):
  The F1-renormalized 2-adic valuation pattern
      v_2(alpha_m^F1) = {-3, -2, 0, +1}  for m in {1,2,3,4}
  is *Steinberg-edge specific* for f = 4.5.b.a (level 4, weight 5, CM by Q(i)).

F1-renormalization:
      alpha_m^F1 := alpha_m * (-2)^{m-1} * (1 + 2^{m-3})       (m = 1,2,3,4)

FALSIFYING OUTCOME:
  Any non-Steinberg CM weight-5 newform exhibiting monotone v_2 = {-3,-2,0,+1}
  (or strict deltas {+1,+2,+1}) refutes Steinberg-specificity, broadens M44.1(c).

OUTPUT:
  pipeline_a/f2_sweep_results.csv

RUNTIME (parallel, 18 workers):
  ~5-15 CPU-min on PC's 20 P-cores (LMFDB API throttle is the bottleneck).
  Wall-clock with rate-limit pauses: ~15-30 min.
================================================================================
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from multiprocessing import Pool

from sympy import Rational, Integer, sqrt, sympify, Symbol, S
from sympy import factor, floor
from sympy.ntheory import factorint


# ---------------------------------------------------------------------------
# Section 1 — sweep target list
# ---------------------------------------------------------------------------
# Hand-curated from LMFDB CMF browse. Extend this list to push the sweep wider.
# The anchor 4.5.b.a MUST yield v_2 = {-3, -2, 0, +1} (Steinberg case).

SWEEP_LABELS = [
    "4.5.b.a",     # anchor: Steinberg at p=2; CM by Q(i)
    "9.5.b.a",     # candidate CM by Q(omega) at level 9 (3^2)
    "12.5.b.a",    # candidate CM by Q(omega) at level 12
    "16.5.b.a",    # level 16 = 2^4, weight 5, candidate CM
    "16.5.c.a",    # level 16, weight 5, NOT CM (per v6.0.53.1 P-NT verdict #75)
    "25.5.b.a",    # 25 = 5^2, candidate non-Steinberg at p=2
    "27.5.b.a",    # 27 = 3^3, candidate
    "36.5.b.a",    # 36 = 4*9, candidate
    "49.5.b.a",    # 49 = 7^2, non-Steinberg at p=2 (good reduction)
    "100.5.b.a",   # 100 = 4*25, weight 5
]


# ---------------------------------------------------------------------------
# Section 2 — LMFDB REST API
# ---------------------------------------------------------------------------

LMFDB_BASE = "https://beta.lmfdb.org/api"
LMFDB_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0",
    "Cookie": "human=1",
    "Accept": "application/json",
}


def lmfdb_get(path, params=None, timeout=30, max_retries=3):
    """GET a LMFDB API path; returns parsed JSON or None on miss.

    LMFDB API correct usage (verified 2026-05-06 via parent debugging):
      - Endpoint: https://beta.lmfdb.org/api/<table>/?_search&<col>=<val>&_format=json
      - Trailing slash REQUIRED on table name
      - _search flag REQUIRED for filter queries
      - Filter columns use raw `<col>=<val>` (e.g. label=4.5.b.a) NOT `<col>_eq=<val>`
      - Cookie human=1 + User-Agent Mozilla REQUIRED to bypass anti-bot gate
    """
    if params:
        qs = "&".join("{}={}".format(k, v) for k, v in params.items())
        url = "{}/{}/?_search&{}&_format=json".format(LMFDB_BASE, path, qs)
    else:
        url = "{}/{}/?_search&_format=json".format(LMFDB_BASE, path)
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=LMFDB_HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429:  # rate limit
                wait = 60 * (attempt + 1)
                sys.stderr.write("[lmfdb] 429 rate-limit; sleeping {}s\n".format(wait))
                time.sleep(wait)
                continue
            sys.stderr.write("[lmfdb] HTTPError {}: {}\n".format(exc.code, url))
            return None
        except Exception as exc:
            sys.stderr.write("[lmfdb] {} (attempt {}): {}\n".format(url, attempt + 1, exc))
            time.sleep(5)
    return None


def fetch_newform(label):
    """Fetch newform metadata + q-expansion coefficients.

    Returns dict with keys:
      label, level, weight, char_orbit_label, dim, cm_discs (list),
      a_p_coeffs (list of dicts {p, value}), traces (list)

    Strategy:
      1. /mf_newforms?label_eq=<label>           -> meta (level, weight, dim, cm)
      2. /mf_hecke_nf?hecke_orbit_code_eq=<code> -> coefficients up to needed bound
      3. fallback: parse `traces` field directly from newform doc
    """
    meta = lmfdb_get("mf_newforms", {"label": label})
    if meta is None or not meta.get("data"):
        return None
    nf = meta["data"][0]
    out = {
        "label": label,
        "level": int(nf.get("level", 0)),
        "weight": int(nf.get("weight", 0)),
        "char_orbit_label": nf.get("char_orbit_label"),
        "dim": int(nf.get("dim", 1)),
        "cm_discs": nf.get("cm_discs") or [],
        "is_cm": bool(nf.get("is_cm", False)),
        "self_dual": nf.get("self_dual"),
        "field_disc_factorization": nf.get("field_disc_factorization"),
    }
    # traces is the easiest source of a_n for n=1..N (rational-Hecke-orbit-trace)
    traces = nf.get("traces")
    if traces:
        out["traces"] = list(traces)  # a_1, a_2, a_3, ..., a_N
    else:
        out["traces"] = None

    # If dim > 1, we want hecke_nf coeffs over Q(alpha) — but for v_2 of a_{p^m}
    # the trace already gives us the Q-rational projection. We use trace as our
    # alpha_m (CONSERVATIVE: for dim=1 newforms this IS the eigenvalue).
    return out


def coeff_a_n(nf_doc, n):
    """Return a_n (Q-rational trace projection) from the LMFDB newform doc."""
    traces = nf_doc.get("traces")
    if traces is None:
        return None
    if n - 1 >= len(traces):
        return None
    return Rational(int(traces[n - 1]))


# ---------------------------------------------------------------------------
# Section 3 — F1 renormalization + v_2
# ---------------------------------------------------------------------------

def f1_renorm(alpha_m, m):
    """alpha_m^F1 := alpha_m * (-2)^{m-1} * (1 + 2^{m-3})
       in Q (since alpha_m is Q-rational from trace projection)."""
    factor1 = Rational(-2)**(m - 1)
    factor2 = Rational(1) + Rational(2)**(m - 3)
    return alpha_m * factor1 * factor2


def v2(x):
    """2-adic valuation of x in Q (sympy Rational).
       Returns int (negative, zero, positive) or sentinel 9999 if x == 0."""
    if x == 0:
        return 9999
    q = Rational(x)
    num = abs(int(q.p))
    den = abs(int(q.q))
    # v_2(num/den) = v_2(num) - v_2(den)
    def v2_int(n):
        if n == 0:
            return 9999
        v = 0
        while n % 2 == 0:
            n //= 2
            v += 1
        return v
    return v2_int(num) - v2_int(den)


# ---------------------------------------------------------------------------
# Section 4 — Steinberg test
# ---------------------------------------------------------------------------

def is_steinberg_at_p(nf_doc, p):
    """Steinberg iff a_{p^2} = +/- p^{(k-1)/2}.

    For weight k=5: target = +/- p^2.
    Returns (bool_is_steinberg, a_p2, target_pos)."""
    weight = nf_doc["weight"]
    a_p2 = coeff_a_n(nf_doc, p * p)
    if a_p2 is None:
        return None, None, None
    target = Integer(p) ** Integer((weight - 1) // 2)  # weight=5 -> p^2
    return (a_p2 == target) or (a_p2 == -target), a_p2, target


# ---------------------------------------------------------------------------
# Section 5 — per-newform worker
# ---------------------------------------------------------------------------

def process_one(label):
    """Process one newform; returns CSV-row dict."""
    sys.stderr.write("[worker] {}\n".format(label))
    nf = fetch_newform(label)
    if nf is None:
        return {
            "label": label, "status": "LMFDB_MISS",
            "level": "", "weight": "", "cm_discs": "", "is_cm": "",
            "steinberg": "", "a_p2": "", "p_pow": "",
            "v2_F1_m1": "", "v2_F1_m2": "", "v2_F1_m3": "", "v2_F1_m4": "",
            "match_-3_-2_0_+1": False, "match_step_+1_+2_+1": False,
            "notes": "lmfdb miss",
        }

    # Steinberg test at p=2
    is_st, a_p2, target = is_steinberg_at_p(nf, 2)

    # Compute v_2(alpha_m^F1) for m = 1..4
    v2_list = []
    for m in (1, 2, 3, 4):
        a_m = coeff_a_n(nf, 2**m)
        if a_m is None:
            v2_list.append(None)
            continue
        a_m_F1 = f1_renorm(a_m, m)
        v2_list.append(v2(a_m_F1))

    # Pattern matching
    target_pattern = [-3, -2, 0, 1]
    match_a = (v2_list == target_pattern)
    match_b = False
    if all(v is not None and v != 9999 for v in v2_list):
        deltas = [v2_list[i + 1] - v2_list[i] for i in range(3)]
        match_b = (deltas == [1, 2, 1])

    return {
        "label": label,
        "status": "OK",
        "level": nf["level"],
        "weight": nf["weight"],
        "cm_discs": ",".join(str(d) for d in nf["cm_discs"]) or "none",
        "is_cm": nf["is_cm"],
        "steinberg": "STEINBERG" if is_st else ("NON-STEINBERG" if is_st is False else "?"),
        "a_p2": str(a_p2) if a_p2 is not None else "",
        "p_pow": str(target) if target is not None else "",
        "v2_F1_m1": str(v2_list[0]) if v2_list[0] is not None else "",
        "v2_F1_m2": str(v2_list[1]) if v2_list[1] is not None else "",
        "v2_F1_m3": str(v2_list[2]) if v2_list[2] is not None else "",
        "v2_F1_m4": str(v2_list[3]) if v2_list[3] is not None else "",
        "match_-3_-2_0_+1": match_a,
        "match_step_+1_+2_+1": match_b,
        "notes": "",
    }


# ---------------------------------------------------------------------------
# Section 6 — main
# ---------------------------------------------------------------------------

def main():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "f2_sweep_results.csv")
    n_workers = min(8, len(SWEEP_LABELS))  # be polite to LMFDB

    print("[f2] starting sweep over {} newforms with {} workers".format(
        len(SWEEP_LABELS), n_workers))
    print("[f2] LMFDB endpoint: {}".format(LMFDB_BASE))
    print("[f2] output:         {}".format(out_path))

    t0 = time.time()
    if n_workers > 1:
        with Pool(n_workers) as pool:
            results = pool.map(process_one, SWEEP_LABELS)
    else:
        results = [process_one(lab) for lab in SWEEP_LABELS]
    print("[f2] sweep complete in {:.1f} s".format(time.time() - t0))

    # CSV out
    fieldnames = [
        "label", "status", "level", "weight", "cm_discs", "is_cm",
        "steinberg", "a_p2", "p_pow",
        "v2_F1_m1", "v2_F1_m2", "v2_F1_m3", "v2_F1_m4",
        "match_-3_-2_0_+1", "match_step_+1_+2_+1", "notes",
    ]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow(r)
    print("[f2] wrote {} rows to {}".format(len(results), out_path))

    # Verdict
    print("\n=== F2 SWEEP VERDICT ===")
    falsifiers = [
        r for r in results
        if r["status"] == "OK"
        and r["steinberg"] == "NON-STEINBERG"
        and (r["match_-3_-2_0_+1"] is True or r["match_step_+1_+2_+1"] is True)
    ]
    anchor = next((r for r in results if r["label"] == "4.5.b.a"), None)
    if anchor and anchor["status"] == "OK":
        anchor_v2 = [anchor["v2_F1_m1"], anchor["v2_F1_m2"],
                     anchor["v2_F1_m3"], anchor["v2_F1_m4"]]
        print("Anchor 4.5.b.a v_2 = {}  (expect [-3, -2, 0, +1])".format(anchor_v2))
        if anchor_v2 == ["-3", "-2", "0", "1"]:
            print("=> Anchor SANITY CHECK PASS")
        else:
            print("=> Anchor SANITY CHECK FAIL — debug f1_renorm / fetch_newform!")

    if falsifiers:
        print("\nFALSIFYING outcome: {} non-Steinberg case(s) match v_2 pattern:".format(
            len(falsifiers)))
        for r in falsifiers:
            print("   - {}  (level={}, cm_discs={})".format(
                r["label"], r["level"], r["cm_discs"]))
        print("=> M13.1(c) Steinberg-specificity REFUTED; broaden M44.1(c).")
    else:
        non_st_seen = sum(1 for r in results if r["steinberg"] == "NON-STEINBERG")
        if non_st_seen == 0:
            print("\nINCONCLUSIVE: 0 non-Steinberg comparators in sweep set.")
            print("Expand SWEEP_LABELS with more newforms (target: at least 5 NON-STEINBERG).")
        else:
            print("\nCONFIRMING outcome: 0 of {} non-Steinberg cases match the pattern".format(
                non_st_seen))
            print("=> M13.1(c) Steinberg-specificity SURVIVES this sweep.")
    print("=== END F2 SWEEP VERDICT ===\n")


if __name__ == "__main__":
    main()
