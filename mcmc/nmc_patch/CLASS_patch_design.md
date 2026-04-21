# CLASS NMC patch — equation design sheet

One-page sketch of what `source/background.c` and `source/perturbations.c`
must compute when the flag `nmc_xi_chi != 0` is set. Symbols follow CLASS
conventions: primes = d/dτ (conformal time), 𝓗 = a'/a.

## 1. Action

```
S = ∫ d⁴x √(-g) [ (M_P²/2 − ξ_χ χ²/2) R  +  ½(∂χ)²  −  V(χ) ]
```

(`derivations/D1-kg-nmc.py`, line 6–8.)

## 2. Background sector — additions to `background.c`

### 2.1 Modified Friedmann equation

The G_μν χ² piece of T_μν shifts the effective Planck mass:

```
M_P²_eff(a) = M_P² − ξ_χ χ(a)²                                        (B1)
3 M_P²_eff 𝓗² = a² [ ρ_r + ρ_m + ρ_ν + ρ_Λ(a) + ρ_χ ]                 (B2)
ρ_χ = ½ χ'²/a² + V(χ) − 6 ξ_χ 𝓗 χ χ'/a²                               (B3)
```

`ρ_Λ(a)` keeps its w0-wa CPL form from stock CLASS (so that `w0_fld`, `wa_fld`
still enter through `background_w_fld()`).

### 2.2 Klein-Gordon ODE for χ(τ)

From D1 (`derivations/D1-kg-nmc.py` eq. at line 86):

```
χ'' + 2𝓗 χ' + a²( V'(χ) + ξ_χ R χ ) = 0                               (B4)
```

with the background Ricci scalar

```
R = 6 ( 𝓗'/a² + 𝓗²/a² )                                               (B5)
```

Implementation: add two entries `pba->index_bg_chi`, `pba->index_bg_chi_prime`
to the `background_vector`; integrate (B4) alongside ρ_fld in
`background_derivs()`. Initial conditions: χ(a_ini) = χ_0, χ'(a_ini) = 0
(slow-roll start; χ_0 tuned internally so that the tracker attractor reaches
Ω_χ at a=1).

### 2.3 Consistency check to implement

`ξ_χ = 0` ⇒ (B1)–(B4) collapse to stock Friedmann + decoupled scalar.
Add `class_test(...)` that the relative deviation of `H(z)` from stock CLASS
is < 1e-10 when `xi_chi = 0`.

## 3. Perturbation sector — additions to `perturbations.c`

Work in synchronous gauge (CLASS default). Add two new members to the
perturbation y-vector: `δχ`, `δχ'`.

### 3.1 Perturbed Klein-Gordon

Linearising D1:

```
δχ'' + 2𝓗 δχ' + ( k² + a² V''(χ) + a² ξ_χ R ) δχ
   + ξ_χ a² χ δR + ½ h' χ' = 0                                        (P1)
```

where `δR` in synchronous gauge is

```
δR = −2 a⁻² [ 3𝓗 η' − k² η + ½ h'' + 𝓗 h' ]                           (P2)
```

(η, h are the CLASS metric perturbations.)

### 3.2 Perturbed stress-energy (from D2)

`derivations/D2-stress-nmc.py` gives the covariant T_μν. Linearised, the new
NMC contributions to the (δρ_χ, δP_χ, θ_χ, σ_χ) sourced by the metric via
Einstein's equations are:

```
δρ_χ^NMC  = −2 ξ_χ [ 3𝓗 χ χ'/a² · h'/2  +  χ² δG⁰₀  +  𝓗 χ δχ' · (−6) ]
δP_χ^NMC  = ⅔ ξ_χ [ χ² δG^i_i  +  2 □(χ δχ) ]
(ρ+P) θ_χ^NMC  =  −2 ξ_χ k² ( χ χ' δχ + 𝓗 χ² δχ − … )
(ρ+P) σ_χ^NMC  =  −2 ξ_χ χ² σ_metric                                  (P3)
```

(Full expressions: Hwang & Noh 2005, Eq. 38–41; hi_class `perturbations.c`
around `approx == hi_class_qs`.)

### 3.3 Modified Einstein equations

Divide the Hamiltonian constraint and the anisotropy equation by M_P²_eff(a)
rather than M_P². In practice, multiply all metric source terms in the CLASS
`perturb_einstein()` routine by `M_P²/M_P²_eff(a)`.

## 4. Numerical tolerances

- Tight `background_integration_stepsize` (<1e-3): χ'' eq. is stiff near
  radiation-matter equality.
- Add `perturbations_integration_tolerance` override for the χ sector:
  1e-5 absolute, 1e-4 relative.
- Use CLASS's `quasi_static` approximation only if |ξ_χ| < 1e-3; otherwise
  solve the full ODE.

## 5. References

- Faraoni 2000, gr-qc/0002091 (T_μν NMC).
- Hwang & Noh 2005, astro-ph/0412068 (perturbations in generalised gravity).
- Zumalacárregui+ 2017, 1605.06102 (hi_class).
- Bellini & Sawicki 2014, 1404.3713 (EFT-of-DE α_i parametrisation).

## 6. Paper cross-references

- D1 (KG equation) — `derivations/D1-kg-nmc.py`
- D2 (T_μν + trace) — `derivations/D2-stress-nmc.py`
- D3 (no-ghost ξχ²/M_P² < 1) — `derivations/D3-noghost.py`
- D4 (w0-wa mapping in NMC) — `derivations/D4-wa-w0-nmc.py`
