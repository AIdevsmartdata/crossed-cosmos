# PRINCIPLES.md — operational rules for future editing agents

Rules we learned the hard way. Each has a specific past incident (commit
SHA or adversarial report file) to anchor it; do not soften unless you
have a specific new reason.

---

**1. Honesty gate.** If a claim cannot be supported by the RAG cache
(`paper/_rag/`), the derivation scripts (`derivations/D*-report.md` +
`_results/*.json`), or a verified bibliography reference, STOP and log;
do not paraphrase from training-data memory. The moment you write a
number or a citation that you "remember", you are one edit away from a
fabricated reference.
*Anchor:* V3-adversarial (commit a20af13) and V5-adversarial (commit
0297eab) both surfaced this class of problem — silent orphan bib
entries in v4.3.0 were created by agents citing from memory.

**2. Cross-model adversarial is mandatory for load-bearing derivations.**
Claude-attacks-Claude misses same-family biases. Route at least one
adversarial pass per tag through a different model family: Magistral,
Mistral Large, DeepSeek, Gemini, or GPT. Same-family self-review is not
a substitute.
*Anchor:* V6-mistral-cross-check caught that Mistral's PPN derivation
is linear-in-ξ (graviton-dressing only); Claude's quadratic matches
canonical Chiba/Faraoni. A Claude-only adversarial would not have
produced the Chiba 1999 citation commit (4667039).

**3. Bib discipline.** No `\cite{KEY}` without verifying KEY exists in
`eci.bib` and the cited work actually supports the claim. No bib entry
without a `\cite{}` site (orphans accumulate silently because BibTeX
only warns on missing, not on unused). Run `bib_audit.md` script after
every bib edit.
*Anchor:* V5-adv (0297eab) caught 4 orphaned bib entries in v4.3.0
(AAL2023, DESY5, DESIForecast, Matsubara2003) plus a stale
`% TODO-BIB: Matsubara2003` comment blocking the A6 attribution.

**4. Unicode in .tex and caption hygiene.** No bare Unicode glyphs in
captions or prose; always `\Lambda`, `\xi`, `\chi`, `\sigma` etc.
hyperref's Unicode-in-PDFstring warnings are benign; compile-breaking
glyphs in captions are not.
*Anchor:* commit ef78f34 fixed a Λ → `\Lambda` caption leak in §3.7
that slipped through v4.6 pre-tag compile.

**5. Label hygiene.** No `\ref{sec:X}` without a matching `\label{sec:X}`
somewhere. Forward references to section numbers in prose ("§3.6") that
are not `\ref{}`-mediated break silently when sections are re-ordered.
*Anchor:* V5-adv m1 (2026-04-22) flagged "\S3.6" hardcoded on
eci.tex:57 and 68. commit 6b93377 fixed a §3.7 missing-label against
`sec:action`.

**6. Prose vs comment for heuristics.** A `% HEURISTIC` comment in the
.tex source is not sufficient. Load-bearing heuristic claims must say
"heuristic" in the visible prose so a reader without the source sees
the qualifier.
*Anchor:* V1-D8-verification §3 ("EFT bound δM_P² ≤ Λ²: assumption,
not theorem") led to the requirement R3 that "heuristic" appear three
times in §3.6 (body + Caveat 1).

**7. Release gate: no tag without an adversarial SHIP verdict.** Every
vX.Y tag must have a matching `_adversarial_review_vX_Y_*.md` with
verdict SHIP (not FIX, not BLOCK). If the verdict is FIX, apply the
fixes, re-run the adversarial, and tag only after SHIP.
*Anchor:* V5-adv FIX → commits b7510da + 4633ce8 → V5-adv-rerun SHIP
(d921099) → tag v4.3.0 only after. Same pattern V8 → v4.5.

**8. §5 / A3 / CryptoCensorship rule: if 6/6 reviewers flag it, demote
to appendix, don't rescue.** The v4.5 attempt to rescue A3 by adding a
toy dictionary made the weak step more visible, not less. Peer-v2
explicitly said so. The honest response is quarantine.
*Anchor:* `paper/_v4.5_A3_decision.md` (Option Y) → peer-v2 unanimous
rejection (`paper/peer_pre_review_v2.md` Key flip) → commit 775c184
quarantined §5 to Appendix A. Generalise the rule.

**9. Credit frugality.** Prefer Qwen / Magistral for bulk reviewer and
generation calls; reserve GPT-5.4 Pro / Opus 4.7 for single milestone
checks. A three-model triangulation at non-reasoning 1min.ai tier is
~530k credits; a single GPT-5.4-Pro call is ~1.26M.
*Anchor:* `paper/peer_pre_review_v2.md` Credit cost section — v2 pass
consumed 0.53% of budget; GPT-5.4-Pro alone would have consumed ∼1.3%.

**10. Silent wet-floor signs we've learned to avoid.**
   - `Bedroya2025` with eprint `2503.19898` is wrong; that arXiv ID is
     a Pan–Ye DESI NMC paper. The correct Bedroya reference is
     `2507.03090` ("Evolving Dark Sector and the Dark Dimension
     Scenario"). Verified V1 §5 + v4.2.1 bib audit (64939d5).
   - `AAL2025` refers to `2501.11690` "Two Micron-Size Dark Dimensions"
     (Fortschr. Phys. 73 e70015), not the AAL 2023 SM-landscape paper
     (`2306.16491`) — both exist; do not conflate.
   - `Matsubara2003` is `astro-ph/0006269` ("Statistics of Smoothed
     Cosmic Fields in Perturbation Theory I"), not `astro-ph/0305472`
     (Rossa–Dettmar). Verified via WebFetch in V5.
   - `Faraoni2000` is not in eci.bib; only `Faraoni2004` exists. Do
     not cite `Faraoni2000` without first adding the bib entry.
*Anchor:* `_v4.3_review_notes.md` 2026-04-22 bib fixes section.

**11. Ground-truth update requirement.** Any release tagged after v4.6
must also commit a delta to GROUND_TRUTH.md (if the scientific claim
changed) or a new DECISIONS.md entry (if only the rationale changed).
If neither is committed, the release is incomplete and the pre-tag
adversarial must fail with FIX. No silent scientific drift between
v4.6 and the next tag.
*Anchor:* this file (v4.6). Future enforcement.

**12. No claim larger than the derivation supports.** D5 is a scaffold,
not a working PH_k calculation; A6 prose must therefore not claim
PH_k discrimination vs bispectrum. D9 numerical B was inside 30% of
D7 analytic; D13 upgraded it to a tabulated B_num, so the prose now
quotes B_num and the Table, not the old (8/√3)A heuristic.
*Anchor:* D5 flagged in v4.0.1 self-audit; D13 propagation in commit
d8ff646 (v4.5).

**13. χ₀ fiducial discipline.** χ₀ = M_P/10 is the single fiducial used
across §3.5, §3.6, §3.7. Do not introduce a different fiducial in a
new section without explicit justification; χ₀-scan statements
(D9's B_local variation; D15's density range) must be flagged as
fiducial-dependent.
*Anchor:* V3-adv C16 (2026-04-22 `_adversarial_review_v4_2_1.md`)
verified χ₀ = M_P/10 identically in §3.5:51 and §3.6:68.

**14. Convention lock: do not touch §2 Conventions subsection without
re-running convention_audit.md.** Metric (−,+,+,+); Faraoni ξ > 0
attractive, `−½ξRχ²` in Lagrangian, `+ξRχ` in EOM; reduced Planck
M_P = 2.435×10¹⁸ GeV; natural ℏ = c = 1; cosmic t unless stated. Any
edit touching these four lines requires a full convention sweep.
*Anchor:* commit f62ea1d added the subsection; V7-adv §C verified 5/5
checks clean. Any silent flip is a major-physics regression.

**15. Forecast-pending vs null-result vs disfavoured: state the verdict
explicitly.** Each phenomenological subsection in §3 must state the
verdict in one of these four categories: **consistent**, **null-result
at current precision**, **disfavoured but non-discriminating**,
**forecast-pending**. Do not leave verdicts implicit.
*Anchor:* GROUND_TRUTH.md Part C. Adversarial reviews have twice had
to re-read §3.5 to extract the 3.29σ verdict (V3 C8, V8 item 10).

**16. Negative literature claims: soften or substantiate.** Sentences of
the form "to our knowledge has not appeared in the literature" are
hard to falsify and invite reviewer scepticism. If you must make one,
attach a specific literature-survey scope; otherwise rephrase as
"has not been tabulated in closed form in [specific references]".
*Anchor:* V8-adv NIT on §3.5 line 84 (2026-04-21).

---

## v6-specific rules (added 2026-04-22 on owner mandate)

**V6-1. No equality without proof — default to Wall-style inequality.**
The v6 equation form is
`dS_gen/dτ_R ≤ κ_R · C_k · Θ(PH_k)`,
NOT equality. Equality was attempted, three independent derivation agents
(Claude/Gemini/Magistral) all verdicted ANSATZ, adversarial landed fatal
Attack #2 (Krylov log regime becomes contradiction under equality).
The inequality form neutralises Attack #2 (Fan 2022 log becomes the
saturating limit) and aligns with every rigorous GSL precursor.
*Anchor:* D18 S/N < 0.5σ at fiducial falsifier, D18b bias-degeneracy
|ρ| = 0.998 — double-lock on pivoting to formal-track equality-to-inequality.

**V6-2. Each assumption labelled M1, M2, M3 in the prose.** Distinguish
POSTULAT / DERIVED / CONJECTURAL explicitly in every paragraph that
introduces one. No hand-waving "it is natural to assume". The reviewer
must see the assumption tree at a glance. Currently M1 (modular-complexity
ansatz Brown-Susskind-style), M2 (CLT/LLN for QRF coarse-graining in
dequantisation map), M3 (chameleon profile α = 0.095).
*Anchor:* V6 Claude derivation report flagged (I1), (I2) as Brown-Susskind
analogies with no type-II proof. The labels prevent silent re-hiding.

**V6-3. No "arrow of time" rhetoric.** Adversarial Attack #4 (arrow-of-time
tautology) is VALID: modular flow has built-in direction, C_k monotone
growth under Brown-Susskind gives the result automatically. Do NOT claim
the equation "explains" the cosmological arrow of time in v6. State only
what it implies: dS_gen ≥ 0 in the modular frame.
*Anchor:* V6-adversarial-attack.md Attack #4 (commit 5d1d052).

**V6-4. No cosmological falsifier in v6.** D18 and D18b killed the
fσ_8 × Θ(PH_2) falsifier at DR3+Euclid precision (S/N ≈ 0.36σ at fiducial,
σ(ε_0) degradation 27× under marginalisation, degeneracy with galaxy bias
b(z) |ρ| = 0.998). v6 is a FORMAL paper, not a cosmology paper. Do NOT
re-propose a cosmological prediction in the v6 draft; JHEP/PRD-formal
does not require one.
*Anchor:* D18-report.md commit 2d46fbe, D18b-report.md commit 9aee7f2.

**V6-5. Weekly scoop surveillance during drafting.** Check arXiv listings
for Pedraza-Svesko-Weller-Davies, Caputa-del Campo-Nandy, and Bianconi
every Monday until v6 is on arXiv. They are the groups most likely to
publish a time-differential gravity-from-complexity statement that
would scoop a component of v6. Log checks in
`paper/_internal_rag/v6_surveillance.md`.
*Anchor:* v6_audit.md §6 (commit 31525e1).
