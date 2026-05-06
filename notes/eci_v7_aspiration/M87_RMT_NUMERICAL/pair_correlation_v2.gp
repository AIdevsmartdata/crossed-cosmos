\\ ============================================================
\\ pair_correlation_v2.gp
\\ M87 — RMT x ECI: Pair correlation R_2(r) for L(4.5.b.a,s)
\\ PARI/GP 2.11+
\\
\\ Usage: Run AFTER r_1_test_v2.gp has produced a log file.
\\
\\ TWO MODES:
\\   Mode A (standalone): re-computes zeros internally (no log file needed)
\\   Mode B (from log):   reads GAP lines from r_1_test_v2.log
\\
\\ Default: Mode A (standalone), self-contained.
\\ To use Mode B: set READ_FROM_LOG = 1 and set LOG_FILE below.
\\ ============================================================
\\
\\ PAIR CORRELATION THEORY (Montgomery 1973, GUE prediction):
\\ For large T, pairs (gamma_m, gamma_n) with gamma_m != gamma_n:
\\   R_2(r) = 1 - (sin(Pi*r)/(Pi*r))^2      [GUE pair correlation]
\\   Integrated: p_pair(r) = r - sin(2*Pi*r)/(2*Pi)  on [0,r]
\\
\\ For SO(even) FAMILIES (Katz-Sarnak):
\\   R_2^{SO}(r) adds a correction term involving cos(2*Pi*r)*J_0(2*Pi*r)
\\   For a SINGLE L-function at large height, GUE dominates.
\\
\\ Chi^2 test: bin R_2(r) in bins [0, 0.1, 0.2, ..., 5.0]
\\   chi2 = sum_bins (observed - expected)^2 / expected
\\   threshold chi2 > 2 * (N_bins - 1) flags systematic GUE deviation
\\ ============================================================

default(parisize, 128000000);
default(realbitprecision, 64);

\\ ----------------------------------------------------------
\\ CONFIGURATION
\\ ----------------------------------------------------------
READ_FROM_LOG = 0;       \\ Set to 1 to read from log file (Mode B)
LOG_FILE = "r_1_test_v2.log";  \\ Only used if READ_FROM_LOG = 1

R_MAX = 5.0;    \\ Maximum normalized separation for histogram
BIN_WIDTH = 0.1;  \\ Histogram bin width
N_BINS = round(R_MAX / BIN_WIDTH);  \\ = 50 bins

\\ Chi^2 threshold: 95th percentile of chi^2(N_BINS-1 = 49 dof) ~ 66.3
\\ Use a more conservative 2*(N_BINS-1) = 98 to avoid false anomaly claims
CHI2_THRESHOLD = 2 * (N_BINS - 1);  \\ = 98

print("====================================================");
print("M87 — Pair Correlation R_2(r) for L(4.5.b.a, s)");
print("====================================================");
print("  Bins: [0, ", R_MAX, "] width ", BIN_WIDTH, " => ", N_BINS, " bins");
print("  Chi^2 threshold: ", CHI2_THRESHOLD, " (conservative 2*(N_bins-1))");
print("");

\\ ----------------------------------------------------------
\\ STEP 1: Obtain normalized gaps
\\ ----------------------------------------------------------

if(READ_FROM_LOG == 0,
  \\ --- Mode A: recompute zeros from scratch ---
  print("Step 1 (Mode A): Recomputing zeros of L(4.5.b.a, s)...");

  mf = mfinit([4, 5, Mod(3,4)], 1);
  F  = mfnewforms(mf);
  if(#F == 0, error("No newforms found."));
  f  = F[1];

  \\ Verify a_2 = -4 again (safety check)
  coefs = mfcoefs(f, 6);
  a2_check = coefs[3];
  if(a2_check != -4,
    error("a_2 mismatch in pair_correlation_v2.gp: got ", a2_check, " expected -4");
  );
  print("  a_2 = -4 confirmed.");

  lf    = lfuninit(f, [50]);
  zeros = lfunzeros(lf, [0, 50]);
  print("  Zeros computed: ", #zeros);

  q_an  = 4 * (5 / (2*Pi))^2;
  Delta(T) = 2*Pi / log(q_an * T / (2*Pi));

  N_zeros = #zeros;
  norm_gaps = vector(N_zeros - 1, j,
    (zeros[j+1] - zeros[j]) / Delta((zeros[j] + zeros[j+1]) / 2)
  );
  print("  Normalized gaps computed: ", #norm_gaps);
  ,

  \\ --- Mode B: read GAP lines from log file ---
  \\ Format expected: "GAP n  value\n"
  print("Step 1 (Mode B): Reading normalized gaps from ", LOG_FILE, " ...");
  norm_gaps = [];
  fid = fileopen(LOG_FILE, "r");
  if(fid == 0, error("Cannot open log file: ", LOG_FILE));
  line = fileread(fid);
  while(line != "",
    if(substr(line, 1, 3) == "GAP",
      \\ parse "GAP n  value"
      parts = strsplit(line, " ");
      \\ parts[3] should be the value (skip empty tokens)
      vals = select(s -> s != "", parts);
      if(#vals >= 3,
        \\ eval() parses the string as a GP expression (handles floats)
        vf = eval(vals[3]);
        norm_gaps = concat(norm_gaps, [vf]);
      );
    );
    line = fileread(fid);
  );
  fileclose(fid);
  print("  Read ", #norm_gaps, " normalized gaps from log.");
);

N_gaps = #norm_gaps;
if(N_gaps < 20,
  print("WARNING: only ", N_gaps, " gaps available; pair correlation may be unreliable.");
  print("  Recommend: extend zeros to height T=200 for robust statistics.");
);

\\ ----------------------------------------------------------
\\ STEP 2: Pair correlation — all pairs (i, j) with i < j
\\ ----------------------------------------------------------
\\ We compute the normalized pairwise separation:
\\   s_{ij} = sum_{n=i}^{j-1} r_n  (sum of gaps between zeros i and j)
\\ This is the correctly normalized pair-correlation variable.
\\
\\ For the pair-correlation HISTOGRAM, we look at all pairs (i,j)
\\ and record s_{ij} = gamma_j - gamma_i / Delta(midpoint_{ij}) ... but
\\ since we only have norm_gaps (not raw zeros), we use:
\\   s_{ij} = sum_{k=i}^{j-1} r_k   (sum of consecutive normalized gaps)
\\ This approximation is standard and exact if Delta were constant.
\\
\\ We restrict to ADJACENT gaps only (j = i+1) for the nearest-neighbor
\\ spacing distribution p(s), which is the most sensitive statistic.
\\ For full pair correlation, we also include all pairs within window W.

print("");
print("Step 2: Building pair correlation histogram...");

\\ Histogram array (1-indexed: bin k covers [(k-1)*BIN_WIDTH, k*BIN_WIDTH))
hist = vector(N_BINS, k, 0);

\\ Count pairs using cumulative normalized separations
\\ For efficiency: use only pairs within window W = R_MAX (normalized)
W = R_MAX;
N_pairs_counted = 0;

for(i = 1, N_gaps,
  s_cumul = 0;
  for(j = i, N_gaps,
    s_cumul += norm_gaps[j];
    if(s_cumul > W, break());  \\ beyond window, skip
    \\ record this pair (i, j+1) with separation s_cumul
    bin_idx = floor(s_cumul / BIN_WIDTH) + 1;
    if(bin_idx >= 1 && bin_idx <= N_BINS,
      hist[bin_idx]++;
      N_pairs_counted++;
    );
  );
);

print("  Total pairs counted: ", N_pairs_counted);

\\ ----------------------------------------------------------
\\ STEP 3: GUE prediction per bin
\\ ----------------------------------------------------------
\\ Pair correlation density: R_2(r) = 1 - (sin(Pi*r)/(Pi*r))^2
\\ Bin k: center r_k = (k - 0.5) * BIN_WIDTH
\\ Expected count in bin k: E_k = N_eff * BIN_WIDTH * R_2(r_k)
\\   where N_eff is an effective normalization
\\   We normalize by the total count so E_k sums to N_pairs_counted.

\\ First compute unnormalized R_2 integral over bins
R2_GUE(r) = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);
gue_unnorm = sum(k = 1, N_BINS, R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);
\\ gue_unnorm ~ integral_0^{R_MAX} R_2(r) dr = R_MAX - sin(2*Pi*R_MAX)/(2*Pi)
\\ (analytic formula for GUE pair correlation integrated)

gue_analytic_integral = R_MAX - sin(2*Pi*R_MAX)/(2*Pi);
print("  GUE integral [0,", R_MAX, "]: ", gue_analytic_integral, "  (numerical: ", gue_unnorm, ")");

\\ Normalization factor
if(gue_unnorm < 1e-10, error("GUE normalization near zero"));
norm_factor = N_pairs_counted / gue_unnorm;
gue_expected = vector(N_BINS, k, norm_factor * R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);

\\ ----------------------------------------------------------
\\ STEP 4: Chi^2 statistic
\\ ----------------------------------------------------------
print("");
print("Step 4: Chi^2 test vs GUE...");

chi2 = 0.0;
chi2_dof = 0;

\\ Only include bins with expected count >= 5 (standard chi^2 validity requirement)
for(k = 1, N_BINS,
  if(gue_expected[k] >= 5,
    chi2 += (hist[k] - gue_expected[k])^2 / gue_expected[k];
    chi2_dof++;
  );
);

chi2_dof_reduced = chi2_dof - 1;  \\ subtract 1 for normalization constraint
print("  Chi^2 = ", chi2, "  with ", chi2_dof_reduced, " effective dof");
print("  Threshold: ", CHI2_THRESHOLD);

if(chi2 > CHI2_THRESHOLD,
  print("  WARNING: chi^2 = ", chi2, " > ", CHI2_THRESHOLD);
  print("  Systematic deviation from GUE detected.");
  print("  ACTION: Increase N_zeros (extend to T=200), recheck normalization.");
  ,
  print("  PASS: chi^2 = ", chi2, " <= ", CHI2_THRESHOLD, " (consistent with GUE)");
);

\\ ----------------------------------------------------------
\\ STEP 5: Nearest-neighbor spacing distribution (p(s))
\\ ----------------------------------------------------------
\\ This is the most sensitive statistic for symmetry type near central point.
\\ p_GUE(s) = (Pi/2)*s*exp(-Pi*s^2/4)   [Wigner surmise for GUE]
\\ p_SO(s)  = (32/Pi^2)*s^2*exp(-4*s^2/Pi)  [Wigner surmise for GOE/SO]
\\ Note: for actual L-function zeros the Wigner surmise is approximate.

print("");
print("Step 5: Nearest-neighbor spacing distribution p(s)...");

\\ CORRECT Wigner surmise (Mehta, Random Matrices 3rd ed., eqs. 6.2.13-6.2.15):
\\   GOE (beta=1): p(s) = (Pi/2)*s*exp(-Pi*s^2/4)
\\   GUE (beta=2): p(s) = (32/Pi^2)*s^2*exp(-4*s^2/Pi)
\\   GSE (beta=4): p(s) = (2^18/(3^6*Pi^3))*s^4*exp(-64*s^2/(9*Pi))
\\ All have mean = 1 by normalization.
\\ For SO(even) family near central point: GOE-like (beta=1) repulsion
\\ For large heights (single form, Montgomery conjecture): GUE-like (beta=2)

\\ Build p(s) histogram from nearest-neighbor gaps only
nn_hist = vector(N_BINS, k, 0);
for(j = 1, N_gaps,
  s = norm_gaps[j];
  bin_idx = floor(s / BIN_WIDTH) + 1;
  if(bin_idx >= 1 && bin_idx <= N_BINS, nn_hist[bin_idx]++);
);

\\ GUE Wigner surmise expected counts
\\ p_GUE(s) = (32/Pi^2)*s^2*exp(-4*s^2/Pi), mean = 1 by construction
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

\\ Normalize: total expected = N_gaps
gue_nn_unnorm = sum(k=1, N_BINS, p_GUE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);
goe_nn_unnorm = sum(k=1, N_BINS, p_GOE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);

gue_nn_expected = vector(N_BINS, k,
  N_gaps * p_GUE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH / gue_nn_unnorm
);
goe_nn_expected = vector(N_BINS, k,
  N_gaps * p_GOE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH / goe_nn_unnorm
);

\\ Chi^2 for nearest-neighbor: GUE vs GOE
chi2_nn_gue = 0.0; chi2_nn_goe = 0.0; nn_dof = 0;
for(k = 1, N_BINS,
  if(gue_nn_expected[k] >= 3,  \\ lower threshold for small N
    chi2_nn_gue += (nn_hist[k] - gue_nn_expected[k])^2 / gue_nn_expected[k];
    chi2_nn_goe += (nn_hist[k] - goe_nn_expected[k])^2 / goe_nn_expected[k];
    nn_dof++;
  );
);

print("  NN spacing chi^2 vs GUE: ", chi2_nn_gue, "  (dof~", nn_dof-1, ")");
print("  NN spacing chi^2 vs GOE: ", chi2_nn_goe, "  (dof~", nn_dof-1, ")");

if(chi2_nn_goe < chi2_nn_gue,
  print("  NOTE: p(s) CLOSER TO GOE than GUE (ratio = ", chi2_nn_goe/chi2_nn_gue, ")");
  print("  This is CONSISTENT with SO(even) family prediction near central point.");
  ,
  print("  NOTE: p(s) closer to GUE (ratio chi2_goe/chi2_gue = ", chi2_nn_goe/chi2_nn_gue, ")");
);

\\ ----------------------------------------------------------
\\ STEP 6: Histogram output (for external plotting)
\\ ----------------------------------------------------------
print("");
print("Step 6: Full histogram output...");
print("FORMAT: BIN center  observed  GUE_pair_expected  GUE_nn_expected  GOE_nn_expected");
for(k = 1, N_BINS,
  r_center = (k - 0.5) * BIN_WIDTH;
  printf("BIN %.2f  %d  %.4f  %.4f  %.4f\n",
    r_center, hist[k], gue_expected[k], gue_nn_expected[k], goe_nn_expected[k]
  );
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
  print("  OVERALL: WARNING — pair correlation deviates from GUE");
  print("  Possible sources: (1) too few zeros; (2) CM arithmetic anomaly");
  print("  Recommended: extend to T=200 (N~150 zeros) before claiming anomaly");
  ,
  print("  OVERALL: CONSISTENT WITH GUE pair correlation");
);

if(chi2_nn_goe < chi2_nn_gue,
  print("  NN spacing: closer to GOE/SO(even) — EXPECTED for low-lying zeros");
  ,
  print("  NN spacing: closer to GUE — EXPECTED for large-height zeros");
);

print("");
print("References:");
print("  Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("  Montgomery (1973) pair correlation conjecture");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Shin-Templier arXiv:1208.1945 (Frobenius-Schur indicator)");
print("====================================================");
print("pair_correlation_v2.gp COMPLETE");
print("====================================================");
