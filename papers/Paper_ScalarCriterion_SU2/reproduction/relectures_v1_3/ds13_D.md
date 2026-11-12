### 1. Proposition 7.1 / hypothesis (C) for Wilson SU(2)

**Exact sentence:**  
> “Let \(t\) be a spatial torus with all sides at least \(2\), \(\beta>0\), and \(T=(MPC_\beta M)|_{\mathcal H_{\rm inv}}\) the transfer operator of \cite{TBv12} … so that \(K_t=e^{-6\beta V(t)}T\) satisfies \(Z_\beta(t,M)=\operatorname{Tr}K_t^M\) for \(M\ge2\) …”

**BLOCKING** as an unconditional proof, for the following reasons.

- **Rectangular fibres.** The “Scope” paragraph explicitly says:  
  > “The proofs of \cite{TBv12} are written there for one long direction and a square fibre \(F=(\mathbb Z/L)^2\); … we did not rewrite those proofs for rectangular fibres.”  
  But the proposition as stated covers *every* spatial torus with sides at least \(2\), and the later theorems use the rectangular tori \(\sigma_j=((2n)^j,n^{3-j})\). The assertion that the positivity proof “uses neither parity nor equality of the sides” is not a proof. Unless the extension to rectangular fibres is supplied, hypothesis (C) is not established for the main application.

- **Normalisation \(e^{-6\beta V(t)}\).** The factor is asserted, not derived in this section. Since it multiplies all twisted and untwisted traces, an error would cancel in ratios such as \(Z_k/Z_0\), but it is part of the claimed exact identity \(Z_k=\operatorname{Tr}(C^kK_t^M)\). It should be checked against the Wilson normalisation on rectangular tori, including the number of spatial plaquettes per time slice.

- **Odd sides/periods.** The cut construction with “a fixed plane \(x_i=c_i\)” and the statement that a spatial plaquette contains \(0\) or \(2\) links crossing the cut is standard, but the cited flux-sector proof may have additional parity/divisibility assumptions. The text does not verify this for odd \(L_i\).

**What I could not check:** the actual proof in TBv12 for rectangular fibres and the exact constant \(e^{-6\beta V(t)}\).

---

### 2. Are the Section 8 twisted partition functions the same as the Section 7 \(Z_k\)?

**Exact sentences:**  
Section 7:  
> “the sign of \(\frac12\operatorname{Tr}U_p\) is reversed on the temporal plaquettes of the planes \((0,i)\) lying above the cut \(i\), on one time layer”.  
Section 8:  
> “\(\epsilon_p=-1\) exactly on the plaquettes \((x;0,1)\) with \((x_0,x_1)\) fixed”.

**NON-BLOCKING**, but the wording should be tightened.

The two objects match under the natural interpretation that “one time layer” means a single fixed \(x_0\), and “lying above the cut \(i\)” means \(x_i=c_i\). Then Section 8’s stack at fixed \((x_0,x_1)\) is exactly the Section 7 object for one direction. For several directions, Section 8 says “all with the same time layer”, which is consistent with inserting \(C^k\) in a single factor \(K\) in \(\operatorname{Tr}(C^kK^M)\). However, Proposition 7.1’s phrase “on one time layer” could be read as one layer per direction, not necessarily the same layer. I recommend changing it to “a single common time layer”.

---

### 3. The lower bound \(\Delta_\beta(n)\ge 45\log 2\) asymptotically

**Exact sentence:**  
> “\(\displaystyle \liminf_{\beta\to\infty}\Delta_\beta(n)\ \ge\ 15\log8=45\log2\approx31.19\), which is the exact value \(\Delta_4\) of the deconfined \(\mathbb Z_2\) theory”.

**NON-BLOCKING**, with a wording caveat.

I find no internal contradiction with the published \(\Delta\ge0\), with monotonicity of pressure in the periods, or with Theorem R/Theorem 7.3/Proposition 7.5. The proof uses only the left half of the bracket,
\[
\Delta(n)\ge \sum_j 2^{3-j}\log(1+s_{\sigma_j}(n)),
\]
and Proposition sectors(d), which gives \(\log(1+s_j)\ge\varphi_j\). If all seven nontrivial twists on each \(\Sigma_j\) satisfy \(Z_k/Z_0\to0\), then \(D_j\to7/8\) and \(\varphi_j\to\log8\), so the lower bound follows. This is consistent with Theorem R because Theorem R only applies when \(\Delta(n)\le2^{-9}\); for large \(\beta\) at fixed \(n\) that hypothesis fails. It is also consistent with Theorem twosub’s two-sided equivalence: that theorem does not forbid a large \(\Delta\).

The only objection is that the phrase “which is the exact value \(\Delta_4\) of the deconfined \(\mathbb Z_2\) theory” could be misread as claiming equality for \(SU(2)\). The next sentence says “These are lower bounds, not limit values”, so the meaning is clear, but I would rephrase to avoid ambiguity.

---

### 4. Anteriority/novelty statements

**Exact sentence:**  
> “What we believe is new here is the exact additive decomposition (d) with the vacuum lemma (c), the extension to all cubes, all large times and tori of bounded aspect ratio through Theorem~\ref{thm:R}, the equivalence of Theorem~\ref{thm:twosub} with the criterion, and the scale bound of Proposition~\ref{prop:scale}; we have not searched the literature exhaustively.”

**NON-BLOCKING.** This is appropriately hedged. The later section also says:
> “We do not claim novelty for the asymptotics; we have not found the comparison in the form below…”

and explicitly flags that key older papers CGJK85 and vB84 have not yet been read. That is honest. I would only ensure that the final introduction does not strengthen this into an unqualified novelty claim before those prior-art checks are completed.

---

### What I could not check

- The TBv12 proof on rectangular fibres and the transfer-operator normalisation \(e^{-6\beta V(t)}\).
- The exact reading of BB26v5 Theorem 7.59 used in Proposition scale.
- The constants \(C(n)\), \(\beta_0(n)\), \(C_j\) in Theorem L and Corollary L1 are not explicit; I did not verify them numerically.