# H4 Literature Scan — 2026-Q2
**Agent:** H4 | **Date:** 2026-05-04 | **Budget:** 60 min

---

## H4.A — Modular Flow ↔ RG Flow Papers (2024–2026)

**Summary finding:** After exhaustive search (arXiv API, WebSearch, direct abstract checks), NO paper in 2024–2026 proves or even explicitly claims that Tomita-Takesaki modular flow on a type-II crossed product algebra *is* Wilsonian RG flow. The connection remains completely open in the published literature. The closest papers establish adjacent infrastructure (type-II algebras from crossed products; holographic RG; timelike entanglement entropy as RG probe) but do not forge the specific bridge ECI v7 envisions.

| arXiv ID | Date | Title (short) | Claim re modular-RG | Cites FS 2306.01837 | Cites DEHK 2412.15502 |
|---|---|---|---|---|---|
| 2405.00847 | 2024-05-01 | Faulkner-Speranza: *Gravitational algebras and the generalized second law* | Modular flow geometric on Killing horizons → GSL via crossed-product; **no RG connection** | — (is the paper) | Not cited (predates) |
| 2412.15502 | 2024-12-20 | De Vuyst, Eccles, Hoehn, Kirklin: *Crossed products and QRFs: observer-dependence of gravitational entropy* | Type-III → type-II via observer inclusion; **no RG claim** | Yes | — (is the paper) |
| 2402.18655 | 2024-02-28 | Gao: *Modular flow in JT gravity and entanglement wedge reconstruction* | Type-II∞ algebra; modular flow = boost near RT surface; **no RG claim** | Unknown | Unknown |
| 2312.08534 | 2023-12-13 (pub. 2024-05) | Grieninger-Ikeda-Kharzeev: *Temporal Entanglement Entropy as probe of RG Flow* | Coarse-graining via Euclidean time trace → RG flow proxy; **no modular flow (TT) language** | No | No |
| 2512.16499 | 2025-12-18 | Giataganas: *Timelike Entanglement Entropy and RG Flow Irreversibility* | Timelike c-function captures irreversible RG; **no type-II or modular flow language** | No | No |

**Obstruction note:** The key structural gap is that Wilsonian RG is a semigroup (UV→IR coarse-graining, no inverse), while Tomita-Takesaki modular automorphisms form a one-parameter *group* (reversible). Any identification requires breaking this mismatch, e.g., by analytic continuation or restricting to the KMS-positive half-line. No 2024–2026 paper addresses this obstruction.

**Specific searches yielding zero results:**
- "modular flow as renormalization" — 0 hep-th hits
- "modular RG" + type II — 0 hits
- Bousso "modular Hamiltonian" + "renormalization group" 2024–2025 — 0 hits
- Lashkari + "renormalization" + modular flow 2024–2025 — closest is 2019 paper

---

## H4.B — Wolf-NMC Follow-ups Since April 2025

**Context:** Wolf et al. arXiv:2504.07679 (v3 revised 2025-07-28) finds log B = 7.34 ± 0.6 for NMC over minimal coupling, favoring ξ(φ/M_Pl)² ~ 0.1 cosmologically but generating fifth forces excluded by Cassini (γ-bound: ξ(φ₀/M_Pl)² ≤ 6×10⁻⁶). The Wolf paper concludes NMC quintessence requires new small-scale physics or is unlikely.

| arXiv ID | Date | Title (short) | Finding | Impact on ECI |
|---|---|---|---|---|
| 2508.01759 | 2025-08-03 (v5: 2026-04-28) | Wang, Cai, Guo, S.-J. Wang: *Resolving Planck-DESI tension by NMC quintessence* | NMC dark matter–gravity coupling preferred >3σ; resolves Ωm tension; uses dilaton coupling (swampland-compatible) | Confirms NMC cosmological signal; does NOT address fifth-force tension |
| 2509.13302 | 2025-09-16 | Adam, Hertzberg, Jiménez-Aguilar, Khan: *Comparing minimal/NMC quintessence to 2025 DESI data* | Only "very narrow range" of NMC coupling evades fifth-force bounds; generic ξ excluded | **Constraining for ECI**: Wolf's ξ=2.31 likely in excluded generic range |
| 2510.14941 | 2025-10-16 | Sánchez López, Karam, Hazra: *NMC Quintessence in light of DESI* | log B = 5.52 vs ΛCDM (CMB+DESI+DES Y5); Palatini marginally better than metric; negative ξ for stable de Sitter | Partially confirms Wolf signal; Palatini formulation reduces fifth-force severity |
| 2604.16226 | 2026-04-17 | Karam, Sánchez López, Terente Díaz: *Post-Newtonian Constraints on Scalar-Tensor Gravity* | Palatini NMC satisfies significantly weaker local bounds due to Yukawa suppression; Palatini f(R̂) reproduces GR exterior PPN limit | **Key result for ECI**: Palatini loophole may rescue ξ>0 NMC quintessence from Cassini bound |
| 2604.02204 | 2026-04-02 | Wang, Cai, Guo, Li, S.-J. Wang, Zhang: *NMC quintessence with sign-switching interaction* | Sign-change in dark energy–dark matter coupling; late-universe dark energy weakening; DESI-motivated | Structural variant; does not resolve fifth-force issue |

**Hu et al. 2508.01759 verification:** CONFIRMED — this is "Resolving the Planck-DESI tension by nonminimally coupled quintessence" (Wang, Cai, Guo, S.-J. Wang). The paper was updated to v5 on 2026-04-28 and is published in Phys. Rev. D. The title in the original H4 brief slightly misstated it as "NMC > 3σ" — the actual claim is NMC dark matter coupling preferred >3σ, not a 3σ detection of the Wolf ξ parameter specifically.

**ξ = 2.31 status:** None of the post-Wolf papers verified by abstract test ξ = 2.31 explicitly. Sánchez López et al. 2510.14941 report negative ξ for stable de Sitter, inconsistent with Wolf's positive ξ = 2.31 in the metric formulation. Hertzberg et al. 2509.13302 find generic NMC values are excluded by fifth forces — this directly challenges Wolf's favored value unless Palatini or screening applies.

**Bayesian landscape (DESI DR2):** The broader Bayesian analysis (arXiv:2603.05472) finds that DESI DR2 + Planck alone yields log B = −0.57 for w₀wₐCDM vs ΛCDM, i.e., ΛCDM modestly favored when Occam's razor applies. NMC models with extra parameters face this penalty. The Palatini NMC (2510.14941, log B = 5.52) does better but uses CMB+DESI+DES Y5 combination.

**Vainshtein/screening note:** No 2025–2026 paper was found offering a Vainshtein-screening bypass specific to the Wolf NMC quintessence model that would change the local-gravity bound on ξ. The Karam et al. 2604.16226 Palatini result is the closest: it shows Palatini gravity inherently suppresses fifth forces without invoking additional screening mechanisms.

---

## H4.C — Atkin-Lehner Sanity Check

**Question:** Does W₄ (or W₈) on a weight-5, level-4 (or level-8) newform preserve Hecke eigenvalues T(p) for p coprime to 4 (or 8)?

**Standard result (Diamond-Shurman §5.6, Atkin-Lehner theory):** The Atkin-Lehner operator W_Q on S_k(Γ₀(N)) commutes with T(p) for all primes p not dividing Q. For a newform f of level N with trivial character, W_N acts as a scalar ±1 (the Fricke involution), and for Hall divisors Q | N with Q coprime to N/Q, W_Q commutes with T(p) for gcd(p, Q) = 1. Critically: **the T(p)-eigenvalue of W_Q(f) equals the T(p)-eigenvalue of f** for p coprime to Q, but W_Q(f) may be a *different* newform (with character conjugated). For level 4 or 8 (where the only Hall divisors are the level itself), W₄ on a level-4 newform maps it to another newform (possibly itself) with the same Hecke eigenvalues at primes p not dividing 4, i.e., all odd primes.

**Implication for ECI 2̂(5) search:** If the target sequence (18, 178, −126, −1422, 530) at primes (5, 13, 17, 29, 37) belongs to a level-4 or level-8 weight-5 newform, the Atkin-Lehner image W₄(f) or W₈(f) carries the **same eigenvalues** at all these primes (all coprime to 4 and 8). So if G1.6's LMFDB search misses the form under one Atkin-Lehner sign, the same form exists with the opposite Fricke sign at the same level. The search should check both AL-eigenvalue signs (±1) for level 4 and both signs for level 8.

---

## New BibTeX Entries (for eci.bib v6.0.48)

```bibtex
@article{DeVuyst:2024lip,
  author       = {De Vuyst, Julian and Eccles, Stefan and Hoehn, Philipp A. and Kirklin, Josh},
  title        = {Crossed products and quantum reference frames: on the observer-dependence of gravitational entropy},
  year         = {2024},
  eprint       = {2412.15502},
  archivePrefix = {arXiv},
  primaryClass = {hep-th},
  note         = {v3: 2025-07-08. Type-III→type-II via observer inclusion; observer-dependent entropy.}
}

@article{Wang:2025nmc,
  author       = {Wang, Jia-Qi and Cai, Rong-Gen and Guo, Zong-Kuan and Wang, Shao-Jiang},
  title        = {Resolving the {Planck-DESI} tension by nonminimally coupled quintessence},
  year         = {2025},
  eprint       = {2508.01759},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO},
  journal      = {Phys. Rev. D},
  doi          = {10.1103/r6cx-8ghz},
  note         = {v5: 2026-04-28. NMC dark-matter coupling >3σ preferred; resolves Ω_m tension.}
}

@article{SanchezLopez:2025desi,
  author       = {S\'anchez L\'opez, Samuel and Karam, Alexandros and Hazra, Dhiraj Kumar},
  title        = {Non-minimally coupled quintessence in light of {DESI}},
  year         = {2025},
  eprint       = {2510.14941},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO},
  note         = {Palatini formulation; log B = 5.52 vs ΛCDM; CMB+DESI+DES Y5. Negative ξ preferred.}
}

@article{Karam:2026pn,
  author       = {Karam, Alexandros and S\'anchez L\'opez, Samuel and Terente D\'iaz, Jos\'e Jaime},
  title        = {Post-{Newtonian} constraints on scalar-tensor gravity},
  year         = {2026},
  eprint       = {2604.16226},
  archivePrefix = {arXiv},
  primaryClass = {gr-qc},
  note         = {Palatini NMC satisfies much weaker local bounds than metric NMC (Yukawa suppression); Palatini f(R) reproduces GR PPN exterior.}
}

@article{Adam:2025nmcdesi,
  author       = {Adam, Husam and Hertzberg, Mark P. and Jim\'enez-Aguilar, Daniel and Khan, Iman},
  title        = {Comparing minimal and non-minimal quintessence models to 2025 {DESI} data},
  year         = {2025},
  eprint       = {2509.13302},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO},
  note         = {Only narrow ξ range evades fifth-force bounds; generic NMC excluded.}
}
```

---

## Should ECI v7 Worry About Being Scooped on the Modular-RG Bridge?

**Verdict: No, not yet — but act within 12 months.**

The 2024–2026 literature establishes rich infrastructure on both sides of the bridge (type-II algebras from crossed products: DEHK 2412.15502, Faulkner-Speranza 2405.00847; holographic RG: Dong-Marolf-Rath 2509.21438, dual holography FRG 2511.05786) but no paper has explicitly identified Tomita-Takesaki modular flow with Wilsonian RG flow, even in a conjectural or analogical sense. The Casini-Huerta entanglement entropy / c-theorem programme (2018, Dirac Medal 2024) is adjacent but uses entanglement entropy as a probe of RG, not modular flow as a generator. The key structural obstruction — that modular flow is a group whereas Wilsonian RG is a semigroup — is not addressed by any 2025–2026 paper, suggesting the community has not yet attempted this identification seriously. ECI v7 therefore has a genuine originality window. However, the crossed-product/type-II gravity literature is growing fast (multiple papers per month in 2025), and the connection to KMS states is well-known to experts. A focused group could produce a preprint on the modular-RG bridge in 6–12 months without knowing about ECI. Recommendation: ECI v7 should make the modular-RG bridge claim explicit and publish at least a preprint on this specific sub-claim before end of 2026, or risk being anticipated.
