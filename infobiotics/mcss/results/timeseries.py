from __future__ import division # essential for _get_colour
from traits.api import HasTraits, Float, Str, Color, Enum, Property, \
    cached_property, Array, Instance, Tuple, Bool, List, Int, Any
from traitsui.api import View, HGroup, Item

class Timeseries(HasTraits): #TODO factor out traits into TraitTimeseries and have McssResults produce 'timeseries' objects

    def __init__(self, **traits):
        self.timepoints = traits.pop('timepoints')[:] # copy timepoints
        HasTraits.__init__(self, **traits)

    timepoints = Array
    values = Array
    std = Array(desc='the standard deviations of the timeseries values')
    
    values_type = Enum(['Volume', 'Amount', 'Concentration'])
#    def _values_type_default(self):
#        raise ValueError('values_type must be specified when Timeseries initialised')
    # called erroneously by HasTraits.__init__ even when values_type is in traits
    
    timepoints_units = Str
    values_units = Str
    abbreviated_units = Bool(False)

    run_numbers = Any # list or xrange if all
    num_runs = Property(Int, depends_on='run_numbers')
    @cached_property
    def _get_num_runs(self):
        return len(self.run_numbers)
    
    species = Str
    compartment = Str

    runs_summary = Str
    species_summary = Str
    compartments_summary = Str

    # calculated in McssResults.timeseries
    plot_title = Str # used by TimeseriesPlot to discover whether timeseries from multiple data sets are being plotted 

#    short_title = Str
    short_title = Property(Str, depends_on='species')
    @cached_property
    def _get_short_title(self):
        title = str(self.species) 
        if title == self.species_summary:
            return ''
        else:
            return title if self.species else 'Volume'
                
#    long_title = Str
    long_title = Property(Str, depends_on='run, species, compartment')
    @cached_property
    def _get_long_title(self):
        '''Needed when short title would be ambiguous, i.e. same species 
        name in different simulations when different numbers of runs'''
        title = self.short_title#str(self.species) if self.species else 'Volume'#short_title(species) 
        if self.compartments_summary:
            if self.compartments_summary not in self.plot_title:
                if title:
                    title += ' in '
                title += '%s' % self.compartments_summary
        else:
            if title:
                title += ' in '
            title += '%s' % str(self.compartment)
        if self.runs_summary and self.runs_summary not in self.plot_title:
            runs = self.runs_summary if self.num_runs > 1 else 'run %s' % self.run_numbers[0]
            if title:
                title += ' (%s)' % runs
            else:
                title += runs  
        return title

    filename = Str #TODO use in TimeseriesPlot when multiple data sets used 
    
    xlabel = Property(Str, depends_on='timepoints, abbreviated_units, timepoints_units')
    @cached_property
    def _get_xlabel(self):
        label = 'Time'
        timepoints_units = str(self.timepoints.dimensionality) if self.abbreviated_units and hasattr(self.timepoints, 'dimensionality') else self.timepoints_units
        if timepoints_units != '':
            label += ' (%s)' % timepoints_units
        return label
    
    
    ylabel = Property(Str, depends_on='values, values_type, abbreviated_units, values_units')
    @cached_property
    def _get_ylabel(self):
        label = self.values_type
        values_units = str(self.values.dimensionality) if self.abbreviated_units and hasattr(self.values, 'dimensionality') else self.values_units
        if values_units != '':
            label += ' (%s)' % values_units
        return label    
    
    
    _colour = Color
    colour = Property(Tuple(Float, Float, Float), depends_on='_colour')    
    @cached_property
    def _get_colour(self):
        return (self._colour.red() / 255, self._colour.green() / 255, self._colour.blue() / 255)

#    def _set_colour(self, value):
#        ''' value is a tuple (red, green, blue) where red/green/blue must be 0 <= float <= 1. '''
#        red, green, blue = value
#        return QColor(int(red * 256), int(green * 255), int(blue * 255))

    marker = Str


    view = View(
        HGroup(
            Item('title'),
            Item('_colour'),
            Item('timepoints_units'),
            Item('values_units'),
#            Item('filename', label='Simulation'), #TODO allow user to override this 
            show_labels=False,
        ),
    )


    def pixmap(self, width=4, height=4, dpi=100):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        import StringIO
        from PyQt4.QtGui import QPixmap#, QColor
        fig = Figure(figsize=(width, height), dpi=dpi)
        canvas = FigureCanvasAgg(fig) # needed for savefig below
        ax = fig.add_subplot(111)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.plot(self.timepoints, self.values, color=self.colour, label=self.title)
        file_like_object = StringIO.StringIO()
        fig.savefig(file_like_object, format='png')
        pixmap = QPixmap()
        pixmap.loadFromData(file_like_object.getvalue(), 'PNG')
        file_like_object.close()
        return pixmap


if __name__ == '__main__':
    execfile('timeseries_plot.py')
