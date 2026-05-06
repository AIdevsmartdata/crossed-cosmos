\\ ============================================================
\\ r_1_test_T200.gp
\\ M98 — Paper-grade RMT statistics for L(4.5.b.a, s)
\\ T=200, ~150 zeros, pair correlation + chi^2 vs GUE
\\ Built on M94 v4 verified fixes (lfunmf + single-line vector)
\\ PARI/GP 2.11+
\\ Run:
\\   /home/remondiere/miniforge3/envs/sage/bin/gp -q < r_1_test_T200.gp 2>&1 | tee r_1_test_T200.log
\\ Estimated runtime: 5-20 min (T=200; if slow, reduce to T=100 first)
\\ ============================================================
\\
\\ MATHEMATICAL CONTEXT:
\\ f = 4.5.b.a : Gamma_0(4), wt=5, chi=chi_4 (chi(3)=-1)
\\ Unique newform; CM type; LMFDB label 4.5.b.a; analytic rank = 0
\\ Sato-Tate group: U(1)[D_2] (CM form)
\\ Epsilon (root number): +1
\\ LMFDB verified (M81): a_2=-4, a_5=-14
\\
\\ RMT HYPOTHESIS D4-#2 (M81, M87, M92, M94):
\\ CM newforms are conjectured to have SO(even) symmetry type
\\ (Katz-Sarnak 1999; Shin-Templier arXiv:1208.1945).
\\ Question: do the ~150 low-lying zeros of L(4.5.b.a,s) up to T=200
\\ show GUE pair correlation (as individual L-function zeros must at
\\ large height, Montgomery 1973) or anomalous clustering
\\ consistent with CM arithmetic structure?
\\
\\ r_1 ANOMALY CRITERION (Hamieh-Wong arXiv:2412.03034 inspired):
\\   r_1 in [0.5, 2.0] => normal, GUE/SO(even)
\\   r_1 > 2.5        => anomalous => NEW (Exp.Math. letter potential)
\\   Full chi^2 vs GUE (pair correlation) at >=150 zeros => paper-grade
\\
\\ ANALYTIC CONDUCTOR:
\\   q_an = N * (k/(2*Pi))^2 = 4 * (5/(2*Pi))^2 = 25/Pi^2 ~ 2.5331
\\   Mean spacing at height T:
\\   Delta(T) = 2*Pi / log(q_an * T / (2*Pi))
\\
\\ MEMORY NOTE:
\\   parisize 1GB set below.  If PARI aborts on your machine, reduce
\\   to 512000000 (512 MB) and try T=150 first.
\\ ============================================================

default(parisize, 1024000000);   \\ 1 GB as per M98 spec
default(realbitprecision, 64);   \\ ~19 decimal digits, sufficient for T=200 zeros

\\ ---- Wall-clock timing ----
time_start = getwalltime();

print("====================================================");
print("M98 -- L(4.5.b.a, s) zeros up to T=200");
print("Paper-grade RMT statistics: r_1, pair correlation, chi^2");
print("Built on M94 v4 (lfunmf fix + single-line vector fix)");
print("ECI project -- Kevin Remondiere, 2026-05-06");
print("====================================================");
print("");

\\ ============================================================
\\ GLOBAL HELPERS
\\ ============================================================

\\ Analytic conductor (verified M81 from LMFDB):  N=4, k=5
q_an_val = 4 * (5 / (2*Pi))^2;  \\ = 25/Pi^2

\\ Local mean spacing at height T (GUE prediction)
Delta_local(T) = 2*Pi / log(q_an_val * T / (2*Pi));

\\ GUE pair correlation density: R_2(r) = 1 - (sin(Pi*r)/(Pi*r))^2
R2_GUE(r) = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);

\\ Wigner surmise distributions (Mehta, Random Matrices 3rd ed.)
\\ GOE (beta=1): p(s) = (Pi/2)*s*exp(-Pi*s^2/4)   mean=1
\\ GUE (beta=2): p(s) = (32/Pi^2)*s^2*exp(-4*s^2/Pi) mean=1
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

\\ Pair correlation histogram parameters
R_MAX = 5.0;
BIN_WIDTH = 0.1;
N_BINS = round(R_MAX / BIN_WIDTH);  \\ 50
CHI2_THRESHOLD = 2 * (N_BINS - 1);  \\ 98 (conservative)

\\ ============================================================
\\ STEP 1: Build modular form space + verify coefficients
\\ ============================================================

print("Step 1: Initializing modular form space [4, 5, Mod(3,4)]...");
mf = mfinit([4, 5, Mod(3,4)], 1);
F = mfeigenbasis(mf);

if(#F == 0, error("No newforms found -- verify mfinit([4,5,Mod(3,4)],1) on this PARI version"));
print("  Newforms found: ", #F, "  (expected: 1 for 4.5.b.a unique)");
if(#F > 1, print("  WARNING: multiple newforms; using first.  Check LMFDB label matches."));

f = F[1];

\\ Coefficient verification (LMFDB live-verified by M81, 2026-05-06)
coefs = mfcoefs(f, 6);
a2_got = coefs[3];
a5_got = coefs[6];

print("  a_2 = ", a2_got, "  (LMFDB: -4)");
print("  a_5 = ", a5_got, "  (LMFDB: -14)");

if(a2_got != -4,
  error("a_2 MISMATCH: got ", a2_got, " expected -4.  HALTING.  Wrong newform or PARI issue.")
);
if(a5_got != -14,
  error("a_5 MISMATCH: got ", a5_got, " expected -14.  HALTING.")
);
print("  Coefficient verification: PASS");
print("");

\\ ============================================================
\\ STEP 2: Construct L-function and compute zeros to T=200
\\ (M94 fix: lfunmf(mf, f) before lfuninit)
\\ ============================================================

T_MAX = 200;

print("Step 2: Building L-function object and computing zeros up to T=", T_MAX, "...");
print("  (This may take 5-20 min; parisize=1GB)");
print("  Time elapsed so far: ", (getwalltime() - time_start)/1000, " sec");

\\ M94 Bug 1 fix: must use lfunmf(mf, f) to get L-data object
ldata = lfunmf(mf, f);
lf = lfuninit(ldata, [T_MAX]);

print("  lfuninit DONE.  Time: ", (getwalltime() - time_start)/1000, " sec");

zeros = lfunzeros(lf, [0, T_MAX]);
N_zeros = #zeros;

print("  lfunzeros DONE.  Time: ", (getwalltime() - time_start)/1000, " sec");
print("  Number of zeros found: ", N_zeros, "  (expected: ~150 by Weyl law)");

\\ Weyl law check: N(T) ~ (T/(2*Pi)) * log(q_an_val*T/(2*Pi)) - T/(2*Pi)
weyl_est = (T_MAX/(2*Pi)) * log(q_an_val * T_MAX / (2*Pi)) - T_MAX/(2*Pi);
print("  Weyl law estimate N(", T_MAX, ") ~ ", round(weyl_est));

if(N_zeros < 50,
  print("  WARNING: fewer than 50 zeros. Statistics unreliable. Increase T or parisize.");
  print("  [TBD: increase parisize to 2GB or 4GB and retry with T=200]")
);
if(N_zeros >= 50 && N_zeros < 150,
  print("  NOTE: ", N_zeros, " zeros found. >=50 is minimally useful; >=150 preferred for paper-grade.")
);
if(N_zeros >= 150,
  print("  PAPER-GRADE: ", N_zeros, " >= 150 zeros. Pair correlation statistics are reliable.")
);

print("");

\\ ============================================================
\\ STEP 3: Normalized gaps r_n
\\ (M94 fix: vector() on single line)
\\ ============================================================

print("Step 3: Computing normalized gaps r_n = (gamma_{n+1} - gamma_n) / Delta_local...");

if(N_zeros < 2, error("Fewer than 2 zeros -- cannot compute gaps."));

\\ M94 Bug 2 fix: single-line vector() call
norm_gaps = vector(N_zeros - 1, j, (zeros[j+1] - zeros[j]) / Delta_local((zeros[j] + zeros[j+1]) / 2));

N_gaps = #norm_gaps;
print("  Computed ", N_gaps, " normalized gaps.");
print("");

\\ ============================================================
\\ STEP 4: Basic gap statistics
\\ ============================================================

print("Step 4: Gap statistics...");

r1 = norm_gaps[1];
r_mean = sum(j = 1, N_gaps, norm_gaps[j]) / N_gaps;
r_max  = vecmax(norm_gaps);
r_min  = vecmin(norm_gaps);
r_mean_dev = abs(r_mean - 1.0);

\\ Variance: Var(r) = E[r^2] - (E[r])^2
r_mean_sq = sum(j=1, N_gaps, norm_gaps[j]^2) / N_gaps;
r_var = r_mean_sq - r_mean^2;
r_std = sqrt(r_var);

\\ GUE theoretical variance for NNS: Var_GUE ~ 0.286 (Mehta, Table A.7)
\\ (This is for unbounded range; finite-T correction applies)

print("  N_gaps:                      ", N_gaps);
printf("  r_1 (first normalized gap):  %.8f\n", r1);
printf("  mean(r_n):                   %.8f   [GUE expect: ~1.000]\n", r_mean);
printf("  std(r_n):                    %.8f   [GUE expect: ~0.53 for NNS]\n", r_std);
printf("  var(r_n):                    %.8f\n", r_var);
printf("  max(r_n):                    %.8f\n", r_max);
printf("  min(r_n):                    %.8f\n", r_min);
printf("  |mean - 1|:                  %.8f   [warn if > 0.15]\n", r_mean_dev);
print("");

\\ ============================================================
\\ STEP 5: r_1 anomaly verdict
\\ ============================================================

print("Step 5: r_1 anomaly verdict...");

if(r1 >= 0.5 && r1 <= 2.0,
  printf("  r_1 VERDICT: PASS -- r_1 = %.6f in [0.5, 2.0] (normal GUE/SO(even))\n", r1),
  if(r1 > 2.5,
    printf("  r_1 VERDICT: ANOMALY -- r_1 = %.6f > 2.5\n", r1);
    print("  ACTION: NEW Exp.Math. letter potential.");
    print("  Cross-cite: Hamieh-Wong arXiv:2412.03034 (CM arithmetic effect)");
    print("  Verify: does anomaly persist for T=500, T=1000?"),
    printf("  r_1 VERDICT: BORDERLINE -- r_1 = %.6f in (2.0, 2.5]\n", r1);
    print("  ACTION: need T=500 to resolve; run pair_correlation chi^2 now.")
  )
);

if(r_mean_dev > 0.15,
  printf("  MEAN VERDICT: WARNING -- |mean-1| = %.6f > 0.15\n", r_mean_dev),
  printf("  MEAN VERDICT: OK -- |mean-1| = %.6f <= 0.15\n", r_mean_dev)
);
print("");

\\ ============================================================
\\ STEP 6: Pair correlation histogram (Montgomery R_2)
\\ ============================================================

print("Step 6: Pair correlation histogram (all pairs, window W=5.0)...");

hist_pair = vector(N_BINS, k, 0);
N_pairs_counted = 0;

for(i = 1, N_gaps,
  my(s_cumul, bin_idx);
  s_cumul = 0;
  for(j = i, N_gaps,
    s_cumul += norm_gaps[j];
    if(s_cumul > R_MAX, break());
    bin_idx = floor(s_cumul / BIN_WIDTH) + 1;
    if(bin_idx >= 1 && bin_idx <= N_BINS,
      hist_pair[bin_idx]++;
      N_pairs_counted++
    )
  )
);

print("  Total pairs counted: ", N_pairs_counted);

\\ GUE normalization
gue_unnorm = sum(k = 1, N_BINS, R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);
gue_analytic_integral = R_MAX - sin(2*Pi*R_MAX)/(2*Pi);
printf("  GUE integral [0,%g]: analytic=%.6f  numerical=%.6f\n", R_MAX, gue_analytic_integral, gue_unnorm);

if(gue_unnorm < 1e-10, error("GUE normalization near zero -- check BIN_WIDTH and R_MAX"));
norm_factor_pair = N_pairs_counted / gue_unnorm;
gue_expected_pair = vector(N_BINS, k, norm_factor_pair * R2_GUE((k - 0.5) * BIN_WIDTH) * BIN_WIDTH);
print("");

\\ ============================================================
\\ STEP 7: Chi^2 test vs GUE (pair correlation)
\\ ============================================================

print("Step 7: Chi^2 test (pair correlation vs GUE)...");

chi2_pair = 0.0;
chi2_pair_dof = 0;
for(k = 1, N_BINS,
  if(gue_expected_pair[k] >= 5,
    chi2_pair += (hist_pair[k] - gue_expected_pair[k])^2 / gue_expected_pair[k];
    chi2_pair_dof++
  )
);
chi2_pair_dof_reduced = chi2_pair_dof - 1;

printf("  Pair corr chi^2 = %.4f  with %d effective dof\n", chi2_pair, chi2_pair_dof_reduced);
printf("  Conservative threshold: %d  (2*(N_bins-1))\n", CHI2_THRESHOLD);

if(chi2_pair > CHI2_THRESHOLD,
  printf("  PAIR CORR: WARNING chi^2=%.2f > %d (GUE DEVIATION)\n", chi2_pair, CHI2_THRESHOLD),
  printf("  PAIR CORR: PASS chi^2=%.2f <= %d (consistent with GUE)\n", chi2_pair, CHI2_THRESHOLD)
);
print("");

\\ ============================================================
\\ STEP 8: Nearest-neighbor spacing distribution P(s)
\\ ============================================================

print("Step 8: Nearest-neighbor spacing distribution P(s) vs GUE/GOE...");

nn_hist = vector(N_BINS, k, 0);
for(j = 1, N_gaps,
  my(bin_idx);
  bin_idx = floor(norm_gaps[j] / BIN_WIDTH) + 1;
  if(bin_idx >= 1 && bin_idx <= N_BINS, nn_hist[bin_idx]++)
);

gue_nn_unnorm = sum(k=1, N_BINS, p_GUE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);
goe_nn_unnorm = sum(k=1, N_BINS, p_GOE_wigner((k-0.5)*BIN_WIDTH) * BIN_WIDTH);

\\ M94 single-line vector() fix applied here:
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

printf("  NN spacing chi^2 vs GUE: %.4f  (dof~%d)\n", chi2_nn_gue, nn_dof-1);
printf("  NN spacing chi^2 vs GOE: %.4f  (dof~%d)\n", chi2_nn_goe, nn_dof-1);

if(chi2_nn_goe < chi2_nn_gue,
  printf("  NOTE: P(s) CLOSER TO GOE (beta=1, SO(even)). Ratio=%.4f\n", chi2_nn_goe/chi2_nn_gue);
  print("  INTERPRETATION: consistent with SO(even) family prediction for CM newform."),
  printf("  NOTE: P(s) closer to GUE. Ratio chi2_goe/chi2_gue=%.4f\n", chi2_nn_goe/chi2_nn_gue);
  print("  INTERPRETATION: large-height GUE dominance taking over.")
);
print("");

\\ ============================================================
\\ STEP 9: Full histogram output (machine-readable for CSV/plotting)
\\ ============================================================

print("Step 9: Full histogram tables...");
print("FORMAT: BIN r_center  pair_obs  GUE_pair_exp  nn_obs  GUE_nn_exp  GOE_nn_exp");
for(k = 1, N_BINS,
  my(rc);
  rc = (k - 0.5) * BIN_WIDTH;
  printf("BIN %.2f  %d  %.4f  %d  %.4f  %.4f\n",
    rc, hist_pair[k], gue_expected_pair[k], nn_hist[k], gue_nn_expected[k], goe_nn_expected[k])
);

\\ ============================================================
\\ STEP 10: Export raw zeros (for zeros_T200.csv)
\\ ============================================================

print("");
print("Step 10: Raw zeros export (gamma_n values)...");
print("CSV_HEADER: n,gamma_n,norm_gap_to_next");

for(j = 1, N_zeros - 1,
  printf("CSV %d,%.12f,%.8f\n", j, zeros[j], norm_gaps[j])
);
printf("CSV %d,%.12f,NA\n", N_zeros, zeros[N_zeros]);

\\ ============================================================
\\ STEP 11: Summary verdict (paper-grade)
\\ ============================================================

time_total = (getwalltime() - time_start)/1000;

print("");
print("====================================================");
print("M98 FINAL SUMMARY -- Paper-grade RMT statistics");
print("====================================================");
printf("  Form:              4.5.b.a  (Gamma_0(4), wt=5, chi_4, CM)\n");
printf("  T_max:             %d\n", T_MAX);
printf("  N_zeros:           %d  (Weyl ~ %d)\n", N_zeros, round(weyl_est));
printf("  N_gaps:            %d\n", N_gaps);
printf("  q_an (analytic):   %.6f  (= 25/Pi^2)\n", q_an_val);
printf("  \n");
printf("  r_1:               %.8f\n", r1);
printf("  mean(r_n):         %.8f  [GUE: 1.0]\n", r_mean);
printf("  std(r_n):          %.8f\n", r_std);
printf("  max(r_n):          %.8f\n", r_max);
printf("  min(r_n):          %.8f\n", r_min);
printf("  \n");
printf("  chi^2 pair corr vs GUE:  %.4f / %d dof\n", chi2_pair, chi2_pair_dof_reduced);
printf("  chi^2 NN vs GUE:         %.4f / %d dof\n", chi2_nn_gue, nn_dof-1);
printf("  chi^2 NN vs GOE:         %.4f / %d dof\n", chi2_nn_goe, nn_dof-1);
printf("  \n");
printf("  Wall-clock time: %.1f sec\n", time_total);

\\ Final verdict
print("");
print("VERDICT:");

if(r1 > 2.5,
  printf("  r_1 = %.6f ANOMALOUS (>2.5) => ALERT: NEW Exp.Math potential\n", r1)
);
if(r1 >= 0.5 && r1 <= 2.0,
  printf("  r_1 = %.6f NORMAL [0.5, 2.0]\n", r1)
);
if(r1 > 2.0 && r1 <= 2.5,
  printf("  r_1 = %.6f BORDERLINE (2.0, 2.5] -- needs T=500\n", r1)
);

if(chi2_pair > CHI2_THRESHOLD,
  printf("  Pair corr chi^2=%.2f DEVIATES from GUE => ALERT: NEW if confirmed\n", chi2_pair),
  printf("  Pair corr chi^2=%.2f consistent with GUE\n", chi2_pair)
);

if(chi2_nn_goe < chi2_nn_gue,
  print("  NN spacing: favors GOE/SO(even) (EXPECTED: CM form, epsilon=+1, low zeros)"),
  print("  NN spacing: favors GUE (expected at large height)")
);

if(N_zeros < 50,
  print("  CAUTION: statistics based on N < 50 zeros -- unreliable, extend to T=300+")
);
if(N_zeros >= 50 && N_zeros < 150,
  printf("  CAUTION: %d zeros found (< 150 target). Statistics marginally reliable.\n", N_zeros);
  print("  [TBD if N<150: increase parisize to 2GB and retry, or extend T to 300]")
);
if(N_zeros >= 150,
  printf("  CONFIRMED PAPER-GRADE: %d zeros, pair correlation statistics reliable.\n", N_zeros)
);

print("");
print("References:");
print("  Montgomery (1973) pair correlation conjecture");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("  Shin-Templier arXiv:1208.1945 (Frobenius-Schur, symplectic CM)");
print("  Mehta: Random Matrices, 3rd ed. (Wigner surmise, chi^2 tests)");
print("  LMFDB 4.5.b.a: https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/4/5/b/a/");
print("====================================================");
print("r_1_test_T200.gp COMPLETE");
print("====================================================");
