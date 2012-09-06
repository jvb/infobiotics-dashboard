'''
Created on 6 Sep 2012

@author: jvb
'''

import numpy as np

import tables

write = tables.openFile('test.h5', 'w')
#write.removeNode('/', 'a')
a = write.createEArray('/', 'a', tables.Int32Atom(), (2,3,0), expectedrows=4)
a.append(np.zeros((2,3,5)))

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
