from infobiotics.common.api import Params, ParamsRelativeFile
from enthought.traits.api import Str, Int, Long, Bool, Range, on_trait_change, Enum, Undefined
from infobiotics.commons.traits.api import FloatGreaterThanZero, IntGreaterThanZero
from infobiotics.poptimizer.poptimizer_preferences import POptimizerParamsPreferencesHelper

class POptimizerParams(Params):
    
    def _handler_default(self):
        from infobiotics.poptimizer.poptimizer_params_handler import POptimizerParamsHandler
        return POptimizerParamsHandler(model=self)
        
    def _preferences_helper_default(self):
        helper = POptimizerParamsPreferencesHelper()
        return helper

    executable_name = 'poptimizer'
    
    _parameters_name = 'POptimizerParameters'
    _parameter_set_name = 'POptimizerParameters'
    
    num_initials = Int(1, desc='the number of initial models to use')
    initial_file = ParamsRelativeFile(auto_set=False, enter_set=True, desc="the prefix for initial model file names, to which\ a number and '.txt' will be added, e.g. prefix1.txt")
    target_file = ParamsRelativeFile(auto_set=False, enter_set=True, desc="the prefix for target timeseries files, to which\ a number and '.txt' will be added, e.g. prefix1.txt")
    target_obj_num = Int(1, #FIXME should be redundant, but isn't yet 
        desc="""the number of objects with target timeseries.
An example target timeseries file with 2 objects should look like: 

    time protein1 rna1
    0 0 0
    10 71.2679 2.208
    20 113.7169 1.3306
    30 132.9971 0.8434
    40 140.0816 0.5794
    50 141.2028 0.4495
        """,
    )
    nonfix_module_lib_file = ParamsRelativeFile(exists=True, desc='a filename for the non-fixed module library to evolve models')
    fix_module_lib_file = ParamsRelativeFile('Null', desc="a filename for the fixed module library (should be 'Null' if empty)")
    molecules = Str#TODO(desc='the possible values for all variables when instantiating a module in the library (colon-separated list of strings)')

    seednum = Long(desc='the seed number used to initialize the random generator')
    
    maxtime = FloatGreaterThanZero(desc='the total simulation time of the input data')
    interval = FloatGreaterThanZero(desc='the interval time between two sampling data points of input data')
    maxmodulesno = IntGreaterThanZero(Undefined, desc='the maximum number of modules contain in one model') #TODO
    simu_runs = IntGreaterThanZero(20, desc='the number of simulations when running the simulator to calculate the fitness of one individual')

    # structure optimisation
    fitness_func_type = Enum(['RandomWeightedSum','EqualWeightedSum'], desc='the fitness function chosen to do the model quality evaluation')
    para_opti_algo = Enum(['DE','GA','EDA','CMA-ES'], desc='the algorithm chosen to do the model parameter optimization')
    percent_paraopti = Range(0.0, 1.0, 0.1, desc='the percentage of the individuals in the model population on which to do the parameter optimization')
    maxgeno = IntGreaterThanZero(50, desc='the maximum number of generations to evolve the best model')
    popsize = IntGreaterThanZero(50, desc='the population size for a generation\n(recommend 10x the maximum number of modules)')
    
    # parameter optmisation
    DE_psize = IntGreaterThanZero(50, desc='the population size for DE parameter optimization')
    DE_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with DE')
    GA_psize = IntGreaterThanZero(50, desc='the population size for GA parameter optimization')
    GA_maxxo = IntGreaterThanZero(950, desc='the number of multi_parent crossover performed in GA parameter optimization')
    EDA_psize = IntGreaterThanZero(50, desc='the population size for EDA parameter optimization')
    EDA_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with EDA')
    CMAES_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with CMA-ES')
    # above not shown in favour of parameter_optmisation_generations and parameter_optmisation_population_size in handler
    
    # below not shown
    show_progress = Bool(False, desc='whether to show progress of the optimization procedure')
    debug_mode = Bool(False, desc='print information to stdout useful for code debug')

    def parameter_names(self):
        parameter_names = [
            'target_file',
            'target_obj_num',
            'initial_file',
            'num_initials',
            'nonfix_module_lib_file',
            'fix_module_lib_file',
            'molecules',
            'seednum',
            'maxtime',
            'interval',
            'maxmodulesno',
            'simu_runs',
            'fitness_func_type',
            'para_opti_algo',
            'percent_paraopti',
#            'show_progress',
#            'debug_mode',
            'maxgeno',
            'popsize',
#            'DE_psize',
#            'DE_maxgeno',
#            'GA_psize',
#            'GA_maxxo',
#            'EDA_psize',
#            'EDA_maxgeno',
#            'CMAES_maxgeno',
        ]
        if self.para_opti_algo == 'GA':
            return parameter_names + [
                'GA_psize',
                'GA_maxxo',
            ]
        elif self.para_opti_algo == 'DE':
            return parameter_names + [
                'DE_psize',
                'DE_maxgeno',
            ]
        elif self.para_opti_algo == 'EDA':
            return parameter_names + [
                'EDA_psize',
                'EDA_maxgeno',
            ]
        elif self.para_opti_algo == 'CMA-ES':
            return parameter_names + [
#                'DE_psize',
                'CMAES_maxgeno',
            ]
        else:
            raise ValueError("para_opti_algo not in ('GA', 'DE', 'EDA', 'CMA-ES')")
        
#    def _nonfix_module_lib_file_changed(self, library): pass #TODO update maxmodulesno, maxgeno, popsize

    
if __name__ == '__main__':
    parameters = POptimizerParams()
    parameters.configure()
    