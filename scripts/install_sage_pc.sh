#!/usr/bin/env bash
# install_sage_pc.sh — install SageMath via mamba/conda-forge on PC gamer
# Usage:  bash install_sage_pc.sh
# No sudo required. ~30 min total. ~2 GB disk.

set -euo pipefail
LOG=/tmp/install_sage_$(date +%s).log
exec > >(tee -a "$LOG") 2>&1
echo "[install_sage] start at $(date); log=$LOG"

# ----- 1. miniforge -------------------------------------------------------
if [ -d "$HOME/miniforge3" ]; then
  echo "[install_sage] miniforge3 already present at $HOME/miniforge3"
else
  echo "[install_sage] downloading miniforge installer (~110 MB) ..."
  curl -fsSL -o /tmp/miniforge.sh \
    https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
  echo "[install_sage] running miniforge installer ..."
  bash /tmp/miniforge.sh -b -p "$HOME/miniforge3"
  rm -f /tmp/miniforge.sh
fi

export PATH="$HOME/miniforge3/bin:$PATH"
hash -r

# Add to ~/.bashrc once
if ! grep -qF 'miniforge3/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/miniforge3/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo "[install_sage] mamba: $(mamba --version 2>&1 | head -1)"

# ----- 2. sage env -------------------------------------------------------
if mamba env list | grep -q '^sage '; then
  echo "[install_sage] env 'sage' already exists; skipping create"
else
  echo "[install_sage] creating env 'sage' from conda-forge (~25 min, ~1.5 GB) ..."
  mamba create -n sage -c conda-forge -y sage python=3.11
fi

# ----- 3. activate + verify ----------------------------------------------
# shellcheck source=/dev/null
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate sage

echo "[install_sage] sage path: $(which sage)"
echo "[install_sage] sage version:"
sage --version

echo "[install_sage] quick smoke test (sage -c '1+1') ..."
sage -c "print('SAGE_OK', 1+1)"

# ----- 4. ready message --------------------------------------------------
cat <<EOF

[install_sage] ✓ DONE.

To use sage in a new shell:
  source ~/miniforge3/etc/profile.d/conda.sh
  conda activate sage
  sage --version

Or just:
  ~/miniforge3/envs/sage/bin/sage --version

Next step: run the ECI falsifier scripts.
  cd /home/remondiere/crossed-cosmos
  scp from VPS srv1637824:/root/crossed-cosmos/notes/eci_v7_aspiration/M63_SAGE_SCRIPTS/r3_c1_falsifier.sage .
  ~/miniforge3/envs/sage/bin/sage r3_c1_falsifier.sage --numerical-only

Log: $LOG
EOF
