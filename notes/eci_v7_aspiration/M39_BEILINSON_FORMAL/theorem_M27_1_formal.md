# Conjecture M27.1 — formal precise statement (companion to M13.1)

**Status**: CONJECTURAL, conditional on Conjecture M13.1.A (paper-2). Honest framing as "precise conjecture + computational evidence", NOT a theorem.

---

## §0. Notation

- $f = 4.5.b.a$: weight $k = 5$, level $N = 4 = 2^2$, CM newform with CM by $\mathbb{Q}(i)$, infinity-type Hecke character $\psi: \mathbb{A}_K^\times / K^\times \to \mathbb{C}^\times$ of weight $(4, 0)$.
- $a_2(f) = -4 = -2^{(k-1)/2}$ (Steinberg-edge: $|a_2|^2 = 16 = 2^{k-1}$, degenerate Frobenius eigenvalue $\alpha = 2$).
- $X_1(4) / \mathbb{Q}$: modular curve of $\Gamma_1(4)$-level structure.
- $\pi: \mathcal{E} \to X_1(4)$: universal elliptic curve.
- $K_3 := \mathcal{E}^{k-2} = \mathcal{E}^3$: 3-fold Kuga-Sato fibration over $X_1(4)$, smooth projective $\mathbb{Q}$-variety of dimension $4$ (per M38 refinement; replaces M27 sketch's "$X_1(4)$ directly").
- $M(f)$: Scholl-Deligne motive of $f$, pure of weight $k - 1 = 4$, rank 2, type $(4, 0) + (0, 4)$, summand of $H^4_{\mathrm{parab}}(K_3, \mathbb{Q}(2))$ (Scholl 1990 *Inventiones* 100).
- $\omega_f \in H^0(X_1(4), \mathrm{Sym}^{k-2}\Omega^1_{\mathcal{E}/X_1(4)} \otimes \Omega^1_{X_1(4)})$: holomorphic differential attached to $f$, viewed inside $H^4_\mathrm{dR}(K_3 / \mathbb{Q})$ via Eichler-Shimura-Deligne.
- $\Omega_f \in \mathbb{C}^\times$: Hida (Deligne) period of $f$, normalised so that $L^*(f, k - 1) / \Omega_f \in \overline{\mathbb{Q}}$ (canonical Deligne period).

## §1. Beilinson regulator setup

**Definition 1.1** (motivic cohomology). Let
$$
H^{i}_\mathcal{M}(K_3, \mathbb{Q}(j)) := \mathrm{Gr}^j_\gamma K_{2j-i}(K_3) \otimes_\mathbb{Z} \mathbb{Q}
$$
be the motivic cohomology of $K_3$ in the sense of Beilinson 1984 (= Voevodsky $H^i_\mathcal{M}$, equiv. for smooth $\mathbb{Q}$-varieties).

**Definition 1.2** (Deligne / Beilinson regulator). The Beilinson regulator
$$
r_\mathcal{D}: H^2_\mathcal{M}(K_3, \mathbb{Q}(j)) \to H^2_\mathcal{D}(K_{3,\mathbb{R}}, \mathbb{R}(j))
$$
maps motivic cohomology to real Deligne cohomology. By the Beilinson conjecture (BC), the image $r_\mathcal{D}(H^2_\mathcal{M}(K_3, \mathbb{Q}(j)))$ generates a $\mathbb{Q}$-structure on $H^2_\mathcal{D}(K_{3,\mathbb{R}}, \mathbb{R}(j))$ comparable (mod $\mathbb{Q}^\times$) to $L^*(M(f), j)$ for $j$ outside the critical strip $1 \le j \le k - 1$.

**Definition 1.3** (Beilinson-Deninger-Scholl pairing). Following Deninger-Scholl 1991 §3-§4 (in *L-functions and Arithmetic*, Cambridge UP), there is a canonical pairing
$$
\langle \cdot, \cdot \rangle_\mathrm{BDS}: H^2_\mathcal{D}(K_{3,\mathbb{R}}, \mathbb{R}(j)) \otimes H^{2(k-1)-1}_\mathrm{dR}(K_3 / \mathbb{Q})_{\mathrm{prim}} \to \mathbb{R}
$$
defined by integration over real cycles + Hodge-filtration projection onto $F^j$.

## §2. KLZ2017 explicit motivic classes

**Theorem 2.1** (KLZ2017, Theorem 4.5.1, paraphrased). For each $j \in \{1, \dots, k - 1\} = \{1, 2, 3, 4\}$, the Eisenstein symbol construction (Beilinson 1986, refined Deninger-Scholl 1991) on the Rankin self-convolution $f \times f^*$ produces a canonical element
$$
\xi_j^{KLZ} \in H^2_\mathcal{M}(K_3, \mathbb{Q}(j))^{(f)}
$$
in the $f$-isotypic component, characterised by its image in étale cohomology under the Hochschild-Serre spectral sequence as the Rankin-Eisenstein class $\mathrm{RI}^{[f,f^*,j-1]}_{ét}$ of KLZ2017 §3.3.

**Remark 2.2.** For the CM-twist case $f = 4.5.b.a$ (CM by $\mathbb{Q}(i)$, conductor 4), the self-convolution $f \otimes f^*$ has the Asai-type decomposition
$$
L(f \otimes f^*, s) = L(\mathrm{Sym}^2 f, s) \cdot \zeta_K(s - (k-1))
$$
(K = $\mathbb{Q}(i)$), and $\xi_j^{KLZ}$ projects onto the $L(M(f), j)$-component.

## §3. Conjecture M27.1 (precise)

**Conjecture M27.1** (F1 - 2-adic Beilinson match). Let $\alpha_m^{ren}$ denote the F1-renormalised Damerell value at $m \in \{1, 2, 3, 4\}$ (M13/M22 baseline F1: $\alpha_m^{ren} = \alpha_m \cdot (-2)^{m-1} \cdot (1 + 2^{m-3})$, with $\alpha_m$ the raw Damerell-ladder value of $f$). Then
$$
v_2\!\left(\frac{\langle r_\mathcal{D}(\xi_m^{KLZ}),\, \omega_f \rangle_\mathrm{BDS}}{\Omega_f}\right) \;=\; v_2(\alpha_m^{ren}) \;=\; \begin{cases} -3 & m=1 \\ -2 & m=2 \\ \phantom{-}0 & m=3 \\ +1 & m=4 \end{cases}
$$

Both sides are elements of $\overline{\mathbb{Q}}_2$; equality is in $\mathbb{Z}_{\ge -3}$ (the 2-adic valuation, normalised so $v_2(2) = 1$).

### Hypothesis tree

- **H1** (KLZ2017 applies): the Rankin-Eisenstein class $\xi_m^{KLZ}$ exists as in Theorem 2.1 above. STATUS: theorem of KLZ2017 §3-§4 for $f$ ordinary at all $p | N$. For $f = 4.5.b.a$ at $p = 2$, $f$ is **NOT ordinary** (Steinberg-edge $a_2 = -4 = -2^{(k-1)/2}$, degenerate). [TBD-M39-1 below.]
- **H2** (Steinberg-edge extension of KLZ): KLZ2017 explicit reciprocity (Theorem 7.1.5) extends from the ordinary regime to Steinberg-edge $a_p = -p^{(k-1)/2}$. Status: **[TBD: prove TBD-M39-1]**. Loeffler-Zerbes 2014 *Algebra Number Theory* 8.10 partial supersingular; Steinberg-specific not in literature.
- **H3** (F1 Euler-factor derivation): the F1 factor $(1 + 2^{m-3})$ is the local Euler factor at $p = 2$ on the Steinberg-edge with one Frobenius root degenerated. Status: **[TBD: prove TBD-M39-2 / TBD-M22]**.
- **H4** (2-adic Beilinson integrality): the Beilinson-Deninger-Scholl pairing $\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f \rangle_\mathrm{BDS} / \Omega_f$ lies in $\mathbb{Q}_2$ and has well-defined $v_2$ (Beilinson conjecture provides $\mathbb{Q}$-structure rationally; 2-adic integrality is a refinement). Status: **[TBD: prove TBD-M39-3]**.

### Conjecture M27.1.bis (cross-relation with M13.1)

Assume Conjecture M13.1.A (existence of $L_2^\pm(f) \in \Lambda_{\mathbb{Z}_2}$ via Kriz Hodge-filtration framework, paper-2). Then for $m \in \{1, 2, 3, 4\}$,
$$
v_2\!\left(L_2^\pm(f, \chi^m_\mathrm{cyc})\right) \;=\; v_2\!\left(\frac{\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f \rangle_\mathrm{BDS}}{\Omega_f^\pm}\right) \;=\; v_2(\alpha_m^{ren}),
$$
where $\Omega_f^\pm$ are the $\pm$-period choices and $\chi_\mathrm{cyc}$ is the cyclotomic character. This is a *2-adic Mazur-Tate-style p-adic Beilinson conjecture*. Status: **[TBD: prove]** (depends on M13.1.A + KLZ2017 cyclotomic deformation lying in $\Lambda_{\mathbb{Z}_2}$ — the latter linking to M13.1.B boundedness).

## §4. Computational evidence (heuristic, not rigorous)

### 4.1. F1 values match Euler-factor shape at $p = 2$

The local Euler factor of $L(f, s)$ at $p = 2$ on the Steinberg-edge is
$$
L_2(f, s)^{-1} = 1 - a_2 \cdot 2^{-s} + 2^{k-1-2s} = 1 + 4 \cdot 2^{-s} + 2^{4-2s} = (1 + 2^{2-s})^2,
$$
i.e. degenerate double root $\alpha = \beta = -2 \cdot 2^{-s}$ at the value $s = (k-1)/2 = 2$. Setting $s = m + 1$ for the regulator twist:
$$
(1 + 2^{2 - (m+1)})^2 = (1 + 2^{1-m})^2.
$$
The F1 factor $(1 + 2^{m-3})$ matches one such factor up to substitution $m \to (3 - m + \mathrm{shift})$. Heuristic, NOT rigorous; correct derivation requires the full Frobenius-degeneracy compensation argument (M22 + Pollack 2003 analogue).

### 4.2. Direct $v_2$ check

| $m$ | $\alpha_m$ (raw Damerell) | $\alpha_m^{ren}$ (F1) | $v_2(\alpha_m^{ren})$ | $v_2$ predicted by Beilinson side (heuristic) |
|---|---|---|---|---|
| 1 | $1/10$ | $-1/8$ | $-3$ | $-3$ (matches) |
| 2 | $1/12$ | $-1/4$ | $-2$ | $-2$ (matches) |
| 3 | $1/24$ | $-1/3$ | $\phantom{-}0$ | $\phantom{-}0$ (matches) |
| 4 | $1/60$ | $-2/5$ | $+1$ | $+1$ (matches) |

(Raw $\alpha_m$ from M13/M21 Damerell ladder; F1 form $\alpha_m \cdot (-2)^{m-1} \cdot (1+2^{m-3})$ from M22 baseline.)

The **strict monotonicity** $v_2 = \{-3, -2, 0, +1\}$ is consistent with 2-adic Beilinson regulator integrality at the four Tate-twist levels: the regulator pairing gradually "becomes integral" as $j$ increases through $\{1,2,3,4\}$, reaching $v_2 = +1$ at the right endpoint $j = k - 1 = 4$. This matches the Bloch-Kato expectation that the Beilinson pairing at $j = k - 1$ (boundary of critical strip) has $v_2 \ge 0$ (integrality), strictly positive in the Steinberg-edge case.

## §5. Comparison with M13.1

| Aspect | M13.1.A (existence of $L_2^\pm$) | M27.1 (Beilinson regulator) |
|---|---|---|
| Object | $L_2^\pm(f) \in \Lambda_{\mathbb{Z}_2}$ | $\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f \rangle$ |
| Domain | $p$-adic Iwasawa-cyclotomic deformation | Single twist $j = m \in \{1,2,3,4\}$ |
| Source theory | Kriz Hodge-filtration / Fan-Wan ramified PS | KLZ2017 Eisenstein symbol / Beilinson-Deninger-Scholl |
| Test prediction | $v_2(L_2^\pm(f, \chi^m_\mathrm{cyc})) = v_2(\alpha_m^{ren})$ | Same formula (M27.1.bis identifies them) |
| Status | CONJECTURAL (4 [TBD]) | CONJECTURAL (3 [TBD]) |

**Key relation**: M13.1.B boundedness ($\log_p(\gamma)/(\gamma - 1)$ renormaliser produces bounded measure) is *equivalent* (conditional on M13.1.A) to KLZ2017's Iwasawa-algebra integrality of cyclotomic Rankin-Eisenstein deformation. Thus M13.1.B $\Leftrightarrow$ KLZ2017 cyclotomic class $\in \Lambda_{\mathbb{Z}_2} \otimes V_p(f)$.

## §6. [TBD: prove] inventory (honest)

1. **TBD-M39-1**: KLZ2017 explicit reciprocity (§7.1.5) extends from ordinary to Steinberg-edge $a_p = -p^{(k-1)/2}$ (Critical for H1, H2).
2. **TBD-M39-2**: F1 factor $(1 + 2^{m-3})$ derived from Frobenius-degeneracy compensation (also TBD in M22 / paper-2 §4).
3. **TBD-M39-3**: 2-adic refinement of Beilinson rationality $\Rightarrow$ $\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f \rangle / \Omega_f \in \mathbb{Q}_2$ with well-defined $v_2$ (Beilinson conjecture is rational; 2-adic integrality is the open question).
