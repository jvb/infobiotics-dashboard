from __future__ import division # essential for _get_colour
from enthought.traits.api import HasTraits, Float, Str, Color, Enum, Property, \
    cached_property, Array, Instance, Tuple, Bool, List
from run import Run
from species import Species
from compartment import Compartment

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import StringIO
from PyQt4.QtGui import QPixmap#, QColor
from enthought.traits.ui.api import View, HGroup, Item

class Timeseries(HasTraits):

    std = Array(desc='the standard deviations of the timeseries values')

    runs = List(Run)
    run = Instance(Run)
    species = Instance(Species) # None == Volume
    compartment = Instance(Compartment)

    timepoints = Array
    timepoints_units = Str
    
    values_type = Enum(['Amount', 'Concentration', 'Volume'])
    values = Array
    values_units = Str
    
    abbreviated_units = Bool(True)

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


#    title = Property(Str, depends_on='values_type, run, species, compartment')
    title = Str

    def _title_default(self):
        return self._get_title()
    
#    @cached_property
    def _get_title(self):
        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
        if self.values_type == 'Volume':
            if self.run == None:
                return 'Volume of %s' % (compartment_name_and_xy_coords)
#                return '%s' % (compartment_name_and_xy_coords)
            else:
                return 'Volume of %s in run %s' % (compartment_name_and_xy_coords, self.run._run_number)
#                return '%s in run %s' % (compartment_name_and_xy_coords, self.run._run_number)
        else:
            if self.run == None:
                return '%s of %s in %s' % (self.values_type, self.species.name, compartment_name_and_xy_coords)
#                return '%s in %s' % (self.species.name, compartment_name_and_xy_coords)
            else:
                return '%s of %s in %s of run %s' % (self.values_type, self.species.name, compartment_name_and_xy_coords, self.run._run_number)
#                return '%s in %s of run %s' % (self.species.name, compartment_name_and_xy_coords, self.run._run_number)
    
    
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


    def pixmap(self, width=4, height=4, dpi=100):
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

    view = View(
        HGroup(
            Item('title'),
            Item('_colour'),
            Item('timepoints_units'),
            Item('values_units'),
            show_labels=False,
        ),
    )


if __name__ == '__main__':
    execfile('timeseries_plot.py')
