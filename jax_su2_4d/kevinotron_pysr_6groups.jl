#!/usr/bin/env julia
# KEVINOTRON PySR — 6 gauge groups symbolic regression
# Kévin Rémondière (ORCID 0009-0008-2443-7166)
# 46 data points, 10 features → S2/A
# 6 slope points, 8 features → S2/A/beta (Dynkin invariant)

using SymbolicRegression

println("=== KEVINOTRON PySR — 6 GAUGE GROUPS ===")
println("Julia $(VERSION)")

# Group properties: [dim, C2, lnZ, rank, n_pos_roots, root_ratio, weyl_order, d_fund]
gp = Dict(
    "SU2" => [3.0, 2.0, log(2), 1.0, 1.0, 1.0, 2.0, 2.0],
    "SU3" => [8.0, 3.0, log(3), 2.0, 3.0, 1.0, 6.0, 3.0],
    "SU4" => [15.0, 4.0, log(4), 3.0, 6.0, 1.0, 24.0, 4.0],
    "Sp4" => [10.0, 3.0, log(2), 2.0, 4.0, sqrt(2), 8.0, 4.0],
    "SO7" => [21.0, 5.0, log(2), 3.0, 9.0, sqrt(2), 48.0, 7.0],
    "G2"  => [14.0, 4.0, 0.0, 2.0, 6.0, sqrt(3), 12.0, 7.0],
)

ee_raw = [
    ("SU2",2.50,4,7.215),("SU2",2.50,6,7.165),("SU2",2.50,8,7.131),
    ("SU2",2.50,10,7.155),("SU2",2.50,12,7.134),
    ("SU3",6.06,4,14.169),("SU3",6.06,6,14.026),("SU3",6.06,8,14.033),
    ("SU3",6.06,10,14.002),("SU3",6.06,12,13.985),
    ("SU4",10.80,4,21.688),("SU4",10.80,6,21.528),("SU4",10.80,8,21.528),
    ("SU4",10.80,10,21.536),("SU4",10.80,12,21.539),
    ("G2",10.0,4,18.303),("G2",10.0,6,18.085),("G2",10.0,10,18.080),("G2",10.0,12,18.087),
    ("G2",9.6,4,15.993),("G2",9.6,6,15.673),("G2",9.6,8,15.648),
    ("G2",9.8,4,17.226),("G2",9.8,6,16.931),("G2",9.8,8,16.863),
    ("G2",10.2,4,19.213),("G2",10.2,6,19.185),("G2",10.2,8,19.242),
    ("G2",10.4,4,20.481),("G2",10.4,6,20.368),("G2",10.4,8,20.389),
    ("Sp4",8.0,4,20.674),("Sp4",8.0,6,20.617),("Sp4",8.0,8,20.566),
    ("Sp4",6.0,4,10.29),("Sp4",10.0,4,33.72),("Sp4",12.0,4,44.86),("Sp4",14.0,4,55.59),
    ("SO7",20.0,4,56.383),("SO7",20.0,6,56.105),("SO7",20.0,8,56.197),
    ("SO7",10.0,4,9.67),("SO7",15.0,4,30.18),("SO7",25.0,4,89.85),
    ("SO7",30.0,4,116.53),("SO7",40.0,4,170.06),
]

N = length(ee_raw)
println("$N data points")

# Build feature matrix X (10 x N) and target y (N)
X = zeros(Float64, 10, N)
y = zeros(Float64, N)

for (i, (grp, beta, L, s2a)) in enumerate(ee_raw)
    props = gp[grp]
    X[1,i] = beta
    X[2,i] = props[1]  # dim
    X[3,i] = props[2]  # C2
    X[4,i] = props[3]  # lnZ
    X[5,i] = props[4]  # rank
    X[6,i] = props[5]  # n_pos_roots
    X[7,i] = props[6]  # root_ratio
    X[8,i] = props[7]  # weyl_order
    X[9,i] = props[8]  # d_fund
    X[10,i] = 1.0/L^2
    y[i] = s2a
end

vnames = ["beta","dim","C2","lnZ","rank","nroots","rr","W","df","invL2"]

# ============================================================
# RUN 1: Full S2/A = f(all features)
# ============================================================
println("\n=== RUN 1: S2/A = f(beta, group_props, 1/L^2) — $N points ===")

options1 = Options(
    binary_operators=[+, -, *, /],
    unary_operators=[sqrt, log, exp],
    populations=30,
    maxsize=25,
    parsimony=0.003f0,
    adaptive_parsimony_scaling=100.0f0,
)

hof1 = equation_search(X, y;
    niterations=200,
    options=options1,
    variable_names=vnames,
    parallelism=:multithreading,
)

println("\n--- RUN 1 PARETO FRONT ---")
for (i, member) in enumerate(hof1)
    println("  c=$(member.complexity)  loss=$(round(member.loss, digits=6))  $(member.tree)")
end

# ============================================================
# RUN 2: Dynkin invariant S2/A/beta = f(group_props only)
# ============================================================
println("\n=== RUN 2: Dynkin invariant — 6 slope points ===")

slopes = [2.8585, 2.3121, 1.9938, 2.5739, 2.8075, 1.8020]
slope_names = ["SU2","SU3","SU4","Sp4","SO7","G2"]

X2 = zeros(Float64, 8, 6)
for (i, grp) in enumerate(slope_names)
    X2[:,i] .= gp[grp]
end
y2 = Float64.(slopes)

vnames2 = ["dim","C2","lnZ","rank","nroots","rr","W","df"]

options2 = Options(
    binary_operators=[+, -, *, /],
    unary_operators=[sqrt, log, exp, inv],
    populations=40,
    maxsize=20,
    parsimony=0.005f0,
)

hof2 = equation_search(X2, y2;
    niterations=500,
    options=options2,
    variable_names=vnames2,
    parallelism=:multithreading,
)

println("\n--- RUN 2 PARETO FRONT (Dynkin invariant) ---")
for (i, member) in enumerate(hof2)
    println("  c=$(member.complexity)  loss=$(round(member.loss, digits=8))  $(member.tree)")
end

println("\n=== PYSR COMPLETE ===")
