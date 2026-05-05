# A75 — Literature table (twistor ↔ modular / Hecke / CM / Q(i))

All entries arXiv-live-verified 2026-05-05. **No bibkey written to `eci.bib`.**

| # | arXiv ID | Year | Authors | Title | Twistor? | Modular? | Q(i) / CM? | LMFDB 4.5.b.a? | ECI-relevance |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **0909.4299** | 2009 | Bao, Kleinschmidt, Nilsson, Persson, Pioline | Instanton Corrections to the Universal Hypermultiplet and Automorphic Forms on SU(2,1) | ✓ contact pot. on Z | ✓ Picard mod. SU(2,1;Z[i]) Eisenstein | ✓ **Z[i] explicit + CM hypothesis** | ✗ | **STRONGEST candidate.** Reunites twistor + Q(i) + CM. Gap = Eisenstein vs cusp eigenform. |
| 2 | 1005.4848 | 2010 | Bao, Kleinschmidt, Nilsson, Persson, Pioline | Rigid Calabi-Yau threefolds, Picard Eisenstein series and instantons | (✓ context) | ✓ PU(2,1;O_d) for general imag. quad. | ✓ generalizes Z[i] to O_d | ✗ | Generalisation of #1; same gap. |
| 3 | 1702.05497 | 2017 | Alexandrov, Banerjee, Manschot, Pioline | Multiple D3-instantons and mock modular forms II | ✓ holomorphic action SL(2,Z) on Z | ✓ vector-valued mock modular | ✗ | ✗ | Modularity générique, pas CM / arith. — WEAK. |
| 4 | 1207.1109 | 2012 | Alexandrov, Manschot, Pioline | D3-instantons, Mock Theta Series and Twistors | ✓ linearized Z + SL(2,Z) | ✓ mock theta cancelling anomalies | ✗ | ✗ | Same lineage as #3 — WEAK. |
| 5 | 1206.1341 | 2012 | Alexandrov, Persson, Pioline | S-duality in Twistor Space | ✓ | ✓ SL(2,Z) family of QK metrics | ✗ | ✗ | WEAK (no arithmetic). |
| 6 | **2403.17045** | 2024 | Donagi, Pantev, Simpson | Twistor Hecke eigensheaves in genus 2 | ✓ Deligne-Hitchin Z | ✓ **Hecke** (géométrique) | ✗ | ✗ | Hecke géom-Langlands, NOT arithmétique. Off-target. |
| 7 | 2110.12300 | 2021 | Simpson | Twistor geometry of parabolic structures rank 2 | ✓ | ✓ Hecke gauge groupoid | ✗ | ✗ | Same lineage — off-target. |
| 8 | 2303.13947 | 2023 | Simpson | Twistor space for local systems on open curve | ✓ | ✓ Hecke groupoid | ✗ | ✗ | Same lineage — off-target. |
| 9 | 1312.3828 | 2014 | Adamo, Casali, Skinner | Ambitwistor strings and scattering equations at one loop | ✓ ambitwistor | ✓ partition fct mod. invariant | ✗ | ✗ | Worldsheet-modularity générique. WEAK. |
| 10 | 2406.09165 | 2024 | Adamo, Bogna, Mason, Sharma | Gluon scattering on the self-dual dyon | ✓ | ✗ | ✗ | ✗ | Off-target. |
| 11 | 2507.18605 | 2025 | Adamo, Bogna, Mason, Sharma | Graviton scattering on self-dual black holes | ✓ | ✗ | ✗ | ✗ | Off-target. |
| 12 | 1503.06983 | 2015 | Hohenegger, Iqbal, Rey | M String, Monopole String and Modular Forms | (Atiyah-Hitchin context) | ✓ Jacobi forms congruence subgroup | ? (subgroup non spécifié dans abs.) | ✗ | WEAK — congruence subgroup pas Q(i)-CM identifié. |
| 13 | 1910.13788 | 2019 | Huybrechts | Complex multiplication in twistor spaces | ✓ Z(K3) | ✗ (no L-fct) | ✓ K3 CM endomorphism field | ✗ | Geometric CM, but K3 not directly ECI. WEAK-MEDIUM. |
| 14 | 2102.07285 | 2021 | Viganò | CM and Noether-Lefschetz Loci of Twistor of K3 | ✓ | ✗ | ✓ CM endomorphism field | ✗ | Same as #13 — geometric, not L-fct. |
| 15 | 0906.2526 | 2010 | Y. Abe | Holonomies in twistor space 2: Hecke algebra | ✓ | (Iwahori-Hecke at gauge level) | ✗ | ✗ | Hecke ALGEBRA (Iwahori), not Hecke OPERATORS on modular forms. WEAK. |

---

## Searches performed (all live arXiv API)

```
1. all:"twistor" AND all:"modular form"          → 15 hits, top 2 retained
2. all:"twistor" AND all:"Hecke"                 → 10 hits, top 4 retained
3. all:"twistor" AND all:"CM newform"            → 0 hits
4. ti:"mock modular" AND ti:"twistor"            → 0 hits
5. all:"twistor" AND all:"LMFDB"                 → 0 hits
6. all:"twistor string" AND all:"modular"        → ~10 hits, decorative
7. all:"ambitwistor" AND all:"modular"           → 7 hits, decorative
8. all:"Atiyah-Hitchin" AND all:"modular"        → 1 candidate (#12)
9. au:Adamo AND au:Mason AND all:"twistor"       → 2 recent (no arith)
10. all:"twistor" AND all:"complex multiplication" → 4 hits, top = #1, #13, #14
11. all:"twistor" AND all:"Eisenstein"           → 2 hits, top = #1
12. all:"Picard modular" AND all:"twistor"       → confirms #1
13. all:"Picard modular" AND all:"Z[i]" AND all:"Eisenstein" → confirms #1, #2
14. au:Pioline AND all:"twistor" AND all:"Picard" → confirms #1
15. au:Alexandrov AND au:Pioline AND all:"twistor" → confirms #3-#5 lineage
```

**Conclusion :** un seul cluster (#1, #2 Bao-Pioline) atteint le seuil MEDIUM
pour l'analogie Q(i) + CM + twistor. Tous les autres sont décoratifs ou hors-cible.
