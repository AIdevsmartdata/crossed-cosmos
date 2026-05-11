\\ PARI/GP script for m183 full proof test
\\ For each class-number‑1 discriminant D in {-4,-3,-7,-11,-19,-43,-67,-163}
\\ compute alpha_2 = L(f,2)*Pi^2 / Omega^4, where f is the rational CM weight‑5
\\ newform of level |D| (for D=-3, level 12 with conductor‑4 character) and
\\ Omega is the real period of the associated Heegner elliptic curve.
\\ Print the rational alpha_2 and verify that its denominator contains 3 iff D ≡ 2 (mod 3).

default(realprecision,200);

{
TestDs = [-4, -3, -7, -11, -19, -43, -67, -163];
for(i = 1, #TestDs,
  D = TestDs[i];

  if(D == -4,
    N = 4;
    G = DirGroup(N);
    chiIdx = -1;
    for(j = 1, #G,
      c = G[j];
      ok = 1;
      forprimestep(p = 2, 11,
        if(gcd(p, N) > 1, next);
        if(chareval(G, c, p) != kronecker(-4, p), ok = 0; break);
      );
      if(ok, chiIdx = j; break);
    );
    chi = G[chiIdx];
    tau = sqrt(-4)/2;          \\ tau = i
  , D == -3,
    N = 12;
    G12 = DirGroup(12);
    chiIdx = -1;
    for(j = 1, #G12,
      c = G12[j];
      ok = 1;
      forprimestep(p = 2, 11,
        if(gcd(p, 12) > 1, next);
        if(chareval(G12, c, p) != kronecker(-4, p), ok = 0; break);
      );
      if(ok, chiIdx = j; break);
    );
    chi = G12[chiIdx];
    tau = (1+sqrt(D))/2;        \\ tau = (1+sqrt(-3))/2
  ,
    N = abs(D);
    G = DirGroup(N);
    chiIdx = -1;
    for(j = 1, #G,
      c = G[j];
      ok = 1;
      forprimestep(p = 2, 11,
        if(gcd(p, N) > 1, next);
        if(chareval(G, c, p) != kronecker(D, p), ok = 0; break);
      );
      if(ok, chiIdx = j; break);
    );
    chi = G[chiIdx];
    if(D % 4 == 1,
      tau = (1+sqrt(D))/2;
    ,
      tau = sqrt(D)/2;
    );
  );

  \\ Heegner elliptic curve
  jinv = ellj(tau);
  E = ellinit(ellfromj(jinv));
  Om = ellperiods(E)[1];          \\ real half‑period

  \\ weight‑5 newform and L‑function
  mf = mfinit([N, 5, chi]);
  F = mfeigenbasis(mf)[1];
  Lf = lfunmf(mf, F);
  lv = lfun(Lf, 2);

  alpha = lv * Pi^2 / Om^4;
  a_r = bestappr(alpha, 10^117);
  den = denominator(a_r);
  expect3 = (D % 3) == 2;
  has3   = (den % 3) == 0;
  ok = if(has3, expect3, !expect3);

  printf("D=%5d  alpha_2 = %s\n", D, a_r);
  printf("       denominator = %d, contains 3: %s, expected: %s  → %s\n",
         den, if(has3, "yes", "no"), if(expect3, "yes", "no"),
         if(ok, "PASS", "FAIL"));
);
}
