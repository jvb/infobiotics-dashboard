from enthought.traits.ui.api import Group, VGroup, Item, Spring, HGroup

poptimizer_params_group = Group(
    VGroup(
        VGroup(
            Item('num_initials', label='Number of initial model files'),
            Item('initial_file', label='Prefix for initial model file names'),
            Item('target_obj_num', label='Number of target timeseries'), #FIXME should be redundant, but isn't yet
            Item('target_file', label='Prefix for target timeseries file names'),
            Item('nonfix_module_lib_file', label='Non-fixed module library'),
            Item('fix_module_lib_file', label='Fixed module library'),
            Item('molecules', label='Molecule names (colon-separated)'),
            Item('seednum', label='Random seed'),
            label='Input parameters',
        ),
        VGroup(
            HGroup(
                Item('maxtime', label='Simulation length'),
                Item('interval', label='Sampling interval'),
            ),
            Item('simu_runs', label='Ensemble size (simulation runs)'),
            Item('fitness_func_type', label='Fitness function'),
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
                    label='Parameter optimization',
                ),
#                layout='tabbed',
            ),
            label='Evaluation',
        ),
        layout='tabbed',
    ),
    Spring(),
)


if __name__ == '__main__':
    execfile('poptimizer_params.py')
    