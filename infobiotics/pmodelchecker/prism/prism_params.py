from infobiotics.pmodelchecker.api import PModelCheckerParams
from enthought.traits.api import Str, Enum

class PRISMParams(PModelCheckerParams):

    def _handler_default(self):
        from prism_params_handler import PRISMParamsHandler
#        from infobiotics.pmodelchecker.prism.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

    _parameter_set_name = 'prism'

    model_checker = 'PRISM'
    results_file = 'results.psm'

    def translate_model_specification(self):
        super(PRISMParams, self).translate_model_specification(self._cwd, self.model_specification, self.PRISM_model)
        PRISM_model = self.PRISM_model
        self.PRISM_model = ''
        self.PRISM_model = PRISM_model
    
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
                'formula_parameters',
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
#    parameters.load('test/Const/Const_PRISM.params')
    parameters.configure()
                        