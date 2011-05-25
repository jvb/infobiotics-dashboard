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
	unsigned int i, j, k, ***amounts;

	// parse command line and read in parameters
	SimulationParameters parameters;
	parameters.read(argc, argv);

	// make sure log to memory parameter set
	parameters.log_memory = true;

	// create p-system from parameters specified in parameter file
	Psystem psystem(parameters);

	// run simulation
	psystem.execute(parameters.max_time);

	// output amounts
	amounts = psystem.getAmountsDataset();
	for(i = 0; i < psystem.getNumTimepoints(); i++)
		for(j = 0; j < psystem.getNumSpecies(); j++)
			for(k = 0; k < psystem.getNumCompartments(); k++)
				printf("time=%f species=%ld compartment=%ld level=%ld\n", \
						i * parameters.log_interval, j, k, amounts[j][k][i]);

	return 0;
}
