# M90 Literature Table: Anticyclotomic IMC for K Imaginary Quadratic

**Mission:** R-2.1 target = char_Λ(Sel_2^{anti-cyc}(K,T_f)) = (L_2^{anti-cyc}(f,T))
for f = 4.5.b.a (weight 5, level 4, CM newform), K = Q(i), p = 2 (RAMIFIED in K).

Key obstructions for p=2 ramified in K=Q(i):
- K = Q(i) has discriminant D_K = -4, so 2 | D_K (ramification)
- p=2 is NOT odd — nearly all frameworks require p ≥ 3 or p ≥ 5
- Standard Heegner hypothesis requires p split; p=2 does not split in Q(i)
- Most Galois representation technology (Greenberg selmer, signed selmer) uses p-adic Hodge theory best developed for p ≥ 3

Legend: ✓ = yes/compatible, ✗ = no/excluded, ~ = partial/conditional, ? = unknown/not stated, [TBV] = to be verified in full text

---

## Table 1: Core Papers

| # | Paper | arXiv / Ref | K imag-quad ✓/✗ | p ramified OK? | p=2 OK? | Weight k | Ordinary | IMC proved | Notes |
|---|-------|-------------|-----------------|----------------|---------|----------|----------|------------|-------|
| 1 | Pollack–Weston "On anticyclotomic μ-invariants of modular forms" | math/0610694; Compositio Math. 147 (2011) 1353–1381 | ✓ | ✗ (implicitly) | ✗ | k=2 only | [TBV] | μ-part only | Requires N = N⁺N⁻ split/inert factorization; p must be odd [TBV for ramified]; foundational reference |
| 2 | Chida–Hsieh "On the anticyclotomic Iwasawa main conjecture for modular forms" | arXiv:1304.3311; Compositio Math. 151 (2014) 863–897 | ✓ | ✗ (N⁻ inert/ramified in K but p separate) | ✗ (p ≥ 3 implicit) | k ≥ 2 | ✓ ordinary | One divisibility | Level N = N⁺N⁻; p-ordinary; Heegner hyp; p odd implicit; does NOT require p split, but p∤ND_K likely required [TBV] |
| 3 | Büyükboduk–Lei "Anticyclotomic p-ordinary Iwasawa Theory of Elliptic Modular Forms" | arXiv:1602.07508 | ✓ | ✗ | ✗ | k ≥ 2 | ✓ ordinary | Full IMC | Requires p SPLITS in K; Beilinson-Flach Euler system |
| 4 | Castella–Do "Diagonal cycles and anticyclotomic Iwasawa theory of modular forms" | arXiv:2303.06751; JEMS (2025) | ✓ | ? | ✗ | k ≥ 2 | ✗ (non-ordinary OK) | One divisibility toward Greenberg IMC | Root number +1 required; no explicit split requirement stated in abstract but inert setting in followup 2507.22755 |
| 5 | Burungale–Büyükboduk–Lei "Anticyclotomic Iwasawa theory GL₂-type non-ordinary primes" | arXiv:2211.03722; arXiv:2310.06813 | ✓ | ✗ | ✗ | k=2 (elliptic curves) | ✗ (supersingular) | One divisibility | p ≥ 5 EXPLICITLY; split or inert in K; ramified excluded; only weight 2 |
| 6 | Longo–Pati–Vigni "Anticyclotomic Iwasawa main conjectures for modular forms" | arXiv:2603.22483; March 2026 | ✓ (incl. K=Q(i) for p≥5) | ✗ | ✗ | k ≥ 4 even | ✓ ordinary | FULL equality (both divisibilities) | Requires p ODD, p ∤ N·D_K so p≠2 for K=Q(i); otherwise K=Q(i) allowed with p≥5 |
| 7 | Nguyen "Congruent modular forms and anticyclotomic Iwasawa theory" | arXiv:2503.00247; Oct 2025 | ✓ | ✗ | ✗ | k ≥ 2 (general) | ✗ (not required) | Congruence comparison of BDP L-functions; conditional IMC | p odd required; p splits in K required; K=Q(i) allowed if p≥5 splits in Q(i) |
| 8 | Fan–Wan "p-adic Waldspurger Formula for Non-split Primes and Converse of GZK" | arXiv:2304.09806 | ✓ | ✓ | ✓ | CM Hecke characters (not general newforms) | — | Converse GZK (Selmer rank 1 → analytic rank 1); NOT full IMC | CRITICAL: p=2 and ramified p BOTH ALLOWED; but restricted to SELF-DUAL HECKE CHARACTERS (CM forms only); does not prove char ideal equality |
| 9 | Longo–Pati "Exceptional zero formulae for anticyclotomic p-adic L-functions in the ramified case" | arXiv:1707.06019; J. Number Theory 185 (2018) | ✓ | ✓ | ? (odd implicit) | k=2 | Mult. reduction at p | p-adic L-function + exceptional zero formula; NOT IMC | First systematic treatment of p ramified in K; elliptic curves with multiplicative reduction; p odd probably required |
| 10 | Bertolini–Longo–Venerucci "Anticyclotomic main conjectures for elliptic curves" | arXiv:2306.17784; Feb 2026 v2 | ✓ | ✗ | ✗ | k=2 only | both ord/ss | Near-full IMC (up to exceptional case) | p ≥ 5 EXPLICIT; p ∤ D_K required; split or inert (NOT ramified); K=Q(i) blocked by p≥5 AND p∤4 requirements |
| 11 | Burungale–Castella–Skinner "Base change and Iwasawa Main Conjectures for GL₂" | arXiv:2405.00270 | ✓ | ✗ | ✗ | k=2 | ✓ ordinary | Full IMC (cyclotomic + anticyclotomic) | p odd + all primes dividing Np split in K; relaxes E[p] ramification hypotheses but NOT the p-split-in-K requirement |
| 12 | Wan "Iwasawa Main Conjecture for Rankin-Selberg p-adic L-functions" | arXiv:1408.4044; Algebra Number Theory 14 (2020) | ✓ | ? | ✗ | general f, CM higher weight | ✓ ordinary | One divisibility (L ∣ char ideal) | General modular form × CM form; conditions on p not explicit in abstract; p odd likely; split [TBV] |
| 13 | Isik "Anticyclotomic Iwasawa Theory of Hecke Characters at Ordinary Primes" | arXiv:2412.10980 | ✓ (K=Q(i) as special case) | ✗ | ✗ | CM Hecke characters | ✓ ordinary (p-ord) | Full equality (Theorem A) | p odd + primes above p split in K; K=Q(i) included for p≥5 splitting in Q(i); p=2 excluded |
| 14 | Arnold "Anticyclotomic main conjectures for CM modular forms" | J. reine angew. Math. 606 (2007) 41–78 | ✓ | ? | ✗ | k ≥ 2 even, CM | supersingular | One divisibility / half-IMC | CM forms of even weight at supersingular prime; generalizes Agboola-Howard; p odd likely; conditions on ramification [TBV] |
| 15 | Liu–Tian–Xiao "Iwasawa's main conjecture for Rankin-Selberg motives, anticyclotomic" | arXiv:2406.00624 | ~ (CM fields general) | ? | ✗ | GL(n)×GL(n+1) automorphic | — | One-sided divisibility | Very general CM field setting; not restricted to imaginary quadratic K; p conditions not detailed in abstract |

---

## Table 2: Hypothesis Distance from R-2.1

**Target R-2.1:** char_Λ(Sel_2^{anti-cyc}(Q(i), T_{4.5.b.a})) = (L_2^{anti-cyc}(4.5.b.a))

| Paper | Δ-1: p odd required (not p=2) | Δ-2: p unramified in K required | Δ-3: weight k=2 only (not k=5) | Δ-4: ordinary only (f=4.5.b.a is CM, check) | Δ-5: split in K required | Δ-6: only one divisibility | Δ-7: only CM Hecke char (not general newform) | Total Δ |
|-------|-------------------------------|--------------------------------|-------------------------------|-----------------------------------------------|--------------------------|----------------------------|----------------------------------------------|---------|
| Pollack–Weston (math/0610694) | ✗ (probably) | ✗ yes | ✗ yes | ~ | ✗ yes | ✗ (μ-part) | ~ | 4–5 |
| Chida–Hsieh (1304.3311) | ✗ yes | ✗ probably | no (k≥2) | ✓ | ✗ maybe not | ✗ (one div.) | no | 3–4 |
| Longo-Pati-Vigni (2603.22483) | ✗ yes | ✗ yes (p∤D_K) | no (k≥4) | ✓ | no (Heg. flexible) | no (full=) | no | **2** |
| Fan–Wan (2304.09806) | no (p=2 OK!) | no (ramified OK!) | no (chars) | ✓ (CM) | no | ✗ (not full IMC) | ✗ yes (CM chars) | **3 functional** |
| Bertolini-Longo-Venerucci (2306.17784) | ✗ yes | ✗ yes | ✗ yes | ~ | ✗ (sp/inert) | ~ | no | 4 |
| Isik (2412.10980) | ✗ yes | ✗ yes (split) | no (chars) | ✓ | ✗ split req. | no (full=) | ✗ yes (chars) | 3 |

**Notes on 4.5.b.a ordinarity at p=2:** f = 4.5.b.a is a CM newform of level 4, weight 5. Since p=2 ramifies in K=Q(i) (the CM field), the form has a specific local behavior at p=2. CM forms at primes ramified in the CM field are typically supersingular-like or have specific CM-type Hecke eigenvalue behavior — the Hecke eigenvalue a_2(f) for a CM form of type K=Q(i) at the ramified prime p=2 is likely 0 or a unit [TBV via LMFDB]. This matters for the ordinary vs. non-ordinary classification.

---

## Table 3: Ramified-p Literature Timeline

| Year | Paper | Ramified-p claim | Scope |
|------|-------|-----------------|-------|
| 2007 | Arnold, J. reine 606 | Not specifically ramified; supersingular focus | CM forms |
| 2017 | Longo–Pati (1707.06019) | FIRST systematic: p ramified in K, L-function construction | Weight 2, mult. red. |
| 2019 | Andreatta–Iovita (1905.00792) | p NON-SPLIT (inert specifically, not ramified) | p-adic L-functions |
| 2023 | Fan–Wan (2304.09806) | p=2 AND ramified ALL allowed | CM Hecke chars only |
| 2025 | Nguyen (2503.00247) | p odd, p splits in K | Congruence method |
| 2026 | Longo-Pati-Vigni (2603.22483) | p odd, p ∤ D_K (so p≠2 for K=Q(i)) | k≥4 ordinary, full IMC |

**Summary gap:** No paper as of May 2026 proves an anticyclotomic IMC for a general (non-CM Hecke character) newform of weight ≥ 3 at p=2 ramified in an imaginary quadratic field.
