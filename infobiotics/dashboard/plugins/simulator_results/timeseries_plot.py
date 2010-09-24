from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Instance, Str, List, Float, Bool, Button, on_trait_change, Tuple, Dict, Array, Enum
from timeseries import Timeseries 
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MatplotlibFigureEditor
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from infobiotics.commons import colours
from enthought.traits.ui.api import View, VGroup, Item, HGroup, Spring, ListEditor, InstanceEditor
from infobiotics.commons.matplotlib.draggable_legend import DraggableLegend
from infobiotics.commons.matplotlib.matplotlib_figure_size import resize_and_save_matplotlib_figure

class TimeseriesPlot(HasTraits):
    font_properties = FontProperties(size='medium')#'small'
    
    figure = Instance(Figure, ())
    title = Str('title')
    timepoints = Array
    timeseries = List(Timeseries)

    list_widget = Button
    def _list_widget_fired(self):
        from PyQt4.QtGui import QListWidget, QListView, QAbstractItemView, QListWidgetItem, QIcon
        from PyQt4.QtCore import QSize
        list_widget = QListWidget()
        list_widget.setViewMode(QListView.IconMode) # list_widget.setViewMode(QListView.ListMode)
        list_widget.setAcceptDrops(False)
        list_widget.setFlow(QListWidget.LeftToRight)
        list_widget.setWrapping(True)
        list_widget.setResizeMode(QListView.Adjust)
        list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        size = 150
        list_widget.setWordWrap(False)
        list_widget.setUniformItemSizes(True)
        list_widget.setIconSize(QSize(size, size))
        list_widget.setGridSize(QSize(size - 1, size - 1)) # hides label
#        list_widget.hideInvariants = True #TODO
        for timeseries in self.timeseries:
            QListWidgetItem(QIcon(timeseries.pixmap()), timeseries.title, list_widget)
        self._list_widget = list_widget # must keep reference to list_widget or it gets destroyed when method returns 
        self._list_widget.show()
    
    save_resized = Button

    def _save_resized_fired(self):
        resize_and_save_matplotlib_figure(self.figure)
        

    show_individual_legends = Bool(False)
    
    def _show_individual_legends_changed(self):
        if self.show_individual_legends:
            self._create_individual_legends()
        else:
            for timeseries, line in self.timeseries_to_line_map.iteritems():
                legend = line.axes.get_legend()
                if legend is not None: 
                    legend.set_visible(False)
        self._redraw_figure()
    
    def _create_individual_legends(self):        
        for timeseries, line in self.timeseries_to_line_map.iteritems():
            DraggableLegend(line.axes.legend(loc='best', prop=self.font_properties))
        
    
    show_figure_legend = Bool(False)
    
    def _show_figure_legend_changed(self):
        if self.show_figure_legend:
            if hasattr(self, 'figure_legend'):
                self.figure_legend.set_visible(True)
            else:
                if self.figure.canvas is not None:
                    self.figure_legend = DraggableLegend(self._create_figure_legend())
                else:
                    self.figure_legend = self._create_figure_legend()
        else:
            if hasattr(self, 'figure_legend'):
                self.figure_legend.set_visible(False)
                del self.figure_legend
#            self.figure_legend.remove() # planned but not implemented in 0.99.0
        self._redraw_figure()

    def _create_figure_legend(self):
#        lines = [line for line, label in self.lines]
#        labels = [label for line, label in self.lines]
        lines = []
        labels = []
#        print len(self.timeseries_to_line_map)
        for timeseries, line in self.timeseries_to_line_map.iteritems():
            lines.append(line)
            labels.append(timeseries.title)
        return self.figure.legend(
            lines,
            labels,
            loc='lower center', # http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure.legend 
            prop=self.font_properties
        ) 


#    style = Enum(['Combined', 'Stacked', 'Tiled'])
#    style = Enum(['Stacked', 'Combined', 'Tiled'])
    style = Enum(['Tiled', 'Stacked', 'Combined'])
    
    show_gridlines = Bool(True)

    show_volumes_separately = Bool
    
    @on_trait_change('style, timeseries, show_gridlines, show_volumes_separately')
    def _update_figure(self):
#        self.timeseries_to_line_map.clear()
        self.figure.clear()
#        adjustprops = dict(left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
#        self.figure.subplots_adjust(**adjustprops)
        
        if self.style == 'Combined':
            self.combine()
        elif self.style == 'Stacked':
            self.stack()
        elif self.style == 'Tiled':
            self.tile()

        self.figure.set_facecolor('white')
        
        self._show_figure_legend_changed()
        self._show_individual_legends_changed()
        
        self._redraw_figure()

    some_volumes = Bool
    
    def _timeseries_changed(self):
        # determine if some volumes but not (no volumes or all volumes)
        volumes = 0
        for timeseries in self.timeseries:
            if timeseries.species.name == 'Volumes':
                volumes += 1
        if 0 < volumes < len(self.timeseries):
            self.some_volumes = True
        else:
            self.some_volumes = False
        if self.some_volumes:
            self.not_volumes = [timeseries for timeseries in self.timeseries if timeseries.species.name != 'Volumes']
            self.volumes = [timeseries for timeseries in self.timeseries if timeseries.species.name == 'Volumes']
        
    def combine(self):
        if self.some_volumes: # plot species on left y-axis and volumes on right y-axis
            axes = self._create_axes(self.not_volumes[0].xlabel, self.not_volumes[0].ylabel, 111)
            for timeseries in self.not_volumes:
                self._plot_timeseries(axes, timeseries)
            axes = self._create_axes_twinx(axes, self.volumes[0].ylabel)
            for timeseries in self.volumes:
                self._plot_timeseries(axes, timeseries)
        else:
            axes = self._create_axes(self.timeseries[0].xlabel, self.timeseries[0].ylabel, 111)
            for timeseries in self.timeseries:
                self._plot_timeseries(axes, timeseries)
        adjustprops = dict(left=0.1, bottom=0.15, right=0.9, top=0.85, wspace=0.2, hspace=0.2)
        self.figure.subplots_adjust(**adjustprops)
             

    def _create_axes(self, xlabel, ylabel, *args, **kwargs):
        axes = self.figure.add_subplot(*args, **kwargs) # works for 111, (1, 1, 1) and sharex=axes
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        if self.show_gridlines:
            axes.grid(True, which='major')
            axes.grid(True, which='minor')
        return axes
    
    def _create_axes_twinx(self, axes, ylabel):
        axes = axes.twinx()
        axes.set_ylabel(ylabel)
#        if self.show_gridlines:
#            axes.grid(True, which='major')
#            axes.grid(True, which='minor')
        return axes

    def _plot_timeseries(self, axes, timeseries):
        self._plot_line(axes, timeseries)
#        if self.averaging: #TODO
#            self._plot_errorbars(axes, timeseries)

    def stack(self):
        if len(self.timeseries) == 1:
            self.combine()
            return
        rows = len(self.timeseries)
        cols = 1
        for i, timeseries in enumerate(reversed(self.timeseries)):
            if i == 0:
                axes = self._create_axes(timeseries.xlabel, timeseries.ylabel, rows, cols, rows)
                shared_axes = axes
            else:
                axes = self._create_axes('', timeseries.ylabel, rows, cols, rows - i, sharex=shared_axes)
                for label in axes.get_xticklabels():
                    label.set_visible(False)
            self._plot_timeseries(axes, timeseries)
            if not self.some_volumes:
                axes.set_ylabel('')
        if not self.some_volumes:
            self.figure.text(0.02, 0.5, self.timeseries[0].ylabel, rotation=90, ha='center', va='center')
        adjustprops = dict(left=0.1, bottom=0.15, right=0.97, top=0.85, wspace=0.2, hspace=0.2)
        self.figure.subplots_adjust(**adjustprops)
    
    def tile(self):
        if len(self.timeseries) == 1:
            self.combine()
            return
        elif len(self.timeseries) == 2:
            self.stack()
            return
        rows, cols = arrange(len(self.timeseries))
        for i, timeseries in enumerate(self.timeseries):
#            axes = self._create_axes(timeseries.xlabel, timeseries.ylabel, rows, cols, i + 1)
#            self._plot_line(axes, timeseries)
#            if i + 1 < len(self.timeseries) - (cols - 1):
#                for label in axes.get_xticklabels():
#                    label.set_visible(False)
#                axes.set_xlabel('')
            axes = self._create_axes('', timeseries.ylabel, rows, cols, i + 1)
            self._plot_line(axes, timeseries)
            if i + 1 < len(self.timeseries) - (cols - 1):
                for label in axes.get_xticklabels():
                    label.set_visible(False)
            if not self.some_volumes:
                axes.set_ylabel('')
        self.figure.text(0.5, 0.02, self.timeseries[0].xlabel, ha='center')#, va='center')
        if not self.some_volumes:
            self.figure.text(0.02, 0.5, self.timeseries[0].ylabel, rotation=90, ha='center', va='center')
        adjustprops = dict(left=0.1, bottom=0.15, right=0.97, top=0.85, wspace=0.35, hspace=0.25)
        self.figure.subplots_adjust(**adjustprops)



#    lines = List(Tuple(Line2D, Str))
    timeseries_to_line_map = Dict(Timeseries, Line2D)

    def _plot_line(self, axes, timeseries):
        print timeseries.colour
        lines = axes.plot(
            timeseries.timepoints, #self.timepoints, #TODO change range here?
            timeseries.values,
            label=timeseries.title,
            color=timeseries.colour,
        )
        line = lines[0]
#        print line
#        self.lines.append((line, timeseries.label))
        self.timeseries_to_line_map[timeseries] = line

    def _plot_errorbars(self, axes, timeseries): #TODO
        raise NotImplementedError

    @on_trait_change('timeseries:_colour')
    def _update_line_color(self, timeseries, _, old, new):
        line = self.timeseries_to_line_map[timeseries]
        line.set_color(timeseries.colour)
        self._redraw_figure()

    def _redraw_figure(self):
        if self.figure.canvas is not None:
            self.figure.canvas.draw()

    
    def traits_view(self):
        return View(
            VGroup(
                Item('timeseries',
                    style='readonly',
                    editor=ListEditor(
                        style='custom',
                        editor=InstanceEditor(),
                    ),
                ),
                Item('style', style='custom'),
                HGroup(
                    Item('figure',
                        editor=MatplotlibFigureEditor(
                            toolbar=True,
                            toolbar_above=False,
                        ),
                        show_label=False,
                    ),
                ),
                HGroup(
                    Item('show_volumes_separately', visible_when='object.some_volumes'),
                    'show_gridlines',
                    'show_individual_legends',
                    'show_figure_legend',
                    Spring(),
                ),
                HGroup(
                    Item('save_resized'),
                    Item('list_widget', label='Edit timeseries...'),
                    show_labels=False,
                ),
                show_border=True,
                show_labels=False,
            ),
            width=640, height=480,
            resizable=True,
            title=self.title,
        )

#    def configure_traits(self, *args, **kwargs):
##        self._update_figure() #TODO add via do_later via timer 
#        super(TimeseriesPlot, self).configure_traits(*args, **kwargs)
        
def arrange(number):
    ''' Returns the smallest rows x columns tuple for a given number of items.
    
    Adapted from Pawel's tiling code.
    
    '''
    import math
    rows = math.sqrt(number / math.sqrt(2))
    cols = rows * math.sqrt(2)
    if number <= math.ceil(rows) * math.floor(cols):
        rows = int(math.ceil(rows))
        cols = int(math.floor(cols))
    elif number <= math.floor(rows) * math.ceil(cols):
        rows = int(math.floor(rows))
        cols = int(math.ceil(cols))
    else:
        rows = int(math.ceil(rows))
        cols = int(math.ceil(cols))
    return (rows, cols)


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
    from simulator_results import Run, Species, Compartment
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
    molecules = Timeseries(
        run=run,
        species=species,
        compartment=compartment,
        timepoints=timepoints,
        values=np.sin(np.arange(number_of_timepoints)),
        values_type='Molecules',
        _colour=colours.colour(0),
    )
    concentration = Timeseries(
        run=run,
        species=species,
        compartment=compartment,
        timepoints=timepoints,
        values=np.cos(np.arange(number_of_timepoints)),
        values_type='Concentration',
        _colour=colours.colour(1),
    )
    volume = Timeseries(
        run=run,
        species=volumes_species,
        compartment=compartment,
        timepoints=timepoints,
        values=np.tan(np.arange(number_of_timepoints)),
        values_type='Volume',
        _colour=colours.colour(2),
    )
    timeseries = [
        molecules,
        concentration,
        volume,
        molecules,
    ]
#    volume.colour = (0.2, 0, 0.7)
    TimeseriesPlot(
        timepoints=timepoints,
        timeseries=timeseries,
        title='titular',
    ).configure_traits()


def multiple_subplots_with_one_axis_label():
    import pylab

    figprops = dict(figsize=(8., 8. / 1.618), dpi=128)                                          # Figure properties
    adjustprops = dict(left=0.1, bottom=0.1, right=0.97, top=0.93, wspace=0.2, hspace=0.2)       # Subplot properties
    
    fig = pylab.figure(**figprops)                                                              # New figure
    fig.subplots_adjust(**adjustprops)                                                          # Tunes the subplot layout
    
    ax = fig.add_subplot(3, 1, 1)
    bx = fig.add_subplot(3, 1, 2, sharex=ax, sharey=ax)
    cx = fig.add_subplot(3, 1, 3, sharex=ax, sharey=ax)
    
    ax.plot([0, 1, 2], [2, 3, 4], 'k-')
    bx.plot([0, 1, 2], [2, 3, 4], 'k-')
    cx.plot([0, 1, 2], [2, 3, 4], 'k-')
    
    pylab.setp(ax.get_xticklabels(), visible=False)
    pylab.setp(bx.get_xticklabels(), visible=False)
    
    bx.set_ylabel('This is a long label shared among more axes', fontsize=14)
    cx.set_xlabel('And a shared x label', fontsize=14)

    fig.show()

if __name__ == '__main__':
#    multiple_subplots_with_one_axis_label()
    main()
