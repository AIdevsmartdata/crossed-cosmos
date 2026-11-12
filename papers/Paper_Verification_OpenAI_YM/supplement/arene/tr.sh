#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/nano-lean/target/release/nl-fast
cd /work/arene
date -u +%FT%TZ > journaux/trace_nl.debut
nice -n 10 /usr/bin/time -v $B -j 1 --trace --axioms propext,Classical.choice,Quot.sound /work/export/joint.ndjson > journaux/trace_nl.out 2> journaux/trace_nl.err &
P=$!; echo $P > journaux/trace_nl.pid
/work/arene/garde120.sh $P /work/arene/journaux/garde_trace_nl.log &
wait $P; echo RC=$? > journaux/trace_nl.rc; date -u +%FT%TZ > journaux/trace_nl.fin
