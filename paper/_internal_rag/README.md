# paper/_internal_rag/

**Purpose.** Internal "what do WE know, and with what confidence" index for the
ECI framework paper. Distinct from `paper/_rag/`, which caches *external*
literature. This directory aggregates *our own* results: derivation outcomes,
adversarial-review verdicts, open caveats, and known-wrong attempts.

## For future editing agents — READ FIRST

Before you write any numerical claim, any bound, any verdict sentence in
`paper/*.tex`:

1. Open `INDEX.md`.
2. Section 1 — is the number you're about to quote already derived? Use the
   tabulated value with its stated confidence. Do **not** re-paraphrase from
   memory.
3. Section 2 — has an adversarial reviewer already landed a finding on this
   block? Respect the verdict; do not silently regress.
4. Section 3 — open caveat attached to the claim? Either address it or preserve
   the flagging language.
5. Section 4 — this approach on the rejected-attempts list? Don't re-propose it
   without an explicit new reason.

## What this index is NOT

- Not a substitute for reading the underlying `derivations/D*-report.md`,
  `derivations/_results/D*-summary.json`, or the cited `_adversarial_review_*.md`.
- Not a complete literature map (see `paper/literature_map.md`).
- Not a bibliography audit (see `paper/bib_audit.md`).

## How to use this directory

Future editing agents must read GROUND_TRUTH.md first, then DECISIONS.md,
then PRINCIPLES.md, before consulting INDEX.md for specific values, and
finally `_rag/INDEX.md` for external primary sources.

## Maintenance

After landing any new D*, V*, or adversarial review, append a row to the
relevant section of `INDEX.md` in the same commit. Keep entries terse — one
line per derivation result, one bullet per caveat. Move detail into the
source file, not the index.
