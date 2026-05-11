\\ PARI/GP script for m184 mechanism test
\\ For each class‑number‑1 discriminant D in {-7,-11,-19,-43,-67,-163}
\\ compute ord_2 of the discriminant of the quadratic form
\\    Q(x,y) = a x^2 + b x y + c y^2,
\\ where a,b,c are derived from the period basis (omega1, omega2) of the
\\ minimal Weierstrass model for the associated Heegner elliptic curve.
\\ Compare the obtained v2(discriminant) with the c^4 pattern:
\\    c^4 = 4   →  v2 = 2  (expected for D = -11, -19)
\\    c^4 = 1   →  v2 = 0  (expected for D = -7, -43, -67, -163)

default(realprecision,200);

{
TestDs = [-7, -11, -19, -43, -67, -163];
for(i = 1, #TestDs,
  D = TestDs[i];

  \\ Heegner point
  if(D % 4 == 1,
    tau = (1 + sqrt(D)) / 2;
  ,
    tau = sqrt(D) / 2;
  );
  jinv = ellj(tau);
  E = ellinit(ellfromj(jinv));

  per = ellperiods(E);
  om1 = per[1];
  om2 = per[2];

  a = (om1*conj(om1)).real;
  c = (om2*conj(om2)).real;
  b = 2 * (om1*conj(om2)).real;

  disc = b^2 - 4*a*c;                    \\ discriminant of Q
  drat = -disc;                          \\ work with positive rational
  dnum = numerator(drat);
  dden = denominator(drat);
  v2 = valuation(dnum, 2) - valuation(dden, 2);

  expected = if(D == -11 || D == -19, 2, 0);
  printf("D = %5d   v2(disc) = %d   expected = %d   %s\n",
         D, v2, expected, if(v2 == expected, "PASS", "FAIL"));
);
}
