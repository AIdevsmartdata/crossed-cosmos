# Supplementary material, version 1.1: tilted bound

This folder accompanies version 1.1 of the note "An area law for four-dimensional SU(2) lattice gauge theory up to β ≈ 0.813"
(Section 5.5, "A tilted bound", and Section 6.6, "Tilted certificates"). It adds to the supplementary material of version 1.0, which is
unchanged; the weights file at J* = 40674/100000 is `supplement/data/poids_m11_J40674_100000.txt` of version 1.0. Comments and messages
in the programs are in French. SHA-256 fingerprints of every file are in `SHA256SUMS`. Notation as in the note: tilt e^η = a/b on the
steps ±e1, rate σ_η, P = 2^30 ρ'.

## `certification/`

| file | role |
|---|---|
| `cert_incline11.c` | tilted transfer operator with memory m ≤ 12 on the FULL state space D^m (no symmetry reduction), power iteration, integer vector H = max(1, ⌈2^40 h/h_max⌉), P = ⌈2^30 ρ_fl (1+10^-9)⌉ + 1, exact check of Σ_d c_d p_min(N,13) H(next) ≤ P·2^10·a·b·H(s) in 128-bit integers (c_+e1 = a², c_-e1 = b², c_d = ab otherwise); writes H as little-endian uint64, indexed by the base-6 code with the most recent step as leading digit |
| `b7_verif11.py` | second program, written separately by the same author with independent implementation choices: reversed digit order, H read through the digit permutation, successors and window counts recomputed from the digits, exact check with 22-bit limbs in int64 (no 128-bit arithmetic), by blocks; `--temoin` stops at the first block containing a violation |
| `b7_constantes.py` | θ = J P/2^30, K0, C = K0/(1−θ²) in exact rationals; σ_η = η − log θ and log C in Arb balls at 128 and 256 bits (python-flint), with precision and `ctx.cap` guards; usage `b7_constantes.py <folder of cert_J*_a*_b*.json> <folder of weights files>` |

## `checks/`

| file | role |
|---|---|
| `table4_fractions.py`, `table4_fractions.txt` | second computation of the constants of Table 4, written separately during the review of the draft (another Claude instance): exact fractions and 60-digit decimal logarithms, no Arb; also R_min on odd tori (constant 2 K0/(1−θ)); same values as `b7_constantes.py` |

## `data/`

| file | content |
|---|---|
| `poids_m11_J40500_100000.txt`, `poids_m11_J40000_100000.txt`, `poids_m11_J35294_100000.txt` | weights files of Table 2 of the note (β ≤ 0.81, 0.80, 0.70588), as in version 1.0; `c1_poids_exacts.py` regenerates them byte for byte |
| `cert_J<J>_a<a>_b<b>.json`, `..._execution.log` | output of `cert_incline11` (m = 11) for the five rows of Table 4 and for the run at η = 0 (J = 40674, a = b = 1) |
| `verif_J<J>_a<a>_b<b>.json` | output of `b7_verif11.py` for the same six runs (zero violations on 362 797 056 states each) |
| `temoin_negatif_J40674_a251_b250.json` | negative control with P lowered by 10^-5 (relative): violations, return code 1 |
| `controles_unite/` | controls at the unit level: P − 5 fails for the five rows of Table 4; at η = 0 the new vector passes with P = A = 2639854083 and fails with A − 1; regenerated H at η = 0 has the fingerprint of `SHA256_H.txt` |
| `SHA256_H.txt` | SHA-256 of the six vectors H (2 902 376 448 bytes each), which are deposited, compressed with `xz -9e`, in the Zenodo record of version 1.1 (`H_J<J>_a<a>_b<b>.bin.xz`; too large for GitHub) |
| `constantes_m11.json`, `table_tilted_m11.json` | constants of Table 4 (θ, σ_η, K0, C, R_min), with the guards |
| `verif_cert_published_m11.log` | re-check, for version 1.1, of the published memory-11 certificate of version 1.0 with the published `verif_cert.c` (command and SHA-256 of the files in the log): "CERTIFICAT VALIDE", A = 2639854083 |
| `validation_bs_cert_incline11.txt` | `cert_incline11` with the weights of Borgs and Seiler and η = 0: ρ1 = 17/6, ρ3 = 2.786995498, ρ5 = 2.765374896 |

## Commands

Run in this folder, after copying `poids_m11_J40674_100000.txt` from `supplement/data/` into `data/` (`H.bin` is a 2.9 GB output file;
the second command needs about 11 GB of memory and takes about 35 s on 8 cores):

```
gcc -O3 -fopenmp -o certification/cert_incline11 certification/cert_incline11.c -lm
certification/cert_incline11 11 data/poids_m11_J40674_100000.txt 201 200 H.bin
python3 certification/b7_verif11.py 11 data/poids_m11_J40674_100000.txt 201 200 H.bin 2639868799
sha256sum H.bin        # must match H_J40674_a201_b200.bin in data/SHA256_H.txt
python3 certification/b7_constantes.py data data
python3 checks/table4_fractions.py data
```

Instead of regenerating it, the vector can be unpacked from the Zenodo record of version 1.1: `xz -dk H_J40674_a201_b200.bin.xz`
(2 902 376 448 bytes), then the third and fourth commands are run with `H_J40674_a201_b200.bin` in place of `H.bin` (the third reads the
vector by blocks and takes about 15 minutes).

The other rows of Table 4: (J, a, b) = (40674, 251, 250), (40500, 10, 9), (40000, 5, 4), (35294, 7, 4); control run (40674, 1, 1).
The runs used Python 3.14.4, numpy, python-flint 0.9.0 and gcc 15.2.0 on x86-64, without machine-specific compiler options; on another
platform the floating-point iteration may round differently, which gives another valid certificate (if it passes the check) with
slightly different H_min, P and constants.

## The two certificates at η = 0

An integer certificate is a pair (vector, integer) for which the inequality holds exactly. `tm_cert` (version 1.0) takes the smallest
integer admissible for its vector: A = 2639854083. `cert_incline11` takes P = ⌈2^30 ρ_fl (1+10^-9)⌉ + 1 with 2^30 ρ_fl = 2639854082.44,
hence P = 2639854087. With the vector of `cert_incline11`, the smallest admissible integer is also A (see `data/controles_unite/`).
Both certificates are valid; Theorem 2.1 of the note uses the published one.
