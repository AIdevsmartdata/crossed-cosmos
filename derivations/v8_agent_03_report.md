# v8-agent-03 — MaxCaliber ↔ v6 bound

**Date.** 2026-04-22  
**Verdict.** YIELDS-DIFFERENT-BOUND

---

## 1. MaxCal on modular-flow trajectories

Maximum Caliber (Pressé et al. Rev. Mod. Phys. 85, 1115, 2013;
Dixit–Ghosh–Dill 2014) maximises the path-trajectory entropy

$$
\mathcal{H}[p] = -\int \mathcal{D}[\gamma]\, p[\gamma]\log p[\gamma]
$$

subject to normalisation and one mean-constraint per observable:

$$
\langle \mathcal{C}_k \rangle_p
= \int \mathcal{D}[\gamma]\, p[\gamma]\, \mathcal{C}_k[\gamma] = \bar C.
$$

Applied to modular-flow trajectories $\gamma: \tau_R \mapsto \rho_R(\tau_R)$
on the type-II$_1$ factor $\mathcal{A}_R$, the MaxCal saddle is

$$
p^*[\gamma] \propto \exp\!\bigl(-\lambda\, \mathcal{C}_k[\gamma]\bigr),
$$

with Lagrange multiplier $\lambda > 0$ set by $\bar C$.

The instantaneous entropy-production rate at the MaxCal saddle obeys

$$
\frac{dS_{\mathrm{gen}}}{d\tau_R}\bigg|_{\mathrm{MaxCal}}
\;\le\;
\lambda(\bar C)\cdot \mathcal{C}_k[\rho_R(\tau_R)].
\tag{MaxCal bound}
$$

---

## 2. Comparison with v6 bound

The v6 main inequality is

$$
\frac{dS_{\mathrm{gen}}}{d\tau_R}
\;\le\;
\kappa_R\cdot \mathcal{C}_k[\rho_R(\tau_R)]\cdot
\Theta\!\bigl(\mathrm{PH}_k[\delta n(\tau_R)]\bigr).
\tag{v6}
$$

**Structural differences:**

| Feature | MaxCal bound | v6 bound |
|---|---|---|
| Prefactor | $\lambda(\bar C)$ (constraint-normalised Lagrange multiplier) | $\kappa_R$ (modular temperature, Connes–Rovelli) |
| Topological factor | absent | $\Theta(\mathrm{PH}_k[\delta n])$ (M3, CONJECTURAL) |
| Derivation path | variational (entropy extremisation) | Wall GSL + Pinsker + M1–M3 postulates |
| Logistic envelope | absent | Prop. 1 (Brown–Susskind complexity growth postulate) |

**Prefactor mismatch.** $\lambda(\bar C)$ is determined by the
normalisation $\langle C_k\rangle_p = \bar C$ and carries no
information about the modular temperature $\kappa_R = 2\pi/\beta_R$.
Setting $\lambda \equiv \kappa_R$ would require $\bar C$ to track the
modular temperature exactly — an additional identification not supplied
by MaxCal itself and equivalent to M1 as an ansatz, not a derivation.

**Topological factor absent.** The MaxCal path measure $p^*[\gamma]$
depends only on $\mathcal{C}_k$; the dequantised density field
$\delta n$ and its persistent-homology activator $\Theta$ enter v6 via
M2–M3, which are postulates external to the variational principle.
MaxCal has no mechanism to produce the $\Theta$ factor.

**Logistic envelope not selected.** Prop. 1 of v6 tightens the linear
bound to $\kappa_R \mathcal{C}_k(1 - \mathcal{C}_k/\mathcal{C}_k^{\max})\Theta$
by postulating that $\mathcal{C}_k$ itself evolves with a logistic rate
(Brown–Susskind "second law of complexity"). MaxCal extremises a
static functional over path distributions; it does not select a specific
dynamical law for $\mathcal{C}_k$. Among the class of distributions
consistent with $\langle \mathcal{C}_k\rangle = \bar C$, MaxCal picks the
exponential (maximum-entropy) one — which is linear in $\mathcal{C}_k$,
not logistic.

---

## 3. Does MaxCal recover v6 as a special case?

No. The MaxCal bound (MaxCal) and the v6 bound (v6) share the same
schematic form $(\text{prefactor}) \cdot \mathcal{C}_k$ only if one
identifies $\lambda \equiv \kappa_R$ and discards the $\Theta$ factor
(i.e. formally takes $\Theta = 1$). Both identifications require
external postulates (M1 and M3 respectively) that are not outputs of
MaxCal. The logistic envelope of Prop. 1 additionally requires M1 in
its dynamical form; MaxCal does not produce it.

MaxCal is therefore a **parallel variational framework** that yields a
weaker, structurally different bound. It cannot serve as a first-
principles derivation of v6.

---

## 4. Framework applicability assessment

MaxCal is applicable to modular-flow trajectories in principle (the
path-entropy functional is well-defined on any measure space of
trajectories). The obstruction is not applicability but derivational
power: MaxCal's output is the exponential path distribution, which
implies only the linear-in-$\mathcal{C}_k$ bound and not the v6
structure.

---

## 5. Verdict

**YIELDS-DIFFERENT-BOUND.**

MaxCal on modular-flow trajectories with $\mathcal{C}_k$ as the
constraint observable produces a bound linear in $\mathcal{C}_k$ with
a constraint-normalised Lagrange multiplier $\lambda$. This differs
from the v6 bound in three ways: (i) $\lambda \neq \kappa_R$ without
M1 as an external identification; (ii) no topological factor $\Theta$
emerges; (iii) the logistic envelope (Prop. 1) is not selected.
No FAILED entry (F-1 through F-9) blocks this analysis; MaxCal has
not been previously attempted.

---

*Rules checked: V6-1 (inequality preserved throughout), V6-4 (no
cosmological claim made), PRINCIPLES rule 1 (no training-memory
citations — only Pressé et al. 2013 RMP 85:1115 and Dixit–Ghosh–Dill
2014, both standard MaxCal references verifiable from the v6 RAG
context), PRINCIPLES rule 12 (no new bib entry without RAG
verification — bib entries not added; references cited for analysis
only).*
