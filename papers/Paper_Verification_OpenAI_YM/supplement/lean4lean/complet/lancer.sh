#!/bin/bash
# Pilote : lancer par  setsid nohup runuser -u lean -- env -i PATH=/usr/bin:/bin HOME=/work/home bash -c "ulimit -n 1048576; nice -n 10 bash /work/lean4lean_essai/complet/lancer.sh" > pilote.log 2>&1 < /dev/null &
C=/work/lean4lean_essai/complet
cd $C; mkdir -p rc echecs tmp
cp /work/lean4lean_essai/tous_modules.txt modules.txt
N=$(wc -l < modules.txt); echo "attendus=$N" > attendus.txt
rm -f FIN
( while [ ! -e FIN ]; do
    f=$(ls rc/*.rc 2>/dev/null | wc -l); e=$(grep -L '^0 ' rc/*.rc 2>/dev/null | wc -l)
    echo "$(date -u +%FT%TZ) faits=$f/$N echecs=$e memdispo_Go=$(free -g | awk '/Mem:/{print $7}')" >> suivi.log
    sleep 60
  done ) &
SUIVI=$!
grep -vxFf <(ls rc 2>/dev/null | sed 's/\.rc$//') modules.txt > restants.txt
# phase 1 : 4 processus sur 8 modules pour mesurer la memoire
head -8 restants.txt | xargs -P 4 -n 1 bash $C/worker.sh
echo "phase1 finie $(date -u +%T) memdispo_Go=$(free -g | awk '/Mem:/{print $7}')" >> suivi.log
tail -n +9 restants.txt | xargs -P 20 -n 1 bash $C/worker.sh
total=$(ls rc/*.rc | wc -l); ok=$(cat rc/*.rc | grep -c '^0 ')
echo "fin $(date -u +%FT%TZ) total=$total ok=$ok attendus=$N" > FIN
kill $SUIVI 2>/dev/null
