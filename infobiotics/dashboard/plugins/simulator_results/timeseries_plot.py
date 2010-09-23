from __future__ import division
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Instance, Str, List, Float, Bool, Button, on_trait_change, Tuple
from enthought.traits.ui.api import View, VGroup, Item, HGroup, Spring, ListEditor, InstanceEditor
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MatplotlibFigureEditor
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from enthought.traits.api import HasTraits, List, Float, Str, Color, Enum, Property, cached_property, Array
from simulator_results import Run, Species, Compartment
from infobiotics.commons.traits.int_greater_than_zero import IntGreaterThanZero
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import StringIO
from PyQt4.QtGui import QPixmap

from infobiotics.commons import colours

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

class TimeseriesPlot(HasTraits):
    figure = Instance(Figure, ())
    title = Str('title')
    timepoints = Array
    timeseries = List(Timeseries)

#    list_widget = Button
#    def _list_widget_fired(self):
#        from PyQt4.QtGui import QListWidget, QListView, QAbstractItemView, QListWidgetItem, QIcon
#        from PyQt4.QtCore import QSize
#        list_widget = QListWidget()
#        list_widget.setViewMode(QListView.IconMode)
#        list_widget.setAcceptDrops(False)
#        list_widget.setFlow(QListWidget.LeftToRight)
#        list_widget.setWrapping(True)
#        list_widget.setResizeMode(QListView.Adjust)
#        list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
#        size = 150
#        list_widget.setWordWrap(False)
#        list_widget.setUniformItemSizes(True)
#        list_widget.setIconSize(QSize(size, size))
#        list_widget.setGridSize(QSize(size, size)) # hides label
##        list_widget.hideInvariants = True #TODO
#        for timeseries in self.timeseries:
#            QListWidgetItem(QIcon(timeseries.pixmap()), timeseries.label, list_widget)
##            QListWidgetItem(QIcon(timeseries.pixmap()), '', list_widget)
#        self._list_widget = list_widget # must keep reference to list_widget or it gets destroyed when method returns 
#        self._list_widget.show()
    
    save_resized = Button

    def _save_resized_fired(self):
#        resize_and_save_matplotlib_figure(self.figure)
        self.figure.clear()

    show_individual_legends = Bool
    show_figure_legend = Bool
    
    def _show_figure_legend_changed(self, value):
        if value:
            lines = [line for line, _ in self.lines]
            labels = [label for _, label in self.lines]
            legend = self.figure.legend(lines, labels, loc='right')#TODO, prop=self.fontManager)
        else:
            self.figure.legend_ = None

    style = Enum(['Combined', 'Stacked', 'Tiled'])
    
    @on_trait_change('style, timeseries._colour')
    def update_figure(self):
        self.figure.clear()
#        return
        if self.style == 'Combined':
            self.combine()
        elif self.style == 'Stacked':
            self.stack()
        elif self.style == 'Tiled':
            self.tile()

    lines = List(Tuple(Line2D, Str))

    def line(self, axes, timeseries, colour=None):
        print timeseries.colour
        lines = axes.plot(
            timeseries.timepoints, #self.timepoints, #TODO change range here?
            timeseries.values,
            label=timeseries.label,
            color=colour if colour is not None else timeseries.colour,
        )
        self.lines.append((lines[0], timeseries.label))
    
    def combine(self):
        print 'combine'
        
        # determine if some volumes but not (no volumes or all volumes)
        volumes = 0
        for timeseries in self.timeseries:
            if timeseries.species.name == 'Volumes':
                volumes += 1
        if 0 < volumes < len(self.timeseries):
            some_volumes = True
        else:
            some_volumes = False

        self.axes = self.figure.add_subplot(111)
        if not some_volumes: # either all volumes or no volumes
            # plot all on 1st y-axis
            self.axes.set_xlabel(timeseries[0].xlabel)
            self.axes.set_ylabel(timeseries[0].ylabel)
            for i, timeseries in enumerate(self.timeseries):
                colour = colours.colour(i)
#                colour = timeseries.colour
                self.line(self.axes, timeseries)#, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
        else:
            # mix, plot species on 1st y-axis and volumes on 2nd y-axis
            not_volumes = [timeseries for timeseries in self.timeseries if timeseries.species.name != 'Volumes']
            volumes = [timeseries for timeseries in self.timeseries if timeseries.species.name == 'Volumes']
            self.axes.set_xlabel(not_volumes[0].xlabel)
            self.axes.set_ylabel(not_volumes[0].ylabel)
            for i, timeseries in enumerate(not_volumes):
                colour = colours.colour(i)
                self.line(self.axes, timeseries)#, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
            axes = self.axes.twinx()
            axes.set_ylabel(volumes[0].ylabel)
            for i, timeseries in enumerate(volumes):
                i += len(not_volumes) #TODO don't need simulation after all, unless we want consistent colours for all species
                colour = colours.colour(i)
                self.line(axes, timeseries)#, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
            
        self.finalise()        
    
    def finalise(self):
        self.figure.set_facecolor('white')
    
    def stack(self):
        print 'stack'
    
    def tile(self):
        print 'tile'
    
    def traits_view(self):
        return View(
            VGroup(
                Item('style', style='custom'),
                Item('timeseries',
                    style='readonly',
                    editor=ListEditor(
                        style='custom',
                        editor=InstanceEditor(),
                    ),
                ),
#                Item('list_widget'),
                HGroup(
                    Item('figure',
                        editor=MatplotlibFigureEditor(
                            toolbar=True
                        ),
                        show_label=False,
                    ),
                ),
                HGroup(
                    'show_individual_legends',
                    'show_figure_legend',
                    Spring(),
                    Item('save_resized'),
                ),
                show_border=True,
                show_labels=False,
            ),
            width=640, height=480,
            resizable=True,
            title=self.title
        )


def main():
    number_of_timepoints = 100
    class Simulation(object):
        pass
    simulation = Simulation()
    simulation.number_of_species = 1 #TODO use for colouring: volumes = number + compartment index
    class Attributes(object):
        pass
    attributes = Attributes()
    attributes.number_of_compartments = 1
    attributes.number_of_timepoints = number_of_timepoints
    attributes.simulated_time = 100
    run = Run(
        attributes=attributes,
        run_number=1,
        simulation=simulation,
    )
    species = Species(
        index=0,
        name='A',
        simulation=simulation,
    )
    volumes_species = Species(
        index=None, #TODO
        name='Volumes',
        simulation=simulation,
    )
    compartment = Compartment(
        index=0,
        id=0,
        name='::::',
        x_position=0,
        y_position=0,
        template_index=0,
        run=run,
        simulation=simulation,
    )
    import numpy as np
    timepoints = np.arange(number_of_timepoints)
    timeseries = [
        Timeseries(
            run=run,
            species=species,
            compartment=compartment,
            timepoints=timepoints,
            values=np.sin(np.arange(number_of_timepoints)),
            values_type='Molecules',
            _colour=colours.colour(0),
        ),
        Timeseries(
            run=run,
            species=species,
            compartment=compartment,
            timepoints=timepoints,
            values=np.cos(np.arange(number_of_timepoints)),
            values_type='Concentration',
            _colour=colours.colour(1),
        ),
        Timeseries(
            run=run,
            species=volumes_species,
            compartment=compartment,
            timepoints=timepoints,
            values=np.tan(np.arange(number_of_timepoints)),
            values_type='Volume',
            _colour=colours.colour(2),
        ),
    ]
    TimeseriesPlot(
        timepoints=timepoints,
        timeseries=timeseries,
        title='titular',
    ).configure_traits()


if __name__ == '__main__':
    main()
