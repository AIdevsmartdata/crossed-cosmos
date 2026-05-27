#!/usr/bin/env julia
"""
kevinotron_pysr.jl -- Pure Julia PySR for Kevinotron EE data
============================================================
Direct Julia interface to SymbolicRegression.jl (no Python bridge).
Runs faster and gives more control than PySR-via-PyCall.

Usage:
  julia kevinotron_pysr.jl              # run all
  julia kevinotron_pysr.jl --quick      # quick mode (50 iterations)
  julia kevinotron_pysr.jl --full       # full mode (500 iterations)

Author: Kevin Remondiere
Date: 2026-05-27
"""

using Pkg

# Ensure SymbolicRegression is installed
try
    using SymbolicRegression
catch
    Pkg.add("SymbolicRegression")
    using SymbolicRegression
end

using Printf
using Statistics
using Random
using LinearAlgebra

# ============================================================
# DATA
# ============================================================

# Format: (group_label, beta, L, S2/A, C2, dim_adj, |Z|, d_fund)
const DATA_MATCHED = [
    # SU(2) β=2.50
    (2.50, 4,  7.22, 2, 3,  2, 2),
    (2.50, 6,  7.17, 2, 3,  2, 2),
    (2.50, 8,  7.13, 2, 3,  2, 2),
    (2.50, 10, 7.16, 2, 3,  2, 2),
    (2.50, 12, 7.13, 2, 3,  2, 2),
    # SU(3) β=6.06
    (6.06, 4,  14.17, 3, 8,  3, 3),
    (6.06, 6,  14.03, 3, 8,  3, 3),
    (6.06, 8,  14.03, 3, 8,  3, 3),
    (6.06, 10, 14.00, 3, 8,  3, 3),
    (6.06, 12, 13.99, 3, 8,  3, 3),
    # SU(4) β=10.80
    (10.80, 4,  21.69, 4, 15, 4, 4),
    (10.80, 6,  21.53, 4, 15, 4, 4),
    (10.80, 8,  21.53, 4, 15, 4, 4),
    (10.80, 10, 21.54, 4, 15, 4, 4),
    (10.80, 12, 21.54, 4, 15, 4, 4),
    # G₂ β=10.0 (no L=8)
    (10.0, 4,  18.30, 4, 14, 1, 7),
    (10.0, 6,  18.09, 4, 14, 1, 7),
    (10.0, 10, 18.08, 4, 14, 1, 7),
    (10.0, 12, 18.09, 4, 14, 1, 7),
]

const DATA_G2_MULTIBETA = [
    (9.6,  4, 15.99, 4, 14, 1, 7),
    (9.6,  6, 15.67, 4, 14, 1, 7),
    (9.6,  8, 15.65, 4, 14, 1, 7),
    (9.8,  4, 17.23, 4, 14, 1, 7),
    (9.8,  6, 16.93, 4, 14, 1, 7),
    (9.8,  8, 16.86, 4, 14, 1, 7),
    (10.2, 4, 19.21, 4, 14, 1, 7),
    (10.2, 6, 19.19, 4, 14, 1, 7),
    (10.2, 8, 19.24, 4, 14, 1, 7),
    (10.4, 4, 20.48, 4, 14, 1, 7),
    (10.4, 6, 20.37, 4, 14, 1, 7),
    (10.4, 8, 20.39, 4, 14, 1, 7),
]

# ============================================================
# BUILD FEATURE MATRIX
# ============================================================

function build_features(data)
    n = length(data)
    # Features: C2, dim_adj, ln|Z|, d_fund, beta, 1/L², n_roots, beta/d_fund
    X = zeros(Float64, n, 8)
    y = zeros(Float64, n)
    for i in 1:n
        β, L, s2a, C2, dim, Z, df = data[i]
        X[i, 1] = Float64(C2)                            # C2
        X[i, 2] = Float64(dim)                            # dim_adj
        X[i, 3] = log(max(Float64(Z), 1.0))              # ln|Z|
        X[i, 4] = Float64(df)                             # d_fund
        X[i, 5] = β                                       # beta
        X[i, 6] = 1.0 / L^2                              # 1/L²
        X[i, 7] = Float64(C2 * (C2 - 1) ÷ 2)            # n_roots = |Φ⁺|
        X[i, 8] = β / Float64(df)                         # beta/d_fund
        y[i]    = s2a
    end
    return X, y
end

# ============================================================
# RUN SYMBOLIC REGRESSION
# ============================================================

function run_sr(; quick::Bool=false)
    all_data = vcat(DATA_MATCHED, DATA_G2_MULTIBETA)
    X, y = build_features(all_data)
    n, p = size(X)

    niter = quick ? 50 : 200
    feature_names = ["C2", "dim_adj", "lnZ", "d_fund", "beta", "inv_L2",
                     "n_roots", "beta_over_df"]

    println("=" ^ 72)
    println("KEVINOTRON PySR (Julia native) -- SymbolicRegression.jl")
    println("=" ^ 72)
    println("Data: $n points, $p features")
    println("Features: ", join(feature_names, ", "))
    println("Iterations: $niter")
    println()

    # ---- Run 1: Full free-form ----
    println("--- Run 1: Free-form symbolic regression ---")

    options = Options(
        binary_operators=[+, -, *, /],
        unary_operators=[log, sqrt, square],
        populations=20,
        population_size=40,
        maxsize=25,
        parsimony=0.005f0,
        ncycles_per_iteration=500,
        timeout_in_seconds=quick ? 60.0 : 300.0,
        seed=42,
        deterministic=true,
        progress=true,
    )

    hall_of_fame = equation_search(
        X', y;           # SymbolicRegression expects features × samples
        options=options,
        variable_names=feature_names,
        niterations=niter,
        parallelism=:serial,
    )

    println("\nTop equations (Pareto front):")
    for (i, member) in enumerate(hall_of_fame.members)
        if member.exists
            eq_str = string_tree(member.tree, options; variable_names=feature_names)
            @printf("  [%2d] loss=%.6f  %s\n", member.tree.degree + 1,
                    member.loss, eq_str)
        end
        i >= 10 && break
    end

    # ---- Run 2: Normalized (remove UV divergence) ----
    println("\n--- Run 2: Normalized S2/A / (beta/d_fund) ---")

    y_norm = y ./ X[:, 8]   # S2_norm = S2/A / (beta/d_fund)
    # Only use group features (drop beta, beta/d_fund)
    X_grp = X[:, [1, 2, 3, 4, 6, 7]]  # C2, dim_adj, lnZ, d_fund, 1/L², n_roots
    feature_names_grp = ["C2", "dim_adj", "lnZ", "d_fund", "inv_L2", "n_roots"]

    options2 = Options(
        binary_operators=[+, -, *, /],
        unary_operators=[log, sqrt, square],
        populations=20,
        population_size=40,
        maxsize=20,
        parsimony=0.008f0,
        ncycles_per_iteration=500,
        timeout_in_seconds=quick ? 60.0 : 300.0,
        seed=42,
        deterministic=true,
        progress=true,
    )

    hall_of_fame2 = equation_search(
        X_grp', y_norm;
        options=options2,
        variable_names=feature_names_grp,
        niterations=niter,
        parallelism=:serial,
    )

    println("\nTop normalized equations:")
    for (i, member) in enumerate(hall_of_fame2.members)
        if member.exists
            eq_str = string_tree(member.tree, options2;
                                 variable_names=feature_names_grp)
            @printf("  [%2d] loss=%.6f  %s\n", member.tree.degree + 1,
                    member.loss, eq_str)
        end
        i >= 10 && break
    end

    # ---- Manual hypothesis tests (4-point group decomposition) ----
    println("\n--- Manual hypothesis tests (4 matched groups) ---")

    # Average S2/A for L >= 8 per group
    groups = ["SU(2)", "SU(3)", "SU(4)", "G₂"]
    C2_vals = [2.0, 3.0, 4.0, 4.0]
    dim_vals = [3.0, 8.0, 15.0, 14.0]
    Z_vals = [2.0, 3.0, 4.0, 1.0]
    dfund_vals = [2.0, 3.0, 4.0, 7.0]
    nroots_vals = [1.0, 3.0, 6.0, 6.0]

    # Compute L>=8 averages from matched data
    s2a_avg = Float64[]
    group_ranges = [(1, 5), (6, 10), (11, 15), (16, 19)]
    for (i_start, i_end) in group_ranges
        vals = [DATA_MATCHED[i][3] for i in i_start:i_end if DATA_MATCHED[i][2] >= 8]
        push!(s2a_avg, mean(vals))
    end

    hypotheses = Dict{String, Vector{Float64}}(
        "C2"             => C2_vals,
        "dim_adj"        => dim_vals,
        "C2(C2-1)/2"     => [c*(c-1)/2 for c in C2_vals],
        "C2²"            => [c^2 for c in C2_vals],
        "dim_adj + lnZ"  => [dim_vals[i] + log(max(Z_vals[i], 1.0))
                             for i in 1:4],
        "C2*d_fund"      => [C2_vals[i]*dfund_vals[i] for i in 1:4],
        "C2 + lnZ"       => [C2_vals[i] + log(max(Z_vals[i], 1.0))
                             for i in 1:4],
    )

    @printf("  %-25s %8s %8s %10s\n", "Hypothesis", "a", "b", "max_res%")
    @printf("  %-25s %8s %8s %10s\n", "-"^25, "-"^8, "-"^8, "-"^10)

    for (name, xvals) in sort(collect(hypotheses); by=kv->kv[1])
        # Simple linear regression y = a*x + b
        xv = Float64.(xvals)
        n_g = length(xv)
        x_mean = mean(xv)
        y_mean_h = mean(s2a_avg)
        a = sum((xv .- x_mean) .* (s2a_avg .- y_mean_h)) /
            sum((xv .- x_mean).^2)
        b = y_mean_h - a * x_mean
        y_pred = a .* xv .+ b
        max_resid = maximum(abs.(y_pred .- s2a_avg) ./ s2a_avg) * 100
        @printf("  %-25s %8.3f %8.3f %10.2f%%\n", name, a, b, max_resid)
    end

    println("\n" * "=" ^ 72)
    println("DONE")
    println("=" ^ 72)
end

# ============================================================
# MAIN
# ============================================================

quick_mode = "--quick" in ARGS
run_sr(quick=quick_mode)
