# Cover letter — Journal of Number Theory

**Manuscript** : "The number of Q-rational weight-5 CM newforms attached to
an imaginary quadratic field: a theorem (Gauss 1801) and a conjecture
(Rubin 1991)"
**Author** : Kevin Remondière (Independent researcher, Tarbes, France)
**ORCID** : 0009-0008-2443-7166
**Email** : kevin.remondiere [at] gmail.com
**Length** : 8 pp, 1 table, ancillary PARI/GP script
**Date** : 16 May 2026

---

Kévin Remondière
Independent researcher
Tarbes, France
ORCID: 0009-0008-2443-7166
kevin.remondiere [at] gmail.com

16 May 2026

Editor-in-Chief
*Journal of Number Theory*
Elsevier

Dear Editor,

I am pleased to submit for your consideration the manuscript

> **"The number of Q-rational weight-5 CM newforms attached to an imaginary
> quadratic field: a theorem (Gauss 1801) and a conjecture (Rubin 1991)"**

for publication in the *Journal of Number Theory* as a short note (8 pp,
amsart class, JNT-acceptable; an `elsarticle.cls` conversion can be supplied
on editorial request).

**Result.** Let `K = Q(√D)` be an imaginary quadratic field of fundamental
discriminant `D < 0`, and let `r(D)` denote the number of weight-5 Hecke
newforms of level `|D|` with complex multiplication by `K`, Nebentypus
`χ_K`, and *all* Fourier coefficients rational. The paper proves, in
three pages of elementary harmonic analysis on `Cl(K)`, that when `Cl(K)`
is a 2-group `r(D) = |Cl(K)[2]| = 2^{rk₂ Cl(K)} = 2^{t-1}`, with
`t = ω(|D|)`. The last equality is Gauss's 1801 genus theorem
(*Disquisitiones* §§225–237, cf. Cox 1989 Thm. 3.15). A precise
conjecture for the case where `Cl(K)` admits non-trivial *odd* torsion —
consistent with, but not derived from, Rubin's 1991 main conjecture
(Invent. Math. **103**, 25–68) — complements the theorem.

**Theorem vs Conjecture, honestly labelled.** The proved part (T) rests
*entirely* on classical 1801 input plus the standard Galois action on
CM Hecke eigenforms; no Iwasawa-theoretic input is used. The open part
(C) is *explicitly* labelled open. The novelty I claim is the
*explicit identification* of `r(D)` with the Gauss invariant at weight 5,
plus the new pure 2-rank-4 anchor; I do not claim priority on
`|Cl(K)[2]| = 2^{t-1}` or on the rationality criterion `ψ̄² = 1`.

**Numerical anchors.** Both statements are verified on **seven** anchors
spanning `rk₂ ∈ {0, 2, 3, 4}`, including the first known fundamental
discriminant of pure 2-rank 4, `D = −5460 = −4·3·5·7·13`, where
`r(−5460) = 16` is confirmed by two independent PARI/GP methods
(`mfeigenbasis` and direct theta enumeration). An extension sweep over
`D ∈ [−10000, −1000]` produced **452** further Gauss-Cox–predicted
anchors which all confirm the theorem. The ancillary script
`D5460_theta_direct.gp` reproduces the rank-4 anchor in under a minute.

**Manuscript.** 8 pages, 1 table, 8 references (Cox 1989, Gauss 1801,
Miyake 2006, Rubin 1991, Shimura 1971, PARI 2024, Smith 2017
[arXiv:1702.02325], Smith 2025 [arXiv:2503.17619]). The §5 paragraph
on Cohen–Lenstra–Gerth compatibility cites the two Smith arXiv references
with explicit hyperlinks; the proof itself (§§1–4) uses only the
classical (non-arXiv) references. No conflict of interest; original
submission, not under review elsewhere. An endorsement request has
been sent to Prof. Don Zagier (MPIM Bonn) for the arXiv math.NT
primary 11F11.

**Suggested reviewers** (declared without solicitation): Don Zagier
(MPIM Bonn); Henri Cohen (Bordeaux); Karl Rubin (UC Irvine);
Lawrence C. Washington (Maryland).

I am grateful for your consideration.

Sincerely,

Kévin Remondière

---

## Editorial-Manager metadata

| Field | Value |
|---|---|
| Article type | Short note |
| Primary subject classification (MSC 2020) | 11F11 |
| Secondary | 11R29, 11F30, 11G15 |
| Keywords | Q-rational newforms; complex multiplication; weight 5; class group; 2-torsion; genus theory; imaginary quadratic field; Hecke characters |
| Files attached | `main.pdf` (8 pp); `D5460_theta_direct.gp` (PARI/GP, ancillary) |
| Ancillary scripts | PARI/GP `mfeigenbasis` driver + direct theta-series enumerator |
| Word count (body) | ~2 400 |

**Submission portal** : https://www.editorialmanager.com/jnt/ (Elsevier
Editorial Manager).
