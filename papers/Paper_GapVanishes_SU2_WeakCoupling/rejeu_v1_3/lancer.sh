#!/bin/bash
# Relance (dans un bac a sable sans droits ni reseau) : programmes autonomes seulement ; sortie standard = sortie.
# NB : programmes_opus_stokes/fragments_non_autonomes/ (stokes_lib.py, drv_*.py) ne sont PAS autonomes : voir README.md.
mkdir -p sorties_relance
for f in programmes_opus_stokes/run?.py programmes_opus_calculs/*.py ma_stokes/ma_L2.py comptabilite/comptabilite_ma.py comptabilite/w_symbols_ma.py; do
  python3 -I $f > sorties_relance/$(basename $f .py).txt
done
