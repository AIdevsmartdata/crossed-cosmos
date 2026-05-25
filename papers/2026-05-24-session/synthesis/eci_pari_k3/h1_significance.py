"""
Significance test for the apparent k=6 match:
  sum_{p=3}^17 Tr(Frob | H^2) = 284
  Σ_first 14 primes = 281
  Diff = 3, relative 1.07%

Is this significant or coincidence?
- 9 partial sums tested
- Each compared with closest Σ_j primes (j ∈ 1..30 say)
- Closest within ~3% is "luck" probability?

Adversarial null: simulate random a_p sequences with Sato-Tate
distribution and see how often we find sum-partial close to Σ first k primes.
"""

import numpy as np
from sympy import sieve

np.random.seed(42)

# Real data partial sums
data_traces = [6, -26, 14, 22, -42, 310, 38, 46, -74, 62, -218, 838, 86, 94]
data_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

prime_seq = list(sieve.primerange(2, 500))
sum_primes_first_k = [sum(prime_seq[:k]) for k in range(1, 50)]
print("Sum of first k primes (first 20):", sum_primes_first_k[:20])
print()

# Real match analysis: best partial sum + best k
real_matches = []
for j_end in range(1, len(data_traces)+1):
    partial = sum(data_traces[:j_end])
    # find best k
    best_k = min(range(1, 50), key=lambda k: abs(sum_primes_first_k[k-1] - partial))
    diff = abs(sum_primes_first_k[best_k-1] - partial)
    rel_diff = diff / max(abs(partial), 1)
    real_matches.append((j_end, partial, best_k, sum_primes_first_k[best_k-1], rel_diff))

print("REAL Fermat quartic K3 partial sums vs Σ first k primes:")
print(f"{'j (sum to p_j)':<14} {'partial':<10} {'best k':<7} {'Σ_k primes':<12} {'rel err':<8}")
for j, p, k, s, r in real_matches:
    print(f"{j:<14} {p:<10} {k:<7} {s:<12} {r*100:.2f}%")

# Best match overall
best_real = min(real_matches, key=lambda x: x[4])
print(f"\nBest real match: j_end={best_real[0]}, k={best_real[2]}, rel_err={best_real[4]*100:.3f}%")

print()
print("="*70)
print("Null hypothesis: random a_p with same magnitudes")
print("="*70)
# Use ACTUAL p's but RANDOM signs and ranges (within Weil bound)
# More fair: use bootstrap RESAMPLED data
# Or use random Gaussian a_p ~ N(0, sigma_p) with sigma_p ~ p (Sato-Tate variance)

n_trials = 5000
min_rel_errs = []
for trial in range(n_trials):
    # Sample random traces with same magnitudes as real, random signs
    fake_traces = [np.random.choice([-1, 1]) * abs(t) for t in data_traces]
    # Or fully random within Weil bound:
    # fake_traces = [np.random.uniform(-22*p, 22*p) for p in data_primes]
    matches = []
    for j_end in range(1, len(fake_traces)+1):
        partial = sum(fake_traces[:j_end])
        best_k = min(range(1, 50), key=lambda k: abs(sum_primes_first_k[k-1] - partial))
        diff = abs(sum_primes_first_k[best_k-1] - partial)
        rel = diff / max(abs(partial), 1)
        matches.append(rel)
    min_rel_errs.append(min(matches))

min_rel_errs = np.array(min_rel_errs)
print(f"Null distribution (random signs preserving magnitudes), {n_trials} trials:")
print(f"  Mean best match rel_err: {min_rel_errs.mean()*100:.2f}%")
print(f"  Std: {min_rel_errs.std()*100:.2f}%")
print(f"  Real best rel_err: {best_real[4]*100:.3f}%")
print(f"  Fraction of trials with rel_err <= real ({best_real[4]*100:.3f}%): {np.mean(min_rel_errs <= best_real[4])*100:.2f}%")

# More aggressive null: fully random a_p within Weil bound
print()
print("Null with full Weil-bounded random a_p:")
np.random.seed(123)
n_trials = 5000
min_rel_errs2 = []
for trial in range(n_trials):
    fake_traces = [np.random.uniform(-22*p, 22*p) for p in data_primes]
    matches = []
    for j_end in range(1, len(fake_traces)+1):
        partial = sum(fake_traces[:j_end])
        best_k = min(range(1, 50), key=lambda k: abs(sum_primes_first_k[k-1] - partial))
        diff = abs(sum_primes_first_k[best_k-1] - partial)
        rel = diff / max(abs(partial), 1)
        matches.append(rel)
    min_rel_errs2.append(min(matches))

min_rel_errs2 = np.array(min_rel_errs2)
print(f"  Mean best match rel_err: {min_rel_errs2.mean()*100:.2f}%")
print(f"  Std: {min_rel_errs2.std()*100:.2f}%")
print(f"  Fraction of trials with rel_err <= real ({best_real[4]*100:.3f}%): {np.mean(min_rel_errs2 <= best_real[4])*100:.2f}%")

# So if 50%+ of random trials beat the real result, this is INSIGNIFICANT
# If 5% or less, this is significant at 2sigma

print()
print("="*70)
print("Verdict on H1:")
print("="*70)
if np.mean(min_rel_errs <= best_real[4]) > 0.20:
    print("INCONCLUSIVE / LIKELY COINCIDENCE")
    print(f"  Real best match (k=6: sum a_p=284 vs Σ_14=281, 1.07%) is comparable")
    print(f"  to what's expected from random Sato-Tate traces.")
elif np.mean(min_rel_errs <= best_real[4]) > 0.05:
    print("WEAKLY SIGNIFICANT (1-2 sigma)")
else:
    print("STRONGLY SIGNIFICANT (>2 sigma)")
