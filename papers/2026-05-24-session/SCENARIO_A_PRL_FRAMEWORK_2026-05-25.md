# Framework PRL Scenario A — κ²(SU(2)) = 1/4 lattice confirmation

**Pre-draft prepared while MH production runs (PID 1586888).**

## Title options

1. "First lattice measurement of the Bisognano-Wichmann entropy coefficient
   in SU(2) Yang-Mills: support for κ² = 1/4"
2. "Direct measurement of the leading area-law coefficient in SU(2) lattice
   entanglement entropy"

## Abstract template (~150 words PRL)

We report the first lattice extraction of the leading area-law coefficient κ
governing the Rényi-2 entanglement entropy in 4D SU(2) Yang-Mills theory.
Using the Bisognano-Wichmann boost-generator observable evaluated on standard
Wilson lattice ensembles at β=2.4, we measure κ on L ∈ {8, 12, 16} via finite-
size scaling. We find κ = [VALUE] ± [ERR], consistent with the Bekenstein-
Hawking value κ_BH = 1/2 within [X]σ. This direct extraction circumvents the
α-integration cancellation of leading divergences that affects the Buividovich-
Polikarpov method (companion paper, Zenodo 10.5281/zenodo.20379361), and
provides the first numerical support for the conjecture κ²(SU(2)) = 1/4 in 4D
pure gauge theory. The result connects lattice gauge theory directly to the
black-hole entropy area law S = A/4.

## Sections (4 pages PRL)

1. **Introduction** — EE in gauge theory, κ²=1/4 hypothesis from gravity-EE
   correspondence (Jacobson 1995, Wald 1993, Bekenstein 1973), prior BP method
   limitations

2. **Method** — Bisognano-Wichmann modular Hamiltonian on lattice, clover
   T_{00}, strip-weighted observable

3. **Results** — L-scaling table, κ extraction with errors, comparison to 1/2

4. **Discussion** — Universality test (β-scan if done), comparison to BP
   sub-leading C(β) from companion paper, future work (SU(3), continuum extrap)

5. **Conclusion** — First direct support for κ²=1/4, opens path to lattice
   gravity-emergence tests

## Status κ²=1/4 Attempt B post-MH

| Scenario MH result | P(κ²=1/4 fundamental) |
|--------------------|-----------------------|
| A: κ ≈ 0.5 within 5-10% | 50-70% (+ MH evidence supports) |
| B: κ clean ≠ 0.5 | 5-10% (falsified simplest case) |
| C: noise dominates | 20-30% (unchanged) |

## Pre-allocated DOI/release plan

- Zenodo v7.6.0 : κ paper + MH code + data
- GitHub release v7.6.0 : same assets
- Bitcoin stamp PDF before submission
- Companion to β-scan paper v7.5.0

## Why this draft exists

While MH production runs (~1-3h), having the paper framework pre-ready means
that once κ extracted, we can fill in numbers + ship within hours, not days.
If Scenario A confirmed, the priority is RAPID publication via arXiv preprint
(needs Bauerschmidt endorsement still — separate Kevin action).

If Scenario B/C, this framework is repurposed honestly.
