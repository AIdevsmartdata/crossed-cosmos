# Dobrushin uniqueness for the 4D SU(2) Wilson lattice gauge measure for β < 2/9

Version 1.4 (28 October 2026; literature update of v1.3 of 28 September 2026, which was not publicly released). Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

This folder is self-contained. It holds:
- the note (PDF and LaTeX source);
- two interval-arithmetic certificates of one-link inequalities: the chordal one (main result) and the geodesic one (secondary result);
- an independent check of each certificate;
- a standalone Lean 4 project with the rational parts of both certificates;
- the small calculations cited in the note.

## Prior public statement (no priority claim)

the uniqueness range beta < 2/9 for the four-dimensional SU(2) model (with exponential decay and a lattice mass gap) and the all-field bound W1(nu_b, nu_b') <= |b - b'|/4 on S^3 were stated publicly, with proofs, in the preprint of D. Bhattacharjee and U. Bhattacharya, "Mass Gap of Lattice Yang-Mills Theory up to the Dobrushin Ceiling", hexagon:2610.00341v1, 18 October 2026 (Theorems E, F and 7). This note was prepared independently and makes no priority claim. Its own contributions: the exact one-link chordal coefficient E_kappa[x_perp^2] for kappa <= 4/3 with an explicit remainder, the exact geodesic coefficient 8 beta/(9 pi), two independent interval-arithmetic certificates, Lean-checked final steps, and explicit transfers of the published constants of Levin, Royer, Gross, Simon and Shen-Zhu-Zhu to the Wilson link.

## Statement

**Theorem 1 (main result).** Let β ≥ 0 be the Wilson coupling, with weight exp(−β Σ_p (1 − ½ Re Tr U_p)) and
normalised Haar measure on each link of Z⁴. For 0 ≤ β < 2/9 ≈ 0.2222, the SU(2) Wilson specification on Z⁴ has
exactly one Gibbs (DLR) measure.

- Other normalisations:
  - with β_W = 4/g², it is g² > 18;
  - in the 't Hooft normalisation of Shen–Zhu–Zhu (CMP 2023), it is β_tH < 1/18.
- **Method.** Dobrushin's criterion in its Wasserstein (W₁) form, with the Euclidean (chordal) metric of R⁴ on SU(2) ≅ S³. This is the metric of Levin (CMP 1980).
- **Key input (Theorem 6 of the note).** For all κ ∈ [0, 4/3], the one-site coefficient is D_ch(κ) = E_κ[x_⊥²] ≤ 1/4 − κ²/(96 Z(κ)) ≤ 1/4 − 0.0084 κ². It is maximal at zero field, where it equals 1/4.
  - Each of the 18 neighbouring links has influence exactly β/4, so the Dobrushin sum is 9β/2.
  - This confirms Levin's Remark 3.7 conjecture (maximum at zero field) for N = 4 and |g| ≤ 4/3 only.
  - 2/9 is Levin's published bound, transferred to the Wilson link (2√5/45), with his factor √5 replaced by 1.

**Theorem 2 (geodesic criterion; the main result of v1.2).** With the geodesic metric, the exact coefficient is 8β/(9π), uniformly for κ ≤ 3π/8. The Dobrushin sum is then 16β/π, which gives the weaker range β < π/16 ≈ 0.19635.

Each threshold is sharp for its own criterion.

**Status of each part** (the labels are defined in the note):

| part | status |
|---|---|
| κ = 0 values (1/4 and 8/(9π)), influence coefficients, existence, flux bound, explicit field, elimination of the direction, the bound by 1/4 | proved on paper |
| the one-variable inequality on [0, 4/3] (chordal) and the one-link inequality for κ > 0 (geodesic) | interval-certified (Arb / python-flint); the chordal one is also recertified by an independent implementation (mpmath interval arithmetic + exact rationals) |
| the final rational inequalities, two algebraic steps, threshold arithmetic | Lean-checked, on the three standard axioms only |

## Contents

| path | what it is |
|---|---|
| `note/dobrushin_su2_wilson_v1_4.pdf`, `.tex` | the note (22 pages; pdflatex, three passes) |
| `certificate_chordal/` | the certificate of the main result (see below) |
| `independent_check_chordal/` | independent check of the chordal certificate (see below) |
| `certificate_geodesic/` | the geodesic certificate of v1.2, unchanged except for comments (see below) |
| `independent_check_geodesic/` | independent check of the geodesic certificate (see below) |
| `lean/` | standalone Lean 4 project (toolchain `v4.34.0`, Mathlib `v4.34.0`); see below |
| `calc/` | short SymPy / mpmath / SciPy scripts and logs cited in the note: transfers of the Levin, Royer and Gross constants; numerical linear programs |
| `SHA256SUMS` | checksums of every file in this folder |
| `CITATION.cff`, `.zenodo.json` | citation and archive metadata |

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

`cert_ch.py`, `cert_lien.py` and the Lean modules are shipped byte-identical to the versions whose SHA-256 values are quoted in the note and in the Lean data files, so their comments were not edited.

## Reproduction

The regenerated files go to `out/` in each folder. They are not shipped.

**1. Chordal certificate** (Python ≥ 3.11, `python-flint==0.9.0`, NumPy, mpmath; a few minutes on one CPU with the gate suite, about 20 s for the certificate alone):

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

## What the Lean part covers, exactly

For the **chordal** part, Lean proves:
- `certificat_cordal`, a conditional implication: **if** real functions Ñ, J̃₀, J̃₁ are bounded box by box by the 256 exported rational boxes, **then** max(J̃₀, J̃₁) < Ñ on [0, 4/3];
- `boites_ok` and `boites_chaine`, by `decide +kernel`;
- the two algebraic steps `etape_alpha` and `etape_kappa2`;
- the threshold arithmetic: 18·β·(1/4) < 1 ⇔ β < 2/9, and 6β < 4/3.

For the **geodesic** part, Lean proves:
- `bP cs 0 0 KW < 0` for each of the 160 exported vectors;
- the implication `certificat_boites`;
- the threshold arithmetic for π/16.

Lean does **not** cover:
- the flux bound, the explicit field and the elimination of the direction (chordal, proved on paper);
- the reduction of §5.1 (geodesic, proved on paper);
- the box bounds themselves and the positivity of m (Arb, interval-certified);
- the constants 0.0084 and 0.0085;
- the covering of [0, π] by the geodesic boxes.

## Limitations (see §8 of the note)

1. **Uniqueness only.** No decay of correlations, spectral gap, log-Sobolev inequality or area law is claimed.
2. **Formalisation boundary.** The mathematical reductions are proved on paper, not formalised. For the chordal certificate they were re-derived line by line in an independent verification.
3. **Audit.** The first geodesic certificate was wrong; the erratum in the note explains why. Both present certificates pass guards designed for that failure mode, plus independent recomputations. They have not been audited by anyone outside the project, and the note has not been refereed.
4. **Prior art; limitation of the literature search.**
   - Read on the page images, with locations given in the note: Levin (CMP 1980), Royer (AIHP 1986), Gross (CMP 1979) and Simon (CMP 1979).
   - None of these papers mentions gauge theories, and none states a threshold β < π/16, β < 2/9 or better.
   - **Not consulted:** Seiler's monograph (LNP 159), the content of Georgii's book (only the table of contents was read), and Simon's book *The Statistical Mechanics of Lattice Gases* (1993).
   - Any of these three may contain a Dobrushin-type statement for plaquette interactions. No claim of the note rests on them.
5. **Range of fields.** The chordal identity is certified for κ ≤ 4/3 only, which is exactly what β < 2/9 requires. Levin's conjecture for N = 4 and all fields is not addressed.
6. **Scope.** This is a strong-coupling statement. It says nothing about the continuum limit or the Yang–Mills mass gap problem.

## Provenance

- **Lean modules.** The six `.lean` modules are byte-identical to commit `1b0f039c53c1e2a11c496cc5a1cb7774ab5a010e` of the author's Lean library.
  - Its parent is `7a211ed`. The three geodesic modules are unchanged since `7a211ed`, the commit cited in v1.2.
  - `DobrushinCordale/Donnees.lean` has SHA-256 `72a09014…` and `DobrushinLien/Donnees.lean` has `9d6c0628…`, the values quoted in the note.
  - Only `lakefile.toml`, `PrintAxioms.lean` and the package name in `lake-manifest.json` are new. The manifest pins the Mathlib revision `5ed2965256430c3649e86755f9576b54eca72435`.
- **Certificate scripts.**
  - `cert_ch.py`, `cert_lien.py` and the two certificate JSON files match the SHA-256 values in the note.
  - Some helper scripts differ from the author's working copies in comments only: internal task names and paths were removed.
  - `certificate_chordal/gates.py` also writes to `out/` and `logs/` inside its own folder.
  - The independent-check scripts read and write relative paths instead of absolute ones.
  - `independent_check_chordal/parse_lean_boxes.py` was written for this archive.
- **Independent check (geodesic).** `vc_boites_v2.py` reads `Donnees.lean` from a file instead of through `git show`.

## License, citation, AI use

- **License.** CC BY 4.0.
- **Citation.** See `CITATION.cff`.
- **Archive.** The archive is deposited as a separate Zenodo record. It is related by `isPartOf` to the concept record 10.5281/zenodo.19686398 of the earlier crossed-cosmos releases; it is not a version of that concept.
- **AI use.** The note, the certificate code and the Lean files were prepared with the assistance of Claude (Opus 5.5, Anthropic).
  - Every claim in the note carries a status label.
  - Every reference was checked against Crossref, arXiv, Project Euclid or Numdam, or it is marked "not consulted".
