#!/bin/bash
export PATH=/work/home/.cargo/bin:/usr/bin:/bin HOME=/work/home CARGO_BUILD_JOBS=16 CARGO_TARGET_DIR=/work/arene/logicaffeine/target
cd /work/arene/logicaffeine || exit 1
git log -1 --format=%H
date -u +%FT%TZ
S=$(date +%s)
nice -n 10 /usr/bin/time -v cargo build --locked --profile arena -p logicaffeine-kernel --features unchecked-access --example logos_kernel
echo "RC=$? duree=$(( $(date +%s)-S )) s"
sha256sum target/arena/examples/logos_kernel
