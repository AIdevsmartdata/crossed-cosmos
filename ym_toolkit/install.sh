#!/bin/bash
# YM Toolkit install — 2026-05-21
# RTX 5060 Ti 16 GB compatible
set -e
echo "=== YM Toolkit installation ==="
pip install --upgrade pip
pip install numpy scipy matplotlib torch numba sympy
pip install pysr            # symbolic regression (will auto-install Julia)
pip install giotto-tda      # persistent homology
pip install ripser          # topology
pip install scikit-learn    # NN classifier
echo "✓ Install OK. Run : python3 0_framework_check.py"
