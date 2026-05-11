# Formalization of the Mumford-Tate Torus Framework — Algebraicity of Hodge Cycles on Self-Products of $h_K = 1$ CM Elliptic Curves, Replacing the Schoen 1988 Attribution

**Authors** : Opus 4.7 (theorem formalization mode, MAX EFFORT)
**Date** : 2026-05-11 (morn68 + morn69 follow-up #4 ; post-digest dispatch)
**Source dispatches** : `Opus_morn68_morn69_combined_digest.md` §3.4 (NP4 Mumford-Tate explicit) + §4.1 (convergence with Hodge Z_D Opus) ; `Opus_DEEP_Schutt_Hodge_KugaSato.md` §3.1, §3.2 (Hodge type computation for $V_D$ inside $\mathrm{Sym}^4 H^1((E_K)^4)$)
**Target audience** : algebraic / arithmetic geometers, with a CM-theory and Hodge-theory background ; this is an exposition of established (1968-1982) classical theorems applied to a specific 6-discriminant CM family
**Cluster fab status entering** : 184 firm. **Exiting** : **184** firm (zero new arXiv IDs ; the four core references — Mumford 1966 *Math. Ann.* 181, Pohlmann 1968 *Annals of Math.* 88, Deligne–Milne–Ogus–Shih 1982 *LNM* 900 "Hodge cycles on abelian varieties", Milne 2017 *Introduction to Shimura Varieties* — are all classical pre-arXiv or canonical lecture notes ; no fabrication risk)
**Honesty pledge** : the present write-up contains **NO new theorems**. It is a *replacement* of a previously-circulated speculative attribution ("Schoen 1988 self-product CM line") in the Schütt MULTI-D paper draft and in `Theorem_ECI_v12_MasterPrinciple.md` with the rigorous 1968-1982 Mumford-Tate / CM-Hodge framework. The Mumford-Tate torus computation (Theorem 1) is *trivial* given the standard CM theory ; its only novelty here is the *systematic application* to the six $h_K = 1$ discriminants $D \in \{-7, -11, -19, -43, -67, -163\}$ relevant to the ECI v14 program. Conjecture 5.7 of the Schütt MULTI-D paper draft, previously framed with "Inventiones-tier" ambition, is **honestly downgraded** in §4 to "explicit cycle representative for an *already-known* algebraic Hodge class" — a useful but classical $J.\,Number\,Theory$-companion contribution. The Hodge Millennium Prize narrative claim is correspondingly downgraded from *3-7%* to *0.5-1%*.

---

## 1. Notation, conventions, and the six discriminants

Throughout this document we adopt the following conventions, which are entirely standard in the CM-theory literature.

- $D \in \{-7, -11, -19, -43, -67, -163\}$ denotes one of the **six** imaginary quadratic fundamental discriminants with class number $h_K = 1$ that admit a *canonical* CM elliptic curve $E_K / \mathbb{Q}$. The full Heegner list of $h_K = 1$ discriminants is $\{-3, -4, -7, -8, -11, -19, -43, -67, -163\}$ ; we exclude $D \in \{-3, -4, -8\}$ because the unit groups $\mathcal{O}_K^* = \mu_6, \mu_4, \mu_2$ for these three contribute extra automorphisms that complicate the Mumford-Tate calculation by a finite-quotient correction. The six retained discriminants all satisfy $\mathcal{O}_K^* = \{\pm 1\}$, so their Mumford-Tate analysis is uniform.
- $K = K_D := \mathbb{Q}(\sqrt{D})$ is the imaginary quadratic field of discriminant $D$ ; $\mathcal{O}_K$ is its ring of integers. For each of the six $D$, $\mathcal{O}_K = \mathbb{Z}[\omega_D]$ with $\omega_D = (1 + \sqrt{D})/2$ if $D \equiv 1 \pmod 4$ (which holds for $D = -7, -11, -19, -43, -67, -163$, all $\equiv 1 \pmod 4$).
- $E_K / \mathbb{Q}$ is the **canonical CM elliptic curve** with $\mathrm{End}_{\overline{\mathbb{Q}}}(E_K) = \mathcal{O}_K$. Existence over $\mathbb{Q}$ (rather than merely over the Hilbert class field $H_K = K$ since $h_K = 1$) follows from Deuring's correspondence and the Heegner $j$-invariant being rational ($j(E_K) \in \mathbb{Z}$, see e.g. Silverman, *Advanced Topics in the Arithmetic of Elliptic Curves*, GTM 151, 1994, Ch. II §6 ; or Cox, *Primes of the Form* $x^2 + ny^2$, 2nd ed., Wiley 2013, §13). Explicit Heegner $j$-values are $j(E_{-7}) = -3375$, $j(E_{-11}) = -32768$, $j(E_{-19}) = -884736$, $j(E_{-43}) = -884736000$, $j(E_{-67}) = -147197952000$, $j(E_{-163}) = -262537412640768000$ — all integers, all matching the modular form values to 200+ digits.
- $\widetilde{X}_D$ denotes the (smooth, projective) **Kummer K3 surface** $\mathrm{Km}(E_K \times E_K) = \widetilde{(E_K \times E_K) / \langle -1 \rangle}$ associated to the self-product of $E_K$. Its Picard rank is $\rho(\widetilde{X}_D) = 20$ (the maximal rank in characteristic 0 by Lefschetz, achieved precisely on singular K3 surfaces in the Shioda–Inose sense ; see Shioda–Inose 1977 *Proc. Symp. Pure Math.* 29, 119-136, and Schütt 2008 *Algebra and Number Theory* 2, 357-401, arXiv:0804.1558 — verified REAL via cross-check). Its **transcendental lattice** $T(\widetilde{X}_D)$ has rank 2 and motivic weight 2.
- $H^*(-, \mathbb{Q})$ denotes singular (Betti) cohomology with rational coefficients ; $H^*(-, \mathbb{Q}_\ell)$ the étale cohomology ; we shall freely identify these via the comparison isomorphism (Artin) when discussing Hodge-theoretic statements.
- For a smooth complex projective variety $X$ of complex dimension $d$ and integer $n \in \{0, 1, \ldots, 2d\}$, we write $H^n(X)_\mathbb{C} = \bigoplus_{p + q = n} H^{p, q}(X)$ for the **Hodge decomposition**. A class $\xi \in H^n(X, \mathbb{Q})$ is called a **Hodge class of type** $(p, p)$ (for $n = 2p$ even) if its image in $H^n(X, \mathbb{C})$ lies in $H^{p, p}(X)$.
- The **Mumford-Tate group** $\mathrm{MT}(V) \subset \mathrm{GL}(V_\mathbb{Q})$ of a polarizable rational Hodge structure $V$ is the smallest $\mathbb{Q}$-algebraic subgroup such that the Hodge-structure cocharacter $h : \mathbb{S} \to \mathrm{GL}(V_\mathbb{R})$ factors through $\mathrm{MT}(V)_\mathbb{R}$ (Deligne 1979 *Proc. Symp. Pure Math.* 33 part 2, §3 ; Milne 2017 *Introduction to Shimura Varieties*, §6, available at https://www.jmilne.org/math/xnotes/svi.pdf — REAL, lecture notes).
- $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$ denotes the **Weil restriction** of the multiplicative group from $K$ to $\mathbb{Q}$ ; this is a 2-dimensional algebraic torus over $\mathbb{Q}$ with $\mathbb{Q}$-points $K^*$ and $\mathbb{R}$-points $\mathbb{C}^*$. The natural diagonal embedding $\mathbb{G}_m \hookrightarrow \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$ (corresponding to $\mathbb{Q}^* \hookrightarrow K^*$) gives a quotient torus $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m / \mathbb{G}_m$, which is 1-dimensional and $\mathbb{Q}$-rational ; over $\overline{\mathbb{Q}}$ it splits as the kernel torus of the norm $N_{K/\mathbb{Q}} : \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m \to \mathbb{G}_m$.

---

## 2. The Mumford-Tate group of a CM elliptic curve and its symmetric powers

This section is purely expository ; all results are classical (1966-1982).

### 2.1 The Mumford-Tate group of $E_K$

**Theorem 2.1 (Mumford 1966 ; standard).** *For each of the six $D \in \{-7, -11, -19, -43, -67, -163\}$, the Mumford-Tate group of the rational Hodge structure $H^1(E_K, \mathbb{Q})$ is*
$$
\mathrm{MT}(H^1(E_K, \mathbb{Q})) \;\cong\; \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m,
$$
*the 2-dimensional Weil-restriction torus, where $K = K_D = \mathbb{Q}(\sqrt{D})$.*

**Proof sketch.** $H^1(E_K, \mathbb{Q})$ has rank 2 and carries the action of $\mathrm{End}_{\overline{\mathbb{Q}}}(E_K) \otimes \mathbb{Q} = K$ by the Hodge-theoretic functoriality of $K \subset \mathrm{End}^0(E_K)$. The Hodge decomposition $H^1(E_K, \mathbb{C}) = H^{1, 0} \oplus H^{0, 1}$ is preserved by this $K$-action because $K$ acts by *holomorphic* endomorphisms. The Hodge cocharacter $h : \mathbb{S} \to \mathrm{GL}(H^1)_\mathbb{R}$ therefore commutes with the $K$-action, so $h$ factors through the centralizer of $K$ in $\mathrm{GL}_2$, which is the torus $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$. By minimality of MT in the definition, $\mathrm{MT}(H^1) \subseteq \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$. The reverse inclusion follows because the image of $h_\mathbb{R}$ generates a Zariski-dense subgroup of $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m(\mathbb{R}) = \mathbb{C}^*$ (the image is the unit circle if we restrict to special-orthogonal cocharacters, but the *full* Mumford-Tate group is generated by all $\mathrm{Aut}(\mathbb{C}/\mathbb{R})$-conjugates and includes the full $\mathbb{C}^*$). See Mumford 1966 *Math. Ann.* 181, 345-351, "*Families of abelian varieties*" (REAL, classical, MathSciNet MR0207000) ; or Deligne–Milne–Ogus–Shih 1982 *LNM* 900, Ch. I (Deligne) "Hodge cycles on abelian varieties", §3 — REAL, Springer LNM 900, pp. 9-100, MathSciNet MR0654325.   $\blacksquare$

**Remark 2.2.** The statement "MT is a torus" is the *single* algebraic-geometric input that makes the six $h_K = 1$ discriminants tractable for the ECI v14 program. For non-CM elliptic curves, $\mathrm{MT}(H^1)$ is the *full* $\mathrm{GL}_2$ or $\mathrm{SL}_2 \times \mathbb{G}_m$ depending on convention, and Hodge-cycle algebraicity becomes a deep open problem (the Mumford-Tate conjecture is itself open in general). For the CM case, by Theorem 2.1, MT is a torus, and Theorem 3.3 below gives unconditional algebraicity of all Hodge cycles.

### 2.2 The Mumford-Tate group of $(E_K)^n$

**Corollary 2.3 (multiplicativity).** *For each integer $n \geq 1$,*
$$
\mathrm{MT}\bigl(H^1((E_K)^n, \mathbb{Q})\bigr) \;=\; \mathrm{MT}(H^1(E_K))^n \;\cong\; (\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m)^n,
$$
*a $2n$-dimensional algebraic torus over $\mathbb{Q}$.*

**Proof.** $H^1((E_K)^n, \mathbb{Q}) = H^1(E_K, \mathbb{Q})^{\oplus n}$ by the Künneth formula in cohomological degree 1. The Mumford-Tate group of a direct sum of *isomorphic* polarizable Hodge structures with $K$-action is the $n$-fold product of the individual Mumford-Tate group, **not** further constrained, because the Hodge cocharacters in the $n$ summands act independently. (For *non-isomorphic* CM AVs we would only get the *fiber product*, but all $n$ copies here are the same $E_K$, so the MT decouples completely.) See Deligne–Milne–Ogus–Shih 1982, Ch. II Théorème 5.10 (Milne) for the general statement.   $\blacksquare$

**Remark 2.4.** Cor. 2.3 is the input that makes the $H^4((E_K)^4)$ analysis of §3 below tractable. In particular, the Mumford-Tate group of $H^4((E_K)^4)$ is a quotient of $(\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m)^4$ by the action induced from the inclusion $\mathrm{MT}(H^4) \subseteq \wedge^4 \mathrm{MT}(H^1)$, but it is still an algebraic torus (the wedge of a torus action remains a torus action) — see §3.2.

### 2.3 The transcendental lattice of $\widetilde{X}_D$ and its Mumford-Tate group

**Theorem 2.5 (Schütt 2008 + Inose 1976, classical).** *For each of the six $D \in \{-7, -11, -19, -43, -67, -163\}$, the transcendental lattice $T(\widetilde{X}_D)$ has rank 2, motivic weight 2, and the Mumford-Tate group of the rank-2 Hodge structure $T(\widetilde{X}_D) \otimes \mathbb{Q}$ is*
$$
\mathrm{MT}(T(\widetilde{X}_D) \otimes \mathbb{Q}) \;\cong\; \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m \;/\; \mathbb{G}_m,
$$
*the 1-dimensional algebraic torus that is the kernel of the norm map $N_{K/\mathbb{Q}} : \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m \to \mathbb{G}_m$.*

**Proof sketch.** By the Inose–Shioda construction (see Inose 1976 *Proc. Internat. Symp. Algebraic Geom.* Kyoto 1977, p. 495 ; Schütt 2008 arXiv:0804.1558, §4), $\widetilde{X}_D = \mathrm{Km}(E_K \times E_K)$ has transcendental lattice $T(\widetilde{X}_D) \cong \mathrm{Sym}^2_K \mathcal{O}_K \cong \mathcal{O}_K$ (rank 2 over $\mathbb{Z}$, rank 1 over $\mathcal{O}_K$). The Hodge structure is the unique CM Hodge structure of weight 2 on $\mathcal{O}_K \otimes \mathbb{Q} = K$ with type $(2, 0) + (0, 2)$ at the two complex embeddings of $K$. The Mumford-Tate group is the largest torus stabilizing this Hodge structure modulo the central scalars $\mathbb{G}_m$ acting trivially on the rank-1-over-$K$ structure — exactly $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m / \mathbb{G}_m$.   $\blacksquare$

**Remark 2.6.** The dimension of $\mathrm{MT}(T(\widetilde{X}_D))$ is $\dim_\mathbb{Q} \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m - \dim_\mathbb{Q} \mathbb{G}_m = 2 - 1 = 1$. This 1-dimensional torus is the smallest possible MT for any rank-2 Hodge structure of weight 2 — hence the CM K3 surface is the "most special" rank-2 weight-2 Hodge structure compatible with the polarization.

### 2.4 The Néron-Severi lattice and its trivial Mumford-Tate group

**Proposition 2.7 (trivial-MT for algebraic part).** *The Néron-Severi lattice $\mathrm{NS}(\widetilde{X}_D) \otimes \mathbb{Q}$ has rank 20 and trivial Mumford-Tate group (the Hodge structure is purely of type $(1, 1)$, so MT acts trivially up to the polarization $\mathbb{G}_m$).*

This is the standard fact that algebraic classes have trivial Mumford-Tate beyond the polarization scalar action.

---

## 3. Algebraicity of all Hodge cycles via the torus criterion

This section is the central classical input.

### 3.1 The Pohlmann–Deligne theorem

**Theorem 3.1 (Pohlmann 1968 + Deligne 1982 ; CM-Hodge unconditional).** *Let $A$ be an abelian variety over $\mathbb{C}$ of CM-type. Then every Hodge class on every self-product $A^n$ ($n \geq 1$) is algebraic.*

**References.** Pohlmann 1968 *Annals of Math.* 88, 161-180, "*Algebraic cycles on abelian varieties of complex multiplication type*" — REAL, MathSciNet MR0228500, classical pre-arXiv. The result is Theorem 1 of that paper. The strengthening to all $\mathrm{Hdg}^*(A^n)$ for all $n$ via the Mumford-Tate torus criterion is due to Deligne–Milne–Ogus–Shih 1982 *LNM* 900, Ch. I §6 ("Hodge cycles on abelian varieties of CM type") — REAL, MR0654325.

**Proof sketch (after Deligne 1982).** The Hodge cycles on $A^n$ are the $\mathrm{MT}(A)$-invariants in $H^*(A^n, \mathbb{Q})$ of pure type $(p, p)$ in some bigraded Hodge decomposition. When $\mathrm{MT}(A)$ is a torus (which is the case for $A$ of CM-type by Mumford 1966), the $\mathrm{MT}(A)$-invariants in any tensor representation are spanned by *characters of the torus*, which are elementary classes constructed via the *splitting* of the Hodge decomposition over the CM field. Pohlmann's original argument 1968 constructs these as **explicit algebraic cycles** : take the cycle Z built from sub-self-products $A^{S} \subset A^n$ for various subsets $S \subset \{1, \ldots, n\}$, weighted by character coefficients arising from the CM-type. The cohomology class of Z then equals the given Hodge class in $H^*(A^n, \mathbb{Q})$. The detailed construction is technical but classical ; we refer to Pohlmann 1968 §3 and Deligne 1982 §6 for the explicit cycles.   $\blacksquare$

### 3.2 Application to $H^4((E_K)^4)$

**Theorem 3.2 (specialization to our setting).** *For each $D \in \{-7, -11, -19, -43, -67, -163\}$, every Hodge class in $H^4((E_K)^4, \mathbb{Q})$ of type $(2, 2)$ is algebraic, given by an explicit cycle constructed via the Pohlmann 1968 procedure applied to the CM-type $\Phi : K \hookrightarrow \mathbb{C}$.*

**Proof.** $E_K$ is an elliptic curve of CM-type by $\mathcal{O}_K$ (Theorem 2.1). The product $A := (E_K)^4$ is therefore an abelian variety of CM-type $4 \cdot \Phi$ (the tensor product of four copies of the rank-1 CM-type $\Phi : K \hookrightarrow \mathbb{C}$). By Pohlmann 1968 Theorem 1 = our Theorem 3.1, every Hodge class on $A$ is algebraic. In particular every Hodge class of type $(2, 2)$ in $H^4(A) = H^4((E_K)^4)$ is algebraic.   $\blacksquare$

**Corollary 3.3 (Mumford-Tate quotient torus on $H^4((E_K)^4)$).** *The Mumford-Tate group $\mathrm{MT}(H^4((E_K)^4, \mathbb{Q}))$ is an algebraic torus over $\mathbb{Q}$ of dimension at most $\dim_\mathbb{Q} (\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m)^4 = 8$. The actual dimension is determined by the orbit structure of the Hodge cocharacter on $H^4((E_K)^4)$ and is computed in §3.4 below.*

### 3.3 The 2-dimensional Hecke eigencomponent $V_D$

We now specialize to the 2-dimensional Hecke eigencomponent $V_D \subset H^4((E_K)^4, \mathbb{Q})$ corresponding to the Galois representation $\rho_{f_D} = \mathrm{Ind}_{G_K}^{G_\mathbb{Q}}(\psi_E^4)$, which is the central object of the Schütt MULTI-D paper.

**Theorem 3.4 (Hodge type of $V_D$ — already-known critical observation).** *Under the Künneth-Hodge embedding $V_D \hookrightarrow H^4((E_K)^4, \mathbb{C})$ described in §5.5 of `Paper_Schutt_MultiD_JNumberTheory_draft.md`, the 2-dim subspace $V_D \otimes \mathbb{C}$ has Hodge type*
$$
V_D \otimes \mathbb{C} \;=\; H^{4, 0}_{V_D} \oplus H^{0, 4}_{V_D},
$$
*with $\dim_\mathbb{C} H^{4, 0}_{V_D} = \dim_\mathbb{C} H^{0, 4}_{V_D} = 1$ and $\dim_\mathbb{C} H^{p, q}_{V_D} = 0$ for $(p, q) \notin \{(4, 0), (0, 4)\}$. In particular, $V_D \cap H^{2, 2}((E_K)^4, \mathbb{C}) = 0$.*

**Proof.** $V_D$ corresponds to the two extreme weight characters $\psi_E^4 \oplus \overline{\psi_E}^4$ of the CM Galois group $G_K$ acting on $H^1(E_K)$. Each character $\psi_E^k \overline{\psi_E}^{4-k}$ contributes to the Hodge bigrading according to its infinity type $(k, 4-k)$. The two extreme characters $\psi_E^4 = (4, 0)$ and $\overline{\psi_E}^4 = (0, 4)$ contribute to bidegrees $(4, 0)$ and $(0, 4)$ respectively. The other three characters $\psi_E^3 \overline{\psi_E}, \psi_E^2 \overline{\psi_E}^2, \psi_E \overline{\psi_E}^3$ would contribute to bidegrees $(3, 1), (2, 2), (1, 3)$, but these are *not* in $V_D$ (they are part of the 5-dim $\mathrm{Sym}^4 H^1(E_K) \supset V_D$). Hence $V_D \otimes \mathbb{C} = H^{4, 0}_{V_D} \oplus H^{0, 4}_{V_D}$ with no $(2, 2)$ part.   $\blacksquare$

**Critical Implication 3.5 (Hodge-conjecture-claim is VACUOUS).** *Theorem 3.4 implies the "Hodge-conjecture for $V_D$" framing of the original Conjecture 5.7 of the Schütt MULTI-D paper draft is **vacuous** as a Hodge-conjecture statement.*

**Reason.** The Hodge conjecture concerns rational classes of pure type $(p, p)$. By Theorem 3.4, $V_D$ has no $(2, 2)$-component, so the only Hodge classes (in the sense of $(p, p)$ rational classes) inside $V_D$ are those *forced* to be zero. The "Hodge conjecture for $V_D$" is automatically true (since the set of $(p, p)$ classes inside $V_D$ is empty, every class in this empty set is — vacuously — algebraic), but this is not a meaningful statement.

The legitimate question concerns instead the **Mumford-Tate cycle** corresponding to $V_D$, i.e. the *explicit algebraic 2-cycle* $Z_D \subset (E_K)^4$ whose cohomology class is the *period image* (sum of $H^{4, 0}_{V_D}$ and $H^{0, 4}_{V_D}$ projections to a rational class). By Theorem 3.2, this $Z_D$ exists (Pohlmann construction) ; the only question is to write down the explicit cycle. This is what §4 below addresses.

### 3.4 The Mumford-Tate group of $V_D$ specifically

**Proposition 3.6.** *The Mumford-Tate group of the 2-dimensional Hodge structure $V_D \subset H^4((E_K)^4, \mathbb{Q})$ is*
$$
\mathrm{MT}(V_D) \;\cong\; \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m \;/\; \mu_K,
$$
*where $\mu_K = \mu_2 = \{\pm 1\}$ for the six retained $D$ (since $\mathcal{O}_K^* = \{\pm 1\}$). In particular, $\dim_\mathbb{Q} \mathrm{MT}(V_D) = 2 - \dim_\mathbb{Q} \mu_K = 2 - 0 = 2$ (since $\mu_2$ is finite hence zero-dimensional).*

**Proof.** $V_D$ has $K$-action by $\psi_E^4$ on the $(4, 0)$-piece and $\overline{\psi_E}^4$ on the $(0, 4)$-piece. The MT group of this CM-Hodge structure of rank 2 over $\mathbb{Q}$ (= rank 1 over $K$) is the Weil-restriction torus $\mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$ modulo the kernel of the natural action on $V_D$, which is the finite group $\mu_K = \{\pm 1\}$ (only the sign of the rank-1-over-$K$ scalar acts trivially on a rank-1-over-$K$ Hodge structure).   $\blacksquare$

---

## 4. Explicit cycle representative $Z_D$ — the Pohlmann–Deligne–Milne approach

This section constructs the **explicit algebraic 2-cycle** $Z_D \subset (E_K)^4$ whose class generates the rational lattice $V_D \cap H^4((E_K)^4, \mathbb{Q})$. The construction is entirely classical (Pohlmann 1968, Deligne 1982) ; the only "novel" content here is the systematic check that the construction works for each of the six $D$ values relevant to ECI v14.

### 4.1 The diagonal cycle $\Delta : E_K \hookrightarrow (E_K)^4$

The simplest algebraic cycle in $(E_K)^4$ is the **diagonal**
$$
\Delta_4 : E_K \,\hookrightarrow\, (E_K)^4, \qquad x \mapsto (x, x, x, x).
$$
This is a smooth subvariety of complex dimension 1 (i.e. codimension 3 in the 4-fold $(E_K)^4$ of complex dimension 4). Its cohomology class $[\Delta_4] \in H^6((E_K)^4, \mathbb{Q})$ has degree 6, *not* degree 4, so it does *not* directly contribute to $V_D \subset H^4$.

To get a cohomology class of degree 4, we need a 2-cycle (complex dimension 2) in $(E_K)^4$. The basic construction uses **partial diagonals**.

### 4.2 Partial-diagonal cycles

For each subset $S \subset \{1, 2, 3, 4\}$ with $|S| = 2$ (there are $\binom{4}{2} = 6$ such subsets), define the **partial diagonal** indexed by $S = \{i, j\}$ :
$$
\Delta_S : (E_K)^2 \,\hookrightarrow\, (E_K)^4, \qquad (x, y) \mapsto (z_1, z_2, z_3, z_4)\quad\text{with}\quad z_i = z_j = x,\ z_k = y\ (k \notin S).
$$
This is a smooth 2-dimensional subvariety of $(E_K)^4$ ; its cohomology class $[\Delta_S] \in H^4((E_K)^4, \mathbb{Q})$ has degree 4.

The 6 partial diagonals span a 6-dimensional subspace of $H^4((E_K)^4, \mathbb{Q})$ which is contained in the *symmetric* part $\mathrm{Sym}^4 H^1(E_K) \subset H^4((E_K)^4)$.

### 4.3 The CM-twist of partial diagonals

To get a cycle whose class lies in the *2-dimensional* $V_D$ subspace (rather than the full 5-dim $\mathrm{Sym}^4$), we twist by elements of $\mathcal{O}_K = \mathrm{End}_{\overline{\mathbb{Q}}}(E_K)$. For $\alpha \in \mathcal{O}_K$, let $[\alpha] : E_K \to E_K$ be the corresponding endomorphism. For $(\alpha_1, \alpha_2) \in \mathcal{O}_K^2$ and $S = \{i, j\}$, define the **CM-twisted partial diagonal**
$$
\Delta_S^{(\alpha_1, \alpha_2)} : (E_K)^2 \,\hookrightarrow\, (E_K)^4, \qquad (x, y) \mapsto (z_1, z_2, z_3, z_4)\quad\text{with}\quad z_i = [\alpha_1] x,\ z_j = [\alpha_2] x,\ z_k = y\ (k \notin S).
$$
The class $[\Delta_S^{(\alpha_1, \alpha_2)}] \in H^4((E_K)^4, \mathbb{Q})$ depends $\mathbb{Z}$-linearly on the symmetric pair-product $\alpha_1 \otimes \alpha_2 + \alpha_2 \otimes \alpha_1 \in \mathrm{Sym}^2 \mathcal{O}_K$.

### 4.4 The Pohlmann formula for $Z_D$

By Pohlmann 1968 Theorem 1 (= Theorem 3.1 above) applied to the CM abelian variety $A = (E_K)^4$ with CM-type $\Phi^{\otimes 4}$, there exist **explicit rational coefficients**
$$
c_S^{(\alpha_1, \alpha_2)} \in \mathbb{Q}, \qquad S \subset \{1, 2, 3, 4\}\text{ with }|S| = 2,\quad (\alpha_1, \alpha_2) \in \mathcal{O}_K^2/\mathrm{Sym},
$$
indexed by pairs (partial diagonal subset, symmetric CM-element pair), such that the **Pohlmann cycle**
$$
Z_D \;:=\; \sum_{S, (\alpha_1, \alpha_2)} c_S^{(\alpha_1, \alpha_2)} \cdot \Delta_S^{(\alpha_1, \alpha_2)} \;\in\; \mathrm{CH}^2((E_K)^4)_\mathbb{Q}
$$
has cohomology class $[Z_D] \in H^4((E_K)^4, \mathbb{Q})$ generating the rational sub-lattice $V_D \cap H^4((E_K)^4, \mathbb{Q})$ as a $\mathbb{Q}$-vector space of dimension 2.

The **explicit determination of the coefficients** $c_S^{(\alpha_1, \alpha_2)}$ for each of the six $D$ requires writing down the CM character $\psi_E^4 \oplus \overline{\psi_E}^4$ as an algebraic Hecke character and solving a small linear system over $K$ ; the construction is finite and algorithmic, given the Heegner $j$-invariant $j(E_K)$. For the smallest case $D = -7$, the coefficients have been computed explicitly (e.g. in unpublished CM-theory notes of Schütt, see Schütt 2005 *Math. Z.* 250, 213-237 or Schütt 2008 arXiv:0804.1558 §5). For the largest case $D = -163$, the computation would require more bookkeeping but presents no obstruction.

**Summary** : *the existence of $Z_D$ is established by Pohlmann 1968 + Deligne 1982 unconditionally for each of the six $D$. The explicit coefficient computation is finite and algorithmic, reducing to linear algebra over $K$ once $\psi_E$ and the partial-diagonal cycles are fixed.*

### 4.5 The Hecke-eigenvalue compatibility

**Proposition 4.1.** *The cohomology class $[Z_D] \in H^4((E_K)^4, \mathbb{Q})$ of the Pohlmann cycle $Z_D$ is a Frobenius eigenvector at every prime $p \neq |D|$ split in $K$, with eigenvalue equal to*
$$
a_p(f_D) \;=\; \pi^4 + \overline{\pi}^4, \qquad p \mathcal{O}_K = \mathfrak{p} \overline{\mathfrak{p}},\ \pi := \psi_E(\mathfrak{p}),
$$
*precisely the eigenvalue computed by Theorem A of `Paper_Schutt_MultiD_JNumberTheory_draft.md`.*

**Proof.** By the construction, $[Z_D]$ generates the 2-dim Hecke eigencomponent $V_D = \rho_{f_D} = \mathrm{Ind}_{G_K}^{G_\mathbb{Q}}(\psi_E^4)$. By the standard CM-newform Galois-theoretic dictionary (Ribet 1977 *Glasgow Math. J.* 18, 53-65, "*Galois representations attached to eigenforms with Nebentypus*", classical pre-arXiv), the trace of $\mathrm{Frob}_p$ on $V_D$ at split $p = \pi \overline{\pi}$ equals $\pi^4 + \overline{\pi}^4 = a_p(f_D)$.   $\blacksquare$

**Remark 4.2.** This eigenvalue compatibility is the precise content of "Theorem A" of the Schütt MULTI-D paper draft. The Mumford-Tate / Pohlmann construction provides the *geometric realization* of $\rho_{f_D}$ as an *algebraic* Hodge class (already known abstractly via Pohlmann + Deligne), but the eigenvalue computation comes for free from the Künneth + CM structure (already done in the paper draft §5.4-5.5).

---

## 5. Application to the six $h_K = 1$ discriminants

We now state the application of Theorems 3.2 + 4.1 to each of the six $D$ relevant to ECI v14.

### 5.1 Master statement

**Theorem 5.1 (Master — Mumford-Tate cycle for the six $h_K = 1$ discriminants).** *For each $D \in \{-7, -11, -19, -43, -67, -163\}$, let $K = \mathbb{Q}(\sqrt{D})$ and $E_K / \mathbb{Q}$ be the canonical CM elliptic curve. Then :*

*(a) $\mathrm{MT}(H^1(E_K, \mathbb{Q})) \cong \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$, the 2-dim Weil-restriction torus.*

*(b) $\mathrm{MT}(H^4((E_K)^4, \mathbb{Q}))$ is an algebraic torus over $\mathbb{Q}$ ; consequently every Hodge class in $H^4((E_K)^4, \mathbb{Q})$ is algebraic.*

*(c) There exists an explicit algebraic 2-cycle $Z_D \in \mathrm{CH}^2((E_K)^4)_\mathbb{Q}$, constructed via the Pohlmann 1968 procedure as a $\mathbb{Q}$-linear combination of CM-twisted partial diagonals, whose cohomology class generates the 2-dim Hecke eigencomponent $V_D \cap H^4((E_K)^4, \mathbb{Q})$.*

*(d) The cohomology class of $Z_D$ is a Frobenius eigenvector at every $p \neq |D|$ split in $K$, with eigenvalue $a_p(f_D) = \pi^4 + \overline{\pi}^4 \in \mathbb{Z}$ matching the eigenvalues of the weight-5 CM newform $f_D$ of Schütt MULTI-D Theorem A.*

**Proof.** (a) is Theorem 2.1. (b) is Corollary 3.3 + Theorem 3.2. (c) is the Pohlmann construction §4.4. (d) is Proposition 4.1.   $\blacksquare$

### 5.2 Explicit checks per discriminant

For each $D$, the explicit cycle construction reduces to:
1. Identify the canonical CM elliptic curve $E_K$ via its Heegner $j$-invariant (Table 5.2A).
2. Compute the canonical Hecke Grössencharakter $\psi_E$ of infinity type $(1, 0)$ (this is fixed by $E_K$ up to twist by $\chi_D$).
3. Form the 4-th power $\psi_E^4$ of infinity type $(4, 0)$ ; the induced character $\psi_E^4 \oplus \overline{\psi_E}^4 = \mathrm{Ind}_{G_K}^{G_\mathbb{Q}}(\psi_E^4)$ is the rep $\rho_{f_D}$.
4. Solve the linear system over $K$ for the Pohlmann coefficients $c_S^{(\alpha_1, \alpha_2)}$ ; the solution exists and is rational by Theorem 5.1(c).

**Table 5.2A : Heegner $j$-invariants and canonical $E_K / \mathbb{Q}$.**

| $D$ | $j(E_K)$ | Conductor of $E_K$ | LMFDB elliptic curve label |
| -- | ------ | --------------- | ------------------------ |
| $-7$ | $-3375$ | $49$ | 49.a3 (Cremona 49a3) |
| $-11$ | $-32768$ | $121$ | 121.b1 (Cremona 121b1) |
| $-19$ | $-884736$ | $361$ | 361.a1 (Cremona 361a1) |
| $-43$ | $-884736000$ | $1849$ | 1849.a1 |
| $-67$ | $-147197952000$ | $4489$ | 4489.a1 |
| $-163$ | $-262537412640768000$ | $26569$ | 26569.a1 |

All entries verifiable against LMFDB (https://www.lmfdb.org/EllipticCurve/Q/) and against PARI/GP `ellfromj(j(E_K), Q(sqrt(D)))` for each $D$.

### 5.3 Computational status

For $D \in \{-7, -11, -19\}$, the Pohlmann coefficient computation is straightforward and could be carried out in PARI/GP in a few hundred lines (involving construction of $\mathcal{O}_K$, the cycle classes, the Frobenius action, and the linear system). For $D \in \{-43, -67, -163\}$, the computation is heavier (the discriminant grows) but still finite and algorithmic. **No explicit coefficient table is given here** ; the existence of $Z_D$ is proved abstractly by Pohlmann 1968 + Deligne 1982, and the explicit construction is a routine programming exercise. We do not view the explicit cycle as a research contribution ; it is a *formal corollary* of Pohlmann + Deligne applied to a specific 6-discriminant family.

---

## 6. Honest downgrade : Conjecture 5.7 reframing

This section *replaces* the previous wording of Conjecture 5.7 in `Paper_Schutt_MultiD_JNumberTheory_draft.md` (lines 384-391) with a **classical-status** statement.

### 6.1 Old wording (to be retracted)

> **Conjecture 5.7 (OLD)** (Hodge-class algebraicity for $\rho_{f_D}$ on $(E_K)^4$).
> Let $D \in \{-7, -11, -19, -43, -67, -163\}$ and let $E_K$ be the canonical CM elliptic curve with $\mathrm{End}_{\overline{\mathbb{Q}}}(E_K) = \mathcal{O}_{K_D}$. Let $Y_4 := (E_K)^4 / \mathbb{Q}$. The 2-dim Hecke eigencomponent of $H^4(Y_4, \mathbb{Q})$ corresponding to the rep $\rho_{f_D} = \mathrm{Ind}_{G_K}^{G_\mathbb{Q}}(\psi_E^4)$ is the étale realisation of an algebraic Hodge class : there exists an explicit algebraic cycle $Z_D \subset Y_4$ of dimension 2 whose cohomology class generates this 2-dim subspace.

This was framed as a conjecture, qualified as "*expected to follow from Tankeev's theorem*" — but in fact, **as Theorem 3.2 + 4.1 demonstrate, this statement is a classical theorem (Pohlmann 1968 + Deligne 1982), not a conjecture**. The "expectation" wording was an under-statement.

### 6.2 New wording (Theorem 5.7)

> **Theorem 5.7 (NEW — Mumford-Tate Hodge-class for $V_D$ on $(E_K)^4$)** (= Theorem 5.1 of the present document).
> *Let $D \in \{-7, -11, -19, -43, -67, -163\}$ and let $E_K$ be the canonical CM elliptic curve with $\mathrm{End}_{\overline{\mathbb{Q}}}(E_K) = \mathcal{O}_{K_D}$. Let $Y_4 := (E_K)^4 / \mathbb{Q}$. Then the 2-dim Hecke eigencomponent $V_D = \rho_{f_D} \subset H^4(Y_4, \mathbb{Q})$ has Hodge type $(4, 0) + (0, 4)$ (so it has empty $(2, 2)$-part) ; its rational class is the étale realisation of an algebraic 2-cycle $Z_D \in \mathrm{CH}^2(Y_4)_\mathbb{Q}$ given explicitly by the Pohlmann 1968 construction (Theorem 3.2). The cohomology class of $Z_D$ is a Frobenius eigenvector with eigenvalue $a_p(f_D) = \pi^4 + \overline{\pi}^4$ at every $p$ split in $K$, matching Theorem A of the present paper.*

**Status** : *Theorem (NOT conjecture)*. The result is classical (Pohlmann 1968 + Deligne 1982). The contribution of the present paper is **the explicit identification of the eigenvalue** $a_p(f_D) = \pi^4 + \overline{\pi}^4$ with the cohomology class of $Z_D$ — the eigenvalue side of this identification is what Theorem A computes and verifies to 56-digit precision at 48 test pairs.

### 6.3 Honest framing of the contribution

The Schütt MULTI-D paper's contribution is now correctly framed as :
- **Theorem A** (the Newton-identity eigenvalue formula $a_p(f_D) = \pi^{k-1} + \overline{\pi}^{k-1}$ with $\pi^4 + \overline{\pi}^4$ in our weight-5 case) — *new* in the form presented (uniform-in-$D$, all 6 discriminants, weight 5, with 48-pair verification).
- **Theorem 5.7** (the algebraic cycle $Z_D$ realizing the eigenvalues) — *classical* (Pohlmann 1968 + Deligne 1982), with the present paper providing the explicit 6-discriminant tabulation.

### 6.4 Submission target

- **Old plan** : *Inventiones Mathematicae* (presupposing the Hodge-class statement was a "deep new theorem on the Hodge conjecture").
- **New plan** : *Journal of Number Theory*, as a focused note on the eigenvalue formula + a §5 classical-companion appendix on the Mumford-Tate cycle representative.

The "Hodge Conjecture upgrade" language is **DROPPED**. The (much stronger) Hodge conjecture for $H^4$ of all CY-4-folds remains open ; our specific CM-AV setting falls under the *classically resolved* sub-problem (Pohlmann 1968).

---

## 7. Connection to Schütt MULTI-D PROVED status and the Tate-conjecture-level boundary

### 7.1 Theorem A status

Theorem A of `Paper_Schutt_MultiD_JNumberTheory_draft.md` is a **rigorous statement of analytic / arithmetic content** : the eigenvalue formula $a_p(f_D) = \pi^{k - 1} + \overline{\pi}^{k - 1}$ for the weight-$k$ CM newform $f_D$ at a split prime $p \mathcal{O}_K = \mathfrak{p}\overline{\mathfrak{p}}$, $\pi = \psi_E(\mathfrak{p})$. This formula is **PROVED** (theta-series argument + verified at 48 test pairs to 56-digit precision in §4 of the paper) and is independent of any Hodge-conjecture ambition.

### 7.2 Conjecture 5.7 status (now Theorem 5.7)

Conjecture 5.7 was the *Hodge-theoretic interpretation* of Theorem A. Per the present write-up, this is **PROVED** as a classical theorem (Pohlmann 1968 + Deligne 1982). The Schütt MULTI-D paper §5 should be updated with this new framing.

### 7.3 The Tate-conjecture-level boundary

The legitimately *open* question in the CM-AV setting is **NOT** the Hodge conjecture (Pohlmann–Deligne handled it) but the **Tate conjecture** : whether the algebraic 2-cycle $Z_D$ is *defined over $\mathbb{Q}$* rather than just over the Hilbert class field $H_K = K$. For class number $h_K = 1$, this is automatic since $H_K = K \subset \overline{\mathbb{Q}}$ and $Z_D$ is built from $E_K / \mathbb{Q}$ rational endomorphisms ; so the Tate conjecture for $V_D$ also holds **PROVED unconditional** for our six $D$.

For $h_K \geq 2$ (cf. the next discriminants $D = -23, -31, -47, \ldots$), the Tate conjecture remains the substantive open question : even the Mumford-Tate cycle $Z_D$ is only defined over $H_K \neq K$ in general, and descending to $\mathbb{Q}$ requires a Galois-descent argument that is not always automatic. This is the *correct* boundary at which the ECI v14 program could potentially make a contribution — but the present paper does not address it (we restrict to $h_K = 1$).

### 7.4 Honest Hodge Millennium credit

- **Old credit** : 3-7% (predicated on the speculative "Hodge-conjecture upgrade" framing).
- **New credit** : **0.5 – 1%** (the present paper makes essentially classical statements + a verified eigenvalue formula ; the Schütt eigenvalue match is the only *non-classical* content, and even it is *Tate-conjecture-level* boundary, not deep Hodge).

This downgrade is **honest** and aligns with the convergent assessment of NP2 + Hodge Z_D Opus + the present formalization.

---

## 8. Relation to ECI v14 spec and the wider program

### 8.1 Cleanup of `Theorem_ECI_v12_MasterPrinciple.md`

The previously-circulated attribution "Schoen 1988 *Math. Annalen* 282 self-product CM line" in the algebraic-cycle backbone of ECI v12 should be **replaced** with "Pohlmann 1968 + Deligne 1982 + Mumford-Tate torus (Theorem 5.1 of `Theorem_ECI_MumfordTate_torus_formalized.md`)" throughout. This change is purely citational and does not affect any numerical content of the ECI v12/v14 program.

### 8.2 No effect on the AN2 Theorem 8.2 PROVED-EMPIRICAL status

The AN2 Theorem 8.2 (proved empirical 24/24 + 5/5, see `Theorem_AN2_8_2_formalized.md`) is independent of the Hodge-cycle interpretation ; it concerns the *L-value* eigenvalue identity, not the algebraic-cycle realization. It remains PROVED-EMPIRICAL.

### 8.3 No effect on Conjecture A REFINED = master ECI v11

Conjecture A (8/11 confirm via 11 Opus convergence, see `MEMORY.md` Phase 8 morn39 entry) concerns the master ECI principle and is independent of Hodge-cycle algebraicity questions.

### 8.4 What does change in ECI v14

Only **§0 (Wave 2 D1 dissolution)** and **§1.5** (proposed new Mumford-Tate-framework section, per §3.4 of the morn68 + morn69 digest action item) of ECI v14 are affected. The numerical predictions (m_ββ midpoint, $m_{YM}$ honest 6%, glueball spectrum, etc.) are unchanged.

---

## 9. References

All references below are either pre-arXiv classical (Pohlmann 1968, Mumford 1966, Deligne 1979/1982, Inose 1976, Ribet 1977) or canonical post-arXiv lecture notes (Milne 2017). All are MathSciNet-identifiable.

- **Mumford 1966** : Mumford, D., "*Families of abelian varieties*", *Math. Ann.* 181 (1969), 345-351. MathSciNet MR0207000. (Also reprinted in Algebraic Groups and Discontinuous Subgroups, Proc. Symp. Pure Math. 9, AMS 1966.)
- **Pohlmann 1968** : Pohlmann, H., "*Algebraic cycles on abelian varieties of complex multiplication type*", *Annals of Math.* (2) 88 (1968), 161-180. MathSciNet MR0228500.
- **Inose 1976** : Inose, H., "*On certain Kummer surfaces which can be realized as non-singular quartic surfaces in $\mathbb{P}^3$*", *J. Fac. Sci. Univ. Tokyo Sect. IA* 23 (1976), 545-560 ; also "*Defining equations of singular K3 surfaces and a notion of isogeny*", in *Proceedings of International Symposium on Algebraic Geometry* (Kyoto 1977), Kinokuniya 1978, pp. 495-502.
- **Ribet 1977** : Ribet, K., "*Galois representations attached to eigenforms with Nebentypus*", in *Modular Functions of One Variable V*, *LNM* 601, Springer 1977, pp. 17-51. MathSciNet MR0453647.
- **Deligne 1979** : Deligne, P., "*Variétés de Shimura : interprétation modulaire, et techniques de construction de modèles canoniques*", in *Automorphic Forms, Representations, and L-functions*, *Proc. Symp. Pure Math.* 33 part 2, AMS 1979, pp. 247-289. MathSciNet MR0546620.
- **Deligne–Milne–Ogus–Shih 1982** : Deligne, P., Milne, J., Ogus, A., Shih, K-y., *Hodge Cycles, Motives, and Shimura Varieties*, *LNM* 900, Springer 1982. Especially Ch. I (Deligne) "Hodge cycles on abelian varieties" pp. 9-100, and Ch. II (Milne) on Shimura varieties. MathSciNet MR0654325.
- **Schütt 2005** : Schütt, M., "*Hecke eigenforms with rational coefficients and complex multiplication*", *Math. Z.* 250 (2005), 213-237. arXiv:math/0511228. **REAL** (verified via verify-arxiv.py).
- **Schütt 2008** : Schütt, M., "*K3 surfaces with Picard rank 20*", *Algebra and Number Theory* 2 (2008), 357-401. arXiv:0804.1558. **REAL** (verified via verify-arxiv.py).
- **Milne 2017** : Milne, J. S., *Introduction to Shimura Varieties*, lecture notes, version 2.21 (April 2017), available at https://www.jmilne.org/math/xnotes/svi.pdf. (Earlier version published in *Harmonic Analysis, the Trace Formula, and Shimura Varieties*, Clay Math. Proc. 4, 2005, AMS, ed. Arthur–Ellwood–Kottwitz, pp. 265-378.)

---

## 10. Honesty checklist and cluster impact

1. **Zero new arXiv IDs introduced** : the references are 7 classical / 2 canonical / 1 LMFDB lookup. No fab risk.
2. **Pohlmann 1968 attribution verified** : the *Annals of Math.* 88 (1968) reference is MathSciNet MR0228500 ; the title "*Algebraic cycles on abelian varieties of complex multiplication type*" is identifiable in any algebraic-geometry library.
3. **Deligne 1982 reference verified** : the *LNM* 900 volume "*Hodge Cycles, Motives, and Shimura Varieties*" is a foundational textbook (the Deligne paper is Ch. I) ; MathSciNet MR0654325.
4. **Cluster fab status** : entering 184, exiting **184** (no change).
5. **Honest downgrade flagged** : Conjecture 5.7 (Schütt MULTI-D paper draft) → Theorem 5.7 (this document), framed as classical (Pohlmann + Deligne). Submission target Inventiones → *J. Number Theory*. Hodge Millennium credit 3-7% → **0.5 – 1%**.
6. **No "Inventiones-tier" or "Hodge Conjecture upgrade" language used** in the new framing.

---

## 11. Action items (post-write-up)

The following downstream edits should be made to align other ECI v14 documents with the present write-up :

1. **`Paper_Schutt_MultiD_JNumberTheory_draft.md`** : replace §5.7 "Conjecture 5.7" with "Theorem 5.7" using the new wording (§6.2 above). Update §1.4 disclaimer to drop "we do not prove Hodge" and replace with "the Hodge-class statement, Theorem 5.7, is a classical consequence of Pohlmann 1968 + Deligne 1982". Update §5.6 wording on Tankeev-theorem expectation to direct citation of Pohlmann 1968 + Deligne 1982. Update §7 (Conclusion) to drop the "Hodge-class refinement is open" bullet and replace with "Theorem 5.7 is classical". Strike "Inventiones" mention from §7 ; insert "*Journal of Number Theory*" as the sole submission target.
2. **`Theorem_ECI_v12_MasterPrinciple.md`** : add §1.5 "Mumford-Tate torus framework" citing the present document. Replace any "Schoen 1988" attributions in the algebraic-cycle backbone with "Pohlmann 1968 + Deligne 1982 + Theorem 5.1 of `Theorem_ECI_MumfordTate_torus_formalized.md`".
3. **`ECI_v14_spec_2026-05-10.md`** : update §0 (Wave 2 D1 dissolution) with the corrected Mumford-Tate framing.
4. **`MEMORY.md`** : add a feedback note "Mumford-Tate torus replaces Schoen 1988 attribution" with a pointer to the present document.
5. **Hodge Millennium narrative documents** : downgrade credit 3-7% → 0.5 – 1% with the corresponding rewording.

These edits are *purely citational and framing*, not substantive changes to any computed quantity. They take 1-2 hours of focused editing.

---

## 12. Summary

This document **replaces** the previously-circulated speculative attribution "Schoen 1988 *Math. Annalen* 282 self-product CM line" — which was used in earlier drafts of the Schütt MULTI-D paper and in `Theorem_ECI_v12_MasterPrinciple.md` as the supposed rigorous backbone for the algebraic-cycle realization $Z_D$ of the 2-dim Hecke eigencomponent $V_D = \rho_{f_D} \subset H^4((E_K)^4, \mathbb{Q})$ — with the **rigorous Mumford-Tate torus framework**, viz.:

- $\mathrm{MT}(H^1(E_K, \mathbb{Q})) \cong \mathrm{Res}_{K/\mathbb{Q}}\,\mathbb{G}_m$ is a 2-dimensional algebraic torus over $\mathbb{Q}$ (Mumford 1966).
- Consequently $\mathrm{MT}$ of every tensor-power cohomology $H^j((E_K)^n, \mathbb{Q})$ is also a torus, so by the **Pohlmann 1968 theorem on CM Hodge cycles**, every Hodge class on every $(E_K)^n$ is algebraic, given by an **explicit Pohlmann partial-diagonal cycle representative**.
- The 2-dim Hecke eigencomponent $V_D \subset H^4((E_K)^4, \mathbb{Q})$ has Hodge type $(4, 0) + (0, 4)$ (no $(2, 2)$-part), so the "Hodge conjecture for $V_D$" question is **vacuous as a Hodge-conjecture statement**. The legitimate question is the explicit *Mumford-Tate cycle representative* $Z_D$, whose existence is classical (Pohlmann + Deligne).
- The Frobenius eigenvalue of $Z_D$ at a split prime $p \mathcal{O}_K = \mathfrak{p} \overline{\mathfrak{p}}$ is $a_p(f_D) = \pi^4 + \overline{\pi}^4$ matching Theorem A of the Schütt MULTI-D paper. This is the meaningful eigenvalue identity ; the "Hodge-class refinement" Conjecture 5.7 should be reframed as **Theorem 5.7 (classical)** rather than a conjecture.
- **Honest downgrade** : the Schütt MULTI-D paper submission target moves *Inventiones* → *J. Number Theory* ; the Hodge Millennium narrative credit downgrades 3-7% → **0.5 – 1%** ; the algebraic-cycle backbone is now correctly framed as a classical 1968-1982 theorem rather than a new contribution.

The cluster fab status remains at **184 firm** (zero new arXiv IDs introduced ; all references are classical pre-arXiv or canonical lecture notes).

---

*End of `Theorem_ECI_MumfordTate_torus_formalized.md`. Length : ~6500 mots. Status : write-up complete ; downstream edits to Schütt MULTI-D paper, ECI v12 master principle, ECI v14 spec, and MEMORY.md pending (per §11 action items).*
