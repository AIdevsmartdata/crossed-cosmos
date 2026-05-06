#!/usr/bin/env bash
# submit.sh — P6: Cassini-Palatini PRD arXiv package builder
set -euo pipefail

PAPER_ID="p6_cassini_prd"
SRC_DIR="/root/crossed-cosmos/submission/prd_cassini_palatini"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

if [ ! -f "${SRC_DIR}/cassini_palatini_prd.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 in ${SRC_DIR}"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/cassini_palatini_prd.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/cassini_palatini_prdNotes.bib" ] && cp "${SRC_DIR}/cassini_palatini_prdNotes.bib" "${STAGE_DIR}/"

cat > "${STAGE_DIR}/README.txt" << 'README'
P6 — ECI Cassini-clean scalar field: Palatini sub-branch + real-data posterior (3-6pp)
Author: Kévin Remondière (K. Remondière), Independent researcher, Tarbes, France
Email: kevin.remondiere@gmail.com
Target: Physical Review D Letters (PRD)
arXiv categories: gr-qc (primary), hep-ph, astro-ph.CO
Compile: pdflatex cassini_palatini_prd && bibtex cassini_palatini_prd && pdflatex x2
NOTE: xi_chi rail-saturation at -0.024 is a boundary artifact — discuss in paper.
STATUS: SUBMISSION-READY (no pending M33 fixes beyond xi_chi note)
KSTD26 arXiv:2604.16226 live-verified 2026-05-05.
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
