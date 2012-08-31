from infobiotics.shared.traits_imports import * 
from infobiotics.dashboard.mcss_results.mcss_results_editors import *


data_group = VGroup(
#    HSplit(
    HGroup(
        VGroup(
#            Item('species', 
            Item('object.simulation.species', 
                 editor=speciesTableEditor, 
                 enabled_when='object.summary_species=="selected"',
                 show_label=False,
            ),
            label='Species',
        ),
        VGroup(
#            Item('compartments', 
            Item('object.simulation.compartments', 
                 editor=compartmentsTableEditor,
                 enabled_when='object.summary_position=="in selected compartments"',
                 show_label=False,
            ),
            label='Compartments',
        ),
        VGroup(
#            Item('runs', 
            Item('object.simulation.runs', 
                 editor=runsTableEditor,
                 enabled_when='object.average_runs_which=="selected"',
                 show_label=False,
            ),
            label='Runs',
        ),
    ),
)    

    
timepoints_group = HGroup(
    Label('From'),
    Item('from_', label='From', show_label=False),
    Label('to'),
    Item('to', show_label=False),
    Label('every'),
    Item('every', 
        editor=RangeEditor(
            low_name='_every_low', 
            high_name='_every_high', 
            mode='spinner'
        ),
        show_label=False
    ),
    HGroup(
        Label('x'),
        Item('log_interval', show_label=False, style='readonly'), 
        Item('units', show_label=False, style='readonly'), 
        Spring()
    ),
    label='Timepoints',
)


data_options_group = VGroup(
    HGroup(
        Label('Average'),
        Item('average_runs', show_label=False),
        Item('average_runs_which', show_label=False),
        Label('runs'),
        Spring(),
    ),
    HGroup(
        Label('Summarise'),
        Item('plot_summary', show_label=False),
        Label('by'),
        Item('summary_type', show_label=False), # averging/summing
        Label('the quantities of'),
        Item('summary_species', show_label=False), # each/all
        Label('species'),
        Item('summary_position', show_label=False),
    ),
    label='Data options',
)


plot_type_group = VGroup(
    HGroup(
        Item('plot_type', style='custom', editor=plot_type_editor, show_label=False),
        Spring(),
    ),
    label='Plot type',
)


plot_options_group = VGroup(
    Item('plot_quantities', label='Plot quantities as'),
    Item('plot_volumes'),
    Item('timeseries_options', visible_when='object.plot_type=="Timeseries"', style='custom'),# show_label=False),
    Item('surface_options', visible_when='object.plot_type=="Surface"', style='custom', show_label=False),
    Item('histogram_options', visible_when='object.plot_type=="Histogram"', style='custom', show_label=False),
    Item('continuous_histogram_options', visible_when='object.plot_type=="Continuous Histogram"', style='custom', show_label=False),
    label='Plot options',
)
