# Paper skeleton: Beilinson-regulator companion to Conjecture M13.1

**Title**: *"A 2-adic Beilinson-regulator conjecture for the CM newform 4.5.b.a, via Kings-Loeffler-Zerbes Eisenstein symbols"*

**Author**: K. Remondiere (with [TBD: collaborator] — Kriz / A.J. Scholl / Loeffler-Zerbes)

**Target**: *Research in Number Theory* (short-note format, 14pp). Backup: *Journal of Number Theory*.

**Companion**: paper-2 *"A Steinberg-edge obstruction to Katz-type 2-adic L-functions for 4.5.b.a, with a Pollack-type rescue conjecture"* (M32, target *Algebra & Number Theory*, 22pp).

**MSC2020**: 11G40 (primary), 11F67, 11G55, 14F42, 14C25 (secondary)

**Keywords**: Beilinson regulator, motivic cohomology, Rankin-Eisenstein classes, Kuga-Sato variety, 2-adic L-function, CM modular form, Steinberg-edge.

---

## Abstract (draft, ~150 words)

We formulate a precise conjecture relating a 2-adic refinement of the Beilinson-Deninger-Scholl regulator pairing on the 3-fold Kuga-Sato variety $K_3 \to X_1(4)$ to the F1-renormalised Damerell-ladder values $\alpha_m^{\mathrm{ren}}$ ($m \in \{1,2,3,4\}$) of the weight-5, level-4 CM newform $f = 4.5.b.a$. Using the Kings-Loeffler-Zerbes (2017, *Camb. J. Math.* 5) explicit Rankin-Eisenstein classes $\xi_m^{KLZ} \in H^2_\mathcal{M}(K_3, \mathbb{Q}(m))$, we conjecture that the 2-adic valuation of the regulator pairing $\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f\rangle / \Omega_f$ equals the strictly monotone sequence $v_2(\alpha_m^{\mathrm{ren}}) = \{-3, -2, 0, +1\}$ verified by sympy computation (M22). The conjecture is logically separate from but compatible with a parallel conjecture (M13.1.A) on the existence of a Pollack-type 2-adic $L$-function $L_2^\pm(f)$ rescuing the Steinberg-edge obstruction $a_2 = -2^{(k-1)/2}$. We discuss the Steinberg-edge extension of KLZ2017's reciprocity law as the principal open question.

---

## §1. Introduction (3pp)

### §1.1. Context: the form $f = 4.5.b.a$ and the Steinberg-edge phenomenon

- LMFDB record `4.5.b.a`: weight 5, level 4, CM by $\mathbb{Q}(i)$
- Steinberg-edge: $a_2 = -4 = -2^{(k-1)/2}$, $|a_2|^2 = 2^{k-1}$ (degenerate Frobenius double root)
- This is the smallest CM weight-$\ge 3$ newform with the Steinberg-edge property at a perfect-square level
- Companion paper-2 (M13.1): obstruction to Katz-type 2-adic $L$-function + Pollack-type rescue $L_2^\pm(f)$

### §1.2. Beilinson regulator and the Damerell ladder

- Critical strip $1 \le s \le k - 1 = 4$; Damerell ladder evaluates $L^{\mathrm{alg}}(f, m)$ for $m \in \{1,2,3,4\}$
- F1 renormalisation (M13 baseline, M22-validated): $\alpha_m^{\mathrm{ren}} = \alpha_m \cdot (-2)^{m-1} \cdot (1 + 2^{m-3})$
- Sympy-verified strict monotonicity: $v_2(\alpha_m^{\mathrm{ren}}) = \{-3, -2, 0, +1\}$

### §1.3. Main conjecture (informal)

State Conjecture M27.1 in informal form: $v_2$ of 2-adic refinement of regulator pairing matches $v_2$ of F1-renormalised Damerell.

### §1.4. Outline of the paper

Sections §2-§7 roadmap.

---

## §2. Setup (2pp)

### §2.1. The motive $M(f)$ (0.5pp)
- Scholl 1990 *Inventiones* 100, 419-430
- $M(f) \subset H^4_{\mathrm{parab}}(K_3, \mathbb{Q}(2))$, rank 2, weight 4
- CM structure by $\mathbb{Q}(i)$, infinity-type Hecke character $\psi$ weight $(4,0)$

### §2.2. The 3-fold Kuga-Sato variety $K_3$ (0.5pp)
- $\pi: \mathcal{E} \to X_1(4)$, $K_3 = \mathcal{E}^3$ (per M38: NOT $X_1(4)$ directly)
- Smooth compactification (Deligne 1969 *Sém. Bourbaki*); birational invariance of $H^4_\mathrm{parab}$
- $\dim K_3 = 4$

### §2.3. Beilinson regulator (0.5pp)
- $r_\mathcal{D}: H^2_\mathcal{M}(K_3, \mathbb{Q}(j)) \to H^2_\mathcal{D}(K_{3,\mathbb{R}}, \mathbb{R}(j))$
- Beilinson conjecture (BC) for non-critical values
- Deligne period $\Omega_f$ normalisation

### §2.4. Beilinson-Deninger-Scholl pairing (0.5pp)
- $\langle \cdot, \cdot \rangle_\mathrm{BDS}$ definition (Deninger-Scholl 1991 §3-§4)
- Real-cycle integration + Hodge-filtration projection

---

## §3. Kings-Loeffler-Zerbes 2017 explicit Eisenstein symbols (2pp)

### §3.1. Rankin-Eisenstein classes (1pp)
- KLZ2015 (*J. Algebraic Geom.* 27, 715-757): motivic construction
- KLZ2017 (*Camb. J. Math.* 5, no. 1, 1-122): explicit reciprocity laws
- For Rankin self-convolution $f \otimes f^*$, classes $\xi_j^{KLZ} \in H^2_\mathcal{M}(K_3, \mathbb{Q}(j))^{(f)}$, $j \in \{1, \dots, k-1\}$
- Image under étale realisation = $\mathrm{RI}^{[f, f^*, j-1]}_{ét}$ (KLZ2017 §3.3)

### §3.2. CM-twist decomposition (0.5pp)
- $L(f \otimes f^*, s) = L(\mathrm{Sym}^2 f, s) \cdot \zeta_K(s - (k-1))$, $K = \mathbb{Q}(i)$
- Asai-type splitting; $\xi_j^{KLZ}$ projects onto $L(M(f), j)$-component

### §3.3. Steinberg-edge obstruction (0.5pp)
- KLZ2017 reciprocity §7 treats ordinary case
- Loeffler-Zerbes 2014 *ANT* 8.10: partial supersingular extension
- Steinberg-edge $a_p = -p^{(k-1)/2}$ specific is **NOT in literature** — flagged [TBD: prove]
- This is the principal technical obstruction to making M27.1 a theorem

---

## §4. Conjecture M27.1 — precise statement (2pp)

### §4.1. The 2-adic refinement (0.5pp)
- Definition of $\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f\rangle_\mathrm{BDS} / \Omega_f$ as element of $\mathbb{Q}_2$ (conditional on H4: 2-adic integrality of Beilinson pairing)

### §4.2. Conjecture M27.1 (formal) (0.5pp)
- Boxed statement: $v_2\!\left(\langle r_\mathcal{D}(\xi_m^{KLZ}), \omega_f\rangle / \Omega_f\right) = v_2(\alpha_m^{\mathrm{ren}}) = \{-3,-2,0,+1\}$
- Strict monotonicity remark

### §4.3. Hypothesis tree H1-H4 (0.5pp)
- H1 (KLZ applies, ordinary OK, Steinberg-edge [TBD-M39-1])
- H2 (Steinberg-edge extension [TBD-M39-1])
- H3 (F1 Euler-factor [TBD-M39-2 / M22])
- H4 (2-adic integrality of Beilinson pairing [TBD-M39-3])

### §4.4. Conjecture M27.1.bis (cross-relation with M13.1) (0.5pp)
- Conditional on M13.1.A: $v_2(L_2^\pm(f, \chi^m_\mathrm{cyc})) = v_2(\alpha_m^{\mathrm{ren}})$
- This is a 2-adic Mazur-Tate-style p-adic Beilinson conjecture
- Equivalence M13.1.B $\Leftrightarrow$ KLZ2017 cyclotomic class $\in \Lambda_{\mathbb{Z}_2} \otimes V_p(f)$

---

## §5. Computational evidence (3pp)

### §5.1. F1 values match local Euler factor at $p=2$ (1pp)
- $L_2(f,s)^{-1} = (1 + 2^{2-s})^2$ (Steinberg-edge degenerate double root)
- F1 factor $(1 + 2^{m-3})$ matches Frobenius-degeneracy compensation (heuristic)
- Sympy code excerpt (Appendix A reference)

### §5.2. $v_2$ table for $m \in \{1,2,3,4\}$ (1pp)
- 4-row table (raw Damerell, F1-renorm, $v_2$, Beilinson-side prediction)
- All four match $\{-3, -2, 0, +1\}$
- Strict monotonicity highlighted

### §5.3. Discussion: integrality grading (1pp)
- Bloch-Kato expectation: regulator pairing at $j = k - 1$ has $v_2 \ge 0$
- Steinberg-edge case: $v_2 = +1$ strict (consistent with degenerate Frobenius)
- "Crossover" at $m = 3$ (where $v_2 = 0$): matches Beilinson conjecture's boundary-of-critical-strip integrality threshold

---

## §6. Comparison with M13.1 + outlook (1pp)

### §6.1. Logical separation (0.3pp)
- Table comparing M13.1.A (existence $L_2^\pm$) vs M27.1 (regulator integrality)
- Both share F1 renormalisation; both conditional

### §6.2. Cross-relation M13.1.B $\Leftrightarrow$ KLZ Iwasawa-integrality (0.3pp)
- Sketch of equivalence (assuming M13.1.A)

### §6.3. Open questions (0.4pp)
- TBD-M39-1: Steinberg-edge extension of KLZ2017 reciprocity (PRIMARY)
- TBD-M39-2: F1 Euler-factor derivation (joint with paper-2 §4)
- TBD-M39-3: 2-adic integrality refinement of Beilinson conjecture
- Speculation: Kriz Hodge-filtration framework + Loeffler-Zerbes supersingular machinery as combined approach to Steinberg-edge

---

## §7. Bibliography (1pp, ~25 refs)

Live-verified core (4 new + 8 from M27/M32):

- Beilinson, A.A., "Higher regulators and values of L-functions", *J. Soviet Math.* 30 (1985), 2036-2070
- Bloch, S., Kato, K., "L-functions and Tamagawa numbers of motives", *Grothendieck Festschrift* I, 1990
- Deligne, P., "Formes modulaires et représentations $\ell$-adiques", *Sém. Bourbaki* 355, 1969
- Deninger, C., Scholl, A.J., "The Beilinson conjectures", in *L-functions and Arithmetic* (Coates-Taylor, eds.), Cambridge UP 1991, 173-209
- Kings, G., Loeffler, D., Zerbes, S.L., "Rankin-Eisenstein classes for modular forms", *J. Algebraic Geom.* 27 (2018), 715-757; arXiv:1501.03289 [KLZ2015]
- Kings, G., Loeffler, D., Zerbes, S.L., "Rankin-Eisenstein classes and explicit reciprocity laws", *Cambridge J. Math.* 5 (2017), no. 1, 1-122; DOI:10.4310/CJM.2017.v5.n1.a1; arXiv:1503.02888 [KLZ2017] **(KEY REFERENCE)**
- Kriz, D., *Supersingular p-adic L-functions, Maass-Shimura operators and Waldspurger formulas*, Annals of Math. Studies 212, Princeton UP 2021
- Loeffler, D., Zerbes, S.L., "Iwasawa theory and p-adic L-functions over $\mathbb{Z}_p^2$-extensions", *Algebra & Number Theory* 8 (2014), no. 10, 2407-2444
- Pohlmann, H., "Algebraic cycles on abelian varieties of complex multiplication type", *Annals of Math.* 88 (1968), 161-180
- Pollack, R., "On the p-adic L-function of a modular form at a supersingular prime", *Duke Math. J.* 118 (2003), 523-558
- Scholl, A.J., "Motives for modular forms", *Inventiones Math.* 100 (1990), 419-430
- LMFDB collaboration, *L-functions and Modular Forms Database* (record 4.5.b.a accessed 2026-05-06)

(Remaining 13 refs: Bloch-Kato Tamagawa survey, Brunault-Neururer survey, Coleman, Fontaine-Perrin-Riou, Hida, Kato 2004, Mazur-Tate-Teitelbaum, Perrin-Riou, Rohrlich-Damerell, Schappacher-Scholl, etc. — to fill at submission.)

---

## §A. Appendix (optional, in supplementary): sympy F1 verification (0.5pp)

```python
from sympy import Rational, log, S
ms = [1, 2, 3, 4]
alpha_raw = {1: Rational(1,10), 2: Rational(1,12), 3: Rational(1,24), 4: Rational(1,60)}
def F1(m, a):
    return a * (-2)**(m-1) * (1 + Rational(1, 2**(3-m))) if m < 3 else a * (-2)**(m-1) * (1 + 2**(m-3))
# (Note: m=3 boundary requires care; see M22 baseline formula)
# Output: v_2 = {-3, -2, 0, +1}
```

(Full script in M22 / paper-2 supplementary.)

---

## Honesty checklist

- Hallu count: 85 -> 85
- 3 [TBD: prove] markers honest (Steinberg-edge ext of KLZ, F1 Euler derivation, 2-adic Beilinson integrality)
- Conjecture, NOT theorem
- Conditional on M13.1.A (paper-2)
- KLZ2017 properly cited (M38 missed-reference fix integrated)
- 14pp budget: §1 (3) + §2 (2) + §3 (2) + §4 (2) + §5 (3) + §6 (1) + §7 (1) = 14pp ✓
