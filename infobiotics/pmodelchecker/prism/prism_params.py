from infobiotics.pmodelchecker.api import PModelCheckerParams
from enthought.traits.api import on_trait_change

class PRISMParams(PModelCheckerParams):

    def __handler_default(self):
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


    @on_trait_change('model_specification, PRISM_model')
    def translate_model_specification(self, object, name, old, new):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from self.model_specification. '''
        
        self._translated = False
        if self.model_specification == '': return # guard

#        # can't get here that empty RelativeFiles are erroneous 
#        if hasattr(self, '_PRISM_model_tempfile') and self.PRISM_model_ != self._PRISM_model_tempfile.name:
#            # delete old temporary file
#            del self._PRISM_model_tempfile #TODO may not be enough now that 'delete=False' below
#        
#        if self.PRISM_model == '':
#            # create temporary file
#            self._PRISM_model_tempfile = tempfile.NamedTemporaryFile(suffix='.sm', dir=self.directory, delete=False)
#            self._PRISM_model_tempfile.close()
#            # trigger translation with temporary file
#            if sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 6): 
#                self.trait_set(PRISM_model=os.path.relpath(self._PRISM_model_tempfile.name, self.directory))
#            else:
#                self.trait_set(PRISM_model=self._PRISM_model_tempfile.name)
#            return
            
        from infobiotics.pmodelchecker.prism.api import PRISMExperiment # avoids circular import    
        translate = PRISMExperiment(directory=self.directory)
        translate.trait_setq(# set quietly otherwise this triggers _model_specification_changed above
            model_specification=self.model_specification,
            PRISM_model=self.PRISM_model_, # must set PRISM_model with PRISM_model_ as trait_setq doesn't trigger creation of shadow trait 
            task='Translate',
        ) 
        translate.perform(thread=False)
        self._model_specification_changed = True if name == 'model_specification' else False # needed by PModelCheckerParamsHandler.model_specification_changed
        self._translated = True
        
        

if __name__ == '__main__':
    parameters = PRISMParams()
    parameters.configure()
                        
