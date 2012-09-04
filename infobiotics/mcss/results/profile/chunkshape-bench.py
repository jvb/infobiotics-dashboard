#!/usr/bin/env python
# Benchmark the effect of chunkshapes in reading large datasets.
# You need at least PyTables 2.1 to run this!
# F. Alted

from __future__ import division

import numpy, tables
from time import time

#dim1, dim2 = 360, 6109666
dim1, dim2, dim3 = 58, 10000, 36001 
print 'array (%s, %s, %s) uncompressed size (GB):' % (dim1, dim2, dim3), (dim1*dim2*dim3*4) / (1024**3)
#rows_to_read = range(0, 360, 36)
rows_to_read = range(0, 36001, 3600)#int(dim3/10)) # ten equally spaced rows

filters = tables.Filters(complevel=9, complib='lzo', 
						shuffle=False,# True by default 
#						fletcher32=False # False by default
)

# different chunksizes
chunksize = 1000

# different chunkshapes
#chunkshape = (dim1, dim2, chunksize) # (1, 10000, 1000)
chunkshape = (1, dim2, chunksize) # (1, 10000, 1000)
#chunkshape = (1, 1000, chunksize) # (1, 1000, 1000)
print "Specified chunkshape:", chunkshape

'''
f = tables.openFile("/home/jvb/tmp/chunkshape-bench.h5", "w")
#print "="*32
## Pretend to create the EArray
#a = f.createEArray(f.root, "a", tables.Int32Atom(), shape = (dim1, dim2, 0),
#                   expectedrows=dim3) 
#print 'Automatic chunkshape when expectedrows=36001:', a.chunkshape #(26, 10000, 1)'
#f.removeNode(f.root, 'a')
print "="*32
# Really create the EArray
a = f.createEArray(f.root, "a", tables.Int32Atom(), shape = (dim1, dim2, 0),
                   filters=filters, chunkshape=chunkshape,
#                   expectedrows=dim3
) 
print "Actual chunkshape:", a.chunkshape

# Fill the EArray
t1 = time()
zeros = numpy.zeros((dim1, dim2, chunksize), dtype="int32")
for i in xrange(0, dim3, chunksize):
    a.append(zeros)
tcre = round(time()-t1, 3)
thcre = round(dim1*dim2*dim3*4 / (tcre * 1024 * 1024), 1)
print "Time to append %d rows: %s sec (%s MB/s)" % (a.nrows, tcre, thcre)

f.close()
'''

f = tables.openFile("/home/jvb/tmp/chunkshape-bench.h5", "r")
a = f.root.a

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

print "Time to read  1 spec.     1 comp.  36001 timepoints:",
t1 = time()
r1 = a[26,500,:]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  7 spec.     1 comp.  36001 timepoints:",
t1 = time()
r1 = a[range(0, 58, 7), 500,:]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  7 spec.     1 comp.  3600 timepoints:",
t1 = time()
r1 = a[range(0, 58, 7), 500,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  1 spec. 10000 comp.  3600 timepoints:",
t1 = time()
r1 = a[7, :,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  2 spec. 10000 comp. 3600 timepoints:",
t1 = time()
r1 = a[range(7, 47), :,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  1 spec.  1000 comp.  3600 timepoints:",
t1 = time()
r1 = a[7, ::10,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape

print "Time to read  2 spec.  1000 comp. 3600 timepoints:",
t1 = time()
r1 = a[range(7, 47), ::10,::10]
tr1 = round(time()-t1, 3)
thr1 = round(dim1*dim2*len(rows_to_read)*4 / (tr1 * 1024 * 1024), 1)
print "%s sec (%s MB/s)" % (tr1, thr1), r1.shape


f.close(); exit() # copying takes ages so exit early


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
