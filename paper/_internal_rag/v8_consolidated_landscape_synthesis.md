# Consolidated landscape synthesis — 3-agent gap-analysis (2026-04-22)

**Purpose.** Owner request: clarify the plausible theoretical landscape
around v5 (phenomenological, NMC quintessence) and v6 (formal,
type-II GSL) by identifying (a) what calculations remain, (b) what
published work aligns or contradicts, (c) what is invalidated, and
(d) how our two papers sit in the 30-year panorama.

**Inputs.** Three Sonnet agent reports:
- `v5_gap_analysis.md` (commit `dd7afeb`) — 5 findings, Wolf-2025 supersession central
- `v6_gap_analysis.md` (commit `a06fe21b148459a7c` result) — 5 findings, M1-theorem gap central
- `physics_landscape_1996_2026.md` (commit `df6d972`) — 90 entries, 48 ACTIVE / 22 FADING / 3 REFUTED / 7 DORMANT / 10 CONTESTED

---

## Part A — Where each paper sits in the plausible landscape

### v5 — NMC quintessence, DESI DR2 + Pantheon+

**Ecosystem:** joins the ACTIVE DESI-DR2-driven dark-energy dynamical
programme, alongside:
- Ye et al. 2025 (ξ_χ Hints of NMC, PRL 134:181002)
- Wolf et al. 2025 (ξ_χ(χ₀/M_P)² ≲ 6×10⁻⁶ PPN bound, PRL 135:081001)
- Pan-Ye 2026 (arXiv:2503.19898)
- Sanchez-Lopez-Karam-Hazra 2025 (arXiv:2510.14941)

**v5's positioning:** MCMC null result posterior-dominated (BF_01 ≈ 1,
Δχ² = −0.04), consistent with the whole NMC cluster and with ΛCDM.
Wolf 2025 PPN bound is **40× tighter than our MCMC**, so the v5
cosmological fit *does not add constraint* over Wolf; its value lies
in covariance matrix exposure (bias marginalisation), not in
tightening ξ_χ.

**Scientific adjacency:** Poulin-Smith 2026 EDE (f_EDE = 0.09 ± 0.03)
reduces H₀ tension to ~2σ. This **weakens the external motivation**
for extra NMC degrees of freedom beyond ΛCDM+EDE, but does not
invalidate v5, which is specifically about the NMC quintessence
prior (compatible with ΛCDM when ξ_χ → 0).

### v6 — Formal type-II crossed-product GSL inequality

**Ecosystem:** backbone ACTIVE:
- CLPW 2023 (type-II_1 de Sitter crossed product)
- DEHK 2025a,b (type-II_∞ observer-dependent)
- Faulkner-Speranza 2024 (modular differential GSL)
- Kirklin 2025 (non-semiclassical refinement)
- **NEW (now in v6.0.4)**: Liu 2026, Kudler-Flam 2024, Hollands-Longo 2025

**v6's positioning:** adds a *complexity-bounded* source term
(κ_R C_k Θ) to the modular GSL framework. No 2024-2026 paper
provides the same combination. Agent v6 gap-analysis confirms
**no scoop as of 2026-04-22** — weekly surveillance remains active.

**Scientific adjacency:** Liu et al. 2026 (2601.07915) uses the same
half-sided modular inclusion machinery for QFC in perturbative QG
on horizon subalgebras. Our inequality is complementary, not
competing.

---

## Part B — Calculations remaining, ordered by cost

### Cheap (hours, can execute locally)

**v5-A** *(highest-value cheap fix)*: **χ(z) evolution for Cassini
frozen-field validation** (v5 finding 5). One-page ODE
integration z=0.1→0 at MAP (w₀=−0.881, wₐ=−0.272) to certify
Δχ/χ₀ < 5%. Cost: 1-agent 30 min.

**v6-A** *(applied in v6.0.4)*: add Liu 2026 + KFLS 2024 +
Hollands-Longo 2025 + Barrow 2025 citations; add FLRW scope
footnote; update §7 open questions. **DONE** in commit `a41c394`.

**v5-B** *(easy revision)*: update §3.5 of `paper/eci.tex` to state
explicitly that Wolf 2025 PPN bound (ξ_χ(χ₀/M_P)² ≲ 6×10⁻⁶,
→ |ξ_χ| ≲ 6×10⁻⁴ at χ₀=M_P/10) is the **consolidated PPN
constraint** and that the cosmological fit is complementary
rather than tightening. Cost: 30 min manual edit + recompile.

### Medium (day, agent task)

**v5-C**: Full Fisher forecast DR3 + Euclid DR1 + LSST Y10 at nuisance
marginalisation level. Verdict from agent v5: σ(ξ_χ) remains
above Cassini saturation through both data releases →
**structural null result**. This justifies not redoing the
full MCMC; a Fisher-only forecast communicates the projection
cleanly.

**v6-B**: Explicit connection between the v6 Pinsker step and Liu
2026 QFC proof in perturbative QG. A short technical note could
position v6 as the *complexity-bounded* generalisation of Liu's
QFC result on horizon subalgebras. Cost: 1 week.

### Large (months, research)

**v5-D**: χ(z) non-perturbative evolution with full NMC coupling; a
rewrite of the DR2 pipeline using CLASS with hi_class NMC
implementation. User already has the hi_class_nmc patch in
`mcmc/nmc_patch/`; the MCMC was done via Cobaya plugin route.
A full C-patch route is a multi-month project.

**v6-C** *(still open, F-1)*: M1 type-II theorem: identify the
modular-commutator source with κ_R C_k *exactly*. Kirklin 2025
and FS 2024 prove only monotonicity; no complexity source. This
gap is **structural**; it does not prevent JHEP submission but
defines the next research direction.

**v6-D**: Extension of KS-microlocal covariance (v6.0.3,
DERIVED-UNDER-M2) beyond dS static patch. The compact-support
hypothesis of GKS 2012 fails in FLRW; KFLS 2024 algebraic FLRW
construction is the natural starting point for this extension.

---

## Part C — Who aligns, who contradicts, who is invalidated

### v5 alignment

| Reference | Alignment | Note |
|---|---|---|
| Ye 2025 PRL 134:181002 | ALIGNS | Hints of NMC but <3σ detection |
| Wolf 2025 PRL 135:081001 | ALIGNS + TIGHTER | PPN bound 40× tighter |
| Pan-Ye 2026 arXiv:2503.19898 | ALIGNS | DR2 compatible |
| Sanchez-Lopez 2025 | ALIGNS | Updated thawing constraints |
| DESI DR2 2025 | MOTIVATES | 2.6-3.9σ dark energy dynamical |

### v5 contradicts / invalidates

**No mainstream 2020-2023 NMC paper claims detection at |ξ_χ*| > 0.20
(which would be excluded at 3σ by our MCMC).** v5 does not
*falsify* any prior work at 3σ; it *challenges* claims of
tension with ΛCDM at ≤1.5σ.

### v6 alignment

| Reference | Alignment | Note |
|---|---|---|
| CLPW 2023 arXiv:2206.10780 | BACKBONE | type-II_1 dS algebra |
| DEHK 2025a,b | BACKBONE | type-II_∞ observer |
| Faulkner-Speranza 2024 | EXTENDS | modular GSL without complexity |
| Kirklin 2025 | EXTENDS | non-semiclassical; no complexity source |
| Liu 2026 arXiv:2601.07915 | PARALLEL | QFC proof, horizon subalgebras |
| Hollands-Longo 2025 | REINFORCES | simplified QNEC proof |
| KFLS 2024 arXiv:2406.01669 | EXTENDS SCOPE | FLRW type-II algebras |

### v6 contradicts / invalidates

**None directly.** The v6 logistic envelope (Prop. 1) is a
*strengthening* of Wall / Faulkner-Speranza, never stricter than
FS24 (verified by F2 consistency check, commit `7e7f99b`). It does
not invalidate prior work; it refines the inequality under
explicit additional postulates M1-M3.

---

## Part D — 30-year panorama: where we sit

### Our 2 papers in context of the 90-entry landscape

**v5 sits in ACTIVE cluster:** NMC quintessence + thawing + DESI DR2,
alongside EDE (Poulin-Smith 2026), DD (Vafa-Montero-Valenzuela
2022, Bedroya 2025), and dynamical-dark-energy programmes.

**v6 sits in ACTIVE cluster:** type-II crossed-product algebras +
modular GSL + complexity, alongside CLPW, DEHK, FS, Kirklin, Liu,
Hollands-Longo.

### What we do NOT overlap with

- MOND relativistic completions (Skordis-Złośnik 2021, CONTESTED) —
  orthogonal phenomenology
- Verlinde 2011/2017 entropic gravity — our v6 agent-12 found Verlinde
  2011 matches v6 at leading order (POSITIVE-PARTIAL) but diverges
  sign-opposite at 2017 DM formulation
- Amplituhedron / positive geometry (ACTIVE, Arkani-Hamed 2013-2024)
  — different framework entirely
- String cosmology (pre-big-bang, ekpyrotic, CCC) — different
  cosmological foundation
- Swampland conjectures beyond DD (weak gravity, SDC) — relevant as
  inputs to v5 but not directly structural

### What could threaten our scope in 2027+

- **JWST-era Hubble tension resolution.** If Poulin-Smith 2026 EDE
  robustness is confirmed and extends to other methods (SNe II,
  TDCOSMO), v5 NMC motivation weakens. v5 remains valid as a
  parallel constraint but becomes less central.
- **DESI DR3 + Euclid DR1.** If w(z) dynamical dark energy
  consolidates (3σ+ confirmation), the motivation for NMC
  quintessence strengthens. σ(ξ_χ) tightening is structural not
  transformative at DR3.
- **Type-II FLRW algebras (KFLS 2024 follow-ups).** If a FLRW
  analogue of CLPW is proved with a concrete complexity-bounded
  rate, our v6 static-patch result becomes a special case of a
  broader statement.
- **Proof of M1 in type-II factor.** Would upgrade v6 from
  inequality-under-postulate to theorem. This is exactly what F-1
  re-open condition says and what no 2024-2026 paper has delivered.

---

## Part E — Explicit action items for next revision cycles

### Immediate (this session)

1. ✅ v6.0.4 published with 4 new citations + FLRW footnote
2. v5 `paper/eci.tex` §3.5 update: Wolf 2025 as consolidated PPN
   bound, positioning cosmological fit as complementary
   (recommended; ~30 min; can be pushed as v5.0.2 minor revision)
3. χ(z) ODE validation of Cassini frozen-field (can be a small
   appendix or an artefact commit `derivations/V8-chi-z-Cassini.py`
   ~30 min)

### Short-term (2-4 weeks)

4. Submit v6.0.4 to JHEP when endorsement for `hep-th` becomes
   available; arXiv deposit under `hep-th` primary + `gr-qc`
   cross-list
5. Submit v5.0.2 (Wolf-consolidated edit) to EPJ C SCOAP3
6. Submit chimere-omega-0.1 to cs.LG (no endorsement needed for
   first-time cs.LG submission in many cases)

### Medium-term (2-12 months)

7. v7 follow-up paper: explicit connection v6 Pinsker step ↔ Liu
   2026 QFC proof (positions v6 as complexity-bounded generalisation)
8. FLRW extension of KS-covariance along KFLS 2024 line (open
   question (iv) now in v6.0.4 §7)
9. Watchlist active surveillance per V6-5 rule: Pedraza, Caputa,
   Bianconi, plus now Liu, Hollands-Longo, Kudler-Flam, Leutheusser,
   Satishchandran

### Long-term (multi-year)

10. M1 type-II theorem (FAILED.md F-1 re-open) — requires
    professional NCG collaboration, not solo work
11. Full FLRW type-II crossed-product with complexity source — a
    thesis-scale project

---

## Bottom line

**The two papers (v5, v6) are correctly scoped and correctly
positioned in the April 2026 landscape.** They sit in ACTIVE
clusters, are not threatened by any 2024-2026 publication, and both
benefit from verified literature integration (v6.0.4 just applied;
v5 revision draftable in 30 min).

**No new equation, no new falsifier, no new framework proposed by
this synthesis.** The gap-analyses are **working-programme maps**,
not paper-level contributions. The scientific-output pipeline
(pre-registered falsifiers + FAILED.md 17 entries + cross-model
audit) continues to deliver **diagnostic value** rather than
breakthrough claims.

**This is the honest ceiling for independent-researcher output
at this budget and scope in April 2026.** The next decisive
scientific event for us is either: (a) a type-II M1 theorem by a
professional collaborator, (b) DESI DR3 + Euclid DR1 release
(2026-2027), or (c) an independent FLRW-type-II extension
(expected 2-3 year horizon). We are correctly positioned to
integrate any of these when they arrive.
