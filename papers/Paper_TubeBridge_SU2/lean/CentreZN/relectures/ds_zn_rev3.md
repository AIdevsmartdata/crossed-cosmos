1. **OK** — Section 5 bis, sign convention.  
   Checked: Kanazawa eq. (9) defines  
   \(\langle F^{[m]}[V]\rangle=\frac1N\sum_k z^{mk}\langle O^{[k]}[V]\rangle\) with \(z=e^{2\pi i/N}\). If \(\hat Z_q=\sum_k \zeta^{qk}Z_k\) with \(\zeta=z\), then  
   \[
   \frac{\hat Z_q}{N Z_0}
   =\frac1{NZ_\Lambda}\sum_k z^{qk}Z^{[k]}
   =\langle F^{[q]}[V]\rangle.
   \]
   The claimed sign convention is correct.

2. **OK** — Section 5 bis, composition paragraph.  
   The identity
   \[
   1-\langle F^{[0]}[V]\rangle=\sum_{m\not\equiv0}\langle F^{[m]}[V]\rangle
   \]
   is correct: summing the Fourier projectors gives
   \[
   \sum_{m=0}^{N-1}F^{[m]}=\frac1N\sum_k O^{[k]}\sum_m z^{mk}=O^{[0]}=1.
   \]

3. **GAP** — Section 5 bis, “Par (27) … par (12) …”.  
   Theorem 2(27) of Kanazawa uses a vortex stack \(V\) that links once with \(C\). The text does not explicitly verify that the \(V\) used in the bound (12) is the same linking stack, nor does it state that the fixed base point of \(V\) lies inside the rectangle \(C\).  
   Repair: add explicitly that \(V\) is the transverse stack with base point inside \(C\), so that it links \(C\) once.

4. **GAP/UNVERIFIABLE** — Section 5 bis, “\(L_\mu=2^p l_\mu, L_\nu=2^{p'}l_\nu\) (condition de sa preuve, p. 9)”.  
   The quoted Theorem 2 on p. 6 does not contain this side-divisibility condition. The relevant p. 9 is not quoted, so the hypothesis cannot be checked from the provided extract. If the proof there requires it, the chosen periods satisfy it by construction.

5. **GAP** — Section 5 bis, final displayed inequality.  
   The step
   \[
   2\epsilon^{A_C/(L_\mu L_\nu)}
   \le
   2(N-1)^{A_C/(L_\mu L_\nu)}
   (1-e^{-2\beta L_\perp})^{A_C}
   \]
   requires the uniform bound
   \[
   \rho_{N,m}(\beta L_\perp)\le 1-e^{-2\beta L_\perp}
   \]
   for every \(m\not\equiv0\). This bound is not stated or proved in the displayed section 5 bis text. If it is part of (12) or Corollary S, the citation is missing. Conditional on that bound, the algebra is correct.

6. **OK** — Section 5 bis, final constants algebra.  
   Conditional on item 5, let \(r=A_C/(L_\mu L_\nu)\) and \(R=1-e^{-2\beta L_\perp}\). If
   \[
   \epsilon\le (N-1)R^{L_\mu L_\nu},
   \]
   then
   \[
   2\epsilon^r\le 2(N-1)^r R^{rL_\mu L_\nu}
   =2(N-1)^r R^{A_C}.
   \]
   Thus the exponents in the displayed final bound are algebraically correct.

7. **OK** — Section 5 bis, \(N=2\) specialization.  
   With \(\rho_{2,1}(\kappa)=\tanh\kappa\), one gets
   \[
   \epsilon^r=\tanh(\beta L_\perp)^{L_\mu L_\nu\cdot A_C/(L_\mu L_\nu)}
   =\tanh(\beta L_\perp)^{A_C},
   \]
   so the claimed \(N=2\) bound follows conditionally.

8. **OK** — Section 5 bis, “Variante (26)”.  
   From Kanazawa (26),
   \[
   |\langle W_R(C)\rangle|
   \le
   \langle F^{[N(R)]}[V]\rangle^{r}
   +(1-\langle F^{[0]}[V]\rangle)^r,
   \quad r=\frac{A_C}{L_\mu L_\nu}.
   \]
   The first term is bounded by \((\rho_{N,N(R)}(\beta L_\perp)^{L_\mu L_\nu})^r=\rho_{N,N(R)}(\beta L_\perp)^{A_C}\), and the second by \(\epsilon^r\). The stated variant is correct conditional on the same bounds.

9. **OK** — Section 8, \(N=4\) setup.  
   For \(t=x+iy\) and \(\zeta=i\), the displayed expressions
   \[
   S=2(\cosh x+\cosh y),\quad
   A_1=2\sinh x-2i\sinh y,\quad
   A_2=2(\cosh x-\cosh y)
   \]
   are correct. The substitutions \(x=u+v,\ y=u-v\) give
   \[
   \cosh x+\cosh y=2\cosh u\cosh v,\quad
   \cosh x-\cosh y=2\sinh u\sinh v.
   \]

10. **OK** — Section 8, identity for \(r_{4,1}\).  
    With \(r_{4,1}(t)=|A_1|/S\),
    \[
    1-r_{4,1}(t)^2
    =\frac12(\operatorname{sech}^2u+\operatorname{sech}^2v).
    \]
    This identity checks out by direct algebra.

11. **OK** — Section 8, convexity of \(h(\sigma)=\operatorname{sech}^2(\sqrt\sigma)\).  
    For \(w=\sqrt\sigma\),
    \[
    h'(\sigma)=-\frac{\tanh w}{w\cosh^2 w}.
    \]
    Both \(\tanh(w)/w\) and \(1/\cosh^2 w\) are positive decreasing, so their product is positive decreasing; hence \(h'\) is increasing. Therefore \(h\) is convex. The Jensen step
    \[
    \operatorname{sech}^2u+\operatorname{sech}^2v
    \ge 2\operatorname{sech}^2(s/2)
    \]
    under \(u^2+v^2=s^2/2\) is correct.

12. **OK** — Section 8, \(q=2\) bound.  
    For \(a=\cosh x,\ b=\cosh y\), the function \((a-b)/(a+b)\) is increasing in \(a\) and decreasing in \(b\):
    \[
    \partial_a f=\frac{2b}{(a+b)^2}\ge0,\quad
    \partial_b f=-\frac{2a}{(a+b)^2}\le0.
    \]
    Thus
    \[
    r_{4,2}(t)\le \frac{\cosh\kappa-1}{\cosh\kappa+1}
    =\tanh^2(\kappa/2).
    \]
    The conclusion \(\rho_{4,2}(\kappa)=\tanh^2(\kappa/2)\) is correct, with equality at \(t=\kappa\) or \(t=i\kappa\).

13. **OK** — Section 8, \(N=4\) conclusion for \(q=\pm1\).  
    From the convexity bound,
    \[
    1-r_{4,1}(t)^2\ge \operatorname{sech}^2(s/2),
    \]
    hence
    \[
    r_{4,1}(t)\le \tanh(s/2)\le \tanh(\kappa/2).
    \]
    Equality is attained at \(t=\kappa\). Therefore
    \[
    \rho_{4,\pm1}(\kappa)=\tanh(\kappa/2).
    \]

14. **OK** — Section 8, \(N=3\) reduction.  
    Set \(a=e^{x_0}, b=e^{x_1}, c=e^{x_2}\). Since \(x_0+x_1+x_2=0\), \(abc=1\), and
    \[
    P=ab+bc+ca=e^{-x_0}+e^{-x_1}+e^{-x_2}.
    \]
    For \(q=\pm1\),
    \[
    |A_1|^2=S^2-3P,
    \]
    so
    \[
    r_{3,\pm1}^2=1-\frac{3P}{S^2}.
    \]
    The polynomial
    \[
    4X^3-3\kappa^2X-\kappa^3\cos 3\phi=0
    \]
    has roots \(x_j=\kappa\cos(\phi+2\pi j/3)\), by the identity \(\cos 3\theta=4\cos^3\theta-3\cos\theta\). The symmetric sums \(S\) and \(P\) therefore depend only on \(c=\cos3\phi\). Maximizing \(r^2\) is equivalent to maximizing \(S^2/P\), so the stated equivalence for the boundary circle is correct.

END OF REVIEW