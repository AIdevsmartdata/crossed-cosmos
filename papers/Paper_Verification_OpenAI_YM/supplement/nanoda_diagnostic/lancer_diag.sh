#!/bin/bash
# À lancer sous lean. Rejeu de DIAGNOSTIC (binaire instrumenté) du même export, 32 fils, nice 10.
# Garde : arrêt du diagnostic (son propre PID seulement) si sa mémoire dépasse 50 Go ou après 50 minutes.
set -u
D=/work/diag_nanoda; E=/work/export
cd $D || exit 2
cat > diag.json <<JSON
{ "export_file_path": "$E/joint.ndjson", "use_stdin": false,
  "num_threads": 32, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": [], "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$D/diag_pp.txt",
  "print_success_message": true }
JSON
: > diag_pp.txt; : > diag.suivi
date '+%F %T' > diag.debut
nice -n 10 $D/src_copie/target/release/nanoda_bin $D/diag.json > diag.out 2> diag.err &
P=$!
echo $P > diag.pid
for i in $(seq 300); do
  sleep 10
  kill -0 $P 2>/dev/null || break
  R=$(awk '/VmRSS/{print int($2/1048576)}' /proc/$P/status 2>/dev/null)
  echo "$(date +%T) rss=${R}Go debut=$(grep -c '^DEBUT' diag.err) fin=$(grep -c '^FIN' diag.err)" >> diag.suivi
  if [ "${R:-0}" -ge 50 ]; then echo "garde : mémoire ${R} Go, arrêt du diagnostic" >> diag.suivi; kill $P; break; fi
done
kill -0 $P 2>/dev/null && { echo "garde : 50 minutes, arrêt du diagnostic" >> diag.suivi; kill $P; }
wait $P 2>/dev/null; echo "RC=$?" > diag.rc
date '+%F %T' > diag.fin
