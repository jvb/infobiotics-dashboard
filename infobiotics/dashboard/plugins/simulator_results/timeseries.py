from enthought.traits.api import HasTraits, List, Float, Str, Color, Enum, Property, cached_property, Array, Instance, Tuple
from simulator_results import Run, Species, Compartment
from infobiotics.commons.traits.int_greater_than_zero import IntGreaterThanZero
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import StringIO
from PyQt4.QtGui import QPixmap
from enthought.traits.ui.api import View, HGroup, Item

class Timeseries(HasTraits):

    species = Instance(Species) # None == Volume?
    compartment = Instance(Compartment)
    run = Instance(Run)
    
    timepoints = Array
    timepoints_units = Str
    
    values = Array
    values_type = Enum(['Molecules', 'Concentration', 'Volume'])
    values_units = Str

    label = Property(Str)
    
    @cached_property
    def _get_label(self, depends_on='values_type, run, species, compartment'):
        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
        if self.values_type == 'Volume':
            if self.run == None:
                return 'Volume of %s' % (compartment_name_and_xy_coords)
            else:
                return 'Volume of %s in run %s' % (compartment_name_and_xy_coords, self.run._run_number)
        else:
            if self.run == None:
                return '%s of %s in %s' % (self.values_type, self.species.name, compartment_name_and_xy_coords)
            else:
                return '%s of %s in %s of run %s' % (self.values_type, self.species.name, compartment_name_and_xy_coords, self.run._run_number)

    xlabel = Property(Str, depends_on='timepoints_units')
    
    @cached_property
    def _get_xlabel(self):
        label = 'Time'
        if self.timepoints_units != '':
            label += ' (%s)' % self.timepoints_units
        return label

    ylabel = Property(Str, depends_on='values_type, values_units')
    
    @cached_property
    def _get_ylabel(self):
        label = self.values_type
        if self.values_units != '':
            label += ' (%s)' % self.values_units
        return label

    _colour = Color
    
    colour = Property(Tuple(Float, Float, Float), depends_on='_colour')

    @cached_property
    def _get_colour(self):
        return (self._colour.red() / 255, self._colour.green() / 255, self._colour.blue() / 255)

    def pixmap(self, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        canvas = FigureCanvasAgg(fig) # needed for savefig below
        ax = fig.add_subplot(111)
        ax.plot(self.timepoints, self.values, color=self.colour, label=self.label)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.label)
        file_like_object = StringIO.StringIO()
        fig.savefig(file_like_object, format='png')
        pixmap = QPixmap()
        pixmap.loadFromData(file_like_object.getvalue(), 'PNG')
        file_like_object.close()
        return pixmap

    view = View(
        HGroup(
            Item('label', style='readonly'),
            Item('_colour'),
            show_labels=False,
        ),
    )
