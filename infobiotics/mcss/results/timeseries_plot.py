import infobiotics
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import (HasTraits, Instance, Str, List, Float, Bool,
    Button, on_trait_change, Tuple, Dict, Array, Enum, Property, Range, Any, Button,
    cached_property)
from enthought.traits.ui.api import (View, VGroup, Item, HGroup, Spring,
    ListEditor, InstanceEditor, SetEditor, RangeEditor)
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
from timeseries import Timeseries
from matplotlib.ticker import ScalarFormatter, NullFormatter
from infobiotics.commons.quantities.traits_ui_converters import time_units, TimeUnit, time_units_editor, volume_units, VolumeUnit, volume_units_editor, substance_units, SubstanceUnit, substance_units_editor, concentration_units, ConcentrationUnit, concentration_units_editor

class HiddenOffsetScalarFormatter(ScalarFormatter): 
    ''' Use hide_offset=True to remove scientific notation label by default or
    'axes.xaxis.get_major_formatter().hide_offset = True' instead.
    
    '''
    def __init__(self, hide_offset=False, useOffset=True, useMathText=False):
        self.hide_offset = hide_offset
        ScalarFormatter.__init__(self, useOffset=useOffset, useMathText=useMathText)
    
    def get_offset(self):
        if self.hide_offset:
            return ''
        return ScalarFormatter.get_offset(self)

def get_scientific_formatter():
    scientific_formatter = HiddenOffsetScalarFormatter(useOffset=False, useMathText=True)
    scientific_formatter.set_powerlimits((-3, 4))
    scientific_formatter.set_scientific(True) # forces scientific outside powerlimits
    return scientific_formatter

class TimeseriesPlot(HasTraits):

    _figure = Instance(Figure, ())

    def __init__(self, **traits):
        ''' Call _update_figure only once during initialisation. '''
        HasTraits.__init__(self)
        self.trait_setq(**traits)
        self._timeseries_changed()
        self._update_units()
#        self._update_figure()
    
    font_size = Range(1, 20, 12)

    font_properties = Property(Instance(FontProperties), depends_on='font_size')
    
    @cached_property
    def _get_font_properties(self):
        return FontProperties(size=self.font_size)
    

    scientific_time_ticklabels = Bool(True)
    scientific_amounts_ticklabels = Bool(True)
    scientific_volume_ticklabels = Bool(True)


    figure_title = Str #TODO get from McssResultsDialog

#    def _figure_title_default(self):
#        return 'figure\ntitle'


    timeseries = List(Timeseries)
    _timeseries = List(Timeseries)
    
    def _timeseries_changed(self):
        self._timeseries = self.timeseries[:]

    _some_volumes = Property(Bool, depends_on='_timeseries')#, plot_volumes')
    _amounts = Property(List(Timeseries), depends_on='_timeseries')
    _volumes = Property(List(Timeseries), depends_on='_timeseries')#, plot_volumes')
    _amounts_to_volumes_map = Property(Dict(Timeseries, Timeseries), depends_on='timeseries') # each non-volume timeseries should have a corresponding volume timeseries (if volumes is selected in the species list widget) [which will be shared between non-volume timeseries]

    style = Enum(['Combined', 'Tiled', 'Stacked'])
    
    separate_volumes = Bool

    @on_trait_change('_amounts, _volumes')
    def _update_separate_volumes(self):
        if len(self._amounts) == 0 or len(self._volumes) == 0:
            self.separate_volumes = False

#    plot_volumes = Bool(True)

    gridlines = Bool(True)

    figure_legend = Bool#(True)
    individual_legends = Bool    
    
    individual_volume_labels = Bool
    individual_amounts_labels = Bool
    individual_time_labels = Bool

    abbreviated_units = Bool(True)

    @on_trait_change('timeseries, abbreviated_units')
    def _update_timeseries_abbreviated_units(self):
        for timeseries in self.timeseries:
            timeseries.abbreviated_units = self.abbreviated_units
        self._update_figure()


    window_title = Str('window title') #TODO necessary/used?
    
    
    @cached_property
    def _get__some_volumes(self):
        if 0 < len(self._volumes) < len(self._timeseries):
            return True
        else:
            return False

    @cached_property
    def _get__amounts(self):
        return [timeseries for timeseries in self._timeseries if timeseries.values_type != 'Volume']
    
    @cached_property
    def _get__volumes(self):
#        if self.plot_volumes:
        return [timeseries for timeseries in self._timeseries if timeseries.values_type == 'Volume']
#        else:
#            return []
    
    @cached_property
    def _get__amounts_to_volumes_map(self):
        _amounts_to_volumes_map = {}
        for amounts in self._amounts:
            amounts_compartment_index = amounts.compartment.index
            for volumes in self._volumes:
                if volumes.compartment.index == amounts_compartment_index:
                    _amounts_to_volumes_map[amounts] = volumes
                    break
        return _amounts_to_volumes_map
    

    @on_trait_change('style, individual_legends')
    def _change_individual_legends_visibility(self):
        if self.individual_legends:
            self._create_individual_legends()
        else:
            for timeseries, line in self._timeseries_to_line_map.iteritems():
                legend = line.axes.get_legend()
                if legend is not None: 
                    legend.set_visible(False)
        self._redraw_figure()
    
    def _create_individual_legends(self):        
        for timeseries, line in self._timeseries_to_line_map.iteritems():
            DraggableLegend(line.axes.legend(loc='best', prop=self.font_properties))
        
    
    @on_trait_change('style, figure_legend')
    def _change_figure_legend_visibility(self):
        if self.figure_legend:
            if hasattr(self, '_figure_legend'):
                self._figure_legend.set_visible(True)
            else:
                if self._figure.canvas is not None:
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
        for timeseries, line in self._timeseries_to_line_map.iteritems():
            lines.append(line)
            labels.append(timeseries.title)
        return self._figure.legend(
            lines,
            labels,
            loc='upper center', # http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure.legend 
            prop=self.font_properties
        ) 
    

#    @on_trait_change('+') # dangerous
    @on_trait_change('\
        style, \
        _timeseries, \
        _timeseries:_colour, \
        font_size, \
        gridlines, \
        separate_volumes, \
        individual_volume_labels, \
        individual_amounts_labels, \
        individual_time_labels, \
        scientific_time_ticklabels, \
        scientific_amounts_ticklabels, \
        scientific_volume_ticklabels, \
        timepoints_units, \
        volumes_units, \
        substances_units, \
        concentrations_units')
    def _update_figure(self):
        

        # start from scratch
        self._figure.clear()
        
        if len(self._timeseries) < 1:
#            self._redraw_figure()
            return
        
        if not hasattr(self, 'axes'):
            self.axes = []
        del self.axes[:]
#        self._timeseries_to_line_map.clear() # legends?
        
        # create axes and plot timeseries on them
        if self.style == 'Combined':
            self.combine()
        elif self.style == 'Stacked':
            self.stack()
        elif self.style == 'Tiled':
            self.tile()
            
        if len(self.figure_title) > 0:
            self._figure.suptitle(self.figure_title)
            
        # remove excess labels            
        
        volumes_label = ''
        for timeseries in self.timeseries:
            if timeseries.values_type == 'Volume':
                volumes_label = timeseries.ylabel
                break
        
        if not self.individual_time_labels:
            self._figure.text(0.4, 0.02, self._timeseries[0].xlabel, ha='center', va='bottom') # made Time text off-centre so as not to clash with offset  
            # remove individual time labels
            for axes in self.axes:
                axes.set_xlabel('')
        if not self.separate_volumes:
            if not self.individual_amounts_labels:
                if len(self._amounts) > 0:
                    self._figure.text(0.02, 0.5, self._amounts[0].ylabel, rotation=90, ha='left', va='center')
                    for axes in self.axes:
                        if isinstance(axes, AxesSubplot):
                            axes.set_ylabel('')
            if not self.individual_volume_labels:# and self.plot_volumes:
                if not self._some_volumes and len(self._volumes) > 0:
                    # only volumes - label on left
                    self._figure.text(0.02, 0.5, volumes_label, rotation=90, ha='right', va='center')
                    for axes in self.axes:
                        axes.set_ylabel('')
                else:
                    # mixed - label on right
                    self._figure.text(0.98, 0.5, volumes_label, rotation=90, ha='center', va='center')
                    for axes in self.axes:
                        if type(axes) == Axes: # can't use isinstance here because AxesSubplot is a subclass of Axes 
                            axes.set_ylabel('')

        self.maximise_plot_area()   
        
        self._figure.set_facecolor('white')
        
#        self._figure_legend_changed() #TODO
#        self._individual_legends_changed() #TODO
        
        self._redraw_figure()


    def maximise_plot_area(self):
        subplot_params = dict(left=0.075, right=0.925, top=0.955, bottom=0.1, hspace=0.25, wspace=0.10) # good general spacing for 6 plots combined, tiled or stacked 

        if len(self.figure_title) > 0:
            subplot_params.update(top=0.9)

        if not self._some_volumes or (self.separate_volumes and self.style != 'Combined'):
            # no secondary y-axis - more right
            subplot_params.update(right=0.975)

#        if self.style == 'Tiled':
#            if self.separate_volumes:
#                subplot_params.update(wspace=0.25)
#            else:
#                subplot_params.update(wspace=0.1)
#
#        if self.scientific_time_ticklabels: # increase hspace to ensure offset is obvious
#            subplot_params.update(hspace=subplot_params['hspace'] + 0.05)
#
#        if self.scientific_amounts_ticklabels: # decrease left maximise plot area
#            subplot_params.update(left=subplot_params['left'] - 0.05)
#
#        if self.scientific_volume_ticklabels: # increase right maximise plot area
#            subplot_params.update(right=subplot_params['right'] + 0.05)
            
        self._figure.subplots_adjust(**subplot_params)


#    # doesn't update legends ! 
#    @on_trait_change('_timeseries:_colour')
#    def _update_line_color(self, timeseries, _, old, new):
#        line = self._timeseries_to_line_map[timeseries]
#        line.set_color(timeseries.colour)
#        self._redraw_figure()

    def _redraw_figure(self):
        if self._figure.canvas is not None:
            self._figure.canvas.draw()

    def _create_axes(self, timeseries, *args, **kwargs):
        ''' Create a subplot (labelled depending on traits) returning axes. 
        
        Can override labels using axes.set_xlabel('') or axes.set_ylabel('').
        
        '''
        axes = self._figure.add_subplot(*args, **kwargs) # works for 111, (1, 1, 1) and sharex=axes
        self.axes.append(axes)

#        axes.ticklabel_format(style='plain', axis='y')
#        if self.scientific_time_ticklabels:
#            axes.xaxis.set_major_formatter(get_scientific_formatter())
#        if (timeseries.values_type != 'Volume' and self.scientific_amounts_ticklabels) or (timeseries.values_type == 'Volume' and self.scientific_volume_ticklabels):
#            axes.yaxis.set_major_formatter(get_scientific_formatter())
        self._format_axes_ticklabels(axes, timeseries)

        axes.set_xlabel(timeseries.xlabel)
        axes.set_ylabel(timeseries.ylabel)
        
        if self.gridlines:
            axes.grid(True, which='major')
#            axes.grid(True, which='minor') # doesn't do anything
        
        return axes

    def _create_axes_twinx(self, axes, timeseries): 
        axes = axes.twinx()
        self.axes.append(axes)

#        axes.ticklabel_format(style='plain', axis='y')
#        if (timeseries.values_type != 'Volume' and self.scientific_amounts_ticklabels) or (timeseries.values_type == 'Volume' and self.scientific_volume_ticklabels):
#            axes.yaxis.set_major_formatter(get_scientific_formatter())
        self._format_axes_ticklabels(axes, timeseries)

        axes.set_ylabel(timeseries.ylabel) # can't use Volume (order_of_mag M), especially for shared ylabel

        # don't show gridlines for secondary y-axis.
        
        return axes

    def _format_axes_ticklabels(self, axes, timeseries):
#        axes.ticklabel_format(style='sci', scilimits=(-3, 3), axis='both', useoffset=True)
        axes.ticklabel_format(style='plain', axis='both') # reset formatter style
        if self.scientific_time_ticklabels:
            axes.xaxis.set_major_formatter(get_scientific_formatter())
        if (timeseries.values_type != 'Volume' and self.scientific_amounts_ticklabels) or (timeseries.values_type == 'Volume' and self.scientific_volume_ticklabels):
            axes.yaxis.set_major_formatter(get_scientific_formatter())


    def _plot_timeseries(self, axes, timeseries):
        if len(timeseries.errors) > 0:
            self._plot_errorbars(axes, timeseries)
        self._plot_line(axes, timeseries)
    
    def _plot_errorbars(self, axes, timeseries):
        step = 1
        axes.errorbar(
            timeseries.timepoints[::step],
            timeseries.values[::step],
            yerr=timeseries.errors[::step],
            linestyle='None',
            color=timeseries.colour,
            marker=timeseries.marker,
        ) 


#    lines = List(Tuple(Line2D, Str))
    _timeseries_to_line_map = Dict(Timeseries, Line2D)

    def _plot_line(self, axes, timeseries):
        lines = axes.plot(
            timeseries.timepoints,
            timeseries.values,
            label=timeseries.title,
            color=timeseries.colour,
            linestyle='--' if timeseries.values_type == 'Volume' else '-',
            marker=timeseries.marker,
        )
        line = lines[0]
#        print line
#        self.lines.append((line, timeseries.label))
        self._timeseries_to_line_map[timeseries] = line


    def combine(self):
        if self._some_volumes: # plot species on left y-axis and volumes on right y-axis
            axes = self._create_axes(self._amounts[0], 111)
            for timeseries in self._amounts:
                self._plot_timeseries(axes, timeseries)
            axes = self._create_axes_twinx(axes, self._volumes[0])
            for timeseries in self._volumes:
                self._plot_timeseries(axes, timeseries)
        else:
            axes = self._create_axes(self._timeseries[0], 111)
            for timeseries in self._timeseries:
                self._plot_timeseries(axes, timeseries)

    def __hide_xinfo(self, axes):
        axes.set_xlabel('')
        for label in axes.get_xticklabels():
            label.set_visible(False)
        axes.xaxis.get_major_formatter().hide_offset = True
        
    def __hide_yinfo(self, axes):
        axes.set_ylabel('')
        for label in axes.get_yticklabels():
            label.set_visible(False)
        axes.yaxis.get_major_formatter().hide_offset = True
        
    def stack(self):
        if len(self._timeseries) == 1:
            self.combine()
            return
        cols = 1
        if self.separate_volumes:
            rows = len(self._timeseries)
            for i, timeseries in enumerate(reversed(self._timeseries[:-1])):
                if i == 0:
                    axes = self._create_axes(timeseries, rows, cols, rows - 1)
                    shared_axes = axes
                else:
                    axes = self._create_axes(timeseries, rows, cols, rows - (i + 1), sharex=shared_axes)
                self.__hide_xinfo(axes)
                self._plot_timeseries(axes, timeseries)
            timeseries = self._timeseries[-1]
            axes = self._create_axes(timeseries, rows, cols, rows)
            self._plot_timeseries(axes, timeseries)
        else:
            rows = len(self._amounts)
            # first to penultimate (one from bottom) plots: x-axis should *not* be labelled
            for i, amounts in enumerate(reversed(self._amounts[:-1])):
                if i == 0:
                    axes = self._create_axes(amounts, rows, cols, rows - 1)
                    shared_axes = axes
                else:
                    axes = self._create_axes(amounts, rows, cols, rows - (i + 1), sharex=shared_axes)
                self.__hide_xinfo(axes)
                self._plot_timeseries(axes, amounts)
                try:
                    volumes = self._amounts_to_volumes_map[amounts]
                    axes = self._create_axes_twinx(axes, volumes)
                    self._plot_timeseries(axes, volumes)
                    axes.xaxis.get_major_formatter().hide_offset = True # need to do this because the twin axes x axis formatter overwrites the true axes x axis formatters
                except KeyError: pass # clever way of making this work regardless of _some_volumes
            # bottom axes: x-axis should be labelled
            amounts = self._amounts[-1]
            axes = self._create_axes(amounts, rows, cols, rows)
            self._plot_timeseries(axes, amounts)
            try:
                volumes = self._amounts_to_volumes_map[amounts]
                axes = self._create_axes_twinx(axes, volumes)
                self._plot_timeseries(axes, volumes)
            except KeyError: pass # clever way of making this work regardless of _some_volumes

    def tile(self):
        if self.separate_volumes:
            if len(self._timeseries) == 1:
                self.combine()
                return
            elif len(self._timeseries) == 2:
                self.stack()
                return
            rows, cols = arrange(self._timeseries)
            for i, timeseries in enumerate(self._timeseries):
                axes = self._create_axes(timeseries, rows, cols, i + 1)
                self._plot_timeseries(axes, timeseries)
                # show xlabels for lowest plot of each column 
                if i + 1 < len(self._timeseries) - (cols - 1):
#                    axes.set_xlabel('')
#                    for label in axes.get_xticklabels():
#                        label.set_visible(False)
##                    axes.xaxis.set_major_formatter(NullFormatter())
#                    axes.xaxis.get_major_formatter().hide_offset = True
                    self.__hide_xinfo(axes)
        else:
            if len(self._amounts) == 1:
                self.combine()
                return
            elif len(self._amounts) == 2:
                self.stack() #TODO do side-by-side instead
                return
            rows, cols = arrange(self._amounts)
            for i, amounts in enumerate(self._amounts):
                axes = self._create_axes(amounts, rows, cols, i + 1)
                self._plot_timeseries(axes, amounts)
                # show xlabels for lowest plot of each column 
                if (i + 1) < len(self._amounts) - (cols - 1):
#                    axes.set_xlabel('')
#                    for label in axes.get_xticklabels():
#                        label.set_visible(False)
##                    axes.xaxis.get_major_formatter().hide_offset = True
                    self.__hide_xinfo(axes)
                if (i + 1) % cols != 1:
#                    axes.set_ylabel('')
#                    for label in axes.get_yticklabels():
#                        label.set_visible(False)
#                    axes.yaxis.set_major_formatter(NullFormatter())
                    self.__hide_yinfo(axes)
                try:
                    volumes = self._amounts_to_volumes_map[amounts]
                    axes = self._create_axes_twinx(axes, volumes)
                    self._plot_timeseries(axes, volumes)
                    if (i + 1) % cols != 0 and (i + 1) != len(self._amounts):
#                        axes.set_ylabel('')
#                        for label in axes.get_yticklabels():
#                            label.set_visible(False)
#                        axes.yaxis.set_major_formatter(NullFormatter())
                        self.__hide_yinfo(axes)
                    if (i + 1) < len(self._amounts) - (cols - 1):
                        axes.xaxis.get_major_formatter().hide_offset = True # need to do this because the twin axes x axis formatter overwrites the true axes x axis formatters
#                        self.__hide_xinfo(axes)
                except KeyError: pass # clever way of making this work regardless of _some_volumes

#    def _options_fired(self):
#        self.edit_traits(
#            view=View(
#                VGroup(
#                    HGroup(
#                        Item('style', style='custom'),
#                    ),
#                    HGroup(
#                        Item('separate_volumes', visible_when='object._some_volumes and not object.style=="Combined"'),
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
#                    Item('_timeseries',
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

    timepoints_units = TimeUnit
    volumes_units = VolumeUnit
    substances_units = SubstanceUnit
    concentrations_units = ConcentrationUnit
    
    @on_trait_change('timeseries')
    def _update_units(self):
        ''' Assumes all timepoints, amounts and volumes are of the same units respectively. '''
        self.timepoints_units = self.timeseries[0].timepoints_units
        if len(self._volumes) > 0:
            self.volumes_units = self._volumes[0].values_units
        if len(self._amounts) > 0:
            if self._amounts[0].values_type == 'Amount':
                self.substances_units = self._amounts[0].values_units
            else: # self._amounts[0].values_type == 'Concentration':
                self.concentrations_units = self._amounts[0].values_units
    
    def _timepoints_units_changed(self):
        for timeseries in self._timeseries:
            timeseries.timepoints = timeseries.timepoints.rescale(time_units[self.timepoints_units])
            timeseries.timepoints_units = self.timepoints_units
    
    def _volumes_units_changed(self):
        for timeseries in self._volumes:
            timeseries.values = timeseries.values.rescale(volume_units[self.volumes_units])
            timeseries.values_units = self.volumes_units
            
    def _substances_units_changed(self):
        for timeseries in self._amounts:
            if timeseries.values_type == 'Amount':
                timeseries.values = timeseries.values.rescale(substance_units[self.substances_units])
                timeseries.values_units = self.substances_units
    
    def _concentrations_units_changed(self):
        for timeseries in self._amounts:
            if timeseries.values_type == 'Concentration':
                timeseries.values = timeseries.values.rescale(concentration_units[self.concentrations_units])
                timeseries.values_units = self.concentrations_units
            

    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Item('edit_timeseries', show_label=False),
                    Item('style', style='custom'),
                    Item('separate_volumes', enabled_when='object._some_volumes and not object.style=="Combined"'),
#                    Item('plot_volumes', visible_when='len([timeseries for timeseries in object.timeseries if timeseries.values_type=="Volume"]) > 0'),
                ),
                HGroup(
                    Item('timepoints_units',
                        editor=time_units_editor,
                        visible_when='len(object._timeseries) > 0'
                    ),
                    Item('substances_units',
                        editor=substance_units_editor,
                        visible_when='[timeseries for timeseries in object._amounts if timeseries.values_type == "Amount"]'
                    ),
                    Item('concentrations_units',
                        editor=concentration_units_editor,
                        visible_when='[timeseries for timeseries in object._amounts if timeseries.values_type == "Concentration"]'
                    ),
                    Item('volumes_units',
                        editor=volume_units_editor,
                        visible_when='len(object._volumes) > 0'
                    ),
                    'abbreviated_units',
                ),
#                HGroup(
#                   'amounts_type', #TODO remove
#                   Item('concentration_units',
#                       editor=EnumEditor(values={'M':'1:M', 'mM':'2:mM', 'uM':'3:uM', 'pM':'4:pM', 'fM':'5:fM'}),
#                       visible_when='object.amounts_type=="Concentration"'),
#                   Item('volume_units',
#                       editor=EnumEditor(values={'L':'1:L', 'mL':'2:mL', 'uL':'3:uL', 'pL':'4:pL', 'fL':'5:fL'}),
#                       visible_when='len(object.volumes) > 0'),
#                ),
                HGroup(
                    'gridlines',
                    'figure_legend',
                    Item('individual_legends', visible_when='not object.style=="Combined"'),
                    Item('font_size',
                        editor=RangeEditor(mode='text')
                    ),
                    Spring(),
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
                    Item('_figure',
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
#                    Item('list_widget'),
#                    'print_SubplotParams',
                    show_labels=False,
                ),
                show_border=True,
                show_labels=False,
            ),
#            width=640, height=480,
            width=1024, height=768,
            resizable=True,
            title=self.window_title,
        )

#    print_SubplotParams = Button
#    def _print_SubplotParams_fired(self):
#        p = self._figure.subplotpars
#        print 'left=%s, right=%s, top=%s, bottom=%s, hspace=%s, wspace=%s' % (p.left, p.right, p.top, p.bottom, p.hspace, p.wspace)
    

    save_resized = Button

    def _save_resized_fired(self):
        resize_and_save_matplotlib_figure(self._figure)


    edit_timeseries = Button

    _timeseries_mapping = Property(List(Timeseries), depends_on='separate_volumes, timeseries')
    
    @cached_property
    def _get__timeseries_mapping(self):
#        from infobiotics.commons.traits.ui.values_for_enum_editor import values_for_EnumEditor
        if self.separate_volumes:
#            l = [(timeseries, timeseries.title) for timeseries in self.timeseries]
#            w = len(str(len(l)))
#            import string
#            d = dict((timeseries, '%s:%s' % (string.zfill(i + 1, w), title)) for i, (timeseries, title) in enumerate(l))
#            print d
#            return d
            return dict([(timeseries, ':%s' % timeseries.title) for timeseries in self.timeseries])
        else:
            return dict([(timeseries, ':%s' % timeseries.title) for timeseries in self.timeseries if timeseries.values_type != 'Volume'])

    def _edit_timeseries_fired(self):
        self.edit_traits(
            view=View(
                VGroup(
                    HGroup('separate_volumes'),
                    Item('_timeseries',
                        editor=SetEditor(
#                            values=dict([(timeseries, ':%s' % timeseries.title) for timeseries in self.timeseries]),
                            name='_timeseries_mapping',
                            can_move_all=True,
                            ordered=True,
                            left_column_title='Available Timeseries',
                            right_column_title='Selected Timeseries',
                        ),
                        show_label=False,
                    ),
                    show_border=True,
                ),
                title='Edit timeseries',
                resizable=True,
                buttons=['OK', 'Cancel']
            ),
            kind='livemodal',
        )
        self._update_figure()
        


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
        for timeseries in self._timeseries:
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
    from PyQt4.QtGui import qApp
    from mcss_results_widget import McssResultsWidget
    from PyQt4.QtCore import Qt
    
    argv = qApp.arguments()
#    argv.insert(1, '/home/jvb/dashboard/examples/modules/module1.h5')
    argv.insert(1, '/home/jvb/dashboard/examples/germination_09.h5')
    if len(argv) > 2:
        print 'usage: python timeseries_plot.py [h5file]'
        sys.exit(2)
    if len(argv) == 1:
#        shared.settings.register_infobiotics_settings()
        self = McssResultsWidget()
    elif len(argv) == 2:
        self = McssResultsWidget(filename=argv[1])

    self.ui.runs_list_widget.select(0)
    self.ui.runs_list_widget.select(1)
#    self.ui.species_list_widget.select(-1)
#    self.ui.species_list_widget.select(-2)
    for item in self.ui.species_list_widget.findItems("SIG1", Qt.MatchWildcard): item.setSelected(True)
    self.volumes_list_widget_item.setSelected(True)
    self.ui.compartments_list_widget.select(-1)
    self.ui.compartments_list_widget.select(-2)
    self.ui.compartments_list_widget.select(-3)

    self.every = 3600
    self.ui.timepoints_data_units_combo_box.setCurrentIndex(self.ui.timepoints_data_units_combo_box.findText('seconds'))
    
    self.ui.timepoints_display_units_combo_box.setCurrentIndex(self.ui.timepoints_display_units_combo_box.findText('milliseconds'))
#    self.ui.timepoints_display_units_combo_box.setCurrentIndex(self.ui.timepoints_display_units_combo_box.findText('minutes'))
#    self.ui.timepoints_display_units_combo_box.setCurrentIndex(self.ui.timepoints_display_units_combo_box.findText('hours'))

    self.ui.quantities_data_units_combo_box.setCurrentIndex(self.ui.quantities_data_units_combo_box.findText('molecules'))
#    self.ui.quantities_data_units_combo_box.setCurrentIndex(self.ui.quantities_data_units_combo_box.findText('picomoles'))
    
#    self.ui.quantities_display_type_combo_box.setCurrentIndex(self.ui.quantities_display_type_combo_box.findText('molecules'))
#    self.ui.quantities_display_type_combo_box.setCurrentIndex(self.ui.quantities_display_type_combo_box.findText('moles'))
    self.ui.quantities_display_type_combo_box.setCurrentIndex(self.ui.quantities_display_type_combo_box.findText('concentrations'))

#    self.ui.moles_display_units_combo_box.setCurrentIndex(self.ui.moles_display_units_combo_box.findText('femtomoles'))
#    self.ui.concentrations_display_units_combo_box.setCurrentIndex(self.ui.concentrations_display_units_combo_box.findText('femtomolar'))
    self.ui.concentrations_display_units_combo_box.setCurrentIndex(self.ui.concentrations_display_units_combo_box.findText('nanomolar'))
    
    self.ui.volumes_data_units_combo_box.setCurrentIndex(self.ui.volumes_data_units_combo_box.findText('microlitres'))
    
#    self.ui.volumes_display_units_combo_box.setCurrentIndex(self.ui.volumes_display_units_combo_box.findText('microlitres'))
    self.ui.volumes_display_units_combo_box.setCurrentIndex(self.ui.volumes_display_units_combo_box.findText('attolitres'))
    
    self.ui.average_over_selected_runs_check_box.setChecked(False)
    
#    runs, species, compartments = self.selected_items()
#    print runs
#    print species
#    print compartments
##    run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
#    _, _, _, averaging = self.options()
#    print averaging
#    timepoints_data_units, timepoints_display_units, quantities_data_units, quantities_display_type, quantities_display_units, volume, volumes_data_units, volumes_display_units = self.units()
#    print timepoints_data_units
#    print timepoints_display_units
#    print quantities_data_units
#    print quantities_display_type
#    print quantities_display_units
#    print volume
#    print volumes_data_units
#    print volumes_display_units
    
    self.plot()
    

if __name__ == '__main__':
    main()
