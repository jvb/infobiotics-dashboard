from infobiotics.pmodelchecker.pmodelchecker_params import PModelCheckerParams
from enthought.traits.api import Str

class PRISMParams(PModelCheckerParams):

    def __handler_default(self):
        from infobiotics.pmodelchecker.prism.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

#    def _get__preferences_path(self):
#        '''Overrides Params._get__preferences_path'''
#        return 'prism'
    _preferences_path = Str('prism')

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

    def translate_model_specification(self, name):#, object, name, old, new):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from self.model_specification. '''
        self._translated = False
        if self.model_specification == '': return # guard
        from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment # avoids circular import    
        translate = PRISMExperiment(directory=self.directory)
        translate.trait_setq(# set quietly otherwise this triggers _model_specification_changed above
            model_specification=self.model_specification_,
            PRISM_model=self.PRISM_model_, # must set PRISM_model with PRISM_model_ as trait_setq doesn't trigger creation of shadow trait 
            task='Translate',
        ) 
        if translate.perform(thread=False, expecting_no_output=True):
            self._translated = True
#        self._model_specification_changed = True if name == 'model_specification' else False # needed by PModelCheckerParamsHandler.model_specification_changed
        
        

if __name__ == '__main__':
    parameters = PRISMParams()
    parameters.configure()
                        
