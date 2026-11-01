import LoiAire.Calcul

/-! Constantes du certificat m = 11 (sans Mathlib, partagées avec l'exécutable `verifcert`). -/

namespace LoiAire

/-- p_1..p_13 en J* = 40674/100000, Q = 2^40 (fichier certificats/m11/poids_m11_J40674_100000.txt). -/
def p_m11 : List Nat := [487896913543, 348672765140, 268031351885, 216748489288, 181605857440, 156132437338,
  136863227132, 121796139246, 109700441729, 99780443822, 91499925396, 84484813690, 78536544842]
/-- ρ'* = A/B = 2639854083/2^30. -/
def A_m11 : Nat := 2639854083
def B_m11 : Nat := 1073741824
def Hmin_m11 : Nat := 663930282413
def Hmax_m11 : Nat := 1099511627776

end LoiAire
