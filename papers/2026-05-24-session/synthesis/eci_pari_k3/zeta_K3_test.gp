\\ Test ECI ζ_M(s) for K3:
\\ ζ_K3(s) = prod_p L_p(s)
\\ where L_p has degree 22 generically.
\\
\\ For diagonal Fermat quartic, the local zeta function decomposes:
\\ Z_p(T) = 1/((1-T)(1-pT)^{20}(1-p^2T)(1-Q_p(T)))
\\ where Q_p(T) is the L-polynomial of the transcendental part.
\\
\\ For p ≡ 3 mod 4 (good reduction, our case):
\\   Tr(Frob | H^2) = 2p (observation)
\\   This means: 20 eigenvalues from NS contribute total 2p (most cancel out)
\\               2 eigenvalues from T (transcendental) contribute 0
\\   Detailed: NS Frob has 18 eigenvalues = -p, 2 eigenvalues = +p?
\\           or 20 eigenvalues at +p, with subtraction from special cycles?
\\
\\ Actually the standard result for Fermat quartic:
\\   #X(F_p) = p^2 + p + 1 + Q(p)
\\ where Q(p) involves Jacobi sums.
\\
\\ Let's compute Jacobi sum-based formula.

\\ The number of points on Fermat hypersurface x_0^d + ... + x_n^d = 0 in P^n over F_p:
\\ #X(F_p) = (number of (x_0,...,x_n) in F_p^{n+1} \ 0 with sum_i x_i^d = 0) / (p-1)
\\
\\ Use Weil's formula:
\\ #X(F_p) - (p^{n-1} + p^{n-2} + ... + 1) = -[sum over Jacobi]
\\
\\ For Fermat quartic in P^3 (n=3):
\\ #X(F_p) = (p^3 + p^2 + p + 1)/(p+1) + ... no wait
\\ #P^3(F_p) = (p^4-1)/(p-1) = p^3 + p^2 + p + 1
\\ But #X is a surface (2-dim variety), so #X(F_p) ≈ p^2 generically
\\ Lefschetz formula: #X(F_p) = 1 + p + Tr(Frob|H^1) + p Tr(Frob|H^1) + p^2 + Tr(Frob|H^2)
\\ But for K3, H^1 = 0, so #X(F_p) = 1 + 0 + 0 + p^2 + Tr(Frob|H^2) = p^2 + 1 + Tr(Frob|H^2)
\\ Yes that's what I used.

\\ Jacobi sum approach:
\\ J(chi_1, ..., chi_n) = sum_{x_1+...+x_n=1} chi_1(x_1) ... chi_n(x_n)
\\ For Fermat quartic: characters chi of order 4 on F_p^*

\\ Let me compute directly via PARI's lfun and L-function tools

print("--- L-function of Fermat quartic K3 ---");
print();
print("Lefschetz: #X(F_p) = 1 + p^2 + Tr(Frob | H^2)");
print("For K3 with Picard rho_p=20: 20 algebraic eigenvalues + 2 transcendental");
print();

\\ For diagonal quartic surface, the explicit formula (Weil 1949):
\\ # X(F_p) = p^2 + 1 + 3p + (sum of Jacobi sums involving chi_4)
\\ where 3p comes from 3 hyperplane sections, and Jacobi sums give algebraic+transcendental

\\ For p ≡ 1 (mod 4): chi_4 of order 4 exists, gives extra contribution
\\ For p ≡ 3 (mod 4): chi_4 of order 4 doesn't exist (only chi_2), reduced contribution

\\ Test: For p=3 (≡ 3 mod 4), #X(F_3) = 16
\\   = 1 + 9 + Tr(Frob|H^2)
\\   = 10 + 6  ✓
\\ Standard formula: #X(F_p) for p≡3 mod 4 = p^2 + 1 + 3p - (Jacobi w/ chi_2)
\\ For p=3: 9 + 1 + 9 - 3 = 16 ✓

\\ Now: ζ_K3(s) = ζ(s) ζ(s-1) ζ(s-2) ζ(s-1)^{19} L_T(s)
\\ (with 20 algebraic contributions giving zeta(s-1)^{20} basically)

\\ Take log of local Euler factor:
\\ log L_p(s)^{-1} = sum_n a_n / n * p^{-ns}
\\ where a_n = Tr(Frob^n) on H^2

\\ Let me compute Tr(Frob | H^2_transcendental) for our data
\\ Hypothesis: T_X for Fermat quartic is 2-dim, gives weight 3 newform 16.3.b.a
\\ But our data shows nonzero a_p for p≡3 mod 4 (e.g. a_3=6, a_7=14)
\\ which CONTRADICTS the CM newform hypothesis (which gives 0 there)

\\ Resolution: a_p in our table is Tr(Frob | H^2_full), not just transcendental
\\ The Tr=2p for p≡3 mod 4 represents only ALGEBRAIC contribution (20 cycles)
\\ The transcendental contribution is 0 (consistent with CM newform 16.3.b.a, a_p=0)

\\ For p ≡ 1 mod 4:
\\   Algebraic: still 2p? Or extra cycles?
\\   Transcendental: nonzero (CM newform)

\\ Let's separate: Tr(Frob|alg) + Tr(Frob|T) = Tr(Frob|H^2)
\\ Conjecture: Tr|alg = 2p for ALL primes
\\ Then Tr|T = Tr|H^2 - 2p

\\ For p=5: Tr|T = -26 - 10 = -36. Is this 2 * a_5(CM_form)? 2*(-6) = -12. Not matching.
\\ Try Tr|T = a_p(CM_form): a_5 = -6, but Tr|H^2 - 2p = -36. Not matching either.

\\ Maybe algebraic contribution is NOT 2p uniformly for all p.
\\ For p=5: algebraic could include cycles defined over F_5 that aren't over F_3 etc.

\\ ALTERNATIVE: compute discriminant of CM newform, see which level
\\ The Fermat quartic has explicitly computable L-function (Schoen 1988, etc.)

\\ For Fermat quartic K3, the transcendental part has L-function:
\\ L(T, s) = L(psi, s-1) where psi is Hecke Grossencharacter on Q(zeta_8) with infty type (2,0,...)
\\ But Q(zeta_8) has degree 4, so this is degree-4 L-function

\\ Decomposed into Q-rational forms: weight 3 newform on Gamma_0(N)
\\ N depends on the Schoen paper, I believe N=64 with chi_8 character

\\ Let me search PARI directly
print("Search weight-3 CM newforms with specific levels");
\\ Level 16, 32, 64 with various characters
for(N = [8, 16, 32, 64],
print("N=", N);
\\for(d in [1, -1, -4, 8]
\\my(M = mfinit([N, 3, d]));
);

\\ Direct: try Gross-Zagier-style L-function eigen-basis
mf64 = mfinit([64, 3, 1], 1); \\ new, trivial char
print("Level 64, weight 3, trivial char NEW: dim ", mfdim(mf64));
if(mfdim(mf64) > 0, my(eb = mfeigenbasis(mf64)); for(i=1, #eb, print("  Form ", i, " coeffs: ", mfcoefs(eb[i], 20))));

mf64chi8 = mfinit([64, 3, 8], 1); \\ chi_8 char
\\ Wait, chi_8 is not -4 or 1; chi has to be Dirichlet
\\ chi_8 = chi_{Q(sqrt 2)} which is determined by character of order 2 mod 8 sending 5 to -1

print();
\\ Try Schoen's reference:  Fermat quartic K3 transcendental L-fn
\\ should match level 32 chi_{-4} eigenforms
print("Level 32, weight 3, chi=-4, ALL eigenforms (new):");
mf32n = mfinit([32, 3, -4], 1);
print("Dim: ", mfdim(mf32n));
if(mfdim(mf32n) > 0, my(eb = mfeigenbasis(mf32n));
  for(i=1, #eb, print();
  print("  Eigenform ", i, ":");
  my(g = eb[i]);
  for(n=2, 30, my(an = mfcoef(g, n)); if(an != 0, print("    a_", n, " = ", an)));
));

print();
print("--- Now test ECI hypothesis ---");
\\ ECI claims: Σ a_p (sum of Frobenius traces) might match Σ first k primes
\\ for some specific k = dim(G).
\\
\\ But this was statistically tested and found inconclusive.
\\ A more refined test: do the FACTORS of L_p(T) (eigenvalues of Frob)
\\ contain primes as numerical values?

\\ For p=5, Frob eigenvalues on H^2 = 22 algebraic of magnitude 5.
\\ Tr = -26 = sum of these 22 numbers (each magnitude 5).
\\ Mean magnitude = 26/22 = 1.18, far below 5 -> high cancellation.
\\ Some are p=5, some are -5, etc.

\\ The DETERMINANT of Frob on H^2 = p^{22} = 5^{22}.
\\ For K3, det(Frob | H^2) = epsilon * p^{22} where epsilon = ±1 (depending on K3 type)

\\ The crucial number theoretic info is in the L-polynomial roots.
\\ ECI hypothesis: dim G = k <-> roots of L_p(T) form set including primes

\\ Let me just numerically compute L_p polynomial for Fermat quartic at small p
\\ via the trace data and Hasse-Weil zeta function.

\\ For K3:
\\ Z_X(T) = 1 / [(1-T)(1-p^2 T) * P_2(T)]
\\ where P_2(T) = prod (1 - alpha_i T), deg 22.
\\ P_2(T) = 1 - Tr(Frob | H^2) T + ...
\\ Higher coefficients require more info (e.g. Tr(Frob^2), etc.)

\\ Compute Tr(Frob^2) by counting #X(F_{p^2})
\\ # X(F_{p^2}) = 1 + p^4 + Tr(Frob^2 | H^2)
\\ This requires counting over F_{p^2}, which is expensive but doable for small p
