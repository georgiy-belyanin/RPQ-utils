import re
import sys

input_fname = sys.argv[1]
output_fname = sys.argv[2]

s_exp = re.compile(r"^<http://yago-knowledge.org/resource/(\S+)>$")
s_exp_1 = re.compile(r"^<(\S+)>$")

p_exp = re.compile(r"^<http://yago-knowledge.org/resource/(\S+)>$")

# entity
o1_exp = re.compile(r"^<http://yago-knowledge.org/resource/(\S+)>$")

# string
o2_exp = re.compile(r'^"((?:[^"\\]|\\.)*)"$')

# something with schema
o3_exp = re.compile(r'^"((?:[^"\\]|\\.)*)"\^\^<http://yago-knowledge.org/(\S+)>$')

# something with schema
o3_exp_2 = re.compile(r'^"((?:[^"\\]|\\.)*)"\^\^<http://yago-knowledge.org/resource/(\S+)>$')

# something with schema
o3_exp_3 = re.compile(r'^"((?:[^"\\]|\\.)*)"\^\^<http://www.w3.org/2001/XMLSchema#(\S+)$')

# string with idiom
o4_exp = re.compile(r'^"((?:[^"\\]|\\.)*)"@(.+)$')

# other url
o5_exp = re.compile(r"^<(.+)>$")

# point
o6_exp = re.compile(r'^"((?:[^"\\]|\\.)*)"\^\^<http://www\.opengis\.net/ont/geosparql#wktLiteral>$')

# anon
o7_exp = re.compile(r'^_:\w+$')

# math
o8_exp = re.compile(r'^"((?:[^"\\]|\\.)*)"\^\^<http://www\.w3\.org/1998/Math/MathML>$')

anon_count = 0

with open(input_fname, 'r', encoding='utf-8') as input_file, \
     open(output_fname, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        l = line.split()
        s = l[0]
        p = l[1]
        o = ' '.join(l[2:-1])

        #print(line, end='')
        m_s = s_exp.match(s) or s_exp_1.match(s)
        m_p = p_exp.match(p)

        m_o = o1_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->{m_o.groups()[0]} :{m_p.groups()[0]}\n')
            continue

        m_o = o2_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o3_exp_2.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o3_exp_3.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o3_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o4_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]} language:"{m_o.groups()[1]}"\n')
            continue

        m_o = o5_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o7_exp.match(o)
        if m_o is not None:
            anon_count += 1
            output_file.write(f'{m_s.groups()[0]}->_a{anon_count} :{m_p.groups()[0]}\n')
            continue

        print(line)
        print("Unimplemented")
        break





        m_o = o6_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue

        m_o = o8_exp.match(o)
        if m_o is not None:
            output_file.write(f'{m_s.groups()[0]}->"{m_o.groups()[0]}" :{m_p.groups()[0]}\n')
            continue
