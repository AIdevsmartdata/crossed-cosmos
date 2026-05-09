default(parisize, "4G");
default(realprecision, 100);

\\ For each K, find E with CM by O_K, then test α_2 = L(f, 2)·π²/Ω⁴
\\ where f = LMFDB weight-5 newform attached to ψ_K^4

\\ Q(√-7) : E:y²=x³-35x-98 (CM by O_K, conductor 49)
test(D, level, ec_a4, ec_a6) = {
  my(E, om, mf, F, f, cf, Lf, Lv, alpha, ba);
  E = ellinit([0, 0, 0, ec_a4, ec_a6]);
  om = abs(real(E.omega[1]));
  mf = mfinit([level, 5, D], 0);
  F = mfeigenbasis(mf);
  print("=== K=Q(√", D, "), N=", level, " ===");
  print("dim = ", mfdim(mf));
  if(#F > 0,
    f = F[1];
    cf = mfcoefs(f, 15);
    if(type(cf[2]) == "t_INT",
      Lf = lfunmf(mf, f);
      Lv = lfun(Lf, 2);
      alpha = Lv * Pi^2 / om^4;
      ba = bestappr(alpha, 1000);
      printf("alpha = %.50Pf\n", alpha);
      printf("bestappr = %s, diff = %.5Pe\n", ba, alpha - ba*1.0);
      ,
      print("non-rational coef")
    );
  );
};

\\ Q(√-7), known curve: y² = x³ - 35x - 98 (j = -3375)
print("\n--- Q(√-7) candidates ---");
test(-7, 7, -35, -98);
test(-7, 28, -35, -98);
test(-7, 49, -35, -98);

\\ Q(√-2), known curve: y² = x³ + 4x² + 2x (256.a curve, j = 8000)
\\ Try simpler y² = x³ - 2x form? Actually y² = x³ + 8x - 8 has CM by Q(√-2)
print("\n--- Q(√-2) candidates ---");
test(-8, 8, -2, 0);
test(-8, 32, -2, 0);

\\ Q(√-11)
print("\n--- Q(√-11) candidates ---");
test(-11, 11, -11264, -1601280);
test(-11, 44, -11264, -1601280);

quit;
