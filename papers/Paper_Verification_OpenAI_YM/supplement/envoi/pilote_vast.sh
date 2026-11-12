#!/bin/bash
# Pilote des vérifications sur la machine louée (utilisateur lean, environnement vidé). Chaque phase écrit ses journaux
# et un fichier .fin dans /work/etat. Étages : A (passe 1) ; puis B, B2, C, D, E ensemble ; puis F et G ensemble.
set -u
export LC_ALL=C.UTF-8
W=/work; E=$W/etat; O=$W/outils; mkdir -p $E
NP=$(nproc); MEMG=$(awk '/MemTotal/{print int($2/1048576)}' /proc/meminfo)
CG=$(cat /sys/fs/cgroup/memory.max 2>/dev/null || echo max)
if [ "$CG" != max ] && [ -n "$CG" ]; then c=$((CG/1073741824)); [ $c -lt $MEMG ] && MEMG=$c; fi
min(){ [ $1 -lt $2 ] && echo $1 || echo $2; }
TA=${THREADS:-$(min $((NP*2/3)) $((MEMG/2)))}
TD=$(min $((NP/2)) $((MEMG*2/5)))
TG=$(min $((NP/3)) $((MEMG/4)))
echo "coeurs=$NP memoire=${MEMG}Go TA=$TA TD=$TD TG=$TG" > $E/reglages.txt
NS=""; unshare -rn true 2>/dev/null && NS="unshare -rn"
echo "isolation réseau pendant la compilation : ${NS:-AUCUNE (espaces de noms indisponibles dans ce conteneur)}" > $E/isolation.txt
ulimit -s 1048576 2>/dev/null || true
( while true; do echo "$(date +%T) dispo=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)Go cg=$(( $(cat /sys/fs/cgroup/memory.current 2>/dev/null || echo 0)/1073741824 ))Go charge=$(cut -d' ' -f1 /proc/loadavg) $(grep -s oom_kill /sys/fs/cgroup/memory.events | tr '\n' ' ') disque=$(df --output=avail -BG $W | tail -1 | tr -d ' ')"; sleep 30; done ) >> $E/memoire.log 2>&1 &
MEMLOG=$!
envtc(){ echo "PATH=$W/tc/$1/bin:/usr/bin:/bin HOME=$W/home LEAN_NUM_THREADS=$2 LC_ALL=C.UTF-8"; }
P0=$W/travail_4320/OpenAI-YM-20261028; J0=$W/travail_4320/journaux
empreintes(){ # $1 = passe ; recalcule empreintes et résumé après une reprise
  ( cd $P0/.lake/build/lib/lean && find . -name '*.olean' -type f -print0 | sort -z | xargs -0 sha256sum ) > $J0/empreintes_olean_$1.txt
  find $P0/.lake/build -type f -size 0 ! -name '*.hash' > $J0/fichiers_vides_$1.txt
  { echo "olean $(wc -l < $J0/empreintes_olean_$1.txt)"; echo "vides $(wc -l < $J0/fichiers_vides_$1.txt)"; echo "echecs_reprise $(grep -ac '^✖ ' $J0/build_$1_reprise.log)"; } > $J0/resume_$1_reprise.txt; }
passe(){ # $1 = passe, $2 = fils
  ( cd $P0 && env $(envtc 4.32.0 $2) $NS bash $O/interne_build_passe.sh $1 )
  if ! grep -q 'RC=0' $J0/build_$1.rc 2>/dev/null; then
    ( cd $P0 && env $(envtc 4.32.0 $(( $2/2 ))) $NS lake build WilsonReference WilsonConstruction > $J0/build_$1_reprise.log 2>&1; echo "RC=$?" > $J0/build_$1_reprise.rc )
    empreintes $1
  fi
  cp $J0/resume_$1*.txt $J0/build_$1*.rc $E/ 2>/dev/null; }
# ---------- A. passe 1 sous Lean 4.32.0, dossier neuf
date '+%F %T' > $E/A.debut
passe p1 $TA
date '+%F %T' > $E/A.fin
if ! grep -qs 'RC=0' $J0/build_p1.rc $J0/build_p1_reprise.rc; then echo "passe 1 en échec, reprise comprise : arrêt" > $E/ARRET; date '+%F %T' > $E/FIN; kill $MEMLOG; exit 1; fi
# ---------- B. contrôles (les nôtres, puis les trois fournis par OpenAI)
( cd $P0 && env $(envtc 4.32.0 8) $NS bash $O/interne_verifs_copie.sh 4320
  ( cd $P0 && /usr/bin/time -v -o $J0/usage_4320.time env $(envtc 4.32.0 4) $NS lake env lean -j1 -DmaxHeartbeats=0 verification/Usage.lean > $J0/usage_4320.out 2> $J0/usage_4320.err; echo "RC=$?" > $J0/usage_4320.rc )
  date '+%F %T' > $E/B.fin ) &
PB=$!
# ---------- B2. [block removed from this publication: it compiled two files unrelated to this report]
( true
  date '+%F %T' > $E/B2.fin ) &
PB2=$!
# ---------- C. noyau indépendant : témoins, export de toute la clôture, rejeu nanoda
( cd $W/export && env $(envtc 4.32.0 4) $NS bash $O/interne_temoins_nanoda.sh
  date '+%F %T' > $E/C_temoins.fin
  cd $P0 && env $(envtc 4.32.0 8) $NS bash $O/interne_export.sh joint YangMills.jointExistence YangMills.constructed YangMills.su2Theory
  ls -la $W/export/joint.ndjson > $W/export/logs/joint_taille.txt 2>&1; grep -c '"str":"Vintage"' $W/export/joint.ndjson > $W/export/logs/joint_vintage.txt 2>&1
  date '+%F %T' > $E/C_export.fin
  cd $W/export && env $(envtc 4.32.0 4) $NS bash $O/interne_nanoda.sh joint 24 YangMills.jointExistence YangMills.JointExistence YangMills.su2Theory
  date '+%F %T' > $E/C.fin ) &
PC=$!
copie(){ # $1 = dossier ; sources seules + dépendances épinglées sans leurs constructions
  mkdir -p $1 && cp -r $W/src/OpenAI-YM-20261028 $1/ && rm -rf $1/OpenAI-YM-20261028/.git
  mkdir -p $1/OpenAI-YM-20261028/.lake/packages
  for p in $P0/.lake/packages/*; do tar -C $P0/.lake/packages -cf - --exclude="$(basename $p)/.lake" $(basename $p) | tar -C $1/OpenAI-YM-20261028/.lake/packages -xf -; done
  cp $P0/lake-manifest.json $1/OpenAI-YM-20261028/lake-manifest.json; }
# ---------- D. recompilation complète sous Lean 4.32.2 (Mathlib et dépendances depuis les sources), puis contrôles
( copie $W/travail_4322; echo 'leanprover/lean4:v4.32.2' > $W/travail_4322/OpenAI-YM-20261028/lean-toolchain
  ( cd $W/travail_4322/OpenAI-YM-20261028 && env $(envtc 4.32.2 $TD) $NS bash $O/interne_build_4322.sh )
  date '+%F %T' > $E/D.fin ) &
PD=$!
# ---------- E. dernière stable 4.35.0 avec LEUR Mathlib épinglé (refus rapide attendu)
( copie $W/travail_4350; echo 'leanprover/lean4:v4.35.0' > $W/travail_4350/OpenAI-YM-20261028/lean-toolchain
  ( cd $W/travail_4350/OpenAI-YM-20261028 && env $(envtc 4.35.0 16) $NS bash $O/interne_essai_4350.sh )
  date '+%F %T' > $E/E.fin ) &
PE=$!
wait $PB $PB2 $PC $PD $PE
date '+%F %T' > $E/ETAGE2.fin
# ---------- G. essai de portage direct : Lean 4.35.0 + Mathlib v4.35.0 (56a00585), leur code inchangé. RÉSEAU pour update et cache.
( P5=$W/travail_4350m/OpenAI-YM-20261028; L5=$W/travail_4350m/journaux; mkdir -p $L5
  cp -r $W/src/OpenAI-YM-20261028 $W/travail_4350m/ && rm -rf $P5/.git
  cd $P5 && echo 'leanprover/lean4:v4.35.0' > lean-toolchain
  sed -i 's/81a5d257c8e410db227a6665ed08f64fea08e997/56a005855ea17e0b0958f73ec801ae140b0a1679/' lakefile.toml
  grep -c 56a005855ea17e0b0958f73ec801ae140b0a1679 lakefile.toml > $L5/lakefile_modifie.txt; rm -f lake-manifest.json
  env $(envtc 4.35.0 16) lake update > $L5/update.log 2>&1; echo "RC=$?" > $L5/update.rc
  env $(envtc 4.35.0 16) lake exe cache get > $L5/cache_get.log 2>&1; echo "RC=$?" > $L5/cache_get.rc
  date '+%F %T' > $L5/build.debut
  env $(envtc 4.35.0 $TG) $NS timeout 5400 lake build WilsonReference WilsonConstruction > $L5/build.log 2>&1; echo "RC=$?" > $L5/build.rc
  date '+%F %T' > $L5/build.fin
  { echo "olean_produits $(find $P5/.lake/build/lib/lean -name '*.olean' -type f 2>/dev/null | wc -l)"
    echo "modules_en_echec $(grep -ac -E '^✖ ' $L5/build.log)"; echo "lignes_error $(grep -ac -E '(^|: )error' $L5/build.log)"
    echo "--- premiers modules en échec"; grep -a -E '^✖ ' $L5/build.log | head -40
    echo "--- premières erreurs"; grep -a -m 60 -E '(^|: )error' $L5/build.log; } > $L5/resume.txt
  date '+%F %T' > $E/G.fin ) &
PG=$!
# ---------- F. passe 2 sous 4.32.0 dans un dossier de construction neuf, comparaison des empreintes des .olean
mv $P0/.lake/build $W/travail_4320/build_p1 && rm -rf $W/travail_4320/build_p1/ir
passe p2 $TA
( cd $J0 && { cat resume_p1.txt resume_p2.txt; echo "olean différents entre p1 et p2 : $(diff empreintes_olean_p1.txt empreintes_olean_p2.txt | grep -c '^<')"; diff empreintes_olean_p1.txt empreintes_olean_p2.txt | head -10; } > comparaison_p1_p2.txt 2>&1 )
date '+%F %T' > $E/F.fin
wait $PG
kill $MEMLOG 2>/dev/null
date '+%F %T' > $E/FIN
