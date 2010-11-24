from infobiotics.language import *

cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)] # up, right, down, left 

class diffusion(compartment):
    _defines_template = 1
    #TODO a -> (0, 1) 10
#    rxns = ['a -> a 1 # (%s,%s)' % (x, y) for x, y in cardinals]
    rxns = ['a -> a 1 # (%s,%s)' % (_x, _y) for _x, _y in cardinals]
#    del x, y #TODO otherwise these variables get left in class, or prefix with underscore

class rxn(compartment):
    _defines_template = 2
    r1 = 'a -> b 1'

class E(compartment):
    _uses_templates = [1]

class B(compartment):
    _uses_templates = [2]

#for r in diffusion.reactions:
#    print r.str(comment=True)
#for i in diffusion.species:
#    print i.str()
#print
#
#for r in rxn.reactions:
#    print r.str(comment=True)
#print

d = diffusion(
    rxn(),
    'c -> d 5',
    a=10,
    b=20
)
#for i in d.reactions:
#    print i.str(comment=True)
#for i in d.species:
#    print i.str()
#for i in d.compartments:
#    print i.str()
#print d.str()
#print d

#print repr(d)

#print diffusion
print repr(diffusion)

