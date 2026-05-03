# Nested-Diamond Index Conjecture — Verdict

**Conjecture (Vardian-HPS-LL trio open problem, /tmp/krylov_trio_close.md item 4):**
Is there a subfactor inclusion `A(D_O') ⊂ A(D_O)` between nested FRW comoving
diamonds (both satisfying η_i > 0 of Thm 3.5 / `prop:U-iso` of
`paper/frw_typeII_note/frw_note.tex`) whose Kosaki/Jones index equals
`exp(C · R_proper(η_c))`?

**Date.** 2026-05-02. **Bench.** Opus 4.7 (1M context). Sympy + arXiv +
WebSearch triangulated.

---

## 1. Nested diamond inclusion (FRW + Minkowski)

**FRW side.** With the standard double-cone parametrisation
`D_O(η_i, η_f) = { (η, x) : η_i ≤ η ≤ η_f, |x| ≤ R_d − |η − η_c| }`,
`η_c = (η_i+η_f)/2`, `R_d = (η_f−η_i)/2`:

```
D_O'(η_i', η_f') ⊂ D_O(η_i, η_f)   iff   η_i < η_i' AND η_f' < η_f.
```

Sympy-verified (envelope difference = `η_i' − η_i > 0` on one side and
`η_f − η_f' > 0` on the other; /tmp/nested_diamond_index.py §A).
Both diamonds satisfy `0 < η_i, η_i' < η_f', η_f < ∞`, so Thm 3.5 / `prop:U-iso`
applies to both. By isotony of the local net, `A(D_O')_FRW ⊂ A(D_O)_FRW`.

**Minkowski side.** `prop:U-iso` (frw_note line 194) gives a single unitary
`U` on the joint Fock space with `U A(D_O)_FRW U^{-1} = A(M_O)_Mink`. The
construction uses the test-function bijection `f ↦ a^3 f`, which is local
(supports preserved). Therefore the same `U` intertwines the smaller-region
algebras: `U A(D_O')_FRW U^{-1} = A(M_O')_Mink`. Conjugating the inclusion by
`U`:

```
[A(D_O')_FRW ⊂ A(D_O)_FRW]  --U-->  [A(M_O')_Mink ⊂ A(M_O)_Mink]
```

is a W*-isomorphism of inclusions. The Jones-Kosaki index is invariant under
spatial isomorphism, so `[A(D_O)_FRW : A(D_O')_FRW] = [A(M_O)_Mink : A(M_O')_Mink]`.

## 2. Kosaki/Jones index calculation

Both `A(M_O')_Mink` and `A(M_O)_Mink` are type III_1 factors (Buchholz-Wichmann
1986 CMP 106, Wollenberg). The inclusion is the canonical *split inclusion of
type III_1 factors* (Doplicher-Longo Inv. Math. 75 (1984) 493 §3-4; Buchholz-
D'Antoni-Longo CMP 129 (1990) 115; for free massless scalar specifically,
Buchholz CMP 36 (1974) 287 verifies the trace-class / nuclearity hypothesis).

**Triangulated literature consensus (verbatim):**
- Leutheusser-Liu, arXiv:2508.00056 (cited in trio close, Aug 2025):
  > "In the continuum limit of the bulk EFT, the algebra inclusions are split
  > inclusions of type III_1 factors, for which the normal conditional
  > expectation needed for a finite Kosaki index does not exist."
- arXiv:2602.10733 (Feb 2026 QFT info-protocol paper):
  > "spacetime inclusions cannot have finite index ... otherwise we would have
  > a finite-dimensional algebra instead of another type III_1 one."

**Conclusion.** No normal conditional expectation `E : M → N` exists, so the
Kosaki index `Ind(E) = E^{-1}(1)` is not defined as a finite number; equivalently
the minimal index `inf_E Ind(E) = +∞` over the empty set of normal conditional
expectations. **`[A(M_O) : A(M_O')] = +∞`.**

The S^1-conformal-net result `[A(E) : A(E')'] = μ-index = global index <∞`
(Kawahigashi-Longo-Müger arXiv:math/9903104 Thm 5) is for *2D chiral* completely
rational nets; the 4D nested-diamond case is fundamentally non-rational (no
finite list of sectors) and the KLM theorem does not apply.

## 3. Verdict on the identity `[M:N] = exp(C · R_proper(η_c))`

**FALSE for the standard Kosaki/Jones index.** LHS = +∞, RHS = `exp(C · 2 a_0 η_c R_d)`
finite (sympy-verified, /tmp/nested_diamond_index.py §C-F).

**Restricted-class search:**
- *S^1 chiral free boson*: KLM index is finite but is the GLOBAL index over all
  sectors; it does not depend on a continuous geometric parameter `R_proper(η_c)`
  and so cannot equal `exp(C·R_proper)` for varying η_c. No published identity.
- *Möbius-conjugate diamonds*: the inclusion is then an *automorphism*, index
  = 1 = exp(0); requires `R_proper = 0` (trivial).
- *Holographic redefinition (Leutheusser-Liu)*: their `(M:N) := exp(C·Vol(b))`
  is *defined* by exponentiation of bulk volume; it is NOT the Kosaki index and
  is restricted to AdS-bulk subregions (not FRW). Using it to "verify" a
  `(M:N) = exp(C · R_proper)` identity on FRW would require independently
  identifying `Vol(b)` with `R_proper`, which is not done in any paper surveyed.

## 4. Theorem statement / clean obstruction

**Theorem (clean obstruction).** Let `A(D_O')_FRW ⊂ A(D_O)_FRW` be the inclusion
of local algebras of nested FRW comoving diamonds with `0 < η_i < η_i' < η_f' <
η_f < ∞`, in the setting of frw_note Theorem 3.5 (radiation-dominated FRW,
conformally coupled massless scalar, conformal vacuum). Then:

  (i) The inclusion is W*-isomorphic via `Ad U` to the Minkowski split
      inclusion `A(M_O')_Mink ⊂ A(M_O)_Mink` of the conformally identified
      diamonds (consequence of frw_note Prop. U-iso applied region-by-region).

 (ii) The inclusion is a standard split inclusion of type III_1 factors
      in the sense of Doplicher-Longo (Inv. Math. 75, 1984).

(iii) No normal conditional expectation `E : A(D_O)_FRW → A(D_O')_FRW` exists.
      Equivalently, `[A(D_O)_FRW : A(D_O')_FRW]_Kosaki = +∞`.

(iv) The conjectured identity `[A(D_O)_FRW : A(D_O')_FRW]_Kosaki = exp(C·R_proper(η_c))`
      is FALSE: LHS = +∞ while RHS is finite for the bounded diamond
      (`R_proper(η_c) = 2 a_0 η_c R_d < ∞` in radiation-dominated FRW,
      sympy-verified).

## 5. Residual open question (precise)

**Open Q (Krylov-Diameter / volume-as-index bridge).** Find an algebraic
invariant `J(N ⊂ M)` of the standard split inclusion `N ⊂ M` of type III_1
factors associated to a nested FRW comoving-diamond pair, such that:
  - `J(N ⊂ M) ∈ (0, ∞)` is finite for every η_i' > η_i > 0, η_f' < η_f < ∞.
  - `J(N ⊂ M) = exp(C · R_proper(η_c))` for some absolute constant C.
Candidates explicitly excluded by §3: Kosaki index, Jones index, μ-index in
the KLM sense, dimension of the relative commutant.
Candidate invariants worth investigating (each requires a separate analysis):
(a) Buchholz-D'Antoni-Longo *split distance* (CMP 129, 1990); (b) the "depth"
of the Connes-Wassermann inclusion in the Wassermann subfactor of free fermion
nets, transported via boson-fermion duality; (c) the Hawking-Page-style
"effective entropy" associated to the relative entropy of the Bunch-Davies
state restricted to N versus M (Longo *Entropy distribution of localised states*,
CMP 373 (2020) 473). None of these is currently known to equal `exp(C·R_proper)`
on FRW.

## 6. Publishable target

- **Theorem (clean obstruction)** above is publishable as a 6-8 page note in
  **Letters in Mathematical Physics** or as an **Appendix** to the existing
  `paper/frw_typeII_note/frw_note.tex` (preferred: avoids doubling the priority
  claim). Closes the trio open problem of /tmp/krylov_trio_close.md item 4
  with a definitive **NO** for the standard Kosaki/Jones index.
- **Open Q (Krylov-Diameter bridge)** is a research programme, not a publishable
  theorem. CMP / JFA target only after a positive answer for one of the candidate
  invariants above.

**Recommendation.** Fold §1-§4 above into `paper/frw_typeII_note/frw_note.tex`
Section 5 (Open problems), as a new subsection "Nested-diamond Kosaki index
obstruction" with the clean **Theorem (clean obstruction)** statement. Cite
Doplicher-Longo 1984, Buchholz-D'Antoni-Longo 1990, Leutheusser-Liu 2508.00056,
arXiv:2602.10733. Update /tmp/krylov_trio_close.md item 4 from "open problem"
to "answered NO for Kosaki, OPEN for non-Kosaki invariants".
**Do not push.** Local commit only.

---

**Files.**
- `/tmp/nested_diamond_index.py` — sympy verification (§A nesting, §C
  R_proper, §F sanity).
- `/tmp/nested_diamond_index.tex` — LaTeX-ready Theorem statement (clean
  obstruction) for inclusion in frw_note.tex.
- This file `/tmp/nested_diamond_index.md` — verdict report.
