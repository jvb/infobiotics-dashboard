// an example of using the libmcss api
// runs a simulation logging data to memory
// then prints out the species levels
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#include <stdio.h>
#include <mcss/mcss.h>

using namespace Simulation;

int main(int argc, char **argv)
{
	unsigned int i, j, ***amounts;
	double timestep, time;

	// parse command line and read in parameters
	SimulationParameters parameters;
	parameters.read(argc, argv);

	// make sure log to memory parameter set
	parameters.log_memory = true;

	// create p-system from parameters specified in parameter file
	Psystem psystem(parameters);

	// set time to step simulation over
	timestep = 1.0;

	time = timestep;
	while(time < parameters.max_time) {
		// run simulation for specified interval
		psystem.execute(timestep);

		// output amounts for time interval
 		printf("\n*** interval %f-%f\n", time - timestep, timestep);
 		for(i = 0; i < psystem.getNumSpecies(); i++)
 			for(j = 0; j < psystem.getNumCompartments(); j++)
 				printf("time=%f species=%ld compartment=%ld level=%ld\n", \
 						timestep, i, j, \
 						psystem.getSpeciesLevel(i, j));

		// update overall time
		time += timestep;
	}

	return 0;
}
