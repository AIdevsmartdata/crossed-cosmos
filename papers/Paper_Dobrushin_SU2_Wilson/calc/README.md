# Calculations cited in the note

| script | log | purpose (section of the note) |
|---|---|---|
| `levin_transfer.py` (SymPy) | `levin_transfer.log` | Levin's criterion (3.49), transferred to the Wilson link: β_W < 2√5/45 (§7) |
| `royer_transfer.py` (SymPy) | `royer_transfer.log` | Royer's constants, transferred: β_W < 1/9 and < 0.12502 (§7) |
| `chiffres_v1.py` (SymPy) | `chiffres_v1.log` | numerical constants quoted in the note (ratios, thresholds) |
| `gross_transfer.py` (mpmath) | `gross_transfer.log` | Gross's Theorem 3 and Lemma 4.1 + Theorem 1, transferred: β_W < 0.0180 and < ln(10/9)/4 (§7) |
| `lp2d.py` (SciPy/HiGHS) | `lp2d_m14.log` | [numerical] linear programs for sup_f Cov(f, ⟨x,v⟩), geodesic and chordal metrics (Remark 13) |
| `check1d.py`, `lp_chordal.py` (SciPy/HiGHS) | `check1d.log`, `lp_chordal.log` | [numerical] one-dimensional cross-checks of the chordal coefficient (Remark 13) |

The linear programs are floating-point evidence only; they are not part of any proof. They were run before the
chordal identity (Theorem 6 of the note) was proved; the certified statement is in `../certificate_chordal/`.
