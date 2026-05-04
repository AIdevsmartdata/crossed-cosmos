# G1.6 Sign Resolution Report

ECI v7-R&D | 2026-05-04

---

## Verdict

**TRANSCRIPTION ERROR IN TASK PROMPT — the LMFDB a(p) values listed for 4.5.b.a at p=13 and p=29 are impossible from CM theory. Corrected values match H2's construction exactly (5/5). No twist, no construction bug.**

---

## G1.6.A — Construction of 3̂,2(5) in H2

### Formula used

`build_2hat_prime_5.py` transcribes the following formula for Y_3̂,2^(5) (reconstructed from NPP20 arXiv:2006.03058, Appendix D via pdftotext):

```
comp[0] = (3/2)(εθ^9 − 2ε^5θ^5 + ε^9θ)
comp[1] = (√3/2)(−ε^2θ^8 + ε^6θ^4)
comp[2] = (√3/2)(−ε^4θ^6 + ε^8θ^2)
```

with θ = Θ_3(2τ), ε = Θ_2(2τ) as in NPP20 eq. (3.3), expanded in q_4 = exp(iπτ/2).

### NPP20 Appendix D cross-check

The H2 agent's anti-hallucination report (committed to `build_2hat_prime_5.py`) documents:

1. The PDF was fetched from `https://arxiv.org/pdf/2006.03058` and App D extracted via pdftotext. The multi-column LaTeX layout produced scrambled output; the formula was reconstructed by:
   - Parity check: all monomials have total q_4-degree 10 (weight 5 × 2). ✓
   - ε-degree is odd in every monomial (hatted sector). ✓
   - Three components → transforms as 3̂. ✓
   - Numerical Hecke eigenvalue closure verification (sympy, N=400 terms).

2. No transcription bug was identified in the formula itself. The sympy computation confirms eigenvalue closure at all five test primes p ∈ {5, 13, 17, 29, 37} with eigenvalues:

| p | λ_H2(p) |
|---|---------|
| 5 | −14 |
| 13 | −238 |
| 17 | +322 |
| 29 | +82 |
| 37 | +2162 |

---

## G1.6.B — Theoretical analysis of the sign-flip pattern

### Observed pattern (from task prompt)

The task prompt stated LMFDB 4.5.b.a has:

| p | a(p) (task prompt) | λ_H2(p) | ratio |
|---|---|---|---|
| 5 | −14 | −14 | +1 |
| 13 | +238 | −238 | −1 |
| 17 | +322 | +322 | +1 |
| 29 | −82 | +82 | −1 |
| 37 | +2162 | +2162 | +1 |

### Character search

A systematic search over all fundamental discriminants D with |D| ≤ 1000 was performed using the Kronecker symbol χ_D(p) = (D|p). The condition χ(5)=+1, χ(13)=−1, χ(17)=+1, χ(29)=−1, χ(37)=+1 is satisfied by exactly five discriminants with |D| ≤ 500:

| D | cond | χ(5) | χ(13) | χ(17) | χ(29) | χ(37) |
|---|---|---|---|---|---|---|
| +21 | 21 | +1 | −1 | +1 | −1 | +1 |
| −84 | 84 | +1 | −1 | +1 | −1 | +1 |
| −271 | 271 | +1 | −1 | +1 | −1 | +1 |
| −359 | 359 | +1 | −1 | +1 | −1 | +1 |
| +229 | 229 | +1 | −1 | +1 | −1 | +1 |

The smallest-conductor match is **χ_21 = (21|·)**, the Kronecker symbol for Q(√21). Explicitly:

- χ_21(13) = (21|13) = (3|13)·(7|13) = (−1)·(−1) = −1 ✓
- χ_21(29) = (21|29) = (3|29)·(7|29) = (2|29)·(1|29) = +1·... wait, let me restate:

  By QR: (3|13) = (13|3)·(−1)^{(3−1)(13−1)/4} = (1|3)·(−1)^6 = 1 [no sign since 3≡3 mod 4, 13≡1 mod 4]. (3|13) = (13 mod 3|3) = (1|3) = 1. Then (7|13): (7|13) = (13|7)·(−1)^{...}... direct computation: 7 mod 13 = 7, and 7^6 mod 13 = (7^2)^3 = 49^3 ≡ 10^3 = 1000 ≡ 12 ≡ −1 mod 13, so (7|13) = −1. Therefore (21|13) = (3|13)(7|13) = 1·(−1) = −1. ✓
- χ_21(29) = (21|29): (3|29) = (29|3)(−1)^{(2)(28)/4} = (2|3)·(−1)^{14} = (−1)·1 = −1. (7|29) = (29|7)(−1)^{(6)(28)/4} = (1|7)(−1)^{42} = 1·1 = 1. So (21|29) = (−1)(1) = −1. ✓

### Twist level obstruction

A genuine modular form twist f ⊗ χ_D changes the level:
- 3̂,2(5) lives on Γ(4) (level 4).  
- χ_21 has conductor 21. If 3̂,2(5) = 4.5.b.a ⊗ χ_21, the twisted form has level 4·21²/gcd(4,21)² = 1764 ≠ 4.
- Similarly χ_{−84} has conductor 84: level would be 4·84²/4² = 1764.

**Therefore 3̂,2(5) cannot be a genuine twist of 4.5.b.a regardless of which χ_D is chosen.** The sign pattern in the task prompt must have a different explanation.

---

## G1.6.C — CM eigenvalue analysis: the real culprit

### 4.5.b.a is CM by Q(i)

The form 4.5.b.a (weight 5, level 4, nebentypus χ_4, dim 1) has CM by Q(i). For p ≡ 1 mod 4, write p = a² + b² with a odd. The Hecke eigenvalue from the Grössencharacter ψ is:

```
a(p) = ψ(π) + ψ(π̄) = 2 · Re(π^(k−1)) = 2 · Re((a + bi)^4)
```

Direct computation:

| p | a (odd) | b (even) | (a+bi)^4 | 2·Re = a(p) |
|---|---|---|---|---|
| 5 | 1 | 2 | −7 − 24i | **−14** |
| 13 | 3 | 2 | −119 − 120i | **−238** |
| 17 | 1 | 4 | +161 − 240i | **+322** |
| 29 | 5 | 2 | +41 + 840i | **+82** |
| 37 | 1 | 6 | +1081 − 840i | **+2162** |

### The impossible values

For p=13, the CM formula gives 2·Re(π^4) = **−238** for *every* choice of Gaussian prime π above 13 (since Re((a+bi)^4) = Re((b+ai)^4) = Re((−a+bi)^4), etc.). No choice of Gaussian prime gives 2·Re(π^4) = +238. This was verified exhaustively over all (a,b) with a²+b²=13.

Likewise for p=29: 2·Re(π^4) = +82 for all choices. The value −82 is impossible.

**The correct eigenvalues of LMFDB 4.5.b.a are a(13) = −238 and a(29) = +82** — identical to H2's λ(13) = −238 and λ(29) = +82.

### Source of error in the task prompt

The task prompt's LMFDB table:

```
p:    5    13    17    29    37
a(p): −14  +238  +322  −82   +2162
```

The values at p=13 and p=29 are sign-flipped relative to what CM theory requires. This is not a known LMFDB database error (LMFDB is authoritative); rather, the task prompt's listing appears to have transposed the sign convention somewhere in the chain from LMFDB → agent prompt → report. The true LMFDB 4.5.b.a values (as derivable from CM) are:

```
p:    5    13    17    29    37
a(p): −14  −238  +322  +82   +2162
```

which match H2's construction **exactly, 5/5**.

---

## G1.6.D — Construction bug assessment

No construction bug was found in H2's transcription of the NPP20 Appendix D formula. The H2 formula for Y_3̂,2^(5) is correctly reconstructed from the PDF, and the resulting sympy eigenvalues are consistent with the unique CM Grössencharacter of weight 5, level 4, Q(i)-CM. The formula produces the correct Hecke eigenform.

---

## Specific character χ

If a character explanation is still needed for the sign difference between H2 and the (incorrect) task-prompt LMFDB table, the smallest-conductor match is:

**χ_21 = Kronecker symbol (21|·), the quadratic character of Q(√21), conductor 21.**

χ_21(5) = +1, χ_21(13) = −1, χ_21(17) = +1, χ_21(29) = −1, χ_21(37) = +1.

But this is a character describing a data-entry discrepancy in the task prompt, not a genuine mathematical twist relation between modular forms.

---

## LMFDB label of twisted form

Not applicable: no genuine twist exists (the twisted form would have level 1764, not level 4). The correct identification is:

**3̂,2(5) ≡ 4.5.b.a** (same newform, same level 4, same weight 5, same nebentypus χ_4, same Grössencharacter — exact match 5/5 after correcting the task prompt's sign errors at p=13 and p=29).

---

## Corrected eigenvalue table

| p | λ_H2(p) | a(p)_4.5.b.a (corrected) | Match |
|---|---|---|---|
| 5 | −14 | −14 | ✓ |
| 13 | −238 | −238 | ✓ |
| 17 | +322 | +322 | ✓ |
| 29 | +82 | +82 | ✓ |
| 37 | +2162 | +2162 | ✓ |

**5/5 exact match. No twist. No construction bug.**

---

## Files

- `/tmp/agents_v647_evening/G16/verify_match.py` — corrected sympy script producing matching eigenvalues
- `/tmp/agents_v647_evening/H2/build_2hat_prime_5.py` — H2 construction (no bug found)
- `/tmp/agents_v647_evening/H2/closure_table.md` — H2 eigenvalue table (correct)

---

## Anti-hallucination record

- CM eigenvalues computed directly from (a+bi)^4 for p = a²+b² (exact integer arithmetic, no sympy needed).
- Exhaustive check: all Gaussian integers with a²+b²=13 and a²+b²=29 tested; ±238 and ∓82 verified impossible.
- Kronecker symbol χ_21(p) computed from definition (Legendre symbols mod 3 and mod 7 via QR).
- No LMFDB URL could be fetched directly (WebFetch permission denied); LMFDB values were derived from CM theory rather than scraped. The LMFDB label 4.5.b.a is taken from the task prompt; its description (weight 5, level 4, chi_4, CM by Q(i), dim 1) is consistent with the standard classification.
- arXiv:2006.03058 (NPP20) reference verified via API in the G1 infrastructure (`gate_g1_hatted.py`).
