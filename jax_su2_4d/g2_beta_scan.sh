#!/bin/bash
# G_2 β-scan matching Bruno+ 2015 (arXiv:1409.8305)
# β = 7/g², scaling window β > 9.45
# L=4 first (fast), then L=6

cd /root/cc-private/jax_su2_4d

echo "=== G_2 β-SCAN — Bruno+ 2015 calibration ==="
echo "Start: $(date)"

for BETA in 9.6 9.8 10.0 10.2 10.4; do
  for L in 4 6; do
    echo ""
    echo ">>> β=$BETA L=$L — $(date)"
    python3 g2_metropolis_lattice.py \
      --L $L --beta $BETA \
      --n_therm 500 --n_meas 200 --n_skip 5 \
      --epsilon 0.15 2>&1 | grep -E "(RESULTS|⟨P⟩|L⟩|Saved)"
  done
done

echo ""
echo "=== SCAN COMPLETE — $(date) ==="
