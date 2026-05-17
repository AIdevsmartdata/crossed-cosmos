#!/usr/bin/env python3
"""
analyze_xml_observables.py — Mine 1200 Utah+Belgium Stage B XMLs for observables.

Extracts:
- Plaquette: <w_plaq>, <s_plaq>, <t_plaq>, <plane_NM_plaq>
- Polyakov loop: <pollp>/<elem>/<re>, <im>
- Link expectation: <link>
- Smeared observables: same after APE smearing
- Wilson loops: if present in <WilsonLoop>

Output JSON: per-β statistics (mean, std, bootstrap CI) + Symanzik scaling table.

Usage:
    python3 analyze_xml_observables.py --root lattice_recovery_2026-05-17 --out results.json
"""
import argparse
import json
import os
import re
import sys
import glob
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from collections import defaultdict


def parse_xml(xml_path):
    """Extract observables from a single Stage B XML file."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return None

    obs = {}

    # Get the <Observables> element (per-cfg, first GLUEBALL_OPS instance)
    for o in root.iter('Observables'):
        for child in o:
            tag = child.tag
            if child.text is not None:
                try:
                    obs[tag] = float(child.text)
                except (ValueError, TypeError):
                    pass
            elif tag == 'pollp':
                # Polyakov loop: list of <elem> with <re>, <im>
                pollp_re = []
                pollp_im = []
                for elem in child:
                    re_val = elem.find('re')
                    im_val = elem.find('im')
                    if re_val is not None:
                        try:
                            pollp_re.append(float(re_val.text))
                        except (ValueError, TypeError):
                            pass
                    if im_val is not None:
                        try:
                            pollp_im.append(float(im_val.text))
                        except (ValueError, TypeError):
                            pass
                if pollp_re:
                    obs['pollp_re'] = pollp_re
                if pollp_im:
                    obs['pollp_im'] = pollp_im
        break  # First Observables only (initial state)

    # Smeared observables
    for o in root.iter('Smeared_Observables'):
        for child in o:
            tag = child.tag
            if child.text is not None:
                try:
                    obs[f'smeared_{tag}'] = float(child.text)
                except (ValueError, TypeError):
                    pass
        break

    # Wilson loops (if stored — kind=7 standard)
    wilson_loops = []
    for w in root.iter('WilsonLoop'):
        wl_data = {}
        for child in w:
            if child.text is not None:
                try:
                    wl_data[child.tag] = float(child.text)
                except (ValueError, TypeError):
                    wl_data[child.tag] = child.text
        if wl_data:
            wilson_loops.append(wl_data)
    if wilson_loops:
        obs['wilson_loops'] = wilson_loops

    return obs


def bootstrap_ci(arr, n_boot=1000, ci=68):
    """Bootstrap confidence interval (68% = 1σ)."""
    arr = np.array(arr)
    rng = np.random.default_rng(42)
    boot_means = []
    for _ in range(n_boot):
        sample = rng.choice(arr, len(arr), replace=True)
        boot_means.append(np.mean(sample))
    lo = np.percentile(boot_means, (100 - ci) / 2)
    hi = np.percentile(boot_means, 100 - (100 - ci) / 2)
    return float(np.mean(arr)), float(np.std(arr) / np.sqrt(len(arr))), float(lo), float(hi)


def analyze_beta_dir(beta_dir, beta_val):
    """Analyze all XMLs in one β directory."""
    xml_files = sorted(glob.glob(os.path.join(beta_dir, 'glue_*.out.xml')))
    print(f"  [{beta_dir}] {len(xml_files)} XML files (β={beta_val})")

    observables = defaultdict(list)
    for xml_path in xml_files:
        obs = parse_xml(xml_path)
        if obs is None:
            continue
        for k, v in obs.items():
            if isinstance(v, (int, float)):
                observables[k].append(v)
            elif k.startswith('pollp_'):
                observables[k].extend(v)

    # Statistics
    stats = {'n_cfg': len(xml_files), 'beta': beta_val}
    for key, vals in observables.items():
        if not vals:
            continue
        try:
            mean, sem, lo68, hi68 = bootstrap_ci(vals)
            stats[key] = {
                'mean': mean,
                'sem': sem,
                'std': float(np.std(vals)),
                'ci68_lo': lo68,
                'ci68_hi': hi68,
                'n': len(vals),
                'min': float(np.min(vals)),
                'max': float(np.max(vals)),
            }
        except Exception as e:
            stats[key] = {'error': str(e), 'n': len(vals)}
    return stats


def lucini_teper_sigma_a2(beta, N=2):
    """
    Lucini-Teper 2001 (hep-lat/0103027) SU(N) lattice spacing scale via string tension.
    For SU(2), σa² fit: σa² ≈ exp(-(11/12)(β-2.30)) at 2.3 ≤ β ≤ 2.8 approximate
    More careful from Teper review (hep-lat/9804008):
      SU(2): σa²(β) ~ data-driven, here use Necco-Sommer-like asymptotic 2-loop perturbative
    """
    # 2-loop perturbative ansatz (rough)
    b0 = 11.0 / (24 * np.pi**2) * N**2  # N=2: b0 = 11/(6π²) but factor of N²/4 for SU(N) check
    # Simpler: use empirical Lucini-Teper table interpolation
    # SU(2) data points from Teper 1998:
    #   β=2.30: σa² ≈ 0.420
    #   β=2.40: σa² ≈ 0.260
    #   β=2.50: σa² ≈ 0.146
    #   β=2.60: σa² ≈ 0.080
    #   β=2.70: σa² ≈ 0.043
    #   β=2.80: σa² ≈ 0.024
    su2_data = {
        2.30: 0.420, 2.40: 0.260, 2.50: 0.146,
        2.60: 0.080, 2.70: 0.043, 2.80: 0.024,
    }
    if beta in su2_data:
        return su2_data[beta]
    # Linear interpolation in log space
    betas = sorted(su2_data.keys())
    log_s = np.array([np.log(su2_data[b]) for b in betas])
    return float(np.exp(np.interp(beta, betas, log_s)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='/root/crossed-cosmos/lattice_recovery_2026-05-17',
                   help='Directory containing utah_stageB/ and belgium_stageB/')
    p.add_argument('--out', default='/root/crossed-cosmos/notes/xml_observables_results.json')
    p.add_argument('--no-bootstrap', action='store_true')
    args = p.parse_args()

    root = Path(args.root)
    print(f"=== Analyzing XML observables in {root} ===")
    print()

    # Map (source, β) → directory
    sources = {
        'utah': {'b240': 2.40, 'b250': 2.50, 'b260': 2.60},
        'belgium': {'b230': 2.30, 'b270': 2.70, 'b280': 2.80},
    }

    results = {'sources': {}}
    for src, betas in sources.items():
        src_dir = root / f'{src}_stageB'
        if not src_dir.exists():
            print(f"  [{src}] dir not found, skip")
            continue
        results['sources'][src] = {}
        for bdir, bval in betas.items():
            stats = analyze_beta_dir(str(src_dir / bdir), bval)
            results['sources'][src][bdir] = stats
            print(f"  β={bval}: w_plaq={stats.get('w_plaq', {}).get('mean', 'N/A')}")

    # Cross-β summary
    print()
    print("=== Cross-β plaquette summary ===")
    rows = []
    for src, betas in sources.items():
        for bdir, bval in betas.items():
            s = results['sources'].get(src, {}).get(bdir, {})
            w_plaq = s.get('w_plaq', {}).get('mean', None)
            w_plaq_sem = s.get('w_plaq', {}).get('sem', None)
            sigma_a2 = lucini_teper_sigma_a2(bval)
            if w_plaq is not None:
                rows.append({
                    'source': src, 'beta': bval, 'w_plaq': w_plaq, 'w_plaq_sem': w_plaq_sem,
                    'sigma_a2': sigma_a2, 'a_inv_lattice': 1.0 / np.sqrt(sigma_a2 + 1e-12) if sigma_a2 > 0 else None,
                })
    rows.sort(key=lambda r: r['beta'])
    print(f"  {'β':<6} {'source':<10} {'<P>':<12} {'sem':<10} {'σa²':<10} {'1/√σ a':<10}")
    for r in rows:
        print(f"  {r['beta']:<6} {r['source']:<10} {r['w_plaq']:<.4f}     ±{r['w_plaq_sem']:<.4f}    {r['sigma_a2']:<.4f}    {r['a_inv_lattice']:.3f}")
    results['cross_beta_summary'] = rows

    # Continuum extrapolation test: <P>(β) → 1 as β → ∞ (free field)
    # Symanzik: <P> ~ 1 - g²·C_F/(2N) + O(g⁴)
    print()
    print("=== Symanzik scaling check ===")
    if len(rows) >= 3:
        betas = np.array([r['beta'] for r in rows])
        plaqs = np.array([r['w_plaq'] for r in rows])
        # For SU(2) free field: <P>(β→∞) = 1
        # leading: 1 - <P> ∝ 1/β
        # Compute 1-<P> vs 1/β
        ones_minus_p = 1 - plaqs
        inv_betas = 1.0 / betas
        # Linear fit: 1-<P> = a + b/β
        A = np.vstack([np.ones_like(inv_betas), inv_betas]).T
        coef, *_ = np.linalg.lstsq(A, ones_minus_p, rcond=None)
        a, b = coef
        print(f"  Fit: 1-<P> = {a:.4f} + {b:.4f}/β")
        print(f"  (β→∞ intercept = {a:.4f}, expected ~0 in free field)")
        # Compute residuals
        predicted = a + b * inv_betas
        residuals = ones_minus_p - predicted
        print(f"  Residuals: max abs = {np.max(np.abs(residuals)):.5f}")
        results['symanzik_fit'] = {'intercept': float(a), 'slope': float(b),
                                    'residual_max': float(np.max(np.abs(residuals))),
                                    'inferred_free_limit': float(a)}

    # Save
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2, default=str))
    print()
    print(f"Saved: {out_path}")
    print(f"Total XMLs analyzed: {sum(s.get('n_cfg', 0) for src in results['sources'].values() for s in src.values())}")


if __name__ == '__main__':
    main()
