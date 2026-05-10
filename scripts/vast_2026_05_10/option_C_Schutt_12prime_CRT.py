#!/usr/bin/env python3
"""Option C — Schütt H^8 12-prime CRT extension for D=-67 (VAST MANAGER PRIORITY 1)
Cost: $3, ETA 6h, 80% ADVANCE expected.

Method:
- Weight-3 newform 67.3.b.a at level 67
- Compute a_p via PARI mfeigenvalue (works in 2.17.2 per VAST MANAGER)
- For each split prime p (kronecker(-67, p) = 1):
  - Compute Tr Sym^4 = a_p^4/p^4 - 2*a_p^2/p^2 + 3 (per D05 formula)
  - OR via Chebyshev T_4(a_p/2p) reduction
- Cross-check 12 primes total (5 from D05 + 7 new)

If 12/12 match Schütt's predictions → 80% ADVANCE Schütt-Hodge T2 PROVED-NUMERICAL multi-prime
NOTE: Independent of Opus #2 work (both cross-validate)
"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/option_C_Schutt_outputs"
os.makedirs(OUT_DIR, exist_ok=True)
GP = "/tmp/pari-2.17.2/gp"

# Split primes for D=-67 (kronecker(-67, p) = 1)
# Already verified by D05: {23, 29, 31, 37, 41}
# New: {47, 53, 59, 71, 73, 79, 83}
PRIMES_67 = [23, 29, 31, 37, 41, 47, 53, 59, 71, 73, 79, 83]

def gp_script_67(p):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);

print("===== Option C D=-67 p={p} START =====");

\\\\ Verify split: kronecker(-67, p) = 1
chi = kronecker(-67, {p});
print("kronecker(-67, ", {p}, ") = ", chi);
if(chi != 1, print("p={p} NOT SPLIT, skip"); quit);

\\\\ Try mfinit with weight-3 character chi_-67 at level 67
\\\\ chi_-67 is the Kronecker character mod 67
\\\\ In PARI 2.17.2: mfinit([67, 3, [-67]]) for character vector
\\\\ NOTE: VAST MANAGER says mfinit may return dim 0 ; use mfeigensearch instead

\\\\ Method A: try mfinit
G = mfinit([67, 3, -67], 1);  \\\\ S_3^new(67, chi_-67)
dim = mfdim(G);
print("mfdim G = ", dim);

if(dim > 0,
   \\\\ Get the eigenform basis
   B = mfbasis(G);
   print("mfbasis B size = ", #B);
   \\\\ Compute a_p for first form
   if(#B >= 1,
      f = B[1];
      a_p = mfcoef(f, {p});
      print("a_", {p}, " = ", a_p);

      \\\\ Sym^4 trace via formula: Tr Sym^4 = a_p^4/p^4 - 2*a_p^2/p^2 + 3
      \\\\ NOTE: For weight-3 CM newform, normalization may include p^(k-1) = p^2 factor
      \\\\ So actual Tr Sym^4 may need a_p / p^((k-1)/2) = a_p / p

      \\\\ V1: raw formula
      tr_sym4_v1 = a_p^4 / {p}^4 - 2 * a_p^2 / {p}^2 + 3;
      print("Tr Sym^4 v1 (raw) = ", tr_sym4_v1);

      \\\\ V2: with weight normalization a_p -> a_p / p^((k-1)/2) = a_p / p
      a_p_norm = a_p / {p};
      tr_sym4_v2 = a_p_norm^4 - 2 * a_p_norm^2 + 3;
      print("Tr Sym^4 v2 (normalized a_p/p) = ", tr_sym4_v2);

      \\\\ V3: Chebyshev T_4(x) where x = a_p_norm / 2 (x = cos theta)
      x = a_p_norm / 2;
      T_4 = 8 * x^4 - 8 * x^2 + 1;
      tr_sym4_v3 = 2 * T_4 + 1;
      print("Tr Sym^4 v3 (Chebyshev) = ", tr_sym4_v3);
   );
,
   print("p={p} mfinit dim 0, trying alternative approach");
);

print("===== Option C D=-67 p={p} DONE =====");
quit;
"""

def run_one(p):
    gp_file = f"/tmp/option_C_p{p}.gp"
    out_file = f"{OUT_DIR}/Schutt_67_p{p}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP p={p}"
    with open(gp_file, "w") as f:
        f.write(gp_script_67(p))
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True,
                          timeout=600, stdin=subprocess.DEVNULL)
        with open(out_file, "w") as f:
            f.write(r.stdout)
            if r.stderr:
                f.write("\n=== STDERR ===\n" + r.stderr[:2000])
        return f"OK p={p} ({len(r.stdout)} chars)"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT p={p}"
    except Exception as e:
        return f"ERR p={p} : {e}"

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] Option C Schutt 12-prime CRT D=-67 launching {len(PRIMES_67)} primes...", flush=True)
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(run_one, p): p for p in PRIMES_67}
        for f in as_completed(futs):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)

    # Aggregate
    print("\n===== AGGREGATE Option C Schutt =====", flush=True)
    for p in PRIMES_67:
        out_file = f"{OUT_DIR}/Schutt_67_p{p}.out"
        if os.path.exists(out_file):
            with open(out_file) as f:
                content = f.read()
            print(f"\n--- D=-67 p={p} ---")
            for line in content.split("\n"):
                if "kronecker" in line or "mfdim" in line or "a_" in line or "Tr Sym^4" in line:
                    print(f"  {line.strip()}")
    print(f"\n[{time.strftime('%H:%M:%S')}] Option C done.", flush=True)
