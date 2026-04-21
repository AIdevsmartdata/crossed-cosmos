# v3 → v4 corrections log

Verified on 2026-04-21 via Crossref API (`api.crossref.org/works/<doi>`) and arXiv abstracts (`arxiv.org/abs/<id>`). Every reference below was cross-checked; the table records only entries that *changed* between v3 and v4.

## Author attribution errors (4 critical)

| arXiv ID | v3 (wrong) | v4 (verified) | source |
|---|---|---|---|
| 2507.03090 | Anchordoqui–Antoniadis–Lüst | **Bedroya, Obied, Vafa, Wu** — *Evolving Dark Sector and the Dark Dimension Scenario* | arXiv abs page |
| 2511.16606 | "Jiang–Piao" | **Hao Wang & Yun-Song Piao** — *Dark energy after pre-recombination early dark energy in light of DESI DR2 and the latest ACT and SPT data* | arXiv abs page |
| 2604.09148 | "Shiu–Cole" | Rossi, Yu, Michaux — *neutrino mass from cosmic web persistent homology* (no relation to Shiu–Cole). **Removed.** Correct Shiu–Cole: **arXiv:1812.06960** (JHEP 03 (2019) 054), **arXiv:1712.08159** (JCAP 03 (2018) 025). | arXiv |
| 2512.09852 | "Shiu–Cole" | Calles, Contardo, Noreña, Yip, Shiu — *Primordial non-Gaussianity: fast simulations and persistent summary statistics* (Cole absent). **De-listed.** | arXiv |

## Experimental bounds updated

| Quantity | v3 citation | v4 citation | Value change |
|---|---|---|---|
| Ġ/G (LLR) | Williams–Turyshev–Boggs 2004 (historical) | **Biskupek–Müller–Torre**, *Universe* 7(2), 34 (2021), DOI 10.3390/universe7020034 | **≈ 2 orders of magnitude tighter**: Ġ/G = (−5.0 ± 9.6) × 10⁻¹⁵ yr⁻¹ |
| N_eff | Planck 2018 (arXiv:1807.06209) | **ACT DR6 — Calabrese et al.**, *JCAP* 11 (2025) 063, arXiv:2503.14454 | **2.86 ± 0.13** (ACT-P-LB), 2.89 ± 0.11 (+BBN). Significantly tighter than Planck 2018 ; critical for Dark Dimension scenario. |

## APS short DOI format (2025+)

PRD / PRL / PRX adopted a random-hash short-DOI format in 2025. Examples verified via Crossref API, 2026-04-21:

| Short DOI | Paper | arXiv |
|---|---|---|
| `10.1103/tr6y-kpc6` | DESI DR2 II (Abdul-Karim et al., PRD 112, 2025) | 2503.14738 |
| `10.1103/jysf-k72m` | Wolf et al., *Assessing Cosmological Evidence for Nonminimal Coupling* (PRL 135, 2025) | 2504.07679 |
| `10.1103/hqwq-m19h` | Pan–Ye, *Nonminimally coupled gravity constraints from DESI DR2 data* (PRD 113, L041304, 2026) | 2503.19898 |
| `10.1103/bx25-1g5d` | Poulin–Smith–Calderón–Simon, *Impact of ACT DR6 and DESI DR2 for EDE and H_0* (PRD 113, 2026) | 2505.08051 |

Old long-form DOIs (e.g. `10.1103/PhysRevD.112.083515`) still resolve but APS landing pages prefer the short form for post-2025 papers.

## Sign convention (methodological)

v4 adds an explicit note at every NMC occurrence: **Faraoni/Capozziello–Faraoni convention** is used throughout. In this convention, ξ = 1/6 is the conformal coupling (per Birrell–Davies 1982). The opposite-sign convention (ξ = −1/6 conformal, used e.g. by Bezrukov–Shaposhnikov Higgs inflation) is *not* used here. Mixing conventions in the literature is a known source of sign errors — v4 avoids it.

## Equations technical verification

All equations in the scalar-tensor block (action, T_μν^(χ), Klein–Gordon, no-ghost condition) were cross-checked against:
- Faraoni, *Phys. Rev. D* **62**, 023504 (2000), arXiv:gr-qc/0002091 — Eqs. 1.1, 1.2, 2.7–2.13, 4.8.
- Faraoni, *Cosmology in Scalar-Tensor Gravity*, Springer 2004.
- Capozziello–Faraoni, *Beyond Einstein Gravity*, Springer 2011.
- Birrell–Davies, *Quantum Fields in Curved Space*, CUP 1982 — Eq. 3.190.
- Hrycyna, *Phys. Lett. B* **768**, 218 (2017), arXiv:1511.08736.

Signs, factors and conservation identities (∇^μ T_μν^total = 0) are consistent in the Faraoni convention.
