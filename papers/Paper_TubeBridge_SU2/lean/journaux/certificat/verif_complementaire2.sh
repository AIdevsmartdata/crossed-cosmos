#!/bin/bash
# Vérifications complémentaires du théorème prouvé (pilote, 11/11/2026). À lancer sous lean sur la machine louée.
# (1) recompilation sous Lean 4.32.2 ; (2) export de la clôture et rejeu par le noyau indépendant nanoda (binaire non modifié).
set -u
T=/work/lean_tube; F=$T/su2_3.lean; M=$T/mod; mkdir -p $M $T/nanoda2
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
# (1) Lean 4.32.2
[ -s $T/verif2_4322.out ] || ( cd /work/travail_4322/OpenAI-YM-20261028 && env PATH=/work/tc/4.32.2/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8 nice -n 5 timeout 1200 lake env lean $F > $T/verif2_4322.out 2>&1; echo "RC=$?" >> $T/verif2_4322.out )
# (2) module compilé sous 4.32.0, export, nanoda
cp $F $M/TubeComplet.lean
( cd /work/travail_4320/OpenAI-YM-20261028 && env PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8 bash -c "nice -n 5 timeout 1200 lake env lean -R $M -o $M/TubeComplet.olean $M/TubeComplet.lean > $T/olean2.out 2>&1; echo RC=\$? >> $T/olean2.out; LP=\$(lake env printenv LEAN_PATH); LEAN_PATH=\$LP:$M nice -n 5 timeout 1800 /work/outils/bin/lean4export TubeComplet -- $BUILTINS TubeAreaVerif.enonce_canonique_A TubeAreaVerif.enonce_canonique_B TubeArea.wilson_column_flip_bound TubeArea.sharp_one_edge TubeArea.column_flip_bound > $T/nanoda2/tube.ndjson 2> $T/nanoda2/export.err; echo RC=\$? > $T/nanoda2/export.rc" )
wc -l < $T/nanoda2/tube.ndjson > $T/nanoda2/export.lignes; sha256sum $T/nanoda2/tube.ndjson > $T/nanoda2/tube.sha256
cat > $T/nanoda2/tube.json <<JSON
{ "export_file_path": "$T/nanoda2/tube.ndjson", "use_stdin": false,
  "num_threads": 16, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": ["TubeAreaVerif.enonce_canonique_A", "TubeAreaVerif.enonce_canonique_B", "TubeArea.wilson_column_flip_bound"], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$T/nanoda2/tube_pp.txt",
  "print_success_message": true }
JSON
: > $T/nanoda2/tube_pp.txt
/usr/bin/time -v -o $T/nanoda2/nanoda.time nice -n 5 timeout 3600 /work/outils/bin/nanoda_bin $T/nanoda2/tube.json > $T/nanoda2/nanoda.log 2>&1; echo "RC=$?" > $T/nanoda2/nanoda.rc
date '+%F %T' > $T/nanoda2/FIN
