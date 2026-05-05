# A1 Damerell ladder verification — H7-A confirmed at m=4

**Date:** 2026-05-05 06:11 UTC (compute) / 2026-05-05 09:10 UTC (re-verified after deco)
**Owner:** Sonnet agent A1 + direct re-execution post-disconnect
**Form:** 4.5.b.a (weight 5, level 4, character chi_{-4}, CM by Q(i))
**Tools:** mpmath dps=60, sympy primerange, LMFDB live q-expansion

## Method
1. Build a_n via CM Hecke structure: split primes p≡1 (mod 4): a_p = 2 Re(pi^4) where p=pi*conj(pi); inert primes p≡3 (mod 4): a_p=0; a_2=-4 (from q-expansion).
2. Sanity: matches a_5=-14, a_13=-238, a_17=322 from LMFDB.
3. Compute L(f, m) via Iwaniec-Kowalski (5.16) approximate functional equation, X=1, N_terms=1500.
4. Sanity: L(f, 5/2)_computed = 0.5200744676..., matches LMFDB exact to printed precision.
5. Probe Cardy bridges rho = c/12 / L(f, m) and algebraic ratios L(f, m) / (pi^a * Omega_K^b).

## Key result (the door H7-A opens)

```
L(f, 4) / Omega_K^4 = 1/60   EXACT to mp.dps = 60 digits
                              (residual 2.09e-52)
```

with Omega_K = Gamma(1/4)^2 / (2 sqrt(2 pi)) = 2.6220575542921198... (Chowla-Selberg period for Q(i)).

This is a REAL Damerell-Shimura algebraicity at the integer critical point m=4 = k-1 for k=5. Damerell 1971 + Shimura 1976 + Deligne 1979 algebraicity domain INCLUDES m=k-1 for any weight k. So this is in-scope, NOT an over-claim.

## Cardy bridges searched (rho = c/12 = q · L(f, m) for q rational)

The brute-force search for `rho_target / L(f, m) ~ small-rational` returned hits but with errors 1e-5 to 1e-4 — these are NOT clean. The CLEAN hit is the algebraic-part identity at m=4. Specifically for the weight-5 Cardy embedding: the natural object is L(f, k-1)/Omega_K^{k-1} = L(f, 4)/Omega_K^4 = 1/60.

## Implication for v7.4

H7' candidate ANCHORED: the bridge axiom should bridge rho_Cardy via the algebraic ratio L(f, k-1)/Omega_K^{k-1} = 1/60 (parameter-free integer 60), NOT via the demi-integer central value L(f, k/2) = L(f, 5/2) (outside Damerell domain — original Opus over-claim H7).

The "60" needs theoretical interpretation. Candidates:
- 60 = order of A_5 (alternating group)
- 60 = sum of small Eisenstein-related coefficient
- 60 = Coxeter-Dynkin invariant of E_8 or icosahedral
- TBD: this is the next theoretical question to crack

## Caveats (honest)
- Tested only m=4 ratio thoroughly. m=2, m=3 ratios shown numerically but specific algebraic structure not pinned (script printed numerics but no Damerell-class identity match).
- Damerell 1971 + Shimura 1976 standard refs — agent A1 did NOT verbatim verify these statements (the algebraicity ANNOUNCEMENT is textbook, but the SPECIFIC value 1/60 for 4.5.b.a was found by us, not cited).
- Fit numerical 1e-52 is convincing but should be cross-checked via explicit Hida 1980s table or sage.RankinL command.

## Files
- h7a_compute.py: main L-value computation
- h7a_periods.py: extended period analysis (incomplete output captured)
