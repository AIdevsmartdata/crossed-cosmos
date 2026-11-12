#!/bin/bash
export PATH=/work/tc/4.32.0/bin:/usr/bin:/bin HOME=/work/home
cd /work/lean4lean_essai/temoins
cat > TemoinFaux2.lean <<'X'
import Lean
open Lean Elab Command
def ty : Expr := mkApp3 (mkConst ``Eq [1]) (mkConst ``Nat) (mkRawNatLit 1) (mkRawNatLit 2)
def va : Expr := mkApp2 (mkConst ``Eq.refl [1]) (mkConst ``Nat) (mkRawNatLit 1)
set_option debug.skipKernelTC true in
run_cmd liftCoreM <| addDecl <| .thmDecl { name := `Faux2.bad, levelParams := [], type := ty, value := va }
X
LEAN_PATH=/work/lean4lean_essai/temoins/build lean TemoinFaux2.lean -o build/TemoinFaux2.olean; echo "compile rc=$?"
export LEAN_PATH=/work/lean4lean_essai/temoins/build
L=/work/lean4lean_essai/src/.lake/build/bin/lean4lean
m=TemoinFaux2
/usr/bin/time -v nice -n 10 $L -v $m > run_$m.out 2> run_$m.err; echo "lean4lean $m rc=$?"; cat run_$m.out; grep -E "lean4lean found|mismatch" -A2 run_$m.err | head -5
echo ---; cat run_TemoinFaux1.out; head -8 run_TemoinFaux1.err
