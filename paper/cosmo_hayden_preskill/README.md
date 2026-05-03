# A Cosmological Hayden-Preskill Protocol

Standalone math.OA + quant-ph note (9 pages, compiled with `pdflatex`).

## Files

- `note.tex` — main LaTeX source (9 pages, ~520 KB PDF).
- `note.bib` — bibliography (19 entries, all arXiv-API verified 2 May 2026).
- `note.pdf` — compiled output (9 pages, ~520 KB).
- `verify.py` — sympy verification (5 algebraic claims, all PASS).
- `README.md` — this file.

## Build

```bash
pdflatex note.tex && bibtex note && pdflatex note.tex && pdflatex note.tex
```

Output: `note.pdf` (9 pages).

## Status

- The Krylov-Hubble identity at PLC (radiation FRW) is sympy-PASS.
- The HP form Δt = H⁻¹ log₂(d/k) with β=2π/H is sympy-PASS.
- The fidelity bound F ≥ 1 - O(k²/d²) (HP07 / Yoshida-Kitaev style) is sympy-PASS.
- The era×diamond table from the gauge audit is sympy-PASS.
- The MSS bound saturation at modular β=2π is sympy-PASS.

## What this is and is NOT

The result is a CONJECTURAL theorem: conditional on (H1) rigorous Block A1
on II_∞ crossed products and (H2) modular Lyapunov saturation on the FRW
vacuum (not just the CFT₂ vacuum). It is not a proven cryptographic
primitive, not a bound on cosmological observables, and not gauge-
unconditional — see `note.tex` §7 ("What this is NOT") for the full list.

## Recommended publication target

quant-ph short note (12-16 pp), with the math.OA paper closing (H1) as a
follow-up. PRD is also possible if the hep-th angle is emphasised. Do
NOT submit as a long flagship paper — the conditional-on-(H1)/(H2)
status is too prominent.

## Citations verified (2 May 2026, arXiv API)

All 19 bib entries arXiv-API checked:
HaydenPreskill07 (0708.4025), YoshidaKitaev17 (1710.03363),
Witten22CrossedProduct (2112.12828), CLPW23 (2206.10780),
ChenPenington24 (2406.02116), CMPT24 (2306.14732), Vardian26 (2602.02675),
Parker19 (1812.08657), AguilarGutierrez25 (2511.03779), MSS15 (1503.01409),
FaulknerLPW16 (1605.08072), FaulknerSperanza24 (2405.00847),
CHM11 (1102.0440 — corrected from the 0805:012 reference in piste1, which
was the wrong arXiv ID), ChenBouland24 (2404.16751), Schuster25 (2509.26310).
Connes 1973, Connes-Takesaki 1977, Hislop-Longo 1982, Bisognano-Wichmann 1975
are pre-arXiv and verified by journal reference only.

Internal references: `frwnote` (commit 72c3617), `piste1note`
(/tmp/piste1_hubble_kc.md and /tmp/piste1_gauge_audit.md).
