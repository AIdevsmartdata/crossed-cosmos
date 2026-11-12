# lean4lean, pass over all modules (11 November 2026, UTC)
- `modules.txt`: the 9470 module names; `FIN2`: "total=9463 ok=9463 attendus=9470 reportes=7".
- `rc_par_module.tsv`: for each of the 9463 completed modules: name, return code (all 0), duration in seconds (sum 153 446 s).
- `lourds.txt`, `lourds_auto.txt`: the seven modules postponed (five stopped by the operator, code 143; `YM.RG08.Clef.Bravo` killed, code 137, cause not recorded; `YM.Work.F05` terminated, code 143, by the memory guard of the restarted pass).
- `reportes/`: return code and duration (`*.rc`: "code seconds") and the (empty) logs of the postponed modules from the first pass.
- `worker.sh`, `lancer.sh`, `bilan.sh`, `pilote.log`, `suivi.log`: scripts and progress records.
- Reruns of the seven modules, one at a time on a second rented machine (nominal 55 GB, timeout 3 hours each): see `../relances/` (state read on 12 November 2026 at 05:20 CET: F05 and Clef.Bravo code 0; Valse.Pellets stopped by the timeout, code 124; Typeface.Press running; Typeface.Cards, Solos.Hues and Flues.Hearth not started).
