#!/bin/bash
# Seconde version de Lean (4.32.2) pour CentreZN : extraction de la chaine tc/4.32.2 et du .lake 4.32.2 (archives locales du 11/11,
# envoyees dans /work/lean_zn_rejeu_1112/), compilation de main.lean (Mathlib recompile sous 4.32.2), lecture des axiomes.
# A lancer SOUS L'UTILISATEUR lean. Aucune ecriture hors de /work/lean_zn_rejeu_1112.
set -u
R=/work/lean_zn_rejeu_1112; J=$R/out; ts(){ date -u '+%F %T UTC'; }
cd $R
echo "[$(ts)] extraction" > $J/r4322.log
zstd -dc tc.tar.zst | tar -xf - -C $R/tc 2>>$J/r4322.err
ls $R/tc >> $J/r4322.log
mkdir -p $R/ws4322 && zstd -dc actif_lean_4322.tar.zst | tar -xf - -C $R/ws4322 2>>$J/r4322.err
echo "[$(ts)] extrait ; $(ls $R/ws4322 | tr '\n' ' ')" >> $J/r4322.log
L=$(find $R/tc -maxdepth 3 -type d -name bin | head -5 | tr '\n' ' '); echo "bin dirs: $L" >> $J/r4322.log
BIN=$(find $R/tc -maxdepth 3 -type d -path '*4.32.2*' -name bin | head -1); echo "BIN=$BIN" >> $J/r4322.log
export PATH=$BIN:/usr/bin:/bin HOME=/work/home LEAN_NUM_THREADS=16 LC_ALL=C.UTF-8
ulimit -s 1048576 2>/dev/null
lean --version >> $J/r4322.log 2>&1
LP=$(for d in $R/ws4322/.lake/packages/*/.lake/build/lib/lean $R/ws4322/.lake/build/lib/lean; do [ -d $d ] && printf '%s:' $d; done)
echo "LEAN_PATH=$LP" >> $J/r4322.log
mkdir -p $R/m1; cp $R/src/main.lean $R/m1/CentreZNRejeu.lean
sha256sum $R/m1/CentreZNRejeu.lean >> $J/r4322.log
T0=$(date +%s)
LEAN_PATH=$LP nice -n 10 timeout 3000 lean -R $R/m1 -o $R/m1/CentreZNRejeu.olean $R/m1/CentreZNRejeu.lean > $J/main4322.out 2>&1; echo "RC=$?" >> $J/main4322.out
echo "[$(ts)] compile 4.32.2 fini en $(( $(date +%s)-T0 )) s ; $(tail -1 $J/main4322.out)" >> $J/r4322.log
# export + nanoda si possible (le binaire lean4export est celui de 4.32.0 : peut refuser des .olean 4.32.2)
if grep -q '^RC=0$' $J/main4322.out; then
  BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
  DECLS=$(for n in centre_flip_bound twist_ratio_bound rho_crude rho_two sharp_one_plaquette centre_flip_bound_crude twist_ratio_bound_crude recover_column_flip_bound recover_twist_ratio_bound mixed_word_neutral wilson_centre_flip_bound torus_charge_explicit torus_charge_sum torus_charge_image wilson_twist_ratio_torus wilson_twist_ratio_torus_crude; do printf 'CentreZN.%s ' $n; done)
  mkdir -p $R/nano2
  LEAN_PATH=$LP:$R/m1 timeout 1800 /work/outils/bin/lean4export CentreZNRejeu -- $BUILTINS $DECLS > $R/nano2/zn.ndjson 2> $J/export4322.err; echo "export 4.32.2 RC=$? lignes=$(wc -l < $R/nano2/zn.ndjson)" >> $J/r4322.log
  head -c 400 $J/export4322.err >> $J/r4322.log
fi
echo DONE > $J/FIN_4322
