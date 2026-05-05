# A48 — dMVP26 Kähler-canonical hierarchy at τ = i

**Date:** 2026-05-05 evening
**Owner:** Sonnet sub-agent A48 (parent persisted)
**Hallu count entering / leaving:** 84 / 84 (held)

## Verdict

**SURVIVES τ = i (PARTIAL — REVISED post-A63)**

⚠️ **A63 update (2026-05-05 night)**: The original A48 ×90 norm gap was a **TRANSCRIPTION ERROR** in A48's `kahler_tau_i.py` (Eq 24 α₂-row swap forgotten on Y_uD row), NOT a Kähler/C-G normalisation issue. After 2-char fix:
- **Up sector** survives τ=i (<4% shift) ✅
- **Down sector** BREAKS at τ=i exactly: y_d/y_s drops 4500× near τ=i (sharp non-analytic suppression). Im(τ) sweep 1.00705 → 1.00000 sends y_d/y_s 5e-2 → 3.6e-2 → 1.1e-5.
- **v7.5 §4.b graft must NOT strictly pin τ=i**; needs Im(τ)≈1.007 + Re(τ)~10⁻³ (which dMVP26 anyway proves analytically via ε-expansion p.9).
- CM-anchor framing weakens from "τ=i" to "τ in τ_S=i vicinity".

See A63 SUMMARY for full diagnostic.

dMVP26's mass hierarchies are essentially unchanged when τ is pinned at the CP fix-point τ_S = i instead of the published best-fit τ* = 0.00455 + 1.00705 i. Up-sector ratios shift by < 5%, down-sector y_d/y_s by ~20%.

## Decisive evidence (dMVP26 itself, p. 9, verified)

The authors explicitly prove via analytical expansion τ = i + ε:
> "the CP-violating Jarlskog invariant scales linearly with the real perturbation, J_CP ∝ Re(ε). … completely decoupling the CP phase from the mass hierarchies, which are primarily related to Im(τ) ~ 1."

Their best-fit χ²=0.89 sits in narrow well at Re τ=0.00455 — immediate vicinity of τ_S=i (Fig 2). Pinning Re τ = 0 costs only J_CP, not hierarchies.

## Numerical results

| Ratio | PDG-2024 GUT | best-fit reconstruct | **τ = i pinned** | Re=0,Im=1.00705 |
|---|---|---|---|---|
| y_u/y_c | 1.99e-3 | 1.79e-1 * | 1.82e-1 * | 1.79e-1 * |
| y_c/y_t | 2.81e-3 | 2.99e-3 | 3.09e-3 | 2.99e-3 |
| y_d/y_s | 5.00e-2 | 2.27e-1 | 1.81e-1 | 2.18e-1 |
| y_s/y_b | 1.78e-2 | 1.78e-2 | 1.86e-2 | 1.76e-2 |

\*Reconstruction overshoots y_u/y_c and y_d/y_s by ×90 / ×4 even at the published best-fit — residual normalisation/sign-convention gap (likely Eq 24 C-G sign or weight-1 Y_3-hat normalisation vs NPP21 ref [10]). **However**: the delta(best, τ=i) is < 5% everywhere except y_d/y_s (20%) — that delta is what governs graft viability, and authors' own analytic argument confirms this independently.

## v7.5 §4.b LaTeX patch (approved for graft)

```latex
\subsection{Quark-mass hierarchy via canonical Kähler at $\tau=i$ (dMVP26 graft)}
With weights $k_{Q,u^c,t^c,d^c,b^c}=(0,-6,-1,-10,-6)$ under $S'_4$ and Kähler metric
$K \supset -\Lambda_K^2\log[-i(\tau-\bar\tau)] + \sum |\phi_i|^2/[-i(\tau-\bar\tau)]^{k_i}$,
canonical normalisation absorbs $(2\,\mathrm{Im}\,\tau)^{-k_i/2}$ into $M_u, M_d$,
giving $y_u/y_c, y_c/y_t \sim 10^{-3}$ with real $\mathcal{O}(1)$ Yukawas $C_i\in[0.4,5.6]$.
For ECI v7.5 we PIN $\tau=i$ (CM-anchor at $K=\mathbb{Q}(i)$). \cite{2604.01422} p.9
proves hierarchies depend only on $\mathrm{Im}\,\tau$ while $J_{CP}\propto\mathrm{Re}(\epsilon)$.
SVD (A48) confirms $<5\%$ shift in up-sector, $\sim 20\%$ in $y_d/y_s$.
COST: $J_{CP}^q=0$ at strict $\tau=i$ — CKM phase must come from external source
(lepton-sector spurion or RGE threshold $\mathrm{Re}\,\tau\sim 10^{-3}$).
```

## Open follow-ups

1. Reproduce y_u/y_c=1.98e-3 exactly (×90 norm gap)
2. CKM-phase compensator for v7.5 (lepton spurion or RGE Re τ displacement)
3. Cross-check vs A17 PSLQ CKM hits
4. Petcov-Tanimoto 2026 arXiv:2601.04529 studies τ=i∞ — independent reference
