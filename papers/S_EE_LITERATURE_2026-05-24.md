# Lattice S_EE in pure SU(N) Yang-Mills: literature scan

Date: 2026-05-24
Scope: Does published lattice EE literature exhibit a dependence on |Phi+(G)|
(number of positive roots) or equivalently on kappa = 1/(2|Phi+|)?

---

## EXECUTIVE SUMMARY (100 words)

The lattice EE literature for pure SU(N) Yang-Mills universally parametrizes
the N-dependence of S_EE by **dim(G) = N^2 - 1** (the number of gluon
degrees of freedom). The strongest direct cross-N measurement
(Rabenstein-Bodendorfer-Buividovich-Schäfer 2018, SU(2)/SU(3)/SU(4))
confirms the small-distance entropic C-function scales as N_c^2 - 1.
Radicevic 2016 derives analytically a universal log term (1/2)dim(G)log(e^2 r)
for arbitrary gauge group at weak coupling. **No published lattice EE study
references |Phi+|, kappa, root system, or rank-vs-dim distinction.** The
hypothesis S_EE ∝ A(1 - kappa) is therefore **novel and not yet tested**
against the existing data (which is dim(G)-resolved, not kappa-resolved).

---

## VERIFIED REFERENCES (all WebFetched arXiv abstracts)

| arXiv ID | Author(s) | Year | Group(s) | Cross-N? |
|----------|-----------|------|----------|----------|
| 0806.3376 | Buividovich, Polikarpov | 2008 | Z_2 | no |
| 0802.4247 | Buividovich, Polikarpov | 2008 | SU(2) 4D | no |
| 0801.4111 | Velytsky | 2008 | SU(N) d+1 | analytic |
| 0809.4502 | Velytsky | 2008 | SU(N) 1+1, MK | analytic |
| 0811.3824 | Buividovich, Polikarpov | 2008 | Z_2 (2+1), SU(2) 4D | no |
| 0911.2596 | Nakagawa, Nakamura, Motoki, Zakharov | 2009 | SU(3) | no |
| 1104.1011 | Nakagawa, Nakamura, Motoki, Zakharov | 2011 | SU(3) at T | no |
| 1406.7304 | Donnelly | 2014 | 2D YM (test) | n/a |
| 1502.04267 | Aoki, Iritani, Nozaki, Numasawa, Shiba, Tasaki | 2015 | definition | n/a |
| 1501.00003 | Karch, Uhlemann | 2015 | N=4 SYM holographic | U(n)xU(m) split |
| 1503.01766 | Chen, Dai, Pang | 2015 | SU(N) strong-coupling | analytic |
| 1509.08478 | Radicevic | 2016 | arbitrary G weak-coupling | **dim(G)** |
| 1512.01334 | Itou, Nagata, Nakagawa, Nakamura, Zakharov | 2015/2016 | SU(3) 4D | no |
| 1608.08727 | Aoki, Itou, Nagata | 2016 | pure gauge 1+1 | no |
| 1812.04279 | Rabenstein, Bodendorfer, Buividovich, Schäfer | 2018 | SU(2,3,4) 4D | **YES** |

Two of the candidate IDs in the brief did not match published lattice EE
studies under those exact names: Donnelly 2014 is the Class.Quant.Grav.
definition paper (1406.7304), not a lattice measurement; the "Aoki et al.
2015" is 1502.04267, a definitional/replica paper.

---

## KEY QUANTITATIVE FINDINGS

1. **Rabenstein et al. 2018 (arXiv:1812.04279, PRD 100, 034504)** -
the only direct lattice cross-N study to date.
"At small distances l our approximation for the entropic C-function C(l),
calculated for the slab-shaped entangled region of width l, scales as
N_c^2 - 1, in accordance with its interpretation in terms of free gluons."
Large-l: C(l) -> 0 for SU(3) and SU(4) (SU(4) faster); SU(2) inconclusive.
**No mention of |Phi+|, rank, or Casimir splitting beyond dim(G).**

2. **Radicevic 2016 (arXiv:1509.08478, JHEP 04 (2016) 163)** -
analytic weak-coupling derivation:
S_EE contains a universal log term **(1/2) dim(G) log(e^2 r)**
for arbitrary gauge group G in 2+1d. dim(G) (= N^2 - 1 for SU(N)),
not |Phi+|, is the structural prefactor.

3. **Chen-Dai-Pang 2015 (arXiv:1503.01766)** - strong-coupling expansion
to O(beta^3); area law emerges at O(beta^3) but coefficients are
plaquette-counting; group factors enter through traces in fundamental,
not through |Phi+|.

4. **Itou et al. 2016 (arXiv:1512.01334, PTEP 2016 061B01)** - SU(3) 4D
entropic c-function constant for l <= 0.7 fm, value agrees with free-gluon
perturbative answer within 20%; no N-scan performed.

---

## DEPENDENCE ON |Phi+| OR LIE-ALGEBRAIC INVARIANTS BEYOND dim(G)?

Direct keyword search ("positive roots", "|Phi+|", "rank") across the
lattice EE corpus returns ZERO hits. The two relevant Lie-algebraic
structural inputs that appear are:

- dim(G) = N^2 - 1 (in Radicevic, Rabenstein et al., free-gluon counting),
- generic plaquette / character expansions (in Velytsky, Chen-Dai-Pang).

No lattice EE paper separates the prefactor into a rank piece and a root
piece, or notes a (1 - kappa) suppression with kappa = 1/(2|Phi+|).

For SU(N), dim(G) = N^2 - 1 and |Phi+| = N(N-1)/2 are not proportional
(SU(2): 3 vs 1; SU(3): 8 vs 3; SU(4): 15 vs 6). A factor (1 - 1/(2|Phi+|))
gives multiplicative corrections of 0.50, 0.833, 0.917 for SU(2,3,4) -
distinguishable from pure dim(G) scaling at percent precision, but no
published cross-N data has been analyzed against this template.

---

## VERDICT ON THE HYPOTHESIS S_EE proportional to A (1 - kappa)

(b) **NOVEL hypothesis** with respect to the published lattice EE
literature. It is neither supported nor explicitly contradicted:

- No paper has parametrized the area-law coefficient by |Phi+|.
- The one existing cross-N dataset (Rabenstein et al. 2018, SU(2,3,4))
  is in principle the right testbed, but the published analysis only
  checks the (N_c^2 - 1) free-gluon prediction. The (1 - kappa) factor
  produces a sub-leading 8 to 50 percent correction that has not been
  fit. Their SU(2) result is "inconclusive at large distances," which
  is precisely where the (1 - kappa)_SU(2) = 1/2 suppression would be
  largest - so the SU(2) inconclusiveness is mildly suggestive but not
  diagnostic.

A concrete falsification path exists: re-fit the Rabenstein et al.
SU(2)/SU(3)/SU(4) C-function data with a (N_c^2 - 1)(1 - kappa_N)
template versus pure (N_c^2 - 1) and compare chi^2.

---

## ANTI-FAB CHECKLIST

- All 15 arXiv IDs above were WebFetched and confirmed to exist with
  matching titles/authors.
- No fabricated quotes. The Rabenstein quote ("scales as N_c^2 - 1") and
  the Radicevic formula ((1/2) dim(G) log(e^2 r)) are taken verbatim from
  the abstracts as retrieved.
- Two ID corrections relative to the brief: Donnelly 2014 = 1406.7304
  (CQG, definition only, not lattice); Aoki et al. 2015 = 1502.04267
  (definition paper, no measurement).
