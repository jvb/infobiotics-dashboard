from infobiotics.core.traits.params_relative_file import ParamsRelativeFile
from infobiotics.core.params import Params
from enthought.traits.api import Enum, Bool, Range, Float, Int, String, Str
from infobiotics.commons.traits.api import IntGreaterThanZero, RelativeFile
from infobiotics.mcsscmaes.mcsscmaes_preferences import McssCmaesParamsPreferencesHelper

class McssCmaesParams(Params):

    def _handler_default(self):
        from infobiotics.mcsscmaes.api import McssCmaesParamsHandler
        return McssCmaesParamsHandler(model=self)

    def _preferences_helper_default(self):
        helper = McssCmaesParamsPreferencesHelper()
        return helper

    executable_name = 'mcsscmaes' #TODO used by what?
    
    _parameters_name = 'mcsscmaes'
    _parameter_set_name = 'McssCmaesParameters'

    population_size = IntGreaterThanZero(desc="number of individuals in population (lambda)")
    num_parameters = IntGreaterThanZero(desc="number of parameters (N)")
    max_iterations = Range(low= -1.0, desc="maximum number of iterations (stopMaxIter)")
    max_function_evals = Float(-1.0, desc="maximum number of fitness function evaluations (stopMaxFunEvals)")
    stop_fitness = Float(0.0, desc="stop if fitness is less than given value (stopFitness)")
    stop_fitness_diff = Float(1.0E-12, desc="stop if fitness differences are less than given value (stopTolFun)")
    stop_fitness_diff_best = Float(1.0E-13, desc="stop if fitness differences of best individuals are less than given value (stopTolFunHist)")
    stop_step_size = Float(0.0, desc="stop if parameter steps are less than given value (stopTolX)")
    stop_sd = Float(1.0E3, desc="stop if standard deviation is greater than given value (stopTolUpXFactor)")
    seed = Range(low=0, desc="random number seed (seed)")
    max_eigen_decomposition_time = Float(1.0, desc="maximum CPU time fraction for eigensystem decomposition (maxTimeFractionForEigendecompostion)")
    updatecov = Float(-1.0, desc="number of generations before updating eignesystem (updatecov)")
    updatecov_multiplier = Float(1.0, desc="multiplier for updatecov (fac*updatecov)")
    resume_distribution = Str("_no_", desc="filename of restart distribution to read (resume)") #TODO ParamsRelativeFile?
    used_parameter_file = Str("non", desc="filename to saved parameters actually used to (actparcmaes.par)") #TODO ParamsRelativeFile?
    weights = Enum(['log', 'linear', 'equal'], desc="(weights)")
    mu = Int(-1, desc="(mu)")
    fac_cs = Float(-1.0, desc="(fac*cs)")
    fac_damps = Float(-1.0, desc="(fac*damps)")
    ccumcov = Float(-1.0, desc="(ccumcov)")
    mucov = Float(-1.0, desc="(mucov)")
    fac_ccov = Float(-1.0, desc="(fac*ccov)")
    diagonal_covariance_matrix = Float(0.0, desc="(diagonalCovarianceMatrix)")
    fac_max_func_evals = Float(1.0, desc="(fac*maxFunEvals)")

    function_file = ParamsRelativeFile(exists=True,
        filter=[
            'Shared object (*.so)',
            'All files (*)'
        ],
        desc="file containing user defined functions")
    initial_x = Enum(['random', 'user', 'fixed'], desc="initial optimisation starting point")
    mcss_parameter_file = ParamsRelativeFile(exists=True,
        filter=[
            'mcss parameter files (*.params)',
            'All files (*)'
        ],
        desc="mcss parameter filename")
    parallel_runs = Bool(True, desc="perform individual mcss runs in parallel")
    lower_bound = Float(0.0, desc="lower bounds for parameter values")
    upper_bound = Float(1.0, desc="upper bounds for parameter values")
    mcss_executable = RelativeFile('mcss', executable=True, desc="mcss executable")
    column_separator = String(' ', minlen=1, maxlen=1, desc="separator for input data columns, 1 character wide (0 < len <= 1)")
    target_data_file = ParamsRelativeFile(exists=True, desc="file containing target data")
    data_file = RelativeFile('cmaes.h5', writable=True, desc="file to save optimisation results to")
    compress = Bool(True, desc="compress hdf5 output")
    compression_level = Range(0, 9, 9, desc="hdf5 compression level (0-9; 9=best)")
#    show_progress = Bool(False, desc="output current log interval to screen")
    runs = Range(low=0, desc="number of simulation runs to perform for each individual (overrides mcss runs parameter)")
    
    def parameter_names(self): #TODO why isn't this a trait?
        return ['population_size', 'num_parameters', 'max_iterations', 'max_function_evals', 'stop_fitness', 'stop_fitness_diff', 'stop_fitness_diff_best', 'stop_step_size', 'stop_sd', 'seed', 'max_eigen_decomposition_time', 'updatecov', 'updatecov_multiplier', 'resume_distribution', 'used_parameter_file', 'weights', 'mu', 'fac_cs', 'fac_damps', 'ccumcov', 'mucov', 'fac_ccov', 'diagonal_covariance_matrix', 'fac_max_func_evals', 'function_file', 'initial_x', 'mcss_parameter_file', 'parallel_runs', 'lower_bound', 'upper_bound', 'mcss_executable', 'column_separator', 'target_data_file', 'data_file', 'compress', 'compression_level',
#                'show_progress', 
                'runs', ]


if __name__ == '__main__':
    parameters = McssCmaesParams()

#    print parameters.directory
#    
#    function_file_trait_handler = parameters.trait('function_file').handler
#    print function_file_trait_handler.directory
#    
#    column_separator_trait_handler = parameters.trait('column_separator').handler
    
#    parameters.edit()
#    parameters.save()
    parameters.configure()
    
