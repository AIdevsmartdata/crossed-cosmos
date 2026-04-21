# Changelog

All notable changes to ECI are logged here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), semver.

## [4.0.0] — 2026-04-21

### Fixed — bibliography
- **arXiv:2507.03090** re-attributed to Bedroya–Obied–Vafa–Wu, *Evolving Dark Sector and the Dark Dimension Scenario* (v3 erroneously attributed to Anchordoqui–Antoniadis–Lüst).
- **arXiv:2511.16606** re-attributed to Wang & Piao, *Dark energy after pre-recombination EDE in light of DESI DR2, ACT, SPT* (v3 erroneously "Jiang–Piao").
- **arXiv:2604.09148** removed — it is Rossi-Yu-Michaux on neutrino cosmic web, unrelated to Shiu–Cole. Correct Shiu–Cole references now: arXiv:1812.06960 (JHEP 03 (2019) 054) and arXiv:1712.08159 (JCAP 03 (2018) 025).
- **arXiv:2512.09852** de-listed — authors were Calles et al., not "Shiu–Cole".

### Updated — experimental bounds
- Ġ/G bound updated from Williams–Turyshev–Boggs 2004 to **Biskupek–Müller–Torre**, *Universe* 7(2), 34 (2021), DOI 10.3390/universe7020034: Ġ/G = (−5.0 ± 9.6) × 10⁻¹⁵ yr⁻¹ (≈ 2 orders of magnitude tighter).
- N_eff bound updated from Planck 2018 to **ACT DR6 (Calabrese et al.)**, JCAP 11 (2025) 063, arXiv:2503.14454: N_eff = 2.86 ± 0.13. Critical for Dark Dimension viability.

### Added
- Primordial cosmology section (Big Bang as decodability boundary; inflation as algebraic necessity; revisited Weyl Curvature Hypothesis).
- 30+ new references (2024–2026) — see `paper/eci.bib`.
- Short APS DOI format for 2025+ entries (e.g. `10.1103/tr6y-kpc6`) verified via Crossref.
- Repository scaffolding for symbolic derivations (`derivations/`) and numerical sanity checks (`numerics/`) — SOTA 2026 open-science norm.
- `AI_USE.md` transparency disclosure.
- `docs/REVIEW_NOTES.md` self-audit response log.

### Changed (v4.0.1 self-audit corrections, pre-release)
- **A3 downgraded from axiom to "working conjecture"** in the manuscript, with explicit caveat that Cryptographic Censorship is proven only in AdS/CFT and that its cosmological extension is not established.
- **Prediction (1) flagged as non-discriminating** vs wCDM inside the quoted $(w_0, w_a)$ band pending the `w_a(w_0; \xi_\chi)` analytic computation (companion in `derivations/w0-wa-nmc`).
- JEPA / modular-flow structural analogy postponed to a companion paper (out of scope for core framework paper).

### Changed
- Editorial target: **EPJ C** (SCOAP3 OA, IF 4.3) as primary; *Foundations of Physics* as backup.
- Explicit note on Faraoni sign convention (ξ = 1/6 conformal) added next to every NMC equation.

## [3.x] — previous drafts

Private. Not archived publicly. v4 is the first public release.
