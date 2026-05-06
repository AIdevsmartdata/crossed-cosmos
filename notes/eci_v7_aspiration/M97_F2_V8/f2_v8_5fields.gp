\\=======================================================================
\\ M97 F2 v8 — 5 Heegner-Stark fields: d in {2, 19, 43, 67, 163}
\\ Compute R(f) = Pi * L(f,1) / L(f,2) for weight-5 CM newforms
\\ Verify R-6 Conjecture 3.3: R(f) in Q iff K = Q(i)
\\
\\ Per M85 Lemma:
\\   d=2  (Type II, K=Q(sqrt(-2))): k=5 odd => level N=8
\\   d=19 (Type IV): k=5 odd => level N=19
\\   d=43 (Type IV): k=5 odd => level N=43
\\   d=67 (Type IV): k=5 odd => level N=67
\\   d=163(Type IV): k=5 odd => level N=163
\\
\\ Conrey indices (from M62 pattern + analytic derivation):
\\   d=2:   Mod(3,8)   [chi_{-8}, confirmed: chareval matches K(-8,.)]
\\   d=19:  Mod(18,19) [chi_{-19}=Legendre(./19), Conrey=d-1 pattern from M62]
\\   d=43:  Mod(42,43) [same pattern]
\\   d=67:  Mod(66,67) [same pattern]
\\   d=163: Mod(162,163) [same pattern]
\\
\\ Verification: M62 confirmed d=7 Conrey=6 (d-1), d=11 Conrey=10 (d-1).
\\
\\ PARI 2.15.4 syntax: use functions for blocks, my() declared without =
\\ Run: gp -q < f2_v8_5fields.gp 2>&1 | tee f2_v8_5fields.log
\\=======================================================================

default(realprecision, 80);
B9 = 10^9;

\\=======================================================================
\\ Core computation function: given mf space, eigenbasis member, field d
\\ Prints all diagnostics and VERDICT
\\=======================================================================
do_compute(mf, F, d, label) = {
  Lobj = lfunmf(mf, F);
  L1 = lfun(Lobj, 1);
  L2 = lfun(Lobj, 2);
  L3 = lfun(Lobj, 3);
  L4 = lfun(Lobj, 4);
  print("  LVALS_", label, ": L1=", L1, " L2=", L2, " L3=", L3, " L4=", L4);
  Rf = Pi * L1 / L2;
  sqd = sqrt(d);
  print("  Rf_", label, "=", Rf);
  Rfq = bestappr(Rf, B9);
  Rfr = bestappr(Rf/sqd, B9);
  print("  Rf_BESTAPPR_", label, "=", Rfq);
  print("  Rf_OVER_SQRTD_", label, "=", Rfr);
  \\ Bootstrap ladder
  a1b = L1*Pi^3/L4;
  a2b = L2*Pi^2/L4;
  a3b = L3*Pi/L4;
  print("  BOOT_", label, ": a1/sqd=", bestappr(a1b/sqd,B9), " a2=", bestappr(a2b,B9), " a3/sqd=", bestappr(a3b/sqd,B9));
  \\ Rationality test
  rq = abs(Rf - Rfq);
  rr = abs(Rf - Rfr*sqd);
  print("  RESID_Q_", label, "=", rq);
  print("  RESID_SQRTD_", label, "=", rr);
  if(rq < 1e-50,
    print("VERDICT_", label, ": Rf IN Q = ", Rfq),
    if(rr < 1e-50,
      print("VERDICT_", label, ": Rf IN Q(sqrt(", d, "))\\Q = (", Rfr, ")*sqrt(", d, ")"),
      print("VERDICT_", label, ": UNDETERMINED - residuals Q=", rq, " sqrtd=", rr)
    )
  );
  print("DONE_", label);
};

\\=======================================================================
\\ d=2, N=8, K=Q(sqrt(-2))
\\ Kronecker(-8,.): K(-8,1)=1, K(-8,3)=1, K(-8,5)=-1, K(-8,7)=-1
\\ chareval tests (confirmed): Mod(3,8) -> chareval at 3,5,7 = 0,1/2,1/2
\\   => chi(3)=+1, chi(5)=-1, chi(7)=-1 which matches K(-8,.)
\\ So Conrey index = 3 mod 8 for chi_{-8}
\\=======================================================================
print("======================================================");
print("d=2 K=Q(sqrt(-2)) N=8 k=5 chi=Mod(3,8)");
print("======================================================");
{
  d = 2;
  N = 8;
  k = 5;
  conrey = 3;
  label = "8.5.d2";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B == 0,
    print("  NO FORMS FOUND at N=8 k=5 chi=Mod(3,8)"),
    for(j=1, #B,
      F = B[j];
      print("  j=", j, " a2=", mfcoef(F,2), " a3=", mfcoef(F,3), " a5=", mfcoef(F,5), " a7=", mfcoef(F,7));
      do_compute(mf, F, d, label)
    )
  )
}

\\=======================================================================
\\ d=19, N=19, K=Q(sqrt(-19))
\\ Conrey index = 18 (= d-1 pattern from M62: d=7 used 6, d=11 used 10)
\\=======================================================================
print("");
print("======================================================");
print("d=19 K=Q(sqrt(-19)) N=19 k=5 chi=Mod(18,19)");
print("======================================================");
{
  d = 19;
  N = 19;
  k = 5;
  conrey = 18;
  label = "19.5.d19";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B == 0,
    print("  NO FORMS at chi=Mod(18,19) - trying other quadratic chars"),
    for(j=1, #B,
      F = B[j];
      print("  j=", j, " a2=", mfcoef(F,2), " a3=", mfcoef(F,3), " a5=", mfcoef(F,5));
      do_compute(mf, F, d, label)
    )
  )
}

\\=======================================================================
\\ Fallback for d=19: if Mod(18,19) gives 0 forms, try other Conrey index
\\ The other quadratic char mod 19 has Conrey index = quadratic residue generator
\\ We test Mod(7,19) as a secondary candidate
\\=======================================================================
{
  chi_test = znchar(Mod(7,19));
  mf_test = mfinit([19, 5, chi_test], 1);
  B_test = mfeigenbasis(mf_test);
  if(#B_test > 0,
    print("  FALLBACK d=19: Mod(7,19) gives ", #B_test, " forms"),
    print("  FALLBACK d=19: Mod(7,19) also empty")
  );
  if(#B_test > 0,
    for(j=1, #B_test, do_compute(mf_test, B_test[j], 19, "19.5.d19.fb"))
  )
}

\\=======================================================================
\\ d=43, N=43, K=Q(sqrt(-43))
\\=======================================================================
print("");
print("======================================================");
print("d=43 K=Q(sqrt(-43)) N=43 k=5 chi=Mod(42,43)");
print("======================================================");
{
  d = 43;
  N = 43;
  k = 5;
  conrey = 42;
  label = "43.5.d43";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B == 0,
    print("  NO FORMS at chi=Mod(42,43)"),
    for(j=1, #B,
      F = B[j];
      print("  j=", j, " a2=", mfcoef(F,2), " a3=", mfcoef(F,3), " a5=", mfcoef(F,5));
      do_compute(mf, F, d, label)
    )
  )
}

\\=======================================================================
\\ d=67, N=67, K=Q(sqrt(-67))
\\=======================================================================
print("");
print("======================================================");
print("d=67 K=Q(sqrt(-67)) N=67 k=5 chi=Mod(66,67)");
print("======================================================");
{
  d = 67;
  N = 67;
  k = 5;
  conrey = 66;
  label = "67.5.d67";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B == 0,
    print("  NO FORMS at chi=Mod(66,67)"),
    for(j=1, #B,
      F = B[j];
      print("  j=", j, " a2=", mfcoef(F,2), " a3=", mfcoef(F,3), " a5=", mfcoef(F,5));
      do_compute(mf, F, d, label)
    )
  )
}

\\=======================================================================
\\ d=163, N=163, K=Q(sqrt(-163))
\\=======================================================================
print("");
print("======================================================");
print("d=163 K=Q(sqrt(-163)) N=163 k=5 chi=Mod(162,163)");
print("======================================================");
{
  d = 163;
  N = 163;
  k = 5;
  conrey = 162;
  label = "163.5.d163";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B == 0,
    print("  NO FORMS at chi=Mod(162,163)"),
    for(j=1, #B,
      F = B[j];
      print("  j=", j, " a2=", mfcoef(F,2), " a3=", mfcoef(F,3), " a5=", mfcoef(F,5));
      do_compute(mf, F, d, label)
    )
  )
}

\\=======================================================================
\\ Also run anchors from M62 to verify same R(f) values (sanity check)
\\=======================================================================
print("");
print("======================================================");
print("SANITY CHECK: d=1 anchor (4.5.b.a, should give R=6/5)");
print("======================================================");
{
  d = 1;
  N = 4;
  k = 5;
  conrey = 3;
  label = "4.5.b.a";
  chi = znchar(Mod(conrey, N));
  mf = mfinit([N, k, chi], 1);
  B = mfeigenbasis(mf);
  print("  nforms=", #B);
  if(#B > 0,
    F = B[1];
    Lobj = lfunmf(mf, F);
    L1 = lfun(Lobj, 1);
    L2 = lfun(Lobj, 2);
    Rf = Pi*L1/L2;
    print("  Rf_anchor=", Rf, " bestappr=", bestappr(Rf, B9));
    print("  Sanity: expect 6/5=", 6/5, " got ~", Rf)
  )
}

print("");
print("======================================================");
print("M97 F2 v8 COMPLETE");
print("======================================================");
quit
