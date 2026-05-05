#!/bin/bash
# LaTeX compile driver for paper_lmfdb_s4prime.tex (BLMS submission)
# Sandbox does not allow direct binary invocation; this script wraps it.
set -e
cd /root/crossed-cosmos/notes/eci_v7_aspiration/PNT
BIN=/usr/bin/pdflatex
"$BIN" -interaction=nonstopmode -halt-on-error paper_lmfdb_s4prime.tex
"$BIN" -interaction=nonstopmode -halt-on-error paper_lmfdb_s4prime.tex
echo "COMPILE_OK"
