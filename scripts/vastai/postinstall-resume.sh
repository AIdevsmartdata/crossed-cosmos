#!/usr/bin/env bash
# postinstall-resume.sh — recovers from postinstall-base.sh failures encountered
# on Vast.ai 2026-05-02. Specifically:
#   - polychord-py3 does NOT exist on PyPI (set -e in base postinstall would
#     abort here; this script runs with set +e and skips it).
#   - cosmopower deps drag in tensorflow 2.13 + numpy 1.24 + jax 0.4.38, which
#     downgrade an already-set-up venv. Re-pin numpy<2 explicitly.
#   - AxiCLASS Makefile invokes `python` (not python3) and pip without
#     --no-build-isolation, so build env doesn't see Cython. Fix here.
#
# Usage: source /etc/profile.d/vastai-physics.sh
#        source ~/.venv/physics/bin/activate
#        bash postinstall-resume.sh

set +e   # do NOT abort on individual pip failures; many are optional

source /etc/profile.d/vastai-physics.sh
source /root/.venv/physics/bin/activate

echo ">> [4b/9] MCMC + nested sampling (skip polychord-py3 — does not exist on pip)"
pip install --upgrade \
    "cobaya[mcmc]" \
    dynesty nautilus-sampler ultranest \
    emcee zeus-mcmc \
    pymc pyro-ppl numpyro \
    optuna nevergrad 2>&1 | tail -5

echo ">> [5/9] Posterior analysis"
pip install --upgrade getdist anesthetic chainconsumer corner arviz 2>&1 | tail -3

echo ">> [6/9] Cosmology side libraries"
pip install --upgrade camb classy_sz cosmopower cosmopower_jax 2>&1 | tail -3

echo ">> [6b] Re-pin numpy<2 (cosmopower's tensorflow drags numpy 1.24, which is fine, but >=2 breaks classy ABI)"
pip install --upgrade --force-reinstall "numpy<2" 2>&1 | tail -2

echo ">> [7/9] Persistent homology + number theory"
pip install --upgrade gudhi ripser persim giotto-tda primesieve 2>&1 | tail -3

echo ">> [8/9] LLM/ML (skip vllm if unavailable)"
pip install --upgrade \
    transformers datasets accelerate sentencepiece tokenizers \
    "huggingface_hub[cli]" peft trl bitsandbytes safetensors einops 2>&1 | tail -3

echo ">> [9/9] Build CLASS / AxiCLASS / hi_class"
SRC_DIR="$HOME/src"
mkdir -p "$SRC_DIR"

# IMPORTANT 2026-05-02 finding: AxiCLASS 3.3.0 has an FP precision bug on Zen 3
# (EPYC 7V13) that triggers `condition (z < pba->z_table[pba->bt_size-1]) is true;
# z=0 < z_min=6.66e-16` in background_tau_of_z, even with -O0. Vanilla CLASS
# upstream 3.3.4 does not have this bug. So we install BOTH:
#   - vanilla CLASS for sanity-check / non-EDE workloads
#   - AxiCLASS source for when EDE-specific physics is needed (with patch TBD)

# Vanilla CLASS upstream (preferred default)
cd "$SRC_DIR"
[[ ! -d class_public ]] && git clone --depth 1 https://github.com/lesgourg/class_public.git
( cd class_public && make clean >/dev/null 2>&1
  make -j16 CC=gcc OPTFLAG="-O3 -fopenmp" 2>&1 | tail -3
  cd python && pip install --no-build-isolation -e . 2>&1 | tail -3 )

# AxiCLASS for EDE
cd "$SRC_DIR"
[[ ! -d AxiCLASS ]] && git clone --depth 1 https://github.com/PoulinV/AxiCLASS.git
( cd AxiCLASS && make clean >/dev/null 2>&1
  make -j16 CC=gcc OPTFLAG="-O3 -fopenmp" 2>&1 | tail -3
  # Note: don't pip install AxiCLASS by default; vanilla CLASS is preferred.
  # If you need AxiCLASS, run inside its python/ dir:
  #   pip install --no-build-isolation -e . --force-reinstall
)

# hi_class for αM/αB perturbations (Bellini-Sawicki)
cd "$SRC_DIR"
[[ ! -d hi_class_public ]] && git clone --depth 1 https://github.com/miguelzuma/hi_class_public.git
( cd hi_class_public && make clean >/dev/null 2>&1
  make -j16 CC=gcc OPTFLAG="-O3 -fopenmp" 2>&1 | tail -3 )

echo ">> install mpi4py linked to system OpenMPI (no-binary critical)"
pip install --no-binary=mpi4py mpi4py 2>&1 | tail -3

echo ""
echo "=== smoke tests ==="
python << 'PYSMOKE'
import sys
print(f"Python: {sys.version.split()[0]}")
for name, mod in [("numpy","numpy"),("scipy","scipy"),("sympy","sympy"),
                  ("mpmath","mpmath"),("jax","jax"),("torch","torch"),
                  ("classy","classy"),("cobaya","cobaya"),("anesthetic","anesthetic"),
                  ("chainconsumer","chainconsumer"),("getdist","getdist"),
                  ("camb","camb"),("gudhi","gudhi"),("mpi4py","mpi4py")]:
    try:
        m = __import__(mod)
        print(f"  {name}: {getattr(m, '__version__', '?')}")
    except Exception as e:
        print(f"  {name}: FAIL {type(e).__name__}: {str(e)[:80]}")
try:
    import jax
    print(f"  jax devices: {jax.devices()}")
except Exception:
    pass
try:
    import torch
    print(f"  torch.cuda: avail={torch.cuda.is_available()} count={torch.cuda.device_count()}")
except Exception:
    pass
try:
    import classy
    cl = classy.Class(); cl.set({"output":"mPk"}); cl.compute()
    print(f"  classy.compute() bare LCDM: OK, sigma8 = {cl.sigma8():.4f}")
except Exception as e:
    print(f"  classy.compute(): FAIL {str(e)[:120]}")
PYSMOKE
echo ""
echo "=== resume_postinstall DONE ==="
