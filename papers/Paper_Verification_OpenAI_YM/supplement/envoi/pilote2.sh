#!/bin/bash
# Pilote n° 2 (remplace pilote_vast.sh à partir de la fin de la passe 1) : même contenu, mais les phases indépendantes de la
# passe 1 démarrent tout de suite dans des dossiers séparés (la machine est presque inoccupée pendant la fin, étroite, d'une passe).
set -u
export LC_ALL=C.UTF-8
W=/work; E=$W/etat; O=$W/outils; mkdir -p $E
NS=""
ulimit -s 1048576 2>/dev/null || true
envtc(){ echo "PATH=$W/tc/$1/bin:/usr/bin:/bin HOME=$W/home LEAN_NUM_THREADS=$2 LC_ALL=C.UTF-8"; }
P0=$W/travail_4320/OpenAI-YM-20261028; J0=$W/travail_4320/journaux
echo "pilote2 démarré $(date '+%F %T')" >> $E/pilote2.txt
reprise(){ # $1 = projet, $2 = journaux, $3 = passe, $4 = toolchain, $5 = fils : si la passe a échoué, une reprise, puis empreintes
  if ! grep -qs 'RC=0' $2/build_$3.rc; then
    ( cd $1 && env $(envtc $4 $5) lake build WilsonReference WilsonConstruction > $2/build_$3_reprise.log 2>&1; echo "RC=$?" > $2/build_$3_reprise.rc )
    ( cd $1/.lake/build/lib/lean && find . -name '*.olean' -type f -print0 | sort -z | xargs -0 sha256sum ) > $2/empreintes_olean_$3.txt
    find $1/.lake/build -type f -size 0 ! -name '*.hash' > $2/fichiers_vides_$3.txt
    { echo "olean $(wc -l < $2/empreintes_olean_$3.txt)"; echo "vides $(wc -l < $2/fichiers_vides_$3.txt)"; echo "echecs_reprise $(grep -ac '^✖ ' $2/build_$3_reprise.log)"; } > $2/resume_$3_reprise.txt
  fi; }
copie(){ # $1 = dossier ; sources seules + dépendances épinglées sans leurs constructions (lecture seule dans la passe 1)
  mkdir -p $1 && cp -r $W/src/OpenAI-YM-20261028 $1/ && rm -rf $1/OpenAI-YM-20261028/.git
  mkdir -p $1/OpenAI-YM-20261028/.lake/packages
  for p in $P0/.lake/packages/*; do tar -C $P0/.lake/packages -cf - --exclude="$(basename $p)/.lake" $(basename $p) | tar -C $1/OpenAI-YM-20261028/.lake/packages -xf -; done
  cp $P0/lake-manifest.json $1/OpenAI-YM-20261028/lake-manifest.json; }
# ---------- F. passe 2 sous 4.32.0, dans une copie complète SÉPARÉE (sources vérifiées + mêmes dépendances et cache Mathlib)
( P2=$W/travail_4320_p2/OpenAI-YM-20261028; J2=$W/travail_4320_p2/journaux
  mkdir -p $W/travail_4320_p2 && cp -r $W/src/OpenAI-YM-20261028 $W/travail_4320_p2/ && rm -rf $P2/.git
  mkdir -p $P2/.lake && cp -r $P0/.lake/packages $P2/.lake/packages && cp $P0/lake-manifest.json $P2/lake-manifest.json
  ( cd $P2 && env $(envtc 4.32.0 80) bash $O/interne_build_passe.sh p2 )
  reprise $P2 $J2 p2 4.32.0 40
  date '+%F %T' > $E/F.fin ) &
PF=$!
# ---------- G. essai de portage direct : Lean 4.35.0 + Mathlib v4.35.0 (56a00585), leur code inchangé. RÉSEAU pour update et cache.
( P5=$W/travail_4350m/OpenAI-YM-20261028; L5=$W/travail_4350m/journaux; mkdir -p $L5
  cp -r $W/src/OpenAI-YM-20261028 $W/travail_4350m/ && rm -rf $P5/.git
  cd $P5 && echo 'leanprover/lean4:v4.35.0' > lean-toolchain
  sed -i 's/81a5d257c8e410db227a6665ed08f64fea08e997/56a005855ea17e0b0958f73ec801ae140b0a1679/' lakefile.toml
  grep -c 56a005855ea17e0b0958f73ec801ae140b0a1679 lakefile.toml > $L5/lakefile_modifie.txt; rm -f lake-manifest.json
  env $(envtc 4.35.0 16) lake update > $L5/update.log 2>&1; echo "RC=$?" > $L5/update.rc
  env $(envtc 4.35.0 16) lake exe cache get > $L5/cache_get.log 2>&1; echo "RC=$?" > $L5/cache_get.rc
  date '+%F %T' > $L5/build.debut
  env $(envtc 4.35.0 40) timeout 5400 lake build WilsonReference WilsonConstruction > $L5/build.log 2>&1; echo "RC=$?" > $L5/build.rc
  date '+%F %T' > $L5/build.fin
  { echo "olean_produits $(find $P5/.lake/build/lib/lean -name '*.olean' -type f 2>/dev/null | wc -l)"
    echo "modules_en_echec $(grep -ac -E '^✖ ' $L5/build.log)"; echo "lignes_error $(grep -ac -E '(^|: )error' $L5/build.log)"
    echo "--- premiers modules en échec"; grep -a -E '^✖ ' $L5/build.log | head -40
    echo "--- premières erreurs"; grep -a -m 60 -E '(^|: )error' $L5/build.log; } > $L5/resume.txt
  date '+%F %T' > $E/G.fin ) &
PG=$!
# ---------- E. dernière stable 4.35.0 avec LEUR Mathlib épinglé (refus rapide attendu), 8 fils, 1 h au plus
( copie $W/travail_4350; echo 'leanprover/lean4:v4.35.0' > $W/travail_4350/OpenAI-YM-20261028/lean-toolchain
  ( cd $W/travail_4350/OpenAI-YM-20261028 && env $(envtc 4.35.0 8) bash $O/interne_essai_4350.sh )
  date '+%F %T' > $E/E.fin ) &
PE=$!
# ---------- attendre la fin de la passe 1 (lancée par le premier pilote), reprise si besoin
while [ ! -f $J0/TOUT_p1.fin ]; do sleep 10; done
reprise $P0 $J0 p1 4.32.0 60
cp $J0/resume_p1*.txt $J0/build_p1*.rc $E/ 2>/dev/null
date '+%F %T' > $E/A.fin
if ! grep -qs 'RC=0' $J0/build_p1.rc $J0/build_p1_reprise.rc; then echo "passe 1 en échec, reprise comprise" > $E/ARRET; fi
# ---------- D. recompilation complète sous Lean 4.32.2 (Mathlib et dépendances depuis les sources), puis contrôles
( copie $W/travail_4322; echo 'leanprover/lean4:v4.32.2' > $W/travail_4322/OpenAI-YM-20261028/lean-toolchain
  ( cd $W/travail_4322/OpenAI-YM-20261028 && env $(envtc 4.32.2 64) bash $O/interne_build_4322.sh )
  date '+%F %T' > $E/D.fin ) &
PD=$!
if [ ! -f $E/ARRET ]; then
# ---------- B. contrôles (les nôtres, puis les trois fournis par OpenAI)
( cd $P0 && env $(envtc 4.32.0 8) bash $O/interne_verifs_copie.sh 4320
  ( cd $P0 && /usr/bin/time -v -o $J0/usage_4320.time env $(envtc 4.32.0 4) lake env lean -j1 -DmaxHeartbeats=0 verification/Usage.lean > $J0/usage_4320.out 2> $J0/usage_4320.err; echo "RC=$?" > $J0/usage_4320.rc )
  date '+%F %T' > $E/B.fin ) &
PB=$!
# ---------- B2. [block removed from this publication: it compiled two files unrelated to this report]
( true
  date '+%F %T' > $E/B2.fin ) &
PB2=$!
# ---------- C. noyau indépendant : témoins, export de toute la clôture, rejeu nanoda
( cd $W/export && env $(envtc 4.32.0 4) bash $O/interne_temoins_nanoda.sh
  date '+%F %T' > $E/C_temoins.fin
  cd $P0 && env $(envtc 4.32.0 8) bash $O/interne_export.sh joint YangMills.jointExistence YangMills.constructed YangMills.su2Theory
  ls -la $W/export/joint.ndjson > $W/export/logs/joint_taille.txt 2>&1; grep -c '"str":"Vintage"' $W/export/joint.ndjson > $W/export/logs/joint_vintage.txt 2>&1
  date '+%F %T' > $E/C_export.fin
  cd $W/export && env $(envtc 4.32.0 4) bash $O/interne_nanoda.sh joint 24 YangMills.jointExistence YangMills.JointExistence YangMills.su2Theory
  date '+%F %T' > $E/C.fin ) &
PC=$!
wait $PB $PB2 $PC
fi
date '+%F %T' > $E/ETAGE_BC.fin
wait $PF $PD $PE $PG
J2=$W/travail_4320_p2/journaux
{ cat $J0/resume_p1.txt $J2/resume_p2.txt; echo "olean différents entre p1 et p2 : $(diff $J0/empreintes_olean_p1.txt $J2/empreintes_olean_p2.txt | grep -c '^<')"; diff $J0/empreintes_olean_p1.txt $J2/empreintes_olean_p2.txt | head -10; } > $E/comparaison_p1_p2.txt 2>&1
date '+%F %T' > $E/FIN
