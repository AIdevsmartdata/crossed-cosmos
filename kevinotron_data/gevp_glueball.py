"""
gevp_glueball.py — Solve GEVP for glueball mass from cross-correlator matrix.

GEVP: C(t) v_n(t,t₀) = λ_n(t,t₀) C(t₀) v_n
m_n(t) = -log(λ_n(t)/λ_n(t-1))

The smallest eigenvalue → ground state mass (0++ glueball).
"""
import numpy as np
import json
import sys

def solve_gevp(corr_matrix, t0=1):
    """Solve GEVP for all timeslices.
    
    Args:
        corr_matrix: shape (n_t, n_ops, n_ops) — C(t) for each t
        t0: reference time (typically 1 or 2)
    
    Returns:
        eigenvalues: shape (n_t, n_ops) sorted descending per t
    """
    n_t = corr_matrix.shape[0]
    n_ops = corr_matrix.shape[1]
    eigenvalues = np.zeros((n_t, n_ops))
    
    C_t0 = corr_matrix[t0]
    # Symmetrize
    C_t0 = 0.5 * (C_t0 + C_t0.T)
    
    # Check C(t0) is positive definite (for stable GEVP)
    eigs_t0 = np.linalg.eigvalsh(C_t0)
    if np.min(eigs_t0) <= 0:
        print(f"WARNING: C(t0={t0}) not positive definite (min eig = {np.min(eigs_t0):.2e})")
        # Add regularization
        C_t0 = C_t0 + 1e-12 * np.eye(n_ops)
    
    # Cholesky for stable generalized eigenvalue
    try:
        L = np.linalg.cholesky(C_t0)
        L_inv = np.linalg.inv(L)
    except np.linalg.LinAlgError:
        print(f"WARNING: Cholesky failed for t0={t0}")
        return eigenvalues
    
    for t in range(n_t):
        C_t = corr_matrix[t]
        C_t = 0.5 * (C_t + C_t.T)
        # Transform: M = L^{-1} C(t) L^{-T}
        M = L_inv @ C_t @ L_inv.T
        M = 0.5 * (M + M.T)
        try:
            eigs = np.linalg.eigvalsh(M)
            # Sort descending (largest = ground state for positive correlator)
            eigenvalues[t] = np.sort(eigs)[::-1]
        except np.linalg.LinAlgError:
            eigenvalues[t] = 0.0
    
    return eigenvalues

def effective_masses(eigenvalues, t0=1):
    """Compute m_n(t) = -log(λ_n(t)/λ_n(t-1)) for each state."""
    n_t, n_ops = eigenvalues.shape
    m_eff = np.zeros((n_t - 1, n_ops))
    for t in range(1, n_t):
        for n in range(n_ops):
            l_curr = eigenvalues[t, n]
            l_prev = eigenvalues[t-1, n]
            if l_curr > 0 and l_prev > 0:
                m_eff[t-1, n] = -np.log(l_curr / l_prev)
            else:
                m_eff[t-1, n] = np.nan
    return m_eff

def analyze(json_file):
    """Load JSON correlator data and extract glueball mass."""
    with open(json_file) as f:
        data = json.load(f)
    
    n_ops = data['n_ops']
    smear = data['smear_levels']
    n_t = data['n_t']
    corr_flat = np.array(data['correlator'])
    corr_matrix = corr_flat.reshape(n_t, n_ops, n_ops)
    
    print(f"GEVP analysis: {n_ops} operators (smear levels {smear}), n_t={n_t}")
    print()
    
    # C(0) matrix
    print("C(0) matrix (should be positive definite):")
    print(corr_matrix[0])
    print(f"  Eigenvalues C(0): {np.linalg.eigvalsh(corr_matrix[0])}")
    print()
    
    # Try different t0 values
    for t0 in [1, 2]:
        if t0 >= n_t:
            continue
        print(f"=== GEVP with t0={t0} ===")
        eigs = solve_gevp(corr_matrix, t0=t0)
        m_eff = effective_masses(eigs, t0=t0)
        
        print(f"Eigenvalues λ_n(t):")
        for t in range(n_t):
            print(f"  t={t}: {eigs[t]}")
        
        print(f"\nEffective masses m_n(t):")
        for t in range(m_eff.shape[0]):
            print(f"  t={t}→{t+1}: {m_eff[t]}")
        
        # Plateau estimate (average over t=2,3 for ground state)
        if m_eff.shape[0] >= 3:
            plateau = np.nanmean(m_eff[1:3, 0])
            print(f"\n  m_0++ × a (ground state, t=2,3 plateau): {plateau:.4f}")
        print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 gevp_glueball.py <correlator.json>")
        sys.exit(1)
    analyze(sys.argv[1])
