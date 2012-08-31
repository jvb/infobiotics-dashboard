from infobiotics.core.params_handler import ParamsHandler
from poptimizer_params_group import poptimizer_params_group
from enthought.traits.api import Trait, on_trait_change, Str
from infobiotics.commons.traits.api import IntGreaterThanZero
from poptimizer_preferences import POptimizerParamsPreferencesPage

class POptimizerParamsHandler(ParamsHandler):

    def _params_group_default(self):
        return poptimizer_params_group
    
    preferences_page = POptimizerParamsPreferencesPage()
    
    id = 'POptimizerParamsHandler'

    help_urls = [
        ('Quick start', 'http://www.infobiotics.org/infobiotics-workbench/quickStart/optimization.html'),
        ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/optimisation.html'),
        ('Automatic Discovery of Pulse Generators example', 'http://www.infobiotics.org/infobiotics-workbench/models/IFFL/FFLpulse.html'),
        ('Documentation', 'http://www.infobiotics.org/infobiotics-workbench/optimisation/optimisation_Claudio.html'),
    ]
    
    filters = [ # used to create wildcard and filter traits for FileDialog and OpenFileDialog respectively
        ('Experiment parameters', ['*.params', '*.xml']),
        ('All files', ['*']),
    ]


    # 'initial_file' and 'target_file' parameters are prefixes for file names that end in <number>.txt, e.g. prefix1.txt.
    
    @on_trait_change('model:initial_file, model:target_file')
    def warn_about_prefix(self, name, old, new):
        if '.' in new: 
            from enthought.traits.ui.message import auto_close_message
            auto_close_message("\n   Please ensure '%s' is only a prefix for a file name   \n   that ends in 1.txt or similar, e.g. prefix1.txt   \n" % new,
                title='Caution',
                time=5.0,
            )

    
    # pattern allowing full names for Enum items on model using Trait and dict

    def init(self, info):
        super(POptimizerParamsHandler, self).init(info)
        # sync Trait shadow values from handler to Enum in model
        self.sync_trait('para_opti_algo_', info.object, alias='para_opti_algo', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
        self.sync_trait('fitness_func_type_', info.object, alias='fitness_func_type', mutual=False) # ditto

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

    fitness_func_type_reversed = {
        'RandomWeightedSum' : 'Random-weighted sum',
        'EqualWeightedSum' : 'Equal-weighted sum',
    }
    
    para_opti_algo_reversed = {
        'DE' : 'Differential Evolution',
        'GA' : 'Genetic Algorithm',
        'EDA' : 'Estimation of Distribution Algorithm',
        'CMA-ES' : 'Covariance Matrix adaptation - Evolutionary Strategies',
    }

    # set Trait in handler using full name from reversed dict 
    # because we can't set shadow trait
    
    def object_para_opti_algo_changed(self, info):
        self.para_opti_algo = self.para_opti_algo_reversed[info.object.para_opti_algo]

    def object_fitness_func_type_changed(self, info):
        self.fitness_func_type = self.fitness_func_type_reversed[info.object.fitness_func_type]


if __name__ == '__main__':
    execfile('poptimizer_params.py')
    
