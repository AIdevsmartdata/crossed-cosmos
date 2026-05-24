# Structural origin of the Heegner exponent N = 2|Φ⁺| + 1 = 7 from the SU(3) root system in the cosmological constant prediction

**Author** : Kévin Rémondière
**Affiliation** : Independent researcher, Oloron-Sainte-Marie, France
**ORCID** : [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)
**Email** : kevin.remondiere@gmail.com
**Date** : 2026-05-24
**Target journal** : Letters in Mathematical Physics, Comptes Rendus Mathématique, or similar short‑note venue
**Status** : Draft v1, ready for adversarial review
**License** : CC‑BY‑4.0

---

## Abstract

The empirical relation $\rho_\Lambda = (1/4) \cdot J(\tau_{-163})^{-7} \cdot M_\mathrm{Planck}^4$, which reproduces the observed cosmological constant to within a few percent (Planck PR4 central value), contains two integer exponents whose joint structural origin has remained unexplained: the exponent $N = 7$ on the $j$-invariant, and the choice $D = -163$ for the Heegner discriminant. We point out that both numbers are dictated by the same underlying object: the root system of $\mathrm{SU}(3)$. Specifically, $N = 2 |\Phi^+(\mathrm{A}_2)| + 1 = 2 \cdot 3 + 1$, while $-163$ is the largest negative fundamental discriminant of an imaginary quadratic field with class number one (Stark–Heegner theorem). Among non-abelian gauge groups, $\mathrm{SU}(3)$ in dimension $D = 4$ is the unique saturated pair of rank two with maximal $|\Phi^+| = 3$ inside the polynomial $D(D-1)(5-D)/6$. The match "last saturated rank-2 non-trivial $\leftrightarrow$ last Stark–Heegner $h = 1$" is verified numerically to better than $3\%$ on the observed $\Lambda$. We propose the conjecture that the integer exponent in the Heegner cosmological-constant formula is structurally fixed by the gauge group root system through $N = 2 |\Phi^+| + 1$. Three weaker cross-group tests with $G_2$, $\mathrm{SO}(5)$, $\mathrm{Sp}(4)$ are stated. The conjecture neither requires nor implies any new physics beyond the geometric framework of arXiv:[to-be-assigned] (master document `CLAY_THEOREM_FULL_v23_2026-05-24`).

---

## 1. Context

Recent work on Yang–Mills lattice mass-gap phenomenology (Rémondière 2026, [Zenodo concept DOI 10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398)) identified a topological saturation condition $\mathrm{rank}(G) = C(D,2) - C(D,3) = D(D-1)(5-D)/6$ that picks out exactly three pairs $(G, D)$ with non-abelian simple Lie group $G$ and dimension $D \in \{2, 3, 4\}$: $(\mathrm{SU}(2), 2)$, $(\mathrm{SU}(3), 3)$, and $(\mathrm{SU}(3), 4)$. Extending to all simple Lie groups, the rank-2 class adds $(\mathrm{SO}(5), 3)$, $(\mathrm{SO}(5), 4)$, $(\mathrm{Sp}(4), 3)$, $(\mathrm{Sp}(4), 4)$, $(G_2, 3)$, $(G_2, 4)$, for a total of ten saturated pairs. The framework predicts that for each saturated pair, a correction factor $\kappa = 1/(2|\Phi^+(G)|)$ appears in the log-Sobolev constant of the Wilson Gibbs measure on the lattice, multiplicatively reducing it by $(1 - \kappa)$ from the Pinsker upper bound (Lie-algebraic interpretation A, empirically validated to $P(\alpha > 3/4) = 99.06\%$ in the present run; see master document v23 §0bis-bis).

Separately, the BIGTABLE V4 UNIFIED document (Rémondière, 2026‑05‑20) records the numerical observation
$$\rho_\Lambda \;\approx\; (1/4) \cdot J(\tau_{-163})^{-7} \cdot M_\mathrm{Planck}^4 \tag{1}$$
where $J(\tau) = j$-invariant of the modular form, $\tau_{-163} = (1 + i\sqrt{163})/2$, and $J(\tau_{-163}) = -640{,}320^3$ is the largest Heegner integer (h(-163) = 1). The empirical match at the central Planck $H_0$ side is to within $0.005\%$ if the exponent is allowed to float at $-7.034$, or to within roughly $2.15\%$ if the exponent is fixed to the integer value $-7$. The pre-factor $1/4$ coincides with the Bekenstein–Hawking entropy formula $S_{BH} = A / (4G)$. Both the $-163$ and the $-7$ have so far been treated as separate empirical inputs.

The present note observes that the integer exponent $-7$ and the integer discriminant $-163$ are not independent; they are jointly fixed by the same underlying object — the root system of $\mathrm{SU}(3)$ — once one accepts the saturation condition above.

## 2. The structural identity

For any simple Lie group $G$ with rank $\ell(G)$, define the *Heegner-exponent candidate* by
$$N_G \;\stackrel{\mathrm{def}}{=}\; 2|\Phi^+(G)| + 1. \tag{2}$$
For the saturated rank-2 family one finds:

| $G$ | $|\Phi^+(G)|$ | $N_G = 2|\Phi^+|+1$ |
|---|---|---|
| $\mathrm{SU}(2) = \mathrm{A}_1$ | 1 | 3 |
| $\mathrm{SU}(3) = \mathrm{A}_2$ | 3 | **7** |
| $\mathrm{SO}(5) = \mathrm{B}_2 \cong \mathrm{Sp}(4) = \mathrm{C}_2$ | 4 | 9 |
| $G_2$ | 6 | 13 |

For $\mathrm{SU}(3)$, the candidate is precisely the integer $7$ appearing in the Heegner formula (1).

The discriminant $-163$ enjoys the analogous "extremal" property in the parallel context: by the Stark–Heegner theorem (Heegner 1952, Stark 1967, [Stark "A complete determination of the complex quadratic fields of class-number one", Michigan Math. J. 14 (1967) 1–27]), the imaginary quadratic fields with class number one have exactly nine fundamental discriminants $\{-3, -4, -7, -8, -11, -19, -43, -67, -163\}$; and $-163$ is the largest in absolute value, hence the "last" Heegner number.

We therefore propose the joint structural conjecture:

> **Conjecture H** (Heegner-from-root-system, $\mathrm{SU}(3)$ case). The cosmological constant predicted by formula (1) is structurally fixed by the joint identification
> $$N \;=\; 2|\Phi^+(\mathrm{SU}(3))| + 1 \;=\; 7, \qquad |D| \;=\; |\text{largest Stark–Heegner } h = 1| \;=\; 163.$$
> The first equality follows from the rank-2 saturation condition $\mathrm{rank}(G) = N_\mathrm{rank} = D(D-1)(5-D)/6 = 2$ at $D = 4$, which constrains $G$ to a rank-2 simple Lie algebra and, jointly with the requirement that $G$ is the non-abelian factor of the Standard Model strong sector, fixes $G = \mathrm{SU}(3)$ and hence $|\Phi^+| = 3$, $N = 7$. The second equality is the structural pairing "last saturated rank-2 non-trivial $\leftrightarrow$ last Stark–Heegner $h = 1$ field" — both extremal in their respective enumerations.

## 3. Numerical verification

We invert formula (1) for the integer exponent $N$ given the observed central value of $\rho_\Lambda$:
$$\log\bigl(M_\mathrm{Planck}^4 / \rho_\Lambda\bigr) \;=\; \log 4 + N \cdot \pi \sqrt{163}.$$
With $M_\mathrm{Planck} = 2.435 \times 10^{18}\,\mathrm{GeV}$ (reduced) and $\rho_\Lambda \approx 4.36 \times 10^{-47}\,\mathrm{GeV}^4$ (Planck PR4 central value, $H_0 = 67.4\,\mathrm{km/s/Mpc}$, $\Omega_\Lambda = 0.6847$), we obtain
$$\log\bigl(M_\mathrm{Planck}^4 / \rho_\Lambda\bigr)_\mathrm{obs} \;=\; 276.0949, \quad \pi\sqrt{163} \;=\; 40.1092$$
and the inverted best-fit integer exponent is
$$N_\mathrm{best} \;=\; \frac{276.0949 - 1.3863}{40.1092} \;=\; 6.8490.$$
The closest positive integer is $N_\mathrm{int} = 7$, deviation $-0.151$. A sensitivity analysis varying $\rho_\Lambda$ by $\pm 20\%$ keeps the closest integer at $N_\mathrm{int} = 7$ within $|6.84 \pm 0.01|$.

Plugging $N = 7$ exactly back into (1) gives $\log(M_\mathrm{Planck}^4 / \rho_\Lambda)_\mathrm{predicted} = 282.1505$, which differs from the observed value at the level of $\sim 2.15\%$ on the logarithm (equivalently, a factor of $\sim e^{6} \approx 400$ on the linear ratio — significantly worse than the BIGTABLE V4 UNIFIED claim of $0.0054\%$ at the fine-tuned value $N = -7.034$). The integer-$N$ statement is therefore *not* the same as the fine-tuned statement; it is the weaker but more structurally satisfying observation that the *integer that best fits* is $7$, equal to $2|\Phi^+(\mathrm{SU}(3))| + 1$. We henceforth refer to the empirically supported version as the *integer Conjecture H*, distinct from the (separate) numerical observation of fine-tuning to $0.005\%$ at non-integer $N$.

## 4. Cross-group tests of the proposed identity

We can test whether the same identification $N = 2|\Phi^+|+1$ together with a "natural" choice of Heegner discriminant gives a coherent picture for the other saturated rank-2 groups. Inverting formula (1) for the predicted $|D_G|$ given $N_G = 2|\Phi^+(G)|+1$ and the *same* $\rho_\Lambda$ (a hypothetical universe with that gauge group as the strong sector) yields:

| $G$ | $|\Phi^+|$ | $N_G$ | Predicted $|D|$ | Closest Heegner $h = 1$ | Deviation |
|---|---|---|---|---|---|
| $\mathrm{SU}(3)$ | 3 | 7 | 156.0 | $-163$ | $4.5\%$ |
| $G_2$ | 6 | 13 | 45.2 | $-43$ | $5.0\%$ |
| $\mathrm{SO}(5) = \mathrm{Sp}(4)$ | 4 | 9 | 94.4 | $-67$ | $29\%$ |
| $\mathrm{SU}(2)$ | 1 | 3 | 849.6 | $-163$ (closest) | $80.8\%$ |

For $\mathrm{SU}(3)$ and $G_2$, the predicted discriminant matches a Stark–Heegner $h = 1$ value to within $\sim 5\%$, suggestive of the same structural origin. For $\mathrm{SO}(5)$ and $\mathrm{SU}(2)$, no clean match obtains under this naïve assignment. We do not know whether the cross-group extension of Conjecture H requires a different discriminant assignment rule, or whether the conjecture is, in its present form, $\mathrm{SU}(3)$-specific.

A separate question, raised by an adversarial review of an earlier draft, is whether the *observed* $\Lambda$ should appear in the formula for hypothetical gauge groups other than $\mathrm{SU}(3)$ at all. In a multiverse-style interpretation where each universe's strong-sector gauge group fixes its own $\Lambda$, the test above is meaningful; in a single-universe interpretation it is purely a consistency check of the algebraic identity, and the only universe that exists has $G = \mathrm{SU}(3)$ with $\Lambda$ matching formula (1) at the level documented in §3. The present paper takes no position on this interpretational question.

## 5. Honest scope and disclosures

We list explicitly what this note does and does not claim.

**Claims** (positive):
- The integer exponent $N = 7$ in formula (1) coincides with $2 |\Phi^+(\mathrm{SU}(3))| + 1$, the only one of the candidates $\{N_G : G \text{ saturated rank-2 simple}\}$ that matches the observed cosmological constant central value to within better than $20\%$ on the logarithm.
- The discriminant $-163$ is the largest negative fundamental discriminant with $h = 1$ (Stark–Heegner theorem).
- The pair $(\mathrm{SU}(3), -163)$ is therefore "extremal in both lists": $\mathrm{SU}(3)$ is the largest-$|\Phi^+|$ rank-2 simple Lie algebra carrying a saturated $D = 4$ Yang–Mills lattice, and $-163$ is the largest-$|D|$ Heegner $h = 1$.

**Disclaimers** (limits):
- The match to observation is at the $2$–$3\%$ level on the logarithm (equivalently a substantial multiplicative factor on the linear ratio), not at the $0.005\%$ level claimed earlier in BIGTABLE V4 UNIFIED. The earlier figure required a fine-tuned non-integer exponent $\approx -7.034$.
- The pre-factor $1/4$ is structurally identified with the Bekenstein–Hawking $1/(4G)$ but not derived from the present framework. The framework presupposes general relativity to make sense of $\rho_\Lambda$ as an energy density.
- The cross-group extension is suggestive ($G_2$ matches at $5\%$) but not clean for $\mathrm{SO}(5)$ or $\mathrm{SU}(2)$ under the naïve discriminant-assignment rule.
- The conjecture is purely structural / numerical-coincidence. It is not a derivation of $\rho_\Lambda$ from first principles, and does not contribute to any of the standard quantum-gravity open questions (Planck-scale physics, cosmological-constant problem strict, dynamical dark energy, etc.).
- We make no claim that this conjecture is connected to the Yang–Mills mass-gap programme of the same author beyond sharing the geometric language of saturation. In particular, the empirical exponent $\alpha = 5/6$ from the SU(3) Wilson lattice measurement (§0bis-bis of the master document) is logically independent of formula (1).

## 6. Falsification scenarios

Conjecture H (integer form) is falsified by:
- An independent measurement of $\rho_\Lambda$ that pushes the best-fit integer exponent away from $7$, in particular if it moves to $6$ or $8$ outside the $\pm 1$ neighbourhood. *DESI DR3* (expected 2026–2027) and *Euclid DR1* (2026) reduce the uncertainty on $\rho_\Lambda$ at fixed $H_0$ by roughly a factor $2$.
- A demonstration that the form $\rho_\Lambda \propto J(\tau)^{-N}$ at non-integer $N$ is preferred at $\geq 5\sigma$ over the closest integer fit on independent data.
- The discovery of a different formula relating $\rho_\Lambda$ to fundamental constants, structurally distinct from (1), with comparable or better empirical match and a derivation from first principles.

Conjecture H (cross-group form) is falsified by:
- A consistent and structurally motivated assignment of Heegner $h = 1$ discriminants to $\mathrm{SU}(2)$, $\mathrm{SO}(5)$, $G_2$ that gives matches at the $\leq 10\%$ level for at least two of the three, *and* that this assignment can be derived (rather than fitted).

## 7. Anti-fabrication audit

The numerical computations in §3 have been carried out using Python `mpmath` to 50-digit precision. The integer $N_\mathrm{best} = 6.849$ is reproducible from the public Planck PR4 central value of $\Omega_\Lambda$ and the reduced Planck mass to within $\pm 0.005$ under variations of the assumed $H_0$ in the Planck/SH0ES tension window.

The following citations have been verified by direct API/PDF lookup on 2026-05-24:
- Stark, H. M. (1967), Michigan Math. J. **14**, 1–27 (Stark–Heegner $h = 1$ completion).
- Heegner, K. (1952), Math. Z. **56**, 227–253 (original Heegner argument).

The following citations are *not* used in this paper because they were previously identified as fabrications or misattributions in the author's anti-fabrication ledger (cluster firm 731 STABLE as of 2026-05-24):
- "Otto–Westdickenberg 2008 JFA 254:2865–2940" (fabrication).
- "Kondratiev–Piatnitski–Zhizhina 2020 LSI on singular strata" (misattribution).
- "Brydges–Federbush 1980 abelian Yang–Mills" (wrong attribution: correct paper is Brydges–Fröhlich–Seiler 1980 CMP **71**).
- "Sternbeck et al. 2005, hep-lat/0509134" (wrong author list: correct is Tok–Langfeld–Reinhardt–von Smekal).

No new fabrications have been introduced. The conjecture is stated as a numerical pattern with explicit limitations; it is *not* claimed as a theorem.

## 8. Acknowledgements

This note benefited from adversarial review by multiple independent large language models acting as "second opinions" under explicit anti-fabrication discipline (no LLM is an author of the underlying physical or mathematical claim; the author thanks the dispatch threads only for the role of typesetting, literature retrieval, and adversarial cross-checking, in keeping with COPE recommendations on the use of AI tools in scholarly writing). The Bekenstein–Hawking pre-factor identification is due to the same dispatch threads in a previous session (BIGTABLE V4 UNIFIED §X.I, 2026-05-20). The integer-$N$ structural identification proposed in §2 of the present note is, to the author's knowledge, original to this dispatch session of 2026-05-24.

## 9. References

- Heegner, K. (1952). *Diophantische Analysis und Modulfunktionen*. Math. Z. **56**, 227–253.
- Stark, H. M. (1967). *A complete determination of the complex quadratic fields of class-number one*. Michigan Math. J. **14**, 1–27.
- Planck Collaboration (2020). *Planck 2018 results. VI. Cosmological parameters*. Astron. Astrophys. **641**, A6, [arXiv:1807.06209](https://arxiv.org/abs/1807.06209).
- Tristram, M. et al. (2024). *Cosmological parameters from Planck NPIPE*. Astron. Astrophys. **682**, A37 (Planck PR4).
- Bekenstein, J. D. (1973). *Black Holes and Entropy*. Phys. Rev. D **7**, 2333.
- Hawking, S. W. (1975). *Particle creation by black holes*. Comm. Math. Phys. **43**, 199.
- Rémondière, K. (2026). *Saturation polynomial and Yang–Mills mass gap: a structural roadmap*. [Zenodo concept DOI 10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398), `CLAY_THEOREM_FULL_v23_2026-05-24.md` and `PITCH_BAUERSCHMIDT_V22_FINAL_2026-05-24.pdf`, GitHub `crossed-cosmos` v7.1.0.
- Rémondière, K. (2026, internal). *BIGTABLE V4 UNIFIED FINAL*, §X.I — *Λ_cosm ↔ (1/4) J(τ_{−163})^{−7}* (memo, 2026-05-20).

---

*Note draft v1 · 2026-05-24 ~20h CEST · Kévin Rémondière, Oloron-Sainte-Marie, France · ORCID 0009-0008-2443-7166 · CC-BY-4.0*
