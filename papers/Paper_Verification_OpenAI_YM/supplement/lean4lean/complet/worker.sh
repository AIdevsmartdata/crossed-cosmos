#!/bin/bash
# usage: worker.sh <module> ; reprise : saute si rc/<module>.rc existe
C=/work/lean4lean_essai/complet
m="$1"
[ -e "$C/rc/$m.rc" ] && exit 0
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
export LEAN_PATH=$(cat /work/lean4lean_essai/lean_path.txt)
t=$(mktemp "$C/tmp/$m.XXXXXX")
s=$(date +%s)
nice -n 10 /work/lean4lean_essai/src/.lake/build/bin/lean4lean "$m" > "$t" 2>&1
rc=$?
d=$(( $(date +%s)-s ))
[ $rc -ne 0 ] && cp "$t" "$C/echecs/$m.log"
rm -f "$t"
echo "$rc $d" > "$C/rc/$m.rc.tmp" && mv "$C/rc/$m.rc.tmp" "$C/rc/$m.rc"
