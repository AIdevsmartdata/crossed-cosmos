# Pan-Yang 2018 NMC Quintessence — Citation Verification

**Verifier:** sub-agent (arXiv API + WebFetch + WebSearch, no Gemini CLI — permission denied)
**Date:** 2026-05-04
**Subject:** Δw_a^NMC = -2 ξ_χ Ω_φ0 = -0.07 claim attributed to "Pan-Yang JCAP 2018, arXiv:1804.05064 eq. 18"

---

## §A — arXiv:1804.05064 metadata

**The arXiv ID is wrong.** Direct hit on the arXiv API:

```
curl -sS "https://export.arxiv.org/api/query?id_list=1804.05064"
```

returns exactly one entry:

- **Title:** *"The FABLE simulations: A feedback model for galaxies, groups and clusters"*
- **Authors:** Nicholas A. Henden, Ewald Puchwein, Sijing Shen, Debora Sijacki
- **Submitted:** 2018-04-13; revised 2018-07-06
- **Journal:** MNRAS (DOI 10.1093/mnras/sty1780)
- **Categories:** astro-ph.GA (primary), astro-ph.CO

This paper is an AREPO/Illustris-style hydrodynamical simulation of AGN+SN feedback in galaxy clusters. It contains **no scalar field, no quintessence, no non-minimal coupling, no equation 18 about w_0/w_a**. It is utterly irrelevant to dark-energy phenomenology.

**Verdict on §A:** [CORRECTED] — the ID 1804.05064 does not point to any Pan-Yang paper. There exist genuine 2018 Pan & Yang JCAP papers (e.g. arXiv:1804.08455 *"Effects of Anisotropic Stress in Interacting DM-DE"* by Yang, Pan, Xu, Mota; arXiv:1804.08558 *"Cosmological constraints on an exponential interaction in the dark sector"* by Yang, Pan, Paliathanasis; JCAP 09(2018)019 *"Tale of stable interacting dark energy"* by Yang, Pan, Di Valentino, Nunes, Vagnozzi, Mota), but they all concern **interacting dark energy** (a Q-coupling between DM and DE in the conservation equations) — **not** non-minimally coupled (ξ R χ²) quintessence. None of them contains a slow-roll formula w_0 = -1 + λ²/3 + 4 ξ Ω_φ.

## §B — Eq. 18 content

There is no eq. 18 of arXiv:1804.05064 about NMC quintessence, because the paper is about cluster hydrodynamics. The formula

```
w_0^NMC = -1 + λ²/3 + 4 ξ_χ Ω_φ0
w_a^NMC = -λ²/2 - 2 ξ_χ Ω_φ0
Δw_a^NMC = -2 ξ_χ Ω_φ0
```

cannot be matched to that arXiv entry. It is a **mis-citation at minimum, fabrication at worst**.

## §C — Structural derivation check

Even setting the bad citation aside, can a generic slow-roll derivation in NMC thawing quintessence with L = -½(∂χ)² - V(χ) - ½ ξ_χ R χ² and V = V_0 exp(-λχ/M_P) yield this formula?

**Pure-quintessence (ξ=0) baseline.** The Scherrer-Sen result (arXiv:0712.3450, *not* 0712.2083 — that ID was also slightly off in the deliverable) for a thawing field with slow-roll parameters ε_V = (M_P V'/V)²/2 = λ²/2 gives, at leading order:

  1 + w(a) ≈ (1+w_0) F(a)²,   with   w_0 + 1 ≈ (λ²/3) Ω_φ0 · [...] (full form involves arctanh of √Ω_φ).

The often-quoted leading-λ² limit is **w_0 ≈ -1 + (λ²/3) Ω_φ0**, *not* -1 + λ²/3 — the deliverable already drops the Ω_φ0 factor on the λ² term, which is non-standard. Mapping to CPL gives w_a ≈ -(λ²/2) Ω_φ0 at leading order, again with an Ω_φ0 multiplier the deliverable omits.

**Adding the NMC term ξ R χ².** The Ricci scalar in a flat FLRW is R = 6(2H² + Ḣ) = 3H²(1 - 3w_tot) ≈ 12H² in the de Sitter limit. The effective potential gets a shift V_eff = V + 3 ξ H² χ² (sign-conventions depending). Near the slow-roll attractor with χ ~ M_P, the modified equation of state has the schematic form:

  w_φ,eff ≈ w_pure + (corrections of order ξ × H²χ²/V).

A direct-coupling limit gives a leading correction at small ξ proportional to **ξ Ω_φ0** (because both the ξ-source term and the field energy density ρ_φ ~ Ω_φ0 ρ_crit feed into the same H² → 12H²Ω_φ0 substitution). So the *form* "Δw ∝ ξ Ω_φ" is plausible at leading order. **However**, the precise coefficients (4 for w_0, 2 for w_a) cannot be obtained without:

1. Specifying Jordan vs Einstein frame (whether the coupling is at action level or after frame transformation),
2. Specifying the sign convention on the ξ R χ² term (some authors use +, some -),
3. Carrying out the autonomous-system fixed-point analysis to subleading order, including the feedback of χ on H through the Friedmann constraint,
4. Mapping numerical w_φ(z) to CPL via a fit at fiducial pivot redshift (typically z_p ≈ 0.5).

The Wolf-García-García-Anton-Ferreira PRL 135 (2025) 081001 paper (arXiv:2504.07679), the Sánchez-López-Karam-Hazra arXiv:2510.14941, and the Adam-Hertzberg arXiv:2509.13302 — i.e. **all three of the leading 2025-2026 NMC+DESI papers we surveyed** — explicitly state that they extract (w_0, w_a) **numerically** by fitting CPL to integrated background trajectories, *not* via a closed-form analytic formula. This strongly suggests no such simple closed-form expression has been derived in the modern literature.

**Conclusion §C:** the structural form "Δw_a ∝ ξ Ω_φ" is plausible at leading order, but the coefficient -2 (and the +4 for w_0) is not derivable from any standard slow-roll calculation we can locate without further assumptions. The precise factors look like an interpolation, not a derivation.

## §D — Cross-references

- **arXiv:2504.07679** (Wolf et al., PRL 135, 081001, 2025): NMC quintessence vs DESI; uses Jordan-frame ξ φ² R, finds posterior ξ = 2.31 (large). Result is **purely numerical**, no analytic w_0(ξ), w_a(ξ) formula given.
- **arXiv:2510.14941** (Sánchez-López, Karam, Hazra 2025): NMC Palatini, exponential potential, late de-Sitter attractor for ξ<0. Extracts w_φ,eff(z) numerically; no closed-form CPL formula.
- **arXiv:2509.13302** (Adam-Hertzberg, JCAP 04(2026)052): Min vs NMC quintessence vs DESI 2025. Numerical: solves EOM and fits CPL post-hoc.

None of these three contemporary references, all working in essentially the same physical setup, exhibits the analytic formula Δw_a = -2 ξ Ω_φ. If such a clean leading-order result existed, at least one of them would quote it.

## §E — Verdict

**[FABRICATED, citation level]** — arXiv:1804.05064 is the FABLE galaxy-simulation paper, not a Pan-Yang NMC quintessence paper. No "eq. 18" supports the formula. Genuine Pan-Yang 2018 JCAP papers exist but treat interacting (Q-coupling) DE, not ξR χ² coupling.

**[UNVERIFIED → weakly DERIVED HERE, formula level]** — the structural form "Δw_a ∝ ξ Ω_φ" is plausible at leading order in ξ (because R ≈ 12H²Ω_φ in dS limit and the ξRχ² term modifies V_eff by ~ξH²M_P²). The coefficient -2 is not justified by any source we located, and three contemporary NMC+DESI papers (Wolf+, Sánchez-López+, Adam-Hertzberg+) explicitly use **numerical** CPL fitting, indicating no clean closed form is in circulation. The deliverable's own Scherrer-Sen leading-order baseline is also slightly mis-stated: w_0 ≈ -1 + (λ²/3)Ω_φ0, not -1 + λ²/3 — the Ω_φ0 multiplier on the λ² term is missing.

**Numerical sanity check:** the arithmetic at ξ_χ=0.05, Ω_φ0=0.7, λ=1 gives the deliverable's stated -0.527, -0.570, -0.070, so the *internal* arithmetic is consistent. But internal consistency of a fabricated formula is not validation.

The discrimination claim "35× factor over Coupled-DE Amendola Δw_a^CDE ≈ -2β² ≈ -0.002 at β² = 0.001" depends critically on the -2ξΩ_φ coefficient. If the coefficient were instead -ξ²Ω_φ or -ξΩ_φ²·(1-Ω_φ) (both of which are dimensionally allowed leading-order corrections in different frames), the discrimination factor collapses by orders of magnitude.

## §F — Recommendation

**Action items for Kevin (ECI v6.0.43, eci.tex line 153, Nobel deliverable):**

1. **Immediately retract the citation "Pan-Yang JCAP 2018 arXiv:1804.05064 eq. 18"** wherever it appears. It is wrong at the arXiv-ID level (FABLE simulations paper) and there is no Pan-Yang JCAP 2018 paper on NMC quintessence at all. Leaving this in any externally-circulated draft is a referee-flag risk and a Zenodo-record-integrity risk for v6.0.43.

2. **Re-tag the formula** Δw_a^NMC = -2ξ_χΩ_φ0 as **[WORKING-CONJECTURE, leading-order ansatz, derivation pending]**. Match the eci.tex line 153 "deferred" status — do not promote it to "verified" until a sympy + analytic derivation exists.

3. **Fix the Scherrer-Sen citation** from arXiv:0712.2083 to **arXiv:0712.3450** (Phys. Rev. D 77, 083515 (2008)). Re-derive the pure-quintessence baseline carefully: the leading-order w_0 in the slow-roll limit carries an Ω_φ0 factor on the λ² term, which the current ECI version has dropped.

4. **Run the actual derivation in P3_5/coupled_de_sympy.py or a new sympy script:** start from the NMC action, derive the modified Friedmann + Klein-Gordon equations, perform the slow-roll expansion explicitly, and extract w_0, w_a as power series in ξ and λ². Either (a) confirm the -2ξΩ_φ coefficient, in which case promote to [DERIVED HERE] with full sympy proof, or (b) find the actual coefficient, in which case update Δw_a^NMC and re-run the DESI DR3 discrimination forecast.

5. **Until step 4 is complete, do not advertise "35× discrimination factor over Coupled-DE Amendola" in any version of the Nobel deliverable.** The discrimination ratio is sensitive to the precise ξ-coefficient and is not currently defensible.

6. **Cross-check against the three modern references** (Wolf 2504.07679, Sánchez-López 2510.14941, Adam-Hertzberg 2509.13302) by re-fitting CPL to their numerical w_φ(z) curves at small ξ to extract an empirical Δw_a/(ξΩ_φ) slope. This gives an independent observational-pipeline-equivalent value of the coefficient that does not depend on getting the analytic derivation right.

**Bottom line:** the formula's *form* is plausible, the *coefficient* is unverified, and the *citation is fabricated/wrong*. This is exactly the failure mode flagged in the user's `feedback_triangulation` and `feedback_crosscheck_fabrication` memory notes. Treat as a v6.0.43 erratum-class issue and address before any further public publication step (e.g. arXiv submission, Vast.ai-rendered figures, Nobel-trajectory cover letter).
