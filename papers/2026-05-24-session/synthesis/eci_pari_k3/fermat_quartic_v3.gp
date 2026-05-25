\\ Extended Frobenius: include more primes p=31..47 and verify
\\ Also compute for Fermat *cubic* (Calabi-Yau 2-fold? actually elliptic curve)
\\ and Kummer surface variants.

count_FQ_chart_w1(p) = my(n=0); for(x=0,p-1, for(y=0,p-1, for(z=0,p-1, if(Mod(x^4+y^4+z^4+1,p)==0, n+=1)))); n;
count_FQ_chart_w0z1(p) = my(n=0); for(x=0,p-1, for(y=0,p-1, if(Mod(x^4+y^4+1,p)==0, n+=1))); n;
count_FQ_chart_w0z0y1(p) = my(n=0); for(x=0,p-1, if(Mod(x^4+1,p)==0, n+=1)); n;
count_FQ_total(p) = count_FQ_chart_w1(p) + count_FQ_chart_w0z1(p) + count_FQ_chart_w0z0y1(p);
trace_frob_h2(p) = my(N); N=count_FQ_total(p); [p, N, N-1-p^2];

print("Extended Frobenius for Fermat quartic, p=31..47");
{forprime(p=31, 47, my(r = trace_frob_h2(p)); print(r));}

\\ Now: check if the SEQUENCE of Frobenius traces matches first N primes for small N
\\ Sequence of (Tr/p) for primes p=3,5,7,11,13,17,19,23,29,31,37,41,43:
\\ Compare with first 14 primes: 2,3,5,7,11,13,17,19,23,29,31,37,41,43
\\ Note p=2 is BAD reduction for Fermat quartic

print();
print("--- Tate twist analysis ---");
print("For each p, eigenvalues of Frob on H^2_{prim} are 22 complex numbers");
print("of magnitude p. The TRANSCENDENTAL part is 2-dim, gives a Hecke eigenvalue.");
print();

\\ Compute the L-function of the Fermat quartic K3 numerically via L_p(T) for several primes
\\ For a K3, L(K3, s) = ∏_p L_p(p^-s)^-1 where L_p is a degree-22 polynomial generically.
\\ For Fermat quartic with Picard rank 20: L_p factors as L_{NS}(T) * L_{trans}(T)
\\ where L_{NS} is degree 20 and L_{trans} is degree 2.

\\ Q3: Test if sum_p log(p) * a_p / p^s converges to ECI quantities at special s.
\\ This is the LOGARITHMIC DERIVATIVE of L-function.
print("Log-derivative of L-function: sum_p (a_p/p) for first primes");
print("If ECI = code based on K3, this sum should hit special values...");

a_p_data = [[3,6],[5,-26],[7,14],[11,22],[13,-42],[17,310],[19,38],[23,46],[29,-74]];
{my(s = 0); for(i=1, #a_p_data, s += a_p_data[i][2]*1.0/a_p_data[i][1]); print("Sum a_p/p (p=3..29) = ", s);}
{my(s = 0); for(i=1, #a_p_data, s += abs(a_p_data[i][2])*1.0/a_p_data[i][1]); print("Sum |a_p|/p (p=3..29) = ", s);}
{my(s = 0); for(i=1, #a_p_data, s += a_p_data[i][2]*1.0/(a_p_data[i][1])^2); print("Sum a_p/p^2 (p=3..29) = ", s);}
{my(s = 0); for(i=1, #a_p_data, s += a_p_data[i][2]*1.0/(a_p_data[i][1])^(3/2)); print("Sum a_p/p^{3/2} (p=3..29) = ", s);}
