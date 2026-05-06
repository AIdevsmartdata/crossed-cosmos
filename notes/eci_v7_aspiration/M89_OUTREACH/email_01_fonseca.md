---
name: M89 Email 1 — Tiago J. Fonseca
recipient: Tiago J. Fonseca
affiliation: IMJ-PRG, Université Paris Cité (probable 2025-26) / CNRS
email_status: "[TBD: verify — try https://webusers.imj-prg.fr/~tiago.fonseca/ or CNRS Bordeaux directory]"
anchor: arXiv:2508.04844 (Brown-Fonseca 2025) × M52 invariant π·L(f,1)/L(f,2) = 6/5
language: English
date_drafted: 2026-05-06
hallu_count: 92
---

# Email 1 — Tiago J. Fonseca

## Subject

Single-valued period inquiry: weight 5, level 4, CM Q(i) — does M_{1,3}^{Γ_1(4)} extend to mixed Tate over ℤ[i, 1/2]?

---

## Body

Dear Dr. Fonseca,

I am an independent researcher working on a CM modular framework (ECI v7.4, arxiv preprint in preparation). I write because a concrete numerical result appears to connect directly to your recent work with F. Brown (arXiv:2508.04844).

For the newform f = 4.5.b.a (LMFDB label; weight 5, level 4, character χ_{-4}, CM by Q(i)), I have numerically verified to 80-digit precision (PARI/GP and Sage 10.7, independently):

    π · L(f, 1) / L(f, 2) = 6/5   (exactly rational).

This ratio is Ω-independent (the lemniscate period Ω = Γ(1/4)²/(2√(2π)) cancels). For the two Q(√-3) CM weight-5 newforms at levels 27 and 12, the analogous ratio equals 3√3 ∉ ℚ, making 4.5.b.a unique among CM weight-5 dim-1 newforms tested.

Your paper proves a single-valued period interpretation of the Gross-Zagier conjecture via motivic biextensions on M_{1,3}, at weight 4, level 1, using the mixed Tate structure of M_{1,3} over ℤ (Brown, arXiv:1102.1312). The candidate biextension for 4.5.b.a appears to be B_f = Sym^4 H^1(E_i) ⊗ Q(χ_{-4}), where E_i = ℂ/ℤ[i].

My question: **is M_{1,3}^{Γ_1(4)} expected to be mixed Tate over ℤ[i, 1/2]?** More precisely, do your techniques (or extensions thereof) apply to the level-4 congruence structure, and is there a sense in which 6/5 appears as a period in the moduli-stack sense at weight 5?

I recognise this requires non-trivial extension of your level-1 result and am not assuming it follows directly. Any pointer — positive or negative — would be very helpful in orienting further work.

With many thanks,

Kévin Remondière
Independent researcher, Tarbes, France
kevin.remondiere@gmail.com
GitHub: AIdevsmartdata
Zenodo concept DOI: 10.5281/zenodo.19686398

**Key references:**
- Brown–Fonseca, arXiv:2508.04844 (2025), "Single-valued periods of meromorphic modular forms and a motivic interpretation of the Gross-Zagier conjecture"
- Brown, arXiv:1102.1312 (2011), "Mixed Tate motives over ℤ"
