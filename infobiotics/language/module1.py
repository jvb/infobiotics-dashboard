from infobiotics.language import *

#cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)] # up, right, down, left 
#
#class diffusion(compartment):
#    _defines_template = 1
#    #TODO a -> (0, 1) 10
##    rxns = ['a -> a 1 # (%s,%s)' % (x, y) for x, y in cardinals]
#    rxns = ['a -> a 1 # (%s,%s)' % (_x, _y) for _x, _y in cardinals] + [compartment(), 5]
##    del x, y #TODO otherwise these variables get left in class, or prefix with underscore
#
#class rxn(compartment):
#    _defines_template = 2
#    r1 = 'a -> b 1'
#
#class E(compartment):
#    _uses_templates = [1]
#
#class B(compartment):
#    _uses_templates = [2]
#
##for r in diffusion.reactions:
##    print r.str(comment=True)
##for i in diffusion.species:
##    print i.str()
##print
##
##for r in rxn.reactions:
##    print r.str(comment=True)
##print
#
#d = diffusion(
#    compartment(),
#    rxn(),
#    'c -> d 5',
#    a=10,
#    b=20
#)
##for i in d.reactions:
##    print i.str(comment=True)
##for i in d.species:
##    print i.str()
##for i in d.compartments:
##    print i.str()
##print d.str()
##print d
#
##print repr(d)
#
##print diffusion
##print repr(diffusion)


me = [compartment(), species('b', 20), 666, 'a 0.1-> b', [compartment(label='x', r='b -> a 5', volume=3)]]
c = compartment(
    compartment(),
    a=10,
    d=compartment(),
    m=me
)
#print c.repr()
print eval(c.repr()).str()
print
##class c(compartment):
#class d(compartment): pass
#class e(compartment): pass
#class f(e): pass 
#class c(f, compartment):
#    a = 11
#    d = compartment(r='a ->c 22', volume=2)
#    m = me
##    f = .5
##    volume = 20
##print c.__metaclass__
##exit()
##print c
##print repr(c)
##print d.repr()
##print e.repr()
#lines = c.repr().split('\n')
#import string
#for i, e in enumerate(lines): 
#    print string.zfill(i, len(str(len(lines)))), e  
##print locals()
##print globals()
#print eval(c.repr()).str()
##print c.str()
