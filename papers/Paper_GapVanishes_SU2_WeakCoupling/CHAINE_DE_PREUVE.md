# Chaîne de preuve de la note v1.3 (taux en volume infini), 12/11/2026. Rien de public.
Auteur : agent de montage Claude Sonnet 5.5 (non-auteur de la note, du taux et de ses lemmes). Trois étiquettes seulement :
**REFAIT** = refait par moi ligne à ligne (calcul à la main dans cette séance) ; **LU** = lu, plausible, non refait ; **NON VÉRIFIÉ** = pas lu en détail.
« Exécuté / recalculé » = a tourné au bac à sable, ce n'est jamais une preuve.

## A. Pièces du taux (section 'An explicit rate')
| Pièce | Étiquette | Ce que j'ai fait / relevé |
|---|---|---|
| lem:V (principe variationnel) | REFAIT | 4 lignes ; vaut pour tout t (T auto-adjoint, norme de T sur Ω⊥), pas besoin de t pair ; Var X est la variance sous μ |
| lem:cacc (Caccioppoli discret, facteur 2) | REFAIT | Cauchy–Schwarz + (η_x+η_y)² ≤ 2(η_x²+η_y²) + (h_x+h_y)² ≤ 2(h_x²+h_y²) : T ≤ 2S, exact |
| **lem:quat (Taylor quaternionique sans petit champ)** | **REFAIT** | |X|²=2β(1−W) ; De^Z[K]=∫e^{(1−s)Z}Ke^{sZ}ds de norme ≤ ‖K‖ ; D²e^Z somme de deux intégrales sur simplexes d'aire 1/2 (norme ≤ ‖K‖‖K'‖) ; Leibniz : ‖D²Q[h,k]‖ ≤ (Σ g|h_j|/2)(Σ g|k_j|/2) ; X−F=(2/g)∫(1−τ)D²Q(τc)[c,c]dτ ⇒ (g/4)A² ; D_hX−D_hF ⇒ (g/2)A|h|. Constantes exactes. Hypothèse implicite : le produit de 4 facteurs est pris dans l'algèbre des quaternions (norme d'opérateur = norme euclidienne), dit dans la note |
| **lem:stein (Stein)** | **REFAIT** (et indépendamment par DeepSeek à l'aveugle, voir RELECTURES) | (i) solution de Stein de l'OU : générateur tr(C∇²)−(x−m)·∇ ✓, ∇P_t f = e^{-t}/√(1−e^{-2t}) E[fZ] ✓, |E f(v·Z)| ≤ E(v·Z)₊ = 1/√(2π) ✓, ∫₀¹dx/√(1−x²)=π/2 ⇒ κ=√(π/8) ✓ (aucune dimension) ; (ii) IPP sous P avec χ lipschitzienne à support compact DANS la carte (|a_e|≤2/g<2π/g, j_g>0 sur le support) : pas de terme de bord ; ∇p=−p∇V ; (x−m)·∇u=∇uᵀC∇E_0 ✓ ; |𝓛u|≤1 ⇒ P(1−χ) ; (iii) ‖C^{1/2}r‖≤N_*Σ|r_e| (bloc diagonal ≤ N_*², via Stokes additif : Var(ζ_e)=⟨w_e,Π_n w_e⟩≤‖w_e‖²≤N_e m_e ≤ N_*²) ✓ ; ‖C^{1/2}L^T‖=1 ✓ ; (iv) ∇E_g−∇E_0=L^T(X−F)+(J_X−L)^T X ✓ ⇒ (g/4)ΣA_p²+2gN_*ΣA_p|X_p| (≤4 liens libres par plaquette) ✓ ; (v) |∇log j|=g(1/t−cot t) ≤ g²|a|/5 sur t=g|a|/2≤1 ✓ (sin t ≥ 5t/6, sin t−t cos t ≤ t³/3, recalculés sur grille) ; (vi) coupure ✓ ; (vii) moyenne sur b : E[A_p²]≤16K, E[A_p|X_p|]≤4πC_1N_* ✓ ⇒ H=(2π²+8π)C_1P_nN_*² ✓, B=D(K+κN_*√K/5) ✓, κDN_*Kg³ ✓. TV = sup sur f lisses à support compact ✓. **Rien d'incorrect trouvé.** Hypothèses non écrites relevées : (1) la loi conditionnelle de a sachant b est bien γ̃_b sous μ (lem:cond, REPRIS, vrai pour tout état de Gibbs) ; (2) K=C_2N_*² majore E|c_e|² pour TOUTES les coordonnées, y compris celles de la boucle de dix facteurs (lem:shorttree) |
| lem:shorttree (arbre court) | REFAIT (profondeur et longueur) ; exécuté n=1..5 (profondeur 5n, ℓ max 10n, N max 20n²) | cas (a)(b)(c) de la coquille vérifiés à la main ; ℓ ≤ 2·5n+1 ; N ≤ 3Lℓ avec L=2n |
| Stokes, appendice (lemme sur lequel tout repose) | **EXÉCUTÉ par ma propre implantation** (voir REJEU) ; preuve écrite : LU, la récurrence suit ce que le test exécute | deux phrases corrigées (t_r jamais constant ; e_k=(v_{k−1},v_k)) |
| lem:H2 (harmonique au second ordre) | REFAIT pour la partie Taylor/symétrie (φ paire, ∇φ impaire, z symétrique ⇒ terme du premier ordre nul ; Hess ≤ 1, 2, 1 pour φ₁, φ₂, φ₁₂ : valeurs propres de φ₁(yyᵀ−I)) ; LU pour la chaîne Caccioppoli→(512/n²)‖H‖² (constantes 256·2, 8 arêtes par sommet) | c_H recalculé (2,116·10¹⁰ ≤ 2,117·10¹⁰) |
| lem:bch2 (étape 2, moments d'ordre deux) | REFAIT | |u−u'| ≤ (g/2)A²|X|+(g²/16)A⁴ ; min(1,·) ; Markov sur |X_ℓ| (E|X_ℓ|²≤4C_2 via δ(Q)≤δ(U_p)+δ(U_p')) ; 2[50gK(λ+1/2)+4C_2/λ²] avec E A_ℓ² ≤ 100K ✓ |
| lem:projrate (vitesse grossière 408/(m−4)²) | **REFAIT** (12/11 ~09h, demande du pilote) : multiplicateur P(k)=E_qE_q*, f̂=a·Pe₁₂, |a|≤r, r|∂q|≤1, ‖∂P‖≤2/r ⇒ |∂_λf̂|≤2+δ_{λ1} ⇒ W≤21≤45 ; ‖u‖²=∫|a|²/r²=1/4 ; coupure ⇒ 408. Vérifié au bac sur grille : symboles de la note = aPe₁₂ à 1e-15 ; max r|∂q| = 1,0000 ; max|∂f̂| = 1,155 ; W = 1,2066 ; ∫|a|²/r² = 0,2500. Dérivation indépendante de GPT-6.1 Sol (même schéma, W≤21). Relecture DeepSeek de ce passage : voir TRAITEMENT_OBJECTIONS |
| Γ_G ≥ c_n²/162 ≥ c(t)²/648 ≥ 6δ | REFAIT | déterminant de I+Σ par couleur ; (1−x)^{-3/2}−1 ≥ 3x/2 ; (3/2)·9^{-5/2}=1/162 ; c_n² ≤ s₁s₂ ; |c_n−c(t)| ≤ c(t)/2 |
| Assemblage, Var ≤ 1/4+Γ_G/2, Γ ≥ Γ_G/2 | REFAIT | |x²−y²|≤2|x−y| ; 3δ'≤1,23δ≤Γ_G/2 ; (1/t)log(1+1/(2Γ_G)) ✓ |
| Corollaire (24 et 36), β₁ ≤ 10^227,73 t^120 | REFAIT / RECALCULÉ | script en arithmétique exacte, tableau dans `rejeu/comptabilite/` : aucune constante fausse |

## B. Pièces reprises des versions 1.0–1.2 (non refaites ligne à ligne par moi, sauf mention)
| Pièce | Étiquette |
|---|---|
| lem:L1 (énergie E(1−W)≤C_1/β, C_1=124) | LU (structure : convexité de log Z, borne inférieure par petites boules, borne supérieure à β/2 par chaînes temporelles, limite n→∞ ; chaque comptage |P|, |bd|, F_n, |Q| vérifié à la main) ; constante 123,7322 < 124 recalculée |
| lem:G, lem:cond, lem:OS, lem:nondeg, lem:S (limite à β→∞), lem:DLRlim, lem:hodge, (H1)-(H3) de lem:H, prop:Y, thm:A, prop:reduced, cor:cubic, cor:obs, prop:tori | NON VÉRIFIÉ par moi (lus en diagonale pour la cohérence des références seulement). Relues par d'autres dans les versions précédentes (voir DEPOUILLEMENT_RELECTURES.md de v1_2) |
| lem:free : c(t) ≥ c_* t^{-6}, c_*=6·10⁻⁵ | LU / NON REFAIT ; arithmétique de la constante (6,35…·10⁻⁵) recalculée par `constantes_verif.py` rejoué ; c(t) recalculé par `ct_schwinger.py` rejoué. **C'est la pièce qui fixe l'exposant 12 de δ∝t^{-12}** ; si c_* était faux de plus qu'un facteur 1,05 le théorème changerait (la structure en puissance de t non) |
| Rem. whichgap (m ≤ m^inv ; m_+ pour t impair) | NON VÉRIFIÉ |

## C. Relevés demandés
**Dépendances (phrase ajoutée dans la note) :** le théorème du taux n'utilise pas lem:S, lem:DLRlim ni prop:Y. Dépendance à signaler : lem:H est ÉNONCÉ « sous ν_n » (mesure limite de DLRlim) ; seules (H1) et (H2), identités valables à b fixé, servent ; (H3) n'est pas utilisée. La note le dit explicitement. Utilisés : V (+whichgap), G, cond, nondeg, L1, stokes+appendice, hodge, cacc, free, (H1)-(H2), preuve de cor:tight avec N_*.

**Hypothèses utilisées sans être énoncées (aucune fatale) :**
1. L'état μ est supposé invariant par translation de TOUT le réseau (pas seulement temporelle) : dit (G^TI, G^RP ⊂ G^TI) ; le déplacement des boucles au centre w_n, en espace ET en temps, l'utilise.
2. β ≥ 2 (lem:L1) et n ≥ 16 : écrits. g ≤ g_* est équivalent à β ≥ β₁(t).
3. Le choix de w_n dépend de μ et de β : légitime car les erreurs de Stein et de BCH sont uniformes en w (elles ne dépendent pas de la position de la boucle) ; c'est dit en une phrase de la preuve de H2, pas dans l'assemblage. À signaler à un relecteur humain.
4. La borne E|a_e|² ≤ K est appliquée aussi aux coordonnées du centre translatées : vraie car lem:shorttree vaut pour toutes les coordonnées de boîte.
**Constantes qui changent entre deux endroits :** aucune de substantielle. (i) THEOREME_TAUX.md dit « 1,988·10⁹ n⁸ » pour H alors que la valeur exacte est 1,923·10⁹ (borne grossière, juste) ; (ii) le QC annonce une somme ≤ 0,41δ avec les comptes exacts : recalculé 0,4071 ; avec l'énoncé cru de H2 (c_H/n² ≤ δ/4) la somme est 0,583δ ; il suffit de δ' ≤ δ, donc le théorème n'en dépend pas ; (iii) 79,03 dans la preuve du corollaire vs 79,0224 exact (inégalité du bon côté).
**« Il est clair que » :** aucun dans la section ; une phrase « by the additive version of Appendix A » dans la preuve du lemme de Stein (passage à Var(ζ_e) ≤ N_*²) est sèche mais la preuve existe (G4 de LEMMES.md ; je l'ai refaite : ligne ci-dessus).
**Défaut de présentation trouvé et corrigé dans v1.3 :** la première rédaction de la section annonçait « borne < 1 dès t ≥ 40, β ≈ 10^468 » ; faux. Le calcul exact donne t ≥ 78 (β₁(78) ≈ 10^454,8) pour la forme en t, et β ≳ 10^536,7 pour la forme simplifiée 24β^{-1/120}log β. Corrigé dans le texte.
**Réserve de fond :** le taux est un taux en puissance de β, astronomiquement plus faible que le taux attendu e^{-cβ} ; il est vide jusqu'à β ~ 10^455. C'est dit dans le résumé, dans §notprove et dans la remarque ajoutée.
