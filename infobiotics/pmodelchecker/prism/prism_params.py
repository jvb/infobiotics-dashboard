from infobiotics.pmodelchecker.pmodelchecker_params import PModelCheckerParams
from enthought.traits.api import Str
from prism_preferences import PREFERENCES_PATH

class PRISMParams(PModelCheckerParams):

    def __handler_default(self):
        from infobiotics.pmodelchecker.prism.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

    def _preferences_helper_default(self):
        from infobiotics.pmodelchecker.prism.prism_preferences import PRISMParamsPreferencesHelper
        return PRISMParamsPreferencesHelper()

    _preferences_path = Str(PREFERENCES_PATH) # otherwise 'pmodelchecker' set from executable_name in Params

    _parameter_set_name = 'prism'

    model_checker = 'PRISM'
    results_file = 'results.psm'
    temporal_formulas = 'temporal_formulas.csl'
    
    def parameter_names(self):
        ''' Returns the subset of parameter names required for a particular 
        PRISMExperiment. '''
        if self.task == 'Translate':
            return [
                'model_checker',
                'model_specification',
                'PRISM_model',
                'task',
            ]
        else:
            return [
                'model_checker',
                'model_specification',
                'PRISM_model',
                'model_parameters',
                'temporal_formulas',
                'task',
                'confidence',
                'precision',
                'results_file',
                'states_file',
                'transitions_file',
                'number_samples',
            ]    


if __name__ == '__main__':
    parameters = PRISMParams()
#    print 'executable', parameters.executable
    parameters.configure()
                        
