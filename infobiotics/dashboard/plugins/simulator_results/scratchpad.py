import numpy as np
from PyQt4.QtGui import QWidget, QMessageBox 
import tables

## testing whether local variables in inner functions can affect those outside
## they don't:
#class _SimulatorResults(object):
#    def get_functions_over_runs(self):
#        chunk_size = 1
#        def iteration(chunk_size=chunk_size):
#            chunk_size += 1
#            assert chunk_size == 2
#        iteration()
#        assert chunk_size == 1
#_SimulatorResults().get_functions_over_runs()        
#exit()

class SimulatorResults(object):

    type = np.float64
    
    def _allocate_array(self, shape, failed_message):
        try:
            array = np.zeros(shape, self.type) # np.empty would be faster... 
        except MemoryError:
            self._out_of_memory_warning(failed_message)
            return
        return array
    
    def _out_of_memory_warning(self, message):
        if self.parent is not None and isinstance(self.parent, QWidget):
            QMessageBox.warning('Out of memory', message, self.parent)
        else:
            print message
    
#    def functions_of_volumes_over_timepoints(self, functions): pass #TODO

    # mcss produces a separate amounts array for each run
    # we want a 4D array to which we can apply functions along any axis
    # we might need to chunk on a different axis (not just timepoints)
#    def get_functions_over_runs(self, functions):
    def functions_of_amounts_over_timepoints(self, functions): # consist name
#        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
#        array of floats and results is a list of 3-D arrays of floats with the 
#        shape (species, compartments, timepoint) for each function in 
#        functions. '''
        
        # reserve memory by allocating results array first
        results = self.allocate_array(
            (
                len(functions),
                len(self.species_indices),
                len(self.compartment_indices),
                len(self._timepoints)
            ),
            'Could not allocate memory for functions.\nTry selecting fewer ', \
            'functions, a shorter time window or a bigger time interval ', \
            'multiplier.'
        )
        if results is None:
            return

        # start with the maximum chunk size
        chunk_size = self.max_chunk_size

        # allocate buffer (4-dimensional array) where one dimension is chunk_size long
        buffer = None
        while buffer is None:
            # progressively reduce chunk_size until buffer fits into memory
            try:
                buffer = np.zeros((len(self.species_indices),
                                      len(self.compartment_indices),
                                      chunk_size, #FIXME this is the crux, we don't want to always chunk along timepoints axis
                                      len(self.run_indices)),
                                      self.type)
            except MemoryError:
                if chunk_size == 0:
                    # can't make chunk_size any smaller so give up #TODO try and chunk along another axis then - recursively?
                    self._out_of_memory_warning('Could not allocate memory for chunk.\nTry selecting fewer runs, species or compartments, a shorter time window or a bigger time interval multipler.')
                    return
                # can still make chunk size smaller
                chunk_size = chunk_size // 2 # halve chunk_size with rounding
#                buffer = None
                continue

        def iteration(chunk_size=chunk_size): # doesn't affect chunk_size outside of function thank goodness
            ''' One iteration reads amounts into buffer and applies functions along axis. '''
            amounts_chunk_end = amounts_chunk_start + (chunk_size * self.every)
            for ri, r in enumerate(self.run_indices):
                amounts = h5.getNode('/run%s' % (r + 1), 'amounts')[:, :, amounts_chunk_start:amounts_chunk_end:self.every] #TODO change to use chunk_axis_index
                for si, s in enumerate(self.species_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        buffer[si, ci, :, ri] = amounts[s, c, :] #TODO works but surely buffer[:, :, :, ri] = amounts[self.species_indices, self.compartment_indices, :] could work too, no?
            stat_chunk_end = stat_chunk_start + chunk_size
            for fi, f in enumerate(functions):
                stat = results[fi][:]
                stat[:, :, stat_chunk_start:stat_chunk_end] = f(buffer)

        h5 = tables.openFile(self.filename)

        amounts_chunk_start = self.start
        stat_chunk_start = 0
        # for each whole chunk
        quotient = len(self._timepoints) // chunk_size
        for _ in range(quotient):
            iteration()#chunk_size)
            amounts_chunk_start = amounts_chunk_end
            stat_chunk_start = stat_chunk_end

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
        return results    


    amounts_axes = ['runs', 'species', 'compartments', 'timepoints']
    
    volumes_axes = ['runs', 'compartments', 'timepoints']


    def functions_of_values_over_axis_chunked(self, array_node_name, array_axes, axis, functions):
    
        assert axis in array_axes

        self.run_indices = range(10)
        self.species_indices = range(5)
        self.compartment_indices = range(3)
        self._timepoints = range(10000000)
    
        axis_to_length_map = { # will work for amounts and volumes
            'runs':len(self.run_indices),
            'species':len(self.species_indices),
            'compartments':len(self.compartment_indices),
            'timepoints':len(self._timepoints),
        }

        #TODO try and allocate a buffer of length of the axis to apply one and if that fails give up completely
        try:
            axis_length = axis_to_length_map[axis]
            test = np.zeros((axis_length,), self.type)
        except MemoryError:
            raise MemoryError("Can't perform calculation: length of axis '%s' is too long (%d) to fit into memory." % (axis, axis_length))
        else:
            del test

        axis_index = array_axes.index(axis)
        
        # find index of an axis that we can chunk on (not axis_index) in case we need to
        available_axes_indices = [i for i, _ in enumerate(array_axes) if i != axis_index]
        try:
            chunk_axis_index = available_axes_indices[-1] # use last axis
        except IndexError, e:
            # no available axis to chunk on, prepare to give up if we need to chunk
            chunk_axis_index = None
            
    
    
    
    
        # determine max chunk size which is the length of the axis given by chunk_axis_index
        if chunk_axis_index is not None:
#            max_chunk_size = eval('len(array[%s])' % ', '.join(['0' if i != chunk_axis_index else ':' for i, _ in enumerate(array_axes)]))
            max_chunk_size = axis_to_length_map[array_axes[chunk_axis_index]]
        else:
            max_chunk_size = 0 # will trigger failure when creating buffer
        chunk_size = max_chunk_size
        
        results_shape = [len(functions)]
        for ax in array_axes:
            if ax != axis:
                results_shape.append(axis_to_length_map[ax])
        print results_shape
        results = np.zeros(results_shape)
         
        buffer = None
        while buffer is None:
            try:
                buffer_shape = []
                for i, ax in enumerate(array_axes):
                    if i == chunk_axis_index:
                        buffer_shape.append(chunk_size)
                    else:
                        buffer_shape.append(axis_to_length_map[ax])
                print buffer_shape
                buffer = np.zeros(buffer_shape)
            except MemoryError, e:
                if chunk_size == 0:
                    raise e #TODO try another chunk_axis
                chunk_size = chunk_size // 2
                continue
        print buffer.shape

SimulatorResults().functions_of_values_over_axis_chunked('amounts', SimulatorResults.amounts_axes, 'timepoints', ['mean', 'std'])

    
#def test_huge_h5():
#    h5 = tables.openFile('../../../../examples/huge/huge.h5')
#    number_of_runs = h5.root._v_attrs.number_of_runs
#    number_of_species = h5.root._v_attrs.number_of_species
#    number_of_compartments = h5.root.run1._v_attrs.number_of_compartments
#    number_of_timepoints = h5.root.run1._v_attrs.number_of_timepoints
##    print number_of_runs, number_of_species, number_of_compartments, number_of_timepoints
#    amounts = np.zeros((number_of_runs, number_of_species, number_of_compartments, number_of_timepoints))
#    for ri in range(number_of_runs):
#        where = '/run%s' % (ri + 1)
#        amounts = h5.getNode(where, 'amounts')
#        print amounts[:]
#    h5.close()
    
    
if __name__ == '__main__':
    pass
#    test_huge_h5()
#    main()
    
