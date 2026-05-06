# F2 sweep — expected results (a priori)

Sub-agent M47, 2026-05-06. Hallu count 86 -> 86.

## Anchor (MUST reproduce)

`4.5.b.a`: weight 5, CM by Q(i), Steinberg edge at p=2 (a_4 = -8 = -2^3).
Per M22 derivation, F1-renormalized `v_2(alpha_m^F1)` for m=1..4 should yield:

| m | alpha_m^F1 raw form  | v_2(alpha_m^F1) |
|---|----------------------|-----------------|
| 1 | alpha_1 * (-1) * (5/4)   | -3 |
| 2 | alpha_2 * (-2) * (3/2)   | -2 |
| 3 | alpha_3 * (-4) * (2)     |  0 |
| 4 | alpha_4 * (-8) * (3)     | +1 |

Pattern: `[-3, -2, 0, +1]`, monotone increase by deltas `[1, 2, 1]`. If the
sweep does NOT reproduce this for `4.5.b.a`, there is a bug in `f1_renorm()`
or in the q-expansion fetch. Stop and debug.

## Likely sweep outcome (most probable)

`9.5.b.a`, `12.5.b.a`, `27.5.b.a`: CM by Q(omega), prime 2 SPLIT in Q(omega)
(disc -3, p=2 splits since -3 is QR mod 8 — actually -3 mod 8 = 5, and
5 is non-residue mod 8, so 2 is INERT in Q(omega)).
Hence `a_2 = 0` in Q(omega) cases (Hecke-CM rule for inert primes), and
`alpha_m` will tend to `0` -> v_2 = +inf (sentinel 9999) for all m. These
cases give **non-falsifying** rows (all v_2 = +inf, no monotone {-3,-2,0,+1}).

`16.5.b.a`, `36.5.b.a`: levels divisible by 2; p=2 ramifies; expected to
also be Steinberg-edge cases. Pattern may again hit `[-3,-2,0,+1]` -> these
rows would be flagged "STEINBERG" not "NON-STEINBERG", so they don't falsify.

`16.5.c.a`: NOT CM (per v6.0.53.1 P-NT verdict, hallu catch #75); will be
skipped or yield arithmetic in coeff-field Q(sqrt(-3)) without monotone
pattern. Non-falsifying.

`25.5.b.a`: candidate CM by Q(i) at level 25 (5^2). p=2 has good reduction;
this is the **most interesting candidate** — non-Steinberg at p=2 (a_4 != +/-4)
yet might still exhibit monotone v_2 if M13.1(c) is broader than Steinberg.

## Decisive scenarios

1. **All non-Steinberg rows show no monotone pattern** => M13.1(c)
   Steinberg-specificity SURVIVES at small-level CM scope. Confidence
   in M44.1(c) fingerprint claim **incrementally raised**.

2. **At least one non-Steinberg row matches `[-3,-2,0,+1]` (or deltas
   `[+1,+2,+1]`)** => Steinberg-specificity REFUTED. M44.1(c) needs
   reformulation; broaden scope to "F1-renormalisable CM weight-5
   newforms at sufficiently arithmetic level".

3. **LMFDB miss for >50% of candidates** => sweep inconclusive; expand
   `SWEEP_LABELS` from LMFDB CMF browse with `weight=5,cm=true`.

## Honest caveats

- The Steinberg test `is_steinberg_at_p` uses `a_{p^2} = +/- p^{(k-1)/2}`.
  M13.1(c) may use a slightly different definition; if all rows come back
  STEINBERG with no NON-STEINBERG comparator, the sweep is
  **non-decisive** and we need a wider `SWEEP_LABELS` list.
- `f1_renorm` formula matches M22 derivation as M47 reads it; if the v_2
  for `4.5.b.a` does not reproduce `[-3,-2,0,+1]`, double-check the
  `(-2^{m-1}) * (1 + 2^{m-3})` factor against M22 precise statement.
- LMFDB API rate-limit: at ~30 calls per sweep, well below limits.
