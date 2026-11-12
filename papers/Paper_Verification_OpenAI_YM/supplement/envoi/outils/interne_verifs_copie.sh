#!/bin/bash
# Nos contrôles et ceux d'OpenAI sur une copie compilée, DANS le bac (leanext, réseau coupé), cwd = projet de la copie.
# usage : interne_verifs_copie.sh SUFFIXE    journaux dans <copie>/journaux/ ; Usage.lean n'est pas rejoué ici.
set -u
S=$1; P=$PWD; L=$(dirname "$P")/journaux; mkdir -p $L
N=/work/nos
cp $N/Verif.lean $L/Verif.lean; cp $N/Temoin.lean $L/Temoin.lean
run1() { local n=$1; shift; date '+%F %T' > $L/$n.debut
  /usr/bin/time -v -o $L/$n.time "$@" > $L/$n.out 2> $L/$n.err; echo "RC=$?" > $L/$n.rc
  date '+%F %T' > $L/$n.fin; }
lean --version > $L/lean_version_verifs_$S.txt 2>&1
run1 verif_nous_$S lake env lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 $L/Verif.lean
run1 temoin_$S     lake env lean $L/Temoin.lean
run1 compact_$S    lake env lean -j1 verification/CompactCheck.lean
run1 joint_$S      lake env lean -j1 -DmaxHeartbeats=0 -DmaxRecDepth=4096 VerifyJoint.lean
date '+%F %T' > $L/TOUT_verifs_$S.fin
