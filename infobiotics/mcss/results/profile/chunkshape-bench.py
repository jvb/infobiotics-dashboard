#!/usr/bin/env python
## Benchmark the effect of chunkshapes in reading large datasets.
## You need at least PyTables 2.1 to run this!
## F. Alted
''' Benchmark the effect of chunkshapes in reading mcss datasets and 
writing/reading mock datasets with same/different chunkshapes/filters.

Adapted from https://github.com/PyTables/PyTables/blob/v.2.4.0/bench/chunkshape-bench.py
'''

from __future__ import division

import numpy as np
import tables

from time import time

import tempfile
import os


def powersof10(min, max=None):
	''' Returns an array of powers of 10 from min to max inclusive. '''
	if not max:
		max = min
		min = 0
#	print np.power(10, np.arange(min, max+1))
	return np.power(10, np.arange(min, max+1))
#print powersof10(6), powersof10(2,5)


def cntg(minpowerof10, maxpowerof10, max=None):
	''' Returns a list of arrays of contiguous (step == 1) integers from 0 to  
	a power of 10 in the interval minpowerof10 <= powerof10 <= maxpowerof10.
	'''
	return [np.arange(0, n) for n in powersof10(minpowerof10, maxpowerof10) if not max or (max and n <= max)]


#def eqsp(max, minpowerof10, maxpowerof10):
#	''' Returns a list of arrays of equally-spaced integers from 0 to max  
##	a power of 10 in the interval minpowerof10 <= powerof10 <= maxpowerof10.
#	'''
#	return [np.arange(0, max, 10**powerof10) for powerof10 in range(minpowerof10, maxpowerof10)]
#				
##print cntg(0, 2, 100)
##for a in reversed(eqsp(10**6+574, 0, 6)):
#for a in reversed(eqsp(574, 0, 6)):
#	print len(a)#, a 
#print 

#def eqsp(apowerof10, minpowerof10, maxpowerof10):
#	''' Returns a list of arrays of equally-spaced integers from 0 to ...
#	
#	[0:10**powerof10:10**minpowerof10]
#	  
#	'''
#	return [np.arange(0, 10**apowerof10, 10**powerof10) for powerof10 in range(minpowerof10, maxpowerof10)]

def eqsp(a, minpowerof10, maxpowerof10):
	''' Returns a list of arrays of equally-spaced integers from 0 to ...
	
	[0:10**powerof10:10**minpowerof10]
	  
	'''
	return [np.ceil(np.arange(0, len(a), (len(a) / 10) * 10**(powerof10 - 1) ) ) for powerof10 in range(minpowerof10, maxpowerof10) if (len(a) / 10) * 10**(powerof10 - 1) <= len(a)]
#	return [np.ceil(np.arange(0, len(a), (len(a) / 10) * 10**(powerof10 - 1) ) ) for powerof10 in range(minpowerof10, maxpowerof10) if True]
#	return [np.ceil(np.arange(0, len(a), (len(a) / 10) * 10**(powerof10 - 1) ) ) for powerof10 in range(minpowerof10, maxpowerof10)]
##	return [np.ceil(np.arange(0, len(a), (len(a) / 10) * 10**(powerof10 - 1) ) ) for powerof10 in range(minpowerof10, maxpowerof10) if len(a) > 10**powerof10]
#	f = lambda a, powerof10: (len(a) / 10) * 10**(powerof10 - 1)
#	return [np.ceil(np.arange(0, len(a), f(a, powerof10) ) ) for powerof10 in range(minpowerof10, maxpowerof10) if f(a, powerof10) >= 10**powerof10]

	

#def eqsp(n, powerof10, max):
for a in reversed(eqsp(np.arange(66666), 0, 6)):
	print len(a), a[-1], a
print 

exit()


Tn = 36001
Cn = 10000
Sn = 58

T = np.array(xrange(Tn))
C = np.array(xrange(Cn))
S = np.array(xrange(Sn))

print eqsp(10, 0, Sn)
print S[eqsp(10, 0, Sn)]


def start_stop_len(a):
	return 'a[0]: %s, a[-1]: %s, len(a): %s' % (a[0], a[-1], len(a))

#print start_stop_len(S[cntg(1,2)[0]]), start_stop_len(C[cntg(1,6)[0]]), start_stop_len(T[cntg(2,6)[0]])
#print start_stop_len(S[cntg(1,2)[-1]]), start_stop_len(C[cntg(1,6)[-1]]), start_stop_len(T[cntg(2,6)[-1]])
#exit()

##print start_stop_len(S[eqsp(Sn, 0,2)[0]]), start_stop_len(C[eqsp(Cn, 0,6)[0]]), start_stop_len(T[eqsp(Tn, 0,6)[0]])
#print start_stop_len(S[eqsp(Sn, 0,2)[-1]]), start_stop_len(C[eqsp(Cn, 0,6)[-1]]), start_stop_len(T[eqsp(Tn, 0,6)[-1]])
#print eqsp(Sn, 0,2)[-1], eqsp(Cn, 0,6)[-1], eqsp(Tn, 0,6)[-1]
s = S[eqsp(Sn, 0,2)[-1]]
c = C[eqsp(Cn, 0,6)[-1]]
t = T[eqsp(Tn, 0,6)[-1]]
print map(len, [s, c, t])
#s = np.linspace(0, Sn, 1)
#print len(s), s 
#s = map(int, map(np.ceil, np.linspace(0, Sn, 10)))
#print len(s), s 
##s = np.linspace(0, Sn, 100)
##print len(s), s 
exit()


#for t in cntg(2,6):
#	for c in cntg(1,6):
#		for s in cntg(1,2):
##			print T[t.start:t.stop:t.step], C[c.start:c.stop:c.step], S[s.start:s.stop:s.step]
##			print T[t], C[c], S[s]
##			print len(S[s]), len(C[c]), len(T[t])#len(T[t]), len(C[c]), len(S[s])
#			print start_stop_len(S[s]), start_stop_len(C[c]), start_stop_len(T[t])
#exit()

#for t in eqsp(Tn, 2,6):
#	for c in eqsp(Cn, 1,6):
#		for s in eqsp(Sn, 1,2):
##			print T[t.start:t.stop:t.step], C[c.start:c.stop:c.step], S[s.start:s.stop:s.step]
##			print T[t], C[c], S[s]
##			print len(S[s]), len(C[c]), len(T[t])#len(T[t]), len(C[c]), len(S[s])
#			print start_stop_len(S[s]), start_stop_len(C[c]), start_stop_len(T[t])
#print
#exit()

reads = [] 
for t in cntg(2,6) + eqsp(Tn, 2,6):
	for c in cntg(1,6) + eqsp(Cn, 1,6):
		for s in cntg(1,2) + eqsp(Sn, 1,2):
#			print T[t.start:t.stop:t.step], C[c.start:c.stop:c.step], S[s.start:s.stop:s.step]
#			print T[t], C[c], S[s]
#			print len(S[s]), len(C[c]), len(T[t])#len(T[t]), len(C[c]), len(S[s])
#			print start_stop_len(S[s]), start_stop_len(C[c]), start_stop_len(T[t])
			r = S[s], C[c], T[t]
			print map(start_stop_len, r)
			reads.append(r)
		print '-'*80
	print '='*80
print len(reads)
#print np.product([len(cntg(2,6) + eqsp(Tn, 2,6)), len(cntg(1,6) + eqsp(Cn, 1,6)), len(cntg(1,2) + eqsp(Sn, 1,2))])
exit()



#def main( #TODO
#	data=None, 
#	write='chunkshape-bench.h5', 
#
#	shape=(100, 1000, 10000),
#	chunkshape=(100, 1000, 100),
#	#TODO maindim=0?,
#	#TODO extdim=2?,
#	filters = tables.Filters(),
#	expectedrows = shape[-1], #TODO NameError: name 'shape' is not defined
#
#	read=None, 
#	
#	path=tempfile.tempdir,
#):
#	assert data or write
#	pass


# default values

# general
path = tempfile.tempdir

data = None

# writing
write = 'chunkshape-bench.h5'
shape = (100, 1000, 10000)
#maindim = 0? #TODO
extdim = 2 #TODO
expectedrows = shape[-1]
chunkshape = (100, 1000, 100)
filters = tables.Filters()

# reading
read = write
chunksize = 100


# user values 

# general
path = '~/tmp' 

data = 'quorumsensing-wt-experiment01.h5'

# writing
write = None
shape = (58, 10000, 36001)
#maindim = 0? #TODO
extdim = 2 # = len(shape) - 1 #TODO
expectedrows = shape[-1]

filters = tables.Filters(complib='zlib', complevel=9, shuffle=False, fletcher32=False) # mcss
#filters = tables.Filters( #TODO
###	complevel=0, # default: no compression 
#	complevel=1, # determined to be best in: http://pytables.github.com/usersguide/optimization.html 
##	complevel=1 <= level <= 9, # ignored by lzo?
#	complib='lzo', # fastest  
##	complib='zlib', # slowest 
#	shuffle=False, # slower for large chunks; default: True if complevel > 0 else False
#	fletcher32=False # default: False
#)

chunkshape = (58, 10000, 1000) # mcss determined
###chunkshape = (1, 58, 36001) # determined: shape=(0, 10000, 36001), expectedrows=36001
##chunkshape = (14, 1, 36001) # determined: shape=(58, 0, 36001), expectedrows=36001
#chunkshape = (26, 10000, 1) # determined: shape=(58, 10000, 0), expectedrows=36001
#chunkshape = (1, 10000, chunksize) # e.g. reading averaging some species in all compartments 

# reading
read = data
chunksize = 1000
#chunksize = 1


# script

assert any([data, write, read])

expandpath = lambda file: os.path.join(os.path.expanduser(path), file)

if data:
#	data = os.path.join(os.path.expanduser(path), data)
	data = expandpath(data)

if write:
#	write = os.path.join(os.path.expanduser(path), write)
	write = expandpath(write)
	if write == data:
		exit('Aborting: write == data ==', data)
		
if read:
#	read = os.path.join(os.path.expanduser(path), read)
	read = expandpath(read)
elif write:
	read = write
elif data:
	read = data


#print 'path =', path
print 'data =', data
print '-'*80
print 'write = ', write
print 'shape =', shape
#print 'maindim =', maindim
print 'extdim =', extdim
print 'expectedrows =', expectedrows
print 'filters =', filters
print 'chunkshape =', chunkshape
print '-'*80
print 'read =', read
print 'chunksize =', chunksize


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


def determine_chunkshape(shape, expectedrows):
#	if not (min(shape) == 0 and len(filter(lambda it: it == 0, shape)) == 1):
##		shape = shape[:-1]+ (0,)
#		shape = setextdim(shape, -1)
	file = tempfile.NamedTemporaryFile(delete=False)
	name = file.name
	file.close()
	f = tables.openFile(name, 'w')
	a = f.createEArray(f.root, 'a', tables.Int32Atom(), 
		shape=shape,
		expectedrows=expectedrows,
	)
	chunkshape = a.chunkshape 
	f.close()
	return chunkshape, shape, expectedrows
#	
#for dim in range(len(shape)):
#	for i in (1, 10, 100, 1000, 10000):
#		determined = determine_chunkshape(shape=setextdim(shape, dim), expectedrows=i)
#		print 'EArray(shape=%s, expectedrows=%s).chunkshape (determined):' % (determined[1], determined[2]), determined[0] 


amounts_atom_type = None
amounts_shape = None
amounts_chunkshape = None
amounts_filters = None

if data:
	print '='*80
	print "h5 = '%s'" % data
	print 'h5 size:', GB_MB_KB_str(os.path.getsize(data))
	h5 = tables.openFile(data)
#	print "h5.filename: '%s'" % h5.filename
#	print 'h5.filters:', h5.filters
	attrs = h5.root._v_attrs
	if 'number_of_runs' in attrs:
		print 'h5 is an mcss simulation'
		print '-'*80
		number_of_runs = attrs.number_of_runs
		print 'number_of_runs:', number_of_runs, '(h5.root._v_attrs.number_of_runs)'

		# first amounts EArray (possibly truncated if number_of_runs == 1)		
		print 'amounts = h5.root.run1.amounts' 
		amounts = h5.root.run1.amounts
		print 'amounts is of type:', type(amounts).__name__
		print 'amounts.atom.type:', amounts.atom.type  
		print 'amounts.atom.size:', amounts.atom.size
		print 'amounts.shape:', amounts.shape
		bytes = np.product(amounts.shape) * amounts.atom.size
		print 'amounts uncompressed size:', GB_MB_KB_str(bytes)
		print 'amounts compressed size (roughly):', GB_MB_KB_str(os.path.getsize(data) / number_of_runs)
		
		print 'amounts.filters:', amounts.filters 

		print 'amounts.maindim:', amounts.maindim
		print 'amounts.extdim:', amounts.extdim
		#TODO why is this 0? does 0 mean species? wouldn't timepoints be better? would timepoints be 2 or 3?
		
#		print 'amounts chunksize:', amounts.chunkshape[-1]
		print 'amounts.chunkshape:', amounts.chunkshape
		print 'amounts chunkshape (determined; extdim=0):', determine_chunkshape(setextdim(amounts.shape, 0), amounts.shape[2])[0] 
		print 'amounts chunkshape (determined; extdim=1):', determine_chunkshape(setextdim(amounts.shape, 1), amounts.shape[2])[0] 
		print 'amounts chunkshape (determined; extdim=2):', determine_chunkshape(setextdim(amounts.shape, 2), amounts.shape[2])[0] 
		#amounts chunkshape (determined; extdim=0): (1, 58, 36001)
		#amounts chunkshape (determined; extdim=1): (14, 1, 36001)
		#amounts chunkshape (determined; extdim=2): (26, 10000, 1)

#		# close h5 and return amounts EArray info
#		h5.close()
#		return amounts.atom.type, amounts.shape, amounts.chunkshape, amounts.filters
		amounts_atom_type = amounts.atom.type
		amounts_shape = amounts.shape
		amounts_chunkshape = amounts.chunkshape
		amounts_filters = amounts.filters

	h5.close()


# mess

# dimensions
dim1, dim2, dim3 = shape


rows_to_read = range(0, dim3, int(dim3/10))#range(0, 360, 36) # ten equally spaced rows #TODO move later or remove


assert len(chunkshape) == len(shape)
for i, dim in enumerate(shape):
	assert 0 < chunkshape[i] <= dim #TODO can chunkshape have a 0 length dimension?  


# write

if False:#write:
#def _write(file): #TODO
#	f = tables.openFile(file, 'w')
#	...
#
#if write:
#	_write(write)
	if write == data:
		exit('Aborting: write == data ==', data)
	else:
		print "="*32
		print 'Writing file:', write 
		f = tables.openFile(write, "w")
		# Pretend to create the EArray to determine chunkshape based on expectedrows
		a = f.createEArray(f.root, "a", tables.Int32Atom(), shape = shape[:-2] + tuple(0),#(dim1, dim2, 0),
		                   expectedrows=dim3) 
		print 'Determined chunkshape (expectedrows=%s):' % dim3, a.chunkshape
		# was (26, 10000, 1) for (58, 10000, 36001)
		f.removeNode(f.root, 'a')
		
		print "="*32
		# Really create the EArray
		a = f.createEArray(f.root, "a", tables.Int32Atom(), shape = (dim1, dim2, 0),
		                   filters=filters, chunkshape=chunkshape,
		#                   expectedrows=dim3
		) 
		print "Actual chunkshape:", a.chunkshape
		
		# Fill the EArray
		t1 = time()
		zeros = np.zeros((dim1, dim2, chunksize), dtype="int32")
		for i in xrange(0, dim3, chunksize):
		    a.append(zeros)
		tcre = round(time()-t1, 3)
		thcre = round(dim1*dim2*dim3*4 / (tcre * 1024 * 1024), 1)
		print "Time to append %d rows: %s sec (%s MB/s)" % (a.nrows, tcre, thcre)
		
		f.close()


# read

print "="*32
print 'Using file:', read
f = tables.openFile(read)
a = f.root.run1.amounts# = f.root.a #TODO fix for write

'''
# Read some row vectors from the original array
print "Time to read 58 spec. 10000 comp.     10 timepoints (0:36001:3600):",
t1 = time()
#for i in rows_to_read: r1 = a[i,:]
for i in rows_to_read: r1 = a[:,:,i]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
#print "Time to read ten rows in original array: %s sec (%s MB/s)" % (tr1, thr1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape, '*', len(rows_to_read)

print "Time to read  1 spec. 10000 comp.     10 timepoints:",
t1 = time()
rows_to_read = xrange(dim3)
for i in rows_to_read: r1 = a[7,:,i]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape, '*', len(rows_to_read)

print "Time to read  1 spec.     1 comp.     10 timepoints:",
t1 = time()
rows_to_read = xrange(dim3)
for i in rows_to_read: r1 = a[7,500,i]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape, '*', len(rows_to_read)
'''


'''
print '-' * 80

print "Time to read  1 spec.     1 comp.  1000 timepoints (0:1000):",
t1 = time()
r1 = a[0, 0, 0:1000]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  1 spec.     1 comp.  1000 timepoints (0:1000):",
t1 = time()
r1 = a[0, 0, 0:1000]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read 58 spec.     1 comp.  1000 timepoints (0:1000):",
t1 = time()
r1 = a[:, 0, 0:1000]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  1 spec. 10000 comp.  1000 timepoints (0:1000):",
t1 = time()
r1 = a[0, :, 0:1000]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  58 spec. 10000 comp.  1000 timepoints (0:1000):",
t1 = time()
r1 = a[:, :, 0:1000]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape


print '-' * 80

print "Time to read  1 spec.     1 comp.  36001 timepoints:",
t1 = time()
r1 = a[26,500,:]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read  1 spec.     1 comp.  36001 timepoints: 206.024 sec (0.1 MB/s) (36001,) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read  9 spec.     1 comp.  36001 timepoints:",
t1 = time()
r1 = a[range(0, 58, 7), 500,:]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read  9 spec.     1 comp.  36001 timepoints: 207.564 sec (0.1 MB/s) (9, 36001) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read  9 spec.     1 comp.  3600 timepoints:",
t1 = time()
r1 = a[range(0, 58, 7), 500,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read  9 spec.     1 comp.  3600 timepoints: 207.309 sec (0.1 MB/s) (9, 3601) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read  1 spec. 10000 comp.  3600 timepoints:",
t1 = time()
r1 = a[7, :,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read  1 spec. 10000 comp.  3600 timepoints: 210.407 sec (0.1 MB/s) (10000, 3601) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read 40 spec. 10000 comp. 3600 timepoints:",
t1 = time()
r1 = a[range(7, 47), :,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read 40 spec. 10000 comp. 3600 timepoints: 390.067 sec (0.1 MB/s) (40, 10000, 3601) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read  1 spec.  1000 comp.  3600 timepoints:",
t1 = time()
r1 = a[7, ::10,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read  1 spec.  1000 comp.  3600 timepoints: 218.413 sec (0.1 MB/s) (1000, 3601) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)

print "Time to read 40 spec.  1000 comp. 3600 timepoints:",
t1 = time()
r1 = a[range(7, 47), ::10,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape
#Time to read 40 spec.  1000 comp. 3600 timepoints: 237.117 sec (0.1 MB/s) (40, 1000, 3601) using file: /home/jvb/tmp/quorumsensing-wt-experiment01.h5; chunkshape: (58, 10000, 1000)
'''

exit(f.close()) # copying takes ages so exit early


print "="*32
# Copy the array to another with a row-wise chunkshape
t1 = time()
#newchunkshape = (dim1, dim2, chunksize*10) # ten times larger
newchunkshape = (1, dim2, chunksize) # per species
b = a.copy(f.root, "b", chunkshape=newchunkshape)
tcpy = round(time()-t1, 3)
thcpy = round(dim1*dim2*dim3*4 / (tcpy * 1024 * 1024), 1)
print "Chunkshape for row-wise chunkshape array:", b.chunkshape
print "Time to copy the original array: %s sec (%s MB/s)" % (tcpy, thcpy)

# Read the same ten rows from the new copied array
t1 = time()
for i in rows_to_read: r2 = b[:,:,i]
tr2 = round(time()-t1, 3)
thr2 = round(dim1*dim2*len(rows_to_read)*4 / (tr2 * 1024 * 1024), 1)
print "Time to read with a row-wise chunkshape: %s sec (%s MB/s)" % (tr2, thr2)
print "="*32
print "Speed-up with a row-wise chunkshape:", round(tr1/tr2, 1)

f.close()
