#!/usr/bin/env python3
"""Verification locale (texte seulement, aucun calcul Lean) par un non-auteur.
1. sha256 de ENONCES_GELES.lean ; 2. enonces des 16 theoremes : fige vs prouve (texte exact ET texte a espaces normalises) ;
3. definitions de la partie B : figees vs DEFS_B ; 4. mots interdits hors commentaires et chaines ; 5. assemblage = auteur moins pieds."""
import re, sys, hashlib, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../src/'
rd = lambda f: open(D + f, encoding='utf-8').read()
fige, A, B, DEFS, GELE = rd('ENONCES_GELES.lean'), rd('CentreZN_A_PROUVE_tour2.lean'), rd('CentreZN_B_PROUVE_tour2.lean'), rd('DEFS_B.lean'), rd('GELE_A.lean')
aut = rd('auteur_CentreZNComplet.lean')
NOMS = ['centre_flip_bound','twist_ratio_bound','rho_crude','rho_two','sharp_one_plaquette','centre_flip_bound_crude','twist_ratio_bound_crude',
 'recover_column_flip_bound','recover_twist_ratio_bound','mixed_word_neutral','wilson_centre_flip_bound','torus_charge_explicit',
 'torus_charge_sum','torus_charge_image','wilson_twist_ratio_torus','wilson_twist_ratio_torus_crude']
ok = True
h = hashlib.sha256(open(D+'ENONCES_GELES.lean','rb').read()).hexdigest()
print('sha256 ENONCES_GELES.lean =', h, 'OK' if h.startswith('17f5a911') and h.endswith('b863') else 'ECART'); ok &= h.startswith('17f5a911')
def enonce(src, nom):
    m = re.findall(r'\ntheorem ' + re.escape(nom) + r'\b(.*?):= by', src, flags=re.S)
    return m
print('\n## 2. enonces (de `theorem NOM` a `:= by`)')
for nom in NOMS:
    a = enonce(fige, nom); b = enonce(A, nom) + enonce(B, nom)
    if len(a) != 1 or len(b) != 1: print(f'{nom}: occurrences fige={len(a)} prouve={len(b)} ECART'); ok = False; continue
    ex = a[0] == b[0]; nm = ' '.join(a[0].split()) == ' '.join(b[0].split())
    print(f'{nom}: texte exact {"identique" if ex else "DIFFERENT"} ; espaces normalises {"identique" if nm else "DIFFERENT"} ({len(a[0])} car.)')
    ok &= ex
print('\n## 3. definitions de la partie B')
i = fige.index('/-! ## Partie B : théorie de type Wilson'); j = fige.index('/-! ## Partie B : énoncés')
dfig = fige[i:j].strip(); dd = DEFS[DEFS.index('/-! ## Partie B : théorie de type Wilson'):].strip()
dd = re.sub(r'\n+end CentreZN\s*(end\s*)?$', '', dd).strip()
print('definitions B figees == DEFS_B :', dfig == dd); ok &= (dfig == dd)
if dfig != dd:
    import difflib; print(''.join(list(difflib.unified_diff(dfig.splitlines(1), dd.splitlines(1)))[:40]))
print('\n## 3b. en-tete GELE_A vs en-tete fige')
print('lignes import/set_option/open/noncomputable/namespace de GELE_A :', [l for l in GELE.splitlines() if re.match(r'(import|set_option|open|noncomputable|namespace)', l)])
print('meme chose dans le fige            :', [l for l in fige.splitlines()[:16] if re.match(r'(import|set_option|open|noncomputable|namespace)', l)])
# 4. mots interdits hors commentaires
def strip(src):
    out, i, n, depth = [], 0, len(src), 0
    while i < n:
        if src.startswith('/-', i): depth += 1; i += 2; continue
        if depth and src.startswith('-/', i): depth -= 1; i += 2; continue
        if depth: i += 1; continue
        if src.startswith('--', i):
            while i < n and src[i] != '\n': i += 1
            continue
        if src[i] == '"':
            i += 1
            while i < n and src[i] != '"': i += 2 if src[i] == '\\' else 1
            i += 1; out.append('""'); continue
        out.append(src[i]); i += 1
    return ''.join(out)
print('\n## 4. mots interdits (hors commentaires)')
INT = r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by|opaque|extern|partial|macro|macro_rules|syntax|elab|notation|infix|postfix|prefix|initialize|builtin_initialize|run_cmd|run_elab|run_meta|import|set_option|attribute|instance|local|scoped|variable|universe|decide\+native|Lean\.ofReduceBool|ofReduceBool|trustCompiler|reduceBool|reduceNat)\b|@\[|^\s*#|\bopen\b'
for nom, src in (('Sol A', A), ('Sol B', B), ('DEFS_B', DEFS), ('GELE_A', GELE)):
    s = strip(src); hits = [(k+1, l.strip()[:90]) for k, l in enumerate(s.splitlines()) if re.search(INT, l)]
    print(nom, ':', len(hits), 'lignes suspectes', hits[:12])
print('\n## 5. assemblage : auteur = GELE_A + A + DEFS_B + B + pieds ?')
pre = GELE + A + DEFS + B
print('prefixe identique au fichier complet de l\'auteur :', aut.startswith(pre), '; longueur prefixe', len(pre), 'fichier auteur', len(aut))
print('\nBILAN texte :', 'OK' if ok else 'ECART')
sys.exit(0 if ok else 1)
