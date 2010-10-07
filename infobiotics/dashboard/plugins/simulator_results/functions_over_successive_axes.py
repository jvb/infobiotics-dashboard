import numpy as np


def functions_of_values_over_axis(array, array_axes, axis, functions): 
    ''' Returns an array similar in shape to 'array' but with the dimension 
    associated with 'axis' removed and a dimension of length len(functions)
    prepended. 

    >>> functions_of_values_over_axis(
    ...     np.zeros((1, 2, 3, 4)),
    ...     ('runs', 'species', 'compartments', 'timepoints'), 
    ...     'runs', 
    ...     (
    ...         lambda array, axis: np.mean(array, axis), 
    ...         lambda array, axis: np.std(array, axis, ddof=1)
    ...     )
    ... ).shape()
    (2,2,3,4)

    '''
    assert axis in array_axes
    assert len(functions) > 0
    for function in functions: assert callable(function) # each item in functions must be a callable, preferably a NumPy ufunc
    axis_index = array_axes.index(axis)
    out_shape = list(array.shape) # make a mutable copy of array.shape
    out_shape.pop(axis_index) # remove the axis functions will be applied along
    out_shape.insert(0, len(functions)) # prepend with functions axis
    out = np.empty(out_shape) # create output array
    for index, function in enumerate(functions): # iterate over functions
        out[index] = function(array, axis=axis_index) # apply function along axis
    return out

#def function_of_values_over_axis(array, array_axes, axis, function):
#    return functions_of_values_over_axis(array, array_axes, axis, [function])


def functions_of_values_over_successive_axes(array, array_axes, axes, functions):
    ''' Returns a tuple of the dimensionally reduced array and a tuple of remaining
    axes names.
     
    Applies each function in the 'functions' to the axis of 'array' indexed
    in 'array axes' from 'axes'. Each application reduces the dimensionality of
    'array' by one dimensional until either axes is exhausted or array has been
    reduced to a single value. 
    
    '''
    assert len(set(axes)) == len(axes) # no axis can be named more than once
    for axis in axes: assert axis in array_axes # each axis must be in array_axes 
    assert len(functions) == len(axes) # each axis must have a corresponding function
    for function in functions: assert callable(function) # each item in functions must be a callable, preferably a NumPy ufunc
    array_axes = list(array_axes[:]) # make a mutable copy of array_axes
    for index, function in enumerate(functions):
        axis = axes[index]
        array = function(array, axis=array_axes.index(axis)) # apply function
        array_axes.remove(axis)
    return array, tuple(array_axes)


mean = lambda array, axis: np.mean(array, axis, dtype=np.float64)

std = lambda array, axis: np.std(array, axis, ddof=1, dtype=np.float64)




class SimulatorResults(object):
    
    amounts_axes = ['runs', 'species', 'compartments', 'timepoints']
    
    volumes_axes = ['runs', 'compartments', 'timepoints']

    
    def functions_of_amounts_over_axis(self, axis, functions):
        ''' Narrow by amounts array. '''
        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, axis, functions)

    def functions_of_volumes_over_axis(self, axis, functions):
        ''' Narrow by volumes array. '''
        return functions_of_values_over_axis(self.volumes(), self.volumes_axes, axis, functions)
    
    def functions_of_amounts_over_runs(self, functions):
        ''' Narrow by amounts array and runs axis. '''
        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, 'runs', (functions))
    
    def mean_and_standard_deviation_of_amounts_over_runs(self):
        ''' Narrow by amounts array, runs axis and mean and std functions. '''
#        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, 'runs', (mean, std))
        return self.functions_of_amounts_over_runs(mean, std)


    def functions_of_amounts_over_successive_axes(self, axes, functions):
        ''' Narrow by amounts array. '''
        return functions_of_values_over_successive_axes(self.amounts(), self.amounts_axes, axes, functions)
    
    def functions_of_volumes_over_successive_axes(self, axes, functions):
        ''' Narrow by volumes array. '''
        return functions_of_values_over_successive_axes(self.volumes(), self.volumes_axes, axes, functions)

    
#    def chunk_generator(self, h5file): #TODO depends on array dimensions (a function for each) and order of dimensions to calculate functions over
#        pass
        


if __name__ == '__main__':
    SimulatorResults.amounts = lambda self: np.arange(48).reshape((2, 2, 3, 4))
    print SimulatorResults().amounts()
#    print SimulatorResults().mean_and_standard_deviation_of_amounts_over_runs()
    print SimulatorResults().functions_of_amounts_over_successive_axes(('compartments', 'species'), (lambda array, axis: np.sum(array, axis), lambda array, axis: np.sum(array, axis)))
