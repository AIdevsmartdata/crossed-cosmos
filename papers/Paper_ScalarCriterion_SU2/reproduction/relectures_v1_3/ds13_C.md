## S1  
TRUE.

- Clearly \(Z_0(M)=\sum_i r_i^M\).
- For fixed \(i\),  
  \[
  \sum_{k\in\mathbb Z_2^3}(-1)^{k\cdot e_i}=
  \begin{cases}
  8,& e_i=0,\\
  0,& e_i\neq 0.
  \end{cases}
  \]
  Hence
  \[
  \sum_k Z_k(M)=8\operatorname{Tr}_0(M).
  \]
- Therefore
  \[
  D=\frac18\sum_{k\neq0}\left(1-\frac{Z_k}{Z_0}\right)
  =\frac18\left(7-\frac{8\operatorname{Tr}_0-Z_0}{Z_0}\right)
  =1-\frac{\operatorname{Tr}_0}{Z_0}.
  \]
- Since \(r_{i0}=1\), \(Z_0=1+s\), so \(h=\log(1+s)=\log Z_0\). Also \(1+s0=\operatorname{Tr}_0\) and \(\sum_kZ_k=8\operatorname{Tr}_0\). Thus
  \[
  \log(1+s0)+\log\!\left(\frac{8Z_0}{\sum_kZ_k}\right)
  =\log\operatorname{Tr}_0+\log\frac{Z_0}{\operatorname{Tr}_0}
  =\log Z_0=h.
  \]

---

## S2  
TRUE.

Let
\[
B_k=\sum_{\substack{i\neq i0\\ k\cdot e_i=1}} r_i^M.
\]
Then \(s=\sum_{i\neq i0}r_i^M\), \(Z_0=1+s\), and
\[
Z_k=1+(s-B_k)-B_k=1+s-2B_k.
\]
Hence
\[
1-\frac{Z_k}{Z_0}
=1-\frac{1+s-2B_k}{1+s}
=\frac{2B_k}{1+s}.
\]
Since \(0\le B_k\le s\) and \(1+s\ge 1\),
\[
0\le \frac{2B_k}{1+s}\le \frac{2s}{1+s}\le 2s.
\]

---

## S3  
TRUE.

Given \(0\le R_k\le r\) for all seven \(k\neq0\),
\[
\sum_{k\neq0}R_k\le 7r.
\]
Thus
\[
1-D=\frac{1+\sum_{k\neq0}R_k}{8}\le \frac{1+7r}{8}.
\]
Therefore
\[
-\log(1-D)=\log\frac1{1-D}
\ge \log\frac8{1+7r}.
\]
If \(r\le 1/7\), then \(1+7r\le 2\), so
\[
\log\frac8{1+7r}\ge \log 4.
\]

For the second part, write
\[
\sum_{k\neq0}R_k=3R+S,
\]
where \(S\) is the sum of the other four \(R_k\)'s, hence \(0\le S\le 4\). Then
\[
D=\frac{7-3R-S}{8}
\ge \frac{7-3R-4}{8}
=\frac{3(1-R)}8.
\]
Also
\[
1-D=\frac{1+3R+S}{8}
\le \frac{5+3R}{8},
\]
so
\[
-\log(1-D)\ge \log\frac8{5+3R}.
\]

---

## S4  
TRUE.

For each \(j\), all summands are nonnegative and the coefficient \(2^{3-j}\) is at least \(1\). Hence
\[
2^{3-j}\bigl(\log(1+s0_j)+\phi_j\bigr)\le \Delta.
\]
Thus
\[
\log(1+s0_j)+\phi_j\le \Delta,
\]
so in particular
\[
\log(1+s0_j)\le \Delta
\]
and
\[
\phi_j=-\log(1-D_j)\le \Delta.
\]
The latter gives
\[
1-D_j\ge e^{-\Delta},
\]
hence
\[
D_j\le 1-e^{-\Delta}.
\]

If \(D_j\to 7/8\) for every \(j=0,1,2,3\), then
\[
\phi_j=-\log(1-D_j)\to -\log(1/8)=\log 8.
\]
Since \(\log(1+s0_j)\ge 0\), the weighted sum is eventually at least
\[
\sum_{j=0}^3 2^{3-j}(\log 8-\epsilon)
=(8+4+2+1)(\log 8-\epsilon)
=15(\log 8-\epsilon).
\]
Thus
\[
\liminf \Delta\ge 15\log 8.
\]

---

## S5  
TRUE.

From
\[
\Omega_0\Omega_1=-\Omega_1\Omega_0,
\]
multiplying on the right by \(\Omega_0^{-1}\) gives
\[
\Omega_0\Omega_1\Omega_0^{-1}=-\Omega_1.
\]
Conjugation preserves trace, so
\[
\operatorname{tr}\Omega_1=-\operatorname{tr}\Omega_1,
\]
hence \(\operatorname{tr}\Omega_1=0\). Similarly, \(\operatorname{tr}\Omega_0=0\).

For a \(2\times2\) matrix with \(\operatorname{tr}\Omega_j=0\) and \(\det\Omega_j=1\), Cayley–Hamilton gives
\[
\Omega_j^2-(\operatorname{tr}\Omega_j)\Omega_j+(\det\Omega_j)I=0,
\]
so
\[
\Omega_j^2+I=0,
\]
i.e. \(\Omega_j^2=-I\).

Now suppose \(W\in SU(2)\) commutes with both. Since \(\Omega_0^2=-I\), any \(W\) commuting with \(\Omega_0\) has the form
\[
W=aI+b\Omega_0
\]
with real \(a,b\) and \(a^2+b^2=1\). Since \(W\) also commutes with \(\Omega_1\),
\[
0=[W,\Omega_1]=b[\Omega_0,\Omega_1].
\]
But
\[
[\Omega_0,\Omega_1]
=\Omega_0\Omega_1-\Omega_1\Omega_0
=2\Omega_0\Omega_1\neq 0.
\]
Thus \(b=0\), so \(W=aI\). Since \(\det W=1\), \(a^2=1\), so \(a=\pm1\). Therefore
\[
W=\pm I.
\]

All statements are true as stated.