#!/bin/bash
# (a) Empreintes du dépôt d'OpenAI (clone en lecture seule) et écart de PublicTheory.lean.
. $(dirname $0)/common.sh
exec > $OUT/a_empreintes.out 2>&1
date '+%F %T'
cd $SRC
echo "HEAD = $(git -c safe.directory='*' rev-parse HEAD)"
echo "--- SOURCES.sha256 d'OpenAI contre le dépôt"
sha256sum -c SOURCES.sha256 > $OUT/a_sources_sha256_c.txt 2>&1; echo "RC=$? ; OK=$(grep -c ': OK$' $OUT/a_sources_sha256_c.txt) ; non-OK=$(grep -vc ': OK$' $OUT/a_sources_sha256_c.txt)"
echo "lignes de SOURCES.sha256 : $(grep -c '' SOURCES.sha256)"
echo "--- notre liste (paquet) envoi/nos/SHA256SUMS_SOURCES (9508 lignes attendues)"
sha256sum -c $PK/envoi/nos/SHA256SUMS_SOURCES > $OUT/a_nos_sha256_c.txt 2>&1; echo "RC=$? ; OK=$(grep -c ': OK$' $OUT/a_nos_sha256_c.txt) ; non-OK=$(grep -vc ': OK$' $OUT/a_nos_sha256_c.txt)"
echo "fichiers du dépôt hors .git : $(find . -path ./.git -prune -o -type f -print | wc -l)"
echo "--- PublicTheory.lean"
echo "recalculé : $(sha256sum PublicTheory.lean)"
echo "challenge.sha256 ligne 1 : $(sed -n 1p verification/challenge.sha256)"
echo "SOURCES.sha256 ligne 10 : $(sed -n 10p SOURCES.sha256)"
echo "verified-sources.sha256 ligne 1 : $(sed -n 1p verification/verified-sources.sha256)"
echo "joint-check.log ligne 5 : $(sed -n 5p verification/joint-check.log)"
echo "--- verified-sources.sha256 (20 fichiers) contre SOURCES.sha256 : fichiers dont l'empreinte diffère"
awk 'NR==FNR{h[$2]=$1;next}{ if(!($2 in h)) print "absent de SOURCES.sha256 : " $2; else if(h[$2]!=$1) print "DIFFERE : " $2 " " $1 " (SOURCES: " h[$2] ")"; else n++ } END{print "identiques : " n}' SOURCES.sha256 verification/verified-sources.sha256
echo "--- challenge.sha256 (8 fichiers) contre SOURCES.sha256"
awk 'NR==FNR{h[$2]=$1;next}{ if(!($2 in h)) print "absent : " $2; else if(h[$2]!=$1) print "DIFFERE : " $2; else n++ } END{print "identiques : " n}' SOURCES.sha256 verification/challenge.sha256
echo "--- le second condensat apparaît-il quelque part dans le dépôt ?"
grep -rIl --exclude-dir=.git 3940e8dd960e2170d214e575819cfd0fab78aaf1d46f688c49ed0840aa003a55 . | sed 's/^/  occurrence : /'
echo "--- 37 transformations ne sont PAS rejouées (contrôle du pilote, non refait)"
date '+%F %T'
