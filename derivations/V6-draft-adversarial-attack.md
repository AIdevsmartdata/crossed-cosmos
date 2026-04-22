# V6 JHEP draft — adversarial attack (hostile referee simulation)

**Date.** 2026-04-21.
**Target.** `paper/v6/v6_jhep.tex` (commits 2d0db1c, 1b55519) +
`derivations/V6-inequality-derivation.{py,md}` (4f9a601) +
`derivations/V6-dequantisation-map.{py,md}` (459ed22).
**Compile.** `latexmk -pdf v6_jhep.tex` up-to-date. 4 pages
(RevTeX fallback, jheppub class 404 on SISSA). 0 undefined refs.
Warnings are benign (hyperref Unicode PDFstring, nameref label).

---

## Per-attack verdict

### Attack 1 — Wall-style pivot / "trivial restatement × Θ"
**Verdict: REBUTTABLE.** A sharp referee will press: the structural
move `RHS_{Wall} · Θ(PH_k)` with `Θ ∈ [0,1]` is *weakening* an already
rigorous inequality by multiplying by a number in [0,1]. Strictly, any
valid Wall-style upper bound remains valid after such multiplication
only if one is multiplying on the LHS of a lower bound, *not* the RHS of
an upper bound — so the activator *strengthens* the claim, not weakens
it, and therefore the inequality is *not* automatic. The content is
genuinely in the M1 identification (modular RHS ↔ κ_R C_k) and in the Θ
multiplicative insertion (M2). Derivation.md §6 pre-flags the additive-
vs-multiplicative ambiguity honestly. The rebuttal survives review *if*
§3 main text explicitly asserts the sign-of-bound logic; currently it
does not. FIX: one sentence in §3 clarifying that Θ strengthens, not
weakens, and that therefore the bound is non-vacuous.

### Attack 2 — M1 Pinsker on modular-flow states
**Verdict: WEAK (i.e. attack lands).** The draft §3 proof sketch says
"spectral decomposition into modular-commutator + operator-growth"
without citing Ceyhan–Faulkner 2020 (half-sided modular pushforward) or
Longo 2019 (positivity) — both of which *are* invoked in the
derivation.md Step 1–2 chain. A JHEP referee will note the
Pinsker-style bound `−dS_rel/dτ ≤ |d⟨H_mod⟩/dτ|` is stated without the
modular-flow justification. Worse, `CeyhanFaulkner2020` and `Longo2019`
are *not present* in `eci.bib` at all (grep confirms). The rigorous
half of Step 1 in derivation.md therefore rests on two uncited works.
This is a load-bearing omission. FIX: add Ceyhan–Faulkner 2020 and
Longo 2019 to eci.bib, cite in §3 proof sketch, state the Pinsker
variant used (Jenssen–Shor style for modular-flow-covariant states).

### Attack 3 — C_k operational definition on physical ρ_R
**Verdict: WEAK (attack lands).** §2 says C_k is "Ma–Huang PRU sense …
interpolates between circuit complexity and information-theoretic
complexity", citing `MaHuang2025, Haferkamp2022, CryptoCensorship`.
But Ma–Huang defines C_k through *distinguishing oracles on ensembles*,
not through a single-state functional. The draft asserts `C_k[ρ_R]`
as a state-dependent functional with no operational recipe. A referee
can legitimately ask: given a single reduced density matrix ρ_R on a
type-II factor, what number is C_k[ρ_R]? The Haferkamp construction
is for unitaries; the Ma–Huang one is for ensembles. Neither directly
yields `C_k[ρ]`. FIX: either (a) define C_k[ρ_R] via the minimal
complexity of any purifying circuit (Stanford–Susskind operational
route), (b) define it as C_k of the modular unitary `e^{−i H_mod τ}`
(Caputa–Magán-style, which is what M1 actually uses), or (c) explicitly
POSTULATE that such a functional exists and label it accordingly. (b) is
cleanest and aligns with derivation.md Step 2.

### Attack 4 — Quantum→classical compression via dequantisation
**Verdict: REBUTTABLE.** The derivation.md §4 / dequantisation-map.md
§6b explicitly notes that `δn` only feeds the **RHS** of the inequality,
so upper-bound control suffices — no information-loss claim is made.
This is a clean answer. The draft §4 currently buries this by saying
"resolves the category mismatch" without restating that Θ(PH_k[δn])
is an *upper envelope* that needs only to bound, not reproduce, the
quantum source. FIX: one sentence in §4 stating "PH_k[δn] provides an
upper envelope on the RHS; no lossless reconstruction of ρ_R is claimed
or needed".

### Attack 5 — α = 0.095 numerology
**Verdict: VALID (attack lands cleanly).** §3 Ass. M3 says α = 0.095 is
"inspired by Barrow Δ ≲ 0.1". This is pattern-matching, not derivation,
and the draft admits as much ("candidate anchor, not a derived
quantity"). The honest framing is acceptable in an ansatz paper, but a
JHEP referee will still flag it as unnecessary precision. The number
`0.095` has three significant figures and no anchor chain. FIX:
either derive α from Barrow fractal-dimension relation (α = Δ/2 or
similar), or demote to "α ∈ (0, 0.1]" range in M3 and remove the
specific numeric 0.095 from the main text. The latter is cheaper and
safer.

### Attack 6 — Fan 2022 "saturation" claim
**Verdict: REBUTTABLE.** The draft §3 and abstract claim Fan 2022 log
regime is the saturating limit. Derivation.md §3 L2 and §4 Attack #2
response neutralise this: Fan's `dS_K/dt ≈ dC_K/(C_K dt)` is
*logarithmic in complexity*, which sits *below* a linear-in-C_k bound,
so it's consistency, not saturation. The draft §3 text already
explicitly says "as the saturating, not derived, rate" and "a
consistency check, not as a derivation of Eq. (1)". That is the
correct framing. However, the abstract still says "saturates to the
Fan (2022) logarithmic Krylov regime" — which on a quick read suggests
equality, not consistency. FIX: abstract wording change from
"saturates to" → "is consistent with, as a sub-linear regime under".

### Attack 7 — M1-independent consequences
**Verdict: VALID (hardest attack).** Every non-trivial consequence
of Eq. (1) rides on M1 (Ass. 1). If M1 fails, the paper degenerates to
Wall/FS24 + topological decoration + dequantisation map. The latter
three are genuine technical contributions (especially the
dequantisation map, which is new and cleanly posed), but the draft
frames the package as if M1 is the load-bearing result. This mis-sells
the contribution. Honest reframing: the dequantisation map +
Θ(PH_k[δn]) activator structure is *the* JHEP-worthy contribution; the
M1 identification is a conjectural scaffold. FIX: §1 introduction
should promote the dequantisation map (Def. 1) to co-equal billing
with Eq. (1). Currently §1 novelty (c) understates the map.

### Attack 8 — Overlap with Pedraza–Svesko–Weller-Davies 2022/2023
**Verdict: WEAK (attack lands — citation gap).** Grep confirms:
`Pedraza2022Threads` and `Carrasco2023` ("Gravitation from optimized
computation") are in `eci.bib` but *not cited* in `v6_jhep.tex`. Their
program derives linearised Einstein from a complexity first-law — which
is precisely the differential-complexity-to-gravity direction of our
Eq. (1). A JHEP referee familiar with the field will flag this
omission as either ignorance or obfuscation. This is an orphan-bib
entry (PRINCIPLES.md rule 3 violation in the making). FIX: add a
paragraph in §5 "Relation to existing GSL statements" — new
sub-paragraph (L5) Pedraza–Svesko–Weller-Davies complexity-Einstein
program — stating that their result derives gravity from a complexity
first-law (equality, integrated) whereas ours is a differential
inequality, modular-time-resolved, with an explicit topological
activator. Cite both `Pedraza2022Threads` and `Carrasco2023`.

---

## Overall verdict

**FIX.** The draft is not SHIP-ready for JHEP but is not BLOCK-worthy
either. Three attacks land cleanly (2, 3, 8); two more land partially
(5, 7). The fixes are all editorial / citation-level, not derivational —
no new theorem needed, no new scripts needed. Estimated effort: one
afternoon of editing + two bib entries. After fixes, the draft is
JHEP-submittable at the "formal framework + labelled postulates + toy
computation" level, which is acceptable in JHEP for ansatz papers
backed by limit checks.

## Top 3 attacks a JHEP referee will actually use

1. **Attack 8 (Pedraza et al. overlap).** Easiest referee hit — two
   orphan bib entries that a field-literate referee will catch in
   30 seconds. Highest signal-to-effort for the referee.
2. **Attack 2 (M1 Pinsker / missing Ceyhan–Faulkner, Longo citations).**
   The rigorous-half of the derivation currently cites its anchors only
   in the companion `.md`, not in the `.tex`. A referee who reads only
   the paper will see the Pinsker bound appear without modular-flow
   justification.
3. **Attack 3 (C_k operational on ρ_R).** The state-dependent functional
   `C_k[ρ_R]` is invoked without an operational recipe; the Ma–Huang /
   Haferkamp citations do not directly supply one. A referee in the
   complexity community will press hard here.

## Minimum modifications to move FIX → SHIP

1. Add `CeyhanFaulkner2020` and `Longo2019` to `eci.bib`; cite in §3
   proof sketch (Attack 2).
2. Cite `Pedraza2022Threads` + `Carrasco2023` in §5 with new (L5)
   sub-paragraph demarcating our differential-inequality vs their
   integrated-equality (Attack 8).
3. Define `C_k[ρ_R]` operationally in §2 as C_k of the modular
   unitary `e^{−i H_mod τ_R}` (Caputa–Magán route), or explicitly
   elevate to postulate M1' (Attack 3).
4. Abstract edit: "saturates to the Fan (2022)..." → "is consistent
   with the Fan (2022) logarithmic Krylov regime as a sub-linear
   saturating limit" (Attack 6).
5. §3 sentence clarifying sign-of-bound logic for Θ (Attack 1).
6. §4 sentence stating PH_k[δn] is an upper-envelope on RHS, no
   lossless reconstruction claimed (Attack 4).
7. §1 introduction: promote dequantisation map (Def. 1) to co-equal
   novelty billing with Eq. (1) (Attack 7).
8. §3 M3: demote α = 0.095 to "α ∈ (0, 0.1]" or add Barrow derivation
   (Attack 5).

After items 1–8 above, a re-run of this adversarial pass is expected
to drop all WEAK verdicts to REBUTTABLE and yield SHIP.

Word count: ~1380.
