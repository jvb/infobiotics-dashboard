from enthought.traits.api import HasTraits, Float, Instance, List, Property
from commons.traits.float_greater_than_zero import FloatGreaterThanZero
from mcss_results_attributes import McssResultsAttributes 

ParamsProgramName = Enum(['mcss','pmodelchecker','poptimizer']) 


class Experiment(HasTraits):
    ''' Dummy class showing perform() returning a Results object. '''
    _params_program_name = ParamsProgramName 
            
    def perform(self):
        return Results()


class Results(HasTraits):
    _params_program_name = ParamsProgramName 


class Species(HasTraits):
    pass

class Compartment(HasTraits):
    pass

class McssResults(HasTraits):
    _params_program_name = 'mcss' 
    attributes = Instance(McssResultsAttributes)
    species = List(Species)
    compartments = List(Compartment)
    timepoints = Property(depends_on='attributes.log_interval, attributes.max_time', cached=True)
    
    def _get_timepoints(self):
        return range(0, attributes.max_time, attributes.log_interval)
    
    def timeseries(self):
        return Timeseries(
            timepoints=self.timepoints,
        )




    
    
    
    

class PlotData(HasTraits):
    pass


class TimedPlotData(PlotData):
    timepoints = List(Float)
    max_time = Property(Float, depends_on='timepoints')
    min_time = Property(Float, depends_on='timepoints')

    def _get_max_time(self):
        return self.timepoints[-1]

    def _get_min_time(self):
        return self.timepoints[0]


class Plot(HasTraits):
    data = Instance(PlotData)
    
    def save(self, filename, format):
        print 'saving'

    
class PlotHandler(Handler):
    
    def save(self, info):
        print 'prompting for filename'
        info.object.save(filename, format)


class TimedPlot(Plot):
    data = Instance(TimedPlotData)
    
    time_max = FloatGreaterThanZero


class Timeseries(TimedPlot):
    ''' Plot of molecules over time for some species in some compartments,
    possibly averaged.
    '''
    pass
    

class Distribution(PlotData):
    pass     

class TimedDistribution(TimedPlotData):
    pass




class Histogram(TimedPlot):
    ''' Distribution of quantities of a species over many compartments
    or
    distribution of quantities of a species in one compartment over time
    or
    distribution of quantities of a species in many compartments over time
    '''
    pass




def test_timeseries():

    results = McssResults()
    timeseries = results.timeseries()
    
    print timeseries.molecules_max
    timeseries.time_max = 1000


def test_api():
    '''
    results.data().plot().attribute
    
    results = mcss.h5 or pmodelchecker.psm or poptimizer.stdout
    
    data (mcss.h5) = 'amounts' of species in compartments at time, or reactions, volumes
    data (pmodelchecker.psm) = 'Result' for each permutation of variables
    data (poptimizer.stdout) = 'Fitness' for each model at generation  
    
    '''
    results = experiment.perform()
    


if __name__ == '__main__':
    pass

#    test_timeseries()
    