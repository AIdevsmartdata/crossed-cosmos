#!/bin/bash
# Variante de assembler.sh pour le paquet : lit les sources ClayYM v1.1 dans ../ClayYM_v1_1_extrait (copie verbatim,
# sha256 dans ../SHA256SUMS) au lieu du chantier clayym_v11. Le texte produit est octet pour octet celui de assembler.sh.
set -e
ICI=$(cd "$(dirname "$0")" && pwd)
C=$ICI/../ClayYM_v1_1_extrait/ClayYM
OUT=${1:-$ICI/main.lean}
echo "import Mathlib" > $OUT
for f in Basic OS Gap Fake/Trivial Transfer GapQ; do
  echo "" >> $OUT
  echo "-- ===== ClayYM/$f.lean (verbatim, sha256 $(sha256sum $C/$f.lean | cut -c1-16)…, imports retirés) =====" >> $OUT
  echo "section  -- enveloppe : borne la portée des 'open' (open scoped ContDiff définit la notation ω)" >> $OUT
  grep -v '^import ' $C/$f.lean >> $OUT
  echo "" >> $OUT
  echo "end  -- ferme le 'noncomputable section' de ClayYM/$f.lean" >> $OUT
  echo "end  -- ferme l'enveloppe" >> $OUT
done
echo "" >> $OUT
echo "-- ===== CritereScalaire.lean (ce chantier) =====" >> $OUT
echo "noncomputable section" >> $OUT
cat $ICI/CritereScalaire.lean >> $OUT
echo "" >> $OUT
echo "end" >> $OUT
sha256sum $OUT
