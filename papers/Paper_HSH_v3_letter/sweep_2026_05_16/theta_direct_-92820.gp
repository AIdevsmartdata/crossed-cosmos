\\ D=-92820 theta-direct verification — HSH v3 OPUS rk_2=5 non-elementary anchor
\\ Cl(K) = Z/8 x Z/2 x Z/2 x Z/2 x Z/2,  h_K = 128,  rk_2 = 5
\\ Prediction: r(D) = |Cl(K)[2]| = 2^{rk_2} = 32 Q-rational eigenforms
\\ Note: h_K = 128 > 2^{rk_2} = 32 — non-elementary 2-group (Z/8 component)
\\ Galois-orbit prediction: distinct theta = (h + |Cl[2]|)/2 = (128 + 32)/2 = 80
\\ Template adapted from theta_direct_-7140.gp (verified 2026-05-15).

D = -92820;
default(parisize, "8G");

print("=== D=-92820 theta-direct (NEW rk_2=5 non-elementary anchor) ===");
q = quadclassunit(D);
print("D=", D, "  h_K=", q.no, "  cyc=", q.cyc);

\\ Enumerate the h_K = 128 reduced forms
{
forms = vector(q.no);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 1000000,
  if(kronecker(D, p) >= 0 && cnt < q.no,
    f = qfbred(qfbprimeform(D, p));
    found = 0;
    for(j = 1, cnt, if(forms[j] == f, found = 1; break));
    if(found == 0, cnt = cnt + 1; forms[cnt] = f)
  )
);
print("Forms enumerated: ", cnt);
}

\\ Compute theta-series coefficients up to N=120
print();
print("Computing theta-series coefficients (N=120) ...");
N = 120;
xmax = 80;
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
      dup = dup + 1
    )
  )
);
}
distinct = cnt - dup;

\\ Matrix-rank check: build the cnt x N theta-coeff matrix and rank it
print();
print("Computing rank of theta-coefficient matrix (", cnt, " x ", N, ") ...");
M = matrix(cnt, N);
{
for(i = 1, cnt, for(j = 1, N, M[i, j] = T[i, j]));
}
rk = matrank(M);
print("Matrix rank: ", rk);

\\ Final result
print();
print("=== RESULT D=-92820 ===");
print("Forms (h_K):                 ", cnt);
print("Distinct theta series:       ", distinct, " / ", cnt);
print("Theta-matrix rank:           ", rk);
print();
print("Predictions (HSH v3 OPUS / Theorem 1):");
print("  rats = |Cl[2]| = 2^rk_2 = 2^5 = 32");
print("  Galois orbits (h + |Cl[2]|)/2 = (128+32)/2 = 80");
print();
print("Observed distinct theta:                    ", distinct);
print("Observed rank:                              ", rk);
print("Theorem 1 predicted distinct (= orbits):    80");

{
if(distinct == 80 && rk == 80,
   print();
   print("*** Galois-orbit count = 80 matches refined formula (h+|Cl[2]|)/2 ***");
   print("*** Theorem 1 r(D) = |Cl[2]| = 32 verified separately via qrat_count_-92820.gp ***"),
   print();
   print("UNEXPECTED: distinct=", distinct, ", rank=", rk, " (predicted 80 = (128+32)/2) — analysis required"));
}
quit;
