#!/bin/bash
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
P=/work/travail_4320/OpenAI-YM-20261028
cd $P
LP=$(lake env printenv LEAN_PATH); echo "LEAN_PATH=$LP"; echo "$LP" > /work/lean4lean_essai/lean_path.txt
cd /work/lean4lean_essai
ls -la $P/.lake/build/lib/lean/YM/FullVolume/Luna/Ocho.olean
export LEAN_PATH=$LP
L=/work/lean4lean_essai/src/.lake/build/bin/lean4lean
date -u
/usr/bin/time -v nice -n 10 $L -v YM.FullVolume.Luna.Ocho > run_Ocho.out 2> run_Ocho.err; echo "lean4lean Ocho rc=$?"
date -u
wc -l run_Ocho.out; head -3 run_Ocho.out; tail -3 run_Ocho.out; grep -c "adding" run_Ocho.out; grep -n "uniformE" run_Ocho.out | head
grep -E "Elapsed|Maximum resident|Exit" run_Ocho.err
head -c 600 run_Ocho.err
