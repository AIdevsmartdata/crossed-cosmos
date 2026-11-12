#!/bin/bash
# Une PASSE de compilation dans un dossier de construction NEUF, DANS le bac (leanext, réseau coupé), cwd = projet.
# usage : interne_build_passe.sh PASSE      (ex. p1, p2) ; journaux dans <copie>/journaux/
# Précautions ajoutées après le plantage du gamer du 11/11 (11h36-11h37, kernel BUG fs/buffer.c:3044) :
#  - refuse de démarrer si .lake/build existe déjà (dossier de construction neuf à chaque passe) ;
#  - à la fin : empreintes de TOUS les .olean du projet (et contrôle des fichiers vides) pour comparer deux passes ;
#  - nettoyeur des *.setup.json des modules terminés (27 Go pour YM, non cités dans les .trace de Lake).
set -u
PASSE=$1; P=$PWD; C=$(dirname "$P"); L=$C/journaux; mkdir -p $L
if [ -e "$P/.lake/build" ]; then echo "REFUS : $P/.lake/build existe (dossier non neuf)" > $L/build_$PASSE.refus; exit 3; fi
lean --version > $L/lean_version_$PASSE.txt 2>&1
( while true; do
    for ir in $P/.lake/build/ir $P/.lake/packages/*/.lake/build/ir; do
      [ -d "$ir" ] || continue
      lib=${ir%/ir}/lib/lean
      find "$ir" -name '*.setup.json' -mmin +5 -print0 2>/dev/null | while IFS= read -r -d '' f; do
        rel=${f#$ir/}; t="$lib/${rel%.setup.json}.trace"
        [ -f "$t" ] && [ "$t" -nt "$f" ] && rm -f "$f"
      done
    done
    df --output=avail -BG /work | tail -1 > $L/disque_libre.txt
    sleep 300
  done ) &
NET=$!
date '+%F %T' > $L/build_$PASSE.debut
lake build WilsonReference WilsonConstruction > $L/build_$PASSE.log 2>&1; echo "RC=$?" > $L/build_$PASSE.rc
date '+%F %T' > $L/build_$PASSE.fin
kill $NET 2>/dev/null
sync
( cd $P/.lake/build/lib/lean && find . -name '*.olean' -type f -print0 | sort -z | xargs -0 sha256sum ) > $L/empreintes_olean_$PASSE.txt
find $P/.lake/build -type f -size 0 ! -name '*.hash' > $L/fichiers_vides_$PASSE.txt
{ echo "olean $(wc -l < $L/empreintes_olean_$PASSE.txt)"; echo "vides $(wc -l < $L/fichiers_vides_$PASSE.txt)";
  echo "echecs $(grep -ac '^✖ ' $L/build_$PASSE.log)"; echo "code139 $(grep -ac 'exited with code 139' $L/build_$PASSE.log)"; } > $L/resume_$PASSE.txt
cat /sys/fs/cgroup/ym4calc.slice/$(basename "$(cut -d: -f3 /proc/self/cgroup)")/memory.peak > $L/mempeak_$PASSE.txt 2>/dev/null
date '+%F %T' > $L/TOUT_$PASSE.fin
