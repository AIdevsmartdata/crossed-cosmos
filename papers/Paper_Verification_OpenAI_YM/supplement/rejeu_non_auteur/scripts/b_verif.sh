#!/bin/bash
# (b) notre Verif.lean (axiomes des trois théorèmes) et les témoins truqués ; usage : b_verif.sh 4320 4.32.0   |   b_verif.sh 4322 4.32.2
. $(dirname $0)/common.sh
V=$1; T=$2; E=$(envlean $V $T 8); P=$(refdir $V)
cd $P
run1 b_verif_nous_$V $E nice -n 10 lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 $PK/envoi/nos/Verif.lean
run1 b_temoin_$V     $E nice -n 10 lean $PK/envoi/nos/Temoin.lean
$E lean --version > $OUT/b_lean_version_$V.txt 2>&1
