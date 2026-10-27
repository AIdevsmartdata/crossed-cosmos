#!/bin/bash
# Build from scratch: fresh .lake, mathlib fetched from GitHub, oleans from the mathlib cache.
set -o pipefail
cd "$(dirname "$0")"
echo "## start $(date -Is)"; elan --version; cat lean-toolchain
echo "## lake exe cache get"; lake exe cache get 2>&1 | tail -5; rc1=$?; echo "RC_cache=$rc1"
echo "## lake build"; lake build 2>&1 | tail -30; rc2=$?; echo "RC_build=$rc2"
echo "## print axioms"; lake env lean PrintAxioms.lean 2>&1; rc3=$?; echo "RC_axioms=$rc3"
echo "## end $(date -Is)"
exit $(( rc1 || rc2 || rc3 ))
