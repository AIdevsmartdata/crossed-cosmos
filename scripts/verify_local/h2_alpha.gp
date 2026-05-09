default(parisize, "8G");
default(parisizemax, "16G");
default(realprecision, 60);

\\ For each h=2 field, find rational newforms AND test α_2 = L(f,2)·π²/Ω⁴ for the corresponding CM elliptic curve

\\ Approximate CM curves for h=2 K (using LMFDB cross-check)
\\ Format: D, [a4, a6] for E with j(τ_K) being algebraic of degree 2

\\ For h=2 we need pairs of curves giving Galois-conjugate j-invariants
\\ For now, scan by level only (without curve), find rationals + test α_2 with E:y²=x³-x as proxy

testD_alpha(D) = {
  my(mf, F, f, cf, Lf, Lv, alpha, ba, om);
  \\ Use a "test" elliptic curve to get a period for normalization
  \\ For now: use E:y²=x³-x just to compare scales
  E_test = ellinit([0,0,0,-1,0]);
  om_test = abs(real(E_test.omega[1]));
  print("=== D=", D, " (using E:y²=x³-x as test curve, om_test=", om_test, ") ===");
  base = -D;
  for(mi = 1, 5,
    N = base * mi;
    if(N > 1000, next);
    err = iferr(mf = mfinit([N, 5, D], 0); dimm = mfdim(mf), E0, -1);
    if(err == -1, next);
    if(dimm == 0, next);
    F = mfeigenbasis(mf);
    if(#F == 0, next);
    for(fi = 1, #F,
      f = F[fi];
      cf = mfcoefs(f, 15);
      if(type(cf[2]) == "t_INT",
        Lf = lfunmf(mf, f);
        Lv = lfun(Lf, 2);
        \\ Just compute L(f,2) and look at it
        ba = bestappr(Lv, 100000);
        diff = abs(Lv - ba*1.0);
        printf("  N=%d fi=%d L(f,2)=%.20Pf bestappr=%s diff=%.2Pe\n", N, fi, Lv, ba, diff);
      );
    );
  );
};

testD_alpha(-15);
testD_alpha(-20);
testD_alpha(-24);
testD_alpha(-35);
testD_alpha(-40);
testD_alpha(-51);
testD_alpha(-52);
testD_alpha(-88);

quit;
