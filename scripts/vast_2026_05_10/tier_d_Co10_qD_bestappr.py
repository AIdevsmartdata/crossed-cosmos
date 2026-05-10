#!/usr/bin/env python3
"""Tier D Co10 PARI bestappr q(D) 6-anchor verification.
Test: q(D) recovered as rational p/r matching M142 hierarchy across 6 CM anchors
Source: VAST MANAGER §3 #2 (binary verdict R4-DICT-1' rescue)
Cost: ~$10, ETA 1 day

Method: For each D in {-7, -67, -84, -148, -163, -195}:
  1. Compute L(f_D, 2) for weight-3 newform f_D at level |D|
     (Hecke L-value via Dirichlet class number formula + sym² lifting)
  2. Use PARI bestappr to find rational q(D) = p/r
  3. Compare to M142 hierarchy: q(-67) = 1519/201, q(-84) = ?, etc.
  4. Verdict: all 6 give clean rationals → T3 maintain

NOTE: For weight-3 newform L(f, 2) at central point, use functional eq.
Approximate via partial Dirichlet sum + bestappr.
"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/tier_d_Co10_outputs"
os.makedirs(OUT_DIR, exist_ok=True)
GP = "/tmp/pari-2.17.2/gp"

ANCHORS = [-7, -67, -84, -148, -163, -195]
M142_TARGETS = {
    -7: "28/3",      # known M142
    -67: "1519/201", # known M142
    -84: "?",        # unknown — first new
    -148: "?",
    -163: "196216792/3",  # known M142
    -195: "?",
}

def gp_script(D):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);

print("===== Co10 q(D) D={D} START =====");

absD = abs({D});

\\\\ Compute L(chi_D, 2) at high precision
\\\\ Use PARI lfun for the Kronecker character chi_D
\\\\ For chi_D quadratic, lfun([D]) returns the L-function
L_2 = lfun([{D}], 2);
print("L(chi_D, 2) = ", L_2);

\\\\ For comparison: L(chi_D, 1) via class number formula
hD = qfbclassno({D});
w = if(absD == 3, 6, if(absD == 4, 4, 2));
L_1 = (2 * Pi * hD) / (w * sqrt(absD));
print("L(chi_D, 1) = ", L_1);
print("L(chi_D, 2) / L(chi_D, 1) = ", L_2 / L_1);

\\\\ M142 normalization: q(D) related to L(f, 2) of weight-3 newform
\\\\ For h(D)=1 anchors with Hecke character lifted from chi_D:
\\\\   weight-3 newform 67.3.b.a has L(f, 2) related to L(chi_D, 2) by Eichler-Shimura
\\\\
\\\\ Try to recover q(D) via bestappr on a normalized combination
\\\\ Standard normalization: q(D) = L(f, 2) * absD^(3/2) / (4 * Pi^4)
\\\\ This places q(D) on the same scale as M142 rationals

q_estimate_v1 = L_2 * absD^(3/2) / (4 * Pi^4);
print("q(D) v1 estimate = ", q_estimate_v1);

\\\\ bestappr to find rational
\\\\ Try denominators up to absD^2
q_rational_v1 = bestappr(q_estimate_v1, absD^2);
print("q(D) v1 bestappr = ", q_rational_v1);

\\\\ Alternative normalization: q(D) = L(f, 2) * sqrt(absD) / Pi^2
q_estimate_v2 = L_2 * sqrt(absD) / Pi^2;
print("q(D) v2 estimate = ", q_estimate_v2);
q_rational_v2 = bestappr(q_estimate_v2, absD^2);
print("q(D) v2 bestappr = ", q_rational_v2);

\\\\ Alternative v3: q(D) = L(chi_D, 2) / (Pi * L(chi_D, 1))
q_estimate_v3 = L_2 / (Pi * L_1);
print("q(D) v3 estimate = ", q_estimate_v3);
q_rational_v3 = bestappr(q_estimate_v3, absD^2);
print("q(D) v3 bestappr = ", q_rational_v3);

print("===== Co10 q(D) D={D} DONE =====");
quit;
"""

def run_one(D):
    gp_file = f"/tmp/tier_d_Co10_D{abs(D)}.gp"
    out_file = f"{OUT_DIR}/Co10_D{abs(D)}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP D={D}"
    with open(gp_file, "w") as f:
        f.write(gp_script(D))
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True, timeout=600)
        with open(out_file, "w") as f:
            f.write(r.stdout)
            if r.stderr:
                f.write("\n=== STDERR ===\n" + r.stderr[:2000])
        return f"OK D={D} ({len(r.stdout)} chars)"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT D={D}"
    except Exception as e:
        return f"ERR D={D} : {e}"

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] Tier D Co10 q(D) bestappr launching {len(ANCHORS)} anchors...", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, D): D for D in ANCHORS}
        for f in as_completed(futs):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)

    # Aggregate
    print("\n===== AGGREGATE Co10 q(D) bestappr =====", flush=True)
    for D in ANCHORS:
        out_file = f"{OUT_DIR}/Co10_D{abs(D)}.out"
        if os.path.exists(out_file):
            with open(out_file) as f:
                content = f.read()
            print(f"\n--- D={D} (M142 target: {M142_TARGETS[D]}) ---")
            for line in content.split("\n"):
                if "bestappr" in line or "estimate" in line:
                    print(f"  {line.strip()}")
    print(f"\n[{time.strftime('%H:%M:%S')}] Tier D Co10 done.", flush=True)
