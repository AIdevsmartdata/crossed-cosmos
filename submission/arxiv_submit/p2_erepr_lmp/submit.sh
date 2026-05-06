#!/usr/bin/env bash
# submit.sh — P2: ER=EPR / Araki-cocycle LMP arXiv package builder
set -euo pipefail

PAPER_ID="p2_erepr_lmp"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/EREPR_REOPEN"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

if [ ! -f "${SRC_DIR}/erepr_araki_consistency_LMP.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 in ${SRC_DIR}"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/erepr_araki_consistency_LMP.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/erepr_araki_consistency_LMP.bib" ] && cp "${SRC_DIR}/erepr_araki_consistency_LMP.bib" "${STAGE_DIR}/"
[ -f "/root/crossed-cosmos/eci.bib" ] && cp "/root/crossed-cosmos/eci.bib" "${STAGE_DIR}/"

cat > "${STAGE_DIR}/README.txt" << 'README'
P2 — Modular flow / Araki-cocycle LMP letter (10pp)
Author: Kévin Remondière, Independent researcher, Tarbes, France
Target: Letters in Mathematical Physics (Springer)
arXiv categories: hep-th (primary), math-ph, math.OA (cross-list)
Compile: pdflatex erepr_araki_consistency_LMP && bibtex ... && pdflatex x2
PENDING fix (M33): strengthen Prop 1 proof with spectral-measure decomposition (1 paragraph)
PENDING verify: Vardian arXiv:2602.02675 live-check before submission
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
