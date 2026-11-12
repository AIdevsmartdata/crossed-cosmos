# Lean Kernel Arena kernels on the exported proof closure (11 November 2026)

Files: scripts `b_nl.sh`, `b_lg.sh` (build), `cal_nl.sh`, `cal_lg.sh` (witnesses), `run_nl.sh`, `run_lg.sh` (full export), `tr.sh`, `ue.sh`
(trace, single declaration), `info.sh`, `garde120.sh` (memory guard; see limit 6); logs in `journaux/`; the 3.6 MB gzip trace is not
included (size and hash in `journaux/TRACE_NON_COPIEE.tsv`). Commits: arena `6c2d82164f1a2b1ac94aee62290fe78a3c3853fb`; nano-lean
`5c8a523de8d021662e024266013cbb693a5885f6` (tag v0.3.3, MIT); logicaffeine `1e6ad5b7c640f8fb1780e7bf141b92a1b5a281c3` (crate
`logicaffeine_kernel`, example `logos_kernel`, MIT). Binary SHA-256: `journaux/INFO_construction.txt`. Binaries were built without the
arena's profile-guided optimisation phase. Input: the export of SHA-256 `f1ff87d70c21f2f2d620d23bb0596a6947cabc3e32ff7ec5725c7a0e7089a06c`
(recomputed on the machine: `journaux/joint.sha256_recalcul`).

Results (return code 0 for both): nano-lean `-j 8 --axioms propext,Classical.choice,Quot.sound`: "187925 attempted, 0 failures, 0 fallbacks",
35 s, 3 890 036 kB (`journaux/full_nl.err`). logos-kernel `--check sem --stats`: "accepted: 180988 declarations, 58605083 records",
6 min 28.6 s, 7 089 736 kB; its own counter prints 187925 declarations (`journaux/full_lg.err`); the difference with 180 988 is not explained here.
`uniformE`: nano-lean trace, "end 182627 elapsed 10.835777ms". Witnesses: see the note, Section 8.2 (`journaux/cal_*`).

Limits: same export file as nanoda (no independence from lean4export or from the compilation); same machine and operator; minimal calibration;
the memory guard of the first runs watched the `time` wrapper process, not the kernel (memory read as 0 GB in `garde_nl.log`), so it
would not have stopped a runaway; actual peak memory stayed at 3.9 GB (nano-lean) and 7.1 GB (logos-kernel).
