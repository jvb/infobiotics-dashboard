from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import (HasTraits, Instance, Str, List, Float, Bool,
    Button, on_trait_change, Tuple, Dict, Array, Enum, Property, Trait,
    cached_property)
from enthought.traits.ui.api import (View, VGroup, Item, HGroup, Spring,
    ListEditor, InstanceEditor, EnumEditor)
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
from matplotlib.axes import Axes, Subplot as AxesSubplot
from matplotlib.ticker import ScalarFormatter, NullFormatter
from timeseries import Timeseries
from infobiotics.commons.ordereddict import OrderedDict

concentrations_ordered_dict = OrderedDict(
    [
        ('M', 0),
        ('mM', -3),
        ('uM', -6),
        ('nM', -9),
        ('pM', -12),
        ('fM', -5),
    ]
)

class HiddenOffsetScalarFormatter(ScalarFormatter): 
    ''' Use hide_offset=True to remove scientific notation label and set
    self.hidden_offset instead.
    
    '''
    def __init__(self, hide_offset=False, useOffset=True, useMathText=False):
        self.hide_offset = hide_offset
        ScalarFormatter.__init__(self, useOffset=useOffset, useMathText=useMathText)
    
    def get_offset(self):
        s = ScalarFormatter.get_offset(self)
        self.hidden_offset = s
        if self.hide_offset:
            return ''
        return s


class FixedOrderFormatter(HiddenOffsetScalarFormatter):
    ''' Formats axis ticks using scientific notation with a constant order of 
    magnitude.
    
    Adapted from http://stackoverflow.com/questions/3677368/matplotlib-format-axis-offset-values-to-whole-numbers-or-specific-number/3679918#3679918
    to use HiddenOffsetScalarFormatter.
    
    '''
    def __init__(self, order_of_mag=0, hide_offset=False, useOffset=True, useMathText=False):
        self._order_of_mag = order_of_mag
        HiddenOffsetScalarFormatter.__init__(self, hide_offset, useOffset=useOffset, useMathText=useMathText)

    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag


class TimeseriesPlot(HasTraits):

    # class attributes (not traits!)

    font_properties = FontProperties(size='medium')#'small'


#    null_formatter = NullFormatter()
    
    time_formatter = ScalarFormatter(useOffset=True, useMathText=True)
    time_formatter.set_scientific(True) # unnecessary?
    time_formatter.set_powerlimits((-3, 4))

    molecules_formatter = ScalarFormatter(useOffset=True, useMathText=True)
    molecules_formatter.set_scientific(True) # unnecessary?
    molecules_formatter.set_powerlimits((-3, 4))


    # traits
    
    time_units = Trait(
        's',
        {
            'seconds':1,
            'minutes':60,
            'hours':3600,
            'microseconds':0.0000001,
            'milliseconds':0.0001,
            'days':86400,
            's':1,
        }
    )
    
    
    amounts_type = Enum(['Molecules', 'Concentration']) #TODO use with concentration_formatter
    
    concentration_units = Trait(
        'uM',
        {
            'M'  : 0,
            'mM' :-3,
            'uM' :-6,
            'nM' :-9,
            'pM' :-12,
            'fM' :-15,
        }
    )
    
    volume_units = Trait(
        'uL',
        {
            'L'  : 0,
            'mL' :-3,
            'uL' :-6,
            'nL' :-9,
            'pL' :-12,
            'fL' :-15,
        }
    )

#    # testing EnumEditor values order and shadow_values - works
#    @on_trait_change('concentration_units, volume_units')
#    def units_changed(self, name, units):
#        print units, getattr(self, name + '_')

    concentration_formatter = Property(Instance(FixedOrderFormatter), depends_on='concentration_units')
    
    volume_formatter = Property(Instance(FixedOrderFormatter), depends_on='volume_units')


    figure = Instance(Figure, ())

    figure_title = Str #TODO get from SimulatorResultsDialog
    
#    def _figure_title_default(self):
#        return 'figure title'

    
    timeseries = List(Timeseries)

    timepoints = Array #TODO necessary/used?

    some_volumes = Property(Bool, depends_on='timeseries')
    amounts = Property(List(Timeseries), depends_on='timeseries')
    volumes = Property(List(Timeseries), depends_on='timeseries')
    amounts_to_volumes_map = Property(Dict(Timeseries, Timeseries), depends_on='timeseries') # each non-volume timeseries should have a corresponding volume timeseries (if volumes is selected in the species list widget) [which will be shared between non-volume timeseries]

    style = Enum(['Combined', 'Stacked', 'Tiled'])
#    style = Enum(['Stacked', 'Combined', 'Tiled'])
#    style = Enum(['Tiled', 'Stacked', 'Combined'])
    
    separate_volumes = Bool

    gridlines = Bool(True)

    figure_legend = Bool(True)
    individual_legends = Bool    
    
    individual_volume_labels = Bool
    individual_amounts_labels = Bool
    individual_time_labels = Bool

    window_title = Str('window title') #TODO necessary/used?
    

    @cached_property
    def _get_concentration_formatter(self):
        return FixedOrderFormatter(order_of_mag=self.concentration_units_, hide_offset=True, useOffset=True, useMathText=True)
    
    @cached_property
    def _get_volume_formatter(self):
        return FixedOrderFormatter(order_of_mag=self.volume_units_, hide_offset=True, useOffset=True, useMathText=True)
    
    
    @cached_property
    def _get_some_volumes(self):
        if 0 < len(self.volumes) < len(self.timeseries):
            return True
        else:
            return False

    @cached_property
    def _get_amounts(self):
        return [timeseries for timeseries in self.timeseries if timeseries.values_type != 'Volume']
    
    @cached_property
    def _get_volumes(self):
        return [timeseries for timeseries in self.timeseries if timeseries.values_type == 'Volume']
    
    @cached_property
    def _get_amounts_to_volumes_map(self):
        amounts_to_volumes_map = {}
        for amounts in self.amounts:
            amounts_compartment_index = amounts.compartment.index
            for volumes in self.volumes:
                if volumes.compartment.index == amounts_compartment_index:
                    amounts_to_volumes_map[amounts] = volumes
                    break
        return amounts_to_volumes_map
    

    @on_trait_change('style, individual_legends')
    def _change_individual_legends_visibility(self):
        if self.individual_legends:
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
        
    
    @on_trait_change('style, figure_legend')
    def _change_figure_legend_visibility(self):
        if self.figure_legend:
            if hasattr(self, '_figure_legend'):
                self._figure_legend.set_visible(True)
            else:
                if self.figure.canvas is not None:
                    self._figure_legend = DraggableLegend(self._create_figure_legend())
                else:
                    self._figure_legend = self._create_figure_legend()
        else:
            if hasattr(self, '_figure_legend'):
                self._figure_legend.set_visible(False)
                del self._figure_legend
#            self._figure_legend.remove() # planned but not implemented in 0.99.0
        self._redraw_figure()

    def _create_figure_legend(self):
        lines = []
        labels = []
        for timeseries, line in self.timeseries_to_line_map.iteritems():
            lines.append(line)
            labels.append(timeseries.title)
        return self.figure.legend(
            lines,
            labels,
            loc='upper center', # http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure.legend 
            prop=self.font_properties
        ) 
    

#    @on_trait_change('+') # dangerous
    @on_trait_change('\
        style, \
        timeseries, \
        timeseries:_colour, \
        gridlines, \
        separate_volumes, \
        individual_volume_labels, \
        individual_amounts_labels, \
        individual_time_labels, \
        scientific_time_ticklabels, \
        scientific_amounts_ticklabels, \
        scientific_volume_ticklabels, \
        concentration_units, \
        volume_units \
        ')
    def _update_figure(self):
#        if len(self.timeseries) == 0:
#            return

        self.figure.clear()
        if not hasattr(self, 'axes'):
            self.axes = []
        del self.axes[:]
#        self.timeseries_to_line_map.clear()
        
        if self.style == 'Combined':
            self.combine()
        elif self.style == 'Stacked':
            self.stack()
        elif self.style == 'Tiled':
            self.tile()
            
        if not self.individual_time_labels:
            self.figure.text(0.5, 0.02, self.timeseries[0].xlabel, ha='center', va='bottom')
            # remove individual time labels
            for axes in self.axes:
                axes.set_xlabel('')

        if not self.separate_volumes:
            if not self.individual_amounts_labels:
                if len(self.amounts) > 0:
                    self.figure.text(0.02, 0.5, self.amounts[0].ylabel, rotation=90, ha='left', va='center')
                    for axes in self.axes:
                        if isinstance(axes, AxesSubplot):
                            axes.set_ylabel('')
    
            if not self.individual_volume_labels:
                if not self.some_volumes and len(self.volumes) > 0:
                    # only volumes - label on left
                    self.figure.text(0.02, 0.5, self.volumes[0].ylabel, rotation=90, ha='right', va='center')
                    for axes in self.axes:
                        axes.set_ylabel('')
                else:
                    # mixed - label on right
                    self.figure.text(0.98, 0.5, self.volumes[0].ylabel, rotation=90, ha='center', va='center')
                    for axes in self.axes:
                        if type(axes) == Axes: # can't use isinstance here because AxesSubplot is a subclass of Axes ! 
                            axes.set_ylabel('')

        adjustprops = dict(bottom=0.1, top=0.925, wspace=0.3, hspace=0.2)
        if len(self.figure_title) > 0:
            adjustprops.update(top=0.85)
            self.figure.suptitle(self.figure_title)
#        adjustprops.update(wspace=0.2, hspace=0.2)
        if not self.some_volumes or (self.separate_volumes and self.style != 'Combined'):
            # no secondary y-axis - more right
            adjustprops.update(left=0.1, right=0.95)
        else:
            # secondary y-axis - less right
            adjustprops.update(left=0.1, right=0.9)
        if self.style == 'Tiled':
            if self.separate_volumes:
                adjustprops.update(wspace=0.25)
            else:
                adjustprops.update(wspace=0.1)
        self.figure.subplots_adjust(**adjustprops)
        
        self.figure.set_facecolor('white')
        
#        self._figure_legend_changed() #TODO
#        self._individual_legends_changed() #TODO
        
        self._redraw_figure()

#    # doesn't update legends ! 
#    @on_trait_change('timeseries:_colour')
#    def _update_line_color(self, timeseries, _, old, new):
#        line = self.timeseries_to_line_map[timeseries]
#        line.set_color(timeseries.colour)
#        self._redraw_figure()

    def _redraw_figure(self):
        if self.figure.canvas is not None:
            self.figure.canvas.draw()

    scientific_time_ticklabels = Bool(True)
    scientific_amounts_ticklabels = Bool(True)
    scientific_volume_ticklabels = Bool(True)

    def _create_axes(self, timeseries, *args, **kwargs):
        ''' Create a subplot (labelled depending on traits) returning axes. 
        
        Can override labels using axes.set_xlabel('') or axes.set_ylabel('').
        
        '''
        axes = self.figure.add_subplot(*args, **kwargs) # works for 111, (1, 1, 1) and sharex=axes
        self.axes.append(axes)

        axes.set_xlabel(timeseries.xlabel)
        axes.set_ylabel(timeseries.ylabel)

#        axes.ticklabel_format(style='sci', scilimits=(-3, 3), axis='both')
        if self.scientific_time_ticklabels: 
            axes.xaxis.set_major_formatter(self.time_formatter)
        if self.scientific_amounts_ticklabels:
            if timeseries.values_type == 'Molecules':
                axes.yaxis.set_major_formatter(self.molecules_formatter)
            elif timeseries.values_type == 'Concentration':
                axes.yaxis.set_major_formatter(self.concentrations_formatter)
        if self.scientific_volume_ticklabels: 
            if timeseries.values_type == 'Volume':
                axes.yaxis.set_major_formatter(self.volumes_formatter)
        
        if self.gridlines:
            axes.grid(True, which='major')
            axes.grid(True, which='minor') # doesn't do anything
        
        return axes

    def _create_axes_twinx(self, axes, timeseries): 
        axes = axes.twinx()
        self.axes.append(axes)

##        axes.set_xlabel(timeseries.xlabel) # not needed
#        axes.set_ylabel(timeseries.ylabel) # use Volume (order_of_mag M)
        axes.set_ylabel('Volume (%s)' % self.volume_units)

#        axes.ticklabel_format(style='sci', scilimits=(-3, 3), axis='both')
        if self.scientific_time_ticklabels: 
            axes.xaxis.set_major_formatter(self.time_formatter)
        if self.scientific_volume_ticklabels: 
            axes.yaxis.set_major_formatter(self.volume_formatter)

        # don't show gridlines for secondary y-axis.
#        if self.gridlines:
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
            axes = self._create_axes(self.amounts[0], 111)
            for timeseries in self.amounts:
                self._plot_timeseries(axes, timeseries)
            axes = self._create_axes_twinx(axes, self.volumes[0])
            for timeseries in self.volumes:
                self._plot_timeseries(axes, timeseries)
        else:
            axes = self._create_axes(self.timeseries[0], 111)
            for timeseries in self.timeseries:
                self._plot_timeseries(axes, timeseries)
        
    def stack(self):
        if len(self.timeseries) == 1:
            self.combine()
            return
        cols = 1
        if self.separate_volumes:
            rows = len(self.timeseries)
            for i, timeseries in enumerate(reversed(self.timeseries)):
                if i == 0:
                    axes = self._create_axes(timeseries, rows, cols, rows)
                    shared_axes = axes
                else:
                    axes = self._create_axes(timeseries, rows, cols, rows - i, sharex=shared_axes)
                    # hide xlabel and xticklabels if not bottom axes 
                    axes.set_xlabel('')
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
                self._plot_timeseries(axes, timeseries)
        else:
            rows = len(self.amounts)
            for i, amounts in enumerate(reversed(self.amounts)):
                if i == 0: # bottom axes (should be labelled)
                    axes = self._create_axes(amounts, rows, cols, rows)
                    shared_axes = axes
                else:
                    axes = self._create_axes(amounts, rows, cols, rows - i, sharex=shared_axes)
                    # hide xlabel and xticklabels if not bottom axes 
                    axes.set_xlabel('')
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
                # plot amounts on primary y-axis
                self._plot_timeseries(axes, amounts)
                # plot volumes on secondary y-axis
                try:
                    volumes = self.amounts_to_volumes_map[amounts]
                    axes = self._create_axes_twinx(axes, volumes)
                    self._plot_timeseries(axes, volumes)
                except KeyError: pass # clever way of making this work regardless of some_volumes

    def tile(self):
        if self.separate_volumes:
            if len(self.timeseries) == 1:
                self.combine()
                return
            elif len(self.timeseries) == 2:
                self.stack()
                return
            rows, cols = arrange(self.timeseries)
            for i, timeseries in enumerate(self.timeseries):
                axes = self._create_axes(timeseries, rows, cols, i + 1)
                self._plot_timeseries(axes, timeseries)
                # show xlabels for lowest plot of each column 
                if i + 1 < len(self.timeseries) - (cols - 1):
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
        else:
            if len(self.amounts) == 1:
                self.combine()
                return
            elif len(self.amounts) == 2:
                self.stack() #TODO do side-by-side instead
                return
            rows, cols = arrange(self.amounts)
            for i, amounts in enumerate(self.amounts):
                axes = self._create_axes(amounts, rows, cols, i + 1)
                self._plot_timeseries(axes, amounts)
                # show xlabels for lowest plot of each column 
                if (i + 1) < len(self.amounts) - (cols - 1):
                    for label in axes.get_xticklabels():
                        label.set_visible(False)
                if (i + 1) % cols != 1:
                    axes.set_ylabel('')
                    for label in axes.get_yticklabels():
                        label.set_visible(False)
                try:
                    volumes = self.amounts_to_volumes_map[amounts]
                    axes = self._create_axes_twinx(axes, volumes)
                    self._plot_timeseries(axes, volumes)
                    if (i + 1) % cols != 0 and (i + 1) != len(self.amounts):
                        axes.set_ylabel('')
                        for label in axes.get_yticklabels():
                            label.set_visible(False)
#                        axes.yaxis.set_major_formatter(self.null_formatter)
#                        axes.yaxis.get_major_formatter().set_scientific(False)
                except KeyError: pass # clever way of making this work regardless of some_volumes

#    def _options_fired(self):
#        self.edit_traits(
#            view=View(
#                VGroup(
#                    HGroup(
#                        Item('style', style='custom'),
#                    ),
#                    HGroup(
#                        Item('separate_volumes', visible_when='object.some_volumes and not object.style=="Combined"'),
#                    ),
#                    HGroup(
#                        'gridlines',
#                    ),
#                    HGroup(
#                        'figure_legend',
#                        Item('individual_legends', visible_when='not object.style=="Combined"'),
#                    ),
#                    HGroup(
#                        Item('individual_volume_labels', visible_when='len(object.volumes) > 0) and not object.style=="Combined"'),
#                        Item('individual_amounts_labels', visible_when='len(object.amounts) > 0 and not object.style=="Combined"'),
#                        Item('individual_time_labels', visible_when='not object.style=="Combined"'),
#                    ),
#                    Item('timeseries',
#                        show_label=False,
##                        style='readonly',
##                        editor=ListEditor(
##                            style='custom',
##                            editor=InstanceEditor(),
##                        ),
#                        style='custom',
#                        editor=timeseries_table_editor,
#                    ),
#                    show_border=True,
#                ),
#                title='Configure timeseries plot',
#            )
#        )
#
#    options = Button

    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                       'amounts_type', #TODO remove
                       Item('concentration_units',
                           editor=EnumEditor(values={'M':'1:M', 'mM':'2:mM', 'uM':'3:uM', 'pM':'4:pM', 'fM':'5:fM'}),
                           visible_when='object.amounts_type=="Concentration"'),
                       Item('volume_units',
                           editor=EnumEditor(values={'L':'1:L', 'mL':'2:mL', 'uL':'3:uL', 'pL':'4:pL', 'fL':'5:fL'}),
                           visible_when='len(object.volumes) > 0'),
                ),
                HGroup(
                    Item('style', style='custom'),
                    Item('separate_volumes', visible_when='object.some_volumes and not object.style=="Combined"'),
                ),
                HGroup(
                    'gridlines',
                    'figure_legend',
                    Item('individual_legends', visible_when='not object.style=="Combined"'),
                ),
                HGroup(
                    Item(label='Show individual axis labels'),
                    Item('individual_time_labels', label='time', visible_when='not object.style=="Combined"'),
                    Item('individual_amounts_labels', label='amounts', visible_when='len(object.amounts) > 0 and not object.style=="Combined"'),
                    Item('individual_volume_labels', label='volume', visible_when='len(object.volumes) > 0 and not object.style=="Combined"'),
                ),
                HGroup(
                    'scientific_time_ticklabels',
                    'scientific_amounts_ticklabels',
                    'scientific_volume_ticklabels',
                ),
                HGroup(
                    Item('figure',
                        editor=MatplotlibFigureEditor(
                            toolbar=True,
#                            toolbar_above=False,
                        ),
                        show_label=False,
                    ),
                ),
                HGroup(
#                    Item('options', show_label=False),
                    Spring(),
                    Item('save_resized'),
                    Item('list_widget', label='Edit timeseries...'),
                    show_labels=False,
                ),
                show_border=True,
                show_labels=False,
            ),
#            width=640, height=480,
            width=1025, height=768,
            resizable=True,
            title=self.window_title,
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


from enthought.traits.ui.api import TableEditor
from enthought.traits.ui.table_column import ObjectColumn
timeseries_table_editor = TableEditor(
    columns=[
        ObjectColumn(name='title',
#            width=0.4,
#            editable=False,
        ),
        ObjectColumn(name='_colour',
#            width=0.2,
#            editor=TextEditor(
##                evaluate=int,#evaluate_int,
#                evaluate_name='evaluate', # see MoleculeConstant.evaluate(value)
#            )
        ),
        ObjectColumn(name='values_units',
#            width=0.4,
#            editable=False,
        ),
    ],
    sortable=False,
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
#    timepoints = np.arange(number_of_timepoints)
    timepoints = np.linspace(0, 1000000, number_of_timepoints)
    molecules = Timeseries(
        run=run,
        species=species,
        compartment=compartment,
        timepoints=timepoints,
#        values=np.sin(np.arange(number_of_timepoints)),
        values=np.linspace(0, 100000, number_of_timepoints),
        values_type='Molecules',
        _colour=colours.colour(0),
    )
    concentration = Timeseries(
        run=run,
        species=species,
        compartment=compartment,
        timepoints=timepoints,
#        values=np.cos(np.arange(number_of_timepoints)),
        values=np.linspace(0, 0.003, number_of_timepoints),
        values_type='Concentration',
        _colour=colours.colour(1),
    )
    volume = Timeseries(
        run=run,
        species=volumes_species,
        compartment=compartment,
        timepoints=timepoints,
#        values=np.tan(np.arange(number_of_timepoints)),
        values=np.linspace(0, 0.000002, number_of_timepoints),
        values_type='Volume',
        _colour=colours.colour(2),
    )
    timeseries = [
        molecules, # if len(timeseries) < 3 tile will defer to stack or combine
        molecules,
        concentration, # concentration and molecules will never be shown together
        volume,
#        volume,
#        volume,
    ]
#    volume.colour = (0.2, 0, 0.7)
    TimeseriesPlot(
        timepoints=timepoints,
        timeseries=timeseries,
        title='titular',
    ).configure_traits()



if __name__ == '__main__':
    main()
