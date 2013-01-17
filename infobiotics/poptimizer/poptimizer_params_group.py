from traitsui.api import Group, VGroup, Item, Spring, HGroup, TextEditor
from traits.api import TraitError
from infobiotics.commons.traits_.int_greater_than_zero import IntGreaterThanZero

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
                Item('maxtime', label='Max time'),
                Item('interval', label='Log interval'),
            ),
            Item('simu_runs', label='Ensemble size (simulation runs)'),
            Item('handler.fitness_func_type', label='Fitness function'),
            Group(
                VGroup(
                    Item('maxmodulesno', label='Maximum number of modules in a model'),
                    Item('popsize', label='Population size'),
                    Item('maxgeno', label='Generations'),
                    label='Structure optimization with Genetic Algorithm', # POptimizer2 will have more structure optimization algorithms than GA
                ),
                VGroup(
                    Item('handler.para_opti_algo', label='Optimization algorithm'),
                    Item('percent_paraopti', label='Proportion of population to optimize'),
                    VGroup(
                        Item('DE_psize', label='Population size'),
                        Item('DE_maxgeno', label='Generations'),
                        visible_when='object.para_opti_algo == "DE"',
                    ),
                    VGroup(
                        Item('GA_psize', label='Population size'),
                        Item('GA_maxxo', label='Generations'),
                        visible_when='object.para_opti_algo == "GA"',
                    ),
                    VGroup(
                        Item('EDA_psize', label='Population size'),
                        Item('EDA_maxgeno', label='Generations'),
                        visible_when='object.para_opti_algo == "EDA"',
                    ),
                    VGroup(
                        Item('CMAES_maxgeno', label='Generations'),
                        visible_when='object.para_opti_algo == "CMA-ES"',
                    ),
                    label='Parameter optimization',
                ),
            ),
            label='Evaluation',
        ),
        layout='tabbed',
    ),
    Spring(),
)


if __name__ == '__main__':
    execfile('poptimizer_params.py')
    