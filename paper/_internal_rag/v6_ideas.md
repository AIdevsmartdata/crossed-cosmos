# v6 Parking Lot — ECI-dynamics companion ideas

Status: **archived, NOT for v5.0**. Material below is speculative, did not
pass the v5.0 editorial bar, and is parked here for potential revisit in a
"v6" companion paper after v5.0 peer-review feedback lands.

Owner responsibility: K. Remondière to review, modify, or discard during
the v5.1 rewrite cycle.

---

## 1. Proposed equation (verbatim, as suggested by external Claude.ai review
of v5.0)

$$
\frac{d\,S_{\rm gen}[\mathcal{R}]}{d\tau_{\mathcal{R}}}
\;=\;
\kappa_{\mathcal{R}}\,
\mathcal{C}_k\bigl[\rho_{\mathcal{R}}(\tau)\bigr]\,
\Theta\!\bigl(\mathrm{PH}_k[\delta n(\tau)]\bigr)
$$

Reading: the proper-time rate of change of the observer-dependent
generalised entropy $S_{\rm gen}[\mathcal{R}]$ is proportional to a
$k$-design complexity functional $\mathcal{C}_k$ of the QRF-reduced state
$\rho_{\mathcal{R}}$, gated by a persistent-homology step function of the
primordial number-density perturbation $\delta n$. The Lagrange-type
coefficient $\kappa_{\mathcal{R}}$ is observer-specific.

## 2. Honest strengths

- **Poetic unification.** Ties the three C's (crossed-product entropy,
  complexity, coarse-grained topology) into a single dynamical line,
  matching the three-strand rhetoric already present in the v5.0 axioms.
- **Touches A1 + A2 + A3 + A6 simultaneously.** $S_{\rm gen}[\mathcal{R}]$
  = A1 functor; $d/d\tau$ invokes A2's thermodynamic emergence; $\mathcal{C}_k$
  is the A3 Cryptographic-Censorship decodability quantity; $\mathrm{PH}_k$
  is the A6 persistent-homology diagnostic. No axiom is left behind.
- **Monotonicity, if true, would give a C-theorem analogue** for
  observer-dependent cosmology — an attractive A2-adjacent result.

## 3. Honest weaknesses blocking v5.0 adoption

**(a) Not derived from a variational principle.** The ansatz is written
down, not obtained from $\delta S_{\rm matter} + \delta S_{\rm grav} = 0$
nor from any modular-flow computation. Compare Jacobson 1995 (A2) which
*derives* Einstein from $\delta Q = T_U\,\delta S$: the proposed line
lacks this anchor.

**(b) Category error on $\alpha = 0.095$ reuse.** External review
suggested identifying $\kappa_{\mathcal{R}}$ with the D15 chameleon
$\alpha = 0.095$. That $\alpha$ was derived from a **density ratio**
$\Theta(\rho)=\exp[-(\rho/\rho_c)^\alpha]$ in §3.6 screening; reusing it
as the exponent of a **topological/entropic rate equation** is a category
error. The two quantities live in different dimensionful spaces
(density vs. information rate).

**(c) Non-falsifiable predictions.** The three proposed consequences
floated in the review (arrow of time from monotonicity, Big Bang as
"algorithmic" boundary, CMB low-$\ell$ anomalies from $\mathrm{PH}_k$
gate opening) are either already in v5.0 under weaker form (the
"decodability boundary" prediction D) or too vague to state a falsifier
range comparable to the Table 1 entries in §4 of v5.0.

**(d) Too close to existing entropic-gravity reformulations.** The line
lives in the same genre as Verlinde 2011 (entropic gravity), Jacobson
1995/2016 (thermodynamic Einstein), and Padmanabhan entropic
cosmology. Without a genuinely new falsifier, adding it to ECI would
dilute the "architectural synthesis" positioning of v5.0 and invite the
criticism "yet another entropic-gravity reskin".

## 4. Decision

**Parked for potential v6 "ECI-dynamics" companion paper**, conditional on
v5.0 peer-review feedback. Triggers that would reopen this note:

- Referee explicitly asks for a dynamical equation linking A1/A3/A6.
- An independent derivation of the modular-flow $d S_{\rm gen}/d\tau$
  appears in the literature (watch: Faulkner–Speranza follow-ups,
  Kirklin 2025 extensions).
- A PH-gated $\delta n$ observable is proposed in upcoming CMB-S4 /
  LiteBIRD forecasts that would make point (c) falsifiable.

Absent those triggers, the equation stays here.

## 5. Source

External Claude.ai editorial review of v5.0, delivered 2026-04-21 as
part of the same feedback pass that produced the v5.0.1 editorial
fixes (bib annotation leak, Eq (9) convention note, abstract
prior-rail flag, §3.6 Resolution (iii) cross-reference). That review
correctly flagged the equation as "out of scope for v5.0"; this note
records the suggestion for posterity without promoting it into the
main text.
