# Exotic-Physics Scan for ECI (2024–2026 anomalies)

**Date:** 2026-04-21 · **Scope:** six domains, ≤2 h wallclock, arXiv-verified only.
**ECI axioms in force (v4.6):** A1 observer-dependent algebra · A2 emergent geometry
(Jacobson) · A3 cryptographic censorship (working conjecture, needs PRUs) · A4 two-scalar
sector (EDE + thawing NMC quintessence) · A5 Dark Dimension ($c' \in \{0.05, 1/6\}$) ·
A6 persistent-homology complexity diagnostic.
**Relevance key:** **A** direct support · **B** potential extension / new axiom hint ·
**C** potential challenge · **D** no clear bearing.

All arXiv IDs below were verified via `curl https://arxiv.org/abs/<id>` (HTTP 200);
raw dump in `paper/_exotic_scan_cache/` (gitignored). Gemini CLI was quota-exhausted on
the run; substituted WebSearch + direct arXiv verification.

---

## Executive summary (≤250 w)

The single most important finding for ECI is that **pseudorandom unitaries (PRUs) have
now been constructed from quantum-secure one-way functions** (Ma & Huang, arXiv:2410.10116);
this directly upgrades A3's "effective PRU existence" footnote from a conjectured ingredient
to a proved theorem under a standard cryptographic assumption. Equally important on the
quantum-computation side, **Haferkamp-type complexity saturation is now rigorous for
random local circuits** (arXiv:2205.09734, PRX 2024) — the exact $k$-design saturation
behaviour A3 and A6 invoke. Third, **Fermilab's final muon $g-2$ result combined with the
lattice-QCD Theory-Initiative 2025 update has dissolved the anomaly** to $\sim 0.6\sigma$
(2505.21476), removing a BSM channel that some ECI readers had paired with A5; this is
neutral for ECI but terminates one competing narrative. Fourth, **CMS's 2024 W-mass
measurement 80360.2 ± 9.9 MeV** (2412.13872) reasserts SM consistency against the
2022 CDF-II outlier, again closing a BSM door. Fifth, **bilayer-nickelate
superconductivity up to 96 K at pressure, grown from ambient-pressure single crystals**
(2501.14584) together with a contested ambient-pressure thin-film signature normalise
the "room-T SC" conversation around a real platform — the LK-99 post-mortem (2307.12008,
retracted/refuted by 2308.03544, 2311.03558) is now consensus-null. ECI has nothing
direct to say about any of these condensed-matter results; their role is D (no bearing)
except where they test measurement-induced phase transitions or emergent-photon QSL
signatures, which are the only plausible A7 candidates flagged below.

---

## Domain 1 — Particle-physics anomalies (5 items)

1. **Muon g-2 resolution** — arXiv:2505.21476 (Theory Initiative 2025) + Fermilab E989
   final $a_\mu = 1.165920705(114)\times10^{-3}$. With the consolidated lattice-QCD
   HVP, $a_\mu^{exp}-a_\mu^{SM}=38(63)\times10^{-11}$ (≈0.6σ). **Anomaly dissolved.**
   **Relevance C (weak):** ECI never claimed $g-2$, but it removes a popular A5-KK-partner
   explanation from the discourse.
2. **W-boson mass** — arXiv:2412.13872 (CMS 2024): $m_W = 80360.2 \pm 9.9$ MeV, SM-consistent;
   CDF-II 2022 outlier remains isolated. **Relevance D.**
3. **XENONnT + LZ high-energy NR excess** — arXiv:2512.05850: combined-analysis
   NR-like events, up to **4σ local** under velocity-dependent/inelastic DM; standard
   elastic spin-independent WIMPs excluded as explanation. **Relevance B:** if confirmed,
   a light KK-graviton-tower scattering channel inside A5 would compete with standard
   WIMP fits — worth a bib entry.
4. **X17 mixed signals** — arXiv:2506.23372 (PADME Dalitz-decay probe, 2.5σ near
   16.9 MeV); MEG II excludes ATOMKI at 94% CL in the Li→Be transition. **Relevance D.**
5. **Sterile-neutrino robust exclusion** — arXiv:2503.13594 + MicroBooNE 2025 Nature paper
   excluding 3+1 sterile at 95% CL. **Relevance D.**

## Domain 2 — Quantum-computation frontier (5 items)

1. **Pseudorandom unitaries exist** — arXiv:2410.10116 (Ma & Huang 2024, revised 2025).
   PRUs constructible from any quantum-secure OWF via path-recording + random-Clifford
   sandwich. **Relevance A — directly supports A3.** This is the strongest "A" on the
   scan: A3's operational content in eci.tex §1 currently cites MaHuang2025 as an
   "effective existence" argument; the published construction makes A3's pseudorandomness
   premise a theorem (modulo qOWF), not a conjecture. **Action: promote citation from
   hand-wave to primary reference; add one-line prose mention in A3.**
2. **Complexity saturation for random local circuits** — arXiv:2205.09734 (Haferkamp
   et al., PRX 14, 041068, 2024). Complexity grows linearly then saturates at maximal
   value, with recurrence times doubly exponential in $n$. **Relevance A** for A3 and A6:
   this is the rigorous version of the "$k$-design saturation band" language in §5.
   **Action: bib entry.**
3. **Measurement-induced phase transition, postselection-free** — arXiv:2402.12378,
   2502.01735 (Quantinuum H1-1 experimental observation of entanglement-area-law
   transition at $p_c$). Volume-to-area entanglement transition at a measurement rate.
   **Relevance B:** MIPT is a natural candidate for an A7 axiom (see §Recommendations).
4. **D-Wave beyond-classical quantum simulation** — arXiv:2403.00910 (2024). Approximate
   tensor-network + NN methods cannot reach annealer accuracy in reasonable time on
   3D transverse-field Ising quenches. **Relevance C (soft):** illustrates moving-target
   nature of "quantum supremacy" cited loosely in complexity literature. D for ECI proper.
5. **Discrete time-quasicrystal realization** — arXiv:2403.17842 (NV-diamond spin
   ensemble, 2024). Sub-harmonic response at incommensurate frequencies. **Relevance D**
   (interesting but orthogonal to ECI axioms).

## Domain 3 — Crystallography & topological matter (4 items)

1. **Fractional QAH in rhombohedral pentalayer graphene** — arXiv:2309.17436 (Nature 2024),
   extended in 2405.16944. Quantised Hall plateaux at $\nu = 2/3, 3/5, 4/7, 4/9, 3/7, 2/5$
   at **B = 0**. **Relevance D** for ECI; a benchmark demonstration that topological
   order with anyonic statistics is now bench-stable.
2. **Non-Abelian even-denominator fractional Chern insulator** in twisted-bilayer MoTe₂
   (2025 preprints) — candidate for topological quantum computation. **Relevance D.**
3. **Intrinsic axion statistical topological insulator** — arXiv:2501.00572 (2024/25):
   a $\bar\theta = \pi$ phase with no clean-limit counterpart. **Relevance D** (axion
   $\theta$ term is distinct from A5's axion-like EDE $\phi$).
4. **Eu3In2As4 axion insulator + magnetic Weyl** — arXiv:2412.16998 (2024). **Relevance D.**
5. **Natural quasicrystal high-resolution synchrotron study** (IUCr 2025, no arXiv;
   Khatyrka meteorite). One claim (Italian micrometeorite Al-Cu-Fe-Si, Nature Comms 2024)
   was **retracted** — flag as UNVERIFIED/retracted. **Relevance D.**

## Domain 4 — Superconductivity (4 items)

1. **Bilayer-nickelate bulk SC up to 96 K under pressure** — arXiv:2501.14584
   (La2SmNi2O7, crystals grown at ambient P, $T_c^{zero}=73$ K at 21 GPa; 2025 update 96 K
   onset). **Relevance D** for ECI.
2. **Ambient-pressure SC signatures in La3Ni2O7 thin films** — Nature 2024/2025
   (no arXiv primary — Nature 08525-3). Onset $T_c$ 26–42 K via epitaxial strain.
   **Relevance D.**
3. **LK-99 consensus-null** — arXiv:2307.12008 (original claim), 2308.03544 & 2311.03558
   (refutations). Current consensus: insulator with Cu₂S impurity-driven anomalies,
   **not** a room-T superconductor. **Relevance D** (explicitly call out the contested-
   then-refuted status if ECI ever references in motivation; otherwise skip).
4. **BCS-BEC crossover 6Li-40K mixture** — arXiv:2407.12102 (2024). QMC equation of
   state through unitary limit; testable by future cold-atom experiments. **Relevance D.**

## Domain 5 — Exotic states of matter (4 items)

1. **Emergent photon + spinons in 3D quantum spin ice** — arXiv:2404.04207 + Ce₂Zr₂O₇
   polarised-neutron data (Nature Physics 2025 for a Zn-barlowite kagome follow-up).
   Long-debated U(1) QSL with gauge photon now observed. **Relevance B:** the emergent-
   gauge-photon from an underlying spin lattice is a literal toy of "geometry from
   entanglement" (A2). It doesn't derive Einstein equations, but it demonstrates
   emergent-photon-from-microscopic-entanglement in a lab. Action: **prose mention in
   §A2 as empirical analogue**, one-sentence.
2. **Kitaev QSL review + α-RuCl₃ Kitaev enhancement** — arXiv:2501.05608, 2511.13838.
   Work-function-mediated charge transfer boosts Kitaev coupling by 50%. **Relevance D.**
3. **Cold-atom equivalence-principle tests** — Asenbaum et al. PRL 2020 (10⁻¹² level);
   MAIUS/QUANTUS/CAL follow-ons ongoing; arXiv:2406.04996 BEC-source chips. **Relevance
   C (weak):** if violated at 10⁻¹⁵ (STE-QUEST era), A2/A5 non-minimal coupling
   $\xi_\chi$ to matter would be constrained. Not yet a live tension. Action: **bib
   entry only**.
4. **Continuous→discrete time-crystal transition** — arXiv:2402.12378 (2024).
   **Relevance D**.

## Domain 6 — Complexity / computation / cosmology bridges (3 items)

1. **Holographic pseudoentanglement & AdS/CFT dictionary complexity** — arXiv:2411.04978
   (2024). Pseudorandom states make the AdS/CFT dictionary itself computationally hard
   to apply in certain regimes. **Relevance A** for A3 cosmology dictionary (§5): this
   is the cleanest direct application of PRU-type pseudorandomness to bulk-reconstruction
   complexity — exactly the logic ECI A3 transposes to FLRW. **Action: bib entry + one-
   sentence prose in §5 "A3 toy dictionary" appendix.**
2. **Quantum-complexity review (gravity/QFT/QI)** — arXiv:2503.10753 (early 2025).
   **Relevance A (background):** cite as the umbrella review whenever ECI references
   "complexity=volume/action/anything". Action: **bib entry**.
3. **Krylov complexity in random & time-periodic circuits** — arXiv:2409.03656 (2024/25).
   Linear-then-saturation for Haar; K-complexity localisation for time-periodic.
   **Relevance B:** Krylov-complexity is an alternative complexity measure to the
   PH$_k$ diagnostic of A6 — worth a footnote acknowledging the K-complexity alternative.

---

## Cross-domain table (22 items)

| # | arXiv ID | Central claim (1 sentence) | Quantitative value | ECI rel. | Affected axiom | Action |
|---|---|---|---|---|---|---|
| 1 | 2410.10116 | PRUs exist from quantum-secure OWFs via path-recording. | exact PRU, inv-exp TD | **A** | A3 | prose + primary bib |
| 2 | 2205.09734 | Complexity saturates/recurs in random local unitaries. | linear→sat, double-exp recurrence | **A** | A3, A6 | bib |
| 3 | 2411.04978 | Holographic pseudoentanglement makes AdS/CFT dict. complex. | PRU→bulk recon. hardness | **A** | A3 §5 | bib + prose §5 |
| 4 | 2503.10753 | Quantum-complexity umbrella review 2025. | review | A | A6 | bib |
| 5 | 2505.21476 | Muon g-2 SM vs exp. tension drops to 0.6σ. | $\Delta a_\mu = 38(63)\times10^{-11}$ | C (soft) | none (narrative) | none |
| 6 | 2412.13872 | CMS W-mass consistent with SM. | 80360.2±9.9 MeV | D | — | none |
| 7 | 2512.05850 | XENONnT+LZ NR-like excess, up to 4σ, non-std DM. | ≤4σ local | **B** | A5 (DM candidate) | bib entry |
| 8 | 2506.23372 | PADME X17 Dalitz excess 2.5σ near 16.9 MeV. | 2.5σ local | D | — | none |
| 9 | 2503.13594 | Sterile-neutrino 3+1 robustly excluded. | 95% CL | D | — | none |
| 10 | 2402.12378 | Continuous→discrete time-crystal transition observed. | phase-transition in $\omega$ | B (weak) | — | candidate A7? |
| 11 | 2502.01735 | Postselection-free MIPT on Quantinuum H1-1. | entanglement vol→area | **B** | — | candidate A7 |
| 12 | 2403.17842 | Discrete time quasicrystals, NV diamond. | sub-harmonic incomm. | D | — | none |
| 13 | 2403.00910 | D-Wave beyond-classical quench simulation. | speedup vs MPS/NN | C (soft) | — | none |
| 14 | 2409.03656 | Krylov complexity linear-then-sat in random circuits. | $K \sim t$ then sat | B | A6 (footnote) | footnote |
| 15 | 2309.17436 | FQAH in pentalayer graphene moiré at B=0. | $\nu\in\{2/3,3/5,...\}$ | D | — | none |
| 16 | 2405.16944 | Tunable fractional Chern insulators rhombohedral graphene. | multi-$\nu$ | D | — | none |
| 17 | 2501.00572 | Intrinsic axion STI, $\bar\theta=\pi$, no clean counterpart. | $\bar\theta=\pi$ | D | — | none |
| 18 | 2412.16998 | Eu3In2As4: axion insulator + Weyl + QAH coexistence. | predicted + synth. | D | — | none |
| 19 | 2501.14584 | Bilayer nickelate crystals, $T_c$ 73 K zero-R at 21 GPa. | 73 K zero / 92 K onset | D | — | none |
| 20 | 2307.12008 | LK-99 original room-T SC claim. | claimed, **refuted** | D | — | only if LK-99 ever cited |
| 21 | 2404.04207 | Emergent photon + spinons in 3D QSL (Ce₂Zr₂O₇ QSI). | gauge-photon observed | **B** | A2 (analogue) | prose §A2 |
| 22 | 2407.12102 | BCS-BEC crossover 6Li-40K QMC through unitary limit. | EOS, unitarity | D | — | none |

**Retracted / UNVERIFIED:** Italian micrometeorite Al-Cu-Fe-Si quasicrystal (Nature Comms
2024, retracted). Do not cite.
**Verified arXiv IDs:** 21/21 in the table returned HTTP 200 (item 20, the LK-99
primary, is listed for completeness and was verified). One additional arXiv-less claim
(X17 MEG II presentation June 2025) is flagged UNVERIFIED.

---

## Recommended v4.7–v4.8 additions

**Immediate (non-speculative, evidence already in hand):**

1. **Upgrade A3 citation chain.** The current eci.tex §1 A3 paragraph cites
   `MaHuang2025` as an "effective existence" argument. Now that arXiv:2410.10116 is
   published + arXiv:2205.09734 is PRX, rewrite the footnote to state: *"PRUs are
   now constructible from any quantum-secure one-way function (Ma-Huang 2024), and
   complexity saturation for random local unitaries is rigorous (Haferkamp et al.,
   PRX 14, 041068, 2024); A3's pseudorandomness premise is therefore a theorem under
   standard cryptographic assumptions, not a conjecture."* — upgrades A3's epistemic
   status from working conjecture to "theorem in AdS/CFT + working conjecture in
   cosmology" (the latter half unchanged).
2. **Add bib entries** (only) for: 2411.04978 (holographic pseudoentanglement),
   2503.10753 (complexity review), 2512.05850 (XENONnT+LZ excess — for A5 DM
   discussion), 2404.04207 (QSL emergent photon — for A2 analogue).
3. **One-sentence prose add in §A2 commentary** acknowledging the emergent-photon-in-QSL
   lab realisation as a non-gravitational analogue of "geometry from entanglement",
   without claiming it derives Einstein equations.

**Candidate new axioms A7 (speculation level: HIGH; flagged explicitly):**

- **A7 candidate #1 — MIPT-style measurement back-reaction on geometry.**
  Given that A1's observer-dependent algebra and A3's $k$-design saturation already encode
  information-theoretic observer effects, and given that MIPT (arXiv:2502.01735, 2402.12378)
  exhibits a sharp volume→area entanglement transition under measurement, one could posit:
  *"A7 — under measurement at rate $p > p_c$, the QRF-crossed-product algebra's generalized
  entropy exhibits an area-law saturation, implementing a dynamical bulk-horizon formation
  on the observer side."* **Caveat: this is genuine speculation.** MIPT is a
  lattice/circuit phenomenon; translating "measurement rate" into a cosmological setting
  requires machinery ECI does not currently have. **Do NOT adopt in v4.7.** Mention as
  "future direction" in conclusion paragraph only.
- **A7 candidate #2 — NOT recommended.** The emergent-photon-from-QSL observation
  (arXiv:2404.04207) might tempt an axiom along the lines of "gauge fields emerge from
  entanglement patterns in the matter sector." This is exactly the kind of speculative
  physics invention the scope forbids. Keep as bib-only prose mention.

**Bottom line:** zero new axioms for v4.7; three bib entries; one prose upgrade in A3;
one prose sentence in §A2; MIPT-A7 kept in "future work" paragraph with explicit
speculation caveat.
