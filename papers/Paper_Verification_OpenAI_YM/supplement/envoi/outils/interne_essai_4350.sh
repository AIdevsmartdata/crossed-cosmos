#!/bin/bash
# Essai sous la dernière stable, Lean 4.35.0, AVEC leur Mathlib épinglé (81a5d257, prévu pour 4.32.0), DANS le bac
# (leanext, réseau coupé), cwd = /work/travail_4350/OpenAI-YM-20261028, PATH = toolchain-4.35.0.
# Borné à 1 h de compilation : on attend un refus rapide ; on relève les premières erreurs et leur nombre.
set -u
L=/work/travail_4350/journaux; mkdir -p $L
lean --version > $L/lean_version.txt 2>&1
date '+%F %T' > $L/build.debut
timeout 3600 lake build WilsonReference > $L/build_reference.log 2>&1; echo "RC=$?" > $L/build_reference.rc
date '+%F %T' > $L/build.fin
{
  echo "modules_construits $(grep -c -E '^(✔|⚠) ' $L/build_reference.log)"
  echo "modules_en_echec $(grep -c -E '^✖ ' $L/build_reference.log)"
  echo "lignes_error $(grep -c -E '(^|: )error' $L/build_reference.log)"
  echo "--- premiers modules en échec"; grep -E '^✖ ' $L/build_reference.log | head -20
  echo "--- premières erreurs"; grep -m 30 -E '(^|: )error' $L/build_reference.log
} > $L/resume.txt
date '+%F %T' > $L/TOUT.fin
