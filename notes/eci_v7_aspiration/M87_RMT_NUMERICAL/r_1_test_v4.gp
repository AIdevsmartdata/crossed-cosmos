\\ ============================================================
\\ r_1_test_v4.gp
\\ M94 — Fixed version of M92 r_1_test_v3.gp
\\ PARI/GP 2.11+
\\ Run: gp -q < r_1_test_v4.gp > r_1_test_v4.log 2>&1
\\ Estimated runtime: 2-5 min for 50 zeros
\\ ============================================================
\\
\\ FIX SUMMARY (M94, 2026-05-06):
\\
\\ BUG 1 (lfuninit t_VEC error):
\\   CAUSE: lfuninit(f, [50]) where f = mfeigenbasis(mf)[1] is a t_VEC eigenform;
\\          lfuninit expects an L-data object, not a raw modular form vector.
\\   FIX:   Use lfunmf(mf, f) to construct the L-data object first, then
\\          lf = lfuninit(ldata, [50]).
\\          PARI docs: lfunmf(mf, {f}) — if f given, L-function of the eigenform f
\\          inside the space mf; if f omitted, L-function of the full space.
\\
\\ BUG 2 (vector multi-line syntax error):
\\   CAUSE: vector(N_zeros - 1, j, \n  expr\n) — PARI batch-mode parser
\\          reads line-by-line; a bare vector(..., j, <newline> is not valid
\\          outside a {braced block}.
\\   FIX:   Put entire vector(N, j, expr) call on a single line.
\\
\\ MATHEMATICAL SETUP (hand-traced, M87 verified):
\\ f = 4.5.b.a : Gamma_0(4), wt=5, chi=chi_4 (chi(3)=-1), LMFDB label 4.5.b.a
\\ Analytic conductor: q_an = N*(k/(2*Pi))^2 = 4*(5/(2*Pi))^2 = 25/Pi^2 ~ 2.5331
\\ Mean spacing at height T: Delta(T) = 2*Pi / log(q_an*T/(2*Pi))
\\ Normalized gap: r_n = (gamma_{n+1} - gamma_n) / Delta((gamma_n+gamma_{n+1})/2)
\\
\\ LMFDB checks (2026-05-06 live-verified by M81):
\\   a_2 = -4,  a_5 = -14,  epsilon(sign FE) = +1,  analytic rank = 0
\\ ============================================================

default(parisize, 128000000);
default(realbitprecision, 64);

print("====================================================");
print("M87/M94 -- L(4.5.b.a, s) zero statistics -- PARI/GP v4");
print("Date: computed by Kevin Remondiere, ECI project");
print("====================================================");
print("");

\\ ----------------------------------------------------------
\\ Helper function: local mean spacing (defined before use)
\\ ----------------------------------------------------------
\\ q_an = 4*(5/(2*Pi))^2 = 25/Pi^2 ~ 2.5331
\\ Delta(T) = 2*Pi / log(q_an * T / (2*Pi))

q_an_val = 4 * (5 / (2*Pi))^2;
Delta_local(T) = 2*Pi / log(q_an_val * T / (2*Pi));

\\ ----------------------------------------------------------
\\ Helper: check_coef(got, expected, name) — print and quit on mismatch
\\ ----------------------------------------------------------
check_coef(got, expected, name) = {
  if(got == expected,
    print("  PASS: ", name, " = ", got, " confirmed."),
    print("  !! ERROR: ", name, " mismatch. Got ", got, " expected ", expected);
    print("  !! Halting. Verify: mfinit([4,5,Mod(3,4)],1) on your PARI version.");
    quit()
  );
}

\\ ----------------------------------------------------------
\\ Helper: verdict_r1(r) — verdict for first normalized gap
\\ ----------------------------------------------------------
verdict_r1(r) = {
  if(r >= 0.5 && r <= 2.0,
    print("  r_1 VERDICT: PASS -- r_1 = ", r, " in [0.5, 2.0] (normal GUE/SO(even))"),
    if(r > 2.5,
      print("  r_1 VERDICT: ANOMALY -- r_1 = ", r, " > 2.5 (possible CM arithmetic effect)");
      print("  ACTION: Dispatch M87-followup; cross-cite Hamieh-Wong arXiv:2412.03034"),
      print("  r_1 VERDICT: BORDERLINE -- r_1 = ", r, " in (2.0, 2.5]");
      print("  ACTION: Compute pair correlation histogram (pair_correlation_v4.gp)")
    )
  );
}

\\ ----------------------------------------------------------
\\ Helper: verdict_mean(dev) — verdict for mean gap
\\ ----------------------------------------------------------
verdict_mean(dev) = {
  if(dev > 0.15,
    print("  MEAN VERDICT: WARNING -- |mean(r) - 1| = ", dev, " > 0.15");
    print("  This suggests systematic deviation from GUE. Recheck needed."),
    print("  MEAN VERDICT: OK -- |mean(r) - 1| = ", dev, " <= 0.15")
  );
}

\\ ===========================================================
\\ STEP 1: Build modular form f = 4.5.b.a
\\ ===========================================================
\\ Gamma_0(4), weight 5, character chi_4: the unique primitive character mod 4
\\ with chi(3) = -1. In PARI: Mod(3,4) encodes chi(3) = zeta_2^1 = -1.

print("Step 1: Initializing modular form space...");
mf = mfinit([4, 5, Mod(3,4)], 1);

\\ mfeigenbasis(mf) returns a vector of eigenform objects (t_VEC of t_VEC).
F = mfeigenbasis(mf);

if(#F == 0, error("No newforms found -- check character specification"));
print("  Number of newforms in space: ", #F);
if(#F > 1, print("  WARNING: found ", #F, " newforms; expected 1 (4.5.b.a unique). Using first."));

f = F[1];
print("  Newform object extracted.");

\\ ===========================================================
\\ STEP 2: Coefficient verification (a_2 and a_5)
\\ ===========================================================
\\ mfcoefs(f, n) returns [a_0, a_1, a_2, ..., a_n] (1-indexed, length n+1)
\\ a_2 = coefs[3],  a_5 = coefs[6]

print("");
print("Step 2: Verifying Hecke coefficients against LMFDB...");
coefs = mfcoefs(f, 6);
a2 = coefs[3];
a5 = coefs[6];

print("  a_2 = ", a2, "  (LMFDB expected: -4)");
print("  a_5 = ", a5, "  (LMFDB expected: -14)");

check_coef(a2, -4, "a_2");
check_coef(a5, -14, "a_5");

\\ ===========================================================
\\ STEP 3: Build L-function and compute zeros up to height 50
\\ ===========================================================
\\
\\ M94 FIX (Bug 1): lfuninit(f, [50]) fails with "incorrect type in
\\ lfunmisc_to_ldata (t_VEC)" because f is a modular form vector, not
\\ an L-data object.
\\
\\ CORRECT sequence (PARI 2.11 manual, §L-functions):
\\   ldata = lfunmf(mf, f);   -- constructs the L-data from eigenform f in space mf
\\   lf    = lfuninit(ldata, [50]);  -- precomputes for zeros up to height 50
\\
\\ lfunmf(mf, f): if f is provided, returns L-data for the eigenform f in mf.
\\ lfuninit(ldata, [T]): precomputes everything needed for lfunzeros up to T.

print("");
print("Step 3: Computing zeros of L(f,s) up to height T=50...");
print("  (This may take 2-5 minutes)");

\\ Bug 1 fix: construct L-data object via lfunmf before calling lfuninit
ldata = lfunmf(mf, f);
lf = lfuninit(ldata, [50]);

zeros = lfunzeros(lf, [0, 50]);

N_zeros = #zeros;
print("  Number of zeros found: ", N_zeros);
if(N_zeros < 10, print("  WARNING: fewer than 10 zeros found; normalization statistics unreliable."));

\\ ===========================================================
\\ STEP 4: Analytic conductor and normalized gaps
\\ ===========================================================

print("");
print("Step 4: Analytic conductor and normalized gaps...");
print("  Analytic conductor q_an = 4*(5/(2*Pi))^2 = ", q_an_val);
print("  Cross-check: 25/Pi^2 = ", 25/Pi^2);

if(N_zeros < 2, print("ERROR: fewer than 2 zeros; cannot compute gaps."); quit());

\\ M94 FIX (Bug 2): vector(N_zeros-1, j, expr) was split across lines in v3.
\\ PARI batch mode cannot parse a top-level vector() with a newline inside the
\\ argument list (outside a {braced block}).  Put on a SINGLE line.
norm_gaps = vector(N_zeros - 1, j, (zeros[j+1] - zeros[j]) / Delta_local((zeros[j] + zeros[j+1]) / 2));

N_gaps = #norm_gaps;

\\ ===========================================================
\\ STEP 5: Statistics
\\ ===========================================================
print("");
print("Step 5: Gap statistics...");

r1 = norm_gaps[1];
r_mean = sum(j = 1, N_gaps, norm_gaps[j]) / N_gaps;
r_max  = vecmax(norm_gaps);
r_min  = vecmin(norm_gaps);

\\ GUE theoretical mean: E[r] = 1.0000 (by construction of normalization)
r_mean_dev = abs(r_mean - 1.0);

print("  Number of gaps: ", N_gaps);
print("  r_1 (first normalized gap):  ", r1);
print("  mean(r_n):                   ", r_mean, "  [GUE expect: ~1.000]");
print("  max(r_n):                    ", r_max);
print("  min(r_n):                    ", r_min);
print("  |mean - 1|:                  ", r_mean_dev, "  [should be < 0.15 for GUE]");

\\ ===========================================================
\\ STEP 6: PASS/ANOMALY verdict
\\ ===========================================================
print("");
print("Step 6: VERDICT...");

verdict_r1(r1);
verdict_mean(r_mean_dev);

\\ ===========================================================
\\ STEP 7: Output all zeros (for pair_correlation_v4.gp post-processing)
\\ ===========================================================
print("");
print("Step 7: All zeros gamma_n (imaginary parts, positive, sorted):");
print("FORMAT: ZERO n gamma_n norm_gap_to_next");

for(j = 1, N_zeros - 1,
  printf("ZERO %d  %.10f  gap_next=%.6f\n", j, zeros[j], norm_gaps[j])
);
printf("ZERO %d  %.10f  (last zero)\n", N_zeros, zeros[N_zeros]);

\\ Also print raw normalized gaps for easy parsing
print("");
print("RAW NORMALIZED GAPS:");
for(j = 1, N_gaps,
  printf("GAP %d  %.8f\n", j, norm_gaps[j])
);

\\ ===========================================================
\\ STEP 8: Delta values at each zero (diagnostic)
\\ ===========================================================
print("");
print("Step 8: Local mean spacing Delta(gamma_n) at each zero:");
for(j = 1, N_zeros,
  printf("DELTA %d  gamma=%.6f  Delta=%.6f\n", j, zeros[j], Delta_local(zeros[j]))
);

print("");
print("====================================================");
print("M87/M94 r_1_test_v4.gp COMPLETE");
print("====================================================");
print("Next step: run pair_correlation_v4.gp on the GAP lines above.");
print("Reference: Hamieh-Wong arXiv:2412.03034 (Hilbert modular Katz-Sarnak)");
print("ECI project: 4.5.b.a is CM form, U(1)[D_2] Sato-Tate, epsilon=+1");
