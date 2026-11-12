import Lean
open Lean Elab Command
def ty : Expr := mkApp3 (mkConst ``Eq [1]) (mkConst ``Nat) (mkRawNatLit 1) (mkRawNatLit 2)
def va : Expr := mkApp2 (mkConst ``Eq.refl [1]) (mkConst ``Nat) (mkRawNatLit 1)
set_option debug.skipKernelTC true in
run_cmd liftCoreM <| addDecl <| .thmDecl { name := `Faux2.bad, levelParams := [], type := ty, value := va }
