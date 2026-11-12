#!/bin/bash
# Fonctions communes du rejeu non-auteur (à sourcer). Exécuté par l'utilisateur lean, nice 10, dans /work/rejeu_rapport.
W=/work/rejeu_rapport; PK=$W/paquet/supplement; OUT=$W/out; SRC=/work/src/OpenAI-YM-20261028
mkdir -p $OUT
refdir(){ echo /work/travail_$1/OpenAI-YM-20261028; }          # compilation de référence, LECTURE SEULE
leanpath(){ local p=$(refdir $1); local tc=/work/tc/$2; local s=""
  for d in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do s="$s$p/.lake/packages/$d/.lake/build/lib/lean:"; done
  echo "$s$p/.lake/build/lib/lean:$tc/lib/lean"; }              # même ordre que `lake env printenv LEAN_PATH`
envlean(){ # $1 = 4320|4322, $2 = toolchain (4.32.0|4.32.2), $3 = fils ; imprime le préfixe `env`
  echo "env -i PATH=/work/tc/$2/bin:/usr/bin:/bin HOME=/work/home LC_ALL=C.UTF-8 LEAN_NUM_THREADS=$3 LEAN_PATH=$(leanpath $1 $2)"; }
run1(){ # run1 NOM cmd... : journalise sortie, erreur, code, durée et mémoire (comme interne_verifs_copie.sh)
  local n=$1; shift; date '+%F %T' > $OUT/$n.debut
  /usr/bin/time -v -o $OUT/$n.time "$@" > $OUT/$n.out 2> $OUT/$n.err; echo "RC=$?" > $OUT/$n.rc
  date '+%F %T' > $OUT/$n.fin; }
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
