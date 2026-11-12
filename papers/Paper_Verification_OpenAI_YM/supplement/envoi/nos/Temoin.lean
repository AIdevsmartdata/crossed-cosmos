import ConcreteSU2

/-! Témoins négatifs du pilote : `#print axioms` doit faire apparaître `sorryAx` et l'axiome ajouté. -/

theorem temoinSorry : (1 : ℕ) = 2 := by sorry

axiom temoinAxiome : (1 : ℕ) = 2

theorem temoinAxiomeUtilise : (1 : ℕ) = 2 := temoinAxiome

#print axioms temoinSorry
#print axioms temoinAxiomeUtilise
