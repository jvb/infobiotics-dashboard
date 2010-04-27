# -*- coding: utf-8 -*-
# an example of using the libmcss python api
# this is essentially the mcss command line simulator implemented in python
# copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
# released under GNU GPL version 3

import mcss
import sys

# parse command line and read in parameters
parameters = mcss.SimulationParameters()
parameters.read(sys.argv)

# create p-system from parameters specified in parameter file
psystem = mcss.Psystem(parameters)

# run simulation
psystem.execute(parameters.max_time)

# tidy up
del parameters
del psystem
