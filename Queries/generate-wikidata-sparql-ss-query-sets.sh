# The parameters we've used to run the SPARQL Wikidata query generator

# Simple query, usually no more than 1 edge starting from the source.
python3 ./generate-wikidata-sparql-ss-queries.py "(<http://www.wikidata.org/prop/direct/P131>)*" > "wikidata-ss-rs-1.txt" 192846
# Simple query but more than 1 edge starting from the source.
python3 ./generate-wikidata-sparql-ss-queries.py "(<http://www.wikidata.org/prop/direct/P279>)*" > "wikidata-ss-rs-2.txt" 192847
# More complex query.
python3 ./generate-wikidata-sparql-ss-queries.py "((<http://www.wikidata.org/prop/direct/P279>|<http://www.wikidata.org/prop/direct/P31>)/((<http://www.wikidata.org/prop/direct/P279>)*|(<http://www.wikidata.org/prop/direct/P31>)*))" > "wikidata-ss-rs-3.txt" 192848
# Limited length query, many state query.
python3 ./generate-wikidata-sparql-ss-queries.py "(((((<http://www.wikidata.org/prop/direct/P31>/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)/(<http://www.wikidata.org/prop/direct/P279>)?)" > "wikidata-ss-rs-4.txt" 192849
# Searching the siblings.
python3 ./generate-wikidata-sparql-ss-queries.py "((^<http://www.wikidata.org/prop/direct/P161>/<http://www.wikidata.org/prop/direct/P161>))/((^<http://www.wikidata.org/prop/direct/P161>/<http://www.wikidata.org/prop/direct/P161>))*" > "wikidata-ss-rs-5.txt" 192850
