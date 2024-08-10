import sys
import random
import datetime

QUERY_COUNT = 10000
MAX_ENTITY_NUMBER = 107346161

if len(sys.argv) == 1:
    print("Generates Wikidata SPARQL single-source queries from random entities to stdout")
    print("Usage: python3 ./generate-wikidata-sparql-queries.py <query>")
    sys.exit()

seed = 1
if len(sys.argv) < 3:
    seed = int(datetime.datetime.now().timestamp())
else:
    seed = int(sys.argv[2])

random.seed(seed)

for i in range(1, QUERY_COUNT + 1):
    print(f'{i},<http://www.wikidata.org/entity/Q{random.randint(1, MAX_ENTITY_NUMBER)}> {sys.argv[1]} ?x1')
