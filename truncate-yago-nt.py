import sys

prop = "http://yago-knowledge.org/resource/"
with open(sys.argv[1], 'r') as f:
    for i in f:
        s = i.split(maxsplit=3)
        if prop not in s[1]:
            continue
        print(i, end='')
