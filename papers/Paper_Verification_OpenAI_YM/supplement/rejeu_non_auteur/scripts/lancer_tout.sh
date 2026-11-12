#!/bin/bash
# Lance tous les rejeux rapides. Les longs (d, e, f, g) sont détachés (un `setsid nohup` chacun) par le lanceur appelant.
. $(dirname $0)/common.sh
S=$(dirname $0)
bash $S/a_empreintes.sh
bash $S/b_verif.sh 4320 4.32.0 &
bash $S/b_verif.sh 4322 4.32.2 &
bash $S/c_compact.sh 4320 4.32.0 &
bash $S/c_compact.sh 4322 4.32.2 &
bash $S/h_vintage.sh
wait
echo "rapides finis $(date '+%F %T')" > $OUT/RAPIDES.fin
