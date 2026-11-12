#!/bin/bash
# Machine louée (conteneur jetable) : paquets de base et utilisateur sans droits. Aucun secret ici.
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null && apt-get install -y -qq git curl zstd ca-certificates build-essential python3 time xz-utils util-linux procps rsync >/dev/null
id lean >/dev/null 2>&1 || useradd -m -s /bin/bash lean
mkdir -p /work && chown lean: /work
echo "coeurs $(nproc)"; free -g | sed -n 2p; df -h /work | tail -1; uname -r; lscpu | grep "Model name" | head -1
runuser -u lean -- unshare -rn true 2>/dev/null && echo UNSHARE_OK || echo UNSHARE_NON
