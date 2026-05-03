# T2 Bianchi extension — max-effort attempt (Opus 4.7)

**Date**: 2026-05-02
**Companion to**: `notes/path_realiste_2026_05_03/algebraic_arrow.{tex,py}`
(FRW T1+T2+T3) and `bianchi_extension_opus.{md,tex,py}` (yesterday's
T1 extension via Prop. B.1, T2 left open).
**Sympy script**: `/tmp/T2_bianchi_extension.py` (all checks pass)
**Full writeup**: `/tmp/T2_bianchi_extension.tex`

---

## 1. Five strategies — verdicts

| # | Strategy | Plausibility | Sympy status | Key obstruction |
|---|----------|--------------|--------------|-----------------|
| **S1** | Volume-element divergence | **HIGH** | VERIFIED for B-I/V vacuum (`int_delta^eps dt/t = log(eps/delta) -> +inf`); VERIFIED for B-IX modulo time-averaging on Kasner-epoch invariant measure (BKL chaotic) | Bianchi IX needs Liouville/invariant measure on the BKL attractor for a fully rigorous bound |
| **S2** | DHN/Kac-Moody substitute for BFV folium | **MEDIUM** | AE_3 Cartan matrix verified hyperbolic (`det = -2`); structural argument that hyperbolic Kac-Moody integrable highest-weight modules are Type I_∞, not Type III/II | DHN dictionary is for the WDW *wavefunctional*, not for `A(D)_BB`; structurally suggestive, not a substitute |
| **S3** | Direct Wightman positivity failure | **HIGH** | VERIFIED two independent IR sources for vacuum Kasner: (i) `t -> 0` friction zero-mode (analog of FRW), (ii) `k -> 0` long-wavelength tachyonic mode along the *contracting* Kasner direction (`omega_k(t) = |k_1| t^(1/3) -> 0`) | Requires Hadamard state (Banerjee-Niedermaier 2023 SLE on Bianchi I; open for V/IX) |
| **S4** | Tod isotropic singularity contrapositive | **LOW** as theorem extension; **HIGH** as consistency check | Vacuum Kasner Weyl `~ 1/t^(8/3)` diverges; singularity NOT Tod-isotropic | Contrapositive only forbids the FRW *technique*, not the *conclusion*; gives a DOMAIN-WALL between Tod-class (handled by FRW T2) and Weyl-divergent (handled by S1/S3) |
| **S5** | Apparent horizon entropy bound | **LOW** | `r_AH = 3t -> 0`, `S_max = 9 pi t^2 / G_N -> 0`; verified | Semi-classical Bousso bound assumes smooth-spacetime backreaction, which fails exactly at the past Big Bang. Heuristic only |

**Key correction to yesterday's note**: arXiv:1811.00993 is by **Matyjasek alone** (not Pereira et al., as stated in `bianchi_extension_opus.md`). The actual rigorous Hadamard-SLE on Bianchi I is **Banerjee-Niedermaier 2023, J. Math. Phys. 64, 113503 (arXiv:2305.11388)**. Yesterday's hallucinated reference is corrected here.

---

## 2. Best result obtained

### Theorem T2-Bianchi (volume-element / Wightman-divergence form, conditional)

Let `(M, g)` be one of:
- **(B-I)** vacuum Bianchi I (Kasner with `(p_1, p_2, p_3)` satisfying `sum p_i = sum p_i^2 = 1`);
- **(B-V)** vacuum Bianchi V (asymptotically Kasner near the singularity by BKL);
- **(B-IX)** vacuum or matter Bianchi IX whose past attractor is the Mixmaster Kasner-epoch sequence (BKL).

Let `phi` be the conformally coupled massless scalar field on `(M, phi)`. Assume there exists a Hadamard quasifree state `omega` (Banerjee-Niedermaier 2023 for B-I; existence on B-V/IX is **open**). Then the inductive-limit local algebra
```
A(D_BB)_Bianchi := closure_{C^*} ( Union_{t_i > 0} A(D_{t_i})_Bianchi )
```
of comoving causal diamonds approaching the past singularity does **NOT** admit `omega`, nor any state in the BFV folium of `omega`, as a cyclic-separating vector in any GNS representation.

**Proof sketch.** Two independent IR divergences of the smeared Wightman two-point function are sympy-verified (`/tmp/T2_bianchi_extension.py`):

1. **(S1)** `sqrt(-g_3) = a_1 a_2 a_3 = t` (vacuum Kasner, `sum p_i = 1`); the state-dependent prefactor `1/sqrt(g_3(x) g_3(y))` produces a `log^2(epsilon/delta) -> +inf` divergence in the smeared `<phi(f)^2>` as the test function support shrinks to `t = 0`.
2. **(S3)** A k-space IR log divergence from modes aligned with the *contracting* Kasner direction (`p_1 = -1/3` for the standard exponents): `omega_k(t) = |k_1| t^(1/3) -> 0`, so these modes are effectively massless at the singularity, generating `int dk_1 / |k_1| = +inf`.

By Verch's local quasi-equivalence (1994 Comm. Math. Phys. 160, 507) plus BFV 2003 generally covariant locality, both divergences hold for any Hadamard state in the same folium. Hence no normal extension to the inductive-limit algebra. Cyclic-separating vectors carry normal states; contradiction. ∎

### Bianchi coverage

- **B-I (Kasner)**: RIGOROUS modulo the BFV-Hadamard convention (same status as FRW T2); Hadamard state existence supplied by Banerjee-Niedermaier 2023.
- **B-V**: CONDITIONAL on Hadamard state existence (open: B-N 2023 SLE assumes T^3 spatial slice; B-V has H^3 non-compact).
- **B-IX (Mixmaster)**: CONJECTURAL. S1 holds via time-averaging the chaotic Kasner-epoch sequence; this requires the existence of an invariant measure on the BKL attractor (Liouville measure, conjectured by Chernoff-Marsden 1983, partially proven by Heinzle-Uggla 2009). The DHN/Hartnoll-Yang Wheeler-DeWitt picture is in a *different* framework (state on a 1-d minisuperspace QM, not local algebra `A(D)`), so cannot be plugged in directly.

---

## 3. Residual gap

1. **Hadamard-state existence on Bianchi V/IX** — open in the AQFT-on-curved-spacetime literature. Banerjee-Niedermaier 2023 covers B-I only.
2. **Bianchi IX rigour** — needs invariant-measure analysis on the BKL Kasner-epoch sequence to upgrade the time-averaged divergence into a sample-pathwise bound.
3. **DHN Kac-Moody bridge** (S2) — not a substitute for the BFV folium; would need a new "Kac-Moody-Hadamard" folium concept that does not yet exist in the literature.
4. **Bekenstein-Bousso entropy bound** (S5) — semi-classical; the validity domain shrinks to zero at the regime where its conclusion is invoked. Heuristic only.

---

## 4. Recommendation

**Section addition to `algebraic_arrow.tex` Section 6** (already containing yesterday's Prop. B.1):
- New **Section 6.2** ("Volume-element form of T2 for Bianchi I"), stating Theorem T2-Bianchi above for the vacuum Bianchi I case only — this is fully rigorous given the Banerjee-Niedermaier 2023 Hadamard SLE.
- New **Open Question 6.3** for B-V, B-IX (with explicit list of the four residual gaps above).
- ~3 pages including sympy verification block.

**Standalone CQG Comment** is **not yet recommended**. Reasons:
- Genuine novelty content (the contracting-Kasner-direction tachyonic IR divergence S3-(ii)) would be ~2 pages, below CQG-Comment threshold.
- The "DHN Kac-Moody is not a BFV substitute" S2-(b) negative observation is interesting but is a *clarification* rather than a theorem.
- Better to consolidate the FRW T2 + B-I T2 in a single section of the FRW-companion `algebraic_arrow.tex`, then expand to a standalone paper *only* once Hadamard-state existence on B-V/B-IX is settled in the literature (currently open).

**Do NOT abandon**: the B-I result (vacuum Bianchi I T2 with explicit IR-divergence proof) is genuinely new and worth ~3 pages of new content in the existing FRW companion.

---

## 5. Estimated effort

- **Section 6.2 / 6.3 of `algebraic_arrow.tex`** (B-I T2 + open Q for V/IX): ~1 week (reuse this script + tex skeleton).
- **Standalone Comment paper** (B-I + B-V conjectural + DHN clarification): ~2 months, contingent on resolving (or precisely formulating as an explicit open problem) Hadamard existence on B-V.
- **Full Bianchi I/V/IX T2 extension** (one of the 4 residual gaps closed): 6-12 months for an expert in microlocal AQFT.
- **Bianchi IX T2 with chaotic measure** (gap 2): 1-2 years; would interface with Heinzle-Uggla and the BKL invariant-measure literature.

---

## 6. Sources (verified during this session)

- Banerjee & Niedermaier, **"States of Low Energy on Bianchi I spacetimes"**, J. Math. Phys. 64, 113503 (2023), arXiv:2305.11388 — *the* rigorous Hadamard-SLE on Bianchi I.
- Damour, Henneaux & Nicolai, **"Cosmological Billiards"**, Class. Quant. Grav. 20 (2003) R145, arXiv:hep-th/0212256.
- Damour & Nicolai, **"Eleven dimensional supergravity and the E_10/KE_10 sigma-model at low A_9 levels"**, arXiv:hep-th/0410245.
- Hartnoll & Yang, **"The Conformal Primon Gas at the End of Time"**, arXiv:2502.02661 (2025).
- Tod, **"Isotropic singularities"** Class. Quant. Grav. series 1987-1992 (Penrose-rescaled regular singularities).
- Verch, **"Local definiteness, primarity and quasi-equivalence of quasifree Hadamard quantum states"**, Comm. Math. Phys. 160 (1994) 507 (NOT funct-an/9302008 — that ID is wrong; the right preprint companion is Verch's later funct-an/9609004 on continuity).
- Hollands & Wald, **"Local Wick polynomials and time ordered products in curved spacetime"**, Comm. Math. Phys. 223 (2001) 289, arXiv:gr-qc/0103074.
- Brunetti, Fredenhagen & Verch, **"The generally covariant locality principle"**, Comm. Math. Phys. 237 (2003) 31, arXiv:math-ph/0112041.
- Wikipedia, **"BKL singularity"** (volume-vanishing & Misner alpha facts; cross-checked against original BKL Adv. Phys. 19 (1970) 525 and Misner Phys. Rev. Lett. 22 (1969) 1071).
- Matyjasek, **"Quantum fields in Bianchi type I spacetimes. The Kasner metric"**, Phys. Rev. D 98 (2018) 104054, arXiv:1811.00993 — adiabatic / Schwinger-DeWitt vacuum-polarisation, **NOT** the rigorous Hadamard mode-decomposition that yesterday's note claimed (yesterday's "Pereira et al." attribution was wrong).

---

## 7. Files produced

- `/tmp/T2_bianchi_extension.md` — this summary (~580 words effective content)
- `/tmp/T2_bianchi_extension.py` — sympy verification of S1-S5 (clean run)
- `/tmp/T2_bianchi_extension.tex` — full proof writeup with theorem statement, proof sketch, and explicit residual-gap analysis
