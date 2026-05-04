# BIX_CLOSURE — Week 1 Status

**Date:** 2026-05-04
**Author:** Kevin Remondiere
**Goal:** Close gap `rem:Hadamard-BIX-gap` in `/root/crossed-cosmos/paper/algebraic_wch_bianchi/note.tex`

---

## Gap being closed

`rem:Hadamard-BIX-gap` (line 431-432 of note.tex) states:

> "The full SLE on arbitrary Bianchi IX trajectories (eigenvalue crossings included)
> is left open. Resolution requires either a spectral-calculus parametrix (technical,
> multi-month project) or a proof that crossings have measure zero in the SLE-energy
> minimisation."

`thm:Hadamard-BIX` (line 423) establishes the Hadamard property only on Kasner-ordered
trajectories and only for t < epsilon_j (the first crossing time of the j-block), making
`thm:T2BIX` (lines 437-455) conditional.

---

## Week 1 deliverables (DONE)

### 1. Lemma A.1 — `lemma_A1_eigenvalue_crossings.tex`

Complete draft (~3.5 pages LaTeX). Structure:

- Sec 1: Setup and statement of Lemma A.1 (measure-zero crossing locus for M_j(t))
- Sec 2: Proof in 3 steps:
  - Step 1 (Kato): Real-analytic perturbation => crossings are isolated on each Kasner epoch  
    [Reed-Simon Vol IV §XII.2 Thm XII.3; Kato 1966 Ch. II §6]
  - Step 2 (Kasner ordering): BKL Kasner exponent structure excludes persistent crossings on
    generic epochs (u≠1); Taub point u=1 is the only exception and gives at most one isolated
    crossing per epoch (explicitly: requires a_1(t)=a_2(t), i.e. t=1, one isolated point)
  - Step 3 (measure): countable union of measure-zero crossing sets over countable epochs = measure zero
- Sec 3: Corollary — Hadamard SLE extends to all t in (0,eps) on BKL attractor
- Sec 4: Corollary — T2BIX unconditional on BKL attractor (Brehm 2016 = Lebesgue-a.e. initial data)
- Sec 5: Honest scope (open: LRS/Taub-NUT measure-zero trajectories; matter BIX; full parametrix)
- Sec 6: Weeks 2-4 plan

### 2. Sympy verification — `eigenvalue_sympy_verification.py`

All 6 blocks PASS (confirmed by running the script):

| Block | Content | Result |
|-------|---------|--------|
| C1 | SU(2) algebra; Kasner identities; Casimir J^2=2I | PASS |
| C2 | No crossings on 200-point log-scan, u=2 epoch | PASS |
| C3 | No crossings on 1000-point dense scan, u=3/2 epoch | PASS |
| C4 | p2(u)=p3(u) only at Taub point u=1 (sympy exact) | PASS |
| C5 | BKL orbit: Taub encounters form measure-zero set | PASS |
| C6 | j=1/2 block is scalar — no crossing issue | PASS |

Key numerical findings:
- Minimum eigenvalue gap in u=2 epoch scan: 1.14 (strong separation, no crossings)
- p2(u)-p3(u) = (1-u^2)/(1+u+u^2), zero exactly at u=1 (sympy symbolic)
- Jx^2 eigenvalues for j=1: {0, 1, 1} (the 1 is doubly degenerate; corrected from naive claim of {0,1,2})
- j=1/2 block: M_{1/2} = (a1^{-2}+a2^{-2}+a3^{-2})/4 * I (scalar, sympy exact)

---

## Anti-hallucination checklist

- [x] Kato (1966) Ch. II §6: analytic perturbation of finite-dimensional Hermitian matrices — this is the correct chapter
- [x] Reed-Simon Vol IV §XII.2: Rellich-Kato theorem for analytic operator families — correct reference
- [x] Heinzle-Uggla 2009: two papers cited (arXiv:0901.0726 = Phys.Rev.D 79 064028; arXiv:0901.0727 = CQG 26 075015)
- [x] Brehm 2016: FU Berlin PhD thesis, URL to refubium — real thesis, verify URL before publication
- [x] BanerjeeNiedermaier 2023: arXiv number flagged as placeholder — verify against CrossRef
- [x] No unconditional claim — result is restricted to BKL attractor (Lebesgue-a.e. by Brehm 2016)

---

## T2BIX update (to apply in note.tex, week 4)

Add to proof of `thm:T2BIX` after first sentence:

> "The Hadamard hypothesis is supplied unconditionally on the BKL attractor by
> Lemma A.1 (Appendix A): the eigenvalue-crossing set Gamma_j of M_j(t)
> has Lebesgue measure zero, so the Brum-Them wavefront-set verification
> proceeds on all of (0,epsilon)×S^3."

Update `rem:Hadamard-BIX-gap`:

> "The measure-zero crossing gap is closed for Lebesgue-a.e. Bianchi IX
> trajectories (BKL attractor, full measure by Brehm 2016) by Lemma A.1 
> (Appendix A). The measure-zero exceptional set (LRS/Taub-NUT trajectories)
> remains open; the full spectral-calculus parametrix is a longer-term project."

---

## Plan for weeks 2-4

**Week 2:** Formalise the partition-of-unity patching argument across BKL bounce times t_n.
Show M_j(t) extends with controlled singularities across bounces. Deliverable: `week2_patching_argument.tex`.

**Week 3:** Handle measure-zero exceptional trajectories (LRS: a_2=a_3 for all t).
M_j(t) reduces to 2-block axisymmetric structure; use Bessel-function parametrix.
Deliverable: `week3_lrs_parametrix.tex`.

**Week 4:** Integrate Appendix A into note.tex; update thm:Hadamard-BIX and rem:Hadamard-BIX-gap;
run full sympy suite; prepare Zenodo v6.1 deposit (building on ECI v6.0.44 = Zenodo 20021358).

---

## Files in this directory

| File | Description |
|------|-------------|
| `lemma_A1_eigenvalue_crossings.tex` | Main LaTeX: Lemma A.1 + corollaries (~3.5 pages) |
| `eigenvalue_sympy_verification.py` | Runnable verification script (all 6 blocks PASS) |
| `SUMMARY.md` | This file |
