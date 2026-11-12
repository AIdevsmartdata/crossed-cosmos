#!/bin/bash
# Mutants (6) compiles en parallele sous Lean 4.32.0 ; chacun doit ECHOUER (code non nul).
set -u
R=/work/lean_zn_rejeu_1112; J=$R/out
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8
ulimit -s 1048576 2>/dev/null
LP=$(cat $R/leanpath4320.txt)
for f in $R/src/mut_*.lean; do b=$(basename $f .lean)
 ( LEAN_PATH=$LP nice -n 10 timeout 1700 lean $f > $J/$b.out 2>&1; echo "RC=$?" >> $J/$b.out ) &
done
wait; echo DONE > $J/FIN_mutants
