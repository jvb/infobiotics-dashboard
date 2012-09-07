'''
Created on 6 Sep 2012

@author: jvb
'''

from __future__ import division 

import numpy as np

import tables

write = tables.openFile('test.h5', 'w')
#write.removeNode('/', 'a')
a = write.createEArray('/', 'a', tables.Int32Atom(), (20,30,0), expectedrows=4)
#a.append(np.zeros((20,30,40)))
#print np.product((20,30,40))
a.append(np.arange(24000).reshape(20,30,40))

## bad: extract whole array
#r = a[:] 
## but good: slice whole array 
#print r[np.ix_(*([0],[0],[0]))] # ok
#print np.ix_(*([0],[0],[0]))
#print

# problem: can't extract array in same way as slicing
#print a[np.ix_(*([0],[0],[0]))] 
# reason:
'''
`key` can be any of the following items:
	...
	* A numpy array (or list or tuple) with the point coordinates.
	  This has to be a two-dimensional array of size len(self.shape)
	  by num_elements containing a list of of zero-based values
	  specifying the coordinates in the dataset of the selected
	  elements. The order of the element coordinates in the array
	  specifies the order in which the array elements are iterated
	  through when I/O is performed. Duplicate coordinate locations
	  are not checked for.
'''

# alternatives:
#selection = ([0,1],[0,1,2],[0,1,2,3])
#selection = ([0],[0],[0]) # ok
#selection = np.ix_(*([0],[0],[0])) # bad
#selection = np.ix_(*([0,1],[0,1,2],[0,1,2,3]))

chunkshape = a.shape

def cntg(start, stop=None):
	if not stop:
		stop = start
		start = 0
	stop = stop
	return slice(start, stop, 1)
#print cntg(10), np.arange(100)[cntg(10)]
#exit()

def eqsp(start, stop, num):
    ''' Like numpy.linspace but returns a slice object. '''
    assert num > 0#1?
    return slice(start, stop, (stop - start) / num)
#print eqsp(1,100,10), np.arange(100)[eqsp(1,100,10)]
#exit()

smaxe = 2#3
cmaxe = 4#5
tmaxe = 6#7

from experiment import pow10s
smaxs = pow10s(smaxe)
cmaxs = pow10s(cmaxe)
tmaxs = pow10s(tmaxe)

from itertools import product
ia = np.array(
		list(product(smaxs, cmaxs, tmaxs))
	).reshape(
		tuple([len(smaxs), len(cmaxs), len(tmaxs), 3]) # 4th dimension is shape
	)
#print ia[2,1,1,:]
#exit()
print ia[0,1,2,:]

#ucngt = np.frompyfunc(cntg, 1, 1) # clever but not right for this
#ias = ucngt(ia)
##print ias.shape, ias
##ias = ucngt(ia, axis=3)
##ias = np.sum(ia, axis=3)
#ias = np.apply_along_axis(cntg, 3, ia)

# ias = index array slices
shp = list(ia.shape)
shp.pop()
shp.insert(0, 3) # prepend a dimension of length 2 to ias
ias = np.empty(tuple(shp))
ucntg = np.frompyfunc(cntg, 1, 1)
for i, p in enumerate([pow10s(3)]):
    ias[i] = ucntg(ia)
print ias



write.close()
