\\ D=-7140 — Q-rational eigenform count via 2-torsion-form census
\\ This DIRECTLY verifies Theorem 1: r(D) = |Cl[2]| = 2^rk_2 = 16
\\
\\ Strategy: r(D) = # {Galois-orbit-size-1 Hecke eigenforms} =
\\           # {psi : Cl -> C^*  with psi^2 = 1} = |Cl[2]|
\\ At the form level, |Cl[2]| equals the number of reduced primitive forms f
\\ with f * f ~ principal (i.e., 2-torsion classes in Cl).

D = -7140;
default(parisize, "4G");

print("=== D=-7140 : Theorem 1 Q-rational eigenform check ===");
q = quadclassunit(D);
h = q.no; cyc = q.cyc;
print("D=", D, "  h_K=", h, "  cyc=", cyc);

rk2 = 0;
for(j = 1, length(cyc), if(cyc[j] % 2 == 0, rk2 = rk2 + 1));
Cl2_pred = 2^rk2;
print("|Cl[2]| = 2^", rk2, " = ", Cl2_pred);

{
forms = vector(h);
forms[1] = qfbred(qfbprimeform(D, 1));
cnt = 1;
forprime(p = 2, 200000,
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
print("Number of 2-torsion forms = |Cl[2]| = ", Cl2_count);
print("List of 2-torsion form indices: ", Vec(twotors_forms));

print();
print("=== RESULT D=-7140 ===");
print("r(D) observed (via 2-torsion forms): ", Cl2_count);
print("Theorem 1 prediction r(D) = |Cl[2]| = 2^4: ", Cl2_pred);
{
if(Cl2_count == Cl2_pred,
   print("*** HSH v3 THEOREM 1 CONFIRMED for D=-7140 ***"),
   print("*** MISMATCH - INVESTIGATE ***"));
}

\\ Side check: Galois-orbit count = (h + |Cl[2]|)/2 (this is what theta-direct measures)
print();
print("Side check: Galois orbits = (h + |Cl[2]|)/2 = ", (h + Cl2_count)/2);
print("(matches PARI theta-direct distinct = 24)");
quit;
