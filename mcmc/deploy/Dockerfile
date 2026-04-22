# ============================================================================
# ECI v4/v5 MCMC — container image for AWS spot / local docker runs
# Base: python:3.11-slim (debian bookworm)
# Target size: < 3 GB (cobaya `cosmo` likelihood data downloaded at runtime
# into /opt/eci/mcmc/packages/, NOT baked into the image).
# ============================================================================
FROM python:3.11-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=5

# --- System build deps ------------------------------------------------------
# gcc/gfortran: CLASS + Planck likelihoods require Fortran
# libgsl-dev: CLASS numerical deps
# mpich + libopenmpi-dev: MPI for cobaya-run -np 4
# libcfitsio-dev: Planck/ACT FITS I/O
# libomp-dev: OpenMP threading
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        gfortran \
        make \
        cmake \
        git \
        wget \
        ca-certificates \
        libgsl-dev \
        libcfitsio-dev \
        libomp-dev \
        mpich \
        libmpich-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# --- Python scientific stack -----------------------------------------------
# Pin numpy<2 for compatibility with legacy Planck clik / Cobaya<3.6
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir \
        "numpy<2.0" \
        "scipy>=1.11" \
        "astropy>=6.0" \
        "mpi4py>=3.1" \
        "cython<3.1" \
        "pyyaml>=6.0" \
        "pandas>=2.0"

# --- Cobaya + samplers + theory --------------------------------------------
# classy: vanilla CLASS Python wrapper (the NMC hi_class variant is bind-mounted
# at /opt/eci and installed at container runtime by run_mcmc.sh if required).
RUN pip install --no-cache-dir \
        "cobaya>=3.5" \
        "getdist>=1.5" \
        "classy" \
 && pip install --no-cache-dir --no-deps "montepython" || true

# --- Workspace --------------------------------------------------------------
# The ECI repo is bind-mounted at /opt/eci by the launch script; do not COPY
# it into the image so the image remains small and reusable.
WORKDIR /opt/eci
VOLUME ["/opt/eci"]

# Packages dir for Planck / ACT / DESI data downloaded by `cobaya-install cosmo`.
# Separate volume so data is reused across container rebuilds.
VOLUME ["/opt/eci/mcmc/packages"]

ENTRYPOINT ["bash", "/opt/eci/mcmc/deploy/run_mcmc.sh"]
