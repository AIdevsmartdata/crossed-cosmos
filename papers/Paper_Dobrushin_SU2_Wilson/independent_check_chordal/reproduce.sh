#!/usr/bin/env bash
# Independent check of the chordal certificate (V-CH). It does NOT use python-flint/Arb and does not import any code
# from ../certificate_chordal:
#  1. coefs_exacts.py: exact rational coefficients (A_j, e_j, 1/Z, m_1, N) up to order 100, own downward solver,
#     solvability residuals asserted to be exactly 0, L[A_j] = q_j checked exactly;
#  2. cert_vch.py: mpmath.iv interval certificate with elementary tail bounds (no complex Cauchy estimates),
#     uniform partition in theta (t = cos theta) with exact weights, naive Horner; 200 boxes of width 1/150 on [0,4/3];
#  3. the same code on the 256 boxes of the Lean data file, and a two-sided consistency check against its rationals;
#  4. negative gates (sabotaged precision, too short series, left-hand side scaled by 0.30) must fail;
#  5. exact_c2_D0.py (SymPy/fractions: D_ch(0) = 1/4, c_2 = 1/96, Z(4/3)); beckmann_mc.py (Monte-Carlo, numerical only).
# Requirements: sympy, mpmath, numpy. Usage: NPROC=8 PYTHON=python3 ./reproduce.sh
set -u
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
NP=${NPROC:-4}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p out logs
fail=0
run () {  # run <log> <expected: ok|refuse> <cmd...>
  local log=$1 exp=$2; shift 2
  "$@" > "logs/$log" 2>&1; local rc=$?
  echo "RC=$rc" >> "logs/$log"
  sed -i "s#$PWD/#./#g" "logs/$log"
  if { [ "$exp" = ok ] && [ $rc -eq 0 ]; } || { [ "$exp" = refuse ] && [ $rc -ne 0 ]; }; then
    echo "PASS  $log (RC=$rc, expected $exp)"
  else
    echo "FAIL  $log (RC=$rc, expected $exp)"; fail=1
  fi
}
run coefs_M100.log ok "$PY" coefs_exacts.py 100
run run_vch_D80_NT1024_NK200_p128.log ok "$PY" cert_vch.py --D 80 --prec 128 --NT 1024 --NK 200 --procs "$NP" --out out/vch_D80_NT1024_NK200_p128.json
grep -q "OK=200/200 .*couverture_\[0,4/3\]=True" logs/run_vch_D80_NT1024_NK200_p128.log \
  && echo "PASS  200/200 boxes, exact covering of [0,4/3]" || { echo "FAIL  200/200 with covering"; fail=1; }
run parse_lean_boxes.log ok "$PY" parse_lean_boxes.py ../lean/KevYM/Certif/DobrushinCordale/Donnees.lean out/boites_lean.json
run run_vch_lean256.log ok "$PY" cert_vch.py --D 80 --prec 128 --NT 1024 --boxes "$(cat out/boites_lean.json.boxes)" --procs "$NP" --out out/vch_lean256.json
run compare_lean256.log ok "$PY" compare_CH.py out/boites_lean.json out/vch_lean256.json
grep -q "incoherences = 0, V-CH OK = 256/256" logs/compare_lean256.log \
  && echo "PASS  256/256 Lean boxes recertified, 0 inconsistency with the Lean rationals" || { echo "FAIL  Lean box comparison"; fail=1; }
# negative gates
VCH_SABOTAGE_PREC=53 run neg_prec53.log refuse "$PY" cert_vch.py --D 80 --prec 128 --NT 256 --boxes "0:1/192" --procs 1 --out out/neg_prec53.json
run neg_M_too_short.log refuse "$PY" cert_vch.py --D 99 --prec 128 --NT 256 --boxes "0:1/192" --procs 1 --out out/neg_M.json
VCH_LHS_SCALE=3/10 run neg_scale0.30.log refuse "$PY" cert_vch.py --D 80 --prec 128 --NT 1024 --boxes "85/64:4/3" --procs 1 --out out/neg_scale030.json
VCH_LHS_SCALE=7/20 run pos_scale0.35.log ok "$PY" cert_vch.py --D 80 --prec 128 --NT 1024 --boxes "85/64:4/3" --procs 1 --out out/pos_scale035.json
# exact checks and a numerical cross-check
run run_exact_c2_D0.log ok "$PY" exact_c2_D0.py
run run_beckmann_mc.log ok "$PY" beckmann_mc.py
[ $fail -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
