/-
Chronométrage, par le noyau de Lean lui-même, de la re-vérification d'UNE déclaration déjà présente dans l'environnement :
on recopie sa déclaration sous un autre nom et on la soumet à `addDecl` (donc au noyau), de façon synchrone.
Usage (dans le projet compilé) :  lake env lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 Chrono.lean
La liste des noms à chronométrer est à la fin du fichier (une commande `#chrono_noyau "Nom.Complet"` par déclaration).
Outil de diagnostic du pilote ; ne modifie rien au projet.
-/
import ConcreteSU2
open Lean Elab Command

set_option Elab.async false
set_option maxHeartbeats 0
set_option maxRecDepth 4096

/-- Nombre de nœuds d'une expression vue comme arbre (plafonné), pour donner un ordre de grandeur de la taille d'une preuve. -/
partial def tailleArbre (e : Expr) (plafond : Nat := 500000000) : Nat := Id.run do
  let mut pile := #[e]
  let mut n := 0
  while !pile.isEmpty do
    let x := pile.back!
    pile := pile.pop
    n := n + 1
    if n ≥ plafond then return n
    match x with
    | .app f a => pile := (pile.push f).push a
    | .lam _ t b _ => pile := (pile.push t).push b
    | .forallE _ t b _ => pile := (pile.push t).push b
    | .letE _ t v b _ => pile := ((pile.push t).push v).push b
    | .mdata _ b => pile := pile.push b
    | .proj _ _ b => pile := pile.push b
    | _ => pure ()
  return n

elab "#chrono_noyau " s:str : command => do
  let cible := s.getString
  let env ← getEnv
  let trouve := env.constants.fold (init := (none : Option ConstantInfo)) fun acc n ci =>
    if acc.isSome then acc else if n.toString (escape := false) == cible then some ci else none
  let some ci := trouve | throwError "déclaration absente de l'environnement : {cible}"
  let copie := ci.name ++ `copieChrono
  let (genre, decl, val) ← match ci with
    | .thmInfo v => pure ("théorème", Declaration.thmDecl { v with name := copie }, v.value)
    | .defnInfo v => pure ("définition", Declaration.defnDecl { v with name := copie }, v.value)
    | .opaqueInfo v => pure ("opaque", Declaration.opaqueDecl { v with name := copie }, v.value)
    | _ => throwError "ni théorème ni définition : {cible}"
  let tType := tailleArbre ci.type 50000000
  let tVal := tailleArbre val 50000000
  let t0 ← IO.monoMsNow
  liftCoreM <| addDecl decl
  let t1 ← IO.monoMsNow
  logInfo m!"CHRONO_NOYAU {cible} | {genre} | noeuds(type)={tType} noeuds(valeur)={tVal} (arbre, plafond 5e7) | noyau Lean : {t1 - t0} ms"
