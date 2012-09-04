'''
Created on 4 Sep 2012

@author: jvb
'''


from __future__ import division

import numpy as np
import tables


#def shapes(species_orders_of_magnitude, compartments_orders_of_magnitude, timepointss_orders_of_magnitude):
def shapes(*orders_of_magnitude):
	''' Returns the set of shapes that are the permutations of the 
	orders_of_magnitude iterable of (min, max) tuples. '''
	shapes = []
	for min_order_of_magnitude, max_order_of_magnitude in orders_of_magnitude:
		shape = (0, 0, 0)
		shapes.append(shape)
	return shapes
#print shapes((0,2), (0,6), (0,6))

def chunkshapes(shape):
	''' Returns a set of chunkshapes that are the order of magnitude 
	permutations of ... shape. '''
#	chunkshapes = []
#	dims = []
#	dim1, dim2, dim3 = shape 
#	for dim in f(:
#		min = 0
#		max = dim
#		dims.append()
	s = lambda max: max #TODO
	c = lambda max: max #TODO
	t = lambda max: max #TODO
	return [(s(dim1), c(dim2), t(dim3)) for dim1, dim2, dim3 in shape]
#print chunkshapes((10,100,1000))
		

def pow10s(emin, emax):
	return [10**e for e in range(emin, emax + 1)]
for o in pow10s(0, 6):
	print o
print
#exit()

def contiguous_indices(imax, emin, emax):
	''' Returns a list of arrays of contiguous (step == 1) integers from 0 to  
	an order of magnitude (power of 10) in the interval emin <= e <= emax. '''
#	return [np.arange(0, 10**e) for e in range(emin, emax) if 10**e <= imax]
	return [np.arange(0, pow10) for pow10 in pow10s(emin, emax) if pow10 <= imax]
for a in contiguous_indices(654321, 0, 6):
	print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
print
#exit()

def evenly_spaced_indices(imax, emin, emax):
#	return [np.ceil(np.linspace(0, imax -1, 10**e)) for e in range(emin, emax + 1) if 10**e <= imax]
	return [np.ceil(np.linspace(0, imax - 1, pow10)) for pow10 in pow10s(emin, emax) if pow10 <= imax]
for a in evenly_spaced_indices(654321, 0, 6):
	print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
print

def indices(shape):
	''' Returns a set of (contiguous, evenly spaced) indices that are the 
	orders of magnitude permutations of ... shape. '''
	s = lambda max: max #TODO
	c = lambda max: max #TODO
	t = lambda max: max #TODO
	contiguous = [((s(dim1), c(dim2), t(dim3)), 'contiguous') for dim1, dim2, dim3 in shape]
	gapped = [((s(dim1), c(dim2), t(dim3)), 'gapped') for dim1, dim2, dim3 in shape] 
	return contiguous + gapped 
#print indices((10,100,1000))
shape = (58, 10000, 36001)
sis = map(lambda d: contiguous_indices(d, 0, 2), shape)
cis = map(lambda d: contiguous_indices(d, 0, 6), shape)
tis = map(lambda d: contiguous_indices(d, 0, 5), shape)
for b in (sis, cis, tis):
	print len(b)
	for c in b:
		for a in c:
			print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
exit()

#maxrowsize = tables.warnings...

'''
def perform(results):
	amount_atom = Int32
	for shape in sorted(shapes, key=lambda shape: np.product(shape)):
		species_total, compartments_total, timepoints_total = shape
		inflated_size = amount_atom * np.product(shape) # bytes
		for chunkshape in chunkshapes(shape):
			if rowsize(chunkshape) > 10000000:#TODO maxrowsize:
				print 'chunkshape %s: N/A' % chunkshape 
				continue
			#TODO write h5file measuring time_write and size_deflated if compressing
			for indices in sorted(indices_list, key=lambda indices: np.product(indices)):
				#TODO read h5file measuring time_read
				#TODO create experiment and append to table
				pass


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


exit()


experiment = table.row

experiment['species_total'], experiment['compartments_total'], experiment['timepoints_total'] = shape 

experiment['amounts_total'] = np.product(shape)

experiment['chunkshape_0'], experiment['chunkshape_1'], experiment['chunkshape_2'] = chunkshape

experiment['size_inflated'] = amounts_total * 4#TODO amounts.atom.size
#experiment['size_deflated'] = os.path.getsize(write)

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

''' 