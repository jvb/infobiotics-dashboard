##import itertools
##axes = ('runs', 'species', 'compartments', 'timepoints')
##for i in range(2, len(axes)):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_function_over_' + '_and_'.join(combo) + '(self):', '#', '(' + ', '.join([axis for axis in axes if axis not in combo]) + ')\n\t\tpass'  
#
#    def get_function_over_runs_and_species(self, f): # (compartments, timepoints)
#        'of levels for all species in each compartment at each timepoint for all runs'
#        shape = (10000, 100000)
#        return np.zeros(shape)
#    def get_function_over_runs_and_compartments(self, f): # (species, timepoints)
#        'of levels of each species in all compartments at each timepoint for all runs'
#        shape = (100, 100000)
#        return np.zeros(shape)
#    def get_function_over_runs_and_timepoints(self, f): # (species, compartments)
#        'of levels of each species in each compartment at all timepoints for all runs'
#        shape = (100, 10000)
#        return np.zeros(shape)
#    def get_function_over_species_and_compartments(self, f): # (runs, timepoints)
#        'of levels for all species in all compartments at each timepoint in each run'
#        shape = (1000, 100000)
#        return np.zeros(shape)
#    def get_function_over_species_and_timepoints(self, f): # (runs, compartments)
#        'of levels for all species in each compartment at all timepoints in each run'
#        shape = (1000, 10000)
#        return np.zeros(shape)
#    def get_function_over_compartments_and_timepoints(self, f): # (runs, species)
#        'of levels of each species in all compartments at all timepoints in each run'
#        shape = (1000, 100)
#        return np.zeros(shape)
#    
#    def get_function_over_runs_and_species_and_compartments(self, f): # (timepoints)
#        'of levels for all species in all compartments at each timepoint for all runs'
#        shape = (100000,)
#        return np.zeros(shape)
#    def get_function_over_runs_and_species_and_timepoints(self, f): # (compartments)
#        'of levels for all species in each compartment at all timepoints for all runs'
#        shape = (10000,)
#        return np.zeros(shape)
#    def get_function_over_runs_and_compartments_and_timepoints(self, f): # (species)
#        'of levels of each species in all compartments at all timepoints for all runs'
#        shape = (100,)
#        return np.zeros(shape)
#    def get_function_over_species_and_compartments_and_timepoints(self, f): # (runs)
#        'of levels for all species in all compartments at all timepoints of each run'
#        shape = (1000,)
#        return np.zeros(shape)
#
#
##import itertools
##axes = ('runs', 'species', 'compartments', 'timepoints')
##for i in (1,):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_function_over_' + '_and_'.join(combo) + '(self):', '#', '(' + ', '.join([axis for axis in axes if axis not in combo]) + ')\n\t\tpass'  
#    
#    # these methods should apply a function along the over_x axis
#    def get_function_over_runs(self): # (species, compartments, timepoints)
#        'of levels for each species in each compartment at each timepoint for all runs'
#        shape = (100, 10000, 10000)
#        return np.zeros(shape)
#    def get_function_over_species(self): # (runs, compartments, timepoints)
#        'of levels for all species in each compartment at each timepoint for each run'
#        shape = (1000, 10000, 100000)
#        return np.zeros(shape)
#    def get_function_over_compartments(self): # (runs, species, timepoints)
#        'of levels for each species in all compartments at each timepoint for each run'
#        shape = (1000, 100, 100000)
#        return np.zeros(shape)
#    def get_function_over_timepoints(self): # (runs, species, compartments)
#        'of levels for each species in each compartment at all timepoints for each run'
#        shape = (1000, 100, 10000)
#        return np.zeros(shape)
#
##FIXME some of these are equivalent to some of the ones below, the arrays just have an extra dimension for runs where below would return a list of arrays of len(runs) 
#
##axes = ('species', 'compartments', 'timepoints')
##for i in range(1, len(axes)):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_levels_over_' + '_and_'.join(combo) + '(self):', '#', '[(' + ', '.join([axis for axis in axes if axis not in combo]) + ')]\n\t\tpass'  
#
#    def get_levels_over_species(self): # [(compartments, timepoints)]
#        'levels for all species in each compartment at each timepoint of each run'
#        shape = (10000, 100000)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_compartments(self): # [(species, timepoints)]
#        'levels of each species in all compartments at each timepoint of each run'
#        shape = (100, 100000)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_timepoints(self): # [(species, compartments)]
#        'levels of each species in each compartment at all timepoints of each run'
#        shape = (100, 10000)
#        return [np.zeros(shape) for _ in range(1000)]
#    
#    def get_levels_over_species_and_compartments(self): # [(timepoints)]
#        'levels for all species in all compartments at each timepoint of each run'
#        shape = (100000,)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_species_and_timepoints(self): # [(compartments)]
#        'levels for all species in each compartment at all timepoints of each run'
#        shape = (10000,)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_compartments_and_timepoints(self): # [(species)]
#        'levels of each species in all compartments for all timepoints of each run'
#        shape = (100)
#        return [np.zeros(shape) for _ in range(1000)]
#
#
#    string_to_method_map = {
#        'of levels for all species in each compartment at each timepoint for all runs':get_function_over_runs_and_species,
#        'of levels of each species in all compartments at each timepoint for all runs':get_function_over_runs_and_compartments,
#        'of levels of each species in each compartment at all timepoints for all runs':get_function_over_runs_and_timepoints,
#        'of levels for all species in all compartments at each timepoint in each run' :get_function_over_species_and_compartments,
#        'of levels for all species in each compartment at all timepoints in each run' :get_function_over_species_and_timepoints,
#        'of levels of each species in all compartments at all timepoints in each run' :get_function_over_compartments_and_timepoints,
#        'of levels for all species in all compartments at each timepoint for all runs':get_function_over_runs_and_species_and_compartments,
#        'of levels for all species in each compartment at all timepoints for all runs':get_function_over_runs_and_species_and_timepoints,
#        'of levels of each species in all compartments at all timepoints for all runs':get_function_over_runs_and_compartments_and_timepoints,
#        'of levels for all species in all compartments at all timepoints of each run' :get_function_over_species_and_compartments_and_timepoints,
#        '':get_function_over_runs,
#        '':get_function_over_species,
#        '':get_function_over_compartments,
#        '':get_function_over_timepoints,
##        '':,
#    }
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
#        return results
#
#    string_to_function_map = {
##        'median':,
#        'mean':lambda array: np.mean(array, axis=3),
#        'standard deviation':lambda array: np.std(array, ddof=1, axis=3),
##        'variance':,
##        'sum':lambda array: np.sum(array, axis=2), #TODO 2?
#    }
#
#    '''
#chunked method used from get_functions_over_runs: 
#1. create results array of correct dimensions, handling MemoryError
#2. create 4-dimensional buffer that fits into memory
#3. repeatedly fill and do stats on buffer filling results
#4. do stats on remainder to finish filling results
#5. return results
#
#idea: seperate chunking from stats calculations
#1. for any stats function from string_to_function dict
#2. pass in results array creation function
#3. pass in do stats function
#
#problem: chunked method always chunks on timepoints dimension
#solution1: change to chunk on whatever dimension 
#solution2: don't chunk
#
#code up a couple and see if/where/how they overlap
#    '''

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


#from collections import deque
import itertools

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
    
    count = 66473 when len(all_axes) = 4 and len(all_functions) = 7
    
    '''
    count = 0
    comb = []
#    for n in range(2, len(all_axes) + 1): # 2 <= n <= len(all_axes)
#        for a in itertools.combinations(all_axes, n):
#            for f in itertools.product(all_functions, repeat=n):
#                for o in itertools.permutations(range(n)):
#                    count += 1
#                    da = [a[i] for i in o]
#                    df = [f[i] for i in o]
#                    comb.append('%s %s' % (da, df))

    for n in range(len(all_axes) + 1):
        for f in itertools.product(all_functions, repeat=n):
            for a in itertools.permutations(all_axes, n):
                count += 1
                comb.append('%s %s' % (a, f))
    print count
    assert count == len(comb)
    assert len(comb) == len(set(comb))
    # all single axis and function pairings
    for i in range(66473 - 66444):
        print comb[i]
    print comb[66473 - 66444] # first pair of axes and function pairing
    return True

test_get_results_for_functions_over_axes_works_for_any_axes_for_any_functions_in_any_order(all_axes, all_functions)

#assert mean([get_results_for_functions_over_axes(f, a)[0] for a in itertools.permutations(all_axes, n) for f in itertools.product(all_functions, repeat=n) or n in range(len(all_axes) + 1)], axis=0) == 0



i = 0
for n in range(len(all_axes) + 1):
    for f in itertools.product(all_functions, repeat=n):
        for a in itertools.permutations(all_axes, n):
            i += 1
print i
exit()

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


#def empty(dims, dim_length):
#    return np.empty([dim_length for _ in range(dims)])
#
##def profile(f):
##    return f
#
#@profile
#def pop_first(a):
#    for _ in range(len(a.shape)):
#        a = np.sum(a, 0)
#    assert a.size == 1
##    print a.size
#    
#@profile
#def pop_last(a):
#    for _ in range(len(a.shape)):
#        a = np.sum(a, len(a.shape) - 1)
#    assert a.size == 1
##    print a.size
#    
#pop_first(empty(10, 7))
#pop_last(empty(10, 7))
