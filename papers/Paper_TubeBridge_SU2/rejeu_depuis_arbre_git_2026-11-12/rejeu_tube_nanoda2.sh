#!/bin/bash
# Deuxieme passe nanoda (meme environnement et memes conventions que rejeu_tube_arbre.sh) : on reexporte la cloture de declarations PLUS RESTREINTES.
# La passe 1 avait inclus YangMills.su2Theory (theoreme d'OpenAI, hors note) : export de 58 690 813 lignes, interrompu par l'operateur apres 5 min (pas une erreur du noyau).
# Passe 2a = comme le certificat du 11/11 : les cinq declarations TubeBridge.* seules. Passe 2b = les 23 declarations de la note (sans su2Theory).
set -u
R=/work/rejeu_tube_1112; J=$R/journaux; OA=/work/travail_4320/OpenAI-YM-20261028
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8
ulimit -s 1048576 2>/dev/null
ts(){ date -u '+%F %T UTC'; }
LIM="prlimit --as=68719476736 --"
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
D5="TubeBridge.signedWilsonEnergy_one TubeBridge.openai_wilson_twist_ratio TubeBridge.openai_wilson_twist_ratio_family TubeBridge.su2_neg_one_mem TubeBridge.openai_su2_twist_ratio"
D23="TubeArea.column_flip_bound TubeArea.sharp_one_edge TubeArea.wilson_column_flip_bound TubeArea.grid_plaq_surjective TubeArea.grid_stokes_rectangle TubeArea.tube_area_law_rectangle TubeArea.neutral_word_flip_invariant TubeArea.mixedWord_neutral TubeArea.wilson_action_area_law_rectangle TubeArea.torus_plaq_explicit TubeArea.torus_plaq_parity TubeArea.torus_plaq_image TubeArea.torus_flip_bound TubeArea.twist_ratio_bound TubeArea.le_of_forall_pow_le_const_mul_pow TubeArea.flux_gap_of_traces TubeArea.wilson_twist_ratio_bound TubeArea.wilson_electric_flux_torus $D5"
cd $OA || exit 8
LP=$(lake env printenv LEAN_PATH)
for P in 2a 2b; do
 if [ $P = 2a ]; then DECLS="$D5"; else DECLS="$D23"; fi
 N=$R/nanoda_$P; mkdir -p $N; T0=$(date +%s)
 LEAN_PATH=$LP:$R/mod nice -n 10 $LIM timeout 1800 /work/outils/bin/lean4export TubePontRejeu -- $BUILTINS $DECLS > $N/tube.ndjson 2> $N/export.err
 echo "[$(ts)] passe $P : export RC=$? lignes=$(wc -l < $N/tube.ndjson) duree=$(( $(date +%s)-T0 )) s ; $(sha256sum $N/tube.ndjson)" >> $J/rejeu2.log
 PP=$(echo $DECLS | sed 's/[^ ][^ ]*/"&"/g; s/ /, /g')
 cat > $N/tube.json <<JSON
{ "export_file_path": "$N/tube.ndjson", "use_stdin": false,
  "num_threads": 8, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": [$PP], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$N/tube_pp.txt",
  "print_success_message": true }
JSON
 : > $N/tube_pp.txt; T0=$(date +%s)
 /usr/bin/time -v -o $N/nanoda.time nice -n 10 $LIM timeout 3000 /work/outils/bin/nanoda_bin $N/tube.json > $J/nanoda_$P.log 2>&1; echo "[$(ts)] passe $P : nanoda RC=$? duree=$(( $(date +%s)-T0 )) s" >> $J/rejeu2.log
 tail -3 $J/nanoda_$P.log >> $J/rejeu2.log; egrep "Maximum resident|Elapsed" $N/nanoda.time >> $J/rejeu2.log
 cp $N/tube_pp.txt $J/nanoda_pp_$P.txt
 rm -f $N/tube.ndjson.keep
done
echo "[$(ts)] FIN2" >> $J/rejeu2.log
