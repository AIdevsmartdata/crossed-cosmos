#!/bin/bash
# Garde mémoire du rejeu nanoda OFFICIEL (PID donné en argument ; processus du pilote, lancé par pilote2.sh).
# Arrête CE processus, et lui seul, si la mémoire disponible de la machine passe sous 30 Go ou si sa mémoire dépasse 150 Go,
# pour protéger les autres travaux (production kvu, compilations Lean). Consigne dans /work/diag_nanoda/garde_memoire.log.
set -u
P=$1; J=/work/diag_nanoda/garde_memoire.log
echo "$(date '+%F %T') garde armée sur le PID $P" >> $J
while kill -0 $P 2>/dev/null; do
  A=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  R=$(awk '/VmRSS/{print int($2/1048576)}' /proc/$P/status 2>/dev/null)
  if [ "${A:-999}" -lt 30 ] || [ "${R:-0}" -gt 150 ]; then
    echo "$(date '+%F %T') ARRÊT du rejeu nanoda officiel (PID $P) : disponible=${A} Go, nanoda=${R} Go" >> $J
    kill $P; sleep 5; kill -0 $P 2>/dev/null && kill -9 $P
    break
  fi
  echo "$(date '+%F %T') disponible=${A} Go nanoda=${R} Go" >> $J
  sleep 120
done
echo "$(date '+%F %T') garde terminée (processus absent)" >> $J
