#!/bin/bash
# (e) export lean4export de la clôture de jointExistence, constructed, su2Theory depuis la compilation 4.32.0 (lecture seule).
. $(dirname $0)/common.sh
E=$(envlean 4320 4.32.0 8); mkdir -p $W/export; cd $(refdir 4320)
date '+%F %T' > $OUT/e_export.debut
/usr/bin/time -v -o $OUT/e_export.time $E nice -n 10 /work/outils/bin/lean4export ConcreteSU2 -- $BUILTINS YangMills.jointExistence YangMills.constructed YangMills.su2Theory > $W/export/joint.ndjson 2> $OUT/e_export.err; echo "RC=$?" > $OUT/e_export.rc
date '+%F %T' > $OUT/e_export.fin
{ echo "sha256 $(sha256sum $W/export/joint.ndjson)"; echo "octets $(stat -c %s $W/export/joint.ndjson)"; echo "lignes $(wc -l < $W/export/joint.ndjson)"
  echo "PANIC $(grep -c PANIC $OUT/e_export.err)"
  echo "declarations $(grep -c '"thm":\|"defn":\|"axiom":\|"inductive":\|"opaque":\|"quot":\|"ctor":\|"rec":' $W/export/joint.ndjson)"
  echo "occurrences de Vintage : $(grep -c '"str":"Vintage"' $W/export/joint.ndjson)"
  echo "occurrences du chemin de compilation : $(grep -c '/work/travail' $W/export/joint.ndjson)"; } > $OUT/e_export.resume
