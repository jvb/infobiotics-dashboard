from enthought.traits.ui.api import Group, VGroup, Item

mc2_mcss_experiment_group = Group(
    VGroup(
        Item('model_file', style='readonly'),
        Item('model_format', visible_when='object.model_file.endswith(".xml")', label='XML type'),
#        Item('just_psystem', visible_when='object.model_format=="xml" or object.model_file.lower().endswith(".psxml")', label='Just initialise P system'),
        Item('duplicate_initial_amounts', visible_when='object.model_format=="SBML" or object.model_file.lower().endswith(".sbml")'),
        Item('max_time'),
        Item('log_interval'),
        Item('runs', style='readonly'),
        Item('data_file', style='readonly'),
#        Item('show_progress'),# not needed when using GUI
        Item('compress', label='Compress output'),
        Item('compression_level', visible_when='object.compress==True'),
        Item('simulation_algorithm'),
        Item('seed', label='Random seed'),
#        label='Required'
    ),
#    
#    VGroup(
#        Item('periodic_x', label='Periodic X dimension'),
#        Item('periodic_y', label='Periodic Y dimension'),
#        Item('periodic_z', label='Periodic Z dimension'),
#        Item('division_direction', label='Direction of cell division'),
#        Item('keep_divisions', label='Keep dividing cells'),
#        Item('growth_type', label='Volume growth type'),
#        label='Spatial'
#    ),
#    
#    VGroup(
#        Item('log_type', label='logging type'),
#        Item('log_propensities', visible_when='object.log_type == "reactions"'),
#        Item('log_volumes'),
#        Item('log_steady_state'),
#        Item('log_degraded'),
##        Item('log_memory', label='log output to memory'),
##        Item('dump'),
#        label='Logging'
#    ),
           
    VGroup(
         Item('program', label='Path to mcss'),
         label='mcss'
    ),
    layout='tabbed'
)        


if __name__ == '__main__':
    execfile('mc2_params.py')
