\\ diag_conductor.gp -- diagnose analytic conductor for 4.5.b.a
\\ Run: gp -q < diag_conductor.gp
default(parisize, 256000000);
default(realbitprecision, 64);

print("=== Conductor diagnostic for 4.5.b.a ===");
mf = mfinit([4, 5, Mod(3,4)], 1);
F  = mfeigenbasis(mf);
f  = F[1];

\\ Build L-data and inspect
ldata = lfunmf(mf, f);
print("ldata type: ", type(ldata));

\\ lfuninit at small T to get lf object
lf = lfuninit(ldata, [50]);
print("lf type: ", type(lf));

\\ Try lfunconductor
c = lfunconductor(lf);
print("lfunconductor(lf) = ", c);

\\ Try lfunan (analytic conductor)
an = lfunan(lf);
print("lfunan(lf) = ", an);

\\ Examine ldata components directly
print("ldata[1] (conductor?) = ", ldata[1]);
print("ldata[2] (Gamma factors?) = ", ldata[2]);
print("ldata[3] (weight?) = ", ldata[3]);
print("ldata[4] (epsilon?) = ", ldata[4]);

\\ Count zeros in [0,50] and [0,200]
z50  = lfunzeros(lf, [0, 50]);
lf200 = lfuninit(ldata, [200]);
z200 = lfunzeros(lf200, [0, 200]);
print("N zeros [0,50]  = ", #z50);
print("N zeros [0,200] = ", #z200);

\\ Compare with Weyl estimates using different conductors
Pi_v = Pi;
for(ctest = 1, 5,
  my(q);
  q = ctest;
  my(w50)  = (50/(2*Pi_v))  * log(q * 50/(2*Pi_v))  - 50/(2*Pi_v);
  my(w200) = (200/(2*Pi_v)) * log(q * 200/(2*Pi_v)) - 200/(2*Pi_v);
  printf("q_an=%d  Weyl(50)=%.1f  Weyl(200)=%.1f\n", q, w50, w200)
);

\\ Correct formula for holomorphic modular form:
\\ N(T) ~ (T/Pi) * log(N_arith * (k/(2*Pi*e))^2 * T/(2*Pi))
\\ where N_arith is the arithmetic conductor
\\ For 4.5.b.a: N=4, k=5, chi=chi_4 (primitive, conductor 4)
\\ q_an = N * (conductor_chi)^2 * (k/(2*Pi))^2 ??
\\ Actually for GL(2): q_an = N * (k/2*Pi)^2 is NOT right.
\\ PARI uses: N(T) ~ T/(2*Pi) * log(Q*T/(2*Pi)) - T/(2*Pi)
\\ where Q = N * (k/(2*Pi))^2 for holomorphic forms
\\ PARI manual (lfunzeros): uses log(sqrt(Q)*T/(2*Pi*e))
\\ Let us print what PARI docs say the analytic conductor is
print("");
print("Checking different Weyl formulae:");
my(N_arith) = 4; my(k_wt) = 5;
my(q1) = N_arith * (k_wt/(2*Pi))^2;
my(w1_200) = (200/(2*Pi)) * log(q1 * 200/(2*Pi)) - 200/(2*Pi);
printf("Formula1: q=N*(k/2pi)^2=%.4f  Weyl(200)=%.1f\n", q1, w1_200);

\\ Alternative: q = N_arith^2 * k_wt^2 / (4*Pi^2)
\\ which is same as above but let's try Q = N * k^2/(4*Pi^2)
my(q2) = N_arith * k_wt^2 / (4 * Pi^2);
my(w2_200) = (200/(2*Pi)) * log(q2 * 200/(2*Pi)) - 200/(2*Pi);
printf("Formula2: q=N*k^2/(4pi^2)=%.4f  Weyl(200)=%.1f\n", q2, w2_200);

\\ LMFDB uses: log conductor = log N + 2 log(k/2) for weight k
\\ analytic cond = N * (k/2)^2
my(q3) = N_arith * (k_wt/2)^2;
my(w3_200) = (200/(2*Pi)) * log(q3 * 200/(2*Pi)) - 200/(2*Pi);
printf("Formula3: q=N*(k/2)^2=%.4f   Weyl(200)=%.1f\n", q3, w3_200);

\\ Empirical: we found 202 zeros up to T=200.
\\ Solve for q_an: 202 = (200/(2*Pi)) * log(q * 200/(2*Pi)) - 200/(2*Pi)
\\ 202 + 200/(2*Pi) = (200/(2*Pi)) * log(q * 200/(2*Pi))
\\ log(q * 200/(2*Pi)) = (202 + 200/(2*Pi)) * 2*Pi / 200
my(rhs) = (202 + 200/(2*Pi)) * 2*Pi / 200;
my(q_emp) = exp(rhs) * 2*Pi / 200;
printf("Empirical q_an from 202 zeros at T=200: %.4f\n", q_emp);
printf("Compare: 25/Pi^2 = %.4f,  N*(k/2)^2 = %.4f\n", 25/Pi^2, N_arith*(k_wt/2)^2);

print("=== end diagnostic ===");
