
# ======================= RUN 7 (bac sandbox) : boîte n = 2 (L = 4), SU(2) 10^4 configurations + additif, arbres T1 et T2 =======================
import multiprocessing as mpc
T0 = time.time()
setup(4)
P1, r1 = tree_note(2); P2, r2 = tree_random(random.Random(7))
FAM = {"tree_T1_note_n2": tree_loops(P1, r1), "tree_T2_random_n2": tree_loops(P2, r2)}
rng = np.random.default_rng(20261112)
CFG = haar(10000, rng)
PT = plaq_table(CFG)
FORM = [random.Random(3).randint(-10**6, 10**6) for _ in LINKS]
def work(args):
    name, i0, i1 = args
    loops = FAM[name][i0:i1]
    mx = 0.0; n12 = 0; n9 = 0; addf = 0; cntf = 0; out = 0; maxN = 0; maxl = 0
    for g in loops:
        recs, ev, info = decompose(g)
        out += info["outside"]; maxN = max(maxN, len(recs)); maxl = max(maxl, len(g) - 1)
        if len(recs) != N_formula(g): cntf += 1
        if path_int(g, FORM) != sum(rc.eps * curl(rc.p, FORM) for rc in recs): addf += 1
        r = check_su2(g, recs, CFG, PT)
        mx = max(mx, r); n12 += r > 1e-12; n9 += r > 1e-9
    return name, mx, n12, n9, addf, cntf, out, maxN, maxl, len(loops)
tasks = []
for name, loops in FAM.items():
    step_ = 50
    for i in range(0, len(loops), step_):
        tasks.append((name, i, min(i + step_, len(loops))))
ctx = mpc.get_context("fork")
res = {}
with ctx.Pool(16) as pool:
    for name, mx, n12, n9, addf, cntf, out, maxN, maxl, k in pool.imap_unordered(work, tasks):
        st = res.setdefault(name, {"loops": 0, "max_res": 0.0, "n_gt_1e-12": 0, "n_gt_1e-9": 0, "add_fail": 0, "count_fail": 0, "outside": 0, "maxN": 0, "maxlen": 0})
        st["loops"] += k; st["max_res"] = max(st["max_res"], mx); st["n_gt_1e-12"] += int(n12); st["n_gt_1e-9"] += int(n9)
        st["add_fail"] += addf; st["count_fail"] += cntf; st["outside"] += out; st["maxN"] = max(st["maxN"], maxN); st["maxlen"] = max(st["maxlen"], maxl)
print(json.dumps({"run": "run7_L4_sandbox", "families": res, "t_total": round(time.time() - T0, 1)}))
