#!/usr/bin/env bash
# TIER 1 batch master — calculs Clay-grade sur GPU libéré
# RUN sur PC gamer : RTX 5060 Ti 16GB
# Note : RAG service STOPPED — restart à la fin pour Kevin

set -e
mkdir -p /tmp/tier1_results
cd /tmp/tier1_results

LOG=/tmp/tier1_results/master.log
exec > >(tee -a "$LOG") 2>&1

echo "================================================================================"
echo "TIER 1 BATCH MASTER — Clay-grade calcs"
echo "Start: $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"
echo "GPU free: $(nvidia-smi --query-gpu=memory.free --format=csv,noheader)"
echo "================================================================================"

# -----------------------------------------------------------------------------
# PHASE A : Kolmogorov L=12 → L=6 (extension précision Conjecture C*)
# -----------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "PHASE A : Kolmogorov L=12 → L=6 β=10 (extension précision)"
echo "$(date) — ETA ~45 min"
echo "================================================================================"

cat > /tmp/tier1_results/kolmogorov_L12.py << 'PYEOF'
import sys, os, time, json
import numpy as np
import cupy as cp
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspaces/vast"))
from su2_hmc_v3 import SU2HMC, random_su2, su2_mul, su2_dagger, project_su2

def block_spin_links(U_fine_flat, L_fine, ndim=4):
    L_coarse = L_fine // 2
    V_fine = L_fine ** ndim
    V_coarse = L_coarse ** ndim
    def fine_idx(x0, x1, x2, x3):
        return ((x0 * L_fine + x1) * L_fine + x2) * L_fine + x3
    def coarse_idx(X0, X1, X2, X3):
        return ((X0 * L_coarse + X1) * L_coarse + X2) * L_coarse + X3
    U_coarse = cp.zeros((ndim * V_coarse, 2, 2), dtype=U_fine_flat.dtype)
    for mu in range(ndim):
        for X0 in range(L_coarse):
            for X1 in range(L_coarse):
                for X2 in range(L_coarse):
                    for X3 in range(L_coarse):
                        x0, x1, x2, x3 = 2*X0, 2*X1, 2*X2, 2*X3
                        f1 = fine_idx(x0, x1, x2, x3)
                        xs = [x0, x1, x2, x3]
                        xs[mu] = (xs[mu] + 1) % L_fine
                        f2 = fine_idx(xs[0], xs[1], xs[2], xs[3])
                        U1 = U_fine_flat[mu * V_fine + f1]
                        U2 = U_fine_flat[mu * V_fine + f2]
                        Uprod = su2_mul(U1[None, ...], U2[None, ...])[0]
                        Uprod = project_su2(Uprod)
                        c_site = coarse_idx(X0, X1, X2, X3)
                        U_coarse[mu * V_coarse + c_site] = Uprod
    return U_coarse

def compute_plaquette_field_4D(hmc):
    L = hmc.L; V = hmc.volume; ndim = hmc.ndim
    sites = cp.arange(V, dtype=cp.int32)
    P_field = cp.zeros(V, dtype=cp.float32); n_pairs = 0
    for mu in range(ndim):
        for nu in range(mu+1, ndim):
            x_mu = hmc.nbr[mu, 0, sites]
            x_nu = hmc.nbr[nu, 0, sites]
            P = su2_mul(hmc.U[mu*V + sites], hmc.U[nu*V + x_mu])
            P = su2_mul(P, su2_dagger(hmc.U[mu*V + x_nu]))
            P = su2_mul(P, su2_dagger(hmc.U[nu*V + sites]))
            P_field += 0.5 * (P[..., 0, 0].real + P[..., 1, 1].real)
            n_pairs += 1
    P_field /= n_pairs
    return cp.asnumpy(P_field).reshape((L,)*ndim)

def C_LSI_proper(P_all):
    P_all = np.asarray(P_all)
    mean_P = np.mean(P_all)
    f = (P_all - mean_P) ** 2
    f2 = f.flatten() ** 2 + 1e-12
    E_f2 = np.mean(f2)
    ent = np.mean(f2 * np.log(f2)) - E_f2 * np.log(E_f2)
    grad_sq = 0.0
    for axis in range(1, P_all.ndim):
        f_shift = np.roll(f, -1, axis=axis)
        grad_sq += np.mean((f_shift - f) ** 2)
    return float(ent / (2 * grad_sq)) if grad_sq > 0 else None

def run_hmc(L, beta, n_therm, n_meas, n_steps=30, tau=1.0, do_blockspin=False, seed_offset=0):
    cp.random.seed(2026 + seed_offset)
    hmc = SU2HMC(L, beta, nsteps=n_steps, tau=tau)
    print(f"  Therm L={L} ({n_therm})...", flush=True)
    t0 = time.time()
    for i in range(n_therm):
        hmc.hmc_step()
    print(f"    done {time.time()-t0:.0f}s <P>={hmc.compute_plaquette():.4f}", flush=True)
    P_f = []; P_b = []
    for i in range(n_meas):
        for _ in range(3): hmc.hmc_step()
        P_f.append(compute_plaquette_field_4D(hmc))
        if do_blockspin:
            U_c = block_spin_links(hmc.U, L)
            hc = SU2HMC(L//2, beta, nsteps=n_steps, tau=tau)
            hc.U = U_c
            P_b.append(compute_plaquette_field_4D(hc))
        if (i+1) % 10 == 0:
            extra = f" <P_b>={float(np.mean(P_b[-1])):.4f}" if do_blockspin else ""
            print(f"    meas {i+1}/{n_meas}: <P>={float(np.mean(P_f[-1])):.4f}{extra}", flush=True)
    return P_f, P_b

BETA = 10.0
print(f"Phase A — Kolmogorov L=12→L=6 β={BETA}")
print(f"[1/2] HMC fine L=12...")
P_fine, P_block = run_hmc(12, BETA, 300, 50, do_blockspin=True, seed_offset=100)
print(f"[2/2] HMC direct coarse L=6...")
P_coarse, _ = run_hmc(6, BETA, 300, 50, do_blockspin=False, seed_offset=200)

C_b = C_LSI_proper(P_block); C_c = C_LSI_proper(P_coarse); C_f = C_LSI_proper(P_fine)
mP_b = float(np.mean(P_block)); mP_c = float(np.mean(P_coarse)); mP_f = float(np.mean(P_fine))
d_C = abs(C_b - C_c) / C_c * 100
d_P = abs(mP_b - mP_c) / mP_c * 100

print(f"\n=== RESULT L=12→L=6 ===")
print(f"  <P> fine={mP_f:.4f} block={mP_b:.4f} coarse={mP_c:.4f} (Δ {d_P:.2f}%)")
print(f"  C_LSI fine={C_f:.4f} block={C_b:.4f} coarse={C_c:.4f} (Δ {d_C:.2f}%)")
print(f"  Précédent L=8→L=4 Δ 10.03%. Trend ↓ ?")

with open("/tmp/tier1_results/phaseA_kolmogorov_L12.json", "w") as f:
    json.dump({
        "L_fine": 12, "L_coarse": 6, "beta": BETA, "n_meas": 50,
        "C_LSI_fine": C_f, "C_LSI_block": C_b, "C_LSI_coarse": C_c,
        "mean_P_fine": mP_f, "mean_P_block": mP_b, "mean_P_coarse": mP_c,
        "delta_CLSI_pct": d_C, "delta_meanP_pct": d_P,
        "comparison_L8_L4_delta_CLSI": 10.03,
    }, f, indent=2)
print("Saved phaseA_kolmogorov_L12.json")
PYEOF

python3 /tmp/tier1_results/kolmogorov_L12.py 2>&1 | tee /tmp/tier1_results/phaseA.log
echo "Phase A done $(date)"

# -----------------------------------------------------------------------------
# PHASE B : Wilson flow extended t∈[0, 1.0] (ancre Mosco G3)
# -----------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "PHASE B : Wilson flow extended t∈[0, 1.0] SU(2) D=4 L=8 β=10"
echo "$(date) — ETA ~20 min"
echo "================================================================================"

cd ~/.openclaw/workspaces/vast/
python3 su2_hmc_v3.py --L 8 --beta 10 --traj 100 --thermal 200 --flow 1.0 --prefix tier1_phaseB 2>&1 | tee /tmp/tier1_results/phaseB.log
# Copy result
cp /tmp/lane_outputs/vast/tier1_phaseB_L8_b10.0.json /tmp/tier1_results/phaseB_wilson_flow.json 2>/dev/null || true
echo "Phase B done $(date)"

# -----------------------------------------------------------------------------
# PHASE C : β-scan SU(2) D=4 L=8 β∈{5,20,50,100,200} (plateau large)
# -----------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "PHASE C : β-scan SU(2) D=4 L=8 β∈{5,20,50,100,200}"
echo "$(date) — ETA ~1h"
echo "================================================================================"

for BETA in 5 20 50 100 200; do
    echo "  β = $BETA"
    python3 su2_hmc_v3.py --L 8 --beta $BETA --traj 150 --thermal 200 --prefix tier1_phaseC_b${BETA} 2>&1 | tail -10
done
# Aggregate
ls /tmp/lane_outputs/vast/tier1_phaseC_*.json | head -5
cp /tmp/lane_outputs/vast/tier1_phaseC_*.json /tmp/tier1_results/ 2>/dev/null || true
echo "Phase C done $(date)"

# -----------------------------------------------------------------------------
# PHASE D : SU(2) D=4 L=16 long β=10 (Symanzik fit extrapolation L→∞)
# -----------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "PHASE D : SU(2) D=4 L=16 β=10 long (Symanzik fit extrapolation)"
echo "$(date) — ETA ~45 min"
echo "================================================================================"

python3 su2_hmc_v3.py --L 16 --beta 10 --traj 200 --thermal 300 --prefix tier1_phaseD_L16 2>&1 | tee /tmp/tier1_results/phaseD.log
cp /tmp/lane_outputs/vast/tier1_phaseD_L16_b10.0.json /tmp/tier1_results/phaseD_L16.json 2>/dev/null || true
echo "Phase D done $(date)"

# -----------------------------------------------------------------------------
# RESTART RAG SERVICE
# -----------------------------------------------------------------------------
echo ""
echo "================================================================================"
echo "RESTART rag-service-pc.service"
echo "================================================================================"
systemctl --user start rag-service-pc.service
sleep 3
systemctl --user status rag-service-pc.service --no-pager 2>&1 | head -3

echo ""
echo "================================================================================"
echo "TIER 1 BATCH DONE $(date)"
echo "Results: /tmp/tier1_results/"
ls -la /tmp/tier1_results/
echo "================================================================================"
