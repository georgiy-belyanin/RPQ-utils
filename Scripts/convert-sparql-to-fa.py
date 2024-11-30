from __future__ import annotations

import os
import sys
import os as pyformlang
#from pyformlang.regular_expression.regex import Regex

mm_prelude = """%%MatrixMarket matrix coordinate pattern general
%%GraphBLAS type bool
"""

if len(sys.argv) < 4:
    print("Converts SPARQL query set into sets of adjacency matrices.")
    print("The script loads the edge-labeled graph with enumerated vertices and labels and")
    print("maps input SPARQL regular queries into an NFAs represented by adjacency matrix")
    print("decomposition.")

    print("Usage: python3 ./convert-sparql-to-fa.py <queries> <graph> <output-dir>")
    print()

    print("It's expected for the input queries file lines to be in such format:")
    print("<query number>,<source or ?var> <query> <destination or ?var>")
    print("Example:")
    print("1,<Q10281806> (<P131>)* ?x1")
    print("2,<Q11193> (<P279>)* ?x1")
    print()
    print("It's expected for the input graph to be represented in the following format:")
    print("\t- '<output-dir>/<number>.txt' is an adjacency matrix in Matrix-Market format")
    print("\t  for the label <number>")
    print("\t- '<output-dir>/vertices.txt' is a map from vertices to its number")
    print("\t- '<output-dir>/edges.txt' is a map from edges to its number")
    print("For getting it, refer to convert-nt-to-mm script")
    print()

    print()
    print("Resulting output:")
    print("\t- '<query number>/<label>.mtx' is an adjacency matrix for the label")
    print("\t- '<query number>/meta.txt' is query meta, starting/final vertices,")
    print("\t  and used labels")
    exit(-1)

class RegAutomaton:
    """
    Automaton representation of regular grammar
    """
    def __init__(self, regex: Regex):
        self.enfa = regex.to_epsilon_nfa().minimize()

        self.states = self.enfa.states
        self.num_states = len(self.states)
        self.symbols = self.enfa.symbols

        self.enum_states = dict(zip(self.states, range(self.num_states)))
        self.start_states = [
            self.enum_states[state] for state in self.enfa.start_states
        ]
        self.final_states = [
            self.enum_states[state] for state in self.enfa.final_states
        ]


    def from_regex_txt(path) -> RegAutomaton:
        with open(path, "r") as file:
            s = file.readline().strip()
            regex = Regex(s)

            return RegAutomaton(regex)

    def load_adjacency_pairs(self) -> None:
        """
        Creates boolean matrices for self automaton
        """
        res = []
        for src_node, transition in self.enfa.to_dict().items():
            for symbol, tgt_node in transition.items():
                res.append((symbol, self.enum_states[src_node] + 1, self.enum_states[tgt_node] + 1))
        return res

PROP_PREFIX = 'http://www.wikidata.org/prop/direct/'
ENTITY_PREFIX = 'http://www.wikidata.org/entity/'


vertices = {}
edges = {}

print('Reading vertices...')
with open(f'{sys.argv[2]}/vertices.txt', 'r') as f:
    for i in f:
        v, n = i.rsplit(maxsplit=1)
        vertices[v] = n

print('Reading edges...')
with open(f'{sys.argv[2]}/edges.txt', 'r') as f:
    for i in f:
        e, n = i.rsplit(maxsplit=1)
        edges[e] = n

print('Processing queries...')

with open(sys.argv[1], 'r') as f:
    for raw_query in f:
        source, query, target = raw_query.split()
        t = source.find(',')
        number = source[:t]
        source = source[t+1:]

        source_s = source[source.rfind('/') + 1:-1]
        target_s = target[target.rfind('/') + 1:-1]
        query_s = query.replace(PROP_PREFIX, '').replace('<', '').replace('>', '').replace('/', ' ').replace(')?', '|$)')
        while '+' in query_s:
            end = query_s.rfind('+')
            j = end - 2
            opened_p = 1 if query_s[end - 1] == ')' else 0
            while opened_p != 0:
                if query_s[j] == ')':
                    opened_p += 1
                elif query_s[j] == '(':
                    opened_p -= 1
                j -= 1
            start = j + 1
            body = query_s[start:end]
            query_s = f'{query_s[:start]} ({body} {body}*) {query_s[end + 1:]}'

        # Actually I haven't implemented a proper conversion of arbitary 2-RPQ into a parsable one
        # The script parses only a specific case of them in which inverse labels start with a ^

        #while '^' in query_s:
        #    start = query_s.find('^')
        #    j = start + 2
        #    opened_p = 1 if query_s[start + 1] == '(' else 0
        #    while opened_p != 0:
        #        if query_s[j] == '(':
        #            opened_p += 1
        #        elif query_s[j] == ')':
        #            opened_p -= 1
        #        j -= 1
        #    start = j + 1
        #    body = query_s[start:end]
        #    query_s = f'{query_s[:start]}(^{body}){query_s[end + 1:]}'
        #TODO: HANDLE 2RPQS
        #if ('^' in query_s)


        print(number, source_s, query_s, target_s)

        r = RegAutomaton(Regex(query_s))

        if source_s[0] != '?' and f'<{ENTITY_PREFIX}{source_s}>' not in vertices or target_s[0] != '?' and f'<{ENTITY_PREFIX}{target_s}>' not in vertices:
            print(f"{number} skipped")
            continue

        not_ok = False
        for symbol in r.symbols:
            if (f'<{PROP_PREFIX}{symbol}>' not in edges) and (f'<{PROP_PREFIX}{str(symbol)[1:]}>' not in edges):
                print(f"{number} skipped")
                not_ok = True
        if not_ok:
            continue
        source_n = vertices[f'<{ENTITY_PREFIX}{source_s}>'] if source_s[0] != '?' else '0'
        target_n = vertices[f'<{ENTITY_PREFIX}{target_s}>'] if target_s[0] != '?' else '0'


        query_dir = f'{sys.argv[3]}/{number}/'
        try:
            os.mkdir(query_dir)
        except:
            pass

        with open(f'{query_dir}meta.txt', 'w') as meta_f:
            meta_f.write(f'{source_n} {target_n}\n')
            meta_f.write(f'{len(r.start_states)} ')
            for symbol in r.start_states:
                meta_f.write(f'{symbol + 1} ')
            meta_f.write('\n')
            meta_f.write(f'{len(r.final_states)} ')
            for symbol in r.final_states:
                meta_f.write(f'{symbol + 1} ')
            meta_f.write('\n')
            meta_f.write(f'{len(r.symbols)} ')
            for symbol in r.symbols:
                symbol_n = edges[f'<{PROP_PREFIX}{symbol}>'] if str(symbol)[0] != '^' else '-' + edges[f'<{PROP_PREFIX}{str(symbol)[1:]}>']
                meta_f.write(f'{symbol_n} ')

        with open(f'{query_dir}raw.txt', 'w') as raw_f:
            raw_f.write(raw_query)

        transitions = r.load_adjacency_pairs()
        for symbol in r.symbols:
            symbol_n = edges[f'<{PROP_PREFIX}{symbol}>'] if str(symbol)[0] != '^' else '-' + edges[f'<{PROP_PREFIX}{str(symbol)[1:]}>']
            with open(f'{query_dir}{symbol_n}.txt', 'w') as symbol_f:
                entry_c = 0
                for pred, src, target in transitions:
                    if pred != symbol:
                        continue
                    entry_c += 1

                symbol_f.write(mm_prelude)
                symbol_f.write(f'{max(len(r.states), 2)} {max(len(r.states), 2)} {entry_c}\n')
                for pred, src, target in transitions:
                    if pred != symbol:
                        continue
                    symbol_f.write(f"{src} {target}\n")

