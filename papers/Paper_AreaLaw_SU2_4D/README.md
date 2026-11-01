# An area law for four-dimensional SU(2) lattice gauge theory up to β ≈ 0.813

Version 1.0 (1 November 2026). Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

This is a stand-alone note. It is deposited on Zenodo as its own record (version 1.0), related to the crossed-cosmos programme record
[10.5281/zenodo.19686398](https://doi.org/10.5281/zenodo.19686398) by `isPartOf`; it is not a version of that record. A companion note
of the same author, [10.5281/zenodo.23856414](https://doi.org/10.5281/zenodo.23856414) (Dobrushin uniqueness for β < 2/9; its
Section 7 proves an area law for β < 2/3 by a different method), is cited in it.

This folder is self-contained. It holds:
- `note/`: the note (PDF, 21 pages, and LaTeX source);
- `supplement/`: the programs of the proof, the weights, the outputs, the independent checks, the memory-11 certificate
  (compressed, see below) and a Lean 4 project (`supplement/lean/`, a partial formalisation, see below).
  `supplement/README.md` describes every file.

## Statement

Let L ≥ 3 and β ≥ 0. On the torus (Z/LZ)⁴, the SU(2) Wilson measure is proportional to exp(−β Σ_p (1 − ½ Re Tr U_p)) with normalised
Haar measure on each link (β = 4/g²). Write W_γ = ½ Tr U_γ.

**Theorem 2.1 (computer-assisted).** Let J* = 40674/100000, β* = 2J* = 0.81348, ρ'* = 2639854083/2³⁰ and
θ* = J*ρ'* = 53686712485971/53687091200000 = 1 − 7.0540…·10⁻⁶. Put C* = K₀/(1 − θ*) with K₀ = 3.97805… (so C* = 5.6393…·10⁵). For
every β ∈ [0, β*], every L ≥ 3 and every planar rectangular loop γ with sides R and T such that 1 ≤ R ≤ L/2 and 1 ≤ T ≤ L − 1,

  |⟨W_γ⟩| ≤ C*^T θ*^(RT).

The constants depend neither on L nor on β. Corollary 2.2: for 0 < β ≤ β*, the string tension (defined with R → ∞) is at least
−log θ* = 7.05…·10⁻⁶ > 0; the bound also holds for every weak limit point of the torus measures. Remark 2.3: with a memory of 13 steps
the same argument gives β ≤ 0.81498 (θ = 1 − 3.1044…·10⁻⁶, C = 1.7002…·10⁶); its certificate (4.4 GB) is not supplied, and the
statement is a remark for that reason.

**Method.** The proof follows the method of Borgs and Seiler (1983, Appendix B): the slab decomposition of Durhuus and Fröhlich, a
random-walk expansion of the slab σ-models and the positivity of the transfer matrix, which yields the range β < 12/17 ≈ 0.7059.
It is refined in two ways. (I) The ratio of slab partition functions is controlled by a strict operator inequality, where the
constant comes from the Peter–Weyl spectrum (the spin-0 mode is extremal), followed by a site-by-site Cauchy–Schwarz factorisation.
(II) The weighted walks are counted with a memory of 11 steps, through a transfer matrix on 7 821 056 symmetry classes whose spectral
radius is bounded by an integer Perron certificate. Every numerical inequality of the proof is verified in exact integer or rational
arithmetic, and the certificate is re-verified by two further programs, one of them written separately for an adversarial
verification.

## What is new and what is not

To our knowledge, the widest explicit confinement range already published for the SU(2) Wilson theory in four dimensions is
β < 12/17 ≈ 0.7059, stated by Borgs and Seiler (Commun. Math. Phys. 91 (1983) 329, eq. (II.55), p. 343, proved in their Appendix B,
pp. 373-377). It concerns correlations of Polyakov loops at every temperature and every magnetic coupling; the authors do not state a
bound for each rectangular loop. This note **refines the threshold of the Borgs–Seiler method** from 12/17 to 0.81348 (+15.2 %), with
bounds for each rectangle on tori, uniform in the volume. It is not an independent method. Tomboulis (arXiv:0707.2179) claims
confinement for all values of the coupling in a preprint that has not been published; Ito and Seiler (arXiv:0803.3019) discuss gaps and
open problems in its argument. It is not counted here as an established range. Fröhlich (1980) announced without proof an estimate
equivalent to β < 4/5 (in the reading discussed in the note); 0.81348 lies above it and below 0.8222, the value of a non-backtracking
heuristic formulated in the note.

## Status and limitations

- **Computer-assisted, verified by machine only.** The analytic part is proved on paper; its numerical inputs are verified in exact
  arithmetic and re-verified by other programs, written with independent implementation choices or in separate sessions. The proof
  and the certificates were checked by independent programs and by adversarial reviews carried out by language models. **No human has
  read the proof**; it has not been refereed. It is formalised in Lean only in part (next section): the analytic reduction, the
  monotonicity lemma and the enclosures of the weights are assumed there.
- Tori only (the factor per site uses exactly six links per site; the trace formula uses periodicity). In infinite volume, only the
  weak limit points of torus measures are covered. Planar rectangular loops only. Strong coupling only: nothing is claimed about the
  continuum limit or the Yang–Mills mass gap. The string tension obtained near the threshold is tiny, and the bound is non-trivial
  only for R above about 1.9·10⁶ at β*.
- The literature search is not exhaustive. Not consulted: Seiler's Lecture Notes in Physics 159 (1982);
  Brydges–Giffen–Durhuus–Fröhlich (1986) beyond its abstract; Guerra–Immirzi–Marra (1978), known only through Borgs–Seiler.
  MathSciNet and zbMATH were not queried and no specialist was consulted.

## Lean formalisation (partial)

`supplement/lean/` is a Lean 4 project (Lean 4.34.0, Mathlib v4.34.0) that states Theorem 2.1 for the Wilson measure on the torus
and proves part of its proof. The exact boundary:

- **Proved in the Lean kernel** (axioms `propext`, `Classical.choice`, `Quot.sound` only; no `sorry`, no `native_decide`; also accepted by the
  independent kernel nanoda, 43 458 declarations): the combinatorial part of the proof (Perron-type bound on the weighted walk counts, window
  and torus lemmas, step-by-step reading of the weights, length of the walks, geometric series); the correctness of the certificate checker for
  every function `H`; the certificates of memory 3, 4 and 5 by `decide +kernel` (memory 3 and 4: β ≤ 0.79718, above 12/17; memory 5:
  β ≤ 0.80438); the final arithmetic (θ*, K₀, C*); and the junction theorem `theoreme1_de_verifiePar`.
- **Established by compiled execution** (trust: the Lean and C compilers, not the kernel): the memory-11 certificate, on all 6¹¹ raw states.
- **Assumed** (the three fields of the structure `HypothesesBS`): the analytic reduction |⟨W⟩| ≤ 2^T G̃^T (Sections 3 and 4 of the note), the
  monotonicity of Lemma 5.1, and the certified bounds on the weights (Proposition 5.4(1)).

The commands to rebuild and check it (about 17 GB of memory at the peak) are in `supplement/README.md`.

## The memory-11 certificate

`supplement/data/certificat_h_m11_J40674_100000.bin.xz` (8 780 360 bytes, SHA-256
`776f4f27be0aabb32ec81050883448b4004db11289b2a1cf338614e188bbc1e4`) is the certificate of Theorem 2.1 compressed with `xz -9e`. Unpacked
it is `certificat_h_m11_J40674_100000.bin`: 125 136 920 bytes, SHA-256
`b50d3769b0ea17d1da13f4e870a7786407192a9885ecceb390ef18cde50cf142`, the fingerprint printed in Section 9 of the note. A raw file of this
size cannot be stored on GitHub (limit 100 MB); the Zenodo record that archives this release also carries the raw file.

```
cd supplement/data
xz -dk certificat_h_m11_J40674_100000.bin.xz          # -k keeps the .xz file
echo "b50d3769b0ea17d1da13f4e870a7786407192a9885ecceb390ef18cde50cf142  certificat_h_m11_J40674_100000.bin" | sha256sum -c -
cd ..
gcc -O3 -fopenmp -o certification/verif_cert certification/verif_cert.c
certification/verif_cert 11 data/poids_m11_J40674_100000.txt data/certificat_h_m11_J40674_100000.bin
```

The last command (about 20 s on 4 cores) must end with `CERTIFICAT VALIDE`. The certificate can also be regenerated from the
programs, byte for byte (`certification/tm_cert 11`, about 20 s, under 0.5 GB); the commands and the other reproduction steps are in
`supplement/README.md`. The whole `SHA256SUMS` list of this folder can be checked with `sha256sum -c SHA256SUMS` from this folder.
The fingerprint of the unpacked certificate is also in `SHA256SUMS`, on a comment line, because the unpacked file is not part of the
repository.

## Compiling the note

```
cd note
pdflatex area_law_su2_4d_v1_0.tex        # three passes
```

## License, citation, AI use

- **License.** CC BY 4.0 (note, programs and data).
- **Citation.** See `CITATION.cff`, and the Zenodo record that archives this release (the note, a zip of this folder and the
  certificate).
- **AI use.** The proof, the programs and the note were prepared with the assistance of AI models (Claude Opus 5.5, Anthropic; Kimi
  K3.1 Pro, Moonshot AI; DeepSeek V4 Pro, DeepSeek); their roles are described in the section "Use of AI" of the note.
