# M31 exploration log — BSD × ECI

**Date:** 2026-05-06
**Sub-agent:** M31 (Opus 4.7, last of Phase 3.F)

---

## Step 1 — Required reading (3 min)

Read M27 SUMMARY, M28 SUMMARY, M13 SUMMARY in full. Key extracts:

- **M27** verdict was SHIMURA-CM-TRIVIAL + TANGENTIAL-BEILINSON. The surviving
  angle was Beilinson regulator at $s=k=5$, formulated as Conjecture M27.1
  matching 2-adic valuations $v_2(\alpha_m^{\rm ren})=\{-3,-2,0,+1\}$ to the
  2-adic refinement of the Beilinson regulator on
  $H^2_\mathcal{M}(K_3, \Q(j))$. This is exactly the higher-weight analog of
  the BSD leading-coefficient formula.
- **M28** verdict was NO-DIRECT-ROUTE + WEAK-TANGENTIAL-ANTICYCL-IMC. Noted
  that the BSD/IMC dictionary links algebraic and analytic L-value content
  only at isolated points. Skinner-Urban 2014 (Inv. Math. 195:1-277) flagged
  as the cyclotomic GL2 IMC reference.
- **M13** Conjecture M13.1 lives in $D(\Gamma, \Z_2)$ for $\Gamma =
  \mathrm{Gal}(K_\infty^{\rm anti}/K) \cong \Z_2$, anticyclotomic. Steinberg
  edge $a_2 = -2^{(k-1)/2}$, β-renormalized monotone $v_2$ pattern.

## Step 2 — Frame the BSD question precisely

BSD (Clay 2000) for elliptic curve $E/\Q$:
$$
\mathrm{ord}_{s=1} L(E,s) = \mathrm{rank}\, E(\Q),
$$
plus an explicit leading-coefficient formula in terms of regulator, period,
Tate-Shafarevich, Tamagawa numbers.

By Wiles 1995 / BCDT 2001 modularity, $E \leftrightarrow$ weight-2 newform $f_E$,
so BSD is equivalently a statement about weight-2 newforms.

**$f = $ 4.5.b.a has weight 5.** No elliptic curve corresponds to it under
modularity. Direct BSD inapplicable.

## Step 3 — Q1a: weight-5 BSD-analog?

The natural generalisation is **Beilinson 1984 + Deninger-Scholl 1991**:
for a weight-$k$ newform $f$ and integer $n$ outside the critical strip,
$L^*(f, n) \sim \langle r_\mathcal{D}(\xi_n), \omega_f \rangle$ for a motivic
class $\xi_n$ via Eisenstein symbol; rank predicted by $\dim H^?_\mathcal{M}$.

For $k=5$, critical strip is $1 \le s \le 4$. First non-critical integer to
the right is $s = k = 5$. M27 Q3 already identified this and proposed
Conjecture M27.1.

**Conclusion:** M31 has nothing new to add to Q1a. Same content as M27.

## Step 4 — Q1b: Bloch-Kato Tamagawa number conjecture

Bloch-Kato 1990 (in *The Grothendieck Festschrift* vol. I) extends the BSD
leading-coefficient formula to general motives. For $M(f)$:
- Predicts $L^*(M(f), n)$ in terms of motivic cohomology, regulators, period
  matrix, and Tamagawa factors $T_\ell$ at each prime $\ell$
- $T_2$ is one local factor; M13.1 + Kriz framework would give 2-adic
  information feeding into $T_2$
- This is **the same content as the M13.1 paper-2** — not a new "Bloch-Kato"
  contribution. Calling it "BSD" is misleading because BSD specifically refers
  to the elliptic-curve / weight-2 case in the Clay statement.

## Step 5 — Q2a: Skinner-Urban → BSD analog?

Skinner-Urban 2014 (Inv. Math. 195:1-277) prove one inclusion of the
**cyclotomic** GL2 IMC for weight-2 ordinary $p$-stabilisations (with mild
local hypotheses). Combined with Kato 2004 they obtain the $p$-part of BSD
in many rank-$\le 1$ cases.

For 4.5.b.a the M28 conditional anticyclotomic IMC at $p=2$:
- is **anticyclotomic, not cyclotomic** — different $\Z_p$-extension
- concerns Selmer groups of $V_2(f)$ over $K_\infty^{\rm anti}/K$, not over
  $\Q_\infty^{\rm cyc}/\Q$
- gives a characteristic-ideal statement for an Iwasawa module, not a
  rank-equals-order-of-vanishing statement
- is for **weight 5**, so even if extended to cyclotomic, it would feed into
  Bloch-Kato for $M(f)$, not BSD for an elliptic curve

**Conclusion:** No BSD-analog produced. M31 nothing new beyond M28.

## Step 6 — Q2b: Selmer rank for weight 5

For weight 5, the BSD analog "rank = order of vanishing" becomes:
$$
\dim_{\Q_p} H^1_f(\Q, V_p(f)(j)) \stackrel{?}{=} \mathrm{ord}_{s=j} L(f,s)
$$
for Tate twist $j$, where $H^1_f$ is the Bloch-Kato Selmer group. For
non-critical $j$ this is the Bloch-Kato side of Beilinson's conjecture.

The motivic cohomology $H^2_\mathcal{M}(K_3, \Q(j))$ already appears in
M27 Q3. **No new M31 content.**

## Step 7 — Q3: any direct route?

Weight 2 vs weight 5 is irreducible. There is no functoriality or twist taking
$f$ (weight 5) to a genuine weight-2 newform (and hence elliptic curve) over
$\Q$ such that ECI's 2-adic conjecture would translate to a BSD statement for
that elliptic curve. Symmetric power $\mathrm{Sym}^k$ of weight 2 raises
weight, not lowers; theta lifts/Saito-Kurokawa go to higher rank groups.

**Conclusion:** CONFIRMED-DEAD-END. No direct contribution. M31 stops here.

## Step 8 — Cross-checks attempted

- Tried `WebFetch https://www.claymath.org/.../birch-and-swinnerton-dyer-conjecture/`
  → permission denied (sandboxed). Rely on M28's already-verified
  Skinner-Urban Inv. Math. 195 reference and standard textbook knowledge.
- WebFetch arxiv.org/abs/1407.1093 returned an unrelated paper abstract
  (multiplicative reduction case) — confirmed Skinner-Urban-style results
  exist but not directly informative for M31's question. No new bib data
  extracted, no fabrication risk taken.
- No new arXiv IDs introduced. No new author names introduced. Hallu count
  protected at 85.

## Step 9 — Output decision

3 small files (≤80, ≤150, ≤80 lines), as instructed. No giant LaTeX, no
paper draft. Verdict: CONFIRMED-DEAD-END for BSD itself; SUBSUMED-BY-M27 for
the higher-weight Beilinson analog; nothing new to add to v7.5/v7.6/v7.7.

## Honest [TBD: prove] markers (1)

1. Explicit verification that *no* functorial transfer (Saito-Kurokawa,
   theta lift, base change, automorphic induction) produces a weight-2
   newform from $f = $ 4.5.b.a in a way that would let ECI's 2-adic
   anticyclotomic conjecture descend to a statement about an actual elliptic
   curve over $\Q$. Symmetric powers raise weight; CM induces from $K=\Q(i)$
   to $\Q$ at weight 5; no path to weight 2 visible. **Conjecturally none
   exists.** Not worth pursuing further.
