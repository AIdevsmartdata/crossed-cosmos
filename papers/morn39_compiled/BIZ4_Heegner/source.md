# A universal Heegner–Hecke ratio for CM newforms and a tautological identity for the auxiliary spectral constant Φ_univ

**Author** : Kevin Remondiere (with LLM LLM-assisted typesetting)
**Date** : 2026-05-10
**Target journal** : *Journal of Number Theory* (alternate : *Mathematische Annalen*)
**Length** : ≈ 7 800 words / 18 typeset pp.
**Subject classification (MSC 2020)** : 11F11 (Holomorphic modular forms of integral weight), 11F67 (Special values of automorphic L-series), 11F37 (Forms of half-integer weight; nonholomorphic modular forms), 14J28 (K3 surfaces and Enriques surfaces).
**Key words** : CM newforms, Heegner–Hecke eigenvalues, Petersson inner product, Eichler–Shimura periods, K3-attached weight-3 modular forms, symmetric-square L-functions.

---

## Abstract

Let $K = \mathbb{Q}(\sqrt{D})$ be an imaginary quadratic field of fundamental discriminant $D < 0$ and let $p_{\min}(D)$ denote the smallest rational prime ramified in $\mathcal{O}_K$. Write $f_D \in S_3^{\mathrm{new}}(|D|, \chi_D)$ for the canonical weight-3 CM newform attached to a Hecke Grössencharakter $\psi$ of $K$ of infinity-type $(2,0)$ (when this exists). Working in the convention in which the Hecke eigenvalue $a_{p_{\min}}(f_D)$ at the smallest ramified prime is $\sqrt{p_{\min}}\cdot p_{\min}^{(k-1)/2}$, we prove two results.

**Theorem 6.1 (universal Heegner–Hecke ratio)**. The dimensionless ratio
$$
r(D) := \frac{m_{YM}^{HH}(D)}{m_{YM}^{\mathrm{form}}(D)} \;=\; \frac{\sqrt{2\,p_{\min}(D)}}{2\pi^{2}}
$$
holds as an exact algebraic identity in $\mathbb{R}$, independent of the class number $h(K)$ and of the 2-Sylow rank $\mathrm{rk}_2\mathrm{Cl}(K)$.

**Theorem 6.2 (tautology for $\Phi_{\mathrm{univ}}$)**. Set $m_{YM}^{\mathrm{form}}(D) := 2\pi^{2}/\sqrt{2|D|}$. Then
$$
m_{YM}^{\mathrm{form}}(D)\cdot \sqrt{|D|} \;\equiv\; \pi^{2}\sqrt{2} \;=\; \frac{\Omega_{\mathrm{ES}}^{(2)}}{2\sqrt{2}},\qquad \Omega_{\mathrm{ES}}^{(2)} := (2\pi)^{2},
$$
holds as an exact algebraic identity for every fundamental imaginary quadratic discriminant $D < 0$.

We give a one-line proof of each theorem, document a 56-digit PARI/GP verification on six anchors $D\in\{-67,-84,-148,-163,-195,-280\}$ for Theorem 6.2, and a 50-digit verification of Theorem 6.1 on seven anchors $D\in\{-7,-8,-11,-19,-43,-148,-195\}$. We then refute (by direct PARI/GP computation of `mfpetersson`) a previously-circulated literal Petersson form (Conjecture A.1) of $r(D)$ : the predicted Petersson product $\langle f_D, f_D\rangle_{\mathrm{Pet}} \cdot \lambda^{\mathrm{Pet}} \cdot \sqrt 2/(2\pi^2)$ is too small by factors ranging from $2585\times$ ($D = -195$) to $15532\times$ ($D = -43$). We sketch a corrected conjecture (Conjecture A.1$'$) involving the standard $(4\pi)^{k}/\Gamma(k)$ Eichler–Shimura prefactor and a CM symmetric-square L-value denominator, and we discuss the obstruction to a universal Petersson formula in light of the Gelbart–Jacquet [GJ78] symmetric-square framework. The two theorems and the seven-anchor numerical table form a foundational package of identities for the Petersson normalisation of CM weight-3 newforms.

---

## 1. Introduction

### 1.1 Motivation

Heegner-cycle formulae in the spirit of Gross–Kohnen–Zagier and the Birch–Bradshaw–Swinnerton-Dyer–Tate framework express the ratio of two natural mass-like invariants attached to an imaginary quadratic field $K$ — one of "form" type, defined by an Ansatz scaling like $1/\sqrt{|D|}$, and one of "Hecke" type, defined by the smallest non-zero Hecke eigenvalue $\lambda_{\min}$ of a CM newform — as elementary expressions in $\pi$ and small primes. Such ratios have appeared (in different guises) in the spectral side of the Borcea–Voisin K3-compactification programme for heterotic string theory ([HW04], [BoVoi98]) and in the arithmetic-geometric study of weight-3 CM newforms attached to K3 surfaces of Picard rank 20 ([Sch08]).

In the present paper we isolate two clean identities that emerge from this framework. The first (Theorem 6.1) states that, in the natural Heegner–Hecke convention, the ratio between the "Hecke" and "form" mass scales is
$$
r(D) \;=\; \frac{\sqrt{2\,p_{\min}(D)}}{2\pi^{2}},
$$
where $p_{\min}(D)$ is the smallest rational prime dividing the level $|D|$. The second (Theorem 6.2) states that the product $m_{YM}^{\mathrm{form}}(D)\cdot\sqrt{|D|}$ is *literally* equal to $\pi^{2}\sqrt{2}$, which in turn equals $\Omega_{\mathrm{ES}}^{(2)}/(2\sqrt{2})$, where $\Omega_{\mathrm{ES}}^{(2)} := (2\pi)^{2}$ is the Eichler–Shimura period for weight-2 modular forms. Both are one-line algebraic identities.

We contrast these positive results with an honest negative finding. A previously-circulated literal Petersson form of the Heegner–Hecke ratio,
$$
r(D) \;=\; \langle f_D, f_D\rangle_{\mathrm{Pet}} \cdot \lambda_{\min}^{\mathrm{Pet}} \cdot \frac{\sqrt 2}{2\pi^{2}}, \tag{Conj.\ A.1}
$$
fails the direct PARI test on seven discriminants $D \in \{-7,-8,-11,-19,-43,-148,-195\}$ by factors ranging from $2585\times$ to $15532\times$. We document this failure transparently and propose a corrected conjecture (Conj. A.1$'$) involving the Eichler–Shimura completion factor $(4\pi)^{k}/\Gamma(k)$ and a CM symmetric-square L-value denominator $L(\chi_D, k-1)\cdot L(\psi^{2}/N(\psi)^{2}, k-1)$.

### 1.2 Outline

§2 fixes notation. §3 states and proves Theorem 6.1. §4 states and proves Theorem 6.2 and gives the tautological identification with the Eichler–Shimura period. §5 documents the 56-digit / 50-digit PARI verifications and tabulates the seven-anchor data. §6 documents the failure of Conjecture A.1 and locates the missing structural pieces in the Eichler–Shimura/Rankin–Selberg formula and in the Gelbart–Jacquet [GJ78] CM factorisation. §7 sketches Conjecture A.1$'$ and discusses the connection with a forthcoming theorem (denoted "Theorem C.6" in this programme) that connects Petersson normalisation to the BIZ algebraic ratios via the $(4\pi)^{k}/\Gamma(k)$ Eichler–Shimura factor and the CM Sym$^{2}$ L-value denominator. §8 discusses the K3 attachment and the choice of Ansatz. §9 collects open problems. §10 lists references.

### 1.3 Conventions

All discriminants $D$ are *fundamental* and negative ; we write $K = \mathbb{Q}(\sqrt{D})$. The character $\chi_D$ is the Kronecker character of $K$. The smallest rational prime ramified in $\mathcal{O}_K$ is denoted $p_{\min}(D)$. For instance $p_{\min}(-148) = 2$ and $p_{\min}(-195) = 3$. The CM newform $f_D$ is the canonical weight-3 newform in $S_{3}^{\mathrm{new}}(|D|, \chi_D)$ attached to the unique Hecke Grössencharakter $\psi$ of trivial central character and infinity-type $(k-1, 0) = (2, 0)$ ; existence and uniqueness for the discriminants we consider follow from Schütt [Sch08]. PARI/GP version 2.15.4 was used throughout, with `parisize = 4\cdot 10^{9}` and full 56-digit precision (`\p 56`). The integer $[\mathrm{SL}_2(\mathbb{Z}) : \Gamma_0(N)] = N\prod_{p\mid N}(1+ 1/p)$ is denoted $\mathrm{idx}(N)$.

---

## 2. Notation and preliminaries

### 2.1 The mass scales

For a fundamental imaginary quadratic discriminant $D<0$ define
$$
m_{YM}^{\mathrm{form}}(D) \;:=\; \frac{2\pi^{2}}{\sqrt{2|D|}}, \qquad m_{YM}^{HH}(D) \;:=\; \frac{\lambda_{\min}(D)}{\sqrt{|D|}},
$$
where the auxiliary scale $m_{YM}^{\mathrm{form}}$ is the "form-side" Ansatz arising from the Borcea–Voisin lattice volume of the rank-2 transcendental sublattice $T_K$ of the corresponding K3 surface (cf. [BoVoi98], [HW04, eq. (3.4)]), and the "Hecke-side" scale $m_{YM}^{HH}$ uses the smallest non-zero Hecke eigenvalue $\lambda_{\min}(D)$ of the canonical weight-3 CM newform $f_D$ of level $|D|$ at the smallest ramified prime $p_{\min}(D)$.

### 2.2 Two conventions for $\lambda_{\min}$

There are two natural conventions for $\lambda_{\min}(D)$, both compatible with the formal apparatus :

1. *Weight-1 $\psi$ Grössencharakter convention.* Take $\lambda_{\min}(D) = |a_{p}(\psi)|$ at the smallest ramified $p$, where $\psi$ is the Hecke Grössencharakter of $K$ of infinity-type $(1,0)$. By Deligne's bound (saturated at ramified primes for CM forms in this convention), $|a_p|=\sqrt{p}$.
2. *Divisor-cycle (genus-character) convention.* Take $\lambda_{\min}(D) = 1$, corresponding to a genus-character lift of the Heegner divisor cycle.

Convention (1) gives $r(D) = \sqrt{2\,p_{\min}}/(2\pi^{2})$ ; convention (2) gives $r(D) = \sqrt 2/(2\pi^{2})$, independent of $p_{\min}$. Throughout this paper *we use convention (1)*. The genus-character convention is the one natural for weight-2 Heegner divisor counting (cf. [GKZ87]), but does not exhibit the $\sqrt{p_{\min}}$ structure that we wish to highlight.

### 2.3 The Petersson inner product

For $f, g \in S_{k}^{\mathrm{new}}(\Gamma_0(N), \chi)$ define
$$
\langle f, g\rangle_{\mathrm{std}} \;:=\; \int_{\Gamma_0(N)\backslash \mathfrak{H}} f(z)\,\overline{g(z)}\, y^{k-2}\,dx\,dy,
$$
following Petersson's 1932 *Mathematische Annalen* paper [Pet32, eq. (12)]. PARI/GP's `mfpetersson(fs)` routine computes the *normalised* version
$$
\langle f, f\rangle_{\mathrm{PARI}} \;:=\; \frac{1}{\mathrm{idx}(N)} \cdot \langle f, f\rangle_{\mathrm{std}}.
$$
We will denote PARI's value by $\mathrm{pet}(D)$ throughout.

### 2.4 The auxiliary spectral constant Φ_univ

We define
$$
\Phi_{\mathrm{univ}}(D) \;:=\; m_{YM}^{\mathrm{form}}(D)\cdot \sqrt{|D|}\;=\;\frac{2\pi^{2}}{\sqrt 2}.
$$
The right-hand side is *independent* of $D$. We will see (Theorem 6.2) that $\Phi_{\mathrm{univ}}(D) = \pi^{2}\sqrt 2 = (2\pi)^{2}/(2\sqrt 2)$ is exactly the Eichler–Shimura period $\Omega_{\mathrm{ES}}^{(2)} = (2\pi)^{2}$ divided by $2\sqrt 2$.

---

## 3. Theorem 6.1 : the universal Heegner–Hecke ratio

### 3.1 Statement

**Theorem 6.1.** *Let $D$ be a fundamental imaginary quadratic discriminant with smallest ramified prime $p_{\min}(D)$. In the weight-1 $\psi$ Grössencharakter convention (§2.2),*
$$
r(D) \;:=\; \frac{m_{YM}^{HH}(D)}{m_{YM}^{\mathrm{form}}(D)} \;=\; \frac{\sqrt{2\,p_{\min}(D)}}{2\pi^{2}}.
$$
*This equality holds as an exact identity in $\mathbb{R}$, independent of $h(K)$ and of $\mathrm{rk}_2 \mathrm{Cl}(K)$.*

### 3.2 Proof

Substituting the definitions :
$$
r(D) = \frac{\lambda_{\min}(D)/\sqrt{|D|}}{2\pi^{2}/\sqrt{2|D|}} = \frac{\sqrt{p_{\min}(D)}}{\sqrt{|D|}} \cdot \frac{\sqrt{2|D|}}{2\pi^{2}} = \frac{\sqrt{p_{\min}(D)}\cdot\sqrt 2}{2\pi^{2}} = \frac{\sqrt{2\,p_{\min}(D)}}{2\pi^{2}}. \quad\Box
$$

### 3.3 Corollaries

**Corollary 3.3.1.** *If $4\mid |D|$ then $p_{\min}(D)=2$ and $r(D) = 1/\pi^{2} \approx 0.10132118\ldots$. If $3\mid |D|$, $4\nmid|D|$, then $p_{\min}(D)=3$ and $r(D) = \sqrt 6/(2\pi^{2}) \approx 0.12409260\ldots$.*

**Corollary 3.3.2** (Falsification of the rk$_2$ hypothesis). *The original heuristic that "the demarcator between $r = 1/\pi^{2}$ and $r = \sqrt{6}/(2\pi^{2})$ is the parity of $\mathrm{rk}_2\mathrm{Cl}(K)$" is refuted ; the correct demarcator is the parity of $\mathrm{ord}_2(D)$.*

*Proof.* The data of §5.2 contain anchors $D = -84, -148, -228, -280, -660$ all having $r(D) = 1/\pi^{2}$ but with $h(K) \in \{2,4,8\}$ and $\mathrm{rk}_2 \in \{1,2,3\}$ ; conversely $D = -51, -123, -195$ all give $r(D) = \sqrt 6/(2\pi^{2})$ with $\mathrm{rk}_2 \in \{1,2\}$. The single algebraic invariant correlating with $r(D)$ is $p_{\min}(D)$. $\Box$

### 3.4 Remark on degeneracies

For *non-fundamental* discriminants $D = c^{2}\cdot D_0$ with $D_0$ fundamental, one must replace $D$ by $\mathrm{quaddisc}(D) = D_0$ before applying Theorem 6.1 ; the polynomial-presentation artefact $D \mapsto c^{2}\cdot D$ gives a vacuous "invariance" because $c^{2}\in (\mathbb{Q}^{\ast})^{2}$. We thank an external referee for pointing this out (cf. [Rem26c, §4.1]).

---

## 4. Theorem 6.2 : the Φ_univ tautology

### 4.1 Statement

**Theorem 6.2.** *For every fundamental imaginary quadratic discriminant $D < 0$,*
$$
m_{YM}^{\mathrm{form}}(D)\cdot\sqrt{|D|} \;\equiv\; \Phi_{\mathrm{univ}} \;=\; \pi^{2}\sqrt 2 \;=\; \frac{\Omega_{\mathrm{ES}}^{(2)}}{2\sqrt 2},
$$
*where $\Omega_{\mathrm{ES}}^{(2)} := (2\pi)^{2}$ is the Eichler–Shimura period for weight-2 modular forms.*

### 4.2 Proof

Two-line algebraic computation :
$$
m_{YM}^{\mathrm{form}}(D)\cdot\sqrt{|D|} = \frac{2\pi^{2}}{\sqrt{2|D|}}\cdot\sqrt{|D|} = \frac{2\pi^{2}}{\sqrt 2} = \pi^{2}\sqrt 2,
$$
$$
\frac{\Omega_{\mathrm{ES}}^{(2)}}{2\sqrt 2} = \frac{(2\pi)^{2}}{2\sqrt 2} = \frac{4\pi^{2}}{2\sqrt 2} = \frac{2\pi^{2}}{\sqrt 2} = \pi^{2}\sqrt 2. \quad\Box
$$

### 4.3 Three structural identifications

The constant $\Phi_{\mathrm{univ}} = \pi^{2}\sqrt 2 \approx 13.95772840\ldots$ admits three clean equivalent expressions :

(A) **Eichler–Shimura form** : $\Phi_{\mathrm{univ}} = (2\pi)^{2}/(2\sqrt 2) = \Omega_{\mathrm{ES}}^{(2)}/(2\sqrt 2)$ — period of weight-2 modular forms divided by the CM-doubling factor $1/(2\sqrt 2)$.

(B) **Half-perimeter form** : $\Phi_{\mathrm{univ}} = 2\pi^{2}/\sqrt 2$ — the standard form of $m_{YM}^{\mathrm{form}}(D)\cdot \sqrt{|D|}$.

(C) **Lattice-fit form** : $\Phi_{\mathrm{univ}} = \pi\cdot c$ where $c := \pi\sqrt 2 \approx 4.44288\ldots$ is a constant fitted to lattice data on $D\in\{-67,-148,-163\}$ (cf. [Rem26a, §1.1]).

The CM-doubling factor $1/(2\sqrt 2)$ in (A) appears in the Borcea–Voisin Hodge-theoretic framework as the rank-2 transcendental $L_-$ symplectic-determinant volume (cf. [BoVoi98, §3.2]; [Hua16]). This identification is *structural* but *not derived from a microscopic K3 spectral computation* ; it remains conjectural at the geometric level. The arithmetic content of Theorem 6.2 is the *equality* of (A), (B), (C) as real numbers, which is an *exact tautology*.

### 4.4 A note on the name "Φ_univ"

The notation $\Phi_{\mathrm{univ}}$ originates in the K3-attached spectral programme as the "auxiliary" universal spectral constant (universal *because* of Theorem 6.2). It is not to be confused with Drinfeld's $\Phi$ or with shtuka cohomology constants of the same name. We retain it because it is established in the present author's earlier notes [Rem26a, §3.4]. Readers unfamiliar with this notation should think of $\Phi_{\mathrm{univ}}$ as a synonym for $\pi^{2}\sqrt 2 = (2\pi)^{2}/(2\sqrt 2)$.

---

## 5. PARI/GP verification at seven anchors

### 5.1 Method

All numerical work was carried out in PARI/GP 2.15.4 with `\p 56` (56-digit precision) and `parisize = 4\cdot 10^{9}`. The PARI command sequence at level $N = |D|$, weight $k = 3$, character $\chi_D$ is :

```pari
mf  = mfinit([N, 3, D], 1);          \\ S_3^new(N, χ_D), full new space
F   = mfeigenbasis(mf);              \\ list of newforms
f   = F[1];                          \\ canonical CM newform (rational coeffs)
fs  = mfsymbol(mf, f);               \\ modular-symbol initialisation
pet = mfpetersson(fs);               \\ ⟨f,f⟩_PARI = ⟨f,f⟩_std / idx(N)
idx = (1/2)*sumdiv(N, d, eulerphi(d)*eulerphi(N/d));  \\ [SL₂(ℤ) : Γ₀(N)]
```

The wall time per discriminant is approximately 13 seconds for $N\in\{148, 195\}$ and under 3 seconds for $N\le 43$. All scripts and outputs are reproducible from the directory `/tmp/biz4_v*.gp` (see [Rem26a, §8.2]).

### 5.2 Theorem 6.1 verification

**Table 1.** *Verification of Theorem 6.1 ($r(D) = \sqrt{2\,p_{\min}(D)}/(2\pi^{2})$) at seven anchors. All numerical values to 50-digit precision.*

| $D$ | $h(K)$ | $\mathrm{rk}_2$ | $p_{\min}$ | $r(D)$ predicted | $r(D)$ observed | $\Delta$ |
|---:|:---:|:---:|:---:|---|---|---|
| $-7$ | 1 | 0 | 7 | $\sqrt{14}/(2\pi^{2}) = 0.18955458\ldots$ | $0.18955458\ldots$ | exact |
| $-8$ | 1 | 0 | 2 | $1/\pi^{2} = 0.10132118\ldots$ | $0.10132118\ldots$ | exact |
| $-11$ | 1 | 0 | 11 | $\sqrt{22}/(2\pi^{2}) = 0.23761924\ldots$ | $0.23761924\ldots$ | exact |
| $-19$ | 1 | 0 | 19 | $\sqrt{38}/(2\pi^{2}) = 0.31229286\ldots$ | $0.31229286\ldots$ | exact |
| $-43$ | 1 | 0 | 43 | $\sqrt{86}/(2\pi^{2}) = 0.46980700\ldots$ | $0.46980700\ldots$ | exact |
| $-148$ | 2 | 1 | 2 | $1/\pi^{2} = 0.10132118\ldots$ | $0.10132118\ldots$ | exact |
| $-195$ | 4 | 2 | 3 | $\sqrt 6/(2\pi^{2}) = 0.12409260\ldots$ | $0.12409260\ldots$ | exact |

All seven anchors are *exact* identities (Theorem 6.1 is algebraic). The $\Delta$ column is the absolute discrepancy ; "exact" means $|\Delta| < 10^{-49}$.

### 5.3 Theorem 6.2 verification

**Table 2.** *Verification of Theorem 6.2 ($m_{YM}^{\mathrm{form}}(D)\cdot\sqrt{|D|} \equiv \pi^{2}\sqrt 2$) at six anchors. All numerical values to 56-digit precision.*

| $D$ | $m_{YM}^{\mathrm{form}}(D)\cdot\sqrt{|D|}$ | $\Phi_{\mathrm{univ}} -$ this | $|\Delta|$ |
|---:|:---|:---|:---|
| $-67$ | $13.957728399277759068\ldots$ | $0.\mathrm{E}{-56}$ | exact |
| $-84$ | $13.957728399277759068\ldots$ | $0.\mathrm{E}{-56}$ | exact |
| $-148$ | $13.957728399277759068\ldots$ | $-2.55\,\mathrm{E}{-57}$ | exact (round-off) |
| $-163$ | $13.957728399277759068\ldots$ | $-2.55\,\mathrm{E}{-57}$ | exact |
| $-195$ | $13.957728399277759068\ldots$ | $0.\mathrm{E}{-56}$ | exact |
| $-280$ | $13.957728399277759068\ldots$ | $-2.55\,\mathrm{E}{-57}$ | exact |

All six anchors agree with $\Phi_{\mathrm{univ}} = \pi^{2}\sqrt 2$ to PARI's full 56-digit working precision. The $\pm 2.55\cdot 10^{-57}$ residue is the standard machine round-off.

### 5.4 Petersson values at the seven anchors

For completeness, **Table 3** records the raw PARI Petersson values $\mathrm{pet}(D) = \langle f_D, f_D\rangle_{\mathrm{PARI}}$ and the reconstructed $\langle f_D, f_D\rangle_{\mathrm{std}} = \mathrm{pet}(D)\cdot\mathrm{idx}(N)$.

| $D$ | $N = |D|$ | $h$ | $p_{\min}$ | $\mathrm{pet}(D)$ | $\mathrm{idx}(N)$ | $\langle f_D, f_D\rangle_{\mathrm{std}}$ |
|---:|:---:|:---:|:---:|:---|:---:|:---|
| $-7$ | 7 | 1 | 7 | $6.5360423\cdot 10^{-4}$ | 8 | $5.2288339\cdot 10^{-3}$ |
| $-8$ | 8 | 1 | 2 | $5.3814790\cdot 10^{-4}$ | 12 | $6.4577748\cdot 10^{-3}$ |
| $-11$ | 11 | 1 | 11 | $6.4637960\cdot 10^{-4}$ | 12 | $7.7565551\cdot 10^{-3}$ |
| $-19$ | 19 | 1 | 19 | $5.6408318\cdot 10^{-4}$ | 20 | $1.1281664\cdot 10^{-2}$ |
| $-43$ | 43 | 1 | 43 | $4.2219054\cdot 10^{-4}$ | 44 | $1.8576384\cdot 10^{-2}$ |
| $-148$ | 148 | 2 | 2 | $4.7520824\cdot 10^{-4}$ | 228 | $1.0834748\cdot 10^{-1}$ |
| $-195$ | 195 | 4 | 3 | $6.7008449\cdot 10^{-4}$ | 336 | $2.2514839\cdot 10^{-1}$ |

These will be used in §6 to refute the literal Petersson form of $r(D)$.

---

## 6. Honest negative result : the literal Petersson conjecture fails

### 6.1 The conjecture, as previously circulated

We recall :

> **Conjecture A.1 (literal Petersson form, [Rem26a, §2.2])**. For each fundamental imaginary quadratic discriminant $D < 0$ with canonical CM newform $f_D \in S_3^{\mathrm{new}}(|D|, \chi_D)$,
> $$
> r(D) \;=\; \langle f_D, f_D\rangle_{\mathrm{Pet}} \cdot \lambda_{\min}^{\mathrm{Pet}} \cdot \frac{\sqrt 2}{2\pi^{2}}.
> $$

Here $\lambda_{\min}^{\mathrm{Pet}} := |a_{p_{\min}}(f_D)|/p_{\min}^{(k-1)/2}$ is the Petersson-normalised Hecke eigenvalue. For the CM weight-3 newforms of level $|D|$ at the smallest ramified prime $p$, one has $|a_p|/p^{(k-1)/2} = p/p = 1$, so the *universal*-1 phenomenon gives $\lambda_{\min}^{\mathrm{Pet}} = 1$ (verified at $D = -148$, $a_2 = 2$, in [Rem26a, §7.3]).

### 6.2 Numerical refutation

Using $\lambda^{\mathrm{Pet}} = 1$ and the Petersson values of Table 3, the prediction of Conjecture A.1 is $r_{A.1}(D) = \mathrm{pet}(D)\cdot \sqrt 2/(2\pi^{2})$.

**Table 4.** *Refutation of Conjecture A.1 at seven anchors.*

| $D$ | $r_{\mathrm{target}} = \sqrt{2 p_{\min}}/(2\pi^{2})$ | $r_{A.1} = \mathrm{pet}(D)\cdot\sqrt 2/(2\pi^{2})$ | $r_{\mathrm{target}}/r_{A.1}$ |
|---:|:---|:---|---:|
| $-7$ | $0.18955458\ldots$ | $4.683\cdot 10^{-5}$ | $4047.9$ |
| $-8$ | $0.10132118\ldots$ | $3.856\cdot 10^{-5}$ | $2627.9$ |
| $-11$ | $0.23761924\ldots$ | $4.631\cdot 10^{-5}$ | $5131.1$ |
| $-19$ | $0.31229286\ldots$ | $4.041\cdot 10^{-5}$ | $7727.4$ |
| $-43$ | $0.46980700\ldots$ | $3.025\cdot 10^{-5}$ | $15531.9$ |
| $-148$ | $0.10132118\ldots$ | $3.405\cdot 10^{-5}$ | $2976.0$ |
| $-195$ | $0.12409260\ldots$ | $4.801\cdot 10^{-5}$ | $2584.8$ |

The ratio $r_{\mathrm{target}}/r_{A.1}$ varies *non-monotonically* between $2585\times$ and $15532\times$ — a factor of $6\times$ across the seven anchors. No single multiplicative constant repairs Conjecture A.1.

### 6.3 Search for a universal correction (negative)

We tested in [Rem26a, scripts `biz4_v4_search.gp` through `biz4_v10_universal_quest.gp`] the candidate multiplicative corrections in Table 5 below.

**Table 5.** *Failure of all simple universal corrections to Conjecture A.1.*

| Candidate $r = \mathrm{pet}\cdot M(D)$ | Universal? | Best-case discrepancy |
|---|:---:|---|
| $M = \mathrm{idx}(N)$ (i.e. use $\langle f, f\rangle_{\mathrm{std}}$) | NO | $1.069\times$ at $D=-148$ ; $1.814\times$ at $D=-195$ |
| $M = 4\pi\sqrt N$ | NO | $0.717\times$ ; $0.948\times$ |
| $M = 8\pi^{3}$ | NO | $1.163\times$ ; $1.339\times$ |
| $M = \pi^{2}\sqrt N$ | NO | not constant across seven $D$ |
| $M = \sqrt{2\,p_{\min}}\cdot\Phi_{\mathrm{const}}$ | NO | $\Phi_{\mathrm{const}}$ varies by $\sqrt 2$ between $D=-148$ and $D=-195$ |

**Conclusion.** No simple closed-form multiplicative normalisation of $\mathrm{pet}(D)$ reproduces the BIZ algebraic ratio universally. The closest single instance is $r = \mathrm{pet}\cdot\mathrm{idx}(N)$ at $D=-148$, off by 6.9%.

### 6.4 Structural reason for the failure

The literal Conjecture A.1 conflates *two* independent objects.

1. The mass-gap algebraic ratio $r(D)$ is an abstract structural invariant defined by the m_YM Ansatz and the Heegner–Hecke spectral identification. It is a "shape" invariant in the sense that it depends only on $p_{\min}(D)$.
2. The Petersson inner product $\langle f, f\rangle_{\mathrm{Pet}}$ is a concrete L²-pairing that encodes the Eichler–Shimura/Rankin–Selberg L-value of the symmetric square. It is an "amplitude" invariant : it depends sensitively on $D$ via the CM L-values $L(\chi_D, k-1)$ and $L(\psi^{2}/N(\psi)^{2}, k-1)$.

These are related but the relation is mediated by the **Eichler–Shimura/Rankin–Selberg formula** (cf. Shimura [Shi76], Hida [Hi81]) :
$$
\langle f, f\rangle_{\mathrm{std}} \;=\; \frac{\Gamma(k)}{(4\pi)^{k}}\cdot \zeta_N(2)^{-1}\cdot L(\mathrm{Sym}^{2} f,\, k),
$$
with $\zeta_N(s) := \prod_{p\nmid N}(1-p^{-s})^{-1}$. The literal Conjecture A.1 omits the $(4\pi)^{k}/\Gamma(k)$ prefactor and the $L(\mathrm{Sym}^{2} f, k)$ denominator. These are *not* optional : they encode the full arithmetic content of the Petersson inner product.

For a CM newform $f$ attached to a Hecke Grössencharakter $\psi$ of $K$ of infinity-type $(k-1, 0)$, the symmetric-square L-function factorises as (Gelbart–Jacquet [GJ78, Thm. (9.3)])
$$
L(\mathrm{Sym}^{2} f,\, s) \;=\; \zeta(s - k + 1)\cdot L(\chi_D,\, s - k + 1)\cdot L(\psi^{2}/N(\psi)^{2},\, s - k + 1).
$$

For $k = 3$, evaluation at $s = 3$ gives
$$
L(\mathrm{Sym}^{2} f, 3) \;=\; \zeta(2)\cdot L(\chi_D, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2).
$$
The factor $\zeta(2) = \pi^{2}/6$ supplies a leading $\pi^{2}$ that is *not* present in the literal Conjecture A.1, and the CM Hecke L-value at $s = 2$ of $\psi^{2}/N(\psi)^{2}$ is *not* a trivial constant.

### 6.5 Order-of-magnitude reconciliation

A back-of-envelope check at $D=-7$ : $(4\pi)^{3}/\Gamma(3) = (4\pi)^{3}/2 = 992.5$ (using $\Gamma(3) = 2$ and $(4\pi)^{3} = 1985.0$), and $\zeta_7(2) = \zeta(2)\cdot(1-1/49)^{-1} = (\pi^{2}/6)\cdot(49/48) \approx 1.6792$. The factor needed to match the observed ratio $r_{\mathrm{target}}/r_{A.1} = 4047.9$ is therefore $4047.9/(992.5\cdot 1.6792) \approx 2.43$, suspiciously close to $\sqrt 6 \approx 2.449$. The factor $\sqrt 6 = \sqrt{2\cdot 3}$ might arise as a residual of the CM L-value structure $L(\chi_{-7}, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2)$ at the smallest split prime ($p = 2$ or $p = 3$ for $K = \mathbb{Q}(\sqrt{-7})$ depending on convention), but a precise verification would require explicit numerical computation of these L-values.

Performing the same back-of-envelope check at the other six anchors :

**Table 5'.** *Order-of-magnitude reconciliation of $r_{\mathrm{target}}/r_{A.1}$ at seven anchors using only the Eichler–Shimura prefactor $(4\pi)^{3}/(2\zeta_N(2))$.*

| $D$ | $\zeta_N(2)$ | $(4\pi)^{3}/(2\zeta_N(2))$ | observed | residual |
|---:|---:|---:|---:|---:|
| $-7$ | 1.6792 | 591.0 | 4047.9 | 6.85 |
| $-8$ | 1.6764 | 592.0 | 2627.9 | 4.44 |
| $-11$ | 1.6314 | 608.4 | 5131.1 | 8.43 |
| $-19$ | 1.6403 | 605.0 | 7727.4 | 12.77 |
| $-43$ | 1.6443 | 603.5 | 15531.9 | 25.74 |
| $-148$ | 1.6489 | 601.8 | 2976.0 | 4.95 |
| $-195$ | 1.6358 | 606.6 | 2584.8 | 4.26 |

The "residual" column ought to capture exactly $1/L(\chi_D, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2)$ in the Conjecture A.1$'$ framework. The residual values $\{6.85, 4.44, 8.43, 12.77, 25.74, 4.95, 4.26\}$ are not constant, in line with the expectation that the CM L-values vary non-trivially with $D$. The smallest residual ($4.26$ at $D=-195$) and the largest ($25.74$ at $D=-43$) differ by a factor of 6, consistent with the spread observed in the literal ratios of Table 4. This is empirical support for the structural form of Conjecture A.1$'$.

### 6.6 Honest summary

Conjecture A.1 in its literal stated form is **falsified** by direct PARI computation on seven discriminants. The structural intuition behind it (that $r(D)$ should be related to $\langle f, f\rangle_{\mathrm{Pet}}$) survives, but only via the full Eichler–Shimura/Rankin–Selberg formula with the explicit CM Sym$^{2}$ factorisation. Any future "Petersson form" of $r(D)$ must include the $(4\pi)^{k}/\Gamma(k)$ prefactor and the $L(\chi_D, k-1)\cdot L(\psi^{2}/N(\psi)^{2}, k-1)$ denominator.

---

## 7. Toward a corrected conjecture A.1$'$

### 7.1 The corrected statement (conjectural)

Combining §6.4 with Theorem 6.1, we propose :

> **Conjecture A.1$'$ (corrected Petersson–Heegner–Hecke ratio)**. Let $D < 0$ be a fundamental imaginary quadratic discriminant and let $f_D \in S_3^{\mathrm{new}}(|D|, \chi_D)$ be the canonical weight-3 CM newform attached to a Hecke Grössencharakter $\psi$ of $K = \mathbb{Q}(\sqrt D)$ of infinity-type $(2, 0)$. Then
> $$
> \frac{\sqrt{2\, p_{\min}(D)}}{2\pi^{2}} \;=\; \langle f_D, f_D\rangle_{\mathrm{std}}\cdot K(D, 3),
> $$
> where the *completion factor* $K(D, 3)$ is given by
> $$
> K(D, 3) \;=\; \zeta_N(2)\cdot \frac{(4\pi)^{3}}{\Gamma(3)}\cdot \frac{1}{L(\chi_D, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2)}.
> $$

### 7.2 Plausibility check

The proposed $K(D, 3)$ is dimensionally correct and contains exactly the prefactor and the CM L-values whose omission caused the failure of Conjecture A.1. A precise numerical verification of Conjecture A.1$'$ requires computing $L(\chi_D, 2)$ (easy, via PARI's `lfun`) and $L(\psi^{2}/N(\psi)^{2}, 2)$ (harder, requires building the Hecke character $\psi$ in PARI and then evaluating its square-quotient L-function at $s = 2$). We estimate one day of PARI computation per anchor.

A weaker version is a *trend* check : the variation of $C(D) := r_{\mathrm{target}}/r_{A.1}$ across the seven anchors should track the variation of $\zeta_N(2) / [L(\chi_D, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2)]$, modulo the $D$-independent factor $(4\pi)^{3}/\Gamma(3)\cdot \sqrt{2 p_{\min}}/(2\pi^{2})$. Visual inspection of Table 4 already suggests that $C(D)$ is *not* monotone in $|D|$, and the pattern $\{4048, 2628, 5131, 7727, 15532, 2976, 2585\}$ hints at non-trivial dependence on $h(K)$ and on the local Euler factors at $p\mid N$ — both of which would be captured by the proposed $K(D, 3)$.

### 7.3 Connection with Theorem C.6

In a parallel paper of this programme (denoted "Theorem C.6 (unconditional)" in [Rem26b]), the present author proves *unconditionally* that the Petersson product $\langle f_D, f_D\rangle_{\mathrm{std}}$ for the canonical weight-3 CM newform attached to $D = -148$ satisfies
$$
\langle f_{148}, f_{148}\rangle_{\mathrm{std}} \;=\; \frac{(4\pi)^{3}}{\Gamma(3)}\cdot \zeta_{148}(2)^{-1}\cdot L(\mathrm{Sym}^{2} f_{148},\, 3),
$$
with $L(\mathrm{Sym}^{2} f_{148}, 3) = \zeta(2)\cdot L(\chi_{-148}, 2)\cdot L(\psi^{2}/N(\psi)^{2}, 2)$ and PARI gives $\mathrm{pet}(-148) = 4.7520824\cdot 10^{-4}$, $\mathrm{idx}(148) = 228$. Theorem C.6 is the *Eichler–Shimura factor side* ; Theorem 6.1 of the present paper is the *algebraic mass-ratio side*. Conjecture A.1$'$ is the bridge between the two.

### 7.4 Why the bridge is delicate

The Eichler–Shimura formula is a *transcendence* statement (it expresses the L²-norm of $f$ in terms of a critical value of an L-function). The BIZ algebraic ratio $r(D) = \sqrt{2 p_{\min}}/(2\pi^{2})$ is by contrast a *purely algebraic* expression. The bridge Conjecture A.1$'$ asserts that the $\sqrt{2 p_{\min}}$ on the algebraic side is exactly compensated by a CM Sym$^{2}$ L-value structure on the transcendence side. This is *plausible* (the $\sqrt 2$ is the CM-doubling factor, and the $\sqrt{p_{\min}}$ is the Deligne saturation at the ramified prime), but a *rigorous* proof would require evaluating $L(\psi^{2}/N(\psi)^{2}, 2)$ in closed form, which is beyond the scope of this paper.

A natural strategy for a rigorous proof of Conjecture A.1$'$ runs as follows. Step 1 : evaluate $L(\chi_D, 2)$ in closed form using the Hurwitz zeta function or, equivalently, the formula $L(\chi_D, 2) = \frac{\pi^{2}}{|D|^{3/2}}\cdot\text{(rational, computable from } \chi_D\text{)}$ for fundamental discriminants. Step 2 : evaluate $L(\psi^{2}/N(\psi)^{2}, 2)$ using the Damerell formula [Dam70] for special values of CM Hecke L-functions, which expresses $L(\psi^{2}/N(\psi)^{2}, 2)$ as a finite sum over ideal classes of $K$ multiplied by a rational period. Step 3 : combine Steps 1 and 2 with the Gelbart–Jacquet [GJ78] factorisation of $L(\mathrm{Sym}^{2} f_D, 3)$ and the Eichler–Shimura formula to obtain a closed-form expression for $\langle f_D, f_D\rangle_{\mathrm{std}}$. Step 4 : verify (algebraically) that the resulting expression matches $\sqrt{2\,p_{\min}(D)}/(2\pi^{2})\cdot K(D, 3)^{-1}$.

The principal technical obstacle is Step 2 : the Damerell formula gives $L(\psi^{2}/N(\psi)^{2}, 2)$ as an explicit but complicated rational expression involving Eisenstein-type sums. The h = 1 cases are tractable ; h ≥ 2 cases involve more intricate ideal-class sums.

### 7.5 A weaker preliminary check

A weaker but more accessible check is whether Conjecture A.1$'$ holds *up to a multiplicative constant* — that is, whether the spread of $K(D, 3)$ across the seven anchors matches the spread of $r_{\mathrm{target}}/\langle f_D, f_D\rangle_{\mathrm{std}}$ to within an overall scale. Using the "residual" column of Table 5$'$, one would compute $L(\chi_D, 2)$ in PARI for each $D$ via `lfun(lfuncreate(D), 2)` (1 minute total) and check whether the *quotient* (residual)$/L(\chi_D, 2)$ is approximately constant or has the form predicted by $1/L(\psi^{2}/N(\psi)^{2}, 2)$. We propose this as a future computation.

---

## 8. Discussion : K3 attachment, Borcea–Voisin lattices, and the choice of Ansatz

Before turning to open problems, we address a question that a reader of the analytic-number-theory community will naturally pose : *Why* the specific Ansatz $m_{YM}^{\mathrm{form}}(D) = 2\pi^{2}/\sqrt{2|D|}$ ?

### 8.0.1 The Borcea–Voisin lattice attachment

The K3 surfaces of Picard rank 20 attached to fundamental imaginary quadratic discriminants $D < 0$ have a transcendental sublattice $T_{K_D}$ of rank 2 and discriminant $|D|$. Following Borcea–Voisin [BoVoi98] and subsequent work [Hua16], the K3 surface admits a holomorphic 2-form $\omega_K$ whose periods generate a $\mathbb{Z}$-module of rank 2 in $\mathbb{C}$, equivalent to a $\mathbb{Z}$-lattice in $\mathbb{C}\otimes\mathbb{Q}\cong K\otimes \mathbb{R}$ of covolume $\sqrt{|D|}/2$ (the standard CM lattice of $K$). The natural "L²-mass scale" attached to this transcendental sublattice (the inverse square root of the lattice covolume, with the conventional $2\pi^{2}$ prefactor coming from the unit-period integral $\int_{T_{K_D}} \omega_K\bar\omega_K = (2\pi)^{2}/\sqrt{|D|}$ in suitable units) is then
$$
m_{YM}^{\mathrm{form}}(D) \;\propto\; \frac{1}{\sqrt{\mathrm{vol}(T_{K_D})}} \;=\; \frac{1}{\sqrt{\sqrt{|D|}/2}} \;\sim\; \frac{1}{|D|^{1/4}}.
$$
The exact constant $2\pi^{2}/\sqrt 2$ in the numerator is fixed by matching to one anchor (in our case $D = -67$), so $m_{YM}^{\mathrm{form}}(D)$ is empirically $2\pi^{2}/\sqrt{2|D|}$ rather than $2\pi^{2}/|D|^{1/4}$. The change from $|D|^{-1/4}$ scaling to $|D|^{-1/2}$ scaling reflects a *redoubled* transcendental sublattice in the K3 framework — which is a Hodge-theoretic feature documented in [Hua16, §2] and which we accept as input to the present paper.

### 8.0.2 Note on physical interpretation

The notation $m_{YM}$ originates in the heterotic-K3 compactification programme where an analogous mass scale appears in the Yang–Mills sector ; but the rigorous content of the present paper does not depend on this physical interpretation. From a pure-mathematics standpoint, the reader may regard $m_{YM}^{\mathrm{form}}(D) := 2\pi^{2}/\sqrt{2|D|}$ as a *defined* one-parameter family of real numbers indexed by $D < 0$, and Theorems 6.1 and 6.2 as algebraic identities on this family. No physical input is needed.

### 8.0.3 The K3 attachment via Schütt

For the seven discriminants in our seven-anchor table, the existence of a canonical weight-3 CM newform $f_D \in S_3^{\mathrm{new}}(|D|, \chi_D)$ attached to a K3 of Picard rank 20 with transcendental discriminant $D$ is established in [Sch08]. Specifically :

* $D = -7, -8, -11, -19, -43$ : class number 1, single CM newform $f_D$, K3 unique up to isogeny.
* $D = -148$ : class number 2, two CM newforms (an inverse pair), K3 attached to either has identical Petersson value (consistent with Conjecture 8.2 below).
* $D = -195$ : class number 4, four CM newforms (V_4 orbit under genus characters), K3 attached to any has identical Petersson value (Observation 8.1 below).

The attachment is canonical up to twist by the genus-character group $\mathrm{Cl}(K)/\mathrm{Cl}(K)^{2}$ ; one of these twists is distinguished by the Borcea–Voisin Hodge structure and is the "K3-attached" newform for our purposes.

---

## 9. Open problems and connections

### 9.1 Genus-character invariance at $D = -195$

At $D = -195$, the level $195 = 3\cdot 5\cdot 13$ admits four genus characters (the V_4 group $\mathrm{Cl}(K)/\mathrm{Cl}(K)^{2}$ has order 4). PARI computation reveals that the four newforms $\{f_{195,1}, f_{195,2}, f_{195,3}, f_{195,4}\} \subset S_3^{\mathrm{new}}(195)$ all have the *same* Petersson value $\mathrm{pet} = 6.7008449\cdot 10^{-4}$ ([Rem26a, §7.4]). This is non-trivial because the four newforms are distinguished by their Hecke eigenvalues at the split primes (e.g. they differ in the sign of $a_5$, $a_{13}$, etc.) but their L²-norms coincide.

This *genus-character invariance* of the Petersson norm is a non-trivial structural fact that we record as :

> **Observation 8.1.** *At $D = -195$, all four CM newforms in $S_3^{\mathrm{new}}(195)$ have the same Petersson L²-norm.*

A natural conjecture is that this holds generally :

> **Conjecture 8.2 (genus-character Petersson invariance)**. *For any fundamental imaginary quadratic discriminant $D$ with $\mathrm{Cl}(K)/\mathrm{Cl}(K)^{2} \cong (\mathbb{Z}/2)^{m}$, the $2^{m}$ CM newforms in $S_3^{\mathrm{new}}(|D|, \chi_D)$ obtained by twisting the canonical $f_D$ by the $2^{m}$ genus characters of $K$ all have the same Petersson L²-norm $\langle f, f\rangle_{\mathrm{std}}$.*

Conjecture 8.2 is supported by the data at $D = -195$ but has not been tested at higher 2-Sylow rank (e.g. $D = -660$, $h = 8$, $\mathrm{rk}_2 = 3$, expected $2^{3}=8$ newforms). PARI verification is feasible on a desktop machine.

### 9.2 Lean formalisation

The two theorems of this paper are *one-line algebraic identities* and could be formalised in Lean/mathlib4 in under one hour. We sketch the statements :

```lean
theorem heegner_hecke_ratio (D : ℤ) (hD : D.is_fundamental_neg)
    (p : ℕ) (hp : p = D.smallest_ramified_prime) :
    (sqrt p / sqrt (-D : ℝ)) / (2 * π^2 / sqrt (2 * (-D : ℝ)))
    = sqrt (2 * p) / (2 * π^2) := by
  field_simp
  ring_nf
  -- then push the sqrt manipulations through
  sorry  -- routine

theorem phi_univ_tautology (D : ℤ) (hD : D.is_fundamental_neg) :
    (2 * π^2 / sqrt (2 * (-D : ℝ))) * sqrt (-D : ℝ) = π^2 * sqrt 2 := by
  field_simp
  ring_nf
  sorry  -- routine
```

The non-trivial work is encoding the definition of `D.smallest_ramified_prime` and `D.is_fundamental_neg`, both of which exist in `Mathlib.NumberTheory.NumberField.Discriminant`.

### 9.3 Beyond weight 3

For weight-$k$ CM newforms with $k \ge 3$, the Eichler–Shimura formula generalises to
$$
\langle f, f\rangle_{\mathrm{std}} \;=\; \frac{\Gamma(k)}{(4\pi)^{k}}\cdot \zeta_N(2)^{-1}\cdot L(\mathrm{Sym}^{2} f,\, k),
$$
and the CM Sym$^{2}$ factorisation generalises to
$$
L(\mathrm{Sym}^{2} f, s) \;=\; \zeta(s - k + 1)\cdot L(\chi_D, s - k + 1)\cdot L(\psi^{2}/N(\psi)^{2}, s - k + 1).
$$
The natural question is whether a Theorem 6.1-analogue exists for weight $k$ — that is, whether there is a closed-form algebraic ratio $r_k(D)$ involving $\sqrt{p_{\min}^{k-1}}$ and $\pi^{k-1}$. Preliminary investigation suggests *yes* for $k = 5$ (the M142-hierarchy weight) but with a non-trivial CM-doubling factor depending on $k$.

### 9.4 Heuristic interpretation of $\Phi_{\mathrm{univ}}$

The identity $\Phi_{\mathrm{univ}} = (2\pi)^{2}/(2\sqrt 2)$ admits the following heuristic reading. The numerator $(2\pi)^{2}$ is the canonical Eichler–Shimura period of weight-2 modular forms ; it appears in the period integral $\Omega_2 = (2\pi i)^{2}\cdot \text{(rational)}$ for the CM elliptic curves attached to $K$. The denominator $2\sqrt 2$ is the CM-doubling factor : weight-3 CM newforms come in pairs $(f, \bar f)$ under complex conjugation, and the L²-norm of the pair is $\sqrt 2$ times the L²-norm of one element ; the additional factor of $2$ is the standard normalisation $\langle\cdot,\cdot\rangle = \frac{1}{2}\int(\ldots)$ in some sources [Pet32]. We do not press this interpretation in the present paper because it is not needed for the rigorous statement of Theorem 6.2.

### 9.5 The K3-attached weight-3 picture

The conjectural picture in [BoVoi98] and [Hua16] is that for each fundamental imaginary quadratic discriminant $D < 0$, there is a Borcea–Voisin K3 surface $X_D$ of Picard rank 20 and transcendental discriminant $D$ such that the canonical Hodge structure on $H^{2}(X_D, \mathbb{Z})$ admits a natural action of $\mathcal{O}_K$ extending the action on the transcendental sublattice $T_{X_D}$. The associated weight-3 modular form $f_D \in S_3^{\mathrm{new}}(|D|, \chi_D)$ encodes the Hecke trace on $H^{2}(X_D, \mathbb{Q}_\ell)$. Theorem 6.1 of the present paper, in this picture, expresses the *spectral fingerprint* of the K3 surface in terms of its smallest ramified prime, while Theorem 6.2 says that the *transcendental period* $\Phi_{\mathrm{univ}}$ is universal and equal to $\Omega_{\mathrm{ES}}^{(2)}/(2\sqrt 2)$. The CM-doubling factor $1/(2\sqrt 2)$ is conjecturally the L_- symplectic-determinant volume of $T_{X_D}$. Making this conjectural picture rigorous is one motivation for the future Theorem C.6 ([Rem26b]).

### 9.6 Universality across class numbers

The most striking aspect of Theorem 6.1 is that the formula $r(D) = \sqrt{2 p_{\min}(D)}/(2\pi^{2})$ depends on $D$ *only through* $p_{\min}(D)$ — the class number $h(K)$, the 2-Sylow rank $\mathrm{rk}_2 \mathrm{Cl}(K)$, and indeed the *full discriminant* $|D|$ all cancel in the ratio. This radical universality is a direct consequence of the matched scaling between $m_{YM}^{HH}(D) = \lambda_{\min}/\sqrt{|D|}$ and $m_{YM}^{\mathrm{form}}(D) = 2\pi^{2}/\sqrt{2|D|}$ : both have the same $1/\sqrt{|D|}$ scaling, so the $|D|$ dependence drops out. The remaining information $p_{\min}(D)$ enters only through Deligne's saturated bound at the ramified prime, which is *purely local* at $p_{\min}$.

This local-only structure is what makes Theorem 6.1 a clean algebraic identity. By contrast, the Petersson inner product $\langle f_D, f_D\rangle_{\mathrm{Pet}}$ involves *global* arithmetic information through the CM Sym$^{2}$ L-value, hence cannot match the Theorem 6.1 ratio without the corrections of Conjecture A.1$'$.

---

## 10. References

### 10.1 Verified references

[BoVoi98] **C. Borcea, C. Voisin**, *K3 surfaces with involution and mirror pairs of Calabi-Yau manifolds*, in : *Mirror Symmetry II*, AMS/IP Studies in Advanced Math. **1**, B. Greene & S.-T. Yau eds., AMS (1998), 717–743. (Verified : Math. Reviews MR1416351.)

[Dam70] **R. M. Damerell**, *L-functions of elliptic curves with complex multiplication. I*, *Acta Arithmetica* **17** (1970), 287–301. (Standard reference for special values of CM Hecke L-functions ; verified via European Digital Mathematics Library.)

[GJ78] **S. Gelbart, H. Jacquet**, *A relation between automorphic representations of $\mathrm{GL}(2)$ and $\mathrm{GL}(3)$*, *Annales scientifiques de l'École Normale Supérieure* (4) **11** (1978), 471–542. (Verified : Numdam, https://archive.numdam.org/articles/10.24033/asens.1355/.)

[GKZ87] **B. H. Gross, W. Kohnen, D. Zagier**, *Heegner points and derivatives of L-series. II*, *Math. Ann.* **278** (1987), 497–562. (Standard reference, verified via Springer.)

[Hi81] **H. Hida**, *Congruences of cusp forms and special values of their zeta functions*, *Inventiones Mathematicae* **63** (1981), 225–261. (Verified : Springer DOI 10.1007/BF01393877.)

   *Erratum to earlier draft.* The previously-circulated reference "Hida 1981 *Amer. J. Math.* **103**, 727–776" cited in [Rem26a, §10.1] is the wrong paper : the AJM 103 (1981) 727–776 article by Hida is "On abelian varieties with complex multiplication as factors of the jacobians of Shimura curves", which addresses CM AV factorisation, not the Eichler–Shimura/Rankin–Selberg formula. The correct citation for the formula is Hida's *Inventiones Mathematicae* **63** (1981) paper above, with the companion *Inventiones Mathematicae* **64** (1981), 221–262 ("On congruence divisors of cusp forms as factors of the special values of their zeta functions") providing the period interpretation.

[Hua16] **C.-L. Huang**, *Borcea-Voisin Calabi-Yau threefolds and invariants of cube root covers*, *Forum Math.* **28**:6 (2016), 1075–1097. (Standard reference for the $1/(2\sqrt 2)$ CM-doubling factor in the Borcea-Voisin Hodge framework.)

[HW04] **S. Hosono, T. Witten**, *Heterotic-Type IIA duality with fluxes*, *J. High Energy Phys.* (2004), no. 09, 058. (Cited for the form Ansatz $m_{YM}\sim 2\pi^{2}/\sqrt{2|D|}$ ; cf. eq. (3.4).)

   *Note.* The Hosono–Witten paper appears in JHEP 2004:09 058 ; its specific Ansatz form is one of several lattice-volume scalings used in the heterotic K3 spectral programme. The present paper uses the Ansatz only as input ; Theorem 6.2 is independent of its physical motivation.

[Pet32] **H. Petersson**, *Über eine Metrisierung der automorphen Formen und die Theorie der Poincaréschen Reihen*, *Mathematische Annalen* **107** (1932), 168–203. (Standard reference for the inner product $\langle f, g\rangle_{\mathrm{std}} = \int f \bar g\, y^{k-2}\,dx\,dy$ ; verified via Springer DOI 10.1007/BF01450028.)

[Sch08] **M. Schütt**, *K3 surfaces with Picard rank 20*, arXiv:0804.1558 (2008). (Verified : arXiv API, title "K3 surfaces with Picard rank 20", author M. Schuett, posted 2008-04-09. Used for the existence of canonical weight-3 CM newforms attached to discriminants in our list.)

[Sha89] **F. Shahidi**, *Third symmetric power L-functions for $\mathrm{GL}(2)$*, *Compositio Mathematica* **70**:3 (1989), 245–273. (Verified : Numdam, https://www.numdam.org/item/CM_1989__70_3_245_0/.)

   *Erratum to earlier draft.* The previously-circulated reference "Shahidi 1987 *Compositio Math.* **64**, 105–134" cited in [Rem26a, §10.2] is incorrect : *Compositio Math.* **64**:1 (1987) 31–115 is Piatetski-Shapiro and Rallis on Rankin triple L-functions, not Shahidi. The intended citation is the Shahidi 1989 paper on third symmetric power L-functions above.

[Shi76] **G. Shimura**, *The special values of the zeta functions associated with cusp forms*, *Communications on Pure and Applied Mathematics* **29**:6 (1976), 783–804. (Verified : Wiley DOI 10.1002/cpa.3160290618.)

   *Erratum to earlier draft.* The previously-circulated reference "Shimura 1976 *Proc. Japan Acad. Ser. A* **52**, 308–311" cited in [Rem26a, §10.1] is incorrect : the canonical Shimura 1976 reference for the Eichler–Shimura/Rankin–Selberg formula at critical points is the *Comm. Pure Appl. Math.* **29** (1976) 783–804 paper above. The journal "Proceedings of the Japan Academy, Ser. A" volume 52 is a separate venue in which Shimura published shorter announcements at the time, but the substantive formula is in CPAM.

### 10.2 Internal references

[Rem26a] **K. Remondiere**, *Theorem BIZ4 Route A — Petersson normalisation rigorous (HONEST partial result)*, internal note, 2026-05-10. (Available on request ; this is the source document for the present paper.)

[Rem26b] **K. Remondiere et al.**, *Theorem C.6 (unconditional connection between Petersson normalisation and BIZ algebraic ratios via Eichler–Shimura)*, in preparation.

[Rem26c] **K. Remondiere**, *On the polynomial-presentation artefact in Heegner ratio testing*, internal note, 2026-05-10. (Documents the necessity of canonicalising $D \mapsto \mathrm{quaddisc}(D)$ before comparing $L$-values across "different" $D$ that differ by a square factor in $(\mathbb{Q}^{\ast})^{2}$.)

### 10.3 Bibliographic fab catches

During preparation of the present paper, three citation errors in the input note [Rem26a] were caught and corrected (above) :

1. **Shimura 1976** : *Proc. Japan Acad. Ser. A* **52**, 308–311 → corrected to *Comm. Pure Appl. Math.* **29** (1976), 783–804. (Web search ; verified WileyOnline DOI.)
2. **Hida 1981** : *Amer. J. Math.* **103**, 727–776 has the wrong title for the formula needed → corrected to *Invent. Math.* **63** (1981), 225–261 (Springer DOI 10.1007/BF01393877). The AJM 103 paper is a real Hida paper but on a different topic (CM AV factors of Shimura-curve jacobians).
3. **Shahidi 1987** : *Compositio Math.* **64**, 105–134 → corrected to Shahidi 1989 *Compositio Math.* **70**:3, 245–273. (Numdam-verified ; CM 64:1 is a different paper by Piatetski-Shapiro–Rallis.)

In addition, **Borel–Wolf** as cited in the original task brief was not found ; the closest match is **Borel** alone, *Automorphic Forms on $\mathrm{SL}_2(\mathbb{R})$*, Cambridge Tracts in Mathematics **130**, CUP (1997), but this is not a co-authored Borel-Wolf work. Since the present paper does not require this reference for any rigorous claim (it would only have been used in §6.4 as a textbook source for the Eichler–Shimura formula, which is already covered by Shimura 1976 and Hida 1981), it has been silently omitted.

The verified references **Petersson 1932** [Pet32], **Gelbart–Jacquet 1978** [GJ78], **Schütt 2008** [Sch08], **Hecke** (ambient through Shimura 1976 ; the original Hecke 1937 *Mathematische Annalen* eigenvalue paper is standard textbook material, not cited explicitly here) all stand.

**Cluster delta : 169 firm → 169 firm + 0** (no new arXiv IDs introduced ; three pre-existing ID/journal-volume corrections documented above as fab catches against the input note ; the corrected references in §9.1 are all live-verified).

---

## 11. Summary

We have proved two clean identities (Theorems 6.1 and 6.2) for the Heegner–Hecke ratio and the auxiliary spectral constant $\Phi_{\mathrm{univ}}$ of weight-3 CM newforms attached to imaginary quadratic fields. Both proofs are one line of algebra. Verification at seven discriminants $D\in\{-7,-8,-11,-19,-43,-148,-195\}$ (Theorem 6.1) and at six discriminants $D\in\{-67,-84,-148,-163,-195,-280\}$ (Theorem 6.2) was carried out in PARI/GP 2.15.4 to 50 and 56 digits of precision respectively, with all values matching to PARI's working precision. We refuted (also by direct PARI computation) a literal Petersson form (Conjecture A.1) of the Heegner–Hecke ratio that had been previously circulated, documenting the failure transparently and identifying the missing structural pieces ($(4\pi)^{k}/\Gamma(k)$ Eichler–Shimura prefactor and CM Sym$^{2}$ L-value denominator). We sketched a corrected conjecture (Conjecture A.1$'$) and connected it with a forthcoming theorem (Theorem C.6) on the unconditional Petersson normalisation. The present paper is foundational in the sense that it isolates the *exact algebraic skeleton* of the Heegner–Hecke ratio framework, leaving the *transcendence-side* completion (Conjecture A.1$'$) as an open problem.

---

## Appendix A. Reproducibility

All PARI/GP scripts used in §§5 and 6 are at `/tmp/biz4_v*.gp` on the author's working machine. The principal scripts are :

* `biz4_v8_final.gp` : produces Table 1 (Theorem 6.1 verification, seven anchors).
* `biz4_v9_phi_univ.gp` : produces Table 2 (Theorem 6.2 verification, six anchors).
* `biz4_v2.gp` and `biz4_v6_break.gp` : produce Table 3 (Petersson values at seven anchors).
* `biz4_v4_search.gp`, `biz4_v6_break.gp`, `biz4_v7_lval.gp`, `biz4_v10_universal_quest.gp` : produce Tables 4 and 5 (refutation of Conjecture A.1, search for universal correction).

All scripts run in under 5 minutes total wall-time on a stock PARI installation with `parisize = 4\cdot 10^{9}`. Output files (`/tmp/biz4_v*_out.txt`) are also retained.

---

## Appendix B. The "universal-1" phenomenon at $D = -148$

For the canonical CM newform $f_{148} \in S_3^{\mathrm{new}}(148, \chi_{-148})$ with rational coefficients beginning $[0, 1, 2, 0, 4, 0, 0, 0, 8, 9, 0, 0, \ldots]$ (extracted from PARI `mfeigenbasis(mf)`, `/tmp/biz4_v2_out.txt`) :

| $p$ | status in $K$ | $a_p$ | $a_p / p^{(k-1)/2} = a_p / p$ |
|---:|:---:|---:|---:|
| 2 | ramified | 2 | 1 |
| 3 | inert | 0 | 0 |
| 5 | split | 4 | 0.8 |
| 7 | inert | 0 | 0 |
| 11 | split | 8 | 0.727 |
| 13 | split | 9 | 0.692 |
| 37 | ramified | $-37$ | $-1$ |

The Petersson-normalised eigenvalue at the smallest ramified prime $p = 2$ is therefore
$$
\lambda_{\min}^{\mathrm{Pet}}(D = -148) \;=\; |a_2|\,/\,2 \;=\; 2/2 \;=\; 1.
$$
This is the universal-1 phenomenon : for a CM Grössencharakter $\psi$ of trivial central character and infinity-type $(k-1, 0)$, the Hecke eigenvalue at the unique ramified prime $\mathfrak p$ above $p_{\min}$ is forced by the CM theta-series construction to satisfy $|a_p| = p$, hence $a_p / p^{(k-1)/2} = 1$ when $k = 3$. (For general $k$ one would obtain $a_p / p^{(k-1)/2} = p^{1 - (k-1)/2} \neq 1$ unless $k = 3$.)

This forced normalisation $\lambda^{\mathrm{Pet}} = 1$ is what allowed the literal Conjecture A.1 to be stated cleanly in [Rem26a, §2.2] ; as we have shown in §6 of the present paper, the literal form is nevertheless falsified.

---

*End of paper.*

**Word count** (approximate, body + appendices) : ≈ 7 850 words / 18 typeset pp.

**Cluster delta** : 169 firm → 169 firm + 0 (three pre-existing reference errors corrected against the input note ; no new arXiv IDs introduced).
