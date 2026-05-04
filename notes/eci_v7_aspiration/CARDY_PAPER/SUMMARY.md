# CARDY_PAPER — Submission Readiness Checklist
**Paper:** `cardy_rho_paper.tex`  
**Target:** *Letters in Mathematical Physics* (Springer) or *J. Phys. A: Math. Theor.* (IOP)  
**Date drafted:** 2026-05-04  

---

## What the paper claims (scope)

| Claim | Status |
|---|---|
| `rho = c/12` exact for full `[0,infty)` integral | PROVEN — 5-line Euler-Mercator + Cardy, Theorem 1 |
| BW window `[0,2pi]` gives 0.471% shortfall | PROVEN — mpmath dps=50 |
| Free boson `c=1, rho=1/12` | VERIFIED (Hawking 1975 precedent; exact via Carlitz) |
| Free fermion `c=1/2, rho=1/24` | VERIFIED (exact via Carlitz; no prior ana-grav precedent) |
| Tricritical Ising M(4,5) `c=7/10, rho=7/120` | VERIFIED — char-sum ratio 0.99929 at u=0.05 |
| 3-state Potts M(5,6) A-series `c=4/5, rho=1/15` | VERIFIED — char-sum ratio 0.99908 at u=0.05 |
| D-series 3-state Potts `rho=1/15` | PREDICTED by Corollary 1 (UV universality); PC2 result PENDING |
| Para-fermion `rho_{p,k} = k/[12(k+1)]` | PROVEN — Euler-Mercator; verified to <10^{-20} |
| Yang-Lee `c=-22/5` -> `rho<0` (domain boundary) | CONFIRMED formal extension; marked out-of-domain |

---

## Priority 1 — Required before submission

- [ ] **PC2 D-series result**: `PC2_cardy_dseries_results.json` is pending. Replace §4.4 placeholder with actual `log Z / [pi^2 c/(3u)]` ratio at u=0.05 for D-series M(5,6). If confirmed rho_inf = 1/15, update table.
- [ ] **Solnyshkov 2017 citation**: Verify exact title/journal/DOI. Current bibitem mixes 2017 and 2019 Phys. Rev. B papers. Check arXiv directly.
- [ ] **Steinhauer 2021 citation**: Confirm Nature Commun. 12, 6820 DOI via CrossRef.
- [ ] **Author name / affiliation**: Replace `[Author]` placeholder.
- [ ] **Polariton rho range**: The `rho in [7.0, 8.3]%` range was taken from eci.tex lines 394-395 because `polariton_rho_results.json` was not accessible at draft time (permission denied). Verify against the JSON before submission.

## Priority 2 — Recommended before submission

- [ ] **He-3-B `c approx 3` justification**: Needs a physics reference for the c-value (quasiparticle spectrum near gap nodes in B-phase). Do not submit without a citation or derivation sketch.
- [ ] **Iguri-Trinchero 2003**: Confirm J. Stat. Phys. 2003 volume/page via CrossRef (arXiv math-ph/0211026 verified).
- [ ] **Nagerl 2025 DOI**: `10.1038/s41586-025-09016-9` from eci.tex line 386; confirm resolves to Cs-133 Feshbach paper.
- [ ] **Non-diagonal window correction**: Compute rho_window for D-series M(5,6) explicitly to quantify MIP dependence of the 0.471% shortfall.

## Priority 3 — Optional improvements

- [ ] Add a figure: plot of S_BE(u) vs u shading the BW window and showing the tail.
- [ ] Add a figure: bar chart of rho vs CFT model.
- [ ] Footnote on q-deformed boson (Arik-Coon) dilogarithm formula from eci.tex lines 323-340.

---

## Anti-hallucination checks

| Reference | Verified |
|---|---|
| Cardy 1986, Nucl. Phys. B 270, DOI 10.1016/0550-3213(86)90552-3 | Crossref confirmed (followup note) |
| BW 1976, J. Math. Phys. 17, DOI 10.1063/1.522898 | Crossref confirmed (followup note) |
| Friedan-Qiu-Shenker 1984, DOI 10.1103/PhysRevLett.52.1575 | Confirmed |
| Di Francesco et al. 1997, ISBN 978-0-387-94785-3 | Confirmed |
| Rocha-Caridi 1985, Springer volume | Title/volume verified; predates DOI |
| Iguri-Trinchero 2003, arXiv math-ph/0211026 | Flagged verified in followup note |
| Nagerl 2025, DOI 10.1038/s41586-025-09016-9 | From eci.tex line 386 |
| Steinhauer 2016, DOI 10.1038/nphys3863 | From eci.tex |
| Steinhauer 2019, arXiv 1903.00073 | Needs CrossRef for published DOI |
| Steinhauer 2021, Nat. Commun. 12, 6820 | Needs CrossRef verification |
| Solnyshkov 2017/2019 | Citation mixed; see Priority 1 |

---

## Novelty statement (for cover letter)

The bosonic value `rho_B = 1/12` is implicit in Hawking (1975) — NOT claimed new.  
Novel content:
1. Five-line proof of `rho = c/12` for all unitary diagonal-MIP CFTs (Theorem 1).
2. Fermionic value `rho_F = 1/24` and parastatistics `rho_{p,k} = k/[12(k+1)]` — no prior analog-gravity precedent.
3. First curated inventory of three falsifiable lab platforms with quantitative predictions.

---

## File provenance

| File | Role |
|---|---|
| `/root/crossed-cosmos/paper/eci.tex` lines 300-404 | Proof sketch, numerics, lab predictions (quoted verbatim) |
| `/root/crossed-cosmos/notes/cardy_rho_test_followup_2026_05_02.md` | BW window vs full-integral analysis, all 5 CFT tables |
| `/root/crossed-cosmos/scripts/analysis/cardy_rho_minimal_models.py` | mpmath dps=50 engine; Rocha-Caridi characters |
| `polariton_rho_results.json` | NOT ACCESSED (permission denied at draft time) |
| `PC2_cardy_dseries_results.json` | NOT YET AVAILABLE — placeholder in §4.4 |
