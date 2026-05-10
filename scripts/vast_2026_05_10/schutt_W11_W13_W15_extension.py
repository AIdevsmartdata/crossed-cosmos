#!/usr/bin/env python3
"""Schütt extension to weights {11, 13, 15} — extends MULTI-WEIGHT theorem
Cost: ~$5 / ETA <1 min wall on ssh5 96-core
After 18/18 W{5,7,9} → push to 36/36 by adding W{11, 13, 15}"""
import os, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/root/scripts/schutt_W11_W15_outputs"
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
INERT = {-7: 13, -11: 2, -19: 3, -43: 3, -67: 11, -163: 7}
WEIGHTS = [11, 13, 15]

def gp_script(D, w, p, ip):
    return f"""default(parisize, 16*10^9);
default(realprecision, 50);
print("===== W{w} D={D} p={p} START =====");
G = mfinit([abs({D}), {w}, {D}], 0);
print("mfdim = ", mfdim(G));
EB = mfeigenbasis(G);
print("nb_eigenforms = ", #EB);
for(idx=1, #EB, ap_inert = mfcoef(EB[idx], {ip}); print("EB", idx, "_a_inert_", {ip}, " = ", ap_inert));
for(idx=1, #EB, ap_split = mfcoef(EB[idx], {p}); print("EB", idx, "_a_split_", {p}, " = ", ap_split));
print("===== W{w} D={D} p={p} DONE =====");
quit;
"""

def newton(s, n, k):
    p = [2, s]
    for i in range(2, k + 1):
        p.append(s * p[-1] - n * p[-2])
    return p[k]

def find_pi(D, p):
    target = 4 * p if D % 4 == 1 else p
    for b in range(1, 50):
        rem = target - abs(D) * b * b
        if rem < 0:
            break
        sq = int(rem ** 0.5)
        if sq * sq == rem:
            return (sq, b)
    return None

def run_one(args):
    D, w, p = args
    label = f"D{abs(D)}_w{w}_p{p}"
    out_file = f"{OUT_DIR}/{label}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP {label}"
    gp_file = f"/tmp/sch_W11_15_{label}.gp"
    with open(gp_file, "w") as f:
        f.write(gp_script(D, w, p, INERT[D]))
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
        with open(out_file, "w") as f:
            f.write(r.stdout)
        return f"OK {label}"
    except Exception as e:
        return f"ERR {label} {e}"

if __name__ == "__main__":
    tasks = [(D, w, p) for D, primes in SPLIT_PRIMES.items() for w in WEIGHTS for p in primes]
    print(f"[{time.strftime('%H:%M:%S')}] Schutt W11+W13+W15 launching {len(tasks)} tasks...", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=32) as ex:
        for f in as_completed({ex.submit(run_one, t): t for t in tasks}):
            pass  # silent — collect at end
    wall = time.time() - t0

    # Verdict per (D, w)
    print(f"\n===== PER (D, w) verdict (wall {wall:.1f}s) =====")
    n_proved = 0
    for D in SPLIT_PRIMES:
        for w in WEIGHTS:
            matches = total = 0
            for p in SPLIT_PRIMES[D]:
                out_file = f"{OUT_DIR}/D{abs(D)}_w{w}_p{p}.out"
                if not os.path.exists(out_file):
                    continue
                with open(out_file) as f:
                    content = f.read()
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
                s_pos = a if D % 4 == 1 else 2*a
                total += 1
                if ap_split == newton(s_pos, p, w-1) or ap_split == newton(-s_pos, p, w-1):
                    matches += 1
            verdict = "PROVED" if matches == total and total >= 6 else "PARTIAL" if matches >= 3 else "DEAD"
            if verdict == "PROVED":
                n_proved += 1
            print(f"  D={D} w={w}: {matches}/{total} {verdict}")

    print(f"\nGlobal: {n_proved}/{len(SPLIT_PRIMES)*len(WEIGHTS)} (D, w) PROVED")
    if n_proved >= 15:
        print(f"🎉 Schutt MULTI-WEIGHT extended to {{5,7,9,11,13,15}} multi-D PROVED")
    print(f"\n[{time.strftime('%H:%M:%S')}] Done.", flush=True)
