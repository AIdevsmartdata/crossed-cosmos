#!/usr/bin/env bash
# Reproduce the interval (Arb) certificate of the chordal one-link identity (Theorem 3 of the note) and its gates.
# Requirements: Python >= 3.11 with python-flint==0.9.0, numpy, mpmath (see requirements.txt).
# Usage:  PYTHON=python3 ./reproduce.sh        (regenerated files go to ./out, logs to ./logs)
# Set QUICK=1 to skip the gate suite (gates.py, about 20 certificate runs).
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
J=cert_D80_NT1024_NK256_cap200_p128.json

# 1. Certificate: truncation order D=80 in kappa (L=85), NT=1024 sub-intervals in y1, NK=256 boxes in kappa on [0,4/3],
#    ctx.cap=200 and ctx.prec=128 set explicitly (guard 1: cap >= L; guard 2: .prec == L on every series and product).
run run_cert_D80_NT1024_NK256_cap200_p128.log ok "$PY" cert_ch.py --D 80 --prec 128 --cap 200 --NT 1024 --NK 256 --out out/$J
grep -q 'TOUTES_OK 256/256' logs/run_cert_D80_NT1024_NK256_cap200_p128.log && echo "PASS  all 256 boxes OK (TOUTES_OK 256/256)" \
  || { echo "FAIL  TOUTES_OK 256/256 missing"; fail=1; }
# The JSON records the wall-clock time ("secondes"); every other field must be identical, and after restoring
# that single field the file must be byte-identical to the shipped one.
"$PY" - "$J" <<'EOF' > logs/json_compare.log 2>&1
import json, sys
j = sys.argv[1]
a, b = json.load(open(j)), json.load(open("out/" + j))
ka, kb = set(a) - {"secondes"}, set(b) - {"secondes"}
assert ka == kb, ("keys differ", ka ^ kb)
diff = [k for k in ka if a[k] != b[k]]
assert not diff, ("fields differ", diff)
b["secondes"] = a["secondes"]
json.dump(b, open("out/normalised_" + j, "w"), indent=1)
print("all fields except 'secondes' identical")
EOF
rc=$?; echo "RC=$rc" >> logs/json_compare.log
if [ $rc -eq 0 ] && cmp -s out/normalised_$J $J; then
  echo "PASS  regenerated JSON identical to the shipped JSON (byte-identical after restoring the timing field)"
else echo "FAIL  regenerated JSON differs from the shipped JSON (see logs/json_compare.log)"; fail=1; fi

# 2. Guards against the truncation failure of python-flint's default ctx.cap = 10.
run guard1_cap10.log refuse "$PY" cert_ch.py --D 80 --prec 128 --cap 10 --NT 64 --NK 4 --boites 0:1 --out out/refused_cap10.json
run guard1_cap84.log refuse "$PY" cert_ch.py --D 80 --prec 128 --cap 84 --NT 64 --NK 4 --boites 0:1 --out out/refused_cap84.json
run guard2_cap84_noguard1.log refuse "$PY" cert_ch.py --D 80 --prec 128 --cap 84 --NT 64 --NK 4 --boites 0:1 --sans-garde-cap --out out/refused_cap84b.json
grep -q "GARDE 2" logs/guard2_cap84_noguard1.log && echo "PASS  guard 2 fired (cap 84 = L-1, guard 1 disabled)" || { echo "FAIL  guard 2 did not fire"; fail=1; }

# 3. Exact gate (fractions, independent of Arb), constant c, numerical gate (floating point: evidence, not proof).
run run_gate_exact.log ok "$PY" gate_exact.py 80
run run_constante_c.log ok "$PY" constante_c.py
run run_gate_numerique.log ok "$PY" gate_numerique.py

# 4. Gate suite: cap 85/100/200/300 (identical boxes) and refusals; order D 40/60/80/100; NT 256..2048; prec 192; NK 64/128/512.
if [ "${QUICK:-0}" != 1 ]; then run run_gates.log ok "$PY" gates.py; sed -i "s#$PWD/#./#g" logs/gates/*.log; fi

# 5. Export to Lean rationals (outward rounding to 2^-40, exact re-check) and comparison with the Lean data file.
run run_export.log ok "$PY" export_lean.py $J out/Donnees.lean
if cmp -s out/Donnees.lean ../lean/KevYM/Certif/DobrushinCordale/Donnees.lean; then
  echo "PASS  exported Donnees.lean is byte-identical to lean/KevYM/Certif/DobrushinCordale/Donnees.lean"
else echo "FAIL  exported Donnees.lean differs from the Lean data file"; fail=1; fi
run run_export_refus_cap10.log refuse "$PY" -c "
import json; j = json.load(open('$J')); j['cap'] = 10; json.dump(j, open('out/tampered_cap10.json', 'w'))
import subprocess, sys; sys.exit(subprocess.run([sys.executable, 'export_lean.py', 'out/tampered_cap10.json', 'out/refused.lean']).returncode)"

[ $fail -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
