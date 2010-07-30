=====
 mcss
=====

-----------------------------------------
multi-compartmental stochastic simulator
-----------------------------------------

:Author: jpt@cs.nott.ac.uk
:Date:   2010-02-06
:Copyright: Infobiotics
:Version: 0.0.34
:Manual section: 1

.. TODO: authors and author with name <email>

SYNOPSIS
========

  mcss PARAMETERFILE [PARAMETER=VALUE] ...

DESCRIPTION
===========

mcss is an application for simulating multi-compartment stochastic P system models. mcss takes a model specified in SBML and simulates it using the multi-compartment Gillespie algorithm, see http://www.infobiotic.org/infobiotics-workbench/modelSimulation/modelSimulation.html. A large number of spatially-distributed compartments containing many chemical species, reactions and transportation channels can be simulated. Templates can be specified which define a set of reactions which can be reproduced in many compartments. mcss is being used to develop Systems/Synthetic Biology computational models of plant systems and bacterial colonies. 

OPTIONS
=======

model_file=<file>					
input model filename (parameter required)

max_time=<double>					
time in seconds to run model for (parameter required)

simulation_algorithm=<dm|ldm>				
simulation algorithm to use dm = direct method ldm = logarithmic direct method

data_file=<file>					
file to save simulation data to (default simulation.h5)

model_format=<sbml|lpp>					
format which model is specified in sbml or lpp (Lattice Population P system)

log_type=<levels|reactions>				
type of log to save reactions = save data on each reaction performed levels = save levels of species periodically (default reactions)

log_interval=<double>			
interval (seconds) to save species level data (default 1.0)

duplicate_initial_amounts=<1|0> 		
duplicate initial amounts of species given in templates (default 0)

seed=<ULONG> 								
random number generator seed if set to 0 use a random seed

log_propensities=<1|0>					
log rule propensities for each compartment (default 0)

log_degraded=<1|0>						
log levels of degraded species (default 0)

log_memory=<1|0>							
log data to memory (default 0)

periodic_x=<1|0>							
use periodic boundary condition for x axis (default 0)

periodic_y=<1|0>							
use periodic boundary condition for y axis (default 0)

periodic_z=<1|0>							
use periodic boundary condition for z axis (default 0)

show_progress=<1|0>						
output current log interval to screen (default 0)

SEE ALSO
========

* pmodelchecker
* poptimizer
