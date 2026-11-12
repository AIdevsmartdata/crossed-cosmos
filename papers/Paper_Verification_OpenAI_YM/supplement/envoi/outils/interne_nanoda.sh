#!/bin/bash
# Rejeu par le noyau indépendant nanoda (Rust, num-bigint, sans runtime Lean ni GMP), DANS le bac (leanext, réseau coupé),
# cwd = /work/export.
# usage : interne_nanoda.sh NOM THREADS [DECL_A_IMPRIMER...]   lit /work/export/NOM.ndjson
# Axiomes permis : les trois standard SEULEMENT ; tout autre axiome présent dans le fichier = erreur fatale.
set -u
E=/work/export; L=$E/logs; NOM=$1; THR=$2; shift 2
PP=$(printf '"%s",' "$@"); PP="[${PP%,}]"; [ $# -eq 0 ] && PP="[]"
cat > $E/nanoda_$NOM.json <<JSON
{ "export_file_path": "$E/$NOM.ndjson", "use_stdin": false,
  "num_threads": $THR, "stack_size_bytes": 536870912,
  "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true, "string_extension": true,
  "pp_declars": $PP, "pp_options": { "proofs": false, "width": 120 },
  "print_axioms": true, "pp_to_stdout": false, "pp_output_path": "$L/nanoda_pp_$NOM.txt",
  "print_success_message": true }
JSON
: > $L/nanoda_pp_$NOM.txt
date '+%F %T' > $L/nanoda_$NOM.debut
/usr/bin/time -v -o $L/nanoda_$NOM.time /work/outils/bin/nanoda_bin $E/nanoda_$NOM.json > $L/nanoda_$NOM.log 2>&1
echo "RC=$?" > $L/nanoda_$NOM.rc
date '+%F %T' > $L/nanoda_$NOM.fin
