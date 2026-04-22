# observer_frame_map.md — Team B re-reading of A4/A5/A6

For each observable the table gives: (a) the "absolute" reading used in the
current v4.6 body of the paper, (b) the "observer-dependent" reading that
Hypothesis B would substitute, (c) the concrete change required in the
corresponding phenomenology subsection.

---

## A4 — NMC quintessence sector (ξ_χ, χ₀, α)

| Aspect | Absolute reading (v4.6) | Observer-dependent reading (B) | Change in §3.5 / §3.7 |
|---|---|---|---|
| ξ_χ | Single Lagrangian coupling, global. Cassini bound \|ξ_χ\|(χ₀/M_P) ≤ 2.4×10⁻³ constrains **the** ξ_χ. | Frame-labelled ξ_χ^(R): the coupling that appears in the graviton kinetic matrix of the observer's crossed-product algebra. Cassini constrains the solar-system-frame value only. | §3.5 caveat: rename "ξ_χ" → "ξ_χ at the solar-system QRF" once; note that a cosmological-frame value inferred from DR3/LSST Y10 w_a need not coincide. No numerical change at the current null-result level. |
| χ₀ fiducial | M_P/10, single value shared by §3.5/§3.6/§3.7 (PRINCIPLES #13). | Observer-frame field excursion: the χ amplitude seen from the comoving-Hubble-diamond clock. Different QRFs see different χ₀. | §3.5 Caveat 2 re-worded: the χ₀ = M_P/10 fiducial is the late-universe-observer's reduced-Planck-scaled thawing excursion; it is not a global field value. D9's χ₀-nonlinearity becomes a frame-spread, not an error bar. |
| α (exponential slope) | Global Lagrangian parameter, α < √2 for acceleration. | Effectively global at late times (quasi-dS limit); but the attractor criterion α<√2 is itself a statement about the observer's static-patch-asymptote. | No numerical change in §3.3. Add one sentence: "α<√2 is the attractor criterion in the late-time static-patch limit." |
| G_eff/η perturbation signature | |Δfσ₈/fσ₈| ≤ 0.4%: universal, below Euclid reach. | Same bound but interpreted as the LSST-observer-frame signature; a different QRF would see the same ratio with ξ_χ^(R) substituted. | §3.7 unchanged numerically. Verdict "null-result at forecast precision" holds frame-by-frame. |

## A5 — Dark Dimension species cutoff (c', ℓ, KK tower)

| Aspect | Absolute reading (v4.6) | Observer-dependent reading (B) | Change in §3.6 |
|---|---|---|---|
| c' = 1/6 | Species-scale exponent of Montero–Vafa–Valenzuela, applied universally. | Slope of Λ_sp(H) inferred in the causal diamond of a late-time geodesic observer; asymptotes to 1/6 in the static-patch limit. | §3.6 primary text unchanged at the arithmetic level. Add one sentence to Caveat 1: "c'=1/6 is the slope seen by the late-time static-patch observer; matter-era QRFs are not covered." |
| ℓ ∈ [0.1, 10] μm | Single extra-dimensional length. | Effective ℓ is a property of the KK tower visible to the diamond; same in the quasi-dS limit. | No change at v4.6 precision; flag at the §3.6 structural-result level. |
| Shared-cutoff hypothesis → \|ξ_χ\| ≤ 8.4×10⁻¹⁹ | Heuristic δM_P² ≤ Λ² applied globally; structural result. | The heuristic bound constrains (ξ_χ^(R), c'^(R)) in a single observer's frame; cross-observer consistency requires the additional assumption that χ is a genuinely bulk mode in **every** QRF. Resolution (i) — χ decoupled — becomes frame-independent automatically; Resolution (ii) — screening — becomes "screening in the solar-system frame only". | §3.6 Resolutions (i)–(iii) gain a one-sentence frame qualifier. No number changes. The structural conclusion ("model-building must pick one of (i)–(iii)") is unchanged. |
| N_eff = 2.86 ± 0.13 | ACT DR6 constraint, global. | Matter-era quantity; NOT covered by Hypothesis B. | ACT/BBN-era statements stay as in v4.6. Flag in §3.6 footnote that the N_eff constraint is observer-independent only insofar as the matter-era QRF extension is assumed. |

## A6 — Persistent homology diagnostic (PH_k, χ_E)

| Aspect | Absolute reading (v4.6) | Observer-dependent reading (B) | Change in A6 prose / §3 predictions |
|---|---|---|---|
| χ_E Euler-characteristic shift | Matsubara 2003 ensemble average over all observer frames. | Single-observer χ_E on a density field restricted to that observer's causal diamond; Matsubara is the frame-averaged expectation. | A6 prose: one sentence clarifying the Matsubara form as a frame average. Prediction 2 unchanged. |
| PH_k refinement (Yip 2024, Calles 2025) | Claimed as finer f_NL estimator than bispectrum. | Finer in the single-observer sample; whether it remains finer under frame-averaging is an open question (D5 SCAFFOLD). | No change to axiom statement, but the "PH_k is a finer estimator" claim picks up an honest "single-observer" qualifier consistent with PRINCIPLES #12 (no claim larger than derivation supports). |
| CMB-S4 / LiteBIRD forecast | f_NL^loc ∈ [1, 5] via PH_k, 2030+. | Same forecast; CMB-S4 and LiteBIRD are effectively single-observer (ours) instruments, so the frame-averaging subtlety is moot at the phenomenology level. | Prediction 2 unchanged. |

---

## Meta: what Hypothesis B does NOT change

- §3.1 DESI DR2 central values, Mahalanobis 3.29σ / 3.33σ / 4.36σ.
- §3.2 f_EDE = 0.09 ± 0.03 (pre-recombination — outside B's defensible scope).
- §3.3 α<√2 attractor arithmetic (reinterpreted, not re-derived).
- §3.4 DM KK candidate phenomenology.
- §4 prediction table numerics.

## Meta: what Hypothesis B DOES change (prose-level only)

- A one-paragraph §1.5 "Unifying hypothesis (B)" block, replacing no existing axiom.
- Frame qualifiers in §3.5 Caveat 2, §3.6 Caveat 1, §3.7 intro, A6 prose.
- An explicit statement in "Structural limitations" item 2: "The QRF functor is
  not rigorously extended to generic FLRW; Hypothesis B is defensible only in
  the late-time quasi-de-Sitter limit (Ω_Λ ≳ 0.7), which is where DESI DR2,
  Cassini, and LSST Y10 operate."
