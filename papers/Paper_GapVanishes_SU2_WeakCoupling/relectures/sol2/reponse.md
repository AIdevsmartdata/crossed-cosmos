The weakest written step is lem:projrate, especially line 1534: “elementary inequalities” conceal the entire quantitative Fourier estimate. It holds after re-derivation; the claimed constant 408 survives. This attack did not refute Theorem thm:rate or Theorem thm:A.

I read the whole note, including the appendix. All line numbers below refer to NOTE_v1_3.tex.

1. lem:projrate, lines 1524–1535. Both the weighted Fourier estimate W <= 45 and the cutoff error require missing algebra. This is my first choice because an incorrect derivative estimate could silently change the quantitative theorem.

2. lem:H2, lines 1503–1518. The delicate point is controlling the harmonic component under the finite-beta comparison measure. The limiting bound (H3) cannot simply be imported here. The actual argument instead uses ||H(b)|| <= ||F(a,b)|| pointwise under the original Gibbs measure, followed by truncation. That works. Selecting the centre by minimizing an expectation also makes it deterministic and common to all five expectations needed later.

3. lem:S, particularly lines 723–798. The vulnerable passage is uniform tail control before normalization, including possible competing flat configurations. The Stokes sublevel estimate controls every free coordinate, so no additional flat family escapes those bounds. The order of limits is correct: fixed box, then beta, then the tail cutoff. This lemma alone would not justify growing boxes; the rate proof replaces it with Stein comparison.

4. lem:cond, lines 564–579. Gauge invariance of the action alone would not establish the claimed conditional law. The required pushforward argument does work: condition on the original exterior; the shell transformation determined by U_TS is then fixed. Apply that deterministic change of variables first, then the interior forest change of variables. The fully gauge-fixed free variables are invariant under interior gauge transformations, so the forest Haar variables integrate out. The resulting kernel depends only on the transformed shell, hence only on b. Conditional expectation then gives the same kernel when conditioning merely on b. No gauge-invariance hypothesis on the original state is needed.

5. lem:L1, lines 419–516. Cancellation of the extensive logarithmic terms depends on the exact temporal-chain count. I obtain the stated counts:
   |bd| = 24m^3, F_n = (3m+4)m^3, |Q| = 3(m−1)m^3.
   Thus F_n−|Q| = 7m^3. The chain integrations remain valid for arbitrary fixed bottom links. Sending m to infinity at fixed beta gives 123.7322276…/beta, so 124 is admissible. Neither rotation invariance nor uniqueness is used.

For the top step, here is a derivation from the definitions.

Work with one colour. Put epsilon_j(k)=exp(ik_j)−1, r=|epsilon| and q=epsilon/r away from k=0. Let E_q denote exterior multiplication by q. The Fourier multiplier of Pi_infinity on two-forms is

P(k) = E_q E_q*.

Write v_hat = a(k)e_12, where a(k)=1−exp(−ik_1), and f=Pi_infinity v. Then |a|<=r and |partial_j a| equals 1 for j=1 and zero otherwise.

Because differentiation of q removes the real radial component,

|partial_j q|^2
= (|partial_j epsilon|^2 − (Re〈q,partial_j epsilon〉)^2)/r^2
<= 1/r^2.

Exterior multiplication has operator norm equal to the vector norm. Consequently,

||partial_j P|| <= 2/r,
|partial_j f_hat| <= 2 + 1_{j=1}.

The multiplier f_hat extends continuously by zero at the origin; these bounded derivatives are also its weak derivatives. Fourier differentiation therefore gives

W := sum_x |x|^2 |f(x)|^2
   = sum_j integral |partial_j f_hat|^2
   <= 3·2^2 + 3^2 = 21.

This proves more than the omitted W<=45 estimate, without checking five componentwise rational expressions.

Now take u=d*Delta^−1 v. Its Fourier multiplier gives du=f and

||u||^2 <= integral |a|^2/r^2 = 1/4,

the last equality following by symmetry among the four coordinates.

Use the note’s cutoff chi, multiplying each link component at its lower endpoint. Its Lipschitz constant is L=2/(m−4). Its support makes d(chi u) an admissible element of R_B under the stated interior-containment hypothesis.

The discrete product rule has exactly two shifted correction terms per plaquette. Summing their squares gives

||d(chi u)−chi f||^2 <= 6L^2 ||u||^2.

Since 1−chi vanishes on B_{m/2},

distance(f,R_B)^2
<= 2 sum_{|x|_infinity>m/2}|f(x)|^2
   + 12L^2||u||^2
<= 8W/m^2 + 48||u||^2/(m−4)^2
<= 180/(m−4)^2.

Finally, because R_B is contained in R_infinity,

〈v,(Pi_infinity−Pi_B)v〉 = distance(f,R_B)^2.

Thus 408/(m−4)^2 holds. Repair: insert this multiplier-and-cutoff calculation into the note. No additional hypothesis is required.

The other specifically requested tests give:

- lem:free, lines 1088–1093: on the selected cubes, setting s=sum_i hat(k_i)^2 gives 2sinh(omega)=2sqrt(s+s^2/4)<=sqrt(7)|k|<2.65|k|. The displayed restricted integral has coefficient 6.352721…·10^−5. I also checked a rational lower certificate exceeding 6·10^−5. The exponent six, hence the squared-correlation exponent twelve, survives.
- rem:whichgap, lines 1128–1139: the invariant subspace reduces the self-adjoint T, giving m<=m^inv. For odd t, the negative spectral contribution is nonpositive, which gives the claimed m_+ bound. Positivity of T is unnecessary.
- Translation to w_n, lines 936–970 and 1550–1553: this translates the entire observable configuration rigidly. Full space-time translation invariance is explicitly assumed. The selected centre need not lie on the original reflection plane: expectations are translated back before applying the time-zero variational argument. No additional reflection symmetry is being used.

Two corrections outside those estimates:

- Lines 69–70 associate the simplified bound 24 beta^−1/120 log(beta) with a threshold near 10^455. Lines 1574 and 1665 correctly distinguish that threshold from the simplified bound’s threshold near 10^537. Solving the latter equality gives log10(beta)=536.6546…. Correct the abstract.
- Line 1597 needs g to be exterior-measurable, with fixed local supports and N sufficiently large relative to those supports. Its identity is false for arbitrary g. Conditioning must be interpreted on the torus before lifting: the full exterior of a periodic lift contains copies revealing U_E. Fixed local identities suffice for the limiting Gibbs claim.

[line referring to internal project files removed]

I did not independently repeat the complete Stein proof, every rate-assembly inequality, the computational replays, Lean checks, or external bibliographic claims. Registry files were not updated because this session is read-only.

[line referring to internal project files removed]

palette: Fourier/Hodge multiplier → projector rate; DLR pushforward → conditional kernel; Caccioppoli → centre selection; convex log Z → energy bound; spectral moments → sector gaps / metaphors discarded: KAM, no applicable small-divisor mechanism; Perelman, no applicable monotone flow. F1/F2: these are upper bounds compatible with Coulomb masslessness and exponentially small SU(2) gaps.