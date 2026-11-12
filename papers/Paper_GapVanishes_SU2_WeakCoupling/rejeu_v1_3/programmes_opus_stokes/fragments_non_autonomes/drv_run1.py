
# ======================= RUN 1 : additif exact, comptes, boîte, témoins négatifs ; arbre court n = 1..5 =======================
T0 = time.time()
out = {"run": "run1_additif_comptes", "eps_longdouble": float(np.finfo(np.longdouble).eps)}
setup(2)
rng_py = random.Random(20261112)
fams = {}
fams["exh_0000"] = closed_walks((0, 0, 0, 0), 6)
fams["exh_1111"] = closed_walks((1, 1, 1, 1), 6)
P1, r1 = tree_note(1); P2, r2 = tree_random(random.Random(7)); P3, r3 = tree_dfs(random.Random(11))
fams["tree_T1_note"] = tree_loops(P1, r1)
fams["tree_T2_random"] = tree_loops(P2, r2)
fams["tree_T3_dfs"] = tree_loops(P3, r3)
fams["random16"] = random_loops(1000, random.Random(99))
forms = [[rng_py.randint(-10**6, 10**6) for _ in LINKS] for _ in range(20)]
Vn = (L + 1) ** 4
An = 6 * L * L * (2 * Vn - 1)
summ = {}
first_fail = None
for name, loops in fams.items():
    st = {"loops": len(loops), "add_fail": 0, "count_fail": 0, "N_gt_3Ll": 0, "N_gt_An": 0, "len_gt_2V-1": 0,
          "outside": 0, "t_const": 0, "t_len": {}, "maxN": 0, "maxlen": 0, "N_zero": 0}
    for g in loops:
        recs, ev, info = decompose(g)
        N = len(recs)
        st["maxN"] = max(st["maxN"], N); st["maxlen"] = max(st["maxlen"], len(g) - 1)
        if N == 0: st["N_zero"] += 1
        st["outside"] += info["outside"]; st["t_const"] += info["t_const"]
        for k, v in info["t_len"].items():
            st["t_len"][k] = st["t_len"].get(k, 0) + v
        if N != N_formula(g):
            st["count_fail"] += 1
        dc = dir_counts(g)
        if N > L * sum(i * dc[i] for i in range(4)) or N > 3 * L * (len(g) - 1):
            st["N_gt_3Ll"] += 1
        if name.startswith("tree"):
            if len(g) - 1 > 2 * Vn - 1: st["len_gt_2V-1"] += 1
            if N > An: st["N_gt_An"] += 1
        for c in forms:
            lhs = path_int(g, c)
            rhs = sum(rc.eps * curl(rc.p, c) for rc in recs)
            if lhs != rhs:
                st["add_fail"] += 1
                if first_fail is None:
                    first_fail = {"family": name, "loop": g, "lhs": lhs, "rhs": rhs}
                break
    st["t_len"] = {str(k): v for k, v in sorted(st["t_len"].items())}
    summ[name] = st
out["L=2"] = summ
out["A_n(L=2)"] = An
out["first_additive_failure"] = first_fail
# témoins négatifs additifs (doivent échouer)
neg = {"flip": 0, "drop": 0, "tested": 0}
for g in fams["tree_T3_dfs"][:200] + fams["random16"][:200]:
    recs, ev, info = decompose(g)
    if len(recs) == 0:
        continue
    neg["tested"] += 1
    c = forms[0]
    lhs = path_int(g, c)
    s = len(recs) // 2
    rhs_flip = sum((-rc.eps if k == s else rc.eps) * curl(rc.p, c) for k, rc in enumerate(recs))
    rhs_drop = sum(rc.eps * curl(rc.p, c) for k, rc in enumerate(recs) if k != s)
    neg["flip"] += (lhs != rhs_flip); neg["drop"] += (lhs != rhs_drop)
out["negative_controls_additive_detected"] = neg
out["t_run1a"] = round(time.time() - T0, 1)

# ---- arbre court T1 (chaînes temporelles + BFS de coquille) pour n = 1..5 : longueur des boucles d'arbre et N (formule) ----
short = {}
for n in range(1, 6):
    setup(2 * n)
    P, r = tree_note(n)
    path = tree_paths(P, r)
    maxlen = 0; maxN = 0; depth = 0
    for x in VERTS:
        depth = max(depth, len(path(x)) - 1)
    for (x, mu) in LINKS:
        y = add(x, mu, 1)
        for (a, b) in ((x, y), (y, x)):
            g = path(a) + path(b)[::-1]
            maxlen = max(maxlen, len(g) - 1)
            maxN = max(maxN, N_formula(g))
    short[n] = {"depth": depth, "max_loop_len": maxlen, "bound_14n-1": 14 * n - 1, "max_N": maxN,
                "bound_6n(14n-1)": 6 * n * (14 * n - 1), "A_n_note": 6 * (2 * n) ** 2 * (2 * (2 * n + 1) ** 4 - 1)}
    if time.time() - T0 > 420:
        break
out["short_tree"] = short
# ---- n = 2 : algorithme littéral sur toutes les boucles de T1, compte = formule et additif exact ----
setup(4)
P, r = tree_note(2)
loops = tree_loops(P, r)
f2 = [random.Random(5).randint(-10**6, 10**6) for _ in LINKS]
bad = 0; badc = 0; outside = 0; done = 0
for g in loops:
    recs, ev, info = decompose(g)
    outside += info["outside"]
    if len(recs) != N_formula(g): badc += 1
    if path_int(g, f2) != sum(rc.eps * curl(rc.p, f2) for rc in recs): bad += 1
    done += 1
    if time.time() - T0 > 560:
        break
out["n2_T1_literal"] = {"loops_done": done, "of": len(loops), "count_fail": badc, "add_fail": bad, "outside": outside}
out["t_total"] = round(time.time() - T0, 1)
print(json.dumps(out))
