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
	unsigned long rid1, rid2, rid3, rid4, rid5, rid6;  // rule ids
	unsigned long cid1, cid2, cid3;  // compartment ids
	unsigned long level;  // species level
	unsigned long num_reactants, reactants[2];
	unsigned long num_products, products[3];
	double reaction_constant;
	double max_time = 3600.0;  // maximum time to run simulation
	double timestep = 60.0;  // interval to step simulation for
	double time;  // current simulation time

	// create empty p system
	Psystem *psystem = new Psystem();

	// set id of p system
	psystem->setId("test_model_1");

	// add some objects to p system
	name = "A";
	sid1 = psystem->addSpecies(name);
	cout << "** added species: name=" << name << " id=" << sid1 << " **\n";
	name = "B";
	sid2 = psystem->addSpecies(name);
	cout << "** added species: name=" << name << " id=" << sid2 << " **\n";
	name = "C";
	sid3 = psystem->addSpecies(name);
	cout << "** added species: name=" << name << " id=" << sid3 << " **\n";
	name = "D";
	sid4 = psystem->addSpecies(name);
	cout << "** added species: name=" << name << " id=" << sid4 << " **\n";

	// add some rulesets to p system
	// first ruleset
	// initialise ruleset
	name = "ruleset1";
	rsid1 = psystem->addRuleSet(name);
	cout << "** added ruleset: name=" << name << " id=" << rsid1 << " **\n";
	// add rule to ruleset
	// create rule A + B -> C
	num_reactants = 2;
	reactants[0] = sid1;
	reactants[1] = sid2;
	num_products = 1;
	products[0] = sid3;
	reaction_constant = 0.1;
	name = "rule1";
	rid1 = psystem->addRule(rsid1, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	cout << "** added rule: name=" << name << " id=" << rid1 << " **\n";
	// create rule C -> A + B
	num_reactants = 1;
	reactants[0] = sid3;
	num_products = 2;
	products[0] = sid1;
	products[1] = sid2;
	reaction_constant = 0.2;
	name = "rule2";
	rid2 = psystem->addRule(rsid1, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	cout << "** added rule: name=" << name << " id=" << rid2 << " **\n";
	// second ruleset
	// initialise ruleset
	name = "ruleset2";
	rsid2 = psystem->addRuleSet(name);
	cout << "** added ruleset: name=" << name << " id=" << rsid2 << " **\n";
	// add rule to ruleset
	// create rule C -> D
	num_reactants = 1;
	reactants[0] = sid3;
	num_products = 1;
	products[0] = sid4;
	reaction_constant = 0.3;
	name = "rule3";
	rid3 = psystem->addRule(rsid2, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	cout << "** added rule: name=" << name << " id=" << rid3 << " **\n";
	// create rule D -> 0
	num_reactants = 1;
	reactants[0] = sid4;
	num_products = 0;
	reaction_constant = 0.1;
	name = "rule4";
	rid4 = psystem->addRule(rsid2, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	cout << "** added rule: name=" << name << " id=" << rid4 << " **\n";
	// thrid ruleset
	// initialise ruleset
	name = "ruleset3";
	rsid3 = psystem->addRuleSet(name);
	cout << "** added ruleset: name=" << name << " id=" << rsid3 << " **\n";
	// add rule to ruleset
	// create rule A -> A (transport rule)
	num_reactants = 1;
	reactants[0] = sid1;
	num_products = 1;
	products[0] = sid1;
	reaction_constant = 0.001;
	name = "rule5";
	rid5 = psystem->addRule(rsid3, name, num_reactants, reactants, \
			num_products, products, reaction_constant);
	// set rule as translocation rule (channel)
	psystem->setChannel(rsid3, rid5);
	cout << "** added rule: name=" << name << " id=" << rid5 << " **\n";

	// add some compartments to p system
	name = "compartment1";
	cid1 = psystem->addCompartment(name);
	cout << "** added compartment: name=" << name << " id=" << cid1 << " **\n";
	name = "compartment2";
	cid2 = psystem->addCompartment(name);
	cout << "** added compartment: name=" << name << " id=" << cid2 << " **\n";
	name = "compartment3";
	cid3 = psystem->addCompartment(name);
	cout << "** added compartment: name=" << name << " id=" << cid3 << " **\n";

	// add ruleset to compartments
	psystem->addRuleSetToCompartment(rsid1, cid1);
	cout << "** added ruleset id=" << rsid1 << " to compartment id=" << cid1 \
			<< " **\n";
	psystem->addRuleSetToCompartment(rsid2, cid1);
	cout << "** added ruleset id=" << rsid2 << " to compartment id=" << cid1 \
			<< " **\n";
	psystem->addRuleSetToCompartment(rsid1, cid2);
	cout << "** added ruleset id=" << rsid1 << " to compartment id=" << cid2 \
			<< " **\n";
	psystem->addRuleSetToCompartment(rsid2, cid2);
	cout << "** added ruleset id=" << rsid2 << " to compartment id=" << cid2 \
			<< " **\n";
	psystem->addRuleSetToCompartment(rsid3, cid3);
	cout << "** added ruleset id=" << rsid3 << " to compartment id=" << cid3 \
			<< " **\n";

	// set targets for translocation rules
	psystem->setRuleTarget(cid3, rsid3, rid5, cid1);
	cout << "** set target of rule id=" << rid5 << " in ruleset id=" << rsid3 \
			<< " in compartment id=" << cid3 << " to compartment id=" << cid1 \
			<< " **\n";
	rid6 = psystem->cloneRule(cid3, rsid3, rid5);
	cout << "** cloned rule id=" << rid5 << " in ruleset id=" << rsid3 \
			<< " in compartment id=" << cid3 << " **\n";
	psystem->setRuleTarget(cid3, rsid3, rid6, cid2);
	cout << "** set target of rule id=" << rid6 << " in ruleset id=" << rsid3 \
			<< " in compartment id=" << cid3 << " to compartment id=" << cid2 \
			<< " **\n";

	// set initial species levels
	// set level of species A in compartment3
	level = 1000;
	psystem->setSpeciesLevel(cid3, sid1, level);
	cout << "** set species id=" << sid1 << " in compartment id=" << cid3 << \
			" to " << level << " **\n";
	// set level of species B in compartment1
	level = 500;
	psystem->setSpeciesLevel(cid1, sid2, level);
	cout << "** set species id=" << sid2 << " in compartment id=" << cid1 << \
			" to " << level << " **\n";
	psystem->setSpeciesLevel(cid2, sid2, level);
	cout << "** set species id=" << sid2 << " in compartment id=" << cid2 << \
			" to " << level << " **\n";

	// set simulation algorithm
	name = "dmq";
	psystem->setSimulationAlgorithm(name);
	cout << "** set simulation algorithm to " << name << " **\n";

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
