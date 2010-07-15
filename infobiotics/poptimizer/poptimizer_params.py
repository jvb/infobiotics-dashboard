from infobiotics.common.api import Params, ParamsRelativeFile
from enthought.traits.api import Str, Int, Long, Bool, Range, on_trait_change, Trait #TODO remove Trait
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
    
    _parameters_name = 'poptimizer'
    _parameter_set_name = 'poptimizer'
    
    target_file = Str(desc='a filename for target time series data')
    target_obj_num = Int(1, desc='the number of objects in the input time series data')
    initial_file = Str(desc='a filename for non-zero initial values settings of some objects')
    num_initials = Int(desc='the number of files for initial values')
    nonfix_module_lib_file = ParamsRelativeFile(exists=True, desc='a filename for the non-fixed module library to evolve models')
    fix_module_lib_file = ParamsRelativeFile(desc='a filename for the fixed module library')
    molecules = Str(desc='the possible values for all variables when instantiating a module in the library (colon-separated list of strings)')
    seednum = Long(desc='the seed number to initialize the random generator')
    
    maxtime = FloatGreaterThanZero(desc='the total simulation time of the input data')
    interval = FloatGreaterThanZero(desc='the interval time between two sampling data points of input data')
    maxmodulesno = IntGreaterThanZero(10, desc='the maximum number of modules contain in one model')
    simu_runs = IntGreaterThanZero(20, desc='the number of simulations when running the simulator to calculate the fitness of one individual')

    #TODO change these to Enum and move Trait to handler
#    fitness_func_type = Str(desc='the fitness function chosen to do the model quality evaluation')
    fitness_func_type = Trait(
        'Random-weighted sum',
        {
            'Random-weighted sum' : 'RandomWeightedSum',
            'Equal-weighted sum' : 'EqualWeightedSum'
        },
        desc='the fitness function chosen to do the model quality evaluation'
    )
    
    para_opti_algo = Trait(
        'Genetic Algorithm',
        {
            'Differential Evolution' : 'DE',
            'Genetic Algorithm' : 'GA',
            'Estimation of Distribution Algorithm' : 'EDA',
            'Covariance Matrix adaptation - Evolutionary Strategies' : 'CMA-ES',
        },
        desc='the algorithm chosen to do the model parameter optimization'
    )
    percent_paraopti = Range(0.0, 1.0, 0.1, desc='the percentage of the individuals in the model population on which to do the parameter optimization')
    
    maxgeno = IntGreaterThanZero(50, desc='the maximum number of generations to evolve the best parameter set')
    popsize = IntGreaterThanZero(50, desc='the population size for a generation')
    # below not shown
    DE_psize = IntGreaterThanZero(50, desc='the population size for DE parameter optimization')
    DE_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with DE')
    GA_psize = IntGreaterThanZero(50, desc='the population size for GA parameter optimization')
    GA_maxxo = IntGreaterThanZero(950, desc='the number of multi_parent crossover performed in GA parameter optimization')
    EDA_psize = IntGreaterThanZero(50, desc='the population size for EDA parameter optimization')
    EDA_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with EDA')
    CMAES_maxgeno = IntGreaterThanZero(20, desc='the maximum number of generations to evolve the best parameter set with CMA-ES')
    
    # below not shown
    show_progress = Bool(False, desc='whether to show progress of the optimization procedure')
    debug_mode = Bool(False, desc='print information to stdout useful for code debug')

    def parameter_names(self):
        return [
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
            'maxgeno',
            'popsize',
            'DE_psize',
            'DE_maxgeno',
            'GA_psize',
            'GA_maxxo',
            'EDA_psize',
            'EDA_maxgeno',
            'CMAES_maxgeno',
            'show_progress',
            'debug_mode',
        ]
    
    def _maxgeno_default(self):
        if self.para_opti_algo_ == 'GA':
            return 950
        elif self.para_opti_algo_ == 'DE':
            return 20
        elif self.para_opti_algo_ == 'EDA':
            return 20
        elif self.para_opti_algo_ == 'CMA-ES':
            return 20        
    
    def _para_opti_algo__changed(self, para_opti_algo_):
        if para_opti_algo_ == 'GA':
            self.popsize = self.GA_psize
            self.maxgeno = self.GA_maxxo
        elif para_opti_algo_ == 'DE':
            self.popsize = self.DE_psize
            self.maxgeno = self.DE_maxgeno
        elif para_opti_algo_ == 'EDA':
            self.popsize = self.EDA_psize
            self.maxgeno = self.EDA_maxgeno
        elif para_opti_algo_ == 'CMA-ES':
            self.maxgeno = self.CMAES_maxgeno
    
    @on_trait_change('DE_maxgeno', 'GA_maxxo', 'EDA_maxgeno', 'CMAES_maxgeno')
    def update_maxgeno(self, maxgeno):
        self.maxgeno = maxgeno
        
    def _maxgeno_changed(self, maxgeno):
        self.DE_maxgeno = self.GA_maxxo = self.EDA_maxgeno = self.CMAES_maxgeno = maxgeno

    def _popsize_changed(self, population_size):
        self.DE_psize = self.GA_psize = self.EDA_psize = population_size
        
    def _maxmodulesno_changed(self, num_modules):
        self.popsize = 10 * num_modules
        
    def _nonfix_module_lib_file_changed(self, library): pass #TODO update maxmodulesno, maxgeno, popsize


if __name__ == '__main__':
    parameters = POptimizerParams()
#    parameters.load('test/fourinitial/four_initial_inputpara.xml')
#    parameters.load('test/promoter/all_para_promoter_inputpara.xml')
#    parameters.load('test/threegene/threegene_inputpara.xml')
    parameters.configure()
    