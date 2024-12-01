import sys

s1 = 'http://www.wikidata.org/entity/Q'
s2 = 'http://www.wikidata.org/entity/Q'
prop = 'http://www.wikidata.org/prop/direct/P'
with open(sys.argv[1], 'r') as f:
    for i in f:
        s = i.split(maxsplit=3)
        if s1 not in s[0] or prop not in s[1] or s2 not in s[2]:
            continue
        print(i, end='')
