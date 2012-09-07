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
selection = np.array(([0,1],[0,1,2],[0,1,2,3]))
print selection.size, selection.shape, selection

print
print a.shape 
#print a[np.ix_(*([0],[0],[0]))] 
#print a[0:1:1] 

chunkshape = a.shape
def cntg(start, stop=None):
	if not stop:
		stop = start
		start = 0
	stop = stop + 1
	return slice(start, stop, 1)
#print cntg(2), cntg(1,10)
slices = map(cntg, chunkshape) 
#print slices 
r = a[slices[0], slices[1], slices[2]]
print r.shape 
#exit()
#print
from math import ceil
def eqsp(n, start=None, stop=None):
	if not start:
		if not stop:
			start = n
		else:
			start = 0
	if not stop:
		stop = start
		start = 0
	stop = stop + 1
	print stop / n, int(stop / n), int(stop / n) or 1, ceil(int(stop / n))# or 2)
	return slice(start, stop, int(stop / n) or 1)
#print eqsp(2,2), eqsp(1,100,10)
from functools import partial
n = 3
slices = map(partial(eqsp, n), chunkshape)
#print slices 
r = a[slices[0], slices[1], slices[2]] [:n, :n, :n]
print r.shape, r
#print a[] 


from experiment import pow10s
smaxe = 2#3
cmaxe = 4#5
tmaxe = 6#7
#for se in pow10s(smaxe):
#	for ce in pow10s(cmaxe):
#		for te in pow10s(tmaxe):
#			pass
##			print se, ce, te
##			for f in cntg, eqsp:
##				print 'cntg:',
##				print ()
##				print 'esqp:',
##				print 
smaxs = pow10s(smaxe)
cmaxs = pow10s(cmaxe)
tmaxs = pow10s(tmaxe)
ia = np.array([smaxs, cmaxs, tmaxs])
from itertools import product
ia = np.array(list(product(smaxs, cmaxs, tmaxs))).flatten().reshape(tuple([len(smaxs), len(cmaxs), len(tmaxs), 3]))
print ia[2,:,:,:]



# see also     def _fancySelection(self, args):


#File "/usr/lib/python2.7/dist-packages/tables/array.py", line 692, in __getitem__
#    def __getitem__(self, key):
"""
Get a row, a range of rows or a slice from the array.

The set of tokens allowed for the `key` is the same as that
for extended slicing in Python (including the ``Ellipsis`` or
``...`` token).  The result is an object of the current
flavor; its shape depends on the kind of slice used as `key`
and the shape of the array itself.

Furthermore, NumPy-style fancy indexing, where a list of
indices in a certain axis is specified, is also supported.
Note that only one list per selection is supported right now.
Finally, NumPy-style point and boolean selections are
supported as well.

Example of use::

    array1 = array[4]                       # simple selection
    array2 = array[4:1000:2]                # slice selection
    array3 = array[1, ..., ::2, 1:4, 4:]    # general slice selection
    array4 = array[1, [1,5,10], ..., -1]    # fancy selection
    array5 = array[np.where(array[:] > 4)]  # point selection
    array6 = array[array[:] > 4]            # boolean selection
"""

write.close()
