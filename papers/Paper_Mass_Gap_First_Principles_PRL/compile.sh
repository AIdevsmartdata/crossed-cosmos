#!/bin/bash
# Compile script for Paper_Mass_Gap_First_Principles_PRL
# Uses inline thebibliography (no bibtex pass needed).

set -e
cd "$(dirname "$0")"

echo "[compile] First pass…"
pdflatex -interaction=nonstopmode main.tex > /tmp/_compile_log_1.txt 2>&1 || true

echo "[compile] Second pass…"
pdflatex -interaction=nonstopmode main.tex > /tmp/_compile_log_2.txt 2>&1 || true

if [ -f main.pdf ]; then
    echo "[compile] OK — main.pdf produced ($(stat -c%s main.pdf) bytes)"
    pages=$(pdfinfo main.pdf 2>/dev/null | awk '/^Pages:/ {print $2}')
    echo "[compile] Page count: ${pages:-unknown}"
else
    echo "[compile] FAILED — see /tmp/_compile_log_2.txt"
    tail -30 /tmp/_compile_log_2.txt
    exit 1
fi
