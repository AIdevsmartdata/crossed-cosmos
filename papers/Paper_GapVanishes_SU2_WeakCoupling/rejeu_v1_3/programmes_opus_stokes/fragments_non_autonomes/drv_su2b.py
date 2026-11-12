
# ======================= RUN SU(2) : FAMILLES choisies par la variable FAMS (définie en tête) =======================
T0 = time.time()
def dstab(X):
    A, B = X
    return np.arctan2(np.sqrt(np.imag(A) ** 2 + np.abs(B) ** 2), np.real(A))
setup(2)
out = {"run": "su2_" + "+".join(FAMS), "nconf": NCONF}
fams = {}
if "exh" in FAMS:
    fams["exh_0000"] = closed_walks((0, 0, 0, 0), 6)
    fams["exh_1111"] = closed_walks((1, 1, 1, 1), 6)
if "rand" in FAMS:
    fams["random16"] = random_loops(1000, random.Random(99))
if "T1" in FAMS:
    P1, r1 = tree_note(1); fams["tree_T1_note"] = tree_loops(P1, r1)
if "T2" in FAMS:
    P2, r2 = tree_random(random.Random(7)); fams["tree_T2_random"] = tree_loops(P2, r2)
if "T3" in FAMS:
    P3, r3 = tree_dfs(random.Random(11)); fams["tree_T3_dfs"] = tree_loops(P3, r3)
rng = np.random.default_rng(SEED)
cfg = haar(NCONF, rng, dtype=DTYPE)
PT = plaq_table(cfg)
cfg8 = (cfg[0][:, :8].copy(), cfg[1][:, :8].copy())
res = {}
worst_loop = None
for name, loops in fams.items():
    st = {"loops": len(loops), "max_res": 0.0, "n_gt_1e-12": 0, "n_gt_1e-9": 0, "step_checked": 0, "step_max_res": 0.0,
          "delta_bound_viol": 0}
    for li, g in enumerate(loops):
        do_steps = (li < STEPS_FIRST) or name.startswith(("exh", "random"))
        recs, ev, info = decompose(g, keep_paths=do_steps)
        r = check_su2(g, recs, cfg, PT)
        if r > st["max_res"]:
            st["max_res"] = r
            if worst_loop is None or r > worst_loop[0]:
                worst_loop = (r, name, li, len(g) - 1, len(recs))
        if r > 1e-12: st["n_gt_1e-12"] += 1
        if r > 1e-9: st["n_gt_1e-9"] += 1
        if do_steps:
            st["step_checked"] += 1
            st["step_max_res"] = max(st["step_max_res"], check_steps(recs, ev, cfg8))
        # inégalité de la note : delta(U(gamma)) <= somme des delta(U_p)
        if li % 10 == 0:
            dg = dstab(hol(g, cfg))
            ds = sum(dstab(PT[rc.p]) for rc in recs) if recs else 0.0 * dg
            st["delta_bound_viol"] += int(np.sum(dg > ds + 1e-12))
            st["delta_max_gap"] = max(st.get("delta_max_gap", -9.0), float(np.max(dg - ds)))
        if time.time() - T0 > TLIM:
            st["stopped_at"] = li + 1
            break
    res[name] = st
    if time.time() - T0 > TLIM:
        break
out["families"] = res
out["worst"] = worst_loop
# témoins négatifs SU(2) sur quelques boucles (doivent donner un résidu O(1))
if NEG:
    negs = {"flip": [], "drop": [], "no_t": [], "reverse": []}
    sample = []
    for name, loops in fams.items():
        sample += [g for g in loops if len(g) > 5][:3]
    cfgs = (cfg[0][:, :100].copy(), cfg[1][:, :100].copy()); PTs = plaq_table(cfgs)
    for g in sample[:8]:
        recs, ev, info = decompose(g)
        if len(recs) < 2: continue
        for m in negs:
            negs[m].append(round(check_su2(g, recs, cfgs, PTs, mutant=m), 4))
    out["negative_controls_su2_residuals"] = negs
out["t_total"] = round(time.time() - T0, 1)
print(json.dumps(out))
