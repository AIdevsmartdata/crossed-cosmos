\\ D=-5460 theta-direct v5 — proper {} wrapping for multi-line blocks
\\ Theorem 1: rats = 2^{rk_2} = 2^4 = 16 expected for Cl((Z/2)^4)
D = -5460;
default(parisize, "4G");

print("=== D=-5460 theta-direct v5 ===");
q = quadclassunit(D);
print("D=", D, "  h_K=", q.no, "  cyc=", q.cyc);

\\ Enumerate the 16 reduced forms
{
forms = vector(q.no);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 100000,
  if(kronecker(D, p) >= 0 && cnt < q.no,
    f = qfbred(qfbprimeform(D, p));
    found = 0;
    for(j = 1, cnt, if(forms[j] == f, found = 1; break));
    if(found == 0, cnt = cnt + 1; forms[cnt] = f)
  )
);
print("Forms enumerated: ", cnt);
}

\\ Display form coefficients
{
for(i = 1, cnt,
  v = Vec(forms[i]);
  print("  Q", i, " = (", v[1], ", ", v[2], ", ", v[3], ")")
);
}

\\ Compute theta-series coefficients up to N=80
print();
print("Computing theta-series coefficients (N=80) ...");
N = 80;
xmax = 40;
T = matrix(cnt, N);
{
for(i = 1, cnt,
  v = Vec(forms[i]);
  A = v[1]; B = v[2]; C = v[3];
  for(x = -xmax, xmax,
    for(y = -xmax, xmax,
      n = A*x^2 + B*x*y + C*y^2;
      if(n >= 1 && n <= N, T[i, n] = T[i, n] + 1)
    )
  )
);
}
print("Theta computation done.");

\\ Display first 12 coefficients
print();
print("First 12 theta coefficients per form:");
{
for(i = 1, cnt,
  s = Str("  Q", i, ": ");
  for(n = 1, 12, s = Str(s, T[i, n], " "));
  print(s)
);
}

\\ Pairwise distinctness check
print();
print("Pairwise distinctness check (using all ", N, " coeffs)...");
dup = 0;
{
for(i = 2, cnt,
  for(j = 1, i - 1,
    same = 1;
    for(k = 1, N, if(T[i, k] != T[j, k], same = 0; break));
    if(same == 1,
      dup = dup + 1;
      print("  DUPLICATE: Q", i, " == Q", j)
    )
  )
);
}
distinct = cnt - dup;

\\ Final result
print();
print("=== RESULT ===");
print("Forms (h_K):           ", cnt);
print("Distinct theta series: ", distinct, " / ", cnt);
print();
print("Predictions:");
print("  Theorem 1 (rats = 2^rk_2 = 2^4):      16");
print("  Alt working draft 2^(rk_2(rk_2+1)/2): 1024");
print("  Atkin-Lehner partial 2^(rk_2+1):      32");
print("Observed distinct theta:                ", distinct);

if(distinct == 16,
  print();
  print("*** Theorem 1 CONFIRMED: rats = 16 = 2^{rk_2=4} ***");
  print("*** Formula validated for rk_2 in {0,2,3,4} ***"),
  print();
  print("UNEXPECTED rats = ", distinct, " — requires further analysis")
);
quit;
