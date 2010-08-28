# example function from npz_info
#def get_timeseries(run_index, species_index, compartment_index):
#    import numpy as np
#    f = np.load('levels.npz')
#    return f['levels'][run_index, species_index, compartment_index, :]
#print get_timeseries(0, 0, 0)

import numpy as np
f = np.load('levels.npz')
levels = f['levels']

def get_results_for_functions_over_axes(functions, axes):
    results = levels # start with 4-dimensional (runs, species, compartments, timepoints) array
    results_axes = ['runs', 'species', 'compartments', 'timepoints'] 
    for fi, f in enumerate(functions):
        axis = axes[fi]
        results = f(results, axis=results_axes.index(axis))
        results_axes.remove(axis)
    return results

# test if order of function application matters when axes are also changed
print get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
print '==\t' * 10
print get_results_for_functions_over_axes((np.sum, np.mean), ('runs', 'compartments')) # functions and axes swapped = OK
print '!=\t' * 10
print get_results_for_functions_over_axes((np.sum, np.mean), ('compartments', 'runs')) # functions swapped but not axes = not OK (a different calculation)
print '-' * 80
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

# subclass SimulatorResults so as not to disturb working code
import simulator_results #FIXME takes ages to import - would separating classes into different modules speed this up?
class SimulatorResults(simulator_results.SimulatorResults):

    def get_results_for_functions_over_axes(self, functions, axes):
        ''' 
        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.mean, np.sum, np.mean), ('species', 'timepoints', 'runs'))
        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.std, np.mean, np.product), ('compartments', 'runs', 'species'))
        '''
        results = levels # start with 4-dimensional (runs, species, compartments, timepoints) array
        results_axes = ['runs', 'species', 'compartments', 'timepoints'] 
        for fi, f in enumerate(functions):
            axis = axes[fi]
            results = f(results, axis=results_axes.index(axis))
            results_axes.remove(axis)
        return results#, results_axes

results = SimulatorResults(
     filename='/home/jvb/dashboard/examples/modules/module1.h5', #str(f['data_file_name']),
     beginning=f['timepoints'][0],
     end=f['timepoints'][-1],
     every=f['timepoints'][1] - f['timepoints'][0],
     species_indices=f['species_indices'],
     compartment_indices=f['compartment_indices'],
     run_indices=f['run_indices'],
)

# before levels changes
print get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
print levels.shape
# change levels
levels = results.get_amounts()[1]
print len(levels), levels[0].shape
print results.get_results_for_functions_over_axes((np.mean, np.sum), ('compartments', 'runs'))
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

# seems to work even though changed levels is a list of 3D arrays and original was 4D array. NumPy is doing some magic - boardcasting? 

#TODO 1 find out about broadcasting  

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
