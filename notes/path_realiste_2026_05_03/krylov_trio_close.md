# Krylov-Diameter Theorem 4 — Trio Closure Attempt

**Date:** 2026-05-02
**Trio under test:** Vardian arXiv:2602.02675 ⊕ Heller-Papalini-Schuhmann arXiv:2412.17785 (PRL 135, 151602) ⊕ Leutheusser-Liu arXiv:2508.00056
**Target:** upgrade `paper/krylov_diameter/krylov_diameter.tex` Theorem 4 (Krylov-Diameter Correspondence) from "conditional on UOGH transfer" to **unconditional**, using a published chain
> modular Krylov spread complexity = log Jones-index of entanglement-wedge subalgebra inclusion = holographic complexity-volume

**Method.** arXiv-API verification (3 papers, opensearch:totalResults=1 each). Full PDF download + page-1 inline read of HPS (pages 1-9, 9-page PRL letter). Vardian PDF (11 pp.) read in detail in the prior /tmp/M1C_vardian_hollands.md run. Leutheusser-Liu (45 pp., HTML) read for Eq. (4) and the Kosaki-index disclaimer.

---

## (1) Verbatim 1-line theorems with equation numbers

**Vardian 2602.02675, eq. (26)** (verbatim, p. 4):
> "O ∈ A → {a^O_n, b^O_n} → (L_S)_{mn} = [tridiagonal Lanczos matrix] → P_O K|_A P_O : spectrum of K|_A → Area Operator."

with structural identity (eq. 27): `L_A = ⊕_α S(χ_α, M_A) P_α = K_A ⊗ I_Ā − K|_A`. Operator modular Liouvillian (eqs. 33–34): `L_S O := [K_A ⊗ I_Ā, O]`.

**Heller-Papalini-Schuhmann 2412.17785 = PRL 135, 151602, eq. (13)** (verbatim, p. 3):
> "2 |log q| C_K(t)_β = ⟨L̂⟩ = [−∂_∆ ⟨e^{−∆L̂}⟩]_{∆=0}"

with operator form (eq. 30): `2 |log q| K̂ = L̂`. The state is `|ψ(t)⟩_β = Z_β^{−1/2} e^{−iT(t−iβ/2)} |0⟩` (eq. 32) on the DSSYK chord Hilbert space, dual to **sine dilaton gravity** (action eq. 2). NOT log Jones-index. Setting: 2D dilaton gravity / finite-N DSSYK.

**Leutheusser-Liu 2508.00056, eq. (4)** (verbatim from HTML extraction):
> "(M : N) = exp(C · Vol(b))"

where `(M:N)` is a **new holographic index** (not Kosaki — they explicitly disclaim equality: *"Currently, it is not clear if (4) can be related to the Kosaki index. Instead, we may view (4) as a definition of a new index using holography."*). `b` is the maximal-volume slice of the bulk subregion dual to relative commutant `N' ∩ M`. Setting: AdS subregion-subalgebra duality, type III_1 in large-N, with §V applied to dS observer algebras.

---

## (2) Composite chain attempt

Attempted three-link chain on FRW comoving diamond `D_O` with `N := A(D_O)_FRW ⋊_σ ℝ` (type II_∞, `frw_note.tex` Thm 3.5):

- **Link A (Vardian).** Identify a Lanczos-extracted spectrum of `K|_A` from boundary modular Krylov data using eq. (26).
- **Link B (HPS).** Convert Krylov spread complexity into a bulk geodesic length via eq. (13): `2|log q| C_K = ⟨L̂⟩`.
- **Link C (LL).** Relate `Vol(b)` to `log[(M:N)]` via eq. (4): `Vol = (1/C) log[(M:N)]`.

Composing (B) ∘ (C): `C_K ∝ Vol ∝ log[(M:N)]`. Then the Krylov-Diameter rate
`(1/C_k) dC_k/dt = (1/Vol) d(Vol)/dt`
should give a geometric rate. Combine with Vardian (A) to identify the area operator on the boundary side as the central element of `K|_A`.

---

## (3) Verdict: chain FAILS on three independent obstructions

**Status: chain DOES NOT CLOSE Krylov-Diameter Thm 4.**

Each obstruction is independent and decisive (any one of them breaks the chain).

### Obstruction T1 — HPS does not say "= log Jones-index".

Verified by full read of HPS pages 1-9: the paper contains **zero** occurrences of the words "Jones", "subfactor", "Kosaki", "log index", "type II_∞ factor", "Murray–von Neumann", or "FRW". HPS proves a **complexity-volume** match in 2D (sine dilaton ↔ DSSYK transfer matrix), with the volume being the geodesic length `L̂` of the Kruskal extension of the AdS_2 black hole (eq. 4). The Sonnet trio's middle link "= log Jones-index" is **misattributed** — HPS supplies "Krylov = volume", not "Krylov = log index". Only **Leutheusser-Liu** supplies "volume = log index". So the Sonnet chain is really a TWO-link chain HPS ∘ LL, not a triple, and the Vardian piece is an independent OAQEC area-operator construction that doesn't compose with the HPS/LL line.

### Obstruction T2 — Setting mismatch: each paper lives in a different algebra type.

| Paper        | Algebra                              | Setting              | Krylov-Diameter target                  |
|--------------|--------------------------------------|----------------------|----------------------------------------|
| Vardian      | type-I code subspace, OAQEC, finite-dim block decomp ⊕_α L(H_A^α)⊗I | AdS/CFT QES + islands | type II_∞ crossed product on FRW diamond |
| HPS          | DSSYK chord Hilbert space (separable, transfer-matrix Lanczos) | 2D sine dilaton gravity | type II_∞ FRW (4D conformally flat) |
| LL           | type III_1 in large-N, "new holographic index" (NOT Kosaki) | AdS subregion-subalgebra duality + dS poles | type II_∞ FRW with semifinite trace |

None of the three is on a type II_∞ crossed product of an FRW comoving-diamond algebra. The Vardian obstruction (O1 from /tmp/M1C_vardian_hollands.md: OAQEC tensor decomposition fails in type II_∞) carries over identically here. HPS adds a new obstruction: the chord Hilbert space is intrinsic to DSSYK and is not equivalent to L^2(N, tr_N) for any FRW crossed product; the holographic dictionary L = 2|log q| n is specific to the q-deformed JT/sine-dilaton story. LL is closer (their type III_1 in large-N matches the underlying III_1 algebra A(D_O)_FRW from `frw_note.tex` Thm 3.5), but their "index" is **defined** holographically via eq. (4), not derived from a subfactor calculation, and their AdS bulk subregion ≠ FRW comoving diamond.

### Obstruction T3 — LL "index" is a definition, not a theorem; the chain is circular when applied to FRW.

Leutheusser-Liu themselves disclaim that (4) is a theorem on Kosaki/Jones index: "we may view (4) as a definition of a new index using holography." For an AdS bulk subregion they have an *independent* definition of `Vol(b)` (the maximal-volume slice in AdS) and they *postulate* the index by exponentiation. To use (4) as the right-hand link of a chain that is supposed to *prove* the Krylov-Diameter rate `(1/C_k) dC_k/dt = 1/R_proper` on FRW, one would need either (a) an independent, subfactor-theoretic computation of an index for the inclusion `A(D_O')_FRW ⊂ A(D_O)_FRW` of nested FRW comoving diamonds, or (b) an independent geometric meaning of `Vol(b)` for the FRW diamond. Neither is established in LL or in `frw_note.tex`. Plugging (4) in as a *definition* makes the resulting "Krylov = volume" identity tautological, not a theorem.

### Obstruction T4 (residual, inherited from M1-C audit) — UOGH on type II_∞ KMS still open.

Even if T1–T3 were waved, the Krylov-Diameter Thm 4 proof sketch (krylov_diameter.tex line 347–360) explicitly uses the modular-Lyapunov slope `λ_L^mod = 2π` from CMPT eq.(4.16)/(5.4), which is the **type-III_1 universal operator-growth hypothesis on chiral CFT**. The Block A definition (Def. 2, lines 251–264) lifts this to type II_∞ via the conditional expectation E:N → A(D_O)_FRW (Remark 2, line 281–301), but **the slope 2π is currently inherited, not proved intrinsically on type II_∞**. Open Question 1 in `krylov_diameter.tex` (lines 485–497) explicitly flags this. Neither HPS, LL, nor Vardian addresses UOGH on type II_∞ KMS states, so this gap survives intact.

---

## (4) Theorem statement upgrade — N/A

Chain does not close, no upgrade is warranted. Theorem 4 of `paper/krylov_diameter/krylov_diameter.tex` should remain in its current "conditional on UOGH transfer" form. The Block A definition, the Casini–Huerta–Myers chain rule, and the era-by-era sympy-verified table are unaffected — those parts of the note are independent of the trio.

---

## (5) Obstruction list (NOT repeating Vardian-Hollands O1–O4 from /tmp/M1C_vardian_hollands.md)

New obstructions specific to the trio attempt:

- **T1.** HPS does not supply "= log Jones-index"; the Sonnet middle link is misattributed. (Verified by full PDF read, zero mentions of Jones/subfactor/Kosaki/index in HPS.)
- **T2.** Each of the three papers lives in a different algebra type (type-I code, DSSYK chord space, AdS large-N type III_1), and none is the type II_∞ crossed product on an FRW comoving diamond.
- **T3.** LL's eq. (4) is *defined* holographically as a new index (their explicit disclaimer); using (4) as a theorem-grade link to FRW makes the "Krylov = volume" identity circular when the FRW diamond's `Vol(b)` is not independently characterised.
- **T5 (additional, on HPS-LL composition).** HPS uses the volume of a Kruskal-extended AdS_2 BH slice (eq. 4); LL uses the maximal-volume slice of an AdS_d bulk subregion. Neither volume is `R_proper(η_c)` of an FRW comoving diamond. The identification of "the volume in HPS" with "the volume in LL" requires a dimensional reduction / uplift bridge that is not in either paper.
- **T6 (residual O1 from prior run).** Vardian's OAQEC tensor decomposition fails in type II_∞ (no density matrix for the diamond algebra). This is identical to obstruction O1 of /tmp/M1C_vardian_hollands.md and survives unchanged in the trio attempt.

Obstructions O2 (Wiesbrock half-sided modular inclusion ≠ FRW Hislop–Longo) and O3 (Lyapunov ≠ entropy-derivative) from the Vardian-Hollands run **do not apply** to the trio because Hollands has been replaced by HPS+LL — but obstruction O1 (Vardian OAQEC type-I limitation) still applies and is renumbered T6.

---

## (6) Recommendation

**Do not write up the trio chain as a Krylov-Diameter supplement.**

Concrete actions:
1. **Add** a one-paragraph "candidate compositions that fail" appendix to `paper/krylov_diameter/krylov_diameter.tex` (or to the v8-bis "Open problems" section) listing T1–T6 with citations to Vardian, HPS, LL — same defensive-citation purpose as point 4 of the Vardian-Hollands recommendation. Cite explicitly: "the Sonnet-frontier-search candidate trio Vardian–HPS–LL does not compose into a proof of Theorem 4 because (T1) HPS does not contain a log-index identity, (T2) the three papers live in incompatible algebra types, (T3) LL's index is a holographic definition not a theorem in the FRW setting."
2. **Cite LL favourably** as a programmatic reference for "volume-as-index in algebraic holography" — the dS application of LL §V is the closest published analogue to what one would want for FRW, and citing it strengthens the open-question framing.
3. **Cite HPS** as the strongest published "Krylov-spread = bulk volume" statement to date — directly relevant to the Krylov-Diameter philosophy, even though it doesn't compose with LL/Vardian into a closed chain.
4. **Open problem to add:** "Is there a subfactor inclusion `A(D_O')_FRW ⊂ A(D_O)_FRW` between nested FRW comoving diamonds whose Kosaki/Jones index is `exp(C · R_proper(η_c))`? An affirmative answer, combined with an extension of HPS to type II_∞, would close the Krylov-Diameter proof."
5. **Do not push** any of this. Local commit only when (1) is drafted; tag it `krylov_diameter_v2_appendix_trio_obstructions` for traceability.

Status of `paper/krylov_diameter/krylov_diameter.tex`: **unchanged**, Theorem 4 remains conditional on UOGH transfer (Remark 2, Open Question 1). The trio attempt **reinforces** rather than weakens that conditional stance.

---

## arXiv API verification (spot-check, /tmp/{vardian,hps,ll}_api.xml)

- **2602.02675v1 (Vardian)**: opensearch:totalResults=1, title "Modular Krylov Complexity as a Boundary Probe of Area Operator and Entanglement Islands", published 2026-02-02T19:00:24Z, primary hep-th, comment "5 pages + supplemental material + appendix". 411,866-byte PDF.
- **2412.17785v2 (HPS)**: opensearch:totalResults=1, title "Krylov spread complexity as holographic complexity beyond JT gravity", published 2024-12-23T18:43:35Z, journal_ref "Phys. Rev. Lett. 135 (2025), 151602", authors Michal P. Heller / Jacopo Papalini / Tim Schuhmann (Ghent), comment "5.5 pages + supplemental, 2 figures; v2: minor improvements... matches published version". 501,832-byte PDF.
- **2508.00056v1 (Leutheusser-Liu)**: opensearch:totalResults=1, title "Volume as an index of a subalgebra", published 2025-07-31T18:00:01Z, primary hep-th (also gr-qc, math-ph), comment "45 pages, 8 figures", authors Samuel Leutheusser / Hong Liu. 1,083,703-byte PDF.

All three confirmed to exist on arXiv as claimed.
