\\ Sanity check: existing 7 anchors from project_HSH_v3_OPUS_VINDICATED.md
\\ D = -23, -260, -280, -420, -456, -924, -5460
\\ AND outside-range candidates we should NOT see in sweep

is_pow2(v) = {my(w=v); while(w>1 && w%2==0, w=w/2); w==1;}

{
print("=== Sanity check 7 existing HSH v3 anchors ===");
print("");
existing = [-23, -260, -280, -420, -456, -924, -5460];
expected_rats = [0, 4, 4, 8, 4, 0, 16];  \\ from memory snapshot
for(i = 1, #existing,
    D = existing[i];
    K_disc = quaddisc(D);
    if(K_disc != D,
        print("D=", D, " : NOT FUNDAMENTAL (quaddisc=", K_disc, ")");
        next();
    );
    Cl = quadclassunit(K_disc);
    cyc = Cl[2];
    h = Cl[1];
    rk_2 = 0;
    for(j = 1, #cyc, if(cyc[j] % 2 == 0, rk_2 = rk_2 + 1));
    is_2grp = 1;
    for(j = 1, #cyc, if(!is_pow2(cyc[j]), is_2grp = 0));
    rats_pred = if(is_2grp, 2^rk_2, 0);
    match = if(rats_pred == expected_rats[i], "MATCH", "*** MISMATCH ***");
    print("D=", D, " | h=", h, " | Cl=", cyc, " | rk_2=", rk_2, " | is_2grp=", is_2grp, " | pred=", rats_pred, " | expected=", expected_rats[i], " | ", match);
);
print("");
print("=== Spot-check key 2-group D from [-2000,-1000] sweep ===");
spot = [-1995, -1992, -1860, -1540, -1320, -1155, -1140, -1092, -1012, -1003];
for(i = 1, #spot,
    D = spot[i];
    K_disc = quaddisc(D);
    if(K_disc != D,
        print("D=", D, " : NOT FUNDAMENTAL");
        next();
    );
    Cl = quadclassunit(K_disc);
    cyc = Cl[2];
    h = Cl[1];
    rk_2 = 0;
    for(j = 1, #cyc, if(cyc[j] % 2 == 0, rk_2 = rk_2 + 1));
    is_2grp = 1;
    for(j = 1, #cyc, if(!is_pow2(cyc[j]), is_2grp = 0));
    rats_pred = if(is_2grp, 2^rk_2, 0);
    print("D=", D, " | h=", h, " | Cl=", cyc, " | rk_2=", rk_2, " | is_2grp=", is_2grp, " | pred=", rats_pred);
);
print("");
print("=== Consistency: 2^rk_2 = h for 2-group (definition) ===");
spot2 = [-1995, -1860, -1140, -1092, -1540, -1320, -1428, -1380, -1155];
for(i = 1, #spot2,
    D = spot2[i];
    Cl = quadclassunit(quaddisc(D));
    cyc = Cl[2]; h = Cl[1];
    rk_2 = 0;
    for(j = 1, #cyc, if(cyc[j] % 2 == 0, rk_2 = rk_2 + 1));
    print("D=", D, " : h=", h, ", #cyc=", #cyc, ", rk_2=", rk_2, ", 2^rk_2=", 2^rk_2, " => 2-group? h is 2-power? ", h, "==2^", valuation(h,2), "?");
);
}
quit();
