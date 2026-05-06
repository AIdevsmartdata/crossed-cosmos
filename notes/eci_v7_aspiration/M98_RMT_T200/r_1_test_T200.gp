\\ ============================================================
\\ r_1_test_T200.gp  v2
\\ M98 — Paper-grade RMT statistics for L(4.5.b.a, s)
\\ T=200, ~150+ zeros, pair correlation + chi^2 vs GUE
\\ Built on M94 v4 verified fixes (lfunmf + single-line vector)
\\ PARI/GP 2.11+  (tested on 2.17.3)
\\
\\ v2 FIXES vs v1:
\\  - Replace `&&` in top-level if() conditions with nested if()
\\    (PARI batch mode: `&&` inside if() at top-level causes t_POL parse)
\\  - Wrap all complex for-loops in {braces} to fix subscript issues
\\  - Add {braces} around multi-statement for-loop bodies
\\ ============================================================
\\
\\ MATHEMATICAL CONTEXT:
\\ f = 4.5.b.a : Gamma_0(4), wt=5, chi=chi_4, CM newform, epsilon=+1
\\ Analytic rank = 0; Sato-Tate U(1)[D_2]; LMFDB verified a_2=-4, a_5=-14
\\ Analytic conductor: q_an = 4*(5/(2*Pi))^2 = 25/Pi^2 ~ 2.5331
\\ Mean spacing at height T: Delta(T) = 2*Pi / log(q_an*T/(2*Pi))
\\ Normalized gap: r_n = (gamma_{n+1}-gamma_n) / Delta((gamma_n+gamma_{n+1})/2)
\\
\\ RMT HYPOTHESIS D4-#2 (M81,M87,M92,M94,M98):
\\ Does the zero statistics follow GUE (individual L-function, large T)
\\ or show CM arithmetic anomaly (r_1 > 2.5 anomaly criterion)?
\\ ============================================================

default(parisize, 1024000000);
default(realbitprecision, 64);

time_start = getwalltime();

print("====================================================");
print("M98 v2 -- L(4.5.b.a,s) zeros T=200, paper-grade RMT");
print("ECI project -- Kevin Remondiere, 2026-05-06");
print("====================================================");
print("");

\\ ============================================================
\\ Global helpers
\\ ============================================================
q_an_val = 4 * (5 / (2*Pi))^2;
Delta_local(T) = 2*Pi / log(q_an_val * T / (2*Pi));
R2_GUE(r)      = if(abs(r) < 1e-10, 0.0, 1.0 - (sin(Pi*r)/(Pi*r))^2);
p_GUE_wigner(s) = (32/Pi^2) * s^2 * exp(-4*s^2/Pi);
p_GOE_wigner(s) = (Pi/2) * s * exp(-Pi*s^2/4);

R_MAX = 5.0;
BIN_WIDTH = 0.1;
N_BINS = 50;
CHI2_THRESHOLD = 98;

\\ ============================================================
\\ STEP 1: Modular form + coefficient check
\\ ============================================================
print("Step 1: mfinit [4,5,Mod(3,4)] ...");
mf = mfinit([4, 5, Mod(3,4)], 1);
F  = mfeigenbasis(mf);
if(#F == 0, error("No newforms found"));
print("  newforms = ", #F);
f    = F[1];
coef = mfcoefs(f, 6);
a2   = coef[3];
a5   = coef[6];
print("  a_2 = ", a2, "  (LMFDB: -4)");
print("  a_5 = ", a5, "  (LMFDB: -14)");
if(a2 != -4, error("a_2 MISMATCH"));
if(a5 != -14, error("a_5 MISMATCH"));
print("  Coefficients VERIFIED.");
print("");

\\ ============================================================
\\ STEP 2: L-function zeros to T=200
\\ ============================================================
T_MAX = 200;
print("Step 2: lfunmf + lfuninit + lfunzeros to T=", T_MAX, " ...");
print("  (parisize=1GB; this takes a few seconds on PARI 2.17)");
ldata = lfunmf(mf, f);
lf    = lfuninit(ldata, [T_MAX]);
print("  lfuninit done.  t=", (getwalltime()-time_start)/1000, "s");
zeros = lfunzeros(lf, [0, T_MAX]);
N_zeros = #zeros;
print("  lfunzeros done.  t=", (getwalltime()-time_start)/1000, "s");
weyl_est = (T_MAX/(2*Pi)) * log(q_an_val * T_MAX / (2*Pi)) - T_MAX/(2*Pi);
print("  N_zeros = ", N_zeros, "  (Weyl ~ ", round(weyl_est), ")");
if(N_zeros < 2, error("Too few zeros"));
print("");

\\ ============================================================
\\ STEP 3: Normalized gaps (M94 single-line fix)
\\ ============================================================
print("Step 3: Normalized gaps ...");
norm_gaps = vector(N_zeros-1, j, (zeros[j+1]-zeros[j]) / Delta_local((zeros[j]+zeros[j+1])/2));
N_gaps = N_zeros - 1;
print("  N_gaps = ", N_gaps);
print("");

\\ ============================================================
\\ STEP 4: Basic statistics
\\ ============================================================
print("Step 4: Basic statistics ...");
r1      = norm_gaps[1];
r_sum   = sum(j=1, N_gaps, norm_gaps[j]);
r_sum2  = sum(j=1, N_gaps, norm_gaps[j]^2);
r_mean  = r_sum / N_gaps;
r_var   = r_sum2/N_gaps - r_mean^2;
r_std   = sqrt(r_var);
r_max   = vecmax(norm_gaps);
r_min   = vecmin(norm_gaps);
r_dev   = abs(r_mean - 1.0);
printf("  r_1        = %.8f\n", r1);
printf("  mean(r_n)  = %.8f   [GUE: ~1.000]\n", r_mean);
printf("  std(r_n)   = %.8f\n", r_std);
printf("  var(r_n)   = %.8f\n", r_var);
printf("  max(r_n)   = %.8f\n", r_max);
printf("  min(r_n)   = %.8f\n", r_min);
printf("  |mean-1|   = %.8f\n", r_dev);
print("");

\\ ============================================================
\\ STEP 5: r_1 verdict
\\ (avoid && in top-level if; use nested if instead)
\\ ============================================================
print("Step 5: r_1 verdict ...");
if(r1 >= 0.5,
  if(r1 <= 2.0,
    printf("  r_1 VERDICT: NORMAL -- r_1=%.6f in [0.5,2.0]\n", r1),
    if(r1 > 2.5,
      printf("  r_1 VERDICT: ANOMALY -- r_1=%.6f > 2.5 => Exp.Math. letter potential\n", r1),
      printf("  r_1 VERDICT: BORDERLINE -- r_1=%.6f in (2.0,2.5]\n", r1)
    )
  ),
  printf("  r_1 VERDICT: SMALL FIRST GAP -- r_1=%.6f < 0.5 (possible CM zero clustering)\n", r1)
);
if(r_dev > 0.15,
  printf("  MEAN VERDICT: WARNING |mean-1|=%.6f > 0.15\n", r_dev),
  printf("  MEAN VERDICT: OK |mean-1|=%.6f\n", r_dev)
);
print("");

\\ ============================================================
\\ STEP 6: Pair correlation histogram
\\ (nested for-loop in {braces}; local vars with my())
\\ ============================================================
print("Step 6: Pair correlation histogram ...");
hist_pair = vector(N_BINS, k, 0);
N_pairs = 0;
{
  for(ii=1, N_gaps, {
    my(sc, bi);
    sc = 0;
    for(jj=ii, N_gaps, {
      sc = sc + norm_gaps[jj];
      if(sc > R_MAX, break());
      bi = floor(sc / BIN_WIDTH) + 1;
      if(bi >= 1,
        if(bi <= N_BINS, {
          hist_pair[bi] = hist_pair[bi] + 1;
          N_pairs = N_pairs + 1
        })
      )
    })
  })
}
print("  Pairs counted: ", N_pairs);

\\ GUE normalisation
gue_unnorm = sum(k=1, N_BINS, R2_GUE((k-0.5)*BIN_WIDTH)*BIN_WIDTH);
if(gue_unnorm < 1e-10, error("GUE norm ~ 0"));
nf_pair = N_pairs / gue_unnorm;
gue_pair_exp = vector(N_BINS, k, nf_pair * R2_GUE((k-0.5)*BIN_WIDTH) * BIN_WIDTH);
print("");

\\ ============================================================
\\ STEP 7: Chi^2 pair correlation vs GUE
\\ ============================================================
print("Step 7: Chi^2 pair correlation vs GUE ...");
chi2_pair = 0.0;
dof_pair  = 0;
{
  for(k=1, N_BINS, {
    if(gue_pair_exp[k] >= 5, {
      chi2_pair = chi2_pair + (hist_pair[k] - gue_pair_exp[k])^2 / gue_pair_exp[k];
      dof_pair = dof_pair + 1
    })
  })
}
dof_pair_r = dof_pair - 1;
printf("  chi^2 pair corr vs GUE = %.4f  dof=%d  threshold=%d\n", chi2_pair, dof_pair_r, CHI2_THRESHOLD);
if(chi2_pair > CHI2_THRESHOLD,
  printf("  PAIR CORR: WARNING chi^2=%.2f > %d => GUE DEVIATION\n", chi2_pair, CHI2_THRESHOLD),
  printf("  PAIR CORR: PASS chi^2=%.2f <= %d\n", chi2_pair, CHI2_THRESHOLD)
);
print("");

\\ ============================================================
\\ STEP 8: Nearest-neighbor spacing P(s) vs GUE/GOE
\\ ============================================================
print("Step 8: Nearest-neighbor spacing P(s) ...");
nn_hist = vector(N_BINS, k, 0);
{
  for(j=1, N_gaps, {
    my(bi);
    bi = floor(norm_gaps[j] / BIN_WIDTH) + 1;
    if(bi >= 1,
      if(bi <= N_BINS,
        nn_hist[bi] = nn_hist[bi] + 1
      )
    )
  })
}
gue_nn_u = sum(k=1, N_BINS, p_GUE_wigner((k-0.5)*BIN_WIDTH)*BIN_WIDTH);
goe_nn_u = sum(k=1, N_BINS, p_GOE_wigner((k-0.5)*BIN_WIDTH)*BIN_WIDTH);
gue_nn_exp = vector(N_BINS, k, N_gaps * p_GUE_wigner((k-0.5)*BIN_WIDTH)*BIN_WIDTH / gue_nn_u);
goe_nn_exp = vector(N_BINS, k, N_gaps * p_GOE_wigner((k-0.5)*BIN_WIDTH)*BIN_WIDTH / goe_nn_u);

chi2_gue = 0.0; chi2_goe = 0.0; dof_nn = 0;
{
  for(k=1, N_BINS, {
    if(gue_nn_exp[k] >= 3, {
      chi2_gue = chi2_gue + (nn_hist[k] - gue_nn_exp[k])^2 / gue_nn_exp[k];
      chi2_goe = chi2_goe + (nn_hist[k] - goe_nn_exp[k])^2 / goe_nn_exp[k];
      dof_nn = dof_nn + 1
    })
  })
}
printf("  chi^2 NN vs GUE = %.4f  (dof~%d)\n", chi2_gue, dof_nn-1);
printf("  chi^2 NN vs GOE = %.4f  (dof~%d)\n", chi2_goe, dof_nn-1);
if(chi2_goe < chi2_gue,
  printf("  P(s): closer to GOE/SO(even)  ratio=%.4f  => CM prediction\n", chi2_goe/chi2_gue),
  printf("  P(s): closer to GUE  ratio=%.4f\n", chi2_goe/chi2_gue)
);
print("");

\\ ============================================================
\\ STEP 9: Histogram table (machine-readable)
\\ ============================================================
print("Step 9: Histogram table ...");
print("BIN_TABLE: r_center pair_obs GUE_pair_exp nn_obs GUE_nn_exp GOE_nn_exp");
{
  for(k=1, N_BINS, {
    my(rc);
    rc = (k-0.5)*BIN_WIDTH;
    printf("BIN %.2f  %d  %.4f  %d  %.4f  %.4f\n",
      rc, hist_pair[k], gue_pair_exp[k], nn_hist[k], gue_nn_exp[k], goe_nn_exp[k])
  })
}
print("");

\\ ============================================================
\\ STEP 10: Raw zeros CSV export
\\ ============================================================
print("Step 10: Raw zeros CSV ...");
print("CSV_HEADER: n,gamma_n,norm_gap_to_next");
{
  for(j=1, N_zeros-1, {
    printf("CSV %d,%.12f,%.8f\n", j, zeros[j], norm_gaps[j])
  })
}
printf("CSV %d,%.12f,NA\n", N_zeros, zeros[N_zeros]);
print("");

\\ ============================================================
\\ STEP 11: Final summary
\\ ============================================================
t_total = (getwalltime()-time_start)/1000;

print("====================================================");
print("M98 v2 FINAL SUMMARY");
print("====================================================");
printf("  Form:         4.5.b.a  (Gamma_0(4), wt=5, chi_4, CM)\n");
printf("  T_max:        %d\n", T_MAX);
printf("  N_zeros:      %d  (Weyl ~ %d)\n", N_zeros, round(weyl_est));
printf("  N_gaps:       %d\n", N_gaps);
printf("  q_an:         %.6f  (= 25/Pi^2)\n", q_an_val);
print("  ---");
printf("  r_1:          %.8f\n", r1);
printf("  mean(r_n):    %.8f  [GUE: 1.0]\n", r_mean);
printf("  std(r_n):     %.8f\n", r_std);
printf("  max(r_n):     %.8f\n", r_max);
printf("  min(r_n):     %.8f\n", r_min);
print("  ---");
printf("  chi^2 pair/GUE:  %.4f  dof=%d  thresh=%d\n", chi2_pair, dof_pair_r, CHI2_THRESHOLD);
printf("  chi^2 NN/GUE:    %.4f  dof=%d\n", chi2_gue, dof_nn-1);
printf("  chi^2 NN/GOE:    %.4f  dof=%d\n", chi2_goe, dof_nn-1);
print("  ---");
printf("  Wall time:    %.1f s\n", t_total);
print("");
print("VERDICT:");

\\ r_1 verdict (no && in if conditions)
if(r1 >= 0.5,
  if(r1 <= 2.0,
    printf("  [NORMAL] r_1=%.6f in [0.5,2.0]\n", r1),
    if(r1 > 2.5,
      printf("  [ANOMALY] r_1=%.6f > 2.5 => NEW Exp.Math. letter potential!\n", r1),
      printf("  [BORDERLINE] r_1=%.6f in (2.0,2.5] -- need T=500\n", r1)
    )
  ),
  printf("  [SMALL r_1] r_1=%.6f < 0.5 -- possible CM zero clustering\n", r1)
);

if(chi2_pair > CHI2_THRESHOLD,
  printf("  [ALERT] Pair corr chi^2=%.2f > %d -- GUE deviation\n", chi2_pair, CHI2_THRESHOLD),
  printf("  [OK] Pair corr chi^2=%.2f consistent with GUE\n", chi2_pair)
);

if(chi2_goe < chi2_gue,
  print("  [SO(even)] P(s) favors GOE -- CM newform prediction confirmed"),
  print("  [GUE] P(s) favors GUE")
);

if(N_zeros >= 150,
  printf("  [PAPER-GRADE] %d >= 150 zeros: statistics reliable\n", N_zeros),
  printf("  [CAUTION] %d < 150 zeros\n", N_zeros)
);

print("");
print("References:");
print("  Montgomery (1973) Proc. Symp. Pure Math. 24, pair correlation");
print("  Katz-Sarnak (1999) BAMS 36(1):1-26");
print("  Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("  Shin-Templier arXiv:1208.1945 (Frobenius-Schur, CM symplectic)");
print("  Mehta: Random Matrices, 3rd ed.");
print("  LMFDB 4.5.b.a: https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/4/5/b/a/");
print("====================================================");
print("r_1_test_T200.gp v2 COMPLETE");
print("====================================================");
