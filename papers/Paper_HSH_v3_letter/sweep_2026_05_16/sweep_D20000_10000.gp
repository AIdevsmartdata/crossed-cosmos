\\ HSH v3 EXTENDED sweep D in [-20000, -10000] fundamental discriminants
\\ Predict rats(D) = 2^rk_2(Cl(K)) if Cl(K) is 2-group, else 0
\\ Per Gauss 1801 Disq. §225-237 + Cox 1989 Thm 3.15 + Rubin 1991
\\ NOTE attribution Gauss/Rubin not Mazur-Rubin (corpus correction 2026-05-15)
\\
\\ This sweep extends the cumulative HSH v3 anchor set:
\\   [-2000, -1000]   ->  81 anchors (Apr-May 2026)
\\   [-10000, -2001]  -> 371 anchors (2026-05-16 morning)
\\   [-20000, -10001] -> ??? anchors (this run)

default(logfile, "/tmp/hsh_sweep_ext20k/sweep_raw.log");
default(log, 1);

print("=== HSH v3 EXTENDED sweep D in [-20000, -10001] ===");
print("Date: 2026-05-16");
print("");

\\ Helper: check if integer v is a power of 2
is_pow2(v) = {my(w=v); while(w>1 && w%2==0, w=w/2); w==1;}

\\ Number of distinct prime factors of |D| (used to check Gauss formula rk_2 = omega(|D|) - 1)
omega_abs(D) = {my(F); F = factor(abs(D)); matsize(F)[1];}

\\ Single-pass: collect all data
{
results = List();
nb_fund = 0;
nb_2group = 0;
nb_non2group = 0;
hist = vector(15);
gauss_ok = 0;
gauss_fail = 0;
gauss_fail_list = List();
sum_h_2group = 0;
for(D = -20000, -10001,
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
    if(is_2grp,
       nb_2group = nb_2group + 1;
       sum_h_2group = sum_h_2group + h,
       nb_non2group = nb_non2group + 1
    );
    if(rk_2 + 1 <= 15, hist[rk_2 + 1] = hist[rk_2 + 1] + 1);
    \\ Gauss formula sanity: rk_2(Cl(K)) = omega(|D|) - 1
    om = omega_abs(D);
    if(rk_2 == om - 1, gauss_ok = gauss_ok + 1,
       gauss_fail = gauss_fail + 1;
       listput(gauss_fail_list, [D, rk_2, om - 1, cyc])
    );
    listput(results, [D, h, cyc, rk_2, is_2grp, rats_pred]);
);

print("--- STATISTICS ---");
print("Total fundamental D in [-20000, -10001]: ", nb_fund);
print("Cl(K) is 2-group: ", nb_2group);
print("Cl(K) NOT 2-group (rats predicted = 0): ", nb_non2group);
print("Mean h on 2-group anchors: ", 1.0 * sum_h_2group / nb_2group);
print("");

print("rk_2 histogram (over all fundamental D, including non-2-group):");
for(i = 1, 15, if(hist[i] > 0, print("  rk_2 = ", i-1, ": ", hist[i])));
print("");

print("--- GAUSS FORMULA sanity check: rk_2(Cl(K)) = omega(|D|) - 1 ---");
print("Passed (rk_2 == omega(|D|) - 1): ", gauss_ok);
print("Failed: ", gauss_fail);
if(gauss_fail > 0 && #gauss_fail_list <= 10,
   print("Failure cases (D, rk_2, omega-1, cyc):");
   for(i = 1, #gauss_fail_list, print("  ", gauss_fail_list[i]))
);
print("");

print("--- 2-group anchors GROUPED by rk_2 ---");
for(target_rk = 0, 10,
    cnt = 0;
    for(i = 1, #results, r = results[i]; if(r[5] == 1 && r[4] == target_rk, cnt = cnt + 1));
    if(cnt > 0, print("  rk_2 = ", target_rk, ": ", cnt, " anchors  (rats = ", 2^target_rk, ")"))
);
print("");

print("--- High-rank pure 2-group anchors (rk_2 >= 4) ---");
for(i = 1, #results, r = results[i]; if(r[5] == 1 && r[4] >= 4, print("  D=", r[1], "  cyc=", r[3], "  h=", r[2], "  rk_2=", r[4], "  rats=", r[6])));
print("");

print("--- Pure elementary rk_2=4 anchors (cyc=[2,2,2,2], rats=16) ---");
purerk4 = List();
for(i = 1, #results, r = results[i]; if(r[5] == 1 && r[4] == 4 && r[3] == [2,2,2,2], listput(purerk4, r[1]); print("  D=", r[1], "  cyc=[2,2,2,2]  h=", r[2])));
print("Total pure rk_2=4 [2,2,2,2] anchors: ", #purerk4);
print("");

print("--- Pure elementary rk_2=5 anchors (cyc=[2,2,2,2,2], rats=32) ---");
purerk5 = List();
for(i = 1, #results, r = results[i]; if(r[5] == 1 && r[4] == 5 && r[3] == [2,2,2,2,2], listput(purerk5, r[1]); print("  D=", r[1], "  cyc=[2,2,2,2,2]  h=", r[2])));
print("Total pure rk_2=5 [2,2,2,2,2] anchors: ", #purerk5);
print("");

print("--- TABLE: 2-group D anchors (HSH v3 candidate anchors) ---");
print("D | h | Cl_cyc | rk_2 | rats_predicted");
print("---|---|--------|------|---------------");
count_anchors = 0;
for(i = 1, #results, r = results[i]; if(r[5] == 1, count_anchors = count_anchors + 1; print(r[1], " | ", r[2], " | ", r[3], " | ", r[4], " | ", r[6])));
print("");
print("=> Total ", count_anchors, " 2-group anchors in D in [-20000, -10001]");
print("");

\\ Write CSV with all 2-group anchors
csvfile = "/root/crossed-cosmos/papers/Paper_HSH_v3_letter/sweep_2026_05_16/anchors_2group_D20000_10000.csv";
write(csvfile, "D,h,Cl_cyc,rk_2,rats_predicted");
for(i = 1, #results,
    r = results[i];
    if(r[5] == 1,
       cyc_str = "\"" ;
       for(j = 1, #r[3], cyc_str = Str(cyc_str, r[3][j], if(j < #r[3], ", ", "")));
       cyc_str = Str(cyc_str, "\"");
       write(csvfile, r[1], ",", r[2], ",", cyc_str, ",", r[4], ",", r[6])
    )
);
print("CSV anchors written: ", csvfile);

\\ Cumulative tally
print("");
print("--- CUMULATIVE HSH v3 ANCHOR TALLY ---");
print("Range [-2000, -1000]   :  81 anchors (May 2026)");
print("Range [-10000, -2001]  : 371 anchors (2026-05-16 AM)");
print("Range [-20000, -10001] : ", count_anchors, " anchors (THIS SWEEP)");
print("Cumulative total       : ", 81 + 371 + count_anchors, " anchors");
}

quit();
