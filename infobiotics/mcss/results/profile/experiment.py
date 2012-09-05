''' This is an experiment designed to the measure the affect on read 
performance of the parameters used when writing EArrays in HDF5 (.h5) files.

The motivation is to improve the read performance and therefore scalability of 
of mcss simulation datasets with respect to data extraction and subsequent 
analysis: i.e. in the mcss-results component of the Infobiotics Dashboard.

The write parameters are:
 * the shape of the array, which determines array size and therefore the size 
 	of h5 file containing the array
 * the compression library used and the compression level
 * the chunkshape used, which is necessary for efficient writing and compression

The write results are:
 * the time to write the h5 file containing the array
 * the compressed sized of the h5 file containing the array
	

The read parameters are:
 * the set of datapoints to read from the array: the indices of the datapoints 
 	along each axis, which can be contiguous or evenly spaced  

The read results are:
 * the time to read the set of datapoints from the array:
	




Created on 4 Sep 2012

@author: jvb
'''


from __future__ import division


# defaults

semin = 0
semax = 2#3
cemin = 0
cemax = 5#6
temin = 0
temax = 6#7


import itertools
import math
from pprint import pprint

import numpy as np

#from tables import IsDescription, Int32Col, Float32Col, BoolCol, openFile
from tables import *


def maxmem(dtype):
	maxmems = pow10s(16)
	allocated = None
	while allocated == None:
		maxmem = maxmems.pop()
		try:
			allocated = np.empty( (maxmem,), dtype)
		except MemoryError:
			continue
	return maxmem


def pow10(e):
	return 10**e

def pow10s(emin, emax=None):
	if not emax:
		emax = emin
		emin = 0
	return [10**e for e in range(emin, emax + 1)]
#for o in pow10s(0, 6):
#	print o
#print
#exit()

def onelevelflatten(ll):
	return [i for l in ll for i in l]

def arrayshape(*emaxs):
	return tuple(map(pow10, *emaxs))
#print arrayshape((1,2,3))
#exit()

def productarrayshapes(*emaxs):
	return [arrayshape(shape) for shape in itertools.product(*map(range, emaxs))]
#print productarrayshapes(semax, cemax, temax)
#exit()

def chunkshapes(shape):
	''' Returns a set of chunkshapes of dimensions up to and including those of 
	shape in increasing order of magnitude from 1. '''
	assert min(shape) > 0
	# orders of magnitude smaller the dimensions
#	print int(math.log10(58))+1, 'chunkshapes(%s)' % (shape,) , map(int, map(math.log10, [i + 1 for i in shape]))
#	chunkshapes = productarrayshapes(*map(int, map(math.log10, [i + 1 for i in shape])))
	chunkshapes = productarrayshapes(*[int(e) + 1 for e in map(math.log10, shape)])
	# plus full length of each dimension 
	chunkshapes = list(itertools.product(*[sorted(list(s.union( (shape[i], ) ))) for i, s in enumerate(map(set, zip(*chunkshapes)))]))
#	# hacks:
#	# add (1,1,1)
#	if (1,1,1) not in chunkshapes:
#		chunkshapes = [(1,1,1)] + chunkshapes
#	# add shape
#	if shape not in chunkshapes:
#		chunkshapes.append(shape)
#	# remove empty shape
#	if tuple() in chunkshapes:
#		chunkshapes.remove( tuple() )
	# fixed
	return chunkshapes
#pprint(chunkshapes((10,100,1000)))
#pprint(chunkshapes((99,999,9999)))
#pprint(chunkshapes((9,99,999)))
#pprint(chunkshapes((1,1,1)))
#exit()

def contiguous_indices(dmax, emin, emax=None):
	''' Returns a list of arrays of contiguous (step == 1) integers from 0 to  
	an order of magnitude (power of 10) in the interval emin <= e <= emax. '''
#	return [np.arange(0, pow10) for pow10 in pow10s(emin, emax) + [dmax] if pow10 <= dmax]
	return [np.arange(0, pow10) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
#for a in contiguous_indices(654321, 0, 6):
#	print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
#print
#exit()

def evenly_spaced_indices(dmax, emin, emax=None):
	return [np.array(map(int, np.ceil(np.linspace(0, dmax - 1, pow10)))) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
#for a in evenly_spaced_indices(654321, 0, 6):
#	print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
#print
#exit()


#def _index_arrays(func, shape, semax, cemax, temax):
#	return zip(*map(onelevelflatten, [
#		map(lambda d: func(d, emax), shape) 
#		for emax in semax, cemax, temax
#	]))
def _index_arrays(func, shape, *emaxs):
	return zip(*map(onelevelflatten, [
		map(lambda d: func(d, emax), shape) 
		for emax in emaxs
	]))

#cntg_index_arrays = zip(*map(onelevelflatten, [
#	map(lambda d: contiguous_indices(d, emax), shape) 
#	for emax in semax, cemax, temax
#]))
def contiguous_index_arrays(shape, semax, cemax, temax):
#	return zip(*map(onelevelflatten, [
#		map(lambda d: contiguous_indices(d, emax), shape) 
#		for emax in semax, cemax, temax
#	]))
	return _index_arrays(contiguous_indices, shape, semax, cemax, temax)
#cntg_index_arrays = contiguous_index_arrays((58, 10000, 36001), semax, cemax, temax)
#pprint(cntg_index_arrays)
#exit()

#evsp_index_arrays = zip(*map(onelevelflatten, [
#	map(lambda d: evenly_spaced_indices(d, emax), shape) 
#	for emax in semax, cemax, temax
#]))
def evenly_spaced_index_arrays(shape, semax, cemax, temax):
#	return zip(*map(onelevelflatten, [
#		map(lambda d: evenly_spaced_indices(d, emax), shape) 
#		for emax in semax, cemax, temax
#	]))
	return _index_arrays(evenly_spaced_indices, shape, semax, cemax, temax)
#evsp_index_arrays = evenly_spaced_index_arrays((58, 10000, 36001), semax, cemax, temax)

#index_arrays = cntg_index_arrays + evsp_index_arrays

def shape(la):
	return tuple(map(len, la))

def shapes(lla):
	return [shape(la) for la in lla]

def size(la):
	return np.product(shape(la))

def shapesize(shape):
	return np.product(shape)

def sizes(lla):
	return [size(la) for la in lla]

## in-place sorting
## descending by dimensions
#index_arrays.sort(key=shape, reverse=True)
## ascending by size
#index_arrays.sort(key=size)
##pprint(shapes(index_arrays))
##pprint(sizes(index_arrays))
##exit()



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


# counts
written = 0
skipped_writing = 0
read = 0
skipped_reading = 0

# generator
def perform(table, dtype, semin=semin, semax=semax, cemin=cemin, cemax=cemax, temin=temin, temax=temax, extdim=2, complib='zlib', complevel=1):
	
	# determine a sensible maximum array size given available memory
	maxsize = maxmem(dtype)

	maxrowsize = 104857600
#	/usr/lib/python2.7/dist-packages/tables/leaf.py:416: PerformanceWarning: The Leaf ``/run10/amounts`` is exceeding the maximum recommended rowsize (104857600 bytes);
#	be ready to see PyTables asking for *lots* of memory and possibly slow
#	I/O.  You may want to reduce the rowsize by trimming the value of
#	dimensions that are orthogonal (and preferably close) to the *main*
#	dimension of this leave.  Alternatively, in case you have specified a
#	very small/large chunksize, you may want to increase/decrease it.
#	  PerformanceWarning)
				
	atom = Atom.from_dtype(np.dtype(dtype))

#	# counts
#	written = 0
#	skipped_writing = 0
#	read = 0
#	skipped_reading = 0

	# list of array shapes
#	ashps = productarrayshapes(semax, cemax, temax) #TODO reinstate
	ashps = [(58, 10000, 36001)] # testing

	# in-place sorting
	# descending by dimensions (timepoints > compartments > species)
	ashps.sort()
	# ascending by size (smallest > largest)
	ashps.sort(key=shapesize)
#	pprint(ashps)

	for shp in ashps:
		
		species_total, compartments_total, timepoints_total = shp
#		print species_total, compartments_total, timepoints_total
		amounts_total = shapesize(shp)
		
		# array size in memory (bytes)
		inflated_size = atom.size * shapesize(shp)

		cntg_index_arrays = contiguous_index_arrays(shp, semax, cemax, temax)
		evsp_index_arrays = evenly_spaced_index_arrays(shp, semax, cemax, temax)
		evry_index_array = [np.arange(0, dmax) for dmax in shp] # == [:, :, :]

		# remove duplicate index arrays and label with type		
		index_array_tuples = []
		index_tuple_tuples = set()
		for iatype, iat in itertools.chain(
			# do contiguous first to avoid labelling contiguous index arrays as evenly spaced
			itertools.product(['contiguous'], cntg_index_arrays + [evry_index_array]), 
			itertools.product(['evenly spaced'], evsp_index_arrays)
		): 
			# get a hashable index tuple tuple from an index array tuple
			itt = tuple(map(tuple, iat))
			# add index array tuple if not already added
			if not itt in index_tuple_tuples:
				index_tuple_tuples.add(itt)
				index_array_tuples.append((iatype, iat))
##		pprint(index_array_tuples)		
##		print len(index_array_tuples), len(index_tuple_tuples)
#		all_index_arrays = cntg_index_arrays + evsp_index_arrays + [evry_index_array] 
#		print len(all_index_arrays), len(index_array_tuples)
#		assert len(all_index_arrays) >= len(index_array_tuples)


		# chunkshapes for writing
		cshps = chunkshapes(shp)
		# in-place sorting
		# descending by dimensions (timepoints > compartments > species)
		cshps.sort()
		# ascending by size (smallest > largest)
		cshps.sort(key=shapesize)
#		pprint(cshps)

		for chunkshape in cshps:
#			print chunkshape

			# writing
			skip_writing = atom.size * shapesize(chunkshape) > maxrowsize #TODO replace with exceedsmaxrowsize(shape) function
			if skip_writing:
				print 'skipping',
			print 'writing array shape %s with chunkshape %s' % (shp, chunkshape) 
			if skip_writing:
				skipped_writing += 1
				continue

			#TODO write h5file measuring time_write and size_deflated if compressing
			
#			size_deflated = TODO
			
			written += 1
					
			# reading
			def f(iat): #TODO move outside loops
				return ', '.join(['%s..%s' % (from_, to) if from_ != to else str(to) for from_, to in [(ia[0], ia[-1]) for ia in iat]])
			for iatype, iat in index_array_tuples:
				skip_reading = atom.size * size(iat) > maxsize
				if skip_reading:
					print 'skipping',
				print 'reading %s %s: %s' % (size(iat), ('%s datapoints' % iatype) if size(iat) > 1 else 'datapoint', f(iat))#shape(iat))

				#TODO read h5file measuring time_read
				
				# yield parameter and result values dict
				yield dict(
						
					# written
					
					species_total=species_total,
					compartments_total=compartments_total,
					timepoints_total=timepoints_total,
					
					amounts_total=amounts_total,
					
					size_inflated=inflated_size,
					size_deflated=size_deflated,
					
					chunkshape_0=chunkshape[0],
					chunkshape_1=chunkshape[1],
					chunkshape_2=chunkshape[2],

					extdim=extdim,
					expectedrows=shp[extdim],
					
#					time_to_write = TODO,
					
					
					# read
					
#					species_indices_total = TODO,
#					compartment_indices_total = TODO,
#					timepoint_indices_total = TODO,

#					read_indices_total = TODO,

#					species_indices_type = TODO,
#					compartment_indices_type = TODO,
#					timepoint_indices_type = TODO,
					
#					time_to_read = TODO,
				)

				if skip_reading:
					skipped_reading += 1
					continue
				read += 1

			print '-'*80
		print '='*80
#	print 'total written: %s, skipped: %s' % (written, skipped_writing)
#	print 'total read: %s, skipped: %s' % (read, skipped_reading)

h5file = openFile('test.h5', mode='w')
group = h5file.createGroup('/', 'results')
table = h5file.createTable(group, 'table', Experiment)
try:
	experiment = table.row
	experiment.update(perform(np.int32))
	experiment.append()
	table.flush()
except Exception, e:
	print e
finally:
	print h5file
	h5file.close()
print 'total written: %s, skipped: %s' % (written, skipped_writing)
print 'total read: %s, skipped: %s' % (read, skipped_reading)
