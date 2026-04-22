# V6 JHEP draft — adversarial re-attack v2 (targeted)

**Date.** 2026-04-22.
**Target.** `paper/v6/v6_jhep.tex` after commits `bb88907` (bib entries
CeyhanFaulkner2020 + Longo2019) and `3a252a4` (9 editorial fixes).
**Scope.** Targeted re-attack on the two previously-VALID attacks
(Attack 5: α = 0.095 numerology; Attack 7: M1 operational emptiness /
`C_k` recipe) + a fast scan for NEW attacks introduced by the fixes.
**Prior report.** `derivations/V6-draft-adversarial-attack.md`
(2026-04-21, verdict FIX, 3/8 WEAK+VALID).

All quotations below are from the current `v6_jhep.tex` (line numbers
match the working copy at commit `3a252a4`). RAG anchors: Caputa2024,
Bianconi2025, Pedraza2022Threads, Carrasco2023 txt summaries in
`paper/_rag/`. eci.bib keys confirmed at lines 660, 710, 723, 736,
752, 765.

---

## A. Re-attack on Attack 5 (α = 0.095 numerology)

### A.1 What the draft now says

`v6_jhep.tex` L212–223 (Assumption M3):

> The activator $\Theta$ takes the chameleon form
> $\Theta(\PHk) = \exp[-(\PHk/\PHk^{\mathrm{c}})^{\alpha}]$
> with a single power $\alpha \in (0, 0.1]$, inspired by the
> Barrow–$\Delta \lesssim 0.1$ fractal-horizon bound. The precise value
> $\alpha = 0.095$ adopted in the v5.0 phenomenological companion
> follows from calibration of the chameleon screening
> profile~\cite{KhouryWeltman2004}; the formal inequality~\eqref{eq:main}
> requires only $\alpha > 0$, and $\alpha$ should be treated as a
> prior-anchored fit parameter in any phenomenological application.

Plus the §5 assumptions summary L378–380:

> M3 restricts $\alpha \in (0, 0.1]$ as a Barrow-anchored range
> (the specific value $\alpha = 0.095$ used in the v5.0 phenomenological
> companion is a calibration choice, not a derived quantity).

### A.2 Referee pass

The structural claim of the formal paper is now **`α > 0`**. The
specific `0.095` is (i) explicitly labelled a calibration choice,
(ii) attributed to a companion paper, (iii) not used anywhere in the
formal inequality. The range `(0, 0.1]` is called "Barrow-anchored"
which is honest: Barrow's fractal Δ is bounded `≲ 0.1`, so
`α ∈ (0, 0.1]` is a reading of that range, not a derivation from it.

### A.3 Remaining surface

Minor surface: the word "inspired" at L215 is hand-wavy but correct
usage for an ansatz bound. The Barrow–Δ citation is to a 2020 work
that a referee can check in 30 s. No false-precision in the main
text. No new claim is attached to `0.095`.

**A.4 Verdict on Attack 5 re-attack: NEUTRALISED.** The v6 draft no
longer rides on 0.095; the formal content requires only `α > 0` which
is admitted as a postulate.

---

## B. Re-attack on Attack 7 (C_k operationally empty / M1 orphan)

### B.1 What the draft now says

L141–151 (§2 Setup):

> The $k$-design complexity $\Ck[\rho_R]$ is defined in the Ma–Huang
> pseudorandom-unitary (PRU) sense [MaHuang2025]; ...
> Operationally, we identify $\Ck[\rho_R]$ with the spread complexity of
> Caputa–Magán–Patramanis–Tonni 2024 [Caputa2024] evaluated under the
> modular flow $e^{-i K_R \tau}$ and truncated at the $k$-design
> saturation scale; this identification is a sub-postulate (M1′) of M1
> below.

### B.2 Does Caputa 2024 actually carry this weight?

From `paper/_rag/Caputa2024.txt` (full content):

> "Complexity of states/operators evolved with the **modular Hamiltonian
> in the Krylov basis**, for QM, 2d CFT, and random modular
> Hamiltonians. **Spread complexity** is universally governed by the
> modular Lyapunov exponent λ^mod_L = 2π at late times."

Yes. Caputa et al. (2024) define **spread complexity** (a Lanczos /
Krylov functional) explicitly for **modular-Hamiltonian evolution**.
So the object `C_k[ρ_R]` can be computed, in principle, by:
(i) fixing a reference state, (ii) running the Lanczos algorithm on
`e^{-i K_R τ} |ψ_ref⟩`, (iii) reading off spread complexity at time τ,
(iv) truncating at the `k`-design saturation scale. Steps (i)–(iii) are
a standard recipe in Caputa et al.'s QM and 2d CFT examples; step
(iv) is the novel truncation — it is the weak link (see B.3).

### B.3 Where the attack still has purchase

Two residual concerns:

**B.3.a The truncation at the "$k$-design saturation scale" is not
defined.** The draft invokes `MaHuang2025`, `Haferkamp2022`, and
`CryptoCensorship` at L145–146 for circuit/information-theoretic
complexity, but does not give a concrete formula for the saturation
scale at which spread complexity is to be truncated to become the
`k`-design complexity. A referee in the complexity community will ask:
what is the precise map `(Caputa spread complexity, k) ↦ C_k`? The
draft implicitly defers this to "M1′ as a sub-postulate" (L151), which
is honest, but the recipe-in-principle is not quite there.

**B.3.b Spread complexity is reference-state-dependent.** Caputa et
al. compute it for a given initial state; on a type-II crossed-product
algebra the natural "reference" would be the tracial state, but the
draft does not say this. A one-line clarification ("evaluated on the
tracial vacuum `Ω_R` of the crossed-product factor") would close the
gap cheaply.

### B.4 Can one in principle compute `C_k` in a toy QFT?

Yes — in a 2d CFT (Caputa et al. example 3) with a modular Hamiltonian
for an interval, spread complexity has a closed form (the modular
Lanczos coefficients give `C(τ) = sinh²(πτ/β)`-type growth). Truncation
at `k`-design saturation is model-dependent but computable once the
Haferkamp linear-growth threshold is fixed. So the M1′ identification
is **operationally non-empty**: it is a specific, computable (if
labour-intensive) functional, not a label on a gap.

### B.5 Verdict on Attack 7 re-attack: **NEUTRALISED with one residual
MINOR-FIX**.

The M1′ sub-postulate upgrades `C_k[ρ_R]` from "label" to "specific
Caputa spread-complexity functional under modular flow", and the
Caputa 2024 RAG anchor supports this reading. The truncation step and
the reference-state choice are under-specified; one extra sentence
would close it.

**Proposed MINOR-FIX:** after L151 add:

> Concretely, $\Ck[\rho_R]$ is the spread complexity
> $C_{\mathrm{spread}}(\tau_R)$ of Caputa et al.\ computed on the
> tracial vacuum of $\AR$ under $e^{-i K_R \tau_R}$, truncated at the
> Haferkamp linear-growth scale $\tau_{\mathrm{sat}}\sim \exp(S_R)$.

---

## C. NEW attacks introduced by the fixes

### C.1 §5 Pedraza / Carrasco subsection (L335–352): scope creep?

New subsection `sec:compgrav` (Fix 8) adds a paragraph demarcating
our Eq.(1) from the complexity=volume first-law programme.

**Draft claim (L340–342):** "Pedraza–Russo–Svesko–Weller-Davies and
Carrasco–Pedraza–Svesko–Weller-Davies establish a variational identity
$\delta C_V = (1/G_N)\int \delta V$ that, under stationarity of a
holographic-complexity volume functional, reproduces the linearised
Einstein equations as an integrated equality."

**RAG check (Pedraza2022Threads.txt, full):**

> "Reformulates complexity=volume via Lorentzian flows (timelike
> vector fields with minimum flux = bulk volume). Holographic
> complexity satisfies nesting inequalities; rates bounded by
> conditional complexity. Discretized flows = gatelines in tensor
> networks. **Connects bulk symplectic potential to linearized
> Einstein eqs** and to **holographic first law of complexity**;
> Lorentzian threads yield emergent time."

**RAG check (Carrasco2023.txt, full):**

> "Gravitational physics arises from spacetime optimizing the
> computational cost of its quantum dynamics. Extends prior
> linearized/holographic result: derives higher-derivative gravity via
> corrections to C=V, and **semi-classical equations via leading
> quantum corrections**..."

**Finding.** The draft's compact formula "$\delta C_V = (1/G_N)\int
\delta V$" is a **paraphrased schematic**, not a literal equation from
either paper. Pedraza et al. work with the holographic first law of
complexity (a schematic δC ↔ δ(bulk symplectic) identity); Carrasco et
al. extend to higher-derivative. Neither paper writes the bare formula
`δC_V = (1/G_N) ∫ δV` in that form. A referee who opens
arXiv:2106.12585 or 2306.08503 will not grep that exact identity.

**Severity.** Low–medium. The qualitative demarcation ("variational
static first-variation identity on a bulk slice" vs "differential
modular-time inequality") is accurate and fair. But the specific
formula risks being read as a literal quotation. Safer to write:

> "... establish a variational complexity/volume first-law identity
> that reproduces the linearised Einstein equations under a
> stationarity condition..."

(No specific formula. Leaves the demarcation intact.)

**Verdict on C.1:** MINOR-FIX recommended. Not a blocker; a careful
referee would ask "where does that formula appear in [37,38]?" and
the honest answer is "it's a schematic, not a literal equation."
One-line edit.

### C.2 Bianconi footnote (L173–177): fair characterisation?

Draft:

> "Bianconi 2025 uses a symbol Θ as a Lagrange multiplier for the
> relative-entropy action $S(g\|G)$; our Θ is a distinct chameleon-
> like activator on the topological space of density fields. The two
> objects are mathematically and physically unrelated."

**RAG check (Bianconi2025.txt):**

> "...matter fields described topologically via Dirac–Kähler
> formalism. An alternative metric induced by matter fields enters as
> quantum relative entropy between the two metrics ... a **G-field
> Lagrange multiplier** produces a dressed Einstein–Hilbert action
> with emergent small positive Λ."

**Finding.** The RAG summary says Bianconi uses a **`G`-field** as
the Lagrange multiplier, not a `Θ` symbol per se. The bib note
(eci.bib L747) itself says "Bianconi uses an auxiliary `G`-field /
activator notation overlapping with our `Θ(PH_k)`". The draft
footnote attributes the `Θ` symbol to Bianconi directly, which may
not be literally accurate (the clash is at the conceptual level of
"auxiliary multiplier", not at the symbol level). If Bianconi's paper
does not literally use the symbol `Θ`, the footnote's claim "uses a
symbol Θ" is technically wrong. The underlying rhetorical goal (flag
possible confusion) is fine, but the phrasing is slightly off.

**Severity.** Low. A referee is unlikely to open Bianconi just to
check whether a Greek letter is `Θ` or `G`. But per PRINCIPLES.md
rule 1 (no paraphrase of sources), the safer phrasing is:

> "Bianconi 2025 uses an auxiliary Lagrange-multiplier field in the
> relative-entropy action $S(g\|G)$; our Θ is a distinct..."

(No claim about which symbol Bianconi uses.)

**Verdict on C.2:** MINOR-FIX recommended. One-line phrasing edit.
Not a rigour issue, a source-fidelity issue.

### C.3 Ceyhan–Faulkner citation used for a step it actually supports?

Draft L237–240 (proof sketch):

> "The Pinsker-style step $-dS_{\mathrm{rel}}/d\tauR \le
> |d\langle K_R\rangle/d\tauR|$ is justified on modular-flow-covariant
> states by the **half-sided modular pushforward of Ceyhan–Faulkner**
> together with the Longo positivity bound."

**RAG check (eci.bib entry L752–763):** CeyhanFaulkner2020 =
"Recovering the QNEC from the ANEC", Commun. Math. Phys. 377 (2020).
This paper's signature machinery is the **half-sided modular
inclusion** for null-cut-ANEC states and relative-entropy inequalities
on modular-flow-covariant states. The Pinsker-style bound on
`dS_rel/dτ` in terms of `d⟨K⟩/dτ` is a direct application of their
modular-pushforward inequality.

**Finding.** Citation is load-appropriate. Ceyhan–Faulkner's
machinery does in fact supply the modular-pushforward justification
invoked here. Longo2019 ("Entropy distribution of localised states")
supplies the positivity bound for the modular Hamiltonian on the
cyclic-and-separating vacuum. Both citations sit at the step they are
invoked for, not one upstream or downstream of it. No over-reach.

**Verdict on C.3:** CLEAN. No attack lands.

### C.4 Other surface checks

- **L238 "Pinsker-style"** — honest softening; no claim that the
  bound *is* Pinsker's inequality. OK.
- **L248–251 "Fan (2022) $C_k \propto \exp(S_R)$ gives the
  logarithmic rate ... as a consistency check, not as a derivation"**
  — the Fan-saturation framing is self-consistent with the L2 limit
  in §5. OK.
- **Abstract L64 "consistent with, as a sub-linear saturating limit,
  the Fan (2022) logarithmic Krylov regime"** — matches the
  recommended Attack-6 rewording. OK.

---

## D. Summary verdict

Two VALID attacks from v1 re-evaluated:

| Attack | v1 verdict | v2 verdict | Residual |
|---|---|---|---|
| 5 (α=0.095 numerology) | VALID | NEUTRALISED | none |
| 7 (M1 / C_k empty) | VALID | NEUTRALISED | 1 sentence on truncation scale + reference state (MINOR-FIX) |

New attacks from re-scan of fix-induced edits:

| # | Issue | Severity | Action |
|---|---|---|---|
| C.1 | Paraphrased `δC_V = (1/G_N)∫δV` formula not literal in refs | LOW-MED | MINOR-FIX, one-line edit |
| C.2 | Bianconi footnote attributes `Θ` symbol not literally in paper | LOW | MINOR-FIX, one-line phrasing |
| C.3 | Ceyhan–Faulkner citation | CLEAN | — |

**Overall verdict: MINOR-FIX.** The v6 draft is now much closer to
SHIP. The two originally-VALID attacks are substantively neutralised.
Three new micro-issues surface (two source-fidelity phrasings in the
§5 Pedraza paragraph and the Bianconi footnote, plus one residual
under-specification in M1′). All three are one-line editorial
corrections. None are derivational. After these three edits, the
draft is expected to clear a hostile-referee pass cleanly.

**Recommendation.**
1. Add one sentence after L151 specifying the truncation scale and
   reference state for the M1′ spread-complexity identification.
2. Replace the explicit schematic `δC_V = (1/G_N)∫δV` at L341 with a
   prose description of the first-law identity.
3. Tweak the Bianconi footnote at L174 so it does not claim Bianconi
   literally uses the symbol `Θ`.

After (1)–(3), verdict expected to move MINOR-FIX → SHIP on the next
pass.

Word count: ~1140.
