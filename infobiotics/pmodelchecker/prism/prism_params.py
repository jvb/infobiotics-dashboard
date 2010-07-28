from infobiotics.pmodelchecker.api import PModelCheckerParams
from enthought.traits.api import Str, Enum
import os.path

class PRISMParams(PModelCheckerParams):

    def _handler_default(self):
        from prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

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
    parameters.configure()
                        