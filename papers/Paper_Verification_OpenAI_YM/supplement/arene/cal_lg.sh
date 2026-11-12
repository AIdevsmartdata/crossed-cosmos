#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/logicaffeine/target/arena/examples/logos_kernel
cd /work/arene
for t in temoinVrai temoinSorry temoinAxiomeUtilise temoinPoison; do
  echo "=== $t"; date -u +%FT%TZ
  nice -n 10 /usr/bin/time -v $B --check sem /work/export/$t.ndjson > journaux/cal_lg_$t.out 2> journaux/cal_lg_$t.err
  echo "RC=$?"; grep -v "^	" journaux/cal_lg_$t.err | head -5
done
