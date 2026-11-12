#!/bin/bash
# (c) CompactCheck d'OpenAI (même commande que interne_verifs_copie.sh). usage : c_compact.sh 4320 4.32.0
. $(dirname $0)/common.sh
V=$1; T=$2; E=$(envlean $V $T 8); cd $(refdir $V)
run1 c_compact_$V $E nice -n 10 lean -j1 verification/CompactCheck.lean
