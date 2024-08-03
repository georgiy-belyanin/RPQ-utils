# The parameters we've used to run the SPARQL Wikidata query generator

# Simple query, usually no more than 1 edge starting from the source.
python3 ./generate-wikidata-sparql-ss-queries.py "(<http://www.wikidata.org/prop/direct/P131>)*" > "P131*.txt" 192846
# Simple query but more than 1 edge starting from the source.
python3 ./generate-wikidata-sparql-ss-queries.py "(<http://www.wikidata.org/prop/direct/P279>)*" > "P279*.txt" 192846
# More complex query.
python3 ./generate-wikidata-sparql-ss-queries.py "((<http://www.wikidata.org/prop/direct/P279>|<http://www.wikidata.org/prop/direct/P31>)/((<http://www.wikidata.org/prop/direct/P279>)*|(<http://www.wikidata.org/prop/direct/P31>)*))" > "P279|P31(P279*|P31*)" 192846
# Limited length query, many state query.
python3 ./generate-wikidata-sparql-ss-queries.py "(((((<http://www.wikidata.org/prop/direct/P31>/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)" > "P31 P279? P279? P279? P279? P279?" 192846
# Searching the siblings.
python3 ./generate-wikidata-sparql-ss-queries.py "((^<http://www.wikidata.org/prop/direct/P161>/<http://www.wikidata.org/prop/direct/P161>))/((^<http://www.wikidata.org/prop/direct/P161>/<http://www.wikidata.org/prop/direct/P161>))*" > "^P161 P161 (^P161 P161)*"
