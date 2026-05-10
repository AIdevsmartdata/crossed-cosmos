#!/bin/bash
# vast_monitor_continuous_v2.sh — VAST MANAGER 2026-05-10 fix
# Changes : pgrep regex '^gp -q' (FIX2) + tmux duplicate count + RAM%

LOG=/root/vast_monitor_continuous.log

while true; do
    echo "=== monitor v2 cycle @ $(date) ===" >> $LOG

    bash /root/vast_watchdog_v2.sh

    df -h / | tail -1 >> $LOG

    # FIX : pgrep '^gp -q' instead of 'gp ' (no false positives)
    n_pari=$(pgrep -f '^gp -q' | wc -l)
    echo "PARI procs (real, ^gp -q): $n_pari" >> $LOG

    n_tmux=$(tmux ls 2>/dev/null | wc -l)
    echo "tmux sessions: $n_tmux" >> $LOG

    # Detect duplicate gpu* sessions
    n_gpu0=$(tmux ls 2>/dev/null | grep -c '^gpu0_')
    n_gpu1=$(tmux ls 2>/dev/null | grep -c '^gpu1_')
    n_gpu2=$(tmux ls 2>/dev/null | grep -c '^gpu2_')
    n_gpu3=$(tmux ls 2>/dev/null | grep -c '^gpu3_')
    echo "tmux gpu0=$n_gpu0 gpu1=$n_gpu1 gpu2=$n_gpu2 gpu3=$n_gpu3 (>1 = duplicate)" >> $LOG

    # RAM%
    ram_pct=$(free | awk '/Mem:/ {printf "%.0f", $3/$2*100}')
    echo "RAM ${ram_pct}%" >> $LOG

    # Active output files
    n_active=$(find /root/scripts -name "*.out" -newer /tmp/marker -type f 2>/dev/null | wc -l)
    echo "Active output files: $n_active" >> $LOG
    touch /tmp/marker

    echo "" >> $LOG
    sleep 300
done
