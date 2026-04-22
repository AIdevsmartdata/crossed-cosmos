# thesis_bridge.md — A/B synthesis for ECI §1.5

*Bridge-coordinator deliverable, 2026-04-21. Written after both teams
committed `draft_section_1_5_*.tex` and `defence_memo.md`. No `.tex`
source outside this file and `section_1_5_thesis_skeleton.tex` was
modified.*

## 1. Common ground

Teams A and B agree on four structural points, all consistent with
`GROUND_TRUTH.md` and `DECISIONS.md`:

1. **ECI v4.6 has no explicit unifying thesis.** The six axioms are
   stitched by shared Lagrangian content (§2) and shared late-time
   phenomenology (§3) but are not co-derived. Both teams accept this
   is an architectural synthesis, not a derivation
   (GROUND\_TRUTH Part A).
2. **A §1.5 slot would add editorial value** iff it does not over-claim.
   Both drafts stay within framework-genre discipline and route heavy
   lifting into honest caveats.
3. **A3 remains the hardest axiom to absorb.** Both teams explicitly
   concede that the pseudo-Riemannian modular-reconstruction theorem
   required to make the A3 cosmological transposition a theorem does not
   exist (Team A memo Part 2 item 1; Team B memo concession 4). Both
   defer to the Appendix-A quarantine established by v4.6 commit
   `775c184` (PRINCIPLES §8).
4. **Neither thesis disturbs the predictive core.** Team A closes its
   draft with "§3.1–§3.7, §4 is unaffected by whether UCG is adopted";
   Team B's "scope match" anchor shows every quantitative §3 prediction
   lives in the late-time quasi-dS regime its hypothesis actually
   covers.

## 2. Key disagreement

The disagreement is one-sided because Team A concedes:

- **Team A** (UCG / complexity-growth) admits in its own defence memo
  that the strong reading fails (`derivation_sketch.md` shows the
  shortest candidate derivation of Eq.(A6-euler) is quadratic in
  $\varepsilon$ where Matsubara is linear in $f_{\rm NL}$) and offers
  only a "weak reading" — a *shared linear-then-plateau profile*, not
  a shared object. In Team A's own words: "If the weak reading is
  considered too thin to justify a §1.5 at all, Team A concedes and
  recommends adopting Team B's alternative."
- **Team B** (observer-dependent cosmology, scoped to late-time
  quasi-dS) defends a narrower claim with a tighter footing: A4/A5/A6
  values are QRF-labelled in the regime where DESI DR2, Cassini,
  LSST Y10 actually measure them, with the static-patch asymptote
  supplying the CLPW/DEHK backing. It does NOT claim to unify the
  matter-era (EDE φ, BBN ξ_χ), and is explicit about this.

On A3: Team A tries to make A3 a specialisation of UCG via
Cryptographic Censorship + Haferkamp + Ma–Huang, but cannot close the
loop without the missing modular theorem. Team B re-reads A3 as the
horizon condition delimiting the subregion on which the QRF crossed
product remains well-defined; this is also not a theorem, but is at
least mathematically the *right type* of statement for the algebraic
framework A1/A2 already admits. **Team B's A3 re-reading is no more
rigorous than Team A's, but is structurally better aligned** with the
axioms already in the paper.

## 3. Honesty verdict

### Team A
- **Survives own defence memo?** Partially. The memo concedes the
  strong reading fails at two places (category mismatch C1, failed
  Gram–Charlier derivation per `derivation_sketch.md`). Only the weak
  reading — shared growth *profile*, not shared object — survives,
  and the author labels it "at the same speculative tier as Appendix A".
- **Publishable as §1.5 in v4.7?** Not as drafted. The box equation
  Eq.(UCG) is visually strong; the text admits it is an
  "analogy schema". That gap will look worse to a referee than it does
  to us. If §1.5 A is to be used, the box must be demoted and C1/C2/C3
  must move from `\emph{}` paragraphs into the running prose.
- **Notable strength.** The falsifier-alignment argument in Part 3(b)
  of the memo — UCG predicts *joint* failure of A3 and A6 under any
  observed monotonicity violation — is genuinely new content, even
  under the weak reading.

### Team B
- **Survives own defence memo?** Yes, in scope. The memo concedes
  matter-era FLRW, EDE, and BBN are outside Hypothesis B; it defends
  only the late-time quasi-dS regime (§3.1, §3.5, §3.6, §3.7). The
  scope match is exact: **every quantitative ECI prediction lives in
  the regime B covers**; the regime it does not cover (pre-recombination
  A4 via Poulin–Smith, BBN via Wolf) is already inherited wholesale from
  external literature in v4.6 and does not invoke the crossed product
  even absent §1.5.
- **Publishable as §1.5 in v4.7?** Close to ready. Part (iv) already
  carries the scope restriction. Minor revisions: label the static-
  patch-asymptote argument as "heuristic" in prose per PRINCIPLES §6
  (the $|\dot H|/H^2$ tolerance claim is explicitly "not a theorem");
  soften "organising principle" to "organising reading" to stay below
  the framework-vs-derivation line (GROUND\_TRUTH Part A).
- **Notable strength.** The re-reading of A4/A5/A6 as observer-frame
  quantities is *consistent with* — not in tension with — v4.6's
  existing Cassini/DESI/LSST Y10 phrasings, which already implicitly
  treat ξ_χ as a solar-system-frame quantity. B is the least-invasive
  unification.

### Fallback: "§1.5 open" framing
Viable if the owner rejects both drafts. The honest text would say:
ECI admits two candidate unifiers (UCG; observer-dependent cosmology);
neither is a theorem; the framework paper does not select between
them. This is not our recommendation because Team B's scoped reading
is ready and Team A has volunteered to yield.

## 4. Recommended editorial path

**Pick B, scoped.** Integrate a version of `draft_section_1_5_B.tex` as
§1.5 in v4.7, with the three minor revisions listed above.

**One-sentence justification.** Team A's own defence memo
(`paper/team_A/defence_memo.md`, Verdict section, lines 88–91) states
that its thesis "does not cleanly survive the hostile reviewer
objection" and explicitly recommends adopting Team B if the weak
reading is thin; Team B's defence memo (`paper/team_B/defence_memo.md`,
"Scope match" anchor, lines 57–61) demonstrates that the late-time
quasi-dS scope restriction covers every quantitative §3 prediction
without overreach. The asymmetry of the two defence memos — one
conceding, the other defending within scope — makes B the dominant
choice.

**What we are NOT doing.** (i) We are not claiming B is a theorem; it
remains a reading. (ii) We are not re-opening the A3 quarantine; §5
stays in Appendix A (PRINCIPLES §8). (iii) We are not promoting B to
a derivation of the six axioms; it re-labels A4/A5/A6 as frame-valued
and A3 as a self-consistency condition, which is weaker than derivation
and is marked so.

## 5. Proposed §1.5 skeleton

Committed as `paper/section_1_5_thesis_skeleton.tex`. It is a standalone
scaffold, not `\input`-ready; compilation is not attempted.

## 6. Cross-dependency map

| §1.5 B content | Touches existing section | Scope of impact | Risk |
|---|---|---|---|
| QRF-labelled $\xi_\chi^{(\mathcal R)}$ reading | §3.5 Caveat 2 (PPN scaling) | Add one sentence: "Cassini constrains the solar-system-frame value". No equation edit. | Low |
| Observer-frame $c'$ reading | §3.6 Caveat 1 (heuristic EFT bound) | Compatible; the species-scale cutoff already references a causal diamond. No numerical change to the $8.4\times 10^{-19}$ figure. | Low |
| Frame-averaged $\mathrm{PH}_k$ reading | §A6 / Appendix on Matsubara baseline | Adds one-sentence caveat that Matsubara is the ensemble average; no equation edit. Aligns with PRINCIPLES §12 (no claim beyond derivation). | Low |
| A3 as horizon condition delimiting QRF subregion | Appendix A (§5 quarantine) | Adds one sentence linking A3's working-conjecture status to the subregion on which A1 is well-defined. Does **not** re-inflate A3 into the main body (PRINCIPLES §8). | Low |
| Matter-era scope exclusion | §3.2 (EDE), §3.5 Wolf 2025 BBN paragraph | One explicit sentence: "Hypothesis B does not cover pre-recombination inputs." Preserves existing v4.6 wording. | Low |
| §3.7 perturbation phrasings | §3.7 | No change required; D14's sub-horizon quasi-static regime is already late-time. | None |
| Abstract | Abstract | Optional one-clause addition: "... organised, in the late-time limit, by an observer-dependent reading of A4–A6." Must not inflate (V8 precedent, DECISIONS 2026-04-21 abstract-fix). | Medium — watch abstract/body consistency gate |
| Ground-truth ledger | `_internal_rag/GROUND_TRUTH.md`, `DECISIONS.md` | PRINCIPLES §11 requires a DECISIONS.md entry for v4.7 reflecting the §1.5 addition and its scope restriction. | Required |

**Scope verdict.** Impact is one-sentence-per-section throughout §3;
no equation or numerical result in §3.1–§3.7 needs to move. Appendix A
gets one additional sentence linking A3's working-conjecture status to
the subregion the crossed product is defined on. The abstract may get
one careful clause. **No §3.5 Caveat 4 rewrite** (Team A's thesis, had
it been chosen, would have forced a rewrite there via UCG re-reading
of the 3.29σ Mahalanobis result; B does not).

---

*End of bridge. Total: ≈ 1450 words.*
