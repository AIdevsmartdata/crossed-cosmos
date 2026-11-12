#!/bin/bash
# Témoins de la chaîne lean4export + nanoda, DANS le bac (leanext, réseau coupé), cwd = /work/export.
# Fichier sans import (prélude seul) : temoinVrai DOIT passer ; temoinSorry, temoinAxiomeUtilise et temoinVrai
# empoisonné (type 2+2=4 réécrit en 2+2=5 dans l'export) DOIVENT être refusés.
set -u
E=/work/export; L=$E/logs; O=$E/olean
mkdir -p $O
cp /work/nos/TemoinNanoda.lean $E/TemoinNanoda.lean
lean -o $O/TemoinNanoda.olean $E/TemoinNanoda.lean > $L/temoins_compile.log 2>&1; echo "RC=$?" > $L/temoins_compile.rc
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
for t in temoinVrai temoinSorry temoinAxiomeUtilise; do
  LEAN_PATH=$O /work/outils/bin/lean4export TemoinNanoda -- $BUILTINS $t > $E/$t.ndjson 2> $L/export_$t.err
  echo "RC=$?" > $L/export_$t.rc
done
# poison : le littéral 4 du type devient 5 (nombre de remplacements consigné)
grep -c '"natVal":"4"' $E/temoinVrai.ndjson > $L/poison_remplacements.txt
sed 's/"natVal":"4"/"natVal":"5"/' $E/temoinVrai.ndjson > $E/temoinPoison.ndjson
bash /work/outils/interne_nanoda.sh temoinVrai 1 temoinVrai
for t in temoinSorry temoinAxiomeUtilise temoinPoison; do
  bash /work/outils/interne_nanoda.sh $t 1
done
# attendu : RC=0 pour temoinVrai, RC≠0 pour les trois autres, avec la cause dans logs/nanoda_*.log
date '+%F %T' > $L/temoins.fin
