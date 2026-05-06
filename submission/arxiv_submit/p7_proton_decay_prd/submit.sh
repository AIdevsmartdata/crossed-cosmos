#!/usr/bin/env bash
# submit.sh — P7: Proton-decay PRD arXiv package builder
# WARNING: DO NOT submit until abstract + §6 B-ratio / fine-tuning disclosure is done (M33).
set -euo pipefail

PAPER_ID="p7_proton_decay_prd"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/OPUS_G112B_M6"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="
echo "IMPORTANT: Verify B-ratio range [0.98,5.54] and fine-tuning disclosure in abstract+§6 BEFORE submitting."

if [ ! -f "${SRC_DIR}/proton_decay_prediction_PRD.pdf" ]; then
    echo "WARNING: PDF not found — run pdflatex x3 in ${SRC_DIR}"
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
cp "${SRC_DIR}/proton_decay_prediction_PRD.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/proton_decay_prediction_PRDNotes.bib" ] && cp "${SRC_DIR}/proton_decay_prediction_PRDNotes.bib" "${STAGE_DIR}/"
# include bayesian scan script as supplemental
[ -f "${SRC_DIR}/m6_bayesian_scan.py" ] && cp "${SRC_DIR}/m6_bayesian_scan.py" "${STAGE_DIR}/" || true
[ -f "${SRC_DIR}/verdict.json" ] && cp "${SRC_DIR}/verdict.json" "${STAGE_DIR}/" || true

cat > "${STAGE_DIR}/README.txt" << 'README'
P7 — Proton-decay B-ratio from modular S'_4 SU(5) at tau=i (4pp)
Author: Kévin Remondière (K. Remondiere), Independent researcher, Tarbes, France
Email: kevin.remondiere@gmail.com
Target: Physical Review D Letters (PRD)
arXiv categories: hep-ph (primary), hep-th
Compile: pdflatex proton_decay_prediction_PRD && bibtex ... && pdflatex x2
MANDATORY BEFORE SUBMISSION (M33):
  1. Revise abstract to include B-ratio range [0.98,5.54]
  2. Add §6 paragraph disclosing Y_5-Y_{45} fine-tuning (1/4000 at M_{T45})
  3. Confirm Domingo DUNE arXiv:2603.18502 live-verified
  4. Confirm dMVP26 arXiv:2604.01422 live-verified
Affiliation: NOTE — tex file says "Hostinger VPS"; change to "Tarbes, France"
README

if [ "${1:-}" != "--dry-run" ]; then
    tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
    echo "Archive created: ${ARCHIVE}"
else
    echo "[DRY RUN] Would create: ${ARCHIVE}"
    ls -la "${STAGE_DIR}/"
fi

echo "=== Done ==="
