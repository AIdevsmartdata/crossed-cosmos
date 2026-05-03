# T2 across Type A Bianchi (II, VI_0, VII_0, VIII) — Opus 4.7 max-effort

**Date**: 2026-05-03
**Companion to**: `/tmp/T2_bianchi_extension.{md,tex,py}` (B-I + outline V/IX), `/tmp/T2_bianchi_IX.{md,tex,py}` (B-IX pathwise via Heinzle-Uggla), `/tmp/T2_bianchi_V.{md,tex,py}` (B-V matter via S3 alone).
**Sympy script**: `/tmp/T2_bianchi_typeA.py` (clean run).
**Full writeup**: `/tmp/T2_bianchi_typeA.tex`.

---

## 1. Setup (Misner-Ryan diagonal, Behr decomposition)

For Type A (`a^a = 0` in Ellis-MacCallum; Wainwright-Ellis 1997 §6) the structure constants are `C^a_{bc} = ε_{bcd} n^{da}`, `n^{ab} = diag(n_1, n_2, n_3)`, `n_i ∈ {-1, 0, +1}`. Sympy-verified (script C1+C2): all six Type A's satisfy `C^a_{ab} = 0` and Jacobi.

| Type | (n_1,n_2,n_3) | Lie group cover  | Compact-quotient topology   | R_3 at iso |
|------|---------------|------------------|------------------------------|-----------|
| I    | (0, 0, 0)     | R^3              | T^3 (flat)                   | 0         |
| II   | (1, 0, 0)     | Heisenberg/Nil^3 | Nilmanifold (NOT flat)       | -1/2      |
| VI_0 | (1,-1, 0)     | E(1,1)           | Solvmanifold                 | -2        |
| VII_0| (1, 1, 0)     | univ. cov. of E(2)| Bieberbach (FLAT)            | 0         |
| VIII | (-1, 1, 1)    | SL(2,R)~         | Seifert / hyperbolic-fibred  | -5/2      |
| IX   | (1, 1, 1)     | SU(2) = S^3      | S^3 / discrete               | +3/2      |

Metric: `ds² = -dt² + Σᵢ a_i(t)² (σⁱ)²`, `σⁱ` left-invariant 1-forms. The R_3 signs (sympy C3, normalised so IX-isotropic > 0) match expectation.

**Correction to user prompt**: the prompt states "II has flat 3-torus quotients available". Bianchi II = Heisenberg group; its compact quotients are *nilmanifolds*, not flat. The flat-quotient Type A's are I (T^3) and VII_0 (Bieberbach). This affects Hadamard analysis below.

## 2. Past attractor (BKL / Wainwright-Hsu)

Verified per type (sympy reproduces `Σpᵢ = Σpᵢ² = 1`):

- **I**: state space *is* the Kasner circle K. No oscillation.
- **II**: single Kasner triple after one Type-II BKL bounce (W-E 1997 §6.2.2).
- **VI_0**: single Kasner; mixed-sign n_i wall is non-confining.
- **VII_0**: single Kasner generically (modulo measure-zero NUT-like orbits; Ringström 2001 arXiv:gr-qc/0103107 for *future* asymptotics — past is time-reversed analogue).
- **VIII**: BKL chaotic (Brehm 2016 arXiv:1606.08058: Lebesgue-a.e. Bianchi VIII vacuum solution converges to Mixmaster).
- **IX**: BKL chaotic, Heinzle-Uggla 2009 attractor theorem (arXiv:0901.0806).

In every case the past attractor lies on the Kasner circle, so each epoch has exactly one contracting `p_1 ∈ (-1/3, 0)` (sympy C4).

## 3. S1 vs S3 status

S1 = volume zero-mode `log²` divergence: needs (i) finite-volume compact spatial quotient with a constant function in L², (ii) zero eigenmode of the Klein-Gordon operator surviving the wall potential. S3 = long-wavelength tachyonic mode along contracting Kasner direction: fires whenever `p_1 < 0`.

| Type | S1 | S3 | Notes |
|------|----|----|-------|
| I    | YES | YES | Both fire on T^3. |
| II   | YES | YES | Nilmanifold has finite vol. + constant in L²; n=(1,0,0) wall non-confining. |
| VI_0 | YES | YES | Solvmanifold compact + constant in L²; mixed-sign n_i non-confining. |
| VII_0| YES | YES | Bieberbach (flat) — same as I up to twisted boundary cond. |
| VIII | NO* | YES | S1 killed by hyperbolic-fibre spectral gap (analogue of B-V on H^3). |
| IX   | NO* | YES | S1 killed for spatial Laplacian; recovered *pathwise* via H-U `V(t) ≤ c t`. |

*B-VIII does NOT have an immediate Heinzle-Uggla pathwise analogue: Brehm 2016 establishes Mixmaster convergence and particle-horizon formation, but I have not located an explicit `V(t) ≤ c t` bound for VIII. The H-U 2009 proof for IX uses S^3-specific monotonic functions (cf. H-U 2010 arXiv:0907.0653); the analogous bound is *expected* for VIII but not yet published.

## 4. Per-type T2 verdict

- **B-II**: **RIGOROUS pending Hadamard** (highly plausible). S1+S3 both fire. SLE on Nil^3 needs Plancherel decomposition on Heisenberg group (Stein 1965; Geller 1980 *CPAM* 33:391; Folland 1982). Estimate **1-3 months expert work** to extend BN23.

- **B-VI_0**: **RIGOROUS pending Hadamard** (plausible). S1+S3 both fire. Solvmanifold harmonic analysis less complete than Heisenberg's, but solvable Lie algebra → standard Plancherel. Estimate **1-3 months**.

- **B-VII_0**: **RIGOROUS pending Hadamard** (most plausible). S1+S3 both fire. Spatial slice is *flat* Bieberbach, so BN23 adapts almost verbatim with twisted boundary cond. Estimate **1-2 months** — closest to a clean result.

- **B-VIII**: **PATHWISE-CONDITIONAL** (hardest of the four). S1 killed by hyperbolic spectral gap; S3 fires pathwise via Brehm 2016. Hadamard existence is open and harder than IX (non-compact universal cover, hyperbolic fibre); comparable to B-V on H^3. Ringström 2019 (arXiv:1808.00786, CMP 372:599) supplies analytic asymptotic framework for KG on Bianchi VIII but does NOT construct a Hadamard state. **Honest assessment**: VIII is harder than I/II/VI_0/VII_0 (microlocal AQFT on non-trivial spectrum) AND harder than IX (no compact spatial topology). It combines worst features of B-V (non-compact spectral gap) and B-IX (Mixmaster chaos).

## 5. Hadamard state existence (per-type, condensed)

I: **YES** (BN23 on T^3). II: **OPEN-plausible** (Heisenberg-Plancherel + BN23). VI_0: **OPEN-plausible** (solvable Lie group Plancherel + BN23). VII_0: **OPEN, MOST plausible** (Bieberbach = finite-index extension of T^3 BN23). VIII: **OPEN, hard** (closest is Ringström 2019 analytic asymptotics, not Hadamard). IX: **OPEN, hard** (S^3 zonal Helgason adapted to chaotic attractor).

## 6. Estimated time-to-publication for unified Type A theorem

- Section in `algebraic_arrow.tex` (B-I rigorous + outline II/VI_0/VII_0/VIII/IX with Hadamard noted): **2-4 weeks**.
- Standalone CQG / J. Math. Phys. paper "T2 across Type A Bianchi", with II/VI_0/VII_0 contingent on a **single** Hadamard SLE prerequisite paper (nilmanifold + Bieberbach + solvmanifold): **6-9 months total**, of which 3-4 are the prerequisite.
- Including B-VIII rigorously: **18-24 months** — needs both an explicit Brehm-style pathwise volume bound for VIII AND a Hadamard SLE on SL(2,R)~, neither in the literature.
- Full unified Type A theorem (all six rigorous): **3-5 years**, gated by Hadamard existence on B-VIII / B-IX.

## 7. Honest residual gaps

1. **VIII Hadamard**: largest unresolved obstacle, closer to V than IX in geometric character.
2. **VIII pathwise volume bound**: Brehm 2016 gives Mixmaster convergence Lebesgue-a.e. but no explicit `V(t) ≤ c t`. Likely true, not in cited literature.
3. **Nilmanifold / solvmanifold SLE**: no published construction of states-of-low-energy on Nil^3 or Sol^3 spacetimes (1-3 months expected; not yet done).

## 8. Files produced

- `/tmp/T2_bianchi_typeA.py` — sympy verification (clean run).
- `/tmp/T2_bianchi_typeA.tex` — full writeup with theorem statements per type.
- `/tmp/T2_bianchi_typeA.md` — this report.

## 9. References (all arXiv-API verified this session)

- Brehm 2016, **arXiv:1606.08058**.
- Ringström 2001, CQG 18:3791, **arXiv:gr-qc/0103107**.
- Ringström 2019, CMP 372:599, **arXiv:1808.00786**.
- Heinzle-Uggla 2009 (attractor), CQG 26:075015, **arXiv:0901.0806**.
- Heinzle-Uggla 2009 (fact/belief), CQG 26:075016, **arXiv:0901.0776**.
- Heinzle-Uggla 2010 (monotonic functions), CQG 27:015009, **arXiv:0907.0653**.
- Banerjee-Niedermaier 2023, JMP 64:113503, **arXiv:2305.11388**.
- Brunetti-Fredenhagen-Verch 2003, CMP 237:31, **arXiv:math-ph/0112041**.
- Damour-Henneaux-Nicolai 2003, CQG 20:R145, **arXiv:hep-th/0212256**.
- Wainwright-Ellis 1997, "Dynamical Systems in Cosmology", CUP (textbook).
- Geller 1980 *CPAM* 33:391; Folland 1982 *Hardy Spaces on Homogeneous Groups* (pre-arXiv classics, cited not re-verified).
