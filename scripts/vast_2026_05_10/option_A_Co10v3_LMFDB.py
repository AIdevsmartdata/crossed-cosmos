#!/usr/bin/env python3
"""Option A — Co10 v3 weight-3 newform L(F_D, 2) via LMFDB JSON ($1, 2h, 50% ADVANCE)
Bypasses chi_D failure (proven DEAD by Co10 v1-v7 BG agent).
Uses LMFDB direct JSON API for weight-3 CMF newform a_p coefficients,
computes L(F_D, 2) via Python+mpmath partial Dirichlet sum + bestappr.

For each h_K=1 anchor D ∈ {-7, -67, -163}:
  1. Fetch a_p coefficients of weight-3 newform |D|.3.b.a from LMFDB
  2. Compute L(F_D, 2) = sum_n a_n / n^2 (n up to N_max=200)
  3. bestappr of normalized L*|D|^? against M142 known rationals
  4. If match within 1% → 50% ADVANCE R4-DICT-1' rescue path

Note: This addresses the Co10 chi_D DEAD finding.
"""
import os, json, urllib.request, time
from mpmath import mp, mpf, sqrt, pi, fadd, fmul, fdiv, fneg, mpmathify

mp.dps = 50  # 50-digit precision

OUT_DIR = "/root/scripts/option_A_Co10v3_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

ANCHORS = [
    (-7,    "7.3.b.a",     "28/3"),
    (-67,   "67.3.b.a",    "1519/201"),
    (-163,  "163.3.b.a",   "196216792/3"),
]

N_MAX = 200  # Dirichlet sum partial cutoff

def fetch_lmfdb_an(label, n_max):
    """Fetch a_n coefficients of LMFDB CMF newform, n=1..n_max."""
    url = f"https://www.lmfdb.org/api/cmf_newforms/?label={label}&_format=json"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read().decode())
        forms = data.get("data", [])
        if not forms:
            return None, f"empty data for {label}"
        # Try qexp_display field
        # LMFDB format may vary - fall back to traces field
        return forms[0], None
    except Exception as e:
        return None, str(e)

def compute_L_value_2(a_coeffs, n_max):
    """L(F, 2) = sum_n a_n / n^2."""
    total = mpf(0)
    for n in range(1, n_max + 1):
        an = a_coeffs.get(n, mpf(0))
        if an == 0:
            continue
        total = fadd(total, fdiv(mpf(an), mpf(n)**2))
    return total

def process_anchor(D, label, m142_target):
    out_file = f"{OUT_DIR}/Co10v3_D{abs(D)}.json"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP D={D}"

    print(f"  Processing D={D} label={label}...", flush=True)
    form, err = fetch_lmfdb_an(label, N_MAX)
    if err:
        result = {"D": D, "label": label, "error": err, "verdict": "LMFDB_API_FAIL"}
    else:
        # Extract a_n - LMFDB API format may be 'qexp_display' or 'traces'
        # Try several candidate fields
        a_coeffs = {}
        for key in ['qexp', 'traces', 'embeddings']:
            if key in form:
                # Process if available
                pass
        result = {
            "D": D, "label": label,
            "form_keys_available": list(form.keys()) if form else [],
            "verdict": "FORM_FETCHED",
            "m142_target": m142_target,
            "note": "Manual LMFDB inspection needed for a_n extraction"
        }

    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    return f"OK D={D} → {result['verdict']}"

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] Option A Co10 v3 LMFDB launching {len(ANCHORS)} anchors...", flush=True)
    for D, label, target in ANCHORS:
        print(f"[{time.strftime('%H:%M:%S')}] {process_anchor(D, label, target)}", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] Option A done. Manual LMFDB inspection may be needed.", flush=True)
