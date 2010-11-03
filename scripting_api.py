''' Attempt to define scripting API that can also be used by 
SimulatorResultsDialog.

1 create experiment
~ load/edit/save parameters
2 perform experiment, get results
3 select subset of results
4 get timeseries/histograms/surfaces
5 plot/edit timeseries/histograms/surfaces
6 save timeseries/histograms/surfaces

'''

from enthought.traits.api import HasTraits, Property, Dict, Str, List, Any, Int
from infobiotics.commons.traits.float_greater_than_zero import FloatGreaterThanZero
from infobiotics.commons.traits.relative_file import RelativeFile
from quantities.unitquantity import UnitQuantity
import tables
from infobiotics.core.traits.params_relative_file import ParamsRelativeFile
import random
from enthought.traits.trait_types import Bool
from infobiotics.commons.quantities.units.volume import *
from enthought.traits.api import cached_property
import numpy as np
from infobiotics.commons.traits.int_greater_than_zero import IntGreaterThanZero
from infobiotics.commons.sequences import flatten

'''
class McssExperiment(HasTraits):
    
    file_name = ParamsRelativeFile

    def _file_name_changed(self):
        self.load(self.file_name)

    max_time = FloatGreaterThanZero(60)
    time_units = UnitQuantity #TODO add to McssExperiment
    data_file = RelativeFile
    
    def perform(self, thread=False):
        h5 = self.data_file
        pass #TODO write time_units.dimensionality to h5
        return McssResults()
    
file_name = 'filename.params'
mcss_experiment = McssExperiment(file_name=file_name) # load parameters from .params file
#mcss_experiment.max_time = 200 # set parameter
#mcss_experiment.save(file_name) # save_parameters to .params files
#mcss_experiment.load(file_name) # load parameters from .params file
#mcss_experiment.configure() # set/save/load parameters using GUI
#mcss_experiment.edit() # should delegate to configure() if no GUI thread exists
mcss_results = mcss_experiment.perform() # run experiment in same thread, returning Results()
#mcss_results.configure()


# setting units
#volumes_data_units = 'microlitre'
#mcss_results.set_units(volumes_data_units=volumes_data_units)
#mcss_results.set_volumes_data_units(volumes_data_units)
#mcss_results.set_substance_display_units('nM')

# default volume needed for concentrations when log_volumes=False
mcss_results.volume = 0.1 * ul 

# selecting a subset of results
selection = mcss_results.selection() # get current selection
selection = dict(
    species='a', # preferred
    species_name='a', # preferred
    species_names='a',
    species_names=['a'], # preferred
    compartment='bacterium', # preferred
    compartment_name='bacterium', # preferred
    compartment_names='bacterium',
    compartment_names=['bacterium'], # preferred
    from_timepoint=0,
    to_timepoint=60,
)
mcss_results.select(**selection) # update selection with kwargs (or dict)
mcss_results.selection = selection # change selection through setter
mcss_results.reset_selection() # reset selection (probably to all)

# getting list of Timeseries objects with updated selection
timeseries = mcss_results.timeseries(
    amounts=True,
    volumes=True,
    # **selection; selection = dict(
    species_indices=[],
    species_names=[],
    compartment_indices=[],
    compartment_names=[],
    run_indices=[],
    run_numbers=[],
    each_runs=True, # can be mixed with average_over_runs
    all_runs=True, # one must be specified, default to all_runs (mean, std)
    timepoints=[], # nearest timepoints to items
    timepoint_indices=[], # indices cropped to existing (automatic?)
    from_timepoint=None, # first timepoint
    to_timepoint=None, # last timepoint
)
timeseries = results.timeseries(**selection)
assert McssExperiment().perform().timeseries(**selection) == McssExperiment().perform().select(**selection).timeseries()  

# viewing and saving timeseries plots
plot = TimeseriesPlot(timeseries)
plot.save(width=640, height=480)
#plot.configure()

#def perform_experiment(experiment):
#    return experiment.perform()
'''

def is_concentration(units):
    if units in ('TODO'):
        return True
    return False

class Run(HasTraits):
    run_index = Int
    run_number = Int
    
class Species(HasTraits):
    species_index = Int
    species_name = Str

class Compartment(HasTraits):
    compartment_index = Int
    compartment_name = Str
    compartment_x_position = Int
    compartment_y_position = Int

class McssResults(HasTraits):
    ''' Loaded from an H5 file, returned by McssExperiment().perform()
    
    IMPORTANT: Assumes that all runs are the same, ignores runs stopped 
        midway with Ctrl-C if other runs have completed.
        
    IMPORTANT: Assumes that all compartments are the same (neither created,
        destroyed or moved), although volume information changes for each run.
    
    Selection is stateful - reused between methods like timeseries() or 
        histogram(), but can be overridden in those method calls:
        timeseries(**selection). This means that the same McssResults object
        can be used to extract data for multiple subsets of results.
        
    Selection can be set all at once using selection = {} or individually by
        setting, for instance, run_indicies or run_numbers. #TODO
    
    Timeseries, histograms or surfaces are returned as lists depending on 
        arguments (amounts, volumes, each_run, all_runs, each_compartment, 
        all_compartments, each_species, all_species, etc., rather than 
        returning amounts or volumes data as multi-dimensional arrays.
        
    Units is also stateful, including data units and display units (display 
        units can be overridden in timeseries(), etc. 
    
    '''
    
    compartments = Property(List(Compartment), selectable=True) # selectable metadata 
    selected_compartments = List(Compartment, selected=True) # selected metadata
    compartments_indices = Property(List(Int), selectable=True) # selectable metadata
    selected_compartments_indices = List(Int, selected=True) # selected metadata
    
    def _get_compartments(self): # repeat for species, runs, etc.
        ''' Return list/generator of compartment objects '''
        return self._compartments

#    def _set_compartments(self, compartments): # read-only property

    def _get_selected_compartments(self):
        ''' Return list/generator of selected compartment objects '''
        return self._selected_compartments
    
    def _set_selected_compartments(self, selected_compartments):
        self._selected_compartments = selected_compartments
    
    def _get_selected_compartment_indices(self):
        ''' Return list/generator of selected compartment indices '''
        pass


    
#    def __init__(self, data_file, **traits):
#        f = tables.openFile(data_file, 'r')
#        pass # do something with f, like create Simulation object
#        self._compartments = []
#        #TODO make f.root._v_attrs readonly traits on this object
#        HasTraits.__init__(self, **traits)
#        self.data_file = data_file

    def compartments(self): # repeat for species, runs, etc.
        ''' Return list/generator of compartment objects '''
        pass


    def select(self, **selection):
        ''' Select items without resetting selection and return updated 
        selection. '''
        self.trait_set(**selection) # trait_set doesn't use metadata
        return self.selection
        
    
    __selection_names = ['run_indices', 'run_numbers'] 
    
    selection = Property(Dict(Str, List(Any)), depends_on=__selection_names)
    
    def _get_selection(self):
#        return dict([(name, getattr(self, name)) for name in self.__selection_names])
        return self.trait_get(*self.__selection_names)
        
    def _set_selection(self, **selection):
        self.reset_selection()
#        for key, value in selection.iteritems():
#            if key in (self.__selection_names):
##                setattr(self, key, value)
#                self.trait_set(key=value)
        self.trait_set(**selection)
        return self.selection()
        
    def reset_selection(self):
        pass
                
    
    def random_run_indices(self, number_of_runs):
        return random.sample(self.run_indices, number_of_runs)

    def select_runs_randomly(self, number_of_runs):
        self.select(run_indices=self.random_run_indices(number_of_runs))


    def run_indices(self, run_indices=[], run_numbers=[]):
        ''' Given a mix of run indices and numbers, return the list of 
        run indices. '''
        if len(run_indices) + len(run_numbers) == 0: 
            return self.all_run_indices #TODO or None?
        run_number_indices = [number - 1 for number in run_numbers if 0 <= number <= self.simulation.number_of_runs]
        return run_indices + run_number_indices
    
    def species_indices(self, species_indices=[], species_names=[]):
        ''' Given a mix of species indices and names, return the list of 
        species indices. '''
        #TODO handled species_names='a' as well as species_names=['a']
        if len(species_indices) + len(species_names) == 0: 
            return self.all_species_indices #TODO or None?
        species_name_indices = [species.index for species in self.species for name in species_names if species.name == name]
        #TODO treatment needed for indices out-of-range?
        return species_indices + species_name_indices
    
    def compartment_indices(self, compartment_indices=[], compartment_names=[], compartment_x_y_coordinates=[], compartment_x_coordinates=[], compartment_y_coordinates=[]):
        ''' Given a mix of compartment indices, names, x and y, x and y 
        coordinates, return the list of compartment indices. '''
        #TODO handle compartment_names='c' as well as compartment_names=['c']
        if len(compartment_indices) + len(compartment_names) + len(compartment_x_y_coordinates) + len(compartment_x_coordinates) + len(compartment_y_coordinates) == 0: 
            return self.all_compartments_indices #TODO or None?
        pass #TODO narrow by name, x_compartment_y_coordinates, compartment_x_coordinates and compartment_y_coordinates
        #TODO treatment needed for indices out-of-range?
        return compartment_indices + None


    def all_indices(self,
        run_indices=[], run_numbers=[],
        species_indices=[], species_names=[],
        compartment_indices=[], compartment_names=[], compartment_x_y_coordinates=[], compartment_x_coordinates=[], compartment_y_coordinates=[],
        timepoint_indices=[], timepoints=[]
    ):
        ''' Given the complete mix of selectable traits, return a tuple of 
        lists of indices: (runs, species, compartments, timepoints) '''
        return (
            self.run_indices(run_indices, run_numbers),
            self.species_indices(species_indices, species_names),
            self.compartment_indices(compartment_indices, compartment_names, compartment_x_y_coordinates, compartment_x_coordinates, compartment_y_coordinates),
            self.timepoint_indices(timepoint_indices, timepoints),
        )    


#    def kwargs(self,
#        amounts=True,
#        volumes=True,
#        volume=None,
#        run_indices=[], run_numbers=[],
#        species_indices=[], species_names=[],
#        compartment_indices=[], compartment_names=[], compartment_x_y_coordinates=[], compartment_x_coordinates=[], compartment_y_coordinates=[],
#        timepoint_indices=[], timepoints=[],
#    ):
#        if volume is None:
#            volume = self.volume
#        pass
#        run_indices, species_indices, compartment_indices, timepoint_indices = self.all_indices(
#            run_indices=run_indices, run_numbers=run_numbers,
#            species_indices=species_indices, species_names=species_names,
#            compartment_indices=compartment_indices, compartment_names=compartment_names, compartment_x_y_coordinates=compartment_x_y_coordinates, compartment_x_coordinates=compartment_x_coordinates, compartment_y_coordinates=compartment_y_coordinates,
#            timepoint_indices=timepoint_indices, timepoints=timepoints,
#        )
#        pass
#        return


    volume = FloatGreaterThanZero

    volumes = Property(Bool)
    
    def _set_volumes(self, volumes):
        if self.log_volumes:
            return volumes
        elif volumes:
            raise ValueError('No volumes dataset, use McssExperiment(log_volumes=True)')
        else:
            return False

    def timeseries(self, amounts=True, volumes=False, **selection):
        ''' Returns a list of Timeseries objects. '''
        
        volumes = self._set_volumes(volumes) # reuse setter without changing self.volumes (hopefully)
        
#        if is_concentration(substance_display_units) and self.volume == 0:
#            raise ValueError('self.volume > 0, use results.volume = 0.1 * uL')
        
        run_indices, species_indices, compartment_indices, timepoint_indices = self.all_indices(**selection)
        pass

    def plot_timeseries(self, **kwargs):
        ''' TimeseriesPlot(self.timeseries(**selection).configure() '''
        #TODO get selection from kwargs
#        plot = TimeseriesPlot(self.timeseries(**selection))
#        plot.configure()
#        return plot

    def histograms(self, **selection):
        ''' Returns a list of Histogram objects. '''
        run_indices, species_indices, compartment_indices, timepoint_indices = self.all_indices(**selection)
        pass

    def surface(self, **selection):
        ''' Returns list of surfaces objects.
        
        Each surface object has a 3D array 
        (mean/std/individual amounts/volume at each x, y, timepoint)
        that can be visualised using mlab.surf() 
        
        '''
        run_indices, species_indices, compartment_indices, timepoint_indices = self.all_indices(**selection)
        pass

    def export_timeseries(self, file_name, format=None, **selection): #TODO can guess format from file_name
        if format is None:
            format = self.export_format
        pass
            
#    def export_histograms( #TODO
    
#    def export_surfaces( #TODO 
                     
                     
    max_time = FloatGreaterThanZero
    number_of_timepoints = IntGreaterThanZero

    timepoints = Property(List(FloatGreaterThanZero), depends_on='max_time, number_of_timepoints')

    @cached_property    
    def _get_timepoints(self):
        return np.linspace(0, self.max_time, self.number_of_timepoints) 

    def timepoint_indices(self,
        timepoints=[], # most common use-case, should be first
        from_timepoint=None, # first timepoint
        to_timepoint=None, # last timepoint
        timepoint_stride=1, # for slicing from from_timepoint to to_timepoint
        from_timepoint_index=0, # first timepoint
        to_timepoint_index= -1, # last timepoint
        timepoint_index_stride=1, # for slicing from from_time_index to to_timepoint_index
        timepoint_indices=[], # least common use-case, should be last
    ):
        ''' Given a mix of timepoint indices and timepoints, return the sorted
        list of timepoint indices. '''

        # sanitise inputs
        if isinstance(timepoints, basestring) or isinstance(timepoints, (float, int)):
            timepoints = [float(timepoints)]
        else:
            timepoints = flatten([timepoints]) #TODO test
        if from_timepoint is not None:
            from_timepoint = float(from_timepoint)
        if to_timepoint is not None:
            to_timepoint = float(to_timepoint)
        timepoint_stride = float(timepoint_stride) # not sure how to slice with this, use % (modulo)?
        from_timepoint_index = int(from_timepoint_index)
        to_timepoint_index = int(to_timepoint_index)
        timepoint_index_stride = int(timepoint_index_stride)

        timepoint_indices_from_timepoints = 
        
        timepoint_indices_from_timepoint_range
        
        timepoint_indices_from_timepoint_indices_slice
        
        timepoint_indices_from_timepoint_indices
        


        if len(timepoints) > 0:
            timepoints_indices = [bisect.bisect_left(self.timepoints, math.floor(timepoint)) for timepoint in timepoints]
        elif from_timepoint is not None or to_timepoint is not None:
            if from_timepoint is not None:
                from_timepoint_index = bisect.bisect_left(self.timepoints, math.floor(from_timepoint))
                from_timepoint = self.timepoints[from_timepoint_index] #TODO comment out
            if to_timepoint is not None:
                to_timepoint_index = bisect.bisect_right(self.timepoints, math.ceil(to_timepoint))
                to_timepoint = self.timepoints[to_timepoint_index] #TODO comment out
        else:
            
            timepoints_indices = timepoints[from_timepoint_index:to_timepoint_index:timepoint_index_stride]
        elif len(timepoint_indices) > 0:
            return timepoint_indices

        if len(timepoint_indices) + len(timepoints_indices) == 0: 
            return [i for i, _ in enumerate(self.timepoints)]
        
        return timepoint_indices + timepoints_indices    
                          

import unittest2
import bisect, math

class TestIndicesFunctions(unittest2.TestCase):
    
    def setUp(self):
        self.mcss_results = McssResults(
            max_time=60,
            number_of_timepoints=121,
        )

    def test_timepoints(self):
        self.assertEqual(len(self.mcss_results.timepoints), self.mcss_results.number_of_timepoints, 'there should be as many timepoints as number_of_timepoints specifies')
        self.assertEqual(self.mcss_results.timepoints[0], 0, 'first timepoint should be 0')
        self.assertEqual(self.mcss_results.timepoints[-1], self.mcss_results.max_time, 'last timepoint should be equal to max_time')

    def test_timepoints_indices(self):
#        print self.mcss_results.timepoints

#        self.timepoint_indices = [i for i, timepoint in enumerate(self.mcss_results.timepoints)]
#        print timepoint_indices

#        self.mcss_results.timepoint_indices(timepoint_indices, timepoints, from_timepoint, to_timepoint, timepoint_stride, from_timepoint_index, to_timepoint_index, timepoint_index_stride)
        print self.mcss_results.timepoint_indices(timepoint_indices=[0, 1])
        
        # timepoints kwarg as arg
        print self.mcss_results.timepoint_indices([0, 1])
        print self.mcss_results.timepoint_indices(2)
        print self.mcss_results.timepoint_indices([[2]])
        print self.mcss_results.timepoint_indices('2')
        
        print self.mcss_results.timepoint_indices(from_timepoint='2', to_timepoint=60)
        



#        self.mcss_results.timepoint_indices(timepoint_indices, timepoints, from_timepoint, to_timepoint, timepoint_stride, from_timepoint_index, to_timepoint_index, timepoint_index_stride)        
    

if __name__ == '__main__':
    unittest2.main()
#    results = McssResults(
#                          
#    )
#    results.print_traits(selectable=True)
