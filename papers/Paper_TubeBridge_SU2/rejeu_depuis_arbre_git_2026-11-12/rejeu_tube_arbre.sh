#!/bin/bash
# Rejeu du Lean de la note « tube / pont » depuis l'ARCHIVE GIT du dossier Paper_TubeBridge_SU2 (non-auteur : Claude Sonnet 5.5).
# Execute sur la machine louee SOUS L'UTILISATEUR lean. Entrees dans /work/rejeu_tube_1112/ : tube_arbre.tar.gz (git archive) et ce script.
# Environnement SEUL pris hors de l'archive : Lean 4.32.0 (/work/tc/4.32.0), Mathlib compile et projet d'OpenAI compile (/work/travail_4320/OpenAI-YM-20261028), lean4export et nanoda (/work/outils/bin).
set -u
R=/work/rejeu_tube_1112; J=$R/journaux; mkdir -p $J
OA=/work/travail_4320/OpenAI-YM-20261028
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=8 LC_ALL=C.UTF-8
ulimit -s 1048576 2>/dev/null
ts(){ date -u '+%F %T UTC'; }
LIM="prlimit --as=68719476736 --"      # 64 GiB d espace d adressage (essai 1 a 16 GiB: echec de mmap des .olean, voir journal)
cd $R || exit 8
echo "[$(ts)] DEBUT ; charge $(cut -d' ' -f1-3 /proc/loadavg) ; $(free -g | awk 'NR==2{print "dispo "$7" Go"}')" > $J/rejeu.log
sha256sum tube_arbre.tar.gz >> $J/rejeu.log
rm -rf arbre mod; mkdir arbre mod
tar xzf tube_arbre.tar.gz -C arbre; echo "[$(ts)] fichiers extraits: $(find arbre -type f | wc -l)" >> $J/rejeu.log
P=$R/arbre/papers/Paper_TubeBridge_SU2
( cd $P && sha256sum -c SHA256SUMS 2>&1 | grep -vc ': OK' ; true ) >> $J/rejeu.log 2>&1
echo "[$(ts)] (ligne precedente : nombre de fichiers du SHA256SUMS NON conformes, attendu 0)" >> $J/rejeu.log
( cd $P/lean && grep -E '^[0-9a-f]{64}' MANIFEST.txt | awk '{print $1"  "$2}' | sha256sum -c - 2>&1 | tail -12 ) >> $J/rejeu.log 2>&1
# mots interdits dans les fichiers Lean de l'archive (hors commentaires, on liste simplement les lignes)
echo "## grep mots interdits (lignes) dans lean/TubePont_pont_6.lean" >> $J/rejeu.log
grep -nE '\b(sorry|admit|native_decide|unsafe|implemented_by|extern)\b|^\s*axiom\b' $P/lean/TubePont_pont_6.lean >> $J/rejeu.log 2>&1; echo "[grep rc=$? ; 1 = aucune ligne]" >> $J/rejeu.log
# (1) compilation du fichier cumulatif DEPUIS L'ARCHIVE, dans le projet d'OpenAI (Lean 4.32.0)
cp $P/lean/TubePont_pont_6.lean mod/TubePontRejeu.lean
sha256sum mod/TubePontRejeu.lean >> $J/rejeu.log
cd $OA || exit 8
echo "[$(ts)] compilation cumulatif" >> $J/rejeu.log; T0=$(date +%s)
nice -n 10 $LIM timeout 3000 lake env lean -R $R/mod -o $R/mod/TubePontRejeu.olean $R/mod/TubePontRejeu.lean > $J/cumulatif.out 2>&1; echo "RC=$?" >> $J/cumulatif.out
echo "[$(ts)] cumulatif fini en $(( $(date +%s)-T0 )) s ; $(tail -1 $J/cumulatif.out)" >> $J/rejeu.log
echo "erreurs: $(grep -c ': error' $J/cumulatif.out) ; avertissements: $(grep -c ': warning' $J/cumulatif.out) ; lignes 'depends on axioms' standard: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $J/cumulatif.out) ; lignes 'does not depend': $(grep -c 'does not depend' $J/cumulatif.out) ; autres 'depends on': $(grep 'depends on axioms' $J/cumulatif.out | grep -vc '\[propext, Classical.choice, Quot.sound\]')" >> $J/rejeu.log
grep -E "depends on axioms|does not depend" $J/cumulatif.out > $J/axiomes.txt
# (2) pied de verification seul : le pied PIED_I.lean de l'archive est la fin du cumulatif ; on le recompile derriere la base gelee de l'archive
cat $P/lean/pieds/PARTIE_ABCDEFGH_pont_gelee.lean > $R/mod/base_gelee.lean
cp $R/mod/base_gelee.lean $R/mod/BaseGeleePied.lean; cat $P/lean/pieds/PIED_I.lean >> $R/mod/BaseGeleePied.lean
echo "[$(ts)] compilation base gelee A--H + PIED_I" >> $J/rejeu.log; T0=$(date +%s)
nice -n 10 $LIM timeout 3000 lake env lean $R/mod/BaseGeleePied.lean > $J/base_gelee_pied.out 2>&1; echo "RC=$?" >> $J/base_gelee_pied.out
echo "[$(ts)] base+pied fini en $(( $(date +%s)-T0 )) s ; $(tail -1 $J/base_gelee_pied.out) ; erreurs $(grep -c ': error' $J/base_gelee_pied.out) ; axiomes standard $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' $J/base_gelee_pied.out)" >> $J/rejeu.log
# (3) export de la cloture et noyau independant nanoda 
DECLS="TubeArea.column_flip_bound TubeArea.sharp_one_edge TubeArea.wilson_column_flip_bound TubeArea.grid_plaq_surjective TubeArea.grid_stokes_rectangle TubeArea.tube_area_law_rectangle TubeArea.neutral_word_flip_invariant TubeArea.mixedWord_neutral TubeArea.wilson_action_area_law_rectangle TubeArea.torus_plaq_explicit TubeArea.torus_plaq_parity TubeArea.torus_plaq_image TubeArea.torus_flip_bound TubeArea.twist_ratio_bound TubeArea.le_of_forall_pow_le_const_mul_pow TubeArea.flux_gap_of_traces TubeArea.wilson_twist_ratio_bound TubeArea.wilson_electric_flux_torus TubeBridge.signedWilsonEnergy_one TubeBridge.openai_wilson_twist_ratio TubeBridge.openai_wilson_twist_ratio_family TubeBridge.su2_neg_one_mem TubeBridge.openai_su2_twist_ratio TubeAreaVerif.enonce_canonique_A TubeAreaVerif.enonce_canonique_B TubeAreaVerif.enonce_canonique_F1 TubeAreaVerif.enonce_canonique_F2 TubeAreaVerif.enonce_canonique_F3 TubeAreaVerif.enonce_canonique_F4 TubeAreaVerif.enonce_canonique_G1 TubeAreaVerif.enonce_canonique_G2 TubeAreaVerif.enonce_canonique_G3 YangMills.su2Theory"
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
N=$R/nanoda; mkdir -p $N
if [ "$(grep -c RC=0 $J/cumulatif.out)" = 1 ]; then
 LP=$(lake env printenv LEAN_PATH)
 echo "[$(ts)] export lean4export" >> $J/rejeu.log; T0=$(date +%s)
 LEAN_PATH=$LP:$R/mod nice -n 10 $LIM timeout 1800 /work/outils/bin/lean4export TubePontRejeu -- $BUILTINS $DECLS > $N/tube.ndjson 2> $N/export.err; echo "export RC=$? lignes=$(wc -l < $N/tube.ndjson) duree=$(( $(date +%s)-T0 )) s" >> $J/rejeu.log
 sha256sum $N/tube.ndjson >> $J/rejeu.log
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
 /usr/bin/time -v -o $N/nanoda.time nice -n 10 $LIM timeout 3600 /work/outils/bin/nanoda_bin $N/tube.json > $J/nanoda.log 2>&1; echo "nanoda RC=$? duree=$(( $(date +%s)-T0 )) s" >> $J/rejeu.log
 tail -3 $J/nanoda.log >> $J/rejeu.log; egrep "Maximum resident|Elapsed" $N/nanoda.time >> $J/rejeu.log
 cp $N/tube_pp.txt $J/nanoda_pp.txt 2>/dev/null
else echo "compilation non reussie : pas d'export" >> $J/rejeu.log; fi
echo "[$(ts)] FIN" >> $J/rejeu.log
echo DONE > $J/FIN
