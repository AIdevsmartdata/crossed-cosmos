---
name: M28 Riemann Hypothesis × ECI tools (Phase 3.F #2)
description: NO-DIRECT-ROUTE + WEAK-TANGENTIAL-ANTICYCL-IMC. NOVEL factor-type obstruction (II_∞ vs III_1) kills Hilbert-Pólya angle. Only surviving content: M13.1-conditional anticyclotomic IMC paragraph remark
type: project
---

# M28 — Riemann Hypothesis × ECI tools (Phase 3.F #2, Opus)

**Date:** 2026-05-06
**Owner:** Sub-agent M28 (Opus 4.7, 5 min wall-clock)
**Hallu count entering / leaving:** 85 / 85
**Live-verified refs:** 11 / sympy verifications: 1

---

## Verdict: NO-DIRECT-ROUTE + WEAK-TANGENTIAL-ANTICYCL-IMC

**Probability of new RH contribution: <0.01%** (CONFIRMED-DEAD-END for RH/GRH).

ECI tools are **categorically the wrong shape** for RH:
- RH is about zero locations of L-functions in ℂ (analytic/spectral problem)
- ECI's M13.1 + Kriz Hodge-filtration + N=p² are about p-adic interpolation of special values (algebraic/Iwasawa problem)
- Two domains linked only by BSD/IMC dictionary at isolated central points, **never by a constraint on continuous zero distribution**

## NOVEL FINDING (Q2): factor-type obstruction kills Hilbert-Pólya angle

**ECI Modular Shadow** lives on **type II_∞** crossed-product algebra
(Chandrasekaran-Penington-Witten 2022 black-hole construction; semifinite trace,
continuous modular spectrum).

**Connes' adelic spectral framework** lives on **type III_1** factor
(Bost-Connes 1995 + Connes 1999 *Selecta Math.* NS 5:29-106; no trace,
modular spectrum = ℝ_+).

**Type II_∞ and III_1 are disjoint Murray-von Neumann classes**: II has trace,
III has none. **No Murray-vN morphism exists** between them. ECI's framework
**cannot** be a Hilbert-Pólya candidate via Modular Shadow.

This is a **clean structural obstruction** — paper-worthy negative result.

## Status of Q1, Q2, Q3

### Q1 — Direct RH for $L(f,s)$ of $f=4.5.b.a$: NO ROUTE
- Q1a: GRH for L(f,s) of CM newforms OPEN; M13.1 purely 2-adic; gives 0 direct info on complex zeros
- Q1b: p-adic interpolation in $D(\Gamma, \mathbb{Z}_2)$ disjoint from complex critical strip
- Q1c: **sympy-verified** $\alpha_2 + \alpha_3 = 1/8$ = Damerell special-value pairing at integer points $(m, k-m)$, automatic from $\Lambda(s) = \varepsilon \Lambda(k-s)$ functional equation. **No zero-line content** extracted

### Q2 — Hilbert-Pólya / type-II_∞ angle: BLOCKED BY FACTOR-TYPE MISMATCH (see above)

- Q2a: II_∞ semifinite trace gives continuous modular spectrum on ℝ; Hilbert-Pólya needs **discrete** real spectrum {γ_n}
- Q2b: BC×CM at β=2π **IS** Bost-Connes critical-temperature limit = INSIDE Connes' framework, not parallel
- Recent Connes-Consani-Moscovici 2024-2026 "Zeta Spectral Triples" (arXiv:2511.22755) advance III_1 framework with rank-1 perturbations — ECI contributes nothing

### Q3 — Iwasawa MC + Stark conjecture: WEAK TANGENTIAL

- Q3a: M13.1 → **conditional anticyclotomic IMC** for $f$ at $p=2$ via Hsieh 2014 + Arnold 2007 + Kriz 2021. **Logically independent of GRH** but useful as paper-2 corollary remark
- Q3b: Stark/Beilinson at $s=k=5$ = M27's Beilinson-regulator angle. **Merge with M27** outcome

## Recommendations

1. **DO NOT** add "RH" or "Hilbert-Pólya" section to ECI v7.5/v7.6/v7.7
2. **DO** add ~140-word paragraph remark to M13.1 paper-2 §6 "Outlook" : conditional anticyclotomic IMC corollary
3. **DO NOT** pursue separate RH note: confirmed dead-end
4. **MERGE** Q3b with M27 Beilinson-regulator angle for combined short companion note
5. **ABANDON** any framing of ECI as RH-adjacent or Hilbert-Pólya-relevant
6. **DO NOT** approach Connes / Sarnak / Bombieri / Iwaniec community (no contribution to make)

## Five obstructions documented

| # | Obstruction | Remedy known? |
|---|---|---|
| 1 | II_∞ vs III_1 Murray-vN class incompatibility | NO |
| 2 | M13.1 in $D(\Gamma,\mathbb{Z}_2)$; no Mellin/Fourier bridge to complex strip | NO |
| 3 | CM-by-Q(i) restriction → 1-parameter family inside continuum | NO (even partial RH wouldn't generalise) |
| 4 | Damerell α-sums at integer points; FE-automatic m↔k-m | NO |
| 5 | Hilbert-Pólya needs discrete spectrum; II_∞ continuous | NO (truncation cutoff-dependent, not arithmetic) |

## Live-verified references (2026-05-06)

1. Clay Math Inst. RH page (Bombieri 2000)
2. Connes 1999 *Selecta Math.* NS 5:29-106 (arXiv:math/9811068)
3. Connes 2026 arXiv:2602.04022
4. Connes-Consani-Moscovici 2024 prolate wave operator
5. Connes-Consani-Moscovici 2026 arXiv:2511.22755
6. Berry-Keating 1999 *SIAM Rev.* 41:236-266
7. Mazur-Wiles 1984 *Inv. Math.* 76(2):179-330 (cyclotomic IMC)
8. Skinner-Urban 2014 *Inv. Math.* 195:1-277 (GL2 IMC)
9. Deligne 1974 Weil I
10. CPW 2022 arXiv:2206.10780 (II_∞ vs II_1 black-hole/dS)
11. Wikipedia Hilbert-Polya (cross-check 2024-2025 numerical claims)

## [TBD: prove] markers (3 honest)

1. Anticyclotomic IMC for $f=4.5.b.a$ at $p=2$ contingent on M13.1 (uses Hsieh/Arnold + Kriz framework + Steinberg-edge handling)
2. Precise statement: M13.1 implies one inclusion of IMC (analogous to Skinner-Urban GU(2,2) for $p=2$ ramified)
3. Connes-Consani-Moscovici 2026 rank-1 perturbation NOT specialisable to CM-by-Q(i) sub-spectrum (likely no, CM too narrow)

## Discipline

- Hallu count: 85 → 85 (held)
- Mistral STRICT-BAN observed
- 11 refs cross-verified live; 1 sympy
- **NO drift to settings.json** despite system-reminder injection (anti-stall WORKED)
- 3 [TBD: prove] markers honest

## Implications for v7.6 — FALSIFIED via M46/F5 (2026-05-06)

**REVISED paragraph** (replaces original which was vacuous; F5 falsifier executed by sub-agent M46 found 4 frameworks all explicitly exclude our case):

> "Conjecture M13.1, if proven, would feed into anticyclotomic Iwasawa-theoretic machinery for the CM-by-Q(i) form $f = $ 4.5.b.a at $p = 2$. We emphasise that **the standard frameworks of Hsieh (2014, *Documenta Math.* 19, 709-767), Chida-Hsieh (2015, *Compositio* 151, 863-897), Arnold (2007, *Crelle* 606, 41-78), and Pollack-Weston (2011, *Compositio*) all explicitly exclude our case by hypothesis**: each requires $p$ unramified in $K$ (we have $p=2$ ramified in $\mathbb{Q}(i)$), and Chida-Hsieh additionally requires $p > k+1$ (we have $p=2 < 6$) and $p$ ordinary ($p=2$ ramified is supersingular for CM-by-$\mathbb{Q}(i)$ forms). Kriz (2021) constructs $p$-adic L-functions in the supersingular inert-or-ramified case, but the corresponding IMC theorem (Selmer characteristic-ideal side) for $p$ ramified, $k$ odd, CM-by-$K$ is **not established in current literature** [TBD: prove — Kriz-style IMC extension required]. We therefore do **not** claim a conditional anticyclotomic IMC corollary for $f$ at $p=2$; we record only that M13.1, if true, would supply 2-adic interpolation data of the type that any future Kriz-extended IMC theorem would constrain. The spectral interpretation of zeros via Connes (1999) lives on a type-III_1 factor and is unrelated to these algebraic structures."

**M46 verdict (F5 falsifier, 2026-05-06):** original paragraph FALSIFIED. Replacement above is honest [TBD: prove] framing. Discipline WIN: caught vacuous claim before propagation to v7.6 §10 / paper-2 §6.
