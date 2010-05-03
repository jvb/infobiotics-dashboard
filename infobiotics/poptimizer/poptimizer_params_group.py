from enthought.traits.ui.api import Group, VGroup, Item

poptimizer_params_group = Group(
    VGroup(
        Item('target_file', label='Filename prefix for target files'),
        Item('target_obj_num', label='Number of target timeseries files'),
        Item('initial_file', label='Filename prefix for initial files'),
        Item('num_initials', label='Number of initial model files'),
        Item('nonfix_module_lib_file', label='Non-fixed module library'),
        Item('fix_module_lib_file', label='Fixed module library'),
        Item('molecules', label='Molecule names (colon-separated)'),
        Item('seednum', label='Random seed'),
        label='Input parameters',
    ),
    VGroup(
        Item('fitness_func_type', label='Fitness function'),
#            Item('maxtime', label='Simulation length (time)'),
#            Item('interval', label='Sampling interval (time)'),
        Item('simu_runs', label='Ensemble size (simulation runs)'),
        label='Evaluation',
    ),
    Group(
        VGroup(
            Item('maxmodulesno', label='Maximum number of modules in a model'),
            Item('popsize', label='Population size'),
            Item('maxgeno', label='Number of generations'),
            label='Structure optimization with Genetic Algorithm',
        ),
        VGroup(
            Item('para_opti_algo', label='Optimization algorithm'),
            Item('percent_paraopti', label='Proportion of population to optimize'),
            Item('popsize', label='Population size', visible_when='object.para_opti_algo_ != "CMA-ES"'),
            Item('maxgeno', label='Generations'),
#            Item('DE_psize', visible_when='object.para_opti_algo_=="DE"'),
#            Item('DE_maxgeno', visible_when='object.para_opti_algo_=="DE"'),
#            Item('GA_psize', visible_when='object.para_opti_algo_=="GA"'),
#            Item('GA_maxxo', visible_when='object.para_opti_algo_=="GA"'),
#            Item('EDA_psize', visible_when='object.para_opti_algo_=="EDA"'),
#            Item('EDA_maxgeno', visible_when='object.para_opti_algo_=="EDA"'),
#            Item('CMAES_maxgeno', visible_when='object.para_opti_algo_=="CMA-ES"'),
            label='Parameter optimization',
        ),
#        orientation='horizontal',
        layout='tabbed',
    ),
)


if __name__ == '__main__':
    execfile('poptimizer_params.py')