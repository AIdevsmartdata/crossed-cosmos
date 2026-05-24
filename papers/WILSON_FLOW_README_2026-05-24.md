# Wilson Flow SU(3) D=3 — JAX module

**Date** : 2026-05-24
**Author** : Kévin Rémondière (ORCID 0009-0008-2443-7166)
**Purpose** : Lüscher gradient flow integrator for SU(3) lattice gauge in D=3,
to extract α(β) without MK contamination or HMC breakdown at β ≥ 100.

---

## Files

| File | Role |
|---|---|
| `/tmp/voie1_calcs/wilson_flow_su3_d3.py` | Core module (RK3 Lüscher + Sigma + Z + E(t) + t* finder) |
| `/tmp/voie1_calcs/wilson_flow_test_run.py` | End-to-end pipeline: HMC therm + flow + smoothed ⟨P(t_ref)⟩ |
| `/tmp/voie1_calcs/WILSON_FLOW_README_2026-05-24.md` | This document |

## Verified arXiv reference

- **arXiv:1006.4518** — M. Lüscher, "Properties and uses of the Wilson flow in lattice QCD",
  JHEP 08 (2010) 071, CERN-PH-TH/2010-143. **VERIFIED** via WebFetch (arXiv abstract page)
  and the PDF (pages 1–4, 17–21) was inspected to extract equations (1.3), (1.4),
  Appendix A (notational conventions including `tr(T^a T^b) = -δ_ab/2` for
  Lüscher's anti-hermitian generators), and Appendix C eq. (C.2) for the RK3
  integrator coefficients (1/4, 8/9, −17/36, 3/4, −8/9, 17/36). All formulae in
  the module match Lüscher's eqs. (C.1)–(C.3).

## API

```python
import wilson_flow_su3_d3 as wf

# 1. Geometry (build once per L)
nbr = wf.build_neighbors_3D(L)

# 2. JIT step (compile once per L)
step = wf.make_wilson_flow_step(L, nbr)

# 3. One RK3 step from V_t to V_{t+eps}
U_new = step(U, eps)              # U shape (3*L^3, 3, 3) complex64

# 4. Full evolve t in [0, t_max]
result = wf.wilson_flow_evolve(U, L, t_max=2.0, eps=0.02,
                               use_clover=False, record_every=1)
# result : {'t_arr', 'E_arr', 'U_final', 'eps', 'n_step'}

# 5. Energy density at fixed U
E = wf.energy_density(U, L, use_clover=False)
E_cl = wf.energy_density(U, L, use_clover=True)

# 6. Reference flow time  t* such that  t*^2 . E(t*) = E_ref
t_star, traj = wf.find_t_ref(U, L, E_ref=0.3, eps=0.02, t_max=10.0)
# WARNING : 0.3 is the D=4 BMW value (PRL 1203.4469). For D=3 the
# reference constant MUST be re-calibrated empirically. We do NOT hard-code
# a D=3 default.

# 7. Smoothed plaquette at fixed flow time (for alpha extraction)
P_tref, U_flow = wf.smoothed_plaquette_at_t(U, L, t_ref=1.0, eps=0.02)
```

## Sanity tests (run via `python wilson_flow_su3_d3.py --L 4`)

All 4 tests **PASS** in the current implementation (verified 2026-05-24) :

| Test | Expectation | Result (L=4, eps=0.02, t_max=0.5) |
|---|---|---|
| 1. cold start | E(t) = 0 | max\|E(t)\| = 8.9e-8 (machine eps) |
| 2. hot start | E(t) monotone decreasing | 0/24 positive dE/dt steps; E: 2.99 → 0.85 |
| 3. SU(3) preservation | det V_t = 1 | max\|det - 1\| = 7.2e-7 (single-prec floor) |
| 4. reproducibility | same seed ⇒ same E(t) | max difference = 0.0 (bitwise) |

## Pipeline test (HMC + Wilson flow integration)

```bash
python3 /tmp/voie1_calcs/wilson_flow_test_run.py \
        --beta 25 --L 4 --n_therm 100 --n_meas 5 \
        --n_md 15 --t_max 2.0 --eps_flow 0.02 --t_ref 1.0
```

Output JSON `/tmp/voie1_calcs/wilson_flow_test_run.json` contains :
- `t_arr` : flow times
- `E_plaq_mean / E_clover_mean` : ⟨E(t)⟩ averaged over configs
- `t2E_plaq_mean / t2E_clover_mean` : ⟨t² E(t)⟩
- `P_at_tref_per_config` + `_mean / _err` : ⟨P(t_ref)⟩ smoothed plaquette

Verified on quick smoke (β=10, L=4, 30 therm, 3 meas, t_max=0.8) :
- HMC therm acc 87 %
- Wilson flow E_plaq drops 0.90 → 0.03 (factor 30) in t = 0.8
- Smoothed ⟨P(t_ref=0.5)⟩ = 0.9803 ± 0.0009 (UV noise washed out vs raw ⟨P⟩ = 0.71)
- Wall time 6 s on CPU (1 thread JAX)

## Sign-convention derivation (important)

Lüscher 2010 eq. (1.4) reads `dV/dt = -g_0^2 [∂_{x,mu} S_w(V)] V` with
`S_w(U) = (1/g_0^2) Σ_p Re tr{1 - U_p}`. Appendix A defines `T^a` as **anti-hermitian**
generators with `tr(T^a T^b) = -δ_ab/2`. Our HMC module uses **hermitian** Gell-Mann
generators `T_a = λ_a/2` with `tr(T_a T_b) = +δ_ab/2`. The relative sign and the
factor of `i` in the Lie derivative change between conventions, and the safest
approach is to **pin the sign empirically** : the flow must drive E(t) DOWN.

We define `Ω(x, mu) = U(x, mu) · Σ(x, mu)` where `Σ = Σ_nu [staple_fwd_nu + staple_bwd_nu]`
is our staple sum. We then set

    Z(V) = - TA[Ω],     TA[M] = (1/2)(M - M†) - (1/(2N)) tr(M - M†) I

and the RK3 step (Lüscher Appendix C eq. (C.2)) is

    Z_i = eps . Z(W_i)              ,  i = 0, 1, 2
    W_1 = exp( (1/4) Z_0 ) . W_0
    W_2 = exp( (8/9) Z_1 - (17/36) Z_0 ) . W_1
    W_3 = exp( (3/4) Z_2 - (8/9) Z_1 + (17/36) Z_0 ) . W_2
    V_{t+eps} = W_3

Empirical sanity test 2 (hot start) **verifies the sign** : 0 / 24 positive dE/dt
steps. Without the negation in `drift_Z` (or with `Ω = U · Σ†`), the flow goes
the wrong way (E increases) — both wrong signs caught during development and
the correct configuration is now baked in and protected by sanity test 2.

## Reference scale t_0 — honest caveat for D=3

In **D = 4** SU(3) the standard scale-setting reference is

    t_0^2 . ⟨E(t_0)⟩ = 0.3                  (Lüscher 2010 eq. (2.4), BMW 2012 PRL 1203.4469)

with the **clover-improved** E. For **D = 3** SU(3) we are NOT aware of any
literature-agreed reference constant : the proper procedure is

1. Pick the convention (plaquette vs clover for E ; lattice spacing units for t).
2. Empirically measure t² ⟨E(t)⟩(β) on a high-statistics scan over β.
3. Fit a smooth interpolant; pick a t_0 value such that the *scaling* of t_0(β)
   has the expected continuum-limit behaviour (asymptotic freedom in D = 3 is
   power-law, not log, so the scaling is qualitatively different from D = 4).

The `find_t_ref(...)` API ACCEPTS `E_ref` as a parameter and applies linear
interpolation on the (t, t²E) trajectory ; the default `E_ref = 0.3` is the
**D = 4 BMW value** and **should NOT be used blindly** in D = 3.

## Anti-fab notes

* arXiv:1006.4518 verified (title, author, journal, DOI, content of equations 1.3,
  1.4, A.2, A.3, A.4, C.1, C.2, C.3 cross-checked against the PDF).
* No new constants invented. The `E_ref = 0.3` default is flagged as D=4-only
  in both docstring and README.
* Sign of the drift is fixed by an empirical sanity test (test 2). Two wrong-sign
  combinations were caught and discarded during development before producing the
  final passing build.
* Clover-improved E is implemented from scratch following Lüscher 2010 Sec. 2.3
  (4-plaquette sum -> TA-projection -> F_munu = -(i/2) TA(Q) hermitian -> E =
  (1/V) Σ (1/2) tr F^2). The relative factor ~2 vs plaquette E observed in the
  test run is *qualitatively* the expected discretization-improvement factor for
  a smooth field at t > 0; the precise multiplicative constant differs and must
  be measured empirically before being used to set t_0.
* Matrix exp uses Taylor 15 terms + 1 scaling-squaring step (X -> X/2, exp,
  square). This is JIT-friendly (no Python control flow on traced values) and
  has been verified to preserve det V = 1 to single-precision floor (test 3).
* No external Python dependencies beyond JAX and NumPy. No download of arXiv
  preprint required at runtime (the constants are hard-coded with literature
  references in the docstrings).

## Production-run recommendations (for the gamer-PC GPU overnight run)

1. Pre-thermalize HMC for at least `n_therm = 500` at each β.
2. Use `n_meas = 20–50` configs separated by 2–5 HMC sweeps (decorrelation
   length ~ 1 / mass_gap; for β ~ 25–200 in D = 3 SU(3) this is typically
   2–5 sweeps).
3. Wilson flow each config with `eps_flow = 0.01` (Lüscher's stable value;
   integration error O(1e-6) per Appendix C) up to `t_max ~ 2.0` (covers the
   plateau region for L = 6..8).
4. Record E(t) on a coarse grid (every 5–10 steps; `record_every = 5`).
5. Record smoothed ⟨P(t_ref)⟩ at several `t_ref ∈ {0.5, 1.0, 1.5}` to
   cross-check robustness of the α extraction.
6. Use clover-improved E for the final scaling analysis (factor ~2 improvement
   in continuum-limit cancellation of a² corrections).
7. Fit `log[⟨P(t_ref)⟩(β) - P_∞]` vs `log β` for α; expected α = 3/4 for D = 3
   SU(3) per the framework prediction κ = 1/(2(D−1)).
