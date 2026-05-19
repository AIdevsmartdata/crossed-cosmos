\\ D=-8580 theta-direct verification — HSH v3 OPUS rk_2=4 anchor
\\ Cl(K) = Z/4 x Z/2 x Z/2 x Z/2,  h_K = 32,  rk_2 = 4
\\ Prediction: rats = |Cl(K)[2]| = 2^{rk_2} = 16 distinct theta-series

D = -8580;
default(parisize, "4G");

print("=== D=-8580 theta-direct (NEW rk_2=4 anchor) ===");
q = quadclassunit(D);
print("D=", D, "  h_K=", q.no, "  cyc=", q.cyc);

{
forms = vector(q.no);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 200000,
  if(kronecker(D, p) >= 0 && cnt < q.no,
    f = qfbred(qfbprimeform(D, p));
    found = 0;
    for(j = 1, cnt, if(forms[j] == f, found = 1; break));
    if(found == 0, cnt = cnt + 1; forms[cnt] = f)
  )
);
print("Forms enumerated: ", cnt);
}

{
for(i = 1, cnt,
  v = Vec(forms[i]);
  print("  Q", i, " = (", v[1], ", ", v[2], ", ", v[3], ")")
);
}

print();
print("Computing theta-series coefficients (N=80) ...");
N = 80;
xmax = 50;
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

print();
print("First 12 theta coefficients per form:");
{
for(i = 1, cnt,
  s = Str("  Q", i, ": ");
  for(n = 1, 12, s = Str(s, T[i, n], " "));
  print(s)
);
}

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

print();
print("Computing rank of theta-coefficient matrix (", cnt, " x ", N, ") ...");
M = matrix(cnt, N);
{
for(i = 1, cnt, for(j = 1, N, M[i, j] = T[i, j]));
}
rk = matrank(M);
print("Matrix rank: ", rk);

print();
print("=== RESULT D=-8580 ===");
print("Forms (h_K):                 ", cnt);
print("Distinct theta series:       ", distinct, " / ", cnt);
print("Theta-matrix rank:           ", rk);
print();
print("Predictions:");
print("  HSH v3 OPUS (rats=2^rk_2 = 2^4 = 16):     16");
print("  Naive h_K (if no merging):                32");
print("Observed distinct theta:                    ", distinct);
print("Observed rank:                              ", rk);

{
if(distinct == 24 && rk == 24,
   print();
   print("*** Galois-orbit count = 24 matches refined formula (h+|Cl[2]|)/2 ***");
   print("*** Theorem 1 r(D) = |Cl[2]| = 16 verified separately via qrat_count_-8580.gp ***"),
   print();
   print("UNEXPECTED: distinct=", distinct, ", rank=", rk, " (predicted 24 = (32+16)/2) — analysis required"));
}
quit;
