# V7–D — No-go proposition for log-type saturation envelopes

**Status.** Short formal memo, intended for inclusion as a Remark in a
future v6.2 revision OR in a standalone technical note bundling B + C
+ D. Not a theorem of wide generality — a specific no-go for one class
of proposed envelope forms.

**Date.** 2026-04-22. Commit: (this file).

---

## Context

The v6.2 main inequality (Eq. 1) admits a logistic-type tightening
(Proposition 1):

$$
\frac{dS_{\mathrm{gen}}}{d\tau_R} \;\le\; \kappa_R\,\mathcal{C}_k
\left(1-\frac{\mathcal{C}_k}{\mathcal{C}_k^{\max}}\right)\,
\Theta(\mathrm{PH}_k[\delta n]).
\tag{Form A}
$$

A Claude-app proposal (audit `v6_claude_app_audit_v2.md`) offered as
"minimal correction" a logarithmic envelope

$$
\frac{dS_{\mathrm{gen}}}{d\tau_R} \;\le\;
\frac{k_B}{\tau_R^{\*}}\,\log\!\left(1+\frac{\mathcal{C}_k}{\mathcal{C}_k^{\*}}\right)\,
\Theta(\mathrm{PH}_k[\delta n(\tau_R-\Delta,\tau_R)]),
\tag{Form B}
$$

with $\tau_R^{\*} = \hbar/(2\pi k_B T_R)$, $\mathcal{C}_k^{\*} = 2^n$.

This memo establishes that Form B is **inconsistent with the Fan 2022
logarithmic Krylov regime** at scrambling saturation, while Form A is
consistent. The result is a constraint on admissible envelope shapes,
not a uniqueness statement.

---

## Proposition D1 (Saturation vanishing of the LHS)

**Setting.** Let $\AR$ be a type II$_\infty$ crossed-product algebra
with modular flow $\sigma^R_{\tau_R}$ and KMS-$\beta_R$ equilibrium
state $\rho_R$. Let $\mathcal{C}_k$ denote the $k$-design complexity
(PRU / Caputa spread complexity under modular flow), with scrambling
plateau $\mathcal{C}_k^{\max} \sim \exp(S_R)$ (Haferkamp 2022;
Brown–Susskind 2018).

**Fan 2022 / Krylov saturation condition.** In the regime
$\mathcal{C}_k \to \mathcal{C}_k^{\max}$, the complexity rate
$\dot{\mathcal{C}}_k \to 0$ (Haferkamp plateau), and Fan 2022 shows
$\dot{S}_K \propto \dot{\mathcal{C}}_K / \mathcal{C}_K$ in the
logarithmic Krylov regime. Hence the physical entropy rate at full
scrambling satisfies

$$
\lim_{\mathcal{C}_k \to \mathcal{C}_k^{\max}}
\frac{dS_{\mathrm{gen}}}{d\tau_R} = 0.
\tag{Saturation}
$$

**Claim.** The logistic envelope of Form A satisfies (Saturation);
the log envelope of Form B does not.

**Proof of consistency (Form A).** Substituting
$\mathcal{C}_k = \mathcal{C}_k^{\max}$ in Form A:

$$
\kappa_R\,\mathcal{C}_k^{\max}\cdot\left(1 - \frac{\mathcal{C}_k^{\max}}
{\mathcal{C}_k^{\max}}\right)\cdot\Theta(\cdots) =
\kappa_R\,\mathcal{C}_k^{\max}\cdot 0 \cdot \Theta(\cdots) = 0.
$$

Hence any state saturating Form A at $\mathcal{C}_k = \mathcal{C}_k^{\max}$
has zero entropy rate, consistent with (Saturation). $\square$

**Proof of inconsistency (Form B).** Substituting
$\mathcal{C}_k = \mathcal{C}_k^{\max} \sim \exp(S_R)$ and
$\mathcal{C}_k^{\*} = 2^n$ in Form B, with
$S_R \sim n \log 2$ (von Neumann entropy of the maximally-scrambled
state on $n$ qubits):

$$
\mathcal{C}_k / \mathcal{C}_k^{\*} \sim \exp(S_R)/2^n \sim
\exp(n \log 2)/2^n = 1.
$$

Therefore

$$
\frac{k_B}{\tau_R^{\*}}\,\log(1 + 1)\,\Theta(\cdots) =
\frac{k_B \log 2}{\tau_R^{\*}}\,\Theta(\cdots).
$$

This is a **finite, $\Theta$-dependent positive quantity** with value
$\Theta(\cdots)\cdot k_B \log 2 / \tau_R^{\*}$. At saturation,
$\Theta \to 1$ if the persistent-homology activator has approached
its classical limit, giving

$$
\lim_{\mathcal{C}_k \to \mathcal{C}_k^{\max}}
[\text{Form B RHS}] = \frac{k_B \log 2}{\tau_R^{\*}} > 0.
$$

Form B therefore permits $dS_{\mathrm{gen}}/d\tau_R$ bounded above by a
non-zero positive number at scrambling saturation, violating
(Saturation) unless some independent mechanism forces the LHS to zero.
No such mechanism is provided in Form B's statement. $\square$

---

## Corollary D2 (Class of admissible envelopes)

A saturation-envelope function $\Phi(\mathcal{C}_k/\mathcal{C}_k^{\max})$
appearing as

$$
\frac{dS_{\mathrm{gen}}}{d\tau_R} \;\le\;
\kappa_R\,\mathcal{C}_k\,\Phi(\mathcal{C}_k/\mathcal{C}_k^{\max})\,\Theta
$$

must satisfy the boundary condition $\mathcal{C}_k \cdot
\Phi(\mathcal{C}_k/\mathcal{C}_k^{\max}) \to 0$ as
$\mathcal{C}_k \to \mathcal{C}_k^{\max}$ in order to be consistent with
the Fan 2022 logarithmic saturation.

The logistic $\Phi(x) = 1 - x$ passes; pure $\Phi(x) = 1$ (no envelope)
does not; $\log$-shifted $\Phi(x) = \log(1+x)/x$ (i.e. the Form B
shape rewritten) does not in the limit $x \to \mathcal{C}_k^{\max}/\mathcal{C}_k^{\*}$
unless $\mathcal{C}_k^{\*}$ is adjusted to grow as $\mathcal{C}_k^{\max}$.

An equivalent admissibility criterion: any envelope of the form
$\Phi(x)$ with $x = \mathcal{C}_k/\mathcal{C}_k^{\max}$ must satisfy
$\Phi(1) = 0$.

---

## Scope and caveats

1. This is a **consistency constraint** with Fan 2022, not a uniqueness
   theorem. Other envelope families that vanish at $x=1$ may exist
   (e.g. $\Phi(x) = (1-x)^n$ for $n \ge 1$); the proposition rules in
   the logistic and rules out the pure-log, but does not single out the
   logistic.

2. The proposition uses the weak form of Fan 2022 at saturation
   ($\dot{S}_K \to 0$); it does not require the full Fan logarithmic
   law in its interior. A stronger statement — that the logistic is
   the \emph{unique} envelope reproducing Fan \emph{everywhere} in the
   scrambling regime — requires a longer derivation and is not claimed
   here.

3. The Mistral Magistral cross-check on 2026-04-22 (see
   `paper/_internal_rag/v6_claude_app_audit_v2.md`) confirms this
   verdict independently.

4. If one wishes to use a log-shape envelope as an *approximation*
   away from saturation, this is unobjectionable; the no-go is
   specifically about the limit behaviour.

---

## Relation to the main v6 text

The Proposition 1 logistic envelope currently in v6.2 §5 automatically
satisfies the admissibility criterion (D2). No change to v6.2 is
necessary. A one-sentence Remark could optionally be added after
Prop.1 pointing out that the logistic shape is selected among
envelope-class candidates by this saturation-vanishing constraint, but
this is not mandatory; the proposition as stated stands.

If the technical note bundling V7-B (Bogomolny-Keating fit on Odlyzko
residual) + V7-D (this memo) is produced as a standalone Zenodo /
arXiv deposit, the no-go can appear as a short technical lemma with
the proof above.
