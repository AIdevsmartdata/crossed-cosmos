#!/usr/bin/env python3
"""Verification statique par un non-auteur : enonces, prefixe publie, mots interdits."""
import re, sys, hashlib, json
P = sys.argv[1]  # dossier lean publie v1.1
def rd(f): return open(f, encoding='utf-8').read()
def strip_comments(s):
    # retire commentaires blocs (imbriques) et lignes, en gardant les chaines
    out=[];i=0;depth=0;n=len(s)
    while i<n:
        if s.startswith('/-',i): depth+=1;i+=2;continue
        if depth and s.startswith('-/',i): depth-=1;i+=2;continue
        if depth: i+=1;continue
        if s.startswith('--',i):
            while i<n and s[i]!='\n': i+=1
            continue
        out.append(s[i]);i+=1
    return ''.join(out)
def statements(s):
    s=strip_comments(s)
    res={}
    for m in re.finditer(r'^(theorem|noncomputable def|def)\s+(\w+)(.*?)(?::=\s*by|:=\s*$|:=\s)', s, re.S|re.M):
        pass
    # decoupage : de "theorem X" jusqu'au premier ":= by" a profondeur zero (les enonces n'ont pas de := interne)
    for m in re.finditer(r'^(theorem|noncomputable def|def) (\w+)', s, re.M):
        st=m.start(); k=s.find(':=',st)
        res[m.group(2)]=re.sub(r'\s+',' ',s[st:k]).strip()
    return res
E=statements(rd('ENONCES.lean')); R=statements(rd('RECIPROQUE_full.lean')); C=statements(rd('COMBINE.lean'))
ok=True
print('sha256 ENONCES', hashlib.sha256(open('ENONCES.lean','rb').read()).hexdigest())
for nm in E:
    for lab,D in (('RECIPROQUE_full',R),('COMBINE',C)):
        same = nm in D and D[nm]==E[nm]
        print(f'{nm:20s} {lab:16s}', 'IDENTIQUE' if same else 'DIFFERENT')
        ok&=same
# corps des defs : comparer aussi les corps des def jusqu'au prochain item (def a corps apres :=)
def body(s,nm):
    s=strip_comments(s); s=s[s.index('namespace Reciproque'):]; m=re.search(r'^(?:noncomputable )?def '+nm+r'\b',s,re.M); k=s.find(':=',m.start())
    e=re.search(r'\n\s*\n',s[k:]); return re.sub(r'\s+',' ',s[k:k+e.start()]).strip()
for nm in ('sT','Delta','Rep','HypSpec','HypRec'):
    for lab,f in (('RECIPROQUE_full','RECIPROQUE_full.lean'),('COMBINE','COMBINE.lean')):
        same=body(rd('ENONCES.lean'),nm)==body(rd(f),nm); print('corps def',nm,lab,'IDENTIQUE' if same else 'DIFFERENT'); ok&=same
# prefixe publie
pub=open(P+'/main.lean','rb').read(); comb=open('COMBINE.lean','rb').read()
pref = comb.startswith(pub)
print('COMBINE commence par main.lean publie (octet pour octet):',pref, len(pub),'octets;', 'ajoute', len(comb)-len(pub),'octets /', comb[len(pub):].count(b'\n'),'lignes')
ok&=pref

# corps de Reciproque.lean contenu tel quel dans COMBINE
r=rd('RECIPROQUE_full.lean'); c=rd('COMBINE.lean')
a=r[r.index('namespace Reciproque'):r.index('end Reciproque')]
b=c[c.index('namespace Reciproque'):]
same=b.startswith(a); print('corps de namespace Reciproque de RECIPROQUE_full recopie tel quel dans COMBINE:',same); ok&=same
# mots interdits hors commentaires
bad=['sorry','admit','axiom','native_decide','unsafe','implemented_by','@[extern]','opaque','extern']
for f in ('RECIPROQUE_full.lean','COMBINE.lean'):
    s=strip_comments(rd(f))
    for b in bad:
        hits=[(s[:m.start()].count('\n')+1) for m in re.finditer(r'(?<![\w.])'+re.escape(b)+r'(?![\w])',s)]
        if hits: print('INTERDIT',f,b,hits[:5]); ok=False
print('mots interdits hors commentaires: balayage fait')
print('VERDICT_STATIQUE','OK' if ok else 'ECHEC')
