'''Creates the dependency graph for a set of reactions.

Answers the question: 
    Having applied a reaction, which reactions do I now need to update the 
    propensities for?

'''
from multiset import multiset
import itertools
from pprint import pprint
import subprocess
import random

def random_multiset():
    '''Returns a multiset with 1 or 2 species.'''
    m = {}
    n = random.randint(1, 2)
    while n > 0:
        o = random.randint(1, n)
        n -= o
        x = random.choice('abcdefghijklmnopqrstuvwxyz')
        m[x] = o
    return m 

def id_generator(prefix):
    i = 0
    while True:
        i += 1
        yield '%s%d' % (prefix, i)

r_id_generator = id_generator('r')

class r(object):
    def __init__(self, reactants={}, products={}):
        self.id = r_id_generator.next()
        self.reactants = multiset(reactants)
        self.products = multiset(products)
    def __str__(self):
        return '"%s: %s -> %s"' % (self.id, self.reactants, self.products)
    def __repr__(self):
        return str(self)
        return self.id

rs = [
#    # whiteboard example
#    r({'a':1}, {'a':1, 'b':1}),
#    r({'b':1}, {'c':1}),
#    r({'a':1}, {'c':1}),
#    r({'d':1}, {'e':1}),
    # Gibson and Bruck
    r({'a':1, 'b':1}, {'c':1}),
    r({'b':1, 'c':1}, {'d':1}),
    r({'d':1, 'e':1}, {'e':1, 'f':1}),
    r({'f':1}, {'d':1, 'g':1}),
    r({'e':1, 'g':1}, {'a':1}),
]
#rs = [r(random_multiset(), random_multiset())for i in range(100)]

dg = {}

def dg_add(rx, ry):
    try:
        g = dg[rx]
        g.add(ry)
    except KeyError:
        dg[rx] = set([ry])

# find dependencies for all r in rs against all r in rs
for rx, ry in itertools.product(rs, rs):
    for r in set(rx.reactants.keys() + rx.products.keys()):
        # add ry to rx's dependencies if r in ry.reactants and rx produces less or more of r than it consumes
        if r in ry.reactants.keys() and rx.reactants[r] != rx.products[r]:
            dg_add(rx, ry)

# convert to list
for k in dg.keys():
    v = dg[k]
    dg[k] = list(v)
pprint(dg)
#exit()
#echo "digraph G {Hello->World}" | dot -Tpng >hello.png
dot = 'digraph G {'
for k, v in dg.iteritems():
    for d in v: 
        dot += '%s->%s;\n' % (k, d) 
dot += '}'
subprocess.Popen("echo '%s' | dot -Tpng > dg.png" % dot, shell=True)
