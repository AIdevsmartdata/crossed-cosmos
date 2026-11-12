#!/bin/bash
# Assemble main.lean = import Mathlib + sources ClayYM v1.1 (verbatim, imports retirés, section fermée) + CritereScalaire.lean
set -e
C=/root/physique/chantiers/clayym_v11/ClayYM
ICI=$(dirname "$0")
OUT=$ICI/main.lean
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
