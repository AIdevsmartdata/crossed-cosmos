default(realprecision, 80);
mf = mfinit([4,5,-4], 0);
F = mfeigenbasis(mf);
f = F[1];
Lf = lfunmf(mf, f);
Lv2 = lfun(Lf, 2);
printf("L(f,2)              = %.40Pf\n", Lv2);

\\ Hurwitz/lemniscate period: omega_lem = Gamma(1/4)^2 / (2*sqrt(2*pi))
\\ But more standard: omega_1 = real period of E:y^2=x^3-x = 2*ellelliptic1stkind ...
\\ Let's compute via PARI's elliptic curve API

E = ellinit([0, 0, 0, -1, 0]);  \\ y^2 = x^3 - x
print("E periods: ", E.omega);
om1 = abs(real(E.omega[1]));
printf("om_real = %.40Pf\n", om1);
om2 = abs(imag(E.omega[2]));
printf("om_imag = %.40Pf\n", om2);

\\ Try alpha_2 with various periods
printf("Pi^2 = %.40Pf\n", Pi^2);
test1 = Lv2 * Pi^2 / om1^4;
printf("L(f,2)*pi^2/om_real^4 = %.30Pf  (1/12=%.30Pf)\n", test1, 1.0/12);
printf("ratio = %.20Pf\n", test1 * 12);

\\ Hurwitz constant ϖ = Gamma(1/4)^2 / (2*sqrt(2*pi))
varpi = gamma(1/4)^2 / (2 * sqrt(2*Pi));
printf("varpi (Hurwitz) = %.40Pf\n", varpi);
test2 = Lv2 * Pi^2 / varpi^4;
printf("L(f,2)*pi^2/varpi^4 = %.30Pf\n", test2);
printf("test2 * 12 = %.20Pf\n", test2 * 12);

\\ Try om1 / 2 (half-period), 2*om1 (double)
for(c = 1, 4,
  oc = om1 / c;
  tc = Lv2 * Pi^2 / oc^4;
  printf("L(f,2)*pi^2/(om_real/%d)^4 = %.20Pf  ratio*12 = %.10Pf\n", c, tc, tc*12);
);

\\ Maybe omega_1 should be 2*om1 or 2*omega_+ in Hecke convention
om_plus = real(E.omega[1]);  \\ in PARI ω_1 is real
om_minus = imag(E.omega[2]); \\ ω_2 has imag part, ω_2 = i*ω_+/AGM stuff
printf("E.omega[1] = %s\n", E.omega[1]);
printf("E.omega[2] = %s\n", E.omega[2]);
quit;
