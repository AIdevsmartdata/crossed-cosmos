#!/usr/bin/env python3
# Instrumentation de DIAGNOSTIC de nanoda (aucun changement de la logique de vérification) :
# chaque fil écrit sur stderr « DEBUT idx nom » avant de vérifier une déclaration et « FIN idx secondes » après.
# Sert à identifier la ou les déclarations sur lesquelles le rejeu officiel (binaire NON modifié) ne termine pas.
import sys
p = sys.argv[1]
s = open(p).read()
old = """                                    if let Some((_, declar)) = self.declars.get_index(idx) {
                                        self.check_declar(declar);
                                    } else {"""
new = """                                    if let Some((_, declar)) = self.declars.get_index(idx) {
                                        let t0 = std::time::Instant::now();
                                        self.with_ctx(|ctx| eprintln!("DEBUT {} {:?}", idx, ctx.debug_print(declar.info().name)));
                                        self.check_declar(declar);
                                        eprintln!("FIN {} {:.3}", idx, t0.elapsed().as_secs_f64());
                                    } else {"""
assert s.count(old) == 1, s.count(old)
open(p, 'w').write(s.replace(old, new))
print("patch appliqué")
