# V6-F2 notes — JT / FS24 cross-check

This commit documents the V6-F2 JT-gravity consistency cross-check of the v6
main inequality against Faulkner–Speranza 2024 (arXiv:2405.00847,
JHEP 11 (2024) 099).

Artifacts (introduced alongside the D2 CLT check in the preceding commit
b73bbcc due to a staging glitch; this commit carries the correct F2 label):

- `derivations/V6-F2-JT-consistency.py` — sympy symbolic setup, numerical
  check at 5 τ_R points. Run with `python3 derivations/V6-F2-JT-consistency.py`.
- `derivations/V6-F2-report.md` — side-by-side comparison + verdict.
- `paper/_rag/FaulknerSperanza2024.txt` — RAG cache of FS24 (arXiv:2405.00847).

## FS24 main GSL quoted verbatim

From `paper/_rag/FaulknerSperanza2024.txt`, Eq. (3.58):

> ⟨A_λ̃ / 4 G_N⟩ + S_λ̃^out − ⟨A_λ / 4 G_N⟩ − S_λ^out ≥ 0

(Also Eq. (3.57) and Eq. (4.31), identical in structure.)

## Honesty-gate disclosure

FS24 does not contain a labeled "Theorem 3.1". The paper's central result is
the monotonicity inequality (3.57)/(3.58)/(4.31). The V6-F2 script compares
v6 Eq.(1) against these inequalities, not against a paraphrased theorem.

## Verdict

**PASS** — v6 upper bound ≥ FS24 admissible rate at all τ_R ∈ {0, 0.25, 0.5,
1.0, 2.0}. Saturation at τ_R = 0 in the classical Θ=1 regime. No regime
examined makes v6 stricter than FS24.
