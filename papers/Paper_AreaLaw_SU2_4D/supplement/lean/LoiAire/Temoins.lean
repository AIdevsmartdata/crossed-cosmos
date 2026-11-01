import LoiAire.CertPetits

/-!
# Témoins négatifs du vérificateur (noyau)

Avec un rayon légèrement trop petit (A diminué de 10⁶, soit ≈ 4·10⁻⁴ en relatif), ou un `H` constant, la MÊME
fonction `verifie` renvoie `false` : le vérificateur n'est pas trivialement vrai.
-/

namespace LoiAire

set_option maxRecDepth 100000

theorem verifie_m3_temoin_rayon : verifie 3 p_m3 (2^40) (A_m3 - 1000000) B_m3 Hmin_m3 Hmax_m3 arbre_m3.get = false := by
  decide +kernel

theorem verifie_m5_temoin_rayon : verifie 5 p_m5 (2^40) (A_m5 - 1000000) B_m5 Hmin_m5 Hmax_m5 arbre_m5.get = false := by
  decide +kernel

theorem verifie_m5_temoin_H_constant : verifie 5 p_m5 (2^40) A_m5 B_m5 Hmin_m5 Hmax_m5 (fun _ => 2^40) = false := by
  decide +kernel

end LoiAire
