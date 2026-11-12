## Part 1

Assume \(0\leq\kappa<\infty\). For \(N=1\), there is no nonzero charge. For any \(N\), \(\rho_{N,0}(\kappa)=1\). Below, \(q\neq0\pmod N\).

**The proposed inequality is true.** In fact, a stronger universal inequality holds:
\[
\boxed{|A_q(t)|\leq \tanh |t|\,S(t).}
\]

Write \(r=|t|\). Since
\[
\sum_{j=0}^{N-1}\zeta^{qj}=0,\qquad e^{-r}\leq f_j(t)\leq e^r,
\]
subtracting \(e^{-r}\) gives
\[
|A_q(t)|
=\left|\sum_j\zeta^{qj}(f_j(t)-e^{-r})\right|
\leq S(t)-Ne^{-r}.
\]
Because \(S(t)\leq Ne^r\), this proves
\[
|A_q(t)|\leq (1-e^{-2r})S(t).
\]

For the stronger inequality, put
\[
a=e^{-r},\qquad b=e^r,\qquad
h=\frac{2ab}{a+b},\qquad
\eta=\frac{b-a}{b+a}=\tanh r.
\]
Every \(u\in[a,b]\) satisfies
\[
|u-h|\leq\eta u.
\]
Indeed, this is equivalent to
\((1-\eta)u\leq h\leq(1+\eta)u\), whose extreme cases are \(u=b\) and \(u=a\). Consequently,
\[
|A_q(t)|
=\left|\sum_j\zeta^{qj}(f_j(t)-h)\right|
\leq\sum_j|f_j(t)-h|
\leq\tanh r\,S(t).
\]

The sharp constants for \(N=2,3,4\) are
\[
\boxed{
\begin{array}{c|c|c}
N&q&\rho_{N,q}(\kappa)\\ \hline
2&1&\tanh\kappa\\[2mm]
3&1,2&\displaystyle\frac{e^{3\kappa/2}-1}{e^{3\kappa/2}+2}\\[3mm]
4&1,3&\tanh(\kappa/2)\\[1mm]
4&2&\tanh^2(\kappa/2)
\end{array}}
\]
In every row, \(t=\kappa\) attains the supremum.

**Proof for \(N=2\).** Writing \(t=x+iy\),
\[
\frac{|A_1(t)|}{S(t)}
=\frac{|e^x-e^{-x}|}{e^x+e^{-x}}
=|\tanh x|.
\]
Since \(|x|\leq|t|\leq\kappa\), the result follows, with equality at \(t=\kappa\).

**Proof for \(N=3\).** Put
\[
a=\Re t,\qquad b=\Re(\zeta t),\qquad c=\Re(\zeta^2t).
\]
For \(r=|t|\),
\[
a+b+c=0,\qquad a^2+b^2+c^2=\frac32r^2.
\]

We first determine the extrema of \(e^a+e^b+e^c\) under these constraints. For \(r>0\), the constraint set is a circle. At an extremum, its tangent derivative vanishes, so there are real \(\lambda,\mu\) such that
\[
e^a=\lambda+\mu a,\qquad
e^b=\lambda+\mu b,\qquad
e^c=\lambda+\mu c.
\]
A strictly convex exponential and a straight line cannot intersect at three distinct points. Thus at least two of \(a,b,c\) coincide. Solving the constraints shows that the only possible extremal triples, up to permutation, are
\[
(r,-r/2,-r/2),\qquad (-r,r/2,r/2).
\]
Moreover,
\[
e^r+2e^{-r/2}-(e^{-r}+2e^{r/2})
=4\sinh(r/2)\bigl(\cosh(r/2)-1\bigr)\geq0.
\]
Therefore, defining
\[
M_+=e^r+2e^{-r/2},\qquad M_-=e^{-r}+2e^{r/2},
\]
we have
\[
e^a+e^b+e^c\leq M_+,\qquad
e^{-a}+e^{-b}+e^{-c}\geq M_-.
\]

Since \(a+b+c=0\), direct expansion gives
\[
|e^a+\zeta e^b+\zeta^2e^c|^2
=(e^a+e^b+e^c)^2-3(e^{-a}+e^{-b}+e^{-c}).
\]
Hence
\[
\frac{|A_1(t)|^2}{S(t)^2}
\leq 1-\frac{3M_-}{M_+^2}
=\left(\frac{e^{3r/2}-1}{e^{3r/2}+2}\right)^2.
\]
Equality holds at \(t=r\). The displayed expression increases with \(r\), proving the formula on the disk. Finally, \(A_2(t)=\overline{A_1(t)}\), so the same result holds for \(q=2\). The case \(r=0\) is immediate.

**Proof for \(N=4\).** Write \(t=x+iy\). Then
\[
S(t)=2(\cosh x+\cosh y),
\]
\[
A_1(t)=2(\sinh x-i\sinh y),\qquad
A_2(t)=2(\cosh x-\cosh y).
\]

For \(q=2\), interchange \(x,y\) if necessary so that \(|x|\geq|y|\). Then
\[
\frac{|A_2(t)|}{S(t)}
=\frac{\cosh x-\cosh y}{\cosh x+\cosh y}
\leq\frac{\cosh\kappa-1}{\cosh\kappa+1}
=\tanh^2(\kappa/2).
\]
Equality holds at \((x,y)=(\kappa,0)\).

For \(q=1\), set
\[
u=\frac{x+y}{2},\qquad v=\frac{x-y}{2}.
\]
Elementary hyperbolic identities give
\[
\frac{|A_1(t)|^2}{S(t)^2}
=\frac{\tanh^2u+\tanh^2v}{2},
\qquad
u^2+v^2=\frac{x^2+y^2}{2}\leq\frac{\kappa^2}{2}.
\]
The function
\[
g(s)=\tanh^2\sqrt{s},\qquad s\geq0,
\]
is increasing and concave. To verify concavity, for \(z>0\),
\[
g'(z^2)=\frac{\tanh z\,\operatorname{sech}^2z}{z}>0,
\]
and
\[
\frac{d}{dz}\log g'(z^2)
=\frac1{\sinh z\cosh z}-2\tanh z-\frac1z<0,
\]
because \(\sinh z\cosh z\geq z\). Also \(g'(s)\to1\) as \(s\downarrow0\). Thus
\[
\frac{g(u^2)+g(v^2)}2
\leq g\!\left(\frac{u^2+v^2}{2}\right)
\leq g(\kappa^2/4).
\]
Taking square roots proves \(\rho_{4,1}(\kappa)=\tanh(\kappa/2)\), with equality at \(t=\kappa\). Conjugation gives the same result for \(q=3\).

**What I can prove for arbitrary \(N\), including \(N\geq5\).** There is an exact reduction to a one-dimensional maximization:
\[
\boxed{
\rho_{N,q}(\kappa)=
\max_{0\leq\theta\leq\pi/N}
\frac{\left|\displaystyle\sum_{j=0}^{N-1}
 \zeta^{qj}e^{\kappa\cos(\theta+2\pi j/N)}\right|}
{\displaystyle\sum_{j=0}^{N-1}
 e^{\kappa\cos(\theta+2\pi j/N)}}.
}
\tag{1}
\]
In particular, a maximizer lies on \(|t|=\kappa\).

Here is a proof of that boundary assertion. Regard \(t=x+iy\) and set
\[
H(t)=\frac{A_q(t)}{S(t)}.
\]
Each \(f_j\) satisfies \(\Delta f_j=f_j\), so
\[
\Delta A_q=A_q,\qquad \Delta S=S.
\]
Expanding \(\Delta(SH)\) yields
\[
LH=0,\qquad
L=\Delta+2\nabla\log S\cdot\nabla.
\]
This equation holds separately for the real and imaginary parts. Furthermore,
\[
|\partial_x\log S|\leq1,
\]
since it is a weighted average of numbers \(\cos(2\pi j/N)\).

For any real \(\phi\), let \(u=\Re(e^{-i\phi}H)\). Then \(Lu=0\), whereas
\[
L(e^{3x})=(9+6\partial_x\log S)e^{3x}>0.
\]
For \(\varepsilon>0\), \(u+\varepsilon e^{3x}\) cannot attain its maximum in the interior of the disk: at an interior maximum its gradient vanishes and its Laplacian is nonpositive, contradicting \(L(u+\varepsilon e^{3x})>0\). Letting \(\varepsilon\downarrow0\) gives
\[
u(t)\leq\max_{|z|=\kappa}u(z).
\]
Choose \(\phi\) so that \(u(t)=|H(t)|\). This proves the boundary assertion.

Finally,
\[
H(\zeta t)=\zeta^{-q}H(t),\qquad
H(\overline t)=\overline{H(t)}.
\]
These symmetries reduce the angular interval to \([0,\pi/N]\), proving (1).

Thus the exact constant is characterized by an explicit compact one-variable maximum, and
\[
0\leq\rho_{N,q}(\kappa)\leq\tanh\kappa<1
\quad(\kappa<\infty).
\]
Also \(\rho_{N,q}(\kappa)\to1\) as \(\kappa\to\infty\): along \(t=\kappa\), the \(j=0\) term dominates all other terms.

**My remaining limitation:** I do not prove which angle maximizes (1) for every \(N\geq5\). In particular, I do not assert that \(t=\kappa\) always maximizes it, or present its value there as a general closed form.

## Part 2

Let \(m=|P|\geq1\), and write
\[
G=\mathbb Z_N^P,\qquad
H=\left\{c\in G:\sum_pc_p=0\right\}.
\]

The assumptions I use are:

- \((\Omega,\Sigma,\mu)\) is a probability space.
- Each \(T_p:\Omega\to\mathbb C\) is measurable, with \(|T_p|\leq\kappa<\infty\) almost everywhere.
- \(R:\Omega\to[0,\infty)\) is measurable and belongs to \(L^1(\mu)\).
- For every required charge vector \(c\), there is a measurable map \(\tau_c\) with \((\tau_c)_*\mu=\mu\), satisfying the stated covariance and invariance almost everywhere.

Neither invertibility nor a group-action law is needed. Only finitely many maps are selected, so all required almost-everywhere identities can be imposed simultaneously on a common full-measure set.

The exponential factors lie between \(e^{-m\kappa}\) and \(e^{m\kappa}\), so every integral below is finite. If \(\int R=0\), the conclusions are trivial; otherwise all denominators are strictly positive.

**The sharp abstract constant is**
\[
\boxed{C=\rho_{N,q}(\kappa)^m.}
\tag{2}
\]

For \(a\in G\), define
\[
F(a)=\int_\Omega R\prod_{p\in P}f_{a_p}(T_p)\,d\mu.
\]
Measure preservation and covariance give
\[
F(a+c)=F(a)\qquad(c\in H).
\]
Consequently \(F(a)\) depends only on \(\sum_pa_p\), and
\[
F(a)=Z_{\sum_pa_p}.
\]
Each fiber of the sum map \(G\to\mathbb Z_N\) has \(N^{m-1}\) elements. Therefore
\[
\sum_k Z_k
=N^{1-m}\int_\Omega R\prod_p S(T_p)\,d\mu,
\tag{3}
\]
and, using \(\zeta^{q\sum_pa_p}=\prod_p\zeta^{qa_p}\),
\[
\sum_k\zeta^{qk}Z_k
=N^{1-m}\int_\Omega R\prod_p A_q(T_p)\,d\mu.
\tag{4}
\]
Taking absolute values and applying Part 1 separately to each factor proves (2).

**Sharpness.** Choose \(t_*\) attaining \(\rho_{N,q}(\kappa)\), whose existence follows from continuity on the compact disk. Take
\[
\Omega=H
\]
with uniform probability measure, and define
\[
T_p(h)=\zeta^{h_p}t_*,
\qquad R=1,\qquad
\tau_c(h)=h+c.
\]
These maps realize every charge in \(H\). Since
\[
S(\zeta^jt_*)=S(t_*),\qquad
A_q(\zeta^jt_*)=\zeta^{-qj}A_q(t_*),
\]
we have, for \(h\in H\),
\[
\prod_pA_q(T_p(h))=A_q(t_*)^m.
\]
Equations (3)–(4) now give
\[
\frac{\left|\sum_k\zeta^{qk}Z_k\right|}{\sum_kZ_k}
=\left|\frac{A_q(t_*)}{S(t_*)}\right|^m
=\rho_{N,q}(\kappa)^m.
\]
Thus no smaller universal constant is possible.

**Open-surface variant.** Now assume every vector \(c\in G\) is realized. Let \(W\) be measurable, \(|W|\leq1\) almost everywhere, and
\[
W(\tau_c\omega)=
\zeta^{q\sum_{p\in A}c_p}W(\omega).
\]
Put
\[
Z=\int_\Omega R e^{\sum_p\Re T_p}\,d\mu.
\]
Averaging the transformed integral over all \(c\in G\) gives
\[
\int_\Omega WR e^{\sum_p\Re T_p}\,d\mu
=
N^{-m}\int_\Omega WR
\prod_{p\in A}A_q(T_p)
\prod_{p\notin A}S(T_p)\,d\mu.
\]
The same averaging without \(W\) gives
\[
Z=N^{-m}\int_\Omega R\prod_pS(T_p)\,d\mu.
\]
Hence
\[
\boxed{
\left|\int_\Omega WR e^{\sum_p\Re T_p}\,d\mu\right|
\leq \rho_{N,q}(\kappa)^{|A|}Z.
}
\tag{5}
\]
For \(A=\varnothing\), the factor is \(1\).

This constant is also sharp: take \(\Omega=G\) uniformly,
\[
T_p(h)=\zeta^{h_p}t_*,
\qquad W(h)=\zeta^{q\sum_{p\in A}h_p},
\qquad R=1,
\]
with translations \(\tau_c\). Direct factorization gives equality in modulus.

The full-charge hypothesis matters. If only \(H\) is realized, take \(A=P\) and \(W=1\). Its required covariance on \(H\) is then trivial, while (5) would incorrectly require \(Z\leq\rho^mZ\).

## Part 3

For the requested radius \(\kappa=\beta l^2\), assume \(\beta\geq0\). For arbitrary real \(\beta\), the same proof uses \(\kappa=|\beta|l^2\).

**The claimed numerical bound is true:**
\[
\boxed{
\left|\sum_{k=0}^{N-1}\zeta^{qk}Z_k\right|
\leq
\rho_{N,q}(\beta l^2)^{\,l^2}
\sum_{k=0}^{N-1}Z_k.
}
\tag{6}
\]

There is, however, a correction to the requested invariance statement: the transformations generally change \((0,1)\)-plaquettes at other base points. Those plaquettes must be included among the variables being averaged.

**The variables and invariant weight.** Write
\[
p=(u,v)=(x_0,x_1)\in B=(\mathbb Z/l\mathbb Z)^2,
\qquad y=(x_2,x_3).
\]
Use the abstract index set \(P=B\), and define
\[
T_{u,v}(U)=\frac{\beta}{N}
\sum_{y\in(\mathbb Z/l\mathbb Z)^2}
\operatorname{Tr}U_{(u,v,y),01}.
\tag{7}
\]
Thus each abstract variable collects an entire transverse fiber of \(l^2\) plaquettes. Since every plaquette matrix is unitary,
\[
|\operatorname{Tr}U_{x,01}|\leq N,
\qquad |T_{u,v}|\leq\beta l^2.
\]

Define
\[
R(U)=
\exp\!\left[
\frac{\beta}{N}
\sum_{\substack{x,\ \mu<\nu\\(\mu,\nu)\ne(0,1)}}
\Re\operatorname{Tr}U_{x,\mu\nu}
\right].
\tag{8}
\]
The untwisted weight is exactly
\[
R(U)\exp\!\left(\sum_{p\in B}\Re T_p(U)\right),
\]
and the specified twist replaces \(T_{a,b}\) by \(\zeta^kT_{a,b}\). Thus these are precisely the \(Z_k\) of Part 2.

The configuration space is \(SU(N)^{4l^4}\), with normalized product Haar measure. All functions in (7)–(8) are continuous. In particular,
\[
e^{-5\beta l^4}\leq R\leq e^{5\beta l^4},
\]
and every twisted full weight lies between \(e^{-6\beta l^4}\) and \(e^{6\beta l^4}\). All integrability and positivity assumptions are therefore satisfied.

**The link transformations.** Choose arbitrary functions
\[
s_0,s_1:B\to\mathbb Z_N.
\]
For every transverse coordinate \(y\), define
\[
\begin{aligned}
(\tau_sU)((u,v,y),0)&=\zeta^{s_0(u,v)}U((u,v,y),0),\\
(\tau_sU)((u,v,y),1)&=\zeta^{s_1(u,v)}U((u,v,y),1),
\end{aligned}
\tag{9}
\]
and leave links in directions \(2,3\) unchanged.

Here \(\zeta^j\) means \(\zeta^jI_N\). This belongs to \(SU(N)\), since its determinant is \(\zeta^{jN}=1\). Each coordinate map in (9) is left multiplication by a fixed group element. It preserves Haar measure, is continuous, and has inverse obtained by replacing \(s\) with \(-s\). Hence \(\tau_s\) preserves the full product measure.

For arbitrary central link exponents \(s_\mu(x)\), multiplication around the plaquette gives the phase
\[
c_{\mu\nu}(x)
=s_\mu(x)+s_\nu(x+\widehat\mu)
-s_\mu(x+\widehat\nu)-s_\nu(x).
\tag{10}
\]
This follows directly because central factors commute with every link and an inverse link contributes the inverse central factor.

For (9), equation (10) becomes
\[
c(u,v)
=s_0(u,v)-s_0(u,v+1)
+s_1(u+1,v)-s_1(u,v)
\tag{11}
\]
in orientation \((0,1)\). It is independent of \(y\), so
\[
T_{u,v}(\tau_sU)=\zeta^{c(u,v)}T_{u,v}(U).
\tag{12}
\]

For every other orientation,
\[
\begin{aligned}
c_{02}(x)&=s_0(x)-s_0(x+\widehat2)=0,\\
c_{03}(x)&=s_0(x)-s_0(x+\widehat3)=0,\\
c_{12}(x)&=s_1(x)-s_1(x+\widehat2)=0,\\
c_{13}(x)&=s_1(x)-s_1(x+\widehat3)=0,\\
c_{23}(x)&=0.
\end{aligned}
\]
Thus all five other plaquette orientations are unchanged as matrices, and
\[
R(\tau_sU)=R(U).
\]

The twisted weight transforms exactly into
\[
R(U)\exp\!\left[
\sum_{p\in B}\Re\bigl(\zeta^{\,k1_{\{p=(a,b)\}}+c(p)}T_p(U)\bigr)
\right].
\tag{13}
\]
It redistributes twist charges among base points while preserving their total.

**Every zero-sum charge vector is realized.** Summing (11) over the periodic base gives
\[
\sum_{u,v}c(u,v)=0
\]
by telescoping.

Conversely, let \(c:B\to\mathbb Z_N\) have total sum zero. The following construction uses only addition and subtraction, so it works for composite \(N\) and for every \(l\geq2\).

Using representatives \(0,\ldots,l-1\), put
\[
r(v)=\sum_{u=0}^{l-1}c(u,v).
\]
Define
\[
s_0(u,v)=
\begin{cases}
-\displaystyle\sum_{b=0}^{v-1}r(b),&u=0,\\
0,&u\ne0.
\end{cases}
\tag{14}
\]
The empty sum is zero. Periodicity and \(\sum_vr(v)=0\) imply
\[
s_0(u,v)-s_0(u,v+1)=1_{\{u=0\}}r(v),
\]
including at \(v=l-1\).

Set
\[
d(u,v)=c(u,v)-1_{\{u=0\}}r(v).
\]
Then \(\sum_ud(u,v)=0\) for each \(v\). Define
\[
s_1(u,v)=\sum_{a=0}^{u-1}d(a,v).
\tag{15}
\]
Again, including the periodic wraparound,
\[
s_1(u+1,v)-s_1(u,v)=d(u,v).
\]
Substitution into (11) returns exactly \(c(u,v)\). This proves surjectivity onto all zero-sum charges.

**The case \(l=2\), explicitly.** Write the prescribed charges as
\[
c_{00},c_{10},c_{01},c_{11},
\qquad c_{00}+c_{10}+c_{01}+c_{11}=0.
\]
Choose
\[
\begin{array}{c|rrrr}
(u,v)&(0,0)&(1,0)&(0,1)&(1,1)\\ \hline
s_0(u,v)&0&0&-(c_{00}+c_{10})&0\\
s_1(u,v)&0&-c_{10}&0&-c_{11}.
\end{array}
\]
Formula (11) gives, in the same order,
\[
c_{00},\quad c_{10},\quad
-(c_{00}+c_{10})-c_{11},\quad c_{11},
\]
which is the prescribed vector. There is no division by \(2\).

This uses the link convention in the question: the positive links labelled \((x,\mu)\) and \((x+\widehat\mu,\mu)\) remain distinct link variables when \(l=2\). Reversing a labelled link introduces its inverse; it does not identify these two positive links.

**Why the additional invariance demand needs correction.** A base point \(p\ne(a,b)\) acquires phase \(\zeta^{c(p)}\) under (9), so its \((0,1)\)-plaquettes are invariant precisely when \(c(p)=0\).

More generally, for any central link multiplication, even one depending on all four coordinates, (10) implies
\[
\sum_{u,v}c_{01}(u,v,y)=0
\]
for each fixed \(y\). If every \((0,1)\)-plaquette away from the single base point \((a,b)\) were invariant, this would force
\[
c_{01}(a,b,y)=0
\]
as well. Such transformations cannot create nontrivial charges solely on that sheet while leaving all other plaquettes fixed.

The correct decomposition is therefore (7)–(8): all \((0,1)\)-fibers belong to \(P\); the other orientations form \(R\).

All hypotheses of Part 2 now hold with
\[
|P|=l^2,\qquad \kappa=\beta l^2,
\]
proving (6). In particular, one may use
\[
C\leq\tanh(\beta l^2)^{l^2}
\leq(1-e^{-2\beta l^2})^{l^2},
\]
or the sharper closed forms from Part 1 for \(N=3,4\). Sharpness in the abstract setting does not assert sharpness for the restricted \(SU(N)\) lattice variables.

**Relation to flux projectors.** Define, purely algebraically,
\[
\Phi_q=\frac1N\sum_{k=0}^{N-1}\zeta^{qk}\frac{Z_k}{Z_0}.
\]
Then
\[
\sum_k\zeta^{qk}Z_k=NZ_0\Phi_q,\qquad
\sum_kZ_k=NZ_0\Phi_0,
\]
and the bounded ratio is
\[
\frac{|\Phi_q|}{\Phi_0}.
\]
Also \(\sum_q\Phi_q=1\), by finite character orthogonality.

[MEMORY, UNVERIFIED] In the Tomboulis–Yaffe/Kanazawa formalism, these Fourier combinations are electric-flux projector expectations, with a possible replacement \(q\leftrightarrow -q\) depending on the twist convention. In a transfer description with a center operator \(V\), \(V^N=1\), the corresponding projector is
\[
P_q=\frac1N\sum_k\zeta^{qk}V^k.
\]
If the twisted partition functions are represented as \(Z_k=\operatorname{Tr}(KV^k)\), then
\[
\sum_k\zeta^{qk}Z_k=N\operatorname{Tr}(KP_q).
\]
The identification of the lattice twists with that transfer representation is recalled here, not independently proved or needed for (6).

[MEMORY, UNVERIFIED] For \(SU(2)\), the conventional electric-flux quantity is
\[
e^{-F_{\mathrm{el}}}=\frac{Z_0-Z_1}{2Z_0}=\Phi_1.
\]
Thus, writing the signed twist ratio as \(r=(Z_0-Z_1)/(Z_0+Z_1)\),
\[
r=\frac{\Phi_1}{1-\Phi_1},
\qquad
\Phi_1=\frac{r}{1+r}.
\]
This specifies the normalization difference.

**Scope and palette checks.** This finite-volume estimate does not establish a four-dimensional mass gap or a volume-uniform area law. Its constant approaches \(1\) as the transverse size grows. Indeed, let
\[
\delta_N=\min_{j\ne0}\bigl(1-\cos(2\pi j/N)\bigr)>0.
\]
Evaluation at \(t=\kappa\), using the reverse triangle inequality, gives
\[
1-\rho_{N,q}(\kappa)\leq2(N-1)e^{-\delta_N\kappa}.
\]
Therefore, for fixed \(\beta>0\),
\[
0\leq1-\rho_{N,q}(\beta l^2)^{l^2}
\leq2(N-1)l^2e^{-\delta_N\beta l^2}\longrightarrow0.
\]
For F1, the finite center-averaging mechanism also applies to finite subgroups of \(U(1)\) and to higher-dimensional finite lattices; it makes no confinement claim in their weak-coupling phases. For F2, no spectral-gap lower bound is obtained, and the displayed contraction degenerates exponentially with increasing coupling or transverse area.

The five retained mathematical objects are:

| Palette group | Precise object and what it establishes here | Status | Resolves the 4D gap obstruction? |
|---|---|---|---|
| 1 | \(L=\Delta+2\nabla\log S\cdot\nabla\), with barrier \(e^{3x}\): reduces the disk supremum to its boundary | Proved above | No |
| 18 | Exponential extrema on the three-logit circle; concavity of \(\tanh^2\sqrt{s}\): sharp \(N=3,4\) constants | Proved above | No |
| 22 | Characters of \(\mathbb Z_N^P\) and the sum map: exact product identities and sharp abstract bounds | Proved above | No |
| 7 | Periodic discrete curl (11), with explicit right inverse (14)–(15): realizes every zero-sum charge | Proved above | No |
| 26 | Fourier normalization of twisted partition functions: identifies the ratio of flux components | Algebra proved; projector interpretation recalled | No |

Perelman entropy is discarded: no flow or entropy functional controlling these ratios is constructed.  
KAM is discarded: no invariant-torus or small-divisor problem occurs here.

The local record already precedes the SU(2) conclusion at [dossier_ym.md:382](/root/physique/qlab/prompts/dossier_ym.md:382), and records the general factor \(1-e^{-2\kappa}\) at [REVUES_PILOTE.md:2251](/root/physique/qlab/registre/REVUES_PILOTE.md:2251). That factor is an admissible bound, not the sharp supremum defined in this question. The classical flux context is also recorded at [dossier_ym.md:385](/root/physique/qlab/prompts/dossier_ym.md:385). I make no novelty or absence claim.

memory consulted: tube, pont, flux, projecteur, rho, plaquette; retournement.colonne, centre_zn, projecteur.flux; Tomboulis, Kanazawa, electric.flux; Fourier, centre, Brezzi, Jensen, KAM, Perelman.

palette: elliptic boundary maximum; elementary constrained optimization; finite Fourier averaging; periodic discrete curl; flux-projector normalization / Perelman entropy and KAM discarded.

The palette and local records were read; the read-only workspace prevented appending a palette log.

END