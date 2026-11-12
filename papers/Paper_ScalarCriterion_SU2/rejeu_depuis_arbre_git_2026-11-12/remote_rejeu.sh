#!/bin/bash
# Exécuté sur la machine louée SOUS L'UTILISATEUR lean. Reconstruction du Lean du critère scalaire depuis l'ARCHIVE GIT du dossier du paquet.
# Entrées déjà posées dans /work/critere_rejeu/ : crit_arbre.tar.gz, echafaudage/ (lakefile.toml, lean-toolchain, lake-manifest.json, PrintAxioms.lean).
source /work/lean_nous/remote_common.sh      # HOME, ts(), run()
R=/work/critere_rejeu; J=$R/journaux/crit_arbre.log; mkdir -p $R/journaux
export PATH=/work/lean_nous/tc/4.34.0/bin:$PATH
ulimit -n 1048576
CPU="taskset -c 0-15 nice -n 10"
cd $R || exit 8
echo "[$(ts)] DEBUT ; ulimit -n=$(ulimit -n) ; charge: $(cut -d' ' -f1-3 /proc/loadavg)" >> $J
sha256sum crit_arbre.tar.gz echafaudage/* >> $J
run $J rm -rf arbre proj
run $J mkdir arbre proj
run $J tar xzf crit_arbre.tar.gz -C arbre
run $J bash -c 'cd arbre && find . -type f | wc -l'
# sources hachees : verification contre le MANIFEST de l'archive elle-meme
run $J bash -c 'cd arbre/Paper_ScalarCriterion_SU2/lean && grep -E "^[0-9a-f]{64}" MANIFEST.txt | while read h f; do case $f in ClayYM/*) g=../ClayYM_v1_1_extrait/$f;; *) g=$f;; esac; echo "$h  $g"; done | sha256sum -c -'
# projet lake : echafaudage (non fait par git) + main.lean pris DANS l'archive
run $J cp echafaudage/lakefile.toml echafaudage/lean-toolchain echafaudage/lake-manifest.json echafaudage/PrintAxioms.lean proj/
run $J cp arbre/Paper_ScalarCriterion_SU2/lean/main.lean proj/main.lean
run $J sha256sum proj/main.lean
# paquets Mathlib deja telecharges lors de la reconstruction de ce matin (cache officiel) ; AUCUN artefact de build du critere n'est copie
run $J mkdir -p proj/.lake
run $J cp -a /work/lean_nous/nous/crit_proj/.lake/packages proj/.lake/packages
run $J bash -c 'ls proj/.lake; ls proj/.lake/build 2>&1 | head -2'
cd proj || exit 8; T0=$(date +%s)
run $J lean --version; run $J lake --version
echo "## grep sorry/admit/native_decide/axiom (docstrings seulement attendus)" >> $J
grep -rnE '\b(sorry|admit|native_decide)\b|^\s*axiom\b' --include=*.lean . --exclude-dir=.lake >> $J 2>&1
run $J $CPU lake exe cache get
run $J $CPU lake build ; RCB=$?
echo "[$(ts)] RC_build_final=$RCB ; duree build $(( $(date +%s)-T0 )) s" >> $J
run $J $CPU lake env lean PrintAxioms.lean ; RCA=$?
echo "[$(ts)] RC_axiomes=$RCA ; lignes axiomes standard: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $J) ; lignes 'does not depend': $(grep -c 'does not depend' $J)" >> $J
echo "[$(ts)] FIN_TOTALE $(( $(date +%s)-T0 )) s" >> $J
echo DONE > $R/journaux/crit_arbre.done
