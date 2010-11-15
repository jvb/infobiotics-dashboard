__all__ = ['model', 'lpp']

from compartment import compartment
from enthought.traits.api import HasTraits, Array
import numpy as np

# use 2D numpy array for lattice
def find_empty_2D_array_positions(array):
    empty = []
    for x, a in enumerate(np.equal(array, None)):
        for y, i in enumerate(a):
            if i:
                empty.append((x, y))
    return empty

class model(HasTraits):
    distribution = Array(dtype=compartment)
    def empty_positions(self):
        return find_empty_2D_array_positions(self.distribution)

lpp = model # alias
