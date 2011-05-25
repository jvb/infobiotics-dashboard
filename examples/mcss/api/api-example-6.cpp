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
	string name;
	unsigned long i, j;
	unsigned long sid1, sid2, sid3, sid4;  // species ids
	unsigned long rsid1, rsid2, rsid3;  // ruleset ids
	unsigned long rid1, rid2, rid3, rid4, rid5, rid6, lrid;  // rule ids
	unsigned long cid1, cid2, cid3;  // compartment ids
	unsigned long level;  // species level
	unsigned long num_reactants, reactants[2];
	unsigned long num_products, products[3];
	double reaction_constant;
	double max_time = 3600.0;  // maximum time to run simulation
	double timestep = 60.0;  // interval to step simulation for
	double time;  // current simulation time
	unsigned long nb = 3;

	// create empty p system
	Psystem *psystem = new Psystem();

	// set id of p system
	psystem->setId("test_model_1");

	// add some objects to p system
	name = "A";
	sid1 = psystem->addSpecies(name);

	// add some rulesets to p system
	// initialise ruleset
	name = "ruleset1";
	rsid1 = psystem->addRuleSet(name);
	// add rule to ruleset
	num_reactants = 1;
	reactants[0] = sid1;
	num_products = 1;
	products[0] = sid1;
	reaction_constant = 11.0;
	name = "rule1";
	rid1 = psystem->addRule(rsid1, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	// set rule as translocation rule (channel)
	psystem->setChannel(rsid1, rid1);

	// add some compartments to p system
	for(i = 0; i < nb; i++) {
		name = "compartment1";
		cid1 = psystem->addCompartment(name);
	}

	// add ruleset to compartments
	for(i = 0; i < nb; i++) {
		psystem->addRuleSetToCompartment(rsid1, i);
	}

	for(i = 0; i < (nb - 1); i++) {
		psystem->setRuleTarget(i, rsid1, rid1, i + 1);
	}

	for(i = 1; i < nb; i++) {
		lrid = psystem->cloneRule(i, rsid1, rid1);
		psystem->setReactionConstant(i, rsid1, lrid, 10.0);
		psystem->setRuleTarget(i, rsid1, lrid, i - 1);
	}

	// set initial species levels
	for(i = 0; i < nb; i++) {
		level = 1000;
		psystem->setSpeciesLevel(1, sid1, level);
	}

	// set volumes
	for(i = 0; i < nb; i++) {
		psystem->setCompartmentVolume(i, 5000);
	}


	// set simulation algorithm
	name = "dmq";
	psystem->setSimulationAlgorithm(name);

	// output initial amounts
	printf("\n*** initial levels\n");
	for(i = 0; i < psystem->getNumCompartments(); i++)
		for(j = 0; j < psystem->getNumSpecies(); j++)
			printf("time=%f compartment=%ld species=%ld level=%ld\n", \
					0.0, i, j, \
					psystem->getSpeciesLevel(j, i));

	// run simulation
	cout << "** starting simulation **\n";
	time = timestep;
	while(time < max_time) {
		// step simulation until specified time
		psystem->execute(time);

		// output amounts for time interval
		printf("\n*** interval %f-%f\n", time, time + timestep);
		for(i = 0; i < psystem->getNumCompartments(); i++)
			for(j = 0; j < psystem->getNumSpecies(); j++)
				printf("time=%f compartment=%ld species=%ld level=%ld\n", \
						time, i, j, \
						psystem->getSpeciesLevel(j, i));

			// update overall time
			time += timestep;
	}
	cout << "** finished simulation **\n";

	// tidy up
	delete psystem;

	return 0;
}
