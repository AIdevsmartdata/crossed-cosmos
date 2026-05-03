# Residual gaps and structural implications

## What this note actually proves vs. claims

**Proves cleanly:** If you accept the FRW companion note's Theorem 3.5/3.6
(i.e. you accept the conformal pullback identifying A_FRW(D) with the
Minkowski diamond algebra), then `M_FRW(D) = R_{0,1}` follows by routine
W*-algebra concatenation (BDF 1987 + Connes 1976 + Connes-Takesaki 1977).

**Does not prove (gaps left open):**

1. **Massive / non-conformal Hadamard local algebras on FRW are AFD.**
   Beyond the conformal pullback regime, hyperfiniteness of A_FRW(D) is
   conjecturally true via the curved-spacetime path
   (Verch 1994 + Fewster 2015 + nuclearity in Hadamard reps), but
   nuclearity-on-curved-spacetime is itself only proved case-by-case
   (D'Antoni-Hollands 2006 for free Dirac, scattered other free cases).

2. **Interacting matter on FRW.** No theorem-proved hyperfiniteness for
   perturbatively constructed interacting models. Hollands-Wald 2001 gives
   the algebraic framework but does not address W*-type questions for the
   resulting algebras.

3. **Wedge / past-light-cone-without-truncation.** A genuine cosmological
   past-light-cone diamond with eta_i -> 0 hits the Big Bang singularity,
   which the conformal pullback does not handle. The "FRW past-light-cone
   diamond" of the user prompt is interpreted here as a doubly bounded
   diamond with eta_i, eta_f bounded away from 0 (in the de Sitter case,
   bounded away from the conformal future). Lifting this restriction is
   open.

## Structural implications for ECI

### Already-killed leviers, now sharpened

- **R3 [KILLED-BY-VERCH-1994].** Verch 1994 already implied that the
  W*-class of A_FRW(D) is folium-invariant; the present note makes
  explicit that the crossed product is therefore folium-invariant too,
  and equals R_{0,1}. The hope of detecting "different observers see
  different factors" was foreclosed the moment Verch's quasi-equivalence
  was understood — this note records the foreclosure.

- **R8 [REFUTED-BY-WEYL-LAW].** The Weyl-law refutation independently
  killed R8, but R_{0,1}-uniqueness is the structural reason it could not
  have worked: any "spectral / type" invariant of the crossed-product
  algebra is constant across the BFV folium.

### Closed paths

- **Bianchi VI_{-1/9} type-classification path.** As long as the matter
  sector is conformally coupled and the diamond is regular, the W*-type
  is R_{0,1} for both isotropic FRW and anisotropic Bianchi. So
  type-classification cannot be a Bianchi-vs-FRW discriminator. (The
  conformal pullback works for any conformally flat background; Bianchi
  VI_{-1/9} has non-zero Weyl tensor in general, so the conformal
  pullback strictly speaking does NOT apply to Bianchi — but the
  hyperfiniteness conclusion holds via the curved-spacetime path
  modulo nuclearity, so the foreclosure stands as a working
  conjecture.)

### Open paths NOT closed by this note

- **Trace normalisation as observer-discriminator.** R_{0,1} has a
  semifinite normal trace unique up to scaling. The scaling factor IS
  observer-dependent (clock choice, area normalisation). Any putative
  cosmological discriminator should live in the trace normalisation, not
  the W*-type.

- **Modular spectrum on a finite-energy subspace.** Not constrained by
  R_{0,1}-uniqueness. Open.

- **Relative entropy structure on observer pairs.** Not constrained.
  Open.

## Citation paranoia log

- **Verch 1994 CMP 160 507-536** confirmed via Project Euclid
  cmp/1104269708 + Springer DOI 10.1007/BF02173427 + ADS
  1994CMaPh.160..507V. Three independent corroborations.
- **Connes-Takesaki 1977** confirmed Project Euclid tmj/1178240493
  (Tohoku Math. J. 29, 473-575). DOI 10.2748/tmj/1178240493.
- **BDF 1987** Buchholz-D'Antoni-Fredenhagen, NOT a hallucination,
  CMP 111, 123-135, DOI 10.1007/BF01239019. Confirmed via Project
  Euclid cmp/1104159470.
- **"Schroer 1989"** from the user prompt: NOT used in the note. Search
  did not find a specific 1989 Schroer paper matching the description
  ("hyperfiniteness of Hadamard QFT local algebras"). The canonical
  Minkowski-space hyperfiniteness reference is BDF 1987. Replacing
  "Schroer 1989" with BDF 1987 + Fewster 2015 to avoid a probable
  hallucinated citation. Flag this as a 29th near-miss caught in time.
- **Connes 1976** (Annals 104, 73-115) cited for AFD II_infty
  uniqueness. This is the actual classification paper; not on arXiv,
  pre-arXiv. Universally referenced — no hallucination risk.
- **Buchholz 1990** "The structure of local algebras in quantum field
  theory" (in Doplicher-Longo-Roberts proceedings, 1990) — cited as a
  secondary reference for nuclearity in free-field models on Minkowski.
  Less critical to the proof; if the proceedings volume cannot be
  located it can be replaced by the Springer Lecture Notes
  Schroer-Wightman volume or removed entirely.

## Risk register for the note

**Low risk** (high-confidence claims):
- The unitary equivalence of A_FRW(D) and A_Mink(M_D) (already in
  frw_note Thm 3.5).
- The Hislop-Longo type-III_1 classification of the Minkowski diamond
  algebra.
- The Connes-Takesaki + Connes 1976 uniqueness of R_{0,1}.

**Medium risk** (load-bearing folklore):
- That A_Mink(M_D) for the free massless scalar is hyperfinite. This is
  folklore; BDF 1987 gives R⊗Z, factor case gives R, hence hyperfinite
  III_1. If a referee challenges, the safe fallback is to cite
  Brunetti-Guido-Longo 2002 (CMP 233, 1-33) or the modern review of
  Witten 2112.11614 §3.

**Negligible risk:**
- All arXiv-API citations are independently verified.

## Suggested next moves

1. **Submit as math.OA short note.** 6-8 pages, clean structural result,
   companion to the frw_note Thm 3.5/3.6 result. Author acknowledges
   the result is folklore-known but never explicitly recorded for the
   FRW case.

2. **Strengthen Lemma 3 (curved-spacetime hyperfiniteness).** Cite the
   D'Antoni-Hollands "Nuclearity, Local Quasiequivalence and Split
   Property for Dirac Quantum Fields in Curved Spacetime" CMP 261
   (2006) (arXiv:math-ph/0106028) for an explicit nuclearity-on-curved
   theorem, and replace Buchholz1990 (which I could not arXiv-verify)
   with that citation if the proceedings reference cannot be confirmed.

3. **Optional appendix.** A 1-page sympy/numerical-verification cell is
   not really applicable here (operator-algebra is structural), but a
   short proposition listing the precise nuclearity hypothesis used in
   the curved-spacetime path of Lemma~\ref{lem:AFD} would tighten the
   note for an OA referee.
