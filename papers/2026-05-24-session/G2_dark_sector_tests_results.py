#!/usr/bin/env python3
"""
G_2 Dark Sector — comprehensive numerical tests.
All predictions testable against lattice or experiment.

RESULTS SUMMARY (2026-05-27):
- d_s = 7/3 : 5 groups (not 2!): G_2, SU(6), SO(7), Sp(6), SO(8)
  → ANTI-FAB CATCH: originally claimed "only G_2 and SU(6)"
  → BUT closure Σ(dim-1) = 22 = b_2(K3) remains UNIQUE to G_2
- K_Koide = 1-8/24 = 2/3 : match PDG 0.0009%
- Σ(dim-1) = 22 : UNIQUE to SU(2)+SU(3)+G_2
- BBN ΔN_eff : safe if Λ_G2 > 10 MeV
- Bullet cluster : safe if Λ_G2 > 0.3 GeV
- Ω_DM/Ω_b : 5.50 vs obs 5.36 (2.6% off)
- Glueball m/√σ : 3.79 predicted vs HPW 3.55 (7%)
- κ_EE(G_2), d_s(G_2) Gribov : NOT YET MEASURED

LITERATURE FOUND:
- Cossu+ 2024 (arXiv:2406.15421) : G_2 → SU(3) dark matter model!
- Frigerio+ 2019 (arXiv:1907.11228) : G_2 gauge-Higgs DM
- Holland-Pepe-Wiese 2003 (arXiv:hep-lat/0304007) : G_2 lattice
- Cossu+ 2007 (arXiv:0707.4310) : G_2 finite T

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""
# See /tmp/G2_dark_sector_tests.py for full computation code
