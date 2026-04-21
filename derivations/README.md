# Symbolic derivations

Companion symbolic artifacts for `paper/eci.tex`. Each entry corresponds to an equation or a claim in the manuscript that a reviewer might want to re-check automatically. Status column: `PENDING` means the notebook / script is planned, `OK` means committed and reproducible, `REV` means committed but needs re-verification after a paper revision.

| ID | Claim in paper | Tool | Status | File |
|---|---|---|---|---|
| D1 | Variation of the NMC action → Klein–Gordon `□χ − V′ − ξRχ = 0` | Cadabra2 | PENDING | `D1-kg-nmc.ipynb` |
| D2 | Full $T_{\mu\nu}^{(\chi)}$ with $-\xi G_{\mu\nu}\chi^2$ transferred to RHS | Cadabra2 | PENDING | `D2-stress-nmc.ipynb` |
| D3 | No-ghost condition $\xi_\chi \chi^2 / M_P^2 < 1$ from effective kinetic matrix | Cadabra2 + SymPy | PENDING | `D3-noghost.ipynb` |
| D4 | Scherrer–Sen relation extended to first order in $\xi_\chi$: $w_a(w_0; \xi_\chi)$ | SymPy + asymptotic expansion | PENDING | `D4-wa-w0-nmc.ipynb` |
| D5 | Phantom crossing $w=-1$ without ghost in the NMC sector | SymPy + plotting | PENDING | `D5-phantom-crossing.ipynb` |
| D6 | $\Delta N_{\mathrm{eff}}(c', \ell)$ from the KK graviton tower | SymPy | PENDING | `D6-deltaNeff-kk.ipynb` |

## Why this exists

The 2024 v3 draft relied entirely on hand-checking equations against textbook sources (Faraoni 2004, Capozziello–Faraoni 2011, Birrell–Davies 1982). That is insufficient in 2026: a referee will expect at least a computer-algebra notebook that re-generates the key equations under the stated conventions. This folder is the response.

## Stack

- **Cadabra2** (open source, Python-binding) for tensor variations in curved spacetime. `pip install cadabra2` or distribution package. Docs: <https://cadabra.science/>.
- **SymPy** for symbolic algebra and asymptotic expansions where Cadabra is overkill.
- **EinsteinPy** as a fallback for metric manipulations.
- **xAct/Mathematica** is not used (not open source).

## Running

```bash
cd derivations
jupyter lab
```

Every notebook is intended to be self-contained: import the tools, declare the metric and fields, re-derive the equation, and print a final cell with the PDF-ready LaTeX output matching the `.tex` file. Any divergence between the notebook output and the paper is a bug in one of the two.

## Verification policy

Before a release tag (`v4.1`, `v4.2`, ...), every derivation ID above must be either `OK` or explicitly flagged in the CHANGELOG. No silent `PENDING` at release time.
