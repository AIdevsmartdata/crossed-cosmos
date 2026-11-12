#!/bin/bash
# Export lean4export (4.32.0) de constantes ET de toute leur clôture (Init, Mathlib, projet), DANS le bac
# (leanext, réseau coupé), cwd = /work/travail/OpenAI-YM-20261028 (lu en lecture seule par `lake env`).
# usage : interne_export.sh NOM CONSTANTE...      sortie : /work/export/NOM.ndjson + logs/export_NOM.*
set -u
E=/work/export; L=$E/logs; NOM=$1; shift
# Constantes primitives du noyau (liste de Comparator, Main.lean `primitiveTargets` + Quot), comme pour D7.
BUILTINS="Nat String String.mk Char Char.ofNat List eagerReduce optParam autoParam semiOutParam outParam Quot Quot.mk Quot.lift Quot.ind propext Quot.sound Classical.choice Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList"
date '+%F %T' > $L/export_$NOM.debut
/usr/bin/time -v -o $L/export_$NOM.time lake env /work/outils/bin/lean4export ConcreteSU2 -- $BUILTINS "$@" \
  > $E/$NOM.ndjson 2> $L/export_$NOM.err
echo "RC=$?" > $L/export_$NOM.rc
date '+%F %T' > $L/export_$NOM.fin
grep -c PANIC $L/export_$NOM.err > $L/export_$NOM.panic
wc -l < $E/$NOM.ndjson > $L/export_$NOM.lignes
grep -c '"thm":\|"defn":\|"axiom":\|"inductive":\|"opaque":\|"quot":\|"ctor":\|"rec":' $E/$NOM.ndjson > $L/export_$NOM.decls
sha256sum $E/$NOM.ndjson > $E/$NOM.ndjson.sha256
cat /sys/fs/cgroup/ym4calc.slice/$(basename "$(cut -d: -f3 /proc/self/cgroup)")/memory.peak > $L/export_$NOM.mempeak 2>/dev/null
