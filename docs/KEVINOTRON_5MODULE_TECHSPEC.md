# Kevinotron Engine Extension: 5-Module Technical Specification

**Author:** Kevin Remondiere (ORCID 0009-0008-2443-7166)
**Date:** 2026-05-27
**Version:** 1.0
**Hardware target:** i5-14600KF (14c/20t, AVX2, 5.3 GHz) + RTX 5060 Ti 16 GB + 32 GB DDR5

---

## Preamble: Current Architecture Summary

The Kevinotron is a Rust+JAX lattice gauge theory engine structured as follows:

- **Rust binary** (`kevinotron/src/`): Metropolis updates, Wilson action, alpha-integration (BP2008b) for Renyi-2 entanglement entropy, Creutz ratios for string tension. All link variables stored as flat `Vec<f64>` (real groups: `d*d` entries; complex groups: `2*d*d` entries re/im interleaved). The `GaugeGroup` trait provides the polymorphic interface: `identity`, `random_near_id`, `dagger`, `mul`, `trace_re`, `add`, `zero`, `reproject`.
- **JAX Python** (`kevinotron/jax_ds/`): FP spectral analysis via dense `eigvalsh`, covariant Laplacian, spectral dimension from heat kernel. Uses `.npy` configs dumped by Rust.
- **9 gauge groups**: U(1), SU(2-5), G2, Sp(4), SO(7), F4. Groups split into real (G2, SO(7), F4: `d*d` reals, `rmat_*` helpers) and complex (SU(N), Sp(4): `2*d*d` reals, `cmat_*` helpers).
- **Build profile**: LTO, `codegen-units=1`, `target-cpu=native`, rayon for parallel alpha-points.

The `Lattice4D` struct owns all links in a contiguous `Vec<f64>`, indexed by `((x0*Ls + x1)*Ls + x2)*Lt + x3` then `*4 + mu` then `*link_size`. Asymmetric lattices are supported via the `--lt` flag.

---

## MODULE 1: SPARSE FP SPECTRAL (Lanczos)

### 1.1 Motivation

The current FP spectral pipeline (`fp_adjoint_fast.py`) builds a **dense** matrix and calls `jnp.linalg.eigvalsh`. The FP Laplacian dimension is `N_sites * d_adj`. For F4 at L=4: `dim = 256 * 52 = 13312`, dense matrix = 1.42 GB (f64), which barely fits in 16 GB VRAM with workspace. For E6 at L=4: `dim = 256 * 78 = 19968`, dense = 3.19 GB -- tight. At L=6: F4 gives `dim = 1296 * 52 = 67392`, dense = 36.3 GB -- impossible. The FP Laplacian is **extremely sparse**: each row has at most `2*4*d_adj + d_adj = 9*d_adj` nonzeros out of `dim` entries. For F4 at L=4: sparsity = `9*52 / 13312 = 3.5%`. For SU(3) at L=4: `9*8 / 2048 = 3.5%`. Sparsity is universal at ~3.5% for any group at L=4 and drops as L grows.

The Lanczos algorithm finds the k smallest eigenvalues of a symmetric matrix in `O(k * nnz * n_iter)` time with `O(k * dim + nnz)` memory -- orders of magnitude less than dense `O(dim^3)` time and `O(dim^2)` memory.

### 1.2 Architecture

```
kevinotron/jax_ds/sparse_fp.py          # Main module
kevinotron/jax_ds/sparse_fp_test.py     # Validation against dense
kevinotron/jax_ds/vram_budget.py        # VRAM calculator + auto-decision
```

**Public API:**
```python
class SparseFPResult:
    eigenvalues: np.ndarray     # (k,) smallest eigenvalues
    n_neg: int                  # number of negative eigenvalues
    gap: float                  # lambda_{d_adj+1} - lambda_{d_adj}
    d_s: dict                   # spectral dimension UV/mid/IR
    metadata: dict              # timing, convergence, etc.

def sparse_fp_spectrum(
    config: np.ndarray,         # (4, Ls, Ls, Ls, Lt, d, d) link config
    group: str,                 # "su2", "su3", ..., "f4", "e6"
    k: int = 100,               # number of smallest eigenvalues
    sigma: float = 0.0,         # shift-invert target (0.0 for near-zero)
    tol: float = 1e-10,         # convergence tolerance
    max_iter: int = 1000,       # maximum Lanczos iterations
    use_gpu: bool = True,       # attempt GPU via JAX sparse matvec
) -> SparseFPResult:
```

**Integration:** Replaces `build_fp_laplacian_fast` + `eigvalsh` in `fp_adjoint_fast.py`. The dense path is kept as fallback for small matrices (dim < 4096) where dense is faster.

### 1.3 Key Algorithms

**1.3.1 Sparse CSR Construction**

The FP Laplacian is never assembled as a dense matrix. Instead, build a `scipy.sparse.csr_matrix`:

```
FUNCTION build_fp_sparse(config, gens, adj_func, d_adj):
    Ls, Lt = config.shape[1], config.shape[4]
    N_sites = Ls^3 * Lt
    dim = N_sites * d_adj
    
    # Pre-allocate COO arrays
    nnz_estimate = N_sites * (d_adj + 2*4*d_adj^2)  # diagonal + 8 neighbors * d_adj^2
    rows = empty(nnz_estimate, int)
    cols = empty(nnz_estimate, int)
    vals = empty(nnz_estimate, float)
    ptr = 0
    
    # Pre-compute ALL adjoint reps for all 4 directions
    FOR mu in 0..4:
        all_links = config[mu].reshape(-1, d_fund, d_fund)
        all_Ad[mu] = adj_func(all_links, gens)  # (N_sites, d_adj, d_adj)
    
    # Build sparse entries
    FOR each site (x0,x1,x2,x3):
        i = site_index(x0,x1,x2,x3)
        
        # Diagonal block: +8 * I_{d_adj}
        FOR a in 0..d_adj:
            rows[ptr] = i*d_adj + a
            cols[ptr] = i*d_adj + a
            vals[ptr] = 8.0
            ptr += 1
        
        FOR mu in 0..4:
            j = forward_neighbor(x, mu)
            k = backward_neighbor(x, mu)
            Ad = all_Ad[mu][i]
            Ad_back = all_Ad[mu][k]
            
            # Forward: -Ad(U_mu(x))
            FOR a,b in 0..d_adj:
                IF |Ad[a,b]| > 1e-15:
                    rows[ptr] = i*d_adj + a
                    cols[ptr] = j*d_adj + b
                    vals[ptr] = -Ad[a,b]
                    ptr += 1
            
            # Backward: -Ad(U_mu(x-mu))^T
            FOR a,b in 0..d_adj:
                IF |Ad_back[b,a]| > 1e-15:
                    rows[ptr] = i*d_adj + a
                    cols[ptr] = k*d_adj + b
                    vals[ptr] = -Ad_back[b,a]
                    ptr += 1
    
    RETURN csr_matrix((vals[:ptr], (rows[:ptr], cols[:ptr])), shape=(dim, dim))
```

**1.3.2 Implicit Shift-Invert Lanczos**

For finding eigenvalues near `sigma=0`, use `scipy.sparse.linalg.eigsh` with shift-invert mode:

```python
from scipy.sparse.linalg import eigsh, LinearOperator, splu

# Pre-factor M for shift-invert
M_shifted = M_sparse - sigma * sparse.eye(dim)
LU = splu(M_shifted.tocsc())  # O(dim * bandwidth^2)

# Define the operator (M - sigma*I)^{-1}
OPinv = LinearOperator((dim, dim), matvec=lambda x: LU.solve(x))

# Find k eigenvalues nearest to sigma
eigenvalues, eigenvectors = eigsh(
    M_sparse,
    k=k,
    sigma=sigma,
    OPinv=OPinv,
    which='LM',     # largest magnitude of (M-sigma*I)^{-1} = nearest to sigma
    tol=tol,
    maxiter=max_iter,
    return_eigenvectors=True,
)
```

**1.3.3 Stochastic Trace Estimation (Hutchinson) for Spectral Dimension**

When full eigenvalue decomposition is too expensive (dim > 50000), use Hutchinson's estimator for the heat kernel trace:

```
FUNCTION heat_kernel_hutchinson(M_sparse, t, n_samples=50):
    # P(t) = Tr(exp(-t*M)) ~ (1/n_samples) * SUM_i z_i^T exp(-t*M) z_i
    # where z_i are Rademacher random vectors (+1/-1 with equal probability)
    
    traces = []
    FOR i in 1..n_samples:
        z = random_rademacher(dim)
        # Compute exp(-t*M) z via Chebyshev polynomial approximation
        # or via rational approximation (Lanczos-based)
        w = expm_matvec(-t * M_sparse, z)  # scipy.sparse.linalg.expm_multiply
        traces.append(dot(z, w))
    
    RETURN mean(traces), std(traces) / sqrt(n_samples)
```

Use `scipy.sparse.linalg.expm_multiply(A, v)` which computes `exp(A)*v` without forming `exp(A)` explicitly. This uses a scaling-and-squaring method with Pade approximation. Cost: `O(s * nnz)` where `s ~ 20` for typical parameters.

**Spectral dimension** from stochastic heat kernel:

```
d_s(t) = -2 * d(ln P(t)) / d(ln t)
```

Computed via finite differences on a log-spaced grid of `t` values, with `P(t)` estimated by Hutchinson at each `t`.

### 1.4 Data Structures

| Structure | Size | Notes |
|-----------|------|-------|
| CSR matrix | `O(nnz * 12)` bytes | `nnz = N_sites * 9 * d_adj` |
| Lanczos vectors | `k * dim * 8` bytes | Krylov subspace basis |
| LU factorization | `O(dim * bw^2)` bytes | `bw ~ Ls^2 * Lt * d_adj` (sparse bandwidth) |
| Eigenvalues | `k * 8` bytes | Sorted ascending |

**Memory estimates (f64):**

| Group | L | dim | Dense (GB) | Sparse CSR (MB) | Lanczos k=100 (MB) |
|-------|---|-----|-----------|-----------------|-------------------|
| SU(2) | 4 | 768 | 0.005 | 0.4 | 0.6 |
| SU(3) | 4 | 2048 | 0.034 | 1.1 | 1.6 |
| G2 | 4 | 3584 | 0.103 | 4.1 | 2.7 |
| SU(5) | 4 | 6144 | 0.302 | 12.2 | 4.7 |
| F4 | 4 | 13312 | 1.42 | 57.2 | 10.2 |
| E6 | 4 | 19968 | 3.19 | 128.3 | 15.3 |
| F4 | 6 | 67392 | 36.3 | 289.6 | 51.6 |
| E6 | 6 | 101088 | 81.7 | 650.7 | 77.4 |

### 1.5 Performance

**FLOP counts:**
- Sparse CSR construction: `O(N_sites * 4 * d_adj^2 * d_fund)` (adjoint computation dominates)
- One Lanczos iteration: `O(nnz)` = `O(N_sites * 9 * d_adj^2)` for sparse matvec
- Shift-invert solve: `O(dim * bw^2)` for LU, then `O(dim * bw)` per solve
- Total for k eigenvalues: `O(k * n_iter * nnz + dim * bw^2)`, typically `n_iter ~ 3-10k`

**Parallelization strategy:**
- CSR construction: CPU with numpy vectorization (adjoint reps computed in batch per direction)
- `eigsh`: CPU-only (scipy ARPACK). GPU sparse eigensolvers (LOBPCG via JAX) are available but less mature for shift-invert
- LU factorization: CPU via SuperLU (default scipy) or UMFPACK (if scikit-umfpack installed)
- Hutchinson trace: GPU via `jax.scipy.sparse.linalg` for the matvecs

**Estimated runtimes:**

| Group | L | CSR build (s) | eigsh k=100 (s) | Total (s) |
|-------|---|--------------|----------------|-----------|
| SU(3) | 4 | 0.5 | 2 | 3 |
| F4 | 4 | 8 | 30 | 40 |
| E6 | 4 | 15 | 60 | 80 |
| F4 | 6 | 40 | 300 | 350 |
| E6 | 6 | 90 | 600 | 700 |

### 1.6 Validation

1. **Dense cross-check**: For all groups at L=4 where dense fits in memory, compute both dense `eigvalsh` and sparse `eigsh`, verify eigenvalues agree to `|lambda_dense - lambda_sparse| < 1e-8`.
2. **Zero-mode count**: Verify `n_zero = d_adj` for any thermalized config (global gauge invariance).
3. **Symmetry**: Verify `|M - M^T|_max < 1e-12` by checking the CSR structure.
4. **Identity config**: Cold-start config (all links = I) gives `Ad(I) = I`, so FP Laplacian = graph Laplacian with multiplicity `d_adj`. Eigenvalues are `d_adj` copies of the free lattice Laplacian spectrum `lambda_k = 4 * sum_mu sin^2(pi*n_mu/L_mu)`.
5. **Convergence**: Monitor residual `||M*v - lambda*v|| / ||v||` for each eigenpair. Flag if > `10*tol`.
6. **Literature**: SU(2) at L=8, beta=2.4: compare FP gap to Cucchieri-Mendes (arXiv:hep-lat/0508028).

### 1.7 Dependencies

- `scipy>=1.10` (sparse, ARPACK eigsh, expm_multiply)
- `numpy>=1.24`
- Optional: `scikit-umfpack` for faster LU factorization
- Optional: `jax[cuda12]` for GPU-accelerated Hutchinson matvecs

No new Rust crates required.

### 1.8 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| LU factorization OOM for large dim | Blocks shift-invert | Low (L<=8) | Fall back to `which='SM'` without shift-invert; slower but no LU needed |
| ARPACK convergence failure near sigma=0 | No eigenvalues returned | Medium | Increase `maxiter`, try `sigma=0.01` offset, use Thick-Restart Lanczos (pylanczos) |
| Sparse build slow for F4/E6 | Long wall-clock | Medium | Vectorize adjoint computation; use Rust for CSR construction via PyO3 FFI |
| Hutchinson variance too high | Noisy d_s | Low | Increase n_samples to 200; use Hutch++ (arxiv:2010.09649) for 2x speedup |

### 1.9 Timeline

| Task | Person-days |
|------|-------------|
| Sparse CSR builder + tests | 2 |
| eigsh integration + shift-invert | 1 |
| VRAM auto-decision logic | 0.5 |
| Hutchinson heat kernel | 1.5 |
| Dense cross-validation suite | 1 |
| Integration into pipeline | 1 |
| **Total** | **7** |

---

## MODULE 2: HMC (Hybrid Monte Carlo) FOR DYNAMICAL FERMIONS

### 2.1 Motivation

The Kevinotron currently samples pure gauge theory (quenched approximation) via Metropolis. Adding dynamical fermions requires sampling configurations weighted by `det(D[U])`, where `D` is the lattice Dirac operator. HMC achieves this by introducing pseudofermion fields and conjugate momenta, evolving via Hamilton's equations (molecular dynamics), and accepting/rejecting with the Metropolis criterion. This gives exact sampling with `O(V)` scaling (vs `O(V^{4/3})` for pure Metropolis). For G2, the fundamental representation is real, so `det(D)` is real and positive at finite chemical potential mu -- this is the **sign-problem-free** feature that makes G2 a unique testing ground for finite-density QCD.

### 2.2 Architecture

```
kevinotron/src/hmc/mod.rs           # HMC orchestrator
kevinotron/src/hmc/momenta.rs       # Lie algebra momenta sampling + algebra operations
kevinotron/src/hmc/leapfrog.rs      # Leapfrog / Omelyan integrator
kevinotron/src/hmc/wilson_dirac.rs  # Wilson-Dirac operator D_W
kevinotron/src/hmc/force.rs         # Gauge + fermion force computation
kevinotron/src/hmc/cg_solver.rs     # Conjugate gradient for D^dag D
kevinotron/src/hmc/pseudofermion.rs # Pseudofermion field generation + action
kevinotron/jax_ds/hmc_gpu.py        # Optional: GPU-accelerated HMC via JAX
```

**GaugeGroup trait extension** (new methods in `groups/mod.rs`):

```rust
/// Extended GaugeGroup trait for HMC
pub trait GaugeGroupHMC: GaugeGroup {
    /// Number of Lie algebra generators (= dim_adj)
    fn n_generators(&self) -> usize { self.dim_adj() }
    
    /// Get generator T_a as flat matrix (same format as link)
    fn generator(&self, a: usize) -> LinkData;
    
    /// Project Lie-algebra-valued matrix to the algebra:
    ///   pi = sum_a Tr(T_a * M) * T_a (with correct normalization)
    fn project_to_algebra(&self, m: &[f64]) -> Vec<f64>;
    
    /// Compute exp(i * epsilon * pi) * U where pi is a Lie algebra element
    ///   pi given as d_adj coefficients, U as link matrix
    fn exp_ipiu(&self, pi_coeffs: &[f64], epsilon: f64, u: &[f64]) -> LinkData;
    
    /// Compute T_a * U (for force computation)
    fn ta_times_u(&self, a: usize, u: &[f64]) -> LinkData;
}
```

### 2.3 Key Algorithms

**2.3.1 HMC Algorithm (top-level)**

```
FUNCTION hmc_trajectory(lattice, group, params):
    # 1. Sample momenta from Gaussian: pi_a(x,mu) ~ N(0,1)
    pi = sample_gaussian_momenta(lattice, group)
    
    # 2. Generate pseudofermion field: phi = D[U] * eta, eta ~ N(0,1)
    eta = sample_gaussian_vector(dim_fermion)
    phi = D_wilson(lattice, group, kappa) * eta
    
    # 3. Compute initial Hamiltonian
    H_old = kinetic_energy(pi) + gauge_action(lattice) + fermion_action(lattice, phi)
    
    # 4. Molecular dynamics integration (leapfrog)
    lattice_new, pi_new = leapfrog(lattice, pi, phi, group, params)
    
    # 5. Compute final Hamiltonian
    H_new = kinetic_energy(pi_new) + gauge_action(lattice_new) + fermion_action(lattice_new, phi)
    
    # 6. Metropolis accept/reject
    dH = H_new - H_old
    IF dH < 0 OR random() < exp(-dH):
        RETURN lattice_new, ACCEPTED
    ELSE:
        RETURN lattice, REJECTED
```

**2.3.2 Leapfrog Integrator**

Standard leapfrog with Sexton-Weingarten two-timescale integration. The gauge force is cheap; the fermion force requires a CG solve and is expensive. The gauge force is updated `n_inner` times per fermion force update.

```
FUNCTION leapfrog_2ts(lattice, pi, phi, group, dt, n_steps, n_inner):
    # Half-step momenta (fermion force)
    F_ferm = fermion_force(lattice, phi, group)
    pi = pi - (dt/2) * F_ferm
    
    FOR step in 0..n_steps:
        # Inner leapfrog for gauge force
        dt_inner = dt / n_inner
        pi = pi - (dt_inner/2) * gauge_force(lattice, group)
        FOR inner in 0..n_inner-1:
            update_links(lattice, pi, dt_inner, group)
            pi = pi - dt_inner * gauge_force(lattice, group)
        update_links(lattice, pi, dt_inner, group)
        pi = pi - (dt_inner/2) * gauge_force(lattice, group)
        
        # Fermion force (expensive)
        F_ferm = fermion_force(lattice, phi, group)
        IF step < n_steps - 1:
            pi = pi - dt * F_ferm
        ELSE:
            pi = pi - (dt/2) * F_ferm  # half-step at end
    
    RETURN lattice, pi
```

**2.3.3 Link Update**

```
FUNCTION update_links(lattice, pi, dt, group):
    FOR each site x, direction mu:
        U = lattice.get(x, mu)
        pi_coeffs = pi[x, mu]  # d_adj coefficients
        # U_new = exp(i * dt * pi_a * T_a) * U
        U_new = group.exp_ipiu(pi_coeffs, dt, U)
        lattice.set(x, mu, U_new)
```

**2.3.4 Gauge Force**

```
FUNCTION gauge_force(lattice, group):
    # F_a(x,mu) = -(beta / d_fund) * Im Tr(T_a * U(x,mu) * K(x,mu))
    # where K is the staple sum
    
    FOR each site x, direction mu:
        U = lattice.get(x, mu)
        K = lattice.staple_sum(group, x, mu)
        UK = group.mul(U, K)
        
        FOR a in 0..d_adj:
            TaUK = group.ta_times_u(a, UK)
            F[x, mu, a] = -(beta / group.beta_norm()) * group.trace_im(TaUK)
    
    RETURN F
```

**2.3.5 Wilson-Dirac Operator**

The Wilson-Dirac operator on a 4D lattice for gauge group G in the fundamental representation:

```
D_W(x,y)_{alpha,beta}^{i,j} = delta_{xy} * delta_{alphabeta} * delta_{ij}
    - kappa * SUM_{mu=0}^{3} [
        (1 - gamma_mu)_{alpha,beta} * U_mu(x)_{ij} * delta_{y, x+mu}
      + (1 + gamma_mu)_{alpha,beta} * U_mu^dag(y)_{ij} * delta_{y, x-mu}
    ]
```

where `kappa = 1/(2*(m + 4))` is the hopping parameter, `gamma_mu` are the Dirac matrices in the Dirac representation (4x4), and `i,j` are color indices. The full dimension of D_W is `N_sites * 4 * d_fund` (4 Dirac components times fundamental color dimension).

For real groups (G2, SO(7), F4), the fundamental rep is real, so `U_mu^dag = U_mu^T` and the Dirac operator preserves reality properties.

**Gamma matrices** (Euclidean, chiral/Dirac representation):

```
gamma_0 = [[0, 0, 0, i], [0, 0, i, 0], [0, -i, 0, 0], [-i, 0, 0, 0]]
gamma_1 = [[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]]
gamma_2 = [[0, 0, i, 0], [0, 0, 0, -i], [-i, 0, 0, 0], [0, i, 0, 0]]
gamma_3 = [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
```

**Spin projectors** `P_mu^{+-} = (1 -+ gamma_mu) / 2` have rank 2, reducing the Dirac-color structure from `4*d_fund` to `2*d_fund` per hop.

**2.3.6 CG Solver for D^dag D**

The fermion force requires `D^{-1} phi`, computed via CG on the normal equations `(D^dag D) x = D^dag phi`:

```
FUNCTION cg_solve(D, Ddag, phi, tol=1e-12, max_iter=5000):
    b = Ddag * phi
    x = 0
    r = b
    p = r
    rr = dot(r, r)
    
    FOR iter in 1..max_iter:
        Ap = DdagD * p     # = Ddag * (D * p)
        alpha = rr / dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rr_new = dot(r, r)
        IF sqrt(rr_new / dot(b,b)) < tol:
            RETURN x, iter
        beta = rr_new / rr
        p = r + beta * p
        rr = rr_new
    
    RETURN x, max_iter  # did not converge
```

**2.3.7 Fermion Force**

```
FUNCTION fermion_force(lattice, phi, group, kappa):
    # Solve (D^dag D) X = phi to get X = (D^dag D)^{-1} phi
    X = cg_solve(D, Ddag, phi)
    Y = D * X  # Y = D (D^dag D)^{-1} phi
    
    # Force contribution from each link:
    # F_a(x,mu) = -kappa * Re Tr[ T_a * (
    #     (1 - gamma_mu) * Y(x) * X^dag(x+mu)
    #   + (1 + gamma_mu) * X(x+mu) * Y^dag(x)
    # ) * U_mu(x) ]
    # (schematic -- involves spin-color outer products)
    
    FOR each site x, direction mu:
        FOR a in 0..d_adj:
            F[x, mu, a] = fermion_force_component(x, mu, a, X, Y, lattice, group)
    
    RETURN F
```

### 2.4 Data Structures

| Structure | Size | Formula |
|-----------|------|---------|
| Momenta `pi` | `N_links * d_adj * 8` bytes | One Lie algebra vector per link |
| Pseudofermion `phi` | `N_sites * 4 * d_fund * 16` bytes | Complex spinor-color vector |
| CG vectors (x, r, p, Ap) | `4 * N_sites * 4 * d_fund * 16` bytes | 4 CG workspace vectors |
| D_W sparse (implicit) | None (matrix-free) | Applied as stencil operation |

**Memory estimates (f64/c128):**

| Group | L | Momenta (MB) | Fermion vectors (MB) | CG workspace (MB) | Total (MB) |
|-------|---|-------------|---------------------|-------------------|-----------|
| SU(2) | 8 | 3.1 | 4.2 | 16.8 | 24.1 |
| SU(3) | 8 | 8.4 | 6.3 | 25.2 | 39.9 |
| G2 | 8 | 14.7 | 14.7 | 58.7 | 88.1 |
| SU(3) | 16 | 134.2 | 100.7 | 402.7 | 637.6 |

### 2.5 Performance

**FLOP counts per trajectory:**
- Gauge force: `O(N_links * d_fund^3)` per evaluation (staple sum is `6 * 3` matrix multiplies)
- Fermion force: `O(N_CG_iter * 8 * N_sites * d_fund^3)` (one Dslash per CG iteration, 8 hops per site)
- Leapfrog: `n_steps * (n_inner * gauge_force + fermion_force + link_update)`

**Typical parameters:**
- `n_steps = 20`, `n_inner = 5`, `dt = 0.5 / n_steps = 0.025`
- CG iterations: `50-500` depending on `kappa` (closer to `kappa_c` = more iterations)

**Parallelization strategy:**
- **CPU (Rust+rayon)**: Checkerboard decomposition for link updates (even/odd sites). CG matvec parallelized over sites (rayon `par_iter` over chunks).
- **GPU (JAX, optional)**: Full HMC trajectory on GPU. D_W applied as batched stencil via `jax.lax.conv_general_dilated` or explicit scatter-gather. CG solver in JAX with `jax.lax.while_loop`.

**Estimated runtimes (CPU, SU(3), one trajectory):**

| L | Time (s) | CG iters | Notes |
|---|----------|----------|-------|
| 4 | 2 | 50 | Light quarks |
| 8 | 30 | 100 | |
| 12 | 200 | 200 | |
| 16 | 1200 | 300 | May need Hasenbusch mass preconditioning |

### 2.6 Validation

1. **Reversibility**: Run trajectory forward then backward. Verify `|H_final - H_initial| < 1e-8` (exact for exact arithmetic).
2. **dH distribution**: For accepted trajectories, `<exp(-dH)> = 1` exactly (Creutz equality). Monitor over 100+ trajectories.
3. **Acceptance rate**: Target 70-90%. If < 60%, reduce `dt`. If > 95%, increase `dt` or `n_steps`.
4. **Plaquette**: At `kappa=0` (infinite mass), HMC must reproduce quenched Metropolis plaquette. SU(2) at beta=2.4: `<P> = 0.587 +/- 0.003` (literature).
5. **Pion mass**: For SU(3), measure pseudoscalar correlator. At `beta=5.6, kappa=0.156`: `m_pi * a ~ 0.5` (CP-PACS 1999, arXiv:hep-lat/9903015).
6. **G2 at finite mu**: Verify `det(D_W)` remains real positive by monitoring `Im det / Re det < 1e-10` via stochastic estimator.
7. **CG residual**: `||D^dag D x - b|| / ||b|| < 1e-12` after solver converges.

### 2.7 Dependencies

**Rust crates (new):**
- None strictly required -- all linear algebra uses existing `nalgebra` and custom flat-matrix ops
- Optional: `sprs = "0.11"` for sparse matrix support in Rust (if doing CSR-based Dirac operator)

**Python packages:**
- `jax[cuda12]` (existing)
- No new Python dependencies

**Reference implementations:**
- [tmLQCD](https://github.com/etmc/tmLQCD) -- C, full HMC for Wilson/Clover/twisted-mass (BSD license)
- [QUDA](https://github.com/lattice/quda) -- C++/CUDA, GPU-accelerated HMC components (MIT license)
- [LatticeQCD.jl](https://github.com/akio-tomiya/LatticeQCD.jl) -- Julia, pedagogical HMC (MIT license)
- Luscher, "Computational strategies in lattice QCD" (arXiv:1002.4232) -- definitive reference

### 2.8 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| CG solver too slow for exceptional groups | HMC impractical | Medium | Even-odd preconditioning halves the linear system; Hasenbusch mass preconditioning for light quarks |
| Numerical instability in leapfrog | Large dH, low acceptance | Medium | Use 4th-order Omelyan integrator (2x fewer force evals); monitor `|dH|` per trajectory |
| D_W implementation bugs | Wrong physics | High (subtle) | Validate free-field spectrum analytically: `E(p) = sinh^{-1}(sum sin^2(p_mu) + (sum (1-cos(p_mu)) + m)^2)^{1/2}`. Cross-check with tmLQCD on identical config |
| G2 sign problem at large mu | Numerical noise | Low (sign-free proven for real reps) | Monitor `phase(det(D))` stochastically; G2 fund is real so det is manifestly real |

### 2.9 Timeline

| Task | Person-days |
|------|-------------|
| GaugeGroupHMC trait extension + generators for all 9 groups | 2 |
| Lie algebra momenta + exponential map | 1.5 |
| Wilson-Dirac operator (matrix-free stencil) | 3 |
| CG solver + even-odd preconditioning | 2 |
| Gauge force computation | 1 |
| Fermion force computation | 2 |
| Leapfrog + Sexton-Weingarten 2-timescale | 1.5 |
| HMC accept/reject + trajectory management | 1 |
| Validation suite (reversibility, Creutz, plaquette, pion) | 3 |
| JAX GPU port (optional) | 3 |
| **Total** | **20** |

---

## MODULE 3: GLUEBALL SPECTRUM

### 3.1 Motivation

The lightest glueball (scalar 0++ channel) is a fundamental prediction of any gauge theory. Its mass sets the confinement scale. Measuring glueball masses across 9+ gauge groups -- especially F4 and E6 where no prior lattice data exists -- provides unique data for testing the ECI framework and the universal S2/A formula. Comparison of glueball mass ratios (e.g., `m(0++)/sqrt(sigma)`) across groups tests the universality of the confining string picture.

### 3.2 Architecture

```
kevinotron/src/observables/glueball.rs     # Correlator measurement
kevinotron/src/observables/smearing.rs     # APE/stout smearing
kevinotron/src/observables/gevp.rs         # Generalized eigenvalue problem
kevinotron/scripts/glueball_analysis.py    # Effective mass + fit
```

**Observable trait extension:**

```rust
pub struct GlueballMeasurement {
    pub correlator: Vec<Vec<f64>>,  // C_ij(t), i,j = operator index, t = 0..Lt
    pub operators: Vec<String>,     // names: "plaquette", "rectangle_1x2", "chair", ...
    pub smearing_levels: Vec<usize>,
}
```

### 3.3 Key Algorithms

**3.3.1 Spatial Smearing (APE)**

APE smearing reduces UV noise while preserving the glueball signal. Apply iteratively to spatial links only (preserve temporal extent for correlator):

```
FUNCTION ape_smear_spatial(lattice, group, alpha_smear, n_smear):
    FOR iter in 1..n_smear:
        FOR each spatial link U_i(x) (i = 0,1,2):
            # Spatial staple sum (only spatial directions j != i, j < 3)
            K_spatial = 0
            FOR j in {0,1,2} \ {i}:
                K_spatial += forward_staple(x, i, j) + backward_staple(x, i, j)
            
            # Smeared link
            U_smeared = (1 - alpha_smear) * U_i(x) + (alpha_smear / 4) * U_i(x) * K_spatial
            U_smeared = group.reproject(U_smeared)  # back onto group manifold
            lattice.set_spatial(x, i, U_smeared)
    
    RETURN lattice
```

Standard parameters: `alpha_smear = 0.5`, `n_smear = 20-50`.

**3.3.2 Glueball Operators**

For the 0++ channel, construct gauge-invariant operators by summing over all spatial orientations:

```
O_plaq(t)    = SUM_{x,i<j<=2} Re Tr(P_{ij}(x,t))       # 1x1 plaquette
O_rect12(t)  = SUM_{x,i<j<=2} Re Tr(R_{ij}^{1x2}(x,t))  # 1x2 rectangle
O_rect21(t)  = SUM_{x,i<j<=2} Re Tr(R_{ij}^{2x1}(x,t))  # 2x1 rectangle
O_chair(t)   = SUM_{x,i,j,k distinct} Re Tr(chair_{ijk}(x,t))  # bent rectangle
O_plaq_s(t)  = same as O_plaq but on smeared links (different smearing levels)
```

Build these at multiple smearing levels to create an `N_op x N_op` correlator matrix.

**3.3.3 Correlator Measurement**

```
FUNCTION measure_correlator_matrix(lattice, group, operators):
    Lt = lattice.lt
    N_op = len(operators)
    C = zeros(N_op, N_op, Lt)
    
    # Compute operator values at each timeslice
    O = zeros(N_op, Lt)
    FOR i, op in enumerate(operators):
        FOR t in 0..Lt:
            O[i, t] = op.evaluate(lattice, group, t)
    
    # Connected correlator (subtract vacuum)
    FOR i in 0..N_op:
        FOR j in 0..N_op:
            FOR dt in 0..Lt:
                sum = 0
                FOR t0 in 0..Lt:
                    t1 = (t0 + dt) % Lt
                    sum += O[i, t0] * O[j, t1]
                C[i, j, dt] = sum / Lt - mean(O[i]) * mean(O[j])
    
    RETURN C
```

**3.3.4 Effective Mass**

```
m_eff(t) = log(C(t) / C(t+1))
```

For periodic boundary conditions (our case), use the cosh-form:

```
m_eff(t) = arccosh((C(t-1) + C(t+1)) / (2 * C(t)))
```

**3.3.5 Generalized Eigenvalue Problem (GEVP)**

Build the correlator matrix `C_{ij}(t)` from multiple operators. Solve:

```
C(t) v_n(t, t0) = lambda_n(t, t0) C(t0) v_n(t, t0)
```

The effective mass of the n-th state:

```
m_n^eff(t) = log(lambda_n(t, t0) / lambda_n(t+1, t0))
```

This separates excited states much better than single-operator correlators.

```
FUNCTION gevp_analysis(C_matrix, t0):
    # C_matrix: (N_op, N_op, Lt) correlator matrix
    Lt = C_matrix.shape[2]
    N_op = C_matrix.shape[0]
    
    C0 = C_matrix[:, :, t0]  # reference correlator
    eigenvalues = zeros(N_op, Lt)
    
    FOR t in 0..Lt:
        Ct = C_matrix[:, :, t]
        # Solve generalized eigenvalue problem
        # Ct v = lambda C0 v
        lambdas = scipy.linalg.eigvalsh(Ct, C0)
        eigenvalues[:, t] = sort(lambdas)[::-1]  # descending
    
    # Effective masses from eigenvalues
    m_eff = zeros(N_op, Lt-1)
    FOR n in 0..N_op:
        FOR t in 1..Lt-1:
            IF eigenvalues[n, t] > 0 AND eigenvalues[n, t+1] > 0:
                m_eff[n, t] = log(eigenvalues[n, t] / eigenvalues[n, t+1])
    
    RETURN m_eff
```

### 3.4 Data Structures

| Structure | Size | Notes |
|-----------|------|-------|
| Operator values `O[i,t]` | `N_op * Lt * 8` bytes | Per config |
| Correlator matrix `C[i,j,t]` | `N_op^2 * Lt * 8` bytes | Accumulated over configs |
| Smeared lattice copy | Same as lattice | Temporary per smearing level |
| GEVP eigenvalues | `N_op * Lt * 8` bytes | Per jackknife sample |

With `N_op = 6` (3 operators x 2 smearing levels), SU(3) at L=12: correlator matrix = 6*6*24*8 = 6.9 KB per jackknife sample.

### 3.5 Performance

**FLOP counts per config:**
- APE smearing: `O(n_smear * 3 * N_sites * d_fund^3)` (3 spatial directions, staple = 6 mults)
- Operator evaluation: `O(N_op * 3 * N_sites * d_fund^3)` (3 plaquette orientations per spatial site)
- Correlator: `O(N_op^2 * Lt^2)` (negligible)
- GEVP: `O(N_op^3 * Lt)` (negligible)

**Parallelization strategy:**
- Smearing: Parallelize over sites (even/odd checkerboard for thread safety)
- Operator evaluation: Parallelize over timeslices (rayon `par_iter`)
- Correlator accumulation: Sequential per config, then average + jackknife

**Estimated runtimes per config:**

| Group | L | Smearing (ms) | Operators (ms) | Total (ms) |
|-------|---|--------------|---------------|-----------|
| SU(2) | 8 | 50 | 20 | 70 |
| SU(3) | 12 | 300 | 100 | 400 |
| G2 | 8 | 200 | 80 | 280 |
| F4 | 4 | 400 | 150 | 550 |

### 3.6 Validation

1. **Free-field test**: On cold-start (all links = I), `C(t) = const` (no mass gap) -- verify flat correlator.
2. **SU(2) glueball**: At `beta = 2.5`, L = 16, Lt = 32: `m(0++) * a = 1.2 +/- 0.1`. Literature: Teper (arXiv:hep-lat/9804008) gives `m(0++) / sqrt(sigma) = 3.73 +/- 0.17`.
3. **SU(3) glueball**: At `beta = 6.0`, L = 16, Lt = 32: `m(0++) * a = 0.83 +/- 0.05`. Literature: Morningstar-Peardon (1999, arXiv:hep-lat/9911002) gives `m(0++) = 1730 +/- 80` MeV.
4. **G2 glueball**: Literature reference: Holland-Minkowski-Pepe-Wiese (JHEP 2003, arXiv:hep-lat/0302023): `m(0++) / sqrt(sigma) ~ 3.5-4.0`.
5. **GEVP consistency**: Ground state mass from GEVP should agree with single-plaquette effective mass at large t.
6. **Plateau quality**: `chi^2/dof < 2` for constant fit in plateau region `[t_min, t_max]`.

### 3.7 Dependencies

**Rust crates (new):** None.

**Python packages:**
- `scipy.linalg.eigh` for GEVP (existing dependency)
- `lmfit` or `scipy.optimize.curve_fit` for plateau fitting (both already available)

**Reference implementations:**
- [SIMULATeQCD](https://github.com/LatticeQCD/SIMULATeQCD) -- C++/CUDA, multi-GPU glueball measurement (MIT license)
- Morningstar-Peardon noise reduction: arXiv:1403.2936

### 3.8 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Signal-to-noise exponential decay | No plateau visible for t > 3-4 | High for large masses | More smearing levels; variational (GEVP) with 6+ operators; increase statistics to 5000+ configs |
| Finite-volume effects | Systematic shift in mass | Medium | Measure at multiple L values; require `m * L > 5` |
| F4/E6 glueball: no literature benchmark | Cannot validate | Certain | Cross-check ratios: `m(0++)/sqrt(sigma)` should be ~3.5-4.5 (universal string picture); verify SU(2,3), G2 first |
| Excited state contamination | Wrong mass extraction | Medium | GEVP with `t0 >= 2`; multi-exponential fit; constrained curve fitting |

### 3.9 Timeline

| Task | Person-days |
|------|-------------|
| APE smearing module | 1.5 |
| Glueball operators (plaquette, rectangle, chair) | 2 |
| Correlator measurement + accumulation | 1.5 |
| Effective mass + plateau fitting | 1 |
| GEVP solver | 1.5 |
| Integration into main loop (measure every N sweeps) | 1 |
| Validation on SU(2), SU(3), G2 | 2 |
| F4 world-first measurement | 1 |
| **Total** | **12** |

---

## MODULE 4: FINITE TEMPERATURE (Polyakov Loop + Deconfinement)

### 4.1 Motivation

The deconfinement phase transition is characterized by the spontaneous breaking of center symmetry, signaled by the Polyakov loop expectation value. For SU(N) with center Z_N, this is a genuine phase transition (first-order for N >= 3, second-order for N = 2). For groups with trivial center (G2, F4, SO(7)), there is no center symmetry to break, so the transition is a crossover. Mapping this transition across 9+ groups provides critical data for the ECI framework, which connects lattice EE to physical observables. The finite-temperature behavior also determines the critical temperature T_c, the latent heat, and the equation of state.

### 4.2 Architecture

```
kevinotron/src/observables/polyakov.rs     # Polyakov loop measurement
kevinotron/src/observables/mod.rs          # Updated to export polyakov
kevinotron/scripts/finite_temp_scan.py     # T_c scanning script
kevinotron/scripts/binder_analysis.py      # Binder cumulant analysis
```

**GaugeGroup trait extension** (in `groups/mod.rs`):

```rust
pub trait GaugeGroup: Send + Sync {
    // ... existing methods ...
    
    /// Center order |Z(G)|: 1 for G2/SO(7)/F4, N for SU(N), 2 for Sp(4)
    fn center_order(&self) -> usize;
    
    /// Trace in fundamental rep, returning complex (re, im)
    /// For real groups, im = 0 always.
    fn trace_complex(&self, u: &[f64]) -> (f64, f64);
}
```

### 4.3 Key Algorithms

**4.3.1 Polyakov Loop**

```
FUNCTION polyakov_loop(lattice, group, spatial_site):
    # Product of temporal links at fixed spatial position
    x = spatial_site  # (x0, x1, x2)
    prod = group.identity()
    
    FOR t in 0..Lt:
        U_t = lattice.get([x[0], x[1], x[2], t], 3)  # temporal direction = 3
        prod = group.mul(prod, U_t)
    
    # L(x) = (1/d_fund) * Tr(prod)
    RETURN group.trace_complex(prod)
```

**4.3.2 Polyakov Loop Observables**

```
FUNCTION polyakov_observables(lattice, group):
    Ls = lattice.ls
    N_spatial = Ls^3
    
    L_values = []
    FOR x0 in 0..Ls:
        FOR x1 in 0..Ls:
            FOR x2 in 0..Ls:
                (re, im) = polyakov_loop(lattice, group, (x0, x1, x2))
                L_values.append(complex(re, im) / group.dim_fund())
    
    L_mean = mean(L_values)                           # complex mean
    L_abs = mean(|L| for L in L_values)               # |L| mean (order parameter)
    L_abs2 = mean(|L|^2 for L in L_values)            # for susceptibility
    L_abs4 = mean(|L|^4 for L in L_values)            # for Binder cumulant
    
    # Susceptibility: chi_L = V * (<|L|^2> - <|L|>^2)
    chi_L = N_spatial * (L_abs2 - L_abs^2)
    
    # Binder cumulant: B_4 = <|L|^4> / <|L|^2>^2
    B_4 = L_abs4 / L_abs2^2
    
    RETURN {L_mean, L_abs, chi_L, B_4}
```

**4.3.3 Temperature Scan**

The temperature is `T = 1 / (a * Lt)` where `a` is the lattice spacing (set by beta). To scan temperature at fixed lattice spacing, vary Lt:

```
FUNCTION temperature_scan(group, Ls, beta, Lt_values, n_therm, n_meas):
    results = []
    
    FOR Lt in Lt_values:  # e.g., Lt = 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32
        lattice = Lattice4D(group, Ls, Lt, beta)
        
        # Thermalize
        FOR s in 0..n_therm:
            lattice.sweep_alpha(group, 0.0, epsilon, rng)
        
        # Measure
        poly_data = []
        FOR m in 0..n_meas:
            FOR skip in 0..n_skip:
                lattice.sweep_alpha(group, 0.0, epsilon, rng)
            poly = polyakov_observables(lattice, group)
            poly_data.append(poly)
        
        # Average + jackknife errors
        avg = jackknife_average(poly_data)
        results.append((Lt, avg))
    
    RETURN results
```

**4.3.4 T_c Determination**

For second-order transitions (SU(2)): Binder cumulant crossing.

```
FUNCTION find_tc_binder(results_L1, results_L2):
    # B_4 curves for two lattice sizes cross at T_c
    # Interpolate B_4(Lt) for each Ls, find crossing
    # B_4 = 1 in disordered phase, B_4 = 3 in ordered phase (real order parameter)
    # For complex order parameter (SU(N>=3)): B_4 = pi/2 disordered, B_4 = 2 ordered
    
    # Use linear interpolation to find Lt_c where B_4(Ls1) = B_4(Ls2)
    crossing_Lt = bisect(B4_Ls1(Lt) - B4_Ls2(Lt), Lt_min, Lt_max)
    T_c = 1 / (a(beta) * crossing_Lt)
    
    RETURN T_c
```

For first-order transitions (SU(N>=3)): double-peak structure in Polyakov loop histogram.

For crossovers (G2, F4, SO(7)): peak of susceptibility `chi_L(T)`.

**4.3.5 Finite-Size Scaling**

Near T_c, observables scale with the spatial volume:

```
chi_L_max ~ Ls^{gamma/nu}      (susceptibility peak height)
B_4(T_c) ~ const               (Binder cumulant at crossing)
<|L|>(T_c) ~ Ls^{-beta/nu}    (order parameter at T_c)
```

For SU(2): 3D Ising universality class (nu=0.6301, gamma=1.2372, beta=0.3265).
For SU(3): first-order, no universality (delta-function peaks in infinite volume).
For G2: smooth crossover, no divergence.

### 4.4 Data Structures

| Structure | Size | Notes |
|-----------|------|-------|
| Polyakov loop per site | `N_spatial * 16` bytes | Complex (re, im) per spatial site |
| Scan results | `N_Lt * N_meas * 4 * 8` bytes | (L_abs, chi, B4, L_re) per config per Lt |
| Histogram bins | `100 * 8` bytes per Lt | For double-peak analysis |

Memory overhead is negligible. The dominant cost is MC generation.

### 4.5 Performance

**FLOP counts per Polyakov loop measurement:**
- Product of Lt matrices: `Lt * d_fund^3` FLOPs per spatial site
- Total: `N_spatial * Lt * d_fund^3 * 2` (complex multiplication)

**Parallelization:**
- Polyakov loops at different spatial sites are independent -- perfect for rayon `par_iter`
- Temperature scan: each Lt is independent -- can run in parallel on different cores

**Estimated runtimes:**

| Group | Ls | Lt scan points | Configs/point | Wall-clock (h) |
|-------|----|----|------|------|
| SU(2) | 12 | 12 | 2000 | 4 |
| SU(3) | 12 | 12 | 2000 | 8 |
| G2 | 8 | 12 | 2000 | 6 |
| F4 | 4 | 10 | 1000 | 12 |

### 4.6 Validation

1. **High-T limit**: At very small Lt (Lt=2), `<|L|>` should approach `1/d_fund` for all groups (random walk of Lt=2 matrices).
2. **Low-T limit**: At large Lt (Lt >> Ls), `<|L|> -> 0` for SU(N) (confined phase, center symmetry unbroken). For G2, `<|L|>` remains small but nonzero.
3. **SU(2) T_c**: At beta=2.3, `T_c * a ~ 1/N_t_c` with `N_t_c = 4-5` (Fingberg-Heller-Mitrjushkin 1993). Binder cumulant crossing should give 3D Ising critical exponents.
4. **SU(3) T_c**: At beta=6.0, `N_t_c ~ 8` (first-order transition). Look for double-peak structure in Re(L) histogram. Latent heat `Delta(epsilon) / T_c^4 ~ 1.4` (Karsch 2001).
5. **G2 crossover**: Holland-Minkowski-Pepe-Wiese (JHEP 2003, arXiv:hep-lat/0302023) show a first-order deconfinement transition for G2 despite trivial center, with `T_c / sqrt(sigma) ~ 0.9`. Subsequent work by Cossu et al. (arXiv:0709.0669) confirms the transition and studies Polyakov loop susceptibility.
6. **Z_N symmetry**: For SU(N), histogram of `arg(L)` should show N peaks below T_c (Z_N broken) and uniform above T_c.
7. **F4 prediction**: No literature exists. Expect crossover (trivial center, |Z|=1). Susceptibility peak position gives T_c/sqrt(sigma).

### 4.7 Dependencies

**Rust crates:** None new.

**Python packages:**
- `scipy.optimize` for Binder cumulant crossing (existing)
- `matplotlib` for Polyakov loop histograms (existing)

**Literature:**
- Holland, Minkowski, Pepe, Wiese -- JHEP 0307:007 (2003), arXiv:hep-lat/0302023
- Cossu et al. -- arXiv:0709.0669 (G2 finite temperature)
- Lucini, Teper, Wenger -- JHEP 0401:061 (2004), arXiv:hep-lat/0307017 (SU(N) large-N deconfinement)

### 4.8 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Insufficient Ls for finite-size scaling | Cannot extract T_c | Medium | Use at least 3 spatial sizes (Ls=8,12,16 for SU(2/3); Ls=4,6,8 for exceptional groups) |
| Metastability near first-order transition | Stuck in one phase | High for SU(3) | Start from both ordered and disordered initial conditions; parallel tempering; multicanonical simulation |
| Poor signal for exceptional groups at small L | Noisy B4 | Medium | More statistics (5000+ configs); APE-smeared Polyakov loop |
| Lattice spacing ambiguity | Cannot quote T_c in physical units | Low | Use Creutz ratio sigma*a^2 (already implemented) to set scale |

### 4.9 Timeline

| Task | Person-days |
|------|-------------|
| Polyakov loop measurement in Rust | 1 |
| center_order + trace_complex trait extension | 0.5 |
| Susceptibility + Binder cumulant | 0.5 |
| Temperature scan script | 1 |
| Finite-size scaling analysis | 1 |
| Histogram / double-peak analysis | 0.5 |
| Validation on SU(2), SU(3) | 2 |
| G2 crossover measurement | 1 |
| F4 world-first measurement | 1 |
| **Total** | **9** |

---

## MODULE 5: E6 GAUGE GROUP

### 5.1 Motivation

E6 is a 78-dimensional exceptional Lie group with 27-dimensional complex fundamental representation. It is the **first group** that combines non-trivial center (Z3, same as SU(3)) with exceptional Dynkin type. This makes it a uniquely discriminating test for the ECI S2/A formula:

- SU(3): Z3 center, classical type A2
- G2: exceptional, trivial center
- **E6**: exceptional, Z3 center -- combines both features

Group data: `dim_adj = 78`, `dim_fund = 27`, `|Phi+| = 36`, `h^vee = 12`, `|Z| = 3`, `rank = 6`, `beta_norm = d_fund = 27`.

Formula prediction at beta=50: `S2/A = (pi+e)*14 - log(13) - 12 = 69.6` (approximate, using asymptotic formula with `beta - |Phi+| = 14`).

### 5.2 Architecture

```
kevinotron/src/groups/e6.rs            # Rust: E6 group implementation
kevinotron/src/groups/mod.rs           # Updated to include E6
kevinotron/scripts/build_e6_generators.py  # Python: generator construction + validation
kevinotron/scripts/e6_validation.py    # Cross-validation tests
```

**File modifications:**
- `src/groups/mod.rs`: Add `pub mod e6;`
- `src/main.rs`: Add `"e6" => Box::new(E6Group::new())` to group dispatch
- `jax_ds/fp_adjoint_fast.py`: Add E6 to `GROUP_CONFIG` dictionary
- `kevinotron_data/adjoint.py`: Works unchanged (generic over generators)

### 5.3 Key Algorithms

**5.3.1 Generator Construction**

E6 has 78 generators acting on the 27-dimensional complex fundamental representation. Construction via the Chevalley-Serre basis:

**Step 1: Cartan matrix of E6**

```
A_E6 = [[ 2, -1,  0,  0,  0,  0],
         [-1,  2, -1,  0,  0,  0],
         [ 0, -1,  2, -1,  0, -1],
         [ 0,  0, -1,  2, -1,  0],
         [ 0,  0,  0, -1,  2,  0],
         [ 0,  0, -1,  0,  0,  2]]
```

(Dynkin diagram: nodes 1-2-3-4-5 with node 6 branching from node 3.)

**Step 2: Build the 27-dim representation**

The 27-dimensional representation of E6 can be constructed explicitly via the Jordan algebra approach. The exceptional Jordan algebra `J_3(O)` consists of 3x3 Hermitian matrices over the octonions:

```
X = [[alpha,  a^*,  b  ],
     [a,      beta,  c^*],
     [b^*,    c,     gamma]]
```

where `alpha, beta, gamma` are real and `a, b, c` are octonions. This gives `3 + 3*8 = 27` real dimensions = 27 complex dimensions after complexification.

E6 is the automorphism group preserving the determinant of this algebra:

```
det(X) = alpha*beta*gamma - alpha*|c|^2 - beta*|b|^2 - gamma*|a|^2 + 2*Re(a*b*c)
```

**Step 3: Explicit 27x27 matrices**

Use the established construction from the E6Tensors package (arXiv:1605.05920) or the GAP computational algebra system. The practical approach:

```python
FUNCTION build_e6_generators():
    # Method: embed E6 in SU(27) via its 27-dim fundamental rep
    
    # Start from the 6 simple roots (Chevalley generators E_i, F_i, H_i)
    # E_i are raising operators, F_i = E_i^dag are lowering, H_i = [E_i, F_i]
    
    # Build Cartan subalgebra: 6 diagonal generators H_i (27x27)
    # Build root generators: 36 positive root generators E_alpha (27x27)
    #   by iterated commutators [E_i, [E_j, [...]]
    # Build 36 negative root generators F_alpha = E_alpha^dag
    # Total: 6 + 36 + 36 = 78 generators
    
    # Anti-Hermitian basis: T_a = i * (E_alpha - E_alpha^dag) / sqrt(2)  (compact)
    #                        T_b = (E_alpha + E_alpha^dag) / sqrt(2)      (compact)
    #                        T_c = i * H_i                                 (Cartan)
    
    # Normalize: Tr(T_a T_b) = -delta_ab / 2
    
    # Validate: [T_a, T_b] = f^{abc} T_c with correct structure constants
    
    RETURN generators  # (78, 27, 27) complex128
```

**Alternative construction (more robust for numerical work):** Build E6 generators by embedding in SU(27). Start from the 78-dimensional subspace of su(27) that satisfies the E6 Lie bracket closure. Use the known branching rule E6 -> SU(3) x SU(3) x SU(3) to construct the generators in blocks.

The Python script `build_e6_generators.py` computes the 78 generators once and saves them as a `.npy` file. The Rust code loads them at initialization.

**5.3.2 Rust Implementation**

```rust
pub struct E6Group {
    generators: Vec<Vec<f64>>,  // 78 generators, each 2*27*27 = 1458 f64
}

impl E6Group {
    pub fn new() -> Self {
        // Load pre-computed generators from embedded data
        // or compute from Chevalley-Serre basis
        let generators = load_e6_generators();
        assert_eq!(generators.len(), 78);
        E6Group { generators }
    }
}

impl GaugeGroup for E6Group {
    fn name(&self) -> &str { "E6" }
    fn dim_fund(&self) -> usize { 27 }
    fn dim_adj(&self) -> usize { 78 }
    fn is_complex(&self) -> bool { true }
    fn beta_norm(&self) -> f64 { 27.0 }
    
    fn identity(&self) -> LinkData { cmat_identity(27) }
    
    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData {
        let mut w = RngWrapper(rng);
        let mut a = cmat_zero(27);
        for g in &self.generators {
            let c: f64 = w.sample::<f64, _>(StandardNormal) * epsilon;
            for i in 0..a.len() {
                a[i] += g[i] * c;
            }
        }
        // Taylor-12 exponential + unitarization
        let u = cmat_expm_taylor12(&a, 27);
        cmat_unitarize(&u, 27)
    }
    
    fn dagger(&self, u: &[f64]) -> LinkData { cmat_dagger(u, 27) }
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_mul(a, b, 27) }
    fn trace_re(&self, u: &[f64]) -> f64 { cmat_trace_re(u, 27) }
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData { cmat_add(a, b, 27) }
    fn zero(&self) -> LinkData { cmat_zero(27) }
    
    fn reproject(&self, u: &[f64]) -> LinkData {
        cmat_unitarize(u, 27)
    }
}
```

**5.3.3 Matrix Operations Performance**

The critical bottleneck for E6 is the matrix multiply `cmat_mul` with `n=27`:

```
Cost of one cmat_mul(27):
  - 27^3 = 19683 complex multiplications
  - 27^3 = 19683 complex additions
  - Total: ~78732 FLOPs (complex) = ~315K FLOPs (real)
```

Compare: SU(3) cmat_mul = 27 complex mults = ~108 real FLOPs. E6 is **~2900x more expensive per matrix multiply** than SU(3).

**5.3.4 Optimized Matrix Multiply**

For n=27, the naive `O(n^3)` multiply in `cmat_mul` is sufficient (Strassen would give marginal benefit at n=27 and worse numerical stability). However, the inner loop should be optimized:

```rust
// Optimized cmat_mul for n=27 with SIMD potential
pub fn cmat_mul_27(a: &[f64], b: &[f64]) -> LinkData {
    let n = 27;
    let mut c = vec![0.0f64; 2 * n * n];
    for i in 0..n {
        for k in 0..n {
            let (ar, ai) = (a[2*(i*n+k)], a[2*(i*n+k)+1]);
            if ar.abs() < 1e-30 && ai.abs() < 1e-30 { continue; }
            for j in 0..n {
                let (br, bi) = (b[2*(k*n+j)], b[2*(k*n+j)+1]);
                let idx = 2 * (i * n + j);
                c[idx]     += ar * br - ai * bi;
                c[idx + 1] += ar * bi + ai * br;
            }
        }
    }
    c
}
```

The `ikj` loop order (vs `ijk`) gives better cache locality for the output row.

### 5.4 Data Structures

| Structure | Size | Notes |
|-----------|------|-------|
| One E6 link matrix | `2 * 27 * 27 * 8 = 11664` bytes | Complex 27x27 |
| 78 generators | `78 * 11664 = 909792` bytes (~0.87 MB) | Loaded once at init |
| Lattice L=4, Lt=8 | `4^3 * 8 * 4 * 11664 = 95.5 MB` | All link variables |
| Lattice L=6, Lt=12 | `6^3 * 12 * 4 * 11664 = 725 MB` | Approaches 32 GB DDR5 limit |

**Memory budget for E6 at L=6:**

| Component | Size (MB) |
|-----------|-----------|
| Lattice links | 725 |
| Staple buffer (per thread) | 0.011 |
| RNG state | negligible |
| **Total per thread** | 725 |

At L=6, a single lattice occupies ~725 MB, well within the 32 GB DDR5 budget. At L=8: `8^3 * 16 * 4 * 11664 = 3.44 GB` -- still feasible.

FP spectral at L=4: `dim = 256 * 78 = 19968`. Dense: 3.19 GB (f64) -- requires sparse Lanczos (Module 1).

### 5.5 Performance

**FLOP counts per Metropolis sweep:**
- One link update: staple_sum (6 directions x 3 mul_27 + 2 dagger_27) + trial (1 expm + 1 mul_27) + action (2 mul_27 + 2 trace_re)
- Staple sum: ~18 `cmat_mul(27)` = 18 * 315K = 5.67M FLOPs
- Total per link: ~7M FLOPs
- One sweep: `N_links * 7M = 4^3*8*4 * 7M = 14.3 GFLOPs` (L=4)
- At 5 GHz with AVX2 (16 FLOP/cycle, 14 cores): ~14.3G / (5G * 16 * 14) = 0.013s per sweep

**Estimated runtimes (L=4, 500 therm + 200*5 meas = 1500 sweeps):**
- SU(3): ~5 seconds (established baseline)
- E6: ~20 seconds (bottleneck is 27x27 matrix multiply, ~2900x SU(3) per link but fewer sites)
- E6 at L=6: ~300 seconds per sweep (L^4 scaling), total ~450000 seconds = 5 days for full EE scan with 11 alpha-points. This is the practical limit.

**Parallelization:**
- Rayon parallel alpha-points (existing): 11 alpha-points on 14 cores
- No GPU offload for Metropolis (link updates are inherently sequential within a sweep)
- FP spectral: sparse Lanczos on CPU (Module 1 prerequisite)

### 5.6 Validation

1. **Generator closure**: Verify `[T_a, T_b] = f^{abc} T_c` for all 78*77/2 = 3003 pairs. Residual `||[T_a, T_b] - sum_c f^{abc} T_c|| < 1e-14`.
2. **Anti-Hermitian**: `||T_a + T_a^dag|| < 1e-14` for all 78 generators.
3. **Normalization**: `Tr(T_a T_b) = -delta_ab / 2` for all a,b.
4. **Killing form**: `Tr_adj(ad(T_a) ad(T_b)) = 2 * h^vee * Tr_fund(T_a T_b) = 2 * 12 * (-1/2) * delta_ab = -12 * delta_ab`.
5. **Group element properties**: Random element U near identity should satisfy `|det(U)| = 1 +/- 1e-10` and `||U^dag U - I|| < 1e-10`.
6. **Plaquette**: Cold-start `<P> = 1.0` exactly. After thermalization at beta >> 1, `<P> -> 1 - C/beta + ...` with `C = dim_adj / (4 * d_fund) = 78 / 108 = 0.722` (leading weak-coupling).
7. **Strong-coupling expansion**: At beta=0, `<P> = I_1(beta/d_fund) / I_0(beta/d_fund)` for SU(N); analogous check for E6 using character expansion.
8. **Center structure**: Z(E6) = Z_3. Verify that `omega = exp(2*pi*i/3) * I_{27}` commutes with all generators and satisfies `omega^3 = I`. The Polyakov loop should show Z_3 symmetry structure (Module 4 cross-validation).
9. **Branching**: Under E6 -> SU(3)^3, the 27 decomposes as (3,3,1) + (1,3_bar,3) + (3_bar,1,3_bar). Verify numerically by computing Casimir operators in the embedded SU(3) subalgebras.

### 5.7 Dependencies

**Rust crates:** None new (uses existing `nalgebra`, `num-complex`).

**Python packages:**
- `numpy` (existing) for generator construction
- Optional: `sage` or `gap` for Lie algebra computations (used only for initial generator construction, not runtime)

**References:**
- E6Tensors Mathematica package: arXiv:1605.05920
- "E6, the Group" by J.R. Faulkner and J.C. Ferrar: arXiv:1212.3182
- E6 27-dim rep construction via Jordan algebra: Schafer, "Introduction to Nonassociative Algebras" (1966)
- E6 CG coefficients: arXiv:hep-ph/9912365

### 5.8 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Generator construction errors | Wrong physics | Medium | Triple-validate: (1) Lie bracket closure, (2) Killing form matches h^vee=12, (3) character of identity = 27 |
| Taylor-12 expm insufficient for 27x27 | Large reprojection error | Low | Monitor `||U^dag U - I||` after each expm. If > 1e-8, switch to Pade-Scaling-Squaring via nalgebra |
| 27x27 matrix multiply too slow for L>=6 | Production runs impractical | Medium | Use BLAS (openblas-src crate) for matrix multiply; consider blocked matrix-matrix multiply; GPU offload for staple computation |
| cmat_unitarize not det=1 for n=27 | Drift from SU(27) subgroup E6 | Medium | After Gram-Schmidt, compute det and divide last column by det^(1/27). For E6 specifically, also project onto the E6 submanifold using the cubic invariant |
| E6 subgroup projection | Not staying in E6 subset of SU(27) | High | After unitarization, project onto E6 by minimizing `||U - U_E6||` using the 78 generators. This is the E6 analog of the Sp(4) symplectic projection |

### 5.9 Timeline

| Task | Person-days |
|------|-------------|
| Python generator construction + validation | 3 |
| Rust E6 group implementation | 2 |
| Generator embedding in Rust (load from .npy or compile-time include) | 1 |
| E6 reprojection (SU(27) unitarization + E6 submanifold projection) | 2 |
| Integration into main.rs + CLI | 0.5 |
| Plaquette validation (cold/hot start, weak-coupling) | 1 |
| FP spectral integration (requires Module 1 sparse) | 1 |
| EE measurement at L=4 | 1 |
| Performance profiling + optimization | 1.5 |
| **Total** | **13** |

---

## Cross-Module Integration Plan

### Dependency Graph

```
Module 1 (Sparse FP)  <--- standalone, no dependencies
Module 2 (HMC)         <--- standalone, no dependencies
Module 3 (Glueball)    <--- standalone, no dependencies
Module 4 (Finite Temp) <--- standalone, no dependencies
Module 5 (E6 Group)    <--- depends on Module 1 for FP spectral at L>=4
                        <--- benefits from Module 3 for glueball
                        <--- benefits from Module 4 for deconfinement
```

### Recommended Implementation Order

1. **Module 1 (Sparse FP)** -- 7 days. Unblocks all FP analysis for F4 at L>=6 and E6 at any L. Immediate payoff: can re-run all 9-group spectral analysis at L=6.
2. **Module 5 (E6 Group)** -- 13 days. Depends on Module 1 for validation. Provides the 10th gauge group and the critical Z3-exceptional test point.
3. **Module 4 (Finite Temp)** -- 9 days. Simple observable addition with high scientific payoff. Can run independently on existing 9 groups immediately.
4. **Module 3 (Glueball)** -- 12 days. Requires significant statistics (many configs). Can overlap with Module 4 production runs.
5. **Module 2 (HMC)** -- 20 days. Most complex module. Depends on Module 1 (sparse solver reuse for CG preconditioning) and benefits from Module 3 (glueball with dynamical fermions = unquenched spectrum).

**Total estimated effort: 61 person-days.**

### GaugeGroup Trait Evolution

The trait extensions required by modules 2, 4, and 5 should be coordinated:

```rust
pub trait GaugeGroup: Send + Sync {
    // === Existing methods (unchanged) ===
    fn name(&self) -> &str;
    fn dim_fund(&self) -> usize;
    fn dim_adj(&self) -> usize;
    fn is_complex(&self) -> bool;
    fn link_size(&self) -> usize;
    fn beta_norm(&self) -> f64;
    fn identity(&self) -> LinkData;
    fn random_near_id(&self, epsilon: f64, rng: &mut dyn RngCore) -> LinkData;
    fn dagger(&self, u: &[f64]) -> LinkData;
    fn mul(&self, a: &[f64], b: &[f64]) -> LinkData;
    fn trace_re(&self, u: &[f64]) -> f64;
    fn add(&self, a: &[f64], b: &[f64]) -> LinkData;
    fn zero(&self) -> LinkData;
    fn reproject(&self, u: &[f64]) -> LinkData;
    
    // === New methods (Module 4) ===
    fn center_order(&self) -> usize { 1 }  // default: trivial center
    fn trace_complex(&self, u: &[f64]) -> (f64, f64) {
        (self.trace_re(u), 0.0)  // default: real trace
    }
    
    // === New methods (Module 2 -- optional trait) ===
    // fn n_generators(&self) -> usize;
    // fn generator(&self, a: usize) -> LinkData;
    // fn project_to_algebra(&self, m: &[f64]) -> Vec<f64>;
    // fn exp_ipiu(&self, pi_coeffs: &[f64], epsilon: f64, u: &[f64]) -> LinkData;
    
    // === New methods (Module 3) ===
    // fn trace_im(&self, u: &[f64]) -> f64;  // Im Tr(U), for force computation
    
    // === Group-theory constants (useful for all modules) ===
    fn dual_coxeter(&self) -> usize { 0 }  // h^vee
    fn n_positive_roots(&self) -> usize { 0 }  // |Phi+|
}
```

The HMC-specific methods are placed in a separate `GaugeGroupHMC` trait to avoid breaking the existing API. Groups implement this trait only when HMC support is added.

### Shared Utilities

Several utilities are needed across modules and should be factored into shared locations:

1. **Jackknife resampling** (`scripts/jackknife.py`): Used by Modules 3, 4 for error estimation. Currently ad-hoc in various scripts.
2. **Blocked bootstrap** (`scripts/bootstrap.py`): Already exists in main.rs for EE; generalize for glueball and Polyakov.
3. **JSON metadata writer**: Standardize the output format across all modules. Each measurement produces a structured JSON with group, L, Lt, beta, observable, value, error, n_configs, timestamp.
4. **VRAM budget calculator** (`jax_ds/vram_budget.py`): Module 1 introduces this; reuse for Module 2 GPU HMC and Module 5 FP spectral.

### Testing Strategy

Each module includes its own validation suite (detailed in sections 1.6-5.6 above). Integration tests verify cross-module consistency:

1. **FP spectrum identity config**: All modules agree on the free-field spectrum for any group at any L.
2. **Glueball + Finite Temp**: At T >> T_c (small Lt), glueball correlator should show screening mass (Debye mass) instead of confining string mass. Verify `m_eff` decreases as Lt decreases past the transition.
3. **HMC + Quenched comparison**: At infinite fermion mass (kappa=0), HMC results must match Metropolis for all observables.
4. **E6 + Sparse FP**: Dense and sparse eigenvalues agree at L=4 within 1e-8.

---

## Appendix A: VRAM Budget Table

| Group | L | Lt | FP dim | Dense (GB) | Sparse CSR (MB) | Fermion dim | D_W dense (GB) |
|-------|---|----|----|------|------|------|------|
| U(1) | 4 | 8 | 512 | 0.002 | 0.02 | 2048 | 0.034 |
| SU(2) | 4 | 8 | 1536 | 0.019 | 0.2 | 4096 | 0.134 |
| SU(3) | 4 | 8 | 4096 | 0.134 | 1.1 | 6144 | 0.302 |
| SU(4) | 4 | 8 | 7680 | 0.472 | 3.6 | 8192 | 0.537 |
| SU(5) | 4 | 8 | 12288 | 1.21 | 8.7 | 10240 | 0.839 |
| G2 | 4 | 8 | 7168 | 0.411 | 3.2 | 14336 | 1.64 |
| Sp(4) | 4 | 8 | 5120 | 0.210 | 1.7 | 8192 | 0.537 |
| SO(7) | 4 | 8 | 10752 | 0.925 | 6.4 | 14336 | 1.64 |
| F4 | 4 | 8 | 26624 | 5.67 | 38.1 | 53248 | 22.7 |
| **E6** | **4** | **8** | **39936** | **12.8** | **85.5** | **55296** | **24.5** |
| SU(3) | 8 | 16 | 65536 | 34.4 | 17.9 | 98304 | 77.3 |
| E6 | 6 | 12 | 202176 | 327 | 432 | 279936 | 627 |

"Dense" = full matrix in f64. "D_W dense" = Wilson-Dirac in complex128.

Entries in **bold** are the new E6 module additions. Entries marked as > 16 GB require Module 1 (sparse Lanczos).

## Appendix B: Group Constants Reference

| Group | d_fund | d_adj | |Phi+| | h^vee | |Z| | Complex? | beta_norm |
|-------|--------|-------|--------|-------|------|---------|-----------|
| U(1) | 1 | 1 | 0 | 0 | - | Yes | 1 |
| SU(2) | 2 | 3 | 1 | 2 | 2 | Yes | 2 |
| SU(3) | 3 | 8 | 3 | 3 | 3 | Yes | 3 |
| SU(4) | 4 | 15 | 6 | 4 | 4 | Yes | 4 |
| SU(5) | 5 | 24 | 10 | 5 | 5 | Yes | 5 |
| G2 | 7 | 14 | 6 | 4 | 1 | No | 7 |
| Sp(4) | 4 | 10 | 4 | 3 | 2 | Yes | 4 |
| SO(7) | 7 | 21 | 9 | 5 | 1 | No | 7 |
| F4 | 26 | 52 | 24 | 9 | 1 | No | 26 |
| **E6** | **27** | **78** | **36** | **12** | **3** | **Yes** | **27** |

## Appendix C: Open-Source Reference Implementations

| Codebase | Language | License | Relevant features | Repository |
|----------|----------|---------|-------------------|------------|
| Grid | C++ | GPL-2 | IRL Lanczos, Wilson fermions, HMC | github.com/paboyle/Grid |
| QUDA | C++/CUDA | MIT | GPU eigensolver (TRLM), multi-grid CG, HMC force | github.com/lattice/quda |
| tmLQCD | C | GPL-2 | Full HMC, Wilson/Clover, RHMC | github.com/etmc/tmLQCD |
| OpenQCD | C | GPL-3 | DD-HMC, Luscher reference | luscher.web.cern.ch/luscher/openQCD |
| SIMULATeQCD | C++/CUDA | MIT | Multi-GPU, glueball, Polyakov loop | github.com/LatticeQCD/SIMULATeQCD |
| LatticeQCD.jl | Julia | MIT | Pedagogical HMC, all fermion types | github.com/akio-tomiya/LatticeQCD.jl |
| MILC | C | public domain | Staggered fermions, glueball, finite-T | github.com/milc-qcd/milc_qcd |

---

*End of specification.*
