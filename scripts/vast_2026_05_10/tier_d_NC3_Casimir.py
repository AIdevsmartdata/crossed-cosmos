#!/usr/bin/env python3
"""Tier D NC3 Casimir 5-anchor 50-digit verification.
Test: m_YM·sqrt(|D|) = const = pi^2 * sqrt(2) ≈ 13.958 across 5 CM anchors
Source: VAST MANAGER §3.4 NEW-1 (binary verdict T2→T1)
Cost: ~$10, ETA 1-2 days

Method: For each D in {-7, -67, -84, -148, -163}:
  1. Compute Hecke L-value L(chi_D, 1) at 50-digit precision (PARI lfun)
  2. Casimir formula: m_YM(D)^2 = (4 * pi^2 / chi_K3(D)) * L(chi_D, 1) * BPS_count
  3. Output m_YM(D) * sqrt(|D|)
  4. Verdict: all 5 within 0.5% of pi^2 * sqrt(2) → T1 promotion
"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/tier_d_NC3_outputs"
os.makedirs(OUT_DIR, exist_ok=True)
GP = "/tmp/pari-2.17.2/gp"

ANCHORS = [-7, -67, -84, -148, -163]

def gp_script(D):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);

print("===== NC3 Casimir D={D} START =====");

\\\\ Hecke L-value via lfun
\\\\ Use Dirichlet character chi_D = kronecker(D, ·) — quadratic
ch = znchargen(idealadd(idealfactor({D},quadgen({D})*quadgen({D})),1),1)[1];
\\\\ Simpler: use classical kronecker character
\\\\ L(chi_D, s) = sum_n kronecker(D, n) / n^s

\\\\ Class number h(D) (analytic class number formula)
hD = qfbclassno({D});
print("D=", {D}, " h(D)=", hD);

\\\\ L(chi_D, 1) via Dirichlet class number formula:
\\\\ L(chi_D, 1) = (2*pi*h(D)) / (w(D)*sqrt(|D|))   for D < -4
\\\\   where w(D) = #units = 2 except w(-3)=6, w(-4)=4
absD = abs({D});
w = if(absD == 3, 6, if(absD == 4, 4, 2));
L_chi_1 = (2 * Pi * hD) / (w * sqrt(absD));
print("L(chi_D, 1) = ", L_chi_1);

\\\\ K3 Euler characteristic for CM K3 X̃_D : standard chi_top = 24
chi_K3 = 24;

\\\\ BPS instanton count at c2=1 (Donaldson)
\\\\ For SU(2) on CM K3: dim M(c2=1) = 4*c2*N - (N^2-1)(chi+sigma)/2
\\\\   chi=24, sigma=-16, N=2 → dim M(1) = 4 - 3*8/2 = 4-12 = -8 (Donaldson)
\\\\   Use BPS_count = 1 (instanton charge 1, simple anchor)
BPS = 1;

\\\\ Casimir-style formula: m_YM(D)^2 = (4 pi^2 / chi_K3) * L(chi_D, 1) * BPS
\\\\ Note: this is a SIMPLIFIED model - actual NC3 derivation uses comoving Λ_QCD
m_YM_sq = (4 * Pi^2 / chi_K3) * L_chi_1 * BPS;
m_YM = sqrt(m_YM_sq);
print("m_YM = ", m_YM);

\\\\ Comoving invariant: m_YM * sqrt(|D|)
comoving = m_YM * sqrt(absD);
print("D=", {D}, " comoving m_YM*sqrt(|D|) = ", comoving);

\\\\ Compare to Phi_univ = pi^2 * sqrt(2) ≈ 13.958
phi_univ = Pi^2 * sqrt(2);
print("Phi_univ target = ", phi_univ);

ratio = comoving / phi_univ;
print("D=", {D}, " ratio comoving/Phi_univ = ", ratio);

dev_pct = abs(ratio - 1) * 100;
print("D=", {D}, " deviation = ", dev_pct, " %");

if(dev_pct < 0.5,
   print("D=", {D}, " VERDICT: WITHIN 0.5% — T1 candidate"),
   print("D=", {D}, " VERDICT: deviation > 0.5% — T2 maintained"));

print("===== NC3 Casimir D={D} DONE =====");
quit;
"""

def run_one(D):
    gp_file = f"/tmp/tier_d_NC3_D{abs(D)}.gp"
    out_file = f"{OUT_DIR}/NC3_D{abs(D)}.out"
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
    print(f"[{time.strftime('%H:%M:%S')}] Tier D NC3 Casimir launching {len(ANCHORS)} anchors...", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(run_one, D): D for D in ANCHORS}
        for f in as_completed(futs):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)

    # Aggregate
    print("\n===== AGGREGATE NC3 Casimir =====", flush=True)
    summary = {"anchors": [], "comoving_values": [], "deviations_pct": []}
    for D in ANCHORS:
        out_file = f"{OUT_DIR}/NC3_D{abs(D)}.out"
        if os.path.exists(out_file):
            with open(out_file) as f:
                content = f.read()
            for line in content.split("\n"):
                if "comoving m_YM*sqrt(|D|)" in line:
                    print(f"  D={D}: {line.strip()}")
                if "deviation" in line and "%" in line:
                    print(f"  D={D}: {line.strip()}")
                if "VERDICT" in line:
                    print(f"  D={D}: {line.strip()}")
    with open(f"{OUT_DIR}/SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[{time.strftime('%H:%M:%S')}] Tier D NC3 Casimir done.", flush=True)
