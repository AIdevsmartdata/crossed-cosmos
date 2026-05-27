"""
fp_spectral.py — CANONICAL FP spectral analysis.
Uses adjoint.py (unified, tested). No other adjoint code path.
Usage: python3 fp_spectral.py --config config_g2_L4_beta10.0.npy --group g2
"""
import os, sys, argparse
os.environ['JAX_ENABLE_X64'] = '1'
import numpy as np
import jax, jax.numpy as jnp
from time import time
from adjoint import adjoint_rep_batch, build_fp_laplacian

# Generator builders (kept here for convenience)
def _build_gens(group):
    # Import from fp_adjoint_fast.py for G2/SU(N) builders
    exec(open(os.path.join(os.path.dirname(__file__), 'fp_adjoint_fast.py')).read().split('configs = [')[0], globals())
    s = 1.0/np.sqrt(2.0)
    if group == 'g2':
        return build_g2_generators(), False
    elif group.startswith('su'):
        N = int(group[2:])
        return build_sun_generators(N), True
    elif group == 'sp4':
        return build_sun_generators(4), True
    elif group == 'so7':
        gens = []
        for i in range(7):
            for j in range(i+1, 7):
                g = np.zeros((7,7)); g[i,j]=s; g[j,i]=-s
                gens.append(g)
        return np.array(gens), False
    elif group == 'f4':
        return np.load(os.path.join(os.path.dirname(__file__), 'f4_generators_26x26.npy')), False
    else:
        raise ValueError(f'Unknown group: {group}')

def analyze_spectrum(evals):
    n_neg = int(np.sum(evals < -1e-6))
    pos = evals[evals > 1e-6]
    gap = float(pos[0]) if len(pos) > 0 else 0.0
    # Spectral dimension
    ds_mid = 0.0
    if len(pos) > 10:
        tv = np.logspace(-2, 2, 50)
        lP = np.array([np.log(np.sum(np.exp(-t*pos))) for t in tv])
        ds = -2*np.gradient(lP, np.log(tv))
        ds_mid = float(np.mean(ds[15:30]))
    return {'n_neg': n_neg, 'gap': gap, 'ds_mid': ds_mid,
            'lam_min': float(evals[0]), 'lam_max': float(evals[-1]),
            'dim': len(evals)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--group', required=True)
    parser.add_argument('--cpu', action='store_true', help='Force CPU diag')
    args = parser.parse_args()

    gens, is_complex = _build_gens(args.group)
    data = np.load(args.config)
    dim = data.shape[1]**3 * data.shape[4] * len(gens)
    mem_gb = dim**2 * 8 / 1e9

    print(f'{args.group.upper()} FP: {dim}x{dim} ({mem_gb:.2f} GB)', flush=True)

    t0 = time()
    M = build_fp_laplacian(data, gens)
    print(f'Build: {time()-t0:.1f}s, |M-M^T|={np.max(np.abs(M-M.T)):.2e}', flush=True)

    if args.cpu or mem_gb > 12:
        print('CPU eigvalsh...', flush=True)
        from scipy.linalg import eigvalsh
        evals = eigvalsh(M)
    else:
        print('GPU eigvalsh...', flush=True)
        evals = np.sort(np.array(jnp.linalg.eigvalsh(jnp.array(M))))

    r = analyze_spectrum(evals)
    print(f'n_neg={r["n_neg"]}, gap={r["gap"]:.6f}, ds={r["ds_mid"]:.3f}, '
          f'range=[{r["lam_min"]:.3f},{r["lam_max"]:.3f}]', flush=True)

    import json
    out = args.config.replace('.npy', '_fp.json')
    with open(out, 'w') as f:
        json.dump(r, f, indent=2)
    print(f'Saved to {out}', flush=True)
