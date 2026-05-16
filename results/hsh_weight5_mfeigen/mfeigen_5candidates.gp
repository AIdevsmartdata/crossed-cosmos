\p 200
default(parisize, 2^33)
default(parisizemax, 2^33)

/* Helper: print first coefficients for one eigenform */
printcoeffs(f) = {
  local(v);
  v = mfcoefs(f, 5);
  print("  a(1)=", v[2], " a(2)=", v[3], " a(3)=", v[4], " a(4)=", v[5], " a(5)=", v[6]);
}

/* Process one discriminant for weight-5 */
process(D) = {
  local(N, G, chi, m, chi_mod, mf3, dim3, mf5, dim5, basis, nb);
  
  N = abs(D);
  print("=== D=", D, " (N=", N, ") ===");
  t0 = getwalltime();
  
  /* Construct Kronecker character */
  G = znstar(N, 1);
  chi_exp = znchar(D)[2];
  m = znconreyexp(G, chi_exp);
  chi_mod = Mod(m, N);
  
  /* weight-3 (reference) */
  mf3 = mfinit([N, 3, chi_mod], 0);
  dim3 = mfdim(mf3);
  print("  weight-3 dim=", dim3);
  
  /* weight-5 */
  mf5 = mfinit([N, 5, chi_mod], 0);
  dim5 = mfdim(mf5);
  print("  weight-5 dim=", dim5);
  
  if(dim5 <= 0, print("  NO weight-5 eigenforms"));
  if(dim5 <= 0, return(0));
  
  basis = mfeigenbasis(mf5);
  nb = #basis;
  print("  #eigenforms=", nb);
  
  /* Print first 3 eigenforms (max) */
  if(nb > 3, print("  (showing first 3 of ", nb, ")"));
  for(j=1, min(nb, 3), printcoeffs(basis[j]));
  
  t1 = getwalltime();
  printf("  Time: %.1f s\n", (t1-t0)/1000.);
}

/* Main */
candidates = [-260, -280, -356, -404, -420];
print("=== V4 -- Weight-5 mfeigenbasis scan ===");
print("Candidates: ", candidates);
print("MEM: parisize=", default(parisize)/2^20, "MB parisizemax=", default(parisizemax)/2^20, "MB");
print("");

t_total = getwalltime();
for(i=1, #candidates, process(candidates[i]));

printf("\nTotal time: %.1f s\n", (getwalltime()-t_total)/1000.);
print("=== DONE ===");
