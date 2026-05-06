# M31 verdict — BSD × ECI tools

**Date:** 2026-05-06
**Status:** CONFIRMED-DEAD-END (BSD itself) + SUBSUMED-BY-M27 (higher-weight analog)

---

## One-line verdict

ECI tools (M13.1, LMFDB 4.5.b.a, Beilinson regulator from M27) make **no
contribution to the Birch-Swinnerton-Dyer conjecture**, because BSD concerns
elliptic curves over $\Q$ (equivalently weight-2 newforms by Wiles-BCDT
modularity), while $f = $ 4.5.b.a is weight 5. The natural higher-weight
analog (Bloch-Kato Tamagawa number conjecture / Beilinson at $s=k=5$) is
relevant to $M(f)$ and is already documented in M27.

## Probability table

| Direction | Probability of new contribution | Reason |
|---|---|---|
| BSD itself (Clay statement) | <0.05% | Weight 2 vs weight 5 irreducible mismatch |
| Bloch-Kato Tamagawa for $M(f)$ at $p=2$ | n/a | Same content as M13.1 paper-2 (not BSD) |
| Beilinson regulator at $s=k=5$ | n/a | Already M27's Conjecture M27.1 |
| Skinner-Urban-style anticycl. IMC | n/a | Already M28 conditional remark |

## Recommendations to ECI v7.5/v7.6/v7.7 lead

1. **DO NOT** mention "BSD" or "Birch-Swinnerton-Dyer" in any v7.x section
   header. It would be misleading and invite hostile referee response.
2. **DO** add the following one-paragraph footnote to M13.1 paper-2 §6
   "Outlook" (between the M27 Beilinson-regulator paragraph and the M28
   anticyclotomic-IMC paragraph) for reader/referee benefit:

   > *Relation to BSD.* The Birch-Swinnerton-Dyer conjecture is a statement
   > about elliptic curves over $\Q$, equivalently about weight-2 newforms
   > via the modularity theorem (Wiles 1995; Breuil-Conrad-Diamond-Taylor
   > 2001). The newform $f$ studied here has weight 5 and is not associated
   > to any elliptic curve over $\Q$, so BSD itself does not apply. The
   > natural generalisation to the weight-5 motive $M(f)$ is the Bloch-Kato
   > Tamagawa number conjecture (Bloch-Kato 1990) at non-critical integer
   > points, equivalently the Beilinson regulator pairing on
   > $H^2_\mathcal{M}(K_3, \Q(j))$ at $s = k = 5$ (Beilinson 1984;
   > Deninger-Scholl 1991). Conjecture M13.1, if proven, supplies 2-adic
   > information at the prime $\ell = 2$ entering the Tamagawa factor of
   > this conjecture; see [M27 companion note] for a precise formulation.

3. **DO NOT** create a separate M31 paper. M31 produces no standalone
   content.
4. **MERGE** all "ECI vs Clay millennium problems" framing into a single
   §7 "Scope and what this work does *not* claim" of paper-2, citing M27
   (Hodge), M28 (RH), this M31 (BSD), M30 (Navier-Stokes), and the upcoming
   yang-mills sub-agent if any. Use the Phase 3.F dead-end count to
   *strengthen* the credibility of the *positive* M13.1 + M27.1 +
   anticyclotomic-IMC content by making clear what is and is not being
   claimed.

## Collaborator targeting

**None new.** Do not approach Wiles / Skinner / Urban / Bhargava / X. Yuan /
S. Zhang (BSD specialists) with this work. The Beilinson-side targets
(Scholl, Loeffler-Zerbes) are already in M27's outreach list.

## Discipline closeout

- Hallu count: **85 → 85** (held)
- Mistral STRICT-BAN: respected
- 3 files only (SUMMARY ≤ 80 lines, exploration_log ≤ 150 lines, verdict ≤ 80
  lines): respected
- Anti-stall: NO drift to Bash settings.json
- 0 new arXiv lookups successfully executed (WebFetch denied for Clay page,
  one accidental retrieval of unrelated arXiv:1407.1093 — discarded, no
  fabricated bibdata produced)
- 0 new author names, 0 new arXiv IDs, 0 new bibitems introduced
