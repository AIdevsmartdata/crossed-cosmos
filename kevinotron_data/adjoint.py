"""adjoint.py — SINGLE SOURCE OF TRUTH. Auto-normalizing."""
import numpy as np

def adjoint_rep_batch(links_mu, gens, is_complex=None):
    """Ad(U)_{ab} normalized so Ad(I) = I. Works for all groups."""
    d_adj = len(gens)
    n_links = links_mu.shape[0]
    Ad = np.zeros((n_links, d_adj, d_adj))
    
    U = links_mu.astype(np.complex128) if not np.iscomplexobj(links_mu) else links_mu
    Ud = np.conj(np.swapaxes(U, -2, -1))
    gens_c = gens.astype(np.complex128) if not np.iscomplexobj(gens) else gens
    
    # Compute raw Tr(T_a U T_b U†) for all (a,b)
    for a in range(d_adj):
        TaU = np.einsum('ij,njk->nik', gens_c[a], U)
        for b in range(d_adj):
            TbUd = np.einsum('ij,njk->nik', gens_c[b], Ud)
            prod = np.einsum('nij,njk->nik', TaU, TbUd)
            Ad[:, a, b] = np.einsum('nii->n', prod).real
    
    # Normalize: for U=I, Ad_{ab} = Tr(T_a T_b) = c * delta_{ab}
    # We want Ad(I) = I, so divide by c = Tr(T_0 T_0)
    norm = np.trace(gens_c[0] @ gens_c[0]).real
    if abs(norm) > 1e-14:
        Ad /= norm
    
    return Ad


def build_fp_laplacian(config, gens, is_complex=None):
    """Build FP Laplacian using unified adjoint."""
    Ls = config.shape[1]; Lt = config.shape[4]
    d_adj = len(gens); N = Ls**3 * Lt; dim = N * d_adj
    sizes = np.array([Ls, Ls, Ls, Lt])
    M = np.zeros((dim, dim))
    sm = np.zeros((Ls,Ls,Ls,Lt), dtype=int)
    for x0 in range(Ls):
        for x1 in range(Ls):
            for x2 in range(Ls):
                for x3 in range(Lt):
                    sm[x0,x1,x2,x3] = ((x0*Ls+x1)*Ls+x2)*Lt+x3
    for mu in range(4):
        lnk = config[mu].reshape(-1, config.shape[-2], config.shape[-1])
        aAd = adjoint_rep_batch(lnk, gens)
        idx = 0
        for x0 in range(Ls):
            for x1 in range(Ls):
                for x2 in range(Ls):
                    for x3 in range(Lt):
                        i = sm[x0,x1,x2,x3]; ri = i*d_adj
                        M[ri:ri+d_adj, ri:ri+d_adj] += 2.0*np.eye(d_adj)
                        c=[x0,x1,x2,x3]; c[mu]=(c[mu]+1)%sizes[mu]
                        j=sm[tuple(c)]; rj=j*d_adj
                        M[ri:ri+d_adj, rj:rj+d_adj] -= aAd[idx]
                        c2=[x0,x1,x2,x3]; c2[mu]=(c2[mu]-1)%sizes[mu]
                        k=sm[tuple(c2)]; rk=k*d_adj
                        M[ri:ri+d_adj, rk:rk+d_adj] -= aAd[sm[tuple(c2)]].T
                        idx += 1
    return M
