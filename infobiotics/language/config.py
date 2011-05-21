'''Configuration module containing global variables that are used to the
Infobiotics modelling language. 

This is a variation of the singleton pattern where this module, which must be
imported by other modules to be used, is the singleton. Values can be changed
by referencing the module and the attribute, e.g. 
    >>> config.k_on_max = 2e6 * 1 / (M * s)
but bear in mind that those changes are not retroactive and so should really
be made prior to creating model objects or global variables that may rely on
them. (TODO or imports?)

'''

from infobiotics.commons.quantities.units import * # used by time_units and k_on_max

# change behaviour of repr for sequences 
from __builtin__ import repr as long_repr
from repr import repr as short_repr
repr = long_repr

# change how float attributes are handled by compartments
warn_about_floats = True

## a shared logger, e.g. >>> from config import log; log.error('Help!')
#import logging
#log = logging.getLogger('main')
#log.addHandler(logging.StreamHandler())
##log.setLevel(logging.DEBUG)
#log.setLevel(logging.WARN)
##log.setLevel(logging.ERROR)
from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)

# time_units is unit quantity used to rescale reaction rates 
#time_units = millseconds
time_units = seconds
#time_units = minutes
#time_units = hours

# default rate constants
zero = 0 # a stochastic rate constant of zero (time units don't matter because zero is zero whatever the unit and propensity will always be zero)
k_on_max = 1e6 * 1 / (M * s) # the maximal (deterministic) rate of association between two reactants (ref. Northrup), used to calculate k_off from K_D


joiner = '_' # used when, for example, 'a' is complexed with 'b' to produce 'a_b'
def join(*args):
    '''Accepts multiple args and passes them to str.join as a tuple.'''
    if len(args) == 1:
        return joiner.join(*args)
    return joiner.join(args)
