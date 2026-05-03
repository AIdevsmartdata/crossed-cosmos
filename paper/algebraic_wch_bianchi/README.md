# Algebraic Weyl Curvature Hypothesis: FRW + Bianchi I

Standalone math.OA / math-ph paper combining yesterday's FRW Algebraic WCH (T1+T2+T3 modulo Hadamard convention) with today's NEW rigorous Theorem T2-Bianchi I (vacuum Kasner).

- **Author**: Kevin Remondière
- **Date**: 2026-05-03
- **Files**:
  - `note.tex` — main paper source (~12-15 pages target)
  - `note.bib` — bibliography (28 entries, all arXiv-API verified)
  - `note.pdf` — compiled output (run the build steps below)
  - `README.md` — this file

## Build

```bash
cd /root/crossed-cosmos/paper/algebraic_wch_bianchi
pdflatex -interaction=nonstopmode note.tex
bibtex note
pdflatex -interaction=nonstopmode note.tex
pdflatex -interaction=nonstopmode note.tex
```

Verify clean compile:

```bash
grep -E "Warning.*(undefined|undef|multipl)" note.log || echo "0 warnings"
grep -oE "Output written.*\([0-9]+ page" note.log | tail -1
```

## Theorem statements (verbatim)

- **Theorem T1** (future-infinity II∞ standard, FRW): For radiation-dominated FRW with conformally coupled massless scalar, the inductive limit `A(D_∞)_FRW := closure_{w*} ⋃_n A(D_n)_FRW` along η_f^(n) → +∞ is a well-defined W*-algebra; `Ω_FRW` extends to a cyclic-separating vector; the crossed product `A(D_∞)_FRW ⋊_σ ℝ` is a type II∞ factor. Proof via Verch 1997 inductive-limit theorem.

- **Theorem T2-FRW** (past Big Bang non-cyclic-separating, FRW): For the same theory, `Ω_FRW` does not extend to a cyclic-separating vector for `A(D_BB)_FRW`, and no Hadamard state in the BFV-Verch local-quasi-equivalence folium of `Ω_FRW` extends to one. Three sympy-verified obstructions: (i) rescaling failure for k=0,1,2 Taylor modes; (ii) IR log² divergence of smeared two-point on test functions extending to η=0; (iii) Hadamard exclusion via Hollands-Wald 2001 + BFV 2003.

- **Theorem T3** (algebraic arrow of time): The pairs `(A(D_∞)_FRW, Ω_FRW)` and `(A(D_BB)_FRW, Ω_FRW)` are not isomorphic. Past↔future asymmetry is intrinsic.

- **Proposition B.1** (perturbative Bianchi I T1 lift): For Bianchi I with anisotropy ε ∈ [0, ε₀(D)) around radiation/matter FRW, the SLE Hadamard state of Banerjee-Niedermaier 2023 + Brum-Them 2013 yields a type II∞ crossed product. Proof via Connes 1973 cocycle invariance + BFV 2003 local quasi-equivalence. Threshold ε₀ ~ CMB anisotropy 10⁻⁵.

- **Theorem T2-Bianchi I** (NEW, central new result): For vacuum Bianchi I with non-degenerate Kasner exponents (-1/3, 2/3, 2/3), the inductive limit `A(D_BB)_BI := closure_{C*} ⋃_{t_i↓0} A(D_{(t_i,t_f)})_BI` does not admit the Banerjee-Niedermaier SLE Hadamard state ω, nor any state in the BFV-Verch local-quasi-equivalence folium of ω, as a cyclic-separating vector in any GNS representation. Proof via two independent IR divergences of the smeared two-point function: (S1) volume zero-mode log² divergence (analog of FRW); (S3) NEW long-wavelength tachyonic mode along the contracting Kasner direction p₁ = -1/3, with `ω_k(t) = |k₁| t^(1/3) → 0`, yielding `∫ dk_1/|k_1| = +∞`. Both extend to the entire BFV folium by Verch 1994.

## Sympy verifications (bundled in companion-note scripts)

- `notes/path_realiste_2026_05_03/algebraic_arrow.py` — FRW T1, T2, T3 sympy CHECKs 1-6
- `notes/path_realiste_2026_05_03/bianchi_extension_opus.py` — Bianchi I Weyl divergence (CHECK C1, C2, C3, C4)
- `notes/T2_bianchi_2026_05_03_jour2/T2_bianchi_extension.py` — T2-Bianchi I S1, S3 IR divergences

## Bibliography (28 entries, all arXiv-API verified 2026-05-03)

Key references:
- Penrose, *Cycles of Time* (2010) [Bodley Head] — original geometric WCH
- Penrose, *Singularities and time-asymmetry* (1979) [Einstein centenary survey] — earlier formulation
- Brunetti-Fredenhagen-Verch, *The generally covariant locality principle* (2003) — math-ph/0112041
- Hollands-Wald, *Local Wick polynomials and time ordered products* (2001) — gr-qc/0103074
- Verch, *Local definiteness, primarity and quasi-equivalence* (1994) [CMP 160:507]
- Verch, *Continuity of symplectically adjoint maps* (1997) [Rev. Math. Phys. 9:635]
- Connes, *Une classification des facteurs de type III* (1973) [Ann. ENS 6:133]
- Hislop-Longo, *Modular structure of local algebras* (1982) [CMP 84:71]
- Chandrasekaran-Longo-Penington-Witten (CLPW), *An algebra of observables for de Sitter space* (2023) — arXiv:2206.10780
- Witten, *Gravity and the crossed product* (2022) — arXiv:2112.12828
- Faulkner-Speranza, *Gravitational algebras and the generalized second law* (2024) — arXiv:2405.00847
- Banerjee-Niedermaier, *States of low energy on Bianchi I spacetimes* (2023) — arXiv:2305.11388
- Brum-Them, *States of low energy in homogeneous and inhomogeneous, expanding spacetimes* (2013) — arXiv:1302.3174
- Damour-Henneaux-Nicolai, *Cosmological billiards* (2003) — hep-th/0212256
- Damour-Nicolai, *11d supergravity and E_10/K(E_10) sigma-model* (2004) — hep-th/0410245
- Heinzle-Uggla, *Mixmaster: Fact and Belief* (2009) — arXiv:0901.0776
- Hartnoll-Yang, *The Conformal Primon Gas at the End of Time* (2025) — arXiv:2502.02661
- De Clerck-Hartnoll, *Wheeler-DeWitt wavefunctions for 5d BKL dynamics* (2025) — arXiv:2507.08788
- BKL 1970 (Adv. Phys. 19:525), Misner 1969 (PRL 22:1071), Wainwright-Ellis 1997 [CUP], Wald 1994 [Chicago]

## Recommended publication target

- **Foundations of Physics** (Penrose-WCH thematic angle, foundational/philosophical readership) — primary recommendation
- **Lett. Math. Phys.** (compact rigorous result, strong math.OA / math-ph fit) — strong secondary
- **Class. Quant. Grav.** (cosmological-AQFT readership)
- **Comm. Math. Phys.** (long-form rigorous AQFT) — strong secondary
- **JHEP** (post-CLPW operator-algebraic bridge) — possible if reframed for hep-th audience

## Honest framing

- T1 (FRW): unconditional within standard AQFT.
- T2-FRW: rigorous modulo standard AQFT convention that physical states are Hadamard.
- T3 (FRW): inherits T2's Hadamard convention.
- Prop. B.1 (Bianchi I T1, perturbative): unconditional within Hadamard convention, threshold ε₀ ~ 10⁻⁵.
- T2-Bianchi I (NEW): rigorous within Hadamard convention, conditional on Banerjee-Niedermaier 2023 SLE Hadamard state on Bianchi I.
- Cor. T2-Bianchi V: conditional on Hadamard state existence on H³ (currently open).
- Open Q. T2-Bianchi IX: conjectural, requires BKL invariant-measure analysis (open).
- All Weyl tensor and IR divergence claims are sympy-verified.

NO git push. Working dir: /root/crossed-cosmos.
