# posterior_v5.py — invocation guide

Script: `scripts/analysis/posterior_v5.py`
Purpose: posterior analysis of the ECI MCMC v5 chains (9 parameters,
DESI DR2 BAO + Pantheon+, 4 MPI chains).

---

## Prerequisites

Packages required (all present on the Vast.ai physics instance and in the
local `.venv-compute` environment):

```
numpy scipy matplotlib getdist
```

Optional (graceful degradation if absent):

```
anesthetic chainconsumer corner
```

No PolyChord, no web fetches, no Boltzmann code executed.

---

## Typical invocation (on Vast.ai, chains still writing)

Wait for R-1 < 0.02 before running the full analysis.
To do a quick sanity check while chains are still converging:

```bash
cd /root/crossed-cosmos   # or wherever the repo is on the instance
python scripts/analysis/posterior_v5.py \
    --chain-prefix /path/to/eci \
    --burnin 0.30 \
    --max-samples 500 \
    --no-plots
```

This reads at most 500 post-burnin rows per chain, skips the triangle plot,
and writes `notes/posterior_v5_<TODAY>/summary.md` within ~5 seconds.

---

## Full run after convergence (R-1 < 0.02)

```bash
python scripts/analysis/posterior_v5.py \
    --chain-prefix /path/to/eci \
    --burnin 0.30
```

Output directory: `notes/posterior_v5_<DATE>/` (auto-created) containing:

| File | Content |
|---|---|
| `triangle.pdf` | Triangle / corner plot, 9 sampled parameters, 68% + 95% contours |
| `marginals.pdf` | 1-D marginals with flat-prior overlay, 68% CI band |
| `summary.tex` | LaTeX table: mean, 68% CI, 95% CI, prior comparison |
| `summary.md` | Markdown summary + honest discriminator section + Levier #1 implications |

---

## After rsync from Vast.ai to local repo

```bash
# On local machine, after rsync:
rsync -avz vastai:/workspace/eci.{1,2,3,4}.txt mcmc/chains/eci_v50_run1/

python scripts/analysis/posterior_v5.py \
    --chain-prefix mcmc/chains/eci_v50_run1/eci \
    --burnin 0.30
```

---

## All options

```
--chain-prefix PATH   Prefix of chain files (default: <cwd>/eci)
--burnin FLOAT        Burn-in fraction to drop (default: 0.30)
--outdir PATH         Output directory (default: notes/posterior_v5_<DATE>)
--nchains INT         Number of chain files (default: 4)
--no-plots            Skip triangle + marginals; write only .tex and .md
--max-samples INT     Cap post-burnin rows per chain (for quick test runs)
```

---

## What the script does NOT do

- Does not run CLASS, AxiCLASS, or any Boltzmann code.
- Does not fetch data from the internet.
- Does not compute a Bayes factor via thermodynamic integration or nested
  sampling. The Savage-Dickey BF is already computed in
  `mcmc/_results/posterior_summary.json`; copy that number into summary.md
  by hand after the run, or extend this script to read that JSON.
- Does not invent posterior values. All numbers come from the chain files.

---

## Known uncertainties to resolve after the run

1. **Triangle plot backend**: tries getdist first, then corner, then
   matplotlib scatter. If getdist is installed but the MCSamples API has
   changed between versions, pass `--no-plots` and use the marginals only.

2. **Column order in chain files**: the script reads the header line
   (`# weight minuslogpost H0 ...`) directly. If Cobaya writes a different
   header format (e.g. with extra spaces or a different first token), edit
   `read_cobaya_chains()` to match.

3. **Weighted quantiles vs R-hat**: this script uses a simple Kish ESS and
   visual R-1 check (from `eci.progress`). For a formal convergence check
   use `cobaya.analysis` or `arviz`; the script does not replicate that.

4. **prior_dominated_fraction metric**: the chi-square divergence from flat
   is a coarse metric. A KL divergence or a proper boundary-adjusted test
   would be more rigorous, but requires a smooth posterior density estimate
   (e.g. KDE with bandwidth selection). Treat the pdom_score as a rough guide.

---

## Interpreting the output honestly

If `xi_chi` and `chi_initial` show `pdom_score < 0.15` (PRIOR-DOMINATED):
this is the expected outcome for BAO + SN without CMB. Do not interpret
it as a null detection of NMC coupling. It means the data do not constrain
these parameters, not that NMC is ruled out.

The Wolf+2025 reference Bayes factor (log B = 7.34 +/- 0.6 for NMC vs LCDM
on Planck PR4 + DR2 + Pantheon+) is NOT reproduced here because this run
lacks Planck. Any Bayes factor from this run is expected to be near 1
(inconclusive) for the NMC sector.

The (w0, wa) posteriors ARE expected to be informative from DESI DR2 alone,
consistent with the DESI DR2 dynamical dark energy preference.
