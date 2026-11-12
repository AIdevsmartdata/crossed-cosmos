#!/bin/bash
export PATH=/work/home/.cargo/bin:/usr/bin:/bin HOME=/work/home CARGO_BUILD_JOBS=16
cd /work/arene/nano-lean || exit 1
git checkout -q v0.3.3 && git log -1 --format=%H
date -u +%FT%TZ
S=$(date +%s)
nice -n 10 /usr/bin/time -v cargo build --release --locked --bin nl-fast --bin nl-ref
echo "RC=$? duree=$(( $(date +%s)-S )) s"
sha256sum target/release/nl-fast target/release/nl-ref
