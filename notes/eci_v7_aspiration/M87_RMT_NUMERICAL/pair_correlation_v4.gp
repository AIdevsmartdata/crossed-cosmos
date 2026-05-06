\\ ============================================================
\\ pair_correlation_v4.gp
\\ M94 — Fixed version of M92 pair_correlation_v3.gp
\\ PARI/GP 2.11+
\\
\\ Usage: run AFTER r_1_test_v4.gp has produced a log file.
\\
\\ TWO MODES:
\\   Mode A (standalone): re-computes zeros internally (no log file needed)
\\   Mode B (from log):   reads GAP lines from r_1_test_v4.log
\\
\\ Default: Mode A (standalone), self-contained.
\\ To use Mode B: set READ_FROM_LOG = 1 and set LOG_FILE below.
\\ ============================================================
\\
\\ FIX SUMMARY (M94, 2026-05-06):
\\
\\ BUG 1 (lfuninit t_VEC error):
\\   CAUSE: lfuninit(f, [50]) in do_mode_a() — same as r_1_test_v3 Bug 1.
\\   FIX:   ldata = lfunmf(mf, f); lf = lfuninit(ldata, [50]);
\\
\\ BUG 2 (vector multi-line syntax error):
\\   CAUSE: three vector(N, j, expr) calls in do_mode_a() and in the
\\          gue_nn_expected/goe_nn_expected assignments were split across lines.
\\   FIX:   All vector() calls collapsed to single lines.
\\          Inside do_mode_a() the ng = vector(...) was already inside {braces}
\\          so technically valid, but collapsed to single line for safety and
\\          consistency.
\\
\\ PAIR CORRELATION THEORY (Montgomery 1973, GUE prediction):
\\ For large T, pairs (gamma_m, gamma_n) with gamma_m != gamma_n:
\\   R_2(r) = 1 - (sin(Pi*r)/(Pi*r))^2        [GUE pair correlation]
\\   Integrated: p_pair(r) = r - sin(2*Pi*r)/(2*Pi)  on [0,r]
\\
\\ For SO(even) FAMILIES (Katz-Sarnak):
\\   R_2^{SO}(r) adds a correction term involving cos(2*Pi*r)*J_0(2*Pi*r)
\\   For a SINGLE L-function at large height, GUE dominates.
\\
\\ Chi^2 test: bin R_2(r) in bins [0, 0.1, 0.2, ..., 5.0]
\\   chi2 = sum_bins (observed - expected)^2 / expected
\\   threshold chi2 > 2*(N_bins-1) flags systematic GUE deviation
\\ ============================================================

default(parisize, 128000000);
default(realbitprecision, 64);

\\ ----------------------------------------------------------
\\ CONFIGURATION
\\ ----------------------------------------------------------
READ_FROM_LOG = 0;       \\ Set to 1 to read from log file (Mode B)
LOG_FILE = "r_1_test_v4.log";  \\ Only used if READ_FROM_LOG = 1

R_MAX = 5.0;
BIN_WIDTH = 0.1;
N_BINS = round(R_MAX / BIN_WIDTH);  \\ = 50

\\ Chi^2 threshold: conservative 2*(N_BINS-1)
CHI2_THRESHOLD = 2 * (N_BINS - 1);  \\ = 98

print("====================================================");
print("M87/M94 -- Pair Correlation R_2(r) for L(4.5.b.a, s)");
print("====================================================");
print("  Bins: [0, ", R_MAX, "] width ", BIN_WIDTH, " => ", N_BINS, " bins");
print("  Chi^2 threshold: ", CHI2_THRESHOLD, " (conservative 2*(N_bins-1))");
print("");

\\ ----------------------------------------------------------
\\ Global: analytic conductor and mean spacing
\\ ----------------------------------------------------------
q_an_val = 4 * (5 / (2*Pi))^2;
Delta_local(T) = 2*Pi / log(q_an_val * T / (2*Pi));

\\ GUE pair correlation density: R_2(r) = 1 - (sin(Pi*r)/(Pi*r))^2
\\ R_2(0) = 0 by convention (avoids 0/0)
R2_GUE(r) = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);

\\ Wigner surmise distributions
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

\\ ----------------------------------------------------------
\\ MODE A: compute zeros from scratch, return norm_gaps vector
\\ ----------------------------------------------------------
do_mode_a() = {
  my(mf, F, f, coefs, a2c, ldata, lf, zeros, N_zeros, ng);
  print("Step 1 (Mode A): Recomputing zeros of L(4.5.b.a, s)...");

  mf = mfinit([4, 5, Mod(3,4)], 1);

  \\ mfeigenbasis returns t_VEC eigenform objects
  F = mfeigenbasis(mf);
  if(#F == 0, error("No newforms found."));
  f = F[1];

  \\ Verify a_2 = -4
  coefs = mfcoefs(f, 6);
  a2c = coefs[3];
  if(a2c != -4, error("a_2 mismatch in pair_correlation_v4: got ", a2c, " expected -4"));
  print("  a_2 = -4 confirmed.");

  \\ M94 FIX (Bug 1): use lfunmf(mf, f) to get L-data object first.
  ldata = lfunmf(mf, f);
  lf = lfuninit(ldata, [50]);
  zeros = lfunzeros(lf, [0, 50]);
  print("  Zeros computed: ", #zeros);

  N_zeros = #zeros;
  if(N_zeros < 2, error("Fewer than 2 zeros returned by lfunzeros."));

  \\ M94 FIX (Bug 2): single-line vector() call (was split across 3 lines in v3)
  ng = vector(N_zeros - 1, j, (zeros[j+1] - zeros[j]) / Delta_local((zeros[j] + zeros[j+1]) / 2));
  print("  Normalized gaps computed: ", #ng);
  ng;  \\ return value
}

\\ ----------------------------------------------------------
\\ MODE B: read GAP lines from log file, return norm_gaps vector
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
      if(#vals >= 3,
        vf = eval(vals[3]);
        ng = concat(ng, [vf])
      )
    );
    line = fileread(fid)
  );
  fileclose(fid);
  print("  Read ", #ng, " normalized gaps from log.");
  ng;  \\ return value
}

\\ ----------------------------------------------------------
\\ STEP 1: Dispatch to appropriate mode
\\ ----------------------------------------------------------
norm_gaps = if(READ_FROM_LOG == 0, do_mode_a(), do_mode_b(LOG_FILE));

N_gaps = #norm_gaps;
if(N_gaps < 20, print("WARNING: only ", N_gaps, " gaps; pair correlation may be unreliable."));

\\ ----------------------------------------------------------
\\ STEP 2: Pair correlation histogram — all pairs within window W
\\ ----------------------------------------------------------
print("");
print("Step 2: Building pair correlation histogram...");

hist = vector(N_BINS, k, 0);
W = R_MAX;
N_pairs_counted = 0;

for(i = 1, N_gaps,
  my(s_cumul, bin_idx);
  s_cumul = 0;
  for(j = i, N_gaps,
    s_cumul += norm_gaps[j];
    if(s_cumul > W, break());
    bin_idx = floor(s_cumul / BIN_WIDTH) + 1;
    if(bin_idx >= 1 && bin_idx <= N_BINS,
      hist[bin_idx]++;
      N_pairs_counted++
    )
  )
);

print("  Total pairs counted: ", N_pairs_counted);

\\ ----------------------------------------------------------
\\ STEP 3: GUE prediction per bin
\\ ----------------------------------------------------------
gue_unnorm = sum(k = 1, N_BINS, R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);
gue_analytic_integral = R_MAX - sin(2*Pi*R_MAX)/(2*Pi);
print("  GUE integral [0,", R_MAX, "]: ", gue_analytic_integral, "  (numerical: ", gue_unnorm, ")");

if(gue_unnorm < 1e-10, error("GUE normalization near zero"));
norm_factor = N_pairs_counted / gue_unnorm;
gue_expected = vector(N_BINS, k, norm_factor * R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);

\\ ----------------------------------------------------------
\\ STEP 4: Chi^2 statistic vs GUE pair correlation
\\ ----------------------------------------------------------
print("");
print("Step 4: Chi^2 test vs GUE...");

chi2 = 0.0;
chi2_dof = 0;
for(k = 1, N_BINS,
  if(gue_expected[k] >= 5,
    chi2 += (hist[k] - gue_expected[k])^2 / gue_expected[k];
    chi2_dof++
  )
);
chi2_dof_reduced = chi2_dof - 1;

print("  Chi^2 = ", chi2, "  with ", chi2_dof_reduced, " effective dof");
print("  Threshold: ", CHI2_THRESHOLD);

if(chi2 > CHI2_THRESHOLD,
  print("  WARNING: chi^2 = ", chi2, " > ", CHI2_THRESHOLD);
  print("  Systematic deviation from GUE detected.");
  print("  ACTION: Increase N_zeros (extend to T=200), recheck normalization."),
  print("  PASS: chi^2 = ", chi2, " <= ", CHI2_THRESHOLD, " (consistent with GUE)")
);

\\ ----------------------------------------------------------
\\ STEP 5: Nearest-neighbor spacing distribution p(s)
\\ ----------------------------------------------------------
\\
\\ CORRECT Wigner surmise (Mehta, Random Matrices 3rd ed., eqs. 6.2.13-6.2.15):
\\   GOE (beta=1): p(s) = (Pi/2)*s*exp(-Pi*s^2/4)
\\   GUE (beta=2): p(s) = (32/Pi^2)*s^2*exp(-4*s^2/Pi)
\\ All have mean = 1 by normalization.
\\ For SO(even) family near central point: GOE-like (beta=1) repulsion
\\ For large heights (single form, Montgomery conjecture): GUE-like (beta=2)

print("");
print("Step 5: Nearest-neighbor spacing distribution p(s)...");

nn_hist = vector(N_BINS, k, 0);
for(j = 1, N_gaps,
  my(s, bin_idx);
  s = norm_gaps[j];
  bin_idx = floor(s / BIN_WIDTH) + 1;
  if(bin_idx >= 1 && bin_idx <= N_BINS, nn_hist[bin_idx]++)
);

\\ Normalize expected counts to N_gaps total
gue_nn_unnorm = sum(k=1, N_BINS, p_GUE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);
goe_nn_unnorm = sum(k=1, N_BINS, p_GOE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);

\\ M94 FIX (Bug 2): these vector() calls were split across 2 lines each in v3.
\\ Collapsed to single lines.
gue_nn_expected = vector(N_BINS, k, N_gaps * p_GUE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH / gue_nn_unnorm);
goe_nn_expected = vector(N_BINS, k, N_gaps * p_GOE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH / goe_nn_unnorm);

chi2_nn_gue = 0.0; chi2_nn_goe = 0.0; nn_dof = 0;
for(k = 1, N_BINS,
  if(gue_nn_expected[k] >= 3,
    chi2_nn_gue += (nn_hist[k] - gue_nn_expected[k])^2 / gue_nn_expected[k];
    chi2_nn_goe += (nn_hist[k] - goe_nn_expected[k])^2 / goe_nn_expected[k];
    nn_dof++
  )
);

print("  NN spacing chi^2 vs GUE: ", chi2_nn_gue, "  (dof~", nn_dof-1, ")");
print("  NN spacing chi^2 vs GOE: ", chi2_nn_goe, "  (dof~", nn_dof-1, ")");

if(chi2_nn_goe < chi2_nn_gue,
  print("  NOTE: p(s) CLOSER TO GOE than GUE (ratio = ", chi2_nn_goe/chi2_nn_gue, ")");
  print("  This is CONSISTENT with SO(even) family prediction near central point."),
  print("  NOTE: p(s) closer to GUE (ratio chi2_goe/chi2_gue = ", chi2_nn_goe/chi2_nn_gue, ")")
);

\\ ----------------------------------------------------------
\\ STEP 6: Histogram output (for external plotting)
\\ ----------------------------------------------------------
print("");
print("Step 6: Full histogram output...");
print("FORMAT: BIN center  observed  GUE_pair_expected  GUE_nn_expected  GOE_nn_expected");
for(k = 1, N_BINS,
  my(r_center);
  r_center = (k - 0.5) * BIN_WIDTH;
  printf("BIN %.2f  %d  %.4f  %.4f  %.4f\n", r_center, hist[k], gue_expected[k], gue_nn_expected[k], goe_nn_expected[k])
);

\\ ----------------------------------------------------------
\\ STEP 7: Summary verdict
\\ ----------------------------------------------------------
print("");
print("====================================================");
print("PAIR CORRELATION SUMMARY");
print("====================================================");
printf("  Chi^2 (pair corr vs GUE):    %.2f  (threshold: %d)\n", chi2, CHI2_THRESHOLD);
printf("  Chi^2 (NN spacing vs GUE):   %.2f\n", chi2_nn_gue);
printf("  Chi^2 (NN spacing vs GOE):   %.2f\n", chi2_nn_goe);

if(chi2 > CHI2_THRESHOLD,
  print("  OVERALL: WARNING -- pair correlation deviates from GUE");
  print("  Possible sources: (1) too few zeros; (2) CM arithmetic anomaly");
  print("  Recommended: extend to T=200 (N~150 zeros) before claiming anomaly"),
  print("  OVERALL: CONSISTENT WITH GUE pair correlation")
);

if(chi2_nn_goe < chi2_nn_gue,
  print("  NN spacing: closer to GOE/SO(even) -- EXPECTED for low-lying zeros"),
  print("  NN spacing: closer to GUE -- EXPECTED for large-height zeros")
);

print("");
print("References:");
print("  Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("  Montgomery (1973) pair correlation conjecture");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Shin-Templier arXiv:1208.1945 (Frobenius-Schur indicator)");
print("====================================================");
print("pair_correlation_v4.gp COMPLETE");
print("====================================================");
