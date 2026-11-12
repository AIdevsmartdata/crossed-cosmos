# Partial port to Lean 4.35.0 (state when it was stopped)

`SUIVI.tsv`: one line per iteration from 6 to 14 (iteration number, end time of the build (Paris time), number of failed modules at the
start, return code, accumulated project objects, failed modules). Return code 124 = the build was cut by its time limit (from iteration 10).
`ITERATION15.txt`: the build of iteration 15 (not in `SUIVI.tsv`).
The port was stopped by the operator on the evening of 11 November 2026 (cost); the logs record no stop time. The last build, iteration 15
(20:49:35 to 21:39:36 local time), ended on its time limit (code 124): 1 505 project objects out of 9 470, 66 failed modules. No iteration 16 was started.
The record of touched statements (up to iteration 12) has 17 entries; the reports of iterations 13 and 14 state that no statement was touched;
the patch report of iteration 15 records a change in the body of the definition `view`. The patch reports and the record of
touched statements quote lines of the repository under study and of Mathlib; they are not included in this supplement.
