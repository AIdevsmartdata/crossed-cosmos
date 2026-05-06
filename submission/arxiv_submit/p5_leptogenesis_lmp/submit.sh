#!/usr/bin/env bash
# submit.sh — P5: Leptogenesis CSD(1+sqrt6) LMP arXiv package builder
set -euo pipefail

PAPER_ID="p5_leptogenesis_lmp"
SRC_DIR="/root/crossed-cosmos/submission/lmp_leptogenesis_csd1sqrt6"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

if [ ! -f "${SRC_DIR}/leptogenesis_csd_LMP.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 in ${SRC_DIR}"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/leptogenesis_csd_LMP.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/leptogenesis_csd_LMPNotes.bib" ] && cp "${SRC_DIR}/leptogenesis_csd_LMPNotes.bib" "${STAGE_DIR}/"

cat > "${STAGE_DIR}/README.txt" << 'README'
P5 — CSD(1+sqrt6) leptogenesis: structural fingerprint from S'_4 at tau=i (3-6pp)
Author: Kévin Remondière (K. Remondière), Independent researcher, Tarbes, France
Email: kevin.remondiere@gmail.com
Target: Letters in Mathematical Physics (Springer) [hep-ph sector]
arXiv category: hep-ph
Compile: pdflatex leptogenesis_csd_LMP && bibtex leptogenesis_csd_LMP && pdflatex x2
NOTE: revtex4-2 PRL format — arXiv auto-TeXing should handle this fine.
STATUS: SUBMISSION-READY (no pending M33 fixes for this paper)
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
