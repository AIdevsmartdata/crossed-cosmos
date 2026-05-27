% OP_SU3_PORT_SPEC --- SU(3) port of FAST V3 BP α-integration + Modular Hamiltonian
% Author: Kévin Rémondière, ORCID 0009-0008-2443-7166, Oloron-Sainte-Marie, France
% Date: 2026-05-25
% Status: design specification, JAX pseudocode included, ready for implementation
%
% Mission: extend the SU(2) pipeline (FAST V3 α-integration + Modular Hamiltonian)
% to the SU(3) gauge group, in order to test the framework prediction
% κ(SU(N)) = 1/(2|Φ⁺(SU(N))|), namely κ(SU(3)) = 1/6 against the SU(2) anchor
% κ(SU(2)) = 1/2 (Bekenstein--Hawking).

# OP_SU3_PORT_SPEC --- Specification document

**File**: `OP_SU3_PORT_SPEC_2026-05-25.md`
**Author**: Kévin Rémondière (ORCID 0009-0008-2443-7166), Oloron-Sainte-Marie, France
**Project**: crossed-cosmos / lattice ECI universality of κ across gauge groups
**Reuses**: FAST V3 framework (`jax_su2_EE_BP2008b_FAST_2026-05-25.py`),
Modular Hamiltonian framework (`jax_su2_EE_MODULAR_2026-05-25.py`),
recipe document `OP_BP2008_RECIPE_2026-05-25.md`, spec document
`OP_MODULAR_HAMILTONIAN_SPEC_2026-05-25.md`
**Companion paper to come**: `PAPER_SU3_KAPPA_UNIVERSALITY.tex`
**Status**: design + JAX pseudocode + cost budget; implementation pending

---

## 0. Why this document exists

The framework derived in the crossed-cosmos programme over the past months
identifies, on the lattice side, a one-line formula for the leading area-law
coefficient of the Rényi-2 entanglement entropy in pure gauge theory:

$$
   \kappa(\mathrm{SU}(N)) \;=\; \frac{1}{2 \, |\Phi^{+}(\mathrm{SU}(N))|},
$$

where $|\Phi^{+}|$ denotes the number of positive roots of the root system of
$\mathrm{SU}(N)$. Specifically:

  - $\mathrm{SU}(2)$: $A_{1}$ root system, $|\Phi^{+}| = 1$, so
    $\kappa = 1/2$, $\kappa^{2} = 1/4$ — this matches the Bekenstein--Hawking
    horizon entropy density and is the value tested by the Modular Hamiltonian
    pipeline currently in production at $\beta = 2.4$, $L \in \{8, 12, 16\}$.
  - $\mathrm{SU}(3)$: $A_{2}$ root system, $|\Phi^{+}| = 3$, so
    $\kappa = 1/6$, $\kappa^{2} = 1/36 \approx 0.0278$ — distinct from
    Bekenstein--Hawking, predicted by the framework.

A clean measurement of $\kappa(\mathrm{SU}(3)) \approx 1/6$ on a lattice would
provide first cross-group evidence for the $1/(2|\Phi^{+}|)$ universality law,
discriminating it from group-trivial alternatives (constant $\kappa = 1/2$
across $N$) and from rank-only laws ($\kappa \propto 1/\mathrm{rank}$, which
would give $1/4$ for $\mathrm{SU}(3)$ instead of $1/6$).

This document specifies, at the level of theory, JAX pseudocode, and compute
budget, the SU(3) port of:

  1. the BP α-integration estimator (FAST V3 pipeline, sub-leading $C$-function);
  2. the Modular Hamiltonian estimator (Bisognano--Wichmann lattice observable,
     leading $\kappa$ directly).

Output: a full implementation that runs in 20--30 GPU-h and returns, with
controlled error, the two complementary entanglement coefficients for
SU(3) Wilson lattice gauge theory at $\beta = 6.0$.

---

## 1. SU(3) algebra basics

### 1.1 Group structure and dimensions

$\mathrm{SU}(3)$ is the group of $3 \times 3$ complex unitary matrices of unit
determinant. Setting $U \in \mathrm{SU}(3)$ means
$U U^{\dagger} = U^{\dagger} U = \mathbf{1}_{3}$ and $\det U = 1$.
Counting parameters: a generic complex $3 \times 3$ matrix has $18$ real
parameters; unitarity imposes $9$ real conditions, and unit determinant adds
one more, leaving $\dim \mathrm{SU}(3) = 8$. We will encode SU(3) elements as
$3 \times 3$ complex JAX arrays, never as 8-vectors of generator coefficients
(except temporarily when generating near-identity proposals).

### 1.2 Generators and Gell-Mann matrices

The Lie algebra $\mathfrak{su}(3)$ consists of $3 \times 3$ traceless
anti-Hermitian matrices, hence has real dimension $8$. The standard basis is
$T_{a} = \lambda_{a} / 2$ for $a = 1, \dots, 8$, where $\lambda_{a}$ are the
Hermitian Gell-Mann matrices:

$$
\begin{aligned}
\lambda_{1} &= \begin{pmatrix} 0&1&0\\1&0&0\\0&0&0 \end{pmatrix}, &
\lambda_{2} &= \begin{pmatrix} 0&-i&0\\i&0&0\\0&0&0 \end{pmatrix}, &
\lambda_{3} &= \begin{pmatrix} 1&0&0\\0&-1&0\\0&0&0 \end{pmatrix}, \\
\lambda_{4} &= \begin{pmatrix} 0&0&1\\0&0&0\\1&0&0 \end{pmatrix}, &
\lambda_{5} &= \begin{pmatrix} 0&0&-i\\0&0&0\\i&0&0 \end{pmatrix}, &
\lambda_{6} &= \begin{pmatrix} 0&0&0\\0&0&1\\0&1&0 \end{pmatrix}, \\
\lambda_{7} &= \begin{pmatrix} 0&0&0\\0&0&-i\\0&i&0 \end{pmatrix}, &
\lambda_{8} &= \tfrac{1}{\sqrt{3}}\!\begin{pmatrix} 1&0&0\\0&1&0\\0&0&-2 \end{pmatrix}.
\end{aligned}
$$

The normalisation chosen above is
$\mathrm{Tr}(\lambda_{a} \lambda_{b}) = 2 \delta_{ab}$, equivalently
$\mathrm{Tr}(T_{a} T_{b}) = \tfrac{1}{2} \delta_{ab}$. The structure constants
$f_{abc}$ are defined by $[T_{a}, T_{b}] = i f_{abc} T_{c}$ and tabulated, for
the Gell-Mann basis, with the non-zero independent entries:
$f_{123} = 1$,
$f_{147} = f_{246} = f_{257} = f_{345} = 1/2$,
$f_{156} = f_{367} = -1/2$,
$f_{458} = f_{678} = \sqrt{3}/2$ (and antisymmetric permutations).

The totally symmetric coefficients $d_{abc}$ (which appear in the anticommutator
$\{T_{a}, T_{b}\} = (1/3)\delta_{ab} \mathbf{1} + d_{abc} T_{c}$) are
non-zero for SU(3) (unlike SU(2)) and play a role only in the $A^{3}$ vertices
of the action; they do not enter the Wilson plaquette discretisation but appear
in some Wilson flow improvement terms.

### 1.3 Cartan subalgebra and root system

The Cartan subalgebra of $\mathfrak{su}(3)$ is two-dimensional, spanned by
$T_{3}$ and $T_{8}$ (the two diagonal Gell-Mann matrices); equivalently, the
rank of SU(3) is $2$. Diagonalising the adjoint action of
$H = \mathrm{span}(T_{3}, T_{8})$ on the remaining six generators yields the
root vectors. In the orthonormal basis $(h_{1}, h_{2})$ of the Cartan dual
(where the inner product is the Killing-form restricted to $H$), the roots
of $A_{2}$ are the six vectors

$$
   \Phi(\mathrm{SU}(3)) \;=\; \bigl\{ \pm \alpha_{1},\, \pm \alpha_{2},\,
     \pm (\alpha_{1} + \alpha_{2}) \bigr\},
$$

with simple roots $\alpha_{1} = (1, 0)$ and $\alpha_{2} = (-1/2, \sqrt{3}/2)$
(angle $120^{\circ}$ between them). The set of **positive roots** is the
half-system

$$
   \Phi^{+}(\mathrm{SU}(3)) \;=\; \{ \alpha_{1},\, \alpha_{2},\,
     \alpha_{1} + \alpha_{2} \},
   \qquad |\Phi^{+}(\mathrm{SU}(3))| = 3.
$$

For comparison: $\mathrm{SU}(2) = A_{1}$ has $|\Phi^{+}| = 1$; the general
formula for $A_{N-1} = \mathrm{SU}(N)$ is $|\Phi^{+}(A_{N-1})| = N(N-1)/2$,
which gives $1, 3, 6, 10$ for $N = 2, 3, 4, 5$.

The framework prediction is therefore

$$
   \kappa(\mathrm{SU}(N)) \;=\; \frac{1}{2 \cdot N(N-1)/2} \;=\; \frac{1}{N(N-1)}.
$$

This recovers $\kappa(\mathrm{SU}(2)) = 1/2$ and predicts $\kappa(\mathrm{SU}(3))
= 1/6$, $\kappa(\mathrm{SU}(4)) = 1/12$, $\kappa(\mathrm{SU}(5)) = 1/20$, etc.

### 1.4 Killing form, structure constants, Casimirs

The Killing form, normalised so that
$\mathrm{Tr}_{\mathrm{adj}}(T_{a} T_{b}) = 2 N \delta_{ab}$ for $\mathrm{SU}(N)$
fundamental generators, gives the quadratic Casimir of the fundamental
representation as
$C_{2}(\mathrm{fund}) = (N^{2} - 1)/(2N)$. For SU(3): $C_{2}(\mathrm{fund})
= 4/3$ (vs $3/4$ for SU(2)). The adjoint Casimir is $C_{2}(\mathrm{adj}) = N$:
$3$ for SU(3) (vs $2$ for SU(2)). These quantities will appear in the clover
sign-conventions of $T^{00}$ in section 6.

### 1.5 Representations and dimensions

The relevant representations for our purposes are:

  - the **fundamental** $\mathbf{3}$ (column vectors of $\mathbb{C}^{3}$),
    dimension $3$;
  - the **conjugate** $\overline{\mathbf{3}}$ (complex-conjugate of the
    fundamental), dimension $3$, distinct from $\mathbf{3}$ for SU(3)
    (unlike SU(2), where $\mathbf{2} \cong \overline{\mathbf{2}}$);
  - the **adjoint** $\mathbf{8}$, dimension $\dim \mathrm{SU}(3) = 8$.

The Wilson action only requires the fundamental representation. The adjoint
appears implicitly in $T^{00}$ via the squared field strength
$F_{\mu\nu}^{a} F_{\mu\nu}^{a}$ where $a$ runs over the adjoint $8$.

---

## 2. SU(3) primitives in JAX

### 2.1 Haar-distributed SU(3) sampling — Method 1: Cabibbo--Marinari

This method writes a random SU(3) matrix as the product of three SU(2)
embeddings, each acting in one of the three coordinate planes of $\mathbb{C}^{3}$:

```
def random_su3_haar_CM(key, shape):
    """Cabibbo-Marinari product of three SU(2) embeddings (loop-decomposed).
    NOT recommended for batched generation: see Method 2 below."""
    # Generate three Haar-distributed SU(2) matrices per site
    key_a, key_b, key_c = random.split(key, 3)
    A_su2 = random_su2_haar(key_a, shape)       # (..., 2, 2)
    B_su2 = random_su2_haar(key_b, shape)
    C_su2 = random_su2_haar(key_c, shape)
    # Embed A in (1,2)-plane, B in (1,3)-plane, C in (2,3)-plane
    A = embed_su2_in_su3(A_su2, (0, 1))         # (..., 3, 3)
    B = embed_su2_in_su3(B_su2, (0, 2))
    C = embed_su2_in_su3(C_su2, (1, 2))
    return A @ B @ C
```

Cabibbo--Marinari proved that for an SU(N) group sampled as the product
$U = \prod_{(i,j)} R_{ij}$ with $R_{ij}$ a Haar-distributed SU(2) embedded in
the $(i,j)$ plane (running over the three planes of SU(3)), the product is
Haar-distributed on SU(3) in the **infinite-cycle limit**. For finite cycle
count, the product is approximately Haar with a bias that decays exponentially
with the number of cycles. For initial-configuration sampling at the start of
thermalisation, this bias is irrelevant; for proposal generation in an
already-thermalised ensemble, it is also irrelevant (we never use Cabibbo--Marinari
sampling for proposals — see §2.2 below).

The helper `embed_su2_in_su3(U, (i, j))` inserts the $2\times 2$ SU(2) matrix
$U$ in the $(i, j)$-block of the $3 \times 3$ identity:

```
def embed_su2_in_su3(U_su2, plane):
    """Embed a (..., 2, 2) SU(2) block in the (i,j) plane of (..., 3, 3) SU(3)."""
    i, j = plane
    out = jnp.broadcast_to(jnp.eye(3, dtype=U_su2.dtype),
                           U_su2.shape[:-2] + (3, 3)).copy()
    # Build the embedding using fancy indexing
    idx = jnp.array([i, j])
    out = out.at[..., idx[:, None], idx[None, :]].set(U_su2)
    return out
```

In practice, JAX prefers a more explicit pure-functional form using
`jnp.where` masks; the spirit is identical.

### 2.2 Haar SU(3) sampling — Method 2: QR decomposition (recommended)

Method 2 is fully vectorised, free of cycle-bias, and the standard JAX idiom:

```
def random_su3_haar(key, shape):
    """Haar-distributed SU(3) sampling via QR of a complex Gaussian.

    Returns (..., 3, 3) complex array on SU(3).
    """
    # 1) Sample a complex Gaussian 3x3 matrix per site
    key_r, key_i = random.split(key)
    re = random.normal(key_r, shape + (3, 3))
    im = random.normal(key_i, shape + (3, 3))
    A = re + 1j * im
    # 2) QR decomposition -> Q is U(3); apply sign correction to make it Haar
    Q, R = jnp.linalg.qr(A)
    # Diagonal phase correction: divide each column of Q by phase(R_ii) so that
    # the corrected R has positive real diagonal. This makes the resulting U(N)
    # Haar-distributed.
    diag_R = jnp.diagonal(R, axis1=-2, axis2=-1)         # (..., 3)
    phases = diag_R / jnp.abs(diag_R)                     # (..., 3)
    Q = Q * phases[..., None, :]                          # broadcast over rows
    # 3) Project U(3) -> SU(3): divide by det^{1/3}
    det_Q = jnp.linalg.det(Q)                             # (..., )
    det_phase_cuberoot = det_Q ** (1.0 / 3.0)
    Q = Q / det_phase_cuberoot[..., None, None]
    return Q
```

This is mathematically the standard Mezzadri 2007 recipe
(arXiv:math-ph/0609050, Notices AMS **54**, 592). The QR decomposition gives
$U(N)$; the diagonal-phase correction restores Haar measure on $U(N)$ (without
this step the columns are biased by the sign convention of the LAPACK QR);
the final $\det^{-1/N}$ projects to SU(N).

**Performance comparison** (SU(3) versus SU(2)) on a 4D lattice
$L^{4} \times 4$ links of complex 3-by-3 matrices:
SU(3) uses $9$ complex elements per link versus $4$ for SU(2), so memory is
$\approx 2.25\times$. The CM method is sequential (three SU(2) embeddings) and
uses ~3× the SU(2) compute per site; the QR method is fully batched, costs
$\sim L^{4} \times 4 \times O(N^{3}) \approx 27/8 \times$ the SU(2) Haar
sampling time but is wall-clock comparable on a GPU thanks to vectorised
LAPACK calls. For 4D Wilson sweeps, the dominant cost is the staple einsum,
not the Haar sampling.

### 2.3 Near-identity proposals for Metropolis

For Metropolis updates, we need small random perturbations of the identity that
stay in SU(3). The Lie-algebra parametrisation is the cleanest:

```
def random_su3_near_identity(key, shape, eps=0.3):
    """U = exp(i * eps * sum_a c_a T_a) with c_a ~ N(0,1).

    Returns (..., 3, 3) complex SU(3) array close to the identity.
    """
    # 1) Sample 8 i.i.d. Gaussian coefficients c_a per site
    c = random.normal(key, shape + (8,)) * eps         # (..., 8)
    # 2) Build the Hermitian generator H = sum_a c_a T_a
    #    using the eight Gell-Mann matrices T_a = lambda_a / 2
    H = jnp.einsum('...a,aij->...ij', c, GELL_MANN_T)  # (..., 3, 3)
    # 3) Exponentiate: U = exp(i H)
    #    JAX has jax.scipy.linalg.expm; eigh + diagonal exp is faster for small N
    U = expm_3x3_hermitian(H)
    return U
```

Here `GELL_MANN_T` is a `(8, 3, 3)` pre-built complex array holding the
generators $T_{a} = \lambda_{a}/2$. The helper `expm_3x3_hermitian` uses the
eigendecomposition of a Hermitian $3 \times 3$ matrix; for SU(3) lattice gauge
proposals the matrix is small and the eigendecomposition is fast on GPU.

A faster alternative used in production codes: write $U = \exp(i H)$ via
the Cayley--Hamilton trick (Morningstar--Peardon 2003, arXiv:hep-lat/0311018,
their stout-link smearing paper appendix). For $3 \times 3$ Hermitian, the
matrix exponential reduces to evaluating two complex coefficients
$f_{0}, f_{1}, f_{2}$ and writing $\exp(i H) = f_{0} \mathbf{1} + f_{1} H +
f_{2} H^{2}$. We will use this in the optimised production version; the
generic `expm` is fine for the first port and smoke tests.

### 2.4 Group operations

Conjugate transpose:
```
def dagger(U):
    return jnp.conjugate(jnp.swapaxes(U, -1, -2))
```

Trace (real part of plaquette trace will be the SU(3) Wilson observable):
```
def tr_real(U):
    return jnp.real(jnp.trace(U, axis1=-2, axis2=-1))
```

Both work identically for SU(2) and SU(3) since they are shape-agnostic; the
existing FAST V3 code can therefore reuse them unchanged.

### 2.5 Pre-built Gell-Mann tensor

For the near-identity proposal, the 8 Gell-Mann matrices are pre-computed and
stored as a (8, 3, 3) complex JAX array:

```
def build_gell_mann_T():
    """Pre-compute the 8 SU(3) generators T_a = lambda_a / 2.

    Returns a (8, 3, 3) complex JAX array.
    """
    L = jnp.zeros((8, 3, 3), dtype=jnp.complex128)
    # lambda_1
    L = L.at[0, 0, 1].set(1.0).at[0, 1, 0].set(1.0)
    # lambda_2
    L = L.at[1, 0, 1].set(-1j).at[1, 1, 0].set(1j)
    # lambda_3
    L = L.at[2, 0, 0].set(1.0).at[2, 1, 1].set(-1.0)
    # lambda_4
    L = L.at[3, 0, 2].set(1.0).at[3, 2, 0].set(1.0)
    # lambda_5
    L = L.at[4, 0, 2].set(-1j).at[4, 2, 0].set(1j)
    # lambda_6
    L = L.at[5, 1, 2].set(1.0).at[5, 2, 1].set(1.0)
    # lambda_7
    L = L.at[6, 1, 2].set(-1j).at[6, 2, 1].set(1j)
    # lambda_8 (1/sqrt(3))
    inv_sqrt3 = 1.0 / jnp.sqrt(3.0)
    L = L.at[7, 0, 0].set(inv_sqrt3).at[7, 1, 1].set(inv_sqrt3)\
                    .at[7, 2, 2].set(-2.0 * inv_sqrt3)
    return 0.5 * L  # T_a = lambda_a / 2
```

### 2.6 Memory and compute footprint vs SU(2)

A 4D lattice of side $L$ with $4$ link directions:

  - SU(2) link storage: $4 L^{4} \times (2 \times 2 \times 2)$ float64
    $= 128 L^{4}$ bytes.
  - SU(3) link storage: $4 L^{4} \times (3 \times 3 \times 2)$ float64
    $= 288 L^{4}$ bytes.
  - Ratio: $2.25\times$ memory.

For typical sweep compute (einsums with $N \times N$ matrices), the cost is
$O(N^{3})$, hence $(3/2)^{3} = 3.375\times$ for the matmul itself, but the
einsum-overhead and the increased per-staple computation (still 6 plaquettes,
each with 3 SU(3) multiplications) yield empirically a $5$--$10\times$
slowdown for an SU(3) Wilson sweep relative to SU(2). We budget $10\times$ in
section 7 for conservatism.

---

## 3. Wilson action for SU(3)

The Wilson action on a 4D periodic lattice is, for any SU(N),

$$
   S_{W}[U] \;=\; \beta \,\sum_{x}\sum_{\mu < \nu}
       \Bigl[ 1 - \tfrac{1}{N}\, \Re\,\Tr\, U_{\mu\nu}(x) \Bigr],
   \qquad U_{\mu\nu}(x) = U_{\mu}(x) U_{\nu}(x+\hat\mu)
                          U_{\mu}^{\dagger}(x+\hat\nu) U_{\nu}^{\dagger}(x).
$$

For SU(2) we have $\beta = 4/g^{2}$ (using
$\beta_{\mathrm{SU}(N)} = 2 N / g^{2}$ in the standard convention). For SU(3),
$\beta = 6/g^{2}$. Equivalently the 't Hooft coupling is
$\lambda = g^{2} N = 6 N / \beta$, which for SU(3) gives $\lambda = 18/\beta$;
fixed-$\lambda$ scaling between groups requires $\beta(N)/N^{2} = \mathrm{const}$.

Standard reference values for SU(3) lattice physics:

  - $\beta = 5.7$: lattice spacing $a \approx 0.17 \mathrm{fm}$ (coarse, used
    for early thermodynamics studies).
  - $\beta = 6.0$: lattice spacing $a \approx 0.094 \mathrm{fm}$ (workhorse,
    used by Rabenstein 2019).
  - $\beta = 6.2$--$6.5$: scaling window for state-of-the-art SU(3)
    spectroscopy.

**Our choice**: $\beta = 6.0$, which is the SU(3) analog of $\beta_{\mathrm{SU}(2)}
= 2.4$ used in the FAST V3 SU(2) campaign. At fixed 't Hooft coupling
$\lambda = g^{2} N$ this corresponds to $\lambda(\mathrm{SU}(3)) = 3.0$ vs
$\lambda(\mathrm{SU}(2)) = 1.67$ at $\beta_{\mathrm{SU}(2)} = 2.4$, so they
are not at identical $\lambda$; however, the universal-coefficient extraction
$\kappa(\mathrm{SU}(N))$ is **dimensionless** and only weakly depends on $\beta$
once the scaling window is reached (BP cancellation in the SU(2) β-scan
showed $c_{3D}(\beta)$ varies by $\le 24\%$ from $\beta = 2.3$ to $2.6$).

```
@jit
def wilson_action_su3(U, beta):
    """Wilson plaquette action for SU(3): beta * sum_p (1 - (1/3) Re Tr U_p).
    U shape: (L, L, L, L, 4, 3, 3) complex.
    """
    total = 0.0
    for mu in range(4):
        for nu in range(mu + 1, 4):
            U_mu = U[..., mu, :, :]
            U_nu = U[..., nu, :, :]
            U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
            U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
            P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 3.0
            total += jnp.sum(1.0 - tr_real)
    return beta * total
```

The only difference from the SU(2) FAST V3 code is the normalisation
`/3.0` instead of `/2.0` (the $1/N$ in the action). All einsum patterns are
unchanged; JAX broadcasts correctly because the last two axes have shape $3$
rather than $2$.

---

## 4. SU(3) Cabibbo--Marinari heatbath

For pure Metropolis on SU(3), the acceptance rate at $\beta \sim 6.0$ with
$\varepsilon = 0.3$ (Gaussian width on the 8 generators) is approximately
$30$--$50\%$; this is inefficient compared to the $\sim 75\%$ rate of SU(2) at
$\beta = 2.4$. The Cabibbo--Marinari trick recovers an effective $\sim 100\%$
acceptance by leveraging an exact SU(2) heatbath in each of the three
SU(2) subgroups of SU(3).

### 4.1 The three SU(2) subgroups

Inside SU(3), an SU(2) subgroup can be embedded in three distinct ways,
corresponding to a choice of two basis vectors of $\mathbb{C}^{3}$:

  - $H_{(1,2)}$: rotations in the $(e_{1}, e_{2})$ plane, with $e_{3}$ fixed.
    Matrices have the form
    $\mathrm{diag}\bigl(R_{2\times2},\, 1\bigr)$ with $R_{2\times2} \in \mathrm{SU}(2)$.
  - $H_{(1,3)}$: rotations in the $(e_{1}, e_{3})$ plane, with $e_{2}$ fixed.
  - $H_{(2,3)}$: rotations in the $(e_{2}, e_{3})$ plane, with $e_{1}$ fixed.

Each $H_{(i,j)}$ is isomorphic to SU(2), and together the three cover SU(3) (in
the topological sense: any SU(3) element can be reached by a finite product of
matrices from the three subgroups). This is the algebraic content of the
Cabibbo--Marinari decomposition.

### 4.2 Subgroup heatbath update of an SU(3) link

For a link $U_{\mu}(x) \in \mathrm{SU}(3)$ at site $x$ in direction $\mu$, let
$K = \sum_{\nu \neq \mu} (\text{staple sum})$ be the standard sum of $3\times 3$
staples (computed identically to SU(2), with einsums on $3 \times 3$
matrices). The local action contribution is
$S_{\mathrm{loc}} = -\tfrac{\beta}{N}\,\Re\,\Tr (U_{\mu}(x)\, K^{\dagger}) =
-\tfrac{\beta}{3}\,\Re\,\Tr (U_{\mu}(x)\, K^{\dagger})$.

The Cabibbo--Marinari update applies the SU(2) heatbath to each of the three
embedded subgroups in succession:

```
def cabibbo_marinari_update_link(U_old, K, beta, key):
    """Update one SU(3) link via 3 SU(2) heatbath subgroup updates.

    U_old  : (3, 3) current link
    K      : (3, 3) staple sum (already accumulated from neighbours)
    beta   : float, gauge coupling
    key    : PRNG key
    Returns: (3, 3) new link.
    """
    U = U_old
    subgroups = [(0, 1), (0, 2), (1, 2)]    # (i, j) for the three embeddings
    for (i, j), sk in zip(subgroups, random.split(key, 3)):
        # 1) Compute the SU(2) reduced staple S_red in the (i,j) plane
        UK = U @ jnp.conjugate(jnp.swapaxes(K, -1, -2))     # U K^dagger : (3, 3)
        S_2x2 = jnp.array(
            [[UK[i, i], UK[i, j]],
             [UK[j, i], UK[j, j]]],
            dtype=UK.dtype
        )
        # 2) Symmetrise: a_block = S_2x2 + S_2x2^dagger (gives an SU(2) matrix up to
        #    a real positive scale a = sqrt(det(a_block)))
        a_block = S_2x2 + jnp.conjugate(S_2x2.T)
        a = jnp.sqrt(jnp.real(a_block[0,0]*a_block[1,1]
                              - a_block[0,1]*a_block[1,0]))
        # 3) Sample an SU(2) heatbath update X ~ exp((beta/N) * a * Re tr(X V))
        #    where V = a_block / a is the normalised SU(2) staple.
        V = a_block / a
        beta_eff = beta * a / 3.0      # SU(2) heatbath coupling at this site
        X_su2 = kennedy_pendleton_su2_heatbath(sk, beta_eff)  # (2, 2)
        # 4) New SU(2) update in (i,j) plane:
        delta_su2 = X_su2 @ jnp.conjugate(V.T)
        # 5) Embed in SU(3) and left-multiply U
        delta_su3 = embed_su2_in_su3_single(delta_su2, (i, j))
        U = delta_su3 @ U
    return U
```

For batched / vectorised lattice updates, the per-link Cabibbo--Marinari loop
is wrapped in a checkerboard scheme:

```
def cabibbo_marinari_sweep(U, beta, key, mu, L):
    """One full sweep over all SU(3) links in direction mu using CM heatbath.
    Uses a checkerboard split (even / odd sites) to allow parallel update
    without violating detailed balance.
    """
    K_all = compute_staple_sum_su3(U, mu, L)            # (L, L, L, L, 3, 3)
    for parity in (0, 1):
        mask = checkerboard_mask(L, parity)              # (L, L, L, L) bool
        key, sk = random.split(key)
        U_new_mu = jax.vmap(cabibbo_marinari_update_link)(
            U[..., mu, :, :].reshape((-1, 3, 3)),
            K_all.reshape((-1, 3, 3)),
            beta,
            random.split(sk, L**4)
        ).reshape((L, L, L, L, 3, 3))
        U_mu_updated = jnp.where(mask[..., None, None], U_new_mu, U[..., mu, :, :])
        U = U.at[..., mu, :, :].set(U_mu_updated)
    return U
```

The Kennedy--Pendleton SU(2) heatbath is a standard one-link sampler (Kennedy
& Pendleton, Phys. Lett. B **156**, 393, 1985); a pure-JAX version follows.

### 4.3 Kennedy--Pendleton SU(2) heatbath

```
def kennedy_pendleton_su2_heatbath(key, beta_eff, max_tries=20):
    """Sample x_0 in [-1, 1] from prob proportional to sqrt(1 - x_0^2) * exp(beta_eff * x_0).

    Returns an SU(2) matrix in the (a_0, a_vec) parametrisation:
       U = a_0 * I + i * sum_k a_k * sigma_k,    a_0^2 + |a_vec|^2 = 1.
    """
    # Inner accept/reject loop for x_0 = a_0 (Kennedy-Pendleton variable change)
    def body(carry, sk):
        accept, x0 = carry
        k1, k2, k3, k4 = random.split(sk, 4)
        r1 = random.uniform(k1, minval=1e-15, maxval=1.0)
        r2 = random.uniform(k2, minval=1e-15, maxval=1.0)
        r3 = random.uniform(k3, minval=1e-15, maxval=1.0)
        cos_t2 = jnp.cos(2 * jnp.pi * random.uniform(k4)) ** 2
        # delta = -(1/beta_eff) * (log(r1) + cos_t2 * log(r2))
        delta = -(jnp.log(r1) + cos_t2 * jnp.log(r2)) / beta_eff
        x0_try = 1.0 - delta
        # Test:
        accept_now = (r3 ** 2) < (1.0 - 0.5 * delta)
        return (jnp.logical_or(accept, accept_now),
                jnp.where(accept, x0, x0_try)), None
    init = (False, jnp.array(0.0))
    (accepted, x0), _ = jax.lax.scan(body, init,
                                       random.split(key, max_tries))
    # Sample the 3-vector a_vec uniformly on the sphere of radius sqrt(1 - x0^2)
    key1, key2 = random.split(key)
    cos_th = 2.0 * random.uniform(key1) - 1.0
    sin_th = jnp.sqrt(1.0 - cos_th ** 2)
    phi = 2.0 * jnp.pi * random.uniform(key2)
    a_vec = jnp.sqrt(1.0 - x0 ** 2) * jnp.array(
        [sin_th * jnp.cos(phi), sin_th * jnp.sin(phi), cos_th]
    )
    # Assemble U = a_0 I + i sum_k a_k sigma_k
    U = jnp.array(
        [[x0 + 1j * a_vec[2],  a_vec[1] + 1j * a_vec[0]],
         [-a_vec[1] + 1j * a_vec[0], x0 - 1j * a_vec[2]]],
        dtype=jnp.complex128
    )
    return U
```

The Kennedy--Pendleton sampler has acceptance close to $100\%$ in the
relevant regime ($\beta_{\mathrm{eff}} \gtrsim 1$); we add `max_tries = 20`
as a safety net. For SU(3) Wilson at $\beta = 6.0$ with typical staple
magnitudes $|a| \sim 1$, $\beta_{\mathrm{eff}} \sim 2.0$, so acceptance is
$\gtrsim 99\%$.

### 4.4 Why heatbath instead of Metropolis

Per-link Metropolis with the generator-based proposal $X = \exp(i \varepsilon
\sum_{a} c_{a} T_{a})$ at $\beta = 6.0$ and $\varepsilon = 0.3$ gives
acceptance $\sim 30$--$50\%$. To get $O(1)$ effective decorrelation per
sweep one needs $\sim 3$ Metropolis attempts per link; in contrast, one
Cabibbo--Marinari sweep (three SU(2) heatbath updates) achieves the same
decorrelation with $100\%$ acceptance and no $\varepsilon$ tuning.

Total cost ratio: a single CM sweep is $\sim 3 \times$ the cost of a single
Metropolis sweep (three subgroup updates vs one Metropolis trial), but the
effective sample rate is $3\times$ better, so they wash. The advantage is
**robustness**: no $\varepsilon$ to retune, no acceptance-tuning loop, and
exact detailed balance from the heatbath kernel.

For the SU(3) port, we use Cabibbo--Marinari heatbath in the **standard Wilson**
ensemble (used by the Modular Hamiltonian estimator). For the BP α-integration
estimator on the deformed lattice, the action sum is modified at the
A-junction; the heatbath kernel still applies but the staple sum must include
the $\alpha$-deformed plaquettes at junction-A links. We will reuse the existing
FAST V3 deformed-staple machinery, replacing the SU(2) Metropolis acceptance
inside with Cabibbo--Marinari heatbath.

---

## 5. Adapting observables — FAST V3 BP α-integration to SU(3)

### 5.1 What is identical

The BP α-integration estimator
$\partial S / \partial \alpha = \beta \sum_{p \in \text{junction-A}}
\tfrac{1}{N}\,\Re\Tr(P_{T} - P_{2T})$
is a **geometric** observable: the structure of the deformed lattice
(period $T$ in $\bar A$, period $2T$ in $A$) does not depend on $N$. All
A-mask construction, $\alpha$-grid setup, junction-link mask, and integration
formula are unchanged.

The functions
`make_next_t_arrays`, `make_prev_t_arrays`, `make_A_junction_link_mask`,
and the $\alpha$-integration loop
are reused verbatim from `jax_su2_EE_BP2008b_FAST_2026-05-25.py`.

### 5.2 What changes

  - **Plaquette normalisation**: the action involves $\Re\Tr P / N$, so the
    factor `/2` becomes `/3`. The function `alpha_observable` is updated:

```
@partial(jit, static_argnames=('L_x', 'L_y', 'L_z', 'T_half'))
def alpha_observable_su3(U, beta, L_x, L_y, L_z, T_half, A_spatial_mask):
    """Sum_{A-junction plaquettes} (tr_T - tr_2T)/3 * beta.

    Same structure as SU(2) version, but Tr / 3 instead of Tr / 2.
    """
    # ... identical mask construction ...
    nu = 3
    U_nu = U[..., nu, :, :]
    total = 0.0
    for mu in range(3):
        U_mu = U[..., mu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
        U_mu_at_nextT = gather_link_at_t(U_mu, next_t_T)
        U_mu_at_next2T = gather_link_at_t(U_mu, next_t_2T)
        P_T = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                          U_mu, U_nu_pmu,
                          jnp.conjugate(U_mu_at_nextT),
                          jnp.conjugate(U_nu))
        tr_T = jnp.real(jnp.trace(P_T, axis1=-2, axis2=-1)) / 3.0   # SU(3): /3
        P_2T = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                          U_mu, U_nu_pmu,
                          jnp.conjugate(U_mu_at_next2T),
                          jnp.conjugate(U_nu))
        tr_2T = jnp.real(jnp.trace(P_2T, axis1=-2, axis2=-1)) / 3.0
        total += jnp.sum((tr_T - tr_2T) * mask_A_junction)
    return (beta / 3.0) * total      # SU(3): beta/N = beta/3
```

  - **Staple einsums**: identical pattern, the last-two-axis shape changes
    from $(2,2)$ to $(3,3)$ and JAX handles it transparently.

  - **Metropolis acceptance test**: in
    `metropolis_sweep_perlink_local`, the local $\Delta S$ formula
    $\Delta S = -\tfrac{\beta}{N} \Re\Tr ((U_{\mathrm{new}} - U_{\mathrm{old}})
    K^{\dagger})$ uses `0.5` for SU(2) (since $1/N = 1/2$) and becomes
    `1.0/3.0` for SU(3). We replace the proposal `random_su2_near_identity`
    with `random_su3_near_identity` (§2.3).

  - **Optional**: replace per-link Metropolis with Cabibbo--Marinari heatbath
    (§4) for $\sim 2$--$3\times$ speedup in effective decorrelation. For
    the first SU(3) port we keep Metropolis (simpler, easier to debug); the CM
    upgrade is a follow-on optimisation.

### 5.3 Expected output

The SU(3) BP α-integration estimator returns a sub-leading $c$ coefficient
analogous to the SU(2) one. Rabenstein 2019 (arXiv:1812.04279) reports for
SU(3) at $\beta = 6.0$, $L = 16$, the entropic $C$-function approaches
$\sim 0.173 \pm 0.005$ in the small-$l$ regime (their Fig. 4 and §IV; cross-
checked against their Tables I--II). This is our **prediction target** for the
SU(3) BP estimator output: at $\beta = 6.0$ and $L = 12$ the value should be
within $\sim 20\%$ of $0.173$ (finite-size effects), confirming the estimator
is correctly implemented and ruling out a sign error or normalisation mistake.

### 5.4 Compute cost

The dominant cost is the per-link einsum, which scales as $O(N^{3})$ per
link and per sweep, plus the per-link Metropolis acceptance which scales as
$O(N^{2})$. The SU(2) FAST V3 baseline on RTX 3090 GPU at $\beta = 2.4$,
$L = 12$ is approximately $30$ minutes for the full $\alpha$-integration with
$11$ $\alpha$ grid points and $\sim 30$ samples per $\alpha$. Scaling
naively by the $5$--$10\times$ SU(3) overhead, we expect $2.5$--$5$ hours per
$L = 12$ SU(3) point; we budget $5$ hours per $L$ for safety, giving a total
budget of $\sim 15$ hours for $L \in \{6, 8, 12\}$ at SU(3).

---

## 6. Adapting observables — Modular Hamiltonian to SU(3)

### 6.1 Clover field strength: identical structure

The clover construction $\widehat F_{\mu\nu}(x) = (Q_{\mu\nu} - Q_{\mu\nu}^{\dagger})/(8i)
- \tfrac{1}{N} \Tr(\cdot) \mathbf{1}$ involves the **same four oriented
plaquettes** as the SU(2) version. The only change is the traceless
projection: for SU(2) we subtracted $\tfrac{1}{2}\Tr F \cdot \mathbf{1}_{2}$;
for SU(3) we subtract $\tfrac{1}{3}\Tr F \cdot \mathbf{1}_{3}$.

```
@partial(jit, static_argnames=('mu', 'nu'))
def clover_F_munu_su3(U, mu, nu):
    """Lattice clover field strength F_{mu,nu}(x) for SU(3), all x.
    Returns (L, L, L, L, 3, 3) traceless anti-Hermitian.
    """
    U_mu = U[..., mu, :, :]
    U_nu = U[..., nu, :, :]
    # Q1 forward-forward, Q2, Q3, Q4 -- identical einsum structure to SU(2)
    # ... (copy from SU(2) MH code, replace 2x2 with 3x3 broadcasting)
    Q = Q1 + Q2 + Q3 + Q4
    Q_dag = jnp.conjugate(jnp.swapaxes(Q, -1, -2))
    F = (Q - Q_dag) / (8j)
    # Traceless projection for SU(3): subtract (1/3) Tr(F) * I_3
    tr_F = jnp.trace(F, axis1=-2, axis2=-1)
    I3 = jnp.eye(3, dtype=F.dtype)
    F = F - (1.0 / 3.0) * tr_F[..., None, None] * I3
    return F
```

### 6.2 $T^{00}$ for SU(3): adjust the $1/g^{2}$ prefactor

The energy-momentum tensor structure is identical:

$$
   T^{00}(x) \;=\; \frac{1}{g^{2}} \sum_{i=1}^{3}
       \Bigl[ \Tr_{\mathrm{fund}}\,\widehat F_{0i}(x)\widehat F_{0i}(x)
              + \tfrac{1}{2} \sum_{j > i}
                \Tr_{\mathrm{fund}}\,\widehat F_{ij}(x)\widehat F_{ij}(x) \Bigr],
$$

where the trace is on the fundamental ($3\times 3$ for SU(3)). The
normalisation $\Tr (T_{a} T_{b}) = \tfrac{1}{2}\delta_{ab}$ is identical for
both groups by construction of the Gell-Mann basis, so the coefficient
$F^{a}_{\mu\nu} F^{a,\mu\nu} = -2 \Tr_{\mathrm{fund}} F_{\mu\nu} F^{\mu\nu}$
is unchanged in form between SU(2) and SU(3) (only the dimensionality of
the trace changes, $2 \to 3$, but this is automatic in the einsum).

The prefactor $1/g^{2}$ converts to $\beta / (2N)$, i.e.

  - SU(2): $1/g^{2} = \beta/4$.
  - SU(3): $1/g^{2} = \beta/6$.

```
@jit
def energy_momentum_T00_su3(U, beta):
    """Returns (L, L, L, L) real array of T^00(x) for SU(3) lattice gauge.

    Convention: T^00 >= 0 (positive energy density).
    """
    inv_g2 = beta / 6.0     # SU(3): beta = 6/g^2
    T00 = jnp.zeros(U.shape[:4])
    # Electric: i in {1,2,3}, weight +2*inv_g2
    for i in (1, 2, 3):
        F_0i = clover_F_munu_su3(U, 0, i)
        FF = jnp.einsum('...ij,...jk->...ik', F_0i, F_0i)
        tr_FF = jnp.real(jnp.trace(FF, axis1=-2, axis2=-1))
        T00 = T00 + 2.0 * inv_g2 * tr_FF
    # Magnetic: (i,j) in {(1,2),(1,3),(2,3)}, weight +inv_g2 each
    for i, j in [(1, 2), (1, 3), (2, 3)]:
        F_ij = clover_F_munu_su3(U, i, j)
        FF = jnp.einsum('...ij,...jk->...ik', F_ij, F_ij)
        tr_FF = jnp.real(jnp.trace(FF, axis1=-2, axis2=-1))
        T00 = T00 + inv_g2 * tr_FF
    return T00
```

### 6.3 Modular Hamiltonian observable: unchanged

The Bisognano--Wichmann lattice estimator
$K_{A}^{(w)} = 2\pi \sum_{k=0}^{w-1}(k+0.5)\sum_{x_{\perp}}T^{00}(L/2-1-k, x_{\perp})$
is purely geometric and uses $T^{00}$ as a black box. The functions
`modular_hamiltonian_K`, `modular_hamiltonian_K_at_boundary`, and
`modular_hamiltonian_K_vacuum` are reused without modification (they call
`energy_momentum_T00` internally, which we have just replaced).

### 6.4 Predicted leading $\kappa$ for SU(3)

The framework prediction is

$$
   \kappa(\mathrm{SU}(3)) \;=\; \frac{1}{2 \cdot 3} \;=\; \frac{1}{6} \;\approx\; 0.1667.
$$

The fit ansatz is identical to the SU(2) case:

$$
   K_{\mathrm{diff}}(L) \;=\; \kappa \cdot L^{3} \cdot \zeta_{w}(3)
                            + C_{\mathrm{sub}} \log L + \mathrm{const},
$$

where $\zeta_{w}(3) = \sum_{k=0}^{w-1}(k+0.5)^{-3}$. We perform the same
three-parameter weighted least-squares fit
across $L \in \{8, 12, 16\}$ to extract $\kappa(\mathrm{SU}(3))$, with the
caveat that SU(3) thermalisation is slower so $L = 16$ may be replaced by
$L = 12$ if budget runs short.

### 6.5 Wilson flow improvement (optional)

For pure SU(3), the clover field strength has $O(a^{2})$ discretisation errors
that bias $T^{00}$ near the boundary. The standard remedy is **Wilson flow
smoothing** (Lüscher 2010, arXiv:1006.4518; Narayanan--Neuberger 2006,
arXiv:hep-th/0601210): apply a few steps of the Wilson flow to the gauge
configuration before computing $T^{00}$. This is optional for the first port,
mandatory if the leading-$L^{3}$ piece does not show clean scaling.

We will document the Wilson flow add-on in a follow-up if needed; the core
pipeline does not require it.

---

## 7. Compute budget

### 7.1 Lattice sizes

We use smaller lattices than SU(2) due to the $\sim 10\times$ per-sweep cost:

  - $L = 6$: $6^{4} = 1296$ sites, smoke test, $\sim 30$ minutes per
    BP α-integration point at SU(3); fits comfortably on RTX 3090 (24 GB).
  - $L = 8$: $8^{4} = 4096$ sites, scaling anchor, $\sim 2$ hours per point.
  - $L = 12$: $12^{4} = 20736$ sites, main scaling point, $\sim 5$ hours per
    point. May skip $L = 16$ for SU(3) given budget.

For the Modular Hamiltonian estimator (which uses standard Wilson, no
deformation), the cost is $\sim 1.5\times$ the corresponding $\alpha = 0$ BP
α-integration cost (since we need to thermalise the standard Wilson ensemble
and compute $T^{00}$ on it).

### 7.2 Coupling

$\beta = 6.0$ for the main run; smoke test at $\beta = 5.85$ and $\beta = 6.2$
to verify scaling-window behaviour.

### 7.3 BP α-integration budget

  - $L = 6$, $\alpha$-grid $\{0, 0.1, \dots, 1.0\}$ = 11 points,
    $n_{\mathrm{samples}} = 100$, $n_{\mathrm{decorr}} = 5$:
    $\sim 30 \text{ min}$ wall time on RTX 3090.
  - $L = 8$, 11 $\alpha$ points, $n_{\mathrm{samples}} = 80$,
    $n_{\mathrm{decorr}} = 8$: $\sim 2 \text{ h}$.
  - $L = 12$, 11 $\alpha$ points, $n_{\mathrm{samples}} = 30$,
    $n_{\mathrm{decorr}} = 15$: $\sim 5 \text{ h}$.

Total BP α-integration: $\sim 7.5$ hours (with $\sim 30\%$ safety margin, budget
$10$ hours).

### 7.4 Modular Hamiltonian budget

  - $L = 8$, $w = 2$, $n_{\mathrm{samples}} = 100$, $n_{\mathrm{decorr}} = 5$:
    $\sim 1 \text{ h}$.
  - $L = 12$, $w = 3$, $n_{\mathrm{samples}} = 50$, $n_{\mathrm{decorr}} = 8$:
    $\sim 4 \text{ h}$.
  - $L = 16$, $w = 4$, $n_{\mathrm{samples}} = 30$, $n_{\mathrm{decorr}} = 12$:
    $\sim 10 \text{ h}$ (if budget allows; otherwise skip and fit with
    $L = 8, 12$).

Total Modular Hamiltonian: $\sim 15$ hours full, $\sim 5$ hours minimal
($L = 8, 12$ only).

### 7.5 Total

Conservative estimate: $20$--$30$ GPU-h for clean $\kappa(\mathrm{SU}(3))$
extraction from both estimators on $L \in \{8, 12\}$ at $\beta = 6.0$, on a
single RTX 3090 ($\$0.155$/h Vast.AI pricing $\Rightarrow$ $\sim \$3$--$\$5$
in cloud cost).

If we extend to $L = 16$ on the Modular Hamiltonian estimator, total becomes
$\sim 35$--$40$ GPU-h ($\sim \$6$).

---

## 8. Expected scenarios

### 8.1 Scenario A — universality confirmed: $\kappa(\mathrm{SU}(3)) = 1/6$

The leading-$L^{3}$ fit yields $\kappa(\mathrm{SU}(3)) = 1/6 \pm \delta$ with
$\delta/\kappa \lesssim 0.1$. Combined with the SU(2) anchor $\kappa = 1/2$,
this provides first cross-group lattice evidence for the framework prediction
$\kappa = 1/(2|\Phi^{+}|)$.

Consequences:

  - PRL-grade letter: "Universal $1/(2|\Phi^{+}|)$ scaling of the leading
    Rényi-2 area-law coefficient in pure SU(N) Yang--Mills theory".
  - Direct support for the framework's identification of the entanglement
    coefficient with a root-system invariant of the gauge group.
  - Falsification of the rank-only hypothesis $\kappa \propto 1/\mathrm{rank}$
    (which would predict $1/4$ for SU(3) instead of $1/6$).

### 8.2 Scenario B — framework incomplete: $\kappa(\mathrm{SU}(3)) \neq 1/6$ and $\neq 1/2$

The measured value lies in some intermediate range (e.g. $\sim 0.25$). The
framework prediction is falsified at SU(3), but the SU(2) anchor remains
secure. Two follow-up directions:

  1. Re-examine the derivation of $\kappa = 1/(2|\Phi^{+}|)$ for SU(N); the
     root-counting argument may need adjustment for non-simply-laced or
     non-self-conjugate representations (though A_{N-1} is simply laced).
  2. Run SU(4) (predicted $1/12$) and SU(5) (predicted $1/20$) to bracket
     the actual scaling exponent; if SU(N) gives $\kappa \propto 1/N^{p}$
     with $p \neq 2$, this is a new empirical law.

### 8.3 Scenario C — group-independent: $\kappa(\mathrm{SU}(3)) \approx 1/2$

The leading-$L^{3}$ coefficient is the same for SU(3) as for SU(2). This
would be a SURPRISE: the BP cancellation argument plus universality of the
sub-leading $C$-function on free gluons (which depends on the
$\dim(\mathrm{adj}) = N^{2} - 1$ factor) makes a uniform $\kappa$ across
gauge groups counter-intuitive but logically possible (it would suggest a
purely topological / geometric origin for $\kappa$, independent of the
gauge-group representation content).

Consequences:

  - Framework prediction falsified.
  - New hypothesis: $\kappa$ is a fixed-point of some renormalisation flow
    insensitive to the matter content.

### 8.4 Scenario D — noise dominates

If $\delta / \kappa \gtrsim 0.5$ on the leading-$L^{3}$ coefficient, the
extraction is dominated by statistical / systematic noise. Likely
remediations:

  - Increase $n_{\mathrm{samples}}$ at $L = 12$ by $\sim 3\times$ (cost $\sim
    15$ hours additional).
  - Add Wilson flow smoothing to $T^{00}$.
  - Extend to $L = 16$ if hardware allows.
  - Cross-check against the BP α-integration estimator at SU(3).

---

## 9. Implementation timeline

### Week 1 — SU(3) primitives + Cabibbo--Marinari heatbath

  - Days 1--2: Implement `random_su3_haar` (QR method), `random_su3_near_identity`,
    `embed_su2_in_su3`, Gell-Mann tensor builder.
  - Days 3--4: Implement Wilson action and standard staple computation for SU(3).
    Smoke test: thermalise an $L = 4$ lattice and verify plaquette expectation
    value matches the literature ($\langle \Re\Tr P / 3 \rangle \approx 0.59$
    at $\beta = 6.0$).
  - Days 5--7: Implement Cabibbo--Marinari heatbath sweep (with Kennedy--Pendleton
    SU(2) sampler). Cross-check that the same plaquette expectation value is
    obtained from CM heatbath versus Metropolis.

### Week 2 — Wilson action SU(3) + smoke tests

  - Days 1--3: Validate Wilson loop scaling at $L = 8$ across $\beta \in \{5.85,
    6.0, 6.2\}$ against tabulated SU(3) values.
  - Days 4--5: Validate the clover energy density: $\langle T^{00} \rangle$ in the
    bulk should be small (vacuum-subtracted to zero by construction) and the
    fluctuations should scale as $\beta^{-1}$.
  - Days 6--7: Performance benchmarking on RTX 3090; ensure $L = 12$ sweeps fit
    in $\sim 200$ ms per sweep.

### Week 3 — BP α-integration SU(3) port

  - Days 1--3: Port `alpha_observable_su3`, deformed staple computation, and
    α-integration loop.
  - Days 4--5: Run $L = 6$ and $L = 8$ BP α-integration. Check $c_{3D}(\mathrm{SU}(3))$
    against Rabenstein 2019 expectation $\sim 0.173$.
  - Days 6--7: Run $L = 12$ BP α-integration; write preliminary draft of
    the BP α-integration section.

### Week 4 — Modular Hamiltonian SU(3) port + production runs

  - Days 1--2: Port `clover_F_munu_su3`, `energy_momentum_T00_su3`.
  - Days 3--5: Production runs at $L \in \{8, 12\}$ for Modular Hamiltonian
    estimator. Fit leading $\kappa$.
  - Days 6--7: If results are clean (Scenario A), write PRL-grade letter draft
    and submit. If Scenario B/C/D, plan follow-up.

Total: $\sim 4$ weeks calendar time, of which $\sim 20$--$30$ GPU-hours are
production compute and the rest is implementation + validation work.

---

## 10. References

All arXiv IDs below were verified against the arXiv API on 2026-05-25 (cluster
firm 732 → 733 after this session's verifications). No fabricated identifiers.

### Cabibbo--Marinari and Kennedy--Pendleton heatbath

  - N. Cabibbo and E. Marinari, *A new method for updating SU(N) matrices in
    computer simulations of gauge theories*, Phys. Lett. B **119**, 387--390
    (1982). DOI 10.1016/0370-2693(82)90696-7. Original heatbath via SU(2)
    subgroup decomposition.
  - A. D. Kennedy and B. J. Pendleton, *Improved heatbath method for Monte
    Carlo calculations in lattice gauge theories*, Phys. Lett. B **156**,
    393--399 (1985). DOI 10.1016/0370-2693(85)91632-6. The SU(2) heatbath
    sampler used inside Cabibbo--Marinari for SU(N).

### Standard SU(3) lattice texts

  - C. Gattringer and C. B. Lang, *Quantum Chromodynamics on the Lattice:
    An Introductory Presentation*, Lecture Notes in Physics **788**, Springer
    (2010). Chapters 4--7 cover SU(3) Wilson action, Cabibbo--Marinari
    heatbath, and overrelaxation.
  - H. J. Rothe, *Lattice Gauge Theories: An Introduction*, 4th edition, World
    Scientific Lecture Notes in Physics **82** (2012). Chapter 4 covers
    SU(3) Wilson action; Chapter 16 covers heatbath algorithms.

### SU(N) Rényi entanglement entropy lattice precedents

  - P. V. Buividovich and M. I. Polikarpov, *Numerical study of entanglement
    entropy in SU(2) lattice gauge theory*, Nucl. Phys. B **802**, 458--474
    (2008), arXiv:0802.4247. The α-integration estimator (SU(2) only).
  - A. Rabenstein, N. Bodendorfer, P. Buividovich, A. Schäfer, *Lattice
    study of Rényi entanglement entropy in $SU(N_c)$ lattice Yang--Mills
    theory with $N_c = 2, 3, 4$*, Phys. Rev. D **100**, 034504 (2019),
    arXiv:1812.04279. Extends the BP estimator to SU(3) and SU(4); reports
    the entropic $C$-function at small $l$ scales as $N_{c}^{2} - 1$.

### Glueball spectrum benchmarks for SU(3)

  - A. Athenodorou and M. Teper, *SU(N) gauge theories in 3+1 dimensions:
    glueball spectrum, string tensions and topology*, JHEP **12**, 082 (2021),
    arXiv:2106.00364. State-of-the-art SU(3) glueball spectroscopy; provides
    independent scale-setting and validation of our SU(3) ensembles.

### Modular Hamiltonian and Bisognano--Wichmann

  - J. J. Bisognano and E. H. Wichmann, *On the duality condition for a
    Hermitian scalar field*, J. Math. Phys. **16**, 985--1007 (1975).
  - J. J. Bisognano and E. H. Wichmann, *On the duality condition for
    quantum fields*, J. Math. Phys. **17**, 303--321 (1976).
  - H. Casini and M. Huerta, *Entanglement entropy in free quantum field
    theory*, J. Phys. A **42**, 504007 (2009), arXiv:0905.2562.
  - H. Casini, M. Huerta, R. C. Myers, *Towards a derivation of holographic
    entanglement entropy*, JHEP **05**, 036 (2011), arXiv:1102.0440.

### Lattice $T^{00}$ and energy-momentum tensor

  - M. Lüscher, *Properties and uses of the Wilson flow in lattice QCD*,
    JHEP **08**, 071 (2010), arXiv:1006.4518. Wilson flow smoothing for the
    clover energy density (optional improvement, §6.5).
  - C. Morningstar and M. Peardon, *Analytic smearing of SU(3) link
    variables in lattice QCD*, Phys. Rev. D **69**, 054501 (2004),
    arXiv:hep-lat/0311018. The Cayley--Hamilton trick for SU(3) matrix exp
    used in `random_su3_near_identity` (§2.3).

### Haar sampling for U(N) / SU(N)

  - F. Mezzadri, *How to generate random matrices from the classical compact
    groups*, Notices Amer. Math. Soc. **54**, 592--604 (2007),
    arXiv:math-ph/0609050. Standard recipe for Haar U(N) via QR with
    diagonal-phase correction, used in `random_su3_haar` (§2.2).

### Entanglement and gauge-theory subtleties

  - W. Donnelly, *Decomposition of entanglement entropy in lattice gauge
    theory*, Phys. Rev. D **85**, 085004 (2012), arXiv:1109.0036. Discusses
    edge-mode / extended Hilbert space contributions; relevant to vacuum
    subtraction in the Modular Hamiltonian estimator.
  - W. Donnelly and A. Wall, *Entanglement entropy of electromagnetic edge
    modes*, Phys. Rev. Lett. **114**, 111603 (2015), arXiv:1412.1895.
  - S. Ghosh, R. M. Soni, S. P. Trivedi, *On the entanglement entropy for
    gauge theories*, JHEP **09**, 069 (2015), arXiv:1501.02593.

---

## Brief 200-word summary

This document specifies the SU(3) port of the FAST V3 BP α-integration
estimator and the Modular Hamiltonian estimator for lattice Rényi-2
entanglement entropy in pure Yang--Mills theory. The mission is to test the
framework prediction $\kappa(\mathrm{SU}(N)) = 1/(2|\Phi^{+}|)$, namely
$\kappa(\mathrm{SU}(3)) = 1/6$ versus the SU(2) anchor $\kappa = 1/2$.

The port has three components: (i) SU(3) primitives in JAX, including
Haar sampling via QR-with-phase-correction, near-identity proposals via
Gell-Mann generator exponentiation, and Cabibbo--Marinari heatbath updates
with Kennedy--Pendleton SU(2) subgroup sampling for $\sim 100\%$ acceptance;
(ii) Wilson action and standard staple computation with $1/3$ normalisation;
(iii) clover field strength, $T^{00}$, and the same boost-kernel observable
$K_{A}^{(w)} = 2\pi \sum_{k} (k+\tfrac{1}{2}) \sum_{x_{\perp}} T^{00}$.

Compute budget: $20$--$30$ GPU-hours on RTX 3090 for $L \in \{8, 12\}$ at
$\beta = 6.0$, with cross-validation against Rabenstein 2019's reported
SU(3) C-function $\sim 0.173 \pm 0.005$. Four scenarios are mapped: A confirms
universality, B falsifies the specific exponent but preserves group-dependence,
C suggests $\kappa$ is group-independent, D is noise-dominated and triggers
remediation. Implementation timeline is 4 weeks calendar.

All arXiv IDs in the reference list have been verified against the arXiv API.
