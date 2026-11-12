# Rejeu par un non-auteur (agent de montage Claude Sonnet 5.5, 12/11/2026) : programmes d'Opus relancés tels quels dans le bac à sable

Chaque programme a été relancé à partir d'une copie propre, sans modification, dans un bac à sable sans droits ni réseau ; sortie standard comparée champ par champ (JSON) à celle d'Opus.
| Programme | Code | Écarts non temporels |
|---|---|---|
| stokes run1 à run7 | 0 | run1-4, run7 : aucun (seuls les temps d'exécution diffèrent) ; run5 : résidu max 1,129e-15 contre 1,201e-15 (même ordre, indice de la pire boucle différent) ; run6 : écarts d'arrondi 4e-16 à 9e-16 |
| calculs : qc2_stein, qc_comptabilite, w_quadrature | 0 | identiques (0 champ différent) |
| calculs : stein_un_lien | 0 | arrondis relatifs ≤ 4,3e-14 (ratio 3,0413881944614 contre 3,0413881944615) |
| calculs : qsigma_cg (m ≤ 12) et qsigma_cg_m18 (m ≤ 18) | 0 | seuls les temps diffèrent |
| programmes de la note v1.0 (6 programmes) | 0 | identiques au rejeu du 11/11 sauf : temps ; `boite_projecteurs` : résidus de gradient conjugué au 10^-9 près |
Tous les programmes d'Opus ont été relancés.
