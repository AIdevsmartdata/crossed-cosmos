#!/usr/bin/env bash
# Reproduce the interval (Arb) certificate of the one-link inequality and its gates.
# Requirements: Python >= 3.11 with python-flint==0.9.0, numpy (see requirements.txt).
# Usage:  PYTHON=python3 ./reproduce.sh        (all outputs go to ./out and ./logs)
# Expected total run time: a few minutes on a laptop-class CPU.
set -u
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p out logs
fail=0
run () {  # run <log> <expected: ok|refuse> <cmd...>
  local log=$1 exp=$2; shift 2
  "$@" > "logs/$log" 2>&1; local rc=$?
  echo "RC=$rc" >> "logs/$log"
  sed -i "s#$PWD/#./#g" "logs/$log"   # no absolute paths in shipped logs
  if { [ "$exp" = ok ] && [ $rc -eq 0 ]; } || { [ "$exp" = refuse ] && [ $rc -ne 0 ]; }; then
    echo "PASS  $log (RC=$rc, expected $exp)"
  else
    echo "FAIL  $log (RC=$rc, expected $exp)"; fail=1
  fi
}
"$PY" -c "import flint, sys; print('python', sys.version.split()[0], 'python-flint', flint.__version__)"

# 1. Certificate: N=16 series order, NG=22 Gauss nodes, NB=160 boxes in alpha, ctx.cap=200, ctx.prec=128.
run cert_N16_G22_B160_cap200_p128.log ok "$PY" cert_lien.py 16 22 160 --cap 200 --prec 128 --out out/cert_N16_G22_B160_cap200_p128.json
grep -q '^TOUTES_OK' logs/cert_N16_G22_B160_cap200_p128.log && echo "PASS  all 160 boxes OK (TOUTES_OK)" || { echo "FAIL  TOUTES_OK missing"; fail=1; }
if cmp -s out/cert_N16_G22_B160_cap200_p128.json cert_N16_G22_B160_cap200_p128.json; then
  echo "PASS  regenerated JSON is byte-identical to the shipped JSON"
else echo "FAIL  regenerated JSON differs from the shipped JSON"; fail=1; fi

# 2. Guards against the truncation bug of the first certificate (ctx.cap left at its default 10).
run guard1_cap10.log refuse "$PY" cert_lien.py 16 22 160 --cap 10 --prec 128 --out out/refused_cap10.json
run guard2_cap41_noguard1.log refuse "$PY" cert_lien.py 16 22 160 --cap 41 --prec 128 --sans-garde-cap --out out/refused_cap41.json

# 3. Gates (independent checks of the implementation; floating-point gates are evidence, not proof).
for g in G2 G3 G4 G5; do run gate_$g.log ok "$PY" gates.py $g --cap 200 --prec 128; done
run gate_G5b_grid.log ok "$PY" gate_G5b_grille.py

# 4. Export to Lean rationals (upward rounding to 2^-40, exact re-check) and comparison with the Lean data file.
run export_lean.log ok "$PY" export_lean.py out/cert_N16_G22_B160_cap200_p128.json out/Donnees.lean
if cmp -s out/Donnees.lean ../lean/KevYM/Certif/DobrushinLien/Donnees.lean; then
  echo "PASS  exported Donnees.lean is byte-identical to lean/KevYM/Certif/DobrushinLien/Donnees.lean"
else echo "FAIL  exported Donnees.lean differs from the Lean data file"; fail=1; fi

[ $fail -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
