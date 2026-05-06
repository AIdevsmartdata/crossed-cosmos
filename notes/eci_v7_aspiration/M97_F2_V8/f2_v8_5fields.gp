\\=======================================================================
\\ M97 F2 v8 — 5 Heegner-Stark fields: d in {2, 19, 43, 67, 163}
\\ Compute R(f) = Pi * L(f,1) / L(f,2) for weight-5 CM newforms
\\ Verify R-6 Conjecture 3.3: R(f) in Q iff K = Q(i)
\\
\\ Per M85 Lemma (unified conductor table):
\\   d=2  (Type II): k=5 odd => e_k=0 => level N=8
\\   d=19 (Type IV): k=5 odd => e_k=0 => level N=19
\\   d=43 (Type IV): k=5 odd => e_k=0 => level N=43
\\   d=67 (Type IV): k=5 odd => e_k=0 => level N=67
\\   d=163(Type IV): k=5 odd => e_k=0 => level N=163
\\
\\ Strategy: for each level N, enumerate ALL quadratic + trivial characters
\\ mod N, find the weight-5 CM newform (dim=1), and compute R(f).
\\ No Conrey index hardcoded: discovered at runtime.
\\
\\ Output: one line per form:
\\   RESULT_d_N: label N d chi_idx chi_order L1 L2 Rf Rf/sqrt(d) bestappr_Rf bestappr_Rf_over_sqrtd
\\
\\ PARI 2.15.4, 80-digit precision
\\ Run: gp -q < f2_v8_5fields.gp 2>&1 | tee f2_v8_5fields.log
\\=======================================================================

default(realprecision, 80);
B7 = 10^7;
B9 = 10^9;

\\ Helper: find weight-k CM newform of dim=1 at level N
\\ scanning all characters of order dividing 2 (trivial or quadratic).
\\ Returns [chi_idx, chi_order, F, Lobj] or 0 if not found.
find_cm_form(N, k, target_disc) = {
  my(all_chars, found_chi, found_F, found_Lobj, found_ord);
  all_chars = znchars(N);
  found_chi = 0;
  for(i = 1, #all_chars,
    my(chi_idx = all_chars[i];
       chi_ord = zncharorder(N, chi_idx));
    \\ Only consider trivial (order 1) or quadratic (order 2) characters
    if(chi_ord != 1 && chi_ord != 2, next);
    my(chi = znchar(Mod(chi_idx[1], N)));
    my(mf = mfinit([N, k, chi], 1));
    my(B = mfeigenbasis(mf));
    if(#B == 0, next);
    for(j = 1, #B,
      my(fj = B[j]);
      \\ Check if the form has the expected CM discriminant
      \\ We verify by checking a_p for p | N (CM forms have a_p = 0 for inert p)
      \\ For d=prime, p=2 (if p=2 inert in K), or check character parity
      \\ Quick heuristic: compute a few L-values and check R(f) is in Q(sqrt(d))
      \\ We output all dim-1 forms and let R(f) computation decide
      found_chi = chi_idx[1];
      found_ord = chi_ord;
      found_F = fj;
      my(Lobj = lfunmf(mf, fj));
      found_Lobj = Lobj;
      print("  CANDIDATE: N=", N, " k=", k, " chi=Mod(", chi_idx[1], ",", N, ") ord=", chi_ord, " a2=", mfcoef(fj,2), " a3=", mfcoef(fj,3));
      \\ Return the first dim-1 form found
      return([found_chi, found_ord, found_F, found_Lobj, mf])
    )
  );
  print("  NO_FORM_FOUND: N=", N, " k=", k);
  return(0);
};

\\ Compute R(f) + bootstrap ladder for a found form
compute_Rf(label, N, d, chi_idx, chi_ord, F, Lobj, mf) = {
  my(sqd = sqrt(d));
  my(L1 = lfun(Lobj, 1));
  my(L2 = lfun(Lobj, 2));
  my(L3 = lfun(Lobj, 3));
  my(L4 = lfun(Lobj, 4));
  print("  LVALS_", label, ": L1=", L1, " L2=", L2, " L3=", L3, " L4=", L4);

  \\ R(f) = Pi * L(f,1) / L(f,2) -- Omega-independent
  my(Rf = Pi * L1 / L2);
  print("  Rf_", label, "=", Rf);

  \\ Rational approximations
  my(Rfq = bestappr(Rf, B9));
  my(Rfr = bestappr(Rf / sqd, B9));
  print("  Rf_BESTAPPR_", label, "=", Rfq);
  print("  Rf_OVER_SQRTD_", label, "=", Rfr);

  \\ Bootstrap ladder (Omega-independent normalization)
  my(a1b = L1*Pi^3/L4);
  my(a2b = L2*Pi^2/L4);
  my(a3b = L3*Pi^1/L4);
  my(a1br = bestappr(a1b/sqd, B9));
  my(a2bq = bestappr(a2b, B9));
  my(a3br = bestappr(a3b/sqd, B9));
  print("  BOOT_", label, ": a1/sqrt(d)=", a1br, " a2=", a2bq, " a3/sqrt(d)=", a3br);

  \\ Check Rf = a1b / a2b (M80 identity)
  my(Rf_check = a1b / a2b);
  print("  Rf_CHECK_", label, "=", Rf_check, " (should match Rf)");

  \\ Rationality classification
  my(resid_q = abs(Rf - Rfq));  \\ if small: Rf in Q
  my(resid_r = abs(Rf - Rfr * sqd));  \\ if small: Rf = Rfr * sqrt(d), in Q(sqrt(d))
  print("  RESID_Q_", label, "=", resid_q);
  print("  RESID_SQRTD_", label, "=", resid_r);

  \\ Return summary line
  print("RESULT: d=", d, " N=", N, " chi=Mod(", chi_idx, ",", N, ") ord=", chi_ord);
  print("RESULT: Rf=", Rf, " Rf_q=", Rfq, " Rf_over_sqrtd=", Rfr);
  if(resid_q < 1e-50,
    print("VERDICT_", label, ": Rf IN Q [rational] = ", Rfq),
    if(resid_r < 1e-50,
      print("VERDICT_", label, ": Rf IN Q(sqrt(", d, "))\\Q = (", Rfr, ") * sqrt(", d, ")"),
      print("VERDICT_", label, ": Rf NOT in Q or Q(sqrt(d)) - check residuals")
    )
  );
  print("DONE_", label);
};


\\=======================================================================
\\ PART A: Discover and compute for each (d, N)
\\ For each level, scan characters and find the CM dim-1 form
\\=======================================================================

\\ --- d=2, N=8 ---
print("");
print("======================================================");
print("d=2 K=Q(sqrt(-2)) N=8 k=5 [Type II, e_k=0]");
print("Expected: Chi_{-8} = Kronecker(-8,.) mod 8, order 2");
print("======================================================");
{
  my(N=8, k=5, d=2);
  \\ For K=Q(sqrt(-2)): discriminant = -8
  \\ Kronecker(-8,.) mod 8: -8 = -1 * 8 = -1 * 2^3
  \\ chi_{-8}(3) = Kronecker(-8,3) = Kronecker(-1,3)*Kronecker(2,3)*Kronecker(4,3)
  \\ Actually: Kronecker(-8,3) = (-1)^((3-1)/2) * Kronecker(2,3) ...
  \\ Directly: kronecker(-8, 3) = -1 (verify below)
  print("Kronecker(-8,.) values mod 8:");
  for(a=1, 7, if(gcd(a,8)==1, print("  kronecker(-8,",a,")=", kronecker(-8,a))));

  \\ chars mod 8 of order 2:
  my(all8 = znchars(8));
  print("All chars mod 8:");
  for(i=1,#all8,
    my(idx=all8[i][1], ord=zncharorder(8,all8[i]));
    print("  Mod(",idx,",8) order=",ord, " vals: ", vector(7,a, if(gcd(a,8)==1, chareval(znchar(Mod(idx,8)), a, 1), 0)))
  );

  \\ Find the character matching Kronecker(-8,.)
  \\ Kronecker(-8,1)=1, K(-8,3)=?, K(-8,5)=?, K(-8,7)=?
  my(kvals = vector(8, a, if(gcd(a,8)==1, kronecker(-8,a), 0)));
  print("Kronecker(-8,a) for a=1..8: ", kvals);

  \\ Now find the CM form
  \\ For d=2: the CM char should be chi_{-8}
  \\ Try each quadratic char mod 8
  for(i=1,#all8,
    my(idx=all8[i][1], ord=zncharorder(8,all8[i]));
    if(ord != 2, next);
    my(chi = znchar(Mod(idx, 8)));
    my(mf = mfinit([8, 5, chi], 1));
    my(B = mfeigenbasis(mf));
    print("chi=Mod(",idx,",8) ord=",ord," nforms=",#B);
    if(#B > 0,
      for(j=1,#B,
        my(fj=B[j]);
        print("  form j=",j," a2=",mfcoef(fj,2)," a3=",mfcoef(fj,3)," a5=",mfcoef(fj,5)," a7=",mfcoef(fj,7));
        \\ Compute R(f)
        my(Lobj = lfunmf(mf, fj));
        my(L1=lfun(Lobj,1), L2=lfun(Lobj,2));
        my(Rf = Pi*L1/L2);
        my(sqd=sqrt(d));
        print("  L1=",L1," L2=",L2);
        print("  Rf=",Rf," Rf/sqrt(",d,")=",bestappr(Rf/sqd,B9));
        print("  Rf_bestappr=",bestappr(Rf,B9));
        \\ Bootstrap
        my(L3=lfun(Lobj,3), L4=lfun(Lobj,4));
        print("  boot: a1/sqd=",bestappr(L1*Pi^3/L4/sqd,B9)," a2=",bestappr(L2*Pi^2/L4,B9)," a3/sqd=",bestappr(L3*Pi/L4/sqd,B9));
        my(resid_r = abs(Rf - bestappr(Rf/sqd,B9)*sqd));
        my(resid_q = abs(Rf - bestappr(Rf,B9)));
        print("  resid_Q=",resid_q," resid_sqrtd=",resid_r);
        if(resid_q < 1e-50,
          print("  VERDICT d=2: Rf IN Q = ",bestappr(Rf,B9)),
          if(resid_r < 1e-50,
            print("  VERDICT d=2: Rf IN Q(sqrt(2))\\Q = (",bestappr(Rf/sqd,B9),")*sqrt(2)"),
            print("  VERDICT d=2: larger extension or approx too coarse")
          )
        );
        print("  DONE_d2_j",j)
      )
    )
  )
}

\\=======================================================================
\\ --- d=19, N=19 ---
print("");
print("======================================================");
print("d=19 K=Q(sqrt(-19)) N=19 k=5 [Type IV, e_k=0]");
print("Expected: Chi_{-19} = Kronecker(-19,.) mod 19, order 2");
print("======================================================");
{
  my(N=19, k=5, d=19);
  my(sqd=sqrt(d));

  \\ Find the Conrey index for Kronecker(-19,.) mod 19
  print("Kronecker(-19,.) mod 19:");
  for(a=1,18, print("  a=",a," K(-19,a)=",kronecker(-19,a)));

  \\ Find quadratic chars mod 19
  my(all_chars = znchars(19));
  for(i=1,#all_chars,
    my(idx=all_chars[i][1], ord=zncharorder(19,all_chars[i]));
    if(ord != 2, next);
    my(chi = znchar(Mod(idx, 19)));
    my(mf = mfinit([19, 5, chi], 1));
    my(B = mfeigenbasis(mf));
    print("chi=Mod(",idx,",19) ord=",ord," nforms=",#B);
    if(#B > 0,
      for(j=1,#B,
        my(fj=B[j]);
        print("  form j=",j," a2=",mfcoef(fj,2)," a3=",mfcoef(fj,3)," a5=",mfcoef(fj,5));
        my(Lobj = lfunmf(mf, fj));
        my(L1=lfun(Lobj,1), L2=lfun(Lobj,2), L3=lfun(Lobj,3), L4=lfun(Lobj,4));
        my(Rf = Pi*L1/L2);
        print("  L1=",L1," L2=",L2);
        print("  Rf=",Rf);
        print("  Rf_bestappr=",bestappr(Rf,B9));
        print("  Rf_over_sqrtd=",bestappr(Rf/sqd,B9));
        print("  boot: a1/sqd=",bestappr(L1*Pi^3/L4/sqd,B9)," a2=",bestappr(L2*Pi^2/L4,B9)," a3/sqd=",bestappr(L3*Pi/L4/sqd,B9));
        my(resid_q = abs(Rf - bestappr(Rf,B9)));
        my(resid_r = abs(Rf - bestappr(Rf/sqd,B9)*sqd));
        print("  resid_Q=",resid_q," resid_sqrtd=",resid_r);
        if(resid_q < 1e-50,
          print("  VERDICT d=19: Rf IN Q = ",bestappr(Rf,B9)),
          if(resid_r < 1e-50,
            print("  VERDICT d=19: Rf IN Q(sqrt(19))\\Q = (",bestappr(Rf/sqd,B9),")*sqrt(19)"),
            print("  VERDICT d=19: larger extension")
          )
        );
        print("  DONE_d19_j",j)
      )
    )
  )
}

\\=======================================================================
\\ --- d=43, N=43 ---
print("");
print("======================================================");
print("d=43 K=Q(sqrt(-43)) N=43 k=5 [Type IV, e_k=0]");
print("======================================================");
{
  my(N=43, k=5, d=43);
  my(sqd=sqrt(d));

  my(all_chars = znchars(43));
  for(i=1,#all_chars,
    my(idx=all_chars[i][1], ord=zncharorder(43,all_chars[i]));
    if(ord != 2, next);
    my(chi = znchar(Mod(idx, 43)));
    my(mf = mfinit([43, 5, chi], 1));
    my(B = mfeigenbasis(mf));
    print("chi=Mod(",idx,",43) ord=",ord," nforms=",#B);
    if(#B > 0,
      for(j=1,#B,
        my(fj=B[j]);
        print("  form j=",j," a2=",mfcoef(fj,2)," a3=",mfcoef(fj,3)," a5=",mfcoef(fj,5));
        my(Lobj = lfunmf(mf, fj));
        my(L1=lfun(Lobj,1), L2=lfun(Lobj,2), L3=lfun(Lobj,3), L4=lfun(Lobj,4));
        my(Rf = Pi*L1/L2);
        print("  L1=",L1," L2=",L2," L3=",L3," L4=",L4);
        print("  Rf=",Rf);
        print("  Rf_bestappr=",bestappr(Rf,B9));
        print("  Rf_over_sqrtd=",bestappr(Rf/sqd,B9));
        print("  boot: a1/sqd=",bestappr(L1*Pi^3/L4/sqd,B9)," a2=",bestappr(L2*Pi^2/L4,B9)," a3/sqd=",bestappr(L3*Pi/L4/sqd,B9));
        my(resid_q = abs(Rf - bestappr(Rf,B9)));
        my(resid_r = abs(Rf - bestappr(Rf/sqd,B9)*sqd));
        print("  resid_Q=",resid_q," resid_sqrtd=",resid_r);
        if(resid_q < 1e-50,
          print("  VERDICT d=43: Rf IN Q = ",bestappr(Rf,B9)),
          if(resid_r < 1e-50,
            print("  VERDICT d=43: Rf IN Q(sqrt(43))\\Q = (",bestappr(Rf/sqd,B9),")*sqrt(43)"),
            print("  VERDICT d=43: larger extension")
          )
        );
        print("  DONE_d43_j",j)
      )
    )
  )
}

\\=======================================================================
\\ --- d=67, N=67 ---
print("");
print("======================================================");
print("d=67 K=Q(sqrt(-67)) N=67 k=5 [Type IV, e_k=0]");
print("======================================================");
{
  my(N=67, k=5, d=67);
  my(sqd=sqrt(d));

  my(all_chars = znchars(67));
  for(i=1,#all_chars,
    my(idx=all_chars[i][1], ord=zncharorder(67,all_chars[i]));
    if(ord != 2, next);
    my(chi = znchar(Mod(idx, 67)));
    my(mf = mfinit([67, 5, chi], 1));
    my(B = mfeigenbasis(mf));
    print("chi=Mod(",idx,",67) ord=",ord," nforms=",#B);
    if(#B > 0,
      for(j=1,#B,
        my(fj=B[j]);
        print("  form j=",j," a2=",mfcoef(fj,2)," a3=",mfcoef(fj,3)," a5=",mfcoef(fj,5));
        my(Lobj = lfunmf(mf, fj));
        my(L1=lfun(Lobj,1), L2=lfun(Lobj,2), L3=lfun(Lobj,3), L4=lfun(Lobj,4));
        my(Rf = Pi*L1/L2);
        print("  L1=",L1," L2=",L2," L3=",L3," L4=",L4);
        print("  Rf=",Rf);
        print("  Rf_bestappr=",bestappr(Rf,B9));
        print("  Rf_over_sqrtd=",bestappr(Rf/sqd,B9));
        print("  boot: a1/sqd=",bestappr(L1*Pi^3/L4/sqd,B9)," a2=",bestappr(L2*Pi^2/L4,B9)," a3/sqd=",bestappr(L3*Pi/L4/sqd,B9));
        my(resid_q = abs(Rf - bestappr(Rf,B9)));
        my(resid_r = abs(Rf - bestappr(Rf/sqd,B9)*sqd));
        print("  resid_Q=",resid_q," resid_sqrtd=",resid_r);
        if(resid_q < 1e-50,
          print("  VERDICT d=67: Rf IN Q = ",bestappr(Rf,B9)),
          if(resid_r < 1e-50,
            print("  VERDICT d=67: Rf IN Q(sqrt(67))\\Q = (",bestappr(Rf/sqd,B9),")*sqrt(67)"),
            print("  VERDICT d=67: larger extension")
          )
        );
        print("  DONE_d67_j",j)
      )
    )
  )
}

\\=======================================================================
\\ --- d=163, N=163 ---
print("");
print("======================================================");
print("d=163 K=Q(sqrt(-163)) N=163 k=5 [Type IV, e_k=0]");
print("======================================================");
{
  my(N=163, k=5, d=163);
  my(sqd=sqrt(d));

  my(all_chars = znchars(163));
  for(i=1,#all_chars,
    my(idx=all_chars[i][1], ord=zncharorder(163,all_chars[i]));
    if(ord != 2, next);
    my(chi = znchar(Mod(idx, 163)));
    my(mf = mfinit([163, 5, chi], 1));
    my(B = mfeigenbasis(mf));
    print("chi=Mod(",idx,",163) ord=",ord," nforms=",#B);
    if(#B > 0,
      for(j=1,#B,
        my(fj=B[j]);
        print("  form j=",j," a2=",mfcoef(fj,2)," a3=",mfcoef(fj,3)," a5=",mfcoef(fj,5));
        my(Lobj = lfunmf(mf, fj));
        my(L1=lfun(Lobj,1), L2=lfun(Lobj,2), L3=lfun(Lobj,3), L4=lfun(Lobj,4));
        my(Rf = Pi*L1/L2);
        print("  L1=",L1," L2=",L2," L3=",L3," L4=",L4);
        print("  Rf=",Rf);
        print("  Rf_bestappr=",bestappr(Rf,B9));
        print("  Rf_over_sqrtd=",bestappr(Rf/sqd,B9));
        print("  boot: a1/sqd=",bestappr(L1*Pi^3/L4/sqd,B9)," a2=",bestappr(L2*Pi^2/L4,B9)," a3/sqd=",bestappr(L3*Pi/L4/sqd,B9));
        my(resid_q = abs(Rf - bestappr(Rf,B9)));
        my(resid_r = abs(Rf - bestappr(Rf/sqd,B9)*sqd));
        print("  resid_Q=",resid_q," resid_sqrtd=",resid_r);
        if(resid_q < 1e-50,
          print("  VERDICT d=163: Rf IN Q = ",bestappr(Rf,B9)),
          if(resid_r < 1e-50,
            print("  VERDICT d=163: Rf IN Q(sqrt(163))\\Q = (",bestappr(Rf/sqd,B9),")*sqrt(163)"),
            print("  VERDICT d=163: larger extension")
          )
        );
        print("  DONE_d163_j",j)
      )
    )
  )
}

print("");
print("======================================================");
print("M97 F2 v8 COMPLETE");
print("======================================================");
quit
