# -*- coding: utf-8 -*-
# an example of using the libmcss python api
# copyright 2008, 2009 jamie twycross, jpt AT cs.nott.ac.uk
# released under GNU GPL version 3

from random import randint,uniform
import mcss
NB = 3
# create empty p system
ps = mcss.Psystem()

# set id of p system
ps.set_id("test_model_1")

# add some objects to p system
sid1 = ps.add_species("A")

# add some rulesets to p system
# add ruleset
rsid1 = ps.add_ruleset("ruleset1");
# add rule to ruleset
rid1 = ps.add_rule(rsid1, "rule1", ('A',), ('A',), 11.)#uniform(10.,50.) );  # A + B -> C
ps.set_channel(rsid1, rid1)

# add some compartments to the p system
for i in xrange(NB) :
	ps.add_compartment("compartment%d" % i);

# add some rulesets to compartments
for i in xrange(NB) :
	ps.add_ruleset_to_compartment(rsid1, i);

# set targets for translocation rules
for i in xrange(NB - 1) :
	ps.set_rule_target(i, rsid1, rid1, i + 1);
	#ps.set_reaction_constant(i,rsid1,rid1,10.)#uniform(10.,50.) )

for i in xrange(1,NB) :
	lrid = ps.clone_rule(i,rsid1,rid1)
	ps.set_reaction_constant(i,rsid1,lrid,10.)#uniform(10.,50.) )
	ps.set_rule_target(i,rsid1,lrid,i - 1)

# set initial species levels
for i in xrange(NB) :
	ps.set_species_level(i, sid1, 1000)#randint(100,1000) )

# set volumes of compartments
for i in xrange(NB) :
	ps.set_compartment_volume(i, 5000.)#uniform(5000.,20000.) )

# set simulation algorithm
ps.set_simulation_algorithm("dmq")

# output initial amounts
time = 0.0
for i in range(ps.num_compartments()):
	for j in range(ps.num_species()):
		print "** time=%f compartment=%d species=%d level=%d" % (time,i,j,ps.species_level(i,j) )

# run simulation
time = 0.0
max_time = 360.0
timestep = 60.0
while (time < max_time):
	#for cid in (cid1,cid2,cid3) :
	#	ps.set_species_level(cid,sid1,randint(100,1000) )
	#ps.set_species_level(cid1,sid1,0)
	# step simulation for specified interval
	ps.execute(time)

	# output amounts at end of time interval
	for i in range(ps.num_compartments()):
		for j in range(ps.num_species()):
			print "** time=%f compartment=%d species=%d level=%d" % (time+timestep,i,j,ps.species_level(i,j) )

	time += timestep

# tidy up
del ps
