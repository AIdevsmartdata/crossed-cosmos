# Piste B — Opus Deep Proof-Strategy Analysis for v7 (v6 + Liu 2026)

**Date.** 2026-04-22.
**Scope.** Complement to Sonnet Piste-B planning agent. Deep theoretical
strategy; not a broader menu.
**Rules respected.** V6-1 (no equality claim), V6-4 (no cosmology in v6/v7
formal line), rule 1 (honesty), rule 12 (no claim larger than derivation).
**Source discipline.** All Liu 2026 claims below are verified by direct
extraction of arXiv:2601.07915 PDF (text in `/tmp/liu2026.txt`,
equations 8.13–8.40). No training-data paraphrase.

---

## 1. What Liu 2026 actually proves (verbatim anchor)

The paper is Chandrasekaran–Flanagan (contrary to our working shorthand
"Liu 2026" inherited from an earlier agent log — **correct this in the
bib**: first author is **Chandrasekaran**, so bib-key should be
`Chandrasekaran2026Subregion`, not `Liu2026Subregion`). The QFC proof
lives in **§8.2** (not §§3–4 as the mission prompt guessed; §§3–4 are on
canonical half-sided supertranslations and half-sided diffeomorphisms —
the kinematic prelude). The proof structure is:

**(a) Statement proved (Eq. 8.13, 8.15, 8.40):**
\[
  \Theta(u) := \partial_u \bar S_{\mathrm{gen}}(u;\hat\psi),\qquad
  \partial_u \Theta(u) \le 0 \;\Leftrightarrow\; \partial_u^2 \bar S_{\mathrm{gen}}(u;\hat\psi) \le 0.
\]
*Concavity of generalised entropy in the affine horizon parameter $u$* —
i.e. QFC as a **second-derivative** statement.

**(b) HSMI structure (Eq. 8.16–8.18):** one-parameter unitary group
$U(a)=e^{ia\hat P}$ implementing null translation, with
$U(a)\widehat{\mathcal M}_{u_0}U(-a)\subset \widehat{\mathcal M}_{u_0}$ for
$a\ge 0$ (Borchers–Wiesbrock HSMI).

**(c) "Pinsker-style step".** There is **no Pinsker inequality** in the
Liu proof. What v6 calls its "Pinsker step" is the Ceyhan–Faulkner 2020
**variational formula** for $-\partial_u S_{\mathrm{rel}}$ as an
*infimum over commutant unitaries of a positive operator expectation*
(Eq. 8.32 of Liu, = Eq. 1.1 of CF 2020). Pinsker's classical inequality
(on total variation vs KL divergence) does not appear. **v6 §3 prose
should not call the CF step a "Pinsker step"** — it is a
*variational/infimum formula* using HSMI + Connes-cocycle flow. This
is an internal-terminology fix for v6.0.4, not a v7 issue, but it
eliminates ambiguity when we bridge to Liu.

**(d) Compact-support.** Liu imposes **no compact-support assumption on
horizon subalgebras** in §8.2. The only regularity used is (i) HSMI
for $\{\widehat{\mathcal M}_u\}$, (ii) almost-everywhere differentiability
of $S_{\mathrm{rel}}(u)$, (iii) the classical Killing horizon background
(stated explicitly footnote 46). The compact-support assumption in v6
lives elsewhere: it is the GKS 2012 hypothesis (ii) on the PH_k sheaf
quantisation (our §3, KS-microlocal covariance lemma, v6_gap_analysis
§A4). **These are different compact-support conditions in different
functors.** Confusing them is a Piste B failure mode (see §4b below).

**(e) Complexity.** **Liu contains zero occurrences of "complexity"** —
no Krylov, no spread, no Brown–Susskind, no k-design. The only
"rate" on the r.h.s. of Eq. (8.32) is the **averaged null translation
generator** $\hat P_u$. This is the single most important theoretical
datum for Piste B: **Liu's r.h.s. is a geometric/kinematical operator;
v6's r.h.s. is a state-functional $\kappa_R \mathcal{C}_k \Theta$.**

---

## 2. Formal v7 candidate theorem (MVT1 form)

**Hypotheses (carried over from v6.0.4).** Let $\mathcal A_R$ be the
type-II crossed-product von Neumann algebra of CLPW/DEHK on the dS
static patch (or a Killing horizon, so the Liu setting specialises).

- **M1' (complexity operator growth).** There exists a state-functional
  $\mathcal{C}_k[\rho_R]$ (2-Rényi surrogate of k-design PRU complexity,
  Ma–Huang 2025) and a positive constant $\kappa_R$ such that for every
  $\hat\psi$ in a dense subset of the type-II state space, the
  half-sided translation generator restricted to $\hat\psi$ satisfies
  \[
      \langle \hat\psi|\hat P_u|\hat\psi\rangle
      \;\le\;
      \tfrac{1}{2\pi}\kappa_R \,\mathcal{C}_k[\rho_{\hat\psi,u}]\,\Theta(\mathrm{PH}_k[\delta n(u,\hat\psi)]).
  \tag{M1'}
  \]
  (Postulate, not theorem; carried over from v6 M1.)
- **M2' (semi-classical dequantisation).** Same as v6 M2 (N-copy CLT of
  $\delta n$).
- **M3' (Barrow-anchored $\alpha>0$).** Same as v6 M3.

**Theorem candidate (conditional).** Under M1'-M2'-M3', the Liu 2026
variational formula (Eq. 8.32) combined with the HSMI-nesting
argument (Eqs. 8.33–8.39) yields
\[
  -\tfrac{1}{2\pi}\,\partial_u S_{\mathrm{rel}}(u)
  \;=\;
  \inf_{V\in\mathcal U(\widehat{\mathcal M}_u^{\,\prime})} \langle \hat\psi | V^\dagger \hat P_u V|\hat\psi\rangle
  \;\le\;
  \kappa_R\,\mathcal{C}_k[\rho_R(u)]\,\Theta(\mathrm{PH}_k[\delta n(u)]),
  \tag{T1}
\]
and the r.h.s. is non-increasing in $u$ (as $u$ grows the *commutant*
grows → the infimum can only decrease → the bound propagates). Hence
by $\bar S_{\mathrm{gen}}\approx -S_{\mathrm{rel}} + \text{const}$:
\[
  \frac{dS_{\mathrm{gen}}}{d\tau_R}
  \;\le\;
  \kappa_R\,\mathcal{C}_k\,\Theta
  \qquad\text{AND}\qquad
  \frac{d^2 S_{\mathrm{gen}}}{du^2}\le 0.
  \tag{T2}
\]
The first is v6.0.4 Eq. (1) (**first-derivative upper bound**, modular
time, inequality); the second is Liu Eq. (8.13) (**second-derivative
sign**, affine time, concavity).

**What the theorem actually adds over v6.0.4 + Liu separately.** A
*single object on the right-hand side* — namely the infimum
$\inf_V\langle V^\dagger\hat P_u V\rangle$ — that admits **two bounds
simultaneously**: (i) Liu's intrinsic geometrical positivity
→ concavity; (ii) M1' complexity ceiling → rate-bound. If M1' ever
becomes a theorem (v6_gap_analysis §A1), (T1) becomes an unconditional
two-sided control of $\partial_u\bar S_{\mathrm{gen}}$.

**The orthogonality question (mission item 2).** Liu's bound is a
*sign bound on the second derivative* (concavity, QFC). v6's bound is
an *upper bound on the first derivative*. They are **not redundant**
and **not contradictory**: they constrain different derivatives of the
same function. In particular, Liu's QFC says $\Theta(u)$ is monotone
non-increasing; v6 says $\Theta(u)\le \kappa_R\mathcal{C}_k\Theta_{\mathrm{PH}}$
(abuse of notation — Liu's $\Theta$ = quantum expansion; v6's $\Theta$
= PH_k activator; these are **different $\Theta$'s** — terminological
crash to fix in v7 prose). The combined statement is: the quantum
expansion is (i) non-increasing, (ii) bounded above by
$\kappa_R\mathcal{C}_k$ times a topological activator. That is
non-trivial and **non-vacuous only if M1' is believed**.

**Identification of affine $u$ with modular $\tau_R$.** This is the
first technical lemma. See §3, Lemma L1.

---

## 3. Technical lemmas to prove, ranked by necessity

### L1 (load-bearing). Affine-modular identification.

**Statement.** On a Killing horizon of the dS static patch, the affine
parameter $u$ along the horizon generator and the modular-flow
parameter $\tau_R$ of $\mathcal{A}_R$ (CLPW/DEHK crossed product) are
related by $\tau_R = 2\pi\, u/\kappa_{\mathrm{surf}}$ where
$\kappa_{\mathrm{surf}}$ is the surface gravity, **for states in the
semi-classical domain of M2' on which the Bisognano–Wichmann property
holds**.

**Why needed.** v6 Eq. (1) is $\partial_{\tau_R}$; Liu Eq. (8.40) is
$\partial_u$. Without L1 the two inequalities live on different clocks
and combining them is meaningless. This is the *exact same* compact-
support issue we flagged in v6_gap_analysis §A4 (GKS hypothesis),
recast.

**Status.** Known as folklore for Rindler/Killing in CLPW; the CF 2020
proof of QNEC uses exactly this identification. For type-II crossed
product on dS static patch: proven in CLPW 2023 (their §3). **This is
not a new lemma — it is a citation, provided we cite correctly.** If
v7 wants modular-time and Liu's affine-time statements simultaneously,
we cite CLPW §3 + Liu §8.2 and note the identification. The gap v6
currently has is that it silently assumes this identification without
citing; v7 must make it explicit.

**Failure mode.** The identification **fails outside the Killing-horizon
setting**. In FLRW causal diamonds (v6_gap_analysis §A4), the
comoving observer's modular flow is not generated by a Killing vector
on the cosmological horizon, and Kudler-Flam–Leutheusser–
Satishchandran 2024 construct the type-II algebra *without* a
Bisognano–Wichmann geometric identification. For v7, **we explicitly
scope to the dS static patch / Killing-horizon setting**, same
scope as v6. No FLRW.

### L2. Simultaneous well-definedness of Liu's $\hat P_u$ and v6's $\kappa_R\mathcal{C}_k\Theta$.

**Statement.** In the type-II crossed product $\widehat{\mathcal M}_u$
on the Killing-horizon background, the infimum
$\inf_{V\in\mathcal U(\widehat{\mathcal M}_u^{\,\prime})}\langle V^\dagger\hat P_u V\rangle$
(Liu Eq. 8.32, a densely-defined positive number) and the functional
$\kappa_R\mathcal{C}_k[\rho_{\hat\psi,u}]\Theta(\mathrm{PH}_k[\delta n(u)])$
(v6 r.h.s., densely-defined on the same state space given M2') admit
a **common dense domain** of semi-classical uplifted states $\hat\psi$.

**Why needed.** M1' is the bridge. If the two sides are defined on
disjoint dense domains, M1' is vacuous. For v6 alone, $\mathcal{C}_k$
is defined on the Lanczos-truncated sector of the type-II trace
(Caputa–Magan 2024); Liu's $\hat P_u$ acts on the extended Hilbert
space with edge-mode sector. The edge-mode sector is **new** relative
to v6 and must be shown compatible with the dequantisation M2'.

**Status.** **Genuinely open.** This is where v7 does work that
neither v6 nor Liu does. The edge-mode extended Hilbert space of Liu
§5–6 (gravitational corner modes) is a different Hilbert space from
the DEHK QRF Hilbert space used in v6. One must prove (or postulate
with an honest label) that the CLPW/DEHK crossed product embeds into
the Liu extended Hilbert space on the Killing-horizon restriction,
and that M2' dequantisation descends. This is a **non-trivial
embedding of two distinct constructions of "the" gravitational
algebra of a dS Killing horizon.**

**Binary success/failure criterion.** Either there is an explicit
unitary (or Morita) equivalence between the Liu $\widehat{\mathcal M}_u$
and the DEHK $\mathcal A_R$ restricted to a Killing horizon, on a
common vacuum uplift $|\hat\Omega\rangle$, or there is not. If yes,
v7 succeeds as MVT1. If no, v7 reduces to MVT2 (consistency note
without unification).

### L3. Complexity of a horizon cut.

**Statement.** There exists a functional
$\mathcal{C}_k^{\mathrm{cut}}:\{|\hat\psi\rangle\}\to [0,\mathcal{C}_k^{\max}]$
on the type-II horizon algebra $\widehat{\mathcal M}_u$ that restricts
to Ma–Huang k-design complexity in the finite-dim truncation and
satisfies M1' with the Liu $\hat P_u$.

**Why needed.** M1 in v6 postulates $\mathcal{C}_k$ as a state
functional on $\mathcal A_R$; v7's M1' needs the *same object* on
$\widehat{\mathcal M}_u$ with $\hat P_u$ as the rate-operator source.

**Status.** **Open. This is the technical heart of v7.** Candidate
construction: use the Caputa–Magan 2024 spread-complexity definition
(modular-flow Lanczos at the Haferkamp scale) with modular Hamiltonian
$K_u = -\log\Delta_{\hat\Omega;u}$, then use Liu Eq. 8.32 to relate
$\hat P_u$ to the modular-flow infimum. The key technical step is to
show that Liu's $\hat P_u$ (the HSMI generator, positive semi-definite,
= $G$ of Borchers–Wiesbrock) controls (from above or below) the
Krylov dispersion of $K_u$ on semi-classical uplifts. Not obviously
true, not obviously false.

**Binary criterion.** Either a positive-constant Cauchy–Schwarz
bound $\langle\hat\psi|\hat P_u|\hat\psi\rangle \le \kappa_R
\mathcal{C}_k^{\mathrm{cut}}\Theta$ holds on semi-classical uplifts,
or an explicit state violates it. The N ∈ {12, 16, 20} finite-copy
test of v6 §3 can be adapted to probe this.

---

## 4. Honest failure modes

**(a) Trivial co-citation.** Risk **LOW**. The structural parallel
(Liu variational formula Eq. 8.32 ↔ v6 CF-step in §3) is real and
non-trivial: both invoke the CF 2020 infimum theorem. A co-citation
paper would at minimum clarify the relation to v6 readers. But a
paper whose *only* content is "we observe that Liu 2026 Eq. 8.32 is
the infimum form of our §3 CF step" is **MVT3 (position paper)**, not
a theorem. Guard against by requiring at least L1+L2 to be explicitly
written even in MVT3.

**(b) Orthogonal-settings collapse.** Risk **MEDIUM–HIGH**. Liu's
parameter $u$ is affine along the Killing generator; v6's $\tau_R$ is
modular. They coincide only on Killing horizons with
Bisognano–Wichmann (L1). Liu's $\hat P_u$ acts on the Liu extended
Hilbert space with edge modes; v6's $\mathcal{C}_k$ acts on the DEHK
crossed product. Identifying these two is L2, which is **genuinely
open**. If L2 is false or unprovable-in-3-months, v7 collapses to a
consistency-check note (MVT2).

*Clean diagnostic:* attempt L2 in month 1. If no explicit embedding
of the two algebraic constructions on a common vacuum uplift is
found, downgrade to MVT2.

**(c) Negative result (v7 → F-20 Jacobson-style).** Risk **LOW–
MEDIUM**. F-14 (Jacobson–EGJ) failed because $\mathcal{C}_k$ is a
state functional and $d_iS$ is a geometric shear. v7 is **structurally
different**: both sides here are state-functional objects on the
type-II horizon algebra. The categorical type-error of F-14 does not
reproduce. However, a distinct failure is possible: the Liu $\hat P_u$
is a *positive unbounded operator*, not obviously a complexity
surrogate, and M1' may have no positive constant $\kappa_R$ making it
hold on all semi-classical uplifts.

*Clean diagnostic:* run a sympy/qutip adaptation of the v6 N=12,16,20
CLT test with Liu's $\hat P_u$ replaced by a discrete HSMI generator
(SL(2,ℝ) on XXZ chain toy). If the ratio
$\langle\hat P_u\rangle / (\mathcal{C}_k\Theta)$ does **not** admit
an $N$-independent positive upper bound, the bridge fails — document
as **F-20: v6–Liu2026 complexity-expansion bridge, M1' counterexample**.

**The pattern-avoidance lesson from F-6, F-10, F-13, F-14, F-17.**
All five failed because of categorical/framework mismatch between
two objects identified by letter ("k" in F-6, "C" in F-10, "$\xi$" in
F-13, "$S$" in F-14, "zeta residue = vacuum energy" in F-17). The
specific safeguard for v7: **before any identification, cross-check
that both objects live in the same Hilbert-space sector with the same
normalisation convention**. L2 is exactly this cross-check. Do not
skip it.

---

## 5. Minimum viable theorem options

**MVT1 — Full conditional unification theorem.** Prove L1 (cite) + L2
(new) + L3 (new), state T1–T2 as conditional theorem under M1'-M2'-M3'.
~12 pages, JHEP / Commun. Math. Phys. target, 6–9 months solo @ 12
h/week. **High impact, high risk** (L2 open).

**MVT2 — Consistency note.** Prove L1 (cite) only; observe that Liu
Eq. 8.32 provides an *independent* CF-variational anchor for v6's §3
Pinsker-step; no M1' upgrade attempted. Note that v6's
$\partial_{\tau_R}$-bound and Liu's $\partial_u^2$-bound are **mutually
compatible** in the sense that (T1)-without-M1' is a tautological
infimum identity. ~4–5 pages, proceedings / JHEP Letter or
Foundations of Physics. 2–3 months solo @ 12 h/week. **Medium impact,
very low risk.**

**MVT3 — Position paper.** Map the shared structure (CF 2020 infimum,
type-II crossed product, HSMI) across v6, Liu 2026, Faulkner–Speranza
2024, Kirklin 2025, CPSD 2023. No new theorem; clarify who proves
what, on which algebra, on which parameter. Include an explicit
"dictionary table" of observables/parameters across the five works.
~8 pages, Living Reviews in Relativity / Classical and Quantum
Gravity "Topical Review". 3–4 months solo. **Medium-low impact, zero
risk (provided the dictionary is numerically verified).**

---

## 6. Strategic recommendation

**Ranking by impact × feasibility / risk:**

| MVT | Impact | Feasibility (12h/wk, solo) | Risk | Score |
|---|---|---|---|---|
| MVT1 | 9/10 | 3/10 (L2 open) | 7/10 | **3.9** |
| MVT2 | 5/10 | 8/10 | 2/10 | **20.0** |
| MVT3 | 4/10 | 9/10 | 1/10 | **36.0** |

**MVT2 is the right first step.** Rationale:

1. **L1 is a citation, not a theorem.** The modular–affine identification
   on Killing horizons is already in CLPW 2023 §3. MVT2 lifts this
   from v6's silent assumption to an explicit cited lemma.
2. **Liu Eq. 8.32 ≅ v6 §3 CF-step is a real insight**, not a
   coincidence. MVT2 formalises it with two lines of algebra.
3. **MVT2 seeds MVT1.** Once MVT2 exists, L2 becomes a concrete
   follow-up targeted at a specific technical question (embed Liu
   edge-mode construction into DEHK QRF), not an amorphous research
   program. Solo work is feasible because the target is sharp.
4. **No PRINCIPLES risk.** V6-1 preserved (inequality only);
   V6-4 preserved (no cosmology); rule 12 preserved (conditional
   claim).
5. **Endorsement path.** A 4–5-page consistency note on arXiv in
   hep-th with v6 as its main technical dependency is
   endorsable by a CF-2020-literate theorist (Faulkner, Ceyhan,
   Chandrasekaran, Leutheusser). MVT1 would need an endorser *and*
   a collaborator on L2 — not realistic pre-endorsement.

**Do not pursue MVT1 before MVT2 exists.** The probability of a
3-month solo MVT1 attempt producing a clean theorem, given L2 is
open and no collaborator is secured, is low (estimate ≲ 15%).
The probability of MVT2 producing a publishable note given the
structural parallel is already documented above is high (≳ 70%).

**Do not pursue Piste B at all** if MVT3 would crowd out v6 arXiv
submission. v6 JHEP submission is the higher-priority path (v6 is
drafted, audited, endorsement-ready); Piste B is a successor, not a
substitute.

---

## 7. Cross-check against FAILED.md

The 17 failed avenues cluster into seven meta-patterns (FAILED.md
"Meta-patterns"). For v7-MVT2, the at-risk patterns are:

- **Pattern 5 (terminological / category conflation).** v7 risks
  conflating (a) Liu's quantum expansion $\Theta_{\mathrm{Liu}}(u)=
  \partial_u\bar S_{\mathrm{gen}}$ with (b) v6's topological activator
  $\Theta_{\mathrm{v6}}(\mathrm{PH}_k[\delta n])$. Different
  $\Theta$'s, different spaces. **Guard:** rename in v7 prose — use
  $\Theta_Q(u)$ for Liu's quantum expansion and $\mathcal{T}_k$ for
  v6's PH-activator. Commit this rename explicitly in the v7 tex.
- **Pattern 4 (arithmetic errors in load-bearing numbers).** MVT2 is
  pure algebra, no load-bearing numbers. Low risk.
- **Pattern 3 (citation fabrication).** High risk by precedent
  (F-3 Lange fabrication). **Guard:** for every new Liu citation,
  record the equation number verified against `/tmp/liu2026.txt`
  line number; MVT2 manuscript draft ships with a citation-check
  appendix keyed to the PDF line ranges. The first-author
  correction (Chandrasekaran, not Liu) is already an example of this
  guard paying off.
- **Pattern 1 (ANSATZ→THEOREM promotion).** MVT2 avoids by being
  explicitly conditional (M1'-M2'-M3' carried over as postulates
  unchanged from v6).

**What would make v7 fall into the F-14 pattern.** F-14 failed because
the two objects ($\mathcal{C}_k$ vs $d_iS$) lived in different
categories (state functional vs horizon-geometric extrinsic). For v7,
the analogous failure would be if Liu's $\hat P_u$ (a positive
unbounded operator on the Liu extended Hilbert space) turned out to
have no densely-defined restriction to the DEHK crossed-product sector
in which $\mathcal{C}_k$ is defined — i.e. L2 is **false**. The
specific diagnostic is the commutant-nesting Eq. (8.18) restricted to
the DEHK-embedded subalgebra: if the DEHK subalgebra is not stable
under $U(a)$ for $a>0$, the two constructions are incompatible and
v7 falls into F-14 pattern. **Run this check explicitly in MVT2 §4
before extending to MVT1.**

---

## 8. 2-year trajectory (if v7-MVT2 succeeds)

**v7 (MVT2, arXiv Q3 2026).** Consistency note: Liu Eq. 8.32 ≅ v6 §3
CF-step; L1 cited; dictionary across v6 / Liu / FS24 / Kirklin25 / CPSD23.

**v8 (MVT1 or fall-through, arXiv Q1–Q2 2027).** Conditional
unification theorem if L2 closes. Requires: either a collaborator
from the CF-2020 / DEHK sphere, or a sabbatical-level effort.
*Fall-through plan:* if L2 remains open, v8 is the Barrow-Δ
integration (v6_gap_analysis §A3) + CLT theorem for M2' on
bounded-observable N-copy toy (v6_gap_analysis §A2). Pure v6
consolidation, no Liu bridge.

**v9 (FLRW extension attempt, 2027–2028).** Relax the dS-static-patch
scope of L1 to FLRW causal diamonds, using Kudler-Flam–Leutheusser–
Satishchandran 2024 as anchor. **This is multi-paper programme**;
v9 is only the first step (algebraic scope note; no QFC-in-FLRW
claim, which is itself an open problem in the field). Explicitly
acknowledges the compact-support GKS failure (v6_gap_analysis §A4).

**v10 (experimental falsifier, 2028+).** The f_NL-via-PH_k direction
(FAILED F-2 with D18b sensitivity degenerate at 0.998 bias
correlation) needs a new falsifier. Two candidate seeds: (a)
CMB-S4/LiteBIRD joint constraint on (r, n_s, PH_k)-correlated
signature (weakening Prediction 7 — currently flagged v5 gap §D.13);
(b) dS-static-patch QFC *gravitational-wave memory* signature at
LISA — speculative but well-posed. **Decision deferred to 2028
literature landscape.**

**Pre-requisite for all of v8–v10.** arXiv endorsement secured
(currently absent — this is the single most binding non-theoretical
constraint on Piste B). MVT2 is compact enough to *serve as* the
endorsement-securing preprint.

---

## 9. Honest judgment

Piste B is **feasible as MVT2**, feasible-but-improbable as MVT1 in
12-month solo mode, and **too speculative as any cosmological
extension within 24 months**. The single most important action is to
(a) verify the first-author correction to Chandrasekaran (not Liu)
in bib-key, (b) write the 4–5-page MVT2 note, (c) use it for arXiv
endorsement.

The mission asked for a sketch of the MVT-ranked theorem statement
in mathematical notation. See §2 (T1–T2) for MVT1; the MVT2 statement
is the tautological one-liner:

\[
  \boxed{\;
  \text{On a dS Killing horizon, }
  -\tfrac{1}{2\pi}\partial_{\tau_R} S_{\mathrm{rel}}
  \;=\;
  \inf_{V\in\mathcal U(\mathcal A_R')}\!\langle V^\dagger \hat P V\rangle
  \;}
\]

which is a **verbatim transport** of Liu Eq. 8.32 to the modular-time
parameter $\tau_R$ via the CLPW §3 Bisognano–Wichmann identification,
combined with the observation that v6 Eq. (1) r.h.s. is a conjectural
(M1') upper bound on this same infimum. No new theorem on top of
Liu, but a clean dictionary entry. That is the publishable content.

---

*File: paper/_internal_rag/piste_B_opus_deep_analysis.md | ~410 lines |
Source anchor: /tmp/liu2026.txt (arXiv:2601.07915v1, equations 8.13,
8.15, 8.16, 8.17, 8.18, 8.24, 8.25, 8.26, 8.27, 8.32, 8.33, 8.39,
8.40 verified verbatim 2026-04-22).*
