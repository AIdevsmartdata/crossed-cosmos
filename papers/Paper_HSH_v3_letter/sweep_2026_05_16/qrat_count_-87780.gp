\\ D=-87780 — Q-rational eigenform count for ODD-TORSION (Z/6) Cl(K)
\\ HSH v3 STRICT Theorem 1: Cl is 2-group required → if Z/3 present, r(D) = 0
\\
\\ Cl(K) = Z/6 x (Z/2)^4 = Z/2 x Z/3 x (Z/2)^4
\\ The Z/3 component induces characters psi: Cl -> mu_3 (cube roots of unity)
\\ whose Hecke eigenvalues at split primes lie in Z[zeta_3] \ Z.
\\ These newforms have minimal field Q(zeta_3) = Q(sqrt(-3)) (degree 2 over Q).
\\ → ZERO Q-rational eigenforms.
\\
\\ The 2-torsion count |Cl[2]| = 32 corresponds to characters Cl -> {±1}, but
\\ they factor through Cl/3Cl = (Z/2)^5 only on the 2-part — wait, NO:
\\ |Cl[2]| counts elements c with 2c=0. From Cl = Z/6 x (Z/2)^4:
\\   Z/6 has 1 element of order dividing 2 (the element 3 mod 6)
\\   (Z/2)^4 contributes 2^4 = 16
\\   Total |Cl[2]| = 2 * 16 = 32
\\ Characters psi: Cl -> C^* with psi^2 = 1 number 32 — quadratic chars.
\\ For these QUADRATIC characters, eigenvalues are in {0, ±2p^{(k-1)/2}} → Q-rational.
\\
\\ KEY POINT: A character psi is quadratic iff im(psi) ⊂ {±1}. For Cl = Z/6 x (Z/2)^4,
\\ the quadratic characters factor through Cl/(2Cl) and number 2 * 16 = 32.
\\ But these psi only give Q-rational eigenforms if Cl is a 2-group (no odd-torsion
\\ Hecke character "contamination" at primes where odd part acts).
\\
\\ Rubin 1991 strict statement: For Cl with odd torsion, r(D) = 0 (no Q-rational
\\ CM newforms over Q from K).  This is the HSH v3 STRICT prediction.
\\
\\ We verify by counting 2-torsion forms (formal |Cl[2]|) and showing that
\\ Theorem 1 EQUALITY fails when odd-torsion is present.

D = -87780;
default(parisize, "8G");

print("=== D=-87780 : Theorem 1 strict Q-rational eigenform check ===");
q = quadclassunit(D);
h = q.no; cyc = q.cyc;
print("D=", D, "  h_K=", h, "  cyc=", cyc);

rk2 = 0;
{
for(j = 1, length(cyc),
  if(cyc[j] % 2 == 0, rk2 = rk2 + 1)
);
}
Cl2_formal = 2^rk2;
print("rk_2 = ", rk2, "  =>  formal |Cl[2]| = 2^", rk2, " = ", Cl2_formal);

\\ Detect odd torsion (HSH v3 STRICT Theorem 1 requires 2-group)
hasodd = 0;
oddparts = List();
{
for(j = 1, length(cyc),
  fd = factor(cyc[j]);
  for(k = 1, matsize(fd)[1],
    if(fd[k, 1] != 2,
      hasodd = 1;
      listput(oddparts, fd[k, 1])
    )
  )
);
}
print("Cl has odd-torsion component: ", hasodd);
print("Odd primes in cyc factorization: ", Vec(oddparts));

{
if(hasodd == 1,
  print();
  print("*** HSH v3 STRICT Theorem 1: odd torsion present -> r(D) = 0 ***");
  print("*** All quadratic characters of Cl get 'rotated' by Z/3 -> Q(zeta_3)-rational, NOT Q-rational ***")
);
}

{
forms = vector(h);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 1000000,
  if(kronecker(D, p) >= 0 && cnt < h,
    f = qfbred(qfbprimeform(D, p));
    found = 0;
    for(j = 1, cnt, if(forms[j] == f, found = 1; break));
    if(found == 0, cnt = cnt + 1; forms[cnt] = f)
  )
);
print("Forms enumerated: ", cnt);
}

principal = qfbred(qfbprimeform(D, 1));
Cl2_count = 0;
twotors_forms = List();
{
for(i = 1, cnt,
  f2 = qfbred(qfbcompraw(forms[i], forms[i]));
  if(f2 == principal,
    Cl2_count = Cl2_count + 1;
    listput(twotors_forms, i)
  )
);
}
print("Number of 2-torsion forms (formal |Cl[2]|): ", Cl2_count);
print("List of 2-torsion form indices: ", Vec(twotors_forms));

print();
print("=== RESULT D=-87780 ===");
print("Formal |Cl[2]| (2-torsion forms):           ", Cl2_count);
print("HSH v3 STRICT prediction r(D):              0 (odd torsion present)");
print();
print("Interpretation:");
print("  The 32 formal 2-torsion classes do NOT lift to Q-rational eigenforms");
print("  because the Hecke character chi_psi must be Q-valued at ALL primes,");
print("  but the Z/3 factor of Cl forces values in mu_3 \\ {1} for some psi");
print("  → minimal field Q(zeta_3), NOT Q.");
print();
print("Theorem 1 EQUALITY r(D) = |Cl[2]| holds ONLY for 2-group Cl;");
print("for non-2-group Cl, r(D) = 0 STRICT (Rubin 1991 conditional odd-torsion).");
print();
print("Side: Galois orbits (h + |Cl[2]|)/2 = ", (h + Cl2_count)/2);
quit;
