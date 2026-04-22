# ECI v4.5 — AI Peer Pre-Review v2 (3-model frontier triangulation)

**Date:** 2026-04-21
**Target:** `paper/eci.pdf` (framework genre, EPJ C target), v4.4.0 + v4.5 A3-dictionary landed
**Reviewers (1min.ai aggregator, non-reasoning tier):**
- OpenAI **GPT-5.4** (substituted from `gpt-5.4-pro` — pro tier cost 1.26M credits, exceeded team balance)
- Google **Gemini 3.1 Pro** (`gemini-3.1-pro-preview`)
- xAI **Grok 4** (`grok-4-0709`)

Identical prompt (4 EPJ C referee questions), full LaTeX source concatenated (eci.tex + §3.5 + §3.6 + §5-A3), 45.5 KB.
Supersedes v1 (Claude self + Gemini CLI + Magistral-medium). Per-reviewer markdown under `paper/_peer_review_v2/<model>.md`; raw JSON under `raw/`.

---

## Reviewer 1 — OpenAI GPT-5.4

**Q1 (weakest).** A3-based cosmological "toy dictionary" — specifically the "Big Bang as decodability boundary" and "inflation as algebraic necessity" narrative. Notes the author's honesty but argues honesty ≠ strength: an AdS/CFT theorem transplanted into FLRW/dS with no reconstruction map. The proposed observable proxy ε ~ 10⁻⁵ from CMB anisotropy is "hand-waving, not a derived bridge between modular pseudorandomness and cosmological perturbations."

**Q2 (strongest).** The *negative* result: within the Cassini PPN range, the NMC correction to the thawing (w₀, w_a) track is too small to distinguish ECI from minimal thawing at DR2 precision. Concrete, quantitatively bounded, derivation-backed — "the rare part that behaves like physics." Δw_a ~ 10⁻² tied to PPN bounds.

**Q3.** **MAJOR REVISIONS.** "Overclaims unity where it mostly delivers juxtaposition." The A4/A5 cross-constraint rests on a heuristic δM_P² ≲ Λ² not derived in controlled EFT matching; A3 cosmology remains conjectural and should be quarantined from the predictive core. Publishable at EPJ C if restructured: hard core (NMC/PPN/(w₀,w_a) + species-scale arithmetic + DR2 non-discrimination admission) vs speculative appendix.

**Q4.** Full Jordan-frame linear perturbation calculation for ξ_χ R χ²/2 giving G_eff(k,a), η(k,a), f σ₈(z) shift to first order in ξ_χ at Cassini-saturated ξ_χ — a clean yes/no falsifier **independent** of the admitted DR2 (w₀,w_a) failure.

---

## Reviewer 2 — Google Gemini 3.1 Pro

**Q1 (weakest).** Cosmological transposition of A3 (Cryptographic Censorship) to Big Bang + inflation. AdS/CFT theorem mapped onto pseudo-Riemannian dS/FLRW without a valid boundary-to-bulk dictionary; no pseudo-Riemannian analogue for one-sided modular reconstruction. "Big Bang as decodability boundary" and "inflation as algebraic necessity" are narrative extrapolations.

**Q2 (strongest).** §3.6 Swampland × NMC cross-constraint. Forcing the Dark Dimension species-scale cutoff (A5) against NMC quintessence (A4) drives |ξ_χ| ≲ 10⁻¹⁹ — proves the NMC signature is observationally dead in the DE sector absent screening or brane-localized zero-mode. A rigid architecture of mutual restriction.

**Q3.** **MAJOR REVISIONS.** Framework genre acceptable, DESI-Dark-Dimension synthesis genuinely interesting, but currently "speculative manifesto." The §3.5 w_a phenomenology is incomplete without establishing that the (ξ_χ, α, f_EDE, z_c) prior can actually fit current data. A3 toy-dictionary implications must be heavily dialed back — they dilute the rigorous scalar-tensor physics of §3.5 / §3.6.

**Q4.** Explicitly derive the minimum screening potential (chameleon/symmetron) profile required to decouple local χ₀ from the cosmological background (Resolution ii of §3.6) — quantify the local-density threshold to evade the Swampland-EFT bound. Converts vague loophole into hard testable parameter space.

---

## Reviewer 3 — xAI Grok 4

**Q1 (weakest).** A3 as selection rule on admissible bulk geometries in a cosmological setting — explicitly conjectural extrapolation from AdS/CFT without proven dS/FLRW transposition. Crossed-product algebras and pseudorandom unitaries are motivational, not proof. All downstream A3 uses (decodability boundary, inflation-as-necessity) inherit this fragility.

**Q2 (strongest).** Hubble-tension reduction to ~2σ via EDE with f_EDE = 0.09 ± 0.03. Directly synthesizes Poulin-Smith 2026 + Calabrese 2025 across ACT DR6 + DR2 + Planck + Pantheon+, with falsifiable prediction f_EDE ∈ [0.06, 0.12] for SO + SPT-3G. Empirically grounded, no new physics beyond synthesis.

**Q3.** **MAJOR REVISIONS.** "Intriguing architectural synthesis" fit for framework genre with clear falsifiable tests, but over-reliance on A3's cosmological extension, incomplete analytics (deferred NMC w_a), and missing quantitative DR2 MCMC fit. Wants: full Bayesian on (ξ_χ, α, f_EDE, z_c), explicit w_a(w₀; ξ_χ) at first order, stronger A3 evidence or caveats, clearer A4+A5 resolution choice.

**Q4.** Compute the full analytic first-order closed form for w_a(w₀; ξ_χ) in the NMC thawing regime (building on the deferred derivations/w0-wa-nmc companion) as a closed-form discriminator between ECI and wCDM inside the DR2 band, without numerical reliance. Sharpens Prediction 1 for DR3 at σ(w_a) ~ 0.07.

---

## Synthesis table

| Q | GPT-5.4 | Gemini 3.1 Pro | Grok 4 | Convergence |
|---|---|---|---|---|
| **Q1 weakest** | A3 toy-dictionary + ε~10⁻⁵ CMB proxy hand-waved | A3 cosmological transposition (no pseudo-Riemannian modular-reconstruction analogue) | A3 as bulk-geometry selection rule (conjectural, motivational only) | **3/3 UNANIMOUS**: A3 / §5 toy-dictionary |
| **Q2 strongest** | §3.5 negative result — NMC indistinguishable from minimal thawing at DR2 precision (Δw_a ~ 10⁻²) | §3.6 Swampland × NMC cross-constraint (ξ_χ ≲ 10⁻¹⁹) | EDE Hubble-tension reduction to ~2σ (f_EDE = 0.09 ± 0.03) | **3 different picks** — all inside §3.5 / §3.6 / §EDE technical block, but no single consensus strongest |
| **Q3 recommendation** | MAJOR REVISIONS | MAJOR REVISIONS | MAJOR REVISIONS | **3/3 UNANIMOUS**: MAJOR REVISIONS |
| **Q4 calculation** | Jordan-frame first-order perturbation → G_eff, η, fσ₈ at saturated ξ_χ | Minimum screening profile (chameleon/symmetron) to fulfil §3.6 Resolution (ii) | Closed-form w_a(w₀; ξ_χ) first-order analytic, replacing deferred numerical | **3 distinct, complementary** — all target §3.5/§3.6 falsifiability, no duplicates |

**Publication vote:** GPT-5.4 = MAJOR. Gemini 3.1 Pro = MAJOR. Grok 4 = MAJOR. **3/3 MAJOR REVISIONS.**

---

## Convergent findings

- **Weakest (3/3):** A3 / §5 "toy dictionary" is the single weakest point of the manuscript across **every** frontier family (OpenAI, Google, xAI). The v4.5 decision to add §5 rather than demote A3 is *not* rescuing it in reviewer perception — all three explicitly reject the dS/FLRW transposition as insufficient. Two of three (GPT, Gemini) name-check "Big Bang as decodability boundary" and "inflation as algebraic necessity" as narrative, not physics.
- **Strongest (split 1+1+1):** no single consensus. But the three picks all fall inside the §3.5 + §3.6 + EDE-§3 technical block, confirming this is the predictive core. The *negative* / *constraint* framing wins over positive predictions (GPT: NMC-below-DR2-precision; Gemini: ξ_χ ≲ 10⁻¹⁹ kills NMC in DE; Grok: EDE narrows H₀ to 2σ).
- **Verdict (3/3):** MAJOR REVISIONS. No reviewer recommends outright rejection; no reviewer recommends MINOR. The paper sits clearly in "framework genre, revisions needed" regime.

## Top 2 deduped Q4 recommendations for v4.6

1. **Closed-form NMC perturbation / Klein–Gordon output** (merges GPT-Q4 + Grok-Q4): a first-order analytic expression for w_a(w₀; ξ_χ) **and** the induced G_eff(k,a), η(k,a), fσ₈(z) shift at Cassini-saturated ξ_χ. Replaces the heuristic B(Ω_Λ) and the deferred `derivations/w0-wa-nmc`. This was also the v1 Gemini+Magistral convergent ask — reappears under two models in v2.
2. **Screening-profile minimum for §3.6 Resolution (ii)** (Gemini-Q4, orthogonal): explicit chameleon/symmetron profile and local-density threshold that decouples local χ₀ from cosmology and evades the Swampland-EFT bound |ξ_χ| ≲ 10⁻¹⁹. Converts the three-way resolution tree into a hard testable parameter space.

## Comparison to v1 (Claude + Gemini 2.5 CLI + Magistral-medium)

| Axis | v1 | v2 | Flip / confirm |
|---|---|---|---|
| Q1 weakest | A3 cosmological transposition (3/3) | A3 toy-dictionary / §5 (3/3) | **CONFIRMED** — v4.5 adding §5 did not remove the weakness; reviewers now explicitly critique the toy dictionary itself, not just its absence |
| Q2 strongest | §3.5 NMC (2/3), §3.6 Swampland (1/3) | §3.5 negative / §3.6 10⁻¹⁹ / EDE — 1/1/1 split | **NEW**: EDE-§3 now appears as strongest pick (Grok). §3.6 10⁻¹⁹ bound confirmed headline-grade by Gemini (again). GPT reframes strength as the *honest negative* in §3.5. |
| Q3 vote | 3/3 MAJOR | 3/3 MAJOR | **CONFIRMED** |
| Q4 ask | NMC-KG numerical integration for B(Ω_Λ) (2/3) + joint (ξ, f_EDE) χ² grid (1/3) | Jordan-frame first-order perturbation + closed-form w_a(w₀; ξ_χ) + screening profile | **EVOLVED**: v1 asked for numerical B(Ω_Λ); v2 asks for analytic closed-form + perturbation-level observables + screening threshold. Higher technical bar than v1. |

**Key flip:** v1 treated A3 as "demote or add toy dictionary." v4.5 chose Option Y (add toy dictionary). v2 verdict: **the toy dictionary is itself the weakest claim** — it did not rescue A3, it just made the weak step more visible. Decision point for v4.6: either deliver a rigorous dS/FLRW modular-reconstruction analogue, or quarantine §5 to a clearly-labelled speculative appendix.

**Key confirmation:** §3.6 Swampland × NMC cross-constraint (16-orders-of-magnitude tension → ξ_χ ≲ 10⁻¹⁹) stays flagged as headline-grade across two v1+v2 passes.

**Key new finding:** Grok 4 elevates EDE Hubble-tension reduction to "strongest" — no v1 reviewer picked this. The concrete f_EDE ∈ [0.06, 0.12] SO+SPT-3G forecast is re-legitimised as a first-class predictive anchor.

---

## Credit cost (1min.ai team wallet, measured)

| Model | Input tokens | Output tokens | Credits |
|---|---:|---:|---:|
| GPT-5.4 | 20 087 | 633 | 179 138 |
| Gemini 3.1 Pro (preview) | 21 677 | 633 | 152 850 |
| Grok 4 | 19 004 | 606 | 198 306 |
| **Total** | **60 768** | **1 872** | **530 294** |

Team balance: 100 000 000 credits → pass consumed **0.53 %** of budget. Well under the 1% target. (GPT-5.4-Pro would have cost ~1.26M alone → substitution necessary.)

**Commit SHA:** (filled at commit time)
