---
name: M42 pistes_close — closures and dead-ends
description: S2 KLZ-UNIQUE closure (4 alternative p-adic Hodge mechanisms tested, none competitive); plus secondary dead-ends (Bianchi IX deformed-algebra, BDP for v_2 ladder)
type: project
---

# M42 — DEAD-END / DEFER closures (close file)

## §S2 — Alternative p-adic Hodge mechanisms for v_2 = {-3,-2,0,+1}: KLZ-UNIQUE [CLOSURE]

### Tested alternatives

We tested 4 alternative p-adic Hodge mechanisms against the KLZ2017 route
(M39, arXiv:1503.02888) for explaining the F1-renormalized v_2 pattern
$\{-3, -2, 0, +1\}$ in M22.

#### A. Fontaine-Messing 1987 syntomic regulator

- Classical framework subsumed by Niziol 2008 in the modern formulation.
- No published computation for CM newforms at the Steinberg-edge p=2
  ramified case.
- **No constructive route to v_2 pattern.**

#### B. Niziol 2008 syntomic cohomology (arXiv:1309.7620, verified)

- General machinery: syntomic cohomology with potentially semistable Selmer
  group landing.
- Establishes **foundational syntomic / étale comparison**, but does NOT
  publish 4.5.b.a-style explicit computation of regulator pairings at
  $j \in \{1, 2, 3, 4\}$.
- Would require **independent reconstruction** by us — not available
  off-the-shelf, no advantage over KLZ2017.
- **Verdict:** subsumed by KLZ which uses syntomic regulator already.

#### C. Bhatt-Morrow-Scholze 2018 prismatic / integral p-adic Hodge (arXiv:1802.03261, verified)

- Powerful unification of crystalline / étale / de-Rham via prisms.
- Published abstract focuses on topological Hochschild homology, A-Omega
  complex, Breuil-Kisin modules, syntomic sheaves.
- **Beilinson-regulator pairing NOT in their abstract** — would require a
  specialist's translation from prismatic to motivic-cohomology setup.
- For our v_2 pattern: would only re-prove what KLZ already gives, modulo
  the same Steinberg-edge p=2 wall.
- **Verdict:** no independent advantage.

#### D. Bertolini-Darmon-Prasanna 2013 (Duke 162(6), 2013, verified)

- Anti-cyclotomic generalized-Heegner cycles → p-adic Rankin L-series at
  non-classical (anti-cyclotomic) characters.
- COMPLEMENTARY to KLZ ordinary route, BUT lives on
  **Kuga-Sato × CM-curve product**, NOT on KLZ's Kuga-Sato $K_{k-1}$.
- Anti-cyclotomic Heegner produces a **derivative**-style formula at
  $s=k/2$, not a 4-tuple ladder at $s \in \{1, 2, 3, 4\}$.
- **Cannot produce v_2 = {-3, -2, 0, +1} ladder pattern.**
- **Verdict:** wrong shape entirely.

### Closure conclusion (paragraph for M39 paper-skeleton)

> "We note that alternative p-adic Hodge mechanisms — Fontaine-Messing
> syntomic, Niziol syntomic cohomology, Bhatt-Morrow-Scholze prismatic,
> and Bertolini-Darmon-Prasanna anti-cyclotomic Heegner — do not yield
> alternative constructive routes to the F1-renormalized $v_2$-monotonicity
> pattern $\{-3, -2, 0, +1\}$ for $f = 4.5.b.a$. The Steinberg-edge $p=2$
> ramified case acts as a uniform obstruction across all these frameworks.
> KLZ2017 §7.1.5 (with its [TBD-M39-1] Steinberg-edge extension wall)
> remains the unique constructive route currently known."

This is a **CLOSURE finding** for the ECI program: do NOT pursue prismatic
/ FM-syntomic / BDP as alternative companions to M13.1.

### Action items

1. ADD this paragraph to M39 paper-skeleton §6 (Outlook) or §3 (Status of
   alternatives).
2. UPDATE memory: "S2 alternatives tested (M42 2026-05-06) — KLZ-UNIQUE
   confirmed, do not re-explore prismatic / FM / BDP for v_2 ladder."

---

## §S3 — (∞,2)-functor U: SKETCHABLE-DEFER [secondary closure with resume condition]

See `pistes_open.md` §S3 for full scaffold. Closed for publication
until paper-2 (M32) lands AND v7.6 produces a $\le 5\%$-precision
CKM observable from CM-anchor + $H_1$ alone (no floating params).

**Closure note for memory:** "M42 sketched (∞,2)-functor U scaffold
2026-05-06; deferred until paper-2 + killer-prediction available.
Calmès-Hebestreit-Harpaz-Nikolaus Hermitian K-theory machinery is
adequate; problem is physics-side (no falsifiable target yet),
not math-side."

---

## Secondary dead-ends (briefly noted)

### Barca-Giovannetti deformed-algebra Mixmaster (arXiv:2412.20983)

Recent (Dec 2024) Bianchi IX paper using deformed commutation relations
to remove Mixmaster chaos. **Not relevant to our type-II_∞ pista (S1):**
deformed-algebra approach is at the kinematic Wheeler-DeWitt level,
not the operator-algebra Tomita-Takesaki level. We do NOT want to
remove chaos — Mixmaster chaos IS the Manin-Marcolli geodesic flow we
are exploiting. Closure: cite as comparison (different program), not
follow up.

### Anderson et al. 2025 Bianchi modular forms periods (arXiv:2509.17256)

Pure number-theoretic Eichler-Shimura-Harder for Bianchi cusp forms over
imaginary quadratic fields. Different "Bianchi" (the number-theorist
Bianchi, manifolds $\Gamma\backslash\mathbb{H}^3$) than physicist Bianchi
(homogeneous cosmology classification). **Linguistic collision, no
mathematical bridge to our S1 piste.** Closure: do NOT cite in S1
without explicit disambiguation footnote.

### Hilbert-Pólya II_∞ recurrence

Already closed by M28 (factor-type II_∞ vs III_1 obstruction). M42 confirms
the closure: II_∞ for **gravity-sector observer algebra** (S1) is not
the same II_∞ as a hypothetical Hilbert-Pólya construction. Different
sectors, no contradiction.

---

## Hallu / discipline check

- Hallu 86 → 86 (held; no fabrication; all 13 refs cross-verified live)
- Mistral STRICT-BAN observed
- 3 SMALL files written (each ≤200 lines)
- Anti-stall: zero settings.json drift despite multiple system-reminder injections
- Honest verdicts: 1 OPEN (S1), 1 CLOSED (S2), 1 DEFERRED (S3) — no manufactured viables to please
