# morn39 PDF Compilation Report

**Date** : 2026-05-11
**Source corpus** : `/root/crossed-cosmos/notes/heavy_artillery_2026-05-09/morn39`
**Output directory** : `/root/crossed-cosmos/papers/morn39_compiled`
**Toolchain** : pandoc 3.1.3 + pdflatex (TeX Live 2023)

## Summary : **11/11 PDFs compiled cleanly**

## Compilation table

| Short name | Input file | Input mots | Output pages | Output size | Status | Journal target |
|------------|------------|-----------:|-------------:|------------:|--------|----------------|
| Schutt_MultiD | `Paper_Schutt_MultiD_JNumberTheory_draft.md` | 9515 | 16 | 373 KB | **CLEAN** | J. Number Theory |
| Hodge_fourfolds | `Paper_Hodge_Conjecture_6_fourfolds_Inventiones_draft.md` | 13212 | 23 | 480 KB | **CLEAN** | J. Number Theory (downgraded from Inventiones) |
| E08_Maxwell | `Paper_E08_Maxwell_U1_PRD_v1.md` | 16219 | 35 | 556 KB | **CLEAN** | Phys. Rev. D |
| CCNCG_K3FSM | `Paper_CCNCG_CommMathPhys_draft.md` | 9891 | 21 | 423 KB | **CLEAN** | Comm. Math. Phys. |
| ThmC6_FN | `Paper_Theorem_C6_JNumberTheory_v2_polished.md` | 9481 | 19 | 383 KB | **CLEAN** | J. Number Theory |
| BIZ4_Heegner | `Paper_BIZ4_Heegner_Hecke_JNT_draft.md` | 7077 | 15 | 347 KB | **CLEAN** | J. Number Theory |
| KleinSigma_LMP | `Paper_KleinSigma_K3_OS3_LMP_draft.md` | 9064 | 18 | 337 KB | **CLEAN** | Lett. Math. Phys. |
| ECI_v14_spec | `ECI_v14_spec_2026-05-10.md` | 10448 | 24 | 392 KB | **CLEAN** | spec doc (article) |
| MumfordTate | `Theorem_ECI_MumfordTate_torus_formalized.md` | 6131 | 13 | 413 KB | **CLEAN** | companion note (article) |
| AN2_YagerSchertz | `Opus_AN2_Yager_Schertz_PROVED_RIGOROUS.md` | 7059 | 16 | 329 KB | **CLEAN** | analysis note (article) |
| K3_F_SM | `Opus_K3_F_SM_heatkernel_CORRECTED.md` | 8727 | 20 | 355 KB | **CLEAN** | analysis note (article) |

## Per-paper notes

All 11 papers compiled cleanly via pandoc -> pdflatex pipeline. Each underwent two pdflatex passes to resolve internal references and table of contents.

### Issues encountered and resolved (during pipeline development)

1. **lmodern.sty missing** : initial install of pandoc did not include lmodern font package. Resolved by installing `lmodern` apt package + `mktexlsr` to refresh TeX file database.

2. **Unicode characters in text mode** : ~150 distinct unicode chars (mostly math symbols, Greek, mathfrak, mathbb, arrows, sub/superscript digits, semidirect product, propto, end-of-proof tombstone, etc.) appear in text mode in the markdown sources. pdflatex with utf8 inputenc cannot handle these out of the box. Resolved by injecting `\DeclareUnicodeCharacter{...}{\ensuremath{...}}` directives for each into the preamble (185 char declarations).

3. **Combining diacritics** (U+0300..U+030C, U+0338) : combining marks that follow a base letter in the markdown (e.g. `π̄` = pi + combining macron). These cannot be displayed by pdflatex in text mode and would be displayed as `\={}` (empty macron). Resolved by stripping combining marks in markdown preprocessing (the base letter retains its meaning).

4. **Unicode minus sign U+2212** : pandoc emits this verbatim and it fails utf8 inputenc. Resolved by replacing with hyphen-minus in preprocessing.

5. **Emojis** (U+1F389 etc.) : in `ECI_v14_spec_2026-05-10.md`. Resolved by stripping emoji ranges in preprocessing.

6. **Greek letter with macron** (e.g. `ᾱ` U+1FB1) : pandoc cannot decompose to base letter + accent. Resolved by mapping to base Greek letter (loses macron decoration but preserves text).

7. **Display math `\[ ... \]`** : pandoc default markdown does not recognize `\[ ... \]` as display math (only `$$ ... $$`). Resolved by enabling pandoc extension `+tex_math_single_backslash` (in addition to `+tex_math_dollars`).

8. **Inline math `$X - $`** (trailing space before closing dollar) : violates pandoc's `tex_math_dollars` rule (math must abut the dollars without internal whitespace). Pandoc would then escape the dollar signs as literal `\$`, breaking the rendered LaTeX. Resolved by a regex preprocessor that strips leading/trailing whitespace inside single-line `$ ... $` math spans (skipping multi-line `$$ ... $$` display blocks and fenced code blocks to avoid breaking legitimate content).

9. **Custom LaTeX commands** : `\slashed`, `\Tr`, `\Sym`, `\Spec`, `\Hom`, `\End`, `\Aut`, `\Gal`, `\Pic`, `\NS`, `\rank`, `\disc`, `\sgn`, `\Lie` etc. injected as `\providecommand` into preamble (does not redefine any existing LaTeX command).

10. **`pdftotext` decode of pdflatex log** : pdflatex output occasionally contains latin1 bytes mid-stream. Resolved by reading subprocess output as bytes then decoding with `errors="replace"`.

## Generated PDF table of contents

- `/root/crossed-cosmos/papers/morn39_compiled/Schutt_MultiD/main.pdf` (16 pp, 373 KB) -- J. Number Theory
- `/root/crossed-cosmos/papers/morn39_compiled/Hodge_fourfolds/main.pdf` (23 pp, 480 KB) -- J. Number Theory (downgraded from Inventiones)
- `/root/crossed-cosmos/papers/morn39_compiled/E08_Maxwell/main.pdf` (35 pp, 556 KB) -- Phys. Rev. D
- `/root/crossed-cosmos/papers/morn39_compiled/CCNCG_K3FSM/main.pdf` (21 pp, 423 KB) -- Comm. Math. Phys.
- `/root/crossed-cosmos/papers/morn39_compiled/ThmC6_FN/main.pdf` (19 pp, 383 KB) -- J. Number Theory
- `/root/crossed-cosmos/papers/morn39_compiled/BIZ4_Heegner/main.pdf` (15 pp, 347 KB) -- J. Number Theory
- `/root/crossed-cosmos/papers/morn39_compiled/KleinSigma_LMP/main.pdf` (18 pp, 337 KB) -- Lett. Math. Phys.
- `/root/crossed-cosmos/papers/morn39_compiled/ECI_v14_spec/main.pdf` (24 pp, 392 KB) -- spec doc (article)
- `/root/crossed-cosmos/papers/morn39_compiled/MumfordTate/main.pdf` (13 pp, 413 KB) -- companion note (article)
- `/root/crossed-cosmos/papers/morn39_compiled/AN2_YagerSchertz/main.pdf` (16 pp, 329 KB) -- analysis note (article)
- `/root/crossed-cosmos/papers/morn39_compiled/K3_F_SM/main.pdf` (20 pp, 355 KB) -- analysis note (article)

## Pipeline source

Script : `/tmp/compile_papers.py` (Python 3.12 + pandoc 3.1.3 + pdflatex)
Working directory : `/root/crossed-cosmos/papers/morn39_compiled/`
Per-paper artifacts : `<sub>/source.md` (preprocessed markdown), `<sub>/main.tex` (pandoc output + patches), `<sub>/main.pdf` (final), `<sub>/main.log` (pdflatex log), `<sub>/pandoc.log` (pandoc stderr).
