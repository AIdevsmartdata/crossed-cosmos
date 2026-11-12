import ConcreteSU2

/-! Contrôle du pilote (11/11/2026), indépendant des scripts fournis par OpenAI.
1. Axiomes de la clôture des trois résultats annoncés.
2. L'énoncé du `Challenge.lean` d'origine (sha256 d31b227d…), recopié tel quel, est prouvé par le terme
   `YangMills.jointExistence` de la solution.
3. La définition dépliée, recopiée de `ChallengeSpec.lean` l. 186-188 (sha256 e48b0be2…), l'est aussi. -/

#print axioms YangMills.jointExistence
#print axioms YangMills.constructed
#print axioms YangMills.su2Theory

-- Challenge.lean : `theorem YangMills.jointExistence : YangMills.JointExistence := by sorry`
example : YangMills.JointExistence := YangMills.jointExistence

namespace YangMills
-- ChallengeSpec.lean, l. 186-188, recopié.
example : ∀ g : GaugeGroup, g.IsSimple → ∃ C : WilsonFamily g,
  WilsonRegularity C ∧ ∀ p : ℕ → ℕ, StrictMono p → ∃ q : ℕ → ℕ, StrictMono q ∧
    ∃ T : Hierarchy C, T.Properties (p ∘ q) := jointExistence
end YangMills

#check @YangMills.jointExistence
#check @YangMills.su2Theory
#print YangMills.JointExistence
