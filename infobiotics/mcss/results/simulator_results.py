import sip
sip.setapi('QString', 2)
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

mean = lambda array, axis: np.mean(array, axis, dtype=np.float64)
std = lambda array, axis: np.std(array, axis, ddof=1, dtype=np.float64)


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

def functions_of_values_over_axis_generator(array, array_axes, axis, functions): 
    ''' Returns a generator that yields arrays similar in shape to 'array' but 
    with the dimension associated with 'axis' removed, each containing the 
    result of applying a function along the index of the 'axis' in 'array_axes'. 

    >>> mean, std = functions_of_values_over_axis_generator(
    ...     np.zeros((1, 2, 3, 4)),
    ...     ('runs', 'species', 'compartments', 'timepoints'), 
    ...     'runs', 
    ...     (
    ...         lambda array, axis: np.mean(array, axis), 
    ...         lambda array, axis: np.std(array, axis, ddof=1)
    ...     )
    ... )
    >>> print mean.shape, std.shape
    (2,3,4) (2,3,4)

    '''
    assert axis in array_axes
    assert len(functions) > 0
    for function in functions: assert callable(function) # each item in functions must be a callable, preferably a NumPy ufunc
    axis_index = array_axes.index(axis)
    for function in functions: # iterate over functions
        yield function(array, axis=axis_index) # yield result of applying function along axis

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


class SimulatorResults(object):
    
    amounts_axes = ['runs', 'species', 'compartments', 'timepoints']
    
    volumes_axes = ['runs', 'compartments', 'timepoints']    
    
    timepoints_data_units = 'seconds'
    quantities_data_units = 'molecules'
    volumes_data_units = 'litres'
    timepoints_display_units = 'seconds'
    quantities_display_type = 'molecules'
    quantities_display_units = 'molecules'
    volumes_display_units = 'litres'
        
    def __init__(self,
        filename,
        simulation,
        beginning=0,
        end= -1,
        every=1,
        type=float, #decimal.Decimal
        species_indices=None,
        compartment_indices=None,
        run_indices=None,
        parent=None,
        timepoints_data_units='seconds',
        quantities_data_units='molecules',
        volumes_data_units='litres',
        timepoints_display_units='seconds', #TODO use timepoints_data_units if None
        quantities_display_type='molecules', #TODO determine from quantities data units if None
        quantities_display_units='molecules', #TODO use quantities_data_units if None
        volumes_display_units='litres', #TODO use volumes_data_units if None
    ):
        self.parent = parent # used by SimulatorResultsDialog for QMessageBox
        
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
            every = int(every)
        if every > self.finish:
            every = self.finish - self.start
        if every < 1:
            every = 1
        self.every = every

        self._timepoints = Quantity(all_timepoints[self.start:self.finish:self.every], time_units[timepoints_data_units])

        self.max_chunk_size = self.finish - self.start #TODO determine based on any axis not just timepoints

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
        self.timepoints_display_units = str(timepoints_display_units)
        self.quantities_display_type = str(quantities_display_type)
        self.quantities_display_units = str(quantities_display_units)
        self.volumes_display_units = str(volumes_display_units)


    def timepoints(self, timepoints_display_units=None):
        if timepoints_display_units is None:
            timepoints_display_units = self.timepoints_display_units
        timepoints = Quantity(self._timepoints, time_units[self.timepoints_data_units])
        timepoints.units = time_units[timepoints_display_units]    
        return timepoints
    
#        
    
    def allocate_array(self, shape, failed_message):
        '''
        
        >>> million = 1000 * 1000
        >>> results = allocate_array(million, million, million), 'Should raise a MemoryError')
        
        '''
        try:
            array = np.zeros(shape, self.type)
        except MemoryError:
            if self.parent is not None:
                QMessageBox.warning('Out of memory', failed_message)
            else:
                print failed_message
            return
        return array

    def volumes(self, volumes_display_units=None):
        # create array for extracted 'results', printing error if too big for memory
        volumes = self.allocate_array(
            (
                len(self.run_indices),
                len(self.compartment_indices),
                len(self._timepoints)
            ),
            'Could not allocate memory for volumes.\nTry selecting fewer ' \
            'runs, a shorter time window or a bigger time interval multipler.'
        )
        if volumes is None:
            return
        
        # extract results into array
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            volumes_for_one_run = h5.getNode(where, 'volumes')[:, self.start:self.finish:self.every]
            for ci, c in enumerate(self.compartment_indices):
                volumes[ri, ci, :] = volumes_for_one_run[c, :]
        h5.close()
    
        # adjust scale of volumes to match volumes_display_units
        volumes = Quantity(volumes, volume_units[self.volumes_data_units])
        if volumes_display_units is None:
            volumes_display_units = self.volumes_display_units
        volumes.units = volume_units[volumes_display_units]

        return volumes
    
    
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
        return self.functions_of_amounts_over_runs((mean, std))


    def functions_of_amounts_over_successive_axes(self, axes, functions):
        ''' Narrow by amounts array. '''
        return functions_of_values_over_successive_axes(self.amounts(), self.amounts_axes, axes, functions)
    
    def functions_of_volumes_over_successive_axes(self, axes, functions):
        ''' Narrow by volumes array. '''
        return functions_of_values_over_successive_axes(self.volumes(), self.volumes_axes, axes, functions)

    
#    def chunk_generator(self, h5file): #TODO depends on array dimensions (a function for each) and order of dimensions to calculate functions over
#        pass


#    @profile # use profile(results.get_amounts) instead - won't raise "'profile' not found" error
    def amounts(self, quantities_display_type=quantities_display_type, quantities_display_units=quantities_display_units, volume=None): 
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
#            return (self.get_timepoints(timepoints_display_units), [])
            return
        
#        results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self._timepoints)), self.type) for _ in self.run_indices]
        results = [
            self.allocate_array(
                (
                    len(self.species_indices),
                    len(self.compartment_indices),
                    len(self._timepoints)
                ),
                'Could not allocate memory for amounts.\n' \
                'Try selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            )
            for _ in self.run_indices
        ]
        if results is None:
            return
            
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
                    volumes = np.empty((len(self.run_indices), len(self.compartment_indices), len(self._timepoints)))
                    volumes.fill(volume)
                _volume_units = volume_units[self.volumes_data_units]
                _concentration_units = concentration_units[quantities_display_units]

                concentrations = np.zeros(results.shape)
                for ri, r in enumerate(self.run_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        for ti, _ in enumerate(self._timepoints):
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

        return results



        

    def get_functions_over_runs(self, functions):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of floats with the 
        shape (species, compartments, timepoint) for each function in 
        functions. '''
#        try:
#            results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self._timepoints)), self.type) for _ in functions]
#        except MemoryError:
#            message = 'Could not allocate memory for functions.\nTry selecting fewer functions, a shorter time window or a bigger time interval multipler.'
#            if self.parent is not None:
#                QMessageBox.warning('Out of memory', message)
#            else:
#                print message
#            return (self._timepoints, [])
        results = [
            self.allocate_array(
                (
                    len(self.species_indices),
                    len(self.compartment_indices),
                    len(self._timepoints)
                ),
                'Could not allocate memory for functions.\n' \
                'Try selecting fewer functions, a shorter time window or a bigger time interval multipler.'
            )
            for _ in self.run_indices
        ]
        if results is None:
            return        

        chunk_size = self.max_chunk_size

        # create large arrays handling failure
        buffer = None
        while buffer == None:
            # allocate buffer (4-dimensional array)
            try:
                buffer = np.zeros((len(self.species_indices),
                                      len(self.compartment_indices),
                                      chunk_size,
                                      len(self.run_indices)),
                                      self.type)
            except MemoryError:
                if chunk_size == 0:
                    if self.parent is not None:
                        message = 'Could not allocate memory for chunk.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                        return
                # progressively halve chunkSize until buffer fits into memory
                chunk_size = chunk_size // 2
                buffer = None
                continue

        def iteration():
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
        quotient = len(self._timepoints) // chunk_size
        for _ in range(quotient):
            iteration()#chunk_size)
            amounts_chunk_start = self.amounts_chunk_end
            stat_chunk_start = self.statChunkEnd

        # and the remaining timepoints           
        remainder = len(self._timepoints) % chunk_size
        if remainder > 0:
            buffer = np.zeros((len(self.species_indices),
                               len(self.compartment_indices),
                               remainder,
                               len(self.run_indices)),
                               type)
            iteration(remainder)

        h5.close()
        return (self._timepoints, results)


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
        for s in selected_species:
            surface = np.zeros(((xmax - xmin) + 1, (ymax - ymin) + 1, len(self._timepoints)), self.type)

            # fill surface with amounts
            for r in self.run_indices: # only one for now, see SimulationResultsDialog.update_ui()
                where = '/run%s' % (r + 1)
                try:
                    amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.finish:self.every]
                except MemoryError:
                    message = 'Could not allocate memory for amounts.\nTry selecting fewer species, a shorter time window or a bigger time interval multipler.'
                    if self.parent is not None:
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                    return (self._timepoints, [], None, None, None, None)
                if sum_compartments_at_same_xy_lattice_position:
                    for c in selected_compartments:
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :] + surface[c.x_position, c.y_position, :]
                else:
                    for c in selected_compartments:
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :]
            results.append(surface)
        h5.close()
        return (self._timepoints, results, xmin, xmax, ymin, ymax)


#def test():
##    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/NAR-poptimizer/NAR_output.h5')
##    w = SimulationResultsDialog(filename='/home/jvb/phd/eclipse/infobiotics/dashboard/tests/NAR-ok/simulation.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
#
#    if w.loaded:
##        w.ui.species_list_widget.selectAll()
##        w.ui.species_list_widget.setCurrentItem(w.ui.species_list_widget.findItems("proteinGFP", Qt.MatchExactly)[0])
##        for item in w.ui.species_list_widget.findItems("protein1*", Qt.MatchWildcard): item.setSelected(True)
#
##        w.ui.compartments_list_widget.selectAll()
##        w.ui.compartments_list_widget.setCurrentItem(w.ui.compartments_list_widget.item(0))
#
##        w.ui.runs_list_widget.setCurrentItem(w.ui.runs_list_widget.item(0))
#
#        for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
#            widget.item(0).setSelected(True)
#            widget.item(widget.count() - 1).setSelected(True)
#
#        w.ui.average_over_selected_runs_check_box.setChecked(False)
#
####        w.ui.visualise_population_button.click()
#
###        w.plot()
###        w.plotsPreviewDialog.ui.plotsListWidget.selectAll() #TODO rename
###        w.plotsPreviewDialog.combine()
#
##        w.export_data_as('test.csv')    # write_csv
##        w.export_data_as('test.txt')   # write_csv
##        w.export_data_as('test', open_after_save=False)        # write_csv
##        w.export_data_as('test.xls')    # write_xls
#        w.export_data_as('test.npz')    # write_npz
#
##    centre_window(w)
##    w.show()
#
#
#def test_SimulatorResults_export_data_as():
##    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/modules/module1.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
#    for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
#        widget.item(0).setSelected(True)
#        widget.item(widget.count() - 1).setSelected(True)
#    w.ui.average_over_selected_runs_check_box.setChecked(False)
##    w.export_data_as('test.csv')    # write_csv
#    w.export_data_as('test.xls')    # write_xls
##    w.export_data_as('test.npz')    # write_npz
#
#
#def test_volumes():
#    w = main()
#    w.ui.runs_list_widget.select(0)
#    w.ui.species_list_widget.select(-1)
#    w.ui.species_list_widget.select(-2)
#    w.ui.compartments_list_widget.select(-1)
#    w.ui.compartments_list_widget.select(-2)
#    w.every = 100
#    p = w.plot()
##    p.ui.plotsListWidget.selectAll()
##    p.combine()
    

#def profile_SimulatorResults_get_amounts():
#    results = SimulatorResults(
#        '/home/jvb/dashboard/examples/germination_09.h5',
#        None,
#    )
#    get_amounts = profile(results.get_amounts)
#    amounts = get_amounts()
#    print amounts
#    exit()


import sys
from PyQt4.QtGui import qApp
def main():
    argv = qApp.arguments()
#    argv.insert(1, '/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/simulation.h5')
    argv.insert(1, '/home/jvb/phd/eclipse/infobiotics/dashboard/examples/mcss-postprocess/germination_09.h5')
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

