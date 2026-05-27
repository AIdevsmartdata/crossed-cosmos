using SymbolicRegression

println("=== MEGA PySR: SCREENING LAW slope = f(Lie algebra) ===")

# 8 groups: slope S₂/A/β measured at large β
# U(1) at β=5 (not fully asymptotic, correct with -1/(β-1) = -0.25)
slopes = Float64[5.31, 2.86, 2.31, 1.99, 1.43, 1.80, 2.57, 2.81]
names = ["U1", "SU2", "SU3", "SU4", "SU5", "G2", "Sp4", "SO7"]

# Features: [dim_adj, C2, lnZ, rank, n_pos_roots, root_ratio, |W|, d_fund]
X = Float64[
    1   0  0.0     0  0   1.0      1   1;   # U(1)
    3   2  log(2)  1  1   1.0      2   2;   # SU(2)
    8   3  log(3)  2  3   1.0      6   3;   # SU(3)
   15   4  log(4)  3  6   1.0     24   4;   # SU(4)
   24   5  log(5)  4  10  1.0    120   5;   # SU(5)
   14   4  0.0     2  6   sqrt(3) 12   7;   # G₂
   10   3  log(2)  2  4   sqrt(2)  8   4;   # Sp(4)
   21   5  log(2)  3  9   sqrt(2) 48   7;   # SO(7)
]

println("8 data points:")
for i in 1:8
    println("  $(names[i]): slope=$(slopes[i]), |Φ⁺|=$(Int(X[i,5])), C₂=$(Int(X[i,2]))")
end

# Run 1: Full search
println("\n=== RUN 1: slope = f(all features), 8 points ===")
options1 = Options(
    binary_operators=[+, -, *, /],
    unary_operators=[sqrt, log, exp, inv],
    populations=80,
    maxsize=18,
    parsimony=0.005f0,
)

hof1 = equation_search(permutedims(X), slopes;
    niterations=500,
    options=options1,
    variable_names=["dim","C2","lnZ","rank","nroots","rr","W","df"],
    parallelism=:multithreading,
)

println("\n--- RUN 1 PARETO FRONT ---")
for member in hof1
    println("  c=$(member.complexity) loss=$(round(member.loss, digits=6)) $(member.tree)")
end

# Run 2: Just slope vs |Φ⁺| (the dominant variable)
println("\n=== RUN 2: slope = f(|Φ⁺|) only ===")
X2 = reshape(Float64[0, 1, 3, 6, 10, 6, 4, 9], 1, 8)

options2 = Options(
    binary_operators=[+, -, *, /],
    unary_operators=[sqrt, log, exp, inv],
    populations=60,
    maxsize=15,
    parsimony=0.003f0,
)

hof2 = equation_search(X2, slopes;
    niterations=500,
    options=options2,
    variable_names=["nroots"],
    parallelism=:multithreading,
)

println("\n--- RUN 2 PARETO FRONT (slope vs |Φ⁺| only) ---")
for member in hof2
    println("  c=$(member.complexity) loss=$(round(member.loss, digits=6)) $(member.tree)")
end

# Run 3: slope vs (|Φ⁺|, root_ratio) — the two structural variables
println("\n=== RUN 3: slope = f(|Φ⁺|, rr) ===")
X3 = Float64[0 1 3 6 10 6 4 9; 1.0 1.0 1.0 1.0 1.0 sqrt(3) sqrt(2) sqrt(2)]

hof3 = equation_search(X3, slopes;
    niterations=500,
    options=options2,
    variable_names=["nroots", "rr"],
    parallelism=:multithreading,
)

println("\n--- RUN 3 PARETO FRONT (slope vs |Φ⁺| + rr) ---")
for member in hof3
    println("  c=$(member.complexity) loss=$(round(member.loss, digits=6)) $(member.tree)")
end

println("\n=== DONE ===")
