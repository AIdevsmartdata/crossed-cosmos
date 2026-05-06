#!/usr/bin/env bash
# submit.sh — P4: Cardy LMP paper arXiv package builder
set -euo pipefail

PAPER_ID="p4_cardy_lmp"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/CARDY_PAPER"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="

if [ ! -f "${SRC_DIR}/cardy_rho_paper.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 in ${SRC_DIR}"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/cardy_rho_paper.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/cardy_rho_paper.bib" ] && cp "${SRC_DIR}/cardy_rho_paper.bib" "${STAGE_DIR}/"
[ -f "/root/crossed-cosmos/eci.bib" ] && cp "/root/crossed-cosmos/eci.bib" "${STAGE_DIR}/"
# copy python verification script as supplemental
[ -f "/root/crossed-cosmos/scripts/analysis/cardy_rho_minimal_models.py" ] && \
    cp "/root/crossed-cosmos/scripts/analysis/cardy_rho_minimal_models.py" "${STAGE_DIR}/" || true

cat > "${STAGE_DIR}/README.txt" << 'README'
P4 — Universal analog-Hawking ratio rho=c/12 for diagonal MIP CFTs (11pp)
Author: Kévin Remondière, Independent researcher, Tarbes, France
Target: Letters in Mathematical Physics (Springer) or J. Phys. A: Math. Theor. (IOP)
arXiv categories: cond-mat.stat-mech (primary), hep-th, quant-ph
Compile: pdflatex cardy_rho_paper && bibtex cardy_rho_paper && pdflatex x2
PENDING fix (M33): 2-paragraph Virasoro mode-counting argument for Theorem 2
PENDING check (M33): polariton rho range 1/18 — priority check / verify or remove
PENDING fix (M33): §6 falsifier values consistency (window vs rho_inf per platform)
Supplemental: cardy_rho_minimal_models.py (mpmath dps=50 verification)
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
