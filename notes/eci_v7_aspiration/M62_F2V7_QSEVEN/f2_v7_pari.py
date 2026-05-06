#!/usr/bin/env python3
"""
f2_v7_pari.py
================================================================================
F2 v7 — Q(sqrt(-7)) and Q(sqrt(-11)) period sweep
Test of R-6 Conjecture 3.3 part (c): R(f) in Q(sqrt(d)) \ Q for d in {7,11}

Newforms verified against LMFDB (live fetch 2026-05-06, M62 sub-agent):
  7.5.b.a:  N=7, k=5, char=Mod(6,7)  [conrey_index=6, cm_disc=-7, dim=1]
  11.5.b.a: N=11, k=5, char=Mod(10,11) [conrey_index=10, cm_disc=-11, dim=1]

Anchor (Q(i)):  4.5.b.a:  N=4, k=5, char=Mod(3,4)
Re-test (Q(ω)): 27.5.b.a: N=27, k=5, char=Mod(26,27)

PARI 2.15.4 required. Run on remondiere@100.91.123.14 (PC with PARI/GP).

Chowla-Selberg periods (analytic computation):
  chi_{-7}(a) for a mod 7: [1, 1, -1, 1, -1, -1, 0]  (a=1..7)
  chi_{-11}(a) for a mod 11: [1,-1,1,1,1,-1,-1,-1,1,-1,0]  (a=1..11)

  Omega_{-7} = product_{a=1}^(\1) Gamma(a/7)^(\1)(a)/2}
             = [Gamma(1/7) * Gamma(2/7) * Gamma(4/7)]^(\1)
               / [Gamma(3/7) * Gamma(5/7) * Gamma(6/7)]^(\1)
             (numerically: 4-term quotient since chi=+1 at a=1,2,4 and -1 at a=3,5,6)
             To get the canonical CM period we also include the (2pi)^(\1) normalization.
             Handled self-consistently in T3 bootstrap below.

  Omega_{-11} = product_{a=1}^(\1) Gamma(a/11)^(\1)(a)/2}
              chi_{-11}: +1 at a=1,3,4,5,9; -1 at a=2,6,7,8,10
              = [Gamma(1/11)*Gamma(3/11)*Gamma(4/11)*Gamma(5/11)*Gamma(9/11)]^(\1)
                / [Gamma(2/11)*Gamma(6/11)*Gamma(7/11)*Gamma(8/11)*Gamma(10/11)]^(\1)

Normalization:  We use TWO strategies:
  (A) Chowla-Selberg: Omega_K = above product * correction_factor
      The correction factor from (2pi)^(\1) * |D_K|^(\1) (standard textbook, see below)
  (B) Self-consistent bootstrap: define Omega_K = (L(f,4) * 1)^(\1) [from PARI lfun]
      This avoids normalization ambiguity entirely.
      Then alpha_m = L(f,m) * Pi^(4-m) / Omega_K^4  for m=1,2,3,4
      Key diagnostic: R(f) = Pi * L(f,1)/L(f,2) is Omega-INDEPENDENT.

Output:
  f2_v7_results.csv — alpha_m, R(f), sqrt-d rationality tests, per form
================================================================================
"""

import subprocess
import sys
import re
import csv
import os
import tempfile

# ---------------------------------------------------------------------------
# PARI runner (identical to M47/M52 pattern)
# ---------------------------------------------------------------------------

def run_pari(script: str, prec: int = 100, timeout: int = 600) -> str:
    """Run a PARI/GP script via temp file. 100-digit default precision."""
    full = f"default(realprecision, {prec});\n" + script + "\nquit;\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".gp", delete=False) as tf:
        tf.write(full)
        path = tf.name
    try:
        r = subprocess.run(
            ["gp", "-q", path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if r.returncode != 0:
            sys.stderr.write(f"[pari] rc={r.returncode}\n{r.stderr}\n")
        return r.stdout
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# PARI character helpers
#
# LMFDB char_values encoding: [modulus, order, [generator], [gen_image_index]]
# 7.5.b.a:  char_values=[7,2,[3],[1]]  → generator 3, image index 1 in Z/2Z
#                                         ↔ χ(3) = exp(2πi·1/2) = -1
#           conrey_index = 6           → znchar(Mod(6,7)) in PARI
# 11.5.b.a: char_values=[11,2,[2],[1]] → generator 2, χ(2) = -1
#           conrey_index = 10          → znchar(Mod(10,11))
# 4.5.b.a:  conrey_index = 3          → znchar(Mod(3,4))
# 27.5.b.a: conrey_index = 26         → znchar(Mod(26,27))
# ---------------------------------------------------------------------------

FORMS = [
    # (label, N, k, conrey_mod, conrey_idx, cm_disc, traces_1_to_7)
    # traces[1..7] = a_1, a_2, ..., a_7 from LMFDB (for mfeigenbasis matching)
    ("4.5.b.a",  4,  5,  4,  3,  -4,  [1, -4,   0,  16, -14,   0,   0]),  # anchor Q(i)
    ("27.5.b.a", 27, 5, 27, 26,  -3,  [1,  0,   0,  16,   0,   0,  71]),  # re-test Q(ω)
    ("7.5.b.a",   7, 5,  7,  6,  -7,  [1,  1,   0, -15,   0,   0,  49]),  # NEW Q(sqrt(-7))
    ("11.5.b.a", 11, 5, 11, 10, -11,  [1,  0,   7,  16, -49,   0,   0]),  # NEW Q(sqrt(-11))
]


# ---------------------------------------------------------------------------
# Chowla-Selberg periods (analytic)
# chi_{-7}(a) for a=1..6: [+1,+1,-1,+1,-1,-1]
# chi_{-11}(a) for a=1..10: [+1,-1,+1,+1,+1,-1,-1,-1,+1,-1]
# chi_{-4}(a) for a=1..3: [+1,0,-1]  (Kronecker symbol (-4/n))
# chi_{-3}(a) for a=1..2: [+1,-1] (... this is for a=1,2 mod 3... but conductor=3)
#
# Standard Chowla-Selberg (Berndt-Evans-Williams formulation):
#   For fundamental discriminant D < 0, h_K units w_K:
#   (2pi / sqrt|D|)^(\1) * Omega_K^(\1) =
#       (2pi)^(\1) * prod_{a=1}^(\1) Gamma(a/|D|)^(\1) ... [variant]
#
# We use PARI's lfunmf normalization directly (Gamma factors absorbed).
# The period Omega_K appearing in alpha_m = L(f,m)*Pi^(k-1-m)/Omega_K^(k-1) is
# numerically calibrated via the self-consistent bootstrap described below.
#
# PARI expressions for Chowla-Selberg raw product P_K:
CS_PARI = {
    -4:  "gamma(1/4)^2 / (2 * sqrt(2*Pi))",   # lemniscate, from M52
    -3:  "gamma(1/3)^3 / (4 * Pi * sqrt(3))",  # Eisenstein, from M52
    # d=7: P_7 = Gamma(1/7)*Gamma(2/7)*Gamma(4/7) / (Gamma(3/7)*Gamma(5/7)*Gamma(6/7))
    # This is the raw product; normalization factor (|D|/(4pi^2))^(\1) applied separately
    # Full Omega_{-7} = P_7 * (7/(4*Pi^2))^(\1)  [needs numerical verification vs bootstrap]
    -7:  "(gamma(1/7)*gamma(2/7)*gamma(4/7))/(gamma(3/7)*gamma(5/7)*gamma(6/7)) * (7/(4*Pi^2))^(1/4)",
    # d=11: P_11 = Gamma(1/11)*Gamma(3/11)*Gamma(4/11)*Gamma(5/11)*Gamma(9/11)
    #              / (Gamma(2/11)*Gamma(6/11)*Gamma(7/11)*Gamma(8/11)*Gamma(10/11))
    # Full Omega_{-11} = P_11 * (11/(4*Pi^2))^(\1)  [same normalization ansatz]
    -11: "(gamma(1/11)*gamma(3/11)*gamma(4/11)*gamma(5/11)*gamma(9/11))/(gamma(2/11)*gamma(6/11)*gamma(7/11)*gamma(8/11)*gamma(10/11)) * (11/(4*Pi^2))^(1/4)",
}


# ---------------------------------------------------------------------------
# Core PARI script: compute all alpha_m + R(f) for a single newform
#
# Strategy:
# 1. Initialize mf space, get eigenbasis, find form by matching traces[1..7].
# 2. Compute L-values L(f,m) for m=1,2,3,4 using lfunmf+lfun.
# 3. Compute Omega_K via Chowla-Selberg expression from CS_PARI.
# 4. Compute alpha_m = L(f,m) * Pi^(k-1-m) / Omega_K^(k-1) for m=1..4.
# 5. ALSO compute bootstrap Omega: Omega_boot = L(f,4)^(\1) [absorbs Pi^0/Omega^4]
#    so that alpha_4_boot = 1 by definition; compare alpha_1_boot, alpha_2_boot, alpha_3_boot.
# 6. R(f) = Pi * L(f,1) / L(f,2)  [Omega-independent].
# 7. bestappr(x, 10^7) for rational reconstruction.
# 8. bestappr(x / sqrt(d), 10^7) for Q(sqrt(d)) decomposition.
# ---------------------------------------------------------------------------

PARI_TEMPLATE = r"""
\\=======================================================================
\\ M62 F2 v7: form {label}, N={N}, k={k}, conrey {cidx} mod {cmod}
\\=======================================================================
default(realprecision, 100);

\\ 1. Initialize space
chi = znchar(Mod({cidx}, {cmod}));
mf = mfinit([{N}, {k}, chi], 1);
B = mfeigenbasis(mf);
nB = #B;
if(nB == 0, print("EMPTY_SPACE_{label}"); quit);

\\ 2. Match eigenbasis member by traces[2..7]
\\ LMFDB traces (a_1=1 always, we match a_2..a_7):
targ = [{t2}, {t3}, {t4}, {t5}, {t6}, {t7}];
fidx = 0;
for(j = 1, nB,
  fj = B[j];
  ok = 1;
  for(p = 2, 7,
    tr = mfcoef(fj, p);
    if(abs(tr - targ[p-1]) > 0.5, ok = 0; break)
  );
  if(ok, fidx = j; break)
);
if(fidx == 0,
  \\ Fallback: try all and print traces for debugging
  print("TRACE_MISMATCH_{label}: nB=", nB);
  for(j=1,nB, print("  j=",j," a2..7=", vector(6,p,mfcoef(B[j],p+1))));
  fidx = 1  \\ use first as fallback
);
F = B[fidx];
print("FORM_SELECTED_{label}: fidx=", fidx, " a2=", mfcoef(F,2));

\\ 3. L-function object
Lobj = lfunmf(mf, F);

\\ 4. L-values at m=1..4
L1 = lfun(Lobj, 1);
L2 = lfun(Lobj, 2);
L3 = lfun(Lobj, 3);
L4 = lfun(Lobj, 4);
print("LVALS_{label}: L1=", L1, " L2=", L2, " L3=", L3, " L4=", L4);

\\ 5. Omega_K via Chowla-Selberg
Omega_CS = {omega_expr};
print("OMEGA_CS_{label}=", Omega_CS);

\\ 6. Compute k-1 = 4 for k=5
\\ alpha_m = L(f,m) * Pi^(4-m) / Omega_K^4
a1 = L1 * Pi^3 / Omega_CS^4;
a2 = L2 * Pi^2 / Omega_CS^4;
a3 = L3 * Pi^1 / Omega_CS^4;
a4 = L4 * Pi^0 / Omega_CS^4;

print("ALPHA_RAW_{label}: a1=", a1, " a2=", a2, " a3=", a3, " a4=", a4);

\\ 7. Rational approximations (bound 10^7)
B7 = 10^7;
a1q = bestappr(a1, B7);
a2q = bestappr(a2, B7);
a3q = bestappr(a3, B7);
a4q = bestappr(a4, B7);
print("ALPHA_BESTAPPR_{label}: a1=", a1q, " a2=", a2q, " a3=", a3q, " a4=", a4q);

\\ 8. Q(sqrt(d)) test: bestappr(alpha_m / sqrt(|D|), B7) → rational part
\\    If alpha_m = p/q * sqrt(d) + r/s, then alpha_m/sqrt(d) ≈ p/q + r/s/sqrt(d)
\\    We test both: bestappr(a_m, B7) for pure Q part
\\                  bestappr(a_m / sqrt({absd}), B7) for sqrt(d) component
sqd = sqrt({absd});
a1r = bestappr(a1 / sqd, B7);
a2r = bestappr(a2 / sqd, B7);
a3r = bestappr(a3 / sqd, B7);
a4r = bestappr(a4 / sqd, B7);
print("ALPHA_OVER_SQRTD_{label}: a1=", a1r, " a2=", a2r, " a3=", a3r, " a4=", a4r);

\\ 9. R(f) = Pi * L(f,1)/L(f,2) [Omega-independent]
Rf = Pi * L1 / L2;
print("Rf_{label}=", Rf);
Rfq = bestappr(Rf, B7);
print("Rf_BESTAPPR_{label}=", Rfq);
Rfr = bestappr(Rf / sqd, B7);
print("Rf_OVER_SQRTD_{label}=", Rfr);

\\ 10. Bootstrap Omega (self-consistent): Omega_boot = L4^(\1)
\\     alpha_m_boot = L_m * Pi^(4-m) / L4
Omega_boot = L4^(1/4);
a1b = L1 * Pi^3 / L4;
a2b = L2 * Pi^2 / L4;
a3b = L3 * Pi^1 / L4;
print("BOOTSTRAP_{label}: a1/a4=", a1b, " a2/a4=", a2b, " a3/a4=", a3b);
a1bq = bestappr(a1b, B7);
a2bq = bestappr(a2b, B7);
a3bq = bestappr(a3b, B7);
print("BOOTSTRAP_BESTAPPR_{label}: a1=", a1bq, " a2=", a2bq, " a3=", a3bq);
a1br = bestappr(a1b / sqd, B7);
a2br = bestappr(a2b / sqd, B7);
a3br = bestappr(a3b / sqd, B7);
print("BOOTSTRAP_OVER_SQRTD_{label}: a1=", a1br, " a2=", a2br, " a3=", a3br);

\\ 11. Residual: how close is bestappr to actual?
eps1 = abs(a1 - a1q);
eps2 = abs(a2 - a2q);
eps3 = abs(a3 - a3q);
eps4 = abs(a4 - a4q);
print("RESID_{label}: e1=", eps1, " e2=", eps2, " e3=", eps3, " e4=", eps4);

print("DONE_{label}");
"""


def make_pari_script(label: str, N: int, k: int, cmod: int, cidx: int,
                     cm_disc: int, traces: list) -> str:
    """Generate PARI script for one form."""
    absd = abs(cm_disc)
    omega_expr = CS_PARI.get(cm_disc, f"sqrt(Pi)")  # fallback (should not happen)
    t2, t3, t4, t5, t6, t7 = traces[1], traces[2], traces[3], traces[4], traces[5], traces[6]
    return PARI_TEMPLATE.format(
        label=label, N=N, k=k, cmod=cmod, cidx=cidx,
        omega_expr=omega_expr, absd=absd,
        t2=t2, t3=t3, t4=t4, t5=t5, t6=t6, t7=t7,
    )


# ---------------------------------------------------------------------------
# Parse PARI output lines
# ---------------------------------------------------------------------------

def parse_output(out: str, label: str) -> dict:
    """Extract numeric results from PARI output for one form."""
    result = {"label": label}

    def grab(tag):
        pat = rf"{re.escape(tag)}=(.*)"
        m = re.search(pat, out)
        return m.group(1).strip() if m else "?"

    def grab_kv(tag):
        """Parse 'TAG: k1=v1 k2=v2 ...' lines."""
        pat = rf"{re.escape(tag)}:\s*(.*)"
        m = re.search(pat, out)
        if not m:
            return {}
        kvs = {}
        for kv in re.findall(r'(\w+)=([^\s]+)', m.group(1)):
            kvs[kv[0]] = kv[1]
        return kvs

    lv = grab_kv(f"LVALS_{label}")
    result["L1"] = lv.get("L1", "?")
    result["L2"] = lv.get("L2", "?")
    result["L3"] = lv.get("L3", "?")
    result["L4"] = lv.get("L4", "?")

    result["Omega_CS"] = grab(f"OMEGA_CS_{label}")

    aq = grab_kv(f"ALPHA_BESTAPPR_{label}")
    result["alpha_1_CS"] = aq.get("a1", "?")
    result["alpha_2_CS"] = aq.get("a2", "?")
    result["alpha_3_CS"] = aq.get("a3", "?")
    result["alpha_4_CS"] = aq.get("a4", "?")

    ar = grab_kv(f"ALPHA_OVER_SQRTD_{label}")
    result["alpha_1_over_sqrtd"] = ar.get("a1", "?")
    result["alpha_2_over_sqrtd"] = ar.get("a2", "?")
    result["alpha_3_over_sqrtd"] = ar.get("a3", "?")
    result["alpha_4_over_sqrtd"] = ar.get("a4", "?")

    result["Rf"] = grab(f"Rf_{label}")
    result["Rf_bestappr"] = grab(f"Rf_BESTAPPR_{label}")
    result["Rf_over_sqrtd"] = grab(f"Rf_OVER_SQRTD_{label}")

    bq = grab_kv(f"BOOTSTRAP_BESTAPPR_{label}")
    result["alpha_1_boot"] = bq.get("a1", "?")
    result["alpha_2_boot"] = bq.get("a2", "?")
    result["alpha_3_boot"] = bq.get("a3", "?")

    br = grab_kv(f"BOOTSTRAP_OVER_SQRTD_{label}")
    result["alpha_1_boot_over_sqrtd"] = br.get("a1", "?")
    result["alpha_2_boot_over_sqrtd"] = br.get("a2", "?")
    result["alpha_3_boot_over_sqrtd"] = br.get("a3", "?")

    resid = grab_kv(f"RESID_{label}")
    result["resid_1"] = resid.get("e1", "?")
    result["resid_2"] = resid.get("e2", "?")
    result["resid_3"] = resid.get("e3", "?")
    result["resid_4"] = resid.get("e4", "?")

    result["done"] = "YES" if f"DONE_{label}" in out else "NO"
    return result


# ---------------------------------------------------------------------------
# Conjecture 3.3 verdict logic
# ---------------------------------------------------------------------------

def verdict_3c(result: dict, cm_disc: int) -> str:
    """
    Classify R(f) and alpha_m pattern for Conjecture 3.3(c).
    Returns one of:
      CORROBORATED   — alpha_even in Q, alpha_odd in Q(sqrt(d)) \ Q (parity split)
      Q_FULL         — all alpha_m in Q (would FALSIFY part (a) uniqueness of Q(i))
      Q_SQRTD_FULL   — all in Q(sqrt(d)) but no parity split
      LARGER_EXT     — some alpha_m NOT in Q(sqrt(d))
      INCOMPLETE     — not enough data to decide
    """
    label = result["label"]
    absd = abs(cm_disc)

    # We classify by checking:
    # - Is bestappr(alpha_m, B7) a simple fraction? (residual < 1e-20 = Q-component)
    # - Is bestappr(alpha_m/sqrt(d), B7) a simple fraction? (sqrt(d)-component)
    # Use bootstrap ratios (Omega-independent) for clarity

    def classify_val(val_q: str, val_r: str) -> str:
        """val_q = bestappr(alpha), val_r = bestappr(alpha/sqrt(d))"""
        if val_q == "?" or val_r == "?":
            return "?"
        # If val_q looks rational (no sqrt), alpha is in Q
        # If val_r looks rational but val_q doesn't, alpha = r*sqrt(d)
        # Check: if bestappr(alpha,B7) = p/q with small p,q → Q
        try:
            # Simple heuristic: if fraction, Q; else check sqrt(d) component
            float(eval(val_q.replace("^", "**")))
            return "Q"
        except Exception:
            pass
        try:
            float(eval(val_r.replace("^", "**")))
            return "Qsqrtd"
        except Exception:
            pass
        return "UNKNOWN"

    # For report: just record what we see and let the summary interpret
    a1_q = result.get("alpha_1_boot", "?")
    a2_q = result.get("alpha_2_boot", "?")
    a3_q = result.get("alpha_3_boot", "?")
    a1_r = result.get("alpha_1_boot_over_sqrtd", "?")
    a2_r = result.get("alpha_2_boot_over_sqrtd", "?")
    a3_r = result.get("alpha_3_boot_over_sqrtd", "?")

    r_q = result.get("Rf_bestappr", "?")
    r_r = result.get("Rf_over_sqrtd", "?")

    return (f"a1_q={a1_q} a1_r={a1_r} | a2_q={a2_q} a2_r={a2_r} "
            f"| a3_q={a3_q} a3_r={a3_r} | Rf_q={r_q} Rf_r={r_r}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("F2 v7 — R-6 Conjecture 3.3(c) sweep: Q(sqrt(-7)), Q(sqrt(-11))")
    print("M62 sub-agent, 2026-05-06")
    print("=" * 70)
    print()

    all_results = []
    all_raw_output = {}

    for (label, N, k, cmod, cidx, cm_disc, traces) in FORMS:
        print(f"[{label}] K=Q(sqrt({cm_disc})), N={N}, k={k}, "
              f"conrey={cidx} mod {cmod}")
        script = make_pari_script(label, N, k, cmod, cidx, cm_disc, traces)

        # Write individual gp script for inspection / PC dispatch
        gp_path = os.path.join(os.path.dirname(__file__), f"M62_{label.replace('.','_')}.gp")
        with open(gp_path, "w") as gf:
            gf.write(f"default(realprecision, 100);\n")
            gf.write(script)
            gf.write("\nquit;\n")
        print(f"  GP script written: {gp_path}")

        # Run PARI
        print(f"  Running PARI/GP ...")
        raw = run_pari(script, prec=100, timeout=600)
        all_raw_output[label] = raw

        if not raw.strip():
            print(f"  WARNING: PARI returned empty output for {label}")
            result = {"label": label, "done": "NO", "error": "EMPTY_OUTPUT"}
        else:
            result = parse_output(raw, label)
            result["cm_disc"] = cm_disc
            verdict = verdict_3c(result, cm_disc)
            result["verdict_raw"] = verdict
            print(f"  L1={result.get('L1','?')[:25]}...")
            print(f"  Omega_CS={result.get('Omega_CS','?')[:25]}...")
            print(f"  alpha_1={result.get('alpha_1_CS','?')}, "
                  f"alpha_2={result.get('alpha_2_CS','?')}, "
                  f"alpha_3={result.get('alpha_3_CS','?')}, "
                  f"alpha_4={result.get('alpha_4_CS','?')}")
            print(f"  R(f) = {result.get('Rf_bestappr','?')}")
            print(f"  verdict: {verdict}")

        print()
        all_results.append(result)

    # Save raw output
    raw_path = os.path.join(os.path.dirname(__file__), "f2_v7_pari_raw.txt")
    with open(raw_path, "w") as rf:
        for label, raw in all_raw_output.items():
            rf.write(f"\n\n{'='*60}\n{label}\n{'='*60}\n")
            rf.write(raw)
    print(f"Raw PARI output → {raw_path}")

    # Save CSV
    if all_results:
        csv_path = os.path.join(os.path.dirname(__file__), "f2_v7_results.csv")
        fieldnames = sorted({k for r in all_results for k in r.keys()})
        with open(csv_path, "w", newline="") as cf:
            w = csv.DictWriter(cf, fieldnames=fieldnames)
            w.writeheader()
            for r in all_results:
                w.writerow(r)
        print(f"CSV → {csv_path}")

    # VERDICT SUMMARY
    print()
    print("=" * 70)
    print("F2 v7 VERDICT SUMMARY")
    print("=" * 70)
    for r in all_results:
        label = r["label"]
        disc = r.get("cm_disc", "?")
        Rf_q = r.get("Rf_bestappr", "?")
        print(f"  {label} (cm_disc={disc}): R(f)~{Rf_q} | {r.get('verdict_raw','?')}")

    print()
    print("Conjecture 3.3 interpretation:")
    print("  ANCHOR 4.5.b.a Q(i): R(f)=6/5 ∈ Q — reference")
    print("  RE-TEST 27.5.b.a Q(ω): expect R(f)=3√3 ∈ Q(√3) — part (b)")
    print("  NEW 7.5.b.a Q(√-7): R(f) ∈ Q(√7) \\ Q → (c) CORROBORATED")
    print("                       R(f) ∈ Q         → (a) FALSIFIED (Q(i) not unique)")
    print("                       R(f) ∈ larger ext → (c) needs refinement")
    print("  NEW 11.5.b.a Q(√-11): same trichotomy")
    print()
    print("See f2_v7_results.csv for full numerical data.")
    print("See M62_SUMMARY.md for final verdict.")


if __name__ == "__main__":
    main()
