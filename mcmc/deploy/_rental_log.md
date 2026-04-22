# Vast.ai Rental Log — ECI MCMC

One row per rental. Append chronologically. Commit after each teardown.

| Date (UTC) | Target YAML | Host CPU | Spot $/h | Duration | Wallclock | $ total | Result | Notes |
|------------|-------------|----------|----------|----------|-----------|---------|--------|-------|
|            |             |          |          |          |           |         |        |       |

## Column conventions

- **Date (UTC)**: ISO-8601 date of instance destruction.
- **Target YAML**: basename under `mcmc/params/` (e.g. `eci_nmc_optimized`).
- **Host CPU**: `EPYC 9965` / `EPYC 9654` / `EPYC 7763` / etc.
- **Spot $/h**: price quoted at instance creation.
- **Duration**: billed time (`<h>h<m>m`).
- **Wallclock**: from `cobaya-run` start to last checkpoint
  (may be shorter than Duration if setup + tar took time).
- **$ total**: final dashboard charge.
- **Result**: `OK` (R-1 < target), `PARTIAL` (preempted, resumed elsewhere),
  `FAIL` (bug / crash / abandoned).
- **Notes**: preemption count, final R-1, anomalies, link to chains tarball
  checksum.
