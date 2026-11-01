#!/usr/bin/env bash
# Exploration [certifie par intervalles si OK] : portee de cert_xi_arb.py (mode analytique) en fonction de la largeur des boites, a kappa = 20 et 30.
cd "$(dirname "$0")/.."
PY=${PY:-python3}
for spec in "20 0.002" "20 0.001" "20 0.0004" "20 0.0001" "30 0.0004" "30 0.0001" "30 0.00002" "30 0.000005"; do
  set -- $spec
  k1=$($PY -c "from fractions import Fraction; print(Fraction('$1')+10*Fraction('$2'))")
  printf "kappa0=%s largeur=%s : " "$1" "$2"
  $PY scripts/cert_xi_arb.py --NT 500 --k0 "$1" --k1 "$k1" --NK 10 --neg analytique --procs 4 --out /tmp/portee_$$.json 2>&1 | tail -1
done
