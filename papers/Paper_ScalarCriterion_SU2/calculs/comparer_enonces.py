import re,sys,hashlib
def ext(p):
    t=open(p).read()
    # chaque 'theorem NOM ... := by' (statement), hors lemmes aux_
    out=[]
    for m in re.finditer(r'(?m)^theorem\s+(\w+)(.*?):=\s*by', t, re.S):
        if not m.group(1).startswith('aux_'):
            out.append((m.group(1), ' '.join(m.group(2).split())))
    return out
for a,b in [(sys.argv[1],sys.argv[2]),(sys.argv[3],sys.argv[4])]:
    ea,eb=ext(a),ext(b)
    print(a.split('/')[-1], b.split('/')[-1], len(ea), len(eb), 'IDENTIQUES' if ea==eb else 'DIFFERENTS')
    print([n for n,_ in ea])
