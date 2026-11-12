#!/bin/bash
# Vérifications complémentaires du théorème prouvé (pilote, 11/11/2026). À lancer sous lean sur la machine louée.
# (1) recompilation sous Lean 4.32.2 ; (2) export de la clôture et rejeu par le noyau indépendant nanoda (binaire non modifié).
set -u
T=/work/lean_tube; F=$T/complet_1.lean; M=$T/mod; mkdir -p $M $T/nanoda
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
# (1) Lean 4.32.2
[ -s $T/verif_4322.out ] || ( cd /work/travail_4322/OpenAI-YM-20261028 && env PATH=/work/tc/4.32.2/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8 nice -n 5 timeout 1200 lake env lean $F > $T/verif_4322.out 2>&1; echo "RC=$?" >> $T/verif_4322.out )
# (2) module compilé sous 4.32.0, export, nanoda
cp $F $M/ColumnFlipComplet.lean
( cd /work/travail_4320/OpenAI-YM-20261028 && env PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8 bash -c "nice -n 5 timeout 1200 lake env lean -R $M -o $M/ColumnFlipComplet.olean $M/ColumnFlipComplet.lean > $T/olean.out 2>&1; echo RC=\$? >> $T/olean.out; LP=\$(lake env printenv LEAN_PATH); LEAN_PATH=\$LP:$M nice -n 5 timeout 1800 /work/outils/bin/lean4export ColumnFlipComplet -- $BUILTINS TubeAreaVerif.enonce_canonique TubeArea.column_flip_bound > $T/nanoda/colonne.ndjson 2> $T/nanoda/export.err; echo RC=\$? > $T/nanoda/export.rc" )
wc -l < $T/nanoda/colonne.ndjson > $T/nanoda/export.lignes; sha256sum $T/nanoda/colonne.ndjson > $T/nanoda/colonne.sha256
cat > $T/nanoda/colonne.json <<JSON
{ "export_file_path": "$T/nanoda/colonne.ndjson", "use_stdin": false,
  "num_threads": 16, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": ["TubeAreaVerif.enonce_canonique"], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$T/nanoda/colonne_pp.txt",
  "print_success_message": true }
JSON
: > $T/nanoda/colonne_pp.txt
/usr/bin/time -v -o $T/nanoda/nanoda.time nice -n 5 timeout 3600 /work/outils/bin/nanoda_bin $T/nanoda/colonne.json > $T/nanoda/nanoda.log 2>&1; echo "RC=$?" > $T/nanoda/nanoda.rc
date '+%F %T' > $T/nanoda/FIN
