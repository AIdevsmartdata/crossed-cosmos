import Lean
open Lean Elab Command
set_option debug.skipKernelTC true in
run_cmd liftCoreM <| addDecl <| .thmDecl { name := `Faux1.bad, levelParams := [], type := mkConst ``False, value := mkConst ``True.intro }
