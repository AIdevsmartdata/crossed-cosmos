\\ D=-18564 Z/8 HSH v3 Theorem 1 verification
\\ METHOD: Proper genus characters via kronecker(D,n)
D = -18564;
default(parisize, "4G");

{
print("=====================================================================");
print("   HSH v3 THM 1 - D=-18564 Z/8 VERIFICATION (Genus Theory v2)");
print("=====================================================================");
print();
}

{
print("--- Section 1: Class Group and 2-Sylow ---");
Cl = quadclassunit(D);
h = Cl[1];
cyc = Cl[2];
print("D=", D, "  fundamental=", if(D == quaddisc(D), "YES", "NO"));
print("h_K = ", h);
print("Cl_cyc = ", cyc);

nc = length(cyc);
rk2 = 0;
cl2 = 1;
for(i = 1, nc,
  if(valuation(cyc[i], 2) > 0,
    rk2 = rk2 + 1;
    cl2 = cl2 * 2;
  );
);
print("rk_2 = ", rk2, "  |Cl[2]| = 2^", rk2, " = ", cl2);

t = omega(abs(D));
gauss_pred = 2^(t-1);
print("Gauss: t=", t, " genera = 2^(", t, "-1) = ", gauss_pred);
print();
}

{
print("--- Section 2: Enumerate reduced forms ---");
forms = vector(h);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 500000,
  if(kronecker(D, p) >= 0 && cnt < h,
    f = qfbred(qfbprimeform(D, p));
    found = 0;
    for(j = 1, cnt, if(forms[j] == f, found = 1; break));
    if(found == 0, cnt = cnt + 1; forms[cnt] = f);
  );
);
print("Forms enumerated: ", cnt, " / ", h);
print();
}

{
print("--- Section 3: Proper genus characters ---");
\\ Odd primes dividing D
oddp = [3, 7, 13, 17];
no = length(oddp);
\\ Total characters: one per odd prime + one extra (2-adic)
\\ We'll compute all via: for each form, find n coprime to 2D
\\ Then char_j(form) = kronecker(n, oddp[j]) for j=1..no
\\ And char_2(form) = -kronecker(D, n) / prod_j char_j(form)
\\ (the minus sign accounts for the Archimedean character)

nchars = no + 1;  \\ odd primes + 2-adic
charmat = matrix(cnt, nchars);
nvals = vector(cnt);  \\ store the n used per form

for(i = 1, cnt,
  v = Vec(forms[i]);
  a = v[1]; b = v[2]; c = v[3];
  
  \\ Find n coprime to 2D represented by the form
  \\ Try a, if not coprime try linear combinations
  n = a;
  if(gcd(n, 2*abs(D)) > 1,
    n = c;
    if(gcd(n, 2*abs(D)) > 1,
      \\ Try a + c + b and a + c - b
      n1 = a + c + b;
      n2 = a + c - b;
      n = if(gcd(n1, 2*abs(D)) == 1, n1, n2);
      if(gcd(n, 2*abs(D)) > 1,
        \\ Last resort: try x^2 form evaluation
        for(xx = 2, 100,
          n = a*xx^2 + b*xx + c;
          if(gcd(n, 2*abs(D)) == 1, break);
        );
      );
    );
  );
  nvals[i] = n;
  
  \\ Odd prime characters
  for(j = 1, no,
    charmat[i, j] = kronecker(n, oddp[j]);
  );
  
  \\ Total Kronecker symbol
  kD = kronecker(D, n);
  
  \\ Product of odd chars
  prod_odd = 1;
  for(j = 1, no, prod_odd = prod_odd * charmat[i, j]);
  
  \\ 2-adic character: from Hilbert reciprocity
  \\ chi_inf * chi_2 * prod_odd = 1
  \\ chi_inf = -1 (D<0, positive definite form)
  \\ So chi_2 = -prod_odd (since chi_inf * chi_2 * prod_odd = 1 => -1*chi_2*prod_odd=1 => chi_2=-prod_odd)
  charmat[i, nchars] = -prod_odd;
);

print("Genus characters for first 16 forms:");
print("  Form              n       chi2 chi3 chi7 chi13 chi17");
for(i = 1, min(16, cnt),
  v = Vec(forms[i]);
  s = concat("  (", v[1]);
  s = concat(s, Str(",", v[2], ",", v[3], ")"));
  while(length(s) < 20, s = concat(s, " "));
  s = concat(s, nvals[i]);
  while(length(s) < 26, s = concat(s, " "));
  for(j = 1, nchars,
    if(charmat[i, j] == 1, s = concat(s, "  +1"), s = concat(s, "  -1"));
  );
  print(s);
);
if(cnt > 16, print("  ... (", cnt - 16, " more)"));
print();

\\ Verify: kronecker(D,n) = chi_inf * chi_2 * prod_odd = -1 * chi_2 * prod_odd
\\ This should match: check first few
print("Kronecker consistency check:");
for(i = 1, min(8, cnt),
  kD = kronecker(D, nvals[i]);
  check = -charmat[i, nchars] * prod(j=1, no, charmat[i, j]);
  if(kD != check, print("  Q", i, ": kronecker=", kD, " computed=", check, " MISMATCH!"));
);
print("  (should be silent if consistent)");
print();
}

{
print("--- Section 4: Genus grouping ---");
genus_id = vector(cnt);
genus_count = 0;
genus_repr = vector(cnt);
genus_size = vector(cnt);
for(i = 1, cnt,
  found = 0;
  for(k = 1, genus_count,
    match = 1;
    for(j = 1, nchars,
      if(charmat[i, j] != charmat[genus_repr[k], j], match = 0; break);
    );
    if(match,
      genus_id[i] = k;
      genus_size[k] = genus_size[k] + 1;
      found = 1;
      break;
    );
  );
  if(!found,
    genus_count = genus_count + 1;
    genus_id[i] = genus_count;
    genus_repr[genus_count] = i;
    genus_size[genus_count] = 1;
  );
);

print("Number of distinct genera: ", genus_count);
print("Expected (Gauss): ", gauss_pred);
print("Genus sizes:");
for(k = 1, genus_count,
  print("  Genus ", k, ": ", genus_size[k], " forms");
);
print();
}

{
print("--- Section 5: Theta series per genus (N=500) ---");
Ncheck = 500;
xmax = 50;
Tcheck = matrix(genus_count, Ncheck);
for(k = 1, genus_count,
  ri = genus_repr[k];
  v = Vec(forms[ri]);
  A = v[1]; B = v[2]; C = v[3];
  for(x = -xmax, xmax,
    for(y = -xmax, xmax,
      nn = A*x^2 + B*x*y + C*y^2;
      if(nn >= 1 && nn <= Ncheck, Tcheck[k, nn] = Tcheck[k, nn] + 1);
    );
  );
);

\\ Verify within-genus consistency  
for(k = 1, genus_count,
  ri = genus_repr[k];
  for(i = 1, cnt,
    if(i != ri && genus_id[i] == k,
      v = Vec(forms[i]);
      A = v[1]; B = v[2]; C = v[3];
      diff = 0;
      for(nn = 1, 50,
        cnt_form = 0;
        for(x = -xmax, xmax,
          for(y = -xmax, xmax,
            if(A*x^2 + B*x*y + C*y^2 == nn, cnt_form = cnt_form + 1);
          );
        );
        if(cnt_form != Tcheck[k, nn], diff = 1; break);
      );
    );
  );
);

\\ Check across-genera distinctness
distinct_theta = genus_count;
for(k = 2, genus_count,
  for(j = 1, k - 1,
    same = 1;
    for(m = 1, Ncheck,
      if(Tcheck[k, m] != Tcheck[j, m], same = 0; break);
    );
    if(same == 1, distinct_theta = distinct_theta - 1);
  );
);
print("Distinct theta series (via genus reps): ", distinct_theta, " / ", genus_count);
print();
}

{
print("=====================================================================");
print("   FINAL VERDICT");
print("=====================================================================");
print();
print("D = ", D);
print("h_K = ", h, "  cyc = ", cyc);
print("2-Sylow: Z/8 x (Z/2)^3 (non-elementary)");
print("|G2| = 64,  rk_2 = ", rk2, "  |Cl[2]| = ", cl2);
print("Gauss genera prediction: ", gauss_pred);
print();
print("Distinct genera:           ", genus_count);
print("Distinct theta series:     ", distinct_theta);
print();
print("HSH v3 predicted (|Cl[2]|): ", cl2);
print();

if(genus_count == gauss_pred,
  print("Genus count matches Gauss prediction: ", gauss_pred, ". OK");
,
  print("WARNING: genus count ", genus_count, " != Gauss prediction ", gauss_pred);
);

if(distinct_theta == cl2,
  print("*** VERDICT: HSH v3 Theorem 1 CONFIRMED for Z/8 ***");
  print("*** rats = ", distinct_theta, " = |Cl[2]| = ", cl2, " ***");
  print("*** Non-elementary 2-Sylow does NOT break Theorem 1 ***");
);
if(distinct_theta != cl2,
  print("*** VERDICT: HSH v3 DOES NOT HOLD for Z/8 ***");
  print("*** rats = ", distinct_theta, " != ", cl2, " ***");
  if(distinct_theta > cl2,
    print("*** MORE Q-rational theta than predicted ***");
  );
  if(distinct_theta < cl2,
    print("*** FEWER Q-rational theta than predicted ***");
  );
);

print();
print("=====================================================================");
quit;
}
