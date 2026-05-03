# D1 wave -- Lemma 3.4 (BD'78 anomaly transcription)

Date: 2026-05-03
Working dir: `/tmp/agents_2026_05_03_lecture_abc/D1_BD78_anomaly/`
Companion paper: `paper/k_frw_generalised_entropy/note.tex` (carve-out paper)
Supersedes: B1 wave `paper/k_frw_generalised_entropy/lemma34.tex`,
            B1 wave `paper/k_frw_generalised_entropy/sympy_lemma34.py`

## Deliverables produced
1. `lemma34_v2.tex` -- formal Lemma 3.4 proof, ready to drop into the
   carve-out paper as a replacement for `lemma34.tex`.
2. `sympy_anomaly_v2.py` -- machine verification, 28 sympy assertions
   PASS, 2 mpmath@200dps cross-checks PASS.
3. `notes.md` (this file) -- residual gaps, area-law comparison,
   citation-correction record.

## Summary of CORRECTIONS (v2 over B1)

### 1. Bibliographic corrections (caught while transcribing)
* The B1 lemma cites Bunch & Davies (1978) at "Proc. Roy. Soc. A 360
  (1978) 117-134" for the title "Stress tensor and conformal anomalies
  for massless fields in a Robertson-Walker universe". This is a
  CONFLATION of two distinct BD papers:
   - The actual paper with that title is BD (1977), Proc. Roy. Soc. A
     **356**, 569; DOI `10.1098/rspa.1977.0151`. (Found via INSPIRE-HEP
     and confirmed via royalsocietypublishing.org search.)
   - "Proc. Roy. Soc. A 360 (1978) 117" is a DIFFERENT BD paper:
     "Quantum Field Theory in de Sitter Space: Renormalization by
     Point Splitting", DOI `10.1098/rspa.1978.0060`.
* The user-provided identifier "Birrell-Davies, 'Conformal-symmetry
  breaking and cosmological particle creation in lambda phi^4 theory',
  Proc. Roy. Soc. A 361 (1978) 513-526, DOI `10.1098/rspa.1978.0223`"
  does NOT match any record in INSPIRE-HEP or in royalsocietypublishing.org
  search results. The actual paper "Conformal Symmetry Breaking and
  Cosmological Particle Creation in lambda phi^4 Theory" by Birrell &
  Davies is **Phys. Rev. D 22 (1980) 322**, NOT a 1978 PRSA paper.
  We therefore do NOT cite the unverified PRSA reference; instead we
  cite the textbook (Birrell-Davies 1982 monograph, §6.3) as the
  primary FRW-anomaly reference, plus the verified BD '77 PRSA paper
  for the explicit FRW-conformal-vacuum stress tensor.

This is an "n+1"-th hallucination caught (per the user's running tally
of citation hallucinations in the project). The fact-check chain:
  - INSPIRE-HEP API: no Birrell-Davies-coauthored paper in PRSA,
    only BD 1978 papers are PRD 18:4408 (Massless Thirring) and
    Nature 272:35.
  - Birrell-Davies "lambda phi^4" paper: PRD 22:322 (1980),
    listed correctly in INSPIRE-HEP.
  - PRSA `10.1098/rspa.1978.0223`: not retrievable; nearby DOIs
    (rspa.1978.0060, rspa.1978.0064, rspa.1978.0089, rspa.1978.0118,
    rspa.1978.0191) are unrelated to BD.

### 2. Mathematical corrections
**The B1 ansatz** for `<T_00>_anom` (used in `sympy_lemma34.py`
function `Tanom_scaling`):
```
   T00_anom = (1/(4*2880*pi^2)) * R_{mn}R^{mn}
```
is **dimensionally inconsistent**. In conformal frame with
`<T_00> = a^2 rho`, the proper energy density rho has dimension
`length^{-4}` and must scale as `a^{-4}` (curvature)^2 — i.e. the
B1 ansatz misses the `1/a^2` redshift implicit in the conformal-
frame conservation law.

**The v2 derivation** uses the correct Bunch-Davies prescription:
solving the 1st-order linear ODE
```
   rho'(eta) + 4 H(eta) rho(eta) = -H(eta) A_FRW(eta)
```
(obtained by combining trace anomaly `-rho + 3p = A` with conformal-
frame conservation `rho' + 3 H (rho + p) = 0`) via integrating
factor `a^4`:
```
   a^4(eta) rho_anom(eta) = - integral{ a^3 a' A_FRW deta }   (C_0 = 0).
```
This yields the **exact, sympy-verified, conserved** state-independent
piece, which is the unique BD'77 prescription.

### 3. Coefficient corrections
| Era | B1 (provisional) | v2 (sympy-EXACT) | eta_c power |
| --- | --- | --- | --- |
| Radiation | `+R^4 / (1800 eta_c^6)` | `+R^4 / (1800 eta_c^4)` | -4 vs -6 |
| Matter | `+R^4 / (150 eta_c^8)` | `-R^4 / (90 eta_c^4)` | -4 vs -8, sign flipped |

The radiation coefficient (1/1800) is preserved; the eta_c-power
**changes from -6 to -4**. The matter coefficient changes both in
magnitude (1/150 -> 1/90, i.e. larger by ~1.67x) **and in sign**
(+ -> -). Both eras now have uniform eta_c^{-4} scaling, which is
the dimensionally correct behaviour.

### 4. Sign discussion
The radiation Delta_anom is POSITIVE (vacuum energy of conformal
vacuum slightly above Minkowski, on the diamond) while matter is
NEGATIVE. The flip is driven by Box R: on radiation Box R = 0 and
the trace anomaly is purely R_{mn}R^{mn}/(2880pi^2) > 0; on matter,
Box R = -216/eta^12 dominates (more negative than R_{mn}R^{mn} =
+144/eta^12 is positive), so A_FRW becomes negative.

## Comparison to area-law (Solodukhin 2011)

For a conformally coupled scalar, the entanglement entropy across a
sphere has structure (Solodukhin LRR 14 (2011) 8, §5):
```
   S_EE = (1/(4 G_N)) * Area_phys * (1 + O(epsilon^2/Area))
        + c_log * log(Area_phys / 4 pi epsilon^2)  +  finite
```
with c_log = -1/360 for the conformally coupled scalar (Solodukhin
eq. 5.55). In the type II_oo crossed-product algebra of Witten 2021,
the leading divergent area term is absorbed into the trace
renormalisation, but `c_log` and the finite remainder are NOT
absorbed.

Our `Delta_anom` is the geometric (anomaly-driven) part of the
finite remainder. The dimensional ratio is:
```
   Delta_anom_rad / (Area_phys / 4 G_N) = G_N R^2 / (1800 pi eta_c^6)
   Delta_anom_mat / (Area_phys / 4 G_N) = -G_N R^2 / (90 pi eta_c^8)
```
At late cosmological times (eta_c -> infinity), this ratio
vanishes polynomially -- consistent with asymptotic Minkowski
behaviour of the conformal vacuum. At small times
(eta_c ~ R, near the Big Bang), the ratio approaches O(G_N) -- but
the conformal vacuum prescription itself becomes invalid in this
regime (singular Hadamard parametrix), so the lemma should not be
applied there.

## Open Question 3.5: Wald-Zoupas residual

The boundary `partial D_R` is a **Killing horizon of the conformally
mapped Minkowski metric** but **NOT of g_FRW**. The CHM modular flow
of Lemma 3.3 is conformally covariant, so the leading Delta_anom
piece is correctly given by Lemma 3.4. However, sub-leading
extrinsic-curvature corrections from the FRW-vs-Minkowski mismatch
on `partial D_R` survive at order `R K_extr ~ R H(eta_c)`:

* Radiation a=eta: `R H = R / eta_c`
* Matter a=eta^2: `R H = 2 R / eta_c`

For the carve-out paper's regime of interest (R << eta_c, small
diamond compared to cosmological time-scale), these are sub-leading
and Lemma 3.4 is sufficient. The full Wald-Zoupas analysis
(arXiv:gr-qc/9911095) requires:
  1. Identifying the FRW-bulk symplectic flux through `partial D_R`,
  2. Computing the extrinsic-curvature 2-form K_extr on `partial D_R`,
  3. Subtracting the conformally-mapped Minkowski reference.

This is documented as an Open Question in `lemma34_v2.tex` and
flagged for a follow-up companion note. The 8-11 day load-bearing
estimate from v6.0.28 was for the BD'78 transcription (now done);
the Wald-Zoupas residual is an additional ~3-5 day item that does
NOT block paper submission as long as we state the leading-order
result with the explicit sub-leading bound.

## Pre-existing files in working dir (B1 wave-3 Gemini consult)

The directory `/tmp/agents_2026_05_03_lecture_abc/D1_BD78_anomaly/`
contains two pre-existing files from a B1 wave-3 Gemini double-check:
* `gemini_prompt.md` -- the prompt sent to an external Gemini model.
* `gemini_doublecheck.md` -- the Gemini reply.

The Gemini reply contained TWO ERRORS that we override:
1. Gemini claimed `R_{μν} = -(2/η²) diag(0,1,1,1)` and
   `R_{μν}R^{μν} = 6/η^4` for radiation a=η. This is wrong.
   Sympy-verified: in conformal coordinates with mostly-plus signature,
   the Ricci tensor is `R_{μν} = diag(3/η², 1/η², 1/η², 1/η²)` and
   `R_{μν}R^{μν} = (1/a^4)(R_{00}² + 3 R_{ii}²) = 12/η^8`. The
   dimension is correctly L^{-8} because R_{μν}R^{μν} carries TWO
   inverse-metric contractions (each L^{-2}) on top of two factors of
   the Ricci tensor (each L^{-2}).
2. Gemini called the η^{-8} dependence "dimensionally inconsistent"
   and asserted η^{-4}. This is also wrong, for the same reason.

The B1 wave-3 sympy result `A_{rad} = 1/(240π²η^8)` is correct and
sympy-re-verified in `sympy_anomaly_v2.py` §III. The Gemini reply
should be DISCARDED on points (a) and (b); points (c) [kernel
integral 8πR^5/15] and (d) [shape-dependent O(R^2) suppression]
are correct.

This is a useful empirical data point: external LLM consults are
USEFUL for sanity-checking but can themselves contain errors that
sympy verification catches. The user's "no fudge factor" discipline
of mandatory sympy verification is the right escape valve.

## Cross-reference checks (negative results)

* **Steinhauer 2025-2026 saturation envelope** (BEC analogue gravity):
  C-agent landscape report flagged this as not found on arXiv. D1
  makes NO cross-reference to BEC analogue gravity; the conformal-
  anomaly contribution is a pure QFT-on-curved-spacetime result and
  is independent of analogue-gravity considerations. Recorded as a
  null cross-reference.
* **Riegert 1984 Phys. Lett. B 134:56** (non-local effective action
  for the trace anomaly): consulted but not cited; the v2 derivation
  uses only the local Wick-polynomial framework
  (Hollands-Wald 2001) which is sufficient for our scope.

## Summary for paper-submission timeline

* **B1 wave** (prior): "80% paper-ready". The lemma was structurally
  correct but had a "(*) provisional" rational coefficient and a
  bibliographic conflation in the BD'78 reference.
* **D1 wave** (this delivery): rational coefficient is now sympy-
  exact (no provisional markers); BD bibliography is corrected;
  user-supplied DOI 10.1098/rspa.1978.0223 is documented as
  unverified and replaced by the textbook reference; Open Question
  3.5 is formally stated.

**Status: submission-ready for the K_FRW + entropy carve-out paper
section 3.4** -- assuming the carve-out paper text is updated to
reflect the corrected coefficients (radiation 1/1800 eta_c^4 with
plus sign, matter 1/90 eta_c^4 with minus sign) and the corrected
BD bibliography. Recommend 1-2 days of editorial polish to
propagate these corrections through the paper body.

## File checksums (for the user's verification)

```
lemma34_v2.tex            ~17 kB  ~390 lines  formal proof
sympy_anomaly_v2.py       ~16 kB  ~330 lines  28 PASS, 0 FAIL
notes.md                  ~9 kB                this file
```

To regenerate verification:
```
python3 /tmp/agents_2026_05_03_lecture_abc/D1_BD78_anomaly/sympy_anomaly_v2.py
```
Should print 28 `[PASS]` lines + 2 `[PASS] mpmath@200 cross-check`
+ 1 `[INFO]` Solodukhin coefficient.
