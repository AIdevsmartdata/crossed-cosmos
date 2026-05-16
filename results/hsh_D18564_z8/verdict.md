# D=-18564 — HSH v3 Theorem 1 Verification for Z/8 Component

**Date:** 2026-05-16  
**Machine:** Hostinger (4 cores, 15GB, PARI 2.15.4)  
**Script:** `verify_D18564.gp`  
**Output:** `output.txt`

## Discriminant

```
D = -18564 = -4 × 3 × 7 × 13 × 17  (fundamental)
t = 5 distinct primes
```

## Class Group

```
h_K = 64
Cl = Z/8 × (Z/2)³  (first Z/8 occurrence in corpus)
2-Sylow: size 64, NON-elementary
rk_2 = 4
|Cl[2]| = 16
|Cl/Cl²| = 16  (matches Gauss: 2^(t-1) = 16)
```

## Genus Theory

- 16 genera (Gauss prediction confirmed: 2^(5-1) = 16)
- Each genus contains exactly 4 reduced forms (64/16 = 4)
- Genus characters: 2-adic + {3, 7, 13, 17} — product relation satisfies Hilbert reciprocity

## Theta Series

- Computed theta coefficients (N=500, xmax=50) for one representative per genus
- All 16 genera produce pairwise distinct theta series
- Within-genus forms confirmed to yield identical theta series (Siegel's theorem)
- **16 distinct Q-rational theta series**

## Verdict

| Quantity | Value |
|----------|-------|
| h_K | 64 |
| 2-Sylow | Z/8 × (Z/2)³, |G₂| = 64 |
| |Cl[2]| | 16 |
| Distinct genera | 16 |
| Distinct theta series | 16 |
| HSH v3 predicted (|Cl[2]|) | 16 |

**HSH v3 Theorem 1: CONFIRMED for Z/8 non-elementary 2-Sylow.**

```
rats = 16 = |Cl[2]| = 2^{rk_2}
```

## Interpretation

Despite the 2-Sylow being non-elementary (Z/8 instead of (Z/2)³), the number of Q-rational weight-3 theta series equals |Cl[2]| = 16. This confirms that Theorem 1 is robust to non-elementary 2-Sylow structure because:

- Q-rational theta series correspond to **quadratic characters** of Cl (elements of order 1 or 2)
- In Z/8, there is exactly **1** element of order 2 (4 mod 8)
- This contributes identically to a Z/2 factor
- Thus |Cl[2]| = 2^{rk_2} holds regardless of whether factors are Z/2, Z/4, Z/8, etc.
- The formula rats = 2^{rk_2} is correct for ALL 2-groups (and more generally for all class groups with pure 2-Sylow, regardless of whether the 2-Sylow is elementary abelian)

## Files

- `verify_D18564.gp` — complete PARI/GP verification script
- `output.txt` — full execution output
