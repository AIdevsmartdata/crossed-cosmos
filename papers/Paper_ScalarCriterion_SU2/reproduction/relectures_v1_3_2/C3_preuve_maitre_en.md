# Candidate replacement proof of Lemma C(c) (fixed-size twist ratio, d = 4) — to be refereed

## Setting (from the published note, unchanged)
Lambda = prod_{mu=0}^{3} Z/L_mu, L_mu >= 2, V = |Lambda|, links E (|E| = 4V), plaquettes p = (x; mu<nu) (6V of them).
SU(2), normalised Haar measure dU on SU(2)^E. S_0(U) = sum_p (1 - (1/2) Tr U_p) >= 0, U_p = U_{x,mu} U_{x+mu,nu} U_{x+nu,mu}^{-1} U_{x,nu}^{-1}.
Z_0 = int exp(-beta S_0(U)) dU.

**Lemma C(c) (statement as published).** There are c > 0 and beta_0 (depending on Lambda) such that Z_0 >= c beta^{-(9V-3)/2} log beta for beta >= beta_0.
Combined with Lemma C(a), Z_k <= C_1 beta^{-9V/2} (twisted partition function, Morse-Bott), this gives Z_k/Z_0 <= C beta^{-3/2}/log beta.

**What was wrong with the published proof (erratum).** It asserted, in unspecified "gauge-fixed coordinates" (X_mu in su(2)^4 constant modes, q in R^{9(V-1)}),
the bound S_0 <= C( sum_{mu<nu} ||[X_mu,X_nu]||^2 + ||q||^2 ) "by Taylor expansion", uniformly near X = 0, without constructing the coordinates.
Near X = 0 the gauge orbits degenerate (stabiliser jumps from {+-1} to U(1) to SU(2)), so a Taylor argument in a quotient chart is not obviously uniform.

## Replacement proof (no quotient, explicit chart, exact inequalities)

Norms: ||.|| is the Frobenius norm on 2x2 complex matrices; it is invariant under left and right multiplication by unitaries.

**(F1)** For W in SU(2): 1 - (1/2) Tr W = (1/4) ||W - 1||^2.
Proof: ||W - 1||^2 = Tr((W-1)^*(W-1)) = 4 - Tr W - Tr W^* = 4 - 2 Tr W (Tr W is real on SU(2)).

**(F2)** For A, B in su(2): ||e^A e^B e^{-A} e^{-B} - 1|| <= ||[A,B]||.
Proof (SU(2)-specific, algebraic): write A = alpha u, B = beta' v with u, v unit pure quaternions (u^2 = v^2 = -1), alpha, beta' real.
Then e^A = cos alpha + sin alpha u, e^B = cos beta' + sin beta' v, and [e^A, e^B] = sin alpha sin beta' (uv - vu), [A,B] = alpha beta' (uv - vu).
Since |sin x| <= |x|, ||[e^A,e^B]|| <= ||[A,B]||. Finally e^A e^B e^{-A} e^{-B} - 1 = (e^A e^B - e^B e^A) e^{-A} e^{-B}, and the Frobenius norm is unitarily
invariant, so the left side equals ||[e^A, e^B]||. (Alternative proof valid in U(N): Duhamel twice, ||[A, e^B]|| <= ||[A,B]||.)

**(F3)** For unitaries U_i, U_i' (i = 1..4): ||U_1U_2U_3U_4 - U_1'U_2'U_3'U_4'|| <= sum_i ||U_i - U_i'|| (telescoping + unitary invariance);
||U^{-1} - U'^{-1}|| = ||U - U'||; and for q in su(2), ||e^q - 1|| <= ||q|| (e^q - 1 = int_0^1 q e^{tq} dt).

**Step 1 (maximal-tree gauge, exact for Haar).** Root o = (0,0,0,0). Axial maximal tree T: links (x,0) with x_0 <= L_0 - 2; (x,1) with x_0 = 0, x_1 <= L_1 - 2;
(x,2) with x_0 = x_1 = 0, x_2 <= L_2 - 2; (x,3) with x_0 = x_1 = x_2 = 0, x_3 <= L_3 - 2. |T| = V - 1, Ebar := E \ T, |Ebar| = 3V + 1.
For every gauge-invariant integrable f: int_{SU(2)^E} f dU = int_{SU(2)^Ebar} f(1_T, W) dW (W = U_Ebar, normalised Haar on SU(2)^Ebar).
(Standard: the gauge transformation g(U_T) with g_o = 1 that sets the tree links to 1 depends only on U_T; for fixed U_T the map
U_Ebar -> (g.U)_Ebar is a product of fixed left/right translations, which preserves Haar measure.)

**Step 2 (uniform-field family).** For X = (X_0..X_3) in su(2)^4 set U^X_{(x,mu)} = exp(X_mu / L_mu) for all x. Every plaquette (x; mu, nu) has
U^X_p = e^{a_mu} e^{a_nu} e^{-a_mu} e^{-a_nu}, a_mu = X_mu/L_mu. By (F1), (F2):
   S_0(U^X) <= (1/4) sum_p ||[a_mu, a_nu]||^2 = (V/4) sum_{mu<nu} ||[X_mu, X_nu]||^2 / (L_mu L_nu)^2 <= (V/64) sum_{mu<nu} ||[X_mu, X_nu]||^2.     (S2)
Let Phi(X) := (g(U^X_T).U^X)_Ebar, the tree-gauge representative restricted to Ebar. Then S_0(1_T, Phi(X)) = S_0(U^X) (gauge invariance).
For l in Ebar, Phi(X)_l is the holonomy of U^X along the closed loop C_l = (tree path o -> base of l), l, (tree path back to o).
Four special non-tree links: l_0 = ((L_0-1,0,0,0),0), l_1 = ((0,L_1-1,0,0),1), l_2 = ((0,0,L_2-1,0),2), l_3 = ((0,0,0,L_3-1),3).
For l_mu, C_{l_mu} is the straight loop of L_mu steps in direction mu through o, so Phi(X)_{l_mu} = (e^{a_mu})^{L_mu} = e^{X_mu} EXACTLY.

**Step 3 (explicit chart, no inverse function theorem).** Let Qsp := { q in su(2)^Ebar : q_{l_mu} = 0, mu = 0..3 }, a real vector space of
dimension 3(3V+1) - 12 = 9V - 9. Define Psi(X, q)_l := Phi(X)_l exp(q_l) for l in Ebar (so Psi(X,q)_{l_mu} = e^{X_mu}).
Inverse on a neighbourhood of 1: X_mu = log W_{l_mu}, q_l = log( Phi(X)_l^{-1} W_l ). Hence Psi is a diffeomorphism from
{ |X_mu| < r_1, |q_l| < r_1 } onto an open subset of SU(2)^Ebar, for r_1 < pi/sqrt2 (principal branch of log).
Haar density: order the coordinates (X, q) and the image coordinates (W_{l_mu}, then the other W_l). The Jacobian matrix is block lower-triangular
(W_{l_mu} depends on X_mu only; W_l depends on X and on q_l only), with diagonal blocks = derivative of exp at X_mu (mu = 0..3) and derivative of
q_l -> Phi(X)_l exp(q_l) (a left translation of exp) at q_l. Haar measure is left-invariant, so in these coordinates
   dW = prod_mu rho(X_mu) dX_mu * prod_{l != l_mu} rho(q_l) dq_l,
where rho is the density of normalised Haar measure in exponential coordinates: rho(q) = (sin theta / theta)^2 / (2 pi^2) in the R^3 coordinate
q = theta n (n unit), positive and continuous, rho >= rho_min > 0 for |q| <= r_1.

**Step 4 (action bound in the chart, global on the chart).** Each plaquette holonomy is a product of 4 link variables (or inverses); changing
W_l -> W_l e^{q_l} changes it, by (F3), by at most sum_{l in p} ||q_l||. With (a+b)^2 <= 2a^2 + 2b^2 and (sum of 4 terms)^2 <= 4 sum:
   ||W_p(X,q) - 1||^2 <= 2 ||W_p(X,0) - 1||^2 + 8 sum_{l in p} ||q_l||^2.
Summing over p with (F1) and using that each link lies in exactly 6 plaquettes:
   S_0(1_T, Psi(X,q)) <= 2 S_0(U^X) + 12 ||q||^2 <= (V/32) sum_{mu<nu} ||[X_mu,X_nu]||^2 + 12 ||q||^2.                (S4)

**Step 5 (lower bound).** By Steps 1, 3, 4:
   Z_0 >= rho_min^{3V+1} * [ int_{q in Qsp, |q_l| <= r_1} e^{-12 beta ||q||^2} dq ] * [ int_{|X_mu| <= r_1} e^{-beta (V/32) sum ||[X_mu,X_nu]||^2} dX ].
q-integral: a Gaussian in 9V - 9 real dimensions restricted to a fixed box: >= (1/2) (pi/(12 beta))^{(9V-9)/2} for beta >= beta_1.
X-integral I(beta): identify su(2) with R^3 (X = x . (i sigma/2)), so ||[X,Y]|| = |x cross y| / sqrt2 and ||X|| = |x|/sqrt2.
Region R_beta: x_0 = r u (u in S^2), beta^{-1/4} <= r <= r_2; x_i = t_i u + z_i, z_i perp u, |t_i| <= r, |z_i| <= beta^{-1/2}/r (i = 1,2,3).
On R_beta: |x_0 cross x_i| = r |z_i| <= beta^{-1/2}; |x_i cross x_j| <= |t_i||z_j| + |t_j||z_i| + |z_i||z_j| <= 2 beta^{-1/2} + beta^{-1}/r^2 <= 3 beta^{-1/2}.
Hence beta * sum_{mu<nu} |x_mu cross x_nu|^2 <= 3 + 27 = 30 and the integrand is >= exp(-30 V/64).
Lebesgue volume (x_0 in polar coordinates r^2 dr du; for fixed u, dx_i = dt_i d^2 z_i):
   vol(R_beta) = int r^2 dr * 4 pi * prod_{i=1}^{3} (2r * pi beta^{-1} r^{-2}) = 32 pi^4 beta^{-3} int_{beta^{-1/4}}^{r_2} dr/r = 32 pi^4 beta^{-3} ( log r_2 + (1/4) log beta ).
R_beta lies in the box |x_mu| <= r_1' once r_2 is small and beta large (|x_i|^2 <= r_2^2 + beta^{-1/2}).
So I(beta) >= c_X beta^{-3} log beta for beta >= beta_2, with dX = (Lebesgue in x) up to the fixed factor (1/sqrt2)^{12} or its inverse.
Total exponent: (9V-9)/2 + 3 = (9V-3)/2. Hence Z_0 >= c beta^{-(9V-3)/2} log beta. QED.

**Remarks.** (i) All constants are explicit (rho_min, r_1, r_2, beta_0, and exp(-30V/64)); they depend on Lambda. (ii) Nothing is Taylor-expanded:
(S2) and (S4) are exact inequalities valid on the whole chart; the degeneration of gauge orbits at X = 0 is irrelevant because nothing is
quotiented (the global constant gauge transformations act on the chart but are not divided out). (iii) Corollary L1 uses only Lemma C(a),(b)
(ratio <= C beta^{-3/2}); it is unaffected either way.
