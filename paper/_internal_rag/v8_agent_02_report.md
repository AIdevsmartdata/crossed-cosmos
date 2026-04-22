# v8_agent_02_report.md — Legendre K_R ↔ C_BS

**Date:** 2026-04-22  
**Artefact:** `derivations/V8-agent-02-legendre-complexity.py`  
**Verdict:** NO-RELATION

## Setup

Toy type-II_1 factor: 4+4 qubit XXZ modular Hamiltonian (same seed/construction
as `V6-lemma-submultiplicativity.py`).  
K_R = partial-trace restriction of H_mod to the 4-qubit observer subsystem R (16×16).  
Thermal family: rho_beta = exp(-beta K_R)/Z for beta in [0.1, 10].

## Results

| Quantity | Definition | Range over beta scan |
|----------|-----------|----------------------|
| L[K_R](beta) | sup_beta (beta <K_R> - F(beta)) = S_vN(rho_beta) | [0.693, 2.762] |
| C_BS(beta) | 1/Tr(rho_beta^2) — Nielsen purity proxy | [2.000, 15.659] |
| Ratio L/C_BS | | [0.176, 0.476] |

Relative range of ratio: **95.9%**. No stable proportionality constant exists.

## Verdict: NO-RELATION

L[K_R] = S_vN is logarithmically bounded (max ln 16 ≈ 2.77).  
C_BS ~ 1/purity grows linearly in effective Hilbert-space dimension.  
Their ratio drifts by nearly 3× across the beta scan, peaking at intermediate
beta ~ 1.7 and collapsing at both limits.

The Legendre transform of K_R recovers the thermodynamic entropy (von Neumann),
not the Brown-Susskind complexity. These are structurally distinct functionals:
entropy is concave in beta; complexity (purity inverse) is convex. No
multiplicative constant bridges them over the full thermal family.

PRINCIPLES rules 1 and 12 respected: result is negative, reported honestly.
