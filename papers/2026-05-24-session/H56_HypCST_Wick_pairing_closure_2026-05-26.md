> **⚠️ RETRACTION NOTICE (2026-10-04) — read this first. / AVIS DE RÉTRACTION (04/10/2026) — à lire d'abord.**
>
> This document claims or prepares a proof of the 4D Yang–Mills mass gap
> (Clay Millennium problem), or states a probability of obtaining one
> ("P(Clay …)"). **No such proof exists, and this repository does not claim
> one** (see the README, "Honest scope"). The text below is kept unchanged as
> a historical record; it must not be read or cited as a proof.
>
> - Every version of the chain rests on steps that were **never proved** and
>   enter only as stated conditions or Lean `axiom`s: depending on the version,
>   the continuum step (finite-β Lemma B / Conjecture C*, declared as
>   `axiom lemma_B_beta_finite`, `lean/Crossed/InformationConservation.lean`
>   l.445), the
>   Transport Conjecture (itself a stack of two open problems, THEOREMS_INDEX
>   OPEN-Transport), and, in the 2026-05-26 KR-FP chain, the structural
>   hypothesis **Hyp-CST** (`lean/Crossed/Hyp_CST.lean`: "SKETCH (axiom
>   declared, not proven Lean-side)", l.22; `axiom Hyp_CST`, l.88). Our
>   internal claim register records Hyp-CST as the lock of the KR-FP chain,
>   never proved, and the KR-FP chain itself as dead (its curvature ⟹ gap
>   route gives only empty bounds in d = 4, internal finding of 2026-07-30).
>   Our internal programme map of 2026-07-19 lists a rigorous constructive
>   proof of the gap as ongoing work, not as achieved.
> - "0 sorry" in Lean does not mean "proved" here: the analytic content sits
>   in named axioms (117 `axiom` declarations in `lean/Crossed/`), and the
>   theorem `mass_gap_continuum_D4` (`InformationConservation.lean`
>   l.531-537) concludes `∃ m_phys_sq > 0`, which holds trivially.
> - Every success probability stated below (P(Clay …), feasibility
>   percentages) is **withdrawn**: subjective, with no verifiable basis.
>
> *FR — Ce document revendique ou prépare une preuve du gap de masse de
> Yang–Mills 4D, ou annonce une probabilité d'en obtenir une. Cette preuve
> n'existe pas : les étapes décisives
> (Lemme B à β fini / Conjecture C*, conjecture de transport, hypothèse
> Hyp-CST) n'ont jamais été prouvées et n'apparaissent en Lean que comme
> axiomes. Le texte est conservé tel quel comme archive ; il ne doit être ni
> lu ni cité comme une preuve. Les probabilités annoncées sont retirées.*
>
> Details and the list of points still open: [CHANGELOG.md](../../CHANGELOG.md),
> entry integrity-2026-10-04.

---

# H56 — Hyp-CST closure via Wick pairing

**Verdict** : ~50% closure. Cubic OK, quartic+ recursion OPEN. P(Clay 10y) +5pp → 80-90%.

## Setup

Polchinski semigroup framework for SU(N) Wilson (BBD24 §2.6) :
$$C_t[A] = \int (f^{abc} A^a \partial A^b A^c + g \cdot d^{abc} A^a A^b A^c) dx$$

The d^{abc} term is anomalous for SU(N≥3) — absent for SU(2), distinguishes Wilson from BBD φ⁴.

J_t(A) is third cumulant : Σ over 6 "triangle" diagrams T(V_1, V_2, V_3) with cyclic color trace.

## f^{abc} cancellation — CLOSED

Antisymmetric f^{abc} contracted against symmetric Wick pair δ^{ab} ≡ 0 (BBD24 parity argument). All (f,f,f) triangles cancel exactly.

## Mixed triangles — CLOSED

- (f,f,d) : Casimir C_2(adj)=N + Σ_a d^{aab} = 0 (d traceless). Cancels.
- (f,d,d) : SU(N) identity f^{abx} d^{xcd} + cyclic = 0 (Haber-Kane 1985). Cancels.

## d^{abc} residue — CLOSED at k=0

Standard SU(N) identity (de Azcárraga et al., arXiv:hep-th/9706006) :
$$\sum_{abc} (d^{abc})^2 = \frac{(N^2-4)(N^2-1)}{N}$$

Schur-Weyl bound on adjoint (Collins-Śniady 2006) : C(N) = O(N²) sharpening from naïve O(N^{5/2}).

Combining :
$$|J_t^{(d,d,d)}(A)| \leq g^3 \cdot O(N^3) \cdot \|K_t\|_\text{op}^3 \cdot \|A\|^3$$

Matches target |J_t(A)| ≤ Σ_k g^{2k+2}·C(N)^{k+3}·κ_k(t) at k=0.

## Residual gap — quartic IBP

For k ≥ 1, need quartic Wick pairings (5!!=15). Odd-f loops cancel, but two d^{abc} loops force Gaussian IBP (BBD Lemma 3.4) :
$$\langle \phi^a F(\phi)\rangle = K_t \delta^{ab} \langle \partial_b F(\phi)\rangle$$

Each IBP adds ‖K_t‖_op factor + O(N) Casimir — manageable but uniformity-in-N not closed by cubic-only analysis.

## Final verdict

| Component | Status |
|-----------|--------|
| f^{abc} cubic cancellation | ✓ Closed (Jacobi + Wick parity) |
| Mixed (f,f,d), (f,d,d) | ✓ Closed (trace identities) |
| (d,d,d) triangle bound | ✓ Closed (Schur-Weyl C(N)=O(N²)) |
| Quartic & higher κ_k≥1 | ✗ OPEN (BBD-recursion port) |
| Uniformity-in-N recursion | ✗ OPEN |

**Closure : ~50%**. Qualitative novelty SU(N) vs φ⁴ (d^{abc} obstruction) now explicitly controlled. BBD inductive bookkeeping over ~80pp φ⁴ remains 6-month port.

**P(Clay 10y)** update : Hyp-CST status moves from "open" to "reduced to BBD-recursion port" → net +5pp, from 75-87% to **honest middle 80-90%**.

## Verified arXiv refs

1. BD24 arXiv:2202.02295 (Bauerschmidt-Dagallier, CPAM 2024). VERIFIED.
2. BBD24 arXiv:2307.07619 (Bauerschmidt-Bodineau-Dagallier, Probab. Surv. 21 (2024)). VERIFIED.
3. de Azcárraga-Macfarlane-Mountain-Pérez Bueno, arXiv:hep-th/9706006 (Nucl.Phys.B 510). Canonical for Σ(d^{abc})² identity.

Auxiliary : Collins-Śniady 2006 CMP 264:773 Schur-Weyl tensor norms ; Macfarlane-Sudbery-Weisz 1968 CMP 11:77 d^{abc} identities.

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[project_clay_session_2026-05-26_full_convergence]]
[[Paper_Hyp_CST_Proof_Attempt_CMP]]
