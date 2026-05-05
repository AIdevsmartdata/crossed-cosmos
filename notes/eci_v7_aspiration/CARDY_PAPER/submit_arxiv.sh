#!/usr/bin/env bash
# arXiv submission script for Cardy rho=c/12 paper
# Primary: math-ph
# Secondary: hep-th, cond-mat.stat-mech
#
# Run from /root/crossed-cosmos/notes/eci_v7_aspiration/CARDY_PAPER/
#
# Prerequisites:
#   - arXiv account with submission API or web upload
#   - PDF compiled: latexmk -pdf cardy_rho_paper.tex
#   - pdfinfo available (poppler-utils)
#
set -euo pipefail

PAPER_DIR="/root/crossed-cosmos/notes/eci_v7_aspiration/CARDY_PAPER"
TEX_FILE="cardy_rho_paper.tex"
PDF_FILE="cardy_rho_paper.pdf"

echo "=== Step 1: Compile PDF ==="
cd "$PAPER_DIR"
latexmk -pdf -interaction=nonstopmode "$TEX_FILE"

echo "=== Step 2: Check page count ==="
PAGES=$(pdfinfo "$PDF_FILE" | grep "^Pages:" | awk '{print $2}')
echo "Page count: $PAGES"
if [ "$PAGES" -gt 12 ]; then
    echo "WARNING: Page count $PAGES exceeds LMP target of ~10 pages. Consider reducing margins or font."
fi

echo "=== Step 3: Package source for arXiv ==="
# arXiv requires .tex source + any custom .sty files
# Standard packages (amsmath, hyperref, booktabs, geometry, cite) are available on arXiv
SUBMISSION_DIR="${PAPER_DIR}/arxiv_submission"
mkdir -p "$SUBMISSION_DIR"
cp "$TEX_FILE" "$SUBMISSION_DIR/"
# No custom .bbl needed — thebibliography inline
cp "$PDF_FILE" "$SUBMISSION_DIR/" 2>/dev/null || echo "PDF not yet compiled; compile first."

echo "Files in submission package:"
ls -lh "$SUBMISSION_DIR/"

echo ""
echo "=== Step 4: arXiv metadata ==="
cat <<'METADATA'
Title: Universal Analog-Hawking Saturation Ratio rho = c/12
       for Unitary Diagonal Minimal-Invariant-Partition CFTs

Authors: [Author]

Categories:
  Primary:   math-ph  (Mathematical Physics)
  Secondary: hep-th   (High Energy Physics -- Theory)
             cond-mat.stat-mech (Statistical Mechanics)

Abstract (copy from \begin{abstract}...\end{abstract} in TeX):
  We prove that the analog-Hawking saturation ratio
  rho := (2pi)^{-2} int_0^infty S_BW(u) du
  equals c/12 for every unitary 2D CFT carrying a diagonal (A-series)
  modular-invariant partition function with central charge c > 0...
  [use full abstract from TeX]

License: arXiv standard (CC BY 4.0 recommended)

Comments: 10 pages, 4 tables. Submitted to Letters in Mathematical Physics.
METADATA

echo ""
echo "=== Step 5: Upload ==="
echo "Go to https://arxiv.org/submit and upload the files from $SUBMISSION_DIR/"
echo "Or use the arXiv API if you have credentials configured."
echo ""
echo "Submission checklist:"
echo "  [ ] PDF compiled clean (no undefined references)"
echo "  [ ] Page count <= 12"
echo "  [ ] Author name/affiliation filled in (currently [Author])"
echo "  [ ] Polariton rho range [7.0, 8.3]% verified against original data"
echo "  [ ] He-3-B c_eff ~ 3 caveat visible in §7.1"
echo "  [ ] Solnyshkov 2017 phantom removed (replaced with 2011 + 2019 real papers)"
echo "  [ ] D-series PC2 result integrated (§4.4)"
echo "  [ ] Euler-Mercator sign fix applied (§5)"
