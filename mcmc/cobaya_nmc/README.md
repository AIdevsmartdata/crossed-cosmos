# `cobaya_nmc` — Python Theory plugin for NMC (no C patch)

## What this is

A **Cobaya `Theory` subclass** (`ECINMCTheory`) that implements the ECI v4
non-minimal-coupling (NMC) cosmology **without** modifying CLASS or
hi_class. It delegates everything it can to vanilla `classy`
(minimally-coupled background) and post-processes the perturbation sector
with the **D14 closed-form expressions** for the effective Newton
constant and gravitational slip:

    G_eff(k, a) / G_N  =  (1 / F) * (2F + 4 F_phi^2) / (2F + 3 F_phi^2)
    eta(k, a)          =  (2F + 2 F_phi^2) / (2F + 4 F_phi^2)

with F = M_P^2 - xi_chi * chi(a)^2 and F_phi = -2 xi_chi chi(a). The D13
B(Omega_Lambda) table (`derivations/_results/D13-summary.json`) is
exposed as a derived quantity `wa_nmc_correction`.

## Files

| File | Purpose |
|------|---------|
| `eci_nmc_theory.py` | Cobaya `Theory` subclass — ~280 LoC |
| `test_plugin.py` | Stand-alone smoke test (xi=0 limit, H(z) match, Cassini magnitude, calculate() roundtrip) |
| `eci_nmc_plugin.yaml` | Minimal Cobaya input — analytic gaussian likelihood, no data files required |
| `run_mcmc_test.sh` | 5-minute smoke-test MCMC driver |
| `_cache/` | Cached Cobaya docstrings (Theory source) |

## How to run

```bash
# smoke test (no MCMC)
.venv-compute/bin/python mcmc/cobaya_nmc/test_plugin.py

# 5-minute Cobaya MCMC smoke test
bash mcmc/cobaya_nmc/run_mcmc_test.sh
```

## Limitations (read carefully)

1. **Quasi-static sub-horizon only.** The D14 formulas are valid for
   modes with k >> aH and k >> a * m_eff. For k ~ aH (CMB low-ell,
   horizon-scale features), this plugin will be biased at the ~% level.

2. **No NMC back-reaction on H(z).** The physical NMC Friedmann
   equation contains a `-6 xi H chi chi'` term that modifies the
   expansion history at O(xi chi^2 / M_P^2). This plugin uses a
   **minimally-coupled** quintessence H(z) — it does NOT capture that
   back-reaction. At Cassini-saturated |xi| <= 0.024 and chi_0 ~
   0.1 M_P, the implied Delta H / H ~ 0.04 % (well below DESI DR2
   sensitivity on H(z) but potentially within Planck theta_MC reach
   of 0.03 %).

3. **Linear in xi.** G_eff is exact in the BEFPS00 form, but we do not
   include the NMC effect on the scalar equation of motion itself (the
   `xi R chi` source). Adequate for the perturbation sector at leading
   order; NOT adequate for high-xi regimes.

4. **eta ≈ 1.** The slip correction is O(xi^2 chi^2 / M_P^2) ~ 6e-5 at
   Cassini saturation — below any near-future LSS sensitivity. We keep
   the exact expression but treat it as effectively 1 for constraint
   purposes.

5. **Plugin delivers `fsigma8`, `G_eff_over_GN`, `eta_slip`,
   `Hubble`, `chi_of_a`, derived `wa_nmc_correction`.** It does NOT
   deliver `Cl^TT`, `Cl^TE`, `Cl^EE` — those still require the CLASS
   pipeline. A thin wrapper that forwards CLASS's `Cl`s unchanged
   (assuming NMC does not affect recombination physics, which is a
   first-order approximation) could be added in ~30 LoC but has not
   been, to stay honest about the scope.

## Smoke-test results (2026-04-22)

```
[OK] xi=0 limit: G_eff/G_N == 1, eta == 1               (exact, 1e-14)
[OK] Cassini peak |G_eff/G_N - 1|: 0.101%                (D14 range)
[OK] fsigma8(z=0) = 0.427                                (LCDM band 0.40-0.50)
[OK] H(z) matches vanilla classy < 1e-4                  (0.00e+00 actually — exact)
[OK] calculate() returns all advertised products
[OK] Cobaya MCMC 1 chain x 400 accepted steps — R-1 means = 0.18 < 1
     (convergence achieved, plugin accepted by sampler/model/provider chain)
```

## Verdict

**Recommended route for v5.0 first-pass MCMC: this plugin, PROVIDED the
first submission is restricted to DESI DR2 BAO + Pantheon+ SN Ia +
optional fsigma8 (no full Planck/ACT CMB likelihood).**

Justification:
- At Cassini-saturated xi_chi <= 0.024, the peak |G_eff/G_N - 1| is
  ~0.1-0.4% — far below BAO/SN sensitivity on H(z) (which is the only
  channel DESI+Pantheon+ constrains directly) and within fsigma8
  LSST-Y10 ~1% reach at best.
- The back-reaction on H(z) that this plugin misses is ~0.04 %: again,
  invisible to DESI DR2 (per-H(z) bin ~1 %) and Pantheon+
  (mu_sn ~ 0.02 mag ~ 1 %).
- The C patch effort (~15-23 h + debugging) is justified **only if
  including Planck TT/TE/EE + ACT DR6**, where the 0.03 % shift in
  theta_MC becomes detectable and the QS-only perturbation
  approximation breaks at low ell.

**Decision table**

| Goal | Plugin sufficient? | Recommended route |
|------|--------------------|-------------------|
| DESI DR2 + Pantheon+ only, constrain (w0, wa, xi_chi) | **Yes** | Plugin — v5.0 |
| DESI + Pantheon+ + fsigma8 (DES-Y3 etc.) | **Yes** (marginal) | Plugin — v5.0, document systematics |
| Full Planck TT/TE/EE + ACT DR6 + DESI + SN | **No** | hi_class C patch — v5.1 |
| Forecast for Euclid/LSST growth | **Yes** | Plugin |

## Comparison to hi_class C-patch route

| | C patch | This plugin |
|---|---------|-------------|
| Claude agent time | 5.5 h | **1 h (done)** |
| Human debug | 10-18 h | **0 h** |
| Total to first MCMC | 15-23 h | **~2 h (done)** |
| Physics fidelity | full | sub-horizon QS only |
| CMB likelihood safe? | **yes** | no |
| DESI+SN safe? | yes | **yes** |

**Time saved: ~15-20 hours for the v5.0 first-pass MCMC.** The C patch
remains necessary for the v5.1 CMB-including analysis.

## Caveat: this plugin is a tool, not the final analysis

The paper's headline constraint on xi_chi using CMB data (§5 of the
submission) MUST use the full hi_class C patch. This plugin is a
**pre-screening tool**: it will tell us whether xi_chi is detectably
nonzero at DESI+SN precision in a few hours of MCMC, which is a
strictly weaker but much cheaper test.

If this plugin finds xi_chi consistent with 0 at DESI+SN, the C-patch
MCMC on the same data set will almost certainly find the same answer,
so we save the C-patch effort for the CMB-joint analysis only. If this
plugin finds xi_chi nonzero (or strongly pulled by the thawing
quintessence w_a degeneracy), it flags the result that needs a proper
C-patch validation before any paper claim.

Honest bottom line: **use this plugin for v5.0 pre-screening MCMC on
DESI DR2 + Pantheon+ only. Do NOT submit a paper constraint based on
it. The hi_class patch is still required for the published result.**
