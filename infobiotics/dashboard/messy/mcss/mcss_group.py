import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.ui.api import Group, VGroup, Item, FileEditor, TextEditor

group = Group(
    VGroup(
        Item('model_file'),
        Item('model_format', visible_when='object.model_file.endswith(".xml")', label='XML type'),
        Item('just_psystem', visible_when='object.model_format=="xml"', label='Just initialise P system'),
        Item('duplicate_initial_amounts', visible_when='object.model_format=="SBML" or object.model_file.lower().endswith(".sbml")'),
        Item('max_time'),
        Item('log_interval'),
        Item('runs'),
        Item('data_file'),
#        Item('show_progress'), #TODO popup showing stdout and stderr for each params program
        Item('compress', label='Compress output'),
        Item('compression_level', visible_when='object.compress==True'),
        Item('simulation_algorithm'),
        Item('seed', label='Random seed'),
        label='Required'
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
        Item('log_type', label='logging type'),
        Item('log_propensities', visible_when='object.log_type == "reactions"'),
        Item('log_volumes'),
        Item('log_steady_state'),
        Item('log_degraded'),
        Item('log_memory', label='log output to memory'),
        Item('dump'),
        label='Logging'
    ),
    
#    VGroup(
#        Item(label='Copy and paste the script below to reproduce this experiment.'),
#        Item('repr', show_label=False, style='custom', editor=TextEditor()), #TODO
#        label='script',
#    ),
    
    layout='tabbed'
)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    