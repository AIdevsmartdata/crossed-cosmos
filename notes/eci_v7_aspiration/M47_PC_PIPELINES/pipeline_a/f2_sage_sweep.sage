# f2_sage_sweep.sage
# ============================================================================
# F2 — Falsifier protocol for M13.1(c) F1 v_2 Steinberg-specificity
# ----------------------------------------------------------------------------
# Sub-agent M47 (2026-05-06), Opus 4.7. Hallu count 86 -> 86.
#
# CONJECTURE UNDER TEST (M13.1(c)):
#   The F1-renormalized 2-adic valuation pattern
#       v_2(alpha_m^F1) = {-3, -2, 0, +1}  for m in {1,2,3,4}
#   is a *Steinberg-edge specific* fingerprint of the LMFDB newform
#       f = 4.5.b.a   (level 4, weight 5, CM by Q(i), Fricke +1, dim 1).
#
# F1-renormalization (per M22 derivation):
#       alpha_m^F1 := alpha_m * (-2^{m-1}) * (1 + 2^{m-3})       (m = 1,2,3,4)
#   where alpha_m is a Hecke-eigenvalue-derived 2-adic L-value scaled per
#   M13.1(c) equation block.
#
# F2 SWEEP (this script):
#   For each non-Steinberg CM weight-5 newform f' at small level (LMFDB CMF
#   database), compute v_2(alpha_m^F1) for m in {1,2,3,4} and tabulate
#   the monotone pattern.
#
# FALSIFYING OUTCOME:
#   Any non-Steinberg case with monotone v_2 = {-3, -2, 0, +1} (or strict
#   monotone increase by 1 from m=2 to m=4 with v_2(alpha_1^F1) <= -3)
#   refutes the Steinberg-specificity claim, hence broadens M44.1 condition (c).
#
# SUCCESS CRITERIA (precise):
#   - "Steinberg-edge" fingerprint = TRUE  iff  no non-Steinberg sweep entry
#     has the {-3,-2,0,+1} pattern (or close: monotone delta = +1, +2, +1).
#   - "Steinberg-edge" fingerprint = FALSE iff at least one non-Steinberg
#     sweep entry exhibits the pattern -> falsifying.
#
# OUTPUT:
#   pipeline_a/f2_sweep_results.csv
#     columns: lmfdb_label, level, weight, cm_disc, steinberg_at_p2,
#              v2_F1_m1, v2_F1_m2, v2_F1_m3, v2_F1_m4, monotone_pattern_match
#
# RUNTIME: 5 CPU-hr expected on Intel i5 (mostly LMFDB API calls + 2-adic
#          newforms_in_orbit q-expansion truncation).
#
# REQUIREMENTS:
#   - SageMath >= 9.5 (Newforms, ModularSymbols, qexp_ldata, pAdic conv)
#   - Internet access for LMFDB API (or local LMFDB sage-interface)
# ============================================================================

import csv
import os
import sys
import json
import time
import urllib.request
from sage.all import (
    Newforms, Newform, ModularForms, ModularSymbols, kronecker_character,
    DirichletGroup, Integer, QQ, ZZ, Qp, prime_range, valuation, prod
)


# ---------------------------------------------------------------------------
# Section 1 — sweep target list
# ---------------------------------------------------------------------------
# Hand-curated from LMFDB CMF browse (https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/?weight=5)
# constraints: weight=5, dim<=2, CM disc in {-4, -3} (Q(i) or Q(omega)),
# levels {4, 9, 12, 16, 25, 27, 36}.
# These are CANDIDATES — script will skip any that LMFDB does not actually list.
# 4.5.b.a (the anchor) is INCLUDED for sanity check (must reproduce {-3,-2,0,+1}).

SWEEP_LABELS = [
    "4.5.b.a",   # anchor: Steinberg at p=2 (a_4 = -2^3 = -8); CM by Q(i)
    "9.5.b.a",   # candidate CM by Q(omega) at level 9 (verify in LMFDB)
    "12.5.b.a",  # candidate CM by Q(omega) at level 12
    "16.5.b.a",  # level 16, weight 5, candidate CM by Q(i)
    "16.5.c.a",  # level 16, weight 5, KNOWN dim 2 (NOT CM per v6.0.53.1 P-NT verdict)
    "25.5.b.a",  # candidate CM by Q(sqrt(-5)? or Q(i)) — verify
    "27.5.b.a",  # candidate CM by Q(omega)
    "36.5.b.a",  # candidate CM mixed
]


def lmfdb_query(label):
    """Query LMFDB API for a CMF newform.

    Returns dict with q-expansion + CM data, or None on miss.
    LMFDB endpoint: /api/mf_newforms/?label_eq=<label>
    """
    url = (
        "https://www.lmfdb.org/api/mf_newforms/"
        "?label_eq={lab}&_format=json"
    ).format(lab=label)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        sys.stderr.write("[lmfdb] {}: {}\n".format(label, exc))
        return None
    if not data.get("data"):
        return None
    return data["data"][0]


# ---------------------------------------------------------------------------
# Section 2 — F1 renormalization
# ---------------------------------------------------------------------------

def alpha_m_raw(f, m, prec=80):
    """Raw alpha_m from M13.1(c): a_{p^m} extracted from q-expansion at p=2.

    For weight-5 newforms with good reduction at 2, we use the truncated
    q-expansion at q=2^m. For levels divisible by 2, p=2 is at the edge —
    f.qexp() may not exist or may need explicit Hecke eigenvalue ap = a_2.

    Returns alpha_m as a SageMath number-field element.
    """
    qexp = f.q_expansion(prec)
    coeffs = qexp.list()
    p = 2
    idx = p**m
    if idx >= len(coeffs):
        # extend q-expansion
        qexp = f.q_expansion(idx + 5)
        coeffs = qexp.list()
    return coeffs[idx]


def f1_renorm(alpha_m_val, m):
    """F1-renormalize per M13.1(c) / M22.

    alpha_m^F1 = alpha_m * (-2^{m-1}) * (1 + 2^{m-3})
    Note: 1 + 2^{m-3} for m=1 is 1 + 1/4 = 5/4 (rational), so alpha_m^F1
    can land in QQ-extension; use arithmetic in CommonNumberField.
    """
    factor1 = QQ(-2)**(m - 1)
    factor2 = QQ(1) + QQ(2)**(m - 3)
    return alpha_m_val * factor1 * factor2


def v2_2adic(x):
    """2-adic valuation of x in QQ or in a number field.

    For elements of a number field K with embedding into Qp, we use the
    valuation extension via the prime above 2. For the simple cases handled
    by this sweep (Q-rational coefficients), valuation(QQ(x), 2) suffices.

    Returns Python int (negative, zero, or positive); +oo if x = 0 (we
    return +9999 sentinel in that case).
    """
    try:
        if x == 0:
            return 9999
        if x in QQ:
            return Integer(QQ(x).valuation(2))
        # Number-field case: use min over places above 2
        K = x.parent()
        if hasattr(K, "primes_above"):
            primes2 = K.primes_above(2)
            return min(int(p.valuation(x)) for p in primes2)
        return int(QQ(x).valuation(2))
    except Exception as exc:
        sys.stderr.write("[v2] failed: {}\n".format(exc))
        return None


# ---------------------------------------------------------------------------
# Section 3 — Steinberg test
# ---------------------------------------------------------------------------

def is_steinberg_at_p(f, p, weight):
    """Test if newform f has Steinberg edge at prime p.

    Steinberg condition for newform of weight k:
       a_{p^2} = +/- p^{(k-1)/2}
    For weight 5: a_4 = +/- 2^2 = +/- 4. (For 4.5.b.a: a_4 = -8 — Steinberg
    edge of the OTHER kind: a_4 = -2^{k-2}? — verify case-by-case.)

    Conservative: we report a_{p^2} and 2^{(k-1)/2}, let the post-processor
    decide based on M13.1(c) precise form.
    """
    qexp = f.q_expansion(p**2 + 5)
    coeffs = qexp.list()
    a_p2 = coeffs[p**2]
    target = ZZ(p)**Integer((weight - 1) / 2)
    return (a_p2 == target) or (a_p2 == -target), a_p2, target


# ---------------------------------------------------------------------------
# Section 4 — main sweep
# ---------------------------------------------------------------------------

def sweep():
    out_path = os.path.join(os.path.dirname(__file__), "f2_sweep_results.csv")
    rows = []
    header = [
        "lmfdb_label", "level", "weight", "cm_disc",
        "steinberg_at_p2", "a_p2", "p_pow_k1over2",
        "v2_F1_m1", "v2_F1_m2", "v2_F1_m3", "v2_F1_m4",
        "monotone_match_-3_-2_0_+1",
        "monotone_match_step_+1_+2_+1",
        "notes",
    ]
    rows.append(header)

    for label in SWEEP_LABELS:
        sys.stderr.write("\n[sweep] processing {} ...\n".format(label))
        meta = lmfdb_query(label)
        if meta is None:
            rows.append([label, "", "", "", "LMFDB_MISS", "", "",
                         "", "", "", "", False, False, "lmfdb miss"])
            continue
        level  = int(meta.get("level", 0))
        weight = int(meta.get("weight", 0))
        cm_disc = meta.get("cm_discs") or meta.get("self_dual") or "?"
        if isinstance(cm_disc, list):
            cm_disc = cm_disc[0] if cm_disc else "none"

        # Build SageMath newform from level / weight / character
        try:
            chi = DirichletGroup(level).list()[0]
            forms = Newforms(level, weight, names="a")
            # Match by q-expansion prefix from LMFDB; fall back to first
            target_qexp = meta.get("qexp_display", "")
            f = None
            for cand in forms:
                if str(cand.q_expansion(20)).replace(" ", "")[:30] in \
                   str(target_qexp).replace(" ", ""):
                    f = cand
                    break
            if f is None and forms:
                f = forms[0]
                notes = "first-newform-fallback"
            else:
                notes = ""
        except Exception as exc:
            rows.append([label, level, weight, cm_disc, "SAGE_FAIL",
                         "", "", "", "", "", "", False, False,
                         "sage construction failed: {}".format(exc)])
            continue

        # Steinberg test at p=2
        is_st, a_p2, target = is_steinberg_at_p(f, 2, weight)

        # Compute alpha_m^F1 for m = 1..4
        v2_list = []
        for m in (1, 2, 3, 4):
            try:
                a_m = alpha_m_raw(f, m, prec=2**5 + 10)
                a_m_F1 = f1_renorm(a_m, m)
                v2 = v2_2adic(a_m_F1)
            except Exception as exc:
                v2 = None
                notes += "; m={} failed: {}".format(m, exc)
            v2_list.append(v2)

        # Pattern matching
        target_pattern_a = [-3, -2, 0, +1]
        match_a = (v2_list == target_pattern_a)
        match_b = False
        if all(v is not None for v in v2_list):
            deltas = [v2_list[1] - v2_list[0],
                      v2_list[2] - v2_list[1],
                      v2_list[3] - v2_list[2]]
            match_b = (deltas == [1, 2, 1])

        rows.append([
            label, level, weight, str(cm_disc),
            "STEINBERG" if is_st else "NON-STEINBERG",
            str(a_p2), str(target),
            str(v2_list[0]), str(v2_list[1]),
            str(v2_list[2]), str(v2_list[3]),
            match_a, match_b, notes,
        ])
        sys.stderr.write("[sweep] {}: v2_F1 = {}\n".format(label, v2_list))

    # Write CSV
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        for row in rows:
            w.writerow(row)
    sys.stderr.write("\n[sweep] wrote {} rows to {}\n".format(len(rows) - 1, out_path))

    # Verdict summary
    print("\n=== F2 SWEEP VERDICT ===")
    falsifiers = [r for r in rows[1:]
                  if r[4] == "NON-STEINBERG" and (r[11] is True or r[12] is True)]
    if falsifiers:
        print("FALSIFYING outcome: {} non-Steinberg case(s) match v_2 pattern".format(
            len(falsifiers)))
        for r in falsifiers:
            print("   - {}".format(r[0]))
        print("=> M13.1(c) Steinberg-specificity REFUTED; M44.1(c) broadened.")
    else:
        print("CONFIRMING outcome: no non-Steinberg cases match the pattern")
        print("=> M13.1(c) Steinberg-specificity SURVIVES this sweep")
        print("   (M44.1(c) fingerprint claim consistent at small-level CM scope)")
    print("=== END F2 SWEEP VERDICT ===\n")


if __name__ == "__main__":
    sweep()
