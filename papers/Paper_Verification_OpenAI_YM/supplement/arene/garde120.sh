#!/bin/bash
# Garde mémoire : arrête CE processus (PID donné), et lui seul, si sa mémoire résidente dépasse 120 Go ou si MemAvailable < 25 Go.
set -u
P=$1; J=${2:-/work/arene/journaux/garde_memoire.log}
echo "$(date -u '+%F %T') UTC garde armée sur le PID $P" >> $J
while kill -0 $P 2>/dev/null; do
  A=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  R=$(awk '/VmRSS/{print int($2/1048576)}' /proc/$P/status 2>/dev/null)
  if [ "${A:-999}" -lt 25 ] || [ "${R:-0}" -gt 120 ]; then
    echo "$(date -u '+%F %T') UTC ARRET PID $P : disponible=${A} Go, rss=${R} Go" >> $J
    kill $P; sleep 5; kill -0 $P 2>/dev/null && kill -9 $P
    break
  fi
  echo "$(date -u '+%F %T') UTC disponible=${A} Go rss=${R} Go" >> $J
  sleep 30
done
echo "$(date -u '+%F %T') UTC garde terminée" >> $J
