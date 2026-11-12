BLIND RE-DERIVATION

Let \(Q=N_b=N(m,C)\). I write \(P=P_b\). The chart is
\[
\Omega=\{a: |a_e|<2\pi/g\ \forall e\}.
\]
On \(\Omega\),
\[
\frac{dP}{dQ}=p=Z_Q Z_P^{-1} e^{-E_g+E_0}J,\qquad J=\prod_e j_g(a_e).
\]
Hence, on \(\Omega\),
\[
\nabla\log p=-\nabla E_g+\nabla E_0+\nabla\log J .
\]

## 1. Sharp Stein constant

For the Gaussian \(Q=N(m,C)\), the Stein operator is
\[
\mathcal L_C u=\operatorname{tr}(C\operatorname{Hess}u)-(x-m)\cdot\nabla u .
\]
By the affine change \(y=C^{-1/2}(x-m)\), it suffices to consider \(Q=N(0,I)\) and
\[
\mathcal L u=\Delta u-x\cdot\nabla u .
\]
For smooth compactly supported \(g\) with \(0\le g\le 1\), let
\[
P_s g(x)=\mathbb E[g(e^{-s}x+\sqrt{1-e^{-2s}}Z)],\qquad Z\sim N(0,I).
\]
Then \(\partial_s P_s g=\mathcal L P_s g\), and
\[
u(x)=-\int_0^\infty \bigl(P_s g(x)-\mathbb E g(Z)\bigr)\,ds
\]
solves \(\mathcal L u=g-\mathbb E g\).

For a unit vector \(w\), Gaussian integration by parts gives
\[
w\cdot\nabla P_s g(x)
=\frac{e^{-s}}{\sqrt{1-e^{-2s}}}
\mathbb E[(w\cdot Z)g(e^{-s}x+\sqrt{1-e^{-2s}}Z)].
\]
Since \(w\cdot Z\) is a standard one-dimensional Gaussian and \(0\le g\le 1\),
\[
|\mathbb E[(w\cdot Z)g(\cdots)]|
\le \mathbb E[(w\cdot Z)_+]=\frac1{\sqrt{2\pi}}.
\]
Therefore
\[
|w\cdot\nabla u(x)|
\le \frac1{\sqrt{2\pi}}
\int_0^\infty \frac{e^{-s}}{\sqrt{1-e^{-2s}}}\,ds
=\frac1{\sqrt{2\pi}}\frac{\pi}{2}
=\sqrt{\frac{\pi}{8}}.
\]
Returning to \(x\)-coordinates,
\[
\sup_{|v|=1}|v\cdot C^{1/2}\nabla u|\le \sqrt{\pi/8}.
\]
Thus
\[
\boxed{\kappa=\sqrt{\pi/8}}.
\]
This is sharp in one dimension, as seen by smooth approximations to \(g=1_{(-\infty,0]}\).

## 2. Cutoff integration-by-parts identity

Let \(\chi\) be Lipschitz, supported in \(\{g|a_e|\le 2\ \forall e\}\), and equal to \(1\) on \(\{g|a_e|\le 1\ \forall e\}\). This support is strictly inside \(\Omega\). For \(f\in C_c^\infty\) with \(0\le f\le 1\), solve
\[
\mathcal L_C u=f-Qf .
\]
Then \(\mathcal L_C u\,dQ=\operatorname{div}(q C\nabla u)\,dx\). Since
\[
\chi\mathcal L_C u=\chi f-(Qf)\chi,
\]
we have
\[
P(\chi f)=\mathbb E_P[\chi\mathcal L_C u]+(Qf)P\chi .
\]
Thus
\[
Pf-Qf
=\mathbb E_P[\chi\mathcal L_C u]
+P((1-\chi)f)-(Qf)P(1-\chi).
\]
Both \(P((1-\chi)f)\) and \((Qf)P(1-\chi)\) lie between \(0\) and \(P(1-\chi)\), so
\[
|Pf-Qf|
\le |\mathbb E_P[\chi\mathcal L_C u]|+P(1-\chi).
\]

Now integrate by parts. On the support of \(\chi\), \(p=dP/dQ\) is smooth, so
\[
\mathbb E_P[\chi\mathcal L_C u]
=-\mathbb E_P[(C\nabla u)\cdot\nabla\chi]
-\mathbb E_P[\chi(C\nabla u)\cdot\nabla\log p].
\]
Using
\[
|(C\nabla u)\cdot v|
=|(C^{1/2}\nabla u)\cdot(C^{1/2}v)|
\le \kappa |C^{1/2}v|,
\]
we get
\[
\begin{aligned}
|Pf-Qf|
&\le \kappa\,\mathbb E_P[\chi|C^{1/2}(\nabla E_g-\nabla E_0)|]\\
&\quad+\kappa\,\mathbb E_P[\chi|C^{1/2}\nabla\log J|]\\
&\quad+\kappa\,\mathbb E_P|C^{1/2}\nabla\chi|\\
&\quad+P(1-\chi).
\end{aligned}
\]
Taking the supremum over such \(f\) gives the same bound for \(\operatorname{TV}(P_b,N_b)\).

## 3. Choice of cutoff

Choose a one-dimensional Lipschitz cutoff \(\eta\) with
\[
\eta(t)=1\quad(t\le 1),\qquad
\eta(t)=2-t\quad(1\le t\le 2),\qquad
\eta(t)=0\quad(t\ge 2).
\]
Then \(|\eta'|\le 1\). Set
\[
\chi(a)=\prod_e \eta(g|a_e|).
\]
Then \(\chi\) has the required support and
\[
|\nabla_e\chi(a)|\le g\,1_{\{g|a_e|\ge 1\}}.
\]

## 4. Bounding the four terms

Write \(L\) for the linear map \(a\mapsto(F_p)_p\), and \(D\) for the derivative of the nonlinear map \(a\mapsto(X_p)_p\). Put \(R_p=X_p-F_p\). Then
\[
\nabla E_g-\nabla E_0
=D^T X-L^T F
=(D-L)^T X+L^T(X-F).
\]

### First term

Since \(\|C^{1/2}L^T\|=1\),
\[
\|C^{1/2}L^T(X-F)\|
\le \|X-F\|_{\ell^2}
\le \sum_p |X_p-F_p|.
\]
By assumption,
\[
|X_p-F_p|\le \frac g4 A_p^2.
\]
Therefore
\[
\mathbb E\sum_p |X_p-F_p|
\le \frac g4\sum_p \mathbb E[A_p^2]
\le \frac g4 P_n\cdot 16K
=4gKP_n.
\]

For the other part, the assumption
\[
|D_hX_p-D_hF_p|\le \frac g2 A_p|h|
\]
implies that for each boundary link \(e\),
\[
|((D_p-L_p)^T X_p)_e|
\le \frac g2 A_p|X_p|.
\]
Each plaquette has four boundary links, so
\[
\sum_e |((D-L)^T X)_e|
\le 2g\sum_p A_p|X_p|.
\]
Also, from \(\|C_{ee}\|\le N^2\), one has
\[
\|C^{1/2}r\|\le N\sum_e |r_e|.
\]
Thus
\[
\mathbb E\|C^{1/2}(D-L)^T X\|
\le 2gN\sum_p \mathbb E[A_p|X_p|].
\]
By Cauchy–Schwarz,
\[
\mathbb E[A_p|X_p|]
\le \sqrt{\mathbb E[A_p^2]\,\mathbb E[|X_p|^2]}
\le \sqrt{16K\cdot 2C_1}.
\]
With
\[
K=\frac{\pi^2 C_1N^2}{2},
\]
we get
\[
\sqrt{32KC_1}=4\pi C_1N.
\]
Hence
\[
\mathbb E\|C^{1/2}(D-L)^T X\|
\le 2gN\cdot P_n\cdot 4\pi C_1N
=8\pi gC_1P_nN^2.
\]
Using \(4gKP_n=2\pi^2gC_1P_nN^2\), the first term is bounded by
\[
(8\pi+2\pi^2)gC_1P_nN^2
=Hg
\]
with
\[
\boxed{H=(2\pi^2+8\pi)C_1P_nN^2}.
\]

### Second term

On the support of \(\chi\), \(g|a_e|\le 2\), and by assumption
\[
|\nabla_e\log j_g(a_e)|\le \frac{g^2|a_e|}{5}.
\]
Therefore
\[
\mathbb E[\chi\|C^{1/2}\nabla\log J\|]
\le N\sum_e \frac{g^2}{5}\mathbb E|a_e|
\le \frac{g^2}{5}DN\sqrt K.
\]
So the second term contributes
\[
\frac{\kappa}{5}DN\sqrt K\,g^2.
\]

### Third term

Using the chosen \(\chi\),
\[
\|C^{1/2}\nabla\chi\|
\le N\sum_e |\nabla_e\chi|
\le Ng\sum_e 1_{\{g|a_e|\ge 1\}}.
\]
By Markov’s inequality,
\[
P(g|a_e|\ge 1)\le g^2\mathbb E|a_e|^2\le g^2K.
\]
Hence
\[
\mathbb E\|C^{1/2}\nabla\chi\|
\le Ng\cdot D\cdot g^2K
=DNK g^3.
\]
So the third term contributes
\[
\kappa DNK g^3.
\]

### Fourth term

Again by Markov,
\[
P(1-\chi)
\le \sum_e P(g|a_e|\ge 1)
\le Dg^2K.
\]

Combining the four bounds gives
\[
\mathbb E_\mu[\operatorname{TV}(P_b,N_b)]
\le \kappa H g+B g^2+\kappa DNK g^3
\]
with
\[
\boxed{B=D\left(K+\frac{\kappa N\sqrt K}{5}\right)}.
\]

## Comparison of constants

The constants in the statement are:

\[
\kappa,\qquad
H=(2\pi^2+8\pi)C_1P_nN^2,\qquad
B=D\left(K+\frac{\kappa N\sqrt K}{5}\right),
\]
and the final term coefficient is \(\kappa DNK\).

From the derivation above:

1. \(\kappa=\sqrt{\pi/8}\). This is the sharp dimension-free constant for the Stein solution \(C^{1/2}\nabla u\).  
   **Correct and sharp.**

2. The coefficient \(H=(2\pi^2+8\pi)C_1P_nN^2\) is exactly what the first term produces.  
   **Correct.**

3. The coefficient \(B=D(K+\kappa N\sqrt K/5)\) matches the second and fourth terms.  
   **Correct.**

4. The coefficient \(\kappa DNK\) in front of \(g^3\) matches the cutoff-gradient term.  
   **Correct.**

Thus the claimed bound is true with these constants.

## Regularity used

- \(E_g\) is smooth on the chart \(\Omega\), since each \(X_p\) is a smooth function of the exponential coordinates.
- \(j_g\) is smooth and strictly positive on the smaller support \(\{g|a_e|\le 2\}\), so \(\log J\) is smooth there.
- The density ratio \(p=dP/dQ\) is therefore smooth on the support of \(\chi\).
- \(\chi\) is Lipschitz and compactly supported strictly inside \(\Omega\), so the integration by parts
  \[
  \int \chi\,p\,\mathcal L_Cu\,dQ
  =
  -\int q\,C\nabla u\cdot\nabla(\chi p)\,dx
  \]
  has no boundary term.
- The Stein solution is valid and \(C^{1/2}\nabla u\) is bounded for \(f\in C_c^\infty\). The total variation bound then follows by approximating measurable \(0\le h\le 1\) by such \(f\) in \(L^1(P+Q)\).