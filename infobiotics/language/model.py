__all__ = ['model', 'lpp', 'distribution', 'bounded_distribution', 'print_distribution']

from compartments import compartment
import numpy as np


def distribution(fill_compartment_callable, width, height, fill_compartment_args=(), fill_compartment_kwargs={}):
    ''' Returns a 2D array of shape (width, height) fill with fill_compartment(*fill_compartment_args, **fill_compartment_kwargs).
    
    Sets _x and _y for each compartment.
    
    '''
    return np.array(
        [
            [
                fill_compartment_callable(*fill_compartment_args, _x=x, _y=y, **fill_compartment_kwargs)
                for x in range(width)
            ]
            for y in range(height)
        ]
    ) 


def bounded_distribution(fill_compartment_callable, boundary_compartment_callable, width, height, boundary_width=1, boundary_height=1, fill_compartment_args=(), fill_compartment_kwargs={}, boundary_compartment_args=(), boundary_compartment_kwargs={}):
    ''' Returns a 2D array of shape (width, height) with boundary compartments... 
    
    Sets _x and _y for each compartment.
    
    '''
    return np.array(
        [
            [
                fill_compartment_callable(*fill_compartment_args, _x=x, _y=y, **fill_compartment_kwargs) if boundary_width <= x < width - boundary_width and boundary_height <= y < height - boundary_height else boundary_compartment_callable(*boundary_compartment_args, _x=x, _y=y, **boundary_compartment_kwargs)
                for x in range(width)
            ]
            for y in range(height)
        ]
    )


def print_distribution(distribution):
    for x in distribution:
        for y in x:
            print y.__class__.__name__[0],
        print
        

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
        for k, v in kwargs.items(): setattr(self, k, v)

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
                    raise ValueError('All items in distribution must be compartments: %s found instead.' % c)
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
    
#    def get_compartments(self):
#        pass

lpp = model # alias


if __name__ == '__main__':
#    m = model() # ValueError
#    m = model(compartment())
#    m = model([compartment()]) # ValueError
#    m = model([[compartment()]])
#    m = model([[5]])
#    m = model(distribution([[compartment(a=1)]]))
#    m = model([[None]]) # ValueError

#    m = model([[compartment()]], meta='test')
#    print 'm.distribution.shape =', m.distribution.shape
#    print 'm.distribution =', m.distribution
#    print m.meta
    
#    class WildType(compartment): rsmA = 1
#    class rsmAKnockout(WildType): rsmA = None
#    m = model([[rsmAKnockout(name='rsmA', _x=x, _y=y) if (x == 4 and y == 4) else WildType(name='wt', _x=x, _y=y) for x in range(10)] for y in range(10)])
#    print m.distribution.shape
#    for i in m.distribution:
#        for j in i:
#            print j.name, j._x, j._y 

    class boundary(compartment):
        pass

    m = model(bounded_distribution(compartment, boundary, 10, 10))
    print_distribution(m.distribution)


#    # model is evalable!
#    a = eval("""model(
#        [
#            [
#                compartment(
#                    bacteria(),
#                    label='media',
#                    _x=x,
#                    _y=y,
#                ) 
#                for x in range(1)
#            ] 
#            for y in range(1)
#        ]
#    )""")
#    print a
