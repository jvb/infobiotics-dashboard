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
    Regex(regex='.*'), #TODO regex for r1: a + b [c + d ]_l -k_on-> e + f[  g + h]_j k_on   =     0.01
    Instance('reaction'),
    List(Instance('reaction')),
#    List(List(Instance('Reaction'))),
#    List(Tuple(Instance('Reaction'))),
    Tuple(Instance('reaction')),
#    Tuple(List(Instance('Reaction'))),
#    Tuple(Tuple(Instance('Reaction'))),
    #TODO Dict(Str, Reaction)
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


class base(HasTraits):

    id = Str

    name = Property(Str)
    def _get_name(self):
        return self._name if self._name != '' else self.id
    def _set_name(self, name):
        self._name = name
    _name = Str


class reaction(base):
    '''
class Reaction(HasTraits):
    reactants = List(Str)
    products = List(Str)
    constant = Float
    def __str__(self):
        return '%s -> %s' % (self.reactants, self.products)
    def __init__(self, reactants, products, constant=0.0):
        ''' Allows instantiation of reactions with only a pair of strings (or lists of strings). '''
        if isinstance(reactants, str):
            reactants = [reactant.strip() for reactant in reactants.split(',')]
        self.reactants = reactants
        if isinstance(products, str):
            products = [product.strip() for product in products.split(',')]
        self.products = products
        self.constant = constant
    '''

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


class species(base):

    quantity = Quantity

    def __init__(self, quantity, **traits):
        self.quantity = quantity
        super(species, self).__init__(**traits)

    def __str__(self):
        return '%s=%s' % (self.name, self.quantity)

#class gene(species):
##    sequence = dna
#    pass


def id_generator(prefix=''):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1

# from sbml
compartment_id_generator = id_generator('c')
species_id_generator = id_generator('s')
constant_id_generator = id_generator('k')
reaction_id_generator = id_generator('r')


def filter_by_type(dict, type):
    filtered = []

    def fix_missing_id(item, id):
        if hasattr(item, 'id') and item.id == '':
            item.id = id

    def append_item(item, id):
        if isinstance(item, type):
            fix_missing_id(item, id)
            filtered.append(item)
        elif hasattr(item, '__iter__'):
            for i in item:
                append_item(i, globals()['%s_id_generator' % type.__name__].next())

    for id, item in dict.items():
        if id.startswith('_'): continue # skip private keys #TODO necessary now that __dir does this?
        append_item(item, id)

    return filtered

class compartment(base):
    volume = Float #TODO make into a litre/length**3 validated Trait
    __ = Any
    _ = CompartmentOrSpeciesOrReactions

#    def __class_dir(self):
#        return [name for name in dir(self.__class__) if not name.startswith(('__', '_')) and not callable(getattr(self.__class__, name)) and name != 'wrappers']
#
#    def __class_dir_items(self):
#        return dict([(name, getattr(self.__class__, name)) for name in self.__class_dir()])

    def __dir(self):
        return [name for name in dir(self) if not name.startswith(('__', '_')) and not callable(getattr(self, name)) and name != 'wrappers']

    def __dir_items(self):
        return dict([(name, getattr(self, name)) for name in self.__dir()])

    def __attributes(self, type):
        d = dict(self.__class__.__dict__) # copy items from class dictproxy
        d.update(self.__dict__) # overwrite traits with instances from self
        d.update(self.__dir_items()) # catches attributes of superclasses
        return filter_by_type(d, type)

    def __instance_attributes(self, type):
        d = dict(self.__dict__)
#        d.update(self.__dir_items())
        return filter_by_type(d, type)

    def __class_attributes(self, type):
        d = dict(self.__class__.__dict__)
        d.update(self.__dir_items())#d.update(self.__class_dir_items())
        return filter_by_type(dict(d), type)

    def _species(self):
        #TODO self.__attributes(int)
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
        #TODO self.__attributes(str)
        print self.__attributes(tuple)
        return self.__attributes(reaction)

    def _instance_reactions(self):
        return self.__instance_attributes(reaction)

    def _class_reactions(self):
        return self.__class_attributes(reaction)


## multiple inheritance
#
#class c1(compartment):
#    x = compartment(name='1')
#    a = species(1)
#    b = reaction()
#    c = species(3)
#
#class c2(compartment):
#    x = compartment(name='2')
#    c = species(2)
#
#class C(c2, c1):
#    pass
#
#c = C()
#assert c.c.quantity == 2 # c in C2 overrides c in C1
##print [i.name for i in c._compartments()]
##print [str(i) for i in c._species()]
##print [i.name for i in c._reactions()]


# modules

def module(var, var_with_default='a'): #TODO
    r1 = reaction(products=var)
    r2 = reaction(reactants=var_with_default)
    return r1, r2

class HasModule(compartment):
    module1 = module('b')
c = HasModule()
print c.module1
print c._reactions() #TODO look inside tuples for reactions
exit()

#TODO modules within modules 


## knockout as subclass of wildtype
#class WildType(compartment):
#    species_rsmA = 1
#class rsmAKnockout(WildType):
#    species_rsmA = 0
#
#
## use 2D numpy array for lattice
#def find_empty_2D_array_positions(array):
#    empty = []
#    for x, a in enumerate(np.equal(array, None)):
#        for y, i in enumerate(a):
#            if i:
#                empty.append((x, y))
#    return empty
#
#class LPPSystem(HasTraits):
#    distribution = Array(dtype=compartment)
#    def empty_positions(self):
#        return find_empty_2D_array_positions(self.distribution)
#
## aliases
#lpp = LPPSystem
#sps = compartment
#SpatialDistribution = np.array
#
#class model(LPPSystem):
#    distribution = SpatialDistribution([[rsmAKnockout() if (x == 4 and y == 4) else WildType() for x in range(10)] for y in range(10)])
#
#m = model()
##print m.distribution
#print m.distribution[4, 4]
#m.distribution[4, 4] = None
#print m.empty_positions()
