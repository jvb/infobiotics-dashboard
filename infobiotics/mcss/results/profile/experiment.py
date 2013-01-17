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
import os
from pprint import pprint
import tempfile
from time import time

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
#	return [np.arange(0, pow10) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
	return [range(0, pow10) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
#for a in contiguous_indices(654321, 0, 6):
#	print 'len: %s, head: %s, tail: %s' % (len(a), a[0:3], a[-3:])
#print
#exit()

def evenly_spaced_indices(dmax, emin, emax=None):
#	return [np.array(map(int, np.ceil(np.linspace(0, dmax - 1, pow10)))) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
	return [map(int, np.ceil(np.linspace(0, dmax - 1, pow10))) for pow10 in pow10s(emin, emax) if pow10 <= dmax]
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


# counts
written = 0
skipped_writing = 0
read = 0
skipped_reading = 0

# generator
def perform(dtype, semin=semin, semax=semax, cemin=cemin, cemax=cemax, temin=temin, temax=temax, extdim=2, filters=Filters(complib='zlib', complevel=1, shuffle=False, fletcher32=False)):
	
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
##	ashps = productarrayshapes(semax, cemax, temax) #TODO reinstate
#	ashps = [(58, 10000, 36001)] # quorumsensing-wt-experiment01.h5
	ashps = [(1, 2, 3), (10, 20, 30)] # testing

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

		# expectedrows is max extdim # == shp[extdim]
		expectedrows = shp[extdim]

		# determine chunkshape that PyTable would have used
		determined_chunkshape = determine_chunkshape(shp, extdim, expectedrows)
		determined_chunkshape_0, determined_chunkshape_1, determined_chunkshape_2 = determined_chunkshape 


		cntg_index_arrays = contiguous_index_arrays(shp, semax, cemax, temax)
		evsp_index_arrays = evenly_spaced_index_arrays(shp, semax, cemax, temax)
		evry_index_array = [np.arange(0, dmax) for dmax in shp] # == [:, :, :]

		# remove duplicate index arrays and label with type		
		index_array_tuples = []
		index_tuple_tuples = set()
		
		for iatype, iat in itertools.chain(
			# do contiguous first to avoid labelling contiguous index arrays as evenly spaced
			itertools.product(
				['contiguous'],#0,#[indices_type_enum[0]],#['contiguous'], 
				cntg_index_arrays + [evry_index_array]
			), 
			itertools.product(
				['evenly spaced'],#1,#[indices_type_enum[1]],#['evenly spaced'], 
				evsp_index_arrays)
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

			chunksize = shapesize(chunkshape)

			bytes_to_write_per_chunk = atom.size * chunksize

			# writing
			
			skip_writing = chunksize > maxrowsize #TODO replace with exceedsmaxrowsize(shape) function
			
			if skip_writing:
				print 'skipping',
			
			print 'writing array shape %s with chunkshape %s' % (shp, chunkshape) 
			
			if skip_writing:
#				global skipped_writing
				skipped_writing += 1
				continue

			# write temporary h5file measuring time_write and size_deflated if compressing

			tmpfile = tempfile.NamedTemporaryFile(delete=False)
			write = tmpfile.name
			tmpfile.close()
			f = openFile(write, "w")

			# create array
			a = f.createEArray(f.root, 'array', 
				atom, 
#				shape=setextdim(shp, extdim), 
				setextdim(shp, extdim), 
				expectedrows=expectedrows,
				filters=filters,
				chunkshape=chunkshape, 
			)
			
			# write the array in whole chunks
			t1 = time()
			zeros = np.zeros(chunkshape, dtype=dtype)
			try:
				for _ in range(0, shp[extdim], chunkshape[extdim]):
					a.append(zeros)
			except Exception, e:
				print 'error (shp[%s]: %s, chunkshape[%s]: %s):' % (extdim, shp[extdim], extdim, chunkshape[extdim]), e
				continue
#			print '***', a.shape, a[:]
			
			tcre = round(time()-t1, 3) or 10**-6 # avoid divide by zero
			thcre = round(bytes_to_write_per_chunk / (tcre * 1024 * 1024), 1)
			print 'wrote array shape %s with chunkshape %s in %s sec at (%s MB/s)' % (shp, chunkshape, tcre, thcre)

			time_to_write = tcre
			
#			f.close()
			
			size_deflated = os.path.getsize(write)

			global written
			written += 1
					
			
			# reading
			
			def fromto(iat): #TODO move outside loops
				return ', '.join(['%s..%s' % (from_, to) if from_ != to else str(to) for from_, to in [(ia[0], ia[-1]) for ia in iat]])
			
			for iatype, iat in index_array_tuples:
			
				bytes_to_read = atom.size * size(iat)
			
				skip_reading = bytes_to_read > maxsize
				
				if skip_reading:
					print 'skipping',
				
				print 'reading %s %s: %s' % (size(iat), ('%s datapoints' % iatype) if size(iat) > 1 else 'datapoint', fromto(iat))

				# read h5file measuring time_read
				t1 = time()
				
##				print iat
##				iat = np.array(iat)
##				iat = tuple(onelevelflatten(iat))
#				print '***', a.shape, a[:]
#				print iat#iat.shape, iat
#				print 'a[%s]' % (iat,)
#				#TODO ValueError: setting an array element with a sequence.
#				try:
#					read = a[iat]
				
				print 'iat:', iat, 'np.ix_(*iat):', np.ix_(*iat), map(tuple, iat), np.ix_(*map(tuple, iat)), 
				r = a[np.ix_(*map(tuple, iat))]
				
#				except ValueError, e:
#					print 'error:', e
#					continue
				assert np.product(r.shape) == size(iat), '%s, %s' % (r.shape, size(iat))
				del r
				tr1 = round(time()-t1, 3) or 10**-6 # avoid divide by zero
				thr1 = round(bytes_to_read / (tr1 * 1024 * 1024), 1)
				print 'read %s %s (%s) in %s sec at (%s MB/s)' % (size(iat), ('%s datapoints' % iatype) if size(iat) > 1 else 'datapoint', fromto(iat), tr1, thr1)
				print
				
				time_to_read = tr1
				
				# yield parameter and result values dict
				yield dict(
						
					# written
					
					species_total=species_total,
					compartments_total=compartments_total,
					timepoints_total=timepoints_total,
					
					amounts_total=amounts_total,
					
					extdim=extdim,

					expectedrows=expectedrows,
					
					determined_chunkshape_0=determined_chunkshape_0,
					determined_chunkshape_1=determined_chunkshape_1,
					determined_chunkshape_2=determined_chunkshape_2,

					chunkshape_0=chunkshape[0],
					chunkshape_1=chunkshape[1],
					chunkshape_2=chunkshape[2],

					size_inflated=inflated_size,
					size_deflated=size_deflated,

					time_to_write=time_to_write,
					write_rate=thcre,
					
					complib=filters.complib,
					complevel=str(filters.complevel),
					shuffle=filters.shuffle,
					fletcher32=filters.fletcher32,
					
					
					# read
					
					#TODO mix iatypes  
					species_indices_type = iatype,
					species_indices_total = len(iat[0]),

					compartment_indices_type = iatype,
					compartment_indices_total = len(iat[1]),

					timepoint_indices_type = iatype,
					timepoint_indices_total = len(iat[2]),
					
					amounts_indices_total = size(iat),

					bytes_read=bytes_to_read,
					time_to_read=time_to_read,
					read_rate=thr1,
				)

				if skip_reading:
#					global skipped_reading
					skipped_reading += 1
					continue
				
#				global read
				read += 1

			print '-'*80
		
		f.close()	
		os.remove(write)
			
		print '='*80
		
#	print 'total written: %s, skipped: %s' % (written, skipped_writing)
#	print 'total read: %s, skipped: %s' % (read, skipped_reading)

indices_type_enum = ['contiguous', 'evenly spaced']


class Experiment(IsDescription):
	
	# written
	
	species_total = Int32Col()
	compartments_total = Int32Col()
	timepoints_total = Int32Col()
	
	amounts_total = Int32Col()
	
	extdim=Int32Col()

	expectedrows=Int32Col()

	determined_chunkshape_0=Int32Col()
	determined_chunkshape_1=Int32Col()
	determined_chunkshape_2=Int32Col()

	chunkshape_0 = Int32Col()
	chunkshape_1 = Int32Col()
	chunkshape_2 = Int32Col()
	
	size_inflated = Float32Col()
	size_deflated = Float32Col()
	
	time_to_write = Float32Col()
	write_rate=Float32Col()
	
#	complib=EnumCol(['none', 'zlib', 'lzo', 'bzip2', 'blosc'], 'none', 'int8')
	complib=StringCol(5)
##	complevel=EnumCol([str(l) for l in range(9+1)], '0', 'int8')
#	complevel=EnumCol(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], '0', 'int8')
	complevel=Int8Col()
	shuffle=BoolCol()
	fletcher32=BoolCol()
	
	
	# read
	
#'contiguous'
#'evenly spaced'
	
#	species_indices_type = EnumCol(indices_type_enum, 'contiguous', 'int8') 
	species_indices_type = StringCol(16) 
	species_indices_total = Int32Col()

#	compartment_indices_type = EnumCol(indices_type_enum, 'contiguous', 'int8') 
	compartment_indices_type = StringCol(16) 
	compartment_indices_total = Int32Col()
	
#	timepoint_indices_type = EnumCol(indices_type_enum, 'contiguous', 'int8')
	timepoint_indices_type = StringCol(16)
	timepoint_indices_total = Int32Col()
	
	amounts_indices_total = Int32Col()

	bytes_read=Int32Col()
	time_to_read = Float32Col()
	read_rate=Float32Col()


def experiment(complib='zlib', complevel=9, shuffle=False, fletcher32=False):
	filters = Filters(complib=complib, complevel=complevel, shuffle=shuffle, fletcher32=fletcher32)
	
	h5file = openFile('test.h5', mode='w')
#	group = h5file.createGroup('/', 'results')
#	table = h5file.createTable(group, 'table', Experiment)
	table = h5file.createTable('/', 'results', Experiment)
#	print table.cols[:]#['species_indices_type']
#	exit()
	try:
		for result in perform(np.int32, filters=filters):
			experiment = table.row
			for k, v in result.iteritems():
				experiment[k] = v
			experiment.append()
			table.flush()
#	except Exception, e:
#		print 'error ^^^'
#		print 'failed with exception:'#\n', e, '\n'
#		raise e
	finally:
		print '^^^'
		print h5file
		h5file.close()
	print 'total written: %s, skipped: %s' % (written, skipped_writing)
	print 'total read: %s, skipped: %s' % (read, skipped_reading)



def GB_MB_KB_str(bytes):
	return '%s GB (%s MB / %s KB)' % tuple(
		map(
			lambda B: round(B, 3), 
			map(
				lambda exp: bytes / (1024**exp), 
				range(1,4,1)[::-1])))


def setextdim(shape, extdim):
	shape = list(shape)
	shape[extdim] = 0
	return tuple(shape)


def determine_chunkshape(shape, extdim, expectedrows):
#	if not (min(shape) == 0 and len(filter(lambda it: it == 0, shape)) == 1):
##		shape = shape[:-1]+ (0,)
#		shape = setextdim(shape, -1)
	shape = setextdim(shape, extdim)
	file = tempfile.NamedTemporaryFile(delete=False)
	name = file.name
	file.close()
	f = openFile(name, 'w')
	a = f.createEArray(f.root, 'a', Int32Atom(), 
		shape=shape,
		expectedrows=expectedrows,
	)
	chunkshape = a.chunkshape 
	f.close()
	return chunkshape
#	
#for dim in range(len(shape)):
#	for i in (1, 10, 100, 1000, 10000):
#		determined = determine_chunkshape(shape=setextdim(shape, dim), expectedrows=i)
#		print 'EArray(shape=%s, expectedrows=%s).chunkshape (determined):' % (determined[1], determined[2]), determined[0] 



if __name__ == '__main__':
	experiment()
