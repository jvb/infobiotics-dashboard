from __future__ import division # essential for _get_colour
from enthought.traits.api import HasTraits, Float, Str, Color, Enum, Property, \
    cached_property, Array, Instance, Tuple, Bool, List, Int, Any
from enthought.traits.ui.api import View, HGroup, Item

class Timeseries(HasTraits): #TODO factor out traits into TraitTimeseries and have McssResults produce 'timeseries' objects

    def __init__(self, **traits):
        self.timepoints = traits.pop('timepoints')[:] # copy timepoints
        HasTraits.__init__(self, **traits)

    run_numbers = Any # list or xrange if all
    num_runs = Property(Int, depends_on='run_numbers')
    @cached_property
    def _get_num_runs(self):
        return len(self.run_numbers)
    

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

    # calculated in McssResults.timeseries
    short_title = Str
    long_title = Str
    plot_title = Str # used by TimeseriesPlot to discover whether timeseries from multiple data sets are being plotted 

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
