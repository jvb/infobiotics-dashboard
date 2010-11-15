## modules within modules 
#
#def module2():
#    r1 = reaction()
#    r2 = reaction()
#    return r1, r2
#
#def module(var, var_with_default='a'): #TODO
#    r1 = reaction(products=var)
#    r2 = reaction(reactants=var_with_default)
##    r3, r4 = module('c') # infinite recursion!
#    r3, r4 = module2()
##    return r1, r2, r3, r4
#    return {'a':r1, 'b':r2, '1':r3, 'atas':r4}
#
#class HasModule(compartment):
#    module1 = module('b')
#    c = compartment(x=species(10))
#c = HasModule()
#print [(r.id, r) for r in c._reactions()]
##print c._get_item('a')
##print c._get_item('x')
#exit()
