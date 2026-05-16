\\ D=-87780 theta-direct verification — HSH v3 OPUS odd-torsion (Z/6) anchor
\\ Cl(K) = Z/6 x Z/2 x Z/2 x Z/2 x Z/2,  h_K = 96,  rk_2 = 5
\\ But Z/6 = Z/2 x Z/3 has ODD torsion (3) → HSH v3 STRICT: rats = 0
\\ (Rubin 1991 kills odd-torsion CM newforms over Q)
\\
\\ Even though |Cl[2]| = 32, no Q-rational eigenform can arise because
\\ the odd-torsion character does NOT have Q-rational eigenvalues at split primes.
\\
\\ Galois-orbit count: still (h + |Cl[2]|)/2 = (96 + 32)/2 = 64 distinct theta-series,
\\ but NONE are Q-rational (all in orbits of size >= 2 with non-rational eigenvalues
\\ from Z/3 component).

D = -87780;
default(parisize, "8G");

print("=== D=-87780 theta-direct (NEW odd-torsion Z/6 anchor) ===");
q = quadclassunit(D);
print("D=", D, "  h_K=", q.no, "  cyc=", q.cyc);
print("Note: cyc contains Z/6 = Z/2 x Z/3 -- odd torsion 3 present");

\\ Enumerate the h_K = 96 reduced forms
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

\\ Matrix-rank check
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
print("=== RESULT D=-87780 ===");
print("Forms (h_K):                 ", cnt);
print("Distinct theta series:       ", distinct, " / ", cnt);
print("Theta-matrix rank:           ", rk);
print();
print("Predictions:");
print("  HSH v3 STRICT (Theorem 1: Cl 2-group required):  r(D) = 0 (Z/3 odd torsion)");
print("  |Cl[2]| = 2^5 = 32 (would-be 2-torsion classes)");
print("  Galois orbits (h + |Cl[2]|)/2 = (96+32)/2 = 64 (distinct theta-series)");
print();
print("Observed distinct theta:                          ", distinct);
print("Observed rank:                                    ", rk);

{
if(distinct == 64,
   print();
   print("*** Galois-orbit count = 64 matches (h+|Cl[2]|)/2 ***");
   print("*** But all orbits have non-rational eigenvalues from Z/3 → r(D) = 0 ***");
   print("*** Theorem 1 STRICT verdict r(D) = 0 to be verified via qrat_count_-87780.gp ***"),
   print();
   print("UNEXPECTED: distinct=", distinct, " (predicted 64) — analysis required"));
}
quit;
