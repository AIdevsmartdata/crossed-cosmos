#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/nano-lean/target/release/nl-fast
cd /work/arene; mkdir -p journaux
for t in temoinVrai temoinSorry temoinAxiomeUtilise temoinPoison; do
 for opt in "noaxioms" "axioms"; do
  A=""; [ $opt = axioms ] && A="--axioms propext,Classical.choice,Quot.sound"
  echo "=== $t $opt"; date -u +%FT%TZ
  nice -n 10 /usr/bin/time -v $B -j 4 $A /work/export/$t.ndjson > journaux/cal_nl_${t}_$opt.out 2> journaux/cal_nl_${t}_$opt.err
  echo "RC=$?"; tail -3 journaux/cal_nl_${t}_$opt.out; grep -v "^\s" journaux/cal_nl_${t}_$opt.err | head -5
 done
done
