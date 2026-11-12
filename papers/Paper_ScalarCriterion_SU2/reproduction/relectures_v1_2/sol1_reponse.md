I found **no mathematical failure in Theorem R under its stated global assumptions**. Publication still needs corrections to scope and review disclosures. All checks below were read-only; no scripts, builds, network requests or file writes were performed.

**(A) Audit table**

Line references refer to the [candidate TeX](/root/physique/publication/critere_scalaire_2026-11/v1_2/relectures/sol/scalar_criterion_su2_v1_2.tex).

| Statement | Verdict | Reason |
|---|---|---|
| Step 1: pressure monotonicity | CORRECT | \(s_t(M)\ge0\) decreases termwise because \(0\le r_i\le1\). Thus \(h_t(M)\ge0\) decreases, and its product with \(1/M\) decreases. The possibly negative vacuum contribution is constant in \(M\), so causes no problem. Symmetry transfers this argument to every coordinate. |
| Step 1: cylinder limit | CORRECT | \(0\le h_t(M)\le h_t(3)<\infty\), hence \(h_t(M)/M\to0\). This does **not** require a simple leading eigenvalue or \(h_t(M)\to0\). |
| Step 2: non-negativity and recursion at every base | CORRECT | \(\Delta(m)=16m^4[f(m^4)-f((2m)^4)]\ge0\). The published proposition’s proof uses periods \(m,2m,4m\); at every \(m_j\ge3\), all required rectangular sections remain within the assumed domain. No evenness assumption appears. Induction preserves the threshold and gives \(256\Delta_j\le q^{2^j}\). |
| Step 3: \(32\) and \(2/31\) | CORRECT | The deficit contributes \(2^{-k}\), while the four-volume contributes \(16^{-k}\). Therefore \(\frac1{16}\sum_{k\ge0}32^{-k}=\frac1{16}\frac{32}{31}=\frac2{31}\). |
| Step 4: choice of \(J\), limits and subtraction | CORRECT | For each fixed \(M\), choose \(J>j\) dominating all four periods. The resulting lower bound is independent of \(M\). Only afterward is \(M\to\infty\) taken. Separately, \(t_i\ge m\) gives \(f(t,m)\le f(m^4)\). Subtraction gives exactly \(2\Delta(m)V(t)/(31m^3)\). No exchange of limits occurs. |
| (b): four iterations and numerical constant | CORRECT | The exponents are \(9\to10\to12\to16\to24\). Thus \(\gamma=2^{-23}/(31T_0^3)\), and \(2\gamma(96T_0)^3=27/3968<1/20\). Every side in \([2T_0,48T_0)\) is certainly at least \(T_0\). |
| (c): arbitrary integer cubes | CORRECT | Choosing \(m=2^jn\le N<2m\) gives \(V<8m^3\), hence \(h\le q^p/496\le1/992\). Consequently \(r^m\le e^h-1\le2h\le q^p/248\le q^p\). Since \(m=pn\), taking the positive integer power root gives \(r^n\le q\). |
| (d): rectangular tori and final constant | CORRECT | \(V\le576a^3<4608m^3\), including aspect ratio exactly \(24\). Therefore \(h\le(36/31)q^p\le(18/31)2^{1-p}\). Convexity gives the stated estimate with \(\theta=e^{18/31}-1\approx0.78719\). Since \(1/2<\theta<1\), \(2^{1-p}\le\theta^{p-1}\). Finally, \(-\log\theta\approx0.239284\), correctly rounded to \(0.2393\). |
| \(n=3\), odd sides, non-cubic sections | CORRECT | The paper proof needs only integer periods at least \(3\). Coordinate monotonicity has no divisibility condition. The Wilson transfer representation remains an explicit hypothesis; the argument does not silently prove it. |
| (W2): “every \(N\ge1\)” versus the paper’s domain | GAP | This is a domain-description inconsistency, **not a failure of R**. Section 4 only needs \(N,t_i\ge3\). The stronger all-positive-period hypothesis in Lean is expressly disclosed, but the table should distinguish it consistently from the paper’s Wilson domain. |
| \(\Delta(n)=0\) | CORRECT | Recursion gives \(\Delta(m_j)=0\); (a), already at \(j=0\), gives \(h_t(n)=0\) for every \(t_i\ge n\). All excited ratios there are zero. No division by \(q\) is needed. The logarithmic assertion conditioned on \(r>0\) then has no instance. |
| Degenerate \(\lambda_0\); Remark (ii) | GAP | Simplicity is not assumed. It follows for cubes in (c) from \(r_i^n\le q<1\), and for tori in (d) from \(r_i^n\le\theta<1\). Remark (ii) should not present the stronger **cube** bound \(r_i^n\le q\) as applying indiscriminately to every section. |
| Remark (iii): section sizes needed | GAP | The parenthetical “up to the sides of the tori of the statement” understates the proof’s assumptions. The recursion and Step 4 use arbitrarily large dyadic cubes and rectangles. The theorem’s global assumptions cover them; the remark needs correction. |
| Remark (i): negative-transfer example | CORRECT | Set \(c_t=\prod_{k=1}^3(1+\rho^{t_k})^{V(t)/t_k}>0\). Then \(\operatorname{Tr}K_t^M=c_t^M(1+\rho^M)^{V(t)}=Z(t,M)\). The operator is finite-dimensional, self-adjoint, and has eigenvalues \(c_t\) and \(-rc_t\). The product defining \(Z\) is symmetric. For odd \(n\), direct substitution gives exactly \(64n^3\log(1-r^n)-32n^3\log(1+r^{2n})<0\). |
| Exact meaning of BB26 (B*) | CORRECT | BB26 uses the logarithm of the **relative** partition function: \(\log[Z(t,T_0)/\lambda_0(t)^{T_0}]\). This is precisely \(h_t(T_0)\), with the same spatial window and constant restriction. R(b) supplies a stronger spatial-domain statement. |
| Conditional bridge corollary | CORRECT | The supplied Theorem F allows \(T_0\) to depend on \((N,p)\), provided \(3\le T_0\le Nt_0\), with fixed \(y_0\). Taking \(T_0=16n_{N,p}\) and \(y_0=27/3968\) matches those quantifiers and uses the same coupling. Hypothesis (W) and the external theorem remain assumptions. The conditional marking is adequate. |
| Forward implication and scale equivalence | CORRECT | The weighted volumes give \(512\gamma T_0^3\le512/(40\cdot96^3)=1/69120<2^{-9}\). Together with R(b), this establishes the stated equivalence after changing scale. |
| Unqualified aspect-ratio summaries, lines 232 and 543 | ERROR | They omit \(\min_i t_i\ge n\). Theorem R(d) contains this restriction; the summaries currently state a broader conclusion. |
| Priority, open question and mass-gap wording | CORRECT | The text expressly disclaims priority for the existing mechanism and objects, distinguishes BB26’s open question, and leaves weak-coupling smallness and continuum existence unproved. “We did not find…” is appropriately qualified by “This is not a proof of absence.” |
| Lean description | CORRECT | The four principal statements match the frozen statements on inspection. `HypRec` is an explicit assumption in the standalone file; `reciproque_publie` derives it from the published theorem in the combined file. The stronger positive-period domain, absence of (d), logarithmic gap conversion and bridge formalisation are disclosed accurately. I did not rerun kernel checks, hashes or rebuilds. |
| AI disclosure, lines 1082–1089 | ERROR | “Both without tools” is false for this review, which used permitted file-reading tools. “Sol has not re-read this version” is stale or insufficiently version-scoped. `@@RELDONE@@` remains. The packaged `RELECTURES.md` inspected here documents v1.1, not the asserted final v1.2 reviews. |

**(B) Required corrections**

1. **Blocking — restore the size restriction in both summaries, lines 232 and 543.**

   Replace the concluding scope clause with:

   > “…and, with a worse constant, to every spatial torus \(t\) satisfying \(\min_i t_i\ge n\) and \(\max_i t_i\le24\min_i t_i\), as stated in Theorem R(d).”

2. **Blocking — correct the v1.2 review disclosure and remove the unfinished marker.**

   Replace the claims about the present Sol review with:

   > “GPT-6.1 Sol independently reviewed the v1.2 candidate against the local BB26 excerpts and Lean sources, using read-only file-reading tools. It ran no Lean build, computational script or network request. Its report records the checked candidate and required corrections; it does not certify subsequent revisions.”

   Delete `@@RELDONE@@`. Record the actual v1.2 reports before claiming that `RELECTURES.md` contains them. Describe DeepSeek’s review separately according to its recorded report.

   Replace the earlier “Sol has not re-read this version” with:

   > “Those earlier Sol reports concerned the earlier text; the v1.2 review is described separately below.”

   Likewise identify the older Fable and Sonnet preparation paragraphs explicitly as work on v1.0. Add GPT-6 Astra to the opening AI-model list, consistently with its credited discovery of R’s proof.

3. **Non-blocking — correct Remarks (ii) and (iii).**

   Replacement:

   > “(ii) Simplicity of \(\lambda_0\) is not assumed. It follows for the cubes in (c) from \(r_i^n\le q\le1/2\), and for the tori in (d) from \(r_i^n\le\theta<1\).  
   > (iii) The proof assumes symmetry and the positive transfer representation on all integer periods at least \(3\), without an upper cutoff. In particular, the recursion and the cylinder comparison use arbitrarily large dyadic cubes and rectangles. No parity restriction is imposed.”

4. **Non-blocking — align the paper and Lean domain descriptions.**

   In the (W2) table, specify spatial periods and times at least \(2\), followed by:

   > “Section 4 requires this identity only for spatial periods and times at least \(3\). The Lean hypotheses additionally require a symmetric extension satisfying the spectral identities at every positive integer period; that extension is not established here.”

   Adjust the caption’s blanket “paper argument uses periods at least \(2\)” accordingly.

5. **Non-blocking — make the Lean count and freezing chronology precise.**

   Replace “contains four theorems … before any proof” with:

   > “contains four principal theorem statements, together with auxiliary lemmas and proof theorems; the four principal statements were frozen before their Lean proofs were written.”

   There are seven declarations introduced with `theorem` in `Reciproque.lean`, including three auxiliary `_pf` declarations. This does not affect the formalisation.

6. **Non-blocking — clarify the comparison’s chronology and reading scope.**

   Replace “after the present note had been written” with:

   > “after the initial version 1.0 draft had been written”.

   Replace the restrictive “only” reading list with:

   > “The comparison uses the cited passages, principally the abstract, introduction and Sections 7.8 and 7.11, together with the individual transfer and monotonicity lemmas cited here.”

   For the pressure attribution, “follows from the spectral representation and the monotonicity statements in Lemmas 7.12 and 7.44” is more exact than suggesting that the precise normalised-pressure statement is quoted verbatim there.

memory consulted: `critere_scalaire`, `critère scalaire`, `réciproque/reciproque`, `Bhattacharjee`, `27/3968`, `pression/monoton`, `Theorem 7.56`, `Lemma 7.44`, `On the Construction of Quantized Gauge Fields`. The guard was inspected but not executed because it invokes Python; permitted grep searches substituted for it.

The earlier [PISTES.md:59](/root/physique/chantiers/pistes_2026-11-12/PISTES.md:59) already states this converse and its minimum-side restriction. The older “converse is unknown” at [dossier_ym.md:374](/root/physique/qlab/prompts/dossier_ym.md:374) is superseded by its update at [line 387](/root/physique/qlab/prompts/dossier_ym.md:387).

palette: positive spectral traces → coordinate monotonicity and cylinder limit; dyadic recursion/geometric series → \(2/31\); exponential convexity → the aspect-ratio bound; frozen-statement comparison → formalisation scope / metaphors discarded: entropy as a gap mechanism, because it adds no bound; Knabe analogy, because no applicable local-Hamiltonian estimate is supplied. The argument establishes no unconditional Coulomb-phase or five-dimensional gap, and no uniform-in-\(\beta\) lower bound: the required scale \(n\) remains uncontrolled.

**(C) Verdict: AFTER THE BLOCKING CORRECTIONS.**

Theorem R itself needs no changed constant or additional proof argument. The blockers concern the final text’s scope and review provenance.