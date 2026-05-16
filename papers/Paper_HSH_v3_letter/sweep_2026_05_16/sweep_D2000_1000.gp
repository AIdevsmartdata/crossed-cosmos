\\ HSH v3 sweep D in [-2000, -1000] fundamental discriminants
\\ Predict rats(D) = 2^rk_2(Cl(K)) if Cl(K) is 2-group, else 0
\\ Per Gauss 1801 Disq. §225-237 + Cox 1989 Thm 3.15 + Rubin 1991

default(logfile, "/tmp/hsh_sweep/sweep_raw.log");
default(log, 1);

print("=== HSH v3 sweep D in [-2000, -1000] ===");
print("Date: 2026-05-16");
print("");

\\ Helper: check if integer v is a power of 2
is_pow2(v) = {my(w=v); while(w>1 && w%2==0, w=w/2); w==1;}

\\ Single-pass: collect all data
{
results = List();
nb_fund = 0;
nb_2group = 0;
nb_non2group = 0;
hist = vector(10);
for(D = -2000, -1000,
    K_disc = quaddisc(D);
    if(K_disc != D, next());
    nb_fund = nb_fund + 1;
    Cl = quadclassunit(K_disc);
    cyc = Cl[2];
    h = Cl[1];
    rk_2 = 0;
    for(j = 1, #cyc, if(cyc[j] % 2 == 0, rk_2 = rk_2 + 1));
    is_2grp = 1;
    for(j = 1, #cyc, if(!is_pow2(cyc[j]), is_2grp = 0));
    rats_pred = if(is_2grp, 2^rk_2, 0);
    if(is_2grp, nb_2group = nb_2group + 1, nb_non2group = nb_non2group + 1);
    if(rk_2 + 1 <= 10, hist[rk_2 + 1] = hist[rk_2 + 1] + 1);
    listput(results, [D, h, cyc, rk_2, is_2grp, rats_pred]);
);
print("--- TABLE 1: All fundamental D in [-2000, -1000] ---");
print("D | h | Cl_cyc | rk_2 | is_2group | rats_predicted");
print("---|---|--------|------|-----------|---------------");
for(i = 1, #results, r = results[i]; print(r[1], " | ", r[2], " | ", r[3], " | ", r[4], " | ", r[5], " | ", r[6]));
print("");
print("--- STATISTICS ---");
print("Total fundamental D in [-2000, -1000]: ", nb_fund);
print("Cl(K) is 2-group: ", nb_2group);
print("Cl(K) NOT 2-group (rats predicted = 0): ", nb_non2group);
print("");
print("rk_2 histogram (over all fundamental D, including non-2-group):");
for(i = 1, 10, if(hist[i] > 0, print("  rk_2 = ", i-1, ": ", hist[i])));
print("");
print("--- TABLE 2: Only 2-group D (HSH v3 candidate anchors) ---");
print("D | h | Cl_cyc | rk_2 | rats_predicted");
print("---|---|--------|------|---------------");
count_anchors = 0;
for(i = 1, #results, r = results[i]; if(r[5] == 1, count_anchors = count_anchors + 1; print(r[1], " | ", r[2], " | ", r[3], " | ", r[4], " | ", r[6])));
print("");
print("=> ", count_anchors, " 2-group anchors in D in [-2000, -1000]");
print("");
print("--- TABLE 3: Sample non-2-group (rats predicted = 0), first 15 ---");
print("D | h | Cl_cyc | rk_2");
count_zero = 0;
for(i = 1, #results, r = results[i]; if(r[5] == 0 && count_zero < 15, count_zero = count_zero + 1; print(r[1], " | ", r[2], " | ", r[3], " | ", r[4])));
print("");
print("--- 2-group anchors GROUPED by rk_2 ---");
for(target_rk = 0, 6, cnt = 0; for(i = 1, #results, r = results[i]; if(r[5] == 1 && r[4] == target_rk, cnt = cnt + 1)); if(cnt > 0, print("  rk_2 = ", target_rk, ": ", cnt, " anchors  (rats = ", 2^target_rk, ")")));
}

quit();
