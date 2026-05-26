# FIX R1 't Hooft twist lattice — sanity tests #1 + #2 PASS

**Auteur** : Kévin Rémondière (Independent Researcher, Oloron-Sainte-Marie)
**ORCID** : 0009-0008-2443-7166
**Date** : 2026-05-26
**Script patché** : `papers/2026-05-24-session/scripts/jax_su3_tHooft_lattice_PROPER_FIX_2026-05-26.py`
**Original (v1)** : `papers/2026-05-24-session/scripts/jax_su3_tHooft_lattice_PROPER_2026-05-26.py`

---

## 1. Diagnostic confirmé

Le script v1 testait
$$
\Omega_0 \, \Omega_1 \;\stackrel{?}{=}\; \omega \,\Omega_1\, \Omega_0,
\qquad \omega = e^{2\pi i/N}
$$
avec le choix canonique de matrices de twist
$$
\Omega_0 = \mathrm{diag}(1,\omega,\omega^2), \qquad
\Omega_1 = \text{cyclic shift } e_i \mapsto e_{i+1 \bmod N}.
$$
Multiplication directe :
- $\Omega_0\,\Omega_1$ = matrice avec entrées $\{1,\omega,\omega^2\}$ sur la diagonale décalée ;
- $\omega\,\Omega_1\,\Omega_0$ = matrice avec entrées $\{\omega,\omega^2,1\}$ (rotation **opposée**).

L'écart maximum entre les deux est exactement $|1-\omega^2| = \sqrt{3} \approx 1.7321$, ce qui correspond précisément à l'erreur observée (`1.73e+00`). La relation canonique 't Hooft–Witten est en réalité
$$
\Omega_0\,\Omega_1 \;=\; \bar\omega\,\Omega_1\,\Omega_0 \;=\; z_{01}\,\Omega_1\,\Omega_0,
\qquad z_{\mu\nu} = e^{-2\pi i n^{\mu\nu}/N},
$$
ce qui est cohérent avec la constante `Z_TWIST = exp(-2πi/N) = ω̄` déjà utilisée dans l'action.

Pour la sanity #2 (`cold start ⟨P⟩`), l'observé `0.984375 = 1 - 1/64` est obtenu par le calcul correct sur U = Id : le masque `corner` (`x_μ = L-1` AND `x_ν = L-1`) en 4D sélectionne $L^{D-2} = L^2$ plaquettes (et non 1), chacune contribuant Re Tr(z · I)/N = Re(ω̄) = -1/2. D'où
$$
\langle P\rangle_{\rm cold,tw} \;=\; 1 - \frac{1.5 \cdot L^{D-2}}{n_{\rm plaq}} \;=\; 1 - \frac{3}{D(D-1)\,L^2} \;\stackrel{D=4}{=}\; 1 - \frac{1}{4 L^2}.
$$
Pour L=4 cela donne $1 - 1/64 = 0.984375$ — match parfait.

## 2. Patch exact appliqué

**Patch A** (`check_centraliser_lemma`, ligne ~161) :
```python
# v1 (faux)  :  RHS = OMEGA_PHASE * (Om1 @ Om0)
# FIX (juste):  RHS = Z_TWIST     * (Om1 @ Om0)
```
+ diagnostic `tHooft_commutator_max_err_wrong_sign` (≈ 1.7321 si on remet le mauvais signe).

**Patch B** (`sanity_battery` test #2, ligne ~951) :
```python
# v1 :  p_cold_tw_expected = 1.0 - 1.5 / n_plaq
# FIX :  n_corner_plaq      = L ** (DIM - 2)
#         p_cold_tw_expected = 1.0 - 1.5 * n_corner_plaq / n_plaq
```
+ enregistrement de `n_corner_plaquettes` et `n_plaq_total` dans le dict de sanity.

**Patch C** : entête du module + checklist pré-vol mis à jour pour mentionner z = ω̄ et la note FIX.

Les fonctions physiques (`gather_link_twist`, `compute_staples_twisted`, `_wrap_phase_field`, `metropolis_sweep_*`) NE SONT PAS modifiées — le bug R1 était uniquement dans le test de sanity et son baseline analytique.

## 3. Vérification numérique des sanity #1 + #2

Exécution du module FIX (import direct, JAX backend) :

```
[1] Centraliser FIX :
    tHooft_commutator_max_err           = 6.47e-16     (< 1e-10  →  PASS)
    tHooft_commutator_max_err_wrong_sign = 1.7321      (diagnostic v1-bug)
    det(Ω_0) = 1.000000 , det(Ω_1) = 1.000000
    PASS_commutator = True , PASS_det0 = True , PASS_det1 = True

[2] Cold-start FIX (L=4) :
    ⟨P⟩ periodic = +1.000000   (expected 1.0)
    ⟨P⟩ twisted  = +0.984375   (expected +0.984375)
    n_corner = 16 / n_plaq_total = 1536
    PASS = True
```

Vérification croisée des valeurs attendues pour L=8,12,16 : 0.99609375 / 0.99826389 / 0.99902344 (= $1 - 1/(4L^2)$).

## 4. Recommandation

- **Quick test L=4 β=2.5 à relancer immédiatement** avec le FIX (~5 min RTX 5060 Ti). Vérifier également les sanity #3-#5 (hot ⟨P⟩ vs Sternbeck 2005, acceptance ∈ [0.3,0.7], τ_int).
- **ETA run complet 9 configurations** (L ∈ {8,12,16} × β ∈ {2.5,3.0,3.5}) :
  - Estimation conservatrice RTX 5060 Ti, ~60 thermalised configs : ≈ 3 h pour L=8, ≈ 8 h pour L=12, ≈ 22 h pour L=16.
  - Total ≈ 3·(3 + 8 + 22) ≈ **100 h sur une seule GPU** ; en parallélisant les 9 (L,β) sur 2-3 GPU ou avec batching n_decorr réduit ⇒ **3-5 jours** wall-clock end-to-end.
- Validation finale : confronter $\lambda_{\min}(M^\Omega) / m_\Omega^2$ et $C_{\rm LSI}$ aux prédictions Théorème 4.1 / 5.1.

---

*Aucune fonction physique (action, staples, Metropolis, twist BC) modifiée — seul le test de sanity et sa baseline analytique sont patchés. La conservation du flag `Z_TWIST = ω̄` confirme que l'action est correcte ; le bug R1 était local au test diagnostique.*
