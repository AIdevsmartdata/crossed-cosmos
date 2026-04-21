# Numerical sanity checks

Light-weight numerical companions to `paper/eci.tex`. These are *not* the full MCMC / Boltzmann runs needed for a quantitative fit — they are toy-model checks that each quantitative claim lands in a physically admissible region. The full MCMC on DESI DR2 + Planck + ACT DR6 + Pantheon+ is listed on the roadmap and requires either a CPU cloud node (~$50) or a 3-day local run on the author's i5-14600KF.

| ID | Claim | Tool | Status | File |
|---|---|---|---|---|
| N1 | DESI DR2 $(w_0, w_a)$ central values land inside the thawing / NMC phase-space | NumPy + matplotlib | PENDING | `N1-w0wa-scan.ipynb` |
| N2 | $\Delta N_{\mathrm{eff}}$ from KK tower with $c' = 0.05$, $\ell \in [0.1, 10]\,\mu$m vs ACT DR6 bound $2.86 \pm 0.13$ | NumPy | PENDING | `N2-kk-neff.ipynb` |
| N3 | Cassini $\gamma_{\mathrm{PPN}}$ bound $|\gamma-1| < 2.3\times 10^{-5}$ vs NMC effective gravity with $\xi_\chi \chi_0^2/M_P^2$ at local densities | NumPy | PENDING | `N3-ppn-gamma.ipynb` |
| N4 | Biskupek $\dot G / G = (-5.0 \pm 9.6)\times 10^{-15}$/yr vs NMC prediction with $\dot\chi$ today | NumPy | PENDING | `N4-Gdot-G.ipynb` |
| N5 | $f_{\mathrm{EDE}} = 0.09 \pm 0.03$ bound on axion-like EDE at $z_c \sim 3500$ | SymPy + integration | PENDING | `N5-ede-fraction.ipynb` |

## Goal

Every quantitative line in the manuscript ("$c' \simeq 0.05$ compatible with ACT DR6", "$\xi_\chi \chi^2 / M_P^2 < 1$ leaves the Cassini bound intact", ...) should be re-checkable by running a small notebook. If the notebook disagrees with the paper, the paper is wrong.

## What this is NOT

- Not a cosmological parameter inference. That is `mcmc/` (future), using Cobaya + CLASS + AxiCLASS + an NMC patch.
- Not an N-body validation of the persistent-homology predictions. That is `tda/` (future), using GUDHI on Quijote subsamples.

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy sympy matplotlib
jupyter lab
```

## Verification policy

Same as `derivations/`: every ID `OK` or explicitly flagged before a release tag.
