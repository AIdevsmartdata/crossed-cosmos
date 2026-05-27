"""
test_adjoint.py — Unit tests for the adjoint representation.
Run: python3 -m pytest test_adjoint.py -v
"""
import numpy as np
import pytest
import sys
sys.path.insert(0, '/root/kevinotron')
from adjoint import adjoint_rep_batch

# ============ Generator builders ============

def build_so3_gens():
    s = 1.0/np.sqrt(2.0)
    gens = []
    for i in range(3):
        for j in range(i+1, 3):
            g = np.zeros((3,3)); g[i,j]=s; g[j,i]=-s
            gens.append(g)
    return np.array(gens)

def build_su2_gens():
    gens = []
    gens.append(np.array([[0, 0.5j],[0.5j, 0]], dtype=complex))
    gens.append(np.array([[0, 0.5],[-0.5, 0]], dtype=complex))
    gens.append(np.array([[0.5j, 0],[0, -0.5j]], dtype=complex))
    return np.array(gens)

def build_su3_gens():
    exec(open('/root/kevinotron/fp_adjoint_fast.py').read().split('configs = [')[0])
    return build_sun_generators(3)

def build_g2_gens():
    exec(open('/root/kevinotron/fp_adjoint_fast.py').read().split('configs = [')[0])
    return build_g2_generators()

def random_so(n):
    from scipy.stats import ortho_group
    return ortho_group.rvs(n)

def random_su(n):
    from scipy.stats import unitary_group
    U = unitary_group.rvs(n)
    U /= np.linalg.det(U)**(1.0/n)
    return U

# ============ Tests ============

class TestAdjointIdentity:
    """Ad(I) must equal the identity matrix."""
    
    def test_so3(self):
        gens = build_so3_gens()
        I = np.eye(3).reshape(1, 3, 3)
        Ad = adjoint_rep_batch(I, gens)
        np.testing.assert_allclose(Ad[0], np.eye(3), atol=1e-12)
    
    def test_su2(self):
        gens = build_su2_gens()
        I = np.eye(2, dtype=complex).reshape(1, 2, 2)
        Ad = adjoint_rep_batch(I, gens)
        np.testing.assert_allclose(Ad[0], np.eye(3), atol=1e-12)
    
    def test_g2(self):
        gens = build_g2_gens()
        I = np.eye(7).reshape(1, 7, 7)
        Ad = adjoint_rep_batch(I, gens)
        np.testing.assert_allclose(Ad[0], np.eye(14), atol=1e-12)


class TestAdjointHomomorphism:
    """Ad(U) @ Ad(V) = Ad(U @ V)."""
    
    def _check(self, gens, random_fn, d):
        for _ in range(5):
            U = random_fn(d)
            V = random_fn(d)
            UV = U @ V
            Ad_U = adjoint_rep_batch(U.reshape(1,d,d), gens)[0]
            Ad_V = adjoint_rep_batch(V.reshape(1,d,d), gens)[0]
            Ad_UV = adjoint_rep_batch(UV.reshape(1,d,d), gens)[0]
            np.testing.assert_allclose(Ad_U @ Ad_V, Ad_UV, atol=1e-9)
    
    def test_so3(self):
        self._check(build_so3_gens(), random_so, 3)
    
    def test_su2(self):
        self._check(build_su2_gens(), random_su, 2)


class TestAdjointOrthogonality:
    """Ad(U) must be orthogonal: Ad^T @ Ad = I."""
    
    def _check(self, gens, random_fn, d):
        for _ in range(5):
            U = random_fn(d)
            Ad = adjoint_rep_batch(U.reshape(1,d,d), gens)[0]
            np.testing.assert_allclose(Ad.T @ Ad, np.eye(len(gens)), atol=1e-9)
    
    def test_so3(self):
        self._check(build_so3_gens(), random_so, 3)
    
    def test_su2(self):
        self._check(build_su2_gens(), random_su, 2)
    
    def test_g2(self):
        self._check(build_g2_gens(), random_so, 7)


class TestBatchConsistency:
    """Batch of N links should give same result as N individual calls."""
    
    def test_batch_vs_single(self):
        gens = build_so3_gens()
        Us = np.array([random_so(3) for _ in range(10)])
        Ad_batch = adjoint_rep_batch(Us, gens)
        for i in range(10):
            Ad_single = adjoint_rep_batch(Us[i:i+1], gens)
            np.testing.assert_allclose(Ad_batch[i], Ad_single[0], atol=1e-12)


if __name__ == '__main__':
    print("Running adjoint unit tests...", flush=True)
    n_pass = 0
    n_fail = 0
    
    tests = [
        ("Ad(I)=I SO(3)", TestAdjointIdentity().test_so3),
        ("Ad(I)=I SU(2)", TestAdjointIdentity().test_su2),
        ("Ad(I)=I G2", TestAdjointIdentity().test_g2),
        ("Ad(UV)=Ad(U)Ad(V) SO(3)", TestAdjointHomomorphism().test_so3),
        ("Ad(UV)=Ad(U)Ad(V) SU(2)", TestAdjointHomomorphism().test_su2),
        ("Ad^T Ad=I SO(3)", TestAdjointOrthogonality().test_so3),
        ("Ad^T Ad=I SU(2)", TestAdjointOrthogonality().test_su2),
        ("Ad^T Ad=I G2", TestAdjointOrthogonality().test_g2),
        ("Batch consistency", TestBatchConsistency().test_batch_vs_single),
    ]
    
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS: {name}", flush=True)
            n_pass += 1
        except Exception as e:
            print(f"  FAIL: {name} — {e}", flush=True)
            n_fail += 1
    
    print(f"\n{n_pass} passed, {n_fail} failed", flush=True)
