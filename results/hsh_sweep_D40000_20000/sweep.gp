\\ HSH Sweep: D in [-40000, -20001] — chasse rk_2=5 PUR
\\ PARI 2.15.4 — Hostinger VPS
default(parisizemax, 2^30);

{
OUT = "/root/crossed-cosmos/results/hsh_sweep_D40000_20000/";

count = 0;
rk2_dist = vector(6);
total_2group = 0;
rk2_5_list = List();

t0 = getwalltime();

print("=== HSH Sweep D in [-40000, -20001] ===");

for(D = -40000, -20001,
  if(isfundamental(D),
    bnf = bnfinit(x^2 - D, 1);
    cyc = bnf.clgp[2];

    if(#cyc > 0,
      is_2group = 1;
      for(i=1, #cyc, if(cyc[i] % 2 != 0, is_2group = 0; break));
      if(is_2group,
        total_2group = total_2group + 1;
        rk2 = #cyc;
        if(rk2 <= 5, rk2_dist[rk2] = rk2_dist[rk2] + 1);
        if(rk2 > 5,
          print("WARNING: rk_2=", rk2, " > 5 at D=", D, " cyc=", cyc);
        );
        if(rk2 == 5 && cyc == [2,2,2,2,2],
          print("*** FOUND rk_2=5 PUR at D=", D, " cyc=", cyc, " ***");
          listput(rk2_5_list, [D, cyc]);
          write(concat(OUT, "rk2_5_candidates.txt"), D, " ", cyc);
        );
      );
    );

    count = count + 1;
    if(count % 1000 == 0,
      elapsed = (getwalltime() - t0) / 1000.0;
      rate = count / max(elapsed, 0.001);
      print("Progress: ", count, " D=", D, " | elapsed=", floor(elapsed), "s | rk2_dist=", rk2_dist, " | total_2gp=", total_2group);
      write(concat(OUT, "progress.txt"), "count=", count, " D=", D, " elapsed=", elapsed, " rk2_dist=", rk2_dist, " total_2gp=", total_2group);
    );
  );
);

elapsed = (getwalltime() - t0) / 1000.0;

print("");
print("========================================");
print("SWEEP COMPLETE");
print("========================================");
print("Range: D in [-40000, -20001]");
print("Total fundamental D processed: ", count);
print("Elapsed: ", floor(elapsed), "s (", floor(elapsed/60), "m)");
print("Rate: ", count/max(elapsed, 0.001), " D/s");
print("rk_2 distribution (1-5): ", rk2_dist);
print("Total 2-groups found: ", total_2group);
print("Non-2-groups: ", count - total_2group);
print("rk_2=5 PUR candidates: ", #rk2_5_list);

if(#rk2_5_list == 0,
  print("");
  print("=== Cohen-Lenstra Extrapolation ===");
  print("CL prob rk_2=5: 2^{-25} = ", 1.0/2^25);
  print("Expected in this range: ", count * 1.0/2^25);
);

\\ Write results
write(concat(OUT, "sweep_results.txt"),
  "SWEEP D in [-40000, -20001]",
  "",
  "Total fundamental D: ", count,
  "Elapsed: ", floor(elapsed), "s",
  "",
  "rk_2 distribution:",
  "  rk_2=1: ", rk2_dist[1],
  "  rk_2=2: ", rk2_dist[2],
  "  rk_2=3: ", rk2_dist[3],
  "  rk_2=4: ", rk2_dist[4],
  "  rk_2=5: ", rk2_dist[5],
  "  Total 2-groups: ", total_2group,
  "  Non-2-groups: ", count - total_2group
);

if(#rk2_5_list > 0,
  for(i=1, #rk2_5_list,
    write(concat(OUT, "rk2_5_candidates.txt"), rk2_5_list[i][1], " ", rk2_5_list[i][2]);
  );
,
  write(concat(OUT, "rk2_5_candidates.txt"), "NO rk_2=5 PUR found in [-40000, -20001]");
);

write(concat(OUT, "stats.txt"),
  "=== HSH Sweep Stats ===",
  "Range: D in [-40000, -20001]",
  "",
  "Fundamental discriminants: ", count,
  "Elapsed: ", floor(elapsed), "s",
  "",
  "rk_2 distribution:",
  "  rk_2=1: ", rk2_dist[1],
  "  rk_2=2: ", rk2_dist[2],
  "  rk_2=3: ", rk2_dist[3],
  "  rk_2=4: ", rk2_dist[4],
  "  rk_2=5: ", rk2_dist[5],
  "  Total 2-groups: ", total_2group,
  "  rk_2=5 PUR: ", #rk2_5_list,
  "",
  "Cohen-Lenstra extrapolation:",
  "  P(rk_2=5) ~ 2^{-25} = ", 1.0/2^25,
  "  Expected in range: ", count * 1.0/2^25
);

print("");
print("Results written to ", OUT);
quit();
}
