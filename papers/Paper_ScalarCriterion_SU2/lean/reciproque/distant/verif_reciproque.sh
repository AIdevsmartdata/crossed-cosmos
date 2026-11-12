#!/bin/bash
# Vérifications complémentaires CentreZN (pilote, 12/11/2026), adapté de flux_tube_2026-11-11/lean_protege/verif_generique.sh.
# À lancer sous l'utilisateur lean sur la machine louée. Usage : verif_zn.sh FICHIER.lean ETIQUETTE MODULE "decl1 decl2 ..."
# (1) module compilé en .olean sous Lean 4.32.0 (seule chaîne présente sur cette location) ; (2) export de la clôture des
# déclarations par lean4export ; (3) rejeu par le noyau indépendant nanoda (binaire non modifié), axiomes permis : les trois.
set -u
F=$1; TAG=$2; MOD=$3; DECLS=$4
T=/work/lean_reciproque_1112; M=$T/mod_$TAG; N=$T/nanoda_$TAG; mkdir -p $M $N
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
cp $F $M/$MOD.lean
( cd /work/travail_4320/OpenAI-YM-20261028 && env PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8 bash -c "nice -n 10 timeout 1500 lake env lean -R $M -o $M/$MOD.olean $M/$MOD.lean > $T/olean_$TAG.out 2>&1; echo RC=\$? >> $T/olean_$TAG.out; LP=\$(lake env printenv LEAN_PATH); LEAN_PATH=\$LP:$M nice -n 10 timeout 1800 /work/outils/bin/lean4export $MOD -- $BUILTINS $DECLS > $N/zn.ndjson 2> $N/export.err; echo RC=\$? > $N/export.rc" )
wc -l < $N/zn.ndjson > $N/export.lignes; sha256sum $N/zn.ndjson > $N/zn.sha256
PP=$(echo $DECLS | sed 's/[^ ][^ ]*/"&"/g; s/ /, /g')
cat > $N/zn.json <<JSON
{ "export_file_path": "$N/zn.ndjson", "use_stdin": false,
  "num_threads": 16, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": [$PP], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$N/zn_pp.txt",
  "print_success_message": true }
JSON
: > $N/zn_pp.txt
/usr/bin/time -v -o $N/nanoda.time nice -n 10 timeout 3600 /work/outils/bin/nanoda_bin $N/zn.json > $N/nanoda.log 2>&1; echo "RC=$?" > $N/nanoda.rc
date '+%F %T' > $N/FIN
