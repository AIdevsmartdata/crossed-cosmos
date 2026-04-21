# Self-audit review log

This file records the internal technical reviews performed before each release. The goal is anti-fragility: we list the weak points *publicly* in the repository, so any external reviewer starts from a shared baseline rather than re-discovering them.

---

## 2026-04-21 — v4.0.1 pre-release review (reviewer-persona LLM, Opus)

### Section 2 — Equations

- Action, Klein–Gordon, $T_{\mu\nu}^{(\chi)}$, no-ghost condition: **no sign or dimensional error detected** in the Faraoni convention (cross-checked against Faraoni 2000 Éq. 1.1, 2.7–2.13; Birrell–Davies 1982 Éq. 3.190).
- Subtlety on the interpretation of $-\xi G_{\mu\nu} \chi^2$ transferred to the RHS: flagged; the convention choice will be made fully explicit in v4.1 with a dedicated paragraph.
- `derivations/` folder scaffolded to hold the symbolic re-derivations (D1–D6).

### Axioms A1–A6 — architectural coherence

- **A1 → A2** (observer-dependent algebra feeds the generalised entropy in Jacobson's derivation) : strong dependency. Non-perturbative GSL (Faulkner–Speranza 2024, Kirklin 2025) holds in the settings analysed, but extending it to non-stationary FLRW is not established.
- **A3 (Cryptographic Censorship)** : original theorem is AdS/CFT only. Transposition to dS or FLRW is conjectural. **Action taken: downgraded in `paper/eci.tex` from "axiom" to "working conjecture" with an explicit caveat block.**
- **A6 (persistent-homology complexity)** : motivated but not derived. A numerical benchmark comparing $\mathrm{PH}_k$ discrimination vs standard bispectrum on non-Gaussian mock catalogues would close this gap (planned in `tda/`, v4.2).

### Predictions (Section 4)

- **#1 $(w_0, w_a)$ band** : as written, encompasses both ECI and wCDM. **Action taken: explicit note in Section 3.1 that the analytic $w_a(w_0; \xi_\chi)$ relation must be computed before claiming discrimination**. Companion file: `derivations/D4-wa-w0-nmc.ipynb`.
- **#2 $f_{\mathrm{NL}} \in [1, 5]$ via $\mathrm{PH}_k$** : falsifies single-field slow-roll only. Reworded as such internally; v4.1 will clarify.
- **#5 $\dot\alpha/\alpha$** : is a limit, not a prediction. To be re-expressed as "ECI-consistent with optical-clock bound" rather than "ECI predicts".
- **#7 $r < 10^{-3}$** : too generic (most slow-roll models comply). To be re-expressed as a correlated signature $(r, n_s, \mathrm{PH}_k)$.

### Companion-paper scope

- The JEPA / EBM / modular-flow bridge drafted for v3 is **kept out** of the core framework paper. Mixing a structural analogy with peer-reviewable physics weakens both. A standalone companion paper (*"Modular flow and free-energy minimisation: a structural dictionary"*) is on the roadmap.

### Bibliography

- 28 entries in `paper/eci.bib`. 15 critical refs spot-verified via Crossref REST API on 2026-04-21:
  - 4 v3 author-attribution errors corrected (`Bedroya2025`, `WangPiao2025`; two spurious "Shiu–Cole" entries removed).
  - 4 short APS DOIs (2503.14738, 2504.07679, 2503.19898, 2505.08051) resolve correctly with matching titles.
  - Biskupek 2021 (Universe 7(2) 34) confirmed, including the $\dot G/G$ constraint.
  - Calabrese et al. ACT DR6 (arXiv:2503.14454) confirmed with $N_{\mathrm{eff}} = 2.86 \pm 0.13$.
- Remaining 13 entries: verified at the arXiv-abstract level only (title + authors). Full Crossref sweep scheduled for v4.1 — see `bib-check/` once added.

### Outstanding known weak points (explicitly acknowledged)

1. No MCMC fit to DESI DR2 yet. Framework-level paper only. Target: v4.1 to include at least a minimal Cobaya + CLASS + NMC-patch PoC.
2. A3 cosmological extension is unproved.
3. A6 discrimination against bispectrum is not quantified.
4. Dark Dimension $\Delta N_{\mathrm{eff}}(c', \ell)$ inequality against ACT DR6 is stated, not yet computed in `numerics/N2`.

These are work items, not showstoppers, for a framework paper.

---

## Template for future reviews

```markdown
## YYYY-MM-DD — v4.x pre-release review

### Equations
- [findings]

### Axioms
- [findings]

### Predictions
- [findings]

### Bibliography
- [findings]

### Outstanding weak points
- [findings]
```
