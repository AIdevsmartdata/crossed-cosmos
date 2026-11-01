import LoiAire.Certificat
import LoiAire.DonneesM11Calcul

/-!
# Données du certificat m = 11 (théorème 1 de PREUVE.md)

Valeurs recopiées de `certificats/m11/poids_m11_J40674_100000.txt` et de l'en-tête/queue de
`certificats/m11/certificat_h_m11_J40674_100000.bin` (vérifiées à l'exécution par `VerifCert`).
La proposition `CertificatPerron 11 …` n'est PAS démontrée dans le noyau : elle est établie par l'exécution
compilée de `verifiePar 2 11 p_m11 (2^40) A_m11 B_m11 Hmin_m11 Hmax_m11 Hof` (voir `VerifCert.lean`),
dont la correction (`certificat_of_verifiePar`) est, elle, démontrée dans le noyau pour toute fonction `Hof`.
-/

namespace LoiAire

def J_m11 : ℚ := 40674 / 100000

/-- L'énoncé établi par le programme compilé `verifcert`. -/
def CertificatM11 : Prop := CertificatPerron 11 p_m11 (2 ^ 40) A_m11 B_m11 Hmin_m11 Hmax_m11

end LoiAire
