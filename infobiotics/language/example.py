'''Example of deterministic to stochastic rate conversion.'''

class specieslist(list):
    '''Base class for reactants and products species lists.'''
    def __init__(self, *args):
        '''Accepts multiple args and passes them to list as a tuple.'''
        super(specieslist, self).__init__(args) # note missing *
class reactants(specieslist): pass
class products(specieslist): pass


# builtin modules

from infobiotics.language import *

rate = 1.0
zeroth = rate * molar * config.time_units ** -1
zeroth2 = rate * config.time_units ** -1 * molar
first = rate * config.time_units ** -1
second = rate * ((molar ** -1) * (config.time_units ** -1))
K_D = rate * molar
for rate in (zeroth, zeroth2, first, second, K_D):
    print rate, rate.dimensionality.items()

# correct
#assert reaction('->a', 1).has_zeroth_order_reactants() #TODO allow zeroth order reactions?
assert reaction('a ->  ', 1).has_first_order_reactants()
assert reaction('a + a ->  ', 1).has_second_order_homo_reactants()
assert reaction('a + b ->  ', 1).has_second_order_hetero_reactants()

# incorrect
assert not reaction('a ->  ', 1).has_second_order_homo_reactants()
assert not reaction('a ->  ', 1).has_second_order_hetero_reactants()

assert not reaction('a + a ->  ', 1).has_first_order_reactants()
assert not reaction('a + a ->  ', 1).has_second_order_hetero_reactants()

assert not reaction('a + b ->  ', 1).has_first_order_reactants()
assert not reaction('a + b ->  ', 1).has_second_order_homo_reactants()

assert not reaction('a + a + a ->  ', 1).has_first_order_reactants()
assert not reaction('a + a + a ->  ', 1).has_second_order_homo_reactants()
assert not reaction('a + a + a ->  ', 1).has_second_order_hetero_reactants()




exit()



def rxn(reactants=reactants(), products=products(), rate=zero):
    '''A factory function for reaction object.

    >>> print rxn(reactants('a', 'b'), products('a_b'), 0.1 * 1 / s)
    [ a + b ]_l -c-> [ a_b ]_l c=0.1 1/s 
        
    '''
    return reaction(reactants_inside=multiset(reactants), products_inside=multiset(products), rate=rate)

def degradation(reactant, rate=zero):
    '''One reactant degrades to nothing.'''
    return rxn(reactants(reactant), rate=rate)

def consumption(reactant, catalyst, rate=zero):
    '''One reactant is consumed (degraded) by a catalyst (protease?).'''
    return rxn(reactants(reactant, catalyst), products(catalyst), rate)

def annihilation(electron, positron, rate=zero):
    '''Two reactants annihilate each other.'''
    return rxn(reactants(electron, positron), rate=rate)

#print degradation('a', 0)
#print annilation('electron', 'positron', 1000)
#exit()

def association(s1, s2, complex, rate=zero):
#def association(s1_or_complex, s2=None, complex=None, rate=zero):
#    '''Two reactants combine to form one product, a complex of the two.'''
#    if s2 is None:
#        s1, s2 = s1_or_complex.split(joiner)
#    else:
#        s1 = s1_or_complex
#    if complex is None:
#        complex = join(s1, s2)
##    return '{s1} + {s2} -> {s1}_{s2} {rate}'.format(s1=s1, s2=s2, rate=rate)
    return rxn(reactants(s1, s2), products(complex), rate)

def dissociation(complex, s1, s2, rate=zero):
#def dissociation(complex_or_s1, s2=None, s1=None, rate=zero):
#    '''A complex dissociates into '''
##    if not all([complex, s1, s2]): #>>> dissociation()
##        raise ValueError("Either 'complex' or ('s1' and 's2') can be None but not both.")
#    if s2 is None:
#        s1, s2 = complex_or_s1.split(joiner)
#        complex = join(s1, s2)
#    else:
#        complex = complex_or_s1
#    if s1 is None:
#        pass
    return rxn(reactants(complex), products(s1, s2), rate)



def complexation(s1, s2=None, K_D=0 * molar, k_on=0 * 1 / (M * s), k_off=zero):
    if s2 is None:
        s1, s2 = s1.split('_')
    if K_D > 0:
        k_on = k_on_max
        k_off = k_on_max * K_D
    r1 = association(s1, s2, k_on)
    r2 = dissociation(s1, s2, k_off)
    return r1, r2

print complexation('s1', 's2', 0.5)

exit()




class bacteria(compartment):

    a = 10
    b = species('b', 0)

    r1 = 'a -> b 0.1'

    r2 = reaction('b 0.2-> a')

    r3 = reaction('b + b -> d 0.2', desc='complexation')





b = bacteria(
    degradation('a', 0.1),
    degradation('b', 0.2)
)

print b.str()
