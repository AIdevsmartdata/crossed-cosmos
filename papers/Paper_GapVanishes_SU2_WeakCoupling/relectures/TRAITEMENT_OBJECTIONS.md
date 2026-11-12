# Traitement des objections des relectures d'autres familles (texte final v1.3), 12/11/2026

Relectures : Sol 1 (section du taux, lemme de Stein, assemblage) ; Sol 2 (maillon le plus faible de toute la note) ; DeepSeek 1 (re-dérivation du lemme de Stein à partir de son ÉNONCÉ, constantes comprises dans l'énoncé : pas totalement « à l'aveugle » sur les valeurs) ; DeepSeek 2 (attaque des constantes ; réponse obtenue SANS raisonnement étendu : la méta indique `len_reasoning 0`, contenu 13 212 caractères, finish=stop).

| # | Source | Objection | Sort |
|---|---|---|---|
| 1 | Sol 1 (4) | lem:quat : l'estimation de la dérivée « vaut aussi pour un chemin fermé » est FAUSSE si un lien est répété (contre-exemple : plaquette parcourue deux fois, 4|sin(ga/2)| contre 0,1 à ga = 0,1) | CORRIGÉE dans le texte : seule la première estimation vaut pour un chemin ; la seconde pour les plaquettes. N'affecte ni Stein (plaquettes élémentaires) ni BCH (estimation de valeur) |
| 2 | Sol 1 (12) | lem:H2 : le centre w_n doit être le même pour les cinq espérances | CORRIGÉE : énoncé précisé (minimiseur de E min(1,X_w), X_w sur les deux observables, indépendant de φ) |
| 3 | Sol 1 (13), DS 2 | le budget « 0,41δ » n'est pas dérivable des seuls énoncés des lemmes (7δ/12 ≈ 0,583δ) | CORRIGÉE : le texte dit δ' ≤ δ suffit ; 0,59δ avec les énoncés, 0,41δ avec les comptes exacts (recalculé : 0,40706) |
| 4 | Sol 1 (8) | L = D_aF (notation) | CORRIGÉE |
| 5 | Sol 1 (15), DS 2 | « K = 1 » en collision avec K = C₂N_*² | CORRIGÉE (renommée : paramètre de largeur 1) |
| 6 | DS 2 | le terme 100gK(λ+½) du lemme BCH avec le vrai K ≈ 2·10⁶ n⁴ serait grand pour n = 16 | RÉFUTÉE pour le théorème : n_t ≥ 3·10¹¹ t⁶ ; vérifié numériquement (ratio_BCH = 1/12 à 10⁻³⁰ près, script de comptabilité) |
| 7 | Sol 2 (1) | lem:projrate : « inégalités élémentaires » cachent l'estimation de Fourier ; la constante 408 survit | CORRIGÉE à la demande du pilote : dérivation refaite par moi (multiplicateur P=E_qE_q*, |∂f̂| ≤ 2+δ, W ≤ 21) et insérée dans la preuve ; vérifiée au bac (grille fine, symboles = aPe₁₂ à 1e-15, W = 1,2066). Relecture DeepSeek de CE passage : 1er appel (ds3) INUTILISABLE : il affirme W = 45 « par quadrature » alors qu'il n'a pas d'outils (valeur inventée, contredite par W = 1,2066 et ∫|f̂|² = c(0)) ; 2e appel (ds4, consigne interdisant toute valeur numérique) : preuve analytique complète de W ≤ 3 par l'identité Σ_λ|∂_λf̂|² = s+2a(2−s), vérifiée numériquement à 1e-9 (max 2,998, moyenne 1,2058). Passage désormais « proved » |
| 8 | Sol 2 | résumé : le seuil 10^455 est attribué à la forme simplifiée | CORRIGÉE (10^455 pour (12 log t+25,23)/t, 10^537 pour 24β^{-1/120}log β) |
| 9 | Sol 2 | prop:tori : la fonction g de μ_N(fg) = μ_N(γ_E(f)g) ne doit pas dépendre de U_E | CORRIGÉE (v1.2-hérité) ; Stone–Weierstrass explicité |
| 10 | DS 1 | (aucune objection : re-dérivation concordante κ, H, B, g³) | note : l'énoncé fournissait les constantes ; l'accord sur κ = √(π/8) et la structure est indépendant, les constantes H, B sont retrouvées en suivant l'énoncé |
| 11 | Sol 1, Sol 2 | non vérifié par eux : Stein complet (Sol 2), calculs, Lean, bibliographie | dit |
Sol 1 et Sol 2 ont trouvé « aucun défaut fatal ». Sol 2 note que le résultat est déjà dans `qlab/registre/REVUES_PILOTE.md:2360` (antériorité interne).
