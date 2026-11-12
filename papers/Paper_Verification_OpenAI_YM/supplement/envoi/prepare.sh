#!/bin/bash
# Préparation (utilisateur lean, RÉSEAU OUVERT, aucun fichier d'OpenAI n'est compilé ici) : sources vérifiées, toolchains
# officielles vérifiées, cache Mathlib officiel de la révision épinglée, outils du noyau indépendant.
set -u
W=/work; E=$W/etat; L=$W/journaux; mkdir -p $E $L $W/tc $W/home $W/export/logs $W/outils/bin
cd $W
git clone --quiet https://github.com/yang-mills-group/OpenAI-YM-20261028 $W/src/OpenAI-YM-20261028
H=$(git -C $W/src/OpenAI-YM-20261028 rev-parse HEAD); echo "$H" > $L/head_sources.txt
[ "$H" = 3456e5e75cf8d4cd558955a5c7638fba2d68f464 ] || { echo "HEAD inattendu $H" > $E/ECHEC_sources; exit 1; }
( cd $W/src/OpenAI-YM-20261028 && sha256sum --quiet -c $W/nos/SHA256SUMS_SOURCES ) > $L/empreintes_sources.log 2>&1 && echo "OK $(wc -l < $W/nos/SHA256SUMS_SOURCES) fichiers" > $E/sources_ok || { echo ECHEC > $E/ECHEC_empreintes; exit 1; }
dl(){ v=$1; s=$2; curl -sSL --fail -o $W/tc/lean-$v.tar.zst https://github.com/leanprover/lean4/releases/download/v$v/lean-$v-linux.tar.zst && echo "$s  $W/tc/lean-$v.tar.zst" | sha256sum -c - >> $L/toolchains.log 2>&1 && mkdir -p $W/tc/$v && tar -C $W/tc/$v --strip-components=1 --zstd -xf $W/tc/lean-$v.tar.zst && rm $W/tc/lean-$v.tar.zst && $W/tc/$v/bin/lean --version >> $L/toolchains.log; }
dl 4.32.0 fca846f3588724a38ad19ee40292c67cb7438d7555903372e3308eef795ba516 || { echo ECHEC > $E/ECHEC_tc4320; exit 1; }
dl 4.32.2 5f2069e6f5db73780f374ccb49ce8ea649aa20a0cebf0116816744c999ce72aa || echo ECHEC > $E/ECHEC_tc4322
dl 4.35.0 7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d || echo ECHEC > $E/ECHEC_tc4350
mkdir -p $W/travail_4320 && cp -r $W/src/OpenAI-YM-20261028 $W/travail_4320/ && rm -rf $W/travail_4320/OpenAI-YM-20261028/.git
cd $W/travail_4320/OpenAI-YM-20261028
env PATH=$W/tc/4.32.0/bin:/usr/bin:/bin HOME=$W/home lake exe cache get > $L/cache_get.log 2>&1; echo "RC=$?" > $E/cache_get.rc
{ sha256sum lake-manifest.json; sha256sum $W/src/OpenAI-YM-20261028/lake-manifest.json; } > $L/manifeste.txt
for d in .lake/packages/*; do r=$(git -C $d rev-parse HEAD); grep -q "\"rev\": \"$r\"" lake-manifest.json && c=CONFORME || c=DIFFERENT; echo "$(basename $d) $r $c modifs=$(git -C $d status --porcelain | wc -l)"; done > $L/revisions_dependances.txt
cd $W/outils
git clone --quiet https://github.com/leanprover/lean4export && git -C lean4export checkout --quiet 4e7915201d3f9f04470d9eae002fa695f7cdc589
( cd lean4export && env PATH=$W/tc/4.32.0/bin:/usr/bin:/bin HOME=$W/home lake build > $L/lean4export_build.log 2>&1; echo "RC=$?" > $E/lean4export.rc )
cp lean4export/.lake/build/bin/lean4export bin/ 2>/dev/null
git clone --quiet https://github.com/ammkrn/nanoda_lib && git -C nanoda_lib checkout --quiet 0da9f98feadd3a0a2ef4b3dbcf52a298a6fef929
curl -sSf https://sh.rustup.rs | env HOME=$W/home sh -s -- -y --profile minimal --default-toolchain 1.97.0 > $L/rustup.log 2>&1
( cd nanoda_lib && env HOME=$W/home PATH=$W/home/.cargo/bin:/usr/bin:/bin cargo build --release --locked > $L/nanoda_build.log 2>&1; echo "RC=$?" > $E/nanoda.rc )
cp nanoda_lib/target/release/nanoda_bin bin/ 2>/dev/null
sha256sum bin/* > $L/outils_sha256.txt 2>&1
date '+%F %T' > $E/prepare.fin
