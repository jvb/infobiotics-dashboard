from infobiotics.shared.traits_imports import *
from infobiotics.dashboard.plugins.mcss_results.mcss_results_views import *
from infobiotics.dashboard.plugins.mcss_results.mcss_results_plots import *


class McssResultsSpecies(HasTraits):
    name = Str
    index = Int


class McssResultsCompartment(HasTraits):
    compartment_x_position = Int
    compartment_y_position = Int
    compartment_z_position = Int
    

class McssResultsRun(HasTraits):
    run_number = Int
    index = Int
    def _index_default(self):
        self.index = self.run_number - 1
    def _run_number_changed(self):
        self.index = self._index_default()
        

class McssResultsSimulation(HasTraits):
    ''' Contains attributes of an mcss simulation's root node.
    
    '''
    species = List(McssResultsSpecies)
    compartments = List(McssResultsCompartment)
    runs = List(McssResultsRun)
    timepoints = ListFloat


class McssResults(HasTraits):
    '''Displays contents of mcss's H5 output files, 
    allowing simulation results to be saved or plotted.
    '''
    view = mcss_results_view

    filename = File(exists=True)
    def _filename_changed(self):
        simulation = McssResultsSimulation.fromFile(self.filename)

    simulation = Instance(McssResultsSimulation)
#    species = DelegatesTo('simulation')
#    compartments = DelegatesTo('simulation')
#    runs = DelegatesTo('simulation')
    # replaced by Item('object.simulation.species'... in mcss_results_view
    selected_species = List(McssResultsSpecies)
    selected_compartments = List(McssResultsCompartment)
    selected_runs = List(McssResultsRun)
    selected_species_names = ListStr
    selected_compartments_names = ListStr
    selected_runs_names = ListStr
    selected_species_indicies = ListInt
    selected_compartments_indicies = ListInt
    selected_runs_indicies = ListInt
    def _selected_species_changed(self, value):
        self.selected_species_indicies = [species.index for species in self.selected_species]
        self.selected_species_names = [species.name for species in self.selected_species]

    def _selected_compartments_changed(self, value):
        self.selected_compartments_indicies = [compartment.index for compartment in self.selected_compartments]
    def _selected_runs_changed(self, value):
        self.selected_runs_indicies = [run.index for run in self.selected_runs]
        
        
    from_ = Float
    to = Float
    every = Int
    _every_low = Int(1)
    _every_high = Int(10)
    units = Str('seconds')
    log_interval = Float

    plot_quantities = Enum(['molecules','concentrations'])
    plot_volumes = Bool(False)
    average_runs = Bool(label='Average runs')
    average_runs_which = Enum(['selected','all'])
    
    plot_summary = Bool
    summary_type = Enum(['summing','averaging'])
    summary_species = Enum(['selected','each','all'])
    summary_position = Enum(['in selected compartments', 'at each (x,y) lattice position'])

    plot_type = Enum(['Timeseries','Surface','Histogram','Continuous Histogram'])
    timeseries_options = Instance(TimeseriesOptions, TimeseriesOptions())
    surface_options = Instance(SurfaceOptions, SurfaceOptions())
    histogram_options = Instance(HistogramOptions, HistogramOptions())
    continuous_histogram_options = Instance(ContinuousHistogramOptions, ContinuousHistogramOptions())


    def __repr__(self): #TODO 
        repr = ''
        return repr


    def plot(self, info): #TODO
        pass
        

    def save_data(self, info): #TODO
        pass



if __name__ == '__main__':
    
    species = [
        McssResultsSpecies(
            name=name, 
            index=i
        ) for i, name in enumerate('abcdefgh')
    ]
    
    environment = McssResultsCompartment(name='Environment', volume=100)
    compartments = [environment]
    compartments += [
        McssResultsCompartment(
            name='bacteria',
            volume=1, 
            compartment_x_position=x,
            compartment_y_position=y,
            compartment_z_position=z,
            parent=environment,
        ) for x in range(3) for y in range(3) for z in [1]
    ]
    
    runs = [McssResultsRun(run_number=i) for i in range(1,11)]
    
    simulation = McssResultsSimulation(species=species, compartments=compartments, runs=runs)
    
    McssResults(simulation=simulation).configure_traits()
