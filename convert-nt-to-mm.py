import sys

mm_prelude = """%%MatrixMarket matrix coordinate pattern general
%%GraphBLAS type bool
"""

d = sys.argv[2]

f =  open(sys.argv[1], 'r')
fv = open(f'{d}/vertices.txt', 'w')
fe = open(f'{d}/edges.txt', 'w')


vs = {}
ps = {}
pcs = [0]
gs = [0]

total = 0

i = 0
j = 0
for line in f:
    s = line.split()

    v1 = s[0]
    p = s[1]
    v2 = (" ".join(s[2:]))[:-2]

    if v1 not in vs:
        i = i + 1
        vs[v1] = i

    if p not in ps:
        #p[p.find('#')+1:-1] if p.find('#') != -1 else p[p.rfind('/')+1:-1]
        j = j + 1
        ps[p] = j
        gs.append([])
        pcs.append(0)
    pcs[ps[p]] += 1

    if v2 not in vs:
        i = i + 1
        vs[v2] = i

    gs[ps[p]].append((vs[v1], vs[v2]))

    if len(gs[ps[p]]) > 50000:
        with open(f'{d}/{ps[p]}.txt', 'a') as g:
            for l in gs[ps[p]]:
                v1, v2 = l
                g.write(f"{v1} {v2}\n")
            gs[ps[p]] = []

    total += 1

for key in vs:
    fv.write(f'{key} {vs[key]}\n')

for key in ps:
    fe.write(f'{key} {ps[key]}\n')

for k in range(1, j + 1):
    with open(f'{d}/{k}.txt', 'a') as g:
        for l in gs[k]:
            v1, v2 = l
            g.write(f"{v1} {v2}\n")

for k in range(1, j + 1):
    with open(f'{d}/{k}.txt', 'r+') as g:
        content = g.read()
        g.seek(0, 0)
        g.write(mm_prelude)
        g.write(f'{i} {i} {pcs[k]}\n')
        g.write(content)

print(f"Successfully convertes {sys.argv[1]}")
print(f"Triples: {total}, vertices: {i}, predicates: {j}")

fv.close()
fe.close()
f.close()
