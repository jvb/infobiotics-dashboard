from enthought.traits.ui.api import (
    Group, VGroup, Item, HGroup, TextEditor,
)

mcss_params_group = Group(
    VGroup(
        VGroup(
            Item('model_file'),
            HGroup(
                Item('handler.model_format', 
                    label='XML type',
                    visible_when='object.model_file.endswith(".xml")',
                ),
                Item('just_psystem', visible_when='handler.model_format_ != "sbml"', label='Just initialise P system'),
                Item('duplicate_initial_amounts', visible_when='handler.model_format_ == "sbml"'),
            ),
            label='P system model',
        ),
        VGroup( 
            Item('max_time'),
            Item('log_interval'),
            Item('runs'),
            Item('data_file'),
    #        Item('show_progress'), #TODO popup showing stdout and stderr for each params program
            Item('compress', label='Compress output'),
            Item('compression_level', enabled_when='object.compress==True'),
            Item('handler.simulation_algorithm'),
            Item('seed', label='Random seed'),
            label='Simulation',
        ),
        label='Input'
    ),

    VGroup(
        Item('log_type', label='Logging type'),
        Item('log_propensities', enabled_when='object.log_type == "reactions"'),
        Item('log_volumes'),
        Item('log_steady_state'),
        Item('log_degraded'),
        Item('log_memory', label='Log output to memory'),
        Item('dump'),
        label='Output'
    ),
    
    VGroup(
        Item('periodic_x', label='Periodic X dimension'),
        Item('periodic_y', label='Periodic Y dimension'),
        Item('periodic_z', label='Periodic Z dimension'),
        Item('division_direction', label='Direction of cell division'),
        Item('keep_divisions', label='Keep dividing cells'),
        Item('growth_type', label='Volume growth type'),
        label='Spatial'
    ),
    
    VGroup(
        Item(label='Copy and paste the script below to reproduce this experiment.'),
        Item('repr', show_label=False, style='custom', editor=TextEditor()), #TODO
        label='script',
    ),
    
    layout='tabbed',
)
