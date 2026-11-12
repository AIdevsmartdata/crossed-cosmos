#!/bin/bash
set -x
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
cd /work/lean4lean_essai
date -u
cd src && git log -1 --format="%H %ad" && cat lean-toolchain
ulimit -n 1048576
cat LICENSE | head -3
T0=$(date +%s)
nice -n 10 lake build lean4lean; echo "RC_BUILD=$? duree=$(( $(date +%s)-T0 ))s"
sha256sum .lake/build/bin/lean4lean
date -u
