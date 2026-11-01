import LoiAire
-- (a) lemme de Perron abstrait
#print axioms LoiAire.marches_le_certificat
#print axioms LoiAire.marches_le_C_rho_pow
#print axioms LoiAire.marches_eq_pow
#print axioms LoiAire.marches_eq_sum_chemins
#print axioms LoiAire.nombre_chemins_le
-- comptage à mémoire m (lemmes 7.1, 7.2)
#print axioms LoiAire.posList_take
#print axioms LoiAire.Nwin_take
#print axioms LoiAire.Nwin_le_Ntor
#print axioms LoiAire.Gsum_le_Tpow
#print axioms LoiAire.Tpow_le
#print axioms LoiAire.borne_marches
#print axioms LoiAire.borne_marches_tout_n
-- (b) vérificateur prouvé correct, certificats m = 3, 4, 5 vérifiés par le noyau
#print axioms LoiAire.pourTous_correct
#print axioms LoiAire.verifie_correct
#print axioms LoiAire.verifiePar_correct
#print axioms LoiAire.certificat_of_verifie
#print axioms LoiAire.certificat_of_verifiePar
#print axioms LoiAire.verifie_m3
#print axioms LoiAire.verifie_m4
#print axioms LoiAire.verifie_m5
#print axioms LoiAire.certificat_m3
#print axioms LoiAire.certificat_m4
#print axioms LoiAire.certificat_m5
-- (c) arithmétique exacte
#print axioms LoiAire.theta11_eq
#print axioms LoiAire.theta11_lt_one
#print axioms LoiAire.theta13_eq
#print axioms LoiAire.theta13_lt_one
#print axioms LoiAire.theta3_lt_one
#print axioms LoiAire.theta5_lt_one
#print axioms LoiAire.q11_gt_one
#print axioms LoiAire.K11_bornes
#print axioms LoiAire.C11_bornes
#print axioms LoiAire.p_m11_decroissants
-- (d) énoncé conditionnel
#print axioms LoiAire.haarSU2_univ
#print axioms LoiAire.sitesT_eq
#print axioms LoiAire.count_sitesT
#print axioms LoiAire.prodVisites_cons
#print axioms LoiAire.prodVisites_sitesT
#print axioms LoiAire.longueur_ge
#print axioms LoiAire.GtildeA_le
#print axioms LoiAire.loi_aire_conditionnelle
#print axioms LoiAire.theoreme1_conditionnel
#print axioms LoiAire.theoreme1_de_verifiePar
#print axioms LoiAire.theoreme_m5_conditionnel
-- témoins négatifs (le vérificateur renvoie false sur des données fausses)
#print axioms LoiAire.verifie_m3_temoin_rayon
#print axioms LoiAire.verifie_m5_temoin_rayon
#print axioms LoiAire.verifie_m5_temoin_H_constant
-- faits élémentaires sur les poids (§5), démontrés
#print axioms LoiAire.Poids.hJ_pos
#print axioms LoiAire.Poids.hJ_le_one
#print axioms LoiAire.Poids.Mser_continuousOn
#print axioms LoiAire.Poids.Atilde_pos
#print axioms LoiAire.Poids.Atilde_one_le
