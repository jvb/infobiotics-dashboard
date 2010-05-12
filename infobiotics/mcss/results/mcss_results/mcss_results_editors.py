from infobiotics.shared.traits_imports import *

    
#TODO TabularEditor


class McssResultsTableEditor(TableEditor):
    editable=False
    sortable=True
#    show_lines=False
    selection_mode='rows'
    auto_size=True
#    show_column_labels=False


speciesTableEditor = McssResultsTableEditor(
    columns=[
        ObjectColumn(name='name'),
    ],
    selected='object.selected_species',
)


compartmentsTableEditor = McssResultsTableEditor(
    columns=[
#        ObjectColumn(name='parent.name', label='Parent'),
        ObjectColumn(name='name'),
        ObjectColumn(name='compartment_x_position', label='X'),
        ObjectColumn(name='compartment_y_position', label='Y'),
        ObjectColumn(name='compartment_z_position', label='Z'),
    ],
    show_column_labels=True,
    selected='object.selected_compartments',
)                                         


runsTableEditor = McssResultsTableEditor(
    columns=[
        ObjectColumn(name='run_number', label='Number'),
    ],
    selected='object.selected_runs',
)


# needed as workaround for bug when attempting cols > 3 (see 'plot_type' in McssResults) 
plot_type_editor = EnumEditor(
    cols=4,
    values={
        'Timeseries'          :'1:Timeseries',
        'Surface'             :'2:Surface',
        'Histogram'           :'3:Histogram',
        'Continuous Histogram':'4:Continuous Histogram',
    },
)
