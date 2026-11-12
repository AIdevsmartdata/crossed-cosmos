#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/nano-lean/target/release/nl-fast
cd /work/arene
date -u +%FT%TZ > journaux/full_nl.debut
nice -n 10 /usr/bin/time -v $B -j 8 --axioms propext,Classical.choice,Quot.sound /work/export/joint.ndjson > journaux/full_nl.out 2> journaux/full_nl.err &
P=$!
echo $P > journaux/full_nl.pid
/work/arene/garde120.sh $P /work/arene/journaux/garde_nl.log &
wait $P
echo "RC=$?" > journaux/full_nl.rc
date -u +%FT%TZ > journaux/full_nl.fin
