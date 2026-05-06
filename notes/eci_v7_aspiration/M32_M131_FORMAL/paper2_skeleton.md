# Paper-2 skeleton — ANT-tier 22pp

## Title

*"A Steinberg-edge obstruction to Katz-type 2-adic L-functions for the CM newform 4.5.b.a, with a Pollack-type rescue conjecture"*

## Target venue

**Algebra & Number Theory (ANT)** primary. Backup: *Research in Number Theory*.

## Abstract draft (180 words)

> The LMFDB CM newform $f = 4.5.b.a$ of weight 5, level 4, with CM by $\mathbb{Q}(i)$,
> sits at the intersection of two pathologies for $p$-adic $L$-function constructions
> at $p=2$: its Hecke eigenvalue $a_2 = -4 = -p^{(k-1)/2}$ saturates the bad-prime
> Ramanujan bound (the **Steinberg-edge**), and $p=2$ ramifies in the CM field.
> We show that classical Katz, Pollack–Sprung, Andreatta–Iovita, and Lei–Loeffler–Zerbes
> constructions all fail to apply. We then formulate **Conjecture M13.1**, a
> Pollack-type rescue: there exist bounded distributions $L_2^\pm(f)$ on the
> anti-cyclotomic $\mathbb{Z}_2$-extension $\Gamma$ of $\mathbb{Q}(i)$, interpolating
> functional-equation-symmetrised Damerell rationals $(\alpha_m + \alpha_{k-m})/2$
> with a renormalised Euler factor $E_2^\pm(f,m) = (-p^{m-1})(1+p^{m-3})$. We prove
> unconditionally that the renormalised Damerell ladder has strict monotone 2-adic
> valuations $\{-3,-2,0,+1\}$, and that pair-sum rationality forces the level to be
> a perfect square. We outline a proof strategy via Kriz's Hodge filtration framework
> extended to ramified CM, combined with Fan–Wan's ramified principal series machinery.

## Section outline (22pp)

| § | Title | pp |
|---|---|---|
| 1 | Introduction | 3 |
| 2 | Setup and the form 4.5.b.a | 2 |
| 3 | The Steinberg-edge and frameworks that fail | 3 |
| 4 | The Damerell ladder and F1 renormalisation (Theorems C(i), D(i)) | 3 |
| 5 | Conjecture M13.1.A — existence of $L_2^\pm(f)$ | 3 |
| 6 | Conjecture M13.1.B — boundedness | 2 |
| 7 | Conjecture M13.1.C(ii) and D(iii) | 1 |
| 8 | Proof strategy and outlook | 2 |
| App A | Sympy verification scripts | 1 |
| App B | LMFDB cross-check table (9-form sample) | 1 |
| Refs | Bibliography | 1 |
| **Total** | | **22** |

## Section content sketches

### §1 Introduction (3pp)

- Motivation: gaps in the CM-form $p$-adic $L$-function landscape at $p=2$
- The newform 4.5.b.a and its anomalies (Steinberg-edge + ramified CM)
- Statement of main theorems:
  - **Theorem 1.1 (= M13.1.C(i))** UNCONDITIONAL — F1 monotone $v_2$
  - **Theorem 1.2 (= M13.1.D(i))** UNCONDITIONAL — pair-sum rationality
  - **Theorem 1.3 (= M13.1.D(ii))** CONDITIONAL — Steinberg-edge $\Leftrightarrow p^2\mid N$
- Conjecture M13.1 (parts A, B, C(ii), D(iii)) precise statements
- Comparison with prior frameworks (table from M13)
- Overview of strategy

### §2 Setup and the form 4.5.b.a (2pp)

- Definition of $f$, Hecke character $\psi$, CM elliptic curve $E:y^2=x^3+x$
- Damerell rationals $\alpha_m$ for $m=1,2,3,4$ (1/10, 1/12, 1/24, 1/60)
- Anti-cyclotomic $\Gamma$, Iwasawa algebra, distributions $\mathcal{D}(\Gamma,\mathbb{Z}_2)$
- $p=2$ ramified: $\mathfrak{p}=(1+i)$, $p\mathcal{O}_K = \mathfrak{p}^2$, $N(\mathfrak{p})=p$

### §3 The Steinberg-edge and frameworks that fail (3pp)

- **Theorem 1.3 = M13.1.D(ii)**: $a_p = -p^{(k-1)/2} \Leftrightarrow p^2\mid N$
  with $p$ ramified [conditional]
- Why Pollack 2003 fails: requires $a_p=0$ (k=2 ss case)
- Why Sprung 2015, Andreatta–Iovita 2024 fail: explicit $p>3$ hypothesis
- Why Lei–Loeffler–Zerbes 2010 fails: $p$ odd
- Why Bellaïche–Stevens θ-critical doesn't directly apply: weight-5 CM-specific features missing
- Local Langlands picture: ramified principal series (M20)

### §4 The Damerell ladder and F1 renormalisation (3pp)

- **Theorem 1.1 = M13.1.C(i)**: F1 strict monotone $v_2 = \{-3,-2,0,+1\}$
  - Proof = direct computation (sympy-verified, M22)
- Comparison with 7 alternative renormalisations (M22 table)
- F1 derivation sketch from Frobenius-degeneracy compensation [TBD: C7]
- **Theorem 1.2 = M13.1.D(i)**: pair-sum rationality $\Leftrightarrow N$ square
  - Proof = classical functional equation
- 9-form LMFDB cross-check (M21) showing 4.5.b.a is unique with $\alpha_2+\alpha_3 = 1/8$

### §5 Conjecture M13.1.A — existence of $L_2^\pm(f)$ (3pp)

- Statement (interpolation formula with $E_2^\pm$, pair-sums, $\Omega_2$)
- Period $\Omega_2$ from Hodge-filtration generator of $\mathrm{Fil}^4 H^1_{\mathrm{dR}}(E)$
- Why Kriz 2021 framework is the natural setting (Hodge filtration, not Frobenius unit-root)
- Required extension to ramified CM: [TBD: A1]
- Fan–Wan ramified PS local hypothesis: [TBD: A2]
- Explicit Euler factor $E_2^\pm$ from F1: [TBD: A3]

### §6 Conjecture M13.1.B — boundedness (2pp)

- Iwasawa convention $\log_p(-4) = 0$
- Renormaliser $\omega(\gamma) = \log_p(\gamma)/(\gamma-1)$
- Pollack 2003 analogue: bounded measure after renormalisation
- [TBD: B5, B6]

### §7 Conjectures M13.1.C(ii) and D(iii) — embedding and uniqueness (1pp)

- Embedding of Damerell rationals via $\chi_m$ integration
- Uniqueness of 4.5.b.a within minimum perfect-square level
- [TBD: C8, D9, D11]

### §8 Proof strategy and outlook (2pp)

- Step-by-step program toward proving M13.1.A
- Required adaptations to Kriz Ch.~3 for ramified CM
- Companion Beilinson-regulator note (M27.1) at non-critical $s=k=5$
- Riemann-hypothesis remark: M28's anticyclotomic IMC corollary (140 words)
- Open problems

### Appendix A — Sympy verification scripts (1pp)

```python
from sympy import Rational, log
alpha = {1: Rational(1,10), 2: Rational(1,12), 3: Rational(1,24), 4: Rational(1,60)}
# pair-sum check
assert alpha[2] + alpha[3] == Rational(1, 8)  # = 2^-3
# F1 renormalisation
def F1(m, p=2):
    return alpha[m] * (-p**(m-1)) * (1 + p**(m-3))
ren = [F1(m) for m in [1,2,3,4]]
v2 = [int(log(abs(x), 2)) for x in ren]  # log_2 of |x| as Rational
# Expected: ren = [-1/8, -1/4, -1/3, -2/5], v2 = [-3, -2, 0, +1]
```

### Appendix B — LMFDB cross-check table (1pp)

| Form | $k$ | $N$ | $N$ square? | CM | Pair-sum(2,3) | $=2^{-3}$? |
|------|-----|-----|------------|-----|---------------|-----------|
| **4.5.b.a** | 5 | 4 | ✓ | $\mathbb{Q}(i)$ | $1/8 = 2^{-3}$ | **✓** |
| 36.5.d.a | 5 | 36 | ✓ | $\mathbb{Q}(i)$ | rational, $\neq 1/8$ | ✗ |
| 64.5.c.a | 5 | 64 | ✓ | $\mathbb{Q}(i)$ | rational, $\neq 1/8$ | ✗ |
| 100.5.b.a | 5 | 100 | ✓ | $\mathbb{Q}(i)$ | rational, $\neq 1/8$ | ✗ |
| 27.5.b.a | 5 | 27 | ✗ | $\mathbb{Q}(\sqrt{-3})$ | irrational | ✗ |
| 81.5.d.a | 5 | 81 | ✓ | $\mathbb{Q}(\sqrt{-3})$ | in $\mathbb{Q}(\sqrt{-3})$ | ✗ |
| 3.7.b.a | 7 | 3 | ✗ | $\mathbb{Q}(\sqrt{-3})$ | irrational | ✗ |
| 27.3.b.a | 3 | 27 | ✗ | $\mathbb{Q}(\sqrt{-3})$ | irrational | ✗ |
| 12.3.c.a | 3 | 12 | ✗ | $\mathbb{Q}(\sqrt{-3})$ | irrational | ✗ |

## Collaborator targeting

| Mathematician | Affiliation | Why | Action |
|---|---|---|---|
| **Daniel Kriz** | MIT | Hodge filtration framework (M13.1.A) | Email after first draft |
| Antonio Lei | Ottawa | Supersingular Iwasawa, $k\geq 2$ cases | Email after first draft |
| Francesc Castella | UCSB | Anti-cyclotomic main conjecture | Email after first draft |
| Ming-Lun Hsieh | Academia Sinica | Hida–CM $p$-adic $L$-functions | Optional |
| K. Büyükboduk | UC Dublin | θ-critical eigencurve constructions | Optional |
| Y. Fan / X. Wan | CNU / Morningside | Ramified PS framework (§5 hypothesis) | Email for verification |

## Bibliography skeleton (14 key entries)

1. Pollack, R. 2003. "On the $p$-adic $L$-function of a modular form at a supersingular prime." *Duke Math. J.* 118, 523-558.
2. Kobayashi, S. 2003. "Iwasawa theory for elliptic curves at supersingular primes." *Invent. Math.* 152.
3. Kriz, D. 2021. *Supersingular $p$-adic $L$-functions, Maass-Shimura Operators, and Waldspurger Formulas.* AMS-212, Princeton UP. ISBN 9780691216478.
4. Fan, Y.; Wan, X. 2023. arXiv:2304.09806.
5. Andreatta, F.; Iovita, A. 2024. arXiv:1905.00792.
6. Bellaïche, J.; Stevens, G. 2009. "p-adic families of Galois representations."
7. Benois, D.; Büyükboduk, K. 2024. arXiv:2403.16076.
8. Lei, A.; Loeffler, D.; Zerbes, S.L. 2010. arXiv:0912.1263.
9. Burungale, A.; Büyükboduk, K.; Lei, A. 2023. arXiv:2310.06813.
10. Büyükboduk, K.; Neamti, A. 2026. arXiv:2604.13854.
11. Damerell, R.M. 1970/1971. "L-functions of elliptic curves with complex multiplication, I & II." *Acta Arith.*
12. Katz, N.M. 1976. "p-adic interpolation of real analytic Eisenstein series." *Annals of Math.* 104.
13. Hida, H. 1985. "A p-adic measure attached to the zeta functions associated with two elliptic modular forms I." *Invent. Math.* 79.
14. LMFDB Collaboration. *L-functions and Modular Forms Database*, lmfdb.org.

## Submission checklist

- [ ] All [TBD: prove] markers explicitly flagged in text
- [ ] No claim of full construction of $L_2^\pm$
- [ ] Clear separation: 2 unconditional theorems + 1 conditional + 4 conjectures
- [ ] Sympy verification scripts in Appendix A (reproducible)
- [ ] LMFDB labels verified live within last 30 days
- [ ] Hallu count audit: 85 maintained throughout drafting
- [ ] Triple-pass pdflatex compile (0 errors, 0 undef-warns)
- [ ] arXiv endorser secured (math.NT, via Kriz/Lei/Booker)
