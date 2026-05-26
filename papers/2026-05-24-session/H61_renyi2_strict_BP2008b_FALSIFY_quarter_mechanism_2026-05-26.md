# H61 — Renyi-2 strict vs BP2008b : 1/2 × 1/2 mechanism FALSIFIED

**Verdict** : 1/2 × 1/2 = 1/4 mechanism FALSIFIED par lecture directe littérature. β=-a_4/4 reste numériquement vrai mais mechanism unclear. P(decoder) 60-70% → 45-55%.

## Verification BP2008b strict Renyi-2

Agent H61 max-effort a vérifié directement :

**BP2008b arXiv:0802.4247** :
- Eq. (5) : `S[A] = lim_{T→0} ( lim_{s→1} ∂/∂s F[A,s,T] - F(T) )`. s = replica index CONTINUOUS
- Eq. (9) : `(1/|∂A|) ∂S_f/∂l ≈ [F(l+a,2,T) - F(l,2,T)] / (a |∂A|)`. Finite-diff SPATIAL (Δl=a) PAS replica

**Rabenstein 2019 arXiv:1812.04279** (extends BP method) :
- Eq. (14) : `S^(2) = F[A,2,T] - 2F[T] = -log(Z_2/Z²)` STRICT Renyi-2 definition
- Eq. (17)-(20) : α-integration over interpolating action between two slab widths

**Conclusion** : BP/Rabenstein mesure le **strict Renyi-2** entropy S^(2) = -ln(Z_2/Z_1²) on a deformed-topology lattice. La "α-integration" est un outil pour `∂S^(2)/∂l` entre slab widths, PAS approximation finite-diff de replica index.

## Implications pour decoder

| Avant | Maintenant |
|-------|-----------|
| β = -a_4/4 PLAUSIBLE via 1/2 × 1/2 | β = -a_4/4 reste NUMÉRIQUEMENT vrai 0.06σ |
| Mechanism : (1/2 W=-1/2 ln det)·(1/2 BP finite-diff) | Mechanism : (1/2 W=-1/2 ln det)·(??? autre source 1/2) |
| P(decoder structural) 60-70% | P(decoder structural) 45-55% honest |

## Candidates pour le 1/4 mechanism (à explorer)

1. **W = -(1/2) ln det** : 1/2 confirmé Vassilevich convention
2. **Renyi-2 vs vN conversion** : pour 2D CFT S_2/S_vN = 3/8 (factor n^2-1)/(6n) à n=2 dérivée
3. **Codim 2 entangling surface** : 4D bulk → 2D area = codim 2, possible /4 from (codim/dim_bulk)^2
4. **Imaginary-time doubling** : Z_replica = Z_2 a τ_total = 2·β_thermal, possible 1/2
5. **Casini-Huerta n=2 specific** : a_Maxwell=62 sphere, A=a/(90π²) ↔ a_4 ↔ factor specific n
6. **Numerical coincidence** : -11/24 ≈ -a_4_total/4 par chance, mais Z=0.06σ rend hasard improbable

## Lattice two-width test (chained after SU(15) v2)

Script `/tmp/jax_su4_RENYI2_STRICT_vs_BP2008b_H61_2026-05-26.py` (438 lines) prêt :
- SU(4) β=43.2 L∈{4,6,8}
- Method : run α-integration at TWO consecutive slab widths l-1 et l, take difference for strict slope
- Comparison : κ_BP (single-step) vs κ_strict (two-widths)
- Expected outcome (literature) : ratio = 1.00 ± 0.10 (P=75%)
- If ratio = 2 : mechanism CONFIRMED (P=15%)
- If ratio ≠ 1 ≠ 2 : decoder needs revision (P=10%)

Chained after SU(15) v2 PID 1898835 sur pc-maison.

## Anti-fab discipline

- BP2008b arXiv:0802.4247 VERIFIED (Buividovich-Polikarpov, Nucl.Phys. B802:458-474)
- Rabenstein 2019 arXiv:1812.04279 VERIFIED
- Rindlisbacher 2022 arXiv:2211.00425 VERIFIED (overlap problem warning)
- H61 agent flagged honestly : two-width method ≠ literal SWAP_AB but cleanest implementable test

## Pourquoi this matters

C'est un **revers honest** mais pas une catastrophe :
- β = -a_4/4 reste numériquement vrai (le match 0.06σ est trop bon pour coïncidence)
- Le mechanism précis du 1/4 est unknown
- Le decoder n'est pas dead, juste qu'il y a 1 gap théorique de plus

P(decoder strucutral complete) : 45-55% honest (down from 60-70% surge over-optimisme).

## Action items

1. **Cross-check Casini-Huerta n=2 factor explicit** (1 jour) — pourrait être le 1/4 manquant
2. **Lattice two-width test** (chained, 2-4h GPU)
3. **Email Olejnik/Nakagawa raw ρ(λ)** (action humaine ROI #1)
4. **Bridge to N^{5/3} couche 3** — Berges turbulence reste mécanisme

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[H61_solodukhin_uplift_quarter_factor_2026-05-26]]
[[H62_dS_7over3_decoder_rescue_2026-05-26]]
[[correction_H51_anti_fab_vassilevich_2026-05-26]]
[[project_decoder_breakthrough_quarter_dS_7over3_2026-05-26]]
