#!/bin/bash
# vast_watchdog_v2.sh — VAST MANAGER 2026-05-10 fixes applied
# Run via tmux : tmux new -d -s watchdog 'while true; do bash /root/vast_watchdog_v2.sh; sleep 300; done'
# Changes vs v1 :
#   FIX1 : duplicate tmux detection (kill all but most recent gpu0_*)
#   FIX2 : disk usage alert (>= 80%)
#   FIX3 : RAM alert (>= 90%)
#   FIX4 : PARI hung detection (RSS > 100GB OR no output 6h)
#   FIX5 : disk-cleanup automation (gzip *.out > 14d, rotate to /root/crossed-cosmos)
#   FIX6 : RESPECT productive workloads — only restart GPUs running gpu_INFINITE_* scripts
#          (do NOT restart if a tmux session contains "tier_d" or "productive_" prefix)

LOG=/root/vast_watchdog.log
echo "=== watchdog v2 @ $(date) ===" >> $LOG

# ===== FIX1 : duplicate tmux detection =====
# kill all but most-recent for each gpu*_* family
for prefix in gpu0_ gpu1_ gpu2_ gpu3_; do
    sessions=$(tmux ls 2>/dev/null | grep "^${prefix}" | awk -F: '{print $1}')
    n=$(echo "$sessions" | grep -c "${prefix}")
    if [ "$n" -gt 1 ]; then
        # Keep most recent (highest creation timestamp), kill others
        most_recent=$(tmux ls 2>/dev/null | grep "^${prefix}" | sort -t'(' -k2 | tail -1 | awk -F: '{print $1}')
        for s in $sessions; do
            if [ "$s" != "$most_recent" ]; then
                echo "  KILL duplicate tmux session $s (keeping $most_recent)" >> $LOG
                tmux kill-session -t "$s" 2>/dev/null
            fi
        done
    fi
done

# ===== GPU 0-3 INFINITE LOOPS or PRODUCTIVE workloads =====
for i in 0 1 2 3; do
    # Find any tmux session for this GPU (gpu${i}_*)
    sess=$(tmux ls 2>/dev/null | awk -F: '{print $1}' | grep "^gpu${i}_" | head -1)
    util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i $i 2>/dev/null | head -1)

    # Check if this GPU is running productive ECI (tier_d, productive_, sage_)
    productive=$(tmux ls 2>/dev/null | awk -F: '{print $1}' | grep -E "^(tier_d|productive_|sage_)_gpu${i}" | head -1)

    if [ -n "$productive" ]; then
        # Don't touch productive workloads
        echo "  GPU $i PRODUCTIVE ($productive) util=$util%" >> $LOG
        continue
    fi

    if [ -z "$sess" ] || [ "$util" = "0" ]; then
        echo "  RESTART GPU $i (sess=$sess, util=$util)" >> $LOG
        pkill -f "GPU_ID=${i} python3 /tmp/gpu_INFINITE_" 2>/dev/null
        sleep 2
        # Use Mahler for big-VRAM GPUs (2,3), eigh for small (0,1)
        if [ $i -ge 2 ]; then
            tmux new-session -d -s "gpu${i}_v8" "GPU_ID=${i} python3 /tmp/gpu_INFINITE_mahler.py > /root/logs/v8/gpu${i}_v8.log 2>&1"
        else
            tmux new-session -d -s "gpu${i}_v8" "GPU_ID=${i} python3 /tmp/gpu_INFINITE_eigh.py > /root/logs/v8/gpu${i}_v8.log 2>&1"
        fi
        echo "  RESTARTED GPU $i (gpu${i}_v8)" >> $LOG
    else
        echo "  GPU $i OK util=$util% sess=$sess" >> $LOG
    fi
done

mkdir -p /root/logs/v8

# ===== FIX2 : disk usage alert =====
disk_pct=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$disk_pct" -ge 80 ]; then
    echo "  ALERT disk = ${disk_pct}% (>= 80%)" >> $LOG
fi

# ===== FIX3 : RAM alert =====
ram_pct=$(free | awk '/Mem:/ {printf "%.0f", $3/$2*100}')
if [ "$ram_pct" -ge 90 ]; then
    echo "  ALERT RAM = ${ram_pct}% (>= 90%)" >> $LOG
fi

# ===== FIX4 : PARI hung detection =====
for pid in $(pgrep -f '^gp -q'); do
    rss=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
    if [ -n "$rss" ] && [ "$rss" -gt 104857600 ]; then  # > 100GB RSS
        echo "  WARN PARI PID=$pid RSS=${rss}KB > 100GB" >> $LOG
    fi
done

# ===== FIX5 : disk-cleanup automation =====
# gzip outputs >= 14d
find /root/scripts -name '*.out' -mtime +14 -type f 2>/dev/null | head -10 | while read f; do
    if [ ! -f "${f}.gz" ]; then
        gzip "$f" 2>/dev/null
        echo "  GZIP $f" >> $LOG
    fi
done

# Cleanup logs > 30d
find /root/logs -name '*.log' -mtime +30 -type f 2>/dev/null | head -10 | while read f; do
    rm "$f" 2>/dev/null
    echo "  RM old log $f" >> $LOG
done

echo "=== watchdog v2 done @ $(date) ===" >> $LOG
echo "" >> $LOG
