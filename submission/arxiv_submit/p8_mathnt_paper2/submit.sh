#!/usr/bin/env bash
# submit.sh — P8: Math.NT paper-2 (Conjecture M13.1) — FUTURE / skeleton only
# DO NOT run until all 11 [TBD: prove] markers are resolved.
set -euo pipefail

PAPER_ID="p8_mathnt_paper2"
SRC_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/M32_M131_FORMAL"
OUT_DIR="/root/crossed-cosmos/submission/arxiv_submit/${PAPER_ID}"
STAGE_DIR="${OUT_DIR}/stage"
ARCHIVE="${OUT_DIR}/${PAPER_ID}_arxiv.tar.gz"

echo "=== ${PAPER_ID} arXiv package builder ==="
echo "STATUS: SKELETON ONLY — 11 [TBD:prove] markers outstanding."
echo "Target completion: 2026 Q3. DO NOT submit until TBD markers resolved."
echo ""
echo "Available skeleton files in ${SRC_DIR}:"
ls "${SRC_DIR}/" 2>/dev/null || echo "  (directory not found)"
echo ""

if [ "${1:-}" != "--force" ]; then
    echo "Pass --force to build archive from skeleton (for archival/internal use only)."
    exit 0
fi

rm -rf "${STAGE_DIR}" && mkdir -p "${STAGE_DIR}"
[ -f "${SRC_DIR}/theorem_statements.tex" ] && cp "${SRC_DIR}/theorem_statements.tex" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/paper2_skeleton.md" ] && cp "${SRC_DIR}/paper2_skeleton.md" "${STAGE_DIR}/"
[ -f "${SRC_DIR}/SUMMARY.md" ] && cp "${SRC_DIR}/SUMMARY.md" "${STAGE_DIR}/M32_SUMMARY.md"

cat > "${STAGE_DIR}/README.txt" << 'README'
P8 — Steinberg-edge obstruction to 2-adic L-functions for 4.5.b.a (22pp planned)
Author: Kévin Remondière, Independent researcher, Tarbes, France
Email: kevin.remondiere@gmail.com
Target: Algebra & Number Theory (MSP)
arXiv category: math.NT
STATUS: SKELETON ONLY — 11 [TBD:prove] markers
UNCONDITIONAL THEOREMS (2): C(i) F1 monotonicity, D(i) pair-sum rationality
CONDITIONAL THEOREM (1): D(ii) Steinberg-edge (modulo local Langlands D10)
CONJECTURES (4): A (existence), B (boundedness), C(ii) (Damerell), D(iii) (uniqueness)
Primary collaborator target: Daniel Kriz (MIT) — see endorser strategy
README

tar -czf "${ARCHIVE}" -C "${STAGE_DIR}" .
echo "Skeleton archive created (internal use only): ${ARCHIVE}"

echo "=== Done ==="
