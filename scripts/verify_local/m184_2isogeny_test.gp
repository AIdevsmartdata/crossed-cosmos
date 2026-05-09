/* M184 verification — using MINIMAL models for Heegner CM curves */
default(realprecision, 100);
default(parisize, "100M");

print("=== Heegner CM Elliptic Curves: Minimal Cremona models ===");

/* Use ellminimalmodel after ellfromj */
fix_minimal(j) = {
  my(E0, E);
  E0 = ellinit(ellfromj(j));
  E = ellminimalmodel(E0);
  return(E);
};

/* All Heegner CM curves (j-invariants from class equation roots) */
/* D=-3: j=0, but not Heegner-relevant for our weight-5; skip */
/* D=-7: j=-3375 */
print("\n--- D=-7 (j=-3375) ---");
E_7 = fix_minimal(-3375);
print("  Δ_min = ", E_7.disc, " ord_2=", valuation(E_7.disc,2));
print("  cond = ", ellglobalred(E_7)[1]);
print("  ω₁ = ", E_7.omega[1]);
print("  ω₂ = ", E_7.omega[2]);
print("  E[2] tors = ", elltors(E_7));
print("  local at 2 = ", elllocalred(E_7,2));

/* D=-11: j=-32^3 = -32768 */
print("\n--- D=-11 (j=-32768) ---");
E_11 = fix_minimal(-32768);
print("  Δ_min = ", E_11.disc, " ord_2=", valuation(E_11.disc,2));
print("  cond = ", ellglobalred(E_11)[1]);
print("  ω₁ = ", E_11.omega[1]);
print("  ω₂ = ", E_11.omega[2]);
print("  E[2] tors = ", elltors(E_11));
print("  local at 2 = ", elllocalred(E_11,2));

/* D=-19: j=-96^3 = -884736 */
print("\n--- D=-19 (j=-884736) ---");
E_19 = fix_minimal(-884736);
print("  Δ_min = ", E_19.disc, " ord_2=", valuation(E_19.disc,2));
print("  cond = ", ellglobalred(E_19)[1]);
print("  ω₁ = ", E_19.omega[1]);
print("  ω₂ = ", E_19.omega[2]);
print("  E[2] tors = ", elltors(E_19));
print("  local at 2 = ", elllocalred(E_19,2));

/* D=-43: j=-960^3 */
print("\n--- D=-43 (j=-960^3) ---");
E_43 = fix_minimal(-960^3);
print("  Δ_min = ", E_43.disc, " ord_2=", valuation(E_43.disc,2));
print("  cond = ", ellglobalred(E_43)[1]);
print("  ω₁ = ", E_43.omega[1]);
print("  ω₂ = ", E_43.omega[2]);
print("  E[2] tors = ", elltors(E_43));
print("  local at 2 = ", elllocalred(E_43,2));

/* D=-67: j=-5280^3 */
print("\n--- D=-67 (j=-5280^3) ---");
E_67 = fix_minimal(-5280^3);
print("  Δ_min = ", E_67.disc, " ord_2=", valuation(E_67.disc,2));
print("  cond = ", ellglobalred(E_67)[1]);
print("  ω₁ = ", E_67.omega[1]);
print("  ω₂ = ", E_67.omega[2]);
print("  E[2] tors = ", elltors(E_67));
print("  local at 2 = ", elllocalred(E_67,2));

/* D=-163: j=-640320^3 */
print("\n--- D=-163 (j=-640320^3) ---");
E_163 = fix_minimal(-640320^3);
print("  Δ_min = ", E_163.disc, " ord_2=", valuation(E_163.disc,2));
print("  cond = ", ellglobalred(E_163)[1]);
print("  ω₁ = ", E_163.omega[1]);
print("  ω₂ = ", E_163.omega[2]);
print("  E[2] tors = ", elltors(E_163));
print("  local at 2 = ", elllocalred(E_163,2));

/* Now isogeny structure with bigger stack */
print("\n=== Isogeny class data ===");
trap(, print("  D=-7 isogcls TIMEOUT/STACK"), {
  iso7 = ellisomat(E_7, 2);
  print("D=-7  2-isog: ", #iso7[1], " curves");
});
trap(, print("  D=-11 isogcls TIMEOUT/STACK"), {
  iso11 = ellisomat(E_11, 2);
  print("D=-11 2-isog: ", #iso11[1], " curves");
});
trap(, print("  D=-19 isogcls TIMEOUT/STACK"), {
  iso19 = ellisomat(E_19, 2);
  print("D=-19 2-isog: ", #iso19[1], " curves");
});
trap(, print("  D=-43 isogcls TIMEOUT/STACK"), {
  iso43 = ellisomat(E_43, 2);
  print("D=-43 2-isog: ", #iso43[1], " curves");
});
trap(, print("  D=-67 isogcls TIMEOUT/STACK"), {
  iso67 = ellisomat(E_67, 2);
  print("D=-67 2-isog: ", #iso67[1], " curves");
});

/* Now compute c⁴ ratios — both periods squared */
print("\n=== c⁴ test: |ω₂/ω₁|^4 |Δ ω| ===");
print("D=-7  |Δω|^4 = ", abs(E_7.omega[2]/E_7.omega[1])^4);
print("D=-11 |Δω|^4 = ", abs(E_11.omega[2]/E_11.omega[1])^4);
print("D=-19 |Δω|^4 = ", abs(E_19.omega[2]/E_19.omega[1])^4);
print("D=-43 |Δω|^4 = ", abs(E_43.omega[2]/E_43.omega[1])^4);
print("D=-67 |Δω|^4 = ", abs(E_67.omega[2]/E_67.omega[1])^4);
print("D=-163 |Δω|^4 = ", abs(E_163.omega[2]/E_163.omega[1])^4);

quit;
