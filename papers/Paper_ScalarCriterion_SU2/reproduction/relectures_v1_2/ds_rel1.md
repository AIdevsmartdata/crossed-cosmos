(A) Table of statements and verdicts

| Statement | Verdict | Reason (re-derived/checked) |
|---|---|---|
| Step 1: monotonicity of \(f=\log Z/|x|\) | CORRECT | Writing \(Z(t,M)=\lambda_0^M(1+s_t(M))\) gives \(f(t,M)=\lambda_0(t)/V(t)+h_t(M)/(MV(t))\). Since \(0\le r_i\le1\), \(s_t(M)\) and \(h_t(M)\) are non-negative non-increasing; \(1/M\) is non-negative decreasing, so their product is non-increasing. Symmetry (W1) gives the same for spatial coordinates. Also \(h_t(M)\le h_t(3)<\infty\) by trace-class, so \(h_t(M)/M\to0\). |
| Step 2: recursion at every base \(m_j\) | CORRECT | \(f(m^4)-f((2m)^4)=\Delta(m)/(16m^4)\). Monotonicity gives \(f(m^4)\ge f((2m)^4)\), hence \(\Delta(m)\ge0\). At every \(m_j=2^j n\ge3\), the hypotheses of the published doubling proposition are met: (W1)-(W2) hold for all sections with sides at least \(3\), and induction gives \(\Delta_j\le2^{-9}\). Thus \(\Delta_{j+1}\le256\Delta_j^2\le(1/2)\Delta_j\), so \(256\Delta_j\le q^{2^j}\). |
| Step 3: telescoping | CORRECT | \(f(m_i^4)-f(m_{i+1}^4)=\Delta_i/(16m_i^4)\). With \(k=i-j\), term ratio is \(\le 2^{-k}/16^k=32^{-k}\); \(\sum_{k\ge0}32^{-k}=32/31\); multiplied by \(1/16\) gives \(2/31\). |
| Step 4: torus vs diagonal | CORRECT | Choose \(J\) with all sides and \(M\) bounded by \(m_J\). Monotonicity gives \(f(t,M)\ge f(m_J^4)\), and Step 3 gives \(f(m_J^4)\ge f(m^4)-2\Delta(m)/(31m^4)\). The bound is uniform in \(M\), so \(M\to\infty\) is legitimate. Also \(f(t,m)\le f(m^4)\). Subtraction yields \(h_t(m)\le2\Delta(m)V/(31m^3)\). No aspect-ratio assumption is used. |
| Part (b): \(T_0=16n\), \(\gamma\), \(y_0\) | CORRECT | Doubling chain: \(2^{-9}\to2^{-10}\to2^{-12}\to2^{-16}\to2^{-24}\). Hence \(2\Delta(16n)/(31T_0^3)\le 1/(31\cdot2^{23}T_0^3)=\gamma\). Also \(2\gamma(96T_0)^3=2\cdot96^3/(31\cdot2^{23})=27/3968<1/20\). |
| Part (c): all integer cubes \(N\ge n\) | CORRECT | Choose \(p=2^j\) with \(m=pn\le N<2m\). Then \(V<8m^3\), so \(h\le16\Delta(m)/31\le q^p/496\). Then \(r^m\le e^h-1\le2h\le q^p/248\). Since \(r^m=(r^n)^p\), \(r^n\le q/248^{1/p}\le q\). |
| Part (d): aspect ratio \(\le24\) | CORRECT | \(V<4608m^3\), so \(h\le9216\Delta(m)/31\le(36/31)q^p\le(18/31)2^{1-p}\). Convexity gives \(e^{\alpha x}-1\le\alpha(e^x-1)\) for \(\alpha=2^{1-p}\in(0,1]\). With \(\theta=e^{18/31}-1\in(1/2,1)\), \(s_t(m)\le2^{1-p}\theta\le\theta^p\), hence \(r^n\le\theta\). \(- \log\theta\approx0.2393\). |
| Published Proposition constants | CORRECT | Re-checked \(G_1\le2.004D\), \(G_2\le4.024D\), \(G_3\le8.113D\); the displayed sum rounds to \(250.148D^2\le256D^2\). Limit as \(D\to0\) is \(240D^2\). |
| Edge cases \(n=3\), odd/non-cubic sides, \(\Delta=0\) | CORRECT | Proof uses only periods \(\ge3\); no divisibility is required except the dyadic \(m_j\). If \(\Delta(n)=0\), then \(q=0\), all shown ratios vanish, and the constants still work. |
| Remark (ii) on degenerate \(\lambda_0\) | GAP, non-blocking wording | The hypothesis \(\Delta(n)\le2^{-9}\) excludes \(r_i=1\) for the cubes in (c) and the bounded-aspect tori in (d), not necessarily for arbitrary spatial tori with unbounded aspect. The proof itself is unaffected. |
| Remark (i): counterexample with \(\rho=-r\) | CORRECT | The product is symmetric. For a section \(t\), \(Z(t,M)=A^M(1+\rho^M)^V\) with \(A=\prod_{\mu=1}^3(1+\rho^{t_\mu})^{V/t_\mu}\), so \(Z(t,M)=\operatorname{Tr}K_t^M\) for \(K_t=A(1\oplus\rho)^{\otimes V}\). For odd \(n\), \(\Delta(n)=64n^3\log(1-r^n)-32n^3\log(1+r^{2n})<0\). This violates positivity of \(K_t\). |
| Match with BB26 (B*) | CORRECT | Theorem R(b) proves \(h_t(T_0)=\log\widehat Z_t(T_0)\le\gamma V(t)\) for all tori with sides \(\ge T_0\), hence a fortiori for the window \([2T_0,48T_0)\). The constant \(y_0=27/3968\) satisfies \(y_0\le1/20\). |
| Corollary/bridge | CORRECT, conditional | It is explicitly marked conditional on BB26 Theorem F and hypothesis (W) “as we read them; not verified by us.” It does not claim a proof of the mass gap. |
| Lean description | CORRECT | ENONCES.lean contains `interpolation`, `reciproque_Bstar`, and `trou_cubes`, matching the claimed formalised statements. It does not formalise (d), the log form of (c), or the reduction from periods \(\ge1\) to periods \(\ge3\). |
| Priority/comparison/AI wording | CORRECT | The comparison is hedged (“passages read”, “not a proof of absence”), and no priority or mass-gap claim is made. |

(B) Required corrections

1. Non-blocking. In Remark (ii), replace  
   “degenerate eigenvalues are ratios \(r_i=1\), which the hypothesis \(\Delta(n)\le2^{-9}\) excludes”  
   with  
   “degenerate eigenvalues are ratios \(r_i=1\); the gap conclusions in parts (c) and (d) exclude them for the cubes \((N,N,N)\) and for bounded-aspect tori, but the hypothesis alone does not rule them out for arbitrary unbounded-aspect spatial tori.”

2. Non-blocking. In the “Consequence” paragraph, the phrase “up to the choice of the scale (a factor \(16\))” is potentially ambiguous because the forward implication uses a factor \(2\). Replace with:  
   “up to a change of scale: (B*) at \(T_0\) implies \(\Delta(2T_0)\le2^{-9}\), while \(\Delta(n)\le2^{-9}\) implies (B*) at \(16n\); composing the two gives (B*) at \(T_0\) implies (B*) at \(32T_0\).”

3. Non-blocking. In Theorem R(a), it would improve clarity to state explicitly that the condition \(\Delta(m_j)\le2^{-9}\) used in the doubling proposition is part of the induction established in Step 2. No mathematical change is needed.

(C) Overall verdict

No blocking mathematical error was found in the proof of Theorem R. The monotonicity, recursion, telescoping, limit, and all constants check out. The edge cases are handled correctly, and the comparison with BB26 is fair and appropriately conditional. The only issues are minor wording points, principally the degeneracy remark and the scale-factor wording.