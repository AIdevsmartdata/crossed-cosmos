# AxiCLASS Levier #1 EDE workaround tests — all 3 failed

**Date:** 2026-05-02
**Hardware:** Vast.ai EPYC 7V13 (Zen 3), contract 36023758
**Log:** `/tmp/axiclass_workaround.log` (on Vast)

## Background

Levier #1 (12-param: ξ_χ + EDE f_EDE + DD c'_DD on top of v5 9-param) requires
AxiCLASS for the EDE sector. AxiCLASS shooting fails on Zen 3 with a
floating-point precision issue in `background_init` (v3.3.0 build).

Three previously-proposed workarounds were tested in sequence:

| Test | Workaround | Result |
|---|---|---|
| 1 | RK45 evolver instead of default | **FAIL** — `shooting_failed` in `background_init(L:952)`, error in `fzero_N` (`input_shooting(L:990)`) |
| 2 | Loosened tolerances | **FAIL** — same error |
| 3 | RK45 + loosened tolerances | **FAIL** — same error |

All three produce identical error chain: `background_init` → `input_shooting`
→ `fzero_N`, suggesting the failure is in the shooting algorithm convergence
itself, not in the FP boundary tolerance the existing patch (`scripts/vastai/axiclass-fp-fix.patch`) addresses.

## Implication

Levier #1 (full 12-param with EDE) **remains blocked** on this hardware.
Levier #1B (10-param without EDE) is unaffected and continues to converge
on Vast (R-1 ~ 0.5 at 18.4k samples; chain still alive).

## Next options (deferred — not blocking)

1. **Backport CLASS 3.3.4 `fabs(dx)` fix:** The CLASS upstream fixed a similar
   shooting issue in 3.3.4. Requires finding the patch and applying it to
   AxiCLASS 3.3.0 source.
2. **Switch hardware:** Test on Intel-based Vast instance (may avoid Zen 3
   FP corner case).
3. **Skip EDE:** Run Levier #1 with only ξ_χ and c'_DD (no f_EDE). Loses one
   tension-resolution mechanism but keeps the joint MCMC framework.
4. **Different EDE implementation:** klein_axiclass alternative or hi_class
   ULA module.

None of these is urgent — Levier #1B is the headline run; Levier #1 with EDE
is a follow-up enhancement.
