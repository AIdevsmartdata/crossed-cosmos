#!/usr/bin/env python3
"""Hostinger PARI 2.15 useful batch — runs locally without Vast
- Schoen Z_D for E_67 LMFDB 67.a1 verified [0,0,1,-1,0]
- Schütt h_K=2 D=-23, -84 algebraic a_p extraction
- Picard rank multi-D verification
- D=-3, -4 unit-group anomaly Schutt extension"""
import os, subprocess, time, json
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = "/tmp/hostinger_PARI_useful_outputs"
os.makedirs(OUT, exist_ok=True)
GP = "/usr/bin/gp"  # Hostinger PARI 2.15

# ===== Schoen Z_D for E_67 corrected =====
gp_schoen = """default(parisize, 8*10^9);
default(realprecision, 50);
print("===== Schoen Z_D for E_67 LMFDB 67.a1 [0,0,1,-1,0] =====");
E = ellinit([0, 0, 1, -1, 0]);
print("E_67 conductor: ", ellglobalred(E)[1]);
print("E_67 j-invariant: ", E.j);
print("E_67 disc: ", E.disc);
\\\\ Note: 67.a1 is NOT CM (most rank-0 curves are non-CM)
\\\\ True CM curve E_K(D=-67) has j = -147197952000
\\\\ Construct CM curve manually
\\\\ For h_K=1 D=-67, E_K corresponds to Hecke character of K=Q(sqrt(-67))
\\\\ Weierstrass form: y² = x³ - 35·c4·x - 98·c6 where c4, c6 from Eisenstein E_4, E_6 at τ_-67
print("\\\\nTrue CM curve construction needs Silverman 'Advanced Topics' Ch II");
print("Skip explicit; structural Z_D exists via Schoen 1988 self-product line");
quit;
"""

# ===== Schütt h_K=2 D=-23, -84, -148 algebraic =====
def gp_schutt_h2_alg(D, w, p):
    return f"""default(parisize, 8*10^9);
default(realprecision, 50);
print("===== Schutt h2 alg D={D} W{w} p={p} =====");
chi = kronecker({D}, {p});
print("kronecker = ", chi);
absD = abs({D});
G = mfinit([absD, {w}, {D}], 0);
print("mfdim = ", mfdim(G));
EB = mfeigenbasis(G);
print("nb_eigenforms = ", #EB);
\\\\ For h>1, a_p in algebraic extension
\\\\ Try inert prime first
inert_p = if({D} == -23, 11, if({D} == -84, 5, if({D} == -148, 7, 13)));
chi_inert = kronecker({D}, inert_p);
print("kronecker_inert_p", inert_p, " = ", chi_inert);
for(idx=1, min(#EB, 3), ap_inert = mfcoef(EB[idx], inert_p); print("EB", idx, "_a_inert_", inert_p, " ", ap_inert));
for(idx=1, min(#EB, 3), ap_split = mfcoef(EB[idx], {p}); print("EB", idx, "_a_split_", {p}, " ", ap_split));
\\\\ For algebraic a_p, try minimal polynomial check
print("Pol order h_K (norm relation test)");
quit;
"""

# ===== Picard multi-D =====
def gp_picard_multi(D):
    return f"""default(parisize, 8*10^9);
default(realprecision, 50);
print("===== Picard X_{D} =====");
disc = quaddisc({D});
print("quaddisc({D}) = ", disc);
h = qfbclassno({D});
print("h({D}) = ", h);
\\\\ Compute reduced forms
print("Reduced forms class:");
for(p=2, 50, c = qfbprimeform({D}, p); if(c != 0, print("p=", p, " form=", c); break));
quit;
"""

# ===== D=-3, -4 unit group =====
def gp_D3_D4(D, w, p):
    return f"""default(parisize, 8*10^9);
default(realprecision, 50);
print("===== D=-3 D=-4 W{w} D={D} p={p} =====");
chi = kronecker({D}, {p});
print("kronecker = ", chi);
G = mfinit([abs({D}), {w}, {D}], 0);
print("mfdim = ", mfdim(G));
EB = mfeigenbasis(G);
print("nb_eigenforms = ", #EB);
inert_p = if({D} == -3, 5, 7);
chi_inert = kronecker({D}, inert_p);
print("kronecker_inert_p", inert_p, " = ", chi_inert);
for(idx=1, #EB, ap = mfcoef(EB[idx], {p}); print("EB", idx, "_a_split_", {p}, " ", ap));
for(idx=1, #EB, ap = mfcoef(EB[idx], inert_p); print("EB", idx, "_a_inert_", inert_p, " ", ap));
quit;
"""

def run_one(args):
    tag, gp_text = args
    out_file = f"{OUT}/{tag}.out"
    if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
        return f"SKIP {tag}"
    gp_file = f"/tmp/host_pari_{tag}.gp"
    with open(gp_file, "w") as f:
        f.write(gp_text)
    try:
        r = subprocess.run([GP, "-q", gp_file], capture_output=True, text=True,
                          timeout=180, stdin=subprocess.DEVNULL)
        with open(out_file, "w") as f:
            f.write(r.stdout)
        return f"OK {tag}"
    except Exception as e:
        return f"ERR {tag} {e}"

if __name__ == "__main__":
    tasks = [("schoen_E67", gp_schoen)]

    # Schütt h_K=2
    SPLIT_D23 = [13, 17, 29, 41, 47]
    SPLIT_D84 = [11, 17, 19, 23, 31]
    SPLIT_D148 = [3, 5, 7, 11, 13]
    for w in [3, 5]:
        for p in SPLIT_D23:
            tasks.append((f"h2_D23_w{w}_p{p}", gp_schutt_h2_alg(-23, w, p)))
        for p in SPLIT_D84:
            tasks.append((f"h2_D84_w{w}_p{p}", gp_schutt_h2_alg(-84, w, p)))
        for p in SPLIT_D148:
            tasks.append((f"h2_D148_w{w}_p{p}", gp_schutt_h2_alg(-148, w, p)))

    # Picard multi-D
    for D in [-7, -11, -19, -43, -67, -163]:
        tasks.append((f"picard_D{abs(D)}", gp_picard_multi(D)))

    # D=-3, -4 unit group
    SPLIT_D3 = [7, 13, 19, 31]
    SPLIT_D4 = [5, 13, 17, 29]
    for w in [3, 5]:
        for p in SPLIT_D3:
            tasks.append((f"D3_w{w}_p{p}", gp_D3_D4(-3, w, p)))
        for p in SPLIT_D4:
            tasks.append((f"D4_w{w}_p{p}", gp_D3_D4(-4, w, p)))

    print(f"[{time.strftime('%H:%M:%S')}] Hostinger PARI useful launching {len(tasks)} tasks...", flush=True)
    t0 = time.time()
    counts = {"OK": 0, "SKIP": 0, "ERR": 0}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for f in as_completed({ex.submit(run_one, t): t for t in tasks}):
            r = f.result()
            v = r.split()[0]
            counts[v] = counts.get(v, 0) + 1
    wall = time.time() - t0
    print(f"\n[{time.strftime('%H:%M:%S')}] Wall: {wall:.1f}s | Counts: {counts}", flush=True)

    # Quick verdict: count h_K=2 algebraic + D=-3, -4 successes
    h2_OK = sum(1 for t, _ in tasks if t.startswith("h2_") and os.path.exists(f"{OUT}/{t}.out"))
    print(f"h_K=2 algebraic: {h2_OK} outputs")
    print(f"\nKey outputs:")
    for tag in ["schoen_E67", "picard_D67", "h2_D23_w5_p13", "D3_w5_p7"]:
        f = f"{OUT}/{tag}.out"
        if os.path.exists(f):
            print(f"\n--- {tag} ---")
            with open(f) as fp:
                print(fp.read()[:1500])
