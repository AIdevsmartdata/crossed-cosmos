#!/bin/bash
# Recompilation COMPLÈTE sous Lean 4.32.2 (Mathlib et dépendances depuis les sources, puis YM), DANS le bac
# (leanext, réseau coupé), cwd = /work/travail_4322/OpenAI-YM-20261028, PATH = toolchain-4.32.2.
# Version révisée après le plantage du 11/11 : passe unique en dossier neuf (interne_build_passe.sh, empreintes des .olean),
# puis nos contrôles et VerifyJoint sous 4.32.2 si la compilation est complète.
set -u
P=$PWD; L=$(dirname "$P")/journaux
bash /work/outils/interne_build_passe.sh p4322
if grep -q 'RC=0' $L/build_p4322.rc 2>/dev/null && [ "$(grep -c . $L/fichiers_vides_p4322.txt)" = "0" ]; then
  bash /work/outils/interne_verifs_copie.sh 4322
fi
date '+%F %T' > $L/TOUT.fin
