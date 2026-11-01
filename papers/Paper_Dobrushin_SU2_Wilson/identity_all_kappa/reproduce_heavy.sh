#!/usr/bin/env bash
# reproduce_heavy.sh -- HEAVY computations (about 40 minutes on 8 cores; run at nice 10):
#   (1) Arb certificate of Xi(kappa) < 0 by boxes on [4/3, 20]                          (~2 min)
#   (2) independent mpmath.iv certificate on [4/3, 20], in three ranges of boxes         (~40 min)
#   (3) direct optimal-transport control (POT) + synthesis                               (~5 min)
# Usage (from a folder containing scripts/ ; a Python environment with python-flint, mpmath, numpy, scipy, POT):
#   PY=./venv/bin/python ./reproduce_heavy.sh
# Optional: NPROC=<number of worker processes> (default 8); CORES=<cpu list, e.g. 4-11> pins the processes with taskset
# (default: no pinning). The shipped logs/ and resultats/ come from a run with 8 workers pinned to 8 cores.
set -u
cd "$(dirname "$0")"
PY=${PY:-./venv/bin/python}
CORES=${CORES:-}
NPROC=${NPROC:-8}
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
mkdir -p logs resultats
fail=0
run () {  # run <log> <cmd...>
  local log=$1; shift
  if [ -n "$CORES" ]; then taskset -c "$CORES" nice -n 10 "$@" > "logs/$log" 2>&1; else nice -n 10 "$@" > "logs/$log" 2>&1; fi; local rc=$?
  echo "RC=$rc" >> "logs/$log"
  if [ $rc -eq 0 ]; then echo "PASS  $log"; else echo "FAIL  $log (RC=$rc)"; fail=1; fi
}
echo "== versions"; "$PY" -c "import sys, flint, mpmath, numpy, scipy, ot; print('python', sys.version.split()[0], 'python-flint', flint.__version__, 'mpmath', mpmath.__version__, 'numpy', numpy.__version__, 'scipy', scipy.__version__, 'POT', ot.__version__)" | tee logs/versions_heavy.log
run xi_arb_4s3_20.log "$PY" scripts/cert_xi_arb.py --NT 400 --k0 4/3 --k1 20 --NK 9333 --neg auto --adapt 6 --procs "$NPROC" --out resultats/xi_arb_4s3_20.json
run xi_mpiv_4s3_15.log "$PY" scripts/cert_xi_mpiv.py --NT 250 --k0 4/3 --k1 15 --NK 4267 --procs "$NPROC" --out resultats/xi_mpiv_4s3_15.json
run xi_mpiv_15_18.log "$PY" scripts/cert_xi_mpiv.py --NT 250 --k0 15 --k1 18 --NK 6000 --procs "$NPROC" --out resultats/xi_mpiv_15_18.json
run xi_mpiv_18_20.log "$PY" scripts/cert_xi_mpiv.py --NT 250 --k0 18 --k1 20 --NK 8000 --procs "$NPROC" --out resultats/xi_mpiv_18_20.json
run resume_arb.log "$PY" scripts/resume_cert.py 4/3 20 resultats/resume_arb.json resultats/xi_arb_4s3_20.json
run resume_mpiv.log "$PY" scripts/resume_cert.py 4/3 20 resultats/resume_mpiv.json resultats/xi_mpiv_4s3_15.json resultats/xi_mpiv_15_18.json resultats/xi_mpiv_18_20.json
run ot_controle.log "$PY" scripts/ot_controle.py --procs "$NPROC" --out resultats/ot_controle.json
run synthese_ot.log "$PY" scripts/synthese_ot.py resultats/ot_controle.json resultats/synthese_ot.json
[ $fail -eq 0 ] && echo "ALL HEAVY CHECKS PASSED" || echo "SOME HEAVY CHECKS FAILED"
exit $fail
