# -*- coding: utf-8 -*-
# an example of using the libmcss python api
# copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
# released under GNU GPL version 3

import mcss

# create empty p system
ps = mcss.Psystem()

# set id of p system
ps.set_id("test_model_1")

# add some objects to p system
sid1 = ps.add_species("A")
sid2 = ps.add_species("B")
sid3 = ps.add_species("C")
sid4 = ps.add_species("D")

# add some rulesets to p system
# add ruleset
rsid1 = ps.add_ruleset("ruleset1");
# add rule to ruleset
rid1 = ps.add_rule(rsid1, "rule1", ('A','B'), ('C',), 0.1);  # A + B -> C
# add rule to ruleset
rid2 = ps.add_rule(rsid1, "rule2", ('C',), ('A','B'), 0.2);  # C -> A + B
# add ruleset
rsid2 = ps.add_ruleset("ruleset2");
# add rule to ruleset
rid3 = ps.add_rule(rsid2, "rule1", ('C',), ('D',), 0.3);  # C -> D
# add rule to ruleset
rid4 = ps.add_rule(rsid2, "rule2", ('D',), (), 0.1);  # D -> 0
# add ruleset
rsid3 = ps.add_ruleset("ruleset3");
# add rule to ruleset
rid5 = ps.add_rule(rsid3, "rule1", ('A',), ('A',), 0.001);  # A -> A
# set rule as translocation rule
ps.set_channel(rsid3, rid5)

# add some compartments to the p system
cid1 = ps.add_compartment("compartment1");
cid2 = ps.add_compartment("compartment2");
cid3 = ps.add_compartment("compartment3");

# add some rulesets to compartments
ps.add_ruleset_to_compartment(rsid1, cid1);
ps.add_ruleset_to_compartment(rsid2, cid1);
ps.add_ruleset_to_compartment(rsid1, cid2);
ps.add_ruleset_to_compartment(rsid2, cid2);
ps.add_ruleset_to_compartment(rsid3, cid3);

# clone rule in compartment
rid6 = ps.clone_rule(cid3, rsid3, rid5)

# adjust reaction constant of cloned rule
ps.set_reaction_constant(cid3, rsid3, rid6, 0.002)

# set targets for translocation rules
ps.set_rule_target(cid3, rsid3, rid5, cid1);
ps.set_rule_target(cid3, rsid3, rid6, cid2);

# set initial species levels
ps.set_species_level(cid1, sid2, 500)
ps.set_species_level(cid2, sid2, 500)
ps.set_species_level(cid3, sid1, 1000)

# set volumes of compartments
ps.set_compartment_volume(cid1, 10.0)
ps.set_compartment_volume(cid2, 20.0)
ps.set_compartment_volume(cid3, 30.0)

# set simulation algorithm
ps.set_simulation_algorithm("dmq")

# output initial amounts
time = 0.0
for i in range(ps.num_compartments()):
	for j in range(ps.num_species()):
		print "** time=%f compartment=%d species=%d level=%d" % (time,i,j,ps.level(j, i))

# run simulation
max_time = 3600.0
timestep = 60.0
time = timestep
while (time <= max_time):
	# step simulation for specified interval
	ps.execute(time)

	# output amounts at end of time interval
	for i in range(ps.num_compartments()):
		for j in range(ps.num_species()):
			print "** time=%f compartment=%d species=%d level=%d" % (time,i,j,ps.level(j, i))

	time += timestep

# tidy up
del ps