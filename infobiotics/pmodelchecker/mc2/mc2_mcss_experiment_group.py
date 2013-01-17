from traitsui.api import Group, VGroup, Item

mc2_mcss_experiment_group = Group(
    Item('model_file', style='readonly'),
    Item('handler.model_format', visible_when='object.model_file.endswith(".xml")', label='XML type'),
#    Item('just_psystem', visible_when='object.model_format=="xml" or object.model_file.lower().endswith(".psxml")', label='Just initialise P system'),
    Item('duplicate_initial_amounts', visible_when='object.model_format=="SBML" or object.model_file.lower().endswith(".sbml")'),
    Item('max_time'),
    Item('log_interval'),
    Item('runs', label='Runs (number of samples)', style='readonly'),
    Item('data_file', style='readonly'),
#    Item('show_progress'),# not needed when using GUI
    Item('compress', label='Compress output'),
    Item('compression_level', visible_when='object.compress==True'),
    Item('handler.simulation_algorithm'),
    Item('seed', label='Random seed'),
)        


if __name__ == '__main__':
    execfile('mc2_params.py')
