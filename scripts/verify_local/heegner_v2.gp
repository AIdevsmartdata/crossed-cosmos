default(parisize, "8G");
default(parisizemax, "32G");
default(realprecision, 80);

testK(D, curves, levels) = {
  my(E, om, mf, F, f, cf, Lf, Lv, alpha, ba, diff, found_rat = 0);
  for(ci = 1, #curves,
    E = ellinit([0, 0, 0, curves[ci][1], curves[ci][2]]);
    om = abs(real(E.omega[1]));
    print("D=", D, " curve=[", curves[ci][1], ",", curves[ci][2], "] om=", om);
    for(li = 1, #levels,
      N = levels[li];
      err = iferr(mf = mfinit([N, 5, D], 0); dimm = mfdim(mf), E0, -1);
      if(err == -1, next);
      if(dimm == 0, next);
      F = mfeigenbasis(mf);
      if(#F == 0, next);
      for(fi = 1, #F,
        f = F[fi];
        cf = mfcoefs(f, 30);
        if(type(cf[2]) == "t_INT",
          Lf = lfunmf(mf, f);
          Lv = lfun(Lf, 2);
          alpha = Lv * Pi^2 / om^4;
          ba = bestappr(alpha, 1000);
          diff = abs(alpha - ba*1.0);
          if(diff < 10^(-50),
            printf("  ★ N=%d: alpha = %s EXACT (diff=%.2Pe, dim=%d)\n", N, ba, diff, dimm);
            found_rat = 1;
          );
        );
      );
    );
  );
  if(found_rat == 0, print("  No exact rational found"));
  print("");
};

\\ Heegner h=1 K with multiple curve candidates per K
testK(-8, [[-2, 0], [-4, 0], [4, 0]], [4, 8, 16, 32, 64, 128, 256]);
testK(-11, [[-264, 1694], [-1056, 13552]], [11, 22, 44, 88, 121, 484]);
testK(-19, [[-152, 722], [-608, 5776]], [19, 38, 76, 152, 361]);
testK(-43, [[-3440, 77658]], [43, 86, 172, 1849]);
testK(-67, [[-29480, 1948226]], [67, 134, 268, 4489]);

\\ Q(√-3) more curves
testK(-3, [[0, 1], [0, -1]], [3, 9, 12, 27, 36, 108]);

\\ Q(i) more levels
testK(-4, [[-1, 0]], [4, 16, 32, 64, 100, 144, 256, 196]);

quit;
