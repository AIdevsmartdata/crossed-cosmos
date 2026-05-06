#!/usr/bin/env bash
# submit.sh — P3: Modular Shadow LMP v2.5 arXiv package builder
set -euo pipefail

PAPER_ID="p3_modular_shadow_lmp"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/MODULAR_SHADOW"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

# v2.5 tex exists; pdf was compiled for v2
TEX_FILE="modular_shadow_LMP_v2.5.tex"
if [ ! -f "${SRC_DIR}/modular_shadow_LMP_v2.pdf" ]; then
    echo "WARNING: v2 PDF not found. Need to compile v2.5:"
    echo "  cd ${SRC_DIR} && pdflatex modular_shadow_LMP_v2.5 && bibtex modular_shadow_LMP_v2.5 && pdflatex x2"
else
    echo "NOTE: PDF is from v2; v2.5 tex requires fresh compile before arXiv upload"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/${TEX_FILE}" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/modular_shadow_LMP_v2.5.bib" ] && cp "${SRC_DIR}/modular_shadow_LMP_v2.5.bib" "${STAGE_DIR}/"
[ -f "/root/crossed-cosmos/eci.bib" ] && cp "/root/crossed-cosmos/eci.bib" "${STAGE_DIR}/"

cat > "${STAGE_DIR}/README.txt" << 'README'
P3 — Modular Lyapunov bound (type-II_inf crossed-product) LMP article (19pp + App A)
Author: Kévin Remondière, Independent researcher, Tarbes, France
Target: Letters in Mathematical Physics (Springer)
arXiv categories: hep-th (primary), math-ph, math.OA, cond-mat.quant-gas
Compile: pdflatex modular_shadow_LMP_v2.5 && bibtex ... && pdflatex x2
PENDING fix (M33): 1-page Appendix A.2 Step 2 explicit Mellin saddle / moment
PENDING fix (M33): §6 BEC caveat sentence on finite-rank type-II_inf truncation
PENDING verify: 5 future-dated arXiv IDs (Govindarajan-Sadanandan 2604.11277,
                Benjamin-Fitzpatrick-Li-Thaler 2604.01275, etc.) via arXiv API
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
