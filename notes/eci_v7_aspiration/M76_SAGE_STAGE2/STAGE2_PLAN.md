---
name: Stage 2 dispatch plan — F1 and R3-C-1 falsifiers
description: M76 Sage 10.7 compatibility pass; TODO breakdown by Sage-stdlib vs specialist; outreach plan
type: project
---

# Stage 2 Dispatch Plan — F1 and R3-C-1 Falsifiers (M76, 2026-05-06)

## Context

Stage 1 (numerical surrogate pi*L(f,1)/L(f,2) = 6/5 via Sage lseries) **PASSED
at 1e-16** on PC (M63, 2026-05-06). That used `Newforms(Gamma1(4), 5)`, confirmed
a_2 = -4, and called `f.lseries()`. Fully reproduced M52 PARI 80-digit result.

Stage 2 is the **Beilinson regulator + BDP Heegner distribution** computation.
Both scripts have been updated for Sage 10.7 compatibility by M76. The import
error that triggered this task (`ModularCurve` in r3_c1_falsifier.sage) has been
fixed: `ModularCurve(...)` does not exist in Sage 10.7 stdlib; replaced with
`Gamma1(4)` CongruenceSubgroup.

---

## R3-C-1 Falsifier TODO Breakdown

### SAGE-DOABLE (Kevin or Sonnet, no outreach needed)

| TODO | Description | Sage 10.7 path | Estimated effort |
|------|-------------|----------------|-----------------|
| #0   | Numerical surrogate pi*L(1)/L(2) via f.lseries() | Uncomment body in `numerical_surrogate_r3c1()` | ~1 h |
| #1   | Kuga-Sato 3-fold K_3 over Gamma1(4) | `Gamma1(4)` + dataclass; KLZ §3 affine equations | ~5 h |
| #3   | de Rham class omega_f surrogate | `f.modular_symbols(sign=1)` + KLZ §3 projection | ~5 h |

**Note on TODO #0**: Already validated as Stage 1 (M63 PC run). Code is in the
`numerical_surrogate_r3c1()` function body (commented out). Uncomment + run.

**Note on TODO #1**: `ModularCurve(Gamma1(4))` was the failing import in M63
r3_c1_falsifier.sage v1. Fixed in v2: use `Gamma1(4)` directly. The Kuga-Sato
3-fold K_3 does not need an algebraic-variety object for the falsifier; a
dataclass tracking level + cohomological data (following KLZ §3 Definition 3.1)
is sufficient as input to TODO #2 and #4.

### SPECIALIST NEEDED (external collaboration required)

| TODO | Description | Status in Sage 10.7 | Estimated effort | Outreach target |
|------|-------------|---------------------|-----------------|-----------------|
| #2   | KLZ Eisenstein-symbol classes xi_j (j=1,2) | NOT IN STDLIB | ~15-20 h | David Loeffler, Sarah Zerbes |
| #4   | Beilinson-Deligne regulator pairing to 30 digits | NOT IN STDLIB | ~15-20 h | Francois Brunault, Anton Mellit |

**TODO #2 notes**: Kings-Loeffler-Zerbes arXiv:1503.02888 §7.1. Loeffler has
unpublished Magma code. No Sage/Python port confirmed as of May 2026. A Sage
port would need: Eisenstein symbols on elliptic curves (cf. Beilinson 1985 +
Brunault 2004 explicit formula), evaluated at CM point tau = i in X_1(4)(C).

**TODO #4 notes**: Brunault-Letang arXiv:2402.03247 (2024) provides explicit
Beilinson-Kato regulator computations. Level 4 weight 5 CM case requires
adaptation from their existing examples. Contact Brunault for code availability.

**Total Sage-doable**: ~11 h
**Total specialist**: ~30-40 h
**Compute cost once implemented**: ~50-100 CPU-hr

---

## F1 Falsifier TODO Breakdown

### SAGE-DOABLE

| TODO | Description | Sage 10.7 path | Estimated effort |
|------|-------------|----------------|-----------------|
| #2   | Hecke Grossencharacter psi eigenvalue check | `f.character()` + eigenvalue check at split primes | ~3 h |

**TODO #2 notes**: For split primes p = 1 mod 4 (p != 2), verify psi(p) = a_p(f).
Sage 10.7 `HeckeCharGroup` has partial infinity-type support; eigenvalue approach
is more robust. Cross-check against LMFDB 4.5.b.a Galois representation data.

### SPECIALIST NEEDED

| TODO | Description | Status in Sage 10.7 | Estimated effort | Outreach target |
|------|-------------|---------------------|-----------------|-----------------|
| #1   | AnticyclotomicGalois(K=Q(i), p=2) | NOT IN STDLIB | ~5 h | Iwasawa theorist |
| #3   | BDP Heegner 2-adic distribution L_2^+/- | NOT IN STDLIB | ~20-30 h | Buyukboduk, Lei |

**TODO #1 notes**: p=2 is ramified in K=Q(i) (d_K = -4). Standard IMC theorems
(Hsieh 2014, Chida-Hsieh 2015, Arnold 2007, Pollack-Weston 2011) all exclude
this regime. The anticyclotomic Z_2-tower requires Lubin-Tate / formal group
construction for ramified p; de Shalit 1987 §1-2 is the reference.

**TODO #3 notes**: Core subroutine. Requires BDP 2013 arXiv:1002.4071 §3 +
Kriz 2021 arXiv:1912.02308 adaptation for p=2 supersingular ramified case.
Sage `sage.modular.pollack_stevens` module provides partial overconvergent
modular symbols but Kobayashi +/- decomposition is NOT available natively.

**Total Sage-doable**: ~3 h
**Total specialist**: ~25-35 h
**Compute cost once implemented**: ~50 CPU-hr (M44 F1 estimate)

---

## Critical Obstruction (both falsifiers)

p=2 is **ramified** in K=Q(i) and **supersingular** for f=4.5.b.a (v_2(a_2) = 2).
No existing Sage package handles BDP distributions in this regime as of May 2026.
This is the Kriz 2021 regime (arXiv:1912.02308), which extends BDP to the
supersingular + ramified case but has no canonical Sage port.

---

## Outreach Plan

### Priority 1 — David Loeffler (KLZ Eisenstein symbols, R3-C-1 TODO #2)
- Position: EPFL as of 2025 (verify current)
- Contact: david.loeffler@epfl.ch
- Ask: Is there a Sage/Python port of KLZ Eisenstein symbols at level 4?
  If not, can we get the Magma code + documentation for arXiv:1503.02888 §7.1?
- Attach: r3_c1_falsifier_v2.sage KLZ_class() stub

### Priority 2 — Kazim Buyukboduk (BDP Heegner distribution, F1 TODO #3)
- Position: University College Dublin
- Contact: kazim.buyukboduk@ucd.ie
- Ask: Is there code (any language) for BDP Heegner measure at p=2 ramified
  in the CM field? Reference arXiv:1709.02912.
- Attach: f1_falsifier_v2.sage bertolini_darmon_2adic_plus() stub

### Priority 3 — Antonio Lei (BDP, F1 TODO #3, co-author Buyukboduk-Lei)
- Position: University of Ottawa
- Contact: antonio.lei@uottawa.ca
- Same ask as Buyukboduk; they collaborated on arXiv:1709.02912.

### Priority 4 — Francois Brunault (Beilinson regulator pairing, R3-C-1 TODO #4)
- Position: ENS Lyon (verify current)
- Contact: francois.brunault@ens-lyon.fr
- Ask: Does arXiv:2402.03247 code handle level 4 weight 5 CM forms?
  Can we get the implementation for the Beilinson-Deligne pairing?

### Priority 5 — Sarah Zerbes (KLZ, R3-C-1 TODO #2)
- Position: ETH Zurich (verify current)
- Contact: via ETH math department page
- Fallback if Loeffler not responsive.

---

## Recommended Next Steps (in order)

1. **Kevin or Sonnet (1 h)**: Uncomment TODO #0 in r3_c1_falsifier_v2.sage and
   run smoke test to verify the Sage 10.7 lseries pipeline (already validated
   as M63 Stage 1 but not yet in-repo as executable code).

2. **Kevin or Sonnet (3 h)**: Implement TODO #2 of f1_falsifier_v2.sage
   (Hecke Grossencharacter eigenvalue check; fully Sage-doable).

3. **Kevin (outreach, ~1 h draft)**: Send emails to Loeffler (R3-C-1 TODO #2)
   and Buyukboduk/Lei (F1 TODO #3) referencing the stubs above.
   Use H4_OUTREACH_CONTACTS or H8_OUTREACH_EMAILS templates if available.

4. **Wait for outreach response** before attempting TODO #3 (BDP) or TODO #4
   (Beilinson regulator). These are >20 h each and require specialist code.

5. **Kevin or Sonnet (10 h)**: Once KLZ code obtained, implement R3-C-1
   TODO #1 + #3 (Kuga-Sato scaffold + de Rham class) to wire up the interface.

---

## Dispatch to PC

Scripts `f1_falsifier_v2.sage` and `r3_c1_falsifier_v2.sage` are ready for
smoke test on PC (run with `--smoke` flag):

```bash
sage f1_falsifier_v2.sage --smoke
sage r3_c1_falsifier_v2.sage --smoke
```

Expected output: both print scaffold summaries and exit cleanly without
ImportError or NotImplementedError. The `--smoke` path terminates after
newform construction (a_2 = -4 confirmed) and does NOT call any TODO stubs.

**Stage 2 readiness**: SCAFFOLDS READY. Specialist code is the blocker.
Do NOT claim "Stage 2 ready to run" until TODO #2 (KLZ) and TODO #3 (BDP)
are filled via outreach.
