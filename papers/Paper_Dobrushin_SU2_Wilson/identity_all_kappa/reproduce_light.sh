#!/usr/bin/env bash
# reproduce_light.sh -- calculs LEGERS (< 1 minute au total) : verifications symboliques, exactes, numeriques haute precision, certificat Delta > 0,
# analyse de la limite de la reduction de D7, chaine d'encadrement du flux, table de valeurs, gates du certificat.
# Usage : PY=/chemin/python-avec-flint-mpmath-numpy-scipy PYSYM=/chemin/python-avec-sympy ./reproduce_light.sh
# Chaque etape ecrit dans logs/ et resultats/ ; le script sort avec un code != 0 si UNE etape echoue (les verdicts sont calcules par les scripts).
set -u
cd "$(dirname "$0")"
PY=${PY:-python3}
PYSYM=${PYSYM:-python3}
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
mkdir -p logs resultats
fail=0
run () {  # run <log> <cmd...>
  local log=$1; shift
  "$@" > "logs/$log" 2>&1; local rc=$?
  echo "RC=$rc" >> "logs/$log"
  if [ $rc -eq 0 ]; then echo "PASS  $log"; else echo "FAIL  $log (RC=$rc)"; fail=1; fi
}
echo "== versions"; "$PY" -c "import sys, flint, mpmath, numpy, scipy; print('python', sys.version.split()[0], 'python-flint', flint.__version__, 'mpmath', mpmath.__version__, 'numpy', numpy.__version__, 'scipy', scipy.__version__)" | tee logs/versions.log
"$PYSYM" -c "import sympy; print('sympy', sympy.__version__)" | tee -a logs/versions.log
run verif_symbolique.log "$PYSYM" -I scripts/verif_symbolique.py
run serie_identite_exacte.log "$PYSYM" -I scripts/serie_identite_exacte.py 40 resultats/serie_identite_exacte.json
run ident_num_arb.log "$PY" scripts/ident_num_arb.py --kappas 1/100,1/20,1/10,1/2,1,4/3,2,3,4,5,6,8,10,15,20,30,50,100,200,400 --out resultats/ident_num_arb.json
run ident_num_arb_alea.log "$PY" scripts/ident_num_arb.py --kappas "$(cat scripts/kappas_aleatoires.txt)" --out resultats/ident_num_arb_alea.json
run ident_num_mp.log "$PY" scripts/ident_num_mp.py --kappas 1/2,4/3,3,7,12,25 --dps 30 --out resultats/ident_num_mp.json
run cert_delta_boites.log "$PY" scripts/cert_delta_boites.py --prec 128 --cap 200 --k0 1/5 --k1 10000 --out resultats/cert_delta_boites.json
run table_valeurs.log "$PY" scripts/table_valeurs.py resultats/table_valeurs.json
run d7_limite.log "$PY" scripts/d7_limite.py --out resultats/d7_limite.json
run flux_champ_exact.log "$PY" scripts/flux_champ_exact.py --out resultats/flux_champ_exact.json
run stress_chaine.log "$PY" scripts/stress_chaine.py 60 resultats/stress_chaine.json
run gates_xi.log "$PY" scripts/gates_xi.py
run gates_mpiv.log "$PY" scripts/gates_mpiv.py
[ $fail -eq 0 ] && echo "ALL LIGHT CHECKS PASSED" || echo "SOME LIGHT CHECKS FAILED"
exit $fail
