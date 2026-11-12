#!/bin/bash
# (a, suite) versions des chaînes d'outils, révisions des dépendances, empreintes des binaires d'outils, comparées au rapport.
. $(dirname $0)/common.sh
exec > $OUT/a2_versions.out 2>&1
for v in 4.32.0 4.32.2 4.35.0; do echo "lean $v : $(/work/tc/$v/bin/lean --version)"; done
echo "--- révisions des dépendances de la compilation de référence 4.32.0 (git rev-parse HEAD de chaque dépôt)"
for d in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do echo "$d $(git -c safe.directory='*' -C /work/travail_4320/OpenAI-YM-20261028/.lake/packages/$d rev-parse HEAD) modifs=$(git -c safe.directory='*' -C /work/travail_4320/OpenAI-YM-20261028/.lake/packages/$d status --porcelain | wc -l)"; done
echo "--- binaires des outils"; sha256sum /work/outils/bin/lean4export /work/outils/bin/nanoda_bin
echo "--- révision des sources des outils"
git -c safe.directory='*' -C /work/outils/lean4export rev-parse HEAD; git -c safe.directory='*' -C /work/outils/nanoda_lib rev-parse HEAD
echo "--- lake-manifest.json / lakefile.toml / lean-toolchain du dépôt"; (cd $SRC && sha256sum lake-manifest.json lakefile.toml lean-toolchain)
echo "--- .olean du projet : nombre (4.32.0 et 4.32.2), fichiers vides"
for v in 4320 4322; do P=$(refdir $v)/.lake/build/lib/lean; echo "$v : $(find $P -name '*.olean' -type f | wc -l) olean, vides: $(find $P -name '*.olean' -type f -size 0 | wc -l)"; done
echo "--- .olean des bibliothèques (packages/*/.lake/build/lib/lean) : 4.32.0 (cache Mathlib) et 4.32.2 (recompilées)"
for v in 4320 4322; do echo "$v : $(find $(refdir $v)/.lake/packages -path '*/.lake/build/lib/lean/*' -name '*.olean' -type f 2>/dev/null | wc -l)"; done
