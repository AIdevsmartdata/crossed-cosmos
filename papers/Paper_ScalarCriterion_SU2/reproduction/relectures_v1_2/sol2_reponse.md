**(A) Verification of previous corrections**

Line numbers refer to [the revised TeX](scalar_criterion_su2_v1_2.tex).

| Requested correction | Result |
|---|---|
| Minimum-side restriction in both summaries | **Applied**, lines 231 and 542. |
| Remarks (ii), (iii) | **Applied correctly**, line 526: simplicity is a conclusion on the stated domains; assumptions have no upper cutoff. |
| Domain caption | **Applied**, line 304. The (W2) row itself remains inconsistent; see below. |
| Lean count and freezing chronology | **Applied correctly**, line 1021. Inspection confirms seven `theorem` declarations, including four principal statements. |
| Chronology and reading scope | **Applied in §1.4**, lines 190–191, but stale wording remains elsewhere. |
| AI disclosure | Astra is credited; earlier Sol reports are distinguished. Older preparation paragraphs still need version labels. `@@RELDONE@@` is intentional and **not a finding**. |
| Round trip | **Correct**, lines 89 and 542: (B*) at \(T_0\) implies (B*) at \(32T_0\). |

I found no new mathematical error in Theorem R or its constants. The abstract’s numbered list remains compatible with its subsequent R paragraph. Section 6’s “converse” concerns the distinct thermal-trace estimate; the historical “we did not know” at line 227 is properly scoped.

**(B) Findings**

1. **NON-BLOCKING — attribution and normalisation, line 173; BFS79 entry, line 1104.**

   The OCR fairly supports identifying the positive-transfer/concavity argument and its application in every direction. It does not support presenting the reconstructed inequality as a directly verified transcription. Also specify \(L\le L'\), and retain the volume exponent when describing the partition-function comparison.

   Suggested replacement:

   > “Step 1 follows from the elementary monotonicity of the counting-measure \(\ell^p\) norms: for \(0<L\le L'\), whenever the traces are finite, \((\operatorname{Tr}T^{L'})^{1/L'}\le(\operatorname{Tr}T^L)^{1/L}\). Lemmas 7.12 and 7.44 of BB26v5 contain related thermal-trace and tube-energy monotonicities; the precise pressure statement used here follows from the spectral representation. The OCR of BFS79, PDF p. 39, describes this concavity argument and its application in every direction. Its garbled formula is reconstructed here, giving \(Z(\Lambda)\ge Z(\widetilde\Lambda)^{|\Lambda|/|\widetilde\Lambda|}\).”

   Thus **\(\ell^p\)-norm monotonicity is the right justification**; “is in Lemmas 7.12 and 7.44” needs the qualification above. The bibliography already honestly labels its journal metadata unverified. Identify the scanned source more precisely as “IHES/P/78/237, June 1978, PDF p. 39.”

2. **NON-BLOCKING — (W2) row, lines 280–281.**

   It still says \(N\ge1\), although the Wilson function was introduced on periods \(\ge2\). Replace the domain clauses with:

   > “For every spatial section with all periods at least \(2\) … \(Z_\beta(\sigma,N)=\operatorname{Tr}K_\sigma^N\) for every \(N\ge2\). Section 4 uses this identity only for spatial periods and times at least \(3\).”

   The stronger Lean domain is already disclosed correctly.

3. **NON-BLOCKING — remaining comparison wording.**

   - **Line 184:** replace “after this note was written” with “after the initial version 1.0 draft had been written.”
   - **Lines 916–917 and 1102–1103:** replace the restricted reading description with “the passages listed in §1.4; the remaining text was searched by keywords.”
   - **Line 918:** “their conclusion is wider at a given scale” lacks its former qualification. Replace with:

     > “Their conclusion extends beyond the dyadic-cube conclusion of Theorem 3; Theorem R supplies our extension to arbitrary integer cubes and bounded-aspect-ratio tori.”

   “Incremental content” (177–180) and “Reach” (933–937) are not false, but would better represent v1.2 with one added sentence mentioning R’s scale equivalence and extended spatial domain.

4. **NON-BLOCKING — historical provenance, lines 1011, 1018, 1082 and 1086–1089.**

   Label the older “final package” and Fable/Sonnet preparation descriptions explicitly **v1.0**. Otherwise the claims that the two complete subtrees match the final package conflict with v1.2’s additions inside `lean/`.

   Suggested clarification:

   > “These original rebuild and preparation descriptions concern version 1.0. Version 1.2 adds separate Lean files, whose preparation and rebuilds are described in the dedicated v1.2 paragraphs.”

**Counterexample search.** I analytically tried positive ring products and direct sums
\(Z=e^{a|x|}Z_\rho+e^{b|x|}Z_\sigma\), allowing section-dependent crossings of the leading blocks. A leading multiplicity \(g_t\ge2\) forces \(h_t(m)\ge\log g_t\); the independently checked bounds \(h\le1/992\) for cubes and \(h\le18/31<\log2\) for the stated aspect-ratio domain exclude those crossings under the small-defect hypothesis.

An excited eigenvalue of one section may equal another section’s leading eigenvalue: a bulk rescaling can create such coincidences without changing any ratio or defect. The proof never compares those absolute eigenvalues.

Every recursion profile needed at base \(m\ge3\) uses periods \(m,2m,4m\), so no additional recursion hypothesis failed within the paper’s domain. Arbitrary extensions below \(3\) can violate Lean’s all-positive-period `HypRec`; this is precisely why its stronger domain matters. **No counterexample to (a)–(d) was found.**

**(C) Verdict**

**PASS WITH NON-BLOCKING CORRECTIONS.** Theorem R stands under the stated global (W1)–(W2). Complete the planned review disclosure when the reports are recorded. This review used file-reading tools only; no writes, builds, scripts or network access occurred.

memory consulted: `critere_scalaire`, `critère scalaire`, `réciproque/reciproque`, `pression/monoton`, `7.44`, `Brydges`, `27/3968`; grep substituted for the inspected guard, which invokes Python. [PISTES.md:59](/root/physique/chantiers/pistes_2026-11-12/PISTES.md:59) already records R; “converse unknown” in [dossier_ym.md:374](/root/physique/qlab/prompts/dossier_ym.md:374) is superseded at line 387.

palette: spectral power sums → monotonicity and multiplicity tests; dyadic recursion/geometric series → \(2/31\); exponential convexity → aspect-ratio bound / discarded: entropy as a gap mechanism (no additional bound), Knabe analogy (no applicable local-Hamiltonian estimate). No unconditional Coulomb-phase/5D gap or scale uniform in \(\beta\) follows.