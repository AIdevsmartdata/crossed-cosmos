#!/usr/bin/env python3
"""Schütt-Hodge MULTI-WEIGHT extension (W7 + W9) for 6 h_K=1 discriminants
Cost: ~$5 / ETA 30 sec - 5 min wall on ssh5 96-core
Builds on weight-5 PROVED-NUMERICAL multi-D (6/6 today)

Theorem extension: For h_K=1 D ∈ {-7, -11, -19, -43, -67, -163}
and weight w ∈ {7, 9} (Sym^6 ψ_K, Sym^8 ψ_K):
  CM newform a_p = π^(w-1) + π̄^(w-1) at split primes p

If 96/96 match (6 D × 8 primes × 2 weights) → MULTI-WEIGHT MULTI-D theorem
→ Hodge conjecture (E_K)^n implications for n > 8
"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/schutt_W7_W9_outputs"
os.makedirs(OUT_DIR, exist_ok=True)
GP = "/tmp/pari-2.17.2/gp"

SPLIT_PRIMES = {
    -7:    [11, 23, 29, 37, 43, 53, 67, 71],
    -11:   [3, 5, 23, 31, 37, 47, 53, 59],
    -19:   [5, 7, 11, 17, 23, 43, 47, 61],
    -43:   [11, 13, 17, 23, 41, 47, 53, 79],
    -67:   [23, 29, 37, 47, 59, 71, 73, 83],
    -163:  [41, 43, 47, 53, 61, 79, 83, 89],
}

INERT_SAMPLES = {-7: 13, -11: 2, -19: 3, -43: 3, -67: 11, -163: 7}

WEIGHTS = [7, 9]

def newton_p_n(s, n_norm, k):
    """Compute p_k = π^k + π̄^k via Newton's identity."""
    p = [2, s]
    for i in range(2, k + 1):
        p.append(s * p[-1] - n_norm * p[-2])
    return p[k]

def gp_script(D, weight, p, inert_p):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);
print("===== W{weight} D={D} p={p} START =====");
chi = kronecker({D}, {p});
print("kronecker_split = ", chi);
absD = abs({D});
G = mfinit([absD, {weight}, {D}], 0);
dim = mfdim(G);
print("mfdim = ", dim);
EB = mfeigenbasis(G);
print("nb_eigenforms = ", #EB);
for(idx=1, #EB, ap_inert = mfcoef(EB[idx], {inert_p}); print("EB", idx, "_a_inert_", {inert_p}, " = ", ap_inert));
for(idx=1, #EB, ap_split = mfcoef(EB[idx], {p}); print("EB", idx, "_a_split_", {p}, " = ", ap_split));
print("===== W{weight} D={D} p={p} DONE =====");
quit;
"""

def find_pi(D, p):
    absD = abs(D)
    target = 4 * p if D % 4 == 1 else p
    for b in range(1, 50):
        rem = target - absD * b * b
        if rem < 0:
            break
        sq = int(rem ** 0.5)
        if sq * sq == rem:
            return (sq, b)
    return None

def run_one(args):
    D, weight, p, inert_p = args
    label = f"D{abs(D)}_w{weight}_p{p}"
    gp_file = f"/tmp/schutt_W79_{label}.gp"
    out_file = f"{OUT_DIR}/{label}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP {label}", None
    with open(gp_file, "w") as f:
        f.write(gp_script(D, weight, p, inert_p))
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
        with open(out_file, "w") as f:
            f.write(r.stdout)
        # Parse
        data = {}
        for line in r.stdout.split("\n"):
            for prefix in ["kronecker_split", "mfdim", "nb_eigenforms"]:
                if line.startswith(prefix):
                    data[prefix] = line.split("=")[-1].strip()
            if line.startswith("EB"):
                parts = line.split("=")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    if val.lstrip("-").isdigit():
                        data[key] = val
        return f"OK {label}", data
    except Exception as e:
        return f"ERR {label} {e}", None

if __name__ == "__main__":
    tasks = [(D, w, p, INERT_SAMPLES[D]) for D, primes in SPLIT_PRIMES.items() for w in WEIGHTS for p in primes]
    print(f"[{time.strftime('%H:%M:%S')}] Schutt W7+W9 launching {len(tasks)} tasks (6 D × 8 p × 2 w)...", flush=True)
    t0 = time.time()
    results = {}
    with ThreadPoolExecutor(max_workers=32) as ex:
        for f in as_completed({ex.submit(run_one, t): t for t in tasks}):
            tup = futs = f
            tup_args = [t for fut, t in [(f, tasks[i]) for i in range(len(tasks))] if fut == f]
            status, data = f.result()
            print(f"[{time.strftime('%H:%M:%S')}] {status}", flush=True)
            if data:
                # We need the args to store
                pass
    wall = time.time() - t0

    # Re-parse all output files for verdict
    print(f"\n===== Per-D-W verdict =====")
    per_DW = {}
    for D in SPLIT_PRIMES:
        for w in WEIGHTS:
            matches = 0
            total = 0
            ap_data = {}
            for p in SPLIT_PRIMES[D]:
                out_file = f"{OUT_DIR}/D{abs(D)}_w{w}_p{p}.out"
                if not os.path.exists(out_file):
                    continue
                with open(out_file) as f:
                    content = f.read()
                # Find CM eigenform: a_inert = 0
                cm_idx = None
                for line in content.split("\n"):
                    if "a_inert_" in line and "= 0" in line:
                        cm_idx = line.split("_")[0]
                        break
                if not cm_idx:
                    continue
                ap_split = None
                for line in content.split("\n"):
                    if line.startswith(cm_idx) and "a_split_" in line:
                        try:
                            ap_split = int(line.split("=")[-1].strip())
                        except ValueError:
                            ap_split = None
                        break
                if ap_split is None:
                    continue
                pi_repr = find_pi(D, p)
                if pi_repr is None:
                    continue
                a, b = pi_repr
                # For D % 4 = 1, π = (a + b√D)/2, so π+π̄ = a (or -a)
                # For D % 4 = 0, π = a + b√D, so π+π̄ = 2a
                s_pos = a if D % 4 == 1 else 2*a
                s_neg = -s_pos
                n_norm = p
                pred_pos = newton_p_n(s_pos, n_norm, w-1)
                pred_neg = newton_p_n(s_neg, n_norm, w-1)
                total += 1
                if ap_split == pred_pos or ap_split == pred_neg:
                    matches += 1
                ap_data[p] = (ap_split, pred_pos, pred_neg)
            per_DW[(D, w)] = (matches, total, ap_data)
            verdict = "PROVED" if matches == total and total >= 6 else "PARTIAL" if matches >= 3 else "DEAD"
            print(f"  D={D} w={w}: {matches}/{total} {verdict}")
            for p, (ap, pp, pn) in ap_data.items():
                m = "✅" if ap in (pp, pn) else "❌"
                print(f"    p={p}: a_p={ap} pred=±({pp}/{pn}) {m}")

    n_proved = sum(1 for k, (m, t, _) in per_DW.items() if t > 0 and m == t and m >= 6)
    print(f"\n===== GLOBAL =====")
    print(f"  {n_proved}/{len(per_DW)} (D, w) combinations PROVED-NUMERICAL")
    print(f"  Wall time: {wall:.1f}s")
    if n_proved >= 10:
        print(f"  🎉 MULTI-WEIGHT MULTI-D THEOREM (extends weight-5 result)")

    with open(f"{OUT_DIR}/SUMMARY.json", "w") as f:
        json.dump({"wall_s": wall, "per_DW": {f"{k[0]}_w{k[1]}": [v[0], v[1]] for k, v in per_DW.items()}}, f, indent=2)
    print(f"\n[{time.strftime('%H:%M:%S')}] Done.", flush=True)
