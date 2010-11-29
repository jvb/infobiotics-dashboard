'''Configuration module containing global variables that are used to the
Infobiotics modelling language. 

This is a variation of the singleton pattern where this module, which must be
imported by other modules to be used, is the singleton.

'''

# change behaviour of repr for sequences 
from __builtin__ import repr as long_repr
from repr import repr as short_repr
repr = long_repr

# change how float attributes are handled by compartments
warn_about_floats = True

# a shared logger, e.g. from config import log; log.error('Help!')
import logging
log = logging.getLogger('main')
log.addHandler(logging.StreamHandler())
#log.setLevel(logging.DEBUG)
log.setLevel(logging.WARN)
#log.setLevel(logging.ERROR)

# 'time_units' is a string used to rescale time quantities like reaction rates 
#time_units = 'millseconds'
time_units = 'seconds'
#time_units = 'minutes'
#time_units = 'hours'

