default(parisize, "4G");
default(realprecision, 50);

\\ All h=2 fundamental disc, scan for rational weight-5 newforms with chi_D
h2_list = [-15, -20, -24, -35, -40, -51, -52, -88, -91, -115, -123, -148, -187, -232, -235, -267, -403, -427];

testD(D) = {
  my(mf, F, f, cf, found = 0, base);
  base = -D;
  print("=== D=", D, " h=2 ===");
  for(mi = 1, 7,
    N = base * mi;
    if(N > 1500, next);
    err = iferr(mf = mfinit([N, 5, D], 0); dimm = mfdim(mf), E0, -1);
    if(err == -1, next);
    if(dimm == 0, next);
    F = mfeigenbasis(mf);
    if(#F == 0, next);
    for(fi = 1, #F,
      f = F[fi];
      cf = mfcoefs(f, 30);
      if(type(cf[2]) == "t_INT",
        printf("  N=%d fi=%d a_2..a_5 = %s\n", N, fi, vector(4, j, cf[2+j]));
        found = 1;
      );
    );
  );
  if(found == 0, print("  no rational found"));
};

for(li = 1, #h2_list, testD(h2_list[li]));
quit;
