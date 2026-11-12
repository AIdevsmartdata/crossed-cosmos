#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/logicaffeine/target/arena/examples/logos_kernel
cd /work/arene
date -u +%FT%TZ > journaux/full_lg.debut
nice -n 10 /usr/bin/time -v $B --check sem --stats /work/export/joint.ndjson > journaux/full_lg.out 2> journaux/full_lg.err &
P=$!
echo $P > journaux/full_lg.pid
/work/arene/garde120.sh $P /work/arene/journaux/garde_lg.log &
wait $P
echo "RC=$?" > journaux/full_lg.rc
date -u +%FT%TZ > journaux/full_lg.fin
