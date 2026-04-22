# Effort & cost estimate — NMC patch and downstream MCMC

Date of estimate: 2026-04-21. Cloud pricing verified via web search (see §4).

---

## 1. Claude agent time to write the C patch

Assumes a fresh agent session starting from `NMC_patch_design.md` as the
only spec, and access to the hi_class source tree.

| Task                                                       | Hours |
|------------------------------------------------------------|-------|
| Clone hi_class, read background.c G_i switch, confirm API  | 0.5   |
| Add `nonminimal_coupling` enum + input parser block        | 0.5   |
| Add G_i case in background.c (~50 lines)                   | 1.0   |
| Add `V_chi_form = exponential|cosine` potential plumbing   | 0.5   |
| Write unit tests `test_nmc_zero` and `test_nmc_small`      | 1.5   |
| Add `G_eff(z,k)` and `η(z,k)` output hooks                 | 1.0   |
| Generate unified diff, documentation, .ini examples        | 0.5   |
| **Subtotal — Claude-only**                                 | **5.5** |

## 2. Human C debugging beyond what the agent can do

These are items the agent cannot self-validate without running the build:

| Task                                                        | Hours |
|-------------------------------------------------------------|-------|
| First compile (make class) + fix include/linkage errors     | 1–2   |
| Verify ξ=0 regression test passes to 1e-4 (debug if not)    | 2–4   |
| Tune `tol_background_integration` for ξ = 0.1 stability     | 1–3   |
| Verify QS switcher accepts the new case (method_qs_smg)     | 2–4   |
| Hand-check signs of α_M, α_B against Bellini–Sawicki        | 1     |
| Validate synchronous-gauge δφ IC for ξ ≠ 0                  | 2–3   |
| Commit, tag, document in project paper                      | 0.5   |
| **Subtotal — human debug**                                  | **9.5–17.5** |

**Total wall-clock to a working, tested patch: 15–23 hours** (0.5–1 working
week part-time).

---

## 3. MCMC runtime (DESI DR2 + Planck + ACT DR6 + Pantheon+)

Chains: 4 walkers × 20 000 steps, Gelman–Rubin R−1 < 0.05 convergence
criterion.

### Per-evaluation cost

A CLASS call for a Planck-precision setting (lmax=3000, non-linear Halofit,
ncdm=1, accuracy_default) typically takes **6–12 seconds** on a single modern
core. hi_class with Horndeski integration is ~1.5× slower, so assume
**12–18 s per evaluation** for NMC runs.

Likelihood evaluation (Planck plik_lite + ACT DR6 + DESI BAO + Pantheon+
SN): +2–4 s per step → **~15–22 s total per step**.

### Local — i5-14600KF, 12 physical cores (4P+8E per the lore / common
config; treat as 12 parallel CLASS workers)

- 4 chains × 20000 steps = 80 000 evaluations.
- Cobaya runs chains in parallel but CLASS is the inner cost.
- With 12 workers and one CLASS call at a time per chain (4 chains = 4
  parallel CLASS at best, unless we oversubscribe), effective throughput
  is ≈ 4 evals / 15 s = **960 evals/hour**.
- 80 000 evals → **~83 hours ≈ 3.5 days** of local machine uptime.
- In practice R−1 < 0.05 may converge before 20 000 steps; realistic
  wall-clock **2.5–5 days**.

### Cloud — AWS c7i.24xlarge (96 vCPU, 192 GB), $4.27/hr (us-east-1)

- 96 vCPU / 2 (SMT) ≈ 48 usable CLASS workers.
- Throughput ≈ 48 evals / 15 s = 11 500 evals/hr.
- 80 000 evals → **~7 hours**.
- Cost: 7 h × $4.27/hr ≈ **$30** per full MCMC run.
- Add ~30% overhead for initial adaptation / warm-up: **~$40**.

### RunPod (CPU instances not publicly listed; GPU-focused service)

RunPod does not advertise dedicated CPU instances comparable to c7i
(verified via web search 2026-04). Not recommended for CLASS MCMC.

### Lambda Labs

Similar to RunPod — GPU-focused. For CPU-heavy CLASS work, AWS c7i is
the canonical choice.

### Recommendation

- Prefer **local** for iterative development (free, no setup).
- Use **AWS c7i.24xlarge spot instance** for the final production chains
  (~$30 in spot mode, ~$40 on-demand). Budget **$100** for the full NMC
  analysis including 2 production runs + 1 rerun.

---

## 4. Cloud-price provenance

- AWS c7i.24xlarge: $3064–3127/month = **$4.27–$4.35/hour** (us-east-1).
  Source: CloudPrice, Economize, CloudOptimo (fetched 2026-04-21).
- AWS spot pricing historically 50–70% of on-demand → effective
  **$1.50–2.30/hour** in spot mode.
- RunPod: $0.34–3.49/GPU-hour; no competitive CPU tier.
- Lambda: GPU-focused, no CPU tier advertised.

---

## 5. Alternative path — avoid patching CLASS entirely

### 5.1 Proposal

Use **Cobaya's `theory.classy` wrapper** with a user-supplied external
table of `G_eff(k, a)` and `η(k, a) = Φ/Ψ` generated offline from the
analytic D14 closed-form expressions. The idea:

1. For each MCMC point (ξ, α, V0, chi_ini) generate a 2D table
   G_eff/G_N(k, a) on a fixed (50 × 50) grid using `derivations/D4-*.py`.
2. Feed this into Cobaya's Mead-halofit or an MGCAMB-style interface
   that accepts external MG functions.
3. Leave stock CLASS unmodified.

### 5.2 Feasibility assessment

**Partially feasible but not recommended for ECI A4.** Reasons:

- ✅ Cobaya+classy does support external μ(k, a), Σ(k, a) parametrisations
  via MGCosmoMC/MGCAMB-style hooks (there is a `mg_parametrization`
  option in some forks). Precedent: the f(R), DGP, and Hu–Sawicki
  analyses of 2021–2024 used this route.
- ❌ The D14 analytic G_eff is valid only in the **quasi-static sub-horizon**
  limit. Near horizon crossing the full perturbed ξ R χ term matters.
  For CMB-quality likelihoods (Planck + ACT DR6 cover ℓ up to ~4000,
  which spans both super- and sub-horizon scales at recombination),
  the QS-only approximation introduces a ~1–2% bias that is comparable
  to the ACT DR6 measurement precision.
- ❌ Background H(z) is also modified by NMC (the `−6 ξ H χ χ'` term in
  ρ_eff); the external-table approach can't fix H(z) without also
  intercepting the `background_solve` call, which means we're already
  ~halfway to patching CLASS.
- ❌ Even if we accept the ~1% bias at CMB scales, the MGCAMB route
  still requires writing a Python `Theory` subclass in Cobaya and
  validating it — probably ~half the total effort of just patching
  hi_class, with worse physics fidelity.

### 5.3 Recommendation

**Patch hi_class.** The alternative saves ~50% of the debug time at the
cost of physics correctness the likelihoods can see. For a paper claim,
the patched-hi_class route is the only defensible one.

The MGCAMB-style external-table route may still be useful as a **cheap
consistency check** during early exploration (ξ ∈ [−0.1, 0.1] rough scan)
before committing compute to the full MCMC.

---

## 6. Total budget

| Line item                                      | Cost / Time |
|------------------------------------------------|-------------|
| Claude agent time to write patch               | 5.5 h (free) |
| Human C debug + regression tests               | 10–18 h     |
| Full MCMC on AWS c7i (1 run, spot)             | ~$30        |
| MCMC reruns / sensitivity (budget)             | ~$70        |
| **Grand total**                                | **~20 h + $100** |

Local-only is also viable (~$0, ~5 days extra wall-clock).
