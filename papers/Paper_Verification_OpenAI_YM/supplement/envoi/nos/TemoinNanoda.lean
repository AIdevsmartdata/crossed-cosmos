/-! Témoins pour le noyau indépendant (sans import : seul le prélude de Lean).
`temoinVrai` doit passer ; `temoinSorry` et `temoinAxiomeUtilise` doivent être refusés par nanoda
(axiomes non permis : `sorryAx`, `temoinAxiome`). -/

theorem temoinVrai : (2 : Nat) + 2 = 4 := rfl

theorem temoinSorry : (1 : Nat) = 2 := by sorry

axiom temoinAxiome : (1 : Nat) = 2

theorem temoinAxiomeUtilise : (1 : Nat) = 2 := temoinAxiome
