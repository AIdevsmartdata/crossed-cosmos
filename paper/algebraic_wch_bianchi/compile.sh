#!/bin/bash
set -e
cd /root/crossed-cosmos/paper/algebraic_wch_bianchi
pdflatex -interaction=nonstopmode note.tex
bibtex note
pdflatex -interaction=nonstopmode note.tex
pdflatex -interaction=nonstopmode note.tex
echo "===== COMPILE COMPLETE ====="
ls -la note.pdf
echo "===== UNDEFINED REFS / CITES ====="
grep -E "Warning.*(undefined|undef|multipl)" note.log || echo "0 warnings"
echo "===== PAGE COUNT ====="
grep -oE "Output written.*\([0-9]+ page" note.log | tail -1
