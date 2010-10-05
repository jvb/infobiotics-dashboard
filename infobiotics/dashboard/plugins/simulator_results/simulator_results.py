from infobiotics.commons.qt4 import centre_window
from infobiotics.commons.quantities.traits_ui_converters import Quantity, \
    time_units, substance_units, concentration_units, volume_units
from simulation import load_h5
from simulator_results_dialog import \
    SimulatorResultsDialog as SimulationResultsDialog
import bisect
import math
import numpy as np
import tables
#import decimal

sum_compartments_at_same_xy_lattice_position = True
            
class SimulatorResults(object):
    
    def __init__(self,
        filename,
        simulation,
        beginning=0,
        end= -1,
        every=1,
        chunk_size=2 ** 20,
        type=float, #decimal.Decimal
        species_indices=None,
        compartment_indices=None,
        run_indices=None,
        parent=None,
        timepoints_data_units='seconds',
        quantities_data_units='molecules',
        volumes_data_units='litres',
    ):
        
        self.parent = parent
        
        self.type = type
        
        if simulation is None:
            self.simulation = load_h5(filename)
        else:
            self.simulation = simulation#load_h5(filename) # why do all that object creation again?
        
        self.filename = filename
        
        number_of_timepoints = self.simulation._runs_list[0].number_of_timepoints
        
        log_interval = self.simulation.log_interval
        
        max_time = number_of_timepoints * log_interval#= self.simulation.max_time
        
        all_timepoints = np.linspace(0, max_time, number_of_timepoints + 1)

        if 0 < beginning < all_timepoints[-1]:
            # make start the index of the timepoint closest to, and including, beginning
            self.start = bisect.bisect_left(all_timepoints, math.floor(beginning))
        else:
            # make start the index of the first timepoint
            self.start = 0

        if 0 < end < beginning:
            # shouldn't have to happen because of spinboxes synchronised min/max
            end = -1

        if 0 < end < all_timepoints[-1]:
            # make finish the index of the timepoint closest to, and including, end
            self.finish = bisect.bisect_right(all_timepoints, math.ceil(end))
        else:
            # make finish the index of the final timepoint + 1
            self.finish = len(all_timepoints) #- 1

        if every is not int:
            self.every = int(every)
        else:
            self.every = every
        if every < 1:
            self.every = 1
        if every > self.finish:
            self.every = self.finish - self.start

#        self.timepoints = all_timepoints[self.start:self.finish:self.every]
        self.timepoints = Quantity(all_timepoints[self.start:self.finish:self.every], time_units[timepoints_data_units])

        if chunk_size is not int:
            self.chunkSize = int(chunk_size)
        else:
            self.chunkSize = chunk_size
        if chunk_size < 1:
            self.chunkSize = 1
        if chunk_size > self.finish:
            self.chunkSize = self.finish - self.start

        if species_indices is None:
            self.species_indices = range(self.simulation.number_of_species)
        else:
            self.species_indices = species_indices
        if compartment_indices is None:
            self.compartment_indices = range(self.simulation._runs_list[0].number_of_compartments)
        else:
            self.compartment_indices = compartment_indices
        if run_indices is None:
            self.run_indices = range(0, self.simulation.number_of_runs)
        else:
            self.run_indices = run_indices

        self.timepoints_data_units = str(timepoints_data_units)
        self.quantities_data_units = str(quantities_data_units)
        self.volumes_data_units = str(volumes_data_units)

    # shared class variables used for default arguments, they should not be referenced using self.timepoints_display_units, for instance.
    timepoints_display_units = 'seconds'
    quantities_display_type = 'molecules'
    quantities_display_units = 'molecules'
    volumes_display_units = 'litres'

#    @profile # use profile(results.get_amounts) instead - won't raise "'profile' not found" error
    def get_amounts(self, quantities_display_type=quantities_display_type, quantities_display_units=quantities_display_units, volume=None, timepoints_display_units=timepoints_display_units):#, volumes_display_units='litres'): 
#        ''' Returns a tuple of (timepoints, results) where timepoints is an 1 - D
#        array of floats and results is a list of 3-D arrays of ints with the 
#        shape (species, compartments, timepoint) for each run. '''
        '''
        
        'volume' is used when self.simulation.log_volumes != 1 to fill an array 
        that is the same shape as volumes would be, allowing concentrations to
        be calculated for models without volumes information. 
        
        '''
        if quantities_display_type == 'concentrations' and self.simulation.log_volumes != 1 and volume is None:
            message = 'Cannot calculate concentrations without volumes dataset, rerun simulation with log_volumes=1' 
            if self.parent is not None:
                QMessageBox.warning('Error', message) #TODO test
            else:
                print message
            return (self.get_timepoints(timepoints_display_units), [])
        
        try:
#            million = 1000 * 1000; results = np.zeros((million, million, million)) # should raise a MemoryError
            results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self.timepoints)), self.type) for _ in self.run_indices]
        except MemoryError:
            message = 'Could not allocate memory for amounts.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.finish:self.every]
            for si, s in enumerate(self.species_indices):
                for ci, c in enumerate(self.compartment_indices):
                    results[ri][si, ci, :] = amounts[s, c, :]
#                    results[ri][si, ci, :] = h5.getNode(where, 'amounts')[s, c, self.start:self.finish:self.every] # about 10 times slower!
        h5.close()

        results = np.array(results) # convert from list of 3D arrays to 4D array #TODO test
        results = Quantity(results, substance_units[self.quantities_data_units])

        if self.quantities_data_units != quantities_display_units:
            
            # convert to moles
#            if self.quantities_data_units == 'moles':
#                results = Quantity(results, mole)
#            elif self.quantities_data_units.endswith('moles'):
#                converter = SubstanceConverter(
#                    data=results,
#                    data_units=self.quantities_data_units,
#                    display_units='moles',
#                )
#                results = converter.display_quantity
#            else: # molecules
#                results = Quantity(results / N_A, mole)
            results.units = substance_units['moles']

            # convert from moles to whatever
            if quantities_display_type == 'concentrations':
                
                if self.simulation.log_volumes == 1:
                    _, volumes = self.get_volumes(self.volumes_data_units)
                else:
                    assert volume is not None
                    volumes = np.empty((len(self.run_indices), len(self.compartment_indices), len(self.timepoints)))
                    volumes.fill(volume)
                _volume_units = volume_units[self.volumes_data_units]
                _concentration_units = concentration_units[quantities_display_units]

                concentrations = np.zeros(results.shape)
                for ri, r in enumerate(self.run_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        for ti, t in enumerate(self.timepoints):
                            # can't replace results in-place as it raises a dimensionality error
                            volume = volumes[ri, ci, ti]
                            if volume <= 0:
                                concentrations[ri, :, ci, ti] = np.zeros(results[ri, :, ci, ti].shape) 
                            else:
                                concentrations[ri, :, ci, ti] = (results[ri, :, ci, ti] / (volume * _volume_units)).rescale(_concentration_units)
                results = Quantity(concentrations, _concentration_units)

#            elif quantities_display_units.endswith('moles'):
#                converter = SubstanceConverter(
#                    data=results,
#                    data_units='moles',
#                    display_units=quantities_display_units,
#                )
#                results = converter.display_quantity
#            else: # molecules
#                results = results * N_A
            else:
                results = Quantity(results, substance_units[self.quantities_data_units])
                results.units = substance_units[quantities_display_units]

        return self.get_timepoints(timepoints_display_units), results


    def get_timepoints(self, timepoints_display_units):
#        if self.timepoints_data_units != timepoints_display_units:
#            converter = TimeConverter(
#                data=self.timepoints,
#                data_units=self.timepoints_data_units,
#                display_units=timepoints_display_units
#            )
#            timepoints = converter.display_quantity
#        else:
#            timepoints = Quantity(self.timepoints, time_units[timepoints_display_units])
        timepoints = Quantity(self.timepoints, time_units[self.timepoints_data_units])
        timepoints.units = time_units[timepoints_display_units]    
        return timepoints
        

    def get_volumes(self, volumes_display_units=volumes_display_units, timepoints_display_units=timepoints_display_units):
        
        # create array for extracted 'results', printing error if too big for memory
        try:
            results = np.zeros((len(self.run_indices), len(self.compartment_indices), len(self.timepoints)), self.type)
        except MemoryError:
            message = 'Could not allocate memory for volumes.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])
        
        # extract results into array
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            volumes = h5.getNode(where, 'volumes')[:, self.start:self.finish:self.every]
            for ci, c in enumerate(self.compartment_indices):
                results[ri, ci, :] = volumes[c, :]
        h5.close()
    
        # adjust scale of volumes to match volumes_display_units
        results = Quantity(results, volume_units[self.volumes_data_units])
        results.units = volume_units[volumes_display_units]
        return self.get_timepoints(timepoints_display_units), results
        
    def get_volumes_mean_over_runs(self):
        raise NotImplementedError
        
        


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
#

    mean = lambda array: np.mean(array, axis=3)
    std = lambda array: np.std(array, ddof=1, axis=3)

    def get_amounts_mean_over_runs(self):
        return self.get_functions_over_runs((lambda array: np.mean(array, axis=3),))
#        return self.get_functions_over_runs((SimulatorResults.mean,))
#        return self.get_functions_over_runs((self.mean,))

    def chunk_generator(self, h5file):
        pass

    def get_functions_over_runs(self, functions):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of floats with the 
        shape (species, compartments, timepoint) for each function in 
        functions. '''
        try:
            results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self.timepoints)), self.type) for _ in functions]
        except MemoryError:
            message = 'Could not allocate memory for amounts.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])

        # create large arrays handling failure
        buffer = None
        while buffer == None:
            # allocate buffer (4-dimensional array)
            try:
                buffer = np.zeros((len(self.species_indices),
                                      len(self.compartment_indices),
                                      self.chunkSize,
                                      len(self.run_indices)),
                                      type)
            except MemoryError:
                if self.chunkSize == 0:
                    if self.parent is not None:
                        message = 'Could not allocate memory for chunk.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                        return
                # progressively halve chunkSize until buffer fits into memory
                self.chunkSize = self.chunkSize // 2
                buffer = None
                continue

#            # try to get statistics from data in buffer
#            try:
#                for fi, f in enumerate(functions):
#                    f(buffer)
#            except MemoryError:
#                # progressively halve chunk_size until statistics can be done
#                self.chunk_size = self.chunk_size // 2
#                buffer = None
#                continue

        def iteration(chunk_size):
            """One iteration reads amounts into buffer and applies statistical functions to those amounts."""
            self.amounts_chunk_end = amounts_chunk_start + (chunk_size * self.every)
            for ri, r in enumerate(self.run_indices):
                where = '/run%s' % (r + 1)
                amounts = h5.getNode(where, 'amounts')[:, :, amounts_chunk_start:self.amounts_chunk_end:self.every]
                for si, s in enumerate(self.species_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        buffer[si, ci, :, ri] = amounts[s, c, :] #FIXME works but surely buffer[:, :, :, ri] = amounts[self.species_indices, self.compartment_indices, :] could work too, no?
            self.statChunkEnd = stat_chunk_start + chunk_size
#            print results[1][:,:,stat_chunk_start:self.statChunkEnd]
#            print "amounts.shape: ", amounts.shape, "buffer.shape: ", buffer.shape
#            print "buffer:"
#            print buffer
            for fi, f in enumerate(functions):
                stat = results[fi][:]
                stat[:, :, stat_chunk_start:self.statChunkEnd] = f(buffer)
#                print stat[:,:,stat_chunk_start:self.statChunkEnd], "=", "std(", buffer, ")"

        h5 = tables.openFile(self.filename)

        amounts_chunk_start = self.start
        stat_chunk_start = 0
        # for each whole chunk
        quotient = len(self.timepoints) // self.chunkSize
        for i in range(quotient):
            iteration(self.chunkSize)
            amounts_chunk_start = self.amounts_chunk_end
            stat_chunk_start = self.statChunkEnd

        # and the remaining timepoints           
        remainder = len(self.timepoints) % self.chunkSize
        if remainder > 0:
            buffer = np.zeros((len(self.species_indices),
                               len(self.compartment_indices),
                               remainder,
                               len(self.run_indices)),
                               type)
            iteration(remainder)

        h5.close()
        return (self.timepoints, results)


    def get_surfaces(self):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of floats with the 
        shape (x_position, y_position, timepoint) for each species. '''

        selected_compartments = [compartment for compartment in self.simulation._runs_list[self.run_indices[0]]._compartments_list]
        selected_species = [self.simulation._species_list[i] for i in self.species_indices]

        # create 3D array [x,y,t] for amounts data, x and y dimensions should represent total space
        all_compartments = selected_compartments[0].run._compartments_list
        xmax = max([compartment.x_position for compartment in all_compartments])
        xmin = min([compartment.x_position for compartment in all_compartments])
        ymax = max([compartment.y_position for compartment in all_compartments])
        ymin = min([compartment.y_position for compartment in all_compartments])

        h5 = tables.openFile(self.filename)
        results = []
        for si, s in enumerate(selected_species):
            surface = np.zeros(((xmax - xmin) + 1, (ymax - ymin) + 1, len(self.timepoints)), self.type)

            # fill surface with amounts
            for ri, r in enumerate(self.run_indices): # only one for now, see SimulationResultsDialog.update_ui()
                where = '/run%s' % (r + 1)
                try:
                    amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.finish:self.every]
                except MemoryError:
                    message = 'Could not allocate memory for amounts.\nTry selecting fewer species, a shorter time window or a bigger time interval multipler.'
                    if self.parent is not None:
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                    return (self.timepoints, [], None, None, None, None)
                if sum_compartments_at_same_xy_lattice_position:
                    for ci, c in enumerate(selected_compartments):
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :] + surface[c.x_position, c.y_position, :]
                else:
                    for ci, c in enumerate(selected_compartments):
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :]
            results.append(surface)
        h5.close()
        return (self.timepoints, results, xmin, xmax, ymin, ymax)






def test():
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/NAR-poptimizer/NAR_output.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/phd/eclipse/infobiotics/dashboard/tests/NAR-ok/simulation.h5')
    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')

    if w.loaded:
#        w.ui.species_list_widget.selectAll()
#        w.ui.species_list_widget.setCurrentItem(w.ui.species_list_widget.findItems("proteinGFP", Qt.MatchExactly)[0])
#        for item in w.ui.species_list_widget.findItems("protein1*", Qt.MatchWildcard): item.setSelected(True)

#        w.ui.compartments_list_widget.selectAll()
#        w.ui.compartments_list_widget.setCurrentItem(w.ui.compartments_list_widget.item(0))

#        w.ui.runs_list_widget.setCurrentItem(w.ui.runs_list_widget.item(0))

        for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
            widget.item(0).setSelected(True)
            widget.item(widget.count() - 1).setSelected(True)

        w.ui.average_over_selected_runs_check_box.setChecked(False)

###        w.ui.visualise_population_button.click()

##        w.plot()
##        w.plotsPreviewDialog.ui.plotsListWidget.selectAll() #TODO rename
##        w.plotsPreviewDialog.combine()

#        w.export_data_as('test.csv')    # write_csv
#        w.export_data_as('test.txt')   # write_csv
#        w.export_data_as('test', open_after_save=False)        # write_csv
#        w.export_data_as('test.xls')    # write_xls
        w.export_data_as('test.npz')    # write_npz

#    centre_window(w)
#    w.show()


def test_SimulatorResults_export_data_as():
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/modules/module1.h5')
    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
    for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
        widget.item(0).setSelected(True)
        widget.item(widget.count() - 1).setSelected(True)
    w.ui.average_over_selected_runs_check_box.setChecked(False)
#    w.export_data_as('test.csv')    # write_csv
    w.export_data_as('test.xls')    # write_xls
#    w.export_data_as('test.npz')    # write_npz


def test_volumes():
    w = main()
    w.ui.runs_list_widget.select(0)
    w.ui.species_list_widget.select(-1)
    w.ui.species_list_widget.select(-2)
    w.ui.compartments_list_widget.select(-1)
    w.ui.compartments_list_widget.select(-2)
    w.every = 100
    p = w.plot()
#    p.ui.plotsListWidget.selectAll()
#    p.combine()
    

def profile_SimulatorResults_get_amounts():
    results = SimulatorResults(
        '/home/jvb/dashboard/examples/germination_09.h5',
        None,
    )
    get_amounts = profile(results.get_amounts)
    amounts = get_amounts()
    print amounts
    exit()

def main():
    argv = qApp.arguments()
#    argv.insert(1, '/home/jvb/dashboard/examples/modules/module1.h5')
    argv.insert(1, '/home/jvb/dashboard/examples/germination_09.h5')
    if len(argv) > 2:
        print 'usage: python simulator_results.py {h5file}'#mcss_results.sh {h5file}'
        sys.exit(2)
    if len(argv) == 1:
#        shared.settings.register_infobiotics_settings()
        w = SimulationResultsDialog()
    elif len(argv) == 2:
        w = SimulationResultsDialog(filename=argv[1])
    centre_window(w)
    w.show()
    return w
#    shared.settings.restore_window_size_and_position(w)


if __name__ == "__main__":
    main()
#    test()
#    test_SimulatorResults_export_data_as()
#    test_volumes()
#    profile_SimulatorResults_get_amounts()
    exit(qApp.exec_())

