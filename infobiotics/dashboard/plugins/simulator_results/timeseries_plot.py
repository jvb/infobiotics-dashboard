from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import (HasTraits, Instance, Str, List, Float, Bool,
    Button, on_trait_change, Tuple, Dict, Array, Enum, Property,
    cached_property)
from enthought.traits.ui.api import (View, VGroup, Item, HGroup, Spring,
    ListEditor, InstanceEditor)
from infobiotics.commons import colours
from infobiotics.commons.matplotlib.draggable_legend import DraggableLegend
from infobiotics.commons.matplotlib.matplotlib_figure_size import (
    resize_and_save_matplotlib_figure)
from infobiotics.commons.sequences import arrange
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import (
    MatplotlibFigureEditor)
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from timeseries import Timeseries

class TimeseriesPlot(HasTraits):

    #traits
    
    title = Str('title')

    figure = Instance(Figure, ())
    timepoints = Array
    timeseries = List(Timeseries)

    some_volumes = Property(Bool, depends_on='timeseries')
    volumes = Property(List(Timeseries), depends_on='timeseries')
    amounts = Property(List(Timeseries), depends_on='timeseries')

#    style = Enum(['Combined', 'Stacked', 'Tiled'])
#    style = Enum(['Stacked', 'Combined', 'Tiled'])
    style = Enum(['Tiled', 'Stacked', 'Combined'])
    
    show_gridlines = Bool(True)

    show_figure_legend = Bool(False)
    show_individual_legends = Bool(False)    

    show_volumes_separately = Bool
    
    show_individual_volume_labels = Bool
    show_individual_amounts_labels = Bool
    show_individual_time_labels = Bool


    # class attributes (not traits!)

    font_properties = FontProperties(size='medium')#'small'

    
    @cached_property
    def _get_volumes(self):
        return [timeseries for timeseries in self.timeseries if timeseries.species.name == 'Volumes']
    
    @cached_property
    def _get_amounts(self):
        return [timeseries for timeseries in self.timeseries if timeseries.species.name != 'Volumes']
    
    @cached_property
    def _get_some_volumes(self):
        # determine if some volumes but not (no volumes or all volumes)
#        volumes = 0
#        for timeseries in self.timeseries:
#            if timeseries.species.name == 'Volumes':
#                volumes += 1
#        if 0 < len(self.volumes) < len(self.timeseries):
#            some_volumes = True
#        else:
#            some_volumes = False
#        if some_volumes:
#            self.volumes = [timeseries for timeseries in self.timeseries if timeseries.species.name == 'Volumes']
#            self.amounts = [timeseries for timeseries in self.timeseries if timeseries.species.name != 'Volumes']
#        return some_volumes
        if 0 < len(self.volumes) < len(self.timeseries):
            return True
        else:
            return False

    @on_trait_change('style, show_individual_legends')
    def _change_individual_legends_visibility(self):
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
        
    
    @on_trait_change('style, show_figure_legend')
    def _change_figure_legend_visibility(self):
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
    
    
    @on_trait_change('style, \
        timeseries, \
        timeseries:_colour, \
        show_gridlines, \
        show_volumes_separately, \
        show_individual_volume_labels, \
        show_individual_amounts_labels, \
        show_individual_time_labels')
    def _update_figure(self):

#        self.timeseries_to_line_map.clear()

        self.figure.clear()
        
#        adjustprops = dict(left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)
#        self.figure.subplots_adjust(**adjustprops)
        
        if not self.show_individual_volume_labels and self.some_volumes:
            self.figure.text(0.98, 0.5, self.volumes[0].ylabel, rotation=270, ha='center', va='center')
        
        if not self.show_individual_amounts_labels:
            self.figure.text(0.02, 0.5, self.amounts[0].ylabel if self.some_volumes else self.timeseries[0].ylabel, rotation=90, ha='center', va='center')
        
        if not self.show_individual_time_labels:
            self.figure.text(0.5, 0.02, self.timeseries[0].xlabel, ha='center')#, va='center')

#        if not self.some_volumes:
#            self.figure.text(0.02, 0.5, self.timeseries[0].ylabel, rotation=90, ha='center', va='center')
#            adjustprops = dict(left=0.1, bottom=0.2, right=0.97, top=0.85, wspace=0.2, hspace=0.30)
#            self.figure.subplots_adjust(**adjustprops)
#        else:
#            self.figure.text(0.02, 0.5, self.amounts[0].ylabel, rotation=90, ha='center', va='center')
#            self.figure.text(0.98, 0.5, self.volumes[0].ylabel, rotation=270, ha='center', va='center')
#            adjustprops = dict(left=0.15, bottom=0.15, right=0.92, top=0.85, wspace=0.35, hspace=0.25)
#            self.figure.subplots_adjust(**adjustprops)
        
        if self.style == 'Combined':
            self.combine()
        elif self.style == 'Stacked':
            self.stack()
        elif self.style == 'Tiled':
            self.tile()

        self.figure.set_facecolor('white')
        
#        self._show_figure_legend_changed()
#        self._show_individual_legends_changed()
        
        self._redraw_figure()

#    # doesn't update legends!
#    @on_trait_change('timeseries:_colour')
#    def _update_line_color(self, timeseries, _, old, new):
#        line = self.timeseries_to_line_map[timeseries]
#        line.set_color(timeseries.colour)
#        self._redraw_figure()

    def _redraw_figure(self):
        if self.figure.canvas is not None:
            self.figure.canvas.draw()


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

#    lines = List(Tuple(Line2D, Str))
    timeseries_to_line_map = Dict(Timeseries, Line2D)

    def _plot_line(self, axes, timeseries):
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


    def combine(self):
        if self.some_volumes: # plot species on left y-axis and volumes on right y-axis

#            axes = self._create_axes(self.amounts[0].xlabel, self.amounts[0].ylabel, 111)
#            axes = self._create_axes('', '', 111)
            axes = self.figure.add_subplot(111)
            for timeseries in self.amounts:
                self._plot_timeseries(axes, timeseries)
#            if not self.show_individual_amounts_labels:
#                axes.set_ylabel('')       
#            if not self.show_individual_time_labels:
#                axes.set_xlabel('')
            if self.show_individual_time_labels:
                axes.set_xlabel(timeseries.xlabel)
            if self.show_individual_amounts_labels:
                axes.set_ylabel(timeseries.ylabel)
            
#            axes = self._create_axes_twinx(axes, self.volumes[0].ylabel)
#            axes = self._create_axes_twinx(axes, '')
            axes = axes.twinx()
            for timeseries in self.volumes:
                self._plot_timeseries(axes, timeseries)
#            if not self.show_individual_amounts_labels:
#                axes.set_ylabel('')
            if self.show_individual_volume_labels:
                axes.set_ylabel(timeseries.ylabel)
                                
        else:
#            axes = self._create_axes(self.timeseries[0].xlabel, self.timeseries[0].ylabel, 111)
            axes = self.figure.add_subplot(111)
            for timeseries in self.timeseries:
                self._plot_timeseries(axes, timeseries)
#            if not self.show_individual_amounts_labels:
#                axes.set_ylabel('')
            if self.show_individual_time_labels:
                axes.set_xlabel(timeseries.xlabel)
            if self.show_individual_amounts_labels or self.show_individual_volume_labels:
                axes.set_ylabel(timeseries.ylabel)
        
        adjustprops = dict(left=0.1, bottom=0.15, right=0.9, top=0.85, wspace=0.2, hspace=0.2)
        self.figure.subplots_adjust(**adjustprops)
    
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
        
#        # can test using:
#        self.some_volumes
#        not len(self.volumes) > 0 # no volumes
#        self.show_volumes_separately
        
        if self.show_volumes_separately:
        
            if len(self.timeseries) == 1:
                self.combine()
                return
            elif len(self.timeseries) == 2:
                self.stack()
                return
            
            rows, cols = arrange(self.timeseries)
            
#            # tile showing xlabels for lowest plot of each column 
#            for i, timeseries in enumerate(self.timeseries):
#                axes = self._create_axes(timeseries.xlabel, timeseries.ylabel, rows, cols, i + 1)
#                self._plot_line(axes, timeseries)
#                if i + 1 < len(self.timeseries) - (cols - 1):
#                    for label in axes.get_xticklabels():
#                        label.set_visible(False)
#                    axes.set_xlabel('')

            # tile showing single xlabel for all plots 
            self.figure.text(0.5, 0.02, self.timeseries[0].xlabel, ha='center')#, va='center')
            for i, timeseries in enumerate(self.timeseries):
                axes = self._create_axes('', timeseries.ylabel, rows, cols, i + 1)
                self._plot_line(axes, timeseries)
                if i + 1 < len(self.timeseries) - (cols - 1):
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
                if not self.some_volumes:
                    axes.set_ylabel('')
        
        else:
            
            if len(self.amounts) == 1:
                self.combine()
                return
            elif len(self.amounts) == 2:
                self.stack()
                return
            
            rows, cols = arrange(self.timeseries)
            
            # each non-volume timeseries should have a corresponding volume timeseries (which will be shared between non-volume timeseries) 
            amounts_to_volumes_map = {}
            for amounts_timeseries in self.amounts:
                compartment_index = amounts_timeseries.compartment.index
                for volumes_timeseries in self.volumes:
                    if volumes_timeseries.compartment.index == compartment_index:
                        amounts_to_volumes_map[amounts_timeseries] = volumes_timeseries
                        break
#            print amounts_to_volumes_map
            
            # tile showing single xlabel for all plots 
            self.figure.text(0.5, 0.02, self.timeseries[0].xlabel, ha='center')#, va='center') #TODO factor this out so it is the same for each plot style and can be switched (independently for time, amounts and volumes)
            for i, timeseries in enumerate(self.amounts):
                axes = self._create_axes('', '', rows, cols, i + 1)#timeseries.ylabel
                self._plot_line(axes, timeseries)
                try:
                    not_volume_timeseries = amounts_to_volumes_map[timeseries]
                    axes = self._create_axes_twinx(axes, '')#self.volumes[0].ylabel)
                    self._plot_timeseries(axes, not_volume_timeseries)
                    
                except KeyError:
                    pass
                
                if i + 1 < len(self.timeseries) - (cols - 1):
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
                if not self.some_volumes:
                    axes.set_ylabel('')

        
        if not self.some_volumes:
            self.figure.text(0.02, 0.5, self.timeseries[0].ylabel, rotation=90, ha='center', va='center')
            adjustprops = dict(left=0.1, bottom=0.2, right=0.97, top=0.85, wspace=0.2, hspace=0.30)
            self.figure.subplots_adjust(**adjustprops)
        else:
            self.figure.text(0.02, 0.5, self.amounts[0].ylabel, rotation=90, ha='center', va='center')
            self.figure.text(0.98, 0.5, self.volumes[0].ylabel, rotation=270, ha='center', va='center')
            adjustprops = dict(left=0.15, bottom=0.15, right=0.92, top=0.85, wspace=0.35, hspace=0.25)
            self.figure.subplots_adjust(**adjustprops)


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
                    Item('show_volumes_separately', visible_when='object.some_volumes and not object.style=="Combined"'),
                    'show_gridlines',
                    'show_individual_legends',
                    'show_figure_legend',
#                    Spring(),
                ),
                HGroup(
                    Item('show_individual_volume_labels', visible_when='len(object.volumes) > 0'),
                    Item('show_individual_amounts_labels', visible_when='len(object.amounts) > 0'),
                    'show_individual_time_labels',
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

    save_resized = Button

    def _save_resized_fired(self):
        resize_and_save_matplotlib_figure(self.figure)


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

        
#    def configure_traits(self, *args, **kwargs):
##        self._update_figure() #TODO add via do_later via timer 
#        super(TimeseriesPlot, self).configure_traits(*args, **kwargs)

        
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
#        molecules, # if len(timeseries) < 3 tile will defer to stack or combine
#        molecules,
#        concentration, # concentration and molecules will never be shown together
        volume,
        volume,
        volume,
    ]
#    volume.colour = (0.2, 0, 0.7)
    TimeseriesPlot(
        timepoints=timepoints,
        timeseries=timeseries,
        title='titular',
    ).configure_traits()



if __name__ == '__main__':
    main()
