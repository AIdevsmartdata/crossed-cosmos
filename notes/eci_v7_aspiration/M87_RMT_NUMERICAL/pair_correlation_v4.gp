\\ ============================================================
\\ pair_correlation_v4.gp
\\ M94 (iteration 3) -- Fixed version of M92 pair_correlation_v3.gp
\\ PARI/GP 2.11+
\\
\\ CRITICAL PARI BATCH-MODE PARSER RULE (discovered M94):
\\   Any multi-line for(), if(), or vector() at TOP LEVEL (outside a function
\\   or {braced block}) causes the parser to interpret loop indices as
\\   polynomial variables (t_POL) rather than integers. This triggers:
\\     "incorrect type in gtos [integer expected] (t_POL)"
\\   RULE: ALL top-level for/while/if with multi-line bodies MUST be wrapped
\\   in {outer braces} to activate the block parser.
\\   SAFE: for(k=1,N,{body}) -- single-line body or body in {braces}
\\   SAFE: function calls (code inside function def is already in {braces})
\\
\\ Usage: run AFTER r_1_test_v4.gp has produced a log file.
\\ TWO MODES:
\\   Mode A (standalone): re-computes zeros internally
\\   Mode B (from log):   reads GAP lines from r_1_test_v4.log
\\ Default: Mode A. Set READ_FROM_LOG = 1 for Mode B.
\\ ============================================================
\\
\\ FIX SUMMARY (M94, 2026-05-06):
\\ BUG 1: lfuninit(f,[50]) on t_VEC eigenform -> use lfunmf(mf,f) first
\\ BUG 2: ALL multi-line for()/vector()/if() at top-level wrapped in {braces}
\\         or collapsed to single lines or moved into helper functions.
\\ ============================================================

default(parisize, 128000000);
default(realbitprecision, 64);

\\ ----------------------------------------------------------
\\ CONFIGURATION
\\ ----------------------------------------------------------
READ_FROM_LOG = 0;
LOG_FILE = "r_1_test_v4.log";

R_MAX = 5.0;
BIN_WIDTH = 0.1;
N_BINS = round(R_MAX / BIN_WIDTH);
CHI2_THRESHOLD = 2 * (N_BINS - 1);

print("====================================================");
print("M87/M94 -- Pair Correlation R_2(r) for L(4.5.b.a, s)");
print("====================================================");
print("  Bins: [0, ", R_MAX, "] width ", BIN_WIDTH, " => ", N_BINS, " bins");
print("  Chi^2 threshold: ", CHI2_THRESHOLD, " (conservative 2*(N_bins-1))");
print("");

\\ ----------------------------------------------------------
\\ Global functions
\\ ----------------------------------------------------------
q_an_val = 4 * (5 / (2*Pi))^2;
Delta_local(T) = 2*Pi / log(q_an_val * T / (2*Pi));
R2_GUE(r) = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

\\ ----------------------------------------------------------
\\ MODE A: compute zeros, return norm_gaps
\\ All subscript-loop code is inside function {braces} -- safe.
\\ ----------------------------------------------------------
do_mode_a() = {
  my(mf, F, f, coefs, a2c, ldata, lf, zeros, N_zeros, ng);
  print("Step 1 (Mode A): Recomputing zeros of L(4.5.b.a, s)...");
  mf = mfinit([4, 5, Mod(3,4)], 1);
  F = mfeigenbasis(mf);
  if(#F == 0, error("No newforms found."));
  f = F[1];
  coefs = mfcoefs(f, 6);
  a2c = coefs[3];
  if(a2c != -4, error("a_2 mismatch: got ", a2c, " expected -4"));
  print("  a_2 = -4 confirmed.");
  ldata = lfunmf(mf, f);
  lf = lfuninit(ldata, [50]);
  zeros = lfunzeros(lf, [0, 50]);
  N_zeros = #zeros;
  print("  Zeros computed: ", N_zeros);
  if(N_zeros < 2, error("Fewer than 2 zeros returned by lfunzeros."));
  ng = vector(N_zeros - 1, j, (zeros[j+1] - zeros[j]) / Delta_local((zeros[j] + zeros[j+1]) / 2));
  print("  Normalized gaps computed: ", #ng);
  ng;
}

\\ ----------------------------------------------------------
\\ MODE B: read GAP lines from log file
\\ ----------------------------------------------------------
do_mode_b(logfile) = {
  my(ng, fid, line, parts, vals, vf);
  print("Step 1 (Mode B): Reading normalized gaps from ", logfile, " ...");
  ng = [];
  fid = fileopen(logfile, "r");
  if(fid == 0, error("Cannot open log file: ", logfile));
  line = fileread(fid);
  while(line != "",
    if(substr(line, 1, 3) == "GAP",
      parts = strsplit(line, " ");
      vals = select(s -> s != "", parts);
      if(#vals >= 3, vf = eval(vals[3]); ng = concat(ng, [vf]))
    );
    line = fileread(fid)
  );
  fileclose(fid);
  print("  Read ", #ng, " normalized gaps from log.");
  ng;
}

\\ ----------------------------------------------------------
\\ STEP 2 helper: build pair-correlation histogram
\\ Moving the nested for() inside a function avoids top-level parser issues.
\\ ----------------------------------------------------------
build_pair_hist(ng, nb, bw, wmax) = {
  my(h, np, sc, bi);
  h = vector(nb, k, 0);
  np = 0;
  for(i = 1, #ng,
    sc = 0;
    for(j = i, #ng,
      sc += ng[j];
      if(sc > wmax, break());
      bi = floor(sc / bw) + 1;
      if(bi >= 1 && bi <= nb, h[bi]++; np++)
    )
  );
  print("  Total pairs counted: ", np);
  [h, np];
}

\\ ----------------------------------------------------------
\\ STEP 4 helper: chi^2 statistic (pair correlation)
\\ ----------------------------------------------------------
chi2_paircorr(hist, gue_exp, nb) = {
  my(c2, dof);
  c2 = 0.0; dof = 0;
  for(k = 1, nb,
    if(gue_exp[k] >= 5, c2 += (hist[k] - gue_exp[k])^2 / gue_exp[k]; dof++)
  );
  [c2, dof - 1];
}

\\ ----------------------------------------------------------
\\ STEP 5 helper: nearest-neighbor histogram + chi^2
\\ ----------------------------------------------------------
nn_analysis(ng, nb, bw, n_gaps) = {
  my(nnh, gu_u, go_u, gu_e, go_e, c2g, c2o, dof, bi, s);
  nnh = vector(nb, k, 0);
  for(j = 1, n_gaps, bi = floor(ng[j] / bw) + 1; if(bi >= 1 && bi <= nb, nnh[bi]++));
  gu_u = sum(k=1, nb, p_GUE_wigner((k-0.5)*bw) * bw);
  go_u = sum(k=1, nb, p_GOE_wigner((k-0.5)*bw) * bw);
  gu_e = vector(nb, k, n_gaps * p_GUE_wigner((k-0.5)*bw) * bw / gu_u);
  go_e = vector(nb, k, n_gaps * p_GOE_wigner((k-0.5)*bw) * bw / go_u);
  c2g = 0.0; c2o = 0.0; dof = 0;
  for(k = 1, nb,
    if(gu_e[k] >= 3, c2g += (nnh[k] - gu_e[k])^2 / gu_e[k]; c2o += (nnh[k] - go_e[k])^2 / go_e[k]; dof++)
  );
  [nnh, gu_e, go_e, c2g, c2o, dof - 1];
}

\\ ----------------------------------------------------------
\\ STEP 6 helper: print histogram
\\ ----------------------------------------------------------
print_hist(nb, bw, hist, gue_exp, gue_nn, goe_nn) = {
  my(rc);
  for(k = 1, nb,
    rc = (k - 0.5) * bw;
    printf("BIN %.2f  %d  %.4f  %.4f  %.4f\n", rc, hist[k], gue_exp[k], gue_nn[k], goe_nn[k])
  );
}

\\ ----------------------------------------------------------
\\ Verdict helpers: single function call avoids top-level multi-line if()
\\ ----------------------------------------------------------
verdict_chi2_pair(c2, threshold) = {
  if(c2 > threshold,
    print("  WARNING: chi^2 = ", c2, " > ", threshold);
    print("  Systematic deviation from GUE detected.");
    print("  ACTION: Increase N_zeros (extend to T=200), recheck normalization."),
    print("  PASS: chi^2 = ", c2, " <= ", threshold, " (consistent with GUE)")
  );
}

verdict_nn(c2_goe, c2_gue) = {
  my(ratio_safe);
  ratio_safe = if(abs(c2_gue) < 1e-30, 1.0, c2_goe / c2_gue);
  if(c2_goe < c2_gue,
    print("  NOTE: p(s) CLOSER TO GOE than GUE (ratio = ", ratio_safe, ")");
    print("  This is CONSISTENT with SO(even) family prediction near central point."),
    print("  NOTE: p(s) closer to GUE (ratio chi2_goe/chi2_gue = ", ratio_safe, ")")
  );
}

verdict_summary_chi2(c2, threshold) = {
  if(c2 > threshold,
    print("  OVERALL: WARNING -- pair correlation deviates from GUE");
    print("  Possible sources: (1) too few zeros; (2) CM arithmetic anomaly");
    print("  Recommended: extend to T=200 (N~150 zeros) before claiming anomaly"),
    print("  OVERALL: CONSISTENT WITH GUE pair correlation")
  );
}

verdict_summary_nn(c2_goe, c2_gue) = {
  if(c2_goe < c2_gue,
    print("  NN spacing: closer to GOE/SO(even) -- EXPECTED for low-lying zeros"),
    print("  NN spacing: closer to GUE -- EXPECTED for large-height zeros")
  );
}

\\ ===========================================================
\\ MAIN EXECUTION
\\ ===========================================================

\\ Step 1: Get normalized gaps
norm_gaps = if(READ_FROM_LOG == 0, do_mode_a(), do_mode_b(LOG_FILE));
N_gaps = #norm_gaps;
if(N_gaps < 20, print("WARNING: only ", N_gaps, " gaps; pair correlation may be unreliable."));

\\ Step 2: Pair correlation histogram
print("");
print("Step 2: Building pair correlation histogram...");
ph_result = build_pair_hist(norm_gaps, N_BINS, BIN_WIDTH, R_MAX);
hist = ph_result[1];
N_pairs_counted = ph_result[2];

\\ Step 3: GUE prediction
gue_unnorm = sum(k = 1, N_BINS, R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);
gue_analytic_integral = R_MAX - sin(2*Pi*R_MAX)/(2*Pi);
print("  GUE integral [0,", R_MAX, "]: ", gue_analytic_integral, "  (numerical: ", gue_unnorm, ")");
if(gue_unnorm < 1e-10, error("GUE normalization near zero"));
norm_factor = N_pairs_counted / gue_unnorm;
gue_expected = vector(N_BINS, k, norm_factor * R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);

\\ Step 4: Chi^2 vs GUE pair correlation
print("");
print("Step 4: Chi^2 test vs GUE...");
c2_result = chi2_paircorr(hist, gue_expected, N_BINS);
chi2 = c2_result[1];
chi2_dof_reduced = c2_result[2];
print("  Chi^2 = ", chi2, "  with ", chi2_dof_reduced, " effective dof");
print("  Threshold: ", CHI2_THRESHOLD);
verdict_chi2_pair(chi2, CHI2_THRESHOLD);

\\ Step 5: Nearest-neighbor spacing distribution
print("");
print("Step 5: Nearest-neighbor spacing distribution p(s)...");
nn_result = nn_analysis(norm_gaps, N_BINS, BIN_WIDTH, N_gaps);
nn_hist       = nn_result[1];
gue_nn_expected = nn_result[2];
goe_nn_expected = nn_result[3];
chi2_nn_gue   = nn_result[4];
chi2_nn_goe   = nn_result[5];
nn_dof        = nn_result[6];

print("  NN spacing chi^2 vs GUE: ", chi2_nn_gue, "  (dof~", nn_dof, ")");
print("  NN spacing chi^2 vs GOE: ", chi2_nn_goe, "  (dof~", nn_dof, ")");
verdict_nn(chi2_nn_goe, chi2_nn_gue);

\\ Step 6: Histogram output
print("");
print("Step 6: Full histogram output...");
print("FORMAT: BIN center  observed  GUE_pair_expected  GUE_nn_expected  GOE_nn_expected");
print_hist(N_BINS, BIN_WIDTH, hist, gue_expected, gue_nn_expected, goe_nn_expected);

\\ Step 7: Summary verdict
print("");
print("====================================================");
print("PAIR CORRELATION SUMMARY");
print("====================================================");
printf("  Chi^2 (pair corr vs GUE):    %.2f  (threshold: %d)\n", chi2, CHI2_THRESHOLD);
printf("  Chi^2 (NN spacing vs GUE):   %.2f\n", chi2_nn_gue);
printf("  Chi^2 (NN spacing vs GOE):   %.2f\n", chi2_nn_goe);

verdict_summary_chi2(chi2, CHI2_THRESHOLD);
verdict_summary_nn(chi2_nn_goe, chi2_nn_gue);

print("");
print("References:");
print("  Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("  Montgomery (1973) pair correlation conjecture");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Shin-Templier arXiv:1208.1945 (Frobenius-Schur indicator)");
print("====================================================");
print("pair_correlation_v4.gp COMPLETE");
print("====================================================");
