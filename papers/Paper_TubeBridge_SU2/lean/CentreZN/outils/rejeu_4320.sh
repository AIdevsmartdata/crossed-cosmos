#!/bin/bash
# Rejeu CentreZN par un non-auteur (Claude Sonnet 5.5), a lancer SOUS L'UTILISATEUR lean sur la machine louee, dossier /work/lean_zn_rejeu_1112.
# Lean 4.32.0 + Mathlib du projet d'OpenAI deja compile (lecture seule). Usage: rejeu_4320.sh
set -u
R=/work/lean_zn_rejeu_1112; J=$R/out; OA=/work/travail_4320/OpenAI-YM-20261028
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=16 LC_ALL=C.UTF-8
ulimit -s 1048576 2>/dev/null
ts(){ date -u '+%F %T UTC'; }
mkdir -p $R/m0 $R/nano
( cd $OA && lake env printenv LEAN_PATH ) > $R/leanpath4320.txt 2>$J/leanpath.err
LP=$(cat $R/leanpath4320.txt)
echo "[$(ts)] DEBUT main (Lean $(lean --version | head -1))" > $J/main.log
sha256sum $R/src/main.lean >> $J/main.log
cp $R/src/main.lean $R/m0/CentreZNRejeu.lean
T0=$(date +%s)
LEAN_PATH=$LP nice -n 10 timeout 3000 lean -R $R/m0 -o $R/m0/CentreZNRejeu.olean $R/m0/CentreZNRejeu.lean > $J/main.out 2>&1; echo "RC=$?" >> $J/main.out
echo "[$(ts)] compile fini en $(( $(date +%s)-T0 )) s ; $(tail -1 $J/main.out)" >> $J/main.log
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
DECLS=$(for n in centre_flip_bound twist_ratio_bound rho_crude rho_two sharp_one_plaquette centre_flip_bound_crude twist_ratio_bound_crude recover_column_flip_bound recover_twist_ratio_bound mixed_word_neutral wilson_centre_flip_bound torus_charge_explicit torus_charge_sum torus_charge_image wilson_twist_ratio_torus wilson_twist_ratio_torus_crude; do printf 'CentreZN.%s ' $n; done)
if grep -q '^RC=0$' $J/main.out; then
  T0=$(date +%s)
  LEAN_PATH=$LP:$R/m0 nice -n 10 timeout 1800 /work/outils/bin/lean4export CentreZNRejeu -- $BUILTINS $DECLS > $R/nano/zn.ndjson 2> $J/export.err; echo "export RC=$? lignes=$(wc -l < $R/nano/zn.ndjson) duree=$(( $(date +%s)-T0 )) s" >> $J/main.log
  sha256sum $R/nano/zn.ndjson >> $J/main.log
  PP=$(echo $DECLS | sed 's/[^ ][^ ]*/"&"/g; s/ /, /g')
  cat > $R/nano/zn.json <<JSON
{ "export_file_path": "$R/nano/zn.ndjson", "use_stdin": false, "num_threads": 16, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"], "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true, "pp_declars": [$PP], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$R/nano/zn_pp.txt", "print_success_message": true }
JSON
  : > $R/nano/zn_pp.txt; T0=$(date +%s)
  /usr/bin/time -v -o $J/nanoda.time nice -n 10 timeout 3600 /work/outils/bin/nanoda_bin $R/nano/zn.json > $J/nanoda.log 2>&1; echo "nanoda RC=$? duree=$(( $(date +%s)-T0 )) s" >> $J/main.log
  tail -3 $J/nanoda.log >> $J/main.log; egrep "Maximum resident|Elapsed" $J/nanoda.time >> $J/main.log
  cp $R/nano/zn_pp.txt $J/nanoda_pp.txt 2>/dev/null
else echo "compilation non reussie : pas d'export" >> $J/main.log; fi
echo "[$(ts)] FIN main" >> $J/main.log; echo DONE > $J/FIN_main
