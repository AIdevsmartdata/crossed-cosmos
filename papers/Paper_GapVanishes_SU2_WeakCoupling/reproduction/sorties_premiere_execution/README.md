# Contrôles numériques de la v2 (bac qlab du sandbox host, utilisateur qlab, sans réseau) — 11/11/2026

Code écrit pour la v2, sans réutiliser le code de la v1 ni celui de Qwen. Lancement :
`python3 [internal path] --kind python --timeout S FICHIER.py > FICHIER.qlab.json`.

| Script | Sortie | Job | Ce qui est contrôlé | Résultat |
|---|---|---|---|---|
| `hodge_check.py` | `hodge_check.qlab.json` | 20261111-030646-bd781a | laplacien de Hodge des k-formes du complexe cubique (tores 3⁴, 3×4×5×3, 4⁴, 5×3×4×6), k = 0…4, = laplacien scalaire ⊗ Id, en ENTIERS ; d∘d = 0 ; témoin négatif (orientation fausse) | écart 0 partout ; mutant détecté (écart 2, d∘d ≠ 0) |
| `gauss_formules.py` | `gauss_formules.qlab.json` | 20261111-031016-be7951 | V_K (symbolique), Γ_K (numérique à 10⁻¹⁶), séries en ε = s/K, Monte-Carlo 4·10⁶ | conforme ; MC Cov à 0,5 σ. **Le balayage « forme_en_K » de ce fichier est FAUX (annulation en double précision) : ne pas citer ; voir la ligne suivante** |
| `gauss_forme_mp.py` | `gauss_forme_mp.qlab.json` | 20261111-031428-0ae359 | K ↦ V_K/Γ_K en mpmath 50 chiffres ; ρ²R = 1 + (5/4)(1−ρ²)(s/K)² + O(K⁻³) | décroissante en K, limite (s/c)² ; développement confirmé |
| `boite_projecteurs.py` | `boite_projecteurs.qlab.json` | 20261111-031016-8f3de1 | ⟨v, P_n v_t⟩ dans B_n, n = 2…6, v = F₁₂(0) − F₁₂(e₁) (sandwich des projecteurs, limite libre) | t=0 : 1,08438 ; 1,13626 ; 1,137646 ; 1,1377326 ; 1,1377449 (→ 1,1377495) ; t=1 → 0,1377451 ; t=2 → 0,0183599 |
| `ct_schwinger.py` | `ct_schwinger.qlab.json` | 20261111-032019-c988e6 | c(t), c_F(t), B(t) par représentation de Schwinger (Bessel, mpmath 60 chiffres) | c(0) = 1,13774949168 ; c_F(0) = 0,5 ; table §4 d'ATTAQUE ; t ≥ 2000 : NaN (branche scipy), non utilisé |
| (essai 1) | `ct_schwinger_essai1_plante_t1e4.qlab.json` | 20261111-031016-d827ab | même script, avant correction : planté à t = 10⁴ (série de Bessel mpmath), c(0) non imprimé | archivé tel quel |

Sommes SHA-256 : `SHA256SUMS` (ce dossier).
