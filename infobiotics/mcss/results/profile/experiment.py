'''
Created on 4 Sep 2012

@author: jvb
'''

from tables import IsDescription, Int32Col, Float32Col, BoolCol, openFile

import numpy as np


class Experiment(IsDescription):
	
	# written
	
	species_total = Int32Col()
	compartments_total = Int32Col()
	timepoints_total = Int32Col()
	
	amounts_total = Int32Col() # np.product([total_species, total_compartments, total_timepoints])
	
	chunkshape_0 = Int32Col()
	chunkshape_1 = Int32Col()
	chunkshape_2 = Int32Col()
	
	size_inflated = Float32Col()
	size_deflated = Float32Col()
	
	time_to_write = Float32Col()
	
	# read
	
	species_indices_total = Int32Col()
	compartment_indices_total = Int32Col()
	timepoint_indices_total = Int32Col()
	
	indices_total = Int32Col()

	# indices were contiguous if True, evenly spaced if False
	species_indices_contig = BoolCol() 
	compartment_indices_contig = BoolCol()
	timepoint_indices_contig = BoolCol()
	
	time_to_read = Float32Col()


h5file = openFile('results.h5', mode='w')
group = h5file.createGroup('/', 'group')
table = h5file.createTable(group, 'table', Experiment)

# loop writing and reading h5 files with 3D EArrays of different sizes, chunkshapes and accesses

#TODO generate parameterset
parameterset = []

parameters = {}

#parameters['species_total'] = 
#parameters['compartments_total'] = 
#parameters['timepoints_total'] = 

#parameters['chunkshape_0'] = 
#parameters['chunkshape_1'] = 
#parameters['chunkshape_2'] = 

parameterset.append(parameters)


for parameters in parameterset:

	shape = parameters['species_total'], parameters['compartments_total'], parameters['timepoints_total']
	
	amounts_total = np.product(shape)
	
	chunkshape_0 = parameters['chunkshape_1']
	chunkshape_1 = parameters['chunkshape_2']
	chunkshape_2 = parameters['chunkshape_3']
	
	chunkshape = chunkshape_0, chunkshape_1, chunkshape_2
	expectedrows = parameters['timepoints_total']
	extdim = 2

	
	
	size_inflated = Float32Col()
	size_deflated = Float32Col()
	
	time_to_write = Float32Col()
	
	# read
	
	species_indices_total = Int32Col()
	compartment_indices_total = Int32Col()
	timepoint_indices_total = Int32Col()
	
	indices_total = Int32Col()

	# indices were contiguous if True, evenly spaced if False
	species_indices_contig = BoolCol() 
	compartment_indices_contig = BoolCol()
	timepoint_indices_contig = BoolCol()
	
	time_to_read = Float32Col()
 



experiment = table.row

experiment['species_total'], experiment['compartments_total'], experiment['timepoints_total'] = shape 

experiment['amounts_total'] = np.product(shape)

experiment['chunkshape_0'], experiment['chunkshape_1'], experiment['chunkshape_2'] = chunkshape

experiment['size_inflated'] = amounts_total * 4#TODO amounts.atom.size
experiment['size_deflated'] = os.path.getsize(write)

experiment['time_to_write'] = 0.0#TODO

experiment['species_indices_total'] = 0#TODO
experiment['compartment_indices_total'] = 0#TODO
experiment['timepoint_indices_total'] = 0#TODO

experiment['indices_total'] = 0#TODO

experiment['species_indices_contig'] = True#TODO
experiment['compartment_indices_contig'] = True#TODO
experiment['timepoint_indices_contig'] = True#TODO

experiment['time_to_read'] = 0.0#TODO

experiment.append()

table.flush()

print h5file

h5file.close()

exit() 