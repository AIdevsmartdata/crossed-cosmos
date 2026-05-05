# Cover Letter — Bulletin of the London Mathematical Society

**Journal:** Bulletin of the London Mathematical Society (BLMS)
**Submission type:** Short Research Article
**Proposed subject classification:** 11F11 (Holomorphic modular forms), 11F25 (Hecke-Petersson theory), 11F30 (Fourier coefficients)
**arXiv category:** math.NT

---

Dear Editors of the Bulletin of the London Mathematical Society,

We submit for consideration the short paper

**"Two LMFDB identifications for hatted weight-5 multiplets
of the metaplectic cover S'_4"**

by Kévin Remondière.

**Summary of the paper.**
The metaplectic cover S'_4 of the modular symmetry group S_4, introduced
by Novichkov, Penedo, and Petcov (Nucl. Phys. B 963, 2021; arXiv:2006.03058), is
a group of order 48 whose "hatted" representations carry modular forms
of odd weight at level Γ(4).  We establish two identifications between
forms in this metaplectic setting and classical newforms in the LMFDB:

1.  The hatted triplet **3̂,2(5)** (weight 5) is the unique newform
    **LMFDB 4.5.b.a**: a CM form with complex multiplication by Q(i),
    level 4, weight 5, nebentypus χ₄.  Four independent verifications
    are given: a direct sympy q₄-expansion computation from the NPP20
    formula; a verbatim q-expansion match; Hecke characteristic
    polynomials; and the Grössencharacter formula a(p) = 2·Re((a+bi)⁴)
    for p = a²+b².

2.  The hatted doublet **2̂(5)** (weight 5) is the newform
    **LMFDB 16.5.c.a**: a non-CM form of level 16, weight 5,
    with coefficient field Q(√−3) and Galois dimension 2.
    The identification is verified at 14 primes (p ≤ 113), far beyond
    the Sturm bound B = 10 for this space.

As a corollary, we prove that the Hecke sub-algebra
H₁ = {T(p) : p ≡ 1 (mod 4)} acts as a closed subalgebra on each
hatted multiplet, while T(p) for p ≡ 3 (mod 4) is obstructed
(verified at 10 primes).  This corollary follows immediately from the
χ₄-nebentypus of both identified newforms, and gives the first
systematic explanation of the parity restriction observed in
computational experiments with S'_4.

**Why this is of interest to BLMS readers.**
The result is a clean observation in the arithmetic of modular forms,
using only standard tools (Sturm bounds, Grössencharacter theory,
Hecke operators) but applied to a recently introduced and mathematically
rich setting.  The identification of metaplectic forms with LMFDB entries
provides the first bridge between the growing literature on modular
flavour symmetry and the classical L-function database, opening a
systematic classification problem (extend to all hatted multiplets at
all odd weights).  The paper requires no new compute or conjecture:
all claims follow from standard theory plus explicit Hecke eigenvalue
computations.

**Length and format.**
The paper is approximately 9–10 pages in amsart format, including
two small tables and a bibliography of 9 entries.  It is self-contained
and accessible to any reader familiar with the theory of newforms.

**Conflicts of interest.**
None.

**Suggested reviewers.**
- John Cremona (University of Warwick) — LMFDB expert, arithmetic of
  modular forms.
- Nathan Ryan (Bucknell University) — LMFDB developer, computational
  modular forms.
- Andrew Booker (University of Bristol) — L-functions, modular forms.
- Shaun Stevens (University of East Anglia) — representation theory of
  covering groups.

(None of the suggested reviewers are co-authors or recent collaborators.)

We confirm that this work has not been submitted elsewhere and that all
verifications are documented in an audit trail available at Zenodo:
concept DOI `10.5281/zenodo.19686398` (ECI project archive);
current record v6.0.51: `10.5281/zenodo.20030243`.
Note: this DOI will be updated to the v6.0.52 record once the Zenodo
service recovers from a 504 retry queue (update is queued as of 2026-05-04).

Sincerely,

Kévin Remondière
kevin.remondiere@gmail.com

---

**[STATUS after Final Polish Pass — 2026-05-04]**

Live verifications completed (final pass):
- LMFDB 4.5.b.a: confirmed dim=1, CM by Q(i), char orbit 4.b, q-expansion
  verbatim `q - 4q² + 16q⁴ - 14q⁵ - 64q⁸ + 81q⁹ + 56q¹⁰ - 238q¹³ + 256q¹⁶ + 322q¹⁷ - 324q¹⁸ - 224q²⁰ - 429q²⁵ + 952q²⁶ + 82q²⁹ + ...`
  Root number = +1 (re-confirmed via L-function page; sign = 1, Λ(s) = Λ(5−s)).
- LMFDB 16.5.c.a: confirmed dim=2, coeff field Q(√-3), char orbit 16.c, not CM,
  self-dual = NO (corrected from earlier draft that said yes).
  a(5)=18, a(13)=178, a(17)=-126, a(29)=-1422 live-confirmed.
- arXiv:2604.01422 (dMVP26): authors = Ivo de Medeiros Varzielas and Manuel Paiva. CONFIRMED.
- arXiv:2006.03058 (NPP20): 3 authors, Nucl. Phys. B 963 (2021) 115301. CONFIRMED.
- arXiv:2006.10722 (LYD20): correct title. CONFIRMED.

BLMS requirements (from known journal standards; direct URL blocked):
- Page limit: ≤ 12 printed pages (BLMS standard for short articles).
  Paper is estimated ~9–10 pp in amsart 12pt, well within limit.
- Reference style: LMS standard (author-year or numbered; paper uses numbered).
- Abstract: ~200 words standard for BLMS (paper abstract is ~180 words — within range).
- MSC2020 codes: Primary 11F11; Secondary 11F25, 11F30. Added to TeX file.
- Keywords: added to TeX file.

Zenodo DOI: concept DOI `10.5281/zenodo.19686398`; v6.0.51 record: `10.5281/zenodo.20030243`
(v6.0.52 DOI to be updated once Zenodo recovers)
