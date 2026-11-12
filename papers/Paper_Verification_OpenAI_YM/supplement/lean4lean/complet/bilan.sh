#!/bin/bash
C=/work/lean4lean_essai/complet
cd $C
N=$(wc -l < modules.txt)
f=$(ls rc/*.rc 2>/dev/null | wc -l)
echo "faits: $f / $N"
echo "codes 0: $(cat rc/*.rc 2>/dev/null | grep -c '^0 ')"
echo "durees cumulees (s, somme des modules): $(cat rc/*.rc 2>/dev/null | awk '{s+=$2} END{print s+0}')"
echo "codes non nuls:"
grep -L '^0 ' rc/*.rc 2>/dev/null | while read r; do m=$(basename $r .rc); echo "  $m rc=$(cut -d' ' -f1 $r) : $(grep -m1 -iE 'error|problem|mismatch|fail|PANIC' echecs/$m.log 2>/dev/null || head -1 echecs/$m.log 2>/dev/null)"; done
sha256sum /work/lean4lean_essai/src/.lake/build/bin/lean4lean
[ -e FIN ] && cat FIN
tail -1 suivi.log 2>/dev/null
