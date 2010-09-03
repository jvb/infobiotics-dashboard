# example function from npz_info
#def get_timeseries(run_index, species_index, compartment_index):
#    import numpy as np
#    f = np.load('levels.npz')
#    return f['levels'][run_index, species_index, compartment_index, :]
#print get_timeseries(0, 0, 0)

import numpy as np
f = np.load('levels.npz')
levels = f['levels']

def get_results_for_functions_over_axes(functions=(), axes=()):
    assert len(functions) == len(axes)
    results = levels # start with 4-dimensional (runs, species, compartments, timepoints) array
    results_axes = ['runs', 'species', 'compartments', 'timepoints'] 
    for fi, f in enumerate(functions):
        axis = axes[fi]
        results = f(results, axis=results_axes.index(axis))
        results_axes.remove(axis)
#    return results
    return results, tuple(results_axes)


# setup functions with correct degrees of freedom

import functools
mean = np.mean
#std = np.std
std = functools.partial(np.std, ddof=1)
std.__name__ = 'std'
#var = np.var
var = functools.partial(np.var, ddof=1)
var.__name__ = 'var'
median = np.median
max = np.amax
min = np.amin
sum = np.sum

all_functions = [mean, std, var, median, max, min, sum] 

#functions = [np.std]
#axes = ['runs']
#results, results_axes = get_results_for_functions_over_axes(functions, axes)

# 
original_shape = levels.shape
levels, all_axes = get_results_for_functions_over_axes()
#print levels
assert levels.shape == original_shape
#print all_axes


def test_get_results_for_functions_over_axes_works_for_any_axes_for_any_functions_in_any_order(all_axes, all_functions):
    '''
    Checks that all products of functions for all combinations of axes give the 
    same result no matter what order they are given in (rotation), providing the 
    same function is used for the same axis in a given iteration.
    
    all_axes is the set of axes
    all_functions is the set of functions
    
    n is the number of axes (greater than or equal to 2)
    a is a list containing a combination of n axes
    f is a list of functions, each corresponding to an axis in a
    o is a permuted order of application of f[i] to a[i]
    
    '''
    import itertools
    from collections import deque
    count = 0
    comb = []
    for n in range(2, len(all_axes) + 1): # 2 <= n <= len(all_axes)
        for a in itertools.combinations(all_axes, n):
            for f in itertools.product(all_functions, repeat=n):
#                unrotated_results, _ = get_results_for_functions_over_axes(f, a)
#                unrotated = '%s %s' % (a, f)
#                print zip(a, tuple([g.__name__ for g in f]))
                for o in itertools.permutations(range(n)):
                    count += 1
#                    da = deque(a)
#                    df = deque(f)
#                    for _ in range(1, n): # number of rotations
#                        for d in (da, df): # rotate a and f together
#                            d.rotate(1) # just rotate once since we are doing it in place with a and f
                    da = [a[i] for i in o]
                    df = [f[i] for i in o]
#                    print da, df
                    comb.append('%s %s' % (da, df))
#                    rotated = '%s %s' % (da, df)
#                    assert unrotated != rotated
#                    results, axes = get_results_for_functions_over_axes(df, da) 
#    #                assert results == unrotated_results # can't compare arrays this way :-(
#                    assert results.shape == unrotated_results.shape
#                    for s in itertools.product(*(range(i) for i in results.shape)):
#                        try:
#    #                        assert results[s] == unrotated_results[s] # hide float rounding errors
#                            assert str(results[s]) == str(unrotated_results[s])
#                        except AssertionError:
#                            print '    ', zip(da, tuple([g.__name__ for g in df])), results.shape, axes, s, str(results[s]), '!=', str(unrotated_results[s])
#                            return False
    print count
    print len(comb)
    print len(set(comb))
    assert len(comb) == len(set(comb))
    return True

print test_get_results_for_functions_over_axes_works_for_any_axes_for_any_functions_in_any_order(all_axes, all_functions)


## test if order of function application matters when axes are also changed
#print get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
#print '==\t' * 10
#print get_results_for_functions_over_axes((np.sum, np.mean), ('runs', 'compartments')) # functions and axes swapped = OK
#print '!=\t' * 10
#print get_results_for_functions_over_axes((np.sum, np.mean), ('compartments', 'runs')) # functions swapped but not axes = not OK (a different calculation)
#print '-' * 80
'''
[[ 300.          299.55555556  299.11111111 ...,  287.44444444
   287.44444444  287.44444444]
 [   0.            0.44444444    0.88888889 ...,   12.55555556
    12.55555556   12.55555556]]
==    ==    ==    ==    ==    ==    ==    ==    ==    ==    
[[ 300.          299.55555556  299.11111111 ...,  287.44444444
   287.44444444  287.44444444]
 [   0.            0.44444444    0.88888889 ...,   12.55555556
    12.55555556   12.55555556]]
!=    !=    !=    !=    !=    !=    !=    !=    !=    !=    
[[ 900.          898.66666667  897.33333333 ...,  862.33333333
   862.33333333  862.33333333]
 [   0.            1.33333333    2.66666667 ...,   37.66666667
    37.66666667   37.66666667]]
--------------------------------------------------------------------------------
'''


# now try to match npz results with hdf5 results

## subclass SimulatorResults so as not to disturb working code
#import simulator_results #FIXME takes ages to import - would separating classes into different modules speed this up?
#class SimulatorResults(simulator_results.SimulatorResults):
#
#    def get_results_for_functions_over_axes(self, functions, axes):
#        ''' 
#        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.mean, np.sum, np.mean), ('species', 'timepoints', 'runs'))
#        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.std, np.mean, np.product), ('compartments', 'runs', 'species'))
#        '''
#        results = levels # start with 4-dimensional (runs, species, compartments, timepoints) array
#        results_axes = ['runs', 'species', 'compartments', 'timepoints'] 
#        for fi, f in enumerate(functions):
#            axis = axes[fi]
#            results = f(results, axis=results_axes.index(axis))
#            results_axes.remove(axis)
#        return results#, results_axes
#
#results = SimulatorResults(
#     filename='/home/jvb/dashboard/examples/modules/module1.h5', #str(f['data_file_name']),
#     beginning=f['timepoints'][0],
#     end=f['timepoints'][-1],
#     every=f['timepoints'][1] - f['timepoints'][0],
#     species_indices=f['species_indices'],
#     compartment_indices=f['compartment_indices'],
#     run_indices=f['run_indices'],
#)
#
## before levels changes
#print get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
#print levels.shape
## change levels
#levels = results.get_amounts()[1]
#print len(levels), levels[0].shape
#print results.get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
'''
[[ 300.          299.55555556  299.11111111 ...,  287.44444444
   287.44444444  287.44444444]
 [   0.            0.44444444    0.88888889 ...,   12.55555556
    12.55555556   12.55555556]]
(3, 2, 9, 3601)
3 (2, 9, 3601)
[[ 300.          299.55555556  299.11111111 ...,  287.44444444
   287.44444444  287.44444444]
 [   0.            0.44444444    0.88888889 ...,   12.55555556
    12.55555556   12.55555556]]
'''

# works even though changed levels is a list of 3D arrays and original was a 4D array!
# because NumPy ufuncs work on arrays it is simply constructing an array from the list:   
#print np.array([levels[i] for i in range(len(levels))]).shape





#TODO 2 create interface for get_results_for_functions_over_axes  

#TODO 3 integrate with chunking algorithm below and in simulator_results:SimulatorResults.get_functions_over_runs

'''
chunked method used from get_functions_over_runs: 
1. create results array of correct dimensions, handling MemoryError
2. create 4-dimensional buffer that fits into memory
3. repeatedly fill and do stats on buffer filling results
4. do stats on remainder to finish filling results
5. return results

idea: seperate chunking from stats calculations
1. for any stats function from string_to_function dict
2. pass in results array creation function
3. pass in do stats function

problem: chunked method always chunks on timepoints dimension
solution1: change to chunk on whatever dimension 
solution2: don't chunk

code up a couple and see if/where/how they overlap
'''
