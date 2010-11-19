__all__ = ['model', 'lpp']

from compartments import compartment
import numpy as np


# use 2D numpy array for lattice
def find_empty_2D_array_positions(array):
    empty = []
    for x, a in enumerate(np.equal(array, None)):
        for y, i in enumerate(a):
            if i:
                empty.append((x, y))
    return empty


class model(object):

    def __init__(self, compartments, **kwargs):
        self.distribution = compartments
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def distribution(self):
        return self._distribution
    
    @distribution.setter
    def distribution(self, compartments):
        ''' compartments can be a single compartment, a list of lists of compartments or a 2D NumPy array of dtype compartment. 
        A 2D array of compartments (the distribution) is then checked for empty positions. '''
        if isinstance(compartments, compartment):
            compartments = [[compartments]]
        if isinstance(compartments, list): # convert nested list to array
            compartments = np.array(compartments)
        if isinstance(compartments, np.ndarray) and len(compartments.shape) == 2:
            for c in compartments.flat:
                if not isinstance(c, compartment):
                    print 'got here'  
            distribution = compartments
        else:
            raise ValueError('Distributions (of compartments) must be 2 dimensional arrays of compartment objects.')
        empties = find_empty_2D_array_positions(distribution)
        if len(empties) > 0:
            for e in empties:
                print e
            raise ValueError('Some positions in the distribution are missing a compartment.')
        self._distribution = distribution

    @property
    def compartments(self):
        ''' Returns an iterator over all top-level compartments in the model. '''
        return self.distribution.flat
    
    def get_compartments(self):
        pass

lpp = model # alias

if __name__ == '__main__':
#    m = model() # ValueError
#    m = model(compartment())
#    m = model([compartment()]) # ValueError
#    m = model([[compartment()]])
#    m = model([[5]])
#    m = model(distribution([[compartment(a=1)]]))
#    m = model([[None]]) # ValueError
    m = model([[compartment()]], meta='test')
    print 'm.distribution.shape =', m.distribution.shape
    print 'm.distribution =', m.distribution
    print m.meta
#    
#    class WildType(compartment): rsmA = 1
#    class rsmAKnockout(WildType): rsmA = None
#    m = model([[rsmAKnockout(name='rsmA', _x=x, _y=y) if (x == 4 and y == 4) else WildType(name='wt', _x=x, _y=y) for x in range(10)] for y in range(10)])
#    print m.distribution.shape
#    for i in m.distribution:
#        for j in i:
#            print j.name, j._x, j._y 
