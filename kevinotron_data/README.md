# Kevinotron v3.0

**Lattice Gauge Theory Entanglement Entropy Engine**

Unified measurement of Rényi-2 entanglement entropy, Polyakov loops, glueball correlators, topological charge, and string tension across 10 gauge groups — including the exceptional groups G₂, F₄, and E₆.

## Quick Start

\`\`\`bash
cargo build --release
./target/release/kevinotron --group su3 --ls 4 --beta 6.0 --full-ee
\`\`\`

## Gauge Groups

| Flag | Group | Type | d_fund | d_adj | h∨ | |Φ⁺| | |Z| |
|------|-------|------|--------|-------|-----|------|-----|
| u1   | U(1)  | —    | 1      | 0     | 0   | 0    | 1   |
| su2  | SU(2) | A₁   | 2      | 3     | 2   | 1    | 2   |
| su3  | SU(3) | A₂   | 3      | 8     | 3   | 3    | 3   |
| su4  | SU(4) | A₃   | 4      | 15    | 4   | 6    | 4   |
| su5  | SU(5) | A₄   | 5      | 24    | 5   | 10   | 5   |
| g2   | G₂    | G₂   | 7      | 14    | 4   | 6    | 1   |
| sp4  | Sp(4) | C₂   | 4      | 10    | 3   | 4    | 2   |
| so7  | SO(7) | B₃   | 7      | 21    | 5   | 9    | 2   |
| f4   | F₄    | F₄   | 26     | 52    | 9   | 24   | 1   |
| e6   | E₆    | E₆   | 27     | 78    | 12  | 36   | 3   |

## Modes

### Entanglement Entropy (default)
\`\`\`bash
kevinotron --group su3 --ls 8 --beta 6.06 --full-ee
kevinotron --group f4 --ls 4 --beta 30.0 --full-ee --n-alpha 11
\`\`\`

### HMC (Hybrid Monte Carlo)
\`\`\`bash
kevinotron --group su3 --ls 4 --beta 6.0 --hmc-run --hmc-dt 0.005 --hmc-steps 60 --hmc-traj 100
kevinotron --group g2 --ls 4 --beta 10.0 --hmc-run --hmc-dt 0.003 --hmc-steps 100 --hmc-traj 50
\`\`\`

### Thermal Scan (deconfinement)
\`\`\`bash
kevinotron --group su2 --ls 8 --beta 2.3 --thermal
\`\`\`

### String Tension Calibration
\`\`\`bash
kevinotron --group su3 --ls 8 --beta 6.0 --calibrate
\`\`\`

### Observables (append to --full-ee)
\`\`\`bash
--polyakov-scan     # Polyakov loop + susceptibility
--topo-charge       # Topological charge Q (clover)
--glueball          # Glueball correlators C(t) + m_eff
--fermion-check     # Wilson-Dirac γ₅-hermiticity + CG test
\`\`\`

## Validation

Cold-start validation runs automatically on every launch:
\`\`\`
# VALIDATE: cold start P=1.000000 OK
# VALIDATE: 20-sweep P=0.748 (should be < 1.0)
\`\`\`

Skip with \`--no-validate\` (not recommended).

## Key Parameters

| Flag | Default | Description |
|------|---------|-------------|
| --ls | required | Spatial lattice size L |
| --lt | 2×ls | Temporal lattice size |
| --beta | required | Inverse coupling |
| --n-therm | 500 | Thermalization sweeps |
| --n-meas | 200 | Measurement sweeps |
| --n-skip | 5 | Sweeps between measurements |
| --epsilon | 0.15 | Metropolis step size |
| --n-alpha | 11 | α-integration points for EE |
| --dump-config | false | Save config as .npy |
| --quark-mass | 0.1 | Mass for Wilson-Dirac |

## Output

- **stdout**: RESULT lines (machine-readable)
- **stderr**: Progress, validation, diagnostics
- **JSON**: Auto-saved \`{group}_ee_L{ls}_beta{beta}.json\`
- **.npy**: Config dumps for Python/JAX analysis

## Python Tools

| File | Purpose |
|------|---------|
| python/adjoint.py | Unified adjoint representation (7/7 tests) |
| python/fp_spectral.py | FP operator spectral analysis |
| python/sparse_fp.py | Sparse Lanczos for large FP matrices |
| python/test_adjoint.py | Unit tests for adjoint |

## Architecture

\`\`\`
src/
├── main.rs          # CLI + orchestration
├── lattice.rs       # Lattice4D, Metropolis sweeps
├── fermion.rs       # Wilson-Dirac operator
├── solver.rs        # CG solver (D†D x = b)
├── hmc.rs           # Hybrid Monte Carlo
├── thermal.rs       # Finite temperature scan
├── io.rs            # .npy + JSON output
├── groups/          # 10 gauge groups
│   ├── mod.rs       # GaugeGroup trait
│   ├── su2..su5.rs  # SU(N)
│   ├── g2.rs        # G₂ = Aut(O)
│   ├── sp4.rs       # Sp(4)
│   ├── so7.rs       # SO(7)
│   ├── f4.rs        # F₄ = Der(J₃(O))
│   └── e6.rs        # E₆ = Str₀(J₃(O_C))
└── observables/
    ├── wilson.rs    # Wilson loops
    ├── creutz.rs    # Creutz ratios → σa²
    ├── polyakov.rs  # Polyakov loop
    ├── glueball.rs  # Glueball correlators + APE smearing
    ├── topology.rs  # Topological charge (clover)
    └── scale.rs     # Static potential
\`\`\`

## References

- F₄ generators: derivations of the exceptional Jordan algebra J₃(O)
- E₆ generators: reduced structure algebra Str₀(J₃(O_C))
- EE method: Buividovich-Polikarpov α-integration (arXiv:0802.4247)
- Wilson-Dirac: Gattringer-Lang convention (γ₅ = γ₁γ₂γ₃γ₄)

## Author

Kévin Rémondière (ORCID: 0009-0008-2443-7166)
Independent Researcher, Oloron-Sainte-Marie, France

## License

CC-BY-4.0
