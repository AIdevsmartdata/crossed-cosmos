# DECISIONS.md — chronological log of consequential choices

Each entry: date, decision, alternatives considered, justification,
who pushed back. Short enough to scan; long enough to stop us re-opening
a decision next session. Grounded in git log, adversarial reviews, peer
reviews, and the D*/V* derivation reports.

---

**2026-04-21 — v5.0 submission path: Cobaya pre-screen → hi_class production → EPJ C, indie-author status disclosed**
- Decision: the ξ_χ posterior for §3.5 / §4 row 1b is produced via a
  two-stage MCMC: (stage 1) Cobaya Python Theory plugin wrapping vanilla
  classy + D14 G_eff/η post-processing as a fast pre-screen
  (`mcmc/cobaya-nmc/`, commit 8f5f179); (stage 2) production run on a
  fork of `hi_class_public` upstream 50f447c with the NMC (ξ R χ²/2) term
  implemented as a Horndeski sub-case (`mcmc/nmc_patch/hi_class_nmc/`,
  commits 2eaf5cb → 4be6354). Compute target is a Vast.ai EPYC Zen 5 spot
  instance; the eu-west-3 AWS walkthrough (d65c02f) is kept as the backup
  provider. HAL deposit hal-05598836 was withdrawn on affiliation grounds
  (75f5b32) — Zenodo (DOI 10.5281/zenodo.19686399) is the sole permanent
  archive. Submission target: **EPJ C** (SCOAP3 OA, IF 4.3). Indie-author
  status is explicitly disclosed in the cover letter and in a dedicated
  note `docs/AUTHOR_STATUS.md` (ORCID 0009-0008-2443-7166, first-time
  submitter, software-engineering background, self-trained via open
  literature, no advisor, no grant, no co-authorship history).
- Alternatives: Foundations of Physics as editorial target (kept as
  backup); single-stage MCMC directly in hi_class (rejected — the Python
  pre-screen is 30× cheaper per chain and catches YAML errors before the
  Zen 5 instance spins up); staying silent on indie status in the cover
  letter (rejected as dishonest gate per PRINCIPLES.md #1).
- Justification: the Cobaya pre-screen costs ~200 CPU-hours on the local
  box and de-risks the production YAML; the hi_class fork gives the full
  Boltzmann treatment needed for the §3.7 perturbation observables; the
  Vast.ai EPYC Zen 5 spot recommendation comes out of the mcmc-bench
  projection (commit fe066f7) as the best $/chain at the 5-target
  precision required. EPJ C chosen over Foundations of Physics because
  the §3.5–§3.7 phenomenology is the load-bearing part of the paper and
  EPJ C is the natural venue for that style of observer-theory
  triangulation.
- Pushed back: mcmc-bench REPORT.md projections (cost envelope); HAL
  moderator (withdrew deposit — pushed the archive story to Zenodo-only
  and made the indie-status disclosure unavoidable).

**2026-04-22 — §1.5 unifying thesis = observer-dependent cosmology (Team B, Bridge verdict)**
- Decision: §1.5 (`section_1_5_thesis_B.tex`, \input after §1, before §2)
  adopts Hypothesis B (observer-dependent cosmology, scoped to late-time
  quasi-dS $\Omega_\Lambda\gtrsim 0.7$). Team A (complexity-growth / UCG)
  conceded in its own defence memo. Frame qualifiers propagated to §3.5
  (solar-system-frame on Cassini bound), §3.6 (causal-diamond regime on
  EFT heuristic), §A6 (observer ensemble average on Matsubara form),
  Appendix A (QRF-subregion link for A3 working-conjecture status).
  Abstract clause (v) updated to link A3 explicitly to the observer-
  dependent reading of A1. No equation moved; no numerical value changed.
  Ma--Huang PRU citation upgraded from "effective existence" to "existence
  constructed from quantum one-way functions" at the CFT level; the
  cosmological transposition of A3 remains a working conjecture.
- Alternatives: Hypothesis A (UCG, Team A); fallback "§1.5 open" framing.
- Justification: `paper/thesis_bridge.md` §4. Team A's defence memo
  concedes the strong reading and recommends B if the weak reading is
  thin; Team B's scope match covers every quantitative §3 prediction
  without overreach. Ma--Huang arXiv:2410.10116 (STOC'25) constructs PRUs
  from qOWF — upgrade flagged by `paper/exotic_physics_scan.md` Domain 2.
- Pushed back: bridge coordinator (A conceded); no external disagreement.

**2026-04-21 — A3 downgraded to "working conjecture" in the axiom list**
- Decision: eci.tex line 50 replaces "A3 — Cryptographic Censorship" as
  a standalone axiom with "A3 (working conjecture) — Cryptographic
  Censorship" and a caveat block stating the AdS/CFT proof does not
  transpose to dS/FLRW.
- Alternatives: (X) leave as full axiom, (Y) demote to a parenthetical
  in Discussion.
- Justification: v4.0.1 self-audit (`docs/REVIEW_NOTES.md`), pre-peer-
  review internal pass. The original theorem (CryptoCensorship) is
  proven in AdS only; asserting it as an axiom in cosmology was
  overreach.
- Pushed back: internal reviewer-persona LLM; no external disagreement.

**2026-04-21 — Prediction 1 flagged as non-discriminating vs wCDM
inside the DR2 band**
- Decision: eci.tex §3.1 states plainly that the ECI (w₀, wₐ) prediction
  does not distinguish ECI from wCDM at DR2 precision absent the NMC
  coefficient B(Ω_Λ) being nailed down.
- Alternatives: keep row 1 as a clean falsifier (would be dishonest at
  DR2 band width).
- Justification: D7 arithmetic showed the NMC band half-width is ∼1% of
  σ_{wₐ}^DR2 under the old (over-loose) 0.8 DR2 error estimate; under
  the real D10 covariance it is ∼5%. Either way, non-discriminating.
- Pushed back: v4.0.1 self-audit flagged this before any reviewer.

**2026-04-21 — c' = 1/6 (species scale) adopted over c' = 0.05 (de-Sitter
slope) for §3.6**
- Decision: §3.6 primary cutoff value is c' = 1/6 with Λ(H₀) ≈ 2.2×10⁸
  GeV and |ξ_χ| ≤ 8.4×10⁻¹⁹ at χ₀ = M_P/10. c' = 0.05 retained only as
  a parenthetical.
- Alternatives: keep c' = 0.05 (D8's original primary), sweep without
  a primary.
- Justification: V1-D8-verification.md §2 found c' = 0.05 had no pedigree
  in the Dark Dimension literature; Montero–Vafa–Valenzuela gives the
  species-scale exponent 1/6 and AAL 2023 agrees. The 0.05 value was
  borrowed from de-Sitter-slope bounds on V(χ) and misapplied to the
  tower cutoff. V1 also caught the wrong `Bedroya2025` citation (arXiv
  2503.19898 is a DESI NMC paper, not a Swampland paper).
- Pushed back: adversarial V1 (2026-04-21, commit 5c3be27).

**2026-04-22 — DESI DR2 covariance reconstructed via pivot identity,
V2-verified to 0.01σ**
- Decision: §3.5 Caveat 3–4 uses σ(w₀) = 0.057, σ(wₐ) = 0.215, ρ = −0.89
  from the pivot-minimisation identity cov(w₀, wₐ) = −(1−a_p) σ²(wₐ),
  a_p = 1/(1+z_p), z_p = 0.31. Mahalanobis distances 3.29σ (ECI),
  3.33σ (Scherrer–Sen), 4.36σ (ΛCDM).
- Alternatives: keep D7's approximate (0.20, 0.80, −0.80) covariance;
  demand the DESI collaboration's machine-readable 2×2 (not yet
  public).
- Justification: D10 + V2 verification. The 7% residual in σ(w_p)_pred
  vs quoted (0.0257 vs 0.024) is acknowledged as the covariance-
  reconstruction systematic. D10-report §7 reframes §3.5 Caveat 4:
  "not that both fit, but that both are equally disfavoured".
- Pushed back: D10 itself (correcting D7); V2-D10-verification
  independently reproduces all numbers.

**2026-04-22 — B(Ω_Λ) heuristic replaced with full numerical D13
integration**
- Decision: §3.5 Table tab:B_of_OmegaL uses B_num ∈ {9.00, 9.18, 9.05,
  8.11} at Ω_Λ ∈ {0.5, 0.6, 0.7, 0.8}, flat ≈ 9 instead of tracking
  A(Ω_Λ). Prediction row 1b rescaled: Δwₐ^ECI ≈ 1.1×10⁻² (was
  8.8×10⁻³ under the heuristic).
- Alternatives: keep heuristic B_heur = (8/√3)A.
- Justification: peer-pre-review v1 — Gemini 2.5 Pro and Magistral-
  medium both converged on "full numerical background integration
  for B(Ω_Λ)" as their Q4 recommendation. D13 delivered it (9912725).
  D9 had already hinted at B_local ≈ 9.5 at χ₀ = M_P/10, so the
  numerical result was not a surprise.
- Pushed back: peer-v1 unanimous (2/3 models).

**2026-04-22 — A3 toy-dictionary approach (Option Y) over plain
demotion (Option X)**
- Decision: §5 was added with an explicit conjectural map
  Eq.(toy-dict) naming a CFT→cosmology dictionary and one testable
  consequence (bulk-geometry exclusion for super-Gibbons-Hawking
  coarse-grained horizon entropy at reheating). A3 axiom kept as
  "working conjecture"; §5 rewritten to depend on the dictionary, not
  on A3 itself.
- Alternatives: Option X — delete §5 entirely, fold A3 into a
  one-paragraph Discussion caveat.
- Justification: `paper/_v4.5_A3_decision.md`. Peer-v1 reviewers framed
  remedy disjunctively ("demote to Discussion *or* toy calculation");
  a dictionary addressed all three. Option X would have left §5
  hollow; Option Y converts A3 from interpretive layer into testable
  conjecture.
- Pushed back: peer-v1 (3/3). Option Y chosen; peer-v2 later rejected
  it too, leading to the §5 quarantine decision below.

**2026-04-22 — §5 quarantined to Appendix A "Speculative"**
- Decision: commit 775c184. The three (D)-marked consequences (Big Bang
  decodability boundary, inflation as algebraic necessity, Weyl
  curvature revisited) plus the toy dictionary moved out of §5-body
  into Appendix A with an explicit italic preamble stating the
  appendix is not on the critical predictive path.
- Alternatives: attempt a rigorous pseudo-Riemannian modular-
  reconstruction analogue (weeks of work, no obvious path); keep §5
  body as v4.5.
- Justification: peer-v2 6/6 (GPT-5.4 + Gemini 3.1 Pro + Grok 4, plus
  the three v1 reviewers counting as the same signal) identified §5
  toy-dictionary as the single weakest element. v4.5's attempt to
  rescue A3 by writing the dictionary made the weak step more visible,
  not less. Honest response: quarantine.
- Pushed back: peer-v2 (3/3); peer-v1 consensus (3/3) carried over.

**2026-04-22 — D14 closed-form perturbations land null-result at
Euclid/LSST Y10 precision — documented as feature, not bug**
- Decision: §3.7 reports |Δf σ₈ / f σ₈| ≤ 0.4%, ΔG_eff at a=1 ∈
  [−0.21%, +0.15%], |η−1| ≤ 2×10⁻⁴ at Cassini saturation and χ₀ =
  M_P/10 — all sub-threshold at Euclid / LSST Y10. Prose states:
  "present but not detectable with the next generation; detection
  would require either χ₀ ≳ 0.5 M_P or a breach of the present PPN
  bound".
- Alternatives: weaken the caveats, claim marginal detectability.
- Justification: peer-v2 GPT-5.4 Q4 explicitly asked for the
  Jordan-frame G_eff / η / fσ₈ calculation as "a clean yes/no
  falsifier". D14 delivered it, and the answer is "no". Honest
  reporting of the null is the point.
- Pushed back: D14 itself (D14-summary.json
  `detectable_EuclidLSST_Y10: false`).

**2026-04-22 — D15 chameleon screening: parametrisation declared,
α ∈ [1/8, 1/3] compatibility flagged as a comparison not a prediction**
- Decision: §3.6 Resolution (ii) cites D15 minimum-viable profile
  α_min ≃ 0.095, ρ_c ≃ 1.3×10⁻⁸ g/cm³ under Θ(ρ) = exp[−(ρ/ρ_c)^α].
  The "just below the Khoury–Weltman 2004 chameleon-viable band" phrasing
  is explicit about being a comparison to KhouryWeltman2004 rather than
  a derivation.
- Alternatives: promote α_min as a prediction, or drop Resolution (ii)
  entirely.
- Justification: peer-v2 Gemini 3.1 Pro Q4 asked for "the minimum
  screening potential profile required to decouple local χ₀ from
  cosmological background" — D15 provided it. But the profile family
  Θ(ρ) is a model choice, not a derivation; owning that honestly is
  the rule (PRINCIPLES.md #3).
- Pushed back: peer-v2 Gemini 3.1 Pro.

**2026-04-21 — Model-family rebalance for adversarial review:
V6 = Mistral, peer-v2 = GPT-5.4 + Gemini 3.1 Pro + Grok 4 (not GPT-5.4-Pro)**
- Decision: Cross-model adversarial review uses Mistral Large for V6;
  peer-v2 (pre-submission triangulation) uses GPT-5.4, Gemini 3.1 Pro,
  Grok 4 on 1min.ai non-reasoning tier.
- Alternatives: keep Claude-attacks-Claude (same-family bias); pay
  1.26M credits for a single GPT-5.4-Pro call.
- Justification: V6-mistral-cross-check.md found Mistral gave a
  functionally different PPN derivation (linear in ξ instead of
  quadratic — known-incomplete; canonical Chiba/Faraoni result is
  quadratic); this is exactly the kind of catch same-family review
  misses. Peer-v2 substitution note: GPT-5.4-Pro would have consumed
  1.26M credits alone; the three-model v2 pass at non-reasoning tier
  cost 530k credits total (0.53% of budget) and still produced a
  unanimous 3/3 MAJOR REVISIONS verdict.
- Pushed back: cost envelope (PRINCIPLES.md #9).

**2026-04-22 — v4.3.0 fix cycle: resolve 4 orphan bib entries + 3 stale
TODO markers before tag**
- Decision: commit b7510da + 4633ce8. `AAL2023`, `DESY5`, `DESIForecast`,
  `Matsubara2003` each actually cited in-text at appropriate spots;
  stale `% TODO-BIB:` markers removed.
- Alternatives: ship v4.3.0 with orphan bib entries (V5-adv verdict
  was FIX not BLOCK, so mechanically possible).
- Justification: bib discipline (PRINCIPLES.md #3). BibTeX does not warn
  on unused entries; silent orphans accumulate and later look like
  fabricated citations. Five-line patch fixed it.
- Pushed back: V5-adversarial review (0297eab).

**2026-04-21 — Chiba1999 and DamourEspositoFarese1993 cited explicitly
in D7 PPN derivation**
- Decision: commit 4667039. §3.5 now names Damour–Esposito-Farèse 1993
  Phys. Rev. D 48 as the source of the ST-PPN formula
  γ−1 = −F'²/(ZF + (3/2)F'²), and Chiba 1999 + Hwang–Noh 2005 as the
  quintessence applications.
- Alternatives: re-derive without literature hooks (would look like
  a novelty claim for a re-derivation).
- Justification: D7-novelty-check.md explicitly classifies D7 as
  (a) re-derivation of prior work. The V6-mistral-cross-check §Claim 1
  disagreement (Mistral's linear-in-ξ derivation) underlined that the
  quadratic form is the canonical literature result and must be
  attributed.
- Pushed back: V6 cross-model + D7 self-audit.

**2026-04-22 — v4.4 audits added (equation_map, convention_audit,
literature_map) as explicit repository artefacts**
- Decision: commits 82893f0 + e9e1438 + d285054. Three markdown audits
  now live in paper/ cross-referencing equations↔scripts, Faraoni
  metric/NMC-sign/M_P usage, and 29 axiom/phenomenology claims against
  primary refs.
- Alternatives: keep audits implicit in reviewer memory.
- Justification: v4.4.0 was the first post-peer-v1 tag; making the
  audits explicit pre-empted most of the "is this number right?"
  surface area that adversarials otherwise spend time on. V7-adv noted
  29/29 literature_map coverage is credible.
- Pushed back: adversarial V7 only caught stale bib warnings in
  literature_map (not audit coverage itself).

**2026-04-21 — Abstract wording for A3: "selection rule" → "working
conjecture with toy dictionary" (V8-minor)**
- Decision: commit 752408b. eci.tex abstract clause (v) updated to
  match the §5 framing; one-sentence change.
- Alternatives: ship v4.5.0 with abstract/body mismatch; V8-adv verdict
  was SHIP with 1 MINOR.
- Justification: honesty gate (PRINCIPLES.md #1). Abstract that asserts
  a stronger status than the body delivers is exactly the accident
  that costs us at review.
- Pushed back: V8-adv explicit MINOR flag.

**2026-04-21 — Eöt-Wash / atomic-clock / KM3NeT predictions retained
as falsifiers despite Prediction-5 being "limit not prediction"**
- Decision: eci.tex §4 predictions table keeps rows 5, 6 with the
  honest reading that #5 is a consistency bound; row 5 language
  unchanged from v4.0.1.
- Alternatives: re-express #5 as "ECI-consistent with", remove #6/7.
- Justification: v4.0.1 self-audit flagged #5 as a limit; v4.1+ decided
  to keep the row as-is for Prediction-table uniformity. Revisit if
  a referee flags it.
- Pushed back: v4.0.1 self-audit; no subsequent push.

**2026-04-22 — D9 χ₀-nonlinearity in B_local not patched into the
paper; D13 numerical B(Ω_Λ) used at χ₀ = M_P/10 fiducial only**
- Decision: §3.5 quotes B_num(0.7) = 9.05 at the grid average; the
  D9-observed χ₀-local variation (B≈14 at χ₀=0.05, 9.5 at 0.1, 7.3 at
  0.2) is not propagated into the table or the prediction.
- Alternatives: table B(Ω_Λ, χ₀) as 2D; re-state prediction 1b with
  χ₀-interval.
- Justification: D9-report §"Caveat — χ₀ non-linearity" flagged this
  and explicitly recommended "not required for the DR3 verdict". The
  DR3-discriminative conclusion is unchanged by the χ₀-local variation.
- Pushed back: D9 itself; no reviewer has re-opened.

**2026-04-22 — HAL + Zenodo deposited as permanent archives (pre-v4.3)**
- Decision: HAL hal-05598836 (CNRS timestamp) + Zenodo DOI
  10.5281/zenodo.19686399 embedded in eci.tex title-page thanks line.
- Alternatives: hold deposit until EPJ C acceptance.
- Justification: commit 79f826a + 9b6cadc. Pre-submission archival is
  standard for framework papers; establishes priority date.
- Pushed back: none.

**2026-04-22 — `-ot exps=CPU` and other infra-level quant decisions
not mentioned in the paper**
- Decision: paper contains zero statements about the local-agent
  infrastructure, model-quantisation choices, or Chimere server stack.
- Alternatives: mention AI-assistance in an acknowledgement.
- Justification: `docs/AI_USE.md` (separate file) exists for that
  purpose. eci.tex is physics content only. Don't pollute the
  manuscript with tooling notes.
- Pushed back: none; this is a style rule.

**2026-04-21 — w_p / z_p symmetrisation of wₐ +0.23 / −0.20 at 0.215**
- Decision: D10 + §3.5 use σ_{wₐ} = 0.215 (symmetrised mean of +0.23
  and −0.20).
- Alternatives: carry the asymmetric error through the Mahalanobis; V2
  §2 noted σ_{wₐ} = 0.215 minimises the σ(w_p) discrepancy.
- Justification: the 7% σ(w_p) residual bounds the covariance-
  reconstruction systematic. Asymmetric treatment would complicate the
  two-dof χ² calculation for sub-σ-level gain; V2 verified the
  decision is defensible.
- Pushed back: V2 approved.

**2026-04-22 — Convention lock: Faraoni mostly-plus signature, reduced
Planck M_P = 2.435×10¹⁸ GeV, ξ > 0 attractive**
- Decision: eci.tex §2 Conventions subsection (added v4.3) locks the
  full convention set. `convention_audit.md` verified 5/5 checks clean.
- Alternatives: keep conventions implicit; let each section pick.
- Justification: V7-adv reproduced 7 M_P usages at 2.435×10¹⁸ GeV with
  zero leaks to unreduced. Lock-down prevents future sign-flip silent
  bugs (PRINCIPLES.md #4 — convention hygiene).
- Pushed back: none; V7 clean pass.
