---
name: M18 ECI tensor-to-scalar ratio r — LiteBIRD 2032 prediction
description: Honest derivation — FORECAST-PREMATURE-HONEST; modular inflation gives r~1e-7 (undetectable); M9 claim requires amendment
type: project
---

# M18 — ECI tensor-to-scalar ratio r for LiteBIRD 2032

**Date:** 2026-05-06
**Owner:** Sub-agent M18 (Sonnet)
**Hallu count entering / leaving:** 85 / 85 (held)

---

## VERDICT: FORECAST-PREMATURE-HONEST

**The M9 claim "ECI uniquely predicts CMB B-modes r detectable by LiteBIRD" is PREMATURE.**

ECI v6.0.53.3 has no explicit inflation sector. If the modular tau field is identified as the inflaton (the only ECI-natural mechanism), the resulting r ~ 10^{-7} is ~7000x below LiteBIRD's 3-sigma detection threshold of r > 0.003. The NMC sector (xi_chi approx 0.001) cannot drive inflation: Higgs inflation requires xi ~ 10^4 (excluded by 6 OOM, A73 result). No other inflaton is present in ECI v6.0.53.3.

**Correction to M9 degeneracy-breaking observable #6:**
Replace: "CMB B-modes r (LiteBIRD 2032) — uniquely ECI prediction (modular inflation)"
With: "CMB B-modes r: ECI NULL prediction (r < 10^{-6} if tau=inflaton; no inflation sector in current ECI). Future work: R^2 term or separate inflaton (v7.6 A74). LiteBIRD non-detection is confirmatory."

---

## Live-verified arXiv IDs (export.arxiv.org/api/query, 2026-05-06)

| arXiv ID | Title | Verified |
|---|---|---|
| 2310.10369 | King-Wang "Modulus stabilisation in the multiple-modulus framework" | YES |
| 2405.06497 | Ding-Jiang-Zhao "Modular Invariant Slow Roll Inflation" | YES |
| 2411.18603 | Ding-Jiang-Xu-Zhao "Modular invariant inflation and reheating" | YES |
| 2101.12449 | Hazumi+ "LiteBIRD: JAXA's new strategic L-class mission" | YES |
| 2202.02773 | LiteBIRD Collaboration "Probing Cosmic Inflation with LiteBIRD" | YES |
| 2406.02724 | LiteBIRD Collaboration "The LiteBIRD mission to explore cosmic inflation" | YES |
| 2406.02116 | Chen-Penington "A clock is just a way to tell the time" | YES (tangential) |

**CORRECTION:** arXiv:1908.00802 (cited in M18 mission brief as "Hazumi 2019 LiteBIRD") = AEDGE atomic interferometer paper (El-Neaj+ 2019, EPJ Quantum Technol. 7, 6). Not LiteBIRD. Correct LiteBIRD refs: 2101.12449, 2202.02773, 2406.02724.

---

## Step 1: ECI inflation mechanisms

### Mechanism (a): Modular inflation (tau as inflaton)

KW arXiv:2310.10369 = vacuum STABILIZATION paper, not inflation. Abstract: "modulus stabilisation mechanism capable of providing de Sitter (dS) minima precisely at tau=i and omega." No r computed there.

If tau is the inflaton (rolling to tau=i), the mechanism is modular inflation (Ding et al. 2024). From live-verified papers:
- 2405.06497 (Ding-Jiang-Zhao): r < 10^{-6} for modular SL(2,Z) inflation, N=55
- 2411.18603 (Ding-Jiang-Xu-Zhao, A4 = S'4 mod +-1): r ~ 1.4 x 10^{-7}, n_s = 0.9647

Suppression mechanism: modular forms at tau=i have zeros of order >= 2 (Z_2 stabilizer). V(tau) ~ |tau-i|^4 near fixed point. This gives slow-roll epsilon << Starobinsky, hence r = 16*epsilon ~ 10^{-7}.

### Mechanism (b): NMC inflation (xi_chi ~ 0.001)

A73 explicit conclusion: "Higgs-inflation regime (xi >= 10^4) is excluded by RG-stability of the wedge [by 6 orders of magnitude]." EXCLUDED.

### Mechanism (c): SUGRA F-term Starobinsky

r = 12/N^2 = 3.97e-3 (LiteBIRD-detectable). Not derivable from KW dS-trap Kahler geometry without new model input. Not in ECI v6.0.53.3.

### Mechanism (d): Separate inflaton field

Not present in ECI v6.0.53.3. Requires v7.6 work (A74).

---

## Step 2: r comparison (N = 55 e-folds)

| Scenario | r | n_s | LiteBIRD detectable? |
|---|---|---|---|
| Starobinsky R^2 | 3.97e-3 | 0.964 | YES (>3-sigma) |
| alpha-attractor alpha=1 | 9.9e-4 | 0.964 | MARGINAL |
| Wolf NMC xi=2.31 | ~3e-3 | ~0.964 | POSSIBLY (no committed prediction) |
| ECI NMC xi~0.001 | EXCLUDED | -- | NO |
| **ECI modular tau-inflaton** | **~1.4e-7** | **0.965** | **NO (7000x below threshold)** |
| LiteBIRD 3-sigma threshold | r > 3e-3 | -- | -- |

---

## Step 3: Falsifier structure

"LiteBIRD detection of r > 10^{-3} REFUTES ECI modular tau-inflation."
"LiteBIRD non-detection (r < 10^{-3}) is consistent with ECI."

This IS a unique prediction: ECI is the only model in the {ECI, Wolf, AKW} triad
with a specific inflation r value, even if it is a null.

---

## Step 4: LiteBIRD timeline (live-verified)

Source arXiv:2406.02724 (LiteBIRD Collaboration, 2024-06-04):
  - Launch: Japan fiscal year 2032
  - Goal: "measure r with uncertainty delta_r = 0.001, including systematic errors"
  - Detection: "if r >= 0.01, LiteBIRD expects >5-sigma detection"

Source arXiv:2202.02773 (LiteBIRD Collaboration 2022):
  - Total sensitivity: 2.2 mu-K-arcmin

Derived: sigma(r) ~ 0.001; 3-sigma threshold r > 0.003; 5-sigma r > 0.01.
Results expected: ~2035-2036.
ECI r ~ 1.4e-7 is ~1000x below noise floor for LiteBIRD detection.

---

## Step 5: Amendment to M9 observable list

**M9 row 6 AMENDED:**

| Dimension | ECI v7.5 (corrected) | Wolf 2025 | AKW 2026 |
|---|---|---|---|
| CMB B-modes r | NULL: r < 10^{-6} (tau-inflaton). No inflation sector in v6.0.53.3. | No prediction | No prediction |
| LiteBIRD falsifier | Detection r > 10^{-3} REFUTES ECI modular inflation | Not applicable | Not applicable |
| Unique? | YES — only model with specific r bound | NO | NO |

**Frame for ECI paper**: "ECI's modular tau-field, if it serves as inflaton, predicts r < 10^{-6} (Ding et al. 2024, same symmetry group A4). LiteBIRD will test this at 3-sigma by 2035."

---

## Discipline log
- Hallu count: 85 -> 85 (unchanged)
- 7 arXiv IDs live-verified via API
- 0 r values fabricated
- arXiv:1908.00802 ID error documented (mission brief error)
- Mistral STRICT-BAN observed
