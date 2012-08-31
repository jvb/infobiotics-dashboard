def species_names(self, pattern='', case_sensitive=True, regex=False):
    return filter(self.species, 'name', pattern, case_sensitive, regex)
            
def filter(l, a, pattern='', case_sensitive=True, regex=False):
    ''' Return a subset of the a collection (l) whose item's string 
    attribute (a) matches 'pattern'. 
    
    Uses Unix shell-style wildcards when regex False.
    
    '''
    if pattern == '':
        return [getattr(i, a) for i in l]
    import re
    if regex:
        if not case_sensitive:
            return [getattr(i, a) for i in l if re.search(pattern, getattr(i, a), re.IGNORECASE) != None]
        else:
            return [getattr(i, a) for i in l if re.search(pattern, getattr(i, a)) != None] 
    else:
        import fnmatch
        if not case_sensitive:
            return [getattr(i, a) for i in l if re.search(fnmatch.translate(pattern), getattr(i, a), re.IGNORECASE) != None]
        else:
            return [getattr(i, a) for i in l if re.search(fnmatch.translate(pattern), getattr(i, a)) != None]



''' Attempt to define scripting API that can also be used by 
SimulatorResultsDialog.

1 create experiment
~ load/edit/save parameters
2 perform experiment, get results
3 select subset of results
4 get timeseries/histograms/surfaces
~ get more timeseries/histograms/surfaces
5 plot/edit some timeseries/histograms/surfaces
6 save plots

'''

file_name = 'filename.params'
mcss_experiment = McssExperiment(file_name=file_name) # load parameters from .params file
#mcss_experiment.load(file_name) # load parameters from .params file
mcss_experiment.max_time = 200 # set parameter
mcss_experiment.save(file_name) # save_parameters to .params files
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
    


    def select(self, **selection):
        ''' Select items without resetting selection and return updated 
        selection. '''
        self.trait_set(**selection) # trait_set doesn't use metadata
        return self.selection
        
  