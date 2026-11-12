#!/bin/bash
# (h) comptage des déclarations Vintage.* dans le relevé d'usage d'OpenAI (verification/declaration-usage.tsv) et dans Barrel.lean.
. $(dirname $0)/common.sh
exec > $OUT/h_vintage.out 2>&1
T=$SRC/verification/declaration-usage.tsv
echo "sha256 $(sha256sum $T)"; echo "lignes $(grep -c '' $T)"; head -1 $T
echo "--- déclarations dont le NOM (colonne 2) commence par Vintage."
awk -F'\t' 'NR>1 && $2 ~ /^Vintage\./ {n++; if($3=="used")u++; m[$1]++} END{print "total " n " ; used " u " ; modules " length(m)}' $T
awk -F'\t' 'NR>1 && $2 ~ /^Vintage\./ {t[$1]++; if($3=="used")s[$1]++} END{for(k in t) print "  " k " : " t[k] " (used " s[k]+0 ")"}' $T | sort
echo "--- sans le module YM.UVExtension.Orchard.First"
awk -F'\t' 'NR>1 && $2 ~ /^Vintage\./ && $1!="YM.UVExtension.Orchard.First" {n++; if($3=="used")u++} END{print "fabriquees (hors First) " n " ; used " u}' $T
echo "--- témoin de tête (colonne 4) des lignes Vintage used"
awk -F'\t' 'NR>1 && $2 ~ /^Vintage\./ && $3=="used" {print $4}' $T | sort | uniq -c
echo "--- Barrel.lean : taille et emplois de la commande"
wc -l $SRC/YM/UVExtension/Orchard/Barrel.lean
echo "emplois 'vintage ...' en debut de ligne dans YM/ : $(grep -rE '^vintage[[:space:]]+' $SRC/YM | wc -l) ; occurrences du mot vintage (insensible a la casse) dans YM/ hors Barrel.lean : $(grep -rIi 'vintage' $SRC/YM --include=*.lean | grep -v 'Barrel.lean' | wc -l) ; lignes 'vintage ' (avec espace) : $(grep -rIE '(^|[^A-Za-z.])vintage[[:space:]]+[A-Za-z]' $SRC/YM --include=*.lean | grep -v Barrel.lean | wc -l)"
R13="Challenge ChallengeSpec ConcreteSU2 Construction ContactBridge ContactSpec HierarchyBridge PublicTheory PublicView PublicWilson Solution TraceBridge WilsonBridge"
F13=""; for r in $R13; do F13="$F13 $SRC/$r.lean"; done
echo "--- fichiers de YM/ et des 13 fichiers racine de la construction qui font 'import Lean' ou 'open Lean...'"
grep -lE '^import Lean$|^open Lean|^import Lean\.' -r $SRC/YM $F13 | sed 's/^/  /'
echo "--- (les scripts racine Verify.lean et VerifyJoint.lean, hors construction, importent Lean aussi : $(grep -lE '^import Lean' $SRC/Verify.lean $SRC/VerifyJoint.lean | wc -l))"
for k in native_decide implemented_by skipKernelTC simproc declare_syntax_cat '^opaque' '^unsafe' 'unsafe '; do echo "$k : $(grep -rIE "$k" $SRC/YM $F13 --include=*.lean | wc -l)"; done
echo "partial def : "; grep -rIn 'partial def' $SRC/YM $F13 --include=*.lean | sed 's/^/  /'
echo "maxHeartbeats/maxRecDepth dans lakefile.toml : "; grep -n -iE 'heartbeats|recdepth|leanOptions|weak' $SRC/lakefile.toml | sed 's/^/  /'
