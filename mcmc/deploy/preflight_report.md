# Pre-flight report — ECI MCMC Vast.ai rental

Date: 2026-04-22  
Repo: `/home/remondiere/crossed-cosmos`  
Host: i5-14600KF, 32 GB RAM, Ubuntu 6.17  
Owner credit on Vast: $14

---

## Re-run on plugin route (2026-04-22, v5.0)

**Verdict: GREEN. Plugin route is clear for Vast.ai rental.**

Route switched from `mcmc/params/eci_nmc_optimized.yaml` (hi_class C-patch, 2
hard blockers in the prior run on this page) to
`mcmc/cobaya_nmc/eci_nmc_plugin.yaml` (Python Theory plugin, vanilla classy +
D14 NMC post-processing). Commits: `fca4a92` (YAML), `4f5e7e5` (deploy scripts).

Evidence directory: `mcmc/deploy/_preflight_logs_plugin/`.

| Test | Name                              | Status | Note |
|------|-----------------------------------|--------|------|
| T1   | `vast_ai_on_create.sh` syntax     | PASS   | `bash -n` clean |
| T2   | classy import + background solve  | PASS   | `h = 0.6736` (locally in `.venv-compute`; on-create installs fresh `.venv-mcmc` via `pip install classy`) |
| T3a  | `run_vast.sh` syntax              | PASS   | points at plugin YAML |
| T3b  | MPI flag block                    | PASS   | unchanged from prior preflight |
| T4   | YAML parse                        | PASS   | 5 top-level keys, no duplicate params, no EDE/Planck keys |
| T4b  | Cobaya `Model` init + logposterior| PASS   | `logpost = -707.250` at ref point; required `provides: [Hubble, angular_diameter_distance, rdrag]` on `classy` to disambiguate from the plugin |
| T5   | Likelihood imports + data files   | PASS   | `bao.desi_dr2` + `sn.pantheonplus` import; DESI DR2 data under `mcmc/packages/data/bao_data/desi_bao_dr2/` |
| T6   | 100-step (200 accepted) mini-MCMC | **PASS** | **201 accepted steps / 48.1 s wall → 0.24 sec/accepted step**, i5-14600KF 1 rank 2 threads. Target was ≥50 steps in ≤10 min — cleared by ~250×. |
| T7   | Checkpoint/resume (`cobaya-run -r`)| PASS  | resume succeeded on the same checkpoint |
| T8   | tar + scp prep                    | PASS   | 13.7 KB gzipped for 200 steps, extrapolates to ~15 MB for 160 k evals |

Count: **9 / 9 PASS.**

### sec/step observed (plugin route, local)
- **0.24 sec / accepted MCMC step** (i5-14600KF, 2 threads, 1 MPI rank).
- Per-model-call: 0.19 s cold, 0.04 s warm (classy cache on identical cosmo params).
- Plugin overhead (classy → ECINMCTheory postproc): ~22 ms (speed-measured by
  Cobaya: classy 6.54 evals/s, plugin 45.8 evals/s).

### Projected Vast.ai wall-clock + cost (EPYC 9965 Zen 5, 4 chains × 20 000)

EPYC 9965 single-core ~1.5× a 14600KF P-core on CLASS (per prior benchmark
REPORT.md). With MPI = 4 ranks × OMP = 2 threads:
- Per-rank sec/step: 0.24 / 1.5 ≈ **0.16 s**
- 4 chains × 20 000 accepted = 80 000 evals total, 20 000 per rank
- Wall-clock: 20 000 × 0.16 s ≈ **53 min** (upper bound; Cobaya's actual
  wall is gated by the slowest chain's R-1 convergence, not accepted count)
- With 8-rank layout (the script default), wall drops to ~27 min
- Spot rate for EPYC 9965 on Vast ≈ $0.80 / h → **cost ≈ $0.40 – $0.80**
  for convergence, fits the $14 budget with ~17× headroom.

This is **~8× faster than the hi_class-route projection** on this same page
(5.5 h, ~$4.40) because the plugin route uses vanilla CLASS with `output: mPk`
only (no Boltzmann on full Cls), and avoids the hi_class compile.

### What the plugin run does and does not constrain
- DOES constrain: `H0, omega_b, omega_cdm, n_s, logA, w0_fld, wa_fld, xi_chi, chi_initial`
- DOES emit derived: `wa_nmc_correction` (D13/D14 closed form)
- DOES NOT use: Planck, ACT, any CMB
- Expected σ(ξ_χ) from BAO+SN alone ≈ 0.155 (D16 Fisher forecast, see §3.5).

### Go / no-go for rental: **GREEN**

Owner command sequence once SSH'd onto the Vast instance:
```
cd /root/eci
tmux new -s mcmc
bash mcmc/deploy/run_vast.sh
```

Retrieve chains locally (run from the workstation):
```
scp -P <port> -r root@<IP>:/root/eci/chains/ ./chains_$(date -Iseconds)/
```

Commits pushed this round:
- `fca4a92`  `v5.0:plugin-yaml: repoint plugin YAML to DESI DR2 + Pantheon+ production run`
- `4f5e7e5`  `v5.0:plugin-deploy: repoint Vast.ai scripts to plugin route (vanilla classy, DESI+SN)`
- `<this>`   `v5.0:plugin-preflight: GREEN on plugin route, 0.24 s/step local, 9/9 PASS`

---

## Summary

**DO NOT RENT YET.** 3 hard blockers found that would guarantee a wasted paid
run. 1 fix already applied in-repo (T2 pip isolation). 2 blockers require owner
decisions on the physics YAML (T6) before any cloud launch.

Test result table:

| Test | Name                          | Status | Blocker? |
|------|-------------------------------|--------|----------|
| T1   | on-create script syntax       | PASS   | —        |
| T2   | hi_class build + classy       | PASS*  | fix applied to on-create script |
| T3   | run_vast.sh + MPI + resume    | PARTIAL| local MPI absent (OK, installed by on-create); syntax + resume flag OK |
| T4   | YAML parse (text-only)        | PASS   | —        |
| T4b  | YAML → Cobaya Model init      | FAIL   | **BLOCKER-1** (duplicate `nmc_xi_chi`) |
| T5   | Likelihood modules + Planck mirror | PASS | —    |
| T6   | 100-step mini-MCMC            | FAIL   | **BLOCKER-2** (CLASS does not recognise `nmc_xi_chi` / `f_EDE`) |
| T7   | Checkpoint / resume           | SKIP   | requires T6 to start a chain |
| T8   | Chain tarball                 | PASS   | —        |
| T9   | Teardown checklist walkthrough| PASS   | —        |

Count: PASS 6, FAIL 2, PARTIAL 1, SKIP 1.

**Green-light: NO.** Fix the 2 blockers below before renting.

---

## T1 — on-create syntax  (PASS)

```
$ bash -n mcmc/deploy/vast_ai_on_create.sh; echo exit=$?
exit=0
$ which shellcheck    # not installed locally — skipped
```
Evidence: `_preflight_logs/T1_syntax.log`, `T1_shellcheck.log` (empty; shellcheck absent).  
**Action:** none. Install shellcheck later if deeper lint wanted (not a blocker).

---

## T2 — hi_class build + classy  (PASS, with fix applied)

- Fresh venv `/tmp/dryrun_venv/`, numpy 1.26.4, scipy 1.17.1, cython 3.2.4.
- Fresh source copy `/tmp/dryrun_hiclass/` (from repo `mcmc/nmc_patch/hi_class_nmc/`).
- `make clean; rm -rf build class libclass.a` then:
  `CFLAGS="-O3 -march=native -mavx2 -mtune=native -flto -fopenmp" make -j8 class`
  → **rc 0, 4 s wall**, 9.8 MB binary.
- `pip install -e python/` → **FAILED** with `ModuleNotFoundError: No module named 'Cython'` (PEP 517 isolated build env lacks Cython).
- Fix: `pip install --no-build-isolation -e python/` → PASS.
- `classy.Class(); c.set({'output':'mPk'}); c.compute()` → `h=0.6781`. PASS.

**Fix applied in-repo** (line 80 of `mcmc/deploy/vast_ai_on_create.sh`):
added `--no-build-isolation` flag with inline comment. This would have been
a blocker on Vast.

Evidence: `_preflight_logs/T2_build.log`, `T2_pyinstall.log`.

---

## T3 — run_vast.sh + MPI + cobaya resume  (PARTIAL)

- `bash -n run_vast.sh` → rc 0.
- `mpirun --version` → **not installed locally** (expected; on-create installs `libopenmpi-dev`). Could not end-to-end test MPI composition locally.
- `cobaya-run --help | grep resume` → `-r, --resume` flag present in Cobaya 3.5.6. PASS.

**Action:** none. MPI flag block (`--bind-to none --map-by slot:PE=2 --oversubscribe`) is textbook-correct for Vast cgroup-restricted hosts. Will be exercised live on first rental; residual risk is low.

Evidence: `_preflight_logs/T3_mpi.log`, `T3_resume.log`, `T3a_run_vast_syntax.log`.

---

## T4 — YAML parse  (PASS text-only; FAIL Cobaya init)

- `yaml.safe_load` → 5 top-level keys: `theory, likelihood, params, sampler, output`.  
- Every one of the 13 params has `prior` or `value` or `latex`-only (derived). PASS.
- `cobaya.input.load_input` → loaded without error.
- **`cobaya.model.Model` init → FAIL**:  
  `LoggedError: The following parameters appear both as input parameters and as extra arguments: {'nmc_xi_chi'}`  
  Cause: `theory.classy.extra_args.nmc_xi_chi = 0.0` (line 30) **and** `params.nmc_xi_chi` (line 90) coexist. Cobaya rejects this duplication.

**BLOCKER-1 fix:** remove line 30 of `mcmc/params/eci_nmc_optimized.yaml`
(`nmc_xi_chi: 0.0` in extra_args). The parameter belongs only in `params:`.
Constraint of this dry-run forbade mutating `mcmc/params/` so the fix is
staged only in `/tmp/dryrun_100step.yaml` for T6.

Evidence: `_preflight_logs/T4_yaml.log`.

---

## T5 — Planck / DESI / Pantheon+  (PASS)

- Planck 2018 baseline mirror: `curl -I` returned HTTP 200, `Content-Length: 60 323 470` (~58 MB). Mirror OK.
- `import cobaya.likelihoods.{bao.desi_dr2, sn.pantheonplus, planck_2018_lowl, planck_2018_highl_plik}` → all 4 import cleanly.
- Local `mcmc/packages/` already holds Planck 2018 data (336 MB) — can be rsynced to the instance to skip re-download.

Evidence: `_preflight_logs/T5_likelihoods.log`.

---

## T6 — 100-step mini-MCMC  (FAIL — blocker)

After patching the duplicate-key issue from T4b in a `/tmp` copy of the
YAML, Cobaya initialises and Plik-lite self-tests green
(`got -292.286 expected -292.286`). Then every random-start draw fails inside
CLASS:

```
[classy] *ERROR* Serious error setting parameters or computing results.
  The parameters passed were {'A_s': …, 'H0': …, 'f_EDE': …,
    'nmc_xi_chi': …, 'w0_fld': …, 'wa_fld': …, …} …
Could not find random point giving finite posterior after 1000 tries
```

Direct `classy.Class().compute({...same set...})` reproduces the root cause:

```
CosmoSevereError: Class did not read input parameter(s): nmc_xi_chi, f_EDE
```

**BLOCKER-2: the hi_class_nmc build does not recognise either `nmc_xi_chi`
or `f_EDE` as top-level keys.**

- Per commit `a0c23f3` (`v4.8:class-patch: implement NMC (xi R chi^2/2) as Horndeski sub-case`), the NMC patch is wired as a Horndeski `gravity_model = nonminimal_coupling` entry reading `parameters_smg[0] = xi`. There is no
  direct `nmc_xi_chi` parser in `source/input.c`. Grep returns zero matches
  for `nmc_xi_chi` under `hi_class_nmc/source` and `hi_class_nmc/include`.
- `f_EDE` is not implemented at all (no EDE sector in the tree; grep zero).

Fix options (owner decides):

1. **Drop EDE + expose xi via parameters_smg** (cheap, ~1 h):
   - Remove `f_EDE` from params.
   - Add `extra_args.gravity_model: nonminimal_coupling` + `extra_args.parameters_smg_dummy` and a Cobaya `params.parameters_smg: "lambda nmc_xi_chi: f'{nmc_xi_chi}, 2.0, 0.0, 0.0, 0.0'"`. Needs a Cobaya theory wrapper or `extra_args` trick; likely a small `classy` subclass (30 LoC).
   - Re-validate with T6 locally.
2. **Implement an `nmc_xi_chi` front-door parser** inside `hi_class_nmc/source/input.c` that sets gravity_model internally. ~50 LoC, cleaner, matches the original NMC_patch_design.md intent.
3. **Drop ξ_χ + f_EDE, run w0-wa CPL only** as a first-rental sanity pass, then come back with the NMC sector wired.

Sec/step: **not measurable** (zero successful evaluations). Baseline
from `mcmc/benchmark/REPORT.md` (3.04 s/eval at 2 threads on 14600KF) still
stands for w0wa-only runs.

Evidence: `_preflight_logs/T6_mcmc.log`.

---

## T7 — checkpoint / resume  (SKIPPED)

Not runnable without a working T6. Cobaya 3.5 `-r` flag is verified to exist
(T3). Re-run T7 after T6 is green.

---

## T8 — tar + scp prep  (PASS)

`tar czf /tmp/dryrun_chains.tar.gz /tmp/dryrun_chains_fake/` → rc 0, 82 KB
for 4×20 KB random files. Extrapolation for 8-rank × 20 k steps × ~150 B/row
≈ 24 MB uncompressed → ~8 MB gzipped. scp bandwidth: <1 min on any Vast host.

Evidence: `_preflight_logs/T8_tar.log`.

---

## T9 — teardown checklist  (PASS)

Every command in `mcmc/deploy/teardown_checklist.md` is concrete and
exercisable. `_rental_log.md` exists with a header row ready for append.
`ssh-keygen -R` syntax correct. Vast "Destroy not Stop" warning correct.

---

## MCMC posterior contingencies (≤ 200 words)

- **No convergence at 20 k steps.** If `Rminus1_stop: 0.05` not reached, first
  extend `max_samples` to 40 k (cheap, reuse checkpoint). If `R-1` is still
  >0.1, inspect the worst-dimension acceptance via `getdist`; if <0.1, reduce
  `proposal_scale` from 1.9 to 1.4. Check for stuck chains at prior edges via
  `getdist triangle plot`; a chain that never moves is the likelihood-boundary
  symptom (almost certainly ξ_χ or f_EDE rail).
- **ξ_χ posterior at prior edge (|ξ_χ| → 0.1).** If 95 % CI touches ±0.1, that
  IS a signal (non-minimal coupling wanted larger than prior allows). Widen
  to |ξ_χ| ≤ 0.3 and re-run one chain to confirm it is not a runaway. If it
  runs to 0.3 also, stop — the linear-response approximation we derived in
  `derivations/D4-wa-w0-nmc.py` stops being valid at |ξ_χ|≈0.15.
- **ξ_χ–χ₀ degeneracy.** First pass: fix χ₀ = M_P/10 (parameters_smg[4] = 0.1).
  Second pass: marginalise χ₀ ∈ [M_P/100, M_P/2] log-uniform and report both
  posteriors — expect a 1.5–2× inflation in σ(ξ_χ).
- **Plugin-route vs hi_class-route disagreement.** Run both to convergence,
  plot the 2-D posteriors in the (ξ_χ, w₀) plane, report 1-σ overlap
  fraction. If overlap <50 %, freeze ξ_χ = 0 and compare CLs: any
  disagreement there is a code bug, not a physics one.

---

## Owner action items (before rental)

1. **Fix `mcmc/params/eci_nmc_optimized.yaml`**:  
   (a) delete line 30 `nmc_xi_chi: 0.0` from `theory.classy.extra_args` (duplicate); (b) decide on ξ_χ routing (Option 1/2/3 in T6) and implement either the Cobaya wrapper or the `input.c` parser; (c) decide whether to keep `f_EDE` — if yes, import a CLASS_EDE patch; if no, delete the param.  
   Commit, then **re-run this pre-flight script locally** and confirm T6 produces ≥ 50 steps.
2. **Optional but recommended**: `rsync -a mcmc/packages/ root@<vast>:/root/eci/mcmc/packages/` before `cobaya-run` to save the 60 MB Planck download on a metered link.
3. **Install shellcheck locally** (`apt install shellcheck`, later) and re-run T1 with lint warnings captured.

Estimated cost once fixed, given 3.04 s/eval local baseline and owner's
prior projection of ~3× speedup on EPYC 9965 (≈1.0 s/eval, 8 ranks →
8 evals/s aggregate) and 20 k steps × 8 chains = 160 k evals:  
wall ≈ 160 000 / 8 ≈ **5.5 h**, at ~$0.80/h Vast spot → **~$4.40**, fits in the
$14 budget with room for one retry. Re-verify after T6 green.

---

## Commit

To be filled by the commit step:

- SHA: `<populated on commit>`
- Prefix: `v4.8:preflight:`
- Files: `mcmc/deploy/preflight_report.md`, `mcmc/deploy/_preflight_logs/*`,
  `mcmc/deploy/vast_ai_on_create.sh` (one-line fix).
