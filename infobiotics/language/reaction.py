__all__ = ['reaction']

from enthought.traits.api import Either, Str, List, Tuple, Dict, Int, Property, Float, Instance
from core import named, multiset, Quantity

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

Rate = Either(
    Float,
    Instance(Quantity) # use quantities for rates (time**-1)
)

class reaction(named):
    '''
class Reaction(HasTraits):
    reactants = List(Str)
    products = List(Str)
    constant = Float
    def __str__(self):
        return '%s -> %s' % (self.reactants, self.products)
    def __init__(self, reactants, products, constant=0.0):
        \''' Allows instantiation of reactions with only a pair of strings (or lists of strings). \'''
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
                reactants = multiset(reactants)
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

    rate = Rate

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


