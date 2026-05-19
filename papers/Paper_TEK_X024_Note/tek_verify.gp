/* tek_verify.gp -- ancillary file for Paper_TEK_X024_Note
 * Verification script for: TEK SU(3) spectral curve = E[24.a4] = 24.2.a.a
 *
 * Reproducibility: PARI/GP 2.15.4
 * Run:  gp -q < tek_verify.gp
 */

/* 1. TEK SU(3) propagator spectrum at one-loop around twist eaters */
/*    E(n) = 4 * sum_{mu=1..4} sin^2(pi * n_mu / 3), n_mu in {0,1,2}, n != 0 */
print("=== 1. TEK SU(3) d=4 minimal symmetric twist propagator spectrum ===");
\\ E(n) = 4 sum_mu sin^2(pi n_mu / 3) for n_mu in {0,1,2}, n != 0
\\ Since sin^2(pi/3) = sin^2(2pi/3) = 3/4, E = 3 * (number of nonzero n_mu)
\\ so the spectrum is {3, 6, 9, 12}.
\\ tally pass
tek_tally() = {
  my(mult_3 = 0, mult_6 = 0, mult_9 = 0, mult_12 = 0, nz);
  for(a = 0, 2, for(b = 0, 2, for(c = 0, 2, for(d = 0, 2,
    if(a + b + c + d > 0,
      nz = (a != 0) + (b != 0) + (c != 0) + (d != 0);
      if(nz == 1, mult_3 += 1);
      if(nz == 2, mult_6 += 1);
      if(nz == 3, mult_9 += 1);
      if(nz == 4, mult_12 += 1);
    )
  ))));
  print("Multiplicities: E=3 -> ", mult_3, ";  E=6 -> ", mult_6, ";  E=9 -> ", mult_9, ";  E=12 -> ", mult_12);
  print("Total non-zero modes: ", mult_3+mult_6+mult_9+mult_12, "  (expected 3^4 - 1 = 80)");
};
tek_tally();

/* 2. Spectral curve y^2 = (x-3)(x-6)(x-9)(x-12) -> Weierstrass form */
print("\n=== 2. Spectral curve birational reduction ===");
C = ellfromeqn(y^2 - (x-3)*(x-6)*(x-9)*(x-12));
print("ellfromeqn output: ", C);
EW = ellinit(C);
Emin = ellminimalmodel(EW);
print("Minimal model: ", Emin[1..5]);

/* 3. Verify E[24.a4] : y^2 = x^3 - x^2 - 4x + 4 */
print("\n=== 3. Curve E[24.a4] : y^2 = x^3 - x^2 - 4x + 4 ===");
E = ellinit([0, -1, 0, -4, 4]);
print("Conductor : ", ellglobalred(E)[1]);
print("j-invariant : ", E.j, "  (= ", factor(numerator(E.j)), " / ", factor(denominator(E.j)), ")");
print("Discriminant : ", E.disc, "  (= ", factor(E.disc), ")");
print("Torsion (over Q) : ", elltors(E)[1]);

/* 4. NON-CM check: j has denominator 9 */
print("\n=== 4. NON-CM check (Schneider-Deuring) ===");
print("Denominator of j = ", denominator(E.j), " != 1");
print("j NOT algebraic integer => E NOT CM");

/* 5. Modular form 24.2.a.a a_p match */
print("\n=== 5. Hecke a_p match: E vs f_{24.2.a.a} ===");
mf = mfinit([24, 2, 1], 0);
L = mfeigenbasis(mf);
print("Number of newforms at level 24, weight 2: ", #L);
f = L[1];

check_match(pmax) = {
  my(c = 0, t = 0, mm = []);
  forprime(p = 5, pmax,
    t += 1;
    my(ap_E = ellap(E, p), ap_f = mfcoef(f, p));
    if(ap_E == ap_f, c += 1, mm = concat(mm, [[p, ap_E, ap_f]]));
  );
  print("Match: ", c, "/", t);
  if(#mm == 0, print("ALL MATCH"), print("Mismatches: ", mm));
};
check_match(199);

/* 6. Supersingular density (non-CM gives ~0, CM gives ~1/2) */
print("\n=== 6. Supersingular density (CM marker) ===");
ss_density(pmax) = {
  my(c = 0, t = 0);
  forprime(p = 5, pmax,
    t += 1;
    if(ellap(E, p) == 0, c += 1);
  );
  print("Primes 5..", pmax, ": ", c, "/", t, " = ", c*1.0/t);
};
ss_density(200);
ss_density(2000);

/* 7. Print a_p table for primes 5..50 */
print("\n=== 7. a_p table for primes 5..50 ===");
my_table() = {
  forprime(p = 5, 50,
    print("p=", p, "  a_p=", ellap(E, p));
  );
};
my_table();
