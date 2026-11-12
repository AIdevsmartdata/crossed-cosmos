#!/bin/bash
# (g) Chrono.lean : durées du noyau de Lean 4.32.0 sur cinq déclarations (Chrono_run.lean = Chrono.lean + les cinq commandes).
. $(dirname $0)/common.sh
E=$(envlean 4320 4.32.0 8); cd $(refdir 4320)
run1 g_chrono $E nice -n 10 lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 $PK/nanoda_diagnostic/Chrono_run.lean
