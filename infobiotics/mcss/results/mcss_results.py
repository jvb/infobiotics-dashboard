'''McssResults class extracts simulation data from .h5 (mcss HDF5) files. Also 
has functions for applying NumPy ufuncs along (multiple) axes of N-dimensional 
arrays.'''

from __future__ import division

from quantities.units.time import hour, minute
import operator
from table import indent
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QString#, Qt, SIGNAL, SLOT

from infobiotics.commons.quantities.traits_ui_converters import Quantity, time_units, substance_units, concentration_units, volume_units

from simulation import load_h5

import bisect
import math
#import decimal

import numpy as np

import tables
from infobiotics.commons.quantities.units.volume import microlitre


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
    '''TODO'''

    amounts_axes = ['runs', 'species', 'compartments', 'timepoints']
    
    volumes_axes = ['runs', 'compartments', 'timepoints']    
    
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
        default_volume=0.01 * microlitre,
        **ignored_kwargs
    ):
    
        self.default_volume = default_volume
         
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
        self.simulation = load_h5(filename) if simulation is None else simulation # avoids species/run/compartment object recreation
        self.filename = filename
        
        log_interval = self.simulation.log_interval
#        max_time = self.simulation.max_time # can't be trusted, multiply log_interval by number_of_timepoints instead
        number_of_timepoints = self.simulation._runs_list[0].number_of_timepoints
#        self._timepoints = Quantity(np.linspace(0, max_time, number_of_timepoints), time_units[self.timepoints_data_units])
        self._timepoints = Quantity(np.linspace(0, log_interval * number_of_timepoints, number_of_timepoints), time_units[self.timepoints_data_units])

        self._timestep = Quantity(log_interval, time_units[self.timepoints_data_units])

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
                QMessageBox.warning(self.parent, QString('Out of memory'), QString(failed_message))
            else:
                print failed_message
            return
        return array


    def volumes(self, volumes_display_units=None, **ignored_kwargs):
        
        if not self.has_volumes:
            raise ValueError("mcss simulation '%s' has no volumes dataset." % self.filename)
        
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
        
        'volume' is used when not self.has_volumes to fill an array 
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

        self._extract_amounts(h5, results, self.start, self.stop)
        
        h5.close()

        results, _ = self.convert_amounts_quantities(Quantity(results, substance_units[self.quantities_data_units]), quantities_display_type, quantities_display_units, volume) 
        
        return results
        
    def _extract_amounts(self, h5, destination_array, start, stop):
        for ri, r in enumerate(self.run_indices):
            amounts = h5.getNode('/run%s' % (r + 1), 'amounts')[:, :, start:stop:self.step]
            for si, s in enumerate(self.species_indices):
                for ci, c in enumerate(self.compartment_indices):
                    destination_array[ri, si, ci, :] = amounts[s, c, :]

    def convert_amounts_quantities(self, amounts, quantities_display_type=None, quantities_display_units=None, volume=None):
        if quantities_display_type is None:
            quantities_display_type = self.quantities_display_type
        self.validate_quantities_display_type(quantities_display_type)
        
        if quantities_display_units is None:
            quantities_display_units = self.quantities_display_units
        self.validate_quantities_units(quantities_display_units)
        
        if quantities_display_type == 'concentrations' and not quantities_display_units.endswith('molar'):
            quantities_display_units = 'molar'
        
        if quantities_display_type == 'concentrations' and not self.has_volumes and not self.has_default_volume and volume is None:
            message = 'Cannot calculate concentrations without volumes dataset, rerun mcss with log_volumes=1' 
            if self.parent is not None:
                QMessageBox.warning(self.parent, QString('Error'), QString(message)) #TODO test
            else:
                print message, 'or provide volume argument'# in %s' % self.volumes_data_units
            return
        
        if self.quantities_data_units != quantities_display_units:
            amounts.units = substance_units['moles'] # convert to moles
            # convert from moles to whatever
            if quantities_display_type == 'concentrations':
                if self.has_volumes:
                    volumes = self.volumes()#self.volumes_data_units)
                else:
                    if volume is None:
                        volume = self.default_volume
                    assert volume is not None
                    volumes = np.empty((len(self.run_indices), len(self.compartment_indices), len(self.timepoints)))
                    volumes.fill(volume)
                    _volume_units = volume_units[self.volumes_data_units]
                    volumes = volumes * _volume_units
                _concentration_units = concentration_units['molar']
                concentrations = np.zeros(amounts.shape) * _concentration_units
                np.seterr(divide='ignore') # ignore divide by zero errors - will replace values with np.inf instead
                for si, _ in enumerate(self.species_indices):
                    concentrations[:, si, :, :] = amounts[:, si, :, :] / volumes # divide amount by volume
                concentrations[concentrations == np.inf] = 0 * _concentration_units # replace all occurences of np.inf with 0
                amounts = concentrations.rescale(quantities_display_units) # rescale to display units
            else:
                amounts.units = substance_units[quantities_display_units]
        return amounts, quantities_display_units
    

    def functions_of_amounts_over_runs(self, functions, quantities_display_type=None, quantities_display_units=None, volume=None, **ignored_kwargs):
        '''Returns a 4D array of floats with the shape (functions, species, 
        compartments, timepoint). 
        
        '''
        #TODO ''' or a 3D array of floats with shape (species, compartments, timepoints) if functions is a single function.'''
        import types
        if type(functions) in (types.FunctionType, types.LambdaType):
            functions = (functions,)
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
        chunk_size = len(self.timepoints)
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
                        QMessageBox.warning(self.parent, QString('Out of memory'), QString(message))
                    else:
                        print message
                        return
                # progressively halve chunk_size until buffer fits into memory
                chunk_size = chunk_size // 2
                buffer = None
                continue

        h5 = tables.openFile(self.filename)
        
        def iteration(chunk_size=chunk_size, buffer=buffer, quantities_display_units=quantities_display_units):
            '''Fills buffer with amounts for all runs and updates results with outcome of functions applied to runs.'''
            self.amounts_chunk_stop = amounts_chunk_start + (chunk_size * self.step)
            self._extract_amounts(h5, buffer, amounts_chunk_start, self.amounts_chunk_stop)
            buffer, quantities_display_units = self.convert_amounts_quantities(Quantity(buffer, substance_units[self.quantities_data_units]), quantities_display_type, quantities_display_units, volume)
            self.stat_chunk_stop = stat_chunk_start + chunk_size
            for fi, f in enumerate(functions):
                stat = results[fi] # stat is a 'view' on results so change stat changes results
                stat[:, :, stat_chunk_start:self.stat_chunk_stop] = f(buffer, axis=0) # axis 0 is runs
            return quantities_display_units

        amounts_chunk_start = self.start
        stat_chunk_start = 0
        # for each whole chunk
        quotient = len(self.timepoints) // chunk_size
        for _ in range(quotient):
            quantities_display_units = iteration()#chunk_size, buffer)
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
            quantities_display_units = iteration(remainder, buffer)

        h5.close()
    
        results = Quantity(results, quantities_display_units)
        return results

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
#        compartments = self.compartments
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
            self.compartment_indices = [compartment.index for compartment in compartments if compartment.coordinates() in xy_coordinates and any(map(lambda name: name in compartment.name, names))]

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

    def reset_selection(self):
        self.select_runs()
        self.select_species()
        self.select_compartments()
        self.select_timepoints()             
        
        
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
    mean_runs = results.functions_of_amounts_over_runs((mcss_results.mean))
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
#        rows = [[str(s) for s in (run._run_number, run.number_of_compartments, run.number_of_timepoints, run.simulated_time)] for run in self.simulation._runs_list]
        rows = [[str(s) for s in (run._run_number, run.number_of_compartments, run.number_of_timepoints, run.simulated_time)] for run in self.runs]
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
#        rows = [[str(s) for s in (species.name, species.index)] for species in self.simulation._species_list]
        rows = [[str(s) for s in (species.name, species.index)] for species in self.species]
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
#        rows = [[str(s) for s in (compartment.name, compartment.index, compartment.x_position, compartment.y_position)] for compartment in self.simulation._runs_list[0]._compartments_list]
#        rows = [(compartment.name, compartment.index, compartment.x_position, compartment.y_position) for compartment in self.simulation._runs_list[0]._compartments_list]
        rows = [(compartment.name, compartment.index, compartment.x_position, compartment.y_position) for compartment in self.compartments]
        rows.sort(key=operator.itemgetter(sort_column_index), reverse=reverse)
        table = indent([labels] + rows, hasHeader=True)
        return table
    
    @property
    def runs(self):
        return [self.simulation._runs_list[i] for i in self.run_indices]

    @property
    def compartments(self):
        return [self.runs[0]._compartments_list[i] for i in self.compartment_indices]

    @property
    def species(self):
        return [self.simulation._species_list[i] for i in self.species_indices]


    def len_timeseries(self, amounts=True, volumes=True, mean_over_runs=True):
        len_runs = len(self.runs)
        len_species = len(self.species)
        len_compartments = len(self.compartments)
        if len_runs > 1 and mean_over_runs:
            if amounts and volumes:
                return (len_species * len_compartments) + len_compartments
            elif amounts:
                return len_species * len_compartments
            elif volumes:
                return len_compartments
            else:
                return 0
        else:
            if amounts and volumes:
                return (len_runs * len_species * len_compartments) + (len_runs * len_compartments)
            elif amounts:
                return len_runs * len_species * len_compartments
            elif volumes:
                return len_runs * len_compartments
            else:
                return 0
            
    def timeseries_information(self, sort_column_index=6, reverse=False):
        labels = ('# species', '# compartments', '#runs', 'amounts', 'volumes', 'mean over runs', '# timeseries') 
        len_runs = len(self.runs)
        len_species = len(self.species)
        len_compartments = len(self.compartments)
        rows = []
        for mean_over_runs in True, False:
            for amounts in True, False:
                for volumes in True, False:
                    if not (volumes or amounts):
                        continue
                    len_timeseries = self.len_timeseries(amounts, volumes, mean_over_runs)
                    rows.append([len_species, len_compartments, len_runs, amounts, volumes, mean_over_runs, len_timeseries])
        rows.sort(key=operator.itemgetter(sort_column_index), reverse=reverse)
        table = indent([labels] + rows, hasHeader=True)
        return table

    def ci_factor(self, ci_degree=0.95):
        assert 0 <= ci_degree <= 1
        num_runs = len(self.run_indices)
#        from scipy.special import stdtrit
#        ci_factor = stdtrit(num_runs - 1, 1.0 - (1.0 - ci_degree) / 2.0) / math.sqrt(num_runs)
        from infobiotics.thirdparty.statistics import InverseStudentT
        ci_factor = InverseStudentT(num_runs - 1, 1.0 - (1.0 - ci_degree) / 2.0) / math.sqrt(num_runs)
        return ci_factor

    def timeseries(self, amounts=True, volumes=True, mean_over_runs=True):
        '''Return Timeseries objects for current selection.'''
        
        self.assertions(amounts, volumes, mean_over_runs)

        from timeseries import Timeseries
        from infobiotics.commons import colours
        
        from species import Species

        if volumes:
            volumes_species = Species(
                index=None, #TODO hack
                name='Volumes',
                simulation=self.simulation,
            )

        timeseries = []
        num_species = len(self.species)

        if len(self.runs) > 1 and mean_over_runs:
            if amounts:
                mean_amounts_over_runs, std_amounts_over_runs = self.functions_of_amounts_over_runs((mean, std))
                for ci, c in enumerate(self.compartments):
                    for si, s in enumerate(self.species):
                        timeseries.append(
                            Timeseries(
                                runs=self.runs,
                                species=s,
                                compartment=c,
                                timepoints=self.timepoints,
                                timepoints_units=self.timepoints_display_units,
                                values_type='Concentration' if self.quantities_display_type == 'concentrations' else 'Amount',
                                values=mean_amounts_over_runs[si, ci, :],
                                std=std_amounts_over_runs[si, ci, :],
                                values_units=self.quantities_display_units,
                                _colour=colours.colour(si), #TODO rechoose colours based on different strategy for stacked, etc in timeseries plot
                                marker=colours.marker(ci),
                            ),
                        )
            if volumes:
                mean_volumes_over_runs, std_volumes_over_runs = functions_of_values_over_axis(self.volumes(), self.volumes_axes, 'runs', (mean, std)) 
                for ci, c in enumerate(self.compartments):
                    timeseries.append(
                        Timeseries(
                            runs=self.runs,
                            species=volumes_species,
                            compartment=c,
                            timepoints=self.timepoints,
                            timepoints_units=self.timepoints_display_units,
                            values_type='Volume',
                            values=mean_volumes_over_runs[ci, :],
                            std=std_volumes_over_runs[ci, :],
                            values_units=self.volumes_display_units,
                            _colour=colours.colour(num_species + ci),
                            marker=colours.marker(ci),
                        )
                    )
        
        else: # not mean_over_runs
            if amounts:
                amounts = self.amounts()
                for ri, r in enumerate(self.runs):
                    for ci, c in enumerate(self.compartments):
                        for si, s in enumerate(self.species):
                            timeseries.append(
                                Timeseries(
                                    run=r,
                                    species=s,
                                    compartment=c,
                                    timepoints=self.timepoints,
                                    timepoints_units=self.timepoints_display_units,
                                    values_type='Concentration' if self.quantities_display_type == 'concentrations' else 'Amount',
                                    values=amounts[ri, si, ci, :],
                                    values_units=self.quantities_display_units,
                                    _colour=colours.colour(si),
                                    marker=colours.marker(ci),
                                )
                            )
            if volumes:
                volumes = self.volumes()
                for ri, r in enumerate(self.runs):
                    for ci, c in enumerate(self.compartments):
                        timeseries.append(
                            Timeseries(
                                run=r,
                                species=volumes_species,
                                compartment=c,
                                timepoints=self.timepoints,
                                timepoints_units=self.timepoints_display_units,
                                values_type='Volume',
                                values=volumes[ri, ci, :],
                                values_units=self.volumes_display_units,
                                _colour=colours.colour(num_species + ci),
                                marker=colours.marker(ci),
                            )
                        )
        return timeseries


    def assertions(self, amounts=True, volumes=True, mean_over_runs=True):
        assert amounts or volumes
        
        if volumes and not self.has_volumes:
            raise ValueError("mcss simulation '%s' has no volumes dataset." % self.filename)

        assert len(self.run_indices) > 0
        assert len(self.species_indices) > 0
        assert len(self.compartment_indices) > 0
        assert len(self.timepoints) > 0
    
        
    # remember these within this instance
    csv_precision = 3
    csv_delimiter = ','
    
    def export_timeseries(self, 
        file_name,
        amounts=True, volumes=True, mean_over_runs=True,                  
        csv_precision=None, csv_delimiter=None,
        #TODO custom titles here?
    ):
        ''' Write selected data to a file in csv, xls or npz format.
        
        (Over?)use of inner functions here can result in crytic exceptions, e.g.
            "UnboundLocalError: local variable 'x' referenced before assignment"
        The actual reason for these errors is that variables inside inner 
        functions are immutable, see:           
            http: // stackoverflow.com / questions / 1414304 / local - functions - in - python / 1414320#1414320
        The correct solution is, in this instance, to pass these variables as
        arguments to the inner functions, and the neatest way to do that is as
        default arguments, see write_csv, fix_delimited_string and write_npz. 
        
        '''
        file_name = unicode(file_name)
        from infobiotics.commons.files import writable
        if not writable(file_name):
            raise ValueError("'%s' is not writable." % file_name)

        self.assertions()
        
#        timeseries = []
        num_species = len(self.species)

        if len(self.runs) > 1 and mean_over_runs:
            if amounts:
                mean_amounts_over_runs, std_amounts_over_runs = self.functions_of_amounts_over_runs((mean, std))
#                for ci, c in enumerate(self.compartments):
#                     for si, s in enumerate(self.species):

##                        timeseries.append(
##                            Timeseries(
##                                runs=self.runs,
##                                species=s,
##                                compartment=c,
##                                timepoints=self.timepoints,
##                                timepoints_units=self.timepoints_display_units,
##                                values_type='Concentration' if self.quantities_display_type == 'concentrations' else 'Amount',
##                                values=mean_amounts_over_runs[si, ci, :],
##                                std=std_amounts_over_runs[si, ci, :],
##                                values_units=self.quantities_display_units,
##                                _colour=colours.colour(si), #TODO rechoose colours based on different strategy for stacked, etc in timeseries plot
##                                marker=colours.marker(ci),
##                            ),
##                        )
            if volumes:
                mean_volumes_over_runs, std_volumes_over_runs = functions_of_values_over_axis(self.volumes(), self.volumes_axes, 'runs', (mean, std)) 
#                for ci, c in enumerate(self.compartments):
##                    timeseries.append(
##                        Timeseries(
##                            runs=self.runs,
##                            species=volumes_species,
##                            compartment=c,
##                            timepoints=self.timepoints,
##                            timepoints_units=self.timepoints_display_units,
##                            values_type='Volume',
##                            values=mean_volumes_over_runs[ci, :],
##                            std=std_volumes_over_runs[ci, :],
##                            values_units=self.volumes_display_units,
##                            _colour=colours.colour(num_species + ci),
##                            marker=colours.marker(ci),
##                        )
##                    )
        
        else: # not mean_over_runs
            if amounts:
                amounts = self.amounts()
#                for ri, r in enumerate(self.runs):
#                    for ci, c in enumerate(self.compartments):
#                        for si, s in enumerate(self.species):

##                            timeseries.append(
##                                Timeseries(
##                                    run=r,
##                                    species=s,
##                                    compartment=c,
##                                    timepoints=self.timepoints,
##                                    timepoints_units=self.timepoints_display_units,
##                                    values_type='Concentration' if self.quantities_display_type == 'concentrations' else 'Amount',
##                                    values=amounts[ri, si, ci, :],
##                                    values_units=self.quantities_display_units,
##                                    _colour=colours.colour(si),
##                                    marker=colours.marker(ci),
##                                )
##                            )
            if volumes:
                volumes = self.volumes()
#                for ri, r in enumerate(self.runs):
#                    for ci, c in enumerate(self.compartments):

##                        timeseries.append(
##                            Timeseries(
##                                run=r,
##                                species=volumes_species,
##                                compartment=c,
##                                timepoints=self.timepoints,
##                                timepoints_units=self.timepoints_display_units,
##                                values_type='Volume',
##                                values=volumes[ri, ci, :],
##                                values_units=self.volumes_display_units,
##                                _colour=colours.colour(num_species + ci),
##                                marker=colours.marker(ci),
##                            )
##                        )        
        
        
        #TODO volumes like plot()
        if averaging:
            timepoints, results = results.get_amounts_mean_over_runs()
            mean_index = 0
        else:
            timepoints, results = results.amounts()
        if len(results) == 0:
            return

        header = ['time']# (%s)' % units]
        #TODO move these to method signature?
#        averaging_header_item = '%s in %s mean of %s runs'
        def averaging_header_item(s, c, r):
            return '%s in %s mean of %s runs' % (s, c, r) if r != 1 else '%s in %s mean of %s run' % (s, c, r)
        header_item = '%s in %s of run %s'
#        def header_item(s, c, r):
#            return '%s in %s of run %s' % (s, c, r)

        def write_csv(csv_precision=csv_precision, csv_delimiter=csv_delimiter, results=results):
            # load default or remembered values
            if csv_precision is None:
                csv_precision = self.csv_precision
            if csv_delimiter is None:
                csv_delimiter = self.csv_delimiter

            # data
            if averaging:
                indices = [(ci, si) for ci, c in enumerate(compartments) for si, s in enumerate(species)]
                results = tuple((results[mean_index][si, ci] for ci, si in indices))
                fmt = '%%.%sf' % csv_precision
            else:
                indices = [(ri, ci, si) for ri, r in enumerate(runs) for ci, c in enumerate(compartments) for si, s in enumerate(species)]
                results = tuple((results[ri][si, ci, :] for ri, ci, si in indices))
                d = '%d,' * len(results); fmt = ['%.3f'] + d.split(',')[:-1] # timepoints must be floats, levels are ints
            timepoints_and_levels = (timepoints,) + results
            # http://www.scipy.org/Numpy_Example_List#head-786f6bde962f7d1bcb92272b3654bc7cecef0f32
            np.savetxt(file_name, np.transpose(timepoints_and_levels), fmt=fmt, delimiter=csv_delimiter)
            # transpose converts the tuple of 1D arrays to columns

            # header

            # try for similar non-delimiter
            if csv_delimiter == ',':
                non_delimiter = ';'
            elif csv_delimiter == ' ':
                non_delimiter = '_'
            else:
                non_delimiter = ' '

            # ordered list of other potential non-delimiters
            delimiters = list(' _-,;:+&|/?!#\t')

            def fix_delimited_string(s, non_delimiter=non_delimiter):
                ''' Usage: fix_delimited_string(header_item(s.text(), c.text(), r.text()))) '''
                if str(csv_delimiter) in s:
                    i = 0
                    while str(non_delimiter) in s:
                        try:
                            if str(delimiters[i]) not in s:
                                non_delimiter = delimiters[i]
                                break
                        except IndexError:
                            raise ValueError('All potential non-delimiters (%s) found in string "%s"' % (delimiters, s))
                        i += 1
                    return s.replace(csv_delimiter, non_delimiter)
                return s

            header[0] = fix_delimited_string(header[0])
            if averaging:
                for c in compartments:
                    for s in species:
#                        header.append(fix_delimited_string(averaging_header_item % (s.text(), c.text(), len(runs))))
                        header.append(fix_delimited_string(averaging_header_item(s.text(), c.text(), len(runs))))
            else:
                for r in runs:
                    for c in compartments:
                        for s in species:
                            header.append(fix_delimited_string(header_item % (s.text(), c.text(), r.text())))
#                            header.append(fix_delimited_string(header_item(s.text(), c.text(), r.text())))
            # write header at beginning of file
            from infobiotics.commons.files import prepend_line_to_file
            prepend_line_to_file(csv_delimiter.join(header), file_name)

        def write_xls():
            ''' https: // secure.simplistix.co.uk / svn / xlwt / trunk / README.html '''
            wb = xlwt.Workbook()
            try:
                ws = wb.add_sheet(os.path.basename(self.simulation.model_input_file)[:31])
            except:
                ws = wb.add_sheet('McssResults')
            ws.write(0, 0, header[0])
            for ti in range(len(timepoints)):
                ws.write(1 + ti, 0, timepoints[ti])
            if averaging:
                for ci, c in enumerate(compartments):
                    for si, s in enumerate(species):
                        y = 1 + si + (ci * len(species))
#                        ws.write(0, y, averaging_header_item % (s.text(), c.text(), len(runs)))
                        ws.write(0, y, averaging_header_item(s.text(), c.text(), len(runs)))
                        for ti in range(len(timepoints)):
                            ws.write(1 + ti, y, results[mean_index][si, ci, ti])
            else:
                for ri, r in enumerate(runs):
                    for ci, c in enumerate(compartments):
                        for si, s in enumerate(species):
                            y = 1 + si + (ci * len(species)) + (ri * len(species) * len(compartments))
                            ws.write(0, y, header_item % (s.text(), c.text(), r.text()))
                            for ti in range(len(timepoints)):
                                ws.write(1 + ti, y, results[ri][si, ci, ti])
            wb.save(file_name)

        def write_npz(species_indices=species_indices, compartment_indices=compartment_indices):
            # convert QString to str #TODO is this now unncessary with QString api version 2?
            species_names = [str(s.text()) for s in species]
            compartment_labels_and_positions = [str(c.text()) for c in compartments]
            run_numbers = [str(r.text()) for r in runs]
            kwargs = dict(
                run_indices=np.array(run_indices),
                run_numbers=run_numbers,
                species_indices=species_indices,
                species_names=species_names,
                compartment_indices=compartment_indices,
                compartment_labels_and_positions=compartment_labels_and_positions,
                timepoints=timepoints,
                model_file_name=os.path.basename(self.simulation.model_input_file),
                data_file_name=os.path.basename(self.simulation.data_file),
            )
            if averaging:
                kwargs['means'] = results[mean_index]
                kwargs['shape'] = ('species', 'compartment', 'timepoint')
            else:
                kwargs['levels'] = results
                kwargs['shape'] = ('run', 'species', 'compartment', 'timepoint')
            np.savez(file_name, **kwargs)

        if file_name.endswith('.npz'):
            write_npz()
        elif file_name.endswith('.xls'):
            write_xls()
        else:
            write_csv()#csv_precision, csv_delimiter) # done using default values

#        if copy_file_name_to_clipboard:
#            from infobiotics.commons.qt4 import copy_to_clipboard
#            copy_to_clipboard(file_name)
#
#        if open_after_save:
##            if file_name.endswith('.csv') or file_name.endswith('.xls'):
#            from infobiotics.commons.qt4 import open_file
#            open_file(file_name)

        return file_name        
        
        


    def timeseries_plot(self, mean_over_runs, parent=None, **kwargs):
#        timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=True)
#        timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=True)
#        timeseries = results.timeseries(amounts=True, volumes=True, mean_over_runs=False) 
#        timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=False)
#        timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=False)
        from timeseries_plot import TimeseriesPlot
        import os.path
        timeseries_plot = TimeseriesPlot(
            results=self,
            window_title='Timeseries from %s' % os.path.basename(self.filename),
            timeseries=self.timeseries(
                amounts=True,
                volumes=True if self.has_volumes else False,
                mean_over_runs=mean_over_runs,
            ),
            **kwargs
        )
        ui = timeseries_plot.edit_traits(kind='live')
        return ui
#        widget = ui.control
#        widget.setAttribute(Qt.WA_DeleteOnClose)
#        if parent:
#            widget.connect(parent, SIGNAL("destroyed(QObject*)"), SLOT("close()"))
#        widget.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowMinMaxButtonsHint|Qt.WindowCloseButtonHint)
#        widget.show()
#        return timeseries_plot
    
    def histograms(self, bins=10, data='compartments', sum_species=False, dtype=np.float64):#'float64'):
        '''Returns a 2D array of (histogram array, bin_edges array) tuples with 
        axes (species, timepoints) unless sum_species is True, in which case it 
        returns a 1D array of (histogram array, bin_edges array) tuples with 
        axes (timepoints,), unless average_timepoints is True in which case ... #TODO

#        Returns (array of) histograms for (the sum of all selected/each) species
#        averaging over runs or compartments at time t.

        data must be one of 'compartments' or 'runs'. From whichever it is 
        not, the mean will be taken.

        Note: this method is *not* suitable for use with matplotlib's hist function
        as that calls numpy.histogram itself - we can only pass it the data to 
        create the histogram from (look in McssResultsWidget.histograms for that).

        To access the histograms and bin_edges use: 
            histograms['histogram'][species_index, timepoint_index]
            histograms['bin_edges'][species_index, timepoint_index]
        
        '''

        mean = lambda array, axis: np.mean(array, axis, dtype=dtype)#np.float64)
        sum = lambda array, axis: np.sum(array, axis, dtype=dtype)#np.float64)

        numruns, numspecies, numcompartments, numtimepoints = self.amounts_shape 
        histogram_dtype = self.histogram_dtype(bins, dtype)
        
        data = data.lower()
        range = (0, len(self.compartments)) if data == 'compartments' else (0, len(self.runs))
        if data == 'compartments':
            mean_amounts_over_runs = self.functions_of_amounts_over_runs(mean)[0]
            if sum_species:
                sum_mean_amounts_over_runs_over_species = sum(mean_amounts_over_runs, 0)
                histograms = np.ndarray((numtimepoints,), dtype=histogram_dtype)
                for ti in xrange(numtimepoints):
                    histograms[ti] = np.histogram(sum_mean_amounts_over_runs_over_species[:,ti], bins, range)
            else:
                histograms = np.ndarray((numspecies,numtimepoints), dtype=histogram_dtype)
                for si in xrange(numspecies):
                    for ti in xrange(numtimepoints):
                        histograms[si,ti] = np.histogram(mean_amounts_over_runs[si,:,ti], bins, range)
        elif data == 'runs':
            mean_amounts_over_compartments = mean(self.amounts(), self.amounts_axes.index('compartments'))
            if sum_species:
                sum_mean_amounts_over_compartments_over_species = sum(mean_amounts_over_compartments, 1)
                histograms = np.ndarray((numtimepoints,), dtype=histogram_dtype)
                for ti in xrange(numtimepoints):
                    histograms[ti] = np.histogram(sum_mean_amounts_over_compartments_over_species[:,ti], bins, range)
            else:
                histograms = np.ndarray((numspecies,numtimepoints), dtype=histogram_dtype)
                for si in xrange(numspecies):
                    for ti in xrange(numtimepoints):
                        histograms[si,ti] = np.histogram(mean_amounts_over_compartments[:, si, ti], bins, range)
        else:
            raise ValueError("data argument must be either 'compartments' or 'runs'")
        return histograms

    def histogram_dtype(self, bins, dtype=np.float64):#'float64'):
        # np.zeros(3, dtype=[('x','f4'),('y',np.float32),('value','f4',(2,2))]) # http://docs.scipy.org/doc/numpy/user/basics.rec.html "Defining Structured Arrays"  3) List argument
        return np.dtype([('histogram', dtype, (bins,)),('bin_edges', dtype, (bins+1,))])

    @property
    def amounts_axes(self):
        return ('runs','species','compartments','timepoints')
        
    @property
    def amounts_shape(self):
        return self.num_selected_runs, self.num_selected_species, self.num_selected_compartments, self.num_timepoints

    @property
    def num_selected_runs(self):
        return len(self.run_indices)

    @property
    def num_selected_species(self):
        return len(self.species_indices)
    
    @property
    def num_selected_compartments(self):
        return len(self.compartment_indices)
    
    @property
    def num_timepoints(self):
        return len(self.timepoints)
    

    @property
    def compartment_indices(self):
        return self._compartment_indices

    @compartment_indices.setter
    def compartment_indices(self, compartment_indices):
        _compartment_indices = xrange(self.simulation._runs_list[0].number_of_compartments)
        self._compartment_indices = [i for i in compartment_indices if i in _compartment_indices]


    def surfaces(self):
        '''Returns a 5D array (runs, species, x_position, y_position, timepoints) 
        of the *cumulative* amounts of each species in all the selected compartments
        at each (x,y) position.
        
        The surface of the second species in the third run at timepoint 0 is 
        surfaces()[2,1,:,:,0].
        
        The points that define the area of the surface are retrievable with
        xy_min_max(): (xmin, xmax), (ymin, ymax) = results.xy_min_max()
        
        surfaces = results.surfaces() 
        >>> print surfaces.shape
        (3, 2, 1, 15, 17)
        
        # the mean over runs of each species
        >>> print mean(surfaces, 0).shape 
        (2, 1, 15, 17)
        
        # the mean over runs of the sum of the species amounts
        >>> print mean(sum(surfaces, 1), 0).shape
        (1, 15, 17)
        
        '''

        all_compartments = self.simulation._runs_list[self.run_indices[0]]._compartments_list
        #FIXME has to pick one run to get compartments from - not ideal but can't think of a better way for now 
        
        selected_compartments = [all_compartments[i] for i in self.compartment_indices]
        
        (xmin, xmax), (ymin, ymax) = self.xy_min_max()

        # create surfaces array
        surfaces = self._allocate_array(
            (
                len(self.run_indices),
                len(self.species_indices),
                (xmax - xmin) + 1,
                (ymax - ymin) + 1,
                len(self.timepoints)
            ),
            'Could not allocate memory for surfaces.\n'\
            'Try selecting a shorter time window or a longer time step.'
        )

        amounts = self.amounts()
        
        # fill surfaces with amounts
#        for ri, _ in enumerate(self.run_indices):
#            for si, _ in enumerate(self.species_indices):
#                for ci, _ in enumerate(self.compartment_indices):
#                    compartment = selected_compartments[ci]
#                    surfaces[ri, si, compartment.x_position - xmin, compartment.y_position - ymin, :] += amounts[ri, si, ci, :]
#        np.save('/home/jvb/Desktop/before', surfaces)
        for ci, _ in enumerate(self.compartment_indices):
            compartment = selected_compartments[ci]
            for si, _ in enumerate(self.species_indices):
                surfaces[:, si, compartment.x_position - xmin, compartment.y_position - ymin, :] += amounts[:, si, ci, :]
#        np.save('/home/jvb/Desktop/after', surfaces)
        np.save('/home/jvb/Desktop/next', surfaces)
        return surfaces
    
    def x_min_max(self):
        '''
        xmin, xmax = results.x_min_max()
        '''
        x_positions = [self.simulation._runs_list[0]._compartments_list[i].x_position for i in self.compartment_indices]
        return min(x_positions), max(x_positions)
        
    def y_min_max(self):
        '''
        ymin, ymax = results.y_min_max()
        '''
        y_positions = [self.simulation._runs_list[0]._compartments_list[i].y_position for i in self.compartment_indices]
        return min(y_positions), max(y_positions)
        
    def xy_min_max(self):
        ''' 
        (xmin, xmax), (ymin, ymax) = results.xy_min_max()
        '''
        return self.x_min_max(), self.y_min_max()

    @property
    def has_volumes(self):
        return True if self.simulation.log_volumes == 1 else False #TODO
    
    @property
    def has_default_volume(self):
        try:
            self.default_volume.rescale(volume_units[self.volumes_display_units])
            return True
        except AttributeError:
            return False
        
    

def test1():
    results = McssResults('tests/NAR_simulation.h5')

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
    

def test_surfaces():
    results = McssResults('tests/germination_09.h5')
    results.select_species('SIG1', 'P1')
#    print results.runs_information()
#    print results.species_information(sort_column_index=0)
#    print results.compartments_information(sort_column_index=1)
#    print results.compartments_information(sort_column_index=3)
    results.timestep = 1 * hour
    results.timepoints_display_units = 'minutes'
#    print results.timepoints
    results.select_runs([1, 2, 3])
#    print results.amounts().shape # (3, 2, 39, 17)
    results.select_compartments(xy_coordinates=[(0, y) for y in range(15, 30)])
#    print results.compartment_indices
    surfaces = results.surfaces() 
    print surfaces.shape
    print mean(surfaces, 0).shape # the mean over runs of each species 
    print mean(sum(surfaces, 1), 0).shape # the mean over runs of the sum of the species amounts

def test_timeseries():
    file_name = 'tests/germination_09.h5'
    results = McssResults(file_name)
    print results.timeseries_information()
    exit()
    results.select_species('SIG1')#, 'P1')
    results.timestep = 1 * hour # 961 -> 17
    results.timepoints_display_units = 'minutes'
    results.quantities_display_type = 'concentrations'
    results.quantities_display_units = 'molar'
    results.volumes_data_units = 'microlitres'
    results.volumes_display_units = 'femtolitres'
#    print results.quantities_data_units, results.quantities_display_type, results.quantities_display_units
#    print results.volumes_data_units, results.volumes_display_units
#    print results.amounts().units
    results.select_runs([1, 2, 3])
#    results.select_runs([1])
#    print results.compartments_information(); exit()
    results.select_compartments(['receiver'], [(0, i) for i in range(10, 13)])
    timeseries = results.timeseries(amounts=True, volumes=True, mean_over_runs=True)
#    timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=True)
#    timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=True)
#    timeseries = results.timeseries(amounts=True, volumes=True, mean_over_runs=False) 
#    timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=False)
#    timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=False)
    from timeseries_plot import TimeseriesPlot
    TimeseriesPlot(
        timeseries=timeseries,
        window_title='Timeseries Plot(s) for %s' % file_name,
    ).configure_traits()
    

def test_histograms():
    results = McssResults('../../../examples/mcss/models/module1.h5')
    print results.histograms().shape
    print results.histograms(sum_species=True).shape
    print results.histograms(data='runs').shape
    print results.histograms(data='runs', sum_species=True).shape
     

if __name__ == '__main__':
    import mcss_results_widget
    mcss_results_widget.main('../../../examples/tutorial-autoregulation/autoregulation_simulation.h5')
    
##    test1()
#    test_surfaces()
#    test_timeseries()
#    test_histograms()
