#!/usr/bin/env python3
"""Schutt H^8 multi-weight rescue v2 — FIXED PARI syntax (no inline if-quit, clean for-loop)
Cost: ~$0.30 ; ETA <2 min wall time on ssh5 96-core

Bug fixed: original v1 had inline `if(dim==0, ...; quit)` and `for(idx=1, min(5, #EB), ...; ...; ...)`
that PARI parser choked on. v2 uses clean for-loop with semicolons between statements inside parens,
no early quit, Python handles inert/error cases.

Mission: Validate Opus #6 prediction a_23 (weight-5 CM) = -617 for D=-67.
If at weight 5, eigenform identified with all 8 split primes giving a_p = pi^4 + pi-bar^4 →
Schutt-Hodge RESCUED at weight 5 (DS D05 was wrong weight, not wrong hypothesis).
"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/schutt_w_rescue_v2_outputs"
os.makedirs(OUT_DIR, exist_ok=True)
GP = "/tmp/pari-2.17.2/gp"

# Verified split primes via Option C
SPLIT_67 = [23, 29, 37, 47, 59, 71, 73, 83]   # 8 split primes for D=-67
# D=-163 needs larger primes (smaller p mostly inert) - use Option C-like search
SPLIT_163 = [41, 43, 47, 67, 71, 79, 83, 89]   # candidates - script will verify

WEIGHTS = [3, 5, 7]

def gp_script(D, weight, p):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);
print("===== W{weight} D={D} p={p} START =====");
chi = kronecker({D}, {p});
print("kronecker = ", chi);
absD = abs({D});
G = mfinit([absD, {weight}, {D}], 0);
dim = mfdim(G);
print("mfdim = ", dim);
EB = mfeigenbasis(G);
print("nb_eigenforms = ", #EB);
for(idx=1, #EB, ap = mfcoef(EB[idx], {p}); print("eigenform_", idx, "_a_", {p}, " = ", ap));
print("===== W{weight} D={D} p={p} DONE =====");
quit;
"""

def run_one(args):
    D, weight, p = args
    label = f"D{abs(D)}_w{weight}_p{p}"
    gp_file = f"/tmp/schutt_v2_{label}.gp"
    out_file = f"{OUT_DIR}/{label}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP {label}", None
    with open(gp_file, "w") as f:
        f.write(gp_script(D, weight, p))
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
        with open(out_file, "w") as f:
            f.write(r.stdout)
            if r.stderr:
                f.write("\n=== STDERR ===\n" + r.stderr[:2000])
        # Parse a_p values
        ap_data = {}
        for line in r.stdout.split("\n"):
            if line.startswith("eigenform_"):
                # eigenform_1_a_23 = -617
                parts = line.split("=")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    ap_data[key] = val
            elif line.startswith("kronecker = "):
                ap_data["kronecker"] = line.split("=")[1].strip()
            elif line.startswith("mfdim = "):
                ap_data["mfdim"] = line.split("=")[1].strip()
            elif line.startswith("nb_eigenforms = "):
                ap_data["nb_eigenforms"] = line.split("=")[1].strip()
        return f"OK {label}", ap_data
    except subprocess.TimeoutExpired:
        return f"TIMEOUT {label}", None
    except Exception as e:
        return f"ERR {label} : {e}", None

if __name__ == "__main__":
    tasks = []
    for D, primes in [(-67, SPLIT_67), (-163, SPLIT_163)]:
        for w in WEIGHTS:
            for p in primes:
                tasks.append((D, w, p))

    print(f"[{time.strftime('%H:%M:%S')}] Schutt v2 FIXED launching {len(tasks)} tasks...", flush=True)

    t0 = time.time()
    results = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(run_one, t): t for t in tasks}
        for f in as_completed(futs):
            tup = futs[f]
            status, ap_data = f.result()
            results[tup] = ap_data
            if "OK" in status:
                # Show eigenform a_p
                ef_keys = [k for k in (ap_data or {}) if k.startswith("eigenform_")]
                print(f"[{time.strftime('%H:%M:%S')}] {status} mfdim={ap_data.get('mfdim','?')} nb_ef={ap_data.get('nb_eigenforms','?')} : {', '.join(f'{k}={ap_data[k]}' for k in ef_keys)}", flush=True)
            else:
                print(f"[{time.strftime('%H:%M:%S')}] {status}", flush=True)
    wall = time.time() - t0

    # Aggregate per (D, w)
    print(f"\n===== AGGREGATE Schutt v2 (wall {wall:.1f}s) =====", flush=True)
    for D in [-67, -163]:
        for w in WEIGHTS:
            print(f"\n--- D={D}, weight={w} ---", flush=True)
            primes = SPLIT_67 if D == -67 else SPLIT_163
            for p in primes:
                key = (D, w, p)
                data = results.get(key)
                if not data:
                    print(f"  p={p}: NO DATA", flush=True)
                    continue
                kron = data.get("kronecker", "?")
                if kron == "-1":
                    print(f"  p={p}: INERT (kronecker={kron})", flush=True)
                    continue
                ef_keys = sorted([k for k in data if k.startswith("eigenform_")])
                if ef_keys:
                    print(f"  p={p} (split): mfdim={data.get('mfdim','?')} ; {', '.join(f'{k}={data[k]}' for k in ef_keys)}", flush=True)
                else:
                    print(f"  p={p} (split): NO EIGENFORM DATA", flush=True)

    # Verify CRITICAL prediction: a_23 (D=-67, w=5) = -617 ?
    print(f"\n===== CRITICAL VERIFICATION =====", flush=True)
    key_verify = (-67, 5, 23)
    data_verify = results.get(key_verify, {})
    print(f"D=-67, weight=5, p=23 : looking for a_23 = -617 (Opus #6 prediction)", flush=True)
    for k, v in data_verify.items():
        if k.startswith("eigenform_"):
            verdict = "✅ MATCH OPUS #6" if v.strip() == "-617" else f"❌ NO MATCH (got {v})"
            print(f"  {k} = {v}  {verdict}", flush=True)

    with open(f"{OUT_DIR}/SUMMARY.json", "w") as f:
        json.dump({"wall_s": wall, "results": {f"{k[0]}_{k[1]}_{k[2]}": v for k, v in results.items()}}, f, indent=2)
    print(f"\n[{time.strftime('%H:%M:%S')}] Schutt v2 done.", flush=True)
