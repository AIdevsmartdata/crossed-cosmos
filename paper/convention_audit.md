# Convention audit — ECI v4.4

Scan of `paper/*.tex` and `derivations/D*.py` for sign / metric / unit
consistency against the conventions block declared in `paper/eci.tex`
§2 ("Conventions", line 83).

Paper conventions (reference):
- Metric signature: mostly-plus `(−,+,+,+)`.
- NMC sign (Faraoni): Lagrangian carries `−½ ξ R χ²` (i.e. `ξ > 0` is attractive);
  scalar EOM carries `+ ξ R χ` (explicitly: `□χ − V'(χ) − ξ R χ = 0`).
- Planck mass: reduced `M_P = (8π G)^{−1/2} = 2.435 × 10^{18}` GeV.
- Natural units: `ℏ = c = 1`.
- Time: cosmic `t` for background; conformal `η` only in perturbation equations.

---

## Check 1 — Metric signature (mostly-plus)

Paper declaration: `(−,+,+,+)` (eci.tex:83).

Grep targets: `-g_{\mu\nu}`, `+g_{tt}`, explicit mention of `(+,-,-,-)` or
`(-,+,+,+)`.

Findings:

| file | line | finding | status |
|---|---|---|---|
| eci.tex | 83 | "mostly-plus metric signature `(−,+,+,+)`" — declaration | OK |
| derivations/D2-stress-nmc.py | 74 | `flat-space schematic, metric signature -+++` | OK (consistent) |
| derivations/D2-stress-nmc.py | 78 | `g^μν G_μν = −R  (signature −+++)` | OK (correct in any signature, 4D) |
| derivations/D2-stress-nmc.py | 84 | `signature -+++ → metric trace = 4` | OK |
| derivations/D2-stress-nmc.py | 89 | `In Faraoni convention (−+++ signature)` | OK |
| derivations/D7-ppn-xi-bound.py | 51 | `The action is (Jordan frame, signature −+++)` | OK |
| eci.tex | 87 | `∫ d⁴x √(-g)` + `(∂φ)²` with `-½ (∂φ)²` | OK (mostly-plus: kinetic is `−½ g^{μν} ∂_μφ ∂_νφ`, which is `+½ φ̇²` for time-like derivatives) |
| all others | — | no `+g_{tt}` or `(+,-,-,-)` patterns found | OK |

**Verdict: CLEAN. 7 explicit confirmations, 0 violations.**

---

## Check 2 — NMC sign convention (Faraoni)

Paper declaration (eci.tex:83): `−½ ξ R χ²` in Lagrangian; `+ξ R χ` in field
equation, with full EOM `□χ − V'(χ) − ξ R χ = 0`.

Paper references:
- eci.tex:88 — action: `− ½ ξ_χ R χ²` ✓
- eci.tex:95 — EOM: `□χ − V_χ'(χ) − ξ_χ R χ = 0` ✓
- eci.tex:109 — no-ghost: `M_{P,eff}² = M_P² − ξ_χ χ²` ✓
- section_3_5:15 — action: `−(ξ_χ/2) R χ²`, with `F(χ) = M_P² − ξ_χ χ²` ✓
- section_3_6:8 — coupling stated as `ξ_χ R χ²/2` (magnitude; the `−` sign
  sits in the full Lagrangian, as in §2). ✓

Derivation scripts:

| file | line(s) | form used | matches Faraoni? |
|---|---|---|---|
| D1-kg-nmc.py | 6, 48, 57, 77–80 | L contains `(M_P²/2 − ξχ²/2) R`; EOM `□χ − V'(χ) − ξ R χ = 0`; explicit assert vs Faraoni reference form | YES |
| D2-stress-nmc.py | 61 | `T_nmc = ξ [G_μν χ² + g_μν □(χ²) − ∇μ∇ν(χ²)]` with overall `+ξ` after r.h.s. transfer | YES (matches eci.tex line 104) |
| D2-stress-nmc.py | 90 | comment: "Faraoni writes: ξ[Rχ² + 3□(χ²)] using ξ > 0 and R appears with + in his convention." | YES |
| D3-noghost.py | 5–14, 45 | `M_P_eff² = M_P² − ξ χ²`, no-ghost `ξ χ² / M_P² < 1` | YES |
| D4-wa-w0-nmc.py | — (symbolic) | uses `+ξ_χ R χ` in KG via D1 | YES (inherited) |
| D7-ppn-xi-bound.py | 51 | `F(χ) = M_P² − ξ χ²`, DEF framework | YES |
| D8-swampland-nmc-cross.py | 10–14 | `δM_P² ≡ ξ_χ χ₀²` positive shift magnitude | YES |
| D9-wa-numerical.py | 97–107 | `chi_pp = -(3 + dlnH_dN) chip - Vp/H2 - xi * R * chi / H2` → `□χ − V' − ξ R χ = 0` | YES |

**Verdict: CLEAN. All 8 derivation scripts use Faraoni convention. No sign flips
detected.**

---

## Check 3 — Planck mass (reduced M_P = 2.435×10^18 GeV)

Paper declaration: `M_P = (8π G)^{−1/2} = 2.435 × 10^{18}` GeV.

Grep: `M_P`, `M_\mathrm{Pl}`, `M_{Pl}`, `M_pl`, `2.4(35)? ?.?×? ?10\^{18}`, etc.

Findings:

| file | usage | value | OK? |
|---|---|---|---|
| eci.tex:83 | declaration | `M_P = 2.435 × 10^{18}` GeV | ✓ |
| eci.tex:123 | `ρ_Λ / M_P^4 ≃ 8×10^{-121}` | reduced-Planck convention | ✓ |
| section_3_5:* | all `M_P` | reduced | ✓ |
| section_3_6:32 | `M_P ≃ 2.4×10^{18}` GeV | reduced | ✓ |
| D8-swampland-nmc-cross.py:64 | `M_P_GeV = 2.435e18` | reduced | ✓ |
| D2-stress-nmc.py:105 | `Mp_sq = symbols(r'M_P^2', positive=True)` | symbolic, reduced context | ✓ |
| D9-wa-numerical.py:65 | `MP = 1.0  # Planck mass = 1` | natural unit M_P=1 (reduced implicit) | ✓ |

No `M_{Pl}` / `M_pl` (non-reduced) strings found in `paper/` or
`derivations/*.py`. The only occurrence of "M_pl" in the broader tree is
inside the RAG cache (`_rag/Montero2022.txt`, Montero et al.'s own usage),
which is external and not edited.

**Verdict: CLEAN. Reduced M_P = 2.435×10^18 GeV used uniformly across
paper and scripts.**

---

## Check 4 — Natural units (ℏ = c = 1)

Paper declaration: `ℏ = c = 1` (eci.tex:83).

Grep: `\hbar`, `c^2`, explicit dimensional `ℏc` factors.

Findings:

| file | line | occurrence | verdict |
|---|---|---|---|
| paper/*.tex | — | no `\hbar`, no `c^2`, no explicit dimensional factors | CLEAN |
| D6-deltaNeff-kk.py | 168 | `hbar_c_GeV_m = 1.973e-16   # ħc in GeV·m` | INFORMATIONAL — used only as a numerical conversion factor (GeV ↔ m) when converting the KK-scale length `ℓ ~ 1/T` from inverse-energy to metres; does NOT violate `ℏ = c = 1` (both sides of `ℓ_EW = ℏc / T_EW` remain numerically correct). No action. |
| all other D*.py | — | no `\hbar`, no `c^2` | CLEAN |

**Verdict: CLEAN. ℏ = c = 1 enforced; D6's `hbar_c` constant is a display-unit
conversion, not an equation-of-motion factor. No patch required.**

---

## Check 5 — Time convention (cosmic t vs conformal η)

Paper declaration: cosmic `t` for background; conformal `η` only in
perturbation equations.

Findings:

| file | line | usage | verdict |
|---|---|---|---|
| eci.tex | 83 | declaration | — |
| eci.tex | 57 | `V_φ` "active at `z_c ~ 3500`" (redshift, background) | OK |
| section_3_5:66 | `3H χ̇ = −V' − ξ R χ`, Klein–Gordon with `H = ȧ/a` and cosmic-time dot | OK (cosmic t, background) |
| D9-wa-numerical.py | 84–107 | uses `N = ln(a)` (e-fold time), which is cosmic-time-derived; `dlnH_dN` | OK (background era) |
| D4-wa-w0-nmc.py | — | matter/DE era KG in e-folds | OK (background) |
| all tex/py | — | no `\eta` / conformal-time usage outside perturbation context; paper currently has no perturbation-era displayed equation, so the η-vs-t dichotomy has no active site in v4.4 | N/A |

**Verdict: CLEAN. All displayed equations are background-era; cosmic `t` (or
e-fold `N`) throughout. The conformal-time clause is declarative; no
perturbation equation currently sits in the paper to stress-test it.**

---

## Summary

| check | issues found | patched |
|---|---|---|
| 1. Metric signature (−,+,+,+) | 0 | 0 |
| 2. NMC sign (Faraoni) | 0 | 0 |
| 3. Reduced Planck mass | 0 | 0 |
| 4. Natural units ℏ = c = 1 | 0 (1 informational note on `D6` hbar_c conversion constant) | 0 |
| 5. Cosmic vs conformal time | 0 | 0 |

**Overall verdict: CLEAN.** All 5 convention checks pass across 3 tex files
and 10 derivation scripts. No sign flips, no Planck-mass mismatches, no
implicit ℏ/c factors, no time-variable misuse. No patches applied to
`derivations/*.py`; no commits in the `v4.4:conv:` family required.

### Recommendations for v4.5

1. If a perturbation-era displayed equation is added (e.g. for the CMB /
   growth cross-check of the NMC band), the cosmic-vs-conformal convention
   should be stated inline at the equation's first use.
2. D6's `hbar_c_GeV_m` constant could be renamed `GEVM_CONV_FACTOR` or
   commented `# unit conversion only; natural units ℏ=c=1 enforced in EOMs`
   to pre-empt a future reviewer's confusion. Low priority.
3. Add a brief note in the `§Conventions` subsection that derivation
   scripts (`derivations/D*.py`) all use the same conventions, with a
   pointer to this audit.
