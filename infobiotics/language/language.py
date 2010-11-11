from enthought.traits.api import *
from quantities import Quantity # importing imports sum which overwrite builtin
import numpy as np

# compound trait definitions

Compartments = Either(
    Instance('compartment'),
    List(Instance('compartment')),
    Tuple(Instance('compartment')),
)

Species = Either(
#    Int,
    Instance('species'),
    List(Instance('species')),
    Tuple(Instance('species')),
    DictStrInt, # initial_amounts = {'a':1} 
#    ListStr, Tuple(Str) # alphabet?
)

Reactions = Either(
    Str, #TODO regex for r1: a + b [c + d ]_l -k_on-> e + f[  g + h]_j k_on   =     0.01
    Instance('reaction'),
    List(Instance('reaction')),
#    List(List(Instance('Reaction'))),
#    List(Tuple(Instance('Reaction'))),
    Tuple(Instance('reaction')),
#    Tuple(List(Instance('Reaction'))),
#    Tuple(Tuple(Instance('Reaction'))),
)

CompartmentOrSpeciesOrReactions = Either(
    Instance('compartment'),
    List(Instance('compartment')),
    Tuple(Instance('compartment')),

#    Int,
    Instance('species'),
    List(Instance('species')),
    Tuple(Instance('species')),
    DictStrInt, # initial_amounts = {'a':1} 
#    ListStr, Tuple(Str) # alphabet?

    Str, #TODO regex for r1: a + b [c + d ]_l -k_on-> e + f[  g + h]_j k_on   =     0.01
    Instance('reaction'),
    List(Instance('reaction')),
#    List(List(Instance('Reaction'))),
#    List(Tuple(Instance('Reaction'))),
    Tuple(Instance('reaction')),
#    Tuple(List(Instance('Reaction'))),
#    Tuple(Tuple(Instance('Reaction'))),
)

Reactants = Either(
    Str,
    List(Str, max_len=2),
    Tuple(Str),
    Tuple(Str, Str),
    Dict(Str, Int),
)

Products = Either(
    Str,
    List(Str),
    Tuple(Str),
    Tuple(Str, Str),
    Tuple(Str, Str, Str),
    Dict(Str, Int),
)


class reaction(HasTraits):
    ''' Only ',' and '+' are reserved symbols in species names. '''

    reactants = Property(Reactants)

    def _get_reactants(self):
        return self._reactants

    def _set_reactants(self, reactants):
        if isinstance(reactants, str):
            self._reactants = [j.strip() for i in reactants.split(',') for j in i.split('+')] # nice one-liner
        elif hasattr(reactants, '__iter__'):
            if isinstance(reactants, dict):
                from infobiotics.commons.counter import Counter
                reactants = Counter(reactants)
                if sum(reactants.values()) > 2:
                    raise ValueError('Too many reactants: %s' % reactants)
                else:
                    self._reactants = [k for k, v in reactants.items() for i in range(v)]
            else:
                if len(reactants) > 2:
                    raise ValueError('Too many reactants: %s' % reactants)
                else:
                    self._reactants = [r for r in reactants]

    products = Property(Products)

    def _get_products(self):
        return self._products

    def _set_products(self, products):
        if isinstance(products, str):
            self._products = [j.strip() for i in products.split(',') for j in i.split('+')]
        elif hasattr(products, '__iter__'):
            if isinstance(products, dict):
                self._products = [k for k, v in products.items() for i in range(v)]
            else:
                self._products = [r for r in products]

#TODO recast as unit tests
##r1 = reaction()
##r1.reactants = 'a + b'
##r2 = reaction(reactants='a, b')
##r3 = reaction(reactants=' a + b + c')
##r4 = reaction(reactants='a   ')
##r5 = reaction(reactants={'a':1, ' b':2, 'c  ':3, 'd, ':4, 'e + d':5})
#r6 = reaction(reactants=['a', 'b'])
##r7 = reaction(reactants=['a', 'b', 'c'])
#r7 = reaction(reactants={'a':1, ' b':1}, products=['a', 'b', 'c'])
#exit()

def module(var, var_with_default='a'): #TODO
    r1 = reaction(products=var)
    r2 = reaction(reactants=var_with_default)
    return r1, r2


class species(HasTraits):
    name = Str
    quantity = Quantity
    def __init__(self, quantity, **traits):
        self.quantity = quantity
        super(species, self).__init__(**traits)

#class gene(species):
##    sequence = dna
#    pass


def filter_by_type(dict, type):
    filtered = []
    for k, v in dict.items():

        # skip private keys
        if k.startswith('_'):
            continue

        # fix missing names
        if isinstance(v, type):
            if v.name == '':
                v.name = k
            filtered.append(v)

    return filtered


class compartment(HasTraits):
    name = Str
    __ = Any
    _ = CompartmentOrSpeciesOrReactions

    def __attributes(self, type):
        d = dict(self.__class__.__dict__) # copy items from class dictproxy
        d.update(self.__dict__) # overwrite traits with instances from self
        return filter_by_type(d, type)

    def __instance_attributes(self, type):
        return filter_by_type(self.__dict__, type)

    def __class_attributes(self, type):
        return filter_by_type(dict(self.__class__.__dict__), type)

    def _species(self):
        return self.__attributes(species)

    def _instance_species(self):
        return self.__instance_attributes(species)

    def _class_species(self):
        return self.__class_attributes(species)

    def _compartments(self):
        return self.__attributes(compartment)

    def _instance_compartments(self):
        return self.__instance_attributes(compartment)

    def _class_compartments(self):
        return self.__class_attributes(compartment)

    def _reactions(self):
        return self.__attributes(reaction)

    def _instance_reactions(self):
        return self.__instance_attributes(reaction)

    def _class_reactions(self):
        return self.__class_attributes(reaction)






class WildType(compartment):
    species_rsmA = 1
class rsmAKnockout(WildType):
    species_rsmA = 0

# use 2D numpy array for lattice
def find_empty_2D_array_positions(array):
    empty = []
    for x, a in enumerate(np.equal(array, None)):
        for y, i in enumerate(a):
            if i:
                empty.append((x, y))
    return empty

class LPPSystem(HasTraits):
    distribution = Array(dtype=compartment)
    def validate_distribution(self):
        return find_empty_2D_array_positions(self.distribution)

SpatialDistribution = np.array
class Model(LPPSystem):
    # funny that 'and' gives the wrong distribution by 'or' doesn't
#    distribution = np.array([[WildType() if (x != 4 or y != 4) else rsmAKnockout() for x in range(10)] for y in range(10)])
#    distribution = np.array([[WildType() if (x != 4 and y != 4) else rsmAKnockout() for x in range(10)] for y in range(10)])
    # rephrase it so that exception comes first
    distribution = SpatialDistribution([[rsmAKnockout() if (x == 4 and y == 4) else WildType() for x in range(10)] for y in range(10)])


m = Model()
#print m.distribution
#print m.distribution[4,4]
m.distribution[4, 4] = None
print m.validate_distribution()
print m.distribution.shape
print np.array([]).shape
