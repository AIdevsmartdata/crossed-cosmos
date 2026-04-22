# ECI v6.0 — formal companion (JHEP-track)

**Release tag.** `v6.0.0`
**Commit.** `557ab7d`
**Date.** 2026-04-22

A formal 7-page companion paper to the v5 phenomenological framework paper
(v6 Zenodo version DOI [10.5281/zenodo.19699006](https://doi.org/10.5281/zenodo.19699006); concept DOI [10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398); v5 version DOI [10.5281/zenodo.19696017](https://doi.org/10.5281/zenodo.19696017)).
This is **not a successor** to v5; the two papers operate on orthogonal
tracks.

## What is this

A differential upper bound on the rate of generalised entropy along the
modular flow of a type-II crossed-product observer algebra:

$$
\frac{dS_{\mathrm{gen}}[R]}{d\tau_R}
\;\le\;
\kappa_R \cdot \mathcal{C}_k[\rho_R(\tau)]
       \cdot \Theta(\mathrm{PH}_k[\delta n(\tau)])
$$

with a tightened logistic envelope
$\kappa_R\mathcal{C}_k(1-\mathcal{C}_k/\mathcal{C}_k^{\max})\Theta$ in the
scrambling regime (Prop. 1). A second formal contribution is an explicit
dequantisation map bridging the type-II factor to classical persistent
homology.

## Relation to v5

| | v5.0 (EPJ C, phenomenological) | v6.0 (JHEP, formal) |
|---|---|---|
| Pages | 14 | 7 |
| Track | astro-ph.CO / cosmology | hep-th / mathematical physics |
| Data | DESI DR2 + Pantheon+ MCMC | None — pure formalism |
| Main result | ξ_χ = 0.003 +0.065/-0.070 | dS_gen/dτ_R ≤ κ_R C_k Θ |
| Falsifier | NMC quintessence deviations from ΛCDM | None (D18/D18b killed fσ_8 × Θ(PH_2)) |
| Audience | Cosmologists | Mathematical physicists |

## Audit trail

- Adversarial v1 → 3/8 VALID attacks → 9 editorial fixes (commit `3a252a4`)
- Adversarial v2 targeted → 3 MINOR-FIX edits (commit `a8fb6d6`)
- Peer-eco panel (Gemini Pro + Flash + Magistral): 2 MINOR / 1 MAJOR / 0 REJECT
- §6 programmatic outlook added and adversarially reviewed → SHIP (commit `5f5a9f2`)
- **Adversarial v3 full 7-page pre-deposit sweep** → SHIP → GO (commit `557ab7d`)
- Pre-write audit pipeline `derivations/V6-claims-audit-pipeline.py`: 18/18 gates PASS

## Computational realisation

Four companion scripts reproduce the numerical checks:
- `derivations/V6-dequantisation-map.py` — toy type-II_1 factor, 3 asserts pass
- `derivations/V6-lemma-submultiplicativity.py` — submultiplicativity Lemma 1, 3 asserts pass
- `derivations/V6-F2-JT-consistency.py` — JT consistency vs Faulkner-Speranza, PASS
- `derivations/V6-D2-CLT-convergence.py` — CLT convergence at N∈{12,16,20}, PASS

## What this paper is not

- Not peer-reviewed.
- Not a cosmological prediction (see PRINCIPLES.md V6-4; the D18/D18b
  falsifier fσ_8 × Θ(PH_2) was killed at DR3+Euclid precision).
- Not a theorem for the main postulates M1/M2/M3 (all explicitly labelled
  POSTULATE / ANSATZ / CONJECTURAL).
- Not a revolution: a formal stone placed correctly in a wall under
  construction.

## Deposit status

- GitHub: this release.
- Zenodo: auto-archived on tag creation (toggle the repo at
  https://zenodo.org/account/settings/github/ if not already enabled).
- arXiv: deferred — endorsement for `hep-th` pending.
- JHEP: submission after arXiv ID becomes available.

## How to cite (pre-arXiv)

```bibtex
@misc{Remondiere2026ECIv6,
  author  = {Remondi\`ere, Kevin},
  title   = {From {Faulkner}--{Speranza} to a complexity-bounded
             generalised second law in type-{II} crossed-product algebras},
  year    = {2026},
  howpublished = {GitHub + Zenodo},
  url     = {https://github.com/AIdevsmartdata/crossed-cosmos/tree/master/paper/v6},
  orcid   = {0009-0008-2443-7166}
}
```

## Author

**Kevin Remondière** — Independent Researcher
ORCID: [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)

## License

Text: [CC BY 4.0](../../LICENSE).
