#!/usr/bin/env bash
# submit.sh — P1: P-NT BLMS paper arXiv package builder
# Usage: bash submit.sh [--dry-run]
# Output: p1_pnt_blms_arxiv.tar.gz

set -euo pipefail

PAPER_ID="p1_pnt_blms"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/PNT"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

# --- pre-flight ---
if [ ! -f "${SRC_DIR}/paper_lmfdb_s4prime.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 first in ${SRC_DIR}"
    echo "  cd ${SRC_DIR} && pdflatex paper_lmfdb_s4prime && bibtex paper_lmfdb_s4prime && pdflatex paper_lmfdb_s4prime && pdflatex paper_lmfdb_s4prime"
fi

# --- stage ---
rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/paper_lmfdb_s4prime.tex" "${STAGE_DIR}/"

# Copy .bib if present
[ -f "${SRC_DIR}/paper_lmfdb_s4prime.bib" ] && cp "${SRC_DIR}/paper_lmfdb_s4prime.bib" "${STAGE_DIR}/"
# Copy eci.bib if referenced
[ -f "/root/crossed-cosmos/eci.bib" ] && cp "/root/crossed-cosmos/eci.bib" "${STAGE_DIR}/"

# Copy figures (none currently; placeholder)
# cp "${SRC_DIR}/fig_*.pdf" "${STAGE_DIR}/" 2>/dev/null || true

cat > "${STAGE_DIR}/README.txt" << 'README'
P1 — Two LMFDB identifications for hatted weight-5 multiplets of S'_4
Author: Kévin Remondière, Independent researcher, Tarbes, France
Target: Bulletin of the London Mathematical Society / Math. Research Letters
arXiv category: math.NT
Compile: pdflatex paper_lmfdb_s4prime && bibtex paper_lmfdb_s4prime && pdflatex x2
Anti-hallucination: all LMFDB labels and arXiv IDs live-verified 2026-05-04/05.
README

# --- archive ---
if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
    echo "Size: $(du -sh ${ARCHIVE} | cut -f1)"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
