#!/usr/bin/env python3
"""Compare les bornes exportees par CH (Donnees.lean, rationnels) aux encadrements BILATERES de V-CH.
Coherence exigee : lb_CH <= ub_VCH (sinon CH a sur-minore Nt/Z^2), J_lo_VCH <= h_CH (sinon CH a sous-majore J)."""
import json, sys
from fractions import Fraction as F
sel = json.load(open(sys.argv[1])); res = json.load(open(sys.argv[2]))['res']
bad = 0
for r, v in zip(sel, res):
    k0, k1, lb, h0, h1, i = F(r[0]), F(r[1]), F(r[2]), F(r[3]), F(r[4]), r[5]
    assert F(v['k0']) == k0 and F(v['k1']) == k1
    c1 = float(lb) <= v['ub']; c2 = v['J0_lo'] <= float(h0); c3 = v['J1_lo'] <= float(h1)
    bad += not (c1 and c2 and c3)
    print(f"boite CH #{i:3d} [{k0},{k1}] lb_CH={float(lb):.6e} in [lb_V={v['lb']:.6e}, ub_V={v['ub']:.6e}]:{c1}  "
          f"h0_CH={float(h0):.5e} (J0 in [{v['J0_lo']:.5e},{v['J0_hi']:.5e}]):{c2}  h1_CH={float(h1):.5e} (J1 in [{v['J1_lo']:.5e},{v['J1_hi']:.5e}]):{c3}  "
          f"marge_CH={float(lb-max(h0,h1)):.4e} marge_V={v['marge']:.4e} V:{'OK' if v['ok'] else 'ECHEC'}")
print(f"BILAN comparaison : {len(sel)} boites, incoherences = {bad}, V-CH OK = {sum(v['ok'] for v in res)}/{len(res)}")
sys.exit(1 if bad else 0)
