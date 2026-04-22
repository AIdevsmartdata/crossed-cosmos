# FAILED.md — Registry of explored-and-rejected avenues

**Purpose.** Public record of paths we have already explored and
rejected, with the specific reason each failed. Prevents the same
mistake being re-attempted across sessions or by new agents.

**Format.** Each entry: **(1) Date explored, (2) What was proposed,
(3) Why it failed, (4) Artefact pointer(s), (5) What would be needed
to re-open.** Entries are never deleted, only appended or annotated.

**Pipeline discipline (PRINCIPLES.md rule adjoined):** before any new
agent is launched to explore a research direction, it MUST read this
file. Before writing any new `paper/_internal_rag/v*.md` document, the
author (human or agent) MUST confirm the direction does not match any
FAILED entry.

---

## F-1 — Equality form of v6 main inequality

**Date.** 2026-04-21 / 2026-04-22.

**Proposed.** Promote
$dS_{\mathrm{gen}}/d\tau_R \le \kappa_R \mathcal{C}_k \Theta$
to an equality: $dS_{\mathrm{gen}}/d\tau_R = \kappa_R \mathcal{C}_k \Theta$.

**Why it failed.** Three independent derivation-agent verdicts
(Claude/Gemini/Magistral) returned ANSATZ, not THEOREM. Adversarial
Attack #2 landed fatally: in the Fan (2022) logarithmic Krylov regime,
the equality form becomes a contradiction at scrambling saturation.
Codified as PRINCIPLES.md rule V6-1.

**Artefacts.** `derivations/V6-inequality-derivation.py`,
`derivations/V6-draft-adversarial-attack.md`.

**Re-open conditions.** A rigorous type-II theorem identifying the
modular-commutator source with $\kappa_R \mathcal{C}_k$ exactly (not
up to an inequality), plus a Fan-saturation-compatible rescaling of
$\mathcal{C}_k^{\max}$.

---

## F-2 — Cosmological fσ_8 × Θ(PH_2) falsifier

**Date.** 2026-04-21.

**Proposed.** Use the cross-spectrum between the growth rate $f\sigma_8$
and the order-2 persistent-homology activator $\Theta(\mathrm{PH}_2)$
of the matter density field as a cosmological falsifier for v6.

**Why it failed.** D18 Fisher forecast gave $S/N < 0.5\sigma$ at fiducial
$\epsilon_0 = 0.02$ with DR3+Euclid precision; D18b bias-marginalisation
showed $|\rho(b_0, \epsilon_0)| = 0.998$ (degenerate) and
$\sigma(\epsilon_0)_{\mathrm{marg}}/\sigma(\epsilon_0)_{\mathrm{fix}} = 21.7\times$
(DR3), $26.8\times$ (DR3+Euclid). Codified as PRINCIPLES.md rule V6-4
("v6 is a formal paper, not a cosmology paper; do not re-propose a
cosmological prediction in v6").

**Artefacts.** `derivations/D18-report.md`, `derivations/D18b-report.md`.

**Re-open conditions.** A new falsifier variant passing a D19+
equivalent pipeline: Fisher forecast + nuisance marginalisation +
cross-model adversarial, with $S/N \ge 3\sigma$ post-marginalisation.

---

## F-3 — Claude-app "loi ECI finale" (Einstein 1915 framing)

**Date.** 2026-04-22.

**Proposed.** A "fifth CODATA fundamental constant"
$\kappa_C = 2\pi k_B/\hbar$, an "operational equivalence principle"
between entropy and complexity (analogue of Einstein 1907), and three
cosmological predictions (PBH burst $\times 3$, LISA stochastic
plateau, $\dot\alpha/\alpha \sim H_0$).

**Why it failed.** Three arithmetic errors: $\omega_P = 2\pi k_B T_P/\hbar$
is off by $2\pi$; $S_{BH}(5.1\times 10^{14}\,\text{g}) = 10^{40}$ not
$10^{25}$ (15 orders off), which invalidates the PBH burst $\times 3$
prediction (extension factor becomes $\approx 1$); Lange 2021 PRL 126,
011102 value quoted as $-8.0 \pm 3.6 \times 10^{-18}$/yr was
fabricated (real value $1.0 \pm 1.1 \times 10^{-18}$/yr). Plus four
PRINCIPLES violations (V6-1, V6-4, rule 1, rule 16).

**Artefacts.** `paper/_internal_rag/v6_claude_app_audit.md`,
`derivations/V6-claude-app-numerical-audit.py`.

**Re-open conditions.** Do not.

---

## F-4 — Claude-app v2 "Horndeski augmenté TDA" log envelope

**Date.** 2026-04-22.

**Proposed.** Replace v6.2 logistic envelope with
$dS_{\mathrm{gen}}/d\tau_R \le (k_B/\tau_R^{\*})\log(1+\mathcal{C}_k/\mathcal{C}_k^{\*})\Theta$
with explicit causal window on PH_k.

**Why it failed.** At Fan 2022 scrambling saturation,
$\log(1+\mathcal{C}_k^{\max}/\mathcal{C}_k^{\*}) \to \log 2$, finite
non-zero; logistic envelope correctly goes to $0$. Mistral Magistral
cross-check independent verdict "Form B is a regression". Causal
window claim based on misreading of PH_k temporal structure
(filtration is spatial at fixed $\tau_R$, not historical).

**Artefacts.** `paper/_internal_rag/v6_claude_app_audit_v2.md`,
`derivations/V7-D-log-envelope-nogo.md` (formal no-go).

**Re-open conditions.** A new envelope shape $\Phi(x)$ with
$\Phi(1)=0$ AND a derivation that makes it strictly better than the
logistic on some independent criterion.

---

## F-5 — Claude-app v2 four cosmological falsifiers

**Date.** 2026-04-22.

**Proposed.** v6 cosmological falsifiers: (1) $\Delta H_0/H_0 \sim 5$–$8\%$
from $\Lambda_{\mathrm{eff}}(\tilde{C}, \mathrm{ph}_k)$; (2) GW residual
dispersion at LISA 2035; (3) CMB birefringence $\alpha_{\mathrm{bir}} \sim 0.3°$
at LiteBIRD 2032; (4) $S_8$ growth modified 2–4%.

**Why it failed.** V6-4 applies: no cosmological falsifier for v6
without D18-equivalent pipeline. None of the four carried a Fisher
forecast + nuisance marginalisation + cross-model adversarial verdict.
The $S_8$ prediction is additionally weakened by KiDS-Legacy 2025
reducing the tension to $<1\sigma$ (doc self-acknowledged).

**Artefacts.** Same audit v2.

**Re-open conditions.** Produce a D19+ pipeline artefact per candidate
falsifier. Until then, these are ANALOGY-level motivations.

---

## F-6 — Claude-app v3 ZSA "subsumes ECI v6"

**Date.** 2026-04-22.

**Proposed.** ZSA (Zeta-Spectral Adelic) framework subsumes v6 by
identifying: (a) $\mathcal{C}_k$ $k$-design $\leftrightarrow$
$\sum_{p \le p_k} \log p$ Euler truncation; (b)
$\mathrm{PH}_k[\delta n]$ $\leftrightarrow$ $HP(\mathcal{A})$ periodic
cyclic cohomology.

**Why it failed.** Mistral Magistral independent verdict: (a) is
NOMINAL COINCIDENCE (two different meanings of letter "k"); (b) is
MATHEMATICAL ERROR (persistent homology in TDA and periodic cyclic
cohomology in homological algebra are unrelated structural objects).
The ZSA framework proposal is therefore a synthesis-with-category-errors,
not a rigorous subsumption. Numeric claim on $N_{\mathrm{zeros}}$ at
Planck height was off by 8 orders (10^12 claimed vs 10^20 Riemann-von
Mangoldt).

**Artefacts.** `paper/_internal_rag/v6_claude_app_audit_v3_zsa.md`.

**Re-open conditions.** Rewrite ZSA with rigorously correct identifications
(e.g. replace PH $\leftrightarrow$ HP by PH $\leftrightarrow$
Kashiwara–Schapira microlocal sheaves, and C_k by a specific choice
not conflating k-design and Euler indices) plus numerical corrections.

---

## F-7 — ZSA Λ mechanism via Euler–Maclaurin spectral sum

**Date.** 2026-04-22.

**Proposed.** Obtain $\Lambda \approx (2.24\,\mathrm{meV})^4$ as an
Euler–Maclaurin regularisation residue of the spectral sum over
Riemann zeros on an adelic cutoff $\mu_\zeta$. Presented as "alternative
voie" in Claude-app v3 after the naïve mechanism was admitted to fail.

**Why it failed.** Direct numerical computation on the first 10^5
Odlyzko zeros gave arithmetic residue $S - I \approx 0.449$,
$\Lambda$-independent across $[100, 10000]$, cutoff-independent at
$10\%$. Multiplying by $\Lambda^4/(2\pi)^2$ restores the ordinary
quartic zero-point-energy divergence. No fine-tuned small residue
explains $\Lambda_{\mathrm{obs}}/M_P^4 \sim 10^{-120}$. Verdict
**TRIVIAL-CANCELLATION**.

**Artefacts.** `derivations/V7-euler-maclaurin-lambda.py`,
`derivations/V7-euler-maclaurin-lambda-report.md`, commit `0cdfea6`.

**Re-open conditions.** A non-trivial regularisation prescription
(beyond the smooth-integral subtraction we tested) that isolates
arithmetic-sensitive finite parts. Not currently on the horizon.

---

## F-8 — Sub-Planck-scale numerology

**Date.** 2026-04-22.

**Proposed.** A systematic $|a,b,c| \le 4$ exponent scan across
$\{H_0, \Lambda^{1/4}, m_e, m_p, m_\nu, v_{EW}, \Lambda_{QCD}, F_\pi,
\alpha\}$ normalised by $M_P$, searching for a power-law relation
matching $\Lambda/M_P^2$ below $1\%$ accuracy.

**Why it failed.** No match below $1\%$ beyond two
already-physically-motivated anchors: Friedmann identity
$\Lambda \approx 3 H_0^2 \Omega_\Lambda/c^2$; Montero–Vafa–Valenzuela
$\Lambda^{1/4} \approx m_\nu$. The best exponent for
$H_0/\omega_P \approx (m_e/M_P)^k$ is $k \approx 2.72$, non-rational.
Gonzalo–Montero–Obied–Vafa $\langle H\rangle \sim \Lambda^{1/6}M_P^{1/3}$
fails by $\sim 6240\times$ against observed $v_{EW} = 246\,\mathrm{GeV}$.

**Artefacts.** `derivations/V6-claude-app-v2-numerical-audit.py`
and the Appendix B of v6.1 JHEP draft
(`paper/v6/v6_jhep.tex`, §\ref{app:numerology}).

**Re-open conditions.** A theoretical principle that picks a specific
exponent triple naturally (not by scanning). Without such a principle,
the search space is too large and false positives are guaranteed.

---

## F-9 — Claude-app v3 Test 5 / ZSA 2-point prediction

**Date.** 2026-04-22.

**Proposed.** Use pair-correlation statistics of Odlyzko zeros at
finite height $T$ to test an $O(1/\log T)$ deviation from pure GUE
specifically predicted by Connes–Consani–Moscovici arXiv:2511.22755.

**Why it failed.** Numerical test on 10^5 Odlyzko zeros confirmed a
$>7\sigma$ deviation from pure GUE — but its shape and amplitude
match the 30-year-old Bogomolny–Keating 1996 arithmetic correction,
not a ZSA-specific prediction. Moreover, WebFetch of arXiv:2511.22755
full PDF (652 KB) confirmed the paper gives only 1-point (individual
zero) predictions with high accuracy; no explicit 2-point correction
formula exists to fit. Verdict **STRUCTURED-UNKNOWN** — cannot
discriminate ZSA from BK.

**Artefacts.** `derivations/V7-test5-odlyzko-report.md`, commit `ca3e0e7`.

**Re-open conditions.** An explicit 2-point correction formula from
CCM or a sequel, distinct from Bogomolny–Keating, testable on the
Odlyzko data.

---

## Meta-patterns observed across F-1 through F-9

1. **Premature promotion from ANSATZ/POSTULATE to THEOREM/LAW** — F-1,
   F-3. Fix: PRINCIPLES rule V6-1, pre-write audit pipeline.
2. **Cosmological falsifiers without Fisher/marginalisation pipeline**
   — F-2, F-5. Fix: V6-4.
3. **Citation fabrication** — F-3 (Lange). Fix: bib-DOI-hash pipeline
   (to be implemented).
4. **Arithmetic errors in load-bearing numbers** — F-3 ($S_{BH}$, $2\pi$),
   F-6 ($N_{\rm zeros}$). Fix: numerical-audit auto-trigger (to be
   implemented).
5. **Terminological / category conflation** — F-6 (k-design vs Euler
   truncation; PH vs HP). Fix: require Mistral/Gemini cross-check
   of any "identification" claim.
6. **Numerology via exponent scanning** — F-8. Fix: explicit theoretical
   principle required before accepting any power-law identification.
7. **Extrapolation from mathematical construct to physical reality** —
   F-7 (Euler–Maclaurin Λ), proposed ZSA cosmological reading of
   Bost–Connes. Fix: numerical test before publication.

---

## F-10 through F-17 — v8 15-agent parallel exploration results

Added 2026-04-22 after Sonnet-parallel exploration of 15 analogies.
See `v8_synthesis.md` for full scorecard. Each below is an analogy
tested-and-rejected, added here to prevent re-exploration.

### F-10 — Legendre K_R ↔ C_BS (agent 2)
Legendre transform of modular Hamiltonian equals von Neumann entropy
(bounded $\log 16$), not Brown-Susskind complexity (purity inverse,
linear in Hilbert dim). Ratio $[0.18, 0.48]$ on β ∈ [0.1, 10]. NO
multiplicative constant. Artefact: `derivations/V8-agent-02-*`.
**Re-open**: would require identifying a non-thermodynamic Legendre
partner of K_R which equals C_BS. Unlikely.

### F-11 — Jaynes MaxCaliber → v6 bound (agent 3)
MaxCal yields $p^* \propto e^{-\lambda C_k}$ implying linear-in-$C_k$
bound, not logistic, no topological $\Theta$ factor emerges. Req M1
still external. Artefact: `V8-agent-03-*`.
**Re-open**: would require maxcal constraint on both $C_k$ and PH_k
simultaneously, with non-trivial cross-constraint. Not attempted.

### F-12 — Landau order-param α fit to v5 (agent 4)
GRF percolation universality gives $\alpha \in [0.4, 2.1]$ (cubical
β_1 proxy α=2.12; GKF analytic α=0.43). v5 M3 target $(0, 0.1]$ with
fiducial 0.095. **α cannot arise from this universality class.** Artefact:
`V8-agent-04-*`.
**Re-open**: different random-field ensemble (non-Gaussian, clustered)
might yield smaller α, at the cost of physical motivation.

### F-13 — ξ_χ from Wetterich modular RG (agent 5)
1-loop FRG fixed point is $\xi = 1/6$ (conformal coupling), repulsive
flow, v5 best-fit 0.003 needs fine-tuning width $\sim 6.5 \times 10^{-4}$.
Four ad-hoc flags; identification k = T_R exp(τ_R) not derivable.
Artefact: `V8-agent-05-*`.
**Re-open**: a 2-loop or non-local beta function might change the
landscape. Requires NCG / FRG expert.

### F-14 — Jacobson d_iS → v5 NMC (agent 6, **MOST IMPORTANT BLOCKED BRIDGE**)
Req A fatal: $C_k$ is a state functional, $d_iS$ is extrinsic
horizon-geometric. Categorically different objects. M1 POSTULATE
cannot be bridged into a local polynomial $\xi R \chi^2$. Artefact:
`V8-agent-06-*`.
**Re-open**: a derivation of $C_k$ as a functional of local curvature
observables (rather than global state properties) would be required.
No route currently known.

### F-15 — DD species scale c' ↔ modular γ_m (agent 8)
γ_m = 1 vs c' = 1/6. Framework-mismatch (kinematic weight vs KK-tower
state density). Artefact: `V8-agent-08-*`.
**Re-open**: would need a theorem bridging KK-tower density to
modular spectral density — absent from all RAG references.

### F-16 — Bures metric ↔ C_BS (agent 10)
β=0.141, R²=0.071 power-law; linear R²=-0.95 (strongly rejected).
Bures tracks eigenvalue+eigenvector, C_BS only eigenvalue.
Artefact: `V8-agent-10-*`.
**Re-open**: a modified distance that projects onto the purity
direction might correlate, but then it's not Bures.

### F-17 — Heat-kernel CCM spectral action Λ (agent 15)
Consolidates F-7. $\rho_\Lambda^{\rm spec} \sim 10^{-2} M_P^4$,
off by $10^{120}$ from $\Lambda_{\rm obs}$. ζ-zeros enter $a_4$
(curvature²), not $a_0$ (cosmological constant). The ZSA Λ
mechanism is **definitively closed** via two independent
regularisations (F-7 Euler-Maclaurin + F-17 heat-kernel).
Artefact: `V8-agent-15-*`.
**Re-open**: unlikely; would require a non-perturbative
regularisation invariant none of the surveyed frameworks provides.

---

---

## F-19 — Mock Jacobi form for NMC quintessence horizon Z(τ)

**Date.** 2026-04-22.

**Proposed.** The horizon partition function Z(τ) = Tr_{A_R} e^{−β H_R}
for the NMC quintessence static patch (ξ_χ R χ²/2, χ₀ = M_P/10) admits a
mock Jacobi decomposition à la Dabholkar-Murthy-Zagier 2012 (arXiv:1208.4074),
and the Zwegers harmonic completion reproduces (up to known constants) the
v6 GSL type-II violation term κ_R C_k (1−Θ).

**Why it failed.** Four fatal obstructions:
(1) **Non-holomorphy**: eigenspectrum of H_χ on S³ is irrational
    (ν² = m²_eff/H²_eff − 9/4 ∉ ℤ at χ₀ = M_P/10 fiducial); QNM
    damping also breaks τ-analyticity. Z(τ) is not a meromorphic Jacobi form.
(2) **No modular group action**: τ→τ+1 fails (irrational spectrum);
    τ→−1/τ fails (dS₄ not self-dual under temperature inversion;
    no Cardy formula). Without SL(2,ℤ), mock modular classification is moot.
(3) **Wrong universality class**: D-M-Z 2012 is a theorem about N=4 SUSY
    quarter-BPS dyons on K3×T². NMC quintessence dS₄ is thermal (T_H>0),
    non-BPS, non-SUSY, with Euclidean geometry S⁴ not T². Score: 0/4
    prerequisites satisfied.
(4) **Categorical mismatch**: Zwegers shadow arises from polar (BPS) part
    of a meromorphic Jacobi form; κ_R C_k (1−Θ) is a modular-Hamiltonian
    rate × complexity × PH_k indicator. Dimensionally and structurally
    incompatible.

**Artefacts.** `derivations/V8-piste3-mock-jacobi.py` (sympy + prose),
`paper/_internal_rag/v8_piste3_mock_jacobi_report.md`.

**Re-open conditions.** Embedding NMC quintessence in a type-IIB or N=2
string-theoretic sector where χ is a BPS compactification modulus with an
attractor geometry, and an explicit construction of a holomorphic Jacobi form
from that string partition function. Multi-paper program; not achievable in
a single derivation session.

---

## Meta-update

**Pattern confirmed across v8 15-agent run:**
- Analogies testable in an afternoon do not replace years of expert
  research.
- Strong analogy intuitions (Legendre, Jacobson, Wetterich) fail
  rigorously — that failure is itself diagnostic.
- Genuine positives are REFORMULATIONS of existing structure (agents
  1, 9), not new physics.
- The mathematical-landscape watchlist (Hypothesis H, Bost-Connes/CCM,
  Kashiwara-Schapira) is more refined now: KS is **theorem-rigorous**
  for PH_k reformulation, the other two remain HOOK-PROGRAMMATIC.
