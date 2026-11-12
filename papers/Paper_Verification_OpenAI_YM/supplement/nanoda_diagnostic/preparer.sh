#!/bin/bash
# À lancer sous l'utilisateur lean, sur la machine louée. Construit un nanoda instrumenté dans /work/diag_nanoda (copie des
# sources ; l'original /work/outils/nanoda_lib et le binaire officiel /work/outils/bin/nanoda_bin ne sont pas touchés).
set -u
D=/work/diag_nanoda
export HOME=/work/home PATH=/work/home/.cargo/bin:/usr/bin:/bin LC_ALL=C.UTF-8
mkdir -p $D && cd $D || exit 2
rm -rf src_copie && mkdir src_copie
( cd /work/outils/nanoda_lib && tar cf - --exclude=./target . ) | ( cd src_copie && tar xf - )
( cd /work/outils/nanoda_lib && find . -path ./target -prune -o -type f -print0 | sort -z | xargs -0 sha256sum ) > sources_origine.sha256
python3 $D/patch_progression.py src_copie/src/tc.rs > patch.log 2>&1 || { echo "ECHEC patch"; cat patch.log; exit 3; }
( cd src_copie && diff -u /work/outils/nanoda_lib/src/tc.rs src/tc.rs > ../patch.diff; nice -n 10 cargo build --release --offline > ../build.log 2>&1; echo "RC=$?" > ../build.rc )
cat build.rc; tail -3 build.log
ls -la src_copie/target/release/nanoda_bin 2>&1
sha256sum /work/outils/bin/nanoda_bin src_copie/target/release/nanoda_bin 2>&1
