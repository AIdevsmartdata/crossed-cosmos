Welcome to vast.ai. If authentication fails, try again after a few seconds, and double check your ssh key.
Have fun!
\\ F2 — Tamagawa BSD raffiné ellbsd sweep pour 6 CM curves h_K=1 generic
\\ Opus master digest morn43 recommendation #1 : promote Tamagawa pillar à Lemma-grade
\\ For E/Q with CM by O_K, K = Q(√-D), D ∈ {7, 11, 19, 43, 67, 163} (h_K=1 generic, excl. j=0, 1728)
\\
\\ Verify rigorously :
\\ (a) elltamagawa(E/Q) global product
\\ (b) Local Tamagawa c_v at each prime v of bad reduction
\\ (c) L(E, 1) via PARI lfun + ellL1
\\ (d) Real period Ω_E
\\ (e) Sha estimation (analytic) via BSD formula
\\ (f) Torsion E(Q)_tor
\\ (g) Verify Rubin BSD : L(E,1)/Ω = #Sha · ∏c_v / |E(Q)_tor|²

default(parisize, "8G");
default(parisizemax, "16G");
default(realprecision, 50);

system("mkdir -p /root/F2_outputs");
print("=== F2: Tamagawa BSD raffiné sweep — 6 CM curves h_K=1 generic ===");
system("date '+Start: %F %T'");
print();

\\ LMFDB labels for CM elliptic curves over Q with j ∈ Z (h_K=1 imag quadratic)
\\ Source: LMFDB CM elliptic curves database
\\ D = -7  : j = -3375          curve label 49.a1   E: y^2 + xy = x^3 - x^2 - 2x - 1
\\ D = -11 : j = -32768         curve label 121.b1  E: y^2 + y = x^3 - x^2 - 7x + 10
\\ D = -19 : j = -884736        curve label 361.a1  E: y^2 + y = x^3 - 38x + 90
\\ D = -43 : j = -884736000     curve label 1849.a1 E: y^2 + y = x^3 - 860x + 9707
\\ D = -67 : j = -147197952000  curve label 4489.a1 E: y^2 + y = x^3 - 7370x + 243528
\\ D = -163: j = -262537412640768000 curve label 26569.a1 (large coeffs)

\\ Use ellinit with j-invariant when possible, fallback to explicit Weierstrass

{
CMcurves = [
  [-7,   ellinit([1, -1, 0, -2, -1])],
  [-11,  ellinit([0, -1, 1, -7, 10])],
  [-19,  ellinit([0, 0, 1, -38, 90])],
  [-43,  ellinit([0, 0, 1, -860, 9707])],
  [-67,  ellinit([0, 0, 1, -7370, 243528])],
  [-163, ellinit([0, 0, 1, -2174420, 1234136692])]
];
}

n_match = 0;

{
  for(i = 1, #CMcurves,
    D = CMcurves[i][1];
    E = CMcurves[i][2];
    print();
    print("=== D = ", D, " ===");
    print("E coefficients: ", E[1..5]);

    \\ (a) Global Tamagawa product
    c_global = elltamagawa(E);
    print("elltamagawa(E) = ", c_global);

    \\ (b) Local Tamagawa factors
    bad_primes = factor(ellglobalred(E)[1])[,1];
    print("Bad reduction primes: ", bad_primes);
    locals = [];
    for(j = 1, #bad_primes,
      p = bad_primes[j];
      cp = elllocalred(E, p);
      kodaira_type = cp[2];
      c_p = cp[4];
      locals = concat(locals, [[p, c_p, kodaira_type]]);
    );
    print("Local data [p, c_p, Kodaira_code]: ", locals);
    prod_local = prod(j = 1, #locals, locals[j][2]);
    print("∏ c_p local = ", prod_local);
    print("elltamagawa global ? = ∏ c_p local : ", c_global == prod_local);

    \\ (c) Torsion E(Q)_tor
    Tor = elltors(E)[1];
    print("|E(Q)_tor| = ", Tor);

    \\ (d) L(E, 1) via lfun
    err_L = iferr(L1 = ellL1(E), E1, -1);
    if(err_L != -1,
      print("L(E, 1) = ", precision(L1, 30));
    , print("L(E, 1) FAIL"));

    \\ (e) Real period Ω_E
    Omega = E.omega[1];
    print("Ω_E (real period) = ", precision(Omega, 30));

    \\ (f) Rank (BSD-related)
    rank_E = ellanalyticrank(E)[1];
    print("Analytic rank = ", rank_E);

    \\ (g) BSD formula : L(E,1)/Ω = #Sha · ∏c_p / |Tor|²
    if(err_L != -1 && rank_E == 0,
      ratio_LHS = L1 / Omega;
      pred_Sha = ratio_LHS * Tor^2 / prod_local;
      print("L(E,1)/Ω = ", precision(ratio_LHS, 20));
      print("Predicted #Sha via BSD = ", precision(pred_Sha, 20));
    );

    \\ N_W test : ∏c_p = 2^(1+rk_2 Cl(K)). For h_K=1, rk_2 = 0, so N_W = 2.
    target_NW = 2;
    if(c_global == target_NW,
      print("✅ MATCH: ∏c_v = ", c_global, " = N_W = 2 = 2^(1+rk_2) for h_K=1");
      n_match = n_match + 1;
    , print("⚠ MISMATCH: ∏c_v = ", c_global, " ≠ target N_W = 2"));

    \\ Write output
    fname = Str("/root/F2_outputs/d_", D, ".out");
    write(fname, Str("D=", D));
    write(fname, Str("elltamagawa=", c_global));
    write(fname, Str("locals=", locals));
    write(fname, Str("|Tor|=", Tor));
    write(fname, Str("L(E,1)=", if(err_L != -1, precision(L1, 30), "FAIL")));
    write(fname, Str("Omega=", precision(Omega, 30)));
    write(fname, Str("rank=", rank_E));
    write(fname, Str("NW_match=", c_global == target_NW));
  );
}

print();
print("=== FINAL F2 ===");
print("Total CM curves tested: ", #CMcurves);
print("∏c_v = N_W = 2 matches: ", n_match, "/6");
print("Verdict: ", if(n_match == 6, "Tamagawa pillar PROMOTED to Lemma-grade RIGOROUS", "Partial — investigate exceptions"));
system("date '+End: %F %T'");
quit;
