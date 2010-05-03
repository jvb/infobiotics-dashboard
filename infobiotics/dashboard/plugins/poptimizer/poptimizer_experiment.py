# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: experiment.py 411 2010-01-25 18:03:26Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/poptimizer/experiment.py $
# $Author: jvb $
# $Revision: 411 $
# $Date: 2010-01-25 18:03:26 +0000 (Mon, 25 Jan 2010) $

from infobiotics.shared.traits_imports import *
from infobiotics.dashboard.plugins.experiments.params_experiment import *
from poptimizer_experiment_handler import POptimizerExperimentHandler


class POptimizerExperiment(ParamsExperiment):
    
    handler = POptimizerExperimentHandler
    name = 'POptimizer'
        
    program = '/usr/bin/poptimizer'
    parameters_name = 'poptimizer'
    parameter_set_name = 'POptimizerParameters'

    target_file = Str(desc='a filename for target time series data')
    target_obj_num = Int(1, desc='the number of objects in the input time series data')
    initial_file = Str(desc='a filename for non-zero initial values settings of some objects')
    num_initials = Int(desc='the number of files for initial values')
    nonfix_module_lib_file = File(exists=True, desc='a filename for the non-fixed module library to evolve models')
    fix_module_lib_file = File(desc='a filename for the fixed module library')
    molecules = Str(desc='the possible values for all variables when instantiating a module in the library (colon-separated list of strings)')
    seednum = Long(desc='the seed number to initialize the random generator')
    
    maxtime = FloatGreaterThanZero(desc='the total simulation time of the input data')
    interval = FloatGreaterThanZero(desc='the interval time between two sampling data points of input data')
    maxmodulesno = IntGreaterThanZero(10, desc='the maximum number of modules contain in one model')
    simu_runs = IntGreaterThanZero(20, desc='the number of simulations when running the simulator to calculate the fitness of one individual')

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

    def has_valid_parameters(self): return False #TODO

    def perform(self): pass #TODO

    
if __name__ == '__main__':
    self = POptimizerExperiment()
    self.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/poptimizer/fourinitial/four_initial_inputpara.xml')
#    self.configure_traits()
    self.configure()
