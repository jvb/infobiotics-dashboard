// an example of using the libmcss api
// runs a simulation logging data to memory
// then prints out the species levels
// copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
// released under GNU GPL version 3

#include <iostream>
#include <mcss/mcss.h>

using namespace Simulation;

int main(int argc, char **argv)
{
	unsigned long i = 1;
	
	// parse command line and read in parameters
	SimulationParameters parameters;
	parameters.read(argc, argv);

	// perform 100 simulations
	while(i <= 100) {
		std::cout << "performing simulation " << i++ << "\n";
	
		// create p-system from parameters specified in parameter file
		Psystem *psystem = new Psystem(parameters);

		// run simulation
		psystem->execute(parameters.max_time);

		// free memory
		delete psystem;
	}

	return 0;
}
