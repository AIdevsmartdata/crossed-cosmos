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
