#!/bin/bash
export PATH=/work/home/.cargo/bin:/usr/bin:/bin HOME=/work/home
cd /work/arene
{
echo "date: $(date -u +%FT%TZ)"
for d in nano-lean logicaffeine lean-kernel-arena; do (cd $d; echo "== $d $(git log -1 --format='%H %cd')"; git remote get-url origin; git status --short | head -3); done
echo; head -3 nano-lean/LICENSE; head -3 logicaffeine/LICENSE.md; grep -n "^authors\|^license" nano-lean/Cargo.toml logicaffeine/Cargo.toml logicaffeine/crates/logicaffeine_kernel/Cargo.toml
cd nano-lean; rustc -V; cargo -V; cat rust-toolchain.toml; cd ..
cd logicaffeine; (cd /work/arene/logicaffeine; rustc -V) ; cat rust-toolchain* 2>/dev/null | head; cd ..
sha256sum nano-lean/target/release/nl-fast nano-lean/target/release/nl-ref logicaffeine/target/arena/examples/logos_kernel /work/export/joint.ndjson
head -c 300 /work/export/joint.ndjson | head -1
grep -c "" /dev/null
} > journaux/INFO_construction.txt 2>&1
cat journaux/INFO_construction.txt
