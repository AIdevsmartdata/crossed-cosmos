# Cover letter — Journal of Number Theory (short note)

**Manuscript** : "A motivic-weight anchor at SU(2)/D=−67: a single-discriminant
correspondence and its finite-N limitations"
**Author** : Kévin Remondière (Independent researcher, Tarbes, France)
**ORCID** : 0009-0008-2443-7166
**Email** : kevin.remondiere [at] gmail.com
**Length** : 11 pp total = 8 pp main body + 3 pp Appendix~A (cross-$N$ audit details), 4 tables, ancillary Python script
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

I am pleased to submit for your consideration the short note

> **"A motivic-weight anchor at SU(2)/D=−67: a single-discriminant
> correspondence and its finite-N limitations"**

for publication in the *Journal of Number Theory* (11 pp, amsart class; an
`elsarticle.cls` conversion can be supplied on editorial request).

**Mathematical result.** The Athenodorou–Teper 2021 continuum-extrapolated
lattice spectrum of pure SU(2) Yang–Mills theory
(`arXiv:2106.00364`, Table 34) yields the ratio
`(m_{2++}/m_{0++})² = 2.001 ± 0.029`,
a match to within 0.07% to the integer `2 = 4/2`.
The note observes that this ratio equals the ratio of motivic weights
`w_mot(f_{−67}^{(5)}) / w_mot(f_{−67}^{(3)}) = 4/2`
of two canonical CM newforms attached to the imaginary quadratic field
`K = Q(√−67)` (LMFDB labels `67.5.b.a` and `67.3.b.a`).
The arithmetic foundation is verified by PARI/GP `mfeigenbasis` at the
four smallest split primes `{17, 19, 23, 29}`, confirming the Newton
identity `a_p(w=5) = a_p(w=3)² − 2p²` in each case (Conjecture E-1).

**Honest qualification (Option B reframe).** A cross-N audit across
`N ∈ {2, 3, 4, 5, 6, 8, 10, 12}` plus the large-N extrapolation
(Table 38 of `arXiv:2106.00364`) establishes that the universal hypothesis
`(m_{2++}/m_{0++})² = 2` for all N is rejected at `χ² = 211.7` on 9
degrees of freedom (Gaussian-equivalent `z = 13.4σ`, `p ~ 10^{−40}`).
The SU(2) match is a finite-N coincidence: a `1/N²` subleading correction
at N = 2 pulls the ratio down to accidentally coincide with `√2`.
**Conjecture E-1 as a universal cross-N law is falsified.** It is retained
in the paper as a qualified single-discriminant, single-N empirical
observation at `(D, N) = (−67, 2)`, at tier T_PLAUSIBLE, with explicit
falsifiability conditions for future lattice data.

**Content and novelty.** The mathematical novelty is the *explicit
identification* of a lattice glueball mass ratio with a motivic-weight
ratio of CM newforms at a specific discriminant, together with an
PARI/GP-verified arithmetic check of the underlying Hecke eigenvalue
structure. The note contributes a concrete, falsifiable bridge between
number theory (CM modular forms at D = −67) and lattice Yang–Mills
phenomenology. The cross-N falsification is documented in full to prevent
overclaiming.

**Manuscript.** 11 pages, 2 tables, 19 references (`arXiv:2106.00364`
as primary lattice anchor; Shimura 1971, LMFDB, 't Hooft 1974, Veneziano
1979, Witten 1979; plus ECI working-notes companion papers). An ancillary
Python script (`notes/AT2021_GEVP_refit_test.py`) reproduces the cross-N
chi-squared calculation. No conflict of interest; original submission,
not under review elsewhere.

**Suggested reviewers** (declared without solicitation): Christopher
Fewster (York, UK); Rainer Verch (Leipzig); Michal Wrochna (Utrecht).
Alternative mathematical physics reviewers: David Tong (Cambridge);
Gregory Moore (Rutgers).

I am grateful for your consideration.

Sincerely,

Kévin Remondière

---

## Editorial-Manager metadata

| Field | Value |
|---|---|
| Article type | Short note |
| Primary subject classification (MSC 2020) | 11F11 (Holomorphic modular forms of integral weight) |
| Secondary | 11R29, 81T13, 11G15, 14J28 |
| Keywords | CM newforms; motivic weight; glueball mass ratio; SU(2) lattice; weight 5; imaginary quadratic field; Newton identity; Hecke eigenvalues; Option B reframe |
| Files attached | `main.pdf` (11 pp); `AT2021_GEVP_refit_test.py` (ancillary Python) |
| Ancillary scripts | PARI/GP `mfeigenbasis` verification; Python chi-squared cross-N refit |
| Word count (body) | ~4 800 |

**Submission portal** : https://www.editorialmanager.com/jnt/ (Elsevier
Editorial Manager).
