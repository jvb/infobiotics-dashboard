from compartments import *
import numpy as np
from enthought.traits.api import Array

# knockout as subclass of wildtype
class WildType(Compartment):
    species_rsmA = 1
class rsmAKnockout(WildType):
    species_rsmA = 0
#print WildType()._species_names_and_values()
#print rsmAKnockout()._species_names_and_values()

# override initial amounts in 1 of 100 compartments

# differential distribution of compartments 
#print [WildType() if i != 1 else rsmAKnockout() for i in range(3) ]

# gaussian distribution of rate constants

# reuse numerical distributions in several places of the model


# encapsulate Jamie's modelling process in one file
'''
1. rate conversion from deterministic to stochastic
2. set rate constants

3. amounts conversion from concentration to molecules
4. set initial amounts



'''

# use quantities for rates - time**-1

# default quantites for rates

'''
initial amounts in concentrations get converted to molecules (requires volume)
    general pattern seems to be:
        1. allow amounts to specified via species_X attributes (fairly strict typing)
        2. use __init__ or factory_functions for coercing input (for unreasonable difficult typing)
        3. use a getter/accessor to get the summary of the unknown attribute values
    so in this instance we can allow amounts to specified in various units (or without using 
        defaults for coercion) and get everything in the same units via a getter

'''

# export to SBML - see sbml.py

# export to IML - removing bad chars, etc. 


# create Models algorithmically 


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
#    distribution = Array(dtype=Compartment)
#    def validate_distribution(self):
#        return find_empty_2D_array_positions(self.distribution)
#            
#SpatialDistribution = np.array    
#class Model(LPPSystem):
#    # funny that 'and' gives the wrong distribution by 'or' doesn't
##    distribution = np.array([[WildType() if (x != 4 or y != 4) else rsmAKnockout() for x in range(10)] for y in range(10)])
##    distribution = np.array([[WildType() if (x != 4 and y != 4) else rsmAKnockout() for x in range(10)] for y in range(10)])
#    # rephrase it so that exception comes first
#    distribution = SpatialDistribution([[rsmAKnockout() if (x == 4 and y == 4) else WildType() for x in range(10)] for y in range(10)])
#
#    
#m = Model()
##print m.distribution
##print m.distribution[4,4]
#m.distribution[4,4] = None
#print m.validate_distribution()
#print m.distribution.shape
#print np.array([]).shape


# use multiple inheritance to combine modules

class Compartment1(Compartment):
    reaction1 = Reaction('a','b')
    reaction2 = Reaction('c','d')

class Compartment2(Compartment):
    reaction1 = Reaction('e','f')
    reaction3 = Reaction('g','h')

class Compartment3(Compartment1, Compartment2):
    ''' The composite of a Compartment1 and a Compartment2. '''
    pass

c3 = Compartment3()
c3.print_traits()
print c3._reactions_names_and_values() #FIXME doesn't work! Probably need to iterate over superclasses (mro) to harvest wildcard defined traits!

c1 = Compartment1()
print c1._reactions_names_and_values()
