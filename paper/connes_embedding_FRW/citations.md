# Citation chain for "FRW past-light-cone type II_infty factor is hyperfinite (= R_{0,1})"

All references arXiv-API or DOI verified on 2026-05-03. Paranoid check: 28 hallucinations
caught in this project to date — every entry below has a sourced URL/DOI.

## Structural chain (the spine of the note)

    BFV 2003 (gen. cov. locality) ─┐
                                   │
    Verch 1994 CMP 160 ────────────┼──> A_FRW(D) is type III_1 with universal
    (local quasi-equiv. of           │     folium (Hadamard rep'ns)
     Hadamard quasifree states)      │
                                   │
    BDF 1987 CMP 111  ─────────────┤
    (universal struct. of local      │  + Fewster 2015 (split property in
     algebras → unique hyperfinite   │     curved spacetime via nuclearity)
     III_1 in scaling-limit setting) │
                                   ▼
    Frw_note Thm 3.5/3.6:  A_FRW(D) is hyperfinite type III_1
                                   │
                                   │  (modular flow, Tomita–Takesaki;
    Witten 2022 (2112.12828) ──────┤   intertwined with Hislop–Longo via
    CLPW 2022 (2206.10780) ────────┤   conformal pullback in frw_note)
                                   ▼
                A_FRW(D) ⋊_σ R is type II_∞
                                   │
                                   │  (modular crossed product of a
    Connes–Takesaki 1977 ──────────┤   hyperfinite III_1 factor by R is
    (Tôhoku 29, 473–575)             │   the unique hyperfinite II_∞ = R_{0,1};
                                   │   classification of injective factors)
                                   ▼
                A_FRW(D) ⋊_σ R ≅ R_{0,1}

The hyperfiniteness pass-through (BDF 1987 + Fewster 2015) is the load-bearing
arrow that the FRW note did not establish but which is folklore in AQFT;
making it explicit is the entire point of this companion note.

## Verified primary references

### Pre-arXiv (DOI / journal verified)

| Tag | Reference | Verification |
|---|---|---|
| `ConnesTakesaki1977` | A. Connes, M. Takesaki, "The flow of weights on factors of type III", Tôhoku Math. J. **29** (1977), 473–575. DOI 10.2748/tmj/1178240493 | Project Euclid: https://projecteuclid.org/euclid.tmj/1178240493 |
| `Verch1994` | R. Verch, "Local definiteness, primarity and quasiequivalence of quasifree Hadamard quantum states in curved spacetime", Comm. Math. Phys. **160** (1994), 507–536. DOI 10.1007/BF02173427 | Project Euclid cmp/1104269708; Springer DOI; ADS 1994CMaPh.160..507V |
| `BDF1987` | D. Buchholz, C. D'Antoni, K. Fredenhagen, "The universal structure of local algebras", Comm. Math. Phys. **111** (1987), 123–135. DOI 10.1007/BF01239019 | Project Euclid cmp/1104159470; Springer DOI |
| `BisognanoWichmann1975` | J. Bisognano, E. Wichmann, J. Math. Phys. **16** (1975), 985–1007. DOI 10.1063/1.522605 | (already in frw_note.bib) |
| `BisognanoWichmann1976` | J. Bisognano, E. Wichmann, J. Math. Phys. **17** (1976), 303–321. DOI 10.1063/1.522898 | (already in frw_note.bib) |
| `HislopLongo1982` | P. Hislop, R. Longo, Comm. Math. Phys. **84** (1982), 71–85. DOI 10.1007/BF01208372 | (already in frw_note.bib) |

### arXiv-verified

| Tag | arXiv | Title / Journal | API check |
|---|---|---|---|
| `BFV2003` | math-ph/0112041 | Brunetti–Fredenhagen–Verch, "The generally covariant locality principle…", CMP 237 (2003) 31–68 | totalResults=1, primary math-ph |
| `HollandsWald2001` | gr-qc/0103074 | Hollands–Wald, "Local Wick polynomials…", CMP 223 (2001) 289–326 | totalResults=1, primary gr-qc |
| `Witten2022` | 2112.12828 | Witten, "Gravity and the Crossed Product", JHEP 10(2022) 008 | totalResults=1, primary hep-th |
| `CLPW2023` | 2206.10780 | Chandrasekaran–Longo–Penington–Witten, "An Algebra of Observables for de Sitter Space", JHEP 02(2023) 082 | totalResults=1, primary hep-th |
| `BuchholzVerch1995` | hep-th/9501063 | Buchholz–Verch, "Scaling Algebras and Renormalization Group in AQFT", Rev. Math. Phys. 7 (1995) 1195 | totalResults=1, primary hep-th |
| `Verch1997` | funct-an/9609004 | Verch, "Continuity of symplectically adjoint maps…", Rev. Math. Phys. 9 (1997) 635–674 | totalResults=1, primary math.FA |
| `Fewster2015Split` | 1501.02682 | Fewster, "The split property for locally covariant QFT in curved spacetime", Lett. Math. Phys. 105 (2015) 1633–1661 | totalResults=1, primary math-ph |
| `JNVWY2020` | 2001.04383 | Ji–Natarajan–Vidick–Wright–Yuen, "MIP*=RE" | totalResults=1, primary quant-ph |
| `Witten2022WhyQFT` | 2112.11614 | Witten, "Why does QFT in curved spacetime make sense?…" | totalResults=1, primary hep-th |

## Caveats / corrections from the user prompt

1. **"Schroer 1989" not used.** The user prompt suggested Schroer 1989 as an
   alternative source for hyperfiniteness of Hadamard local algebras; arXiv +
   web search returned no specific 1989 Schroer reference matching that
   description. The canonical Minkowski-space result is BDF 1987
   (CMP 111, 123–135). For the curved-spacetime extension we cite Verch 1994 +
   Fewster 2015 + BDF 1987. **Schroer 1989 is not in the bibliography of this
   note** to avoid a probable hallucinated citation.

2. **"Buchholz–Verch 1995"** is the scaling-algebra paper hep-th/9501063 — it
   discusses scaling limits and short-distance structure but does **not** by
   itself prove "Hadamard local algebras on curved spacetime are
   hyperfinite". The actual hyperfiniteness chain we use is:
   (a) BDF 1987 → Minkowski local algebras are R⊗center;
   (b) Verch 1994 → all quasifree Hadamard reps in curved spacetime are
       locally quasi-equivalent on a relatively compact O, so the W^*-type
       and hyperfiniteness are folium invariants;
   (c) Fewster 2015 → split property holds in the locally covariant setting
       under nuclearity, which together with (a)+(b) yields hyperfiniteness
       for the local algebras of Hadamard reps on globally hyperbolic
       spacetimes admitting nuclearity.

3. **"Connes–Takesaki 1977 → uniqueness"** is correct as stated *modulo*
   Connes' 1976 classification of injective II_∞ factors (Ann. Math. 104,
   73–115). The injectivity/AFD coincidence (Connes 1976) is what makes
   "the modular crossed product of an AFD III_1 by R" automatically AFD II_∞.
   We cite both. (Connes 1976 not separately listed above; it appears in the
   note as `Connes1976`.)

4. **Separability.** Connes–Takesaki / Connes 1976 uniqueness assumes
   separable predual. The Hadamard GNS Hilbert space H_FRW is separable for
   the conformally coupled massless scalar on a globally hyperbolic spacetime
   with second-countable topology (standard; see e.g. Wald 1994 §4 for the
   structure of the one-particle Hilbert space). No separability subtlety.
