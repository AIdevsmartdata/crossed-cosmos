#!/bin/bash
# dispatch.sh
# ============================================================================
# M47 dispatcher: scp pipelines A+B to Kevin's PC gamer, verify environment,
# launch A first then B in tmux sessions.
# ----------------------------------------------------------------------------
# Sub-agent M47, 2026-05-06. Hallu count 86 -> 86.
#
# Usage:
#   ./dispatch.sh              # scp + smoke + launch A in tmux, B armed
#   ./dispatch.sh --only-scp   # just copy files, do not launch
#   ./dispatch.sh --launch-b   # assume A is done, launch B
#
# Prereqs:
#   - Tailscale up on VPS, PC gamer reachable at 100.91.123.14
#   - SSH key auth to remondiere@100.91.123.14 (NOT password)
#   - tmux installed on PC
# ============================================================================

set -euo pipefail

PC_HOST="100.91.123.14"
PC_USER="remondiere"
PC_REMOTE="${PC_USER}@${PC_HOST}"
PC_BASE="/home/remondiere/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES"
LOCAL_BASE="/root/crossed-cosmos/notes/eci_v7_aspiration/M47_PC_PIPELINES"
VENV="/home/remondiere/crossed-cosmos/.venv-mcmc-bench"

MODE="${1:---full}"

echo "[dispatch] M47 pipeline dispatcher  ($(date -Iseconds))"
echo "[dispatch] PC target:    ${PC_REMOTE}"
echo "[dispatch] Remote base:  ${PC_BASE}"
echo "[dispatch] Local base:   ${LOCAL_BASE}"
echo "[dispatch] Mode:         ${MODE}"

# ----------------------------------------------------------------------------
# Step 1: SSH connectivity check
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 1/6: SSH connectivity..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "${PC_REMOTE}" 'echo OK' 2>/dev/null | grep -q OK; then
    echo "[dispatch] ERROR: SSH to ${PC_REMOTE} failed."
    echo "[dispatch] Tailscale may be in re-auth state. Kevin must:"
    echo "  1. Open https://login.tailscale.com/a/<re-auth-URL> from PC"
    echo "  2. Re-run: sudo bash /home/remondiere/pc_calcs/tailscale_shield.sh"
    echo "  3. Re-run this dispatcher: ./dispatch.sh"
    echo ""
    echo "[dispatch] FALLBACK: see manual_launch.md for self-serve steps."
    exit 2
fi
echo "[dispatch] SSH OK"

# ----------------------------------------------------------------------------
# Step 2: SCP pipelines
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 2/6: scp pipelines..."
ssh "${PC_REMOTE}" "mkdir -p ${PC_BASE}/pipeline_a ${PC_BASE}/pipeline_b"
scp -q "${LOCAL_BASE}/SUMMARY.md"                               "${PC_REMOTE}:${PC_BASE}/" 2>/dev/null || true
scp -q "${LOCAL_BASE}/CRITICAL_UPDATE_M47.md"                   "${PC_REMOTE}:${PC_BASE}/" 2>/dev/null || true
scp -q "${LOCAL_BASE}/pipeline_a/f2_python_sweep.py"             "${PC_REMOTE}:${PC_BASE}/pipeline_a/"
scp -q "${LOCAL_BASE}/pipeline_a/f2_sage_sweep.sage"             "${PC_REMOTE}:${PC_BASE}/pipeline_a/" 2>/dev/null || true   # logic-reference only
scp -q "${LOCAL_BASE}/pipeline_a/expected_results.md"            "${PC_REMOTE}:${PC_BASE}/pipeline_a/"
scp -q "${LOCAL_BASE}/pipeline_b/v77_class_pipeline.py"          "${PC_REMOTE}:${PC_BASE}/pipeline_b/"
scp -q "${LOCAL_BASE}/pipeline_b/v77_setup_notes.md"             "${PC_REMOTE}:${PC_BASE}/pipeline_b/"
echo "[dispatch] scp OK"

if [ "${MODE}" = "--only-scp" ]; then
    echo "[dispatch] --only-scp: stopping after scp."
    exit 0
fi

# ----------------------------------------------------------------------------
# Step 3: Verify Python + sympy + requests for Pipeline A
# (Per CRITICAL_UPDATE_M47.md: NO SageMath; pure Python via LMFDB REST + sympy.)
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 3/6: verify Python + sympy on PC for Pipeline A..."
A_VENV_OK=$(ssh "${PC_REMOTE}" "source ${VENV}/bin/activate 2>/dev/null && \
    python -c 'import sympy, urllib.request, multiprocessing; \
        print(\"SYMPY_\"+sympy.__version__)' 2>/dev/null" || echo "MISS")
if [[ "${A_VENV_OK}" == SYMPY_* ]]; then
    echo "[dispatch] Pipeline A deps OK: ${A_VENV_OK}"
    A_READY=1
else
    echo "[dispatch] WARN: sympy import failed in venv. Pipeline A may not run."
    echo "[dispatch] Fix: source ${VENV}/bin/activate && pip install sympy>=1.14 requests"
    A_READY=0
fi

# ----------------------------------------------------------------------------
# Step 4: Verify pipeline B venv
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 4/6: verify pipeline B venv..."
VENV_OK=$(ssh "${PC_REMOTE}" "test -f ${VENV}/bin/activate && echo VENV_OK || echo VENV_MISS")
if [ "${VENV_OK}" != "VENV_OK" ]; then
    echo "[dispatch] ERROR: venv ${VENV} not found on PC."
    echo "[dispatch] Cannot launch pipeline B. Halting."
    exit 3
fi
ssh "${PC_REMOTE}" "source ${VENV}/bin/activate && python -c '
import jax, blackjax, cosmopower_jax
print(\"  jax:\", jax.__version__)
print(\"  blackjax:\", blackjax.__version__)
print(\"  cosmopower_jax:\", cosmopower_jax.__version__)
'" || {
    echo "[dispatch] ERROR: venv import check failed. JAX patch may not be applied."
    echo "[dispatch] Check: ${VENV}/lib/python3.11/site-packages/jax/_src/core.py line ~2445"
    exit 4
}
echo "[dispatch] venv OK"

# ----------------------------------------------------------------------------
# Step 5: Smoke-test pipeline B
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 5/6: pipeline B smoke test..."
if [ "${MODE}" != "--launch-b" ]; then
    ssh "${PC_REMOTE}" "source ${VENV}/bin/activate && \
       python ${PC_BASE}/pipeline_b/v77_class_pipeline.py --smoke 2>&1 | tail -20" || {
        echo "[dispatch] WARN: smoke test failed; check log on PC."
    }
fi

# ----------------------------------------------------------------------------
# Step 6: Launch pipelines in tmux
# ----------------------------------------------------------------------------
echo ""
echo "[dispatch] step 6/6: launching tmux sessions..."

if [ "${MODE}" = "--launch-b" ]; then
    # Skip A; user said A is done
    ssh "${PC_REMOTE}" "tmux kill-session -t v77b 2>/dev/null; \
        tmux new -d -s v77b \
          'cd ${PC_BASE}/pipeline_b && source ${VENV}/bin/activate && \
           python v77_class_pipeline.py --frontend cosmopower \
              --n_warmup 5000 --n_samples 5000 --n_chains 4 \
              2>&1 | tee v77_run_\$(date +%Y%m%d_%H%M).log'"
    echo "[dispatch] Pipeline B launched in tmux session 'v77b'."
    echo "[dispatch] Monitor: ssh ${PC_REMOTE} -t 'tmux attach -t v77b'"
    exit 0
fi

if [ "${A_READY}" = "1" ]; then
    ssh "${PC_REMOTE}" "tmux kill-session -t f2py 2>/dev/null; \
        tmux new -d -s f2py \
          'cd ${PC_BASE}/pipeline_a && \
           source ${VENV}/bin/activate && \
           python f2_python_sweep.py 2>&1 | tee f2_sweep_\$(date +%Y%m%d_%H%M).log'"
    echo "[dispatch] Pipeline A (F2 python sweep) launched in tmux session 'f2py'."
    echo "[dispatch] Expected runtime: ~15-30 min (LMFDB REST throttle)."
    echo "[dispatch] Monitor: ssh ${PC_REMOTE} -t 'tmux attach -t f2py'"
    echo "[dispatch] Output:  ${PC_BASE}/pipeline_a/f2_sweep_results.csv"
else
    echo "[dispatch] SKIP pipeline A (deps not ready). Launching B only."
fi

# Pipeline B armed but NOT auto-launched (parent brief: B after A in)
echo ""
echo "[dispatch] Pipeline B is ARMED but NOT launched automatically."
echo "[dispatch] Once F2 sweep completes (~15-30 min), launch B with:"
echo "    ${0} --launch-b"
echo ""
echo "[dispatch] DONE.  ($(date -Iseconds))"
