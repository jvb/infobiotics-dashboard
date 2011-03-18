'''Provides the McssResults class for getting simulation data out of h5 files
and functions for applying NumPy ufuncs multi-dimensional arrays.'''

import sip
from quantities.units.time import hour, minute
import operator
from table import indent
sip.setapi('QString', 2)
from PyQt4.QtGui import QMessageBox

from infobiotics.commons.quantities.traits_ui_converters import Quantity, time_units, substance_units, concentration_units, volume_units

from simulation import load_h5

import bisect
import math
#import decimal

import numpy as np

import tables


sum_compartments_at_same_xy_lattice_position = True

# pre-defined functions that are applied along one axis 
mean = lambda array, axis: np.mean(array, axis, dtype=np.float64)
#std = lambda array, axis: np.std(array, axis, ddof=1, dtype=np.float64)
std = lambda array, axis: Quantity(np.std(array.magnitude, axis, ddof=1, dtype=np.float64), array.units) if isinstance(array, Quantity) else np.std(array, axis, ddof=1, dtype=np.float64) # work around Quantity.std not having 'ddof' keyword argument
var = lambda array, axis: Quantity(np.var(array.magnitude, axis, ddof=1, dtype=np.float64), array.units) if isinstance(array, Quantity) else np.var(array, axis, ddof=1, dtype=np.float64) # work around Quantity.var not having 'ddof' keyword argument
sum = lambda array, axis: np.sum(array, axis, dtype=np.float64)

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
    is_quantity = isinstance(array, Quantity)
    if is_quantity:
        units = array.units
    axis_index = array_axes.index(axis)
    out_shape = list(array.shape) # make a mutable copy of array.shape
    out_shape.pop(axis_index) # remove the axis functions will be applied along
    out_shape.insert(0, len(functions)) # prepend with functions axis
    out = np.empty(out_shape) # create output array
    for index, function in enumerate(functions): # iterate over functions
        out[index] = function(array, axis=axis_index) # apply function along axis
    if is_quantity:
        out = Quantity(out, units)
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


class McssResults(object):

#    amounts_axes = ['runs', 'species', 'compartments', 'timepoints']
    
#    volumes_axes = ['runs', 'compartments', 'timepoints']    
    
#    timepoints_data_units = 'seconds'
#    quantities_data_units = 'molecules'
#    volumes_data_units = 'litres'
#    timepoints_display_units = 'seconds'
#    quantities_display_type = 'molecules'
#    quantities_display_units = 'molecules'
#    volumes_display_units = 'litres'
        
    def __init__(self,
        filename,
        simulation=None, # McssResultsWidget can provide pre-loaded Simulation here
        from_=0,
        to= -1, #TODO change to 'end'
        #TODO add start, stop and timestep
        step=1,
        type=float,
        species_indices=None,
        compartment_indices=None,
        run_indices=None,
        parent=None,
        timepoints_data_units='seconds',
        quantities_data_units='molecules',
        volumes_data_units='litres',
        quantities_display_type=None, #'molecules',
        timepoints_display_units=None,
        quantities_display_units=None,
        volumes_display_units=None,
        **ignored_kwargs
    ):
        # these can all raise ValueErrors
        self.timepoints_data_units = str(timepoints_data_units)
        self.quantities_data_units = str(quantities_data_units)
        self.volumes_data_units = str(volumes_data_units)

        if quantities_display_type is None:
            if self.quantities_data_units == 'molecules':
                quantities_display_type = 'molecules'
            elif self.quantities_data_units in substance_units:
                quantities_display_type = 'moles'
            elif self.quantities_data_units in concentration_units:
                quantities_display_type = 'concentrations'
            else:
                raise ValueError
        self.quantities_display_type = str(quantities_display_type)

        if timepoints_display_units is None:
            timepoints_display_units = self.timepoints_data_units
        self.timepoints_display_units = str(timepoints_display_units)
        
        if quantities_display_units is None:
            quantities_display_units = quantities_data_units
        self.quantities_display_units = str(quantities_display_units)
        
        if volumes_display_units is None:
            volumes_display_units = volumes_data_units
        self.volumes_display_units = str(volumes_display_units)
        
        
        self.parent = parent # used by McssResultsWidget for QMessageBox
        
        self.type = type
        
        if simulation is None:
            self.simulation = load_h5(filename)
        else:
            self.simulation = simulation#load_h5(filename) # why do all that object creation again?
        
        self.filename = filename
        
        max_time = self.simulation.max_time
        number_of_timepoints = self.simulation._runs_list[0].number_of_timepoints
        self._timepoints = Quantity(np.linspace(0, max_time, number_of_timepoints), time_units[self.timepoints_data_units])

        self._timestep = Quantity(self.simulation.log_interval, time_units[self.timepoints_data_units])

        self._start = 0 
        self._stop = len(self._timepoints)
        self._step = 1

        if 0 < from_ < self._timepoints[-1]:
            # make start the index of the timepoint closest to, and including, from_
            self.start = bisect.bisect_left(self._timepoints, math.floor(from_))
        else:
            # make start the index of the first timepoint
            self.start = 0

        if 0 < to < from_:
            # shouldn't have to happen because of spinboxes synchronised min/max
            to = -1

        if 0 < to < self._timepoints[-1]:
            # make stop the index of the timepoint closest to, and including, to
            self.stop = bisect.bisect_right(self._timepoints, math.ceil(to))
        else:
            # make stop the index of the final timepoint + 1
            self.stop = len(self._timepoints)

        self.max_chunk_size = self.stop - self.start #TODO determine based on any axis not just timepoints

        self.step = step # uses step.setter

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


    # indices

    @property
    def start(self): #TODO rename to _start
        return self._start #TODO rename to __start
    @start.setter
    def start(self, start): #TODO rename to _start
        if 0 < start < self.stop:
            self._start = start
        elif start <= 0:
            self._start = 0
        elif start >= self.stop:
            self._start = self.stop - 1
            print 'to ensure start is less than stop it has been set to %s' % self.start #TODO

    @property
    def stop(self): #TODO rename to _stop
        return self._stop
    @stop.setter
    def stop(self, stop): #TODO rename to _stop
        if self.start < stop < len(self._timepoints):
            self._stop = stop 
        elif stop >= len(self._timepoints):
            self._stop = len(self._timepoints)
        elif stop <= self.start:
            self._stop = self.start + 1
            print 'to ensure stop is greater than start it has been set to %s' % self.stop #TODO

    @property
    def step(self): #TODO rename to _step
        return self._step
    @step.setter
    def step(self, step): #TODO rename to _step
        if step is not int:
            step = int(step)
        if step > self.stop:
            step = self.stop - self.start
        if step < 1:
            step = 1
        self._step = step

    
    # times

    @property
    def from_(self):
#        return float(self.timepoints[0])
        return self.timepoints[0] # is a Quantity
    @from_.setter
    def from_(self, from_):
        if isinstance(from_, Quantity):
            from_.units = time_units[self.timepoints_data_units]
            self.start = int(from_ // self._timestep)
        else:
            self.start = int(from_ // self._timestep.magnitude)
            
    
    @property
    def to(self):
#        return float(self.timepoints[-1])
        return self.timepoints[-1] # is a Quantity
    @to.setter
    def to(self, to):
        if isinstance(to, Quantity):
            to.units = time_units[self.timepoints_data_units]
            self.stop = int(to // self._timestep) + 1
        else:
            self.stop = int(to // self._timestep.magnitude) + 1
        
    @property
    def timestep(self):
        return self.step * self._timestep
    @timestep.setter
    def timestep(self, timestep):
        if isinstance(timestep, Quantity):
            timestep.units = time_units[self.timepoints_data_units]
            self.step = int(timestep // self._timestep)
        else:
            self.step = int(timestep // self._timestep.magnitude)

    
    @property
    def timepoints(self):
        return Quantity(self._timepoints[self.start:self.stop:self.step], time_units[self.timepoints_display_units])

    
    @property
    def timepoints_data_units(self):
        return self._timepoints_data_units
    
    @timepoints_data_units.setter
    def timepoints_data_units(self, timepoints_data_units):
        self.validate_time_units(timepoints_data_units)
        self._timepoints_data_units = timepoints_data_units
    
    def validate_time_units(self, time_units_):
        if time_units_ not in time_units.keys():
            raise ValueError("time_units must be in %s" % tuple(time_units.keys())) #TODO test
    
    @property
    def timepoints_display_units(self):
        return self._timepoints_display_units

    @timepoints_display_units.setter
    def timepoints_display_units(self, timepoints_display_units):
        self.validate_time_units(timepoints_display_units)
        self._timepoints_display_units = timepoints_display_units
    
    
    @property
    def quantities_display_type(self):
        return self._quantities_display_type
    
    @quantities_display_type.setter
    def quantities_display_type(self, quantities_display_type):
        self.validate_quantities_display_type(quantities_display_type)
        self._quantities_display_type = quantities_display_type
        
    def validate_quantities_display_type(self, quantities_display_type):
        if quantities_display_type not in ('molecules', 'concentrations', 'moles'):
            raise ValueError("quantities_display_type must be in ('molecules', 'concentrations', 'moles')")
        
    @property
    def quantities_data_units(self):
        return self._quantities_data_units
    
    @quantities_data_units.setter
    def quantities_data_units(self, quantities_data_units):
        self.validate_quantities_units(quantities_data_units)
        self._quantities_data_units = quantities_data_units

    def validate_quantities_units(self, quantities_units):
        if quantities_units not in substance_units.keys() + concentration_units.keys():
            raise ValueError("quantities_units must be in %s" % tuple(substance_units.keys() + concentration_units.keys())) #TODO test
    
    @property
    def quantities_display_units(self):
        return self._quantities_display_units
    
    @quantities_display_units.setter
    def quantities_display_units(self, quantities_display_units):
        self.validate_quantities_units(quantities_display_units)
        self._quantities_display_units = quantities_display_units
    
    
    @property
    def volumes_data_units(self):
        return self._volumes_data_units
    @volumes_data_units.setter
    def volumes_data_units(self, volumes_data_units):
        self.validate_volumes_units(volumes_data_units)
        self._volumes_data_units = volumes_data_units

    def validate_volumes_units(self, volumes_units):
        if volumes_units not in volume_units.keys():
            raise ValueError("volumes_units must be in %s" % tuple(volume_units.keys())) #TODO test 
    
    @property
    def volumes_display_units(self):
        return self._volumes_display_units
    @volumes_display_units.setter
    def volumes_display_units(self, volumes_display_units):
        self.validate_volumes_units(volumes_display_units)
        self._volumes_display_units = volumes_display_units    
    
    
    def _allocate_array(self, shape, failed_message):
        '''
        
        >>> million = 1000 * 1000
        >>> results = _allocate_array(million, million, million), 'Should raise a MemoryError')
        
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


    def volumes(self, volumes_display_units=None, **ignored_kwargs):
        
        volumes = self._allocate_array(
            (
                len(self.run_indices),
                len(self.compartment_indices),
                len(self.timepoints)
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
            volumes_for_one_run = h5.getNode(where, 'volumes')[:, self.start:self.stop:self.step]
            for ci, c in enumerate(self.compartment_indices):
                volumes[ri, ci, :] = volumes_for_one_run[c, :]
        h5.close()
    
        volumes = Quantity(volumes, volume_units[self.volumes_data_units])

        # adjust scale of volumes to match volumes_display_units
        if volumes_display_units is None:
            volumes_display_units = self.volumes_display_units
        self.validate_volumes_units(volumes_display_units)
        volumes.units = volume_units[volumes_display_units]

        return volumes
    
    
#    def functions_of_amounts_over_axis(self, axis, functions):
#        ''' Narrow by amounts array. '''
#        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, axis, functions)
#
#    def functions_of_volumes_over_axis(self, axis, functions):
#        ''' Narrow by volumes array. '''
#        return functions_of_values_over_axis(self.volumes(), self.volumes_axes, axis, functions)
#    
#    def functions_of_amounts_over_runs(self, functions):
#        ''' Narrow by amounts array and runs axis. '''
#        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, 'runs', (functions))
#    
#    def mean_and_standard_deviation_of_amounts_over_runs(self):
#        ''' Narrow by amounts array, runs axis and mean and std functions. '''
##        return functions_of_values_over_axis(self.amounts(), self.amounts_axes, 'runs', (mean, std))
#        return self.functions_of_amounts_over_runs((mean, std))
#
#
#    def functions_of_amounts_over_successive_axes(self, axes, functions):
#        ''' Narrow by amounts array. '''
#        return functions_of_values_over_successive_axes(self.amounts(), self.amounts_axes, axes, functions)
#    
#    def functions_of_volumes_over_successive_axes(self, axes, functions):
#        ''' Narrow by volumes array. '''
#        return functions_of_values_over_successive_axes(self.volumes(), self.volumes_axes, axes, functions)

    
#    def chunk_generator(self, h5file): #TODO depends on array dimensions (a function for each) and order of dimensions to calculate functions over
#        pass



    

#    @profile # use profile(results.get_amounts) instead - won't raise "'profile' not found" error
    def amounts(self, quantities_display_type=None, quantities_display_units=None, volume=None, **ignored_kwargs):
#        ''' Returns a tuple of (timepoints, results) where timepoints is an 1 - D
#        array of floats and results is a list of 3-D arrays of ints with the 
#        shape (species, compartments, timepoint) for each run. '''
        '''
        
        'volume' is used when self.simulation.log_volumes != 1 to fill an array 
        that is the same shape as volumes would be, allowing concentrations to
        be calculated for models without volumes information. 
        
        '''
        
        results = self._allocate_array(
            (
                len(self.run_indices),
                len(self.species_indices),
                len(self.compartment_indices),
                len(self.timepoints)
            ),
            'Could not allocate memory for amounts.\n' \
            'Try selecting fewer runs, a shorter time window or a bigger time interval multipler.'
        )
        if results is None:
            return
            
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.stop:self.step]
            for si, s in enumerate(self.species_indices):
                for ci, c in enumerate(self.compartment_indices):
                    results[ri, si, ci, :] = amounts[s, c, :]
#                    results[ri, si, ci, :] = h5.getNode(where, 'amounts')[s, c, self.start:self.stop:self.step] # about 10 times slower!
        h5.close()

        results = Quantity(results, substance_units[self.quantities_data_units])

        return self.convert_amounts_quantities(results, quantities_display_type, quantities_display_units, volume)
#        
#
    def convert_amounts_quantities(self, amounts, quantities_display_type=None, quantities_display_units=None, volume=None):
        if quantities_display_type is None:
            quantities_display_type = self.quantities_display_type
        self.validate_quantities_display_type(quantities_display_type)
        
        if quantities_display_units is None:
            quantities_display_units = self.quantities_display_units
        self.validate_quantities_units(quantities_display_units)
        
        if quantities_display_type == 'concentrations' and not quantities_display_units.endswith('molar'):
            quantities_display_units = 'molar'
        
        if quantities_display_type == 'concentrations' and self.simulation.log_volumes != 1 and volume is None:
            message = 'Cannot calculate concentrations without volumes dataset, rerun mcss with log_volumes=1' 
            if self.parent is not None:
                QMessageBox.warning('Error', message) #TODO test
            else:
                print message, 'or provide volume argument in %s' % self.volumes_data_units
            return
        
        if self.quantities_data_units != quantities_display_units:
            
            # convert to moles
            amounts.units = substance_units['moles']

            # convert from moles to whatever
            if quantities_display_type == 'concentrations':
                
                if self.simulation.log_volumes == 1:
                    volumes = self.volumes()#self.volumes_data_units)
                else:
                    assert volume is not None
                    volumes = np.empty((len(self.run_indices), len(self.compartment_indices), len(self.timepoints)))
                    volumes.fill(volume)
                    _volume_units = volume_units[self.volumes_data_units]
                    volumes = volumes * _volume_units
                _concentration_units = concentration_units['molar']
                concentrations = np.zeros(amounts.shape) * _concentration_units
                np.seterr(divide='ignore') # ignore divide by zero errors - will replace values with np.inf instead
#                print amounts.shape
#                print volumes.shape
                for si, _ in enumerate(self.species_indices):
                    concentrations[:, si, :, :] = amounts[:, si, :, :] / volumes # divide amount by volume
                concentrations[concentrations == np.inf] = 0 # replace all occurences of np.inf with 0
                amounts = concentrations.rescale(quantities_display_units) # rescale to display units
            else:
                amounts.units = substance_units[quantities_display_units]
        return amounts
    

    def get_functions_over_runs(self, functions):#, quantities_display_type=None, quantities_display_units=None, volume=None, **ignored_kwargs):
        '''Returns a 4D array of floats with the shape (functions, species, 
        compartments, timepoint).'''
        results = self._allocate_array(# outputs error message if anything goes wrong
            (
                len(functions),
                len(self.species_indices),
                len(self.compartment_indices),
                len(self.timepoints)
            ),
            'Could not allocate memory for functions.\n' \
            'Try selecting fewer functions, a shorter time window or a bigger time interval multipler.'
        )
        if results is None:
            return        

        # create biggest possible buffer
        chunk_size = self.max_chunk_size
        buffer = None
        while buffer == None:
            try:
                buffer = np.zeros(
                    (
                        len(self.run_indices),
                        len(self.species_indices),
                        len(self.compartment_indices),
                        chunk_size,
                    ),
                    self.type
                )
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
            '''Fills buffer with amounts for all runs and updates results with outcome of functions applied to runs.'''
            self.amounts_chunk_stop = amounts_chunk_start + (chunk_size * self.step)
            for ri, r in enumerate(self.run_indices):
                where = '/run%s' % (r + 1)
                amounts = h5.getNode(where, 'amounts')[:, :, amounts_chunk_start:self.amounts_chunk_stop:self.step]
                for si, s in enumerate(self.species_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        buffer[ri, si, ci, :] = amounts[s, c, :] #FIXME works but surely buffer[:, :, :, ri] = amounts[self.species_indices, self.compartment_indices, :] could work too, no?
            self.stat_chunk_stop = stat_chunk_start + chunk_size
            for fi, f in enumerate(functions):
                stat = results[fi] # stat is a 'view' on results so change stat changes results
                stat[:, :, stat_chunk_start:self.stat_chunk_stop] = f(buffer, axis=0) # axis 0 is runs

        h5 = tables.openFile(self.filename)

        amounts_chunk_start = self.start
        stat_chunk_start = 0
        # for each whole chunk
        quotient = len(self.timepoints) // chunk_size
        for _ in range(quotient):
            iteration()#chunk_size)
            amounts_chunk_start = self.amounts_chunk_stop
            stat_chunk_start = self.stat_chunk_stop

        # and the remaining timepoints           
        remainder = len(self.timepoints) % chunk_size
        if remainder > 0:
            buffer = np.zeros(
                (
                    len(self.run_indices),
                    len(self.species_indices),
                    len(self.compartment_indices),
                    chunk_size,
                ),
                self.type
            )
            iteration(remainder)

        h5.close()
    
        results = Quantity(results, substance_units[self.quantities_data_units])
        # would be nice to be to convert quantities to concentrations, etc but shapes don't match 
        # and perhaps not all of the output of the functions are quantities

        return results


#    def timeseries(self):
#        pass
#    
#    def plot_timeseries(self):
#        pass
#    
#    def timeseries_plots(self):
#        pass
#
#    def histograms(self):
#        pass
#    
#    def export_data(self):
#        pass
#
#    def surfaces(self):
#        pass

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
            surface = np.zeros(((xmax - xmin) + 1, (ymax - ymin) + 1, len(self.timepoints)), self.type)

            # fill surface with amounts
            for r in self.run_indices: # only one for now, see SimulationResultsDialog.update_ui()
                where = '/run%s' % (r + 1)
                try:
                    amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.stop:self.step]
                except MemoryError:
                    message = 'Could not allocate memory for amounts.\nTry selecting fewer species, a shorter time window or a bigger time interval multipler.'
                    if self.parent is not None:
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                    return (self.timepoints, [], None, None, None, None)
                if sum_compartments_at_same_xy_lattice_position:
                    for c in selected_compartments:
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :] + surface[c.x_position, c.y_position, :]
                else:
                    for c in selected_compartments:
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :]
            results.append(surface)
        h5.close()
        return (self.timepoints, results, xmin, xmax, ymin, ymax)


    def select_species(self, *names):
        '''Select species with names in 'names'.
        
        if len(names) == 0: select all species
        
        '''
        if len(names) == 0:
            self.species_indices = xrange(self.simulation.number_of_species)
        else:
            self.species_indices = [species.index for species in self.simulation._species_list if species.name in names]
    
    def xy_coordinates(self, min_x, max_x, min_y, max_y):
        '''Returns pairs of (x,y) where min_x <= x <= max_x and min_y <= y <= max_y'''
        return [(x, y) for x in xrange(min_x, max_x + 1) for y in xrange(min_y, max_y + 1)]
    
    def select_compartments(self, names=None, xy_coordinates=None):
        '''Select compartments with names in 'names' and (x,y) coordinates in xy_coordinates.
        
        if names is None and xy_coordinates is None: 
            select all compartments
        elif names is None and xy_coordinates is not None: 
            select compartments for (x,y) in 'xy_coordinates'
        elif names is not None and xy_coordinates is None: 
            select compartments for name in 'names'
        else: 
            select compartments for name in 'names' for (x,y) in 'xy_coordinates'

        '''
        compartments = self.simulation._runs_list[0]._compartments_list
        if names is None and xy_coordinates is None: 
            # select all compartments
            self.compartment_indices = [compartment.index for compartment in compartments]
        elif names is None and xy_coordinates is not None: 
            # select compartments for (x,y) in 'xy_coordinates'
            self.compartment_indices = [compartment.index for compartment in compartments if compartment.coordinates() in xy_coordinates]
        elif names is not None and xy_coordinates is None: 
            # select compartments for name in 'names'
            self.compartment_indices = [compartment.index for compartment in compartments if compartment.name in names]
        else:
            # select compartments for name in 'names' for (x, y) in 'xy_coordinates'
            self.compartment_indices = [compartment.index for compartment in compartments if compartment.coordinates() in xy_coordinates and compartment.name in names]

    def select_runs(self, runs=None, from_=None, to=None, random=None):
        '''Select runs in 'runs', or from 'from_' to 'to', or randomly where 0 < 'random' < len(self.run_indices).'''
        max_runs = self.simulation.number_of_runs
        run_indices = xrange(max_runs)
        if runs is not None:
            run_indices = [i - 1 for i in runs if i > 0 and i <= max_runs]
            if len(run_indices) < len(runs):
                print 'McssResults.select_runs: the following runs are invalid: %s' % [i for i in runs if i <= 0 or i > max_runs] #TODO use logger
        elif from_ is not None:
            if to is not None:
                run_indices = xrange(from_ - 1, to)
            else:
                run_indices = xrange(from_ - 1, max_runs)
        elif to is not None:
            run_indices = xrange(to)
        elif random is not None:
            if not random > len(run_indices):
                import random as rand
                run_indices = rand.sample(run_indices, random)
            else:
                print 'McssResults.select_runs: random > len(run_indices)' #TODO use logger
        self.run_indices = run_indices

    def select_timepoints(self, from_=None, to=None, timestep=None):
        '''Select every 'timestep' timepoints from 'from_' to 'to'.'''
        if from_ is not None:
            self.from_ = from_
        else:
            self.from_ = self._timepoints[0]
        if to is not None:
            self.to = to
        else:
            self.to = self._timepoints[-1]
        if timestep is not None:
            self.timestep = timestep
        else:
            self.timestep = self._timepoints[1] - self._timepoints[0]
             
        
        
    '''
    results = mcss(...)
    #TODO have units parameters in McssParams and write them to the H5 file so that they can be automatically set for McssResults but overridden in McssResultsWidget  
#    results.time_data_units = 'seconds'
#    results.quantities_data_units = 'molecules'
#    results.volumes_data_units = 'litres'
#    results.volumes_display_units = 'microlitres'
#    results.quantities_display_type = 'concentrations'
#    results.quantities_display_units = 'micromolar'
#    results.species_indices = [1,3,2,3]
#    results._species_indices = [1,3,2,3]
#    results.select_species('a', 'b')
#    results.select_compartments((x,y),(x,y),*((x,y) for x in range(2,10) for y in range(3,8))))
#    results.select_runs(2, 7, 8, from_=1, to=10, random=5, all=True)
#    print results.runs_information()
#    print results.species_information()
#    print results.compartments_information()
#    results.from_ = 100
#    results.to = 300
#    results.timestep = 20
#    results.select_timepoints(10,20,30, from_=10, to=30)
    print results.timepoints
    print results.selection()
    amounts = results.amounts()
    volumes = results.volumes()
    surfaces = results.surfaces()
    mean_runs = results.get_functions_over_runs((mcss_results.mean))
    assert mean_runs == mcss_results.functions_of_values_axis(amounts, ('runs', 'species', 'compartments', 'timepoints'), 'runs', (mcss_results.mean,)))
    assert mean_runs == results.mean_over_runs()
    # same for std, var, sum, min, max
    
    '''


    def runs_information(self, truncate=True):
        '''
        Run # | # compartments | # timepoints | Simulated time
        ------------------------------------------------------
        1     | 1              | 601          | 6000.0        
        ...
        200   | 1              | 601          | 6000.0        
        '''
        labels = ('Run #', '# compartments', '# timepoints', 'Simulated time')
        rows = [[str(s) for s in (run._run_number, run.number_of_compartments, run.number_of_timepoints, run.simulated_time)] for run in self.simulation._runs_list]
        table = indent([labels] + rows, hasHeader=True)
        if truncate and self.simulation.number_of_runs > 1:
            s = table.split('\n')
            return '\n'.join((s[0], s[1], s[2], '...', s[-2], s[-1]))
        return table
        
    def species_information(self, sort_column_index=0, reverse=False):
        '''
        Name           | Index
        ----------------------
        gene1          | 0    
        protein1       | 1    
        protein1_gene1 | 2    
        rna1           | 3    
        '''
        labels = ('Name', 'Index')
        rows = [[str(s) for s in (species.name, species.index)] for species in self.simulation._species_list]
        rows.sort(key=operator.itemgetter(sort_column_index), reverse=reverse)
        table = indent([labels] + rows, hasHeader=True)
        return table

    def compartments_information(self, sort_column_index=0, reverse=False):
        '''
        Name         | Index | X | Y
        ----------------------------
        NARbacterium | 0     | 0 | 0
        '''
        labels = ('Name', 'Index', 'X', 'Y')
        rows = [[str(s) for s in (compartment.name, compartment.index, compartment.x_position, compartment.y_position)] for compartment in self.simulation._runs_list[0]._compartments_list]
        rows.sort(key=operator.itemgetter(sort_column_index), reverse=reverse)
        table = indent([labels] + rows, hasHeader=True)
        return table

    def reset_selection(self):
        self.select_runs()
        self.select_species()
        self.select_compartments()
        self.select_timepoints()
        

def test():
    results = McssResults('tests/NAR_simulation.h5')
    exit()
#    print results.runs_information()
#    print results.species_information(1, True)
#    print results.compartments_information()
    
    assert len(results.run_indices) == 200
    assert len(results.compartment_indices) == 1
    assert len(results._timepoints) == 601
    assert len(results.species_indices) == 4

    # select 2 species
    results.select_species('gene1', 'protein1')
    assert len(results.species_indices) == 2
    
    # select species with name
    results.select_compartments(names=['NARbacterium'])
    assert len(results.compartment_indices) == 1
    results.select_compartments()

    # select species with xy_coordinate
    results.select_compartments(xy_coordinates=[(0, 0)])
    assert len(results.compartment_indices) == 1
    results.select_compartments()

    # select species with name and xy_coordinate
    results.select_compartments(xy_coordinates=[(0, 0)], names=['NARbacterium'])
    assert len(results.compartment_indices) == 1
    results.select_compartments()

    # negative test (only compartment is named 'NARbacterium')
    results.select_compartments(names=['PARbacterium'])
    assert len(results.compartment_indices) == 0
    results.select_compartments()
    
    # negative test (only compartment is at (0,0))
    results.select_compartments(xy_coordinates=[(1, 0)])
    assert len(results.compartment_indices) == 0
    results.select_compartments()

#    # select all species
#    results.select_species()
#    assert len(results.species_indices) == 4
#    
#    # select all compartments
#    results.select_compartments()
#    assert len(results.compartment_indices) == 1
    
    results.select_timepoints(100, 200, 20)
    assert len(results.timepoints) == 6
    
    results.select_timepoints(timestep=1 * minute)
    assert len(results.timepoints) == 101

#    results.select_timepoints(5 * minute, 10 * minute, 2 * minute)
#    results.select_timepoints(5 * minute, 10 * minute)
    
    results.select_timepoints()
    assert len(results.timepoints) == 601

    # ........
    
    results.select_species('gene1', 'protein1')
    results.select_compartments(names=['NARbacterium'])
    results.select_timepoints(timestep=1 * minute)
    results.select_runs([1, 7, 6, 20])
    assert results.amounts().shape == (4, 2, 1, 101)
    


if __name__ == '__main__':
    test()
#    execfile('mcss_results_widget.py')
