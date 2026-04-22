# Team A — Derivation Sketch

**Goal.** Attempt, in good faith, to derive the A6 Matsubara
Euler-characteristic shift
```
<chi_E(nu)>_fNL - <chi_E(nu)>_0  =  (fNL * sigma0 * S3 / 6) * H3(nu) * phi(nu)
```
from a complexity functional `C[rho]` on the density field, where
`rho(nu)` is the one-point PDF of the smoothed density contrast delta
expressed in rescaled units `nu = delta/sigma0`. The deeper goal is to
show that this functional is the LSS specialisation of the same
monotone-complexity object that, on the quantum side, specialises to
Haferkamp gate complexity.

This note records exactly how far the attempt goes and where it stops.

---

## Step 1 — Candidate complexity functional

We test the **differential-entropy functional** on the 1-point PDF:
```
C_ent[rho]  :=  - ∫ rho(nu) log rho(nu) d nu.
```
Motivation: (i) it is monotone under coarse-graining-plus-diffusion, the
natural "complexity clock" on a classical field, (ii) it maps cleanly
under the Gram--Charlier expansion, (iii) at zero non-Gaussianity it
reduces to the Gaussian entropy `(1/2) log(2 pi e)`, a known fixed
point.

## Step 2 — Gram--Charlier weak-NG expansion

To leading order in sigma0 under the Matsubara 2003 / Edgeworth
convention,
```
rho(nu)  =  phi(nu) * [ 1 + eps * H3(nu) + O(sigma0^2) ],
eps := (sigma0 * S3) / 6,
```
where `H3(nu) = nu^3 - 3 nu` is the 3rd probabilists' Hermite
polynomial and `phi(nu) = (2 pi)^(-1/2) exp(-nu^2/2)`.

## Step 3 — Expand the functional

Symbolic (sympy) calculation of the O(eps) piece of the entropy
integrand:
```
d/d eps  [ rho log rho ] |_{eps=0}
    =  H3(nu) * phi(nu) * [ log phi(nu) + 1 ]
    =  H3(nu) * phi(nu) * [ 1 - (1/2) log(2 pi) - nu^2 / 2 ].
```
At this pointwise level the Matsubara profile `H3(nu) * phi(nu)` **does**
appear, but multiplied by a `nu`-dependent polynomial factor
`[1 - (1/2) log(2 pi) - nu^2 / 2]`. Integrating against `d nu`:
```
d C_ent / d eps |_{eps=0}
    =  - ∫ H3(nu) phi(nu) [ log phi(nu) + 1 ] d nu
    =  0
```
because `H3` is orthogonal to every Gaussian-weighted polynomial of
degree < 3 (in particular to `1`, `nu^2`, and thus to the bracket which
is degree 2 in nu). The **integrated** linear-in-`eps` entropy shift
vanishes. The leading nonzero entropy shift is O(eps^2):
```
C_ent(eps) - C_ent(0)  =  - (eps^2 / 2) * < H3^2 >_phi  + O(eps^3)
                       =  - 3 eps^2  +  O(eps^3),
```
using `< H3^2 >_phi = 3! = 6`.

**This is the first obstruction.** The Matsubara shift (A6-euler) is
linear in `fNL` (hence linear in `eps`). The differential entropy of
the 1-point PDF is NOT linear in `eps`; it is quadratic. So `C_ent`
reproduces the **scaling class** of the Matsubara object only if one
restricts attention to the pointwise integrand before `d nu`-integration,
which is not what `C_ent` computes.

## Step 4 — Local (pointwise) complexity density

Abandon the integrated functional; instead work with the local
complexity **density**
```
c(nu)  :=  - rho(nu) log rho(nu),
```
whose integral is `C_ent`. At O(eps),
```
c^{(1)}(nu)
  =  - H3(nu) phi(nu) * [ 1 - (1/2) log(2 pi) - nu^2 / 2 ].
```
This is `H3(nu) phi(nu)` weighted by a degree-2 polynomial. The Matsubara
Euler-shift is proportional to `H3(nu) phi(nu)` with **constant**
coefficient `fNL sigma0 S3 / 6`. So the pointwise complexity-density
function is **not** proportional to the Matsubara profile either; the
weight polynomial is extra.

**This is the second obstruction.** Any projection scheme that
"extracts" `H3(nu) phi(nu)` from `c^{(1)}(nu)` would require an explicit
choice of inner product or band-pass filter, and once such a filter is
introduced, the derivation degenerates: *any* linear Gram--Charlier
coefficient can be recovered from *any* sufficiently smooth functional
of rho by choosing the filter accordingly. The derivation becomes
tautological.

## Step 5 — What would be needed to make this rigorous

A genuine derivation of (A6-euler) from a complexity functional that is
**also** the LSS specialisation of the quantum-circuit Haferkamp object
would need:

1. A constructive definition of `C_LSS[Sigma; t]` in terms of persistent
   homology of the super-level-set filtration (candidate given in the
   draft Eq.(C_LSS): total persistence `sum_k ∫ (d-b) dPH_k`).
2. A theorem showing that the **time derivative** of `C_LSS` along
   gravitational structure formation factorises into a Gaussian
   baseline plus a Gram--Charlier-indexed tower of non-Gaussian
   corrections.
3. Identification of the coefficient of `H3(nu) phi(nu)` in that tower
   with `fNL sigma0 S3 / 6`.
4. Separately, a functorial map from the Hilbert-space Haferkamp
   complexity to `C_LSS` under the AdS/CFT $\to$ FLRW transposition of
   A1/A3.

Steps (1)-(3) are plausible LSS-side TDA theorems, adjacent to Yip 2024
but not yet in that paper's text; (4) is the unsolved cosmological
modular-reconstruction problem already flagged in the ECI paper's
DECISIONS.md and quarantined to Appendix A.

## Step 6 — Verdict

- **Succeeds.** Setting up `C_ent` on the Gram--Charlier 1-point PDF is
  well-defined; the Hermite-orthogonality algebra through O(eps^2) is
  explicit and checks symbolically.
- **Fails.** The integrated entropy is quadratic, not linear, in the
  non-Gaussianity parameter. The pointwise complexity density is
  `H3(nu) phi(nu)` **times a non-constant weight**, not the Matsubara
  profile itself.
- **Handwaves.** The draft Eq.(C_LSS) (total persistence) is **assumed**
  to reproduce the Matsubara form in its leading fNL-shift; no theorem
  in the Yip 2024 / Calles 2025 literature currently establishes this
  linearity. Team A has not produced one.
- **Missing bridge.** Even if the LSS-side story were closed, the map
  from Haferkamp gate complexity to `C_LSS` requires the cosmological
  modular-reconstruction theorem that the paper explicitly declines to
  construct (GROUND_TRUTH.md Part E.1).

The honest reading: the differential-entropy attempt reproduces the
**basis element** `H3(nu) phi(nu)` at the pointwise level but neither
the **coefficient** nor the **linearity-in-fNL** of the Matsubara shift.
A6 as it stands is not derivable from UCG in this paper; it is at best
"consistent with" UCG's narrative framing.
