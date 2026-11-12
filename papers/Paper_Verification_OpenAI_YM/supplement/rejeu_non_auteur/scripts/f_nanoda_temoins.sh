#!/bin/bash
# (f) chaîne de témoins lean4export + nanoda : les scripts du paquet (interne_temoins_nanoda.sh, interne_nanoda.sh) avec les
# seuls chemins adaptés (/work/export -> dossier de rejeu, /work/nos -> paquet, /work/outils/interne_nanoda.sh -> copie adaptée).
. $(dirname $0)/common.sh
X=$W/temoins; mkdir -p $X/logs $X/bin
sed "s#/work/export#$X#g; s#/work/nos#$PK/envoi/nos#g" $PK/envoi/outils/interne_nanoda.sh > $X/bin/interne_nanoda.sh
sed "s#/work/export#$X#g; s#/work/nos#$PK/envoi/nos#g; s#/work/outils/interne_nanoda.sh#$X/bin/interne_nanoda.sh#g" $PK/envoi/outils/interne_temoins_nanoda.sh > $X/bin/interne_temoins_nanoda.sh
diff $PK/envoi/outils/interne_nanoda.sh $X/bin/interne_nanoda.sh > $OUT/f_diff_chemins_nanoda.txt
diff $PK/envoi/outils/interne_temoins_nanoda.sh $X/bin/interne_temoins_nanoda.sh > $OUT/f_diff_chemins_temoins.txt
cd $X
env -i PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LC_ALL=C.UTF-8 LEAN_NUM_THREADS=4 nice -n 10 bash $X/bin/interne_temoins_nanoda.sh > $OUT/f_temoins.out 2> $OUT/f_temoins.err; echo "RC=$?" > $OUT/f_temoins.rc
for t in temoinVrai temoinSorry temoinAxiomeUtilise temoinPoison; do echo "== $t : $(cat $X/logs/nanoda_$t.rc) ; $(grep -a -m3 -E 'Checked|Error|assertion|panicked' $X/logs/nanoda_$t.log | tr '\n' '|')"; done > $OUT/f_resume.txt
echo "remplacements du poison : $(cat $X/logs/poison_remplacements.txt)" >> $OUT/f_resume.txt
