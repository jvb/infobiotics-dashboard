class Results(object):
    ''' A multi-dimensional array containing many timeseries. '''
    [run_indices]
    [species_indices]
    compartment_indices
    timepoints

class Timeseries(object):
    ''' A one-dimensional array containing amounts/concentrations/volumes. '''
    timepoints
    levels
    title
    label
    

class Plot(object):
    ''' Contains a figure with one or many lines. '''
    figure
    lines
    title
    def combined(self): 
        ''' Returns '''
        
    def stacked(self): pass
    def tiled(self): pass

class StackedPlot(Plot):
    ''' Contains a figure with '''
        

class Figure(object):
    ''' Contains one or more subplots. '''
    title
    subplots
    legend

class SubPlot(object):
    ''' A plot within a figure that has a set of axes. '''
    title
    axes
    legend

class Line(object):
    ''' Visual representation of a timeseries or its error bars in a figure. '''
    x = timepoints
    y = levels

class Legend(object):
    ''' A legend in a subplot: axes.legend(); or a figure: figure.legend(). '''


class Plot(object):
    
    def __init__(self, timeseries=[]):
        self.figure = Figure()
        self.timeseries = timeseries
        self.lines = [self.line(timeseries) for timeseries in self.timeseries]
    
    def line(self, timeseries):
        pass
            
    
