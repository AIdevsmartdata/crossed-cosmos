#!/bin/bash
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
cd /work/lean4lean_essai
export LEAN_PATH=$(cat lean_path.txt)
L=/work/lean4lean_essai/src/.lake/build/bin/lean4lean
for m in YM.Pert.Align.Cancel YM.Pert.Align.Drivers YM.Pert.Lattice.Symbol; do
  s=$(date +%s)
  /usr/bin/time -v nice -n 10 $L -v $m > run_$m.out 2> run_$m.err; rc=$?
  echo "== $m rc=$rc duree=$(( $(date +%s)-s ))s decls=$(grep -c '^adding' run_$m.out) RSS_ko=$(grep 'Maximum resident' run_$m.err | awk '{print $NF}')"
  tail -1 run_$m.out; grep -E "orbit_eq|key_orb|whole_apply" run_$m.out
done
B=/work/travail_4320/OpenAI-YM-20261028/.lake/build/lib/lean
echo "oleans projet: $(find $B -name '*.olean' | wc -l) ; sous YM/: $(find $B/YM -name '*.olean' | wc -l)"
find $B -name '*.olean' | sed "s#$B/##; s#\.olean##; s#/#.#g" | sort > tous_modules.txt
shuf --random-source=<(yes 42) -n 20 tous_modules.txt > echantillon20.txt
cat echantillon20.txt
s=$(date +%s)
/usr/bin/time -v nice -n 10 $L -v $(cat echantillon20.txt) > run_ech20.out 2> run_ech20.err; rc=$?
echo "== ech20 rc=$rc duree=$(( $(date +%s)-s ))s decls=$(grep -c '^adding' run_ech20.out) RSS_ko=$(grep 'Maximum resident' run_ech20.err | awk '{print $NF}')"
tail -2 run_ech20.out
