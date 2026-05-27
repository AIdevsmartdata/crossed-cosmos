#!/usr/bin/env bash
# Pipeline post-L=16 + batterie : enchaîne automatiquement
#   1. Attend que MK L=16 et batterie finissent (vérifie via JSONs)
#   2. Lance PySR analyse Phase 1
#   3. Lance L=24 + n=100 bootstrap
#   4. Lance PySR analyse Phase 2 (5 points + bootstrap)
#   5. Génère rapport final
#
# Conçu pour tourner toute la nuit en background.

set -e
mkdir -p /tmp/voie1_calcs/results
LOG=/tmp/voie1_calcs/pipeline_post_L16.log
exec > >(tee -a "$LOG") 2>&1

echo "================================================================================"
echo "PIPELINE POST L=16 + BATTERIE — Start: $(date)"
echo "================================================================================"

# === Wait for L=16 done ===
echo ""
echo "[1/5] Attente MK L=16 fini..."
while ! grep -q "verdict\|RESULT L=16" /tmp/mk_L16.log 2>/dev/null; do
    echo "  $(date +%H:%M:%S) — L=16 en cours, attendre 60s..."
    sleep 60
done
echo "  L=16 done $(date)"

# === Wait for batterie done ===
echo ""
echo "[2/5] Attente batterie tests fini..."
while ! grep -q "BATTERIE FINIE\|β dependence" /tmp/mk_battery.log 2>/dev/null; do
    echo "  $(date +%H:%M:%S) — Batterie en cours, attendre 60s..."
    sleep 60
done
echo "  Batterie done $(date)"

# === Phase 1: PySR analyse ===
echo ""
echo "[3/5] PySR analyse Phase 1 (5 points L=4,6,8,12,16)..."
python3 /tmp/voie1_calcs/pysr_delta_L_analysis.py 2>&1 | tee /tmp/voie1_calcs/pysr_phase1.log

# === Phase 2: L=24 + n=100 ===
echo ""
echo "[4/5] Phase 2 raffinement — L=24 + n=100 bootstrap..."
python3 /tmp/voie1_calcs/mk_L24_n100.py 2>&1 | tee /tmp/voie1_calcs/mk_L24_n100.log

# === Phase 2 PySR ===
echo ""
echo "[5/5] PySR analyse Phase 2 (avec L=24 + n=100)..."
python3 /tmp/voie1_calcs/pysr_delta_L_analysis.py 2>&1 | tee /tmp/voie1_calcs/pysr_phase2.log

echo ""
echo "================================================================================"
echo "PIPELINE DONE — $(date)"
echo "================================================================================"
echo "Output files :"
ls -la /tmp/voie1_calcs/results/ | tail -10
