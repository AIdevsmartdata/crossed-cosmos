\\ ============================================================
\\ r_1_test_T200.gp  v3
\\ M98 -- Paper-grade RMT statistics for L(4.5.b.a, s)
\\ T=200, ~150+ zeros, pair correlation + chi^2 vs GUE
\\ PARI/GP 2.11+  (tested 2.17.3)
\\
\\ v3 FIXES vs v2:
\\  - RESERVED NAMES: j=j_invariant, i=sqrt(-1) in PARI.
\\    Use nn, kk, mm, pp as loop variables throughout.
\\  - EMBEDDED BRACES: PARI batch mode disallows { } blocks at
\\    top level (only inside function bodies). Wrap all loops
\\    that need local vars in named functions.
\\  - PRINTF FORMAT: "[" inside a format string is parsed as
\\    vector-subscript start. Avoid "[" and "]" in printf strings;
\\    write "in (0.5 to 2.0)" style or escape via a string variable.
\\ ============================================================
\\
\\ CONTEXT: 4.5.b.a is a CM newform (Gamma_0(4), wt=5, chi_4)
\\ a_2=-4, a_5=-14 (LMFDB verified M81); analytic rank=0
\\ q_an = 25/Pi^2; epsilon=+1; Sato-Tate U(1)[D_2]
\\ ============================================================

default(parisize, 1024000000);
default(realbitprecision, 64);

time_start = getwalltime();

print("====================================================");
print("M98 v3 -- L(4.5.b.a,s) zeros T=200, paper-grade RMT");
print("ECI project -- Kevin Remondiere, 2026-05-06");
print("====================================================");
print("");

\\ ============================================================
\\ Global helpers
\\ ============================================================
q_an_val = 4 * (5 / (2*Pi))^2;
Delta_local(T)  = 2*Pi / log(q_an_val * T / (2*Pi));
R2_GUE(r)       = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

R_MAX         = 5.0;
BIN_WIDTH     = 0.1;
N_BINS        = 50;
CHI2_THRESH   = 98;

\\ ============================================================
\\ build_pair_hist(ng, Ngaps) -- pair correlation histogram
\\ Returns [hist_pair, N_pairs]
\\ Uses reserved-name-safe loop variables mm, pp
\\ ============================================================
build_pair_hist(ng, Ngaps) = {
  my(h, Np, sc, bi);
  h  = vector(N_BINS, kk, 0);
  Np = 0;
  for(mm = 1, Ngaps,
    sc = 0;
    for(pp = mm, Ngaps,
      sc = sc + ng[pp];
      if(sc > R_MAX, break());
      bi = floor(sc / BIN_WIDTH) + 1;
      if(bi >= 1,
        if(bi <= N_BINS,
          h[bi] = h[bi] + 1;
          Np = Np + 1
        )
      )
    )
  );
  [h, Np]
}

\\ build_nn_hist(ng, Ngaps) -- nearest-neighbor histogram
build_nn_hist(ng, Ngaps) = {
  my(h, bi);
  h = vector(N_BINS, kk, 0);
  for(nn = 1, Ngaps,
    bi = floor(ng[nn] / BIN_WIDTH) + 1;
    if(bi >= 1,
      if(bi <= N_BINS,
        h[bi] = h[bi] + 1
      )
    )
  );
  h
}

\\ chi2_vs(obs, exp_v, minexp) -- chi^2 of obs vs exp; skip bins < minexp
chi2_vs(obs, exp_v, minexp) = {
  my(c2, dof);
  c2  = 0.0;
  dof = 0;
  for(kk = 1, N_BINS,
    if(exp_v[kk] >= minexp,
      c2  = c2  + (obs[kk] - exp_v[kk])^2 / exp_v[kk];
      dof = dof + 1
    )
  );
  [c2, dof - 1]
}

\\ export_csv(zeros_v, ng, Nz) -- print CSV lines
export_csv(zeros_v, ng, Nz) = {
  for(nn = 1, Nz - 1,
    printf("CSV %d,%.12f,%.8f\n", nn, zeros_v[nn], ng[nn])
  );
  printf("CSV %d,%.12f,NA\n", Nz, zeros_v[Nz])
}

\\ export_hist(hp, gep, nh, gne, goe) -- histogram table
export_hist(hp, gep, nh, gne, goe) = {
  my(rc);
  for(kk = 1, N_BINS,
    rc = (kk - 0.5) * BIN_WIDTH;
    printf("BIN %.2f  %d  %.4f  %d  %.4f  %.4f\n",
      rc, hp[kk], gep[kk], nh[kk], gne[kk], goe[kk])
  )
}

\\ ============================================================
\\ STEP 1: Modular form
\\ ============================================================
print("Step 1: mfinit [4,5,Mod(3,4)] ...");
mf   = mfinit([4, 5, Mod(3,4)], 1);
F    = mfeigenbasis(mf);
if(#F == 0, error("No newforms found"));
print("  newforms = ", #F);
f    = F[1];
coef = mfcoefs(f, 6);
a2   = coef[3];
a5   = coef[6];
print("  a_2 = ", a2, "  (LMFDB: -4)");
print("  a_5 = ", a5, "  (LMFDB: -14)");
if(a2 != -4,  error("a_2 MISMATCH got ", a2));
if(a5 != -14, error("a_5 MISMATCH got ", a5));
print("  VERIFIED.");
print("");

\\ ============================================================
\\ STEP 2: Zeros to T=200
\\ ============================================================
T_MAX = 200;
print("Step 2: lfunmf + lfuninit + lfunzeros T=", T_MAX, " ...");
ldata  = lfunmf(mf, f);
lf     = lfuninit(ldata, [T_MAX]);
print("  lfuninit done.  t=", (getwalltime()-time_start)/1000, "s");
zeros_v = lfunzeros(lf, [0, T_MAX]);
N_zeros = #zeros_v;
print("  lfunzeros done.  t=", (getwalltime()-time_start)/1000, "s");
weyl_est = (T_MAX/(2*Pi)) * log(q_an_val * T_MAX / (2*Pi)) - T_MAX/(2*Pi);
print("  N_zeros = ", N_zeros, "  (Weyl ~ ", round(weyl_est), ")");
if(N_zeros < 2, error("Too few zeros"));
print("");

\\ ============================================================
\\ STEP 3: Normalized gaps (M94 single-line fix; safe var name)
\\ ============================================================
print("Step 3: Normalized gaps ...");
ng    = vector(N_zeros-1, nn, (zeros_v[nn+1]-zeros_v[nn]) / Delta_local((zeros_v[nn]+zeros_v[nn+1])/2));
N_gaps = N_zeros - 1;
print("  N_gaps = ", N_gaps);
print("");

\\ ============================================================
\\ STEP 4: Basic statistics (safe var names)
\\ ============================================================
print("Step 4: Basic statistics ...");
r1      = ng[1];
r_sum   = sum(nn=1, N_gaps, ng[nn]);
r_sum2  = sum(nn=1, N_gaps, ng[nn]^2);
r_mean  = r_sum / N_gaps;
r_var   = r_sum2/N_gaps - r_mean^2;
r_std   = sqrt(r_var);
r_max   = vecmax(ng);
r_min   = vecmin(ng);
r_dev   = abs(r_mean - 1.0);
printf("  r_1        = %.8f\n", r1);
printf("  mean(r_n)  = %.8f  (GUE: 1.000)\n", r_mean);
printf("  std(r_n)   = %.8f\n", r_std);
printf("  var(r_n)   = %.8f\n", r_var);
printf("  max(r_n)   = %.8f\n", r_max);
printf("  min(r_n)   = %.8f\n", r_min);
printf("  |mean-1|   = %.8f\n", r_dev);
print("");

\\ ============================================================
\\ STEP 5: r_1 verdict
\\ Use string concat for output; avoid [ ] in printf strings
\\ ============================================================
print("Step 5: r_1 verdict ...");
if(r1 < 0.5,
  printf("  r_1 = %.6f < 0.5 -- SMALL FIRST GAP (possible CM zero clustering)\n", r1)
);
if(r1 >= 0.5,
  if(r1 <= 2.0,
    printf("  r_1 = %.6f  VERDICT: NORMAL (in 0.5 to 2.0 -- GUE/SO(even))\n", r1)
  )
);
if(r1 > 2.0,
  if(r1 <= 2.5,
    printf("  r_1 = %.6f  VERDICT: BORDERLINE (2.0 to 2.5) -- need T=500\n", r1)
  )
);
if(r1 > 2.5,
  printf("  r_1 = %.6f  VERDICT: ANOMALY > 2.5 -- Exp.Math letter potential!\n", r1)
);
if(r_dev > 0.15,
  printf("  MEAN: WARNING |mean-1|=%.6f > 0.15\n", r_dev)
);
if(r_dev <= 0.15,
  printf("  MEAN: OK |mean-1|=%.6f\n", r_dev)
);
print("");

\\ ============================================================
\\ STEP 6: Pair correlation histogram (in function -- safe)
\\ ============================================================
print("Step 6: Pair correlation histogram ...");
pair_res  = build_pair_hist(ng, N_gaps);
hist_pair = pair_res[1];
N_pairs   = pair_res[2];
print("  Pairs counted: ", N_pairs);

gue_unnorm = sum(kk=1, N_BINS, R2_GUE((kk-0.5)*BIN_WIDTH)*BIN_WIDTH);
if(gue_unnorm < 1e-10, error("GUE norm near zero"));
nf_pair     = N_pairs / gue_unnorm;
gue_pair_e  = vector(N_BINS, kk, nf_pair * R2_GUE((kk-0.5)*BIN_WIDTH)*BIN_WIDTH);
print("");

\\ ============================================================
\\ STEP 7: Chi^2 pair correlation
\\ ============================================================
print("Step 7: Chi^2 pair correlation ...");
c2p  = chi2_vs(hist_pair, gue_pair_e, 5);
chi2_pair = c2p[1];
dof_pair  = c2p[2];
printf("  chi^2 pair corr vs GUE = %.4f  dof=%d  threshold=%d\n", chi2_pair, dof_pair, CHI2_THRESH);
if(chi2_pair > CHI2_THRESH,
  printf("  PAIR CORR: WARNING chi^2=%.2f > %d (GUE deviation)\n", chi2_pair, CHI2_THRESH)
);
if(chi2_pair <= CHI2_THRESH,
  printf("  PAIR CORR: PASS chi^2=%.2f consistent with GUE\n", chi2_pair)
);
print("");

\\ ============================================================
\\ STEP 8: Nearest-neighbor P(s)
\\ ============================================================
print("Step 8: Nearest-neighbor P(s) ...");
nn_hist   = build_nn_hist(ng, N_gaps);
gue_nn_u  = sum(kk=1, N_BINS, p_GUE_wigner((kk-0.5)*BIN_WIDTH)*BIN_WIDTH);
goe_nn_u  = sum(kk=1, N_BINS, p_GOE_wigner((kk-0.5)*BIN_WIDTH)*BIN_WIDTH);
gue_nn_e  = vector(N_BINS, kk, N_gaps * p_GUE_wigner((kk-0.5)*BIN_WIDTH)*BIN_WIDTH / gue_nn_u);
goe_nn_e  = vector(N_BINS, kk, N_gaps * p_GOE_wigner((kk-0.5)*BIN_WIDTH)*BIN_WIDTH / goe_nn_u);

c2g = chi2_vs(nn_hist, gue_nn_e, 3);
c2o = chi2_vs(nn_hist, goe_nn_e, 3);
chi2_nn_gue = c2g[1];
chi2_nn_goe = c2o[1];
dof_nn      = c2g[2];
printf("  chi^2 NN vs GUE = %.4f  dof~%d\n", chi2_nn_gue, dof_nn);
printf("  chi^2 NN vs GOE = %.4f  dof~%d\n", chi2_nn_goe, dof_nn);
if(chi2_nn_goe < chi2_nn_gue,
  printf("  P(s): closer to GOE/SO(even) -- CM form prediction (ratio=%.4f)\n", chi2_nn_goe/chi2_nn_gue)
);
if(chi2_nn_goe >= chi2_nn_gue,
  printf("  P(s): closer to GUE (ratio=%.4f)\n", chi2_nn_goe/chi2_nn_gue)
);
print("");

\\ ============================================================
\\ STEP 9: Histogram table
\\ ============================================================
print("Step 9: Histogram table ...");
print("BIN_TABLE: r_center pair_obs GUE_pair_exp nn_obs GUE_nn_exp GOE_nn_exp");
export_hist(hist_pair, gue_pair_e, nn_hist, gue_nn_e, goe_nn_e);
print("");

\\ ============================================================
\\ STEP 10: Raw zeros CSV
\\ ============================================================
print("Step 10: Raw zeros CSV ...");
print("CSV_HEADER: n,gamma_n,norm_gap_to_next");
export_csv(zeros_v, ng, N_zeros);
print("");

\\ ============================================================
\\ STEP 11: Final summary
\\ ============================================================
t_total = (getwalltime()-time_start)/1000;

print("====================================================");
print("M98 v3 FINAL SUMMARY");
print("====================================================");
printf("  Form:          4.5.b.a  (Gamma_0(4), wt=5, chi_4, CM)\n");
printf("  T_max:         %d\n", T_MAX);
printf("  N_zeros:       %d  (Weyl ~ %d)\n", N_zeros, round(weyl_est));
printf("  N_gaps:        %d\n", N_gaps);
printf("  q_an:          %.6f  (= 25/Pi^2)\n", q_an_val);
print("  ---");
printf("  r_1:           %.8f\n", r1);
printf("  mean(r_n):     %.8f  (GUE: 1.0)\n", r_mean);
printf("  std(r_n):      %.8f\n", r_std);
printf("  max(r_n):      %.8f\n", r_max);
printf("  min(r_n):      %.8f\n", r_min);
print("  ---");
printf("  chi^2 pair/GUE: %.4f  dof=%d  thresh=%d\n", chi2_pair, dof_pair, CHI2_THRESH);
printf("  chi^2 NN/GUE:   %.4f  dof=%d\n", chi2_nn_gue, dof_nn);
printf("  chi^2 NN/GOE:   %.4f  dof=%d\n", chi2_nn_goe, dof_nn);
print("  ---");
printf("  Wall time:     %.1f s\n", t_total);
print("");
print("VERDICT:");
if(r1 < 0.5,
  printf("  r_1=%.6f SMALL (<0.5): CM zero clustering at base (NOT anomaly in r_1>2.5 sense)\n", r1)
);
if(r1 >= 0.5,
  if(r1 <= 2.0,
    printf("  r_1=%.6f NORMAL (0.5 to 2.0)\n", r1)
  )
);
if(r1 > 2.0,
  if(r1 <= 2.5,
    printf("  r_1=%.6f BORDERLINE (2.0 to 2.5) -- needs T=500\n", r1)
  )
);
if(r1 > 2.5,
  printf("  r_1=%.6f ANOMALY > 2.5 -- NEW Exp.Math. letter potential!\n", r1)
);
if(chi2_pair > CHI2_THRESH,
  printf("  ALERT: Pair corr chi^2=%.2f > %d -- GUE deviation\n", chi2_pair, CHI2_THRESH)
);
if(chi2_pair <= CHI2_THRESH,
  printf("  OK: Pair corr chi^2=%.2f consistent with GUE\n", chi2_pair)
);
if(chi2_nn_goe < chi2_nn_gue,
  print("  P(s): favors GOE/SO(even) -- expected for CM newform, epsilon=+1, low zeros")
);
if(chi2_nn_goe >= chi2_nn_gue,
  print("  P(s): favors GUE")
);
if(N_zeros >= 150,
  printf("  PAPER-GRADE: %d >= 150 zeros; pair correlation statistics reliable.\n", N_zeros)
);
if(N_zeros < 150,
  printf("  CAUTION: %d < 150 zeros\n", N_zeros)
);
print("");
print("References:");
print("  Montgomery (1973) Proc. Symp. Pure Math. 24");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Hamieh-Wong arXiv:2412.03034");
print("  Shin-Templier arXiv:1208.1945");
print("  Mehta: Random Matrices, 3rd ed.");
print("  LMFDB 4.5.b.a: lmfdb.org/ModularForm/GL2/Q/holomorphic/4/5/b/a/");
print("====================================================");
print("r_1_test_T200.gp v3 COMPLETE");
print("====================================================");
