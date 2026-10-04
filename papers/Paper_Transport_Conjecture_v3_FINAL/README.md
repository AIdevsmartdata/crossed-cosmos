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

# Transport Conjecture, v3 (2026)

This folder holds `main.tex`, `main.pdf` and `refs.bib`, kept as a historical record (the only change is a comment-only notice at the top of `main.tex`; `main.pdf` is unchanged). The probabilities it states (e.g. "P(Transport PROVED within 30y)", "P(Clay YM 15y)") are withdrawn. The Transport Conjecture remains open (THEOREMS_INDEX OPEN-Transport).
