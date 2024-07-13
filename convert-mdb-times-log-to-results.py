import sys
import math

QUERIES = 113
RUNS = 30

with open(sys.argv[1], 'r') as f:
    p = 0
    o = 0
    e = 0
    datasets = {}
    for i in range(1, QUERIES + 1):
        datasets[i] = []
    i = 1
    for l in f:
        if l.startswith('Optimizer'):
            o = float(l.split(':')[1].strip()[:-3])
            datasets[i].append(o * 1000 + e * 1000)
            i = i + 1
            if i == QUERIES + 1:
                i = 1
        elif l.startswith('Execution'):
            e = float(l.split(':')[1].strip()[:-3])

    for k, v in datasets.items():
        with open(f"{sys.argv[2]}/{k}.txt", 'w') as r:
            for i in v:
                r.write(f'{i:.0f}\n')
