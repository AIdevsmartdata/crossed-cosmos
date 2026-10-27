#!/usr/bin/env bash
# Independent check in exact rational arithmetic (no quadrature, no arb_series, no import of ../certificate_geodesic):
#  1. vc_exact.py: E_j(alpha) as exact polynomials in cos(alpha) with rational coefficients, j <= 45;
#  2. vc_boites_v2.py: for each of the 160 boxes, rigorous upper bounds U_k of sup_box E_{2k+2} (mpmath.iv + exact
#     Taylor expansion), compared with the 3200 rationals of ../lean/KevYM/Certif/DobrushinLien/Donnees.lean.
# Requirements: python-flint is NOT needed; mpmath (tested with 1.4.1). Usage: PYTHON=python3 ./reproduce.sh
set -u
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p out logs
"$PY" vc_exact.py 16 45 out/E_exact_N16.json > logs/vc_exact_N16.log 2>&1; rc1=$?; echo "RC=$rc1" >> logs/vc_exact_N16.log
"$PY" vc_boites_v2.py out/E_exact_N16.json ../lean/KevYM/Certif/DobrushinLien/Donnees.lean \
      ../certificate_geodesic/cert_N16_G22_B160_cap200_p128.json "${NPROC:-4}" out/vc_boites_v2.json > logs/vc_boites_v2.log 2>&1
rc2=$?; echo "RC=$rc2" >> logs/vc_boites_v2.log
sed -i "s#$PWD/#./#g" logs/*.log
grep -q "VERDICT_BOITES = TOUTES_VRAIES" logs/vc_boites_v2.log && [ $rc1 -eq 0 ] && [ $rc2 -eq 0 ] \
  && { echo "PASS  3200/3200 Lean coefficients are true upper bounds (exact rationals)"; exit 0; } \
  || { echo "FAIL  see logs/"; exit 1; }
