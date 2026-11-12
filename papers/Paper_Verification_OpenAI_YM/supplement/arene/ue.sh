#!/bin/bash
export PATH=/usr/bin:/bin HOME=/work/home
B=/work/arene/nano-lean/target/release/nl-fast
cd /work/arene
$B -j 1 --trace /work/export/temoinVrai.ndjson 2>&1 | head -8
echo ----- uniformE
nice -n 10 /usr/bin/time -v $B -j 4 --axioms propext,Classical.choice,Quot.sound --declaration YM.PhysicalNext.Repeat.Luna.uniformE /work/export/joint.ndjson > journaux/uniformE_nl.out 2> journaux/uniformE_nl.err
echo RC=$?
cat journaux/uniformE_nl.out; grep -v "^	" journaux/uniformE_nl.err; grep -E "Maximum res|Elapsed" journaux/uniformE_nl.err
