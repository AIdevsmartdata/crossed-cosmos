# Pistes A+B+C+D — Consolidated synthesis (Opus max-effort)

**Date.** 2026-04-22 (late-evening session close).
**Inputs.** Five agent outputs:
- Piste A Sonnet → `piste_A_dr3_pipeline_plan.md` (commit `98e775f`)
- Piste B Sonnet → `piste_B_v7_liu_unification_plan.md` (commit with rule-1 alert)
- Piste B Opus max-effort → `piste_B_opus_deep_analysis.md` (commit `96195ad`)
- Piste C Sonnet → `piste_C_institutional_plan.md` (commit `246315d`)
- Piste D Sonnet → `piste_D_crosscutting_resources.md` (commit `f189871`)

## Immediate hygiene outcomes (already applied)

Two rule-1 (honesty-gate) failures were surfaced by the Piste-B
agents operating in parallel and were corrected before this
synthesis:

- **v6.0.5 (commit `5c1b630`)** — author attribution on arXiv:2601.07915
  corrected from "Liu et al." to
  **Chandrasekaran & Flanagan**. Independently confirmed by direct
  WebFetch. Root cause: the upstream v6 gap-analysis Sonnet agent
  (`a06fe21`) wrote "Liu et al." in its summary and I propagated the
  bib entry without primary-source authorship verification.

- **v6.0.6 (commit `c566fea`)** — §3 proof sketch terminology
  corrected from "Pinsker-style" to "variational (Connes-cocycle
  infimum)". Pinsker's inequality proper does not appear in either
  CF 2020 or Hollands-Longo 2025; the technique is a variational
  infimum formula. No scientific content change.

These two hygiene fixes are **the most concrete deliverable of the
Piste planning round**: the parallel-agent methodology caught errors
that a single-agent pipeline would have carried into JHEP
submission.

## Top-3 actions by Piste (concurrent)

### Piste A — DR3 pipeline first-mover
**Priority-1 action, week 1 (€0):** complete hi_class C-patch
validation tests E.2 (analytic small-ξ match) + E.3 (ξ=0.1 sanity)
+ weak-coupling guard; compare C-patch vs Cobaya-plugin route at
v5 MAP with 0.1% tolerance on H(z) and 0.5% on P(k, z=0).
**Gate for all Piste-A downstream.**

**Top-3 blockers identified:**
1. Euclid DR1 likelihood embargo (CRITICAL, 12-24 month window,
   outside our control). Mitigation: prepare a synthetic-Fisher
   stand-in as Plan B.
2. hi_class C-patch validation E.2/E.3 unimplemented (HIGH, gates
   MCMC trustworthiness). Fixable week 1, €0.
3. DR3 full-shape P(k) window-function convolution missing
   (MEDIUM, affects DR3 sensitivity). Implement during month 2-3.

### Piste B — v7 Liu/Chandrasekaran-Flanagan unification

**Recommended track: MVT2** (per Opus max-effort) — a 4-5 page
consistency note transporting Chandrasekaran-Flanagan 2026 Eq. 8.32
to modular time $\tau_R$ via Bisognano-Wichmann identification in
Killing-horizon regime. **Feasibility 8/10, risk 2/10, 2-3 months
solo at 12 h/week.**

**MVT2 seeds MVT1** (full complexity-bounded QFC theorem, solo
in 3 months has 85% failure probability without collaborator — do
not commit there first).

**Critical open lemma L2 — Simultaneous well-definedness:** do the
CF 2026 extended Hilbert space with gravitational edge modes and
the DEHK QRF crossed-product algebra admit a common dense uplift
domain? This is the binary gate: if yes, unification has technical
content; if no, v7 fails as F-20 and must be archived cleanly.

**Priority-1 action:** read CF 2026 §8.2 (the QFC proof section) in
full via WebFetch; run the commutant-nesting stability check
(Eq. 8.18) on the DEHK subalgebra as the concrete L2 diagnostic.

### Piste C — Institutional engagement

**Priority-1 action, week 1 (€0, 1 h):** submit chimere-omega-0.1
to **arXiv cs.LG** — no endorsement required, no affiliation
required, **establishes the author's arXiv account**. Every
subsequent physics-category (hep-th, gr-qc, astro-ph.CO)
endorsement request is strengthened once a live arXiv paper exists.

**Top-3 parallel actions:**
- cs.LG chimere-omega-0.1 submit (this week, 1 h)
- INSPIRE-HEP literature-suggestion for v5 + v6 Zenodo DOIs
  (this week, 1 h, 1-4 weeks curator response)
- Draft + send email Template B to Penington (CLPW, Berkeley) —
  narrow technical question on M1 and KFLS, NOT leading with
  endorsement request (this week, 30 min)

**Second-tier actions:**
- Emails to Faulkner / Speranza / Kirklin (MVT2 co-authorship on v7)
- Connes-Consani-Moscovici direct email (CCM 2-point formula for
  V7-Test5 re-opening)
- Workshop / associate position applications (medium-term)

### Piste D — Cross-cutting RAG + Compute + Knowledge

**Priority-1 action, week 1 (~2 hr, €0):** fetch the 4 missing RAG
entries that gate Piste B + strengthen Piste A bib:
- CF 2026 (arXiv:2601.07915) — full text cached, §8.2 annotated
- Hollands-Longo 2025 (arXiv:2503.04651) — for v6 §3 reinforcement
- Barrow 2504.12205 — for M3 observational caveat context
- Sanchez-Lopez-Karam-Hazra 2025 — for v5 literature alignment

**Top-3 resource investments:**
1. RAG fetch + INDEX.md update (2 hr, €0, unblocks Piste B writing)
2. v5.0.2 §3.5 Wolf-consolidated prose (30 min) — **already applied
   as commit `0165f12`**
3. arXiv hep-th endorser outreach (2 hr prep + 1-2 wk wait, €0)

**No cloud spend recommended this week.** Vast.ai is justified only
for DR3-class MCMC after hi_class C-patch validates.

## Cross-piste convergent findings

### Finding 1 — The parallel-agent methodology works

Two rule-1 failures caught in the same 30-minute window by agents
operating on different scopes (Piste B Sonnet = inventory planning;
Piste B Opus = proof-strategy deep-analysis). Both independently
WebFetched arXiv:2601.07915 and surfaced the Chandrasekaran-Flanagan
correction. The Opus agent additionally surfaced the Pinsker
terminology correction.

**Implication for pipeline:** the REGISTRY_FALSIFIERS + FAILED.md +
parallel-agent cross-check discipline pays exactly the dividend it
is designed to pay. We saved ourselves a rejectable submission.

### Finding 2 — Piste priorities converge on one sequence

Independent priority rankings from the 4 agents agree on an
immediate-first sequence:

1. **Week 1:** arXiv cs.LG submit (Piste C), RAG fetch (Piste D),
   hi_class E.2/E.3 validate (Piste A), Wolf edit *already applied*
   (Piste D cross-applied to v5)
2. **Week 2-3:** Penington / FS / Kirklin emails (Piste C), CF 2026
   §8.2 annotate (Piste B), v7 MVT2 scratch draft (Piste B)
3. **Month 2:** INSPIRE-HEP indexing (Piste C), DR3 full-shape
   window (Piste A), v7 MVT2 first draft (Piste B)
4. **Month 3-6:** Piste A compute commitment (DR3 mocks +
   Vast.ai validation), v7 MVT2 polish + internal adversarial
   (Piste B), institutional affiliation applications (Piste C)

### Finding 3 — Budget envelope

The entire **first-quarter programme (months 0-3) is €0 + author's
time**. The first cloud spend is at month 3-4 on Vast.ai H100
hi_class benchmarking, and the full pipeline validation (DR3-class
MCMC mocks on synthetic data) could reach €1-5k before real data
arrives. This is within the user's previously-stated budget envelope.

## Projected state at end of Q2 2026

If the 3-piste programme executes as planned:

- **v5.0.2** submitted to EPJ C via SCOAP3 (requires author decision
  on submission portal)
- **v6.0.6** submitted to JHEP via SISSA (requires endorsement
  obtained via Piste C / cs.LG first)
- **v7-MVT2** on arXiv as a 4-5 page note coupling
  Chandrasekaran-Flanagan QFC and v6.0.6 under the
  Bisognano-Wichmann dictionary
- **chimere-omega-0.1** live on arXiv cs.LG (the anchor submission)
- **hi_class NMC C-patch** validated, ready for DR3 data release
- **Zenodo archives** continue to serve as the authoritative DOI
  record for all four papers

## What NOT to do

The 4+1 agent outputs converge on a shared "do not" list:

- **Do not** re-open F-1..F-19 without new theorem-level input from
  external publications 2026+
- **Do not** attempt v8 theorematisation bridges without
  first-mover v7 MVT2 landing
- **Do not** launch Chimère Ω Phase 4 from-scratch training
  before any of the 3 Pistes closes
- **Do not** substitute a "review-style unification paper"
  (Opus Piste B MVT3) for a real MVT2 — the former has 10%
  scientific value vs MVT2's higher ratio
- **Do not** accept any agent-provided citation metadata without
  primary-source verification (lesson of v6.0.5 and v6.0.6)

## Owner decision points

The four Pistes yield a clear decision ladder; owner can accept or
modify:

**Do now (€0, this week):**
- [ ] arXiv cs.LG submit chimere-omega-0.1 (see Piste C Template details)
- [ ] RAG fetch CF 2026 + Hollands-Longo 2025 + Barrow 2025 + Sanchez-Lopez 2025 (agent script executable)
- [ ] hi_class E.2/E.3 validation against v5 MAP (fully local, no cloud)
- [ ] INSPIRE-HEP lit-suggestion submit for v5 + v6 Zenodo DOIs

**Do soon (next 2 weeks, €0):**
- [ ] Email to Penington (CLPW Berkeley) — Template B, narrow technical M1+KFLS question
- [ ] Email to Faulkner/Speranza/Kirklin — Template C, v6.0.6 awareness + MVT2 flag
- [ ] Optional: email to Connes-Consani-Moscovici — CCM 2-point formula for V7-Test5 re-open

**Do at month 1 (€0):**
- [ ] Annotate CF 2026 §8.2 in a scratch derivation file
- [ ] v7 MVT2 scratch draft: Bisognano-Wichmann dictionary + v6 Prop. 1 consistency check
- [ ] Submit v5.0.2 to EPJ C (SCOAP3) if no endorsement needed for astro-ph.CO
  or wait until cs.LG + endorsement landed

**Conditional (requires endorsement first):**
- [ ] Submit v6.0.6 to arXiv hep-th + gr-qc cross-list
- [ ] Submit v7-MVT2 to arXiv hep-th

## Bottom line

The Piste programme is honestly executable with €0-5k over
6 months. The rule-1 hygiene fixes already applied (v6.0.5 and
v6.0.6) are material gains from this round. The MVT2 target for
v7 is defensible if CF 2026 §8.2 annotation goes well in week 2.

No F-N entry added this session; two citation fixes instead —
positive outcome. The pipeline is working as designed.
