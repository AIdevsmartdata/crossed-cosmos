# Dobrushin uniqueness for the 4D SU(2) Wilson lattice gauge measure for β < 2/9

Version 1.5 (1 November 2026). The previous version is v1.4 (28 October 2026, DOI [10.5281/zenodo.23712954](https://doi.org/10.5281/zenodo.23712954)); v1.3 of 28 September 2026 was not publicly released.
Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

This folder is self-contained. It holds:
- the note (PDF and LaTeX source);
- `identity_all_kappa/`: the scripts, logs and results of the numerical and interval cross-checks of the new proof of the chordal identity for all fields;
- `verif_loi_aire/`: the scripts and results of the checks cited in the area-law section;
- the two interval-arithmetic certificates of v1.4 (the chordal one is now a second proof on κ ≤ 4/3; the geodesic one is the secondary result), each with an independent check;
- a standalone Lean 4 project with the rational parts of both certificates (unchanged since v1.4);
- the small calculations cited in the note.

## What changed since v1.4

- **The chordal one-link identity now holds for every κ ≥ 0** (v1.4: κ ≤ 4/3). The supremum over directions of the one-site coefficient is exactly
  E_κ[x_⊥²] = I₂(κ)/(κ I₁(κ)). For κ > 0 it is attained exactly for directions orthogonal to the field; oblique directions are strictly smaller, with a two-sided estimate; and the coefficient is strictly decreasing in κ.
  The proof is analytic (divergence-free flux field, slice estimate, exact sum-of-squares identity, Chebyshev association). It is **not formalised in Lean**.
  It was read by one independent reviewer (a language model, Kimi K3.1 Pro: first the proof, then the note as typeset); it has not been refereed by a human.
- The v1.4 proof for κ ≤ 4/3 (interval arithmetic + Lean-checked final steps) is kept as a second proof in Appendix A.
- The influence coefficient of each neighbouring link is exactly β/4 for every β ≥ 0 (this also follows from BB26, see below).
- New remark (Corollary 20): Wu's theorem (2006) gives a Poincaré inequality for β < 2/9, uniform in the volume and the boundary condition. It is a corollary, not a new method.
- Literature section updated: versions v1–v4 of BB26 and their numbering, what is and is not new relative to BB26, Levin's conjecture for N = 4.
- **New Section 7 and Appendix B (application: Wilson's area law for β < 2/3).** The chordal coefficient (Theorem 6, via Corollary 14(b)) is applied to the Durhuus–Fröhlich slab σ-models.
  Dobrushin's comparison (Wasserstein form, proved in Appendix B), a count of walks and an elementary Doeblin bound give
  |⟨W_γ⟩| ≤ min{C_λ^T e^{−λRT}, (1 − e^{−12β})^T} for every rectangular loop, on tori uniformly in the volume, in boxes with free boundary conditions and for **every Gibbs measure** on Z⁴. Hence the string tension is ≥ arcosh(2/β − 2).
  **The range is not new**: Borgs and Seiler (1983; Appendix B of the preprint MPI-PAE/PTh 16/83, read; the CMP version was not consulted) prove confinement for β_W < 12/17 ≈ 0.706 by a transfer-matrix argument.
  **No priority is claimed for any threshold**; the contribution is an independent proof with explicit constants.
  Durhuus–Fröhlich (1980) announced β_W < 2/3 (literal reading) without proof; their written argument covers β_W < 1/6 once a factor 2 is corrected.
  Other ranges cited: Fröhlich 1979 + Aizenman–Barsky–Fernández 1987 (≈ 0.2217, not checked), Cao–Nissim–Sheffield 2025 (1/6), Osterwalder–Seiler 1978 (small β).
  Section numbers after §6 shift by one with respect to v1.4 (literature = §8, limitations = §9); the numbers of all earlier theorems, lemmas and corollaries are unchanged (the new items are numbered 7.1, 7.2, …, B).
- The title of v1.4 is kept; the new items are listed here and in the abstract of the note.

## Prior public statement (no priority claim)

The uniqueness range β < 2/9 for the four-dimensional SU(2) model (with exponential decay and a lattice mass gap), the all-field bound
D_ch(κ) ≤ 1/4, i.e. W₁(ν_b, ν_b′) ≤ |b − b′|/4 on S³, and the exactness of the influence coefficient β/4 for every β were stated publicly, with proofs, in the preprint of
D. Bhattacharjee and U. Bhattacharya, "Mass Gap of Lattice Yang–Mills Theory up to the Dobrushin Ceiling", hexagon:2610.00341v1, 18 October 2026
(Theorems E, F and 7 and Proposition 13; the same statement is Theorem 125 of v4 (p. 64) with J. M. Lockwood; Zenodo 10.5281/zenodo.23786523). This note was prepared
independently and makes no priority claim on them. What is new here, relative to them: the exact value I₂/(κ I₁) of the supremum over directions for every κ ≥ 0, its maximisers,
the two-sided estimate for oblique directions, the strict monotonicity in κ, and an analytic proof. Independently of them: the exact geodesic coefficient 8β/(9π), two
interval-arithmetic certificates with independent checks, Lean-checked final steps, and explicit transfers of the published constants of Levin, Royer and Shen–Zhu–Zhu to the Wilson link.
The area-law application is an independent proof of a range that is not new (see above).

## Statement

**Theorem 1 (main result).** Let β ≥ 0 be the Wilson coupling, with weight exp(−β Σ_p (1 − ½ Re Tr U_p)) and
normalised Haar measure on each link of Z⁴. For 0 ≤ β < 2/9 ≈ 0.2222, the SU(2) Wilson specification on Z⁴ has
exactly one Gibbs (DLR) measure.

- Other normalisations: with β_W = 4/g², it is g² > 18; in the 't Hooft normalisation of Shen–Zhu–Zhu (CMP 2023), it is β_tH < 1/18.
- **Method.** Dobrushin's criterion in its Wasserstein (W₁) form, with the Euclidean (chordal) metric of R⁴ on SU(2) ≅ S³. This is the metric of Levin (CMP 1980).
- **Key input (Theorem 6 of the note).** For all κ ≥ 0, the one-site coefficient is D_ch(κ) = E_κ[x_⊥²] = I₂(κ)/(κ I₁(κ)) ≤ 1/4 − κ²/(96 Z(κ)). It is strictly decreasing, hence maximal at zero field, where it equals 1/4.
  Each of the 18 neighbouring links has influence exactly β/4, so the Dobrushin sum is 9β/2, for every β ≥ 0.
  - For oblique directions at angle α to the field: E[x_⊥²] − cos²α·Δ ≤ D_ch(κ, v) ≤ E[x_⊥²] − ½cos²α·Δ, with Δ(κ) = m² + 4m/κ − 1 > 0, m = I₂/I₁.
  - The bound D_ch ≤ 1/4 for all fields (hence Levin's Remark 3.7 for N = 4) was proved before in BB26; 2/9 is Levin's published bound transferred to the Wilson link (2√5/45) with √5 replaced by 1.

**Theorem 2 (geodesic criterion; the main result of v1.2).** With the geodesic metric, the exact coefficient is 8β/(9π), uniformly for κ ≤ 3π/8. The Dobrushin sum is then 16β/π, which gives the weaker range β < π/16 ≈ 0.19635.

Each threshold is sharp for its own criterion.

**Theorem 7.1 (application: area law; Section 7).** For 0 ≤ β_W < 2/3, λ_*(β) = arcosh(2/β − 2), 0 ≤ λ < λ_*, θ_λ = (β/4)(2 cosh λ + 4) < 1 and C_λ = 8θ_λ/(1 − θ_λ), every rectangular loop with sides R, T satisfies
|⟨W_γ⟩| ≤ min{C_λ^T e^{−λRT}, (1 − e^{−12β})^T} on tori (R ≤ L/2, T ≤ L − 1, uniformly in L), on boxes with free boundary conditions, and for every Gibbs measure on Z⁴.
Corollary 7.2: string tension ≥ λ_*(β); uniform bound e^{−c(β)RT}. **The threshold 2/3 is not new** (Borgs–Seiler 1983, preprint, 12/17); no priority claim.
The proof is not formalised in Lean.

**Corollary 20 (Poincaré, remark-level).** For 0 ≤ β < 2/9, any finite box and boundary condition, Var_μ(f) ≤ (1/3)(1 − 9β/2)⁻¹ Σ_ℓ E_μ|∇_ℓ f|² for the unit-sphere metric on each link
((2/3)(1 − 9β/2)⁻¹ for the metric −Tr(XY)). The constant 1/3 uses the one-site gap ≥ 3 of BB26 (Lemma 4 of v1, Lemma 122 of v4); the elementary Bakry–Émery bound alone gives [(2 − 6β)(1 − 9β/2)]⁻¹.

**Status of each part** (the labels are defined in the note):

| part | status |
|---|---|
| κ = 0 values (1/4 and 8/(9π)), influence coefficients, existence | proved on paper |
| chordal identity for every κ ≥ 0, Theorem 6 (flux field, slice estimate, sum-of-squares identity, Chebyshev) | proved on paper; **not** formalised in Lean; read by one independent reviewer (language model); not refereed |
| the same identity on κ ≤ 4/3, second proof (Appendix A) | proved on paper up to a one-variable inequality, which is interval-certified (Arb; independently recertified with mpmath interval arithmetic) |
| the one-link inequality for κ > 0, geodesic metric | interval-certified |
| the final rational inequalities, two algebraic steps, threshold arithmetic | Lean-checked, on the three standard axioms only |
| cross-checks of the new identity (exact power series to κ³⁹, Arb at 90 digits, interval certificates for Ξ < 0 on [4/3, 20] and Δ > 0 on [1/5, 10⁴], optimal transport) | exact / numerical / interval-certified; **not used in the proof** |
| Corollary 20 (Poincaré) | proved from Wu 2006, Thm 2.1 (read) and BB26 Lemma 4 (read) |
| Theorem 7.1, Corollary 7.2, Proposition 7.7 + Appendix B (area law) | proved on paper from Theorem 6 (Cor. 14(b)); **not** formalised in Lean; read by the same reviewer (language model); not refereed; numerical checks of the normalisations, of the walk count and of the string-tension bound in `verif_loi_aire/` (not part of the proof) |
| Borgs–Seiler threshold 12/17 (prior art, cited) | read in the **preprint** only (pp. 4–5, 19–22, B1–B6); journal version not consulted |

## Contents

| path | what it is |
|---|---|
| `note/dobrushin_su2_wilson_v1_5.pdf`, `.tex` | the note (40 pages, of which Section 7 and Appendix B ≈ 7.5; pdflatex, three passes) |
| `identity_all_kappa/` | scripts, logs and results of the cross-checks of §4.9 of the note; `reproduce_light.sh` (about 1 minute), `reproduce_heavy.sh` (about 40 minutes on 8 cores), `SHA256SUMS` (see below) |
| `verif_loi_aire/` | scripts and results cited in Section 7 (see below) |
| `certificate_chordal/` | the certificate of the v1.4 proof on κ ≤ 4/3 (Appendix A of the note) |
| `independent_check_chordal/` | independent check of the chordal certificate |
| `certificate_geodesic/` | the geodesic certificate of v1.2, unchanged except for comments |
| `independent_check_geodesic/` | independent check of the geodesic certificate |
| `lean/` | standalone Lean 4 project (toolchain `v4.34.0`, Mathlib `v4.34.0`); see below |
| `calc/` | short SymPy / mpmath / SciPy scripts and logs cited in the note: transfers of the Levin, Royer and Gross constants; numerical linear programs |
| `SHA256SUMS` | checksums of every other file in this folder |
| `CITATION.cff`, `.zenodo.json` | citation and archive metadata |

**`identity_all_kappa/`** (about 7 MB, mostly the four JSON files of interval certificates in `resultats/`) contains:
- `scripts/`: `verif_symbolique.py` (SymPy), `serie_identite_exacte.py` (exact series to κ³⁹), `ident_num_arb.py` and `ident_num_mp.py` (identity at fixed κ), `cert_xi_arb.py`, `cert_xi_mpiv.py` (interval certificates of Ξ < 0),
  `cert_delta_boites.py` (Δ > 0), `flux_champ_exact.py`, `stress_chaine.py` (chain of bounds), `ot_controle.py`, `synthese_ot.py` (optimal transport), `d7_limite.py` (why the v1.4 reduction fails above κ ≈ 3.28),
  `table_valeurs.py`, `gates_xi.py`, `gates_mpiv.py`, `resume_cert.py`, `verif_empreintes.py`, `kappas_aleatoires.txt`;
- `logs/` and `resultats/`: the outputs of the shipped runs (`logs/reproduce_heavy.out` and `logs/versions_heavy.log` are those of the heavy run; `logs/versions.log` that of the light run);
- `explor/`: exploration scripts and logs, **not used by any verdict**;
- `reproduce_light.sh`, `reproduce_heavy.sh`, `SHA256SUMS`.

The SHA-256 values quoted in §4.9 of the note are those of ten scripts of `scripts/`; they are shipped byte-identical. The docstrings of these scripts cite "RAPPORT §n" and "D7": "RAPPORT" is the author's internal French working report from which §4 and §4.9 of the note were written (it is not shipped; the statements and proofs are in the note), and "D7" is the internal name of the note.

**`verif_loi_aire/`** contains, with their `.json` and `.log` outputs:
- `s1_normalisations.py`: mechanical checks of the normalisations of Section 7 (the quaternionic identities, the plaquette in a slab, the count of 6 neighbours, the Durhuus–Fröhlich factor 2 and thresholds);
- `s2_quart_symbolique.py`: SymPy/mpmath check of the identities of the proof of Theorem 6 (independent re-implementation; reads nothing from `identity_all_kappa/`);
- `s3_marches.py`: the 840 exact counts of tilted walks (Lemma 7.9) and the decay rate of the walk sum on (ℤ/48ℤ)³;
- `s4_tension.py`: the string-tension bound arcosh(2/β − 2) against the strong-coupling series of Drouffe–Zuber (Remark 7.3);
- `verif_biblio.py`: comparison of the metadata of the references added in v1.5 with Crossref and arXiv (needs network access; it checks metadata only, not the content of the articles).

The checks of `s1`–`s4` are not part of any proof.

**`certificate_chordal/`** contains:
- `cert_ch.py`, the Arb certificate of inequality (5) of the note;
- `gates.py`, the gate suite (cap, order, quadrature, precision, number of boxes);
- `gate_exact.py`, exact rationals, with no Arb;
- `gate_numerique.py`, a floating-point gate;
- `constante_c.py`, the constant 0.0084;
- `export_lean.py`, the export to Lean;
- the certificate JSON, `reproduce.sh`, and the logs of a fresh run in `logs/`.

**`independent_check_chordal/`** contains the independent check of the chordal certificate. It does not use python-flint and imports no code from `certificate_chordal/`:
- `coefs_exacts.py`, exact rational coefficients;
- `cert_vch.py`, mpmath interval certificate with elementary tail bounds;
- `parse_lean_boxes.py` and `compare_CH.py`, two-sided comparison with the Lean rationals;
- `exact_c2_D0.py`, exact checks of D_ch(0) = 1/4 and c₂ = 1/96;
- `beckmann_mc.py`, a Monte-Carlo cross-check (numerical only);
- `reproduce.sh` and logs.

**`certificate_geodesic/`** holds the geodesic certificate of v1.2, unchanged except for comments: `cert_lien.py` (v2) and its helpers, the gates, the export to Lean, the certificate JSON, `reproduce.sh` and logs.

**`independent_check_geodesic/`** is an exact rational recomputation of the E_j(α) (`vc_exact.py`), plus a box-by-box check of the 3200 geodesic Lean rationals (`vc_boites_v2.py`); `reproduce.sh`; logs.

**`lean/`** contains `lakefile.toml`, `lake-manifest.json`, the six modules `KevYM/Certif/DobrushinCordale/{Verif,Donnees,Final}.lean` (chordal) and `KevYM/Certif/DobrushinLien/{Verif,Donnees,Final}.lean` (geodesic), `PrintAxioms.lean`, `build.sh`, and the from-scratch build log.

**Language.** The note and this README are in English. The source code comments, the log messages and the comments in the Lean modules are partly in French and partly internal. In code comments:
- "CH" denotes the chordal certificate;
- "V-CH" denotes its independent check;
- "C2" and "CERT" denote the geodesic certificate.

`cert_ch.py`, `cert_lien.py`, the Lean modules and the ten scripts of `identity_all_kappa/scripts/` quoted in the note are shipped byte-identical to the versions whose SHA-256 values are quoted in the note and in the Lean data files, so their comments were not edited.

## Reproduction

The scripts of `identity_all_kappa/` write into its `logs/` and `resultats/` and **overwrite the shipped files**: run them in a copy of the folder to keep the shipped evidence. The scripts of the v1.4 folders write to `out/` in each folder (not shipped).

**0. New folder `identity_all_kappa/`** (Python ≥ 3.11 with `python-flint==0.9.0`, mpmath, NumPy, SciPy, SymPy; POT for the transport control):

```bash
cd identity_all_kappa && PY=python3 PYSYM=python3 ./reproduce_light.sh      # about 1 minute; exit code 0 only if every check passes
# heavy part (about 40 minutes on 8 cores; NPROC=8 workers by default, optional CORES=<cpu list> pinning):
#   PY=./venv/bin/python ./reproduce_heavy.sh
python3 -I scripts/verif_empreintes.py                                        # every result JSON comes from the current version of its script
```

`PY` is the interpreter with python-flint, mpmath, NumPy and SciPy (and POT for the heavy part); `PYSYM` the one with SymPy.

**0b. `verif_loi_aire/`** (NumPy, mpmath, SymPy; about one minute, `s2` is the slowest):

```bash
cd verif_loi_aire && mkdir -p out && for s in s1_normalisations s2_quart_symbolique s3_marches s4_tension; do
  python3 -I $s.py out/$s.json > out/$s.log || echo "FAIL $s"
  cmp out/$s.json $s.json && cmp out/$s.log $s.log && echo "identical to the shipped $s"
done
```

Each script prints its verdicts on the standard output and exits with a non-zero code if one fails. The shipped `.json` and `.log` files come from such runs and were reproduced byte for byte before shipping.

**1. Chordal certificate of v1.4** (Python ≥ 3.11, `python-flint==0.9.0`, NumPy, mpmath; a few minutes on one CPU with the gate suite, about 20 s for the certificate alone):

```bash
cd certificate_chordal && pip install -r requirements.txt && ./reproduce.sh      # QUICK=1 ./reproduce.sh skips the gate suite
```

The script exits with code 0 only if every check passes:
1. **Certificate.** It regenerates the certificate with D = 80, L = 85, NT = 1024 sub-intervals, NK = 256 boxes in κ, `ctx.cap = 200` and `ctx.prec = 128`, and checks that all 256 boxes pass.
   - The JSON records its own wall-clock time in the field `secondes`. Every other field must be identical to the shipped JSON, and after restoring that one field the file must be byte-identical to it.
2. **Guards.** Both guards refuse a truncated run: `cap = 10` and `cap = 84 = L − 1`, the latter also with guard 1 disabled.
3. **Gates.** It runs the exact gate, the constant, the numerical gate and the gate suite.
4. **Export.** It exports to Lean rationals and checks the result is **byte-identical** to `lean/KevYM/Certif/DobrushinCordale/Donnees.lean`. A tampered JSON (cap 10) is refused.

The shipped `logs/` come from such a run (28 September 2026, Python 3.14.4, python-flint 0.9.0): `ALL CHECKS PASSED`.

**2. Independent check of the chordal certificate** (SymPy, mpmath, NumPy; a few minutes with `NPROC=8`):

```bash
cd independent_check_chordal && NPROC=8 ./reproduce.sh
```

Expected result:
- 200/200 boxes of width 1/150, with exact covering of [0, 4/3], worst margin 1.1395e-2;
- the 256 boxes of the Lean data file recertified, with 0 inconsistency against the Lean rationals, worst margin 1.1426e-2;
- the negative gates refused: precision 53 bits, too short series, left side × 0.30.

**3. Geodesic certificate and its independent check** (as in v1.2):

```bash
cd certificate_geodesic && ./reproduce.sh
cd ../independent_check_geodesic && ./reproduce.sh
```

Expected result: `ALL CHECKS PASSED`, with the JSON and `Donnees.lean` byte-identical, then `TOUTES_VRAIES` for 3200/3200 coefficients.

**4. Lean** (elan; several GB for Mathlib):

```bash
cd lean && lake exe cache get && lake build && lake env lean PrintAxioms.lean
```

Expected result:
- `Build completed successfully`;
- each of the 29 theorems (16 chordal, 13 geodesic) depends only on `[propext, Classical.choice, Quot.sound]`.

The shipped log `lean/logs/build_from_zero.log` comes from `build.sh`, run from an empty `.lake` (28 September 2026). The Mathlib `.olean` files came from the Mathlib cache (`lake exe cache get`).

**5. The note** (pdflatex, three passes, in `note/`; the packages `lmodern`, `cm-super` (T2A Type 1 fonts for the Cyrillic quotations), `babel` with `russian` and `english`, `hyperref`, `xurl`, `tabularx`, `booktabs`, `amsmath`, `amssymb`, `amsthm`, `mathrsfs`, `geometry`):

```bash
cd note && for i in 1 2 3; do pdflatex -interaction=nonstopmode dobrushin_su2_wilson_v1_5.tex; done
```

## What the Lean part covers, exactly

Unchanged from v1.4. For the **chordal** part, Lean proves:
- `certificat_cordal`, a conditional implication: **if** real functions Ñ, J̃₀, J̃₁ are bounded box by box by the 256 exported rational boxes, **then** max(J̃₀, J̃₁) < Ñ on [0, 4/3];
- `boites_ok` and `boites_chaine`, by `decide +kernel`;
- the two algebraic steps `etape_alpha` and `etape_kappa2`;
- the threshold arithmetic: 18·β·(1/4) < 1 ⇔ β < 2/9, and 6β < 4/3.

For the **geodesic** part, Lean proves:
- `bP cs 0 0 KW < 0` for each of the 160 exported vectors;
- the implication `certificat_boites`;
- the threshold arithmetic for π/16.

**The analytic proof of the chordal identity for all κ (Theorem 6 of v1.5) is not formalised.** Lean does **not** cover:
- that proof, nor the area-law section of Section 7 and Appendix B, nor Corollary 20;
- the flux bound, the explicit field and the elimination of the direction of Appendix A (proved on paper);
- the reduction of §5.1 (geodesic, proved on paper);
- the box bounds themselves and the positivity of m (Arb, interval-certified);
- the constants 0.0084 and 0.0085;
- the covering of [0, π] by the geodesic boxes.

## Limitations (see §9 of the note)

1. **Scope.** Uniqueness, Corollary 20 (Poincaré, from Wu 2006) and, as an application, the area law of Section 7 for rectangular loops (β < 2/3; **range not new**, Borgs–Seiler 1983). No other decay of correlations, transfer-matrix gap or log-Sobolev inequality is claimed.
2. **Formalisation boundary.** The new proof (Theorem 6 for all κ) and the area-law section are not in Lean; the earlier reductions are proved on paper only.
3. **Audit.** The first geodesic certificate was wrong (erratum in the note). The new analytic proof was checked symbolically, in exact arithmetic (power series), numerically and by one independent reviewer (a language model); the area-law section was read by the same reviewer. Neither has been refereed.
4. **Prior art; limitation of the literature search.**
   - BB26 prove the bound 1/4 for all fields, β < 2/9 and the exactness of β/4 before this note; Levin, Royer, Gross, Simon and Wu are cited.
   - **Not consulted:** Seiler's monograph (LNP 159), the content of Georgii's book (only the table of contents was read), and Simon's book *The Statistical Mechanics of Lattice Gases* (1993).
   - Area law (Section 7): the Borgs–Seiler threshold (12/17) is read in the preprint only; Brydges–Giffen–Durhuus–Fröhlich (1986) was not consulted beyond its abstract; MathSciNet was not queried; Fröhlich 1979 + ABF 1987 (≈ 0.2217) is an unchecked combination of published ingredients.
5. **Range.** Levin's conjecture for N ≠ 4 is not addressed; the geodesic bound is certified only for κ ≤ 59/50.
6. **Scope of physics.** A strong-coupling statement; nothing about the continuum limit or the Yang–Mills mass gap problem.

## Provenance

- **Lean modules and v1.4 certificates.** The six `.lean` modules are byte-identical to commit `1b0f039c53c1e2a11c496cc5a1cb7774ab5a010e` of the author's Lean library (unchanged since v1.4).
  - Its parent is `7a211ed`. The three geodesic modules are unchanged since `7a211ed`, the commit cited in v1.2.
  - `DobrushinCordale/Donnees.lean` has SHA-256 `72a09014…` and `DobrushinLien/Donnees.lean` has `9d6c0628…`, the values quoted in the note.
  - Only `lakefile.toml`, `PrintAxioms.lean` and the package name in `lake-manifest.json` are new. The manifest pins the Mathlib revision `5ed2965256430c3649e86755f9576b54eca72435`.
  - `cert_ch.py`, `cert_lien.py` and the two certificate JSON files match the SHA-256 values in the note. Some helper scripts differ from the author's working copies in comments only: internal task names and paths were removed.
  - `independent_check_geodesic/vc_boites_v2.py` reads `Donnees.lean` from a file instead of through `git show`.
- **New scripts (`identity_all_kappa/`).** Written on 1 November 2026.
  - Ten of them are quoted by SHA-256 in §4.9 of the note and are byte-identical to those versions.
  - `reproduce_light.sh`, `reproduce_heavy.sh` and `explor/portee_boites.sh` differ from the working copies only in the default interpreter (`python3` instead of a machine-specific path), in comments, and, for the heavy run, in making the CPU pinning optional. `reproduce_heavy.sh` was named differently in the working copy; the two logs `logs/reproduce_heavy.out` and `logs/versions_heavy.log` are unchanged copies of the logs of that run.
  - The internal French working report and the internal review transcripts of the working folder are **not** shipped.
- **Scripts of `verif_loi_aire/`.** Written on 1 November 2026. Two docstrings (`s2`, `s3`) were edited to match the numbering of this note; the scripts were re-run after the edit and reproduce the shipped outputs byte for byte.
- **Independent review.** The new proof of Theorem 6, then the note as typeset, and separately the area-law section (Section 7 and Appendix B), were read by Kimi K3.1 Pro (Moonshot AI), a language model. It compared the statements with the cited sources and recomputed the key identities with its own code.
  - Verdicts: no step found faulty, no objection. The transcripts are not part of this archive.
  - A verdict of a language model is not a certification. A few wording retouches (the author's footnote, item 3 of §9, line breaks of some equations) were made after the last review round.
- **Every reference** was checked against its source (Crossref, arXiv, Project Euclid, Numdam or the page images), or it is marked "not consulted", "metadata only" or "not re-read" in the note.

## License, citation, AI use

- **License.** CC BY 4.0.
- **Citation.** See `CITATION.cff`.
- **Archive.** The note is archived on Zenodo as a new version (1.5) of the record 10.5281/zenodo.23712954 (concept DOI 10.5281/zenodo.23712953). It is related by `isPartOf` to the concept record 10.5281/zenodo.19686398 of the earlier crossed-cosmos releases; it is not a version of that concept. The code is tagged `v7.7.0` in the GitHub repository `AIdevsmartdata/crossed-cosmos`.
- **AI use.** The note, the certificate code and the Lean files were prepared with the assistance of Claude (Anthropic); the analytic proof of Theorem 6 and the area-law section were read by Kimi K3.1 Pro (Moonshot AI).
  - Every claim in the note carries a status label.
